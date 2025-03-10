# Image Processor API Reference

This document provides detailed information about the Image Processor API.

## ImageProcessor Class

The main class for processing images.

```python
from image_processor.transformations.processor import ImageProcessor
```

### Constructor

```python
ImageProcessor(
    input_dir: str, 
    output_dir: str,
    workers: int = 1
)
```

- `input_dir`: Directory containing input images
- `output_dir`: Directory for processed images
- `workers`: Number of worker processes for parallel processing (default: 1)

### Methods

#### process_images

```python
process_images(
    resize_dimensions: Optional[Tuple[int, int]] = (800, 600),
    blur_radius: float = 1.0,
    sharpen_factor: float = 1.5,
    contrast_factor: float = 1.2,
    brightness_factor: float = 1.1,
    output_format: Optional[str] = None
) -> Dict[str, Any]
```

Process all images in the input directory with the specified transformations.

- `resize_dimensions`: Target width and height for resizing
- `blur_radius`: Radius for Gaussian blur
- `sharpen_factor`: Factor for sharpening
- `contrast_factor`: Factor for contrast adjustment
- `brightness_factor`: Factor for brightness adjustment
- `output_format`: Optional output format (e.g., "JPEG", "PNG", "WebP")

Returns a dictionary with processing statistics:
```python
{
    "processed_count": int,  # Number of successfully processed images
    "error_count": int,      # Number of images that failed to process
    "processing_time": float,  # Total processing time in seconds
    "avg_time_per_image": float  # Average processing time per image
}
```

#### process_single_image

```python
process_single_image(
    input_path: str,
    output_path: str,
    resize_dimensions: Optional[Tuple[int, int]] = (800, 600),
    blur_radius: float = 1.0,
    sharpen_factor: float = 1.5,
    contrast_factor: float = 1.2,
    brightness_factor: float = 1.1,
    output_format: Optional[str] = None
) -> bool
```

Process a single image with the specified transformations.

- `input_path`: Path to the input image
- `output_path`: Path to save the processed image
- Other parameters are the same as `process_images`

Returns `True` if processing was successful, `False` otherwise.

## Logger Setup

Utility function to configure logging.

```python
from image_processor.logger import setup_logger
```

### setup_logger

```python
setup_logger(
    log_level: str = "INFO", 
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger
```

Configure logging for the application.

- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_file`: Optional file path to write logs to
- `log_format`: Optional custom log format string

Returns the configured logger instance.

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

## Configuration

```python
from image_processor.config import Config
```

### Config Class

```python
Config(config_file: Optional[str] = None)
```

Load and manage configuration settings.

- `config_file`: Optional path to a configuration file

#### Methods

```python
get(key: str, default: Any = None) -> Any
```

Get a configuration value.

- `key`: Configuration key
- `default`: Default value if key is not found
- Returns: Configuration value

```python
set(key: str, value: Any) -> None
```

Set a configuration value.

- `key`: Configuration key
- `value`: Configuration value

```python
save(config_file: Optional[str] = None) -> None
```

Save configuration to a file.

- `config_file`: Optional path to save the configuration file