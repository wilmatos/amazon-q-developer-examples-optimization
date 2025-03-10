#!/usr/bin/env python3
"""
Script to generate static images for the optimization report.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Create reports directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Benchmark data
benchmark_data = {
    # Time comparison (in seconds)
    'time': {
        'original': 2.62,
        'optimized': 1.01,
        'improvement': 61.5
    },
    
    # CPU usage (in seconds)
    'cpu': {
        'original': 2.20,
        'optimized': 1.37,
        'improvement': 37.7
    },
    
    # Memory usage (in MB)
    'memory': {
        'original': 0.04,
        'optimized': 34.63,
        'change': -86475.0  # Negative indicates increased usage
    },
    
    # Detailed benchmark results
    'detailed_results': [
        {
            'name': "Iteration 1",
            'original': {
                'time': 2.15,
                'memory': 0.12,
                'cpu': 2.07
            },
            'optimized': {
                'time': 1.09,
                'memory': 55.88,
                'cpu': 1.34
            }
        },
        {
            'name': "Iteration 2",
            'original': {
                'time': 3.43,
                'memory': 0.00,
                'cpu': 2.47
            },
            'optimized': {
                'time': 0.94,
                'memory': 13.38,
                'cpu': 1.40
            }
        },
        {
            'name': "Iteration 3",
            'original': {
                'time': 2.28,
                'memory': 0.00,
                'cpu': 2.05
            },
            'optimized': {
                'time': 1.00,
                'memory': 34.63,
                'cpu': 1.37
            }
        }
    ]
}

# Generate time comparison chart
def generate_time_chart():
    labels = ['Original', 'Optimized']
    values = [benchmark_data['time']['original'], benchmark_data['time']['optimized']]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color=['#dc3545', '#28a745'])
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{height:.2f}s', ha='center', va='bottom')
    
    ax.set_title('Average Processing Time (seconds)', fontsize=16)
    ax.set_ylabel('Time (seconds)')
    
    # Add improvement percentage
    improvement = benchmark_data['time']['improvement']
    ax.text(1, values[1] / 2, f'{improvement:.1f}% faster', 
            ha='center', va='center', color='white', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('images/time_comparison.png', dpi=300)
    plt.close()

# Generate resource usage chart
def generate_resource_chart():
    labels = ['CPU Time', 'Memory Usage (MB)']
    original_values = [benchmark_data['cpu']['original'], benchmark_data['memory']['original']]
    optimized_values = [benchmark_data['cpu']['optimized'], benchmark_data['memory']['optimized']]
    
    x = np.arange(len(labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, original_values, width, label='Original')
    rects2 = ax.bar(x + width/2, optimized_values, width, label='Optimized')
    
    ax.set_title('Resource Usage Comparison', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    # Add value labels
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    plt.tight_layout()
    plt.savefig('images/resource_usage.png', dpi=300)
    plt.close()

# Generate iteration comparison chart
def generate_iteration_chart():
    iterations = [result['name'] for result in benchmark_data['detailed_results']]
    original_times = [result['original']['time'] for result in benchmark_data['detailed_results']]
    optimized_times = [result['optimized']['time'] for result in benchmark_data['detailed_results']]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(iterations, original_times, 'o-', color='#dc3545', label='Original')
    ax.plot(iterations, optimized_times, 'o-', color='#28a745', label='Optimized')
    
    ax.set_title('Processing Time by Iteration', fontsize=16)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Time (seconds)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('images/iteration_comparison.png', dpi=300)
    plt.close()

# Generate improvement summary chart
def generate_improvement_chart():
    labels = ['Processing Time', 'CPU Usage', 'Memory Usage']
    improvements = [
        benchmark_data['time']['improvement'],
        benchmark_data['cpu']['improvement'],
        -100  # Memory usage increased, so we cap at -100%
    ]
    
    colors = ['#28a745', '#28a745', '#dc3545']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, improvements, color=colors)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'+{height:.1f}%', ha='center', va='bottom')
        else:
            ax.text(bar.get_x() + bar.get_width()/2., height - 5,
                    f'Increased', ha='center', va='top')
    
    ax.set_title('Performance Improvements', fontsize=16)
    ax.set_ylabel('Improvement (%)')
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('images/improvement_summary.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    # Create images directory inside reports
    os.makedirs('reports/images', exist_ok=True)
    os.chdir('reports')  # Change to reports directory
    
    # Generate all charts
    generate_time_chart()
    generate_resource_chart()
    generate_iteration_chart()
    generate_improvement_chart()
    
    print("Report images generated successfully in reports/images/ directory")