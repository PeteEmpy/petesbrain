# Process Task Notes

Process manual notes from the Task Manager UI.

## Instructions

1. **Read the manual task notes file**:
   - File: `/Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json`
   - This contains notes added via the Task Manager HTML interface

2. **Identify task type** using `task_id`:
   - **UUID format** (e.g., `80ddcc31-...`): Internal task (in `tasks.json`)
   - **Base64 format** (e.g., `bVdZZURmdjZm...`): Google Task

3. **For internal tasks** (UUID):
   - Load from `clients/{client}/product-feeds/tasks.json` (primary) or `clients/{client}/tasks.json` (legacy)
   - For "roksys" client: `roksys/tasks.json`
   - Execute the `manual_note` instruction:
     - "Done" / "Complete" → Mark as completed, move to tasks-completed.md
     - "Update with X" → Append to task notes
     - Other instructions → Execute as specified
   - Use Python to safely edit JSON files

4. **For Google Tasks** (base64 ID):
   - Use Google Tasks MCP to update the task:
   ```python
   mcp__google-tasks__update_task(
       tasklist_id="...",  # Find the list first
       task_id="...",
       notes="Existing notes\n\n---\n**Manual Note (timestamp):**\n{manual_note}"
   )
   ```
   - Append manual note to existing task notes with timestamp
   - Do NOT mark as completed unless manual note says "Done"

5. **After processing all notes**:
   - Clear the file: `echo '[]' > data/state/manual-task-notes.json`
   - Regenerate HTML: `python3 generate-all-task-views.py`

6. **Report results** to user

## Task Type Detection

```python
import re

def is_google_task_id(task_id):
    """
    UUID format: 8-4-4-4-12 hex with dashes
    Google Tasks: 20-30 chars, base64-like, no dashes
    """
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if re.match(uuid_pattern, task_id, re.IGNORECASE):
        return False  # Internal task
    if len(task_id) > 15 and '-' not in task_id:
        return True  # Google Task
    return False
```

## CRITICAL

- This is NOT the Wispr Flow importer
- File location is ALWAYS: `data/state/manual-task-notes.json`
- The `manual_note` field contains the user's instruction
- Personal tasks are in `roksys/tasks.json`
- Client internal tasks check `product-feeds/tasks.json` FIRST, then `tasks.json`
