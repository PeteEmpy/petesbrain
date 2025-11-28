---
name: backup-tasks
description: Manually triggers an immediate backup of all tasks.json files to Google Drive. Use when user says "backup tasks", "backup my tasks", "save tasks", or before major task restructuring.
allowed-tools: Bash, Read
---

# Backup Tasks Skill

---

## What You Do

1. **Confirm the action**:
   ```
   I'll create a backup of all your tasks right now. This includes:
   - All client tasks.json files (internal tasks)
   - Roksys tasks.json
   - Task state files
   - Google Tasks (all lists exported to JSON)
   ```

2. **Run the backup script**:
   ```bash
   python3 /Users/administrator/Documents/PetesBrain/agents/tasks-backup/tasks-backup.py
   ```

3. **Report results**:
   - Show how many files were backed up
   - Show archive size
   - Confirm upload location (Google Drive + local fallback)
   - Show backup filename with timestamp

4. **List recent backups**:
   ```bash
   ls -lht /Users/administrator/Documents/PetesBrain/_backups/tasks/ | head -10
   ```

---

## Expected Output

```
✅ Tasks backup completed successfully!

Backup Details:
📥 Exporting Google Tasks...
   ✅ Peter's List: 20 tasks
   ✅ Client Work: 20 tasks
✅ Exported 2 Google Tasks lists (40 total tasks)

- Local task files: 19
- Google Tasks exports: 2
- Total files: 21
- Archive size: 61.9 KB
- Timestamp: 2025-11-19-1455
- **Cloud Storage:** ✅ Google Drive > PetesBrain-Backups/Tasks/tasks-backup-2025-11-19-1455.tar.gz
- **Local Fallback:** ✅ _backups/tasks/tasks-backup-2025-11-19-1455.tar.gz
- File ID: 1fJX8h0Xg7qGLWIP61Q3g_OIf8ukudXit

**Both cloud and local backups created successfully!**
**Both internal tasks AND Google Tasks are now protected!**

Recent Backups (last 10):
- tasks-backup-2025-11-19-1455.tar.gz (just now)
- tasks-backup-2025-11-19-1155.tar.gz (3 hours ago)
- tasks-backup-2025-11-19-0855.tar.gz (6 hours ago)
...
```

---

## When to Use

- Before major task restructuring
- Before running restore (safety backup)
- When user explicitly requests backup
- Before deleting multiple tasks
- Before testing new task features

---

## Notes

- This is a manual trigger of the automated backup agent
- Automated backups run every 3 hours automatically
- Backups are kept for 30 days
- No confirmation needed (safe operation, creates data)
- Can be run as many times as needed
