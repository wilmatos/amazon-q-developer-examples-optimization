# Image Processor

A Python package for applying various image transformations. This implementation is intentionally inefficient to demonstrate optimization opportunities.

## Features

- Process multiple images in batch
- Apply various transformations:
  - Resize
  - Blur
  - Sharpen
  - Contrast adjustment
  - Brightness adjustment
- Command-line interface
- Configurable logging
- Error handling

## Installation

```bash
pip install .
```

## Usage

### Command Line Interface

```bash
image-processor -i /path/to/input/dir -o /path/to/output/dir [options]
```

Options:
- `--resize width,height`: Resize dimensions (default: 800,600)
- `--blur radius`: Blur radius (default: 1.0)
- `--sharpen factor`: Sharpen factor (default: 1.5)
- `--contrast factor`: Contrast adjustment (default: 1.2)
- `--brightness factor`: Brightness adjustment (default: 1.1)
- `--log-level`: Logging level (default: INFO)
- `--log-file`: Optional log file path

### Python API

```python
from image_processor.transformations.processor import ImageProcessor

# Initialize processor
processor = ImageProcessor(input_dir="/path/to/input", output_dir="/path/to/output")

# Process images with custom parameters
processor.process_images(
    resize_dimensions=(800, 600),
    blur_radius=1.0,
    sharpen_factor=1.5,
    contrast_factor=1.2,
    brightness_factor=1.1
)
```

## Known Inefficiencies

This implementation has several intentional inefficiencies:
1. Images are loaded and saved multiple times during processing
2. No parallel processing
3. No image format optimization
4. No caching of intermediate results
5. No batch processing of transformations

These inefficiencies will be addressed in future optimizations.

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## License

MIT License