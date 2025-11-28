# Task System Decision Guide

**Last Updated:** 2025-11-19
**Status:** ✅ Active - Authoritative Reference

---

## Overview

PetesBrain uses **TWO SEPARATE TASK SYSTEMS** that do not sync with each other:

1. **Internal Client Task System** - `clients/{client}/tasks.json`
2. **Google Tasks** - External API (Google Tasks lists)

**They are completely independent.** A task in one system will NOT appear in the other.

---

## Quick Decision Tree

```
Is this task related to client work?
    ↓ YES
Does it need to recur (weekly, monthly, etc.)?
    ↓ YES
    → Use INTERNAL SYSTEM (clients/{client}/tasks.json)

    ↓ NO (one-time task)
Does it have multiple related sub-tasks (meeting action items, project phases)?
    ↓ YES
    → Use INTERNAL SYSTEM (parent/child hierarchy)

    ↓ NO (simple one-time task)
    → Use INTERNAL SYSTEM (preferred for client work)

↓ NO (personal task, not client-related)
→ Use GOOGLE TASKS ("Peter's List")
```

---

## System 1: Internal Client Task System

### What It Is

- **Storage:** Per-client JSON files at `clients/{client}/tasks.json`
- **Service:** `shared/client_tasks_service.py`
- **Purpose:** Managing all client-related work
- **Daily Briefing:** Shows tasks automatically

### When to Use

✅ **ALWAYS use for:**
- **Client work** (any task related to a specific client)
- **Recurring tasks** (weekly reviews, monthly reports, scheduled check-ins)
- **Multi-step projects** (parent task with multiple child tasks)
- **Meeting action items** (group related tasks from same meeting)
- **Strategic initiatives** (campaigns, audits, multi-week plans)

### Features

- ✅ **Recurring tasks** - Weekly, monthly, custom schedules
- ✅ **Parent/child hierarchies** - Group related tasks
- ✅ **Per-client organization** - Each client has own file
- ✅ **Rich metadata** - Tags, time estimates, priorities, notes
- ✅ **Automatic briefing** - Shows in daily intel report
- ✅ **Completion tracking** - Auto-logs to `tasks-completed.md`

### Task Types

**Standalone Task:**
```python
service.create_task(
    title="[Client] Review campaign performance",
    client="client-slug",
    priority="P1",
    due_date="2025-11-25",
    task_type="standalone"
)
```

**Recurring Task:**
```python
service.create_task(
    title="[Client] Weekly budget review",
    client="client-slug",
    priority="P1",
    recurrence="weekly",  # weekly, monthly, custom
    task_type="standalone"
)
```

**Parent with Children:**
```python
service.create_parent_with_children(
    parent_title="[Client] Q4 Campaign Launch",
    client="client-slug",
    parent_due_date="2025-12-31",
    children_data=[
        {"title": "[Client] Week 1: Setup", "due_date": "2025-12-08"},
        {"title": "[Client] Week 2: Testing", "due_date": "2025-12-15"},
        {"title": "[Client] Week 3: Launch", "due_date": "2025-12-22"}
    ]
)
```

### Examples

✅ "[Devonshire] Weekly Thursday budget and ROAS review" (recurring)
✅ "[Smythson] Q4 Christmas campaign analysis" (one-time)
✅ "[Superspace] 3-week improvement plan" (parent with 13 children)
✅ "[NMA] Fix disapproved sitelinks" (standalone from meeting)

---

## System 2: Google Tasks

### What It Is

- **Storage:** Google Tasks API (cloud)
- **Lists:** "Peter's List" (personal), "Client Work" (AI-generated)
- **Purpose:** Personal reminders and AI-suggested client work
- **Monitoring:** Synced every 6 hours by `agents/system/tasks-monitor.py`

### When to Use

✅ **Use for:**
- **Personal tasks** (not client-related)
- **Quick reminders** (one-time personal to-dos)
- **AI-generated client work** (automated daily suggestions - "Client Work" list)

❌ **DO NOT use for:**
- ❌ Client work you're manually creating
- ❌ Recurring tasks (no API support)
- ❌ Multi-step projects (no hierarchy support)
- ❌ Strategic client initiatives

### Features

- ✅ **Cross-device sync** - Available on phone, web, desktop
- ✅ **Google Calendar integration** - Shows in calendar
- ✅ **Simple interface** - Quick mobile capture
- ❌ **No recurring tasks** (would need manual recreation)
- ❌ **No parent/child hierarchy**
- ❌ **No per-client organization**

### Task Lists

**"Peter's List":**
- Personal tasks (grocery shopping, appointments, etc.)
- Created manually via Google Tasks app/web

**"Client Work":**
- AI-generated daily suggestions
- Created automatically by `daily-client-work-generator.py`
- DO NOT manually create client tasks here

### Examples

✅ "Book dentist appointment" (personal)
✅ "Order new laptop charger" (personal)
✅ "Review quarterly taxes" (personal)
✅ "[Superspace] Review demand gen performance" (AI-generated, appears automatically)

❌ "[Devonshire] Weekly budget review" (recurring - use internal system)
❌ "[Smythson] Launch Christmas campaigns" (client work - use internal system)

---

## Key Differences at a Glance

| Feature | Internal System | Google Tasks |
|---------|----------------|--------------|
| **Storage** | Per-client JSON files | Google cloud API |
| **Purpose** | Client work management | Personal tasks + AI suggestions |
| **Recurring tasks** | ✅ YES | ❌ NO |
| **Parent/child** | ✅ YES | ❌ NO |
| **Client organization** | ✅ Per-client files | ❌ All in one list |
| **Daily briefing** | ✅ Automatic | ✅ Automatic |
| **Completion tracking** | ✅ Auto-logs to tasks-completed.md | ✅ Via tasks-monitor.py |
| **Mobile access** | ❌ NO | ✅ YES (Google Tasks app) |
| **Cross-device sync** | ❌ NO | ✅ YES |
| **Best for** | Client work, projects, recurring | Personal tasks, quick reminders |

---

## Common Scenarios

### Scenario: Weekly Client Review

**Task:** Review Devonshire budget and ROAS every Thursday

**Decision:** ✅ **Internal System (recurring task)**

**Why:**
- Client-related work
- Needs to recur weekly
- Google Tasks doesn't support recurring via API

**Implementation:**
```python
service.create_task(
    title="[Devonshire] Weekly Thursday budget and ROAS review",
    client="devonshire-hotels",
    priority="P1",
    recurrence="weekly",
    recurrence_day="thursday",
    notes="Check ROAS maintained, revenue growth, budget pacing"
)
```

---

### Scenario: Meeting with 5 Action Items

**Task:** Client meeting resulted in 5 follow-up tasks

**Decision:** ✅ **Internal System (parent/child)**

**Why:**
- Client-related work
- Related tasks from same source
- Want to group them together
- Track overall completion

**Implementation:**
```python
service.create_parent_with_children(
    parent_title="[Client] Nov 19 Meeting Action Items",
    client="client-slug",
    parent_due_date="2025-12-01",
    children_data=[
        {"title": "[Client] Action 1", "due_date": "2025-11-22"},
        {"title": "[Client] Action 2", "due_date": "2025-11-25"},
        # ... 3 more
    ]
)
```

---

### Scenario: One-Time Client Analysis

**Task:** Analyze Black Friday campaign performance for Smythson

**Decision:** ✅ **Internal System (standalone)**

**Why:**
- Client-related work
- One-time analysis
- Want it logged to tasks-completed.md when done
- Want it in client's task file

**Implementation:**
```python
service.create_task(
    title="[Smythson] Analyze Black Friday campaign performance",
    client="smythson",
    priority="P1",
    due_date="2025-12-02",
    time_estimate_mins=120,
    task_type="standalone"
)
```

---

### Scenario: Personal Reminder

**Task:** Remember to book dental checkup

**Decision:** ✅ **Google Tasks ("Peter's List")**

**Why:**
- NOT client-related
- Personal task
- Want it on phone/calendar
- Simple reminder

**Implementation:**
- Use Google Tasks app/web interface
- OR use MCP tool:
```python
mcp__google-tasks__create_task(
    tasklist_id="MTY1OTUzNzc4MjgxMDM5NTQwMDY6MDow",  # Peter's List
    title="Book dental checkup",
    due="2025-11-30"
)
```

---

### Scenario: AI Suggests Client Task

**Task:** Daily AI generator suggests reviewing Superspace performance

**Decision:** ✅ **Google Tasks ("Client Work" list) - AUTOMATIC**

**Why:**
- AI-generated suggestion
- Created automatically by daily-client-work-generator.py
- Shows in daily briefing
- User can complete or ignore

**Implementation:**
- Automatic - no manual creation needed
- AI system handles this

---

## Decision Rules Summary

### Use Internal System When:

1. ✅ Task is client-related
2. ✅ Task needs to recur (weekly, monthly, etc.)
3. ✅ Task has multiple sub-tasks (meeting outcomes, project phases)
4. ✅ Task is part of strategic initiative
5. ✅ You want parent/child hierarchy
6. ✅ You want automatic logging to tasks-completed.md

### Use Google Tasks When:

1. ✅ Task is personal (not client work)
2. ✅ Task is quick reminder
3. ✅ You want mobile/calendar sync
4. ✅ AI generated it automatically (don't manually create in "Client Work")

### NEVER:

1. ❌ Create recurring tasks in Google Tasks (no API support)
2. ❌ Create client work tasks in Google Tasks manually (use internal system)
3. ❌ Mix systems for same logical task (creates duplicates)
4. ❌ Create personal tasks in internal system (wrong tool)

---

## For Claude Code: Implementation Guide

### Before Creating Any Task

**Ask yourself:**

1. **Is this client work?**
   - YES → Internal system
   - NO → Google Tasks

2. **Does it recur?**
   - YES → MUST use internal system
   - NO → Continue...

3. **Multiple related sub-tasks?**
   - YES → Internal system (parent/child)
   - NO → Continue...

4. **Is this a personal reminder?**
   - YES → Google Tasks
   - NO → Internal system (default for client work)

### Code Examples

**Internal System (Client Work):**
```python
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()

# Standalone
task = service.create_task(
    title="[Client] Task description",
    client="client-slug",
    priority="P1",
    due_date="2025-11-25",
    task_type="standalone"
)

# Recurring
task = service.create_task(
    title="[Client] Weekly review",
    client="client-slug",
    priority="P1",
    recurrence="weekly",
    task_type="standalone"
)

# Parent/Child
parent = service.create_parent_with_children(
    parent_title="[Client] Project",
    client="client-slug",
    children_data=[...]
)
```

**Google Tasks (Personal):**
```python
# Use MCP tool
mcp__google-tasks__create_task(
    tasklist_id="MTY1OTUzNzc4MjgxMDM5NTQwMDY6MDow",  # Peter's List
    title="Personal reminder",
    due="2025-11-30"
)
```

### Error Prevention

**If you're about to create a task, STOP and check:**

- [ ] Have I determined if this is client work or personal?
- [ ] Does this need to recur? (If yes, MUST use internal system)
- [ ] Am I about to create the same task in both systems? (WRONG - pick one)
- [ ] Am I manually creating in "Client Work" list? (WRONG - that's for AI only)

---

## Migration Notes

**November 18, 2025:**
- Internal system migrated from global file to per-client files
- 39 tasks migrated across 16 clients
- Recurring task support added to internal system

**November 19, 2025:**
- This decision guide created to clarify system usage
- Documented: Recurring tasks CANNOT go in Google Tasks
- Established: Client work belongs in internal system

---

## Troubleshooting

### "I created a task but don't see it in the daily briefing"

**Check:**
1. Which system did you use?
   - Internal: Should appear automatically
   - Google Tasks: Only appears if in "Peter's List" or "Client Work" and due within 7 days

2. Is due date set?
   - Must have due date within next 7 days to appear

3. Is it a parent task?
   - Parent tasks only appear on their own due date (children appear on child due dates)

### "I see duplicate tasks"

**Cause:** Same task created in both systems

**Fix:**
1. Delete from one system (usually Google Tasks)
2. Use decision tree above to determine correct system
3. Keep only in correct system

### "Recurring task disappeared"

**Check:**
1. Which system?
   - Internal: Check `clients/{client}/tasks.json`
   - Google Tasks: Recurring not supported - task would need manual recreation

2. Was it in Google Tasks?
   - If yes, that's the problem - move to internal system

---

## Related Documentation

- `docs/INTERNAL-TASK-SYSTEM.md` - Internal system architecture
- `docs/TASK-INTEGRATION-ARCHITECTURE.md` - Google Tasks integration
- `shared/TASK-SYSTEM-SAFETY-RULES.md` - Safety protocols
- `docs/CLAUDE.md` - Main development guide

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│          TASK SYSTEM DECISION GUIDE                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CLIENT WORK?           → Internal System               │
│  RECURRING?             → Internal System (REQUIRED)    │
│  MULTIPLE SUB-TASKS?    → Internal System (parent/child)│
│  PERSONAL REMINDER?     → Google Tasks (Peter's List)   │
│  AI GENERATED?          → Google Tasks (auto-created)   │
│                                                         │
│  DEFAULT FOR CLIENT WORK: Internal System               │
│  DEFAULT FOR PERSONAL:    Google Tasks                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

**Last Updated:** 2025-11-19
**Author:** Claude Code + Peter Empson
**Status:** ✅ Authoritative Reference
