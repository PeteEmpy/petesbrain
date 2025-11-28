#!/bin/bash
# Google Trends MCP Server Setup Script

set -e

echo "=========================================="
echo "Google Trends MCP Server Setup"
echo "=========================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

echo "1. Creating virtual environment..."
cd "$SCRIPT_DIR"
python3 -m venv .venv
echo "✅ Virtual environment created"

echo ""
echo "2. Installing dependencies..."
.venv/bin/pip install --upgrade pip > /dev/null 2>&1
.venv/bin/pip install -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "3. Verifying installation..."
.venv/bin/python -c "from pytrends.request import TrendReq; print('✅ pytrends working')"
.venv/bin/python -c "import mcp; print('✅ MCP working')"
.venv/bin/python -c "import pandas; print('✅ pandas working')"

echo ""
echo "4. Checking .mcp.json configuration..."
if grep -q "google-trends" "$PROJECT_ROOT/.mcp.json"; then
    echo "✅ Already configured in .mcp.json"
else
    echo "❌ Not found in .mcp.json"
    echo ""
    echo "Add this to $PROJECT_ROOT/.mcp.json:"
    echo ""
    echo '    "google-trends": {'
    echo '      "command": "/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server/.venv/bin/python",'
    echo '      "args": ["/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server/server.py"]'
    echo '    }'
    echo ""
fi

echo ""
echo "5. Checking LaunchAgent..."
PLIST_SOURCE="$PROJECT_ROOT/agents/launchagents/com.petesbrain.trend-monitor.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.petesbrain.trend-monitor.plist"

if [ -f "$PLIST_DEST" ]; then
    echo "✅ LaunchAgent already installed"
else
    echo "Installing LaunchAgent..."
    cp "$PLIST_SOURCE" "$PLIST_DEST"
    launchctl load "$PLIST_DEST"
    echo "✅ LaunchAgent installed and loaded"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Restart Claude Code to load the MCP server"
echo "2. Test with: 'Check Google Trends for christmas trees'"
echo "3. View integration guide: cat INTEGRATION-GUIDE.md"
echo ""
echo "Agent Status:"
launchctl list | grep petesbrain.trend-monitor || echo "Agent not yet scheduled (will run Monday 8:15 AM)"
echo ""
echo "Test the server:"
echo "  cd $SCRIPT_DIR"
echo "  .venv/bin/python test_trends.py"
echo ""
