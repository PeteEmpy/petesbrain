# PetesBrain Migration System - Implementation Complete

**Date:** November 7, 2025  
**Status:** ✅ Complete

## Overview

The laptop migration project has been completed with comprehensive scripts and documentation for transferring PetesBrain to a new machine.

## What Was Created

### 1. Setup Script (`setup-new-machine.sh`)

**Location:** `shared/scripts/setup-new-machine.sh`

A comprehensive setup script that automates the entire migration process:

- ✅ **Tool Checking**: Verifies Python 3, pip, Git, Node.js
- ✅ **Virtual Environments**: Creates main venv and all MCP server venvs
- ✅ **Path Updates**: Automatically updates paths in:
  - LaunchAgent plist files (`agents/launchagents/*.plist`)
  - MCP configuration (`.mcp.json`)
- ✅ **Credential Setup**: Prompts for API keys and environment variables
- ✅ **Directory Creation**: Creates necessary directories
- ✅ **Validation**: Validates JSON and plist syntax
- ✅ **Sync Setup**: Configures sync script alias

**Usage:**
```bash
cd ~/Documents/PetesBrain
chmod +x shared/scripts/setup-new-machine.sh
./shared/scripts/setup-new-machine.sh
```

### 2. Migration Package Creator (`create-migration-package.sh`)

**Location:** `shared/scripts/create-migration-package.sh`

Creates a complete migration package for one-time transfers:

- ✅ **Tarball Creation**: Packages entire project (excludes venv, credentials)
- ✅ **Credentials Checklist**: Documents all credentials that need manual copying
- ✅ **Migration Instructions**: Step-by-step guide for new machine
- ✅ **Setup Script Inclusion**: Includes setup script in package

**Usage:**
```bash
cd ~/Documents/PetesBrain
./shared/scripts/create-migration-package.sh [output-dir]
```

### 3. Existing Tools (Already Available)

- ✅ **Sync Script**: `shared/scripts/sync-petesbrain.sh` - For ongoing sync
- ✅ **Auto-Sync Setup**: `shared/scripts/setup-auto-sync.sh` - LaunchAgent setup
- ✅ **Installation Guide**: `docs/LAPTOP-INSTALLATION-GUIDE.md` - Step-by-step guide
- ✅ **Sync Documentation**: `docs/SYNC-SYSTEM.md` - Sync system docs

## Migration Workflow

### Option A: Git-Based Migration (Recommended)

1. **On Desktop:**
   ```bash
   cd ~/Documents/PetesBrain
   git add -A
   git commit -m "Pre-migration commit"
   git push
   ```

2. **On Laptop:**
   ```bash
   cd ~/Documents
   git clone <repo-url> PetesBrain
   cd PetesBrain
   ./shared/scripts/setup-new-machine.sh
   ```

3. **Copy Credentials:**
   - Copy `.mcp.json`
   - Copy OAuth credential files
   - Set environment variables

4. **Set Up Sync:**
   ```bash
   cd shared/scripts
   ./setup-auto-sync.sh laptop
   ```

### Option B: Migration Package

1. **On Desktop:**
   ```bash
   cd ~/Documents/PetesBrain
   ./shared/scripts/create-migration-package.sh ~/Desktop
   ```

2. **Transfer Package:**
   - Copy tarball to new machine (USB, network, iCloud)

3. **On New Machine:**
   ```bash
   cd ~/Documents
   tar -xzf PetesBrain-migration-*.tar.gz
   cd PetesBrain
   ./shared/scripts/setup-new-machine.sh
   ```

4. **Follow Instructions:**
   - See `CREDENTIALS-CHECKLIST.md` in package
   - Copy credentials manually
   - Follow `MIGRATION-INSTRUCTIONS.md`

## What Gets Updated Automatically

### LaunchAgents
- All paths in `agents/launchagents/*.plist`
- Replaces `/Users/administrator` with current user
- Replaces old project path with new project path
- Validates plist syntax

### MCP Configuration
- Updates all paths in `.mcp.json`
- Updates Python venv paths
- Updates credential file paths
- Validates JSON syntax

### Virtual Environments
- Creates main `venv/` if missing
- Creates `.venv/` for each MCP server:
  - google-analytics-mcp-server
  - google-ads-mcp-server
  - google-photos-mcp-server
  - google-sheets-mcp-server
  - google-tasks-mcp-server
  - facebook-ads-mcp-server
  - email-sync

## What Needs Manual Setup

### Credentials (Security)
These are **NOT** included in migration packages for security:

- `.mcp.json` - MCP server configuration
- OAuth credential files (`.json` files in MCP servers)
- OAuth token files (`token.json`)
- Google service account credentials
- Environment variables (ANTHROPIC_API_KEY, etc.)

See `CREDENTIALS-CHECKLIST.md` in migration package for complete list.

### Post-Migration Steps

1. **Copy Credentials**: Use checklist to copy all credential files
2. **Update Paths**: Run setup script (handles most paths automatically)
3. **Test MCP Servers**: Restart Claude Desktop and test each server
4. **Set Up Sync**: Configure automatic syncing if on laptop
5. **Verify LaunchAgents**: Check that agents are running correctly

## Testing Recommendations

After migration, test:

1. **Python Environment:**
   ```bash
   source venv/bin/activate
   python3 --version
   ```

2. **Sync Script:**
   ```bash
   sync-petesbrain pull
   ```

3. **MCP Servers:**
   - Restart Claude Desktop
   - Test each MCP server individually
   - Check logs if issues occur

4. **LaunchAgents:**
   ```bash
   launchctl list | grep petesbrain
   ```

## Documentation

- **Installation Guide**: `docs/LAPTOP-INSTALLATION-GUIDE.md`
- **Sync System**: `docs/SYNC-SYSTEM.md`
- **Quick Start**: `docs/SYNC-QUICK-START.md`
- **Troubleshooting**: `docs/TROUBLESHOOTING.md`

## Benefits

✅ **Easy Migration**: One script handles entire setup  
✅ **Secure**: Credentials kept separate  
✅ **Automated**: Path updates happen automatically  
✅ **Validated**: Syntax checking prevents errors  
✅ **Documented**: Comprehensive guides included  
✅ **Flexible**: Multiple migration options available  

## Next Steps

1. Test migration on a test machine
2. Document any edge cases encountered
3. Update documentation based on real-world usage
4. Consider adding backup/restore functionality

---

**Status**: Ready for use  
**Last Updated**: November 7, 2025

