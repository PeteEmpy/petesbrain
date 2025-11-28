---
name: task-sync
description: Manually synchronizes tasks bi-directionally between local todo files and Google Tasks. Use when user says "sync tasks", "sync todos", "update tasks", "refresh tasks", or needs immediate synchronization before a meeting or review.
allowed-tools: Bash, Read
---

# Task Sync Skill

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

