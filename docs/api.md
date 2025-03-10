# Image Processor API Reference

This document provides detailed information about the Image Processor API.

## ImageProcessor Class

The main class for processing images.

```python
from image_processor.transformations.processor import ImageProcessor
```

### Constructor

```python
ImageProcessor(input_dir: str, output_dir: str)
```

- `input_dir`: Directory containing input images
- `output_dir`: Directory for processed images

### Methods

#### process_images

```python
process_images(
    resize_dimensions: Optional[Tuple[int, int]] = (800, 600),
    blur_radius: float = 1.0,
    sharpen_factor: float = 1.5,
    contrast_factor: float = 1.2,
    brightness_factor: float = 1.1
)
```

Process all images in the input directory with the specified transformations.

- `resize_dimensions`: Target width and height for resizing
- `blur_radius`: Radius for Gaussian blur
- `sharpen_factor`: Factor for sharpening
- `contrast_factor`: Factor for contrast adjustment
- `brightness_factor`: Factor for brightness adjustment

## Logger Setup

Utility function to configure logging.

```python
from image_processor.utils.logger import setup_logger
```

### setup_logger

```python
setup_logger(log_level: str = "INFO", log_file: Optional[str] = None)
```

Configure logging for the application.

- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_file`: Optional file path to write logs to

## Command Line Interface

The command-line interface is implemented in the `cli` module.

```python
from image_processor.cli import main
```

### main

```python
main(args: Optional[List[str]] = None) -> int
```

Main entry point for the command-line interface.

- `args`: Command line arguments (defaults to sys.argv[1:])
- Returns: Exit code (0 for success, non-zero for failure)

### parse_args

```python
parse_args(args: Optional[List[str]] = None) -> argparse.Namespace
```

Parse command line arguments.

- `args`: Command line arguments (defaults to sys.argv[1:])
- Returns: Parsed arguments

### validate_args

```python
validate_args(args: argparse.Namespace) -> bool
```

Validate command line arguments.

- `args`: Parsed arguments
- Returns: True if arguments are valid, False otherwise