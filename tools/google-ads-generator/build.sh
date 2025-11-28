#!/bin/bash

# Google Ads Text Generator - Build Script
# Packages the application as a standalone macOS .app

echo "=========================================="
echo "Google Ads Text Generator - Build Script"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Building desktop application..."
echo "This may take a few minutes..."
echo ""

# Clean previous builds
rm -rf build dist

# Build with PyInstaller
pyinstaller desktop.spec

echo ""
if [ -d "dist/Google Ads Text Generator.app" ]; then
    echo "=========================================="
    echo "✅ Build successful!"
    echo "=========================================="
    echo ""
    echo "Application created at:"
    echo "  dist/Google Ads Text Generator.app"
    echo ""
    echo "To run the app:"
    echo "  1. Open the 'dist' folder"
    echo "  2. Double-click 'Google Ads Text Generator.app'"
    echo ""
    echo "Or run from terminal:"
    echo "  open 'dist/Google Ads Text Generator.app'"
    echo ""
else
    echo "=========================================="
    echo "❌ Build failed!"
    echo "=========================================="
    echo "Check the output above for errors."
    exit 1
fi
