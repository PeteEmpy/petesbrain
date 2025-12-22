# Task System Guide

**Last Updated:** 2025-12-16
**Status:** ✅ Active - Single Internal System

---

## ⚠️ Important Update - December 16, 2025

**Google Tasks integration has been deprecated.** PetesBrain now uses a **single internal task system** for all task management.

**Historical Context**: Previously, PetesBrain used two independent systems (Internal + Google Tasks). As of December 16, 2025, all Google Tasks functionality has been migrated to the internal system.

---

## Overview

PetesBrain uses a **single internal task system** for all task management:

- **Storage**: Per-client JSON files at `clients/{client}/tasks.json`
- **Service**: `shared/client_tasks_service.py`
- **Archive**: Completed tasks logged to `clients/{client}/tasks-completed.md`
- **UI**: Task Manager skill (`.claude/skills/task-manager/`)

---

## Task System Architecture

### File Structure

```
clients/
├── smythson/
│   ├── tasks.json              # Active tasks
│   ├── tasks-completed.md      # Completed tasks archive
│   └── ...
├── devonshire-hotels/
│   ├── tasks.json
│   ├── tasks-completed.md
│   └── ...
└── roksys/                     # Personal/business tasks
    ├── tasks.json
    ├── tasks-completed.md
    └── ...
```

### Task Properties

```json
{
  "id": "uuid",
  "title": "[Client] Task description",
  "priority": "P0",
  "due": "2025-12-20",
  "recurring": "weekly",
  "parent_id": "uuid",
  "notes": "Additional context",
  "created_at": "2025-12-16T10:00:00",
  "tags": ["google-ads", "optimization"]
}
```

### Priority Levels

- **P0** - Critical/urgent (blocking issues, time-sensitive)
- **P1** - Important (client requests, optimizations)
- **P2** - Normal (improvements, non-urgent)
- **P3** - Low priority (nice-to-have, future work)

### Recurring Tasks

Supported patterns:
- `"weekly"` - Repeats every 7 days
- `"monthly"` - Repeats on same day of month
- `"custom"` - Repeats based on custom interval

When a recurring task is completed, it automatically creates a new instance with the next due date.

### Parent/Child Hierarchy

Tasks can have parent-child relationships for complex projects:

```python
# Parent task
{
  "id": "parent-uuid",
  "title": "[NMA] Q1 2026 Improvement Plan",
  "priority": "P1"
}

# Child tasks
{
  "id": "child-1",
  "parent_id": "parent-uuid",
  "title": "[NMA] Week 1: Audit current campaigns",
  "priority": "P1"
}
```

**Daily Briefing Behavior**: Only overdue child tasks appear in daily briefing (parent tasks are containers).

---

## Using the Task System

### Creating Tasks

**Via Python (agents/scripts)**:
```python
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()
service.create_task(
    title='[Smythson] Review Q4 performance',
    client='smythson',
    priority='P1',
    due='2025-12-20',
    recurring='monthly',
    notes='Check ROAS, revenue, and budget utilization'
)
```

**Via Claude Code**:
- Ask: "Create a task for [client] to [description]"
- Claude will use `ClientTasksService` automatically

### Completing Tasks

**Via Python**:
```python
service = ClientTasksService()
service.complete_task(client='smythson', task_id='task-uuid')
```

**What Happens**:
1. Task marked as completed in `tasks.json`
2. Automatically logged to `clients/{client}/tasks-completed.md`
3. If recurring, new instance created with next due date
4. Task remains in `tasks.json` temporarily (cleanup after 30 days)

### Viewing Tasks

**Task Manager Skill**:
```python
Skill(command='task-manager')
# Opens HTML dashboard in browser with all tasks by client
```

**Via Python**:
```python
service = ClientTasksService()

# All tasks for a client
tasks = service.list_tasks(client='smythson')

# Filter by priority
p0_tasks = service.list_tasks(client='smythson', priority='P0')

# All tasks across all clients
all_tasks = service.list_all_tasks()
```

### Searching Historical Tasks

Completed tasks are permanently archived in `tasks-completed.md` files:

```bash
# Search all completed tasks
grep -r "keyword" clients/*/tasks-completed.md

# Search specific client
grep "keyword" clients/smythson/tasks-completed.md

# Search by date range
grep "2025-12" clients/*/tasks-completed.md
```

---

## Task Workflows

### Client Work Tasks

**When to create**:
- Client requests (email, meeting, message)
- Google Ads optimizations
- Reporting deliverables
- Campaign audits
- Budget adjustments

**Priority guidelines**:
- P0: Client requested urgent, deadline today/tomorrow
- P1: Standard client work, due this week
- P2: Improvements, optimizations, no deadline
- P3: Future enhancements, "nice to have"

**Example**:
```python
service.create_task(
    title='[Devonshire] Review budget allocation for Q1',
    client='devonshire-hotels',
    priority='P1',
    due='2025-12-22',
    notes='Check if current split matches seasonal demand'
)
```

### Recurring Tasks

**When to create**:
- Weekly reporting
- Monthly audits
- Quarterly reviews
- Regular optimizations

**Example**:
```python
service.create_task(
    title='[Smythson] Weekly performance review',
    client='smythson',
    priority='P1',
    recurring='weekly',
    notes='Check ROAS, spend, and new opportunities'
)
```

### Multi-Step Projects

**Use parent/child hierarchy for**:
- Multi-week improvement plans
- Campaign launch checklists
- Meeting action items
- Complex optimizations

**Example**:
```python
# Create parent
parent = service.create_task(
    title='[Tree2mydoor] Q1 Campaign Restructure',
    client='tree2mydoor',
    priority='P1'
)

# Create children
service.create_task(
    title='[Tree2mydoor] Week 1: Audit current structure',
    client='tree2mydoor',
    priority='P1',
    parent_id=parent['id'],
    due='2025-12-20'
)

service.create_task(
    title='[Tree2mydoor] Week 2: Implement new campaigns',
    client='tree2mydoor',
    priority='P1',
    parent_id=parent['id'],
    due='2025-12-27'
)
```

---

## Daily Briefing Integration

Tasks automatically appear in the daily briefing email (7 AM):

**What's Included**:
- Tasks due today (all priorities)
- Overdue tasks (P0, P1 only)
- Overdue child tasks (parent-child projects)

**What's Excluded**:
- Future tasks (not yet due)
- Parent tasks (only children with due dates appear)
- Completed tasks (archived immediately)

**Organized by Client**:
```
Today's Work - Smythson
- [P1] Review Q4 performance (Due today)
- [P0] Fix disapproved ads (Overdue 2 days)

Today's Work - Devonshire Hotels
- [P1] Weekly report (Due today)
```

---

## Task Manager UI

HTML dashboard showing all tasks organized by client:

**Features**:
- Grouped by client
- Color-coded by priority (P0=red, P1=orange, P2=blue, P3=gray)
- Shows due dates and overdue indicators
- Parent-child indentation
- Recurring task indicators

**Access**:
```python
Skill(command='task-manager')
# Opens in browser at file://...
```

---

## Best Practices

### Task Naming

**Use consistent format**:
```
[Client] Action verb + object + context

✅ Good:
- [Smythson] Review Q4 budget allocation
- [Devonshire] Fix disapproved ads in Brand campaign
- [Tree2mydoor] Test new RSA variations

❌ Bad:
- Review budget (missing client)
- Smythson - Q4 stuff (unclear action)
- Check things (no context)
```

### Priority Assignment

**P0 - Critical** (use sparingly):
- Client emergency
- Deadline today
- Blocking issue
- Revenue risk

**P1 - Important** (most tasks):
- Standard client work
- Weekly deliverables
- Optimization opportunities

**P2 - Normal**:
- Improvements
- Testing new approaches
- Non-urgent optimizations

**P3 - Low**:
- Future enhancements
- "Nice to have" features
- Research tasks

### Completion Hygiene

**Always complete tasks when done** (not "later"):
- Keeps daily briefing accurate
- Creates proper audit trail
- Triggers recurring task creation
- Prevents forgotten tasks

**Use completion notes**:
```python
service.complete_task(
    client='smythson',
    task_id='task-uuid',
    completion_notes='Implemented 5 new RSAs, ROAS improved 15%'
)
```

---

## Troubleshooting

### Task Not Showing in Daily Briefing

**Check**:
1. Is the due date today or earlier?
2. Is it a parent task? (Only children with due dates appear)
3. Is the client folder correct?
4. Run: `python3 agents/daily-intel-report/daily-intel-report.py`

### Recurring Task Not Creating New Instance

**Check**:
1. Was the task properly completed via `ClientTasksService`?
2. Check `recurring` property is set correctly
3. Verify task has `id` property (required for recurring)

### Tasks Not in Task Manager UI

**Regenerate HTML**:
```bash
cd /Users/administrator/Documents/PetesBrain
python3 generate-all-task-views.py
```

### Task File Corrupted

**Restore from backup**:
```bash
# Daily backups stored in Google Drive
# Use backup-tasks skill to restore
Skill(command='restore-tasks')
```

---

## Historical Reference: Google Tasks (Deprecated)

**Prior to December 16, 2025**, PetesBrain used two independent systems:

1. **Internal System** - Client work, recurring tasks
2. **Google Tasks** - Personal reminders, AI-generated suggestions

**Why It Was Deprecated**:
- Maintenance overhead (two systems to sync)
- Google Tasks API limitations (no recurring support)
- Confusion about which system to use
- Risk of tasks getting lost between systems

**Migration Details**:
- All active Google Tasks exported to JSON (December 16, 2025)
- 15 relevant tasks migrated to internal system
- 77 low-priority tasks archived
- Google Tasks MCP server disabled
- `google_tasks_client.py` archived
- 6 agents updated to use internal system only

---

## Related Documentation

- **`docs/INTERNAL-TASK-SYSTEM.md`** - Technical implementation details (543 lines)
- **`.claude/skills/task-manager/skill.md`** - Task Manager UI documentation
- **`.claude/skills/backup-tasks/skill.md`** - Task backup procedures
- **`.claude/skills/restore-tasks/skill.md`** - Task restoration guide
- **`shared/client_tasks_service.py`** - Python service implementation

---

## Quick Reference

### Common Operations

```python
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()

# Create task
service.create_task(title='[Client] Description', client='client-slug', priority='P1')

# List tasks
tasks = service.list_tasks(client='client-slug')

# Complete task
service.complete_task(client='client-slug', task_id='uuid')

# Delete task
service.delete_task(client='client-slug', task_id='uuid')
```

### Task Manager

```python
# Open task UI
Skill(command='task-manager')

# Regenerate HTML
# cd ~/Documents/PetesBrain && python3 generate-all-task-views.py
```

---

**For questions or issues, consult `docs/INTERNAL-TASK-SYSTEM.md` or ask Claude Code.**
