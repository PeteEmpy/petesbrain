# PetesBrain Task System - Complete Guide

**Last Updated**: 2025-11-26
**Version**: 2.0 (Post-Migration)

> **Purpose**: This is the SINGLE SOURCE OF TRUTH for the PetesBrain task system. If you're confused about tasks, start here.

---

## Table of Contents

1. [Overview](#overview)
2. [The Two Task Systems](#the-two-task-systems)
3. [File Structure (Critical)](#file-structure-critical)
4. [Core Components](#core-components)
5. [Common Operations](#common-operations)
6. [Scripts Reference](#scripts-reference)
7. [Troubleshooting](#troubleshooting)
8. [Validation & Prevention](#validation--prevention)
9. [Migration History](#migration-history)

---

## Overview

PetesBrain uses **two separate, non-syncing task systems**:

1. **Internal Task System** - Client work tasks stored in JSON files
2. **Google Tasks** - Personal tasks and AI suggestions via Google Tasks API

**CRITICAL**: These DO NOT sync with each other. They are completely independent.

---

## The Two Task Systems

### System 1: Internal Tasks (Primary for Client Work)

**Storage**: `clients/{client}/tasks.json`
**Purpose**: ALL client work, recurring tasks, multi-step projects
**Managed by**: `ClientTasksService` (`shared/client_tasks_service.py`)

**When to use**:
- ✅ Any client work (Google Ads, campaigns, audits, etc.)
- ✅ Recurring tasks (Google Tasks API doesn't support recurrence)
- ✅ Multi-step projects with parent/child relationships
- ✅ Tasks that need verification context (Google Ads settings, etc.)

**When NOT to use**:
- ❌ Personal reminders (use Google Tasks)
- ❌ AI-generated suggestions (use Google Tasks)

---

### System 2: Google Tasks (Personal & Suggestions)

**Storage**: Google Tasks API (lists: "Peter's List", "Client Work", etc.)
**Purpose**: Personal reminders, AI-generated task suggestions
**Managed by**: `google-tasks-mcp-server`

**When to use**:
- ✅ Personal reminders
- ✅ AI-generated task suggestions
- ✅ Quick one-off tasks

**When NOT to use**:
- ❌ Client work (always use internal system)
- ❌ Recurring tasks (API doesn't support)
- ❌ Tasks that need structured data/context

---

## File Structure (Critical)

### ✅ CORRECT Structure

```
clients/
├── {client}/
│   ├── tasks.json              ← PRIMARY: All client tasks go here
│   ├── tasks-completed.md      ← Archive of completed tasks
│   ├── CONTEXT.md              ← Client context
│   ├── audits/
│   ├── emails/
│   ├── reports/
│   └── scripts/
```

### ❌ WRONG Structure (Historical Issue - Fixed 2025-11-26)

```
clients/
├── {client}/
│   └── product-feeds/
│       └── tasks.json          ← NEVER PUT TASKS HERE
```

**Why this was wrong**: Product feeds are for e-commerce product data, not task management.

**What happened**: Scripts checked this location first, so tasks accumulated there incorrectly.

**Fixed on**: 2025-11-26 - All tasks migrated to root, all scripts updated.

---

## Core Components

### 1. ClientTasksService (The Authority)

**File**: `shared/client_tasks_service.py`
**Purpose**: Authoritative service for ALL internal task operations

**Key Methods**:
```python
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()

# Create task
task = service.create_task(
    title='[Client] Do something',
    client='client-slug',
    priority='P0',  # P0=urgent, P1=high, P2=normal, P3=low
    due_date='2025-12-01',
    notes='Additional context',
    tags=['optimization', 'urgent']
)

# Get tasks
active = service.get_active_tasks(client='client-slug')
p0_tasks = service.get_active_tasks(priority='P0')

# Complete task
service.complete_task(task_id, client='client-slug',
                     completion_notes='What was done')

# Get stats
stats = service.get_stats()
```

**IMPORTANT**: This service ONLY looks at `clients/{client}/tasks.json`. It never checks product-feeds.

---

### 2. Task JSON Structure

**File**: `clients/{client}/tasks.json`

```json
{
  "tasks": [
    {
      "id": "uuid-here",
      "title": "[Client] Task title",
      "type": "standalone",  // or "parent" or "child"
      "parent_id": null,     // Only set if type="child"
      "children": [],        // Only set if type="parent"
      "priority": "P0",      // P0, P1, P2, P3
      "due_date": "2025-12-01",
      "time_estimate_mins": 60,
      "notes": "Task details and context",
      "source": "Weekly Report",
      "tags": ["optimization", "urgent"],
      "context": {},         // Structured data (Google Ads IDs, etc.)
      "status": "active",    // "active" or "completed"
      "created_at": "2025-11-26T10:00:00",
      "updated_at": "2025-11-26T10:00:00",
      "completed_at": null
    }
  ],
  "last_updated": "2025-11-26T10:00:00"
}
```

**Task Types**:
- `standalone`: Independent task
- `parent`: Container for multiple child tasks
- `child`: Subtask of a parent (has `parent_id`)

**Priority Levels**:
- `P0`: Urgent - overdue or due within 0-2 days (needs immediate attention)
- `P1`: High - due in 3-14 days (this week/next week)
- `P2`: Normal - due in 15-30 days (this month)
- `P3`: Low - due in 31+ days (when you get to it)

**Important**: "Days until due" is calculated as full 24-hour periods. A task due Friday at 2pm Tuesday is calculated as "2 days" (2.4 days rounds down), so it becomes P0.

---

### 3. Completed Tasks Archive

**File**: `clients/{client}/tasks-completed.md`

**Format**:
```markdown
## [Client] Task Title
**Completed:** 2025-11-26 14:30
**Source:** Weekly Report

Notes about what was done...

---
```

**Important**:
- Tasks are REMOVED from tasks.json when completed
- They are logged to tasks-completed.md (append-only)
- This keeps tasks.json small and fast
- Search completed tasks with grep/search tools

---

## Common Operations

### Creating a New Client

```bash
# 1. Create client directory
mkdir -p clients/new-client

# 2. Create CONTEXT.md
cat > clients/new-client/CONTEXT.md << 'EOF'
# New Client - Context & Strategic Notes

**Voice Transcription Aliases**: new client, newclient, new-client

## Platform IDs
- **Google Ads Customer ID**: 1234567890
- **GA4 Property ID**: [TBD]

EOF

# 3. Create initial tasks.json
cat > clients/new-client/tasks.json << 'EOF'
{
  "tasks": [],
  "last_updated": "2025-11-26T10:00:00"
}
EOF

# 4. Create tasks-completed.md
touch clients/new-client/tasks-completed.md

# 5. Create standard folders
mkdir -p clients/new-client/{audits,briefs,documents,emails,meeting-notes,presentations,reports,scripts,spreadsheets}
```

**CRITICAL**: Do NOT create a `product-feeds/` folder unless the client is e-commerce and needs product feed management.

---

### Adding a Task Manually (Python)

```python
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()

task = service.create_task(
    title='[Smythson] Review Black Friday performance',
    client='smythson',
    priority='P1',
    due_date='2025-12-02',
    time_estimate_mins=120,
    notes='Check final ROAS and budget performance vs targets',
    source='Manual',
    tags=['black-friday', 'retrospective']
)

print(f"Created task: {task['id']}")
```

---

### Adding a Task via Command Line (JSON)

```bash
# For quick additions, directly edit tasks.json
python3 << 'EOF'
import json
from pathlib import Path
from datetime import datetime
import uuid

client = 'smythson'
task_file = Path(f'clients/{client}/tasks.json')

with open(task_file) as f:
    data = json.load(f)

data['tasks'].append({
    'id': str(uuid.uuid4()),
    'title': f'[{client.replace("-", " ").title()}] Task title here',
    'type': 'standalone',
    'parent_id': None,
    'children': None,
    'priority': 'P2',
    'due_date': '2025-12-01',
    'time_estimate_mins': 60,
    'notes': 'Task notes',
    'source': 'Manual',
    'tags': [],
    'context': {},
    'status': 'active',
    'created_at': datetime.now().isoformat(),
    'updated_at': datetime.now().isoformat(),
    'completed_at': None
})

data['last_updated'] = datetime.now().isoformat()

with open(task_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Added task to {task_file}")
EOF
```

---

### Completing a Task

```python
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()

service.complete_task(
    task_id='uuid-here',
    client='smythson',
    completion_notes='Reviewed performance. ROAS was 515%, exceeding 400% target.'
)

# This will:
# 1. Remove task from clients/smythson/tasks.json
# 2. Log to clients/smythson/tasks-completed.md
# 3. Regenerate tasks overview HTML
```

---

### Viewing Tasks

**Option 1: Task Manager (Best)**
```bash
open /Users/administrator/Documents/PetesBrain/tasks-overview.html
# Or priority view:
open /Users/administrator/Documents/PetesBrain/tasks-overview-priority.html
```

**Option 2: Command Line**
```bash
# All tasks for a client
python3 -c "
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()
tasks = service.get_active_tasks(client='smythson')
for t in tasks:
    print(f\"[{t['priority']}] {t['title']}\")
"

# All P0 tasks
python3 -c "
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()
tasks = service.get_active_tasks(priority='P0')
for t in tasks:
    print(f\"{t['_client']}: {t['title']}\")
"
```

**Option 3: Read JSON Directly**
```bash
cat clients/smythson/tasks.json | python3 -m json.tool
```

---

## Scripts Reference

### Critical Scripts (Use These)

#### 1. generate-all-task-views.py
**Purpose**: Generate all HTML task manager views (consolidated script)
**Run**: `python3 generate-all-task-views.py`
**Output**:
- `tasks-overview.html` (grouped by client)
- `tasks-overview-priority.html` (grouped by P0/P1/P2/P3)
- `tasks-manager.html` (Task Manager & Reminders view)

**When to run**:
- After adding/completing tasks manually
- Automatically runs after `ClientTasksService.complete_task()`

---

#### 2. shared/client_tasks_service.py
**Purpose**: Core task management service
**Usage**: Import and use programmatically (see examples above)
**NEVER**: Edit this file unless fixing a bug

---

#### 3. shared/complete_task.py
**Purpose**: Command-line task completion
**Usage**:
```bash
python3 shared/complete_task.py <task_id> <client> "Completion notes"
```

---

### Automated Scripts (Run via LaunchAgents)

#### 1. agents/tasks-backup/tasks-backup.py
**Purpose**: Daily backup of all tasks.json files
**Schedule**: Daily at 6am
**Backup location**: `backups/tasks/YYYY-MM-DD/`
**What it backs up**: All `clients/*/tasks.json` files

---

#### 2. agents/inbox-processor/inbox-processor.py
**Purpose**: Process emails and create tasks automatically
**Schedule**: Every 15 minutes
**What it does**: Scans Gmail, extracts tasks, creates them via ClientTasksService

---

#### 3. agents/task-priority-updater/task-priority-updater.py
**Purpose**: Update task priorities based on due dates
**Schedule**: Daily at 8am
**What it does**: Escalates tasks to P0 if due today, P1 if due this week

---

### Utility Scripts

#### 1. shared/scripts/cleanup-completed-tasks.py
**Purpose**: Remove old completed tasks from tasks.json
**Usage**: `python3 shared/scripts/cleanup-completed-tasks.py --dry-run`
**What it does**: Removes tasks marked "completed" older than 30 days

---

#### 2. shared/scripts/process-manual-task-notes.py
**Purpose**: Process manual task notes from Task Manager UI
**Usage**: Automatic when you add notes in Task Manager

---

## Troubleshooting

### Problem: Tasks not appearing in Task Manager

**Check 1: Is the tasks.json file in the right place?**
```bash
# Should be here:
ls clients/my-client/tasks.json

# NOT here:
ls clients/my-client/product-feeds/tasks.json  # ❌ WRONG
```

**Fix**: Move file to correct location
```bash
mv clients/my-client/product-feeds/tasks.json clients/my-client/tasks.json
```

---

**Check 2: Is the JSON valid?**
```bash
python3 -m json.tool clients/my-client/tasks.json
```

If error, fix JSON syntax.

---

**Check 3: Regenerate HTML**
```bash
python3 generate-all-task-views.py
```

---

### Problem: Tasks appearing twice

**Cause**: Task exists in BOTH root and product-feeds locations

**Check**:
```bash
find clients -name "tasks.json" | grep my-client
```

If you see TWO files, merge them:
```bash
python3 << 'EOF'
import json
from pathlib import Path

client = 'my-client'
root = Path(f'clients/{client}/tasks.json')
pf = Path(f'clients/{client}/product-feeds/tasks.json')

if root.exists() and pf.exists():
    with open(root) as f:
        root_data = json.load(f)
    with open(pf) as f:
        pf_data = json.load(f)

    # Merge
    root_data['tasks'].extend(pf_data['tasks'])

    with open(root, 'w') as f:
        json.dump(root_data, f, indent=2)

    # Remove duplicate
    pf.unlink()
    print(f"Merged {len(pf_data['tasks'])} tasks into root")
EOF
```

---

### Problem: Task completed but still showing

**Check 1: Was it completed via ClientTasksService?**
```python
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()

# This is correct:
service.complete_task(task_id, client='my-client', completion_notes='Done')

# This is NOT enough (just marks as completed, doesn't remove):
service.update_task(task_id, client='my-client', status='completed')
```

**Fix**: Use `complete_task()` instead of `update_task()`

---

**Check 2: Is it still in tasks.json?**
```bash
grep "task-title-here" clients/my-client/tasks.json
```

If found, manually remove it or complete via ClientTasksService.

---

### Problem: "Product feeds tasks" warning

**Symptom**: Script warns about `product-feeds/tasks.json`

**Cause**: Legacy tasks.json file still in product-feeds folder

**Fix**: Migrate to root
```bash
# If root doesn't exist, just move
mv clients/my-client/product-feeds/tasks.json clients/my-client/tasks.json

# If root exists, merge first (see "Tasks appearing twice" above)
```

---

### Problem: Tasks.json safety block

**Symptom**: "SAFETY BLOCK: Refusing to save empty tasks array"

**Cause**: ClientTasksService prevented accidental deletion of all tasks

**What to check**:
- Are you accidentally clearing the tasks array?
- Is your script reading the wrong file?

**Fix**: Review your code. This safety feature prevents data loss.

---

## Validation & Prevention

### Validation Script

Create this script to check task system health:

```python
#!/usr/bin/env python3
"""
Validate task system structure and flag issues.
Run: python3 validate-task-system.py
"""
import json
from pathlib import Path

def validate_task_system():
    issues = []
    clients_dir = Path('clients')

    for client_dir in sorted(clients_dir.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith('_'):
            continue

        client = client_dir.name

        # Check 1: Tasks in wrong location?
        pf_tasks = client_dir / 'product-feeds' / 'tasks.json'
        if pf_tasks.exists():
            issues.append(f"❌ {client}: Has product-feeds/tasks.json (should be in root)")

        # Check 2: Has root tasks.json?
        root_tasks = client_dir / 'tasks.json'
        if root_tasks.exists():
            # Check 3: Valid JSON?
            try:
                with open(root_tasks) as f:
                    data = json.load(f)

                # Check 4: Correct structure?
                if 'tasks' not in data:
                    issues.append(f"❌ {client}: tasks.json missing 'tasks' array")

                if 'last_updated' not in data:
                    issues.append(f"⚠️  {client}: tasks.json missing 'last_updated'")

                # Check 5: Task structure
                for task in data.get('tasks', []):
                    if 'id' not in task:
                        issues.append(f"❌ {client}: Task missing 'id'")
                    if 'status' not in task:
                        issues.append(f"⚠️  {client}: Task missing 'status'")

                    # Check for completed tasks still in file
                    if task.get('status') == 'completed':
                        issues.append(f"⚠️  {client}: Completed task still in tasks.json: {task.get('title', 'Unknown')[:50]}")

            except json.JSONDecodeError as e:
                issues.append(f"❌ {client}: Invalid JSON in tasks.json: {e}")

        # Check 6: Has tasks-completed.md?
        completed_md = client_dir / 'tasks-completed.md'
        if not completed_md.exists():
            issues.append(f"⚠️  {client}: Missing tasks-completed.md")

    # Print results
    if not issues:
        print("✅ Task system validation PASSED")
        print("   No issues found")
    else:
        print(f"❌ Task system validation FAILED")
        print(f"   Found {len(issues)} issues:\n")
        for issue in issues:
            print(f"   {issue}")
        return 1

    return 0

if __name__ == "__main__":
    exit(validate_task_system())
```

Save as: `scripts/validate-task-system.py`

**Run regularly**:
```bash
python3 scripts/validate-task-system.py
```

---

### Pre-commit Hook (Optional)

Prevent committing tasks to wrong locations:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Checking for tasks in product-feeds folders..."

# Check if any product-feeds/tasks.json files are being committed
if git diff --cached --name-only | grep -q "product-feeds/tasks.json"; then
    echo "❌ ERROR: Attempting to commit tasks.json in product-feeds folder"
    echo "   Tasks should only be in clients/{client}/tasks.json"
    echo "   Move the file to the correct location before committing"
    exit 1
fi

echo "✅ Task location check passed"
```

---

## Migration History

### 2025-11-26: The Great Migration

**Problem**: Tasks scattered across wrong locations (product-feeds folders)

**Solution**:
1. Backed up all 54 tasks
2. Migrated 11 clients from product-feeds to root
3. Updated 5 scripts to prioritize root location
4. Verified zero data loss

**Result**: All tasks now in correct locations, all scripts consistent

**Details**: See `/docs/MIGRATION-COMPLETE-2025-11-26.md`

---

### Pre-2025-11-26: The Dark Ages

**Issue**: Scripts checked product-feeds FIRST, calling it "primary"

**Why this happened**: Scripts were written to match actual file locations, not intended architecture

**Lesson**: Document architecture FIRST, then implement. Don't let implementation drift from design.

---

## Quick Reference Card

### Where Do Tasks Go?
```
✅ clients/{client}/tasks.json        ← YES, always here
❌ clients/{client}/product-feeds/... ← NO, never here
❌ clients/tasks.json                  ← NO, this is different (main queue)
```

### How to Add a Task?
```python
# Best way (programmatic)
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()
service.create_task(title='[Client] Task', client='client-slug', ...)

# Quick way (manual)
# Edit clients/{client}/tasks.json directly
```

### How to Complete a Task?
```python
# Correct
service.complete_task(task_id, client, completion_notes='What I did')

# Wrong (doesn't remove from tasks.json)
service.update_task(task_id, client, status='completed')
```

### Where Are Completed Tasks?
```
clients/{client}/tasks-completed.md  ← Search here with grep
```

### Two Systems Don't Sync
```
Internal (tasks.json) ←→ ✗ ←→ Google Tasks
   (Use for client work)     (Use for personal)
```

---

## Need Help?

1. **Check this document first**
2. **Run validation**: `python3 scripts/validate-task-system.py`
3. **Check logs**: Look for errors in LaunchAgent logs
4. **Search completed tasks**: `grep -r "task title" clients/*/tasks-completed.md`
5. **Check backup**: `backups/tasks/` for recent backups

**Last resort**: Restore from backup (see Migration History section)

---

**Document Version**: 2.0
**Last Updated**: 2025-11-26
**Maintained By**: Claude Code
**Review Frequency**: After any structural changes to task system
