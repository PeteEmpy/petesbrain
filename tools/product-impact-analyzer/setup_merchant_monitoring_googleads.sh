#!/bin/bash
#
# Setup Merchant Center Monitoring via Google Ads API
# Runs every 6 hours at 6 AM, 12 PM, 6 PM, 12 AM
# Uses existing OAuth credentials - zero additional setup required
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
LAUNCH_AGENT_FILE="$LAUNCH_AGENT_DIR/com.petesbrain.merchant-center.plist"
LOG_FILE="$HOME/.petesbrain-merchant-center.log"

echo "=========================================="
echo "Merchant Center Monitoring Setup"
echo "(via Google Ads API - zero setup required)"
echo "=========================================="
echo ""

# Check if google-ads.yaml exists
GOOGLE_ADS_YAML="$HOME/google-ads.yaml"
if [ ! -f "$GOOGLE_ADS_YAML" ]; then
    echo "❌ ERROR: google-ads.yaml not found at:"
    echo "   $GOOGLE_ADS_YAML"
    echo ""
    echo "This file contains OAuth credentials for Google Ads API."
    exit 1
fi

echo "✓ Found google-ads.yaml with OAuth credentials"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "❌ ERROR: Virtual environment not found at:"
    echo "   $SCRIPT_DIR/.venv"
    echo ""
    echo "Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

echo "✓ Found virtual environment"

# Test the script works
echo "✓ Testing script..."
$SCRIPT_DIR/.venv/bin/python3 $SCRIPT_DIR/merchant_center_via_google_ads.py --client "HappySnapGifts" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Script test successful"
else
    echo "❌ ERROR: Script test failed"
    echo "Try running manually: .venv/bin/python3 merchant_center_via_google_ads.py --client \"HappySnapGifts\""
    exit 1
fi

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
        <string>$SCRIPT_DIR/merchant_center_via_google_ads.py</string>
        <string>--report</string>
        <string>--save</string>
    </array>

    <key>EnvironmentVariables</key>
    <dict>
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
echo "Method: Google Ads API (shopping_performance_view)"
echo "Detects: Products with 0 impressions in last 30 days"
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
echo "✅ Zero additional setup required - works for all clients now!"
echo ""
