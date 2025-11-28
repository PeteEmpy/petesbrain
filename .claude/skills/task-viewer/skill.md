---
name: task-viewer
description: Displays all Google Tasks in a clean, prioritized browser view with P0 urgent tasks at top. Use when user says "view tasks", "show tasks", "list tasks", "what's urgent", "show P0 tasks", "task dashboard", or wants an overview of what needs attention.
allowed-tools: Bash, Read, Write, mcp__google-tasks__list_task_lists, mcp__google-tasks__list_tasks
---

# Task Viewer Skill

## Instructions

When this skill is triggered:

1. **Use the Google Tasks MCP tool** to fetch all tasks from "Client Action Items" list:
   ```
   Use: mcp__google-tasks__list_tasks
   Parameters:
   - tasklist_id: Get from list_task_lists first, find "Client Action Items"
   - show_completed: false (only show active tasks)
   ```

2. **Parse and categorize tasks by priority**:
   - **P0 (URGENT)**: Tasks with `[URGENT]` prefix in title
   - **P1 (HIGH)**: Tasks with `[HIGH]` prefix in title
   - **P2 (NORMAL)**: Tasks without priority prefix
   - **P3 (TRACKING)**: Tasks with `[TRACKING]` prefix in title

3. **Extract key information** from each task:
   - Title (remove priority prefix for display)
   - Client name (extract from `[client-name]` in title)
   - Due date (format as "Today", "Tomorrow", or date)
   - Notes/context (from task notes field)
   - Task ID (for reference)

4. **Generate HTML page** with:
   - Clean, readable layout (Verdana font, proper spacing)
   - Tasks grouped by priority (P0 → P1 → P2 → P3)
   - Color coding:
     - P0: Red background (#ffebee) with bold red text
     - P1: Orange background (#fff3e0)
     - P2: White background (default)
     - P3: Light gray background (#f5f5f5)
   - Each task shows:
     - Priority badge
     - Client name (if present)
     - Task title
     - Due date (if set)
     - Context/notes (collapsed by default, expandable)
   - Count of tasks per priority at top
   - Last refreshed timestamp

5. **Save HTML to temp file and ALWAYS open in browser automatically**:
   ```bash
   # Save to /tmp/tasks-priority-view.html
   # ALWAYS open with: open /tmp/tasks-priority-view.html
   ```

   **CRITICAL: ALWAYS open the HTML file in the browser automatically. Do not just save the file - the user expects to see it displayed in their browser every time.**

6. **Summarize in chat**:
   - "Opened task view in browser with X urgent, Y high, Z normal tasks"
   - Highlight any P0 tasks specifically: "⚠️ 2 URGENT tasks need attention today"
   - Provide file path for manual opening if needed

## HTML Template Structure

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Task Priority View - {timestamp}</title>
    <style>
        body {
            font-family: Verdana, sans-serif;
            font-size: 13px;
            line-height: 1.5;
            margin: 0;
            padding: 20px;
            background: #fafafa;
        }
        .header {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .summary {
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }
        .summary-badge {
            padding: 8px 15px;
            border-radius: 4px;
            font-weight: bold;
        }
        .priority-section {
            margin-bottom: 25px;
        }
        .priority-header {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 4px;
        }
        .task-card {
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
            border-left: 4px solid;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .task-card.p0 {
            background: #ffebee;
            border-left-color: #d32f2f;
        }
        .task-card.p1 {
            background: #fff3e0;
            border-left-color: #f57c00;
        }
        .task-card.p2 {
            background: white;
            border-left-color: #1976d2;
        }
        .task-card.p3 {
            background: #f5f5f5;
            border-left-color: #757575;
        }
        .task-title {
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .task-meta {
            display: flex;
            gap: 15px;
            font-size: 12px;
            color: #666;
            margin-bottom: 8px;
        }
        .task-context {
            font-size: 12px;
            color: #444;
            margin-top: 10px;
            padding: 10px;
            background: rgba(0,0,0,0.03);
            border-radius: 4px;
            display: none;
        }
        .task-context.expanded {
            display: block;
        }
        .expand-btn {
            color: #1976d2;
            cursor: pointer;
            font-size: 12px;
            text-decoration: underline;
        }
        .priority-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
            margin-right: 8px;
        }
        .badge-p0 { background: #d32f2f; color: white; }
        .badge-p1 { background: #f57c00; color: white; }
        .badge-p2 { background: #1976d2; color: white; }
        .badge-p3 { background: #757575; color: white; }
    </style>
    <script>
        function toggleContext(taskId) {
            const context = document.getElementById('context-' + taskId);
            const btn = document.getElementById('btn-' + taskId);
            if (context.classList.contains('expanded')) {
                context.classList.remove('expanded');
                btn.textContent = 'Show context ▼';
            } else {
                context.classList.add('expanded');
                btn.textContent = 'Hide context ▲';
            }
        }
    </script>
</head>
<body>
    <div class="header">
        <h1>Task Priority View</h1>
        <div>Last updated: {timestamp}</div>
        <div class="summary">
            <div class="summary-badge" style="background: #ffebee; color: #d32f2f;">
                ⚠️ {p0_count} URGENT
            </div>
            <div class="summary-badge" style="background: #fff3e0; color: #f57c00;">
                {p1_count} HIGH
            </div>
            <div class="summary-badge" style="background: #e3f2fd; color: #1976d2;">
                {p2_count} NORMAL
            </div>
            <div class="summary-badge" style="background: #f5f5f5; color: #757575;">
                {p3_count} TRACKING
            </div>
        </div>
    </div>

    <!-- P0 Tasks -->
    {p0_section}

    <!-- P1 Tasks -->
    {p1_section}

    <!-- P2 Tasks -->
    {p2_section}

    <!-- P3 Tasks -->
    {p3_section}
</body>
</html>
```

## Example Output

**Chat Summary**:
```
✅ Opened task priority view in browser

📊 Current tasks:
- ⚠️ 2 URGENT (P0) - Need attention today
- 5 HIGH (P1) - Due this week
- 12 NORMAL (P2) - Due this month
- 3 TRACKING (P3) - Future work

🔴 URGENT tasks:
1. [Uno Lighting] Implement £1,800/day budget increase
2. [Godshot] Verify conversion tracking plugin fix

📁 Saved to: /tmp/tasks-priority-view-2025-11-13-153045.html
```

**Browser View**:
- Clean, organized layout with all tasks
- P0 tasks at top with red background
- Expandable context for each task
- Due dates highlighted
- Client names clearly shown

## When to Use This Skill

**Use this skill when**:
- User needs to see what's most urgent
- Planning daily work and prioritizing
- Checking if there are any P0 tasks from meetings
- Getting overview of workload
- Reviewing tasks before a meeting

**Don't use for**:
- Creating new tasks (use task generator skills)
- Marking tasks complete (use task completion flow)
- Syncing tasks (use task-sync skill)

## Notes

- Tasks are fetched fresh from Google Tasks each time (no caching)
- HTML file is timestamped for easy reference
- Context is collapsed by default to keep view clean
- P0 tasks are prominently highlighted
- Works with the new comprehensive meeting extraction system

## Related Skills

- **task-sync**: Sync tasks between local files and Google Tasks
- **task-verification**: Pre-verify tasks before marking complete
- **granola-importer**: Creates tasks from meetings (with P0 detection)

## Future Enhancements

- Filter by client
- Filter by due date range
- Search/filter functionality
- Mark tasks complete directly from view
- Email notification when P0 tasks detected
