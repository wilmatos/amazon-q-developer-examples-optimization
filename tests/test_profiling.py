"""
Test profiling functionality with generated test images.
"""

import os
import unittest
import shutil
from image_processor.transformations.processor import ImageProcessor
from image_processor.utils.test_data import generate_test_images

class TestProfiling(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.test_input_dir = "data/input"
        self.test_output_dir = "data/output"
        
        # Clean up any existing test data
        for dir_path in [self.test_input_dir, self.test_output_dir]:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
            os.makedirs(dir_path)
        
        # Generate test images
        generate_test_images(self.test_input_dir, num_images=5)

    def tearDown(self):
        """Clean up after each test."""
        for dir_path in [self.test_input_dir, self.test_output_dir]:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
            os.makedirs(dir_path)
            # Keep .gitkeep file
            with open(os.path.join(dir_path, '.gitkeep'), 'w') as f:
                pass

    def test_image_processing_performance(self):
        """Test the performance of image processing pipeline."""
        processor = ImageProcessor(self.test_input_dir, self.test_output_dir)
        
        # Process images with default parameters
        processor.process_images()
        
        # Verify output files were created
        input_files = [f for f in os.listdir(self.test_input_dir) 
                      if not f.startswith('.')]
        output_files = [f for f in os.listdir(self.test_output_dir) 
                       if not f.startswith('.')]
        
        self.assertEqual(
            len(input_files), 
            len(output_files), 
            "Number of output files should match input files"
        )

if __name__ == '__main__':
    unittest.main()