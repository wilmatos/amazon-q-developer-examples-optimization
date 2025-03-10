#!/bin/bash

# Script to generate test images for the image processor
# This script checks if the input directory is empty and generates test images if needed

INPUT_DIR="data/input"
NUM_IMAGES=5
IMAGE_SIZE="1920,1080"

# Create directories if they don't exist
mkdir -p "$INPUT_DIR"
mkdir -p "data/output"

# Check if input directory is empty (excluding .gitkeep)
if [ $(find "$INPUT_DIR" -type f -not -name ".gitkeep" | wc -l) -eq 0 ]; then
    echo "Input directory is empty. Generating test images..."
    
    # Check if the image-processor command is available
    if command -v image-processor &> /dev/null; then
        image-processor -i "$INPUT_DIR" -o "data/output" --generate-test-images "$NUM_IMAGES"
        echo "Generated $NUM_IMAGES test images in $INPUT_DIR"
    else
        echo "image-processor command not found. Installing package..."
        pip install -e .
        image-processor -i "$INPUT_DIR" -o "data/output" --generate-test-images "$NUM_IMAGES"
        echo "Generated $NUM_IMAGES test images in $INPUT_DIR"
    fi
else
    echo "Input directory already contains images. Skipping generation."
    ls -la "$INPUT_DIR" | grep -v ".gitkeep"
fi

echo "Ready to run image processing tests or profiling."