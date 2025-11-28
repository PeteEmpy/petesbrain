# Bi-Directional Task Synchronization

**Status:** ✅ Active  
**Last Updated:** 2025-11-08

## Overview

PetesBrain now has **bi-directional synchronization** between local todo files (`todo/*.md`) and Google Tasks. Changes in either system automatically sync to the other.

## How It Works

### Google Tasks → Local Files (via tasks-monitor.py)

**Runs:** Every 1 hour (via LaunchAgent)

**What it syncs:**
- ✅ Task completion status
- ✅ Task title changes
- ✅ Notes/details changes
- ✅ Due date changes
- ✅ Task uncompletion (moved back to active)

**How it works:**
1. Polls all Google Tasks
2. Compares with previous state
3. Finds matching local todo file by Google Task ID
4. Updates local file with changes

**Example:**
```
You complete a task in Google Tasks app
  ↓
tasks-monitor.py runs (every 1 hour)
  ↓
Detects completion
  ↓
Finds local todo file by Task ID
  ↓
Updates status: - [ ] Todo → - [x] Completed (2025-11-08 14:30)
```

### Local Files → Google Tasks (via sync-todos-to-google-tasks.py)

**Runs:** Every 1 hour (via LaunchAgent)

**What it syncs:**
- ✅ Status changes (`- [ ]` ↔ `- [x]`)
- ✅ Title changes (if you edit the `# Title`)
- ✅ Notes/details changes (if you edit `## Details`)
- ✅ Due date changes (if you edit `**Due Date:**`)

**How it works:**
1. Scans all local todo files
2. Extracts Google Task ID from each file
3. Compares current file state with last sync state
4. Updates Google Tasks with any changes

**Example:**
```
You edit todo/20251108-review-budgets.md:
  - Change status to - [x] Completed
  - Update title
  ↓
Run: python3 agents/system/sync-todos-to-google-tasks.py
  ↓
Script detects changes
  ↓
Updates Google Task:
  - Marks as completed
  - Updates title
```

## Usage

### Automatic Sync (Both Directions)

Both sync scripts run automatically every hour via LaunchAgents:
- **Google Tasks → Local**: `tasks-monitor.py` (every 1 hour)
- **Local → Google Tasks**: `sync-todos-to-google-tasks.py` (every 1 hour)

No manual action needed - changes sync automatically within 1 hour.

### Manual Sync

You can also run either script manually anytime:

```bash
# Sync Google Tasks → Local files
python3 agents/system/tasks-monitor.py

# Sync Local files → Google Tasks
python3 agents/system/sync-todos-to-google-tasks.py
```

## What Gets Synced

### ✅ Synced Fields

| Field | Google Tasks → Local | Local → Google Tasks |
|-------|---------------------|---------------------|
| Status (completed/incomplete) | ✅ Yes | ✅ Yes |
| Title | ✅ Yes | ✅ Yes |
| Notes/Details | ✅ Yes | ✅ Yes |
| Due Date | ✅ Yes | ✅ Yes |

### ⚠️ Not Synced (Yet)

- Notes section additions (only full replacement)
- Custom metadata fields
- File attachments

## Matching Files to Tasks

Files are matched to Google Tasks using the **Google Task ID** stored in the local file:

```markdown
**Google Task ID:** abc123xyz789
```

The sync scripts search for this ID in various formats:
- `**Google Task ID:** abc123xyz789`
- `Google Task ID: abc123xyz789`
- `` `abc123xyz789` ``

## Sync State Tracking

The sync system tracks:
- **tasks-state.json**: Tracks Google Tasks state (for Google → Local sync)
- **todo-sync-state.json**: Tracks local file state (for Local → Google sync)

These files prevent unnecessary updates and detect what changed.

## Troubleshooting

### Tasks Not Syncing

**Check:**
1. Does the local file have a Google Task ID?
2. Is the Task ID correct? (check in Google Tasks web)
3. Run sync script manually to see errors

### Duplicate Updates

**Cause:** Both sync scripts running simultaneously

**Fix:** The state files prevent this, but if issues occur:
- Wait for one sync to complete before running the other
- Check sync state files aren't corrupted

### Status Not Updating

**Check:**
1. Is the status format correct? (`- [ ]` or `- [x]`)
2. Is it in the `## Status` section?
3. Run sync script to see if errors occur

## Examples

### Example 1: Complete Task in Google Tasks

1. Open Google Tasks app
2. Mark task as complete
3. Wait for tasks-monitor.py to run (or run manually)
4. Local file updates: `- [ ] Todo` → `- [x] Completed (2025-11-08 14:30)`

### Example 2: Edit Task Locally

1. Edit `todo/20251108-review-budgets.md`:
   - Change title
   - Mark as complete: `- [x] Completed`
2. Run: `python3 agents/system/sync-todos-to-google-tasks.py`
3. Google Task updates with new title and completion status

### Example 3: Change Due Date in Google Tasks

1. Update due date in Google Tasks web/app
2. tasks-monitor.py detects change
3. Local file updates: `**Due Date:** 2025-11-10`

## Future Enhancements

- Real-time sync (file watcher for instant updates)
- Conflict resolution (when both systems change simultaneously)
- Sync custom metadata fields
- Sync notes section additions (not just replacements)

---

**Related Documentation:**
- [Google Tasks Integration](GOOGLE-TASKS-INTEGRATION.md)
- [Tasks Monitor](../agents/system/tasks-monitor.py)
- [Sync Script](../agents/system/sync-todos-to-google-tasks.py)

