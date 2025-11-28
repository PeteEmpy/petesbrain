#!/bin/bash

# Google Ads Text Generator - Start Script

echo "=========================================="
echo "Google Ads Text Generator"
echo "=========================================="
echo ""

# Load environment variables from .env file first (most reliable)
if [ -f .env ]; then
    echo "Loading environment from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Fallback: Load environment variables from shell config
if [ -z "$ANTHROPIC_API_KEY" ]; then
    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi
    if [ -f ~/.zshrc ]; then
        source ~/.zshrc
    fi
fi

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY environment variable is not set"
    echo ""
    echo "Option 1 (Recommended): Create a .env file in this directory:"
    echo "  echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env"
    echo ""
    echo "Option 2: Add to your shell config (~/.bashrc or ~/.zshrc):"
    echo "  export ANTHROPIC_API_KEY='sk-ant-...'"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Installing dependencies..."
    source .venv/bin/activate
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

echo ""
echo "Starting Flask application..."
echo "The app will be available at: http://localhost:5001"
echo "Opening browser automatically..."
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Open browser after a short delay (let Flask start first)
(sleep 3 && open http://localhost:5001) &

.venv/bin/python app.py
