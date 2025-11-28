#!/bin/bash
# Setup Merchant Center Disapproval Monitoring

set -e  # Exit on error

echo "=========================================="
echo "Merchant Center Disapproval Monitor Setup"
echo "=========================================="
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_FILE="$HOME/Library/LaunchAgents/com.petesbrain.disapproval-monitor.plist"

# Check for required environment variables
echo "Checking environment variables..."

if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "❌ GOOGLE_APPLICATION_CREDENTIALS not set"
    echo ""
    echo "Please add to ~/.bashrc or ~/.zshrc:"
    echo "export GOOGLE_APPLICATION_CREDENTIALS='/path/to/credentials.json'"
    exit 1
fi

if [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "❌ Credentials file not found: $GOOGLE_APPLICATION_CREDENTIALS"
    exit 1
fi

if [ -z "$GMAIL_APP_PASSWORD" ]; then
    echo "⚠️  GMAIL_APP_PASSWORD not set - email alerts will not work"
    echo ""
    echo "To enable email alerts, add to ~/.bashrc or ~/.zshrc:"
    echo "export GMAIL_APP_PASSWORD='your-gmail-app-password'"
    echo ""
    read -p "Continue without email alerts? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✓ Environment variables OK"
echo ""

# Check Python virtual environment
echo "Checking Python virtual environment..."

if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "❌ Virtual environment not found"
    echo "Run ./setup_automation.sh first"
    exit 1
fi

echo "✓ Virtual environment OK"
echo ""

# Create LaunchAgent plist
echo "Creating LaunchAgent..."

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.disapproval-monitor</string>

    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/.venv/bin/python3</string>
        <string>$SCRIPT_DIR/disapproval_monitor.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>6</integer>  <!-- 6 AM -->
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>12</integer>  <!-- 12 PM (noon) -->
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>18</integer>  <!-- 6 PM -->
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>0</integer>  <!-- 12 AM (midnight) -->
            <key>Minute</key>
            <integer>0</integer>
        </dict>
    </array>

    <key>EnvironmentVariables</key>
    <dict>
        <key>GOOGLE_APPLICATION_CREDENTIALS</key>
        <string>$GOOGLE_APPLICATION_CREDENTIALS</string>
EOF

if [ -n "$GMAIL_APP_PASSWORD" ]; then
cat >> "$PLIST_FILE" << EOF
        <key>GMAIL_APP_PASSWORD</key>
        <string>$GMAIL_APP_PASSWORD</string>
EOF
fi

cat >> "$PLIST_FILE" << EOF
    </dict>

    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>

    <key>StandardOutPath</key>
    <string>$HOME/.petesbrain-disapproval-monitor.log</string>

    <key>StandardErrorPath</key>
    <string>$HOME/.petesbrain-disapproval-monitor-error.log</string>

    <key>RunAtLoad</key>
    <false/>  <!-- Don't run on load, only on schedule -->

    <key>Nice</key>
    <integer>1</integer>  <!-- Lower priority -->
</dict>
</plist>
EOF

echo "✓ LaunchAgent plist created"
echo ""

# Load LaunchAgent
echo "Loading LaunchAgent..."

# Unload if already loaded
launchctl unload "$PLIST_FILE" 2>/dev/null || true

# Load new version
launchctl load "$PLIST_FILE"

if launchctl list | grep -q "com.petesbrain.disapproval-monitor"; then
    echo "✓ LaunchAgent loaded successfully"
else
    echo "❌ Failed to load LaunchAgent"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Disapproval monitoring will run every 6 hours:"
echo "  - 6:00 AM"
echo "  - 12:00 PM (noon)"
echo "  - 6:00 PM"
echo "  - 12:00 AM (midnight)"
echo ""
echo "Alerts will only be sent during business hours (9 AM - 6 PM, weekdays)"
echo ""
echo "Logs:"
echo "  Standard: ~/.petesbrain-disapproval-monitor.log"
echo "  Errors:   ~/.petesbrain-disapproval-monitor-error.log"
echo ""
echo "Manual commands:"
echo "  # Test run (ignore business hours)"
echo "  cd $SCRIPT_DIR"
echo "  .venv/bin/python3 disapproval_monitor.py --test"
echo ""
echo "  # Check specific client"
echo "  .venv/bin/python3 disapproval_monitor.py --client \"Tree2mydoor\" --test"
echo ""
echo "  # View logs"
echo "  tail -f ~/.petesbrain-disapproval-monitor.log"
echo ""
echo "  # Reload LaunchAgent (after changes)"
echo "  launchctl unload $PLIST_FILE"
echo "  launchctl load $PLIST_FILE"
echo ""

# Offer to run test
read -p "Run test check now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running test check..."
    echo ""
    cd "$SCRIPT_DIR"
    .venv/bin/python3 disapproval_monitor.py --test
fi

echo ""
echo "Setup complete!"
