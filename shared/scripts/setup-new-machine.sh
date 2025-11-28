#!/bin/bash
#
# PetesBrain - New Machine Setup Script
# Comprehensive setup for migrating PetesBrain to a new machine (laptop)
#
# Usage: ./setup-new-machine.sh
#
# This script:
# - Checks for required tools (Python, Git, etc.)
# - Updates all absolute paths in LaunchAgents and MCP configs
# - Creates virtual environments for MCP servers
# - Prompts for API keys and credentials
# - Validates configuration
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
OLD_USER="administrator"
OLD_PATH="/Users/${OLD_USER}/Documents/PetesBrain"
NEW_USER=$(whoami)
NEW_PATH="${HOME}/Documents/PetesBrain"

# Detect actual project location (might be different)
if [ -f "${PROJECT_DIR}/.mcp.json" ] || [ -f "${PROJECT_DIR}/README.md" ]; then
    ACTUAL_PROJECT_DIR="$PROJECT_DIR"
else
    # Try common locations
    if [ -d "${HOME}/Documents/PetesBrain" ]; then
        ACTUAL_PROJECT_DIR="${HOME}/Documents/PetesBrain"
    else
        echo -e "${RED}✗ Cannot find PetesBrain project directory${NC}"
        echo "Please run this script from within the PetesBrain directory or ensure"
        echo "PetesBrain is located at: ${HOME}/Documents/PetesBrain"
        exit 1
    fi
fi

cd "$ACTUAL_PROJECT_DIR"
PROJECT_DIR="$ACTUAL_PROJECT_DIR"

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    PetesBrain - New Machine Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Project Directory:${NC} $PROJECT_DIR"
echo -e "${YELLOW}Old User:${NC} $OLD_USER"
echo -e "${YELLOW}New User:${NC} $NEW_USER"
echo -e "${YELLOW}Old Path:${NC} $OLD_PATH"
echo -e "${YELLOW}New Path:${NC} $NEW_PATH"
echo ""

# ============================================================================
# Step 1: Check Required Tools
# ============================================================================

echo -e "${BLUE}Step 1: Checking Required Tools${NC}"
echo "─────────────────────────────────────────────────────────"

MISSING_TOOLS=()

# Check Python 3
if ! command -v python3 &> /dev/null; then
    MISSING_TOOLS+=("python3")
    echo -e "${RED}✗ Python 3 not found${NC}"
else
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python 3 found: $PYTHON_VERSION${NC}"
fi

# Check pip
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    MISSING_TOOLS+=("pip3")
    echo -e "${RED}✗ pip3 not found${NC}"
else
    echo -e "${GREEN}✓ pip3 found${NC}"
fi

# Check Git
if ! command -v git &> /dev/null; then
    MISSING_TOOLS+=("git")
    echo -e "${RED}✗ Git not found${NC}"
else
    GIT_VERSION=$(git --version)
    echo -e "${GREEN}✓ Git found: $GIT_VERSION${NC}"
fi

# Check Node.js (for some MCP servers)
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠ Node.js not found (optional, needed for some MCP servers)${NC}"
else
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js found: $NODE_VERSION${NC}"
fi

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo ""
    echo -e "${RED}✗ Missing required tools: ${MISSING_TOOLS[*]}${NC}"
    echo "Please install missing tools before continuing."
    echo ""
    echo "On macOS, you can install with:"
    echo "  brew install python3 git"
    exit 1
fi

echo ""

# ============================================================================
# Step 2: Create Main Virtual Environment
# ============================================================================

echo -e "${BLUE}Step 2: Setting Up Main Virtual Environment${NC}"
echo "─────────────────────────────────────────────────────────"

if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo -e "${YELLOW}→ Creating main virtual environment...${NC}"
    python3 -m venv "$PROJECT_DIR/venv"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Install main requirements if they exist
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo -e "${YELLOW}→ Installing main requirements...${NC}"
    source "$PROJECT_DIR/venv/bin/activate"
    pip install --upgrade pip > /dev/null 2>&1
    pip install -q -r "$PROJECT_DIR/requirements.txt" || echo -e "${YELLOW}  Some packages failed to install (may be okay)${NC}"
    deactivate
    echo -e "${GREEN}✓ Main requirements installed${NC}"
else
    echo -e "${YELLOW}  No requirements.txt found, skipping${NC}"
fi

echo ""

# ============================================================================
# Step 3: Update Paths in LaunchAgents
# ============================================================================

echo -e "${BLUE}Step 3: Updating LaunchAgent Paths${NC}"
echo "─────────────────────────────────────────────────────────"

LAUNCH_AGENTS_DIR="$PROJECT_DIR/agents/launchagents"
UPDATED_AGENTS=0

if [ -d "$LAUNCH_AGENTS_DIR" ]; then
    for plist in "$LAUNCH_AGENTS_DIR"/*.plist; do
        if [ -f "$plist" ]; then
            FILENAME=$(basename "$plist")
            echo -e "${YELLOW}→ Updating $FILENAME...${NC}"
            
            # Backup original
            cp "$plist" "${plist}.backup"
            
            # Update paths
            sed -i '' "s|$OLD_PATH|$PROJECT_DIR|g" "$plist"
            sed -i '' "s|/Users/$OLD_USER|$HOME|g" "$plist"
            
            # Validate plist syntax
            if plutil -lint "$plist" > /dev/null 2>&1; then
                echo -e "${GREEN}  ✓ Updated and validated${NC}"
                UPDATED_AGENTS=$((UPDATED_AGENTS + 1))
            else
                echo -e "${RED}  ✗ Invalid plist syntax after update${NC}"
                # Restore backup
                mv "${plist}.backup" "$plist"
            fi
        fi
    done
    
    echo -e "${GREEN}✓ Updated $UPDATED_AGENTS LaunchAgent files${NC}"
else
    echo -e "${YELLOW}  No LaunchAgents directory found${NC}"
fi

echo ""

# ============================================================================
# Step 4: Update MCP Server Configuration
# ============================================================================

echo -e "${BLUE}Step 4: Updating MCP Server Configuration${NC}"
echo "─────────────────────────────────────────────────────────"

MCP_CONFIG="$PROJECT_DIR/.mcp.json"

if [ -f "$MCP_CONFIG" ]; then
    echo -e "${YELLOW}→ Updating .mcp.json paths...${NC}"
    
    # Backup original
    cp "$MCP_CONFIG" "${MCP_CONFIG}.backup"
    
    # Update paths using Python for JSON handling
    python3 << EOF
import json
import sys

with open("$MCP_CONFIG", "r") as f:
    config = json.load(f)

old_path = "$OLD_PATH"
new_path = "$PROJECT_DIR"
old_user_path = "/Users/$OLD_USER"
new_user_path = "$HOME"

def update_paths(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                obj[key] = value.replace(old_path, new_path).replace(old_user_path, new_user_path)
            else:
                update_paths(value)
    elif isinstance(obj, list):
        for item in obj:
            update_paths(item)
    elif isinstance(obj, str):
        return obj.replace(old_path, new_path).replace(old_user_path, new_user_path)

update_paths(config)

with open("$MCP_CONFIG", "w") as f:
    json.dump(config, f, indent=2)

print("✓ Updated MCP configuration")
EOF
    
    # Validate JSON
    if python3 -m json.tool "$MCP_CONFIG" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ MCP configuration updated and validated${NC}"
    else
        echo -e "${RED}✗ Invalid JSON after update, restoring backup${NC}"
        mv "${MCP_CONFIG}.backup" "$MCP_CONFIG"
    fi
else
    echo -e "${YELLOW}  No .mcp.json found${NC}"
fi

echo ""

# ============================================================================
# Step 5: Set Up MCP Server Virtual Environments
# ============================================================================

echo -e "${BLUE}Step 5: Setting Up MCP Server Virtual Environments${NC}"
echo "─────────────────────────────────────────────────────────"

MCP_SERVERS_DIR="$PROJECT_DIR/infrastructure/mcp-servers"
MCP_SERVERS_WITH_VENV=(
    "google-analytics-mcp-server"
    "google-ads-mcp-server"
    "google-photos-mcp-server"
    "google-sheets-mcp-server"
    "google-tasks-mcp-server"
    "google-trends-mcp-server"
    "google-drive-mcp-server"
    "facebook-ads-mcp-server"
    "meta-ads-mcp-server"
    "microsoft-ads-mcp-server"
    "bing-search-mcp-server"
)

SETUP_COUNT=0

for server in "${MCP_SERVERS_WITH_VENV[@]}"; do
    SERVER_DIR="$MCP_SERVERS_DIR/$server"
    
    if [ -d "$SERVER_DIR" ]; then
        echo -e "${YELLOW}→ Setting up $server...${NC}"
        
        # Create virtual environment if it doesn't exist
        if [ ! -d "$SERVER_DIR/.venv" ]; then
            python3 -m venv "$SERVER_DIR/.venv"
            echo -e "  ✓ Virtual environment created${NC}"
        fi
        
        # Install requirements if they exist
        if [ -f "$SERVER_DIR/requirements.txt" ]; then
            source "$SERVER_DIR/.venv/bin/activate"
            pip install --upgrade pip > /dev/null 2>&1
            pip install -q -r "$SERVER_DIR/requirements.txt" || echo -e "  ${YELLOW}⚠ Some packages failed to install${NC}"
            deactivate
            echo -e "  ✓ Dependencies installed${NC}"
        fi
        
        SETUP_COUNT=$((SETUP_COUNT + 1))
    fi
done

# Also check for email-sync venv
EMAIL_SYNC_DIR="$PROJECT_DIR/shared/email-sync"
if [ -d "$EMAIL_SYNC_DIR" ]; then
    echo -e "${YELLOW}→ Setting up email-sync...${NC}"
    if [ ! -d "$EMAIL_SYNC_DIR/.venv" ]; then
        python3 -m venv "$EMAIL_SYNC_DIR/.venv"
        echo -e "  ✓ Virtual environment created${NC}"
    fi
    if [ -f "$EMAIL_SYNC_DIR/requirements.txt" ]; then
        source "$EMAIL_SYNC_DIR/.venv/bin/activate"
        pip install --upgrade pip > /dev/null 2>&1
        pip install -q -r "$EMAIL_SYNC_DIR/requirements.txt" || echo -e "  ${YELLOW}⚠ Some packages failed to install${NC}"
        deactivate
        echo -e "  ✓ Dependencies installed${NC}"
    fi
    SETUP_COUNT=$((SETUP_COUNT + 1))
fi

echo -e "${GREEN}✓ Set up $SETUP_COUNT MCP server environments${NC}"
echo ""

# ============================================================================
# Step 6: Prompt for API Keys and Credentials
# ============================================================================

echo -e "${BLUE}Step 6: API Keys and Credentials${NC}"
echo "─────────────────────────────────────────────────────────"

echo -e "${YELLOW}The following credentials may need to be set up:${NC}"
echo ""
echo "1. ANTHROPIC_API_KEY - For Claude AI features"
echo "2. Google OAuth credentials - For Google services (Drive, Sheets, etc.)"
echo "3. Meta/Facebook credentials - For Meta Ads MCP server"
echo "4. WooCommerce credentials - Already in MCP config (may need updating)"
echo ""

read -p "Do you want to set up environment variables now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    SHELL_RC="$HOME/.zshrc"
    if [ ! -f "$SHELL_RC" ]; then
        SHELL_RC="$HOME/.bashrc"
    fi
    
    echo ""
    echo -e "${YELLOW}Setting up environment variables in $SHELL_RC${NC}"
    echo ""
    
    # ANTHROPIC_API_KEY
    if ! grep -q "ANTHROPIC_API_KEY" "$SHELL_RC" 2>/dev/null; then
        read -p "Enter ANTHROPIC_API_KEY (or press Enter to skip): " ANTHROPIC_KEY
        if [ -n "$ANTHROPIC_KEY" ]; then
            echo "" >> "$SHELL_RC"
            echo "# PetesBrain - Anthropic API Key" >> "$SHELL_RC"
            echo "export ANTHROPIC_API_KEY=\"$ANTHROPIC_KEY\"" >> "$SHELL_RC"
            echo -e "${GREEN}✓ ANTHROPIC_API_KEY added${NC}"
        fi
    else
        echo -e "${YELLOW}  ANTHROPIC_API_KEY already configured${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}Note:${NC} Other credentials (Google OAuth, Meta, etc.) need to be"
    echo "configured manually in their respective credential files."
    echo "See documentation in each MCP server directory for setup instructions."
fi

echo ""

# ============================================================================
# Step 7: Create Necessary Directories
# ============================================================================

echo -e "${BLUE}Step 7: Creating Necessary Directories${NC}"
echo "─────────────────────────────────────────────────────────"

DIRECTORIES=(
    "$HOME/Library/LaunchAgents"
    "$PROJECT_DIR/shared/data"
    "$PROJECT_DIR/todo"
)

for dir in "${DIRECTORIES[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}✓ Created: $dir${NC}"
    else
        echo -e "${YELLOW}  Already exists: $dir${NC}"
    fi
done

echo ""

# ============================================================================
# Step 8: Validate Configuration
# ============================================================================

echo -e "${BLUE}Step 8: Validating Configuration${NC}"
echo "─────────────────────────────────────────────────────────"

VALIDATION_ERRORS=0

# Check MCP config
if [ -f "$MCP_CONFIG" ]; then
    if python3 -m json.tool "$MCP_CONFIG" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ MCP configuration is valid JSON${NC}"
    else
        echo -e "${RED}✗ MCP configuration has invalid JSON${NC}"
        VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
    fi
fi

# Check LaunchAgents
if [ -d "$LAUNCH_AGENTS_DIR" ]; then
    for plist in "$LAUNCH_AGENTS_DIR"/*.plist; do
        if [ -f "$plist" ]; then
            if plutil -lint "$plist" > /dev/null 2>&1; then
                echo -e "${GREEN}✓ $(basename "$plist") is valid${NC}"
            else
                echo -e "${RED}✗ $(basename "$plist") has invalid syntax${NC}"
                VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
            fi
        fi
    done
fi

# Check virtual environments
MISSING_VENVS=0
for server in "${MCP_SERVERS_WITH_VENV[@]}"; do
    SERVER_DIR="$MCP_SERVERS_DIR/$server"
    if [ -d "$SERVER_DIR" ] && [ ! -d "$SERVER_DIR/.venv" ]; then
        echo -e "${YELLOW}⚠ Missing venv: $server${NC}"
        MISSING_VENVS=$((MISSING_VENVS + 1))
    fi
done

if [ $VALIDATION_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Configuration validation passed${NC}"
else
    echo -e "${RED}✗ Found $VALIDATION_ERRORS validation errors${NC}"
fi

echo ""

# ============================================================================
# Step 9: Set Up Sync Script Alias
# ============================================================================

echo -e "${BLUE}Step 9: Setting Up Sync Script Alias${NC}"
echo "─────────────────────────────────────────────────────────"

SHELL_RC="$HOME/.zshrc"
if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -f "$SHELL_RC" ]; then
    if ! grep -q "sync-petesbrain" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# PetesBrain Sync" >> "$SHELL_RC"
        echo "alias sync-petesbrain='$PROJECT_DIR/shared/scripts/sync-petesbrain.sh'" >> "$SHELL_RC"
        echo -e "${GREEN}✓ Sync alias added to $SHELL_RC${NC}"
        echo -e "${YELLOW}  Run: source $SHELL_RC${NC}"
    else
        echo -e "${YELLOW}  Sync alias already exists${NC}"
    fi
fi

echo ""

# ============================================================================
# Summary
# ============================================================================

echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}    Setup Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Summary:${NC}"
echo "  • Updated LaunchAgent paths: $UPDATED_AGENTS"
echo "  • Set up MCP server environments: $SETUP_COUNT"
echo "  • Updated MCP configuration"
echo "  • Created necessary directories"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Source your shell config:"
echo "   source $SHELL_RC"
echo ""
echo "2. Set up OAuth credentials for MCP servers:"
echo "   - Google services: Check shared/mcp-servers/google-*/README.md"
echo "   - Meta Ads: Check shared/mcp-servers/meta-ads-mcp-server/README.md"
echo ""
echo "3. Test sync (if on laptop):"
echo "   sync-petesbrain pull"
echo ""
echo "4. Set up automatic syncing (optional):"
echo "   cd $PROJECT_DIR/shared/scripts"
echo "   ./setup-auto-sync.sh laptop"
echo ""
echo -e "${YELLOW}For detailed documentation, see:${NC}"
echo "  • docs/LAPTOP-INSTALLATION-GUIDE.md"
echo "  • docs/SYNC-SYSTEM.md"
echo ""

