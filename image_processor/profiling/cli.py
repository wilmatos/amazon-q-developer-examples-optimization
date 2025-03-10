"""
Command-line interface for the profiling framework.
"""

import argparse
import json
import os
from typing import List, Optional

from .profiler import ImageProcessorProfiler

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments for the profiler.
    
    Args:
        args: Command line arguments
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Profile image processing performance",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-i", "--input-dir",
        required=True,
        help="Directory containing input images"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        required=True,
        help="Directory for processed images and profiling results"
    )
    
    parser.add_argument(
        "--stress-test",
        action="store_true",
        help="Run stress test with multiple iterations and parameter variations"
    )
    
    parser.add_argument(
        "--iterations",
        type=int,
        default=5,
        help="Number of iterations for stress testing"
    )
    
    parser.add_argument(
        "--params-file",
        help="JSON file containing parameter variations for stress testing"
    )
    
    return parser.parse_args(args)

def load_param_variations(params_file: str) -> List[dict]:
    """
    Load parameter variations from a JSON file.
    
    Args:
        params_file: Path to JSON file containing parameter variations
        
    Returns:
        List of parameter dictionaries
    """
    with open(params_file, 'r') as f:
        return json.load(f)

def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the profiling CLI.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parsed_args = parse_args(args)
    
    try:
        # Create profiler
        profiler = ImageProcessorProfiler(
            os.path.join(parsed_args.output_dir, 'profiling_results')
        )
        
        if parsed_args.stress_test:
            # Load parameter variations if specified
            param_variations = None
            if parsed_args.params_file:
                param_variations = load_param_variations(parsed_args.params_file)
            
            # Run stress test
            results = profiler.stress_test(
                parsed_args.input_dir,
                os.path.join(parsed_args.output_dir, 'stress_test_output'),
                parsed_args.iterations,
                param_variations
            )
            
            # Save and visualize results for each iteration
            for i, result in enumerate(results):
                profiler.visualize_results(result)
                profiler.save_results(result)
                
        else:
            # Run single profiling session
            results = profiler.profile_processing(
                parsed_args.input_dir,
                os.path.join(parsed_args.output_dir, 'processed_images')
            )
            
            # Generate visualizations and save results
            profiler.visualize_results(results)
            profiler.save_results(results)
            
        return 0
        
    except Exception as e:
        print(f"Error during profiling: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())