# Tasks Backup System

**Created:** 2025-11-19  
**Purpose:** Prevent catastrophic data loss from accidental task deletions  
**Status:** ✅ Active and operational

---

## Overview

After the incident where tasks were accidentally deleted, this system provides comprehensive backup and recovery capabilities for all task data across PetesBrain.

**Key Features:**
- ✅ Automated backups every 3 hours
- ✅ 30 days of backup history (240 backups)
- ✅ Cloud storage (Google Drive) + local fallback
- ✅ Manual backup on-demand
- ✅ Safe restoration with multiple confirmations
- ✅ Point-in-time recovery to any backup

---

## Architecture

### 1. Automated Agent

**Location:** `agents/tasks-backup/`

**Schedule:** Every 3 hours (10,800 seconds)

**What It Backs Up:**
- All `clients/*/tasks.json` files (internal tasks)
- `roksys/tasks.json`
- `data/state/tasks-state.json`
- `data/state/tasks-completed.json`
- `data/state/client-tasks.json`
- **Google Tasks** (all task lists exported to JSON) - NEW in Nov 2025

**Storage:**
- **Primary:** ✅ Google Drive `PetesBrain-Backups/Tasks/` (cloud) - ACTIVE
- **Fallback:** `_backups/tasks/` (local) - always saved
- **Format:** `tasks-backup-YYYY-MM-DD-HHMM.tar.gz`
- **Retention:** 30 days (automatically cleaned up locally)

**Logs:**
- `~/.petesbrain-tasks-backup.log` (stdout)
- `~/.petesbrain-tasks-backup-error.log` (stderr)

---

### 2. Manual Backup Skill

**Location:** `.claude/skills/backup-tasks/`

**Trigger:** User says "backup tasks" or "backup my tasks"

**Use Cases:**
- Before major task restructuring
- Before running restore (safety backup)
- Before deleting multiple tasks
- Before testing new task features
- Any time user wants a backup

**How It Works:**
1. User requests backup
2. Claude confirms and runs backup script
3. Reports results (files, size, location)
4. Shows list of recent backups

**No confirmation needed** - it's a safe operation that only creates data.

---

### 3. Restore Skill

**Location:** `.claude/skills/restore-tasks/`

**Trigger:** User says "restore tasks" or "restore my tasks from backup"

**Safety Features:**
✅ Initial warning about destructive operation
✅ Automatic safety backup before restore
✅ Preview of backup contents
✅ Multiple confirmation steps
✅ Requires typing "RESTORE" exactly (case-sensitive)
✅ Post-restore verification
✅ Rollback instructions provided

**Process Flow:**
1. **Warning:** Explain this will overwrite current tasks
2. **Safety Backup:** Create backup of current state
3. **List Backups:** Show all available backups with details
4. **User Selection:** User picks backup number
5. **Preview:** Show what's in selected backup
6. **Confirmation:** User must type "RESTORE" exactly
7. **Execute:** Restore backup files
8. **Verify:** Confirm restoration successful
9. **Report:** Provide rollback instructions

**Safeguards:**
- Never skips safety backup
- Requires exact "RESTORE" confirmation
- Clear warnings at every step
- Restoration is always reversible
- User always knows what's happening

---

## Usage

### Automated Backups (No Action Required)

Backups run automatically every 3 hours. Check status:

```bash
# View recent backup log
tail -50 ~/.petesbrain-tasks-backup.log

# List recent backups
ls -lht /Users/administrator/Documents/PetesBrain/_backups/tasks/ | head -10

# Check agent status
launchctl list | grep tasks-backup
```

---

### Manual Backup

Just say to Claude:

```
backup tasks
```

or

```
backup my tasks
```

Claude will:
1. Run the backup script
2. Show results (files backed up, size, location)
3. List recent backups

---

### Restore from Backup

Say to Claude:

```
restore tasks
```

or

```
restore my tasks from backup
```

**Claude will guide you through:**
1. Creating a safety backup (automatic)
2. Selecting which backup to restore
3. Previewing backup contents
4. Multiple confirmations
5. Executing restore
6. Verifying results

**IMPORTANT:** You must type "RESTORE" exactly to proceed.

---

## What Gets Backed Up

### Internal Task Files (19 files as of Nov 2025)

```
clients/*/tasks.json (16 client task files)
data/state/tasks-state.json
data/state/tasks-completed.json
data/state/client-tasks.json
```

### Google Tasks Export (NEW - Nov 2025)

```
google-tasks/peter's-list.json
google-tasks/client-work.json
```

**Archive Structure:**
```
tasks-backup-YYYY-MM-DD-HHMM.tar.gz
├── clients/*/tasks.json (internal tasks)
├── data/state/*.json (state files)
└── google-tasks/*.json (Google Tasks exports)
```

**Typical Backup Size:** ~60 KB (compressed, includes Google Tasks)

---

## Backup Schedule

| Time  | Backup | Age When Next Runs |
|-------|--------|-------------------|
| 00:00 | Backup 1 | 3 hours old |
| 03:00 | Backup 2 | 3 hours old |
| 06:00 | Backup 3 | 3 hours old |
| 09:00 | Backup 4 | 3 hours old |
| 12:00 | Backup 5 | 3 hours old |
| 15:00 | Backup 6 | 3 hours old |
| 18:00 | Backup 7 | 3 hours old |
| 21:00 | Backup 8 | 3 hours old |

**8 backups per day × 30 days = 240 backups maximum**

After 30 days, oldest backups are automatically deleted.

---

## Installation & Setup

### 1. Install Agent (Already Done)

Agent is already installed and configured:

```bash
# Verify agent files exist
ls -la /Users/administrator/Documents/PetesBrain/agents/tasks-backup/

# Verify LaunchAgent plist
ls -la /Users/administrator/Documents/PetesBrain/agents/launchagents/com.petesbrain.tasks-backup.plist
```

### 2. Load Agent

To start the automated backups:

```bash
# Copy plist to LaunchAgents directory
cp /Users/administrator/Documents/PetesBrain/agents/launchagents/com.petesbrain.tasks-backup.plist ~/Library/LaunchAgents/

# Load the agent
launchctl load ~/Library/LaunchAgents/com.petesbrain.tasks-backup.plist
```

### 3. Verify Agent Running

```bash
# Check if agent is loaded
launchctl list | grep tasks-backup

# Check log for successful backup
tail -20 ~/.petesbrain-tasks-backup.log
```

You should see output like:
```
============================================================
Tasks Backup Agent
Started: 2025-11-19 14:51:09
============================================================
📥 Exporting Google Tasks...
   ✅ Peter's List: 20 tasks
   ✅ Client Work: 20 tasks
✅ Exported 2 Google Tasks lists (40 total tasks)
✅ Created backup archive: tasks-backup-2025-11-19-1451.tar.gz
   Local task files: 19
   Google Tasks exports: 2
   Total files: 21
   Archive size: 61.9 KB
📤 Uploading to Google Drive: tasks-backup-2025-11-19-1451.tar.gz
   Size: 61.9 KB
✅ Uploaded to Google Drive successfully
   File ID: 1MtGHgY1rtVOhZw7fkRXPpRwvIqOyb5Pu
   Location: PetesBrain-Backups/Tasks/tasks-backup-2025-11-19-1451.tar.gz
✅ Local backup saved: /Users/administrator/Documents/PetesBrain/_backups/tasks/tasks-backup-2025-11-19-1451.tar.gz
...
```

---

## Troubleshooting

### Agent Not Running

```bash
# Unload and reload
launchctl unload ~/Library/LaunchAgents/com.petesbrain.tasks-backup.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.tasks-backup.plist

# Check for errors
cat ~/.petesbrain-tasks-backup-error.log
```

### No Backups Created

```bash
# Run manually to see errors
python3 /Users/administrator/Documents/PetesBrain/agents/tasks-backup/tasks-backup.py

# Check permissions
ls -la /Users/administrator/Documents/PetesBrain/_backups/
```

### Restore Failed

If restore fails:
1. Check the safety backup was created (it's created automatically)
2. Run manual backup first
3. Try restore again
4. Contact for help with backup file path

### Backup Directory Missing

```bash
# Create backup directory
mkdir -p /Users/administrator/Documents/PetesBrain/_backups/tasks
```

---

## Recovery Scenarios

### Scenario 1: Accidentally Deleted Tasks (Today)

**Solution:** Restore from most recent backup (max 3 hours old)

```
Say to Claude: "restore tasks"
Select: Backup #1 (most recent)
```

---

### Scenario 2: Need Tasks from Yesterday

**Solution:** Restore from backup ~24 hours ago

```
Say to Claude: "restore tasks"
Select: Backup from yesterday (check timestamps)
```

---

### Scenario 3: Need Tasks from Last Week

**Solution:** Restore from backup 7 days ago

```
Say to Claude: "restore tasks"
Select: Backup from 7 days ago (within 30-day window)
```

---

### Scenario 4: Restore Went Wrong

**Solution:** Immediately restore from the safety backup

The safety backup is created BEFORE every restore, so you can always undo:

```
Say to Claude: "restore tasks"
Select: The safety backup (most recent, created just before restore)
Type: RESTORE
```

---

## File Structure

```
PetesBrain/
├── agents/
│   ├── tasks-backup/
│   │   ├── agent.md
│   │   ├── tasks-backup.py
│   │   └── config.plist
│   └── launchagents/
│       └── com.petesbrain.tasks-backup.plist
│
├── .claude/skills/
│   ├── backup-tasks/
│   │   └── skill.md
│   └── restore-tasks/
│       └── skill.md
│
├── _backups/
│   └── tasks/
│       ├── tasks-backup-2025-11-19-1155.tar.gz
│       ├── tasks-backup-2025-11-19-0855.tar.gz
│       └── ... (up to 240 backups)
│
└── docs/
    └── TASKS-BACKUP-SYSTEM.md (this file)
```

---

## Monitoring & Maintenance

### Daily Checks (Optional)

```bash
# Check last backup time
ls -lt /Users/administrator/Documents/PetesBrain/_backups/tasks/ | head -3

# Check backup count (should be 80 after 10 days)
ls /Users/administrator/Documents/PetesBrain/_backups/tasks/ | wc -l

# Check log for errors
grep "❌" ~/.petesbrain-tasks-backup.log
```

### Weekly Checks (Recommended)

```bash
# Verify agent still running
launchctl list | grep tasks-backup

# Check backup directory size
du -sh /Users/administrator/Documents/PetesBrain/_backups/tasks/

# Test manual backup
Say to Claude: "backup tasks"
```

### Monthly Checks

```bash
# Verify 30-day retention working
# Should see ~240 backups (8/day × 30 days)
ls -l /Users/administrator/Documents/PetesBrain/_backups/tasks/ | wc -l

# Test restore (with immediate rollback)
Say to Claude: "restore tasks"
Select recent backup
Verify preview looks correct
Type: RESTORE
Then immediately: "restore tasks" again and select safety backup to rollback
```

---

## Future Enhancements

### Phase 1 (Current - COMPLETE)
✅ Automated local backups every 3 hours
✅ Manual backup skill
✅ Safe restore skill with safeguards
✅ 30-day retention
✅ Local fallback storage
✅ **Google Drive cloud upload** (ACTIVE)

### Phase 2 (Nov 2025 - COMPLETE)
✅ **Google Tasks export** - Includes all Google Tasks in backups
✅ **Unified Task Manager** - Shows both internal tasks and Google Tasks
✅ **Task completion script** - Automatic routing between systems
✅ **Enhanced reporting** - Breakdown of internal vs Google Tasks

### Phase 3 (Planned)
⏳ Backup integrity verification
⏳ Email alerts on backup failure
⏳ Backup size trending
⏳ Google Drive cleanup (remove old backups from cloud)

### Phase 4 (Future)
💡 Incremental backups (save space)
💡 Cross-region cloud redundancy
💡 Web interface for browse/restore
💡 Automated restore testing

---

## Key Principles

1. **Automated & Reliable:** Backups run automatically, no manual intervention
2. **Cloud + Local:** Redundancy at two levels
3. **Safe Recovery:** Multiple safeguards prevent accidental restore
4. **Point-in-Time:** Can recover to any 3-hour window in last 30 days
5. **Transparent:** User always knows what's happening
6. **Reversible:** Every restore creates safety backup first
7. **Low Overhead:** Compressed archives, minimal storage (~12 MB for 240 backups)

---

## Support

**Questions?**
- Check logs: `tail -50 ~/.petesbrain-tasks-backup.log`
- Test backup: Say to Claude "backup tasks"
- View backups: `ls -lht _backups/tasks/ | head -10`
- Ask Claude: "How do I restore tasks from backup?"

**Issues?**
- Agent not running: Check launchctl status
- No backups: Run script manually to see errors
- Restore failed: Safety backup always available
- Need help: Full documentation in this file

---

---

## Complete Task Management Workflow (Nov 2025)

### The Dual-System Architecture

**PetesBrain uses TWO task systems in parallel:**

1. **Internal Tasks** (`clients/*/tasks.json`, `CONTEXT.md`)
   - Campaign optimization work
   - Technical implementations
   - Strategic planning
   - Client-specific projects

2. **Google Tasks** (via Google Tasks API)
   - External commitments (meetings, calls)
   - Calendar reminders
   - Personal work items
   - Cross-client tasks

### Unified Task Manager

**View all tasks in one place:**

```
# Open Task Manager
Say to Claude: "open task manager"

# Or run manually
cd /Users/administrator/Documents/PetesBrain
python3 generate-tasks-overview-priority.py
open tasks-overview-priority.html
```

**What it shows:**
- ✅ All internal tasks (from `clients/*/tasks.json`)
- ✅ All Google Tasks (from Google Tasks API)
- ✅ Grouped by priority (P0, P1, P2, P3)
- ✅ Source clearly labeled (Internal vs Google Tasks)
- ✅ Due dates, time estimates, notes
- ✅ Parent-child task relationships

**Example output:**
```
Loading internal tasks...
Loaded 32 internal tasks
Fetched 35 active tasks from Google Tasks

============================================================
Total: 67 active tasks
  Internal tasks: 32
  Google Tasks: 35
============================================================
P0: 12 tasks
P1: 5 tasks
P2: 37 tasks
P3: 0 tasks
============================================================
```

### Task Completion Script

**Complete tasks with automatic routing:**

```bash
# The script determines automatically which system to use
cd /Users/administrator/Documents/PetesBrain/shared
./complete_task.py --task-id "xyz123" --title "Fix sitelinks" --client "smythson"
```

**Automatic routing logic:**
- Has client name? → Internal CONTEXT.md
- Meeting/call/reminder? → Google Tasks
- External commitment? → Google Tasks
- Campaign work? → Internal CONTEXT.md

**What it does:**
1. Determines task source automatically
2. Completes task in appropriate system
3. Logs to `tasks-completed.md` (if internal)
4. Provides clear confirmation

### How It All Works Together

**Backup System protects BOTH systems:**
- Every 3 hours: Backs up internal tasks.json files
- Every 3 hours: Exports Google Tasks to JSON
- Stores both in same archive: `tasks-backup-YYYY-MM-DD-HHMM.tar.gz`
- Uploads to Google Drive + saves local copy

**Recovery is complete:**
- Lost internal tasks? Restore from backup ✅
- Lost Google Tasks? Restore from backup ✅
- Both systems covered automatically ✅

**Workflow:**
1. **View tasks**: Open Task Manager → See all tasks from both systems
2. **Work on tasks**: Complete work as normal
3. **Complete tasks**: Use completion script → Automatic routing
4. **Protected**: Backups run every 3 hours → Both systems covered

---

**System Status:** ✅ Active
**Last Updated:** 2025-11-19 (Added Google Tasks integration)
**Next Review:** 2025-12-19  
