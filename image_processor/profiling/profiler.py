"""
Profiling utilities for image processing operations.
"""

import json
import time
from contextlib import contextmanager
from typing import Dict, Any
import psutil
import os

class ProcessingProfiler:
    """Profile image processing operations and save results."""
    
    def __init__(self, output_path: str):
        """
        Initialize the profiler.
        
        Args:
            output_path: Path where the profiling report will be saved
        """
        self.output_path = output_path
        self.start_time = None
        self.end_time = None
        self.metrics = {}
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Gather system information."""
        cpu_info = {
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
        }
        
        memory = psutil.virtual_memory()
        memory_info = {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent
        }
        
        return {
            'cpu': cpu_info,
            'memory': memory_info,
            'platform': os.uname().sysname
        }
    
    def start(self):
        """Start profiling."""
        self.start_time = time.time()
        self.metrics['system_info'] = self._get_system_info()
    
    def stop(self):
        """Stop profiling and save results."""
        self.end_time = time.time()
        
        self.metrics.update({
            'execution_time': self.end_time - self.start_time,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'final_system_info': self._get_system_info()
        })
        
        # Save profiling results
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()