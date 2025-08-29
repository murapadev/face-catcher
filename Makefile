# Face Catcher Makefile

.PHONY: help install test clean run example lint format

# Default target
help:
	@echo "Face Catcher - Available commands:"
	@echo ""
	@echo "  install     Install dependencies"
	@echo "  test        Run installation tests"
	@echo "  test-quick  Quick test with 5 images"
	@echo "  test-full   Full test with 20 images"
	@echo "  example     Run example script"
	@echo "  clean       Clean generated files"
	@echo "  lint        Run code linting"
	@echo "  format      Format code"
	@echo "  setup       Setup development environment"
	@echo ""

# Install dependencies
install:
	pip install -r requirements.txt

# Run installation test
test:
	python tests/test_installation.py

# Quick test with 5 images
test-quick:
	python face_catcher.py --count 5 --output ./test_output --verbose

# Full test with 20 images
test-full:
	python face_catcher.py --count 20 --output ./test_output --detector retinaface --verbose

# Run example
example:
	python example.py

# Clean generated files
clean:
	rm -rf test_output/
	rm -rf example_output/
	rm -rf classified_images/
	rm -rf downloads/
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "*.log" -delete

# Setup development environment
setup: install
	@echo "Setting up Face Catcher development environment..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file"; fi
	@echo "Development environment ready!"

# Code formatting (if black is installed)
format:
	@if command -v black >/dev/null 2>&1; then \
		black face_catcher.py src/ tests/ example.py; \
		echo "Code formatted with black"; \
	else \
		echo "black not installed. Install with: pip install black"; \
	fi

# Code linting (if flake8 is installed)
lint:
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 face_catcher.py src/ tests/ example.py; \
		echo "Linting completed"; \
	else \
		echo "flake8 not installed. Install with: pip install flake8"; \
	fi

# Show project status
status:
	@echo "Face Catcher Project Status"
	@echo "=========================="
	@echo "Python version: $$(python --version)"
	@echo "Working directory: $$(pwd)"
	@echo "Dependencies status:"
	@python -c "import sys; modules=['requests','numpy','pandas','tqdm','cv2','deepface']; [print(f'  {m}: ✅') if __import__(m) else print(f'  {m}: ❌') for m in modules]" 2>/dev/null || echo "  Some dependencies missing"
	@echo ""
	@if [ -d "classified_images" ]; then echo "Output directory exists: classified_images/"; fi
	@if [ -f ".env" ]; then echo "Configuration file exists: .env"; fi
