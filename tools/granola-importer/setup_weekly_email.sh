#!/bin/bash
#
# Setup Weekly Email Summary using LaunchAgent
# Sends email every Monday at 9:00 AM
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_NAME="com.petesbrain.granola-weekly-summary"
PLIST_FILE="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python3"

echo "=================================================="
echo "Granola Weekly Summary - Email Setup"
echo "=================================================="
echo ""

# Check if config exists
if [ ! -f "$SCRIPT_DIR/config.yaml" ]; then
    echo "❌ Error: config.yaml not found"
    echo ""
    echo "Please configure email settings first:"
    echo "1. Copy config.example.yaml to config.yaml"
    echo "2. Edit config.yaml with your email settings"
    echo "3. Run this script again"
    exit 1
fi

echo "✓ Found config.yaml"

# Check if venv exists
if [ ! -x "$PYTHON_PATH" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "Please run: python3 -m venv $SCRIPT_DIR/venv"
    exit 1
fi

echo "✓ Found Python virtual environment"

# Create LaunchAgent directory if it doesn't exist
mkdir -p "$HOME/Library/LaunchAgents"

# Create plist file for weekly email
# Runs every Monday at 9:00 AM
cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>

    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_PATH}</string>
        <string>${SCRIPT_DIR}/send_weekly_summary.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>$HOME/.petesbrain-granola-weekly-email.log</string>

    <key>StandardErrorPath</key>
    <string>$HOME/.petesbrain-granola-weekly-email.log</string>

    <key>WorkingDirectory</key>
    <string>${SCRIPT_DIR}</string>
</dict>
</plist>
EOF

echo "✓ Created LaunchAgent: $PLIST_FILE"

# Load the service
launchctl unload "$PLIST_FILE" 2>/dev/null || true
launchctl load "$PLIST_FILE"

echo "✓ Service loaded and scheduled"
echo ""
echo "=================================================="
echo "Weekly Email Setup Complete!"
echo "=================================================="
echo ""
echo "Weekly summary emails will be sent:"
echo "  • Every Monday at 9:00 AM"
echo "  • To: $(grep 'recipient:' config.yaml | awk '{print $2}' | tr -d '"')"
echo "  • Logs: $HOME/.petesbrain-granola-weekly-email.log"
echo ""
echo "Test it now:"
echo "  source venv/bin/activate"
echo "  python3 send_weekly_summary.py"
echo ""
echo "Useful commands:"
echo "  Stop weekly emails: launchctl stop ${PLIST_NAME}"
echo "  Uninstall: launchctl unload $PLIST_FILE && rm $PLIST_FILE"
echo ""
