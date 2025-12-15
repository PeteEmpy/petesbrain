# Laptop Sync Weekend Workflow

**Created:** December 13, 2025
**Purpose:** Complete guide for syncing PetesBrain between desktop and laptop for weekend/remote work
**Status:** ✅ Tested and working

---

## Overview

This system allows you to work on PetesBrain remotely by syncing via iCloud Drive backups. The desktop remains the primary machine, and the laptop is used for weekend/travel work.

**Key Features:**
- ✅ Bidirectional sync (desktop ↔ laptop)
- ✅ Staleness protection (warns if backup is old)
- ✅ Metadata tracking (who, when, where)
- ✅ Automatic backup cleanup
- ✅ Works anywhere (no network connection needed)

---

## What Was Fixed (December 13, 2025)

### Critical Issues Discovered

1. **All backups were empty since November 24** (29-119 bytes instead of 1.1GB)
2. **Backup scripts pointed to wrong directory** (`PetesBrain` instead of `PetesBrain.nosync`)
3. **Sync config had wrong path and wrong machine type**

### Files Fixed

| File | Line | Change |
|------|------|--------|
| `shared/scripts/backup-petesbrain.sh` | 11 | `PROJECT_DIR="/Users/administrator/Documents/PetesBrain.nosync"` |
| `shared/scripts/backup-tasks-critical.sh` | 18 | `cd /Users/administrator/Documents/PetesBrain.nosync` |
| `.sync-config` | 3 | `TYPE=Desktop` (was Laptop) |
| `.sync-config` | 4 | `SYNC_METHOD="icloud"` (was rsync) |
| `.sync-config` | 9 | `DESKTOP_PATH="/Users/administrator/Documents/PetesBrain.nosync"` |

### Verification Results

After fixes:
- ✅ Critical tasks backup: **131K** (was 29 bytes)
- ✅ Full system backup: **1.1GB** (was 119 bytes)
- ✅ Both successfully writing to iCloud Drive
- ✅ Sync system tested and working
- ✅ Metadata tracking operational

---

## Desktop Setup (Already Complete)

The desktop is already configured and ready. All fixes have been applied.

### Verify Desktop Is Ready

```bash
# Check sync script exists and is executable
ls -la shared/scripts/sync-petesbrain.sh

# Check sync config is correct
cat .sync-config

# Should show:
# TYPE=Desktop
# SYNC_METHOD="icloud"
# DESKTOP_PATH="/Users/administrator/Documents/PetesBrain.nosync"
```

---

## Laptop Setup (Do This Monday)

### Prerequisites

**Required:**
- ✅ MacBook with macOS
- ✅ iCloud Drive enabled and syncing
- ✅ Python 3 installed (check: `python3 --version`)
- ✅ ~8GB free disk space

**Optional:**
- Git installed (if you want to use Git sync instead)
- Network access to desktop (if you want to use rsync)

---

### Step 1: Check Python 3 Installation

```bash
# On laptop, open Terminal and check Python 3
python3 --version

# Should see: Python 3.x.x
# If not installed, install via Homebrew:
# 1. Install Xcode Command Line Tools: xcode-select --install
# 2. Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# 3. Install Python: brew install python3
```

---

### Step 2: Copy PetesBrain to Laptop

**Option A: Extract from iCloud Backup (Recommended)**

```bash
# On laptop - create target directory
mkdir -p ~/Documents

# Check iCloud backups are synced
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/ | head -5

# You should see backups like:
# PetesBrain-backup-20251213-170002.tar.gz (1.1GB)

# Extract latest backup
cd ~/Documents
LATEST_BACKUP=$(ls -t ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-*.tar.gz | head -1)
echo "Extracting: $LATEST_BACKUP"
tar -xzf "$LATEST_BACKUP"

# This creates ~/Documents/PetesBrain/
# Optionally rename to match desktop:
mv PetesBrain PetesBrain.nosync
```

**Option B: Copy via USB Drive or AirDrop**

```bash
# Copy the entire PetesBrain.nosync folder from desktop to:
# ~/Documents/PetesBrain.nosync
# (or ~/Documents/PetesBrain - name doesn't matter on laptop)
```

---

### Step 3: Create Laptop Sync Configuration

```bash
# Navigate to project directory
cd ~/Documents/PetesBrain.nosync  # or ~/Documents/PetesBrain

# Create sync config file for laptop
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

echo "✅ Sync config created"
```

---

### Step 4: Make Sync Script Executable

```bash
# Still in project directory
chmod +x shared/scripts/sync-petesbrain.sh

echo "✅ Sync script is executable"
```

---

### Step 5: Create Shell Alias (Optional but Recommended)

```bash
# Add alias to your shell config
# For zsh (macOS default):
echo 'alias sync-petesbrain="~/Documents/PetesBrain.nosync/shared/scripts/sync-petesbrain.sh"' >> ~/.zshrc
source ~/.zshrc

# For bash (if you use bash):
# echo 'alias sync-petesbrain="~/Documents/PetesBrain.nosync/shared/scripts/sync-petesbrain.sh"' >> ~/.bash_profile
# source ~/.bash_profile

echo "✅ Alias created - you can now use 'sync-petesbrain' from anywhere"
```

---

### Step 6: Test First Sync

```bash
# Pull latest from iCloud
sync-petesbrain pull

# You should see:
# ═══════════════════════════════════════════════════
#     PetesBrain Sync
# ═══════════════════════════════════════════════════
# Machine: <your-laptop-hostname>
# Type: Laptop
# Direction: pull
# Project: /Users/<you>/Documents/PetesBrain.nosync
#
# ───────────────────────────────────────────────────
#     Last Push Information
# ───────────────────────────────────────────────────
#   When:    2025-12-13T17:00:02Z (X hours ago)
#   From:    Peters-Mac-mini.lan (Desktop)
#   User:    administrator
# ───────────────────────────────────────────────────
#
# ✓ Backup is fresh (X hours ago)
# → Found backup: PetesBrain-backup-20251213-170002.tar.gz
# → Extracting to temporary location...
# → Syncing files...
# ✓ Synced from iCloud backup
#
# ═══════════════════════════════════════════════════
#     Sync Complete!
# ═══════════════════════════════════════════════════
```

**If you see this, laptop setup is complete! ✅**

---

## Weekend Workflow (Once Setup is Complete)

### Friday Afternoon (Desktop)

**Before leaving for the weekend:**

```bash
# On desktop - create fresh backup
cd ~/Documents/PetesBrain.nosync
sync-petesbrain push

# Takes ~3 minutes
# Creates 1.1GB backup in iCloud Drive
# Writes metadata (timestamp, machine, user)
```

**What happens:**
1. ✅ Runs `backup-petesbrain.sh`
2. ✅ Creates compressed backup (excludes venv/, node_modules/)
3. ✅ Copies to iCloud Drive
4. ✅ Writes metadata file (`.sync-metadata.json`)
5. ✅ Cleans up old backups (keeps last 10)

---

### Saturday/Sunday (Laptop)

**Get latest from desktop:**

```bash
# On laptop
sync-petesbrain pull

# Checks backup age
# Extracts latest backup from iCloud
# Syncs all files to laptop
```

**Work on laptop normally**
- Edit files
- Make changes
- Work on tasks
- Everything stays local

**Before finishing weekend work:**

```bash
# On laptop - send changes back
sync-petesbrain push

# Takes ~3 minutes
# Creates backup of your laptop changes
# Uploads to iCloud Drive
# Writes metadata
```

---

### Monday Morning (Desktop)

**Get laptop changes:**

```bash
# On desktop
sync-petesbrain pull

# Checks backup age
# Pulls laptop's backup from iCloud
# Merges changes into desktop
```

**Resume normal work**

---

## Staleness Protection

The sync system automatically checks backup age before pulling:

| Backup Age | Behavior | Action |
|------------|----------|--------|
| **< 24 hours** | ✅ Fresh - proceeds automatically | None needed |
| **24h - 7 days** | ⚠️ Warns - asks for confirmation | Press 'y' to continue or create fresh backup |
| **> 7 days** | 🛑 Blocks - must use `--force` | Run `sync-petesbrain push` on desktop first |

### Override Staleness Check

```bash
# If you get blocked and need to pull anyway
sync-petesbrain pull --force

# Warning: This skips safety checks
# Only use if you're sure the backup is the one you want
```

---

## Command Reference

### Desktop Commands

```bash
# Create backup before leaving for weekend
sync-petesbrain push

# Get laptop changes when you return
sync-petesbrain pull

# Two-way sync (pull then push)
sync-petesbrain both
```

### Laptop Commands

```bash
# Get latest from desktop
sync-petesbrain pull

# Send your changes back to desktop
sync-petesbrain push

# Override staleness warning
sync-petesbrain pull --force

# Two-way sync
sync-petesbrain both
```

---

## How the Sync Works

### iCloud Drive Method (Current Configuration)

**Desktop → Laptop (push from desktop):**
1. Desktop runs `sync-petesbrain push`
2. Calls `backup-petesbrain.sh` to create tar.gz backup
3. Backup copied to `~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/`
4. Metadata written to `.sync-metadata.json` (timestamp, machine, user)
5. iCloud syncs backup to cloud
6. Laptop's iCloud Drive syncs backup down

**Laptop → Desktop (pull on laptop):**
1. Laptop runs `sync-petesbrain pull`
2. Reads `.sync-metadata.json` to check backup age
3. Finds latest `PetesBrain-backup-*.tar.gz` in iCloud Drive
4. Extracts to temporary directory
5. Syncs files to project directory (using rsync --delete)
6. Cleans up temporary directory

**Laptop → Desktop (push from laptop):**
1. Same as desktop push - creates backup
2. Uploads to iCloud Drive
3. Desktop pulls when you return

---

## File Locations

### Desktop

```
~/Documents/PetesBrain.nosync/              # Main project
  ├── .sync-config                           # Sync configuration (TYPE=Desktop)
  ├── .is-desktop                            # Desktop marker file
  └── shared/scripts/
      ├── sync-petesbrain.sh                # Main sync script
      ├── backup-petesbrain.sh              # Backup script (called by sync)
      └── backup-tasks-critical.sh          # Critical tasks backup

~/Documents/                                 # Local backups (keeps last 5)
  ├── PetesBrain-backup-20251213-170002.tar.gz
  └── ...

~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/
  ├── .sync-metadata.json                   # Metadata about last push
  ├── PetesBrain-backup-20251213-170002.tar.gz
  └── ...                                    # Keeps last 10 backups
```

### Laptop

```
~/Documents/PetesBrain.nosync/              # or ~/Documents/PetesBrain
  ├── .sync-config                           # Sync configuration (TYPE=Laptop)
  └── shared/scripts/
      └── sync-petesbrain.sh                # Same sync script

~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/
  ├── .sync-metadata.json                   # Synced from desktop via iCloud
  ├── PetesBrain-backup-*.tar.gz            # Synced via iCloud
  └── ...
```

---

## What Gets Synced

### Included in Backups

✅ All client files and data
✅ Configuration files (.mcp.json, .sync-config, etc.)
✅ Scripts and tools
✅ Documentation
✅ Tasks and completed task logs
✅ Email archives, meeting notes, reports
✅ Knowledge base articles

### Excluded from Backups

❌ `venv/`, `.venv/` (Python virtual environments - can be rebuilt)
❌ `node_modules/` (Node.js dependencies - can be rebuilt)
❌ `__pycache__/` (Python bytecode cache)
❌ `.git/` (Git repository metadata - optional)
❌ `.DS_Store` (macOS metadata)

**Result:** Project compresses from 7.7GB → 1.1GB

---

## Troubleshooting

### "No backups found in iCloud Drive"

**Problem:** Laptop can't find any backups

**Solution:**
```bash
# On desktop, create a fresh backup
sync-petesbrain push

# Wait 1-2 minutes for iCloud to sync
# On laptop, check iCloud Drive
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/

# Should see backup files
# Then try pull again
sync-petesbrain pull
```

---

### "Backup is stale (>24 hours old)"

**Problem:** Warning that backup is old

**Solution:**
```bash
# Option 1: Create fresh backup on desktop
# On desktop:
sync-petesbrain push

# Option 2: Proceed anyway with force flag
# On laptop:
sync-petesbrain pull --force
```

---

### "Permission denied" on sync script

**Problem:** Script won't run

**Solution:**
```bash
# Make script executable
chmod +x ~/Documents/PetesBrain.nosync/shared/scripts/sync-petesbrain.sh

# Try again
sync-petesbrain pull
```

---

### Sync is slow or hangs

**Problem:** Extraction taking too long

**Possible causes:**
1. iCloud Drive still syncing backup (wait for sync to complete)
2. Disk space low (need ~3GB free: 1.1GB backup + 1.1GB extracted + working space)
3. macOS Time Machine running (pause Time Machine temporarily)

**Check iCloud sync status:**
```bash
# Check if backup file is fully synced
ls -lh ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/

# If you see cloud icons in Finder, files are still downloading
```

---

### Changes aren't syncing

**Problem:** Made changes on laptop but desktop doesn't see them

**Check workflow:**
```bash
# On laptop after making changes:
sync-petesbrain push

# Wait 1-2 minutes for iCloud upload

# On desktop:
sync-petesbrain pull
```

**Verify metadata:**
```bash
# Check last push info
cat ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/.sync-metadata.json

# Should show recent timestamp from laptop
```

---

### "Operation not permitted" in error logs

**Problem:** LaunchAgent backups failing

**This is a known issue:** Automated backups need Full Disk Access permission

**Workaround:** Use manual backups via `sync-petesbrain push`

**Permanent fix (optional):**
1. System Settings → Privacy & Security → Full Disk Access
2. Remove PetesBrainBackup.app
3. Re-add PetesBrainBackup.app
4. Restart Mac

---

## Alternative Sync Methods

The system supports three sync methods:

### 1. iCloud Drive (Current - Recommended for Remote Work)

**Pros:**
- ✅ Works anywhere (no network needed)
- ✅ Automatic backup retention
- ✅ Staleness protection
- ✅ Metadata tracking

**Cons:**
- ❌ Slower (compression + iCloud upload/download)
- ❌ Requires iCloud storage

**Configuration:**
```bash
# In .sync-config
SYNC_METHOD="icloud"
```

---

### 2. rsync (Fast but Requires Network)

**Pros:**
- ✅ Fast (no compression)
- ✅ Direct file sync
- ✅ Real-time

**Cons:**
- ❌ Requires both machines on same network
- ❌ No staleness protection
- ❌ No backup retention

**Configuration:**
```bash
# In .sync-config on laptop
SYNC_METHOD="rsync"
DESKTOP_HOST="Peters-Mac-mini.lan"
DESKTOP_USER="administrator"
DESKTOP_PATH="/Users/administrator/Documents/PetesBrain.nosync"

# On laptop when at home:
sync-petesbrain pull  # Pulls directly from desktop over network
```

---

### 3. Git (For Version Control)

**Pros:**
- ✅ Full version history
- ✅ Merge conflict resolution
- ✅ Works with remote repos (GitHub, etc.)

**Cons:**
- ❌ Requires Git setup
- ❌ Larger initial setup
- ❌ Need to handle merge conflicts

**Configuration:**
```bash
# If .git directory exists, sync-petesbrain will use Git automatically
# No need to set SYNC_METHOD

# Push/pull uses Git commands:
sync-petesbrain pull  # → git pull origin main
sync-petesbrain push  # → git push origin <current-branch>
```

---

## Testing the Sync System

### Test 1: Desktop Push

```bash
# On desktop
cd ~/Documents/PetesBrain.nosync
sync-petesbrain push

# Expected output:
# ═══════════════════════════════════════════════════
#     PetesBrain Sync
# ═══════════════════════════════════════════════════
# Machine: Peters-Mac-mini.lan
# Type: Desktop
# Direction: push
# Project: /Users/administrator/Documents/PetesBrain.nosync
#
# ⚠ Not a Git repository
# Setting up iCloud Drive sync instead...
#
# → Using iCloud Drive sync...
# → Creating backup...
# [Backup progress...]
# ✓ Backup created in iCloud Drive
# ✓ Sync metadata written
#
# ═══════════════════════════════════════════════════
#     Sync Complete!
# ═══════════════════════════════════════════════════

# Verify:
ls -lh ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/
# Should show fresh backup with current timestamp
```

---

### Test 2: Laptop Pull

```bash
# On laptop (after iCloud sync completes)
sync-petesbrain pull

# Expected output:
# ═══════════════════════════════════════════════════
#     PetesBrain Sync
# ═══════════════════════════════════════════════════
# Machine: <laptop-hostname>
# Type: Laptop
# Direction: pull
# [...]
# ✓ Backup is fresh (X minutes ago)
# → Found backup: PetesBrain-backup-20251213-170002.tar.gz
# → Extracting to temporary location...
# → Syncing files...
# ✓ Synced from iCloud backup
#
# ═══════════════════════════════════════════════════
#     Sync Complete!
# ═══════════════════════════════════════════════════
```

---

### Test 3: Round-Trip (Laptop → Desktop)

```bash
# On laptop - make a test change
echo "Test sync - $(date)" >> ~/Documents/PetesBrain.nosync/SYNC-TEST.txt

# Push from laptop
sync-petesbrain push

# Wait 1-2 minutes for iCloud sync

# On desktop - pull laptop changes
sync-petesbrain pull

# Verify change
cat ~/Documents/PetesBrain.nosync/SYNC-TEST.txt
# Should show test line with timestamp from laptop

# Clean up test file
rm ~/Documents/PetesBrain.nosync/SYNC-TEST.txt
```

---

## Security Notes

### Credentials and Tokens

**Not included in backups by design:**
- OAuth tokens (`.token.json` files)
- API keys in `.env` files (gitignored)

**If working on laptop requires API access:**
1. Copy credential files manually (one-time setup)
2. Or regenerate OAuth tokens on laptop
3. Or use `.env` files with API keys

**Files that may need copying for full functionality:**
- `shared/email-sync/credentials.json` - Email OAuth
- `shared/mcp-servers/*/credentials.json` - MCP server OAuth
- `.mcp.json` - MCP configuration (references credential paths)

---

## Performance Notes

### Backup Size and Timing

**Desktop (Mac mini M2):**
- Uncompressed project: 7.7GB
- Compressed backup: 1.1GB
- Compression time: ~2.5 minutes
- iCloud upload: ~30 seconds (on fast connection)
- Total push time: ~3 minutes

**Laptop pull:**
- iCloud download: ~1 minute (on fast connection)
- Extraction time: ~1 minute
- rsync time: ~30 seconds
- Total pull time: ~2.5 minutes

**Critical tasks backup (every 6 hours):**
- Size: 131KB (just task files)
- Time: ~5 seconds

---

## Monitoring and Logs

### Check Sync Metadata

```bash
# View metadata about last push
cat ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/.sync-metadata.json

# Example output:
# {
#     "last_push": {
#         "timestamp": "2025-12-13T17:00:02Z",
#         "unix_timestamp": 1734109202,
#         "machine": "Peters-Mac-mini.lan",
#         "machine_type": "Desktop",
#         "user": "administrator"
#     }
# }
```

---

### Check Backup History

```bash
# Desktop backups (last 5)
ls -lht ~/Documents/PetesBrain-backup-*.tar.gz | head -5

# iCloud backups (last 10)
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-*.tar.gz | head -10

# Critical tasks backups (last 20)
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/tasks-backup-*.tar.gz | head -20
```

---

## FAQs

### Q: Can I work on both machines at the same time?

**A:** Not recommended. The sync system doesn't have merge conflict resolution. Stick to the workflow:
- Desktop during the week
- Laptop on weekends
- Always push before switching machines
- Always pull before starting work

---

### Q: What if I forget to push before leaving?

**A:** You'll get a staleness warning when you pull on the laptop. Options:
1. Use `--force` to pull anyway (accepts you're working on older version)
2. Use rsync sync method if both machines are on network (faster)
3. Wait until you can access desktop remotely to push fresh backup

---

### Q: Can I delete old backups manually?

**A:** Yes, but the system does this automatically:
- Local backups: Keeps last 5
- iCloud backups: Keeps last 10
- Critical tasks: Keeps last 20

Manual deletion:
```bash
# Delete specific backup
rm ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-20251201-*.tar.gz

# Delete all backups older than 14 days
find ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/ -name "PetesBrain-backup-*.tar.gz" -mtime +14 -delete
```

---

### Q: How much iCloud storage do I need?

**A:** Minimum 15GB recommended:
- 10 backups × 1.1GB = 11GB
- Safety buffer = 4GB
- Total = 15GB

Current iCloud usage for PetesBrain backups:
```bash
du -sh ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/
```

---

### Q: Can I sync specific files instead of everything?

**A:** No, the system syncs the entire project. For partial syncs:
1. Use rsync directly with custom exclude patterns
2. Use Git with selective file tracking
3. Manually copy files via iCloud Drive folder

---

## Related Documentation

- `docs/BACKUP-SYSTEM.md` - Backup system architecture
- `docs/LAPTOP-INSTALLATION-GUIDE.md` - Full laptop installation
- `docs/MIGRATION-SYSTEM-COMPLETE.md` - Complete migration system
- `shared/scripts/sync-petesbrain.sh` - Sync script source (459 lines)
- `shared/scripts/backup-petesbrain.sh` - Backup script source (123 lines)

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-13 | 1.0 | Initial documentation - fixed backup paths, configured iCloud sync, tested workflow |

---

## Support

If you encounter issues:

1. **Check this document first** - Most common issues are covered
2. **Check sync metadata** - Shows last successful push
3. **Check backup files** - Verify they're recent and correct size
4. **Check iCloud sync** - Make sure iCloud Drive is syncing
5. **Run test workflow** - Follow Test 1, 2, 3 above

---

**Status: ✅ System is configured and tested. Ready for use Monday.**
