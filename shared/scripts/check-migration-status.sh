#!/bin/bash
#
# PetesBrain Migration Status Checker
# Checks current state of migration and identifies next steps
#
# Usage: ./check-migration-status.sh
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

cd "$PROJECT_DIR"

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    PetesBrain Migration Status Check${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Project Directory:${NC} $PROJECT_DIR"
echo -e "${YELLOW}Current User:${NC} $(whoami)"
echo -e "${YELLOW}Hostname:${NC} $(hostname)"
echo ""

# Track what's done
STEPS_COMPLETE=0
STEPS_TOTAL=9
ISSUES_FOUND=0

# ============================================================================
# Step 1: Check Python 3 Installation
# ============================================================================

echo -e "${BLUE}Step 1: Python 3 Installation${NC}"
echo "─────────────────────────────────────────────────────────"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python 3 installed: $PYTHON_VERSION${NC}"
    STEPS_COMPLETE=$((STEPS_COMPLETE + 1))
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "  Install with: brew install python3"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if command -v pip3 &> /dev/null || python3 -m pip --version &> /dev/null; then
    echo -e "${GREEN}✓ pip3 available${NC}"
else
    echo -e "${RED}✗ pip3 not found${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

echo ""

# ============================================================================
# Step 2: Check Main Virtual Environment
# ============================================================================

echo -e "${BLUE}Step 2: Main Virtual Environment${NC}"
echo "─────────────────────────────────────────────────────────"

if [ -d "$PROJECT_DIR/venv" ]; then
    if [ -f "$PROJECT_DIR/venv/bin/python3" ]; then
        echo -e "${GREEN}✓ Main venv exists and has Python${NC}"
        STEPS_COMPLETE=$((STEPS_COMPLETE + 1))
    else
        echo -e "${YELLOW}⚠ venv directory exists but Python not found${NC}"
        echo "  Recreate with: python3 -m venv venv"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo -e "${YELLOW}⚠ Main venv not created${NC}"
    echo "  Create with: python3 -m venv venv"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

echo ""

# ============================================================================
# Step 3: Check MCP Server Virtual Environments
# ============================================================================

echo -e "${BLUE}Step 3: MCP Server Virtual Environments${NC}"
echo "─────────────────────────────────────────────────────────"

MCP_SERVERS_DIR="$PROJECT_DIR/shared/mcp-servers"
MCP_SERVERS_WITH_VENV=(
    "google-analytics-mcp-server"
    "google-ads-mcp-server"
    "google-photos-mcp-server"
    "google-sheets-mcp-server"
    "google-tasks-mcp-server"
    "facebook-ads-mcp-server"
)

VENVS_CREATED=0
VENVS_MISSING=0

for server in "${MCP_SERVERS_WITH_VENV[@]}"; do
    SERVER_DIR="$MCP_SERVERS_DIR/$server"
    if [ -d "$SERVER_DIR" ]; then
        if [ -d "$SERVER_DIR/.venv" ]; then
            if [ -f "$SERVER_DIR/.venv/bin/python3" ]; then
                echo -e "${GREEN}✓ $server venv exists${NC}"
                VENVS_CREATED=$((VENVS_CREATED + 1))
            else
                echo -e "${YELLOW}⚠ $server venv incomplete${NC}"
                VENVS_MISSING=$((VENVS_MISSING + 1))
            fi
        else
            echo -e "${YELLOW}⚠ $server venv missing${NC}"
            VENVS_MISSING=$((VENVS_MISSING + 1))
        fi
    fi
done

# Check email-sync venv
EMAIL_SYNC_DIR="$PROJECT_DIR/shared/email-sync"
if [ -d "$EMAIL_SYNC_DIR" ]; then
    if [ -d "$EMAIL_SYNC_DIR/.venv" ]; then
        echo -e "${GREEN}✓ email-sync venv exists${NC}"
        VENVS_CREATED=$((VENVS_CREATED + 1))
    else
        echo -e "${YELLOW}⚠ email-sync venv missing${NC}"
        VENVS_MISSING=$((VENVS_MISSING + 1))
    fi
fi

if [ $VENVS_MISSING -eq 0 ]; then
    STEPS_COMPLETE=$((STEPS_COMPLETE + 1))
fi

echo ""
echo -e "${YELLOW}Summary:${NC} $VENVS_CREATED venvs created, $VENVS_MISSING missing"
echo ""

# ============================================================================
# Step 4: Check Path Updates
# ============================================================================

echo -e "${BLUE}Step 4: Path Updates${NC}"
echo "─────────────────────────────────────────────────────────"

OLD_USER="administrator"
CURRENT_USER=$(whoami)
PATHS_UPDATED=true

# Check LaunchAgents
LAUNCH_AGENTS_DIR="$PROJECT_DIR/agents/launchagents"
if [ -d "$LAUNCH_AGENTS_DIR" ]; then
    OLD_PATHS_FOUND=0
    for plist in "$LAUNCH_AGENTS_DIR"/*.plist; do
        if [ -f "$plist" ]; then
            if grep -q "/Users/$OLD_USER" "$plist" 2>/dev/null; then
                OLD_PATHS_FOUND=$((OLD_PATHS_FOUND + 1))
                PATHS_UPDATED=false
            fi
        fi
    done
    
    if [ $OLD_PATHS_FOUND -eq 0 ]; then
        echo -e "${GREEN}✓ LaunchAgent paths updated${NC}"
    else
        echo -e "${YELLOW}⚠ $OLD_PATHS_FOUND LaunchAgent files still have old paths${NC}"
        echo "  Run: ./shared/scripts/setup-new-machine.sh"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo -e "${YELLOW}⚠ LaunchAgents directory not found${NC}"
fi

# Check MCP config
MCP_CONFIG="$PROJECT_DIR/.mcp.json"
if [ -f "$MCP_CONFIG" ]; then
    if grep -q "/Users/$OLD_USER" "$MCP_CONFIG" 2>/dev/null; then
        echo -e "${YELLOW}⚠ MCP config still has old paths${NC}"
        echo "  Run: ./shared/scripts/setup-new-machine.sh"
        PATHS_UPDATED=false
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    else
        echo -e "${GREEN}✓ MCP config paths updated${NC}"
    fi
else
    echo -e "${YELLOW}⚠ MCP config file not found${NC}"
fi

if [ "$PATHS_UPDATED" = true ]; then
    STEPS_COMPLETE=$((STEPS_COMPLETE + 1))
fi

echo ""

# ============================================================================
# Step 5: Check Credentials
# ============================================================================

echo -e "${BLUE}Step 5: Credentials Check${NC}"
echo "─────────────────────────────────────────────────────────"

CREDENTIALS_MISSING=0

# Check MCP config exists
if [ ! -f "$MCP_CONFIG" ]; then
    echo -e "${RED}✗ .mcp.json not found${NC}"
    CREDENTIALS_MISSING=$((CREDENTIALS_MISSING + 1))
else
    echo -e "${GREEN}✓ .mcp.json exists${NC}"
fi

# Check key credential files
CREDENTIAL_FILES=(
    "shared/email-sync/credentials.json"
    "shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json"
    "shared/mcp-servers/google-photos-mcp-server/credentials.json"
    "shared/mcp-servers/google-sheets-mcp-server/credentials.json"
    "shared/mcp-servers/google-tasks-mcp-server/credentials.json"
)

for cred_file in "${CREDENTIAL_FILES[@]}"; do
    if [ -f "$PROJECT_DIR/$cred_file" ]; then
        echo -e "${GREEN}✓ $(basename "$cred_file") exists${NC}"
    else
        echo -e "${YELLOW}⚠ $cred_file missing${NC}"
        CREDENTIALS_MISSING=$((CREDENTIALS_MISSING + 1))
    fi
done

if [ $CREDENTIALS_MISSING -eq 0 ]; then
    STEPS_COMPLETE=$((STEPS_COMPLETE + 1))
fi

echo ""

# ============================================================================
# Step 6: Check Sync Script Setup
# ============================================================================

echo -e "${BLUE}Step 6: Sync Script Setup${NC}"
echo "─────────────────────────────────────────────────────────"

SYNC_SCRIPT="$PROJECT_DIR/shared/scripts/sync-petesbrain.sh"
if [ -f "$SYNC_SCRIPT" ]; then
    if [ -x "$SYNC_SCRIPT" ]; then
        echo -e "${GREEN}✓ Sync script exists and is executable${NC}"
        STEPS_COMPLETE=$((STEPS_COMPLETE + 1))
    else
        echo -e "${YELLOW}⚠ Sync script not executable${NC}"
        echo "  Fix with: chmod +x $SYNC_SCRIPT"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo -e "${RED}✗ Sync script not found${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# Check alias
SHELL_RC="$HOME/.zshrc"
if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -f "$SHELL_RC" ]; then
    if grep -q "sync-petesbrain" "$SHELL_RC" 2>/dev/null; then
        echo -e "${GREEN}✓ Sync alias configured${NC}"
    else
        echo -e "${YELLOW}⚠ Sync alias not configured${NC}"
        echo "  Add with: echo 'alias sync-petesbrain=\"$PROJECT_DIR/shared/scripts/sync-petesbrain.sh\"' >> $SHELL_RC"
    fi
fi

echo ""

# ============================================================================
# Step 7: Check Git Setup
# ============================================================================

echo -e "${BLUE}Step 7: Git Configuration${NC}"
echo "─────────────────────────────────────────────────────────"

if [ -d "$PROJECT_DIR/.git" ]; then
    REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
    if [ -n "$REMOTE" ]; then
        echo -e "${GREEN}✓ Git repository with remote configured${NC}"
        STEPS_COMPLETE=$((STEPS_COMPLETE + 1))
    else
        echo -e "${YELLOW}⚠ Git repository but no remote${NC}"
        echo "  Configure with: git remote add origin <repo-url>"
    fi
else
    echo -e "${YELLOW}⚠ Not a Git repository${NC}"
    echo "  Initialize with: git init"
fi

echo ""

# ============================================================================
# Step 8: Check Environment Variables
# ============================================================================

echo -e "${BLUE}Step 8: Environment Variables${NC}"
echo "─────────────────────────────────────────────────────────"

SHELL_RC="$HOME/.zshrc"
if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -f "$SHELL_RC" ]; then
    if grep -q "ANTHROPIC_API_KEY" "$SHELL_RC" 2>/dev/null; then
        echo -e "${GREEN}✓ ANTHROPIC_API_KEY configured${NC}"
        STEPS_COMPLETE=$((STEPS_COMPLETE + 1))
    else
        echo -e "${YELLOW}⚠ ANTHROPIC_API_KEY not configured${NC}"
        echo "  Add with: echo 'export ANTHROPIC_API_KEY=\"your-key\"' >> $SHELL_RC"
    fi
else
    echo -e "${YELLOW}⚠ Shell config file not found${NC}"
fi

echo ""

# ============================================================================
# Step 9: Check Automatic Sync Setup
# ============================================================================

echo -e "${BLUE}Step 9: Automatic Sync Setup${NC}"
echo "─────────────────────────────────────────────────────────"

LAUNCH_AGENT="$HOME/Library/LaunchAgents/com.petesbrain.sync.plist"
if [ -f "$LAUNCH_AGENT" ]; then
    echo -e "${GREEN}✓ Automatic sync LaunchAgent configured${NC}"
    if launchctl list | grep -q "petesbrain.sync" 2>/dev/null; then
        echo -e "${GREEN}✓ Automatic sync is running${NC}"
        STEPS_COMPLETE=$((STEPS_COMPLETE + 1))
    else
        echo -e "${YELLOW}⚠ LaunchAgent exists but not running${NC}"
        echo "  Start with: launchctl load $LAUNCH_AGENT"
    fi
else
    echo -e "${YELLOW}⚠ Automatic sync not configured${NC}"
    echo "  Set up with: cd shared/scripts && ./setup-auto-sync.sh laptop"
fi

echo ""

# ============================================================================
# Summary
# ============================================================================

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Migration Status Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Progress:${NC} $STEPS_COMPLETE / $STEPS_TOTAL steps complete"

if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}✓ No issues found!${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Test sync: sync-petesbrain pull"
    echo "2. Test MCP servers (restart Claude Desktop)"
    echo "3. Verify LaunchAgents are running"
else
    echo -e "${YELLOW}⚠ Found $ISSUES_FOUND issues${NC}"
    echo ""
    echo -e "${BLUE}Recommended Actions:${NC}"
    echo ""
    
    if ! command -v python3 &> /dev/null; then
        echo "1. Install Python 3:"
        echo "   brew install python3"
        echo ""
    fi
    
    if [ ! -d "$PROJECT_DIR/venv" ] || [ $VENVS_MISSING -gt 0 ]; then
        echo "2. Run setup script to create virtual environments:"
        echo "   ./shared/scripts/setup-new-machine.sh"
        echo ""
    fi
    
    if [ "$PATHS_UPDATED" = false ]; then
        echo "3. Update paths in LaunchAgents and MCP config:"
        echo "   ./shared/scripts/setup-new-machine.sh"
        echo ""
    fi
    
    if [ $CREDENTIALS_MISSING -gt 0 ]; then
        echo "4. Copy credentials from original machine:"
        echo "   See: docs/MIGRATION-SYSTEM-COMPLETE.md"
        echo ""
    fi
fi

echo ""
echo -e "${BLUE}For detailed instructions, see:${NC}"
echo "  • docs/LAPTOP-INSTALLATION-GUIDE.md"
echo "  • docs/MIGRATION-SYSTEM-COMPLETE.md"
echo ""

