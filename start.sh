#!/bin/bash

echo "🚀 PROJECT NIV - Starting Production Dashboard System"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python is not installed"
        echo "Please install Python 3.8+ from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python is installed"
echo ""

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not available"
    echo "Please ensure pip is installed with Python"
    exit 1
fi

echo "✅ pip is available"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirement.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully!"
echo ""

# Run the production system
echo "🚀 Starting PROJECT NIV Production System..."
echo ""
$PYTHON_CMD production_main.py

echo ""
echo "Press any key to continue..."
read -n 1