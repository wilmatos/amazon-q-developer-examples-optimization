# Image Processor Usage Guide

This document provides detailed instructions on how to use the Image Processor package.

## Installation

Install the package from the source directory:

```bash
# Basic installation
pip install .

# Development installation
pip install -e ".[dev]"

# With optional dependencies
pip install ".[all]"
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
- `--workers`: Number of worker processes (default: 1)
- `--format`: Output image format (default: same as input)
- `--config`: Path to configuration file
- `--dry-run`: Show what would be done without actually processing images

### Examples

Basic usage:
```bash
image-processor -i ./input_images -o ./output_images
```

Custom transformations:
```bash
image-processor -i ./input_images -o ./output_images --resize 1024,768 --blur 2.0 --contrast 1.5
```

With parallel processing:
```bash
image-processor -i ./input_images -o ./output_images --workers 4
```

With specific output format:
```bash
image-processor -i ./input_images -o ./output_images --format webp
```

With logging to file:
```bash
image-processor -i ./input_images -o ./output_images --log-level DEBUG --log-file processor.log
```

Using a configuration file:
```bash
image-processor --config my_config.json
```

## Python API

You can also use the Image Processor as a Python library:

```python
from image_processor.transformations.processor import ImageProcessor
from image_processor.logger import setup_logger

# Setup logging (optional)
logger = setup_logger(log_level="INFO", log_file="processor.log")

# Initialize processor with parallel processing
processor = ImageProcessor(
    input_dir="./input_images", 
    output_dir="./output_images",
    workers=4  # Use 4 worker processes
)

# Process images with default parameters
result = processor.process_images()
logger.info(f"Processed {result['processed_count']} images in {result['processing_time']:.2f} seconds")

# Or with custom parameters
result = processor.process_images(
    resize_dimensions=(1024, 768),
    blur_radius=2.0,
    sharpen_factor=1.8,
    contrast_factor=1.5,
    brightness_factor=1.2,
    output_format="WebP"  # Convert all images to WebP format
)

# Process a single image
success = processor.process_single_image(
    input_path="input.jpg",
    output_path="output.webp",
    resize_dimensions=(1024, 768),
    output_format="WebP"
)
```

## Configuration File

You can use a JSON configuration file to store processing parameters:

```json
{
  "input_dir": "./input_images",
  "output_dir": "./output_images",
  "workers": 4,
  "transformations": {
    "resize_dimensions": [1024, 768],
    "blur_radius": 2.0,
    "sharpen_factor": 1.8,
    "contrast_factor": 1.5,
    "brightness_factor": 1.2
  },
  "output_format": "WebP",
  "logging": {
    "level": "INFO",
    "file": "processor.log"
  }
}
```

Load the configuration in your Python code:

```python
from image_processor.config import Config
from image_processor.transformations.processor import ImageProcessor

config = Config("config.json")
processor = ImageProcessor(
    input_dir=config.get("input_dir"),
    output_dir=config.get("output_dir"),
    workers=config.get("workers", 1)
)

transformations = config.get("transformations", {})
processor.process_images(
    resize_dimensions=transformations.get("resize_dimensions", (800, 600)),
    blur_radius=transformations.get("blur_radius", 1.0),
    sharpen_factor=transformations.get("sharpen_factor", 1.5),
    contrast_factor=transformations.get("contrast_factor", 1.2),
    brightness_factor=transformations.get("brightness_factor", 1.1),
    output_format=config.get("output_format")
)
```

## Supported Image Formats

The Image Processor supports the following image formats:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)
- AVIF (.avif) - requires additional dependencies

## Error Handling

The Image Processor includes robust error handling:
- Invalid input directory: The application will exit with an error message
- Invalid image files: The application will log an error and continue processing other images
- Invalid parameters: The application will validate parameters and exit with an error message if they are invalid
- Processing errors: Individual image processing errors are caught and logged

All errors are logged to the console and optionally to a log file.

## Performance Considerations

- For large batches of images, use parallel processing with the `--workers` option
- For memory-constrained environments, process images in smaller batches
- For web delivery, consider using WebP or AVIF output formats
- Monitor memory usage when processing very large images