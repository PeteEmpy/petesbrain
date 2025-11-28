# Manual Notes Workflow
**Created:** 2025-11-19
**Status:** ✅ Active - Critical Workflow Documentation

---

## Overview

Users can add notes to tasks via the task manager HTML interface. These notes MUST be included when tasks are completed.

---

## Workflow

### 1. Adding Notes to Active Tasks

**Via HTML Interface:**
1. User opens `tasks-overview.html` or `tasks-overview-priority.html`
2. Clicks "Add Note" button on any active task
3. Types their note
4. Clicks "Save Note"

**What happens:**
- Note is stored temporarily in browser's `manualNotes` object
- Visual indicator shows task has a manual note (highlighted)
- "Process All Notes" button appears with count badge

### 2. Saving Notes for Processing

**User clicks "Process All Notes":**
- All notes are exported as JSON
- Saved to `data/state/manual-task-notes.json`
- OR sent to local server if `save-task-notes.py` is running

**Structure:**
```json
[
  {
    "client": "godshot",
    "task_id": "abc-123",
    "task_title": "[Godshot] Task name",
    "task_type": "standalone",
    "task_priority": "P1",
    "task_notes": "Original task notes...",
    "manual_note": "User's manual note added via UI"
  }
]
```

### 3. Processing Manual Notes

**Run processor:**
```bash
python3 shared/scripts/process-manual-task-notes.py
```

**OR if using Downloads:**
```bash
python3 shared/scripts/process-manual-task-notes.py ~/Downloads/manual-task-notes.json
```

**Claude then:**
1. Reads each note with full context
2. Analyzes whether task is complete
3. Decides if follow-up tasks are needed
4. Updates `clients/{client}/tasks.json`
5. If completing, logs to `clients/{client}/tasks-completed.md` **WITH MANUAL NOTES INCLUDED**

---

## 🚨 CRITICAL: Completing Tasks with Manual Notes

### When Manually Completing a Task

**ALWAYS check for manual notes FIRST:**

```python
# 1. Check if task has manual notes
manual_notes_file = Path('data/state/manual-task-notes.json')
manual_notes = []
if manual_notes_file.exists():
    with open(manual_notes_file, 'r') as f:
        all_notes = json.load(f)
    manual_notes = [n for n in all_notes if n['task_id'] == task_id]

# 2. Combine original notes + manual notes
combined_notes = task.get('notes', '')
if manual_notes:
    for note_data in manual_notes:
        combined_notes += f"\n\n**Manual Note (added {datetime.now().strftime('%Y-%m-%d')}):**\n{note_data['manual_note']}"

# 3. Log to tasks-completed.md with FULL notes
completion_entry = f"""## {task_title}
**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Source:** {source}

{combined_notes}

---
"""
```

### Example - Correct Completion Logging

**Task in tasks.json:**
```json
{
  "id": "abc-123",
  "title": "[Godshot] Verify conversion tracking",
  "notes": "Check WooCommerce plugin is reporting correctly",
  "priority": "P0"
}
```

**Manual note added via UI:**
```
"Checked plugin - working correctly. Tested with 3 sample orders, all tracked properly."
```

**Correct tasks-completed.md entry:**
```markdown
## [Godshot] Verify Conversion Tracking
**Completed:** 2025-11-19 17:45
**Source:** Manual completion (reported in Claude Code)

Check WooCommerce plugin is reporting correctly

**Manual Note (added 2025-11-19):**
Checked plugin - working correctly. Tested with 3 sample orders, all tracked properly.

**Resolution:** Tracking verified as functioning correctly. No issues found.

---
```

---

## Display in Task Manager

### Completed Tasks Section

When user expands a completed task in the HTML view:

**Shows:**
1. ✅ Task title (with strikethrough)
2. ✅ Completion date
3. ✅ **ALL NOTES** from `completion_notes` field
   - Original task notes
   - Manual notes added via UI
   - Completion summary
   - Follow-up actions
   - Everything written to tasks-completed.md

**Parser (`parse_completed_tasks_from_markdown`):**
- Extracts title
- Extracts completion date and source
- **Captures EVERYTHING after metadata until `---` separator**
- Includes:
  - Original descriptions
  - Manual notes
  - Bullet lists
  - Sections with headers
  - Code blocks
  - Tables
  - All formatting preserved

---

## Verification Checklist

**Before completing ANY task, verify:**

- [ ] Checked `data/state/manual-task-notes.json` for manual notes
- [ ] Combined ALL notes (original + manual)
- [ ] Logged full combined notes to `tasks-completed.md`
- [ ] Removed task from `tasks.json`
- [ ] Regenerated HTML: `python3 generate-tasks-overview.py`
- [ ] Verified completed task displays all notes in HTML

---

## Common Mistakes

### ❌ WRONG: Only logging completion summary

```markdown
## Task Name
**Completed:** 2025-11-19
**Source:** Manual

Done.

---
```

### ✅ CORRECT: Full context + manual notes

```markdown
## Task Name
**Completed:** 2025-11-19 14:30
**Source:** Manual completion (reported in Claude Code)

Original task context explaining what needed to be done...

**Manual Note (added 2025-11-19):**
User's note with specific details about how they completed it...

**Actions Taken:**
- Specific step 1
- Specific step 2

**Results:**
- Outcome 1
- Outcome 2

**Next Steps:**
- Follow-up action if needed

---
```

---

## Related Documentation

- `docs/TASK-COMPLETION-WORKFLOW.md` - Task completion protocol
- `docs/CLAUDE.md` - Main development guide (Manual Task Completion Protocol)
- `shared/scripts/process-manual-task-notes.py` - Automated processor
- `shared/scripts/save-task-notes.py` - Local server for saving notes

---

**Key Principle:** Manual notes are just as important as original task notes. Never lose context by omitting them during completion.
