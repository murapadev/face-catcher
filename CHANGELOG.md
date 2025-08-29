# Changelog

All notable changes to Face Catcher will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-06-13

### Removed

- **Duplicate Detection**: Removed MD5 checksum-based duplicate detection to simplify downloads
- **--skip-duplicates argument**: No longer available in command line interface
- **ENABLE_DUPLICATE_CHECK**: Removed from configuration options

### Changed

- Downloads now always save all images without checking for duplicates
- Improved download performance by removing hash calculations
- Simplified statistics reporting (removed duplicate counts)

## [1.0.0] - 2025-06-13

### Added

- Initial release of Face Catcher
- Image downloading from thispersondoesnotexist.com
- Face analysis using DeepFace library
- Age and ethnicity classification
- Automatic image organization by age groups and ethnicities
- Concurrent downloading for improved performance
- Progress tracking with tqdm progress bars
- Comprehensive error handling and logging
- Command-line interface with multiple options
- JSON export of analysis results and statistics
- Multiple face detector backends support
- Configurable age group definitions
- Detailed documentation and examples

### Features

- **Age Classification**: Child (0-12), Teen (13-19), Adult (20-59), Senior (60+)
- **Ethnicity Classification**: Asian, Black, Indian, Latino/Hispanic, Middle Eastern, White
- **Face Detectors**: OpenCV, SSD, DLIB, MTCNN, RetinaFace, MediaPipe
- **Output Formats**: Organized directories, JSON analysis results, statistics
- **Performance**: Concurrent downloads, progress tracking, error recovery

### Technical Details

- Python 3.7+ compatibility
- DeepFace integration for facial analysis
- OpenCV for image processing
- Requests for HTTP downloading
- Threading for concurrent operations
- Comprehensive test suite
- Modular architecture with separate components

### Documentation

- Complete README with usage examples
- Installation instructions
- Configuration options
- Troubleshooting guide
- API documentation
- Example scripts
