#!/usr/bin/env python3
"""
Main script to run image processor benchmarks and generate optimization report.
"""

import os
import sys
import logging
from pathlib import Path

from image_processor.profiling.benchmark import ImageProcessorBenchmark, run_benchmarks
from image_processor.utils.test_data import generate_test_images

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    """Run benchmarks and generate reports."""
    # Create reports directory if it doesn't exist
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        
    logger.info("Starting benchmark run")
    logger.info("This will compare the original image processor against the optimized version")
    
    # Run benchmarks
    benchmark = run_benchmarks()
    
    logger.info("Benchmark run complete")
    logger.info(f"Results have been saved to {reports_dir}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())