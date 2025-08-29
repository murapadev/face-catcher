# Face Catcher 🎭

A Python script that downloads AI-generated face images from thispersondoesnotexist.com and automatically classifies them by age and ethnicity using advanced deep learning models.

## 🌟 Features

- **Image Download**: Downloads n images from thispersondoesnotexist.com
- **Face Analysis**: Uses DeepFace library for accurate age and ethnicity recognition
- **Smart Classification**: Automatically organizes images into folders by age groups and ethnic backgrounds
- **Progress Tracking**: Real-time progress bars and detailed statistics
- **Error Handling**: Robust error handling for network issues and analysis failures
- **Configurable**: Easy configuration through command-line arguments

## 🚀 Quick Start

### Prerequisites

- Python 3.7 to 3.12 (TensorFlow/DeepFace not yet compatible with Python 3.13+)
- pip package manager

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/face-catcher.git
cd face-catcher
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

**Note**: If you encounter TensorFlow installation issues on Python 3.13+, please use Python 3.12 or lower.

### Usage

#### Basic Usage

Download 50 images with automatic classification:

```bash
python face_catcher.py --count 50
```

#### Advanced Usage

```bash
python face_catcher.py --count 100 --output ./my_images --detector retinaface --concurrent 5
```

#### Command Line Arguments

| Argument           | Description                  | Default                   |
| ------------------ | ---------------------------- | ------------------------- |
| `--count, -n`      | Number of images to download | 10                        |
| `--output, -o`     | Output directory             | `./classified_images`     |
| `--detector, -d`   | Face detector backend        | `opencv`                  |
| `--concurrent, -c` | Concurrent downloads         | 3                         |
| `--age-groups`     | Custom age group ranges      | `child,teen,adult,senior` |
| `--verbose, -v`    | Verbose logging              | `False`                   |

### Example Output Structure

```
classified_images/
├── by_age/
│   ├── child_0-12/
│   ├── teen_13-19/
│   ├── adult_20-59/
│   └── senior_60+/
├── by_ethnicity/
│   ├── asian/
│   ├── black/
│   ├── indian/
│   ├── latino_hispanic/
│   ├── middle_eastern/
│   └── white/
├── raw_downloads/
├── analysis_results.json
└── statistics.json
```

## 🧠 Technology Stack

- **DeepFace**: Advanced facial analysis library
- **OpenCV**: Computer vision operations
- **Requests**: HTTP library for downloading images
- **Pillow**: Image processing
- **tqdm**: Progress bars
- **pandas**: Data manipulation

## 📊 Supported Classifications

### Age Groups

- **Child**: 0-12 years
- **Teen**: 13-19 years
- **Adult**: 20-59 years
- **Senior**: 60+ years

### Ethnicity Categories

- Asian
- Black
- Indian
- Latino/Hispanic
- Middle Eastern
- White

## 🎯 Accuracy & Performance

The face analysis is powered by DeepFace, which achieves:

- **Age Estimation**: ~95% accuracy within ±5 years
- **Ethnicity Classification**: ~90% accuracy
- **Face Detection**: 97%+ detection rate with RetinaFace detector

## 🔧 Configuration

### Environment Variables

Create a `.env` file for custom configuration:

```env
# Download settings
DEFAULT_COUNT=50
DEFAULT_OUTPUT_DIR=./classified_images
DEFAULT_CONCURRENT_DOWNLOADS=3

# Analysis settings
DEFAULT_DETECTOR=retinaface

# Logging
LOG_LEVEL=INFO
LOG_FILE=face_catcher.log
```

### Advanced Detector Options

Choose from multiple face detectors based on your needs:

| Detector     | Speed  | Accuracy   | Best For        |
| ------------ | ------ | ---------- | --------------- |
| `opencv`     | ⚡⚡⚡ | ⭐⭐       | Fast processing |
| `ssd`        | ⚡⚡   | ⭐⭐⭐     | Balanced        |
| `mtcnn`      | ⚡     | ⭐⭐⭐⭐   | High accuracy   |
| `retinaface` | ⚡     | ⭐⭐⭐⭐⭐ | Best accuracy   |

## 📈 Usage Examples

### Research & Demographics

```bash
# Download 1000 images for demographic research
python face_catcher.py -n 1000 -d retinaface -c 10 -o ./research_data
```

### Quick Testing

```bash
# Quick test with 20 images
python face_catcher.py -n 20 --verbose
```

### Custom Age Groups

```bash
# Use custom age group definitions
python face_catcher.py -n 100 --age-groups "baby,child,adult,elderly"
```

## 🛠️ Development

### Project Structure

```
face-catcher/
├── face_catcher.py          # Main application
├── src/
│   ├── downloader.py        # Image download logic
│   ├── analyzer.py          # Face analysis logic
│   ├── classifier.py        # Image classification
│   └── utils.py             # Utility functions
├── tests/
│   ├── test_downloader.py
│   ├── test_analyzer.py
│   └── test_classifier.py
├── requirements.txt
├── .env.example
└── README.md
```

### Running Tests

```bash
python -m pytest tests/ -v
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## ⚠️ Important Notes

### Ethical Considerations

- These are AI-generated faces, not real people
- Use responsibly and in compliance with your local laws
- Respect rate limits of thispersondoesnotexist.com
- Consider the ethical implications of facial analysis technology

### Limitations

- Analysis accuracy depends on image quality
- Some edge cases may be misclassified
- Network connectivity required for downloads
- Large downloads may take significant time

### Privacy & Security

- No personal data is collected or stored
- All processing happens locally
- Images are synthetic, not real people
- No external APIs beyond image download

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ImportError: No module named 'cv2'`

```bash
pip install opencv-python
```

**Issue**: DeepFace model download fails

```bash
# Clear cache and retry
rm -rf ~/.deepface
python face_catcher.py -n 1
```

**Issue**: Too many requests error

```bash
# Reduce concurrent downloads
python face_catcher.py -n 100 -c 1
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ThisPersonDoesNotExist.com](https://thispersondoesnotexist.com/) for providing AI-generated faces
- [DeepFace](https://github.com/serengil/deepface) for the facial analysis framework
- [StyleGAN2](https://github.com/NVlabs/stylegan2) for the underlying GAN technology

## 📞 Support

- 🐛 [Report Bug](https://github.com/yourusername/face-catcher/issues)
- 💡 [Request Feature](https://github.com/yourusername/face-catcher/issues)
- 📖 [Documentation](https://github.com/yourusername/face-catcher/wiki)

---

⭐ **Star this repository if you find it useful!** ⭐
