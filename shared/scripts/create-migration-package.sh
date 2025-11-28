#!/bin/bash
#
# PetesBrain - Create Migration Package
# Creates a complete migration package for transferring PetesBrain to another machine
#
# Usage: ./create-migration-package.sh [output-dir]
#
# This script:
# - Creates a tarball of the entire project (excluding venv, __pycache__, etc.)
# - Documents what credentials need to be copied manually
# - Includes setup script for new machine
# - Lists manual configuration steps
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
OUTPUT_DIR="${1:-$HOME/Desktop}"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
PACKAGE_NAME="PetesBrain-migration-${TIMESTAMP}"
PACKAGE_DIR="$OUTPUT_DIR/$PACKAGE_NAME"
TARBALL="$OUTPUT_DIR/${PACKAGE_NAME}.tar.gz"

cd "$PROJECT_DIR"

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    PetesBrain Migration Package Creator${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Project Directory:${NC} $PROJECT_DIR"
echo -e "${YELLOW}Output Directory:${NC} $OUTPUT_DIR"
echo -e "${YELLOW}Package Name:${NC} $PACKAGE_NAME"
echo ""

# Create package directory
echo -e "${YELLOW}→ Creating package directory...${NC}"
mkdir -p "$PACKAGE_DIR"
echo -e "${GREEN}✓ Package directory created${NC}"
echo ""

# Copy project files (excluding venv, __pycache__, etc.)
echo -e "${YELLOW}→ Copying project files...${NC}"

rsync -av \
    --exclude='venv' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='.DS_Store' \
    --exclude='*.log' \
    --exclude='node_modules' \
    --exclude='.mcp.json' \
    --exclude='shared/credentials/*.json' \
    --exclude='shared/email-sync/credentials.json' \
    --exclude='shared/mcp-servers/*/credentials.json' \
    --exclude='shared/mcp-servers/*/token.json' \
    --exclude='shared/mcp-servers/*/gcp-oauth.keys.json' \
    --exclude='shared/calendar_token.json' \
    --exclude='*.backup' \
    "$PROJECT_DIR/" "$PACKAGE_DIR/" || {
    echo -e "${RED}✗ Failed to copy files${NC}"
    exit 1
}

echo -e "${GREEN}✓ Files copied${NC}"
echo ""

# Create credentials checklist
echo -e "${YELLOW}→ Creating credentials checklist...${NC}"

cat > "$PACKAGE_DIR/CREDENTIALS-CHECKLIST.md" << 'EOF'
# PetesBrain Migration - Credentials Checklist

**IMPORTANT:** The following credentials and files were NOT included in the migration package for security reasons. You must copy these manually from your original machine.

## Required Credentials

### 1. MCP Server Configuration
- **File:** `.mcp.json` (in project root)
- **Location:** `$PROJECT_DIR/.mcp.json`
- **Action:** Copy this file manually (contains OAuth tokens and paths)

### 2. Google OAuth Credentials

#### Google Drive MCP Server
- **File:** `shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json`
- **Action:** Copy from original machine

#### Google Photos MCP Server
- **File:** `shared/mcp-servers/google-photos-mcp-server/credentials.json`
- **File:** `shared/mcp-servers/google-photos-mcp-server/token.json`
- **Action:** Copy both files from original machine

#### Google Sheets MCP Server
- **File:** `shared/mcp-servers/google-sheets-mcp-server/credentials.json`
- **Action:** Copy from original machine

#### Google Tasks MCP Server
- **File:** `shared/mcp-servers/google-tasks-mcp-server/credentials.json`
- **File:** `shared/mcp-servers/google-tasks-mcp-server/token.json`
- **Action:** Copy both files from original machine

#### Google Analytics MCP Server
- **File:** `shared/mcp-servers/google-analytics-mcp-server/credentials.json`
- **File:** `shared/mcp-servers/google-analytics-mcp-server/token.json`
- **Action:** Copy both files from original machine

#### Google Ads MCP Server
- **File:** `shared/mcp-servers/google-ads-mcp-server/credentials.json`
- **File:** `shared/mcp-servers/google-ads-mcp-server/token.json`
- **Action:** Copy both files from original machine

### 3. Email Sync Credentials
- **File:** `shared/email-sync/credentials.json`
- **Action:** Copy from original machine

### 4. Calendar Token
- **File:** `shared/calendar_token.json`
- **Action:** Copy from original machine

### 5. Environment Variables
Set these in your shell config (`~/.zshrc` or `~/.bashrc`):

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 6. Meta/Facebook Ads Credentials
- **File:** `shared/mcp-servers/meta-ads-mcp-server/.env`
- **Action:** Copy from original machine or recreate with:
  - `META_APP_ID`
  - `META_APP_SECRET`

### 7. LaunchAgents (if using)
- **Location:** `~/Library/LaunchAgents/com.petesbrain.*.plist`
- **Action:** These will be recreated by setup script, but you may need to update paths manually

## Quick Copy Commands

From your original machine, run these commands to copy credentials:

```bash
# Set these variables
ORIGINAL_PROJECT="/Users/administrator/Documents/PetesBrain"
NEW_PROJECT="$HOME/Documents/PetesBrain"

# Copy MCP config
cp "$ORIGINAL_PROJECT/.mcp.json" "$NEW_PROJECT/.mcp.json"

# Copy Google credentials
cp "$ORIGINAL_PROJECT/shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json" \
   "$NEW_PROJECT/shared/mcp-servers/google-drive-mcp-server/"
cp "$ORIGINAL_PROJECT/shared/mcp-servers/google-photos-mcp-server/"{credentials.json,token.json} \
   "$NEW_PROJECT/shared/mcp-servers/google-photos-mcp-server/"
cp "$ORIGINAL_PROJECT/shared/mcp-servers/google-sheets-mcp-server/credentials.json" \
   "$NEW_PROJECT/shared/mcp-servers/google-sheets-mcp-server/"
cp "$ORIGINAL_PROJECT/shared/mcp-servers/google-tasks-mcp-server/"{credentials.json,token.json} \
   "$NEW_PROJECT/shared/mcp-servers/google-tasks-mcp-server/"

# Copy email sync credentials
cp "$ORIGINAL_PROJECT/shared/email-sync/credentials.json" \
   "$NEW_PROJECT/shared/email-sync/"

# Copy calendar token
cp "$ORIGINAL_PROJECT/shared/calendar_token.json" \
   "$NEW_PROJECT/shared/"
```

## After Migration

1. Run `setup-new-machine.sh` to update paths and set up virtual environments
2. Copy credentials using commands above
3. Update `.mcp.json` paths if needed
4. Test each MCP server individually
5. Set up automatic syncing if on laptop

EOF

echo -e "${GREEN}✓ Credentials checklist created${NC}"
echo ""

# Create migration instructions
echo -e "${YELLOW}→ Creating migration instructions...${NC}"

cat > "$PACKAGE_DIR/MIGRATION-INSTRUCTIONS.md" << EOF
# PetesBrain Migration Instructions

**Package Created:** $(date)
**From Machine:** $(hostname)
**Project Path:** $PROJECT_DIR

## Step 1: Extract Package

On your new machine:

\`\`\`bash
cd ~/Documents
tar -xzf $PACKAGE_NAME.tar.gz
cd PetesBrain
\`\`\`

## Step 2: Run Setup Script

\`\`\`bash
chmod +x shared/scripts/setup-new-machine.sh
./shared/scripts/setup-new-machine.sh
\`\`\`

This script will:
- Check for required tools (Python, Git, etc.)
- Create virtual environments
- Update all paths in LaunchAgents and MCP configs
- Set up sync scripts

## Step 3: Copy Credentials

**IMPORTANT:** See \`CREDENTIALS-CHECKLIST.md\` for detailed instructions.

You must manually copy:
- \`.mcp.json\` file
- All OAuth credential files
- Environment variables

## Step 4: Update Paths in .mcp.json

After copying \`.mcp.json\`, update paths:

\`\`\`bash
# Replace old user path with new path
sed -i '' 's|/Users/administrator|$HOME|g' .mcp.json
sed -i '' 's|/Users/administrator/Documents/PetesBrain|$HOME/Documents/PetesBrain|g' .mcp.json
\`\`\`

Or edit manually to replace:
- \`/Users/administrator\` → \`\$HOME\`
- Old project path → New project path

## Step 5: Test Installation

\`\`\`bash
# Test Python environment
source venv/bin/activate
python3 --version

# Test sync (if on laptop)
sync-petesbrain pull

# Test MCP servers (restart Claude Desktop after updating .mcp.json)
\`\`\`

## Step 6: Set Up Automatic Syncing (Laptop Only)

\`\`\`bash
cd shared/scripts
./setup-auto-sync.sh laptop
\`\`\`

## Troubleshooting

### Virtual environments not created
- Run: \`python3 -m venv venv\` in project root
- For each MCP server: \`python3 -m venv shared/mcp-servers/[server-name]/.venv\`

### Paths still wrong
- Run setup script again: \`./shared/scripts/setup-new-machine.sh\`
- Manually edit LaunchAgents in \`agents/launchagents/\`
- Manually edit \`.mcp.json\`

### MCP servers not working
- Check credentials are copied correctly
- Verify paths in \`.mcp.json\` are correct
- Restart Claude Desktop
- Check logs in each MCP server directory

### Sync not working
- Check Git is configured: \`git remote -v\`
- Or set up iCloud Drive sync (see docs/SYNC-SYSTEM.md)

## Additional Resources

- **Installation Guide:** \`docs/LAPTOP-INSTALLATION-GUIDE.md\`
- **Sync System:** \`docs/SYNC-SYSTEM.md\`
- **Troubleshooting:** \`docs/TROUBLESHOOTING.md\`

EOF

echo -e "${GREEN}✓ Migration instructions created${NC}"
echo ""

# Copy setup script
echo -e "${YELLOW}→ Including setup script...${NC}"
if [ -f "$PROJECT_DIR/shared/scripts/setup-new-machine.sh" ]; then
    cp "$PROJECT_DIR/shared/scripts/setup-new-machine.sh" "$PACKAGE_DIR/shared/scripts/"
    chmod +x "$PACKAGE_DIR/shared/scripts/setup-new-machine.sh"
    echo -e "${GREEN}✓ Setup script included${NC}"
else
    echo -e "${YELLOW}⚠ Setup script not found${NC}"
fi

echo ""

# Create tarball
echo -e "${YELLOW}→ Creating tarball...${NC}"
cd "$OUTPUT_DIR"
tar -czf "$TARBALL" "$PACKAGE_NAME" || {
    echo -e "${RED}✗ Failed to create tarball${NC}"
    exit 1
}

echo -e "${GREEN}✓ Tarball created: $TARBALL${NC}"
echo ""

# Calculate size
SIZE=$(du -h "$TARBALL" | cut -f1)
echo -e "${BLUE}Package Size:${NC} $SIZE"
echo ""

# Summary
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}    Migration Package Created!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Package Location:${NC}"
echo "  $TARBALL"
echo ""
echo -e "${BLUE}Package Contents:${NC}"
echo "  • Complete PetesBrain project (excluding venv and credentials)"
echo "  • Setup script: shared/scripts/setup-new-machine.sh"
echo "  • Credentials checklist: CREDENTIALS-CHECKLIST.md"
echo "  • Migration instructions: MIGRATION-INSTRUCTIONS.md"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Transfer the tarball to your new machine:"
echo "   - Via USB drive"
echo "   - Via network: scp $TARBALL user@newmachine:~/Desktop/"
echo "   - Via iCloud Drive"
echo ""
echo "2. On new machine, extract and follow MIGRATION-INSTRUCTIONS.md"
echo ""
echo "3. Copy credentials manually (see CREDENTIALS-CHECKLIST.md)"
echo ""
echo -e "${RED}⚠ IMPORTANT:${NC} Credentials are NOT included in the package!"
echo "You must copy them manually for security reasons."
echo ""

