"""
Detailed memory profiling of the image processor.
"""

from image_processor.transformations.processor import ImageProcessor
from image_processor.utils.test_data import generate_test_images
import os
import shutil
import logging
from PIL import Image, ImageEnhance, ImageFilter

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ProfiledImageProcessor(ImageProcessor):
    """Extended image processor with profiled methods."""
    
    @profile
    def _process_single_image(self, filename, resize_dimensions, blur_radius, 
                             sharpen_factor, contrast_factor, brightness_factor):
        """Profiled version of the image processing method."""
        try:
            input_path = os.path.join(self.input_dir, filename)
            output_path = os.path.join(self.output_dir, f"processed_{filename}")
            
            logger.info(f"Processing image: {filename}")
            
            # Resize
            image = Image.open(input_path)
            image = image.resize(resize_dimensions, Image.LANCZOS)
            image.save(output_path)
            
            # Blur
            image = Image.open(output_path)
            image = image.filter(ImageFilter.GaussianBlur(blur_radius))
            image.save(output_path)
            
            # Sharpen
            image = Image.open(output_path)
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(sharpen_factor)
            image.save(output_path)
            
            # Contrast
            image = Image.open(output_path)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast_factor)
            image.save(output_path)
            
            # Brightness
            image = Image.open(output_path)
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness_factor)
            image.save(output_path)
            
            logger.info(f"Successfully processed: {filename}")
            
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}")
            raise

def main():
    """Run the image processor with detailed memory profiling."""
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
    logger.info("Processing images with detailed profiling...")
    processor = ProfiledImageProcessor(input_dir, output_dir)
    processor.process_images()
    logger.info("Processing complete.")

if __name__ == "__main__":
    main()