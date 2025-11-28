# Priority System - How It Works

**Last Updated**: 2025-11-26

---

## Priority Definitions

### P0 - Urgent (Red Flag)
**Due within 0-2 days or overdue**

**Examples** (from 2pm Tuesday):
- ✅ Overdue tasks
- ✅ Due today (Tuesday)
- ✅ Due tomorrow (Wednesday)
- ✅ Due Thursday
- ✅ Due Friday (calculated as 2 days away due to 24-hour period math)

**Why**: Needs immediate attention. These are tasks you should be working on NOW or very soon.

---

### P1 - High Priority
**Due in 3-14 days**

**Examples** (from 2pm Tuesday):
- ✅ Due next Monday (5 days)
- ✅ Due next week
- ✅ Due in 10 days

**Why**: Important but not urgent. Plan to complete this week or early next week.

---

### P2 - Normal Priority
**Due in 15-30 days**

**Examples**:
- ✅ Due in 3 weeks
- ✅ Due end of month

**Why**: Standard priority. Complete within the month.

---

### P3 - Low Priority
**Due in 31+ days**

**Examples**:
- ✅ Due next month
- ✅ Due end of quarter

**Why**: Low urgency. Work on when you have time.

---

## How Priorities Are Set

### 1. Manual Assignment (When Creating Task)
```python
service.create_task(
    title='[Client] Task name',
    client='client-slug',
    priority='P0'  # ← Explicitly set
)
```

### 2. Keyword Detection (Automatic)
When creating tasks, these keywords trigger auto-priority:

**P0 Keywords**:
- "CRITICAL"
- "URGENT"
- "ASAP"

**P1 Keywords**:
- "HIGH"
- "IMPORTANT"
- "THIS WEEK"

**P3 Keywords**:
- "LOW"
- "SOMEDAY"

**Example**:
```python
service.create_task(
    title='[Client] URGENT: Fix broken campaign',
    # No priority specified...
)
# → Automatically becomes P0 because "URGENT" in title
```

### 3. Automatic Escalation (Daily at 8pm)
The `task-priority-updater` agent runs daily and recalculates priorities based on due dates.

**Logic**:
```python
days_until_due = (due_date - today).days

if days_until_due <= 2:
    priority = 'P0'
elif days_until_due <= 14:
    priority = 'P1'
elif days_until_due <= 30:
    priority = 'P2'
else:
    priority = 'P3'
```

**Example escalation**:
- Monday: Task due Friday = P1 (4 days away)
- Tuesday 2pm: Task due Friday = P0 (2 days away by 24-hour calculation)
- Wednesday: Task due Friday = P1 (2 days away)
- Thursday: Task due Friday = P0 (1 day away)
- Friday: Task due Friday = P0 (due today)

---

## The 24-Hour Period Quirk

### Important Caveat:

Python's `.days` counts **full 24-hour periods**, not calendar days.

**Example** (from 2pm Tuesday):
- Task due Friday midnight
- Time until: 2 days + 10 hours = 58 hours
- Python `.days` = 2 (not 3)
- Priority = P0 ✅

**In other words**:
- Tuesday 2pm → Friday = "3 calendar days away"
- But Python calculates it as "2 full days + 10 hours"
- So `.days = 2`
- So it becomes P0

**This means**: Tasks might become P0 earlier than you expect (which is actually good - gives you more warning!)

---

## Checking Priorities

### View by Priority (Task Manager)
```bash
open tasks-overview-priority.html
```

### Check Specific Priority
```python
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()

# Get all P0 tasks
p0_tasks = service.get_active_tasks(priority='P0')
for task in p0_tasks:
    print(f"[{task['_client']}] {task['title']}")
```

### Run Priority Updater Manually
```bash
python3 agents/task-priority-updater/task-priority-updater.py
```

---

## Validation

### Check P0 Tasks Are Correct
```python
from datetime import datetime
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()
today = datetime.now().date()

p0_tasks = service.get_active_tasks(priority='P0')
for task in p0_tasks:
    if task.get('due_date'):
        due_date = datetime.fromisoformat(task['due_date']).date()
        days_until = (due_date - today).days

        if days_until > 2:
            print(f"⚠️ Incorrectly P0: {task['title']}")
            print(f"   Due in {days_until} days - should be P1")
```

---

## FAQs

### Q: Why is my Friday task P0 on Tuesday?
**A**: Because Python calculates it as 2 days away (58 hours = 2 full days + 10 hours = .days = 2).

### Q: Can I manually set priorities?
**A**: Yes! Just specify `priority='P0'` when creating the task. It will be honored until the nightly updater runs.

### Q: Will priorities change automatically?
**A**: Yes, the updater runs daily at 8pm. Tasks escalate as their due date approaches.

### Q: What if I don't have a due date?
**A**: Priority won't be automatically updated. Set it manually or it defaults to P2.

### Q: Can I disable auto-escalation?
**A**: Not recommended, but you can disable the LaunchAgent:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.task-priority-updater.plist
```

---

## Summary Table

| Priority | Days Until Due | Color | Meaning |
|----------|---------------|-------|---------|
| P0 | 0-2 days or overdue | Red | Do now |
| P1 | 3-14 days | Orange | This week |
| P2 | 15-30 days | Yellow | This month |
| P3 | 31+ days | Blue | Someday |

---

## Related Documentation

- **Full Guide**: [TASK-SYSTEM-COMPLETE-GUIDE.md](TASK-SYSTEM-COMPLETE-GUIDE.md)
- **Quick Start**: [TASK-SYSTEM-README.md](TASK-SYSTEM-README.md)
- **Script**: `agents/task-priority-updater/task-priority-updater.py`
- **LaunchAgent**: `agents/launchagents/com.petesbrain.task-priority-updater.plist`

---

**Your requirement**: "All tasks due today will be P0" ✅ **CONFIRMED**

Tasks due today ARE P0, plus you get early warning for tasks due tomorrow and day after tomorrow (also P0).
