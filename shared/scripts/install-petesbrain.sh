#!/bin/bash
#
# PetesBrain Sync System - Installation Script
# Installs PetesBrain on a new machine (laptop) and sets up sync
#
# Usage: ./install-petesbrain.sh [sync-method]
#   sync-method: 'git' (default), 'icloud', or 'rsync'
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SYNC_METHOD="${1:-git}"
INSTALL_DIR="$HOME/Documents/PetesBrain"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    PetesBrain Installation & Sync Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Sync Method:${NC} $SYNC_METHOD"
echo -e "${YELLOW}Install Directory:${NC} $INSTALL_DIR"
echo ""

# Check if already installed
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠ PetesBrain already exists at: $INSTALL_DIR${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create installation directory
mkdir -p "$(dirname "$INSTALL_DIR")"

case "$SYNC_METHOD" in
    git)
        echo -e "${YELLOW}→ Setting up Git-based sync...${NC}"
        
        # Check if Git remote repository is configured
        if [ -d "$INSTALL_DIR/.git" ]; then
            cd "$INSTALL_DIR"
            REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
            
            if [ -z "$REMOTE" ]; then
                echo -e "${YELLOW}⚠ No Git remote configured.${NC}"
                echo "Please set up a Git repository (GitHub, GitLab, etc.) first."
                echo ""
                echo "On your desktop machine, run:"
                echo "  cd $INSTALL_DIR"
                echo "  git remote add origin <your-repo-url>"
                echo "  git push -u origin main"
                echo ""
                read -p "Press Enter to continue with local Git setup..."
            fi
        else
            echo -e "${YELLOW}→ Cloning from Git repository...${NC}"
            read -p "Enter Git repository URL (or press Enter to skip): " GIT_REPO
            
            if [ -n "$GIT_REPO" ]; then
                git clone "$GIT_REPO" "$INSTALL_DIR" || {
                    echo -e "${RED}✗ Failed to clone repository${NC}"
                    exit 1
                }
                echo -e "${GREEN}✓ Cloned from Git repository${NC}"
            else
                echo -e "${YELLOW}⚠ Skipping Git clone. You'll need to set up manually.${NC}"
                mkdir -p "$INSTALL_DIR"
            fi
        fi
        ;;
        
    icloud)
        echo -e "${YELLOW}→ Setting up iCloud Drive sync...${NC}"
        
        ICLOUD_BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups"
        
        if [ ! -d "$ICLOUD_BACKUP_DIR" ]; then
            echo -e "${RED}✗ iCloud Drive backup directory not found${NC}"
            echo "Please run a backup on your desktop machine first:"
            echo "  backup-petesbrain"
            exit 1
        fi
        
        # Find latest backup
        LATEST_BACKUP=$(ls -t "$ICLOUD_BACKUP_DIR"/PetesBrain-backup-*.tar.gz 2>/dev/null | head -1)
        
        if [ -z "$LATEST_BACKUP" ]; then
            echo -e "${RED}✗ No backups found in iCloud Drive${NC}"
            echo "Please run a backup on your desktop machine first."
            exit 1
        fi
        
        echo -e "${YELLOW}→ Found latest backup: $(basename "$LATEST_BACKUP")${NC}"
        echo -e "${YELLOW}→ Extracting backup...${NC}"
        
        cd "$(dirname "$INSTALL_DIR")"
        tar -xzf "$LATEST_BACKUP"
        
        echo -e "${GREEN}✓ Extracted from iCloud backup${NC}"
        ;;
        
    rsync)
        echo -e "${YELLOW}→ Setting up rsync-based sync...${NC}"
        echo "This requires direct network access to your desktop machine."
        read -p "Enter desktop machine address (user@hostname or IP): " DESKTOP_HOST
        
        if [ -z "$DESKTOP_HOST" ]; then
            echo -e "${RED}✗ Desktop host required for rsync${NC}"
            exit 1
        fi
        
        DESKTOP_PATH="/Users/administrator/Documents/PetesBrain"
        
        echo -e "${YELLOW}→ Syncing from desktop...${NC}"
        rsync -avz --exclude='.git' --exclude='venv' --exclude='__pycache__' \
            "$DESKTOP_HOST:$DESKTOP_PATH/" "$INSTALL_DIR/" || {
            echo -e "${RED}✗ Failed to sync from desktop${NC}"
            exit 1
        }
        
        echo -e "${GREEN}✓ Synced from desktop${NC}"
        ;;
        
    *)
        echo -e "${RED}✗ Unknown sync method: $SYNC_METHOD${NC}"
        echo "Valid methods: git, icloud, rsync"
        exit 1
        ;;
esac

# Install sync scripts
echo ""
echo -e "${YELLOW}→ Installing sync scripts...${NC}"

if [ -f "$SCRIPT_DIR/sync-petesbrain.sh" ]; then
    cp "$SCRIPT_DIR/sync-petesbrain.sh" "$INSTALL_DIR/shared/scripts/"
    chmod +x "$INSTALL_DIR/shared/scripts/sync-petesbrain.sh"
    echo -e "${GREEN}✓ Sync script installed${NC}"
fi

# Create command alias
echo ""
echo -e "${YELLOW}→ Setting up command alias...${NC}"

SHELL_RC="$HOME/.zshrc"
if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -f "$SHELL_RC" ]; then
    if ! grep -q "sync-petesbrain" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# PetesBrain Sync" >> "$SHELL_RC"
        echo "alias sync-petesbrain='$INSTALL_DIR/shared/scripts/sync-petesbrain.sh'" >> "$SHELL_RC"
        echo -e "${GREEN}✓ Alias added to $SHELL_RC${NC}"
        echo -e "${YELLOW}  Run: source $SHELL_RC${NC}"
    else
        echo -e "${YELLOW}  Alias already exists in $SHELL_RC${NC}"
    fi
fi

# Set up Python environment
echo ""
echo -e "${YELLOW}→ Setting up Python environment...${NC}"

if [ -f "$INSTALL_DIR/requirements.txt" ]; then
    cd "$INSTALL_DIR"
    python3 -m venv venv 2>/dev/null || echo "venv already exists"
    source venv/bin/activate
    pip install -r requirements.txt 2>/dev/null || echo "No requirements.txt or pip install failed"
    echo -e "${GREEN}✓ Python environment ready${NC}"
else
    echo -e "${YELLOW}  No requirements.txt found, skipping Python setup${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}    Installation Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Source your shell config:"
echo "   source $SHELL_RC"
echo ""
echo "2. Navigate to PetesBrain:"
echo "   cd $INSTALL_DIR"
echo ""
echo "3. Sync with desktop:"
echo "   sync-petesbrain"
echo ""
echo "4. Set up environment variables (if needed):"
echo "   export ANTHROPIC_API_KEY='your-key'"
echo ""
echo -e "${YELLOW}For automatic syncing, see: docs/SYNC-SYSTEM.md${NC}"
echo ""

