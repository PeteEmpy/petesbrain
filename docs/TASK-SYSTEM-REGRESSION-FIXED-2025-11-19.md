# Task System Regression Fixed - 2025-11-19

## Problem

Completed tasks were appearing in the task manager even after being marked complete.

## Root Cause

The `ClientTasksService.complete_task()` method in `shared/client_tasks_service.py` was **marking tasks as completed** instead of **removing them** from tasks.json.

```python
# ❌ WRONG (old code)
completed_task = self.update_task(task_id, client, status='completed', ...)
```

This violated the Manual Task Completion Protocol which states:

> **CRITICAL:** Tasks MUST be removed from tasks.json, not just marked completed.
> Completed tasks left in tasks.json will reappear in task managers.

## Solution

Updated `complete_task()` method to:

1. **Remove** task from tasks.json immediately (not mark as completed)
2. **Log** to tasks-completed.md immediately
3. No weekly cleanup needed - tasks gone instantly

```python
# ✅ CORRECT (new code)
# Find and remove the task
for i, t in enumerate(data['tasks']):
    if t['id'] == task_id:
        completed_task = data['tasks'].pop(i)  # REMOVE, don't mark
        break

# Save tasks.json without the task
self._save_client_tasks(client, data)

# Log to permanent record
self._log_to_completed_file(client, completed_task, completion_notes)
```

## Files Modified

- `shared/client_tasks_service.py` (lines 377-508)
  - Fixed `complete_task()` method to REMOVE tasks instead of marking completed
  - Added `_log_to_completed_file()` helper method
  - Added `_rebuild_cache()` method to update task manager cache
  - Cache now rebuilds automatically after every task completion

## Testing

Previously had 23 completed tasks stuck in tasks.json files. These were cleaned up manually, and the fix ensures no new ones will accumulate.

## Related Files (Correct Implementations)

- `shared/complete_task.py` - Already had correct implementation
- `shared/scripts/cleanup-completed-tasks.py` - Weekly cleanup (now backup only)

## Additional Fix: Task Manager Cache Issue

**Problem Discovered (Nov 19, 18:10):**
Even after tasks were correctly removed from `clients/[client]/tasks.json`, they still appeared in the task manager UI.

**Root Cause:**
Task manager reads from `data/state/client-tasks.json` (aggregated cache file), which wasn't being updated when tasks were completed.

**Solution:**
Added `_rebuild_cache()` method that:
- Aggregates all tasks from all clients
- Writes to `data/state/client-tasks.json`
- Called automatically after every task completion

**Result:**
Task manager now updates immediately when tasks are completed. No stale tasks in UI.

## Prevention

The weekly cleanup script remains as a safety net, but with this fix, completed tasks should never accumulate in tasks.json.
