#!/bin/bash
#
# Product Impact Analyzer - Real-Time Monitoring Setup
#
# Sets up daily monitoring for critical product changes
#
# Usage:
#   ./setup_monitoring.sh

set -e  # Exit on error

# Source bashrc to get environment variables
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

echo "=========================================================================="
echo "Product Impact Analyzer - Real-Time Monitoring Setup"
echo "=========================================================================="
echo ""

# Configuration
TOOL_DIR="/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer"
PLIST_FILE="com.petesbrain.product-monitor.plist"
PLIST_SOURCE="$TOOL_DIR/$PLIST_FILE"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_FILE"

# Step 1: Check prerequisites
echo "Step 1: Checking prerequisites..."

if [ ! -f "$TOOL_DIR/monitor.py" ]; then
    echo "ERROR: monitor.py not found"
    exit 1
fi

if [ ! -d "$TOOL_DIR/.venv" ]; then
    echo "ERROR: Virtual environment not found"
    echo "Please run ./setup_automation.sh first"
    exit 1
fi

echo "  ✓ Prerequisites OK"

# Step 2: Make monitor.py executable
chmod +x "$TOOL_DIR/monitor.py"
echo "  ✓ monitor.py made executable"

# Step 3: Check environment variables
echo ""
echo "Step 2: Checking environment variables..."

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY not set"
    exit 1
fi
echo "  ✓ ANTHROPIC_API_KEY found"

if [ -z "$GMAIL_APP_PASSWORD" ]; then
    echo "ERROR: GMAIL_APP_PASSWORD not set"
    exit 1
fi
echo "  ✓ GMAIL_APP_PASSWORD found"

# Step 4: Create LaunchAgent plist
echo ""
echo "Step 3: Creating LaunchAgent configuration..."

# Read template and substitute values
TEMP_PLIST=$(mktemp)
cat "$PLIST_SOURCE" | \
    sed "s|WILL_BE_REPLACED_BY_SETUP_SCRIPT|$ANTHROPIC_API_KEY|g" | \
    sed "s|<string>WILL_BE_REPLACED_BY_SETUP_SCRIPT</string>|<string>$GMAIL_APP_PASSWORD</string>|g" \
    > "$TEMP_PLIST"

# Install plist
mkdir -p "$HOME/Library/LaunchAgents"
cp "$TEMP_PLIST" "$PLIST_DEST"
rm "$TEMP_PLIST"

echo "  ✓ LaunchAgent configuration installed"

# Step 5: Load LaunchAgent
echo ""
echo "Step 4: Loading LaunchAgent..."

# Unload if already loaded
if launchctl list | grep -q "com.petesbrain.product-monitor"; then
    echo "  Unloading existing LaunchAgent..."
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
fi

# Load new configuration
launchctl load "$PLIST_DEST"
echo "  ✓ LaunchAgent loaded"

# Verify it's running
sleep 1
if launchctl list | grep -q "com.petesbrain.product-monitor"; then
    echo "  ✓ LaunchAgent is active"
else
    echo "  ⚠ Warning: LaunchAgent may not have loaded correctly"
fi

# Step 6: Configure alert thresholds
echo ""
echo "Step 5: Monitoring configuration..."
echo ""
echo "Current alert thresholds (edit config.json to change):"
echo "  Revenue drop alert: £500"
echo "  Revenue spike alert: £500"
echo "  Click drop alert: 50%"
echo "  Missing products alert: 5+ products"
echo "  Alert hours: 9 AM - 6 PM (weekdays only)"
echo ""

read -p "Would you like to customize these thresholds? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "To customize, edit: $TOOL_DIR/config.json"
    echo "Look for the 'monitoring' section and adjust values."
    echo ""
    read -p "Press Enter to continue..."
fi

# Step 7: Test run (optional)
echo ""
echo "Step 6: Testing monitoring (optional)..."
echo ""
read -p "Run a test check now? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running test monitoring check..."
    cd "$TOOL_DIR"
    .venv/bin/python3 monitor.py --test
    echo ""
    echo "  ✓ Test complete - check output above"
fi

# Step 8: Summary
echo ""
echo "=========================================================================="
echo "✓ MONITORING SETUP COMPLETE"
echo "=========================================================================="
echo ""
echo "Schedule:"
echo "  Runs daily at 10:00 AM"
echo ""
echo "What it monitors:"
echo "  - Revenue drops > £500/day (critical alert)"
echo "  - Revenue spikes > £500/day (opportunity alert)"
echo "  - Click drops > 50%"
echo "  - Products missing from feed (5+)"
echo ""
echo "Alert delivery:"
echo "  Email: petere@roksys.co.uk (during business hours only)"
echo "  Slack: Not configured (add webhook to config.json to enable)"
echo ""
echo "Logs:"
echo "  ~/.petesbrain-product-monitor.log"
echo "  ~/.petesbrain-product-monitor-error.log"
echo ""
echo "Management commands:"
echo "  View status:  launchctl list | grep product-monitor"
echo "  View logs:    tail -f ~/.petesbrain-product-monitor.log"
echo "  Manual run:   cd $TOOL_DIR && .venv/bin/python3 monitor.py --test"
echo "  Reload:       launchctl unload ~/Library/LaunchAgents/$PLIST_FILE &&"
echo "                launchctl load ~/Library/LaunchAgents/$PLIST_FILE"
echo ""
echo "Configuration:"
echo "  Edit alert thresholds: $TOOL_DIR/config.json (monitoring section)"
echo "  Add Slack webhook: config.json -> monitoring.slack_webhook"
echo "  Change schedule: ~/Library/LaunchAgents/$PLIST_FILE"
echo ""
echo "=========================================================================="
