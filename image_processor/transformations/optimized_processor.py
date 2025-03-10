"""
Core image processing functionality - Optimized version.
"""

import os
import logging
from PIL import Image, ImageEnhance, ImageFilter
from typing import Tuple, Optional
import concurrent.futures
from functools import lru_cache

logger = logging.getLogger(__name__)

class OptimizedImageProcessor:
    """
    An optimized version of the ImageProcessor class that addresses known inefficiencies:
    1. Eliminates redundant loading/saving operations
    2. Implements parallel processing
    3. Adds caching for repeated operations
    4. Performs batch processing of transformations
    """

    def __init__(self, input_dir: str, output_dir: str):
        """
        Initialize the OptimizedImageProcessor.

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
    
    @lru_cache(maxsize=32)  # Cache for repeated operations with same parameters
    def _get_image_format(self, filename: str) -> str:
        """Determine the best format to save the image based on filename extension."""
        lower_filename = filename.lower()
        if lower_filename.endswith(('.jpg', '.jpeg')):
            return 'JPEG'
        elif lower_filename.endswith('.png'):
            return 'PNG'
        elif lower_filename.endswith('.bmp'):
            return 'BMP'
        elif lower_filename.endswith('.tiff'):
            return 'TIFF'
        else:
            return 'JPEG'  # Default format
    
    def process_images(self, 
                      resize_dimensions: Optional[Tuple[int, int]] = (800, 600),
                      blur_radius: float = 1.0,
                      sharpen_factor: float = 1.5,
                      contrast_factor: float = 1.2,
                      brightness_factor: float = 1.1,
                      max_workers: int = 4):
        """
        Process all images in the input directory using parallel processing.

        Args:
            resize_dimensions: Target width and height for resizing
            blur_radius: Radius for Gaussian blur
            sharpen_factor: Factor for sharpening
            contrast_factor: Factor for contrast adjustment
            brightness_factor: Factor for brightness adjustment
            max_workers: Maximum number of worker threads for parallel processing
        """
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        
        # Get list of image files
        image_files = [
            filename for filename in os.listdir(self.input_dir)
            if any(filename.lower().endswith(fmt) for fmt in supported_formats)
        ]
        
        # Process images in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    self._process_single_image,
                    filename,
                    resize_dimensions,
                    blur_radius,
                    sharpen_factor,
                    contrast_factor,
                    brightness_factor
                ): filename for filename in image_files
            }
            
            for future in concurrent.futures.as_completed(futures):
                filename = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error processing {filename}: {str(e)}")

    def _process_single_image(self,
                            filename: str,
                            resize_dimensions: Tuple[int, int],
                            blur_radius: float,
                            sharpen_factor: float,
                            contrast_factor: float,
                            brightness_factor: float):
        """
        Apply transformations to a single image efficiently by:
        1. Loading the image only once
        2. Applying all transformations in sequence
        3. Saving the final result only once
        """
        try:
            input_path = os.path.join(self.input_dir, filename)
            output_path = os.path.join(self.output_dir, f"processed_{filename}")
            
            logger.info(f"Processing image: {filename}")
            
            # Load the image only once
            image = Image.open(input_path)
            
            # Apply all transformations in sequence without intermediate saves
            # 1. Resize
            image = image.resize(resize_dimensions, Image.LANCZOS)
            
            # 2. Blur
            image = image.filter(ImageFilter.GaussianBlur(blur_radius))
            
            # 3. Sharpen
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(sharpen_factor)
            
            # 4. Contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast_factor)
            
            # 5. Brightness
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness_factor)
            
            # Save the final result only once, with optimized format
            image_format = self._get_image_format(filename)
            image.save(output_path, format=image_format, optimize=True)
            
            logger.info(f"Successfully processed: {filename}")
            
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}")
            raise