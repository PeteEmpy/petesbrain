#!/bin/bash

# Google Photos MCP Server - OAuth Setup Script
# This script sets up the Python environment and initializes OAuth authentication

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "========================================="
echo "Google Photos MCP Server - OAuth Setup"
echo "========================================="
echo ""

# Check for credentials.json
if [ ! -f "credentials.json" ]; then
    echo "❌ ERROR: credentials.json not found!"
    echo ""
    echo "Please follow these steps:"
    echo "1. Read GCP-SETUP-GUIDE.md for detailed instructions"
    echo "2. Download OAuth credentials from Google Cloud Console"
    echo "3. Save as: $SCRIPT_DIR/credentials.json"
    echo ""
    exit 1
fi

echo "✓ credentials.json found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Run OAuth flow
echo "========================================="
echo "Starting OAuth 2.0 Flow"
echo "========================================="
echo ""
echo "A browser window will open for you to:"
echo "1. Sign in to your Google account"
echo "2. Grant access to Google Photos"
echo "3. The token will be saved to token.json"
echo ""
echo "Press Enter to continue..."
read

# Run a test authentication
python3 - <<EOF
import sys
sys.path.insert(0, '.')

from server import GooglePhotosService

try:
    print("\n🔐 Initializing OAuth flow...\n")
    service = GooglePhotosService()
    print("\n✅ SUCCESS! OAuth authentication complete.")
    print(f"✅ Token saved to: token.json")
    print("\nYou can now use the Google Photos MCP server.")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    sys.exit(1)
EOF

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Update .mcp.json to enable the server (see README.md)"
echo "2. Restart Claude Code"
echo "3. Test with: mcp__google-photos__list_albums"
echo ""
