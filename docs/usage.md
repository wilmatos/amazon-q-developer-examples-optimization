# Image Processor Usage Guide

This document provides detailed instructions on how to use the Image Processor package.

## Installation

Install the package from the source directory:

```bash
pip install .
```

## Command Line Interface

The Image Processor provides a command-line interface for easy use:

```bash
image-processor -i /path/to/input/dir -o /path/to/output/dir [options]
```

### Required Arguments

- `-i, --input-dir`: Directory containing input images
- `-o, --output-dir`: Directory for processed images

### Optional Arguments

- `--resize width,height`: Resize dimensions (default: 800,600)
- `--blur radius`: Blur radius (default: 1.0)
- `--sharpen factor`: Sharpen factor (default: 1.5)
- `--contrast factor`: Contrast adjustment (default: 1.2)
- `--brightness factor`: Brightness adjustment (default: 1.1)
- `--log-level`: Logging level (default: INFO)
- `--log-file`: Optional log file path

### Examples

Basic usage:
```bash
image-processor -i ./input_images -o ./output_images
```

Custom transformations:
```bash
image-processor -i ./input_images -o ./output_images --resize 1024,768 --blur 2.0 --contrast 1.5
```

With logging to file:
```bash
image-processor -i ./input_images -o ./output_images --log-level DEBUG --log-file processor.log
```

## Python API

You can also use the Image Processor as a Python library:

```python
from image_processor.transformations.processor import ImageProcessor
from image_processor.utils.logger import setup_logger

# Setup logging (optional)
setup_logger(log_level="INFO", log_file="processor.log")

# Initialize processor
processor = ImageProcessor(input_dir="./input_images", output_dir="./output_images")

# Process images with default parameters
processor.process_images()

# Or with custom parameters
processor.process_images(
    resize_dimensions=(1024, 768),
    blur_radius=2.0,
    sharpen_factor=1.8,
    contrast_factor=1.5,
    brightness_factor=1.2
)
```

## Supported Image Formats

The Image Processor supports the following image formats:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)

## Error Handling

The Image Processor includes robust error handling:
- Invalid input directory: The application will exit with an error message
- Invalid image files: The application will log an error and continue processing other images
- Invalid parameters: The application will validate parameters and exit with an error message if they are invalid

All errors are logged to the console and optionally to a log file.