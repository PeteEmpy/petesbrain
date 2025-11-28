# Task Completion Workflow - Best Practices

**Last Updated:** 2025-11-19
**Status:** Active Protocol

## The Problem

Completed tasks were accumulating in `tasks.json` files with `status='completed'` instead of being removed, causing them to reappear in task managers.

## The Fix (Nov 19, 2025)

When tasks are completed and logged to `tasks-completed.md`, they must be **REMOVED** from `tasks.json`, not just marked as `status='completed'`.

---

## Correct Completion Workflow

### For Manual Task Completions (via Claude)

When a user reports completing a task:

1. **Log to tasks-completed.md** ✅
   ```python
   # Add entry to clients/{client}/tasks-completed.md
   ```

2. **Remove from tasks.json** ✅
   ```python
   # Load tasks.json
   data = json.load(file)

   # Remove the completed task entirely
   data['tasks'] = [t for t in data['tasks'] if t['id'] != task_id]

   # Save
   json.dump(data, file)
   ```

3. **Clear manual-task-notes.json** ✅
   ```python
   # Reset to empty array
   []
   ```

### For Automated Completions (via tasks-monitor)

The `tasks-monitor` agent handles Google Tasks completions:

1. Detects completed Google Tasks
2. Logs to `tasks-completed.md`
3. Updates `CONTEXT.md`
4. **Does NOT manage local tasks.json** (different system)

---

## Two Separate Task Systems

### System 1: Google Tasks (External)
- **Storage:** Google Tasks API
- **Completion Handler:** `agents/tasks-monitor/tasks-monitor.py`
- **Output:** `tasks-completed.md` + `CONTEXT.md`
- **Runs:** Every 6 hours (via launchctl)

### System 2: Local Tasks.json (Internal)
- **Storage:** `clients/{client}/tasks.json`
- **Completion Handler:** Manual (via Claude Code)
- **Output:** `tasks-completed.md`
- **Must:** Remove tasks after logging, not just mark as completed

---

## Common Mistakes

❌ **Wrong:**
```python
# Marking as completed but leaving in tasks.json
task['status'] = 'completed'
task['completed_at'] = datetime.now().isoformat()
# Still in tasks.json -> will reappear!
```

✅ **Right:**
```python
# Log to tasks-completed.md first
with open('tasks-completed.md', 'a') as f:
    f.write(entry)

# Then remove from tasks.json
data['tasks'] = [t for t in data['tasks'] if t['id'] != task_id]
```

---

## Archive Old Completed Tasks

The `ClientTasksService.archive_completed_tasks()` method can clean up old completed tasks, but it should RARELY be needed if the completion workflow is followed correctly.

```python
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()
archived = service.archive_completed_tasks(older_than_days=30)
print(f"Archived {archived} old completed tasks")
```

---

## Verification

After completing tasks, verify they're gone:

```bash
# Check tasks.json has no completed tasks
grep -l '"status": "completed"' clients/*/tasks.json

# Should return nothing if workflow is correct
```

---

## Future Improvements

Consider adding a cleanup agent that runs weekly to:
1. Check for `status='completed'` in all tasks.json files
2. Verify they exist in tasks-completed.md
3. Remove them from tasks.json
4. Alert if discrepancies found

---

## Related Files

- `shared/client_tasks_service.py` - Task management service
- `agents/tasks-monitor/tasks-monitor.py` - Google Tasks monitor
- `docs/CLAUDE.md` - Manual task completion protocol
- `docs/TASK-SYSTEM-PROTOCOL-TEST.md` - Task system testing
