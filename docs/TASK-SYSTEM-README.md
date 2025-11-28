# Task System - Quick Start

> **Full documentation**: See [TASK-SYSTEM-COMPLETE-GUIDE.md](TASK-SYSTEM-COMPLETE-GUIDE.md)

## The Golden Rules

### 1. ✅ Tasks Go in Root
```
clients/{client}/tasks.json        ← YES, always here
```

### 2. ❌ Never in Product-Feeds
```
clients/{client}/product-feeds/... ← NO, never put tasks here
```

### 3. 🔄 Two Systems Don't Sync
```
Internal (tasks.json) ← NO SYNC → Google Tasks
   (Client work)              (Personal reminders)
```

---

## Quick Commands

### View Tasks
```bash
# Open task manager
open tasks-overview.html

# Or priority view
open tasks-overview-priority.html
```

### Add a Task (Python)
```python
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()

service.create_task(
    title='[Client] Do something',
    client='client-slug',
    priority='P0',
    due_date='2025-12-01',
    notes='Context here'
)
```

### Complete a Task
```python
service.complete_task(
    task_id='uuid-here',
    client='client-slug',
    completion_notes='What I did'
)
```

### Validate System
```bash
python3 scripts/validate-task-system.py
```

---

## Troubleshooting

### Tasks not showing?
1. Check file location: `clients/{client}/tasks.json` (not in product-feeds)
2. Validate JSON: `python3 -m json.tool clients/{client}/tasks.json`
3. Regenerate HTML: `python3 generate-tasks-overview.py`

### Tasks appearing twice?
Check for duplicates:
```bash
find clients/{client} -name "tasks.json"
```
If found in both root and product-feeds, merge them (see full guide).

### Completed task still showing?
Use `service.complete_task()` not `service.update_task(status='completed')`

---

## File Structure

```
clients/{client}/
├── tasks.json              ← All active tasks
├── tasks-completed.md      ← Completed tasks archive
├── CONTEXT.md              ← Client context
├── audits/
├── emails/
├── reports/
└── scripts/
```

---

## Priority Levels

| Priority | Meaning | Due Date |
|----------|---------|----------|
| P0 | Urgent | Today |
| P1 | High | This week |
| P2 | Normal | This month |
| P3 | Low | Someday |

---

## Need More Help?

- **Full guide**: [TASK-SYSTEM-COMPLETE-GUIDE.md](TASK-SYSTEM-COMPLETE-GUIDE.md)
- **Validation**: `python3 scripts/validate-task-system.py`
- **Search completed**: `grep "task" clients/*/tasks-completed.md`
- **Backups**: `backups/tasks/` (daily at 6am)

---

**Last Updated**: 2025-11-26
