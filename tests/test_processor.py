"""
Tests for the image processor.
"""

import os
import shutil
import tempfile
import unittest
from PIL import Image

from image_processor.transformations.processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    """Test cases for the ImageProcessor class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories for input and output
        self.input_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()
        
        # Create a test image
        self.test_image_path = os.path.join(self.input_dir, "test_image.jpg")
        self._create_test_image(self.test_image_path)
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.input_dir, ignore_errors=True)
        shutil.rmtree(self.output_dir, ignore_errors=True)
        
    def _create_test_image(self, path, size=(100, 100), color=(255, 0, 0)):
        """Create a test image with the specified size and color."""
        image = Image.new("RGB", size, color)
        image.save(path)
        
    def test_process_images(self):
        """Test that images are processed and saved to the output directory."""
        processor = ImageProcessor(self.input_dir, self.output_dir)
        processor.process_images(
            resize_dimensions=(50, 50),
            blur_radius=1.0,
            sharpen_factor=1.5,
            contrast_factor=1.2,
            brightness_factor=1.1
        )
        
        # Check that the output file exists
        output_files = os.listdir(self.output_dir)
        self.assertEqual(len(output_files), 1)
        
        # Check that the output file has the expected name
        self.assertTrue(output_files[0].startswith("processed_"))
        
        # Check that the output image has the expected dimensions
        output_path = os.path.join(self.output_dir, output_files[0])
        with Image.open(output_path) as img:
            self.assertEqual(img.size, (50, 50))
            
    def test_error_handling(self):
        """Test that errors are handled properly."""
        # Create a test image
        valid_image_path = os.path.join(self.input_dir, "valid.jpg")
        self._create_test_image(valid_image_path)
        
        # Create an invalid image file
        invalid_image_path = os.path.join(self.input_dir, "invalid.jpg")
        with open(invalid_image_path, "w") as f:
            f.write("This is not a valid image file")
            
        # Remove test_image.jpg created in setUp
        os.remove(self.test_image_path)
            
        processor = ImageProcessor(self.input_dir, self.output_dir)
        
        # The processor should handle the error and continue processing valid images
        processor.process_images()
            
        # Check that the valid image was still processed
        output_files = os.listdir(self.output_dir)
        self.assertEqual(len(output_files), 1)
        self.assertTrue(any("valid" in f for f in output_files))
        
if __name__ == "__main__":
    unittest.main()