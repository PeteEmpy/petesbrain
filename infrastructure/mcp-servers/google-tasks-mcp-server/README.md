# Google Tasks MCP Server

MCP server for managing Google Tasks.

## Features

- List task lists
- Create task lists
- List tasks (with optional completed tasks)
- Create tasks with title, notes, and due dates
- Update tasks
- Complete tasks
- Delete tasks

## Setup

1. Create a Google Cloud Project and enable Google Tasks API
2. Create service account credentials
3. Download credentials as `credentials.json`
4. Set up virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "google-tasks": {
      "command": "/path/to/.venv/bin/python",
      "args": ["/path/to/server.py"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

## Available Tools

- `list_task_lists()` - Get all task lists
- `create_task_list(title)` - Create a new list
- `list_tasks(tasklist_id, show_completed)` - Get tasks
- `create_task(tasklist_id, title, notes, due)` - Create task
- `update_task(tasklist_id, task_id, ...)` - Update task
- `complete_task(tasklist_id, task_id)` - Mark as done
- `delete_task(tasklist_id, task_id)` - Delete task
