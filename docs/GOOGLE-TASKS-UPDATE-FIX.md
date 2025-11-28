# Google Tasks Update Fix

**Date:** 2025-11-06  
**Status:** ✅ Fixed

## Problem

Tasks were being created in Google Tasks but couldn't be easily updated. When users requested changes (e.g., "move Devonshire month end report to Friday"), there was no mechanism to:
1. Find tasks by title/description
2. Update tasks programmatically
3. Ensure updates happened in the correct task list ("Peter's List")

## Root Cause

1. **No search functionality**: The `update_task()` method required a `task_id`, but there was no easy way to find a task by its title
2. **MCP server limitations**: The MCP server required `tasklist_id` which wasn't user-friendly
3. **No helper methods**: No convenience methods to find and update tasks by title

## Solution

### 1. Enhanced GoogleTasksClient (`shared/google_tasks_client.py`)

Added new methods:

- **`get_task_by_title()`** - Enhanced to support exact or partial matching
- **`find_tasks_by_title()`** - Find all tasks matching a search term
- **`update_task_by_title()`** - Convenience method to find and update in one call

All methods default to searching in **"Peter's List"**.

### 2. New MCP Server Tools (`shared/mcp-servers/google-tasks-mcp-server/server.py`)

Added two new MCP tools:

- **`find_task_by_title`** - Search for tasks by title in "Peter's List" (or specified list)
- **`update_task_by_title`** - Find and update tasks by title

These tools make it easy for AI assistants to update tasks when users request changes.

### 3. Helper Script (`shared/scripts/update_google_task.py`)

Created a command-line script for manual task updates:

```bash
# Update due date
python3 shared/scripts/update_google_task.py "Devonshire month end" --due "Friday"

# Update title
python3 shared/scripts/update_google_task.py "Task title" --title "New Title"

# Mark as complete
python3 shared/scripts/update_google_task.py "Task title" --complete

# Update notes
python3 shared/scripts/update_google_task.py "Task title" --notes "New notes"
```

## Usage Examples

### Via Python Code

```python
from shared.google_tasks_client import GoogleTasksClient

client = GoogleTasksClient()

# Find and update a task
result = client.update_task_by_title(
    title="Devonshire month end",
    due_date="Friday",
    exact_match=False  # Allows partial match
)

# Or find first, then update
task = client.get_task_by_title("Devonshire", exact_match=False)
if task:
    client.update_task(
        task_id=task['id'],
        due_date="Friday"
    )
```

### Via MCP Server (for AI assistants)

The MCP server now provides:
- `find_task_by_title(search_term, tasklist_name="Peter's List")`
- `update_task_by_title(search_term, due="2025-11-07T00:00:00Z", ...)`

### Via Command Line

```bash
# List all tasks to find the exact title
python3 -c "from shared.google_tasks_client import GoogleTasksClient; client = GoogleTasksClient(); tasks = client.list_tasks('Peter\'s List'); [print(f'{t.get(\"title\")}') for t in tasks]"

# Update a task
python3 shared/scripts/update_google_task.py "Devonshire" --due "Friday"
```

## Key Features

1. **Default to "Peter's List"**: All methods default to "Peter's List" unless specified
2. **Partial matching**: Can find tasks with partial title matches (e.g., "Devonshire" finds "Complete Devonshire Hotels October 2025 Month-End Report")
3. **Natural language dates**: Supports "Friday", "tomorrow", "2025-11-07", etc.
4. **Error handling**: Clear error messages when tasks aren't found

## Testing

✅ Tested updating "Complete Devonshire Hotels October 2025 Month-End Report" to Friday
✅ Verified task appears correctly in Google Tasks
✅ Confirmed all methods default to "Peter's List"

## Future Improvements

1. Add support for updating multiple tasks at once
2. Add fuzzy matching for better search results
3. Add task history/audit log
4. Add support for recurring task updates

