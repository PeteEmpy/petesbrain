# Task Manager Regeneration Protocol

## CRITICAL: One Script Generates All Three Views

When ANY task changes are made (create, update, complete, delete, priority change, due date change), run this single script:

```bash
python3 generate-all-task-views.py
```

This automatically generates **ALL THREE** HTML views:
1. Standard overview: `tasks-overview.html` (organized by client)
2. Priority overview: `tasks-overview-priority.html` (organized by P0/P1/P2/P3)
3. Task Manager & Reminders: `tasks-manager.html` (clients on left, reminders on right)

The user primarily uses the **Task Manager & Reminders view**, so all three must always be regenerated together.

## When to Regenerate

Regenerate after:
- ✅ Creating tasks
- ✅ Updating task priorities
- ✅ Changing due dates
- ✅ Updating task status (active/waiting/blocked)
- ✅ Adding task notes
- ✅ Completing tasks (via ClientTasksService)
- ✅ Processing manual task notes
- ✅ Any other task modifications

## Why All Three Views Matter

- **Standard view** (`tasks-overview.html`): Organized by client, shows all tasks
- **Priority view** (`tasks-overview-priority.html`): Organized by priority (P0/P1/P2/P3)
- **Task Manager & Reminders** (`tasks-manager.html`): Primary view with clients on left (expandable) and reminders on right

User keeps Task Manager & Reminders view open in browser most of the time. If you only regenerate one or two views, they see stale data.

## DO NOT

❌ Forget to regenerate after task changes
❌ Assume changes will appear without regeneration
❌ Edit HTML files directly (they're generated from templates)

## DO

✅ Run `python3 generate-all-task-views.py` after ANY task change
✅ Verify all three HTML files have current timestamp after regeneration
✅ Test by hard-refreshing browser (Cmd+Shift+R) to see changes
