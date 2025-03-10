"""
Utility functions for generating test images.
"""

import os
import logging
from PIL import Image, ImageDraw
import numpy as np

logger = logging.getLogger(__name__)

def generate_test_images(output_dir: str, num_images: int = 5, size: tuple = (1920, 1080)):
    """
    Generate test images with various patterns for processing.
    
    Args:
        output_dir (str): Directory where test images will be saved
        num_images (int): Number of test images to generate
        size (tuple): Size of the test images (width, height)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created directory for test images: {output_dir}")

    patterns = [
        "gradient",
        "checkerboard",
        "circles",
        "noise",
        "lines"
    ]

    for i in range(num_images):
        pattern = patterns[i % len(patterns)]
        image = _create_pattern(pattern, size)
        filename = f"test_image_{i+1}_{pattern}.png"
        filepath = os.path.join(output_dir, filename)
        image.save(filepath, "PNG")
        logger.info(f"Generated test image: {filename}")

def _create_pattern(pattern: str, size: tuple) -> Image.Image:
    """
    Create an image with the specified pattern.
    
    Args:
        pattern (str): Type of pattern to generate
        size (tuple): Image dimensions (width, height)
    
    Returns:
        Image: Generated test image
    """
    width, height = size
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    if pattern == "gradient":
        # Create a horizontal gradient
        for x in range(width):
            color = int((x / width) * 255)
            draw.line([(x, 0), (x, height)], fill=(color, color, color))

    elif pattern == "checkerboard":
        # Create a checkerboard pattern
        box_size = 100
        for i in range(0, width, box_size):
            for j in range(0, height, box_size):
                if (i + j) // box_size % 2 == 0:
                    draw.rectangle([i, j, i + box_size, j + box_size], fill='black')

    elif pattern == "circles":
        # Draw concentric circles
        max_radius = min(width, height) // 2
        center = (width // 2, height // 2)
        for r in range(0, max_radius, 50):
            draw.ellipse([center[0] - r, center[1] - r,
                         center[0] + r, center[1] + r],
                        outline='black', width=2)

    elif pattern == "noise":
        # Create random noise
        pixels = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        image = Image.fromarray(pixels)

    elif pattern == "lines":
        # Draw diagonal lines
        spacing = 50
        for i in range(-height, width + height, spacing):
            draw.line([(i, 0), (i + height, height)], fill='black', width=2)

    return image