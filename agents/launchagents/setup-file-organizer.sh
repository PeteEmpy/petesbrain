#!/bin/bash
# Setup script for File Organizer LaunchAgent
# Installs weekly automated file organization

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PLIST_NAME="com.petesbrain.file-organizer"
PLIST_FILE="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"
SOURCE_PLIST="$SCRIPT_DIR/${PLIST_NAME}.plist"

echo "=================================================="
echo "File Organizer LaunchAgent Setup"
echo "=================================================="
echo ""

# Check if source plist exists
if [ ! -f "$SOURCE_PLIST" ]; then
    echo "❌ Error: Source plist not found at $SOURCE_PLIST"
    exit 1
fi

# Copy plist to LaunchAgents directory
echo "📋 Copying LaunchAgent plist..."
cp "$SOURCE_PLIST" "$PLIST_FILE"
echo "✓ Copied to: $PLIST_FILE"

# Unload existing agent if running
echo ""
echo "🔄 Unloading existing agent (if running)..."
launchctl unload "$PLIST_FILE" 2>/dev/null || true

# Load the agent
echo "📥 Loading LaunchAgent..."
launchctl load "$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo "✅ LaunchAgent loaded successfully"
else
    echo "❌ Failed to load LaunchAgent"
    exit 1
fi

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Schedule: Every Monday at 8:00 AM"
echo "Logs: ~/.petesbrain-file-organizer.log"
echo "Error log: ~/.petesbrain-file-organizer-error.log"
echo ""
echo "To check status:"
echo "  launchctl list | grep file-organizer"
echo ""
echo "To test manually:"
echo "  cd $PROJECT_ROOT"
echo "  python3 shared/scripts/file-organizer.py --dry-run"
echo ""
echo "To run now (dry-run):"
echo "  python3 shared/scripts/file-organizer.py --dry-run"
echo ""
echo "To run now (live):"
echo "  python3 shared/scripts/file-organizer.py"
echo ""
echo "To unload:"
echo "  launchctl unload $PLIST_FILE"
echo ""
echo "To uninstall:"
echo "  launchctl unload $PLIST_FILE && rm $PLIST_FILE"
echo ""

