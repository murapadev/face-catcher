"""
Face Catcher - AI Face Downloader and Classifier

This script downloads AI-generated face images from thispersondoesnotexist.com
and classifies them by age and ethnicity using DeepFace library.

Author: Pablo
Date: June 2025
License: MIT
"""

import argparse
import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.downloader import ImageDownloader
from src.analyzer import FaceAnalyzer
from src.classifier import ImageClassifier
from src.utils import setup_logging, load_config, create_directory_structure


class FaceCatcher:
    """Main class for the Face Catcher application."""
    
    def __init__(self, config: Dict):
        """
        Initialize the Face Catcher with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.output_dir = Path(config['output_dir'])
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.downloader = ImageDownloader(config)
        self.analyzer = FaceAnalyzer(config)
        self.classifier = ImageClassifier(config)
        
        # Create directory structure
        create_directory_structure(self.output_dir)
        
        self.logger.info(f"Face Catcher initialized with output directory: {self.output_dir}")
    
    def run(self, count: int) -> Dict:
        """
        Main execution method.
        
        Args:
            count: Number of images to download and process
            
        Returns:
            Dictionary with execution statistics
        """
        self.logger.info(f"Starting Face Catcher - downloading {count} images")
        
        statistics = {
            'total_requested': count,
            'downloaded': 0,
            'analyzed': 0,
            'classified': 0,
            'failed_downloads': 0,
            'failed_analysis': 0,
            'age_distribution': {},
            'ethnicity_distribution': {}
        }
        
        try:
            # Step 1: Download images
            self.logger.info("Phase 1: Downloading images...")
            download_results = self.downloader.download_images(count)
            statistics.update({
                'downloaded': download_results['successful'],
                'failed_downloads': download_results['failed']
            })
            
            # Step 2: Analyze faces
            self.logger.info("Phase 2: Analyzing faces...")
            raw_images_dir = self.output_dir / 'raw_downloads'
            image_files = list(raw_images_dir.glob('*.jpg'))
            
            analysis_results = []
            for image_file in image_files:
                try:
                    result = self.analyzer.analyze_face(str(image_file))
                    if result:
                        analysis_results.append({
                            'file': image_file,
                            'analysis': result
                        })
                        statistics['analyzed'] += 1
                    else:
                        statistics['failed_analysis'] += 1
                        self.logger.warning(f"Failed to analyze: {image_file.name}")
                except Exception as e:
                    statistics['failed_analysis'] += 1
                    self.logger.error(f"Error analyzing {image_file.name}: {e}")
            
            # Step 3: Classify and organize images
            self.logger.info("Phase 3: Classifying and organizing images...")
            for result in analysis_results:
                try:
                    self.classifier.classify_and_move(
                        result['file'], 
                        result['analysis']
                    )
                    statistics['classified'] += 1
                    
                    # Update distribution statistics
                    age = result['analysis'].get('age', 'unknown')
                    race = result['analysis'].get('dominant_race', 'unknown')
                    
                    age_group = self.classifier.get_age_group(age)
                    if age_group not in statistics['age_distribution']:
                        statistics['age_distribution'][age_group] = 0
                    statistics['age_distribution'][age_group] += 1
                    
                    if race not in statistics['ethnicity_distribution']:
                        statistics['ethnicity_distribution'][race] = 0
                    statistics['ethnicity_distribution'][race] += 1
                    
                except Exception as e:
                    self.logger.error(f"Error classifying {result['file'].name}: {e}")
            
            # Save results
            self.classifier.save_analysis_results(analysis_results, statistics)
            
            self.logger.info("Face Catcher execution completed successfully!")
            self._print_summary(statistics)
            
            return statistics
            
        except Exception as e:
            self.logger.error(f"Fatal error during execution: {e}")
            raise
    
    def _print_summary(self, stats: Dict):
        """Print execution summary."""
        print("\n" + "="*60)
        print("📊 FACE CATCHER - EXECUTION SUMMARY")
        print("="*60)
        print(f"📥 Images requested: {stats['total_requested']}")
        print(f"✅ Successfully downloaded: {stats['downloaded']}")
        print(f"🔍 Successfully analyzed: {stats['analyzed']}")
        print(f"📁 Successfully classified: {stats['classified']}")
        print(f"❌ Failed downloads: {stats['failed_downloads']}")
        print(f"❌ Failed analysis: {stats['failed_analysis']}")
        
        if stats['age_distribution']:
            print(f"\n👶 Age Distribution:")
            for age_group, count in stats['age_distribution'].items():
                percentage = (count / stats['analyzed']) * 100 if stats['analyzed'] > 0 else 0
                print(f"  {age_group}: {count} ({percentage:.1f}%)")
        
        if stats['ethnicity_distribution']:
            print(f"\n🌍 Ethnicity Distribution:")
            for ethnicity, count in stats['ethnicity_distribution'].items():
                percentage = (count / stats['analyzed']) * 100 if stats['analyzed'] > 0 else 0
                print(f"  {ethnicity}: {count} ({percentage:.1f}%)")
        
        print(f"\n📂 Output directory: {self.output_dir}")
        print("="*60)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Face Catcher - Download and classify AI-generated faces",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python face_catcher.py --count 50
  python face_catcher.py -n 100 -o ./my_images -d retinaface
  python face_catcher.py -n 20 --verbose --concurrent 5
        """
    )
    
    parser.add_argument(
        '--count', '-n',
        type=int,
        default=10,
        help='Number of images to download (default: 10)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='./classified_images',
        help='Output directory (default: ./classified_images)'
    )
    
    parser.add_argument(
        '--detector', '-d',
        type=str,
        default='opencv',
        choices=['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe'],
        help='Face detector backend (default: opencv)'
    )
    
    parser.add_argument(
        '--concurrent', '-c',
        type=int,
        default=3,
        help='Number of concurrent downloads (default: 3)'
    )
    
    parser.add_argument(
        '--age-groups',
        type=str,
        default='child,teen,adult,senior',
        help='Comma-separated age group names (default: child,teen,adult,senior)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging (default: False)'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Setup logging
        log_level = logging.DEBUG if args.verbose else logging.INFO
        setup_logging(log_level)
        
        # Load configuration
        config = load_config()
        
        # Handle age groups - convert command line argument to proper dictionary format
        if args.age_groups != 'child,teen,adult,senior':
            # Custom age groups provided - use default ranges but with custom names
            age_group_names = args.age_groups.split(',')
            if len(age_group_names) == 4:
                config['age_groups'] = {
                    age_group_names[0]: (0, 12),
                    age_group_names[1]: (13, 19), 
                    age_group_names[2]: (20, 59),
                    age_group_names[3]: (60, 100)
                }
            else:
                print(f"⚠️  Warning: Expected 4 age groups, got {len(age_group_names)}. Using defaults.")
        
        # Override config with command line arguments
        config.update({
            'output_dir': args.output,
            'detector_backend': args.detector,
            'concurrent_downloads': args.concurrent,
            'verbose': args.verbose
        })
        
        # Validate count
        if args.count <= 0:
            print("❌ Error: Count must be greater than 0")
            sys.exit(1)
        
        if args.count > 1000:
            response = input(f"⚠️  You're about to download {args.count} images. This may take a while. Continue? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Operation cancelled.")
                sys.exit(0)
        
        # Initialize and run Face Catcher
        face_catcher = FaceCatcher(config)
        statistics = face_catcher.run(args.count)
        
        print(f"\n🎉 Face Catcher completed successfully!")
        print(f"📂 Check your results in: {config['output_dir']}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
