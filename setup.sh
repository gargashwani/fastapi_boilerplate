#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Make artisan executable
chmod +x artisan.py

echo "Setup complete! You can now run:"
echo "source venv/bin/activate"
echo "./artisan.py serve" 