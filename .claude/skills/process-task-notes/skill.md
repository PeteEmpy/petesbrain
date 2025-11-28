---
name: process-task-notes
description: Processes manual task notes from the Task Manager UI. Use when user says "process my task notes", "process task notes", "check task notes", or has added notes via the Task Manager interface.
allowed-tools: Read, Edit, Write, Bash
---

# Process Task Notes

**This skill processes manual notes added via the Task Manager UI.**

---

## CRITICAL: This is NOT the Wispr Flow Importer

- **This skill**: Processes notes from `data/state/manual-task-notes.json` (Task Manager UI)
- **Wispr Flow Importer**: Imports voice notes from Wispr Flow database (separate system)

**If user says "process my task notes" → USE THIS SKILL**
**If user says "import Wispr notes" → Use wispr-flow-importer skill**

---

## Instructions

### Step 1: Read the Manual Task Notes File

```bash
cat /Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json
```

**File location**: `/Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json`

### Step 2: Check if Notes Exist

If the file contains `[]` (empty array), report:
```
✅ No task notes to process - the queue is empty.
```

If notes exist, proceed to Step 3.

### Step 3: Process Each Note

For EACH note in the array, read the `manual_note` field - this contains the user's instruction.

**Note structure**:
```json
{
  "task_id": "uuid",
  "client": "client-slug",
  "task_title": "[Client] Task title",
  "task_type": "standalone|parent|child",
  "task_priority": "P0|P1|P2|P3",
  "task_notes": "Original task context",
  "manual_note": "USER'S INSTRUCTION - EXECUTE THIS",
  "timestamp": "ISO timestamp"
}
```

**The `manual_note` field is the instruction to execute.** Common patterns:

| Manual Note | Action |
|-------------|--------|
| "Done", "Complete", "Finished" | Mark task as completed |
| "Close this", "Can you close this?" | Mark task as completed |
| "Go look in sent folders" | Check `clients/{client}/emails/` for sent emails |
| "Draft a response" | Create email draft |
| "Update with..." | Add information to task notes |
| "Reschedule to..." | Update due date |
| "Change priority to P1" | Update task priority |

### Step 4: Execute the Instruction

**For task completion ("Done", "Close this", etc.):**

1. **Find the task** in `clients/{client}/tasks.json` or `roksys/tasks.json` by matching `task_id`

2. **Log to tasks-completed.md**:
   ```markdown
   ## {Task Title}
   **Completed:** YYYY-MM-DD HH:MM
   **Source:** Task Manager (manual note)

   {Original task notes}

   **Completion Note:** {manual_note content}

   ---
   ```

3. **Remove from tasks.json** using Python:
   ```python
   python3 -c "
   import json
   from datetime import datetime

   with open('path/to/tasks.json', 'r') as f:
       data = json.load(f)

   data['tasks'] = [t for t in data['tasks'] if t['id'] != 'TASK_ID_HERE']
   data['last_updated'] = datetime.now().isoformat()

   with open('path/to/tasks.json', 'w') as f:
       json.dump(data, f, indent=2)
   "
   ```

4. **Regenerate HTML**:
   ```bash
   python3 generate-tasks-overview.py
   ```

### Step 5: Clear Processed Notes

After ALL notes are processed, clear the file:

```bash
echo '[]' > /Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json
```

### Step 6: Report Results

```
✅ Processed {N} task note(s):

1. [Client] Task Title - {action taken}
2. [Client] Task Title - {action taken}

Task views regenerated.
```

---

## File Locations

| File | Purpose |
|------|---------|
| `data/state/manual-task-notes.json` | Queue of notes from Task Manager UI |
| `clients/{client}/tasks.json` | Client task storage |
| `roksys/tasks.json` | Roksys/Personal task storage |
| `clients/{client}/tasks-completed.md` | Completed task log (client) |
| `roksys/tasks-completed.md` | Completed task log (roksys/personal) |

---

## Task Location Mapping

| Client Value | tasks.json Location | tasks-completed.md Location |
|--------------|--------------------|-----------------------------|
| `roksys` | `roksys/tasks.json` | `roksys/tasks-completed.md` |
| `{client-name}` | `clients/{client-name}/tasks.json` | `clients/{client-name}/tasks-completed.md` |

**Note:** Personal tasks (tagged `[Personal]`) are stored in `roksys/tasks.json`.

---

## Troubleshooting

**Notes not appearing:**
- Check file exists: `cat data/state/manual-task-notes.json`
- Verify Task Manager is writing to correct location

**Task not found:**
- Search all tasks.json files: `grep -r "task_id" clients/*/tasks.json roksys/tasks.json`
- Task may already be completed

**JSON parse error:**
- Validate file: `python3 -c "import json; json.load(open('data/state/manual-task-notes.json'))"`

---

## DO NOT CONFUSE WITH

| Skill | Trigger | Purpose |
|-------|---------|---------|
| **process-task-notes** (this) | "process my task notes" | Process Task Manager UI notes |
| **wispr-flow-importer** | "import Wispr notes" | Import voice dictation from Wispr Flow |
| **task-manager** | "open task manager" | Open HTML task view in browser |
| **task-sync** | "sync tasks" | Sync with Google Tasks |
