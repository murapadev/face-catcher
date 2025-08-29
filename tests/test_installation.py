"""
Test script for Face Catcher
Run this to verify the installation and dependencies
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError:
        print("❌ requests not found. Install with: pip install requests")
        return False
    
    try:
        import numpy
        print("✅ numpy imported successfully")
    except ImportError:
        print("❌ numpy not found. Install with: pip install numpy")
        return False
    
    try:
        import pandas
        print("✅ pandas imported successfully")
    except ImportError:
        print("❌ pandas not found. Install with: pip install pandas")
        return False
    
    try:
        import tqdm
        print("✅ tqdm imported successfully")
    except ImportError:
        print("❌ tqdm not found. Install with: pip install tqdm")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError:
        print("❌ Pillow not found. Install with: pip install Pillow")
        return False
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError:
        print("❌ OpenCV not found. Install with: pip install opencv-python")
        return False
    
    try:
        from deepface import DeepFace
        print("✅ DeepFace imported successfully")
    except ImportError:
        print("❌ DeepFace not found. Install with: pip install deepface")
        return False
    
    return True

def test_face_catcher_modules():
    """Test that Face Catcher modules can be imported."""
    print("\nTesting Face Catcher modules...")
    
    try:
        from src.utils import setup_logging, load_config
        print("✅ utils module imported successfully")
    except ImportError as e:
        print(f"❌ utils module import failed: {e}")
        return False
    
    try:
        from src.downloader import ImageDownloader
        print("✅ downloader module imported successfully")
    except ImportError as e:
        print(f"❌ downloader module import failed: {e}")
        return False
    
    try:
        from src.analyzer import FaceAnalyzer
        print("✅ analyzer module imported successfully")
    except ImportError as e:
        print(f"❌ analyzer module import failed: {e}")
        return False
    
    try:
        from src.classifier import ImageClassifier
        print("✅ classifier module imported successfully")
    except ImportError as e:
        print(f"❌ classifier module import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from src.utils import load_config
        config = load_config()
        print("✅ Configuration loaded successfully")
        print(f"   Output directory: {config['output_dir']}")
        print(f"   Detector backend: {config['detector_backend']}")
        print(f"   Concurrent downloads: {config['concurrent_downloads']}")
        return True
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def test_internet_connection():
    """Test internet connection to thispersondoesnotexist.com"""
    print("\nTesting internet connection...")
    
    try:
        import requests
        response = requests.get("https://thispersondoesnotexist.com/", timeout=10)
        if response.status_code == 200:
            print("✅ Internet connection to thispersondoesnotexist.com working")
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Internet connection test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("FACE CATCHER - INSTALLATION TEST")
    print("="*60)
    
    tests = [
        test_imports,
        test_face_catcher_modules,
        test_configuration,
        test_internet_connection
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All tests passed! ({passed}/{total})")
        print("Face Catcher is ready to use.")
        print("\nTry running: python face_catcher.py --count 5")
    else:
        print(f"❌ Some tests failed ({passed}/{total})")
        print("Please install missing dependencies and try again.")
        print("\nInstall all dependencies with: pip install -r requirements.txt")
    
    print("="*60)

if __name__ == "__main__":
    main()
