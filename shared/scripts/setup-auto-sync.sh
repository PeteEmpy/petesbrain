#!/bin/bash
#
# Setup Automatic Sync for PetesBrain
# Creates LaunchAgent for automatic syncing
#
# Usage: ./setup-auto-sync.sh [desktop|laptop]
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

MACHINE_TYPE="${1:-laptop}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SYNC_SCRIPT="$PROJECT_DIR/shared/scripts/sync-petesbrain.sh"
LAUNCH_AGENT="$HOME/Library/LaunchAgents/com.petesbrain.sync.plist"

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    PetesBrain Automatic Sync Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Machine Type:${NC} $MACHINE_TYPE"
echo ""

# Validate machine type
if [[ "$MACHINE_TYPE" != "desktop" && "$MACHINE_TYPE" != "laptop" ]]; then
    echo -e "${RED}✗ Invalid machine type: $MACHINE_TYPE${NC}"
    echo "Usage: $0 [desktop|laptop]"
    exit 1
fi

# Check sync script exists
if [ ! -f "$SYNC_SCRIPT" ]; then
    echo -e "${RED}✗ Sync script not found: $SYNC_SCRIPT${NC}"
    exit 1
fi

# Determine sync frequency and direction
if [ "$MACHINE_TYPE" = "desktop" ]; then
    INTERVAL=7200  # 2 hours
    DIRECTION="push"
    DESCRIPTION="Push changes to remote"
else
    INTERVAL=3600  # 1 hour
    DIRECTION="pull"
    DESCRIPTION="Pull latest changes"
fi

# Create LaunchAgent plist
echo -e "${YELLOW}→ Creating LaunchAgent...${NC}"

cat > "$LAUNCH_AGENT" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.sync</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$SYNC_SCRIPT</string>
        <string>$DIRECTION</string>
    </array>
    
    <key>StartInterval</key>
    <integer>$INTERVAL</integer>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>$HOME/.petesbrain-sync.log</string>
    
    <key>StandardErrorPath</key>
    <string>$HOME/.petesbrain-sync-error.log</string>
    
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
</dict>
</plist>
EOF

echo -e "${GREEN}✓ LaunchAgent created${NC}"
echo "  Location: $LAUNCH_AGENT"

# Load LaunchAgent
echo ""
echo -e "${YELLOW}→ Loading LaunchAgent...${NC}"

# Unload if already exists
launchctl unload "$LAUNCH_AGENT" 2>/dev/null || true

# Load new agent
launchctl load "$LAUNCH_AGENT"

echo -e "${GREEN}✓ LaunchAgent loaded${NC}"

# Summary
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}    Automatic Sync Configured!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo "  Machine: $MACHINE_TYPE"
echo "  Frequency: Every $((INTERVAL / 60)) minutes"
echo "  Direction: $DIRECTION"
echo "  Description: $DESCRIPTION"
echo ""
echo -e "${BLUE}Management:${NC}"
echo "  Check status: launchctl list | grep petesbrain.sync"
echo "  View logs: tail -f ~/.petesbrain-sync.log"
echo "  Stop sync: launchctl unload $LAUNCH_AGENT"
echo "  Start sync: launchctl load $LAUNCH_AGENT"
echo ""

