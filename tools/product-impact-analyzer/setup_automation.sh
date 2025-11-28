#!/bin/bash
#
# Product Impact Analyzer - Phase 2 Automation Setup
#
# Sets up weekly automated analysis every Tuesday at 9 AM
#
# Usage:
#   ./setup_automation.sh

set -e  # Exit on error

# Source bashrc to get environment variables
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

echo "=========================================================================="
echo "Product Impact Analyzer - Phase 2 Automation Setup"
echo "=========================================================================="
echo ""

# Configuration
TOOL_DIR="/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer"
PLIST_FILE="com.petesbrain.product-impact-analyzer.plist"
PLIST_SOURCE="$TOOL_DIR/$PLIST_FILE"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_FILE"

# Step 1: Check prerequisites
echo "Step 1: Checking prerequisites..."

if [ ! -d "$TOOL_DIR" ]; then
    echo "ERROR: Tool directory not found: $TOOL_DIR"
    exit 1
fi

if [ ! -f "$TOOL_DIR/run_automated_analysis.py" ]; then
    echo "ERROR: Automation script not found"
    exit 1
fi

# Check for virtual environment
if [ ! -d "$TOOL_DIR/.venv" ]; then
    echo "  Creating virtual environment..."
    cd "$TOOL_DIR"
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
    echo "  ✓ Virtual environment created"
else
    echo "  ✓ Virtual environment exists"
fi

# Step 2: Get API keys from environment
echo ""
echo "Step 2: Configuring environment variables..."

# Check for ANTHROPIC_API_KEY
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY not set"
    echo "Please set it in your ~/.bashrc or ~/.zshrc:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi
echo "  ✓ ANTHROPIC_API_KEY found"

# Check for GMAIL_APP_PASSWORD (optional but recommended)
if [ -z "$GMAIL_APP_PASSWORD" ]; then
    echo "  ⚠ Warning: GMAIL_APP_PASSWORD not set"
    echo "  Email delivery will be disabled"
    echo "  To enable email, set in ~/.bashrc or ~/.zshrc:"
    echo "    export GMAIL_APP_PASSWORD='your-app-password'"
    GMAIL_PASSWORD=""
else
    echo "  ✓ GMAIL_APP_PASSWORD found"
    GMAIL_PASSWORD="$GMAIL_APP_PASSWORD"
fi

# Step 3: Create LaunchAgent plist
echo ""
echo "Step 3: Creating LaunchAgent configuration..."

# Read template
if [ ! -f "$PLIST_SOURCE" ]; then
    echo "ERROR: Plist template not found: $PLIST_SOURCE"
    exit 1
fi

# Create temp plist with substituted values
TEMP_PLIST=$(mktemp)
cat "$PLIST_SOURCE" | \
    sed "s|WILL_BE_REPLACED_BY_SETUP_SCRIPT|$ANTHROPIC_API_KEY|g" | \
    sed "s|<string>WILL_BE_REPLACED_BY_SETUP_SCRIPT</string>|<string>$GMAIL_PASSWORD</string>|g" \
    > "$TEMP_PLIST"

# Install plist
mkdir -p "$HOME/Library/LaunchAgents"
cp "$TEMP_PLIST" "$PLIST_DEST"
rm "$TEMP_PLIST"

echo "  ✓ LaunchAgent configuration installed to:"
echo "    $PLIST_DEST"

# Step 4: Load LaunchAgent
echo ""
echo "Step 4: Loading LaunchAgent..."

# Unload if already loaded
if launchctl list | grep -q "com.petesbrain.product-impact-analyzer"; then
    echo "  Unloading existing LaunchAgent..."
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
fi

# Load new configuration
launchctl load "$PLIST_DEST"
echo "  ✓ LaunchAgent loaded"

# Verify it's running
sleep 1
if launchctl list | grep -q "com.petesbrain.product-impact-analyzer"; then
    echo "  ✓ LaunchAgent is active"
else
    echo "  ⚠ Warning: LaunchAgent may not have loaded correctly"
fi

# Step 5: Configure email recipient
echo ""
echo "Step 5: Email configuration..."

CONFIG_FILE="$TOOL_DIR/config.json"

# Check current email configuration
EMAIL_TO=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['alert_settings']['email_to'])" 2>/dev/null || echo "")

if [ "$EMAIL_TO" == "your-email@example.com" ] || [ -z "$EMAIL_TO" ]; then
    echo "  ⚠ Email recipient not configured in config.json"
    echo ""
    read -p "  Enter email address for weekly reports: " USER_EMAIL

    if [ -n "$USER_EMAIL" ]; then
        # Update config.json with proper email
        python3 << EOF
import json
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)
config['alert_settings']['email_to'] = '$USER_EMAIL'
config['alert_settings']['email_enabled'] = True
with open('$CONFIG_FILE', 'w') as f:
    json.dump(config, f, indent=2)
print("  ✓ Email configured: $USER_EMAIL")
EOF
    else
        echo "  ⚠ Skipping email configuration - you can update config.json manually later"
    fi
else
    echo "  ✓ Email already configured: $EMAIL_TO"
fi

# Step 6: Test run (optional)
echo ""
echo "Step 6: Testing automation (optional)..."
echo ""
read -p "Run a test analysis now? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running test analysis (dry-run mode)..."
    cd "$TOOL_DIR"
    .venv/bin/python3 run_automated_analysis.py --dry-run --test
    echo ""
    echo "  ✓ Test complete - check output above"
fi

# Step 7: Summary
echo ""
echo "=========================================================================="
echo "✓ SETUP COMPLETE"
echo "=========================================================================="
echo ""
echo "Schedule:"
echo "  Every Tuesday at 9:00 AM"
echo ""
echo "What it does:"
echo "  1. Fetches product changes from Google Sheets"
echo "  2. Fetches Google Ads performance data"
echo "  3. Analyzes impact of product changes"
echo "  4. Generates HTML report"
echo "  5. Sends email report (if configured)"
echo "  6. Saves to history for trend tracking"
echo ""
echo "Logs:"
echo "  ~/.petesbrain-product-impact-analyzer.log"
echo "  ~/.petesbrain-product-impact-analyzer-error.log"
echo ""
echo "Management commands:"
echo "  View status:  launchctl list | grep product-impact"
echo "  View logs:    tail -f ~/.petesbrain-product-impact-analyzer.log"
echo "  Manual run:   cd $TOOL_DIR && .venv/bin/python3 run_automated_analysis.py --test"
echo "  Reload:       launchctl unload ~/Library/LaunchAgents/$PLIST_FILE &&"
echo "                launchctl load ~/Library/LaunchAgents/$PLIST_FILE"
echo ""
echo "IMPORTANT:"
echo "  Phase 2 automation requires MCP integration for data fetching."
echo "  Until MCP is integrated, you'll need to manually fetch data via Claude Code."
echo "  See: python3 fetch_data.py for instructions"
echo ""
echo "=========================================================================="
