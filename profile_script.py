"""
Script to profile memory usage of the image processor.
"""

from image_processor.transformations.processor import ImageProcessor
from image_processor.utils.test_data import generate_test_images
import os
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@profile
def process_images(input_dir, output_dir):
    """Process images with memory profiling."""
    processor = ImageProcessor(input_dir, output_dir)
    processor.process_images()
    return processor

def main():
    """Run the image processor with memory profiling."""
    input_dir = "data/input"
    output_dir = "data/output"
    
    # Clean directories
    for dir_path in [input_dir, output_dir]:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    
    # Generate test images
    logger.info("Generating test images...")
    generate_test_images(input_dir, num_images=5)
    
    # Process images with memory profiling
    logger.info("Processing images...")
    process_images(input_dir, output_dir)
    logger.info("Processing complete.")

if __name__ == "__main__":
    main()