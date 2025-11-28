#!/bin/bash

# Report Generator - Startup Script

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "========================================="
echo "Report Generator - Starting Up"
echo "========================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check for ANTHROPIC_API_KEY (optional, for future AI features)
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "Note: ANTHROPIC_API_KEY not set (optional for basic functionality)"
    echo ""
fi

# Start Flask app
echo ""
echo "========================================="
echo "Report Generator is running!"
echo "========================================="
echo ""
echo "Web Interface: http://localhost:5002"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
