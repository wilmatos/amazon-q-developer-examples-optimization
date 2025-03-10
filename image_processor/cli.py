"""
Command-line interface for the image processor.
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from typing import List, Optional, Tuple

from image_processor.transformations.processor import ImageProcessor
from image_processor.utils.logger import setup_logger
from image_processor.profiling.profiler import ProcessingProfiler

def get_default_paths():
    """Get default paths for input, output, and reports directories."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return {
        'input': os.path.join(base_dir, 'data', 'input'),
        'output': os.path.join(base_dir, 'data', 'output'),
        'reports': os.path.join(base_dir, 'reports')
    }

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Parsed arguments
    """
    default_paths = get_default_paths()
    
    parser = argparse.ArgumentParser(
        description="Process images with various transformations",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-i", "--input-dir",
        default=default_paths['input'],
        help="Directory containing input images"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default=default_paths['output'],
        help="Directory for processed images"
    )
    
    parser.add_argument(
        "--reports-dir",
        default=default_paths['reports'],
        help="Directory for storing profiling reports"
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
    # Create directories if they don't exist
    os.makedirs(args.input_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.reports_dir, exist_ok=True)
    
    # Check if input directory has any files
    if not os.listdir(args.input_dir):
        logging.warning(f"Input directory is empty: {args.input_dir}")
        return False
    
    # Check if resize dimensions are valid
    if len(args.resize) != 2:
        logging.error("Resize dimensions must be specified as width,height")
        return False
    
    return True

def get_report_filename() -> str:
    """Generate a timestamped filename for the profiling report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"profiling_report_{timestamp}.json"

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
        # Initialize profiler
        report_path = os.path.join(parsed_args.reports_dir, get_report_filename())
        profiler = ProcessingProfiler(report_path)
        
        # Process images
        with profiler:
            processor = ImageProcessor(parsed_args.input_dir, parsed_args.output_dir)
            processor.process_images(
                resize_dimensions=parsed_args.resize,
                blur_radius=parsed_args.blur,
                sharpen_factor=parsed_args.sharpen,
                contrast_factor=parsed_args.contrast,
                brightness_factor=parsed_args.brightness
            )
        
        logging.info(f"Image processing completed successfully. Profiling report saved to: {report_path}")
        return 0
    except Exception as e:
        logging.error(f"Error during image processing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())