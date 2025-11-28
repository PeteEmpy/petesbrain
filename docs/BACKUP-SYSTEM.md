# PetesBrain Backup System

**Created:** November 5, 2025
**Updated:** November 18, 2025 (Added dual-layer protection)
**Status:** ✅ Active and Production-Ready

---

## Overview

**Dual-layer automated backup system** protecting against data loss with two complementary approaches:

1. **Critical Tasks Backup** (Fast & Frequent): Tasks data every 6 hours
2. **Full System Backup** (Comprehensive): Complete project daily at 3 AM

Both layers automatically sync to iCloud Drive for off-site protection.

## Why Two Layers?

**November 18, 2025 - Critical Data Loss Incident:**
An accidental deletion of the entire `clients/` directory caused loss of all task data. While CONTEXT.md files were recovered from git, tasks.json files were never committed and were permanently lost.

**The dual-layer system prevents this**:
- **Critical backup**: Fast (37KB), frequent (every 6 hours), captures tasks immediately
- **Full backup**: Comprehensive (~700MB), daily, captures entire project state
- **iCloud sync**: Both layers backed up off-site automatically

## Features

### Critical Tasks Backup (NEW)
- ⚡ **Fast**: 37KB archive (tasks only)
- ⏰ **Frequent**: Every 6 hours + at system login
- 🎯 **Targeted**: Only tasks.json, tasks-completed.md, experiment spreadsheet
- 🧹 **Smart Cleanup**: Keeps last 20 backups (5 days worth)
- 📁 **Location**: `~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/`

### Full System Backup
- 🔄 **Comprehensive**: Complete project archive (~700MB)
- ⏰ **Daily**: Runs automatically every day at 3:00 AM
- 💾 **Dual Storage**: Local SSD + iCloud Drive
- 🧹 **Automatic Cleanup**: Keeps last 5 local, 10 iCloud backups
- 📊 **Complete Logging**: All operations tracked
- 🎨 **Beautiful Output**: Color-coded status messages

---

## Quick Start

### Run Critical Tasks Backup Now

Fast backup of just tasks data:

```bash
/Users/administrator/Documents/PetesBrain/shared/scripts/backup-tasks-critical.sh
```

**Takes ~1 second, creates 37KB backup**

### Run Full System Backup Now

Complete project backup:

```bash
backup-petesbrain
```

Or run the script directly:

```bash
/Users/administrator/Documents/PetesBrain/shared/scripts/backup-petesbrain.sh
```

**Takes ~5-10 minutes, creates ~700MB backup**

---

## Backup Locations

### Critical Tasks Backups (NEW)
**iCloud Location:** `~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/`
**Format:** `tasks-backup-YYYYMMDD-HHMMSS.tar.gz`
**Size:** ~37KB (tasks only)
**Retention:** Last 20 backups (5 days at 6-hour intervals)
**Purpose:** Fast, frequent protection for task data

**Contents:**
- `clients/*/tasks.json` - All client task files
- `clients/*/tasks-completed.md` - Task completion logs
- `roksys/spreadsheets/rok-experiments-client-notes.csv` - Experiment tracking

### Full System Backups

**Local SSD Backups:**
**Location:** `/Users/administrator/Documents/`
**Format:** `PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz`
**Size:** ~700MB (complete project)
**Retention:** Last 5 backups
**Purpose:** Fast local recovery

**iCloud Drive Backups:**
**Location:** `~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/`
**Format:** `PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz`
**Size:** ~700MB (complete project)
**Retention:** Last 10 backups
**Purpose:** Off-site disaster recovery

---

## Automatic Backups

### Critical Tasks Backup Schedule (NEW)
- **When:** Every 6 hours + at system login
- **LaunchAgent:** `com.petesbrain.critical-tasks-backup.plist`
- **Location:** `~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist`
- **Next runs:** Every 6 hours (21600 seconds)

### Full System Backup Schedule
- **When:** Every day at 3:00 AM (changed from weekly Nov 18, 2025)
- **LaunchAgent:** `com.petesbrain.daily-backup.plist` (renamed from weekly-backup)
- **Location:** `~/Library/LaunchAgents/com.petesbrain.daily-backup.plist`

### Logs

**Critical Tasks Backup:**
- **Standard Output:** `~/.petesbrain-tasks-backup.log`
- **Errors:** `~/.petesbrain-tasks-backup-error.log`

**Full System Backup:**
- **Standard Output:** `~/.petesbrain-backup.log`
- **Errors:** `~/.petesbrain-backup-error.log`
- **Backup History:** `shared/data/backup-log.txt`

### Managing the LaunchAgents

**Check Status (both backups):**
```bash
launchctl list | grep petesbrain.backup
```

**Check Critical Tasks Backup:**
```bash
launchctl list | grep petesbrain.critical-tasks-backup
```

**Check Full System Backup:**
```bash
launchctl list | grep petesbrain.daily-backup
```

**Stop/Start Critical Tasks Backup:**
```bash
# Stop
launchctl unload ~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist

# Start
launchctl load ~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist
```

**Stop/Start Full System Backup:**
```bash
# Stop
launchctl unload ~/Library/LaunchAgents/com.petesbrain.daily-backup.plist

# Start
launchctl load ~/Library/LaunchAgents/com.petesbrain.daily-backup.plist
```

**Test Run (without waiting for schedule):**
```bash
# Critical tasks backup (fast)
launchctl start com.petesbrain.critical-tasks-backup

# Full system backup (slow)
launchctl start com.petesbrain.daily-backup
```

---

## Restoring from Backup

### Restore Critical Tasks Only (Fast - Use This First!)

**When to use:** Lost tasks.json files but rest of project intact (like the Nov 18 incident)

1. Navigate to PetesBrain directory:
```bash
cd /Users/administrator/Documents/PetesBrain
```

2. List available critical backups:
```bash
ls -lt ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/
```

3. Extract critical backup (replaces only task files):
```bash
# Choose the most recent backup
tar -xzf ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/tasks-backup-YYYYMMDD-HHMMSS.tar.gz
```

4. Verify restoration:
```bash
# Check a client's tasks file was restored
cat clients/smythson/tasks.json
```

**What gets restored:**
- All `clients/*/tasks.json` files
- All `clients/*/tasks-completed.md` files
- `roksys/spreadsheets/rok-experiments-client-notes.csv`

**What stays unchanged:**
- Everything else in the project

### Full System Restore (Complete Project)

**When to use:** Complete project loss or corruption

1. Navigate to parent directory:
```bash
cd /Users/administrator/Documents
```

2. **IMPORTANT:** Rename or move current project first:
```bash
mv PetesBrain PetesBrain-old-$(date +%Y%m%d)
```

3. Extract backup:
```bash
# From local backup (faster)
tar -xzf PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz

# From iCloud backup (if local not available)
tar -xzf ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz
```

4. Verify restoration:
```bash
cd PetesBrain
ls -la
```

### Selective File Restore

Extract specific files without restoring everything:

**From critical tasks backup:**
```bash
# List what's in the backup
tar -tzf ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/tasks-backup-YYYYMMDD-HHMMSS.tar.gz

# Extract just one client's tasks
tar -xzf ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/tasks-backup-YYYYMMDD-HHMMSS.tar.gz \
  clients/smythson/tasks.json
```

**From full system backup:**
```bash
# List contents of backup
tar -tzf PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz | grep "path/to/file"

# Extract specific file
tar -xzf PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz PetesBrain/path/to/file.txt
```

### Restore from iCloud (Disaster Recovery)

If your local machine fails, restore from iCloud on any Mac:

**For tasks only:**
1. Open iCloud Drive folder: `PetesBrain-Backups/critical-tasks/`
2. Download latest `tasks-backup-*.tar.gz`
3. Follow critical tasks restore steps above

**For full project:**
1. Open iCloud Drive folder: `PetesBrain-Backups/`
2. Download latest `PetesBrain-backup-*.tar.gz`
3. Follow full system restore steps above

---

## Configuration

### Critical Tasks Backup Settings

Edit `shared/scripts/backup-tasks-critical.sh`:

```bash
# Backup interval: Set in LaunchAgent plist (default: 21600 seconds = 6 hours)
# Retention: Number of backups to keep
# Keep last 20 backups (5 days at 6-hour intervals)
ls -1t "$ICLOUD_DIR"/tasks-backup-*.tar.gz 2>/dev/null | tail -n +21 | xargs rm -f
```

**Change backup frequency:**
Edit `~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist`:

```xml
<key>StartInterval</key>
<integer>21600</integer>  <!-- Seconds between backups (21600 = 6 hours) -->
```

After editing, reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist
```

### Full System Backup Settings

Edit `shared/scripts/backup-petesbrain.sh`:

```bash
MAX_LOCAL_BACKUPS=5   # Number of local backups to keep
MAX_ICLOUD_BACKUPS=10 # Number of iCloud backups to keep
```

**Change backup time:**
Edit `~/Library/LaunchAgents/com.petesbrain.daily-backup.plist`:

```xml
<key>StartCalendarInterval</key>
<dict>
    <!-- Removed Weekday - runs daily -->
    <key>Hour</key>
    <integer>3</integer>       <!-- 24-hour format (3 = 3 AM) -->
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

After editing, reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.daily-backup.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.daily-backup.plist
```

---

## Backup Contents

### Critical Tasks Backup (37KB)

**What's Included:**
- ✅ `clients/*/tasks.json` - All client task files
- ✅ `clients/*/tasks-completed.md` - Task completion logs
- ✅ `roksys/spreadsheets/rok-experiments-client-notes.csv` - Experiment tracking

**What's Excluded:**
- Everything else (this is intentional - speed over completeness)

**Why these files?**
These three items are the most critical and frequently changed data that isn't in git. Tasks drive daily work, task completion logs provide audit trail, and experiment notes explain performance changes.

### Full System Backup (~700MB)

**What's Included:**
- ✅ All client folders and data
- ✅ All tools and scripts
- ✅ Configuration files
- ✅ Documentation
- ✅ Credentials (encrypted)
- ✅ MCP servers
- ✅ Knowledge base
- ✅ Agents and automation
- ✅ Data files and exports

**What's Excluded:**
- ❌ `venv/` folder (Python virtual environment - can be recreated)
- ❌ `__pycache__/` folders (Python cache - regenerated automatically)
- ❌ `.git/` folder (if present - version control)
- ❌ Any files in `.gitignore`

> **Note:** To exclude additional folders, modify the tar command in `backup-petesbrain.sh`

---

## Troubleshooting

### Critical Tasks Backup - Permission Denied (KNOWN ISSUE)

**Symptom:** Error log shows `/bin/bash: Operation not permitted`

**Root cause:** LaunchAgent doesn't have Full Disk Access to read PetesBrain directory

**Status:** Script works when run manually, but LaunchAgent needs system permissions

**Solution:**
1. Open **System Settings** → **Privacy & Security** → **Full Disk Access**
2. Click the **+** button
3. Navigate to `/bin/bash` and add it
4. Or add `/Users/administrator/Documents/PetesBrain/shared/scripts/backup-tasks-critical.sh`
5. Reload LaunchAgent:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist
```

**Workaround:** Run manually as needed:
```bash
/Users/administrator/Documents/PetesBrain/shared/scripts/backup-tasks-critical.sh
```

### Backup Failed - Disk Space

**Symptom:** Error creating backup archive

**Solution:**
1. Check available space: `df -h`
2. Clean up old backups manually:

**Critical tasks backups:**
```bash
ls -lt ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/
rm ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/tasks-backup-YYYYMMDD-HHMMSS.tar.gz
```

**Full system backups:**
```bash
ls -lt /Users/administrator/Documents/PetesBrain-backup-*.tar.gz
rm /Users/administrator/Documents/PetesBrain-backup-YYYYMMDD-HHMMSS.tar.gz
```

### iCloud Backup Failed

**Symptom:** Local backup succeeds but iCloud copy fails

**Possible causes:**
1. iCloud Drive not enabled
2. No internet connection
3. iCloud storage full

**Solution:**
1. Check iCloud status: System Settings → Apple ID → iCloud
2. Ensure iCloud Drive is enabled
3. Check storage: System Settings → Apple ID → iCloud → Manage Storage
4. Free up space or upgrade iCloud storage plan

### Can't Find Backup

**Critical tasks backups:**
```bash
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/
```

**Full system backups (local):**
```bash
ls -lht /Users/administrator/Documents/PetesBrain-backup-*.tar.gz
```

**Full system backups (iCloud):**
```bash
ls -lht ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/
```

### LaunchAgent Not Running

**Check if loaded:**
```bash
# Both backups
launchctl list | grep petesbrain.backup

# Critical tasks only
launchctl list | grep critical-tasks-backup

# Full system only
launchctl list | grep daily-backup
```

**Check logs:**
```bash
# Critical tasks backup
cat ~/.petesbrain-tasks-backup-error.log

# Full system backup
cat ~/.petesbrain-backup-error.log
```

**Reload agent:**
```bash
# Critical tasks backup
launchctl unload ~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist

# Full system backup
launchctl unload ~/Library/LaunchAgents/com.petesbrain.daily-backup.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.daily-backup.plist
```

### Backup Taking Too Long

**Critical tasks backup:**
- Should complete in ~1 second
- If taking longer, check iCloud Drive sync status

**Full system backup:**
- Normal: 5-10 minutes for ~700MB archive
- If longer than 15 minutes, may be iCloud sync delay
- Check: Activity Monitor → Network tab for iCloud upload

---

## Best Practices

1. **Dual-Layer Protection**
   - Critical tasks: Backed up automatically every 6 hours to iCloud
   - Full project: Backed up daily at 3 AM to local SSD + iCloud
   - Both layers provide redundancy and recovery options

2. **Test Restore Periodically**
   Every few months, verify you can successfully restore from both backup types:
   - Critical tasks: Extract a tasks.json file to verify
   - Full system: Verify backup archive integrity with `tar -tzf [backup].tar.gz`

3. **Monitor Backup Logs**
   Check logs weekly to ensure backups are running successfully:
   ```bash
   # Critical tasks backup
   cat ~/.petesbrain-tasks-backup.log | tail -20

   # Full system backup
   cat ~/.petesbrain-backup.log | tail -20
   ```

4. **Keep iCloud Storage Clear**
   - Critical backups: ~740KB for 20 backups (negligible)
   - Full backups: ~7GB for 10 backups (monitor this)
   - Total: ~7.7GB required for both layers

5. **Before Major Changes**
   Run critical backup before risky operations:
   ```bash
   /Users/administrator/Documents/PetesBrain/shared/scripts/backup-tasks-critical.sh
   ```

6. **Document Custom Changes**
   If you modify backup scripts, document changes in this file's Version History

7. **Verify iCloud Sync**
   Occasionally check that backups are syncing to iCloud:
   ```bash
   ls -lh ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/
   ```

8. **Git Commit Important Files**
   While tasks.json files are backed up, CONTEXT.md files should also be in git for version control

---

## Files Reference

### Scripts

**Critical Tasks Backup:**
- `shared/scripts/backup-tasks-critical.sh` - Fast tasks-only backup script

**Full System Backup:**
- `shared/scripts/backup-petesbrain.sh` - Comprehensive project backup script

### LaunchAgents

**Critical Tasks Backup:**
- `~/Library/LaunchAgents/com.petesbrain.critical-tasks-backup.plist` - Every 6 hours automation

**Full System Backup:**
- `~/Library/LaunchAgents/com.petesbrain.daily-backup.plist` - Daily 3 AM automation

### Logs

**Critical Tasks Backup:**
- `~/.petesbrain-tasks-backup.log` - Standard output log
- `~/.petesbrain-tasks-backup-error.log` - Error log

**Full System Backup:**
- `~/.petesbrain-backup.log` - Standard output log
- `~/.petesbrain-backup-error.log` - Error log
- `shared/data/backup-log.txt` - Backup history

### Aliases
- `~/.zshrc` - Contains `backup-petesbrain` command alias (full system backup)

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-05 | 1.0 | Initial backup system created with dual storage (local + iCloud), weekly automation, on-demand backups |
| 2025-11-18 | 2.0 | **Major upgrade: Dual-layer backup system** implemented in response to critical data loss incident. Added critical tasks backup (every 6 hours, 37KB), changed full backup from weekly to daily, both sync to iCloud. LaunchAgent Full Disk Access permission issue documented. |

## Incident History

**November 18, 2025 - Critical Data Loss:**
Accidental deletion of entire `clients/` directory caused loss of all tasks.json files (not in git). CONTEXT.md files recovered from git, but task data permanently lost. Recovery successful via Google Tasks MCP import, but highlighted need for more frequent task backups.

**Response:**
1. Implemented critical tasks backup (every 6 hours)
2. Changed full backup from weekly to daily
3. Both layers now sync to iCloud automatically
4. Dual-layer system ensures task data never more than 6 hours old

---

## Related Documentation

- [System Health Monitoring](SYSTEM-HEALTH-MONITORING.md)
- [Automation Overview](AUTOMATION.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

