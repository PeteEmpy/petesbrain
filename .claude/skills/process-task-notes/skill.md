---
name: process-task-notes
description: Process manual task notes from the Task Manager UI one-at-a-time with user interaction between each task. Use when user says "process my task notes", "process task notes", or "check task notes".
allowed-tools: Read, Edit, Write, Bash, Task, Glob
---

# Process Task Notes - Interactive Workflow

**This skill processes manual notes added via the Task Manager UI in an interactive, conversation-based manner with automatic state persistence.**

---

## Critical: Interactive vs Batch

**NEW BEHAVIOR (Interactive)**:
- Show ONE task at a time
- Wait for user to say "next" before proceeding to next task
- For investigation tasks: actually execute the investigation in this session
- User can interact with investigation until complete
- **Automatically saves progress to manual-task-notes.json after each action** ← STATE PERSISTENCE
- If interrupted or user says "stop": current state is saved and can be resumed
- Only clear file when ALL tasks have been processed

**OLD BEHAVIOR (Batch)**: ~~Process all notes at once~~ DEPRECATED

---

## State Persistence (NEW!)

**Your Question**: "Does stop or interruption actually write the current situation back to the original note?"

**Answer: YES - automatically.**

When you process task notes:
1. After each action (defer/complete/update/investigate), the `processed: true` flag is written to `manual-task-notes.json`
2. The updated file is saved immediately
3. If you say "stop" or conversation is interrupted, the file already has the latest state
4. Next session: skill reads the file, detects `processed: true` markers, and resumes from next unprocessed task

**Python state manager**: `/Users/administrator/Documents/PetesBrain.nosync/shared/scripts/process-task-notes-interactive.py`
- Handles loading/saving JSON
- Detects action types
- Tracks processed vs unprocessed
- Persists state on every change
- Enables resume after interruption

---

## Instructions

### Phase 1: Detect Task Types and Check for Batch Opportunity

**Step 1: Read the Manual Task Notes File**

```bash
cat /Users/administrator/Documents/PetesBrain.nosync/data/state/manual-task-notes.json
```

**File location**: `/Users/administrator/Documents/PetesBrain.nosync/data/state/manual-task-notes.json`

**Step 2: Check if Notes Exist**

If the file contains `[]` (empty array), report:
```
✅ No task notes to process - the queue is empty.
```

If notes exist, proceed to Step 3.

**Step 3: Auto-detect Action Types**

For each note, read the `manual_note` field and auto-detect action type:

| Keywords in manual_note | Action Type | Meaning |
|-------------------------|-------------|---------|
| "move to", "reschedule", "next week", "next month", "December X", "January X" | `defer` | Defer task to a future date |
| "investigate", "look into", "analyse", "check", "research", "examine" | `investigate` | Launch a full investigation in this session |
| "done", "finished", "completed", "close this", "marked complete" | `complete` | Task is done - archive it |
| "add:", "add to notes", "update with", "append", "memo" | `update` | Add information to task notes |

**Step 4: Check for Batch Opportunity**

Count notes with `action_type="complete"`. If 3 or more:

```
I see {N} tasks marked as "Done":
  • [Client 1] Task Title
  • [Client 2] Task Title
  • [Client 3] Task Title

Would you like me to:
  1. Complete all {N} at once (faster) - Recommended
  2. Go through them one-by-one (see details for each)
```

**User response**:
- If "1" or "batch" or "all at once": Jump to batch processing (skip to Phase 3, Batch Branch)
- If "2" or "one-by-one": Continue to Phase 2 (Interactive Branch)

---

### Phase 2: Interactive Single-Task Processing (Default)

**Step 1: Find Next Unprocessed Task**

Identify the first note without `processed: true` marker.

**Step 2: Present Task Summary**

Display clearly:

```
═══════════════════════════════════════
Task {N} of {TOTAL}: {Task Title}
═══════════════════════════════════════

Task: {task_title}
Priority: {task_priority} | Client: {client}
Action Type: {action_type}

Your note: "{manual_note}"

─────────────────────────────────────────
```

**Step 3: Execute Action Based on Type**

#### ACTION: Defer

```
✅ Deferring task to {new_date}
```

1. Extract date from manual_note (e.g., "move to December 18" → "2025-12-18")
2. Update task in `clients/{client}/tasks.json`:
   - Set `due_date` to extracted date
   - Append to `notes`: "Deferred from {today} - {reason from manual_note}"
   - Update `last_updated` timestamp
3. Add confirmation message showing new due date

#### ACTION: Complete

```
✅ Task completed and archived
```

1. Find task in `clients/{client}/tasks.json` or `roksys/tasks.json` by matching `task_id`
2. Log to appropriate `tasks-completed.md`:
   ```markdown
   ## {Task Title}
   **Completed:** {today} {current_time}
   **Source:** Task Manager (manual note)

   **Original Notes:**
   {task_notes}

   **Completion Note:** {manual_note}

   ---
   ```
3. Remove task from tasks.json using Python:
   ```bash
   python3 -c "
   import json
   from datetime import datetime

   with open('{tasks_json_path}', 'r') as f:
       data = json.load(f)

   data['tasks'] = [t for t in data['tasks'] if t['id'] != '{task_id}']
   data['last_updated'] = datetime.now().isoformat()

   with open('{tasks_json_path}', 'w') as f:
       json.dump(data, f, indent=2)
   "
   ```

#### ACTION: Update

```
✅ Task notes updated
```

1. Find task in tasks.json by task_id
2. Append to task's `notes` field:
   ```
   Updated {today}: {content_from_manual_note}
   ```
3. Update `last_updated` timestamp
4. Save updated tasks.json

#### ACTION: Investigate

```
🔍 Launching investigation now...
```

**DO NOT ASK PERMISSION - automatically begin investigation.**

For Crowd Control CTR collapse investigation as example:
1. Explain what you're investigating: "Investigating why posts and stands have low CTR in Crowd Control account vs US performance"
2. Use available tools:
   - **Read emails**: Check `clients/crowd-control/emails/` for messages from Jeremy about product performance
   - **Query Google Ads**: Use GAQL to get posts/stands CTR, impressions, conversions
   - **Check Product Impact**: Review product baselines and trends
3. Create analysis document at `clients/{client}/documents/{investigation-name}-{date}.md` with:
   - Key findings (metrics, performance gaps)
   - Root cause analysis
   - Recommendations
4. **Offer to draft email**: "Would you like me to draft an email to {contact} with these findings?"
5. If user says yes: Create email draft
6. **Report completion**: "✅ Investigation complete. Task updated with findings and next steps."

**User can interact throughout**: Ask clarifying questions, request deeper analysis, modify recommendations. Continue until they're satisfied.

**Step 4: Mark as Processed and Save State**

After executing action:
1. Add `"processed": true` to the note in manual-task-notes.json
2. **SAVE THE FILE IMMEDIATELY** (state persistence)
3. **DO NOT remove the note yet** - keep it with `processed: true` marker

**Why immediate save?** If conversation is interrupted or you say "stop", the file already has the latest state, so session can be resumed next time.

**Step 5: Wait for User Confirmation**

Display:

```
═══════════════════════════════════════
Say "next" to continue to task {N+1} of {TOTAL}
Type "skip" to skip this task
Type "stop" to exit (you can resume later)
═══════════════════════════════════════
```

**Recognize user commands**:
- **"next"**, **"ok"**, **"continue"** → Advance to next task
- **"skip"** → Mark as processed but take no action (for tasks you want to defer manually)
- **"done"**, **"complete"** → Immediately mark task complete (in case you decide mid-way)
- **"stop"** → Exit processing (leave unprocessed notes in file for next session)

**Step 6: Repeat or Finish**

If more unprocessed notes exist → Loop back to Step 1

If all notes have `processed: true`:

```
═══════════════════════════════════════
All task notes processed! Clearing queue...
═══════════════════════════════════════

✅ {N} tasks processed:
  1. [Client] Task Title - {action taken}
  2. [Client] Task Title - {action taken}
  ...

Ready for next session.
```

**State Persistence Note**: All tasks were already saved with `processed: true` during processing. Now clear the file:
```bash
echo '[]' > /Users/administrator/Documents/PetesBrain.nosync/data/state/manual-task-notes.json
```

**Why this works**: Each task was saved immediately after the action was taken. If interrupted before reaching this point, the file would have `processed: true` for completed tasks and the session could resume.

---

### Phase 3: Batch Processing (If User Chooses)

**When user selects batch mode for "Done" notes**:

1. Process all notes with `action_type="complete"`:
   - Log each to tasks-completed.md
   - Remove each from tasks.json
   - Mark as `processed: true`

2. Display summary:
```
✅ Batch completed {N} tasks:
  • [Client 1] Task Title → archived
  • [Client 2] Task Title → archived
  • [Client 3] Task Title → archived
```

3. Continue to remaining non-complete tasks with interactive mode

---

## Resume Capability

### When User Says "Stop"

If user types "stop" or "exit" during processing:

1. Current state is **already saved** to manual-task-notes.json
   - All completed tasks have `processed: true` marker
   - Incomplete tasks have `processed: false`
2. Display confirmation:
   ```
   ✅ State saved. You can resume later with "process my task notes"
   ```
3. Exit processing - conversation ends

### When Conversation is Interrupted

If the conversation is interrupted (timeout, browser close, etc.):

1. **No action needed** - state was already saved after each task action
2. Last successful action has `processed: true` in the file
3. Interrupted action (in progress) remains unprocessed

### Resuming Next Session

**Next time user says "process my task notes":**

1. Script reads manual-task-notes.json and checks for `processed: true` markers
2. If found, report:
   ```
   📋 Resuming... {X} tasks already processed, {Y} remaining.

   ═══════════════════════════════════════
   Task {X+1} of {TOTAL}: {Next Task Title}
   ═══════════════════════════════════════
   ```
3. Continue from where you left off - no data loss

**User can also explicitly ask**: "where were we?" → Show current task summary again

**Example**: If processing 5 tasks and interrupted after task 2:
- Task 1: `processed: true` ✅
- Task 2: `processed: true` ✅
- Task 3: `processed: false` (next to process)
- Task 4: `processed: false`
- Task 5: `processed: false`

Next session will show "Resuming... 2 tasks processed, 3 remaining" and start with Task 3.

---

## Data Structure

**Note format in manual-task-notes.json:**

```json
[
  {
    "task_id": "uuid",
    "client": "client-slug",
    "task_title": "[Client] Task title",
    "task_type": "standalone|parent|child",
    "task_priority": "P0|P1|P2|P3",
    "task_notes": "Original task context",
    "manual_note": "USER'S INSTRUCTION",
    "timestamp": "ISO timestamp",
    "processed": false,
    "action_type": "defer|investigate|complete|update"
  }
]
```

**After user action**: Add `"processed": true` to mark as shown (do not remove from array yet).

---

## File Locations

| File | Purpose |
|------|---------|
| `data/state/manual-task-notes.json` | Queue of notes from Task Manager UI |
| `clients/{client}/tasks.json` | Client task storage |
| `roksys/tasks.json` | Roksys/Personal task storage |
| `clients/{client}/tasks-completed.md` | Completed task log (client) |
| `roksys/tasks-completed.md` | Completed task log (roksys/personal) |
| `clients/{client}/documents/` | Investigation results |
| `clients/{client}/emails/` | Email correspondence |

---

## Task Location Mapping

| Client Value | tasks.json Location | tasks-completed.md Location |
|--------------|--------------------|-----------------------------|
| `roksys` | `roksys/tasks.json` | `roksys/tasks-completed.md` |
| `{client-name}` | `clients/{client-name}/tasks.json` | `clients/{client-name}/tasks-completed.md` |

---

## Key Behaviors

✅ **DO**:
- Auto-detect action types from manual_note text
- Show one task at a time
- Wait for "next" before advancing
- Auto-launch investigations (no permission needed)
- Allow user to interact with investigations
- Mark as `processed: true` (not deleted) after action
- Resume from where left off
- Only clear file when ALL tasks processed
- Offer batch mode for 3+ "Done" notes

❌ **DON'T**:
- Process all tasks at once
- Delete processed notes immediately
- Ask permission for investigation launch
- Clear file until all tasks are shown to user
- Assume you know what "reschedule to X" date should be (extract from note)
- Regenerate HTML until all tasks processed (do it once at end)

---

## Examples

### Example 1: Simple Defer

```
Task: [Devonshire] Analyse property campaign budgets
Priority: P1 | Client: Devonshire Hotels

Your note: "Too early in month after budget decrease. Move to next week"

✅ Deferring task to 2025-12-18
Note added: "Deferred from Dec 10 - too early in month for meaningful data after budget change"

═══════════════════════════════════════
Say "next" to continue to task 2 of 2
```

### Example 2: Investigation with Interaction

```
Task: [Crowd Control] Investigate Product CTR Collapse for Top Products
Priority: P2 | Client: Crowd Control

Your note: "Read emails from Jeremy, use Product Impact Analyzer..."

🔍 Launching investigation now...

Let me check Jeremy's recent emails first...
[Reads and summarizes emails showing US reports posts/stands performing well]

Now querying Google Ads for posts/stands product performance...
[Shows GAQL results: Posts 2.1% CTR, Stands 1.8% CTR]

Checking Product Impact Analyzer...
[Analyses product baselines and trends]

KEY FINDINGS:
- Posts: 2.1% CTR (vs 3.5% US average) - 40% below
- Stands: 1.8% CTR (vs 3.2% US average) - 44% below
- Root cause: Outdated product images

Would you like me to draft an email to Jeremy with these findings?

User: yes

Email draft created. ✅ Investigation complete.

═══════════════════════════════════════
Say "next" to continue (or "stop" to exit)
```

### Example 3: Batch Mode Offer

```
I see 3 tasks marked as "Done":
  • [Devonshire] PMax assets follow-up
  • [Clear Prospects] November report
  • [Superspace] Budget changes confirmation

Would you like me to:
  1. Complete all 3 at once (faster) - Recommended
  2. Go through them one-by-one

User: 1

✅ Batch completed 3 tasks:
  • Devonshire PMax assets → archived
  • Clear Prospects report → archived
  • Superspace budget → archived

═══════════════════════════════════════
Task 4 of 5: NMA Campaign Restructure
═══════════════════════════════════════
```

---

## Troubleshooting

**Notes not appearing:**
- Check file: `cat data/state/manual-task-notes.json`
- Verify Task Manager is writing to correct location
- Check that notes have valid JSON format

**Task not found:**
- Search all tasks.json files for task_id
- Task may already be completed

**User says "where were we?":**
- Check for `processed: true` markers
- Show current unprocessed task again

**Resume interrupted session:**
- Check manual-task-notes.json for `processed: true` flags
- Continue from first unprocessed task
- User can pick up investigation where they left off

---

## DO NOT CONFUSE WITH

| Skill | Trigger | Purpose |
|-------|---------|---------|
| **process-task-notes** (this) | "process my task notes" | Process Task Manager UI notes **interactively** |
| **task-manager** | "open task manager" | Open HTML task view in browser |
| **task-sync** | "sync tasks" | Sync with Google Tasks |

