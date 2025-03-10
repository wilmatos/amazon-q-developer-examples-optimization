"""
Tests for the profiling framework.
"""

import os
import shutil
import tempfile
import unittest
from PIL import Image
import json

from image_processor.profiling.profiler import ImageProcessorProfiler

class TestProfiler(unittest.TestCase):
    """Test cases for the ImageProcessorProfiler class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories
        self.input_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()
        self.profile_dir = tempfile.mkdtemp()
        
        # Create test images
        self.create_test_images()
        
        # Initialize profiler
        self.profiler = ImageProcessorProfiler(self.profile_dir)
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)
        shutil.rmtree(self.profile_dir)
        
    def create_test_images(self, count: int = 3):
        """Create test images for profiling."""
        for i in range(count):
            image = Image.new('RGB', (100, 100), color=f'rgb({i*50}, {i*50}, {i*50})')
            image.save(os.path.join(self.input_dir, f'test_image_{i}.jpg'))
            
    def test_profile_processing(self):
        """Test basic profiling functionality."""
        results = self.profiler.profile_processing(self.input_dir, self.output_dir)
        
        # Check that results contain all expected sections
        self.assertIn('cpu_stats', results)
        self.assertIn('memory_stats', results)
        self.assertIn('timing_stats', results)
        self.assertIn('per_image_stats', results)
        
        # Check that timing stats are present and reasonable
        self.assertGreater(results['timing_stats']['total_time'], 0)
        self.assertGreater(results['timing_stats']['average_time_per_image'], 0)
        
        # Check that memory stats are present and reasonable
        self.assertGreater(results['memory_stats']['peak_memory_mb'], 0)
        
        # Check that per-image stats are present for each test image
        self.assertEqual(len(results['per_image_stats']), 3)
        
    def test_stress_test(self):
        """Test stress testing functionality."""
        iterations = 2
        param_variations = [
            {
                'resize_dimensions': (800, 600),
                'blur_radius': 1.0,
                'sharpen_factor': 1.5,
                'contrast_factor': 1.2,
                'brightness_factor': 1.1
            },
            {
                'resize_dimensions': (1024, 768),
                'blur_radius': 2.0,
                'sharpen_factor': 2.0,
                'contrast_factor': 1.5,
                'brightness_factor': 1.3
            }
        ]
        
        results = self.profiler.stress_test(
            self.input_dir,
            self.output_dir,
            iterations,
            param_variations
        )
        
        # Check that we have results for each iteration and parameter set
        self.assertEqual(len(results), len(param_variations) * iterations)
        
        # Check that each result contains the parameter set used
        for result in results:
            self.assertIn('parameters', result)
            self.assertIn('iteration', result)
            
    def test_save_results(self):
        """Test saving profiling results."""
        results = self.profiler.profile_processing(self.input_dir, self.output_dir)
        self.profiler.save_results(results)
        
        # Check that files were created
        files = os.listdir(self.profile_dir)
        self.assertTrue(any(f.startswith('profile_data_') for f in files))
        self.assertTrue(any(f.startswith('cpu_profile_') for f in files))
        self.assertTrue(any(f.startswith('analysis_report_') for f in files))
        
        # Check that saved data is valid JSON
        json_file = next(f for f in files if f.startswith('profile_data_'))
        with open(os.path.join(self.profile_dir, json_file), 'r') as f:
            loaded_results = json.load(f)
            self.assertEqual(loaded_results['timing_stats'], results['timing_stats'])
            
    def test_visualize_results(self):
        """Test visualization generation."""
        results = self.profiler.profile_processing(self.input_dir, self.output_dir)
        self.profiler.visualize_results(results)
        
        # Check that visualization files were created
        vis_dir = os.path.join(self.profile_dir, 'visualizations')
        self.assertTrue(os.path.exists(vis_dir))
        self.assertTrue(os.path.exists(os.path.join(vis_dir, 'execution_times.png')))
        self.assertTrue(os.path.exists(os.path.join(vis_dir, 'memory_usage.png')))
        
if __name__ == '__main__':
    unittest.main()