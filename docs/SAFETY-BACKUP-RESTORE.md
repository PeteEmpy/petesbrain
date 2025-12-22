# Safety Backup & Restore Guide

**Created:** December 16, 2025
**Purpose:** How to restore desktop from safety backups after laptop push issues

---

## Overview

The laptop sync system automatically creates a **safety backup** on the desktop before every laptop push. This protects against accidental overwrites or corrupted files.

**Backup Details:**
- **Location:** `~/Documents/PetesBrain-Safety-Backups/`
- **Naming:** `safety-backup-YYYYMMDD-HHMMSS.tar.gz`
- **Size:** ~430MB compressed (from 8.7GB project)
- **Retention:** Keeps last 3 backups automatically
- **Creation:** Takes 2-3 minutes before each push

---

## When to Restore

Restore from safety backup if:
- ✅ Laptop push corrupted files on desktop
- ✅ Wrong files pushed from laptop
- ✅ Desktop files accidentally overwritten
- ✅ Need to rollback to pre-push state

**Do NOT restore if:**
- ❌ Just making small edits (use Git instead)
- ❌ Backup is very old (check timestamp)

---

## How Safety Backups Work

### **Automatic Creation**

When you run `sync-petesbrain push` **from laptop**:

1. Laptop SSHs into desktop
2. Desktop runs `create-safety-backup.sh`
3. Creates compressed backup (2-3 minutes)
4. Confirms backup successful
5. Laptop proceeds with rsync push
6. Keeps last 3 safety backups

**If backup fails:**
- You're asked "Continue anyway? (y/n)"
- Say 'n' to abort push
- Say 'y' to push without backup (risky!)

---

## Restore Procedure

### **Step 1: Identify Which Backup**

```bash
# On desktop - list available safety backups
ls -lht ~/Documents/PetesBrain-Safety-Backups/

# Example output:
# safety-backup-20251226-140530.tar.gz  432M  Dec 26 14:05  (most recent)
# safety-backup-20251225-183015.tar.gz  431M  Dec 25 18:30
# safety-backup-20251224-091245.tar.gz  430M  Dec 24 09:12
```

**Choose the backup from BEFORE the problematic push.**

---

### **Step 2: Backup Current State (Just in Case)**

```bash
# On desktop - backup current state before restoring
cd ~/Documents
tar -czf PetesBrain-before-restore-$(date +%Y%m%d-%H%M%S).tar.gz PetesBrain.nosync/
```

This gives you a way to undo the restore if needed.

---

### **Step 3: Restore from Safety Backup**

```bash
# On desktop

# Move current project out of the way
cd ~/Documents
mv PetesBrain.nosync PetesBrain.nosync-OLD

# Extract safety backup
tar -xzf ~/Documents/PetesBrain-Safety-Backups/safety-backup-YYYYMMDD-HHMMSS.tar.gz

# Verify extraction
ls -lh PetesBrain.nosync/
```

**Replace `YYYYMMDD-HHMMSS` with the actual backup timestamp.**

---

### **Step 4: Verify Restoration**

```bash
# On desktop - check critical files
ls -lh ~/Documents/PetesBrain.nosync/clients/*/tasks.json

# Check project size
du -sh ~/Documents/PetesBrain.nosync/

# Check recent file timestamps
ls -lt ~/Documents/PetesBrain.nosync/ | head -10
```

**Expected:**
- Project should be ~8.7GB
- Files should have timestamps from before the push
- All client folders present

---

### **Step 5: Clean Up**

```bash
# On desktop - once verified working

# Remove old broken version
rm -rf ~/Documents/PetesBrain.nosync-OLD

# Remove temporary restore backup (if don't need)
rm ~/Documents/PetesBrain-before-restore-*.tar.gz
```

---

## Quick Restore (One Command)

If you're confident and just want to restore immediately:

```bash
# On desktop
cd ~/Documents && \
  mv PetesBrain.nosync PetesBrain.nosync-BROKEN && \
  tar -xzf ~/Documents/PetesBrain-Safety-Backups/safety-backup-YYYYMMDD-HHMMSS.tar.gz && \
  echo "✓ Restored from safety backup"
```

**Replace `YYYYMMDD-HHMMSS` with actual timestamp.**

---

## Checking Backup Contents (Without Restoring)

Want to peek inside a backup first?

```bash
# List files in backup
tar -tzf ~/Documents/PetesBrain-Safety-Backups/safety-backup-YYYYMMDD-HHMMSS.tar.gz | head -50

# Extract single file to check
tar -xzf ~/Documents/PetesBrain-Safety-Backups/safety-backup-YYYYMMDD-HHMMSS.tar.gz \
  PetesBrain.nosync/clients/smythson/tasks.json

# Check the file
cat PetesBrain.nosync/clients/smythson/tasks.json

# Clean up test extraction
rm -rf PetesBrain.nosync/
```

---

## Manual Backup Creation

Want to create a safety backup manually (before risky operation)?

```bash
# On desktop
cd ~/Documents/PetesBrain.nosync
./shared/scripts/create-safety-backup.sh
```

---

## Backup Management

### **Check Backup Space Usage**

```bash
du -sh ~/Documents/PetesBrain-Safety-Backups/
```

**Typical:** 430MB per backup × 3 = ~1.3GB

---

### **Increase Retention (Keep More Backups)**

Edit `shared/scripts/create-safety-backup.sh`:

```bash
# Change line:
ls -t safety-backup-*.tar.gz 2>/dev/null | tail -n +4 | xargs rm -f

# To keep 5 backups instead:
ls -t safety-backup-*.tar.gz 2>/dev/null | tail -n +6 | xargs rm -f

# To keep 10 backups:
ls -t safety-backup-*.tar.gz 2>/dev/null | tail -n +11 | xargs rm -f
```

---

### **Delete Old Backups Manually**

```bash
# On desktop - delete specific backup
rm ~/Documents/PetesBrain-Safety-Backups/safety-backup-20251201-120000.tar.gz

# Delete all backups older than 7 days
find ~/Documents/PetesBrain-Safety-Backups/ -name "safety-backup-*.tar.gz" -mtime +7 -delete

# Delete all but most recent backup
cd ~/Documents/PetesBrain-Safety-Backups/
ls -t safety-backup-*.tar.gz | tail -n +2 | xargs rm -f
```

---

## Troubleshooting

### **"Safety backup failed" on Push**

**Possible causes:**
1. Not enough disk space (~1GB needed)
2. Permissions issue on backup directory
3. Desktop offline or SSH failed

**Solutions:**
```bash
# Check disk space
df -h ~

# Check backup directory exists
ls -ld ~/Documents/PetesBrain-Safety-Backups/

# Create directory if missing
mkdir -p ~/Documents/PetesBrain-Safety-Backups/

# Test backup script manually
cd ~/Documents/PetesBrain.nosync
./shared/scripts/create-safety-backup.sh
```

---

### **Backup is Huge (>1GB)**

This might indicate venv or node_modules weren't excluded.

**Check what's in backup:**
```bash
tar -tzf ~/Documents/PetesBrain-Safety-Backups/safety-backup-LATEST.tar.gz | grep -E "venv|node_modules" | head -20
```

If you see venv or node_modules, the excludes aren't working.

---

### **Can't Find Backup File**

```bash
# Search for all safety backups
find ~/Documents -name "safety-backup-*.tar.gz" -type f

# Check different locations
ls -lh ~/Documents/PetesBrain-Safety-Backups/
ls -lh ~/Documents/*.tar.gz
```

---

### **Restore Broke Something**

If restore made things worse:

```bash
# Use the "before-restore" backup you made in Step 2
cd ~/Documents
rm -rf PetesBrain.nosync
tar -xzf PetesBrain-before-restore-YYYYMMDD-HHMMSS.tar.gz
```

---

## Testing the System

Want to test restore without breaking anything?

```bash
# On desktop - test restore to different location
cd ~/tmp
tar -xzf ~/Documents/PetesBrain-Safety-Backups/safety-backup-LATEST.tar.gz
du -sh PetesBrain.nosync/
ls -lh PetesBrain.nosync/clients/
rm -rf PetesBrain.nosync/

echo "✓ Backup is valid and can be restored"
```

---

## Timeline Example

**Thursday before holiday:**
```
14:00 - Laptop: sync-petesbrain pull (gets latest)
14:01 - Leave for holiday with laptop
```

**Sunday during holiday:**
```
10:00 - Laptop: Edit files, make changes
18:00 - Laptop: sync-petesbrain push
        → Desktop: Creates safety-backup-20251229-180015.tar.gz (430MB)
        → Desktop: Receives laptop changes via rsync
        → Desktop: Safety backup kept at ~/Documents/PetesBrain-Safety-Backups/
```

**Monday back at desk:**
```
09:00 - Check desktop: Files look wrong!
09:01 - Desktop: Restore from safety-backup-20251229-180015.tar.gz
09:05 - Desktop: Back to pre-push state ✓
09:10 - Investigate what went wrong on laptop
```

---

## Summary

✅ **Safety backups are automatic** - Created before every laptop push
✅ **Quick to restore** - 1-2 minutes extraction time
✅ **Small storage footprint** - 430MB per backup, keeps 3
✅ **No maintenance needed** - Old backups cleaned automatically
✅ **Easy to manage** - Simple tar.gz files, standard tools

**Remember:** Safety backups protect the **desktop** from bad **laptop pushes**. They don't protect laptop or provide version history (use Git for that).

---

## Related Documentation

- **Laptop Sync Guide:** `docs/LAPTOP-SYNC-RSYNC-SETUP.md`
- **Weekend Workflow:** `docs/LAPTOP-SYNC-WEEKEND-WORKFLOW.md`
- **Backup Script:** `shared/scripts/create-safety-backup.sh`
- **Sync Script:** `shared/scripts/sync-petesbrain.sh`

---

**Last Updated:** December 16, 2025
**Status:** ✅ Tested and working
