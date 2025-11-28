#!/bin/bash
#
# Wispr Flow Integration Setup
# Installs LaunchAgent and tests the importer
#

set -e

echo ""
echo "============================================================"
echo "Wispr Flow Integration Setup"
echo "============================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PETESBRAIN_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "✓ PetesBrain root: $PETESBRAIN_ROOT"
echo ""

# Check if Wispr Flow database exists
WISPR_DB_DIR="$HOME/Library/Application Support/Wispr Flow/backups"
if [ ! -d "$WISPR_DB_DIR" ]; then
    echo "❌ Wispr Flow database not found at:"
    echo "   $WISPR_DB_DIR"
    echo ""
    echo "   Is Wispr Flow installed?"
    exit 1
fi

echo "✓ Found Wispr Flow database"

# Check for backup files
BACKUP_COUNT=$(ls -1 "$WISPR_DB_DIR"/*.sqlite 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -eq 0 ]; then
    echo "❌ No backup files found in Wispr Flow directory"
    exit 1
fi

echo "✓ Found $BACKUP_COUNT backup file(s)"
echo ""

# Make script executable
chmod +x "$PETESBRAIN_ROOT/agents/wispr-flow-importer/wispr-flow-importer.py"
echo "✓ Made importer script executable"

# Copy LaunchAgent
PLIST_SOURCE="$PETESBRAIN_ROOT/agents/launchagents/com.petesbrain.wispr-flow-importer.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.petesbrain.wispr-flow-importer.plist"

if [ -f "$PLIST_DEST" ]; then
    echo "⚠️  LaunchAgent already exists, unloading..."
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
fi

cp "$PLIST_SOURCE" "$PLIST_DEST"
echo "✓ Installed LaunchAgent"

# Load LaunchAgent
launchctl load "$PLIST_DEST"
echo "✓ Loaded LaunchAgent"
echo ""

# Test the importer
echo "============================================================"
echo "Testing Importer"
echo "============================================================"
echo ""

cd "$PETESBRAIN_ROOT"
python3 agents/wispr-flow-importer/wispr-flow-importer.py

echo ""
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Dictate a test note in Wispr Flow"
echo "  2. Wait up to 1 hour (or run manually)"
echo "  3. Check: ls -la !inbox/"
echo ""
echo "Manual commands:"
echo "  Run importer:  python3 agents/wispr-flow-importer/wispr-flow-importer.py"
echo "  Process inbox: python3 agents/system/inbox-processor.py"
echo "  View logs:     cat ~/.petesbrain-wispr-flow.log"
echo ""
echo "Documentation: docs/WISPR-FLOW-INTEGRATION.md"
echo ""
