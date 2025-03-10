"""
Core image processing functionality.
"""

import os
import logging
from PIL import Image, ImageEnhance, ImageFilter
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    A class to handle various image transformations.
    Intentionally inefficient for demonstration purposes.
    """

    def __init__(self, input_dir: str, output_dir: str):
        """
        Initialize the ImageProcessor.

        Args:
            input_dir (str): Directory containing input images
            output_dir (str): Directory for processed images
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self._setup_output_directory()

    def _setup_output_directory(self):
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Created output directory: {self.output_dir}")

    def process_images(self, 
                      resize_dimensions: Optional[Tuple[int, int]] = (800, 600),
                      blur_radius: float = 1.0,
                      sharpen_factor: float = 1.5,
                      contrast_factor: float = 1.2,
                      brightness_factor: float = 1.1):
        """
        Process all images in the input directory.

        Args:
            resize_dimensions: Target width and height for resizing
            blur_radius: Radius for Gaussian blur
            sharpen_factor: Factor for sharpening
            contrast_factor: Factor for contrast adjustment
            brightness_factor: Factor for brightness adjustment
        """
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        
        for filename in os.listdir(self.input_dir):
            if any(filename.lower().endswith(fmt) for fmt in supported_formats):
                self._process_single_image(
                    filename,
                    resize_dimensions,
                    blur_radius,
                    sharpen_factor,
                    contrast_factor,
                    brightness_factor
                )

    def _process_single_image(self,
                            filename: str,
                            resize_dimensions: Tuple[int, int],
                            blur_radius: float,
                            sharpen_factor: float,
                            contrast_factor: float,
                            brightness_factor: float):
        """
        Apply transformations to a single image.
        Intentionally inefficient by loading/saving multiple times.
        """
        try:
            input_path = os.path.join(self.input_dir, filename)
            output_path = os.path.join(self.output_dir, f"processed_{filename}")
            
            # Inefficient: Load and save the image multiple times
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