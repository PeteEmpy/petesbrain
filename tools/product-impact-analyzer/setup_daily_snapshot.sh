#!/bin/bash
#
# Setup Daily Product Feed Snapshot via LaunchAgent
#
# This script creates a LaunchAgent that runs the product snapshot daily at 6 AM
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_PATH="$HOME/Library/LaunchAgents/com.petesbrain.product-snapshot.plist"

echo "Setting up Daily Product Feed Snapshot..."
echo

# Check if Python virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Error: Virtual environment not found at $SCRIPT_DIR/.venv"
    echo "Please run: cd $SCRIPT_DIR && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Create LaunchAgent plist
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.product-snapshot</string>

    <key>ProgramArguments</key>
    <array>
        <string>${SCRIPT_DIR}/.venv/bin/python3</string>
        <string>${SCRIPT_DIR}/snapshot_product_feed.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>${SCRIPT_DIR}</string>

    <key>StandardOutPath</key>
    <string>${HOME}/.petesbrain-product-snapshot.log</string>

    <key>StandardErrorPath</key>
    <string>${HOME}/.petesbrain-product-snapshot-error.log</string>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>6</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

echo "Created LaunchAgent plist at: $PLIST_PATH"
echo

# Load the LaunchAgent
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "✅ LaunchAgent loaded successfully"
echo
echo "Schedule: Daily at 6:00 AM"
echo "Logs: ~/.petesbrain-product-snapshot.log"
echo "Error log: ~/.petesbrain-product-snapshot-error.log"
echo
echo "To check status:"
echo "  launchctl list | grep product-snapshot"
echo
echo "To test manually:"
echo "  python3 $SCRIPT_DIR/snapshot_product_feed.py"
echo
echo "To unload:"
echo "  launchctl unload $PLIST_PATH"
echo
echo "⚠️  NOTE: This snapshot script requires Google Ads data to be fetched via Claude Code MCP."
echo "The automated run will fail until the data fetching workflow is integrated."
echo "For now, run snapshots manually via Claude Code."
