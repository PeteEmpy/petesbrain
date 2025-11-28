# Internal Client Task System

**Last Updated:** 2025-11-18
**Status:** ✅ Active (per-client architecture implemented Nov 18, 2025)

## Overview

PetesBrain uses an **internal JSON-based task system** with per-client storage for managing client work. Each client has their own `clients/{client}/tasks.json` file with support for parent/child task hierarchies.

**Google Tasks is still used for:** Personal tasks only ("Peter's List")
**Internal system is used for:** All client-related tasks

## Why Per-Client Architecture?

### Previous Architecture (Before Nov 18, 2025)
- **Single global file**: `data/state/client-tasks.json` contained all client tasks
- **Token limits**: Large file approaching limits, difficult to manage
- **No hierarchy**: All tasks were flat, no way to group related tasks
- **Scaling issues**: Adding clients increased file size

### Current Architecture (Nov 18, 2025+)
- ✅ **Per-client files**: `clients/{client}/tasks.json` (one file per client)
- ✅ **Parent/child support**: Group related tasks from meetings or projects
- ✅ **Scalable**: Each client independent, no global file bloat
- ✅ **Natural organization**: Tasks live with client's other files
- ✅ **Better mental model**: Matches existing pattern (tasks-completed.md per client)

## Architecture

### Storage Pattern

```
clients/
├── smythson/
│   ├── tasks.json               # Smythson's tasks
│   ├── tasks-completed.md
│   └── CONTEXT.md
├── superspace/
│   ├── tasks.json               # Superspace's tasks
│   ├── tasks-completed.md
│   └── CONTEXT.md
└── national-motorsports-academy/
    ├── tasks.json               # NMA's tasks (parent/child example)
    ├── tasks-completed.md
    └── CONTEXT.md
```

Each client's tasks are self-contained in their own file.

### Task Schema

```json
{
  "id": "uuid",
  "title": "[Client Name] Task description",
  "type": "parent|child|standalone",
  "parent_id": "uuid or null",
  "children": ["uuid1", "uuid2"] or null,
  "client": "client-slug",
  "priority": "P0|P1|P2|P3",
  "due_date": "YYYY-MM-DD",
  "time_estimate_mins": 30,
  "notes": "Additional context",
  "source": "Meeting|Email|AI Generated|Manual",
  "tags": ["tag1", "tag2"],
  "context": {
    "google_task_id": "...",
    "migrated_at": "ISO timestamp"
  },
  "status": "active|completed",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "completed_at": "ISO timestamp or null"
}
```

**Key Fields**:
- **type**: `parent`, `child`, or `standalone`
- **parent_id**: For child tasks, references parent UUID
- **children**: For parent tasks, array of child UUIDs
- **client**: Normalized client slug (e.g., "national-motorsports-academy")

### Task Types

**Standalone Task**:
```json
{
  "type": "standalone",
  "parent_id": null,
  "children": null
}
```
Independent task not part of any hierarchy.

**Parent Task**:
```json
{
  "type": "parent",
  "parent_id": null,
  "children": ["uuid1", "uuid2", "uuid3"]
}
```
Groups multiple child tasks (e.g., meeting with multiple action items).

**Child Task**:
```json
{
  "type": "child",
  "parent_id": "parent-uuid",
  "children": null
}
```
Individual action item belonging to a parent.

## Core Service

### Location
`shared/client_tasks_service.py`

### Basic Usage

```python
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()

# Create standalone task
task = service.create_task(
    title="[Superspace] Review campaign performance",
    client="superspace",
    priority="P1",
    due_date="2025-11-20",
    time_estimate_mins=30,
    notes="Check last 7 days",
    source="Manual",
    task_type="standalone"
)

# Get tasks for a client
superspace_tasks = service.get_active_tasks(client="superspace")

# Get P0 tasks across all clients
urgent_tasks = service.get_active_tasks(priority="P0")

# Complete a task
service.complete_task(task['id'], client="superspace")
```

### Parent/Child Tasks

**Creating parent with children**:

```python
parent_task = service.create_parent_with_children(
    parent_title="[NMA] 3-Week Account Improvement Plan",
    client="national-motorsports-academy",
    parent_due_date="2025-12-08",
    parent_notes="Complete 3-week plan from Nov 17 meeting...",
    parent_source="Meeting with Paul Riley & Anwesha (Nov 17, 2025)",
    parent_tags=["nma-improvement-plan", "meeting-nov-17"],
    parent_priority="P1",
    children_data=[
        {
            "title": "[NMA] Week 1: Fix disapproved sitelinks",
            "due_date": "2025-11-19",
            "time_estimate_mins": 30,
            "priority": "P1",
            "notes": "Sitelink fixes...",
            "tags": ["sitelinks", "quick-win"]
        },
        {
            "title": "[NMA] Week 2: Review Target CPA",
            "due_date": "2025-11-29",
            "time_estimate_mins": 60,
            "priority": "P1",
            "notes": "3-week review...",
            "tags": ["target-cpa-review"]
        }
        # ... more children
    ]
)
```

**Benefits**:
- Parent task automatically calculates total time from all children
- Children linked to parent via `parent_id`
- Parent tracks all children via `children` array
- Daily briefing shows only due children (not parent)

**Example**: NMA 3-Week Improvement Plan (Nov 17, 2025)
- 1 parent task (due Dec 8)
- 13 child tasks (due various dates in Nov-Dec)
- Total time: 1,185 minutes (19.75 hours) auto-calculated
- Child tasks organized by week (Week 1, Week 2, Week 3)

## Querying Tasks

### Get Active Tasks

```python
# All active tasks across all clients
all_tasks = service.get_active_tasks()

# Filter by client
superspace = service.get_active_tasks(client="superspace")

# Filter by priority
urgent = service.get_active_tasks(priority="P0")

# Exclude children (show only parents and standalone)
top_level = service.get_active_tasks(include_children=False)

# Combine filters
nma_p1 = service.get_active_tasks(
    client="national-motorsports-academy",
    priority="P1"
)

# Due before date
overdue = service.get_active_tasks(
    due_before="2025-11-18"
)

# Filter by tags
experiments = service.get_active_tasks(
    tags=["nma-improvement-plan"]
)
```

### Get Upcoming/Overdue

```python
# Next 7 days
upcoming = service.get_upcoming_tasks(days=7)

# Overdue tasks
overdue = service.get_overdue_tasks()
```

### Get Specific Task

```python
# Get task by ID (need to know client)
task = service.get_task(task_id, client="superspace")

# Search across all clients
task = service.get_task_any_client(task_id)
```

### Get Statistics

```python
stats = service.get_stats()

# Returns:
{
    'total_tasks': 45,
    'active_tasks': 39,
    'completed_tasks': 6,
    'priority_counts': {'P0': 5, 'P1': 12, 'P2': 18, 'P3': 4},
    'client_counts': {
        'superspace': 8,
        'national-motorsports-academy': 14,
        'smythson': 6,
        # ...
    },
    'overdue_count': 2,
    'clients_with_tasks': 16
}
```

## Daily Briefing Integration

The daily briefing (`agents/daily-intel-report/daily-intel-report.py`) automatically reads from per-client files:

```python
# In daily-intel-report.py
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()
upcoming_tasks = service.get_upcoming_tasks(days=7)

# Filter logic for briefing:
# - Show child tasks due today (NOT parent tasks)
# - Show standalone tasks due in next 7 days
# - Group by client and priority
# - Pre-verify eligible tasks
```

**No code changes needed** - service API remained compatible during migration.

### How Child Tasks Appear

**Parent task** (due Dec 8):
- NOT shown in daily briefing until Dec 8

**Child tasks** (various due dates):
- Shown on their individual due dates
- Labeled with source: "Part of 3-Week Improvement Plan"
- Full notes from child task displayed

This prevents parent "container" tasks from cluttering the briefing.

## Creating Tasks

### Standalone Task (Simple)

```python
task = service.create_task(
    title="[Client] Task description",
    client="client-slug",
    priority="P1",
    due_date="2025-11-20",
    time_estimate_mins=45,
    notes="Context...",
    source="Email",
    tags=["tag1"],
    task_type="standalone"
)
```

### Parent Task with Children (Meetings/Projects)

**Use when**:
- Multiple tasks from same meeting
- Multi-phase project with steps
- Related tasks that should be grouped

**Example**: Meeting with client resulted in 5 action items

```python
parent = service.create_parent_with_children(
    parent_title="[Client] Q4 Strategy Implementation",
    client="client-slug",
    parent_due_date="2025-12-31",
    parent_notes="Based on Q4 strategy meeting Nov 15...",
    parent_source="Meeting (Nov 15, 2025)",
    parent_priority="P1",
    children_data=[
        {
            "title": "[Client] Week 1: Budget analysis",
            "due_date": "2025-11-22",
            "time_estimate_mins": 60,
            "priority": "P1"
        },
        {
            "title": "[Client] Week 2: Campaign restructure",
            "due_date": "2025-11-29",
            "time_estimate_mins": 120,
            "priority": "P1"
        }
        # ... more children
    ]
)
```

## Task Lifecycle

### 1. Creation
- Task created via service → Saved to `clients/{client}/tasks.json`
- Gets UUID, timestamps, normalized client slug
- Parent tasks get empty `children: []` array
- Child tasks get `parent_id` reference

### 2. Active Management
- Daily briefing shows upcoming tasks (next 7 days)
- Child tasks shown individually on their due dates
- Parent tasks shown only when parent itself is due
- Tasks grouped by priority (P0/P1/P2/P3)

### 3. Completion
- Mark complete → Status changed to 'completed'
- Logged to `clients/{client}/tasks-completed.md`
- Completion timestamp recorded
- Task remains in file (not deleted)

### 4. Archival
- Completed tasks >30 days old can be deleted
- Permanent record remains in tasks-completed.md
- Manual cleanup or automated archival script

## Priority System

| Priority | Meaning | Briefing Behavior |
|----------|---------|-------------------|
| **P0** | Critical/Urgent | Show immediately, red flag |
| **P1** | High priority | Show in next 7 days |
| **P2** | Normal | Show in next 7 days |
| **P3** | Low | Show only if due within 3 days |

## Migration from Global File

Tasks were migrated on 2025-11-18 using:

```bash
python3 shared/scripts/migrate_to_perclient_tasks.py --live
```

**Results**:
- 39 tasks migrated from `data/state/client-tasks.json`
- 16 per-client files created
- All metadata preserved (tags, notes, context)
- Backup created: `data/state/client-tasks.json.backup`
- Migration metadata added to each file

**Example migration metadata**:
```json
{
  "tasks": [...],
  "last_updated": "2025-11-18T10:09:54.578293",
  "migrated_from_global": "2025-11-18T10:07:43.781943"
}
```

### NMA Restructure (Example)

During migration, NMA tasks were restructured from 13 standalone tasks to parent/child hierarchy:

**Before**:
- 13 separate tasks (all standalone)
- No grouping or relationship
- All appear in daily briefing

**After**:
- 1 parent task (3-Week Improvement Plan)
- 13 child tasks (Week 1-3 items)
- Only due children appear in briefing

This demonstrates the power of parent/child for organizing meeting outcomes.

## Best Practices

### For AI Agents

1. **Use ClientTasksService** for all task operations
2. **Specify task type** when creating (`parent`, `child`, or `standalone`)
3. **Use parent/child** for meetings with multiple action items
4. **Set realistic due dates** (don't default to "today")
5. **Include time estimates** when possible
6. **Add source** (e.g., "Meeting (Nov 17)", "Email from client")
7. **Normalize client name** to slug (lowercase, hyphens)

### For Task Creation

**Use standalone when**:
- Single independent task
- No relationship to other tasks
- Quick one-off action

**Use parent/child when**:
- Meeting produced 3+ action items
- Multi-week project with phases
- Related tasks from same initiative
- Want to track overall project completion

**Title format**:
- Start with `[Client Name]` for clarity
- Be specific: "[NMA] Week 1: Fix sitelinks" not "[NMA] Fix things"
- Include phase/week if part of series

**Notes**:
- Include full context (what, why, expected outcome)
- Reference source documents/meetings
- Add success criteria when relevant
- Note dependencies on other tasks

**Tags**:
- Use for grouping: `nma-improvement-plan`, `q4-strategy`
- Add topic tags: `sitelinks`, `campaign-creation`, `budget-review`
- Use for filtering: `quick-win`, `urgent`, `requires-client-approval`

## Troubleshooting

### "No tasks showing in briefing"

Check file exists and has active tasks:
```bash
cat clients/[client]/tasks.json | jq '.tasks[] | select(.status == "active")'
```

### "Task created but not in briefing"

Check due date is within next 7 days:
```python
service = ClientTasksService()
task = service.get_task(task_id, client="client-slug")
print(task['due_date'])  # Should be within next week
```

### "Can't find task across clients"

Use `get_task_any_client()`:
```python
task = service.get_task_any_client(task_id)
# Returns task with `_client` field added
```

### "Parent task showing in briefing early"

Parent tasks should only show on their due date. Check:
- Parent `due_date` is the final due date (e.g., Dec 8)
- Child tasks have earlier due dates (Nov 19-Dec 8)
- Briefing filtering logic excludes parents until due

## Files Reference

```
shared/
├── client_tasks_service.py              # Core service (669 lines)
└── scripts/
    └── migrate_to_perclient_tasks.py   # Migration script (120 lines)

clients/{client}/
└── tasks.json                           # Per-client task storage

agents/
└── daily-intel-report/
    └── daily-intel-report.py            # Uses ClientTasksService (line 295)

data/
└── state/
    └── client-tasks.json.backup         # Pre-migration backup
```

## Future Enhancements

Potential improvements:
- **Recurring tasks**: Weekly/monthly repeating tasks
- **Task templates**: Common task patterns (campaign launch, monthly review)
- **Subtask levels**: Child tasks with their own children (3+ levels)
- **Dependencies**: Task X blocks task Y
- **Web UI**: Simple web interface for task management
- **Mobile access**: PWA for mobile task viewing
- **Notifications**: Email/Slack when P0 tasks created
- **Auto-archival**: LaunchAgent to clean up old completed tasks

## Critical Incident: November 23, 2025 Task Loss

### What Happened

On November 23, 2025, between 14:01 and 19:01, **78 tasks disappeared** from 7 client tasks.json files:

| Client | Tasks Lost | Status |
|--------|-----------|---------|
| go-glean | 3 tasks | ✅ Restored from backup |
| godshot | 3 tasks | ✅ Restored from backup |
| just-bin-bags | 1 task | ✅ Restored from backup |
| superspace | 4 tasks | ✅ Restored from backup |
| national-design-academy | 15 tasks | ✅ Extracted from CONTEXT.md |
| positive-bakes | 7 tasks | ✅ Extracted from CONTEXT.md |
| tree2mydoor | 5 tasks | ✅ Restored manually |

**Total**: 78 tasks across 7 clients

### Timeline

- **Nov 23 09:00-14:01**: Tasks exist (hourly backup shows 17 clients with tasks.json files)
- **Nov 23 14:08**: `task-manager` skill modified
- **Nov 23 14:20**: `task-manager` skill modified again
- **Nov 23 19:01**: Tasks gone (hourly backup shows 0 clients with tasks.json files)

### Root Cause

**Unknown script or modification** during task-manager skill update. The exact cause was never determined, but circumstantial evidence points to:

1. Task-manager skill being modified during the exact window of data loss
2. Possible test or migration script that cleared files
3. Synchronization operation that incorrectly removed local files

### Recovery

All 78 tasks were successfully restored:

1. **Backup restoration** (11 tasks from 4 clients): Used Nov 23 09:00 backup (last known good state)
2. **CONTEXT.md extraction** (23 tasks from 2 clients): Tasks existed only in documentation, never had tasks.json
3. **Manual restoration** (5 tasks): Tree2mydoor tasks rebuilt from CONTEXT.md task list

**Backup system worked perfectly** - hourly backups enabled complete recovery with zero data loss.

### Preventions Implemented

#### 1. ClientTasksService Safety Blocks

Location: `shared/client_tasks_service.py`

**Safety mechanisms**:
- **Empty save block**: Refuses to save empty task array if file currently has tasks
- **Large reduction warning**: Warns if >50% of tasks removed in single operation (still allows but logs)
- **Atomic writes**: Write to temp file first, then atomic rename (prevents corruption if interrupted)
- **Audit logging**: All modifications logged to `data/state/tasks-audit.log`

Example of blocked operation:
```
⚠️  SAFETY BLOCK: Refusing to save empty tasks array to smythson/tasks.json
    File currently has 13 tasks
    This looks like accidental data loss. Aborting save.
```

#### 2. Backup Monitoring Agent

Location: `agents/monitoring/backup-task-monitor.py`

**Runs**: Daily at 9 AM via LaunchAgent

**Monitors**:
- Per-client task count changes (alerts on >50% loss)
- Total task count across all clients (alerts on >30% drop)
- Compares current state vs most recent backup

**Alerts**: Logged to `data/state/backup-alerts.log`

Example alert:
```
2025-11-26T09:00:00 | CRITICAL: smythson lost ALL 13 tasks
2025-11-26T09:00:00 | CRITICAL: Total task count dropped 45% (78 → 43)
```

#### 3. Audit Trail System

Location: `data/state/tasks-audit.log`

**Tracks every modification**:
```
2025-11-26T14:16:35 | tree2mydoor | SAVE | 0 → 5 | <module> (restore_tasks.py)
2025-11-26T14:18:22 | smythson | LARGE_REDUCTION | 13 → 6 | complete_task (client_tasks_service.py)
2025-11-26T14:20:15 | go-glean | BLOCKED_EMPTY_SAVE | 3 → 0 | _save_client_tasks (test_script.py)
```

**Columns**:
- Timestamp
- Client
- Action type (SAVE, BLOCKED_EMPTY_SAVE, LARGE_REDUCTION)
- Before/after task counts
- Calling function and script

### Lessons Learned

1. **Backups are critical** - Hourly backup system saved 78 tasks from permanent loss
2. **Multiple safety layers needed** - No single prevention is enough; defense in depth required
3. **Audit trails enable forensics** - Knowing what/when/who helps prevent recurrence
4. **CONTEXT.md as backup** - Tasks documented in CONTEXT.md were recoverable even without tasks.json
5. **Testing needs safeguards** - Unknown script/modification could have been prevented by safety blocks

### Future Improvements

Recommended (not yet implemented):

- [ ] Alert on backup file size drops >20% (earlier detection)
- [ ] Real-time monitoring of tasks.json modifications (not just daily)
- [ ] Weekly backup verification report
- [ ] Require explicit `force=True` flag to save empty task arrays
- [ ] Git tracking of task file changes (version control layer)

## Related Documentation

- `CLAUDE.md` - Main development guide (Task Management section, includes incident summary)
- `docs/AUTOMATION.md` - Daily briefing workflow
- `clients/_templates/CONTEXT.md` - Client folder standards
- `roksys/spreadsheets/rok-experiments-client-notes.csv` - Strategic changes log
