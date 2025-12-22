# Holiday Laptop Quick Start Guide

**Created:** December 16, 2025
**Purpose:** Simple guide for setting up PetesBrain on laptop for holiday work
**Status:** ✅ Ready to use

---

## Overview

This guide helps you set up PetesBrain on your laptop for remote work during the holidays (27th December onwards). The system uses iCloud Drive to sync between desktop and laptop.

**Setup time:** 5-10 minutes
**Storage needed:** ~8GB (1.2GB backup + extracted files)

---

## Before You Leave (Desktop)

### Create Fresh Backup

**Run this command on Thursday 26th December before you leave:**

```bash
cd ~/Documents/PetesBrain.nosync
./shared/scripts/sync-petesbrain.sh push
```

**What this does:**
- Creates 1.2GB compressed backup
- Uploads to iCloud Drive
- Writes metadata (timestamp, machine)
- Takes ~3 minutes

**Verify it worked:**
```bash
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/ | head -3
```

You should see a fresh backup from today (1.2GB).

---

## Laptop Setup (Friday 27th December)

### Option 1: Automated Setup (Recommended)

**Single command to set up everything:**

```bash
# Download and run the setup script
curl -o ~/setup-laptop.sh https://raw.githubusercontent.com/PeteEmpy/petesbrain/main/shared/scripts/setup-laptop.sh
chmod +x ~/setup-laptop.sh
~/setup-laptop.sh
```

**Or if you have the backup extracted already:**

```bash
# If you extracted the backup manually, just run the setup script from inside:
cd ~/Documents/PetesBrain.nosync
./shared/scripts/setup-laptop.sh
```

**The script will:**
1. ✅ Check prerequisites (Python 3, iCloud Drive)
2. ✅ Find latest backup in iCloud
3. ✅ Extract to `~/Documents/PetesBrain.nosync`
4. ✅ Configure laptop sync settings
5. ✅ Create shell alias for easy sync
6. ✅ Test the sync workflow

**Total time:** 5 minutes

---

### Option 2: Manual Setup

If you prefer to do it manually:

**Step 1: Check Prerequisites**

```bash
# Check Python 3
python3 --version  # Should show Python 3.x.x

# Check iCloud backups
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/
```

**Step 2: Extract Backup**

```bash
cd ~/Documents
LATEST_BACKUP=$(ls -t ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-*.tar.gz | head -1)
echo "Extracting: $LATEST_BACKUP"
tar -xzf "$LATEST_BACKUP"
mv PetesBrain PetesBrain.nosync
```

**Step 3: Configure Sync**

```bash
cd ~/Documents/PetesBrain.nosync

# Create sync config
cat > .sync-config << 'EOF'
TYPE=Laptop
SYNC_METHOD="icloud"
DESKTOP_HOST="Peters-Mac-mini.lan"
DESKTOP_USER="administrator"
DESKTOP_PATH="/Users/administrator/Documents/PetesBrain.nosync"
EOF

# Make sync script executable
chmod +x shared/scripts/sync-petesbrain.sh

# Create shell alias
echo 'alias sync-petesbrain="~/Documents/PetesBrain.nosync/shared/scripts/sync-petesbrain.sh"' >> ~/.zshrc
source ~/.zshrc
```

**Step 4: Test**

```bash
sync-petesbrain pull
```

**Expected:** "✓ Backup is fresh" + "✓ Synced from iCloud backup"

---

## Daily Workflow on Laptop

### Simple Commands

```bash
# Morning: Get latest changes
sync-petesbrain pull

# Work on PetesBrain normally
# ... make changes, edit files, etc ...

# Evening: Send changes back
sync-petesbrain push
```

### Two-Way Sync

```bash
# Pull then push in one command
sync-petesbrain both
```

---

## How the Sync Works

### Push (Creating a Backup)

When you run `sync-petesbrain push`:

1. Creates compressed backup (~1.2GB)
2. Excludes venv, node_modules (can be rebuilt)
3. Uploads to iCloud Drive
4. Writes metadata (timestamp, machine, user)
5. Cleans up old backups (keeps last 10)

**Takes:** ~3 minutes

### Pull (Getting Latest)

When you run `sync-petesbrain pull`:

1. Checks metadata (backup age)
2. Finds latest backup in iCloud
3. Extracts to temp directory
4. Syncs files to project directory
5. Cleans up temp directory

**Takes:** ~2-3 minutes

---

## What Gets Synced

### ✅ Included

- All client files and data
- Configuration files
- Scripts and tools
- Documentation
- Tasks and completed tasks
- Email archives, meeting notes, reports
- Knowledge base articles

### ❌ Excluded

- `venv/`, `.venv/` (Python virtual environments)
- `node_modules/` (Node.js dependencies)
- `__pycache__/` (Python cache)
- `.git/` (Git metadata - optional)
- `.DS_Store` (macOS files)

**Result:** 7.7GB project → 1.2GB backup

---

## Backup Age Protection

The sync system checks backup age automatically:

| Backup Age | What Happens |
|------------|--------------|
| **< 24 hours** | ✅ Proceeds automatically |
| **24h - 7 days** | ⚠️ Warns, asks confirmation |
| **> 7 days** | 🛑 Blocks, need `--force` |

**Override staleness check:**
```bash
sync-petesbrain pull --force
```

---

## Working Without API Access

**Note:** OAuth tokens and API keys are NOT included in backups.

### View-Only Work (No Setup Needed)

You can do most work without credentials:
- ✅ Edit documentation
- ✅ Review client files
- ✅ Write scripts
- ✅ Plan strategies
- ✅ Draft emails

### Full API Access (Optional)

If you need to run tools that call APIs:

**Option 1: Copy credentials manually** (one-time)
```bash
# On desktop, copy to USB drive or AirDrop:
# - shared/email-sync/credentials.json
# - infrastructure/mcp-servers/*/credentials.json
# - .mcp.json
```

**Option 2: Regenerate on laptop**
```bash
cd ~/Documents/PetesBrain.nosync
./shared/scripts/setup-oauth-once.sh
```

---

## Troubleshooting

### "No backups found in iCloud Drive"

**Solution:**
```bash
# On desktop:
sync-petesbrain push

# Wait 1-2 minutes for iCloud sync
# On laptop:
sync-petesbrain pull
```

### "Backup is stale (>24 hours old)"

**Solution:**
```bash
# Option 1: Create fresh backup on desktop
sync-petesbrain push

# Option 2: Proceed anyway
sync-petesbrain pull --force
```

### "Permission denied" on sync script

**Solution:**
```bash
chmod +x ~/Documents/PetesBrain.nosync/shared/scripts/sync-petesbrain.sh
```

### Changes aren't syncing

**Check workflow:**
```bash
# On laptop after making changes:
sync-petesbrain push

# Wait 1-2 minutes for iCloud upload

# On desktop when you return:
sync-petesbrain pull
```

### iCloud Drive not syncing

**Check:**
1. System Settings → Apple ID → iCloud → iCloud Drive (enabled)
2. Finder sidebar shows "iCloud Drive"
3. Files aren't stuck downloading (cloud icon in Finder)

### Sync is slow

**Possible causes:**
- iCloud still downloading backup (wait for sync)
- Low disk space (need ~3GB free)
- Time Machine running (pause temporarily)

---

## Command Reference

### Essential Commands

```bash
# Pull latest from desktop
sync-petesbrain pull

# Send changes back to desktop
sync-petesbrain push

# Two-way sync
sync-petesbrain both

# Force pull (skip staleness check)
sync-petesbrain pull --force
```

### Checking Status

```bash
# View last push metadata
cat ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/.sync-metadata.json

# List available backups
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/

# Check sync config
cat ~/Documents/PetesBrain.nosync/.sync-config

# Verify alias
which sync-petesbrain
```

---

## Timeline

### Thursday 26th December (Before Holiday)

**Desktop:**
```bash
# Create fresh backup
cd ~/Documents/PetesBrain.nosync
sync-petesbrain push

# Verify
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/ | head -3
```

### Friday 27th December (Holiday Starts)

**Laptop:**
```bash
# Run setup script
~/setup-laptop.sh

# Or manual setup (5 minutes)
# See "Manual Setup" section above
```

### Daily on Holiday

**Morning:**
```bash
sync-petesbrain pull  # Get latest
```

**Evening:**
```bash
sync-petesbrain push  # Save work
```

### When You Return (Desktop)

**Desktop:**
```bash
sync-petesbrain pull  # Get holiday work
```

---

## Pre-Flight Checklist

**Before leaving on Thursday:**

- [ ] Desktop backup created (`sync-petesbrain push`)
- [ ] Backup visible in iCloud Drive (1.2GB)
- [ ] Metadata shows recent timestamp
- [ ] Laptop has iCloud Drive enabled
- [ ] Laptop has ~8GB free space
- [ ] Python 3 installed on laptop
- [ ] Setup script accessible (`setup-laptop.sh`)

---

## File Locations

### Desktop

```
~/Documents/PetesBrain.nosync/              # Main project
  ├── .sync-config                           # TYPE=Desktop
  ├── .is-desktop                            # Desktop marker
  └── shared/scripts/
      ├── sync-petesbrain.sh                # Sync script
      ├── setup-laptop.sh                   # Laptop setup script
      └── backup-petesbrain.sh              # Backup script

~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/
  ├── .sync-metadata.json                   # Last push info
  ├── PetesBrain-backup-20251226-*.tar.gz  # Latest backup (1.2GB)
  └── ...                                    # Keeps last 10
```

### Laptop

```
~/Documents/PetesBrain.nosync/              # Extracted project
  ├── .sync-config                           # TYPE=Laptop
  └── shared/scripts/
      └── sync-petesbrain.sh                # Same sync script

~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/
  ├── .sync-metadata.json                   # Synced from desktop
  ├── PetesBrain-backup-*.tar.gz            # Synced via iCloud
  └── ...
```

---

## Performance Notes

**Desktop (Mac mini M2):**
- Backup creation: ~2-3 minutes
- iCloud upload: ~30 seconds (fast connection)
- Total push time: ~3 minutes

**Laptop:**
- iCloud download: ~1 minute (fast connection)
- Extraction: ~1-2 minutes
- Total pull time: ~2-3 minutes

---

## FAQ

### Q: Can I work on both machines at the same time?

**A:** Not recommended. The system doesn't merge conflicts. Stick to:
- Desktop during the week
- Laptop on holiday
- Always push before switching
- Always pull before starting work

### Q: What if I forget to push before leaving?

**A:** You'll get a staleness warning on laptop. Options:
1. Use `--force` to pull anyway
2. Access desktop remotely to push
3. Work with older version

### Q: How much iCloud storage do I need?

**A:** Minimum 15GB recommended:
- 10 backups × 1.2GB = 12GB
- Safety buffer = 3GB
- Total = 15GB

### Q: Can I delete old backups?

**A:** System does this automatically (keeps last 10). But yes:
```bash
# Delete specific backup
rm ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-YYYYMMDD-*.tar.gz

# Delete all backups older than 14 days
find ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/ -name "PetesBrain-backup-*.tar.gz" -mtime +14 -delete
```

---

## Related Documentation

- **`docs/LAPTOP-SYNC-WEEKEND-WORKFLOW.md`** (898 lines) - Complete sync guide
- **`docs/SYNC-QUICK-START.md`** (123 lines) - Quick reference
- **`docs/BACKUP-SYSTEM.md`** - Backup architecture
- **`shared/scripts/sync-petesbrain.sh`** (459 lines) - Sync script source
- **`shared/scripts/backup-petesbrain.sh`** (123 lines) - Backup script source

---

## Support

**If you encounter issues:**

1. Check this document first
2. Check sync metadata (shows last push)
3. Verify iCloud Drive is syncing
4. Check backup files (should be ~1.2GB)
5. Run test: `sync-petesbrain pull`

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-16 | 1.0 | Initial holiday quick start guide - verified system working, created setup script |

---

**Status: ✅ System tested and ready for holiday use**

**Last verified:** December 16, 2025
**Last backup:** PetesBrain-backup-20251216-094359.tar.gz (1.2GB)
**Metadata timestamp:** 2025-12-16T09:45:08Z
