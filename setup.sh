#!/bin/bash

# Install the required dependencies
echo "Installing required dependencies..."
pip install -r requirements.txt

# Run the crawling script
echo "Running the crawling script..."
cd helper
python crawl_cv_timviec365.py
cd ..

# Run the main script
echo "Running the main ETL pipeline..."
python main.py