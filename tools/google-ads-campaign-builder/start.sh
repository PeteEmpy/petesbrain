#!/bin/bash

# Google Ads Campaign Builder - Startup Script

echo "🚀 Starting Google Ads Campaign Builder..."
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Run this script from the google-ads-campaign-builder directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade dependencies
echo "📚 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Starting Flask server on http://127.0.0.1:5003"
echo ""
echo "⚠️  IMPORTANT: All campaigns, ad groups, and asset groups"
echo "   are created in PAUSED state for safety."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Export ANTHROPIC_API_KEY if not already set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    # Try to load from shell profile
    if [ -f "$HOME/.zshrc" ]; then
        export ANTHROPIC_API_KEY=$(grep 'export ANTHROPIC_API_KEY' ~/.zshrc 2>/dev/null | cut -d'"' -f2)
    elif [ -f "$HOME/.bashrc" ]; then
        export ANTHROPIC_API_KEY=$(grep 'export ANTHROPIC_API_KEY' ~/.bashrc 2>/dev/null | cut -d'"' -f2)
    fi
fi

# Start Flask app
python3 app.py
