# Task Creation Quick Reference
**Created:** 2025-11-19
**Status:** ✅ Active - Quick Decision Guide

---

## 🚨 STOP BEFORE CREATING ANY TASK

Ask yourself ONE question:

**"Am I manually creating a client work task?"**

- **YES** → Use **Internal System** (`clients/{client}/tasks.json`)
- **NO** (it's personal) → Use **Google Tasks** ("Peter's List")

---

## The Simple Rules

### ✅ Internal System (`clients/{client}/tasks.json`)

**Use for ALL manually created client work:**
- Weekly reports
- Campaign audits
- Client communications
- Analysis tasks
- Strategic initiatives
- Meeting action items
- **ANYTHING client-related you're creating manually**

**How to create:**
```python
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()

service.create_task(
    title="[Godshot] Verify WooCommerce conversion tracking",
    client="godshot",
    priority="P1",
    due_date="2025-11-20",
    source="Weekly Report",
    task_type="standalone"
)
```

---

### ✅ Google Tasks "Client Work" List

**ONLY for AI-generated suggestions:**
- Created automatically by `daily-client-work-generator.py`
- You should **NEVER** manually create tasks here
- These are suggestions you can action or ignore

**If you see:**
```
**Source:** AI Generated (2025-11-11 09:29)
```
→ That's correct, leave it there

---

### ✅ Google Tasks "Peter's List"

**Use for personal tasks:**
- Dentist appointments
- Personal errands
- Non-work reminders

**How to create:**
```python
mcp__google-tasks__create_task(
    tasklist_id="MTY1OTUzNzc4MjgxMDM5NTQwMDY6MDow",
    title="Book dentist",
    due="2025-11-30"
)
```

---

## ❌ Common Mistakes

| ❌ WRONG | ✅ CORRECT |
|----------|-----------|
| Create "[Godshot] run weekly report" in Google Tasks manually | Create in `clients/godshot/tasks.json` |
| Create recurring task in Google Tasks | Create in internal system (Google Tasks has no recurring support) |
| Create meeting action items in Google Tasks | Create parent/child in internal system |
| Quick voice note → Google Tasks | If client work → move to internal system after capture |

---

## Quick Decision Tree

```
┌─────────────────────────────────────┐
│ Am I creating this task manually?   │
└──────────────┬──────────────────────┘
               │
               ▼
     ┌─────────────────┐
     │ Is it client    │
     │ work?           │
     └────┬────────────┘
          │
     YES  │  NO
     ▼    │   ▼
  Internal│  Google Tasks
  System  │  "Peter's List"
          │
          │  ┌──────────────────────┐
          └─►│ It's AI-generated?   │
             │ Leave in "Client     │
             │ Work" list           │
             └──────────────────────┘
```

---

## When You See Client Work in Google Tasks

**If you notice a manually created client work task in Google Tasks:**

1. **Create it properly in internal system**
   ```python
   service.create_task(
       title="[Client] Task title",
       client="client-slug",
       ...
   )
   ```

2. **Delete from Google Tasks**
   ```python
   mcp__google-tasks__delete_task(
       tasklist_id="aEpKT1Blc1JsMXdvcDliXw",
       task_id="task-id"
   )
   ```

3. **Note for future:** Always check before creating

---

## Why This Matters

**Internal System Benefits:**
- ✅ Appears in daily briefing automatically
- ✅ Logged to `tasks-completed.md` when done
- ✅ Per-client organization
- ✅ Supports recurring tasks
- ✅ Supports parent/child hierarchy
- ✅ Rich metadata (time estimates, tags, priorities)

**Google Tasks Problems for Client Work:**
- ❌ No recurring support
- ❌ No hierarchy
- ❌ No per-client organization
- ❌ Manual completion logging required
- ❌ Clutters "Client Work" list (should be AI-only)

---

## Authoritative References

- **Full decision guide:** `docs/TASK-SYSTEM-DECISION-GUIDE.md`
- **Internal system docs:** `docs/INTERNAL-TASK-SYSTEM.md`
- **Safety protocols:** `shared/TASK-SYSTEM-SAFETY-RULES.md`

---

**Remember:** When in doubt, use the Internal System for client work.
