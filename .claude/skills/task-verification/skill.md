---
name: task-verification
description: On-demand verification of Google Tasks using the automated pre-verification system. Use when user says "verify tasks", "verify [client] tasks", "check task status", or needs to confirm Google Ads settings match task requirements.
allowed-tools: Bash, Read, mcp__google-tasks__list_task_lists, mcp__google-tasks__list_tasks, mcp__google-tasks__complete_task, mcp__google-ads__run_gaql
---

# Task Verification Skill

## What This Does

This skill allows you to verify tasks on-demand, outside of the automated Daily Intel Report schedule. Use it when you need to:

- Check specific client tasks immediately
- Verify all outstanding verification tasks across clients
- Re-verify tasks after making account changes
- Preview verification results before daily briefing runs

## How to Use

**Basic Usage**:
```
Verify all outstanding tasks
Verify tasks for [client-name]
Verify urgent tasks
Check all budget verification tasks
```

**Examples**:
- "Verify all Superspace tasks"
- "Check all urgent verification tasks"
- "Verify budget tasks across all clients"
- "Re-verify Smythson campaign status tasks"

## What You Should Do

When this skill is invoked:

1. **Load tasks from Google Tasks**:
   - Use `mcp__google-tasks__list_task_lists` to get task lists
   - Use `mcp__google-tasks__list_tasks` to get tasks from relevant lists
   - Filter based on user's request (client, priority, verification type)

2. **Identify verifiable tasks**:
   - Look for tasks with titles/notes containing verification keywords:
     * "verify", "check", "confirm", "validate"
     * "budget", "ROAS", "campaign status", "target CPA"
   - Extract client names from task titles (format: `[Client] Task description`)

3. **Run batch verification**:
   ```python
   import sys
   from pathlib import Path

   PROJECT_ROOT = Path('/Users/administrator/Documents/PetesBrain')
   sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'scripts'))

   from task_verifier import batch_pre_verify_tasks

   # Convert tasks to dict format
   task_dicts = [
       {
           'title': task['title'],
           'notes': task.get('notes', ''),
           'due': task.get('due', ''),
           'id': task['id']
       }
       for task in tasks
   ]

   # Run verification (automatically batches API calls)
   verified_tasks = batch_pre_verify_tasks(task_dicts)
   ```

4. **Present results**:
   - Group by verification status: ✅ Success, ⚠️ Warning, ❌ Error
   - Show summary for each verified task
   - Include details (budget levels, ROAS values, campaign status)
   - Suggest action: "Reply '[client] verified - close' to mark complete"

5. **Offer to complete tasks**:
   - If verification successful and user confirms, mark task as complete
   - Use `mcp__google-tasks__complete_task` to complete
   - Log to CONTEXT.md and tasks-completed.md

## Output Format

Present results in this format:

```
## Task Verification Results

**3 tasks verified** (2 successful, 1 warning)

### ✅ Successful Verifications

**[Superspace] Verify budget reductions holding**
- Result: UK £330/day, AU £300/day ✅
- Budget controls working correctly since Oct 21
- → Action: Reply "Superspace verified - close" to complete

**[Smythson] Check ROAS above 550%**
- Result: Overall ROAS 582% ✅
- All campaigns above target threshold
- → Action: Reply "Smythson verified - close" to complete

### ⚠️ Warnings

**[Tree2Mydoor] Verify PMax campaign enabled**
- Result: Campaign is PAUSED (expected ENABLED) ⚠️
- Last changed: Nov 10, 2025
- → Action: Investigate why campaign was paused

---

Would you like me to mark any of these tasks as complete?
```

## Filtering Options

Support these filtering modes:

1. **By client**: "Verify all [client] tasks"
   - Filter tasks where title starts with `[client-name]`

2. **By priority**: "Verify urgent tasks"
   - Map urgency keywords to task list names (P0, P1, P2)

3. **By verification type**: "Check all budget tasks"
   - Filter based on keywords: "budget", "ROAS", "campaign status", "setting"

4. **All verification tasks**: "Verify all outstanding tasks"
   - Check all tasks that match verification patterns

## Technical Details

**Task Verifier Module**: `/Users/administrator/Documents/PetesBrain/shared/scripts/task_verifier.py`

**Key Functions**:
- `batch_pre_verify_tasks(tasks)` - Main entry point, handles batching
- `detect_verification_type(title, notes)` - Returns verification type or None
- `extract_client_name(title, notes)` - Returns client name or None

**Verification Types**:
- `budget_check` - Daily budget levels and spend
- `campaign_status` - Campaign ENABLED/PAUSED state
- `performance_threshold` - ROAS/CPA vs targets
- `setting_verification` - Bid strategy settings

**API Efficiency**:
- Batching reduces API calls by 40-80%
- One API call per client per data type (budget or campaign data)
- Cached data reused for multiple verifications

## Important Notes

- Verification results are point-in-time snapshots
- Budget/performance data based on last 7 days
- Campaign status reflects current state at verification time
- Re-verification always fetches fresh data (no caching between skill invocations)

## Error Handling

If verification fails:
- Show error message from task_verifier
- Suggest checking:
  * Google Ads API access
  * Client exists in platform-ids.json
  * Task has valid client name in title
- Offer to skip failed verifications and continue with others

## Example Session

```
User: "Verify all Superspace tasks"

Claude: I'll verify all Superspace verification tasks...

## Task Verification Results

**2 tasks verified** (2 successful)

### ✅ Successful Verifications

**[Superspace] Verify budget reductions holding**
- Result: UK £330/day, AU £300/day ✅
- Budget controls working correctly since Oct 21
- → Action: Reply "Superspace verified - close" to complete

**[Superspace] Check ROAS above 500%**
- Result: Overall ROAS 536% ✅
- Within target range
- → Action: Reply "Superspace verified - close" to complete

---

Would you like me to mark these tasks as complete?
```