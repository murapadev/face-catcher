#!/usr/bin/env python3
"""
Face Catcher - Quick Start Example

This script demonstrates basic usage of Face Catcher
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Run a quick example."""
    print("Face Catcher - Quick Start Example")
    print("=" * 40)
    
    # Import Face Catcher
    try:
        from face_catcher import FaceCatcher
        from src.utils import load_config
    except ImportError as e:
        print(f"Error importing Face Catcher: {e}")
        print("Make sure all dependencies are installed.")
        print("Run: pip install -r requirements.txt")
        return
    
    # Load configuration
    config = load_config()
    config['output_dir'] = './example_output'
    
    # Create Face Catcher instance
    face_catcher = FaceCatcher(config)
    
    # Download and analyze 5 images
    print("Downloading and analyzing 5 images...")
    try:
        statistics = face_catcher.run(5)
        print("\nExample completed successfully!")
        print(f"Check results in: {config['output_dir']}")
    except Exception as e:
        print(f"Error running example: {e}")

if __name__ == "__main__":
    main()
