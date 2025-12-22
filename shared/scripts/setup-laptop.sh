#!/bin/bash
#
# PetesBrain Laptop Setup Script
# Run this on your laptop to set up PetesBrain from iCloud backup
#
# Usage: ./setup-laptop.sh
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    PetesBrain Laptop Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}→ Checking prerequisites...${NC}"
echo ""

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo ""
    echo "Please install Python 3:"
    echo "  1. Install Xcode Command Line Tools: xcode-select --install"
    echo "  2. Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "  3. Install Python: brew install python3"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"

# Check iCloud Drive
ICLOUD_BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups"
if [ ! -d "$ICLOUD_BACKUP_DIR" ]; then
    echo -e "${RED}✗ iCloud Drive backup directory not found${NC}"
    echo ""
    echo "Please ensure:"
    echo "  1. iCloud Drive is enabled on this Mac"
    echo "  2. iCloud Drive is syncing (may take a few minutes)"
    echo "  3. You've run 'sync-petesbrain push' on the desktop"
    echo ""
    echo "Expected location: $ICLOUD_BACKUP_DIR"
    exit 1
fi
echo -e "${GREEN}✓ iCloud Drive found${NC}"

# Find latest backup
LATEST_BACKUP=$(ls -t "$ICLOUD_BACKUP_DIR"/PetesBrain-backup-*.tar.gz 2>/dev/null | head -1)
if [ -z "$LATEST_BACKUP" ]; then
    echo -e "${RED}✗ No backups found in iCloud Drive${NC}"
    echo ""
    echo "Please create a backup on the desktop first:"
    echo "  cd ~/Documents/PetesBrain.nosync"
    echo "  ./shared/scripts/sync-petesbrain.sh push"
    exit 1
fi

BACKUP_SIZE=$(du -h "$LATEST_BACKUP" | cut -f1)
BACKUP_NAME=$(basename "$LATEST_BACKUP")
echo -e "${GREEN}✓ Found backup: ${BACKUP_NAME} (${BACKUP_SIZE})${NC}"
echo ""

# Check metadata
METADATA_FILE="$ICLOUD_BACKUP_DIR/.sync-metadata.json"
if [ -f "$METADATA_FILE" ]; then
    PUSH_TIME=$(python3 -c "import json; print(json.load(open('$METADATA_FILE'))['last_push']['timestamp'])" 2>/dev/null)
    PUSH_MACHINE=$(python3 -c "import json; print(json.load(open('$METADATA_FILE'))['last_push']['machine'])" 2>/dev/null)
    echo -e "${YELLOW}Last backup:${NC} ${PUSH_TIME}"
    echo -e "${YELLOW}From:${NC} ${PUSH_MACHINE}"
    echo ""
fi

# Check disk space
FREE_SPACE=$(df -h ~ | awk 'NR==2 {print $4}')
echo -e "${YELLOW}Free disk space:${NC} ${FREE_SPACE}"
echo ""

# Confirm
echo -e "${BOLD}Ready to set up PetesBrain on this laptop.${NC}"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi
echo ""

# Step 1: Extract backup
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Step 1: Extracting Backup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

TARGET_DIR="$HOME/Documents/PetesBrain.nosync"
if [ -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}⚠ Directory already exists: $TARGET_DIR${NC}"
    echo ""
    read -p "Overwrite? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
    echo -e "${YELLOW}→ Removing existing directory...${NC}"
    rm -rf "$TARGET_DIR"
fi

mkdir -p "$HOME/Documents"
cd "$HOME/Documents"

echo -e "${YELLOW}→ Extracting: ${BACKUP_NAME}${NC}"
echo -e "${YELLOW}  This may take 2-3 minutes...${NC}"
echo ""

if tar -xzf "$LATEST_BACKUP"; then
    # Check if extracted as PetesBrain or PetesBrain.nosync
    if [ -d "PetesBrain" ]; then
        mv PetesBrain PetesBrain.nosync
    fi
    echo -e "${GREEN}✓ Extracted successfully${NC}"
else
    echo -e "${RED}✗ Extraction failed${NC}"
    exit 1
fi
echo ""

# Step 2: Configure laptop sync
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Step 2: Configuring Sync${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

cd "$TARGET_DIR"

echo -e "${YELLOW}→ Creating laptop sync configuration...${NC}"
cat > .sync-config << 'EOF'
# PetesBrain Sync Configuration
# Method: rsync, git, or icloud
TYPE=Laptop
SYNC_METHOD="icloud"

# Desktop hostname (for rsync if needed - leave as-is)
DESKTOP_HOST="Peters-Mac-mini.lan"
DESKTOP_USER="administrator"
DESKTOP_PATH="/Users/administrator/Documents/PetesBrain.nosync"
EOF
echo -e "${GREEN}✓ Sync config created${NC}"

echo -e "${YELLOW}→ Making sync script executable...${NC}"
chmod +x shared/scripts/sync-petesbrain.sh
echo -e "${GREEN}✓ Sync script ready${NC}"
echo ""

# Step 3: Create shell alias
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Step 3: Setting Up Shell Alias${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

SHELL_CONFIG=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_CONFIG="$HOME/.bash_profile"
else
    SHELL_CONFIG="$HOME/.zshrc"
    touch "$SHELL_CONFIG"
fi

# Check if alias already exists
if grep -q "alias sync-petesbrain=" "$SHELL_CONFIG" 2>/dev/null; then
    echo -e "${YELLOW}⚠ Alias already exists in $SHELL_CONFIG${NC}"
else
    echo -e "${YELLOW}→ Adding alias to $SHELL_CONFIG...${NC}"
    echo "" >> "$SHELL_CONFIG"
    echo "# PetesBrain sync alias" >> "$SHELL_CONFIG"
    echo 'alias sync-petesbrain="~/Documents/PetesBrain.nosync/shared/scripts/sync-petesbrain.sh"' >> "$SHELL_CONFIG"
    echo -e "${GREEN}✓ Alias added${NC}"
fi
echo ""

# Step 4: Test sync
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Step 4: Testing Sync${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}→ Testing sync pull...${NC}"
echo ""

# Source the shell config to get the alias in current session
alias sync-petesbrain="$TARGET_DIR/shared/scripts/sync-petesbrain.sh"

if sync-petesbrain pull; then
    echo ""
    echo -e "${GREEN}✓ Sync test successful${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠ Sync test had issues (may be normal if already up-to-date)${NC}"
fi
echo ""

# Done!
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}    ✓ Setup Complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BOLD}PetesBrain is now set up on this laptop.${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "  1. Restart your terminal (or run: source $SHELL_CONFIG)"
echo "  2. Test sync: sync-petesbrain pull"
echo "  3. Work on PetesBrain normally"
echo "  4. Before finishing: sync-petesbrain push"
echo ""
echo -e "${BOLD}Daily workflow:${NC}"
echo ""
echo "  Morning:  sync-petesbrain pull  # Get latest from desktop"
echo "  Evening:  sync-petesbrain push  # Send your changes back"
echo ""
echo -e "${YELLOW}Location:${NC} $TARGET_DIR"
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
