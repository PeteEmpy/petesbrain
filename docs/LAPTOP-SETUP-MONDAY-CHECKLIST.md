# Laptop Setup - Monday Checklist

**Purpose:** Get PetesBrain working on your laptop in 5 simple steps
**Time needed:** ~10 minutes
**When:** Monday morning before you need to work remotely

---

## Prerequisites

✅ Your laptop is turned on
✅ iCloud Drive is enabled and syncing
✅ You can see the backup file in iCloud Drive

**Check iCloud backup is synced:**
```bash
ls -lh ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/
```

You should see: `PetesBrain-backup-20251214-171244.tar.gz` (1.1GB)

If you don't see it, wait a few minutes for iCloud to finish syncing.

---

## Step 1: Extract Project from iCloud

**Copy and paste these commands:**

```bash
# Go to Documents folder
cd ~/Documents

# Find the latest backup
LATEST_BACKUP=$(ls -t ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-*.tar.gz | head -1)

# Show which backup we're using
echo "Using backup: $LATEST_BACKUP"

# Extract it (takes ~2 minutes)
tar -xzf "$LATEST_BACKUP"

# Check it worked
ls -la ~/Documents/PetesBrain/
```

**Expected result:** You should see a `PetesBrain` folder with lots of files inside.

---

## Step 2: Create Laptop Config File

**Copy and paste these commands:**

```bash
# Go into the project
cd ~/Documents/PetesBrain

# Create the config file
cat > .sync-config << 'EOF'
# PetesBrain Sync Configuration
TYPE=Laptop
SYNC_METHOD="icloud"

# Desktop info (leave as-is)
DESKTOP_HOST="Peters-Mac-mini.lan"
DESKTOP_USER="administrator"
DESKTOP_PATH="/Users/administrator/Documents/PetesBrain.nosync"
EOF

# Verify it was created
cat .sync-config
```

**Expected result:** You should see the config file contents displayed.

---

## Step 3: Make Sync Script Executable

**Copy and paste this command:**

```bash
chmod +x ~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh
```

**Expected result:** No output = success.

---

## Step 4: Create Shortcut Command

**Copy and paste these commands:**

```bash
# Add alias to your shell
echo 'alias sync-petesbrain="~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh"' >> ~/.zshrc

# Activate it
source ~/.zshrc

# Test it
which sync-petesbrain
```

**Expected result:** Should show the path to the script.

---

## Step 5: Test the Sync

**Copy and paste this command:**

```bash
sync-petesbrain pull
```

**Expected result:** You should see:

```
═══════════════════════════════════════════════════
    PetesBrain Sync
═══════════════════════════════════════════════════

Machine: <your-laptop-name>
Type: Laptop
Direction: pull
Project: /Users/<you>/Documents/PetesBrain

───────────────────────────────────────────────────
    Last Push Information
───────────────────────────────────────────────────
  When:    2025-12-14T17:13:51Z (X hours ago)
  From:    Peters-Mac-mini.lan (Desktop)
  User:    administrator
───────────────────────────────────────────────────

✓ Backup is fresh (X hours ago)
→ Found backup: PetesBrain-backup-20251214-171244.tar.gz
→ Extracting to temporary location...
→ Syncing files...
✓ Synced from iCloud backup

═══════════════════════════════════════════════════
    Sync Complete!
═══════════════════════════════════════════════════
```

---

## ✅ You're Done!

**PetesBrain is now on your laptop and ready to use.**

---

## How to Use It

### Get Latest from Desktop (Before You Start Work)

```bash
sync-petesbrain pull
```

### Send Your Changes Back (When You're Done)

```bash
sync-petesbrain push
```

---

## Troubleshooting

### "No such file or directory" on Step 1

**Problem:** Backup file not found in iCloud

**Fix:**
1. Check if iCloud Drive is syncing (look in Finder sidebar)
2. Wait 5 minutes for sync to complete
3. Try Step 1 again

---

### "Backup is stale (>24 hours)"

**Problem:** Backup is old

**Fix:** Use force flag:
```bash
sync-petesbrain pull --force
```

---

### "Permission denied" on Step 3

**Problem:** Can't make script executable

**Fix:** Add sudo:
```bash
sudo chmod +x ~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh
```

---

### Command not found: sync-petesbrain

**Problem:** Alias not working

**Fix:** Use full path instead:
```bash
~/Documents/PetesBrain/shared/scripts/sync-petesbrain.sh pull
```

---

## What You DON'T Need to Do

❌ Install MCP servers
❌ Set up LaunchAgents
❌ Create virtual environments
❌ Install Python packages
❌ Configure credentials

**The sync script handles everything automatically!**

---

## Need More Help?

See full documentation: `docs/LAPTOP-SYNC-WEEKEND-WORKFLOW.md`

---

**Total time:** ~10 minutes
**Complexity:** Copy/paste 5 commands
**Result:** PetesBrain working on laptop ✅
