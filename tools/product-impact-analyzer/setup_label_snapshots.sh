#!/bin/bash
#
# Setup Daily Label Snapshots via LaunchAgent
#
# This script creates a LaunchAgent that runs label snapshots daily at 7 AM
# Uses fetch_labels_api.py to fetch all product labels via Google Ads API
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_PATH="$HOME/Library/LaunchAgents/com.petesbrain.label-snapshots.plist"

echo "Setting up Daily Label Snapshots..."
echo

# Check if Python virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Error: Virtual environment not found at $SCRIPT_DIR/.venv"
    echo "Please run: cd $SCRIPT_DIR && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Check if google-ads.yaml exists
if [ ! -f "$HOME/google-ads.yaml" ]; then
    echo "Error: Google Ads configuration not found at ~/google-ads.yaml"
    echo "Please configure Google Ads API credentials first"
    exit 1
fi

# Create LaunchAgent plist
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.label-snapshots</string>

    <key>ProgramArguments</key>
    <array>
        <string>${SCRIPT_DIR}/.venv/bin/python3</string>
        <string>${SCRIPT_DIR}/fetch_labels_api.py</string>
        <string>--all</string>
    </array>

    <key>WorkingDirectory</key>
    <string>${SCRIPT_DIR}</string>

    <key>StandardOutPath</key>
    <string>${HOME}/.petesbrain-label-snapshots.log</string>

    <key>StandardErrorPath</key>
    <string>${HOME}/.petesbrain-label-snapshots-error.log</string>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

echo "✅ Created LaunchAgent plist at: $PLIST_PATH"
echo

# Load the LaunchAgent
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "✅ LaunchAgent loaded successfully"
echo
echo "Schedule: Daily at 7:00 AM"
echo "Logs: ~/.petesbrain-label-snapshots.log"
echo "Error log: ~/.petesbrain-label-snapshots-error.log"
echo
echo "Coverage: 100% of all products across 8 clients via Google Ads API"
echo
echo "To check status:"
echo "  launchctl list | grep label-snapshots"
echo
echo "To test manually:"
echo "  cd $SCRIPT_DIR && .venv/bin/python3 fetch_labels_api.py --all"
echo
echo "To unload:"
echo "  launchctl unload $PLIST_PATH"
echo
