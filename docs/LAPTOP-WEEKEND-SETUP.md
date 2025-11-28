# PetesBrain Laptop Setup - Weekend Work Clone

**Purpose:** Clone PetesBrain to your laptop so you can work on weekends away from your desktop  
**Type:** Sync/Clone setup (NOT permanent migration)  
**Desktop:** Primary machine (main work location)  
**Laptop:** Secondary machine (weekend/travel work)

---

## What This Setup Does

✅ **Clones PetesBrain** to your laptop  
✅ **Keeps both machines in sync** - changes sync between desktop ↔ laptop  
✅ **Works on either machine** - desktop during week, laptop on weekends  
✅ **Automatic syncing** - optional background sync every hour  
✅ **Manual sync** - pull latest before starting work, push before closing  

---

## Your Workflow

### During the Week (Desktop)
- Work normally on desktop
- Changes auto-sync every 2 hours (or manually push)
- Desktop is your primary machine

### Weekend Setup (Laptop)
1. **Before starting work:**
   ```bash
   sync-petesbrain pull
   ```
   Gets latest changes from desktop

2. **Work normally** - Make changes, add files, etc.

3. **Before closing:**
   ```bash
   sync-petesbrain push
   ```
   Sends your changes back to desktop

4. **Automatic:** Laptop pulls latest every hour (optional)

### Back on Desktop (Monday)
- Desktop automatically has all weekend changes
- Or manually pull: `sync-petesbrain pull`

---

## Setup Process

### Step 1: Clone PetesBrain to Laptop

**Option A: Git Clone (Recommended)**
```bash
cd ~/Documents
git clone <your-repo-url> PetesBrain
cd PetesBrain
```

**Option B: From iCloud Backup**
```bash
cd ~/Documents
tar -xzf ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-LATEST.tar.gz
```

**Option C: Via Network (rsync)**
```bash
rsync -avz administrator@desktop:/Users/administrator/Documents/PetesBrain ~/Documents/
```

### Step 2: Run Setup Script

This sets up everything for the laptop:
- Creates virtual environments
- Updates paths (from `/Users/administrator` to your laptop user)
- Sets up sync scripts
- Configures everything

```bash
cd ~/Documents/PetesBrain
chmod +x shared/scripts/setup-new-machine.sh
./shared/scripts/setup-new-machine.sh
```

### Step 3: Copy Credentials

Copy these files from desktop to laptop:
- `.mcp.json` - MCP server configuration
- `shared/email-sync/credentials.json`
- `shared/mcp-servers/*/credentials.json` (OAuth files)
- `shared/mcp-servers/*/token.json` (if they exist)

**Quick copy via network:**
```bash
# From laptop
scp administrator@desktop:/Users/administrator/Documents/PetesBrain/.mcp.json ~/Documents/PetesBrain/
scp administrator@desktop:/Users/administrator/Documents/PetesBrain/shared/email-sync/credentials.json ~/Documents/PetesBrain/shared/email-sync/
# Repeat for other credential files
```

### Step 4: Set Up Sync (Optional but Recommended)

**On Laptop:**
```bash
cd ~/Documents/PetesBrain/shared/scripts
./setup-auto-sync.sh laptop
```

This creates automatic syncing that pulls latest changes every hour.

---

## Daily Usage

### On Laptop (Weekend Work)

**Before starting:**
```bash
sync-petesbrain pull    # Get latest from desktop
```

**While working:**
- Work normally - make changes, add files
- Automatic sync pulls every hour (if enabled)

**Before closing:**
```bash
sync-petesbrain push    # Send changes back to desktop
```

### On Desktop (Weekday Work)

**Before closing:**
```bash
sync-petesbrain push    # Push changes to remote
```

**Automatic:** Desktop pushes every 2 hours (if enabled)

---

## Sync Methods

### 1. Git-Based Sync (Recommended) ⭐

**Best for:** Version control, conflict resolution, reliable sync

**Setup:**
- Desktop: `git remote add origin <repo-url>` (if not already done)
- Desktop: `git push -u origin main`
- Laptop: Already cloned, sync script uses Git automatically

**Usage:**
```bash
sync-petesbrain pull   # Git pull
sync-petesbrain push   # Git push
sync-petesbrain both   # Pull then push
```

### 2. iCloud Drive Sync

**Best for:** Simple setup, no Git needed

**Setup:**
- Desktop creates backups automatically
- Laptop extracts from iCloud backups

**Usage:**
```bash
sync-petesbrain pull   # Extract latest backup
sync-petesbrain push   # Create new backup
```

### 3. rsync Direct Sync

**Best for:** Fast local network sync

**Usage:**
```bash
sync-petesbrain pull   # Sync from desktop
```

---

## What Gets Synced

✅ **Code & Scripts** - All Python scripts, shell scripts  
✅ **Documentation** - All markdown files, guides  
✅ **Client Data** - Client folders, documents, notes  
✅ **Configuration** - Updated paths for laptop  
✅ **Tools** - All tools and utilities  

❌ **NOT Synced** (for security):
- Virtual environments (recreated on laptop)
- Credentials (copied manually)
- Large cache files
- `.git` folder (if using Git sync)

---

## Important Notes

### This is NOT a Migration
- Desktop remains your primary machine
- Laptop is a clone for weekend/travel work
- Both machines stay in sync
- You can work on either machine

### Credentials
- Credentials are NOT synced (security)
- Copy them manually from desktop
- See `docs/MIGRATION-SYSTEM-COMPLETE.md` for full list

### Virtual Environments
- Created fresh on laptop by setup script
- Don't need to sync venv folders
- Setup script handles this automatically

### Paths
- Setup script updates all paths automatically
- Changes `/Users/administrator` → your laptop username
- Updates LaunchAgents, MCP configs, etc.

---

## Troubleshooting

### Sync Conflicts

**Git conflicts:**
```bash
# View conflicts
git status

# Resolve manually, then:
git add .
git commit -m "Resolved conflicts"
sync-petesbrain push
```

### Laptop Out of Sync

**Pull latest:**
```bash
sync-petesbrain pull
```

**Force pull (discard local changes):**
```bash
git fetch origin
git reset --hard origin/main
```

### Credentials Not Working

- Make sure you copied all credential files
- Check paths in `.mcp.json` are correct
- Restart Claude Desktop after updating `.mcp.json`

---

## Quick Reference

```bash
# Check status
./shared/scripts/check-migration-status.sh

# Sync commands
sync-petesbrain pull    # Get latest
sync-petesbrain push    # Send changes
sync-petesbrain both    # Pull then push

# Setup automatic sync
cd shared/scripts && ./setup-auto-sync.sh laptop

# Check sync status
launchctl list | grep petesbrain.sync

# View sync logs
tail -f ~/.petesbrain-sync.log
```

---

## Summary

**What you're doing:**
- Cloning PetesBrain to laptop for weekend work
- Setting up sync so both machines stay in sync
- Desktop = primary, Laptop = secondary

**What you're NOT doing:**
- Permanent migration (desktop stays primary)
- Moving everything (it's a clone/sync)
- Replacing desktop (both machines work together)

**Result:**
- Work on desktop during week ✅
- Work on laptop on weekends ✅
- Changes sync between both ✅
- Everything stays in sync ✅

---

**For detailed setup instructions, see:**
- `docs/LAPTOP-INSTALLATION-GUIDE.md` - Step-by-step setup
- `docs/SYNC-SYSTEM.md` - Complete sync documentation
- `docs/LAPTOP-MIGRATION-NEXT-STEPS.md` - Current status & next steps

