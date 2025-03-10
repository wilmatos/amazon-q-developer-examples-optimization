"""
Command-line interface for the image processor.
"""

import argparse
import logging
import os
import sys
from typing import List, Optional, Tuple

from image_processor.transformations.processor import ImageProcessor
from image_processor.utils.logger import setup_logger

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Process images with various transformations",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-i", "--input-dir",
        required=True,
        help="Directory containing input images"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        required=True,
        help="Directory for processed images"
    )
    
    parser.add_argument(
        "--resize",
        type=lambda s: tuple(map(int, s.split(','))),
        default="800,600",
        help="Resize dimensions as width,height"
    )
    
    parser.add_argument(
        "--blur",
        type=float,
        default=1.0,
        help="Blur radius"
    )
    
    parser.add_argument(
        "--sharpen",
        type=float,
        default=1.5,
        help="Sharpen factor"
    )
    
    parser.add_argument(
        "--contrast",
        type=float,
        default=1.2,
        help="Contrast adjustment factor"
    )
    
    parser.add_argument(
        "--brightness",
        type=float,
        default=1.1,
        help="Brightness adjustment factor"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level"
    )
    
    parser.add_argument(
        "--log-file",
        help="Log file path (if not specified, logs to console only)"
    )
    
    return parser.parse_args(args)

def validate_args(args: argparse.Namespace) -> bool:
    """
    Validate command line arguments.
    
    Args:
        args: Parsed arguments
        
    Returns:
        True if arguments are valid, False otherwise
    """
    # Check if input directory exists
    if not os.path.isdir(args.input_dir):
        logging.error(f"Input directory does not exist: {args.input_dir}")
        return False
    
    # Check if resize dimensions are valid
    if len(args.resize) != 2:
        logging.error("Resize dimensions must be specified as width,height")
        return False
    
    return True

def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line interface.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parsed_args = parse_args(args)
    
    # Setup logging
    setup_logger(parsed_args.log_level, parsed_args.log_file)
    
    # Validate arguments
    if not validate_args(parsed_args):
        return 1
    
    try:
        # Process images
        processor = ImageProcessor(parsed_args.input_dir, parsed_args.output_dir)
        processor.process_images(
            resize_dimensions=parsed_args.resize,
            blur_radius=parsed_args.blur,
            sharpen_factor=parsed_args.sharpen,
            contrast_factor=parsed_args.contrast,
            brightness_factor=parsed_args.brightness
        )
        logging.info("Image processing completed successfully")
        return 0
    except Exception as e:
        logging.error(f"Error during image processing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())