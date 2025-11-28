#!/bin/bash
#
# Setup Facebook Specifications Automation
#
# This script loads the LaunchAgents for Facebook specs monitoring and processing
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

echo "============================================================"
echo "  Facebook Specifications Automation Setup"
echo "============================================================"
echo ""

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCH_AGENTS_DIR"

# Copy plist files
echo "📋 Copying LaunchAgent plist files..."
cp "$SCRIPT_DIR/com.petesbrain.facebook-specs-monitor.plist" "$LAUNCH_AGENTS_DIR/"
cp "$SCRIPT_DIR/com.petesbrain.facebook-specs-processor.plist" "$LAUNCH_AGENTS_DIR/"

# Unload existing agents if they exist (to avoid conflicts)
echo ""
echo "🔄 Unloading existing agents (if any)..."
launchctl unload "$LAUNCH_AGENTS_DIR/com.petesbrain.facebook-specs-monitor.plist" 2>/dev/null || true
launchctl unload "$LAUNCH_AGENTS_DIR/com.petesbrain.facebook-specs-processor.plist" 2>/dev/null || true

# Load the agents
echo ""
echo "🚀 Loading LaunchAgents..."
launchctl load "$LAUNCH_AGENTS_DIR/com.petesbrain.facebook-specs-monitor.plist"
launchctl load "$LAUNCH_AGENTS_DIR/com.petesbrain.facebook-specs-processor.plist"

# Verify they're loaded
echo ""
echo "✅ Verifying agents are loaded..."
launchctl list | grep facebook-specs || echo "⚠️  Agents not found in launchctl list"

echo ""
echo "============================================================"
echo "  Setup Complete!"
echo "============================================================"
echo ""
echo "📅 Monitor Schedule:"
echo "   - Runs every Sunday at 2:00 AM"
echo "   - Checks Meta/Facebook documentation for updates"
echo ""
echo "🔄 Processor Schedule:"
echo "   - Runs every 2 hours (7200 seconds)"
echo "   - Processes files from inbox folders"
echo ""
echo "📁 Inbox Locations:"
echo "   - Meta rep emails: facebook-specifications/_inbox/meta-rep-emails/"
echo "   - Meeting notes: facebook-specifications/_inbox/meeting-notes/"
echo "   - Manual additions: facebook-specifications/_inbox/manual-additions/"
echo ""
echo "📊 Logs:"
echo "   - Monitor: ~/.petesbrain-facebook-specs-monitor.log"
echo "   - Processor: ~/.petesbrain-facebook-specs-processor.log"
echo ""
echo "🧪 Test manually:"
echo "   python3 agents/facebook-specs-monitor/facebook-specs-monitor.py"
echo "   python3 agents/facebook-specs-processor/facebook-specs-processor.py"
echo ""

