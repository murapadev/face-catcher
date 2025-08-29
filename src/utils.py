"""
Utility functions for Face Catcher application.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None):
    """
    Setup logging configuration.
    
    Args:
        level: Logging level
        log_file: Optional log file path
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    
    # Setup file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables and defaults.
    
    Returns:
        Configuration dictionary
    """
    # Load .env file if it exists
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv(env_file)
    
    return {
        'output_dir': os.getenv('DEFAULT_OUTPUT_DIR', './classified_images'),
        'concurrent_downloads': int(os.getenv('DEFAULT_CONCURRENT_DOWNLOADS', '3')),
        'detector_backend': os.getenv('DEFAULT_DETECTOR', 'opencv'),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'log_file': os.getenv('LOG_FILE', None),
        'download_url': 'https://thispersondoesnotexist.com/',
        'request_timeout': 30,
        'retry_attempts': 3,
        'user_agent': 'Face-Catcher/1.0',
        'age_groups': {
            'child': (0, 12),
            'teen': (13, 19),
            'adult': (20, 59),
            'senior': (60, 100)
        }
    }


def create_directory_structure(base_dir: Path):
    """
    Create the directory structure for organizing images.
    
    Args:
        base_dir: Base directory path
    """
    directories = [
        base_dir,
        base_dir / 'raw_downloads',
        base_dir / 'by_age' / 'child_0-12',
        base_dir / 'by_age' / 'teen_13-19',
        base_dir / 'by_age' / 'adult_20-59',
        base_dir / 'by_age' / 'senior_60+',
        base_dir / 'by_ethnicity' / 'asian',
        base_dir / 'by_ethnicity' / 'black',
        base_dir / 'by_ethnicity' / 'indian',
        base_dir / 'by_ethnicity' / 'latino_hispanic',
        base_dir / 'by_ethnicity' / 'middle_eastern',
        base_dir / 'by_ethnicity' / 'white',
        base_dir / 'logs'
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def save_json(data: Any, file_path: Path):
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        file_path: File path
    """
    import numpy as np
    
    def convert_numpy_types(obj):
        """Convert numpy types to native Python types for JSON serialization."""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(item) for item in obj]
        return obj
    
    # Convert numpy types to native Python types
    data = convert_numpy_types(data)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(file_path: Path) -> Dict:
    """
    Load data from JSON file.
    
    Args:
        file_path: File path
        
    Returns:
        Loaded data dictionary
    """
    if not file_path.exists():
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_bytes(bytes_value: float) -> str:
    """
    Format bytes to human readable string.
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} TB"


def validate_image(file_path: Path) -> bool:
    """
    Validate if file is a valid image.
    
    Args:
        file_path: Path to image file
        
    Returns:
        True if valid image, False otherwise
    """
    try:
        from PIL import Image
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False
