"""
Tests for the command-line interface.
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from image_processor.cli import main, parse_args

class TestCLI(unittest.TestCase):
    """Test cases for the command-line interface."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories for input and output
        self.input_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)
        
    def test_parse_args(self):
        """Test argument parsing."""
        args = parse_args([
            "-i", self.input_dir,
            "-o", self.output_dir,
            "--resize", "400,300",
            "--blur", "2.0",
            "--sharpen", "2.5",
            "--contrast", "1.5",
            "--brightness", "0.8",
            "--log-level", "DEBUG"
        ])
        
        self.assertEqual(args.input_dir, self.input_dir)
        self.assertEqual(args.output_dir, self.output_dir)
        self.assertEqual(args.resize, (400, 300))
        self.assertEqual(args.blur, 2.0)
        self.assertEqual(args.sharpen, 2.5)
        self.assertEqual(args.contrast, 1.5)
        self.assertEqual(args.brightness, 0.8)
        self.assertEqual(args.log_level, "DEBUG")
        
    @patch("image_processor.cli.ImageProcessor")
    def test_main_success(self, mock_processor):
        """Test successful execution of the main function."""
        # Create a test image in the input directory
        test_image_path = os.path.join(self.input_dir, "test.jpg")
        with open(test_image_path, "wb") as f:
            f.write(b"dummy image data")
            
        # Call the main function
        exit_code = main([
            "-i", self.input_dir,
            "-o", self.output_dir
        ])
        
        # Check that the processor was called with the correct arguments
        mock_processor.assert_called_once_with(self.input_dir, self.output_dir)
        mock_processor.return_value.process_images.assert_called_once()
        
        # Check that the function returned success
        self.assertEqual(exit_code, 0)
        
    def test_main_invalid_input_dir(self):
        """Test handling of invalid input directory."""
        # Call the main function with a non-existent input directory
        exit_code = main([
            "-i", "/non/existent/directory",
            "-o", self.output_dir
        ])
        
        # Check that the function returned failure
        self.assertEqual(exit_code, 1)
        
if __name__ == "__main__":
    unittest.main()