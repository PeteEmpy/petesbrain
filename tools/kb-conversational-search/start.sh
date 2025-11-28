#!/bin/bash

# PetesBrain Conversational Knowledge Search - Startup Script
# Starts the Flask backend server and opens the web interface

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🧠 Starting PetesBrain Conversational Knowledge Search..."
echo ""

# Check for virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check for Anthropic API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  Warning: ANTHROPIC_API_KEY not found in shell environment"
    echo "Trying to get it from Python (same method as kb-search.py)..."

    # Try to get it from Python - if kb-search.py works, this should too
    ANTHROPIC_API_KEY=$(python3 -c "import os; print(os.environ.get('ANTHROPIC_API_KEY', ''))" 2>/dev/null)

    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "❌ Could not find API key"
        echo "Please set your API key:"
        echo "  export ANTHROPIC_API_KEY='your-key-here'"
        echo ""
        read -p "Press Enter to continue (will fail without API key) or Ctrl+C to exit..."
    else
        echo "✅ Found API key from Python environment"
        export ANTHROPIC_API_KEY
    fi
fi

# Start server in background
echo ""
echo "Starting Flask server on http://127.0.0.1:5555"
echo ""

# Open browser after short delay
(sleep 2 && open http://127.0.0.1:5555) &

# Run server
python3 server.py
