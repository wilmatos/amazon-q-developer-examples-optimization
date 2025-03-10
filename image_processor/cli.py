"""
Command-line interface for the image processor.
"""

import argparse
import logging
import os
import sys
import time
import json
import psutil
from datetime import datetime
from image_processor.transformations.processor import ImageProcessor
from image_processor.utils.test_data import generate_test_images

def setup_logging(log_level, log_file=None):
    """Configure logging for the application."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handlers = [logging.StreamHandler()]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(level=numeric_level, format=log_format, handlers=handlers)

def get_system_info():
    """Get system information for profiling."""
    return {
        "cpu": {
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent()
        },
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent
        },
        "platform": sys.platform
    }

def save_profiling_report(execution_time, system_info, final_system_info):
    """Save profiling information to a JSON file."""
    # Create reports directory if it doesn't exist
    reports_dir = os.path.expanduser("~/.local/lib/python3.10/reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(reports_dir, f"profiling_report_{timestamp}.json")
    
    report = {
        "system_info": system_info,
        "execution_time": execution_time,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "final_system_info": final_system_info
    }
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    return report_path

def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(description="Process images with various transformations.")
    parser.add_argument("-i", "--input-dir", required=True, help="Input directory containing images")
    parser.add_argument("-o", "--output-dir", required=True, help="Output directory for processed images")
    parser.add_argument("--resize", default="800,600", help="Resize dimensions (width,height)")
    parser.add_argument("--blur", type=float, default=1.0, help="Blur radius")
    parser.add_argument("--sharpen", type=float, default=1.5, help="Sharpen factor")
    parser.add_argument("--contrast", type=float, default=1.2, help="Contrast adjustment factor")
    parser.add_argument("--brightness", type=float, default=1.1, help="Brightness adjustment factor")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging level")
    parser.add_argument("--log-file", help="Log file path")
    parser.add_argument("--generate-test-images", type=int, default=0, 
                        help="Generate test images (specify number of images)")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level, args.log_file)
    logger = logging.getLogger()
    
    # Generate test images if requested
    if args.generate_test_images > 0:
        logger.info(f"Generating {args.generate_test_images} test images in {args.input_dir}")
        generate_test_images(args.input_dir, num_images=args.generate_test_images)
    
    # Parse resize dimensions
    try:
        width, height = map(int, args.resize.split(','))
        resize_dimensions = (width, height)
    except ValueError:
        logger.error("Invalid resize dimensions. Format should be width,height")
        sys.exit(1)
    
    # Initialize processor
    processor = ImageProcessor(args.input_dir, args.output_dir)
    
    # Collect system info before processing
    system_info = get_system_info()
    
    # Process images and measure execution time
    start_time = time.time()
    processor.process_images(
        resize_dimensions=resize_dimensions,
        blur_radius=args.blur,
        sharpen_factor=args.sharpen,
        contrast_factor=args.contrast,
        brightness_factor=args.brightness
    )
    execution_time = time.time() - start_time
    
    # Collect system info after processing
    final_system_info = get_system_info()
    
    # Save profiling report
    report_path = save_profiling_report(execution_time, system_info, final_system_info)
    logger.info(f"Image processing completed successfully. Profiling report saved to: {report_path}")

if __name__ == "__main__":
    main()