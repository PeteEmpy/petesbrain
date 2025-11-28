# Task Manager Regeneration Protocol

## CRITICAL: One Script Generates Both Views

When ANY task changes are made (create, update, complete, delete, priority change, due date change), run this single script:

```bash
python3 generate-tasks-overview.py
```

This automatically generates **BOTH** HTML views:
1. Standard overview: `tasks-overview.html` (organized by client)
2. Priority overview: `tasks-overview-priority.html` (organized by P0/P1/P2/P3)

The user primarily uses the **priority view**, so both must always be regenerated together.

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

## Why Both Views Matter

- **Standard view** (`tasks-overview.html`): Organized by client, shows all tasks
- **Priority view** (`tasks-overview-priority.html`): Organized by priority (P0/P1/P2/P3), combines internal + Google Tasks

User keeps priority view open in browser most of the time. If you only regenerate standard view, they see stale data.

## DO NOT

❌ Forget to regenerate after task changes
❌ Assume changes will appear without regeneration
❌ Edit HTML files directly (they're generated from templates)

## DO

✅ Run `python3 generate-tasks-overview.py` after ANY task change
✅ Verify both HTML files have current timestamp after regeneration
✅ Test by hard-refreshing browser (Cmd+Shift+R) to see changes
