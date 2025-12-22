#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# SET YOUR ANTHROPIC API KEY HERE
export ANTHROPIC_API_KEY="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"

echo "=========================================="
echo "Google Ads Text Generator"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "First time setup - Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo ""
echo "Starting application..."
echo "Opening browser in 3 seconds..."
echo ""
echo "The app will open at: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server when done"
echo "=========================================="
echo ""

# Wait 3 seconds then open browser
(sleep 3 && open http://localhost:5001) &

# Start Flask app
python3 app.py
