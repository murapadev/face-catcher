"""
Image downloader module for Face Catcher.
Handles downloading images from thispersondoesnotexist.com
"""

import os
import time
import logging
import requests
from pathlib import Path
from typing import Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .utils import validate_image


class ImageDownloader:
    """Handles downloading images from thispersondoesnotexist.com"""
    
    def __init__(self, config: Dict):
        """
        Initialize the image downloader.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.output_dir = Path(config['output_dir']) / 'raw_downloads'
        self.download_url = config['download_url']
        self.concurrent_downloads = config['concurrent_downloads']
        self.timeout = config['request_timeout']
        self.retry_attempts = config['retry_attempts']
        self.user_agent = config['user_agent']
        
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        
        # Statistics
        self.stats = {
            'successful': 0,
            'failed': 0,
            'total_bytes': 0
        }
    
    def download_single_image(self, image_number: int) -> Dict:
        """
        Download a single image from thispersondoesnotexist.com
        
        Args:
            image_number: Image number for naming
            
        Returns:
            Dictionary with download result
        """
        filename = f"face_{image_number:06d}.jpg"
        filepath = self.output_dir / filename
        
        for attempt in range(self.retry_attempts):
            try:
                # Make request
                response = self.session.get(
                    self.download_url,
                    timeout=self.timeout,
                    stream=True
                )
                response.raise_for_status()
                
                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'image' not in content_type:
                    self.logger.warning(f"Unexpected content type: {content_type}")
                    continue
                
                # Download image data
                image_data = response.content
                
                # Save image
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                # Validate image
                if not validate_image(filepath):
                    filepath.unlink()  # Remove invalid file
                    return {
                        'success': False,
                        'reason': 'invalid_image',
                        'filename': filename,
                        'bytes': 0
                    }
                
                # Success
                file_size = len(image_data)
                return {
                    'success': True,
                    'filename': filename,
                    'filepath': filepath,
                    'bytes': file_size
                }
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Download attempt {attempt + 1} failed for {filename}: {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                continue
            except Exception as e:
                self.logger.error(f"Unexpected error downloading {filename}: {e}")
                break
        
        # All attempts failed
        return {
            'success': False,
            'reason': 'download_failed',
            'filename': filename,
            'bytes': 0
        }
    
    def download_images(self, count: int) -> Dict:
        """
        Download multiple images concurrently.
        
        Args:
            count: Number of images to download
            
        Returns:
            Dictionary with download statistics
        """
        self.logger.info(f"Starting download of {count} images...")
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Progress bar
        with tqdm(total=count, desc="Downloading images", unit="img") as pbar:
            # Use ThreadPoolExecutor for concurrent downloads
            with ThreadPoolExecutor(max_workers=self.concurrent_downloads) as executor:
                # Submit all download tasks
                future_to_number = {
                    executor.submit(self.download_single_image, i): i 
                    for i in range(1, count + 1)
                }
                
                # Process completed downloads
                for future in as_completed(future_to_number):
                    result = future.result()
                    
                    if result['success']:
                        self.stats['successful'] += 1
                        self.stats['total_bytes'] += result['bytes']
                        pbar.set_postfix({
                            'Success': self.stats['successful'],
                            'Failed': self.stats['failed']
                        })
                    else:
                        self.stats['failed'] += 1
                        self.logger.warning(f"Failed to download {result['filename']}: {result['reason']}")
                    
                    pbar.update(1)
        
        # Log summary
        self.logger.info(
            f"Download complete: {self.stats['successful']} successful, "
            f"{self.stats['failed']} failed"
        )
        
        return self.stats
    
    def get_stats(self) -> Dict:
        """Get download statistics."""
        return self.stats.copy()
