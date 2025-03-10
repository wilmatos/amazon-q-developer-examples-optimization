"""
Framework for benchmarking image processor performance.
"""

import time
import os
import psutil
import logging
import shutil
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Callable, Any

from image_processor.transformations.processor import ImageProcessor
from image_processor.transformations.optimized_processor import OptimizedImageProcessor
from image_processor.utils.test_data import generate_test_images

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class BenchmarkMetrics:
    """Class to hold performance metrics for benchmarking."""
    
    def __init__(self):
        """Initialize metrics storage."""
        self.execution_times = {}
        self.memory_usage = {}
        self.cpu_usage = {}
        
    def add_time_metric(self, name: str, duration: float):
        """Add an execution time metric."""
        if name not in self.execution_times:
            self.execution_times[name] = []
        self.execution_times[name].append(duration)
        
    def add_memory_metric(self, name: str, memory_mb: float):
        """Add a memory usage metric."""
        if name not in self.memory_usage:
            self.memory_usage[name] = []
        self.memory_usage[name].append(memory_mb)
        
    def add_cpu_metric(self, name: str, cpu_percent: float):
        """Add a CPU usage metric."""
        if name not in self.cpu_usage:
            self.cpu_usage[name] = []
        self.cpu_usage[name].append(cpu_percent)
    
    def get_avg_time(self, name: str) -> float:
        """Get average execution time for a metric."""
        if name in self.execution_times and self.execution_times[name]:
            return sum(self.execution_times[name]) / len(self.execution_times[name])
        return 0
        
    def get_avg_memory(self, name: str) -> float:
        """Get average memory usage for a metric."""
        if name in self.memory_usage and self.memory_usage[name]:
            return sum(self.memory_usage[name]) / len(self.memory_usage[name])
        return 0
        
    def get_avg_cpu(self, name: str) -> float:
        """Get average CPU usage for a metric."""
        if name in self.cpu_usage and self.cpu_usage[name]:
            return sum(self.cpu_usage[name]) / len(self.cpu_usage[name])
        return 0

class ImageProcessorBenchmark:
    """Benchmark framework for comparing image processors."""
    
    def __init__(self, 
                input_base_dir: str = "data/benchmark_input", 
                output_base_dir: str = "data/benchmark_output",
                report_dir: str = "reports"):
        """
        Initialize the benchmark framework.
        
        Args:
            input_base_dir: Base directory for input test images
            output_base_dir: Base directory for processed output images
            report_dir: Directory for saving benchmark reports
        """
        self.input_base_dir = input_base_dir
        self.output_base_dir = output_base_dir
        self.report_dir = report_dir
        self.metrics = BenchmarkMetrics()
        
        # Create directories
        for dir_path in [self.report_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
    
    def _prepare_directories(self, test_name: str) -> Tuple[str, str]:
        """
        Prepare input and output directories for a test.
        
        Args:
            test_name: Name of the test
            
        Returns:
            Tuple containing input and output directory paths
        """
        input_dir = os.path.join(self.input_base_dir, test_name)
        output_dir = os.path.join(self.output_base_dir, test_name)
        
        # Clean directories
        for dir_path in [input_dir, output_dir]:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
            os.makedirs(dir_path)
            
        return input_dir, output_dir
    
    def _measure_performance(self, processor_fn: Callable, name: str, **kwargs) -> Dict[str, float]:
        """
        Measure performance metrics for a processor function.
        
        Args:
            processor_fn: Function that processes images
            name: Name to use for metrics
            **kwargs: Additional arguments for processor_fn
            
        Returns:
            Dictionary with performance metrics
        """
        process = psutil.Process(os.getpid())
        
        # Measure initial memory
        initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
        
        # Measure CPU and execution time
        start_time = time.time()
        initial_cpu_time = process.cpu_times()
        
        # Run the processor
        result = processor_fn(**kwargs)
        
        # Calculate metrics
        end_time = time.time()
        final_cpu_time = process.cpu_times()
        final_memory = process.memory_info().rss / (1024 * 1024)  # MB
        
        execution_time = end_time - start_time
        memory_usage = final_memory - initial_memory
        cpu_usage = (final_cpu_time.user + final_cpu_time.system) - (initial_cpu_time.user + initial_cpu_time.system)
        
        # Store metrics
        self.metrics.add_time_metric(name, execution_time)
        self.metrics.add_memory_metric(name, memory_usage)
        self.metrics.add_cpu_metric(name, cpu_usage)
        
        logger.info(f"{name}: Time={execution_time:.2f}s, Memory={memory_usage:.2f}MB, CPU={cpu_usage:.2f}s")
        
        return {"time": execution_time, "memory": memory_usage, "cpu": cpu_usage}
    
    def run_original_processor(self, input_dir: str, output_dir: str, **kwargs) -> Dict[str, float]:
        """
        Run the original image processor and measure performance.
        
        Args:
            input_dir: Input directory with test images
            output_dir: Output directory for processed images
            **kwargs: Additional arguments for the processor
            
        Returns:
            Dictionary with performance metrics
        """
        def processor_fn():
            processor = ImageProcessor(input_dir, output_dir)
            processor.process_images(**kwargs)
            return processor
            
        return self._measure_performance(processor_fn, "original")
    
    def run_optimized_processor(self, input_dir: str, output_dir: str, **kwargs) -> Dict[str, float]:
        """
        Run the optimized image processor and measure performance.
        
        Args:
            input_dir: Input directory with test images
            output_dir: Output directory for processed images
            **kwargs: Additional arguments for the processor
            
        Returns:
            Dictionary with performance metrics
        """
        def processor_fn():
            processor = OptimizedImageProcessor(input_dir, output_dir)
            processor.process_images(**kwargs)
            return processor
            
        return self._measure_performance(processor_fn, "optimized")
    
    def run_comparison(self, 
                      test_name: str, 
                      num_images: int = 5, 
                      image_size: Tuple[int, int] = (1920, 1080),
                      iterations: int = 3,
                      **processor_kwargs) -> Dict[str, Dict[str, float]]:
        """
        Run a comparison benchmark between original and optimized processors.
        
        Args:
            test_name: Name of the test
            num_images: Number of test images to process
            image_size: Size of test images
            iterations: Number of times to repeat the test
            **processor_kwargs: Additional arguments for the processors
            
        Returns:
            Dictionary with comparison metrics
        """
        logger.info(f"Running benchmark: {test_name} with {num_images} images of size {image_size}")
        
        results = {"original": {}, "optimized": {}}
        
        for i in range(iterations):
            logger.info(f"Iteration {i+1}/{iterations}")
            
            # Prepare directories
            input_dir, output_dir = self._prepare_directories(f"{test_name}_iter{i+1}")
            
            # Generate test images
            generate_test_images(input_dir, num_images=num_images, size=image_size)
            
            # Run original processor
            orig_metrics = self.run_original_processor(input_dir, os.path.join(output_dir, "original"), **processor_kwargs)
            
            # Clean output directory for optimized version
            opt_output_dir = os.path.join(output_dir, "optimized")
            if os.path.exists(opt_output_dir):
                shutil.rmtree(opt_output_dir)
            os.makedirs(opt_output_dir)
            
            # Run optimized processor
            opt_metrics = self.run_optimized_processor(input_dir, opt_output_dir, **processor_kwargs)
            
            # Store metrics from this iteration
            for metric_name, metric_val in orig_metrics.items():
                if metric_name not in results["original"]:
                    results["original"][metric_name] = []
                results["original"][metric_name].append(metric_val)
                
            for metric_name, metric_val in opt_metrics.items():
                if metric_name not in results["optimized"]:
                    results["optimized"][metric_name] = []
                results["optimized"][metric_name].append(metric_val)
        
        # Calculate averages
        for processor in ["original", "optimized"]:
            for metric in results[processor]:
                results[processor][f"avg_{metric}"] = sum(results[processor][metric]) / len(results[processor][metric])
        
        return results
    
    def generate_charts(self, title: str, save_path: str = None) -> None:
        """
        Generate charts from collected benchmark metrics.
        
        Args:
            title: Title for the charts
            save_path: Path to save charts, if None charts will be displayed
        """
        # Setup plot
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle(title, fontsize=16)
        
        # Extract data
        processor_names = list(self.metrics.execution_times.keys())
        avg_times = [self.metrics.get_avg_time(name) for name in processor_names]
        avg_memory = [self.metrics.get_avg_memory(name) for name in processor_names]
        avg_cpu = [self.metrics.get_avg_cpu(name) for name in processor_names]
        
        # Create bars
        x = np.arange(len(processor_names))
        width = 0.6
        
        # Time chart
        ax1.bar(x, avg_times, width, color=['blue', 'green'])
        ax1.set_xlabel('Processor Type')
        ax1.set_ylabel('Execution Time (s)')
        ax1.set_title('Average Execution Time')
        ax1.set_xticks(x)
        ax1.set_xticklabels(processor_names)
        
        # Memory chart
        ax2.bar(x, avg_memory, width, color=['blue', 'green'])
        ax2.set_xlabel('Processor Type')
        ax2.set_ylabel('Memory Usage (MB)')
        ax2.set_title('Average Memory Usage')
        ax2.set_xticks(x)
        ax2.set_xticklabels(processor_names)
        
        # CPU chart
        ax3.bar(x, avg_cpu, width, color=['blue', 'green'])
        ax3.set_xlabel('Processor Type')
        ax3.set_ylabel('CPU Usage (s)')
        ax3.set_title('Average CPU Usage')
        ax3.set_xticks(x)
        ax3.set_xticklabels(processor_names)
        
        plt.tight_layout()
        
        # Save or display
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

def run_benchmarks():
    """Run a series of benchmarks to compare processors."""
    benchmark = ImageProcessorBenchmark()
    
    # Benchmark with different image counts
    image_counts = [5, 10, 20]
    for count in image_counts:
        results = benchmark.run_comparison(
            f"count_{count}",
            num_images=count,
            image_size=(1920, 1080)
        )
        
    # Benchmark with different image sizes
    image_sizes = [(640, 480), (1280, 720), (1920, 1080), (3840, 2160)]
    for size in image_sizes:
        results = benchmark.run_comparison(
            f"size_{size[0]}x{size[1]}",
            num_images=5,
            image_size=size
        )
    
    # Generate charts
    benchmark.generate_charts(
        "Image Processor Performance Comparison",
        save_path="reports/performance_comparison.png"
    )
    
    # Return benchmark instance for further analysis
    return benchmark

if __name__ == "__main__":
    benchmark = run_benchmarks()