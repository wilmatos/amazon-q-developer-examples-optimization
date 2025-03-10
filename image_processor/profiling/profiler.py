"""
Core profiling functionality for the image processor.
"""

import cProfile
import pstats
import io
import time
import os
import psutil
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
from memory_profiler import profile as memory_profile

from ..transformations.processor import ImageProcessor

class ImageProcessorProfiler:
    """
    A profiler for the image processing application that tracks CPU usage,
    memory consumption, and execution time.
    """

    def __init__(self, output_dir: str):
        """
        Initialize the profiler.

        Args:
            output_dir: Directory to store profiling results
        """
        self.output_dir = output_dir
        self.profile_data = {
            'timestamp': datetime.now().isoformat(),
            'cpu_stats': {},
            'memory_stats': {},
            'timing_stats': {},
            'per_image_stats': {}
        }
        self._setup_output_directory()

    def _setup_output_directory(self):
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    @memory_profile
    def _process_single_image(self, processor: ImageProcessor, 
                            filename: str, 
                            params: Dict) -> Tuple[float, float]:
        """
        Process a single image and measure its execution time and memory usage.

        Args:
            processor: ImageProcessor instance
            filename: Name of the image file
            params: Processing parameters

        Returns:
            Tuple of (execution_time, peak_memory)
        """
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        start_time = time.time()

        processor._process_single_image(filename, **params)

        execution_time = time.time() - start_time
        end_memory = process.memory_info().rss / 1024 / 1024
        peak_memory = end_memory - start_memory

        return execution_time, peak_memory

    def profile_processing(self, 
                         input_dir: str,
                         output_dir: str,
                         params: Optional[Dict] = None) -> Dict:
        """
        Profile the image processing with given parameters.

        Args:
            input_dir: Input directory containing images
            output_dir: Output directory for processed images
            params: Processing parameters (optional)

        Returns:
            Dictionary containing profiling results
        """
        if params is None:
            params = {
                'resize_dimensions': (800, 600),
                'blur_radius': 1.0,
                'sharpen_factor': 1.5,
                'contrast_factor': 1.2,
                'brightness_factor': 1.1
            }

        processor = ImageProcessor(input_dir, output_dir)
        
        # Setup CPU profiler
        pr = cProfile.Profile()
        pr.enable()

        # Process images and collect timing/memory stats
        process = psutil.Process(os.getpid())
        start_time = time.time()
        start_memory = process.memory_info().rss / 1024 / 1024

        for filename in os.listdir(input_dir):
            if any(filename.lower().endswith(fmt) 
                  for fmt in {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}):
                execution_time, peak_memory = self._process_single_image(
                    processor, filename, params)
                
                self.profile_data['per_image_stats'][filename] = {
                    'execution_time': execution_time,
                    'peak_memory_mb': peak_memory
                }

        # Collect overall stats
        pr.disable()
        end_time = time.time()
        end_memory = process.memory_info().rss / 1024 / 1024

        # Save CPU stats
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        self.profile_data['cpu_stats'] = s.getvalue()

        # Save memory stats
        self.profile_data['memory_stats'] = {
            'start_memory_mb': start_memory,
            'end_memory_mb': end_memory,
            'peak_memory_mb': max(stat['peak_memory_mb'] 
                                for stat in self.profile_data['per_image_stats'].values())
        }

        # Save timing stats
        self.profile_data['timing_stats'] = {
            'total_time': end_time - start_time,
            'average_time_per_image': (end_time - start_time) / 
                                    len(self.profile_data['per_image_stats'])
        }

        return self.profile_data

    def stress_test(self, 
                   input_dir: str,
                   output_dir: str,
                   iterations: int = 5,
                   param_variations: Optional[List[Dict]] = None) -> List[Dict]:
        """
        Perform stress testing by processing images multiple times with different parameters.

        Args:
            input_dir: Input directory containing images
            output_dir: Output directory for processed images
            iterations: Number of iterations for each parameter set
            param_variations: List of parameter dictionaries to test

        Returns:
            List of profiling results for each iteration
        """
        if param_variations is None:
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
                },
                {
                    'resize_dimensions': (1920, 1080),
                    'blur_radius': 3.0,
                    'sharpen_factor': 2.5,
                    'contrast_factor': 1.8,
                    'brightness_factor': 1.5
                }
            ]

        stress_results = []
        for params in param_variations:
            for i in range(iterations):
                iteration_output = os.path.join(output_dir, f'iteration_{i}')
                os.makedirs(iteration_output, exist_ok=True)
                
                result = self.profile_processing(input_dir, iteration_output, params)
                result['parameters'] = params
                result['iteration'] = i
                stress_results.append(result)

        return stress_results

    def visualize_results(self, results: Optional[Dict] = None):
        """
        Create visualizations of profiling results.

        Args:
            results: Profiling results (uses stored results if None)
        """
        if results is None:
            results = self.profile_data

        # Create visualization directory
        vis_dir = os.path.join(self.output_dir, 'visualizations')
        os.makedirs(vis_dir, exist_ok=True)

        # Plot execution time per image
        plt.figure(figsize=(12, 6))
        times = [stats['execution_time'] 
                for stats in results['per_image_stats'].values()]
        plt.bar(range(len(times)), times)
        plt.title('Execution Time per Image')
        plt.xlabel('Image Index')
        plt.ylabel('Time (seconds)')
        plt.savefig(os.path.join(vis_dir, 'execution_times.png'))
        plt.close()

        # Plot memory usage per image
        plt.figure(figsize=(12, 6))
        memory = [stats['peak_memory_mb'] 
                 for stats in results['per_image_stats'].values()]
        plt.bar(range(len(memory)), memory)
        plt.title('Peak Memory Usage per Image')
        plt.xlabel('Image Index')
        plt.ylabel('Memory (MB)')
        plt.savefig(os.path.join(vis_dir, 'memory_usage.png'))
        plt.close()

    def save_results(self, results: Optional[Dict] = None):
        """
        Save profiling results to files.

        Args:
            results: Profiling results (uses stored results if None)
        """
        if results is None:
            results = self.profile_data

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save raw data as JSON
        data_file = os.path.join(self.output_dir, f'profile_data_{timestamp}.json')
        with open(data_file, 'w') as f:
            json.dump(results, f, indent=2)

        # Save CPU profile
        cpu_file = os.path.join(self.output_dir, f'cpu_profile_{timestamp}.txt')
        with open(cpu_file, 'w') as f:
            f.write(results['cpu_stats'])

        # Generate analysis report
        self._generate_analysis_report(results, timestamp)

    def _generate_analysis_report(self, results: Dict, timestamp: str):
        """
        Generate a detailed analysis report identifying bottlenecks and suggesting optimizations.

        Args:
            results: Profiling results
            timestamp: Timestamp string for the filename
        """
        report_file = os.path.join(self.output_dir, f'analysis_report_{timestamp}.md')
        
        with open(report_file, 'w') as f:
            f.write('# Image Processing Performance Analysis Report\n\n')
            
            # Overall Statistics
            f.write('## Overall Statistics\n\n')
            f.write(f"- Total Processing Time: {results['timing_stats']['total_time']:.2f} seconds\n")
            f.write(f"- Average Time per Image: {results['timing_stats']['average_time_per_image']:.2f} seconds\n")
            f.write(f"- Peak Memory Usage: {results['memory_stats']['peak_memory_mb']:.2f} MB\n\n")

            # Performance Bottlenecks
            f.write('## Performance Bottlenecks\n\n')
            f.write('### CPU Usage\n')
            f.write('Top time-consuming functions:\n')
            f.write('```\n')
            f.write(results['cpu_stats'][:1000] + '...\n')  # First 1000 chars
            f.write('```\n\n')

            # Memory Analysis
            f.write('### Memory Usage\n')
            f.write(f"- Initial Memory: {results['memory_stats']['start_memory_mb']:.2f} MB\n")
            f.write(f"- Final Memory: {results['memory_stats']['end_memory_mb']:.2f} MB\n")
            f.write(f"- Memory Growth: {results['memory_stats']['end_memory_mb'] - results['memory_stats']['start_memory_mb']:.2f} MB\n\n")

            # Optimization Suggestions
            f.write('## Optimization Suggestions\n\n')
            
            # Memory optimizations
            if results['memory_stats']['peak_memory_mb'] > 1000:  # More than 1GB
                f.write('### Memory Optimizations\n')
                f.write('1. Implement batch processing to limit memory usage\n')
                f.write('2. Use memory-mapped files for large images\n')
                f.write('3. Release memory more aggressively after processing each image\n\n')

            # CPU optimizations
            f.write('### CPU Optimizations\n')
            f.write('1. Implement parallel processing for multiple images\n')
            f.write('2. Optimize the transformation pipeline to reduce redundant operations\n')
            f.write('3. Use numpy operations where possible for better performance\n\n')

            # I/O optimizations
            f.write('### I/O Optimizations\n')
            f.write('1. Reduce disk I/O by processing images in memory\n')
            f.write('2. Implement caching for intermediate results\n')
            f.write('3. Use buffered I/O operations\n\n')

            # Recommendations
            f.write('## Recommendations\n\n')
            f.write('Based on the profiling results, the following improvements are recommended:\n\n')
            f.write('1. Immediate Improvements:\n')
            f.write('   - Implement parallel processing using multiprocessing\n')
            f.write('   - Optimize image loading/saving operations\n')
            f.write('   - Add caching for intermediate results\n\n')
            f.write('2. Long-term Improvements:\n')
            f.write('   - Rewrite core transformation logic using numpy\n')
            f.write('   - Implement streaming processing for large images\n')
            f.write('   - Add support for GPU acceleration\n')