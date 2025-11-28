---
name: restore-tasks
description: Restores tasks.json files from a backup archive with safety protocols. Use when user says "restore tasks", "restore my tasks from backup", or needs to recover lost task data. CRITICAL - requires explicit confirmation before execution.
allowed-tools: Bash, Read, Write
---

# Restore Tasks Skill

**⚠️ CRITICAL SAFETY PROTOCOL - READ CAREFULLY**

---

## Safety Checks (MANDATORY)

### 1. Initial Warning
```
⚠️  WARNING: Task restoration will OVERWRITE all current tasks!

This is a destructive operation that will replace:
- All client tasks.json files (internal tasks)
- Roksys tasks.json
- Task state files
- Google Tasks exports (for reference - Google Tasks remain in Google)

Before proceeding, I MUST:
1. Create a safety backup of current state
2. Show you the list of available backups
3. Get your explicit confirmation

Do you want to continue? (yes/no)
```

**STOP HERE if user says "no" or seems uncertain**

---

### 2. Create Safety Backup

**ALWAYS do this before ANY restore:**

```bash
python3 /Users/administrator/Documents/PetesBrain/agents/tasks-backup/tasks-backup.py
```

Show confirmation:
```
✅ Safety backup created: tasks-backup-2025-11-19-1435.tar.gz

This backup captures your current state before restoration.
If restoration goes wrong, we can restore from this.
```

---

### 3. List Available Backups

```bash
ls -lht /Users/administrator/Documents/PetesBrain/_backups/tasks/
```

Present as table with:
- Backup number (for easy selection)
- Filename
- Date/time
- Size
- Age (how old)

Example:
```
Available Backups:

 #  | Filename                           | Date/Time       | Size    | Age
----|------------------------------------|-----------------|---------|-----------
 1  | tasks-backup-2025-11-19-1130.tar.gz| Nov 19 11:30   | 143 KB  | 3 hrs ago
 2  | tasks-backup-2025-11-19-0830.tar.gz| Nov 19 08:30   | 142 KB  | 6 hrs ago
 3  | tasks-backup-2025-11-19-0530.tar.gz| Nov 19 05:30   | 141 KB  | 9 hrs ago
 ...
```

Ask: **"Which backup number do you want to restore from?"**

---

### 4. Show Restore Preview

After user selects backup number, extract and show preview:

```bash
# Extract to temp location for preview
mkdir -p /tmp/tasks-restore-preview
tar -xzf /Users/administrator/Documents/PetesBrain/_backups/tasks/tasks-backup-XXXX.tar.gz -C /tmp/tasks-restore-preview

# Show what's in the backup
find /tmp/tasks-restore-preview -name "tasks.json" -o -name "tasks-state.json"
```

Present as:
```
Backup Preview: tasks-backup-2025-11-19-1455.tar.gz

This backup contains:
- 19 internal task files (clients + state)
- 2 Google Tasks exports (Peter's List, Client Work)
- Total: 21 files

Internal Tasks:
- 16 client task files
- 3 state files

Google Tasks Snapshot (reference):
- Peter's List: 20 tasks
- Client Work: 20 tasks

Note: Internal tasks will be restored. Google Tasks exports are for reference only
      (actual Google Tasks remain in Google and are not modified by restore).

Total internal tasks in backup: 156 tasks
Total Google Tasks snapshot: 40 tasks
```

---

### 5. Final Confirmation (EXPLICIT)

```
⚠️  FINAL CONFIRMATION REQUIRED

You are about to restore from: tasks-backup-2025-11-19-1130.tar.gz

This will REPLACE all current tasks with the backup from Nov 19, 11:30 AM.

Any changes made since then will be LOST.

Your current state has been backed up to: tasks-backup-2025-11-19-1435.tar.gz

To proceed, type exactly: RESTORE

To cancel, type anything else or just press Enter.
```

**Read user's response**

**If user types ANYTHING other than exactly "RESTORE" (case-sensitive), ABORT:**
```
❌ Restoration cancelled. No changes made.

Your current tasks are safe and unchanged.
```

---

### 6. Execute Restoration (Only if "RESTORE" typed)

```bash
# Extract backup to PetesBrain directory
cd /Users/administrator/Documents/PetesBrain

tar -xzf _backups/tasks/tasks-backup-XXXX.tar.gz

# Verify extraction
echo "Verifying restored files..."
find clients -name "tasks.json" | wc -l
find roksys -name "tasks.json" | wc -l
```

---

### 7. Post-Restoration Report

```
✅ Tasks restored successfully from backup!

Restored: tasks-backup-2025-11-19-1455.tar.gz
Time: 2025-11-19 14:56:01

Files restored:
- 19 internal task files (16 client tasks.json + 3 state files)
- 2 Google Tasks exports extracted (for reference)

Your internal tasks are now at the state from: Nov 19, 2025 14:55

Note: Google Tasks exports are in the backup for reference, but actual Google Tasks
      remain in Google (not modified by this restore). To restore Google Tasks, you
      would need to manually import from the exported JSON files.

Safety backup location (in case you need to revert):
_backups/tasks/tasks-backup-2025-11-19-1435.tar.gz

To revert this restoration, run "restore tasks" again and select backup #1.
```

---

## Emergency Rollback

If restoration goes wrong, immediately:

```bash
# Restore from the safety backup we just created
tar -xzf /Users/administrator/Documents/PetesBrain/_backups/tasks/tasks-backup-2025-11-19-1435.tar.gz -C /Users/administrator/Documents/PetesBrain
```

---

## Safeguards Summary

✅ **Safety backup created automatically before restore**
✅ **Preview backup contents before applying**
✅ **Explicit "RESTORE" confirmation required (case-sensitive)**
✅ **Clear warnings about data loss**
✅ **Post-restore verification**
✅ **Rollback instructions provided**

---

## Notes

- **Never skip the safety backup** - it's your undo button
- **The word "RESTORE" must be typed exactly** - this prevents accidents
- **Restoration is reversible** - we always keep the pre-restore backup
- **Multiple confirmations** - user must confirm multiple times
- **Clear at every step** - user always knows what's happening
