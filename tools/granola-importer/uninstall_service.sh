#!/bin/bash
#
# Uninstall Granola Sync Daemon LaunchAgent
#

set -e

PLIST_NAME="com.petesbrain.granola-importer"
PLIST_FILE="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"

echo "=================================================="
echo "Granola Sync Daemon - Service Uninstaller"
echo "=================================================="
echo ""

if [ ! -f "$PLIST_FILE" ]; then
    echo "❌ Service not installed"
    exit 1
fi

# Unload and remove
launchctl unload "$PLIST_FILE" 2>/dev/null || true
rm "$PLIST_FILE"

echo "✓ Service unloaded and removed"
echo ""
echo "The daemon is no longer running and will not start automatically."
echo "To re-install, run: ./install_service.sh"
echo ""
