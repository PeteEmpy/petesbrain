#!/bin/bash
#
# Setup Merchant Center Disapproval Monitoring
# Runs every 6 hours at 6 AM, 12 PM, 6 PM, 12 AM
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
LAUNCH_AGENT_FILE="$LAUNCH_AGENT_DIR/com.petesbrain.merchant-center.plist"
LOG_FILE="$HOME/.petesbrain-merchant-center.log"

echo "=========================================="
echo "Merchant Center Monitoring Setup"
echo "=========================================="
echo ""

# Check if credentials exist
CREDENTIALS_PATH="/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json"
if [ ! -f "$CREDENTIALS_PATH" ]; then
    echo "❌ ERROR: Credentials file not found at:"
    echo "   $CREDENTIALS_PATH"
    exit 1
fi

echo "✓ Found credentials file"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "❌ ERROR: Virtual environment not found at:"
    echo "   $SCRIPT_DIR/.venv"
    echo ""
    echo "Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

echo "✓ Found virtual environment"

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCH_AGENT_DIR"

# Create the plist file
cat > "$LAUNCH_AGENT_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.merchant-center</string>

    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/.venv/bin/python3</string>
        <string>$SCRIPT_DIR/merchant_center_tracker.py</string>
        <string>--report</string>
        <string>--save</string>
    </array>

    <key>EnvironmentVariables</key>
    <dict>
        <key>GOOGLE_APPLICATION_CREDENTIALS</key>
        <string>$CREDENTIALS_PATH</string>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>

    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>6</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>12</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>18</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>0</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
    </array>

    <key>StandardOutPath</key>
    <string>$LOG_FILE</string>

    <key>StandardErrorPath</key>
    <string>$LOG_FILE</string>

    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
</dict>
</plist>
EOF

echo "✓ Created LaunchAgent plist"

# Set correct permissions
chmod 644 "$LAUNCH_AGENT_FILE"
echo "✓ Set permissions"

# Unload if already loaded (ignore errors)
launchctl unload "$LAUNCH_AGENT_FILE" 2>/dev/null || true

# Load the launch agent
launchctl load "$LAUNCH_AGENT_FILE"
echo "✓ Loaded LaunchAgent"

# Create initial log file
touch "$LOG_FILE"
echo "✓ Created log file: $LOG_FILE"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Merchant Center monitoring will run at:"
echo "  • 6:00 AM"
echo "  • 12:00 PM"
echo "  • 6:00 PM"
echo "  • 12:00 AM (midnight)"
echo ""
echo "View logs:"
echo "  tail -f $LOG_FILE"
echo ""
echo "Check status:"
echo "  launchctl list | grep merchant-center"
echo ""
echo "Test manually:"
echo "  launchctl start com.petesbrain.merchant-center"
echo ""
echo "⚠️  IMPORTANT: Before this will work, you must:"
echo "  1. Grant Merchant Center access to service account"
echo "  2. See MERCHANT-CENTER-SETUP.md for instructions"
echo ""
