#!/bin/bash
##########################################
## Price Monitoring Setup
##########################################

echo "=========================================="
echo "Price Monitoring Setup"
echo "=========================================="
echo ""

# Check environment variables
echo "Checking environment variables..."

if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "❌ GOOGLE_APPLICATION_CREDENTIALS not set"
    echo ""
    echo "Please add to ~/.bashrc or ~/.zshrc:"
    echo "export GOOGLE_APPLICATION_CREDENTIALS='/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json'"
    echo ""
    exit 1
fi

echo "✓ Environment variables OK"
echo ""

# Check Python virtual environment
echo "Checking Python virtual environment..."
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found"
    echo "Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

echo "✓ Virtual environment OK"
echo ""

# Create LaunchAgent plist
PLIST_PATH="$HOME/Library/LaunchAgents/com.petesbrain.price-monitor.plist"

echo "Creating LaunchAgent..."

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.price-monitor</string>

    <key>ProgramArguments</key>
    <array>
        <string>$PWD/.venv/bin/python3</string>
        <string>$PWD/price_tracker.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>$PWD</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>GOOGLE_APPLICATION_CREDENTIALS</key>
        <string>$GOOGLE_APPLICATION_CREDENTIALS</string>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>

    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>6</integer>
            <key>Minute</key>
            <integer>30</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>12</integer>
            <key>Minute</key>
            <integer>30</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>18</integer>
            <key>Minute</key>
            <integer>30</integer>
        </dict>
    </array>

    <key>StandardOutPath</key>
    <string>$HOME/.petesbrain-price-monitor.log</string>

    <key>StandardErrorPath</key>
    <string>$HOME/.petesbrain-price-monitor-error.log</string>

    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

echo "✓ LaunchAgent plist created"
echo ""

# Load LaunchAgent
echo "Loading LaunchAgent..."
launchctl unload "$PLIST_PATH" 2>/dev/null  # Unload if already loaded
launchctl load "$PLIST_PATH"

if [ $? -eq 0 ]; then
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
echo "Price monitoring will run 3 times daily:"
echo "  - 6:30 AM"
echo "  - 12:30 PM (noon)"
echo "  - 6:30 PM"
echo ""
echo "Price changes will be tracked and logged to:"
echo "  monitoring/prices/price_changes_YYYY-MM.json"
echo ""
echo "Logs:"
echo "  Standard: ~/.petesbrain-price-monitor.log"
echo "  Errors:   ~/.petesbrain-price-monitor-error.log"
echo ""
echo "Manual commands:"
echo "  # Track all clients"
echo "  cd $PWD"
echo "  .venv/bin/python3 price_tracker.py"
echo ""
echo "  # Track specific client"
echo "  .venv/bin/python3 price_tracker.py --client \"Tree2mydoor\""
echo ""
echo "  # Generate report"
echo "  .venv/bin/python3 price_tracker.py --report"
echo ""
echo "  # View logs"
echo "  tail -f ~/.petesbrain-price-monitor.log"
echo ""
echo "  # Reload LaunchAgent (after changes)"
echo "  launchctl unload $PLIST_PATH"
echo "  launchctl load $PLIST_PATH"
echo ""
echo ""
echo "Setup complete!"
echo ""
