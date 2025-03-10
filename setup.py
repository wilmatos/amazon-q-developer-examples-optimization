"""
Setup script for the image processor package.
"""

from setuptools import setup, find_packages

setup(
    name="image-processor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Pillow>=9.0.0",
        "matplotlib>=3.5.0",
        "memory_profiler>=0.60.0",
        "psutil>=5.9.0",
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "image-processor=image_processor.cli:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    author="AWS",
    author_email="example@example.com",
    description="A Python package for applying various image transformations",
    keywords="image, processing, transformations",
    python_requires=">=3.8",
)