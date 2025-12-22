---
name: task-sync
description: DEPRECATED - Google Tasks integration has been removed. This skill is no longer functional.
allowed-tools: Read
deprecated: true
deprecated_date: 2025-12-16
---

# Task Sync Skill

## ⚠️ DEPRECATED - December 16, 2025

**This skill has been deprecated as part of the Google Tasks removal.**

**Reason**: Google Tasks integration has been fully removed from PetesBrain. The system now uses only the internal task system (`clients/{client}/tasks.json`).

**Alternative**: Use the internal task system directly via `ClientTasksService` or the `task-manager` skill.

---

## Original Documentation (Historical Reference Only)

## Instructions

When this skill is triggered:

1. **Explain what will happen**:
   - Both sync scripts will run:
     - `tasks-monitor.py` - Syncs Google Tasks → Local files
     - `sync-todos-to-google-tasks.py` - Syncs Local files → Google Tasks
   - This ensures bi-directional synchronization is current

2. **Run the Google Tasks → Local sync**:
   ```bash
   python3 agents/tasks-monitor/tasks-monitor.py
   ```
   - This checks Google Tasks for changes (completions, title updates, notes, due dates)
   - Updates matching local todo files
   - Reports what was synced

3. **Run the Local → Google Tasks sync**:
   ```bash
   python3 agents/sync-todos-to-google-tasks/sync-todos-to-google-tasks.py
   ```
   - This checks local todo files for changes
   - Updates matching Google Tasks
   - Reports what was synced

4. **Summarize the results**:
   - Report how many tasks were synced in each direction
   - Highlight any errors or warnings
   - Note if everything is already in sync

5. **Provide context**:
   - Remind that automatic sync runs every hour via LaunchAgents
   - This manual sync is useful for immediate updates or troubleshooting

## What Gets Synced

### Google Tasks → Local Files
- ✅ Task completion status
- ✅ Title changes
- ✅ Notes/details changes
- ✅ Due date changes
- ✅ Task uncompletion (moved back to active)

### Local Files → Google Tasks
- ✅ Status changes (`- [ ]` ↔ `- [x]`)
- ✅ Title changes
- ✅ Notes/details changes
- ✅ Due date changes

## Example Usage

**User**: "Sync my tasks now"

**Response**: 
- Runs both sync scripts
- Reports: "Synced 3 tasks from Google Tasks to local files, 2 tasks from local files to Google Tasks"
- Confirms synchronization is complete

## Notes

- Both scripts use state files to track changes and avoid unnecessary updates
- Tasks are matched by Google Task ID stored in local files
- If a task doesn't have a Google Task ID, it won't sync
- Errors are logged but don't stop the sync process

## Related Files

- `agents/tasks-monitor/tasks-monitor.py` - Google Tasks → Local sync
- `agents/sync-todos-to-google-tasks/sync-todos-to-google-tasks.py` - Local → Google Tasks sync
- `shared/google_tasks_client.py` - Google Tasks API client
- `docs/BI-DIRECTIONAL-TASK-SYNC.md` - Full documentation

