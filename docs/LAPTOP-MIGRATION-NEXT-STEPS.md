# Laptop Setup - Weekend Work Clone

**Last Updated:** November 7, 2025  
**Status:** Ready to check Python 3 and continue setup  
**Purpose:** Clone PetesBrain to laptop for weekend/travel work (NOT permanent migration)

## What This Is

✅ **Cloning PetesBrain** to your laptop so you can work on weekends  
✅ **Syncing** between desktop (primary) and laptop (secondary)  
✅ **Weekend workflow** - pull before work, push before closing  
✅ **Desktop stays primary** - laptop is for weekend/travel work

**See:** `docs/LAPTOP-WEEKEND-SETUP.md` for complete overview

## What's Been Done

Based on your progress, you've completed:

1. ✅ **Laptop Upgraded** - You upgraded your laptop
2. ✅ **Migration Scripts Created** - Setup scripts are ready to use
3. ✅ **Documentation Available** - Comprehensive guides are in place
4. ✅ **ZSH Configured** - Default shell is ZSH (macOS standard)

## Current State

You're ready to check if Python 3 is installed and continue with the migration setup.

## First Step: Check Python 3

**Before proceeding, verify Python 3 is installed:**

```bash
python3 --version
```

**See:** `docs/CHECK-PYTHON3.md` for detailed instructions on:
- How to check if Python 3 is installed
- How to install it if missing
- Troubleshooting common issues

## Quick Status Check

Run this command to see exactly where you are:

```bash
cd ~/Documents/PetesBrain
./shared/scripts/check-migration-status.sh
```

This will show you:
- What's already set up
- What still needs to be done
- Specific commands to run next

## Next Steps (In Order)

### Step 0: Check Python 3 Installation

**First, verify Python 3 is installed:**

```bash
python3 --version
```

**If you see:** `Python 3.x.x` → ✅ Python 3 is installed, continue to Step 1

**If you see:** `command not found` → Install Python 3 first

**Important:** If you see a message about Xcode Command Line Tools, install those first (see `docs/XCODE-COMMAND-LINE-TOOLS.md`), then install Python 3 (see `docs/CHECK-PYTHON3.md`)

### Step 1: Verify Python 3 is Working

Once Python 3 is installed, verify pip is available:

```bash
pip3 --version  # or: python3 -m pip --version
```

If both work, you're good to continue!

### Step 2: Run the Setup Script

This is the main script that will:
- Create all virtual environments
- Update paths in LaunchAgents and MCP configs
- Set up sync scripts
- Validate everything

```bash
cd ~/Documents/PetesBrain
chmod +x shared/scripts/setup-new-machine.sh
./shared/scripts/setup-new-machine.sh
```

**What it does:**
- ✅ Checks Python 3, pip, Git are installed
- ✅ Creates main `venv/` virtual environment
- ✅ Creates `.venv/` for each MCP server
- ✅ Updates all paths from `/Users/administrator` to your user
- ✅ Updates paths in `.mcp.json`
- ✅ Updates paths in LaunchAgent plist files
- ✅ Sets up sync script alias
- ✅ Validates configuration files

### Step 3: Copy Credentials

After running the setup script, you'll need to copy credentials from your desktop:

**Critical files to copy:**
- `.mcp.json` - MCP server configuration
- `shared/email-sync/credentials.json` - Email sync credentials
- `shared/mcp-servers/*/credentials.json` - OAuth credentials for each MCP server
- `shared/mcp-servers/*/token.json` - OAuth tokens (if they exist)

**Quick copy commands** (run from desktop):

```bash
# Set variables
ORIGINAL_PROJECT="/Users/administrator/Documents/PetesBrain"
NEW_PROJECT="$HOME/Documents/PetesBrain"  # Update with laptop path

# Copy MCP config
scp "$ORIGINAL_PROJECT/.mcp.json" user@laptop:"$NEW_PROJECT/"

# Copy email credentials
scp "$ORIGINAL_PROJECT/shared/email-sync/credentials.json" \
    user@laptop:"$NEW_PROJECT/shared/email-sync/"

# Copy Google credentials (example - repeat for each server)
scp "$ORIGINAL_PROJECT/shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json" \
    user@laptop:"$NEW_PROJECT/shared/mcp-servers/google-drive-mcp-server/"
```

Or use iCloud Drive, USB drive, or network share to transfer files.

### Step 4: Update Paths in .mcp.json (If Needed)

After copying `.mcp.json`, update paths:

```bash
cd ~/Documents/PetesBrain
sed -i '' 's|/Users/administrator|'"$HOME"'|g' .mcp.json
sed -i '' 's|/Users/administrator/Documents/PetesBrain|'"$HOME/Documents/PetesBrain"'|g' .mcp.json
```

Or run the setup script again - it will update paths automatically.

### Step 5: Set Up Environment Variables

Add your API keys to shell config:

```bash
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### Step 6: Test Everything

```bash
# Test Python environment
source venv/bin/activate
python3 --version
deactivate

# Test sync (if Git is set up)
sync-petesbrain pull

# Test MCP servers (restart Claude Desktop after updating .mcp.json)
```

### Step 7: Set Up Automatic Syncing (Optional)

```bash
cd ~/Documents/PetesBrain/shared/scripts
./setup-auto-sync.sh laptop
```

This creates a LaunchAgent that syncs every hour.

## Common Issues & Solutions

### "Python 3 not found" after installation
- Make sure Python 3 is in your PATH
- Try: `which python3` to find it
- On macOS, may need: `brew install python3`

### Virtual environments not creating
- Check Python 3 works: `python3 --version`
- Check permissions: `ls -la venv/`
- Try manually: `python3 -m venv venv`

### Paths still wrong after setup
- Run setup script again: `./shared/scripts/setup-new-machine.sh`
- Or manually edit `.mcp.json` and LaunchAgent plist files

### Credentials not working
- Make sure you copied all credential files
- Check file permissions: `ls -la shared/mcp-servers/*/credentials.json`
- Verify paths in `.mcp.json` are correct

## What Each Script Does

### `setup-new-machine.sh`
**Purpose:** Complete setup for new machine  
**When to use:** First time setting up on laptop  
**What it does:**
- Checks tools (Python, Git, etc.)
- Creates virtual environments
- Updates all paths
- Sets up sync alias

### `check-migration-status.sh`
**Purpose:** Check current migration status  
**When to use:** Anytime to see what's done/what's left  
**What it does:**
- Checks Python installation
- Checks virtual environments
- Checks path updates
- Checks credentials
- Shows next steps

### `sync-petesbrain.sh`
**Purpose:** Sync between desktop and laptop  
**When to use:** Daily, before/after work  
**What it does:**
- Pulls latest changes (laptop)
- Pushes your changes (desktop)
- Syncs via Git or iCloud Drive

### `setup-auto-sync.sh`
**Purpose:** Set up automatic syncing  
**When to use:** After initial setup  
**What it does:**
- Creates LaunchAgent for automatic sync
- Desktop: pushes every 2 hours
- Laptop: pulls every hour

## Documentation Reference

- **Installation Guide:** `docs/LAPTOP-INSTALLATION-GUIDE.md` - Step-by-step walkthrough
- **Migration System:** `docs/MIGRATION-SYSTEM-COMPLETE.md` - Complete overview
- **Sync System:** `docs/SYNC-SYSTEM.md` - Sync documentation
- **Troubleshooting:** `docs/TROUBLESHOOTING.md` - Common issues

## Quick Command Reference

```bash
# Check status
./shared/scripts/check-migration-status.sh

# Run full setup
./shared/scripts/setup-new-machine.sh

# Sync with desktop
sync-petesbrain pull

# Push changes to desktop
sync-petesbrain push

# Set up automatic sync
cd shared/scripts && ./setup-auto-sync.sh laptop
```

## You're Ready!

Since Python 3 is installed, you can now:

1. **Run the status check** to see current state
2. **Run the setup script** to complete migration
3. **Copy credentials** from desktop
4. **Test everything** and start working!

---

**Need help?** Check the status script output - it will tell you exactly what to do next!

