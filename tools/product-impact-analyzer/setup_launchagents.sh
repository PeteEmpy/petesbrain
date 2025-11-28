#!/bin/bash
#
# Setup LaunchAgents for Product Impact Analyzer Automation
#

echo "========================================"
echo "Product Impact Analyzer - LaunchAgents Setup"
echo "========================================"
echo ""

LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCHAGENTS_DIR"

# Copy LaunchAgent files
echo "Installing LaunchAgents..."

# 1. Daily product tracking (8:00 AM)
cp "$SCRIPT_DIR/launchagents/com.petesbrain.product-tracking.plist" "$LAUNCHAGENTS_DIR/"
echo "  ✓ Daily product tracking (8:00 AM)"

# 2. Weekly baseline calculator (Monday 7:00 AM)
cp "$SCRIPT_DIR/launchagents/com.petesbrain.baseline-calculator.plist" "$LAUNCHAGENTS_DIR/"
echo "  ✓ Weekly baseline calculator (Monday 7:00 AM)"

# 3. Weekly impact report (Monday 9:00 AM)
cp "$SCRIPT_DIR/launchagents/com.petesbrain.weekly-impact-report.plist" "$LAUNCHAGENTS_DIR/"
echo "  ✓ Weekly impact report (Monday 9:00 AM)"

echo ""
echo "Loading LaunchAgents..."

# Load the agents
launchctl load "$LAUNCHAGENTS_DIR/com.petesbrain.product-tracking.plist" 2>/dev/null
echo "  ✓ Loaded product-tracking"

launchctl load "$LAUNCHAGENTS_DIR/com.petesbrain.baseline-calculator.plist" 2>/dev/null
echo "  ✓ Loaded baseline-calculator"

launchctl load "$LAUNCHAGENTS_DIR/com.petesbrain.weekly-impact-report.plist" 2>/dev/null
echo "  ✓ Loaded weekly-impact-report"

echo ""
echo "========================================"
echo "SETUP COMPLETE"
echo "========================================"
echo ""
echo "Automation Schedule:"
echo "  Daily (8:00 AM):"
echo "    - Product feed tracker"
echo "    - Product change detector"
echo ""
echo "  Weekly (Monday):"
echo "    - 7:00 AM: Baseline calculator"
echo "    - 9:00 AM: Weekly impact report"
echo ""
echo "Check status:"
echo "  launchctl list | grep petesbrain"
echo ""
echo "View logs:"
echo "  tail -f ~/.petesbrain-product-tracking.log"
echo "  tail -f ~/.petesbrain-baseline-calculator.log"
echo "  tail -f ~/.petesbrain-weekly-impact-report.log"
echo ""
