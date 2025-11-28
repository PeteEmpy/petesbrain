# Task System Fix - 25 November 2025

## Problem

Tasks were being created in the wrong location (`clients/{client}/product-feeds/tasks.json`) instead of the correct location (`clients/{client}/tasks.json`), causing them not to appear in the task manager.

**Root cause:** Old inbox processors were still hardcoded to use the `product-feeds/` subdirectory, which was the legacy location before `ClientTasksService` was created.

## Impact

- Only 2 P0 urgent tasks were visible in task manager
- Actually had 24 P0 tasks across all clients
- 41 total tasks were "hidden" in product-feeds directories

## Solution

### 1. Migrated Existing Tasks

Moved all 41 tasks from `product-feeds/tasks.json` to `clients/{client}/tasks.json`:
- Deduplicated against existing tasks (0 duplicates found)
- Preserved all task metadata
- Deleted empty product-feeds task files

### 2. Updated Inbox Processors

Updated three files to use `ClientTasksService` instead of direct file writes:

**`/agents/inbox-processor/inbox-processor.py`:**
- Added import: `from shared.client_tasks_service import ClientTasksService`
- Replaced manual JSON file creation (lines 739-799)
- Now uses: `task_service.create_task(...)`

**`/agents/ai-inbox-processor/ai-inbox-processor.py`:**
- Added import: `from shared.client_tasks_service import ClientTasksService`
- Replaced manual JSON file creation for quick tasks (lines 636-678)
- Now uses: `task_service.create_task(...)`

**`/shared/scripts/process-manual-task-notes.py`:**
- Updated `load_task_file()` method (lines 34-40)
- Removed product-feeds fallback logic
- Now only reads from `clients/{client}/tasks.json`

### 3. Fixed Task Generator

Updated `generate-tasks-overview.py` to accept multiple task statuses:
- Changed filter from `status == 'active'`
- To: `status in ['active', 'pending', 'in_progress']`
- Updated 3 locations (lines 262, 352, 372)

## Results

**Before:**
- Visible tasks: 2 P0 + handful of others
- Location: Mixed between product-feeds and main

**After:**
- Visible tasks: 17 P0 + 39 other = 56 total client tasks
- Plus 27 Google Tasks = 68 total in task manager
- Location: All in correct `clients/{client}/tasks.json`

## Task Locations (Definitive)

| Task Type | Correct Location | Status |
|-----------|------------------|--------|
| Client work tasks | `clients/{client}/tasks.json` | ✅ Fixed |
| Personal/Roksys tasks | `roksys/tasks.json` | ✅ Correct |
| Product feed monitoring | Should NOT use tasks.json | ⚠️ TBD |
| Google Tasks | Google API ("Peter's List") | ✅ Correct |

## Files Modified

1. `/agents/inbox-processor/inbox-processor.py`
2. `/agents/ai-inbox-processor/ai-inbox-processor.py`
3. `/shared/scripts/process-manual-task-notes.py`
4. `/generate-tasks-overview.py`
5. 13 client `tasks.json` files (migrated tasks)

## Verification

```bash
# Count P0 tasks
find clients -name "tasks.json" -exec jq '.tasks[] | select(.priority == "P0")' {} \; | wc -l
# Result: 24 P0 tasks

# Verify no product-feeds task files
find clients -name "product-feeds/tasks.json"
# Result: (none found)

# Regenerate task overview
python3 generate-tasks-overview.py
# Result: 17 P0 tasks + 39 others = 56 total
```

## Next Steps

1. ✅ All inbox processors now use `ClientTasksService`
2. ✅ Task generator reads correct location
3. ⚠️ Need to update any skills/agents that create tasks
4. ⚠️ Consider deprecating `product-feeds/tasks.json` entirely

## Prevention

Going forward, all task creation MUST use `ClientTasksService`:

```python
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()
task_id = service.create_task(
    title="Task title",
    client="client-slug",
    priority="P0",
    due_date="2025-11-30",
    time_estimate_mins=60,
    notes="Task details",
    source="Source description",
    tags=["tag1", "tag2"],
    task_type="standalone"
)
```

**NEVER write directly to tasks.json files.**

---

**Fixed by:** Claude Code
**Date:** 25 November 2025
**Related docs:** `/docs/TASK-SYSTEM-DECISION-GUIDE.md`
