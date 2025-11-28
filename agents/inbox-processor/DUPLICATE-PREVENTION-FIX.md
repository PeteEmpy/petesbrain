# Duplicate Task Prevention Fix - November 14, 2025

## Problem Statement

The AI task generation system was creating duplicate Google Tasks when processing notes from the inbox. This happened because:

1. **ai-inbox-processor.py** would detect duplicates and add a warning to enhanced files
2. **inbox-processor.py** would read those warnings but **ignore them** and create Google Tasks anyway

This resulted in many duplicate tasks accumulating in Google Tasks (particularly from Nov 11-12 generation runs).

## Root Cause Analysis

### File: `/agents/ai-inbox-processor/ai-inbox-processor.py`

**Lines 690-699**: Duplicate detection logic
```python
duplicate_info, sim_score = check_duplicate_tasks(task_title, original_content)

if duplicate_info and sim_score > 70:
    print(f"  ⚠️  Potential duplicate detected: {sim_score:.1f}% similar to '{duplicate_info.get('title', 'Unknown')}'")
```

- ✅ **Works correctly**: Detects duplicates with >70% similarity
- ✅ **Works correctly**: Adds duplicate warning to enhanced file metadata
- ❌ **Problem**: Doesn't prevent file creation, only warns

**Lines 780-784**: Adds duplicate metadata to enhanced file
```python
if enhanced.get('is_duplicate'):
    enhanced_file_content += f"""⚠️ **DUPLICATE DETECTED**: {enhanced.get('duplicate_action', 'review')}
**Similar to:** {duplicate_info.get('title', 'Unknown')} ({duplicate_info.get('similarity', 0):.1f}% similar)
```

- ✅ **Works correctly**: Preserves duplicate information for downstream processing

### File: `/agents/inbox-processor/inbox-processor.py`

**Lines 117-126**: Extracts duplicate metadata
```python
# Extract duplicate info
if 'DUPLICATE DETECTED' in content:
    dup_match = re.search(r'DUPLICATE DETECTED.*?Similar to:\*\*\s*(.+?)(?:\n|$)', content, re.DOTALL)
    if dup_match:
        metadata['duplicate_check'] = {
            'found': True,
            'similar_to': dup_match.group(1).strip()
        }
else:
    metadata['duplicate_check'] = {'found': False}
```

- ✅ **Works correctly**: Extracts duplicate metadata from enhanced files

**Lines 527-539 (BEFORE FIX)**: Task creation WITHOUT duplicate check
```python
# Create Google Task
google_task_id = None
if GOOGLE_TASKS_ENABLED:
    try:
        client = GoogleTasksClient()
        task = client.create_task(
            title=task_title,
            notes=content,
            due_date=due_date
        )
```

- ❌ **ROOT CAUSE**: Never checked `metadata['duplicate_check']` before creating task
- ❌ **Impact**: Created Google Tasks even when duplicate was detected

## The Fix

### Change 1: Add duplicate check before task creation

**Lines 525-546 (AFTER FIX)**:
```python
# Create Google Task (with duplicate prevention)
google_task_id = None
duplicate_skipped = False

# Check if this is a duplicate before creating task
if processing_metadata.get('duplicate_check', {}).get('found'):
    duplicate_skipped = True
    similar_to = processing_metadata.get('duplicate_check', {}).get('similar_to', 'Unknown')
    print(f"  🔄 SKIPPING Google Task creation - duplicate of: {similar_to}")
elif GOOGLE_TASKS_ENABLED:
    try:
        client = GoogleTasksClient()
        task = client.create_task(
            title=task_title,
            notes=content,
            due_date=due_date
        )
        if task:
            google_task_id = task['id']
            print(f"  ✓ Created Google Task: {task_title}")
    except Exception as e:
        print(f"  ⚠️  Could not create Google Task: {e}")
```

**What changed**:
- Added `duplicate_skipped` flag to track when duplicate detection prevented creation
- Check `processing_metadata['duplicate_check']['found']` before creating Google Task
- If duplicate found, skip task creation and log which task it's similar to
- Only create task if NOT a duplicate AND Google Tasks is enabled

### Change 2: Update status message in local todo file

**Line 572 (AFTER FIX)**:
```python
{f"- ✅ Google Task created: `{google_task_id}`" if google_task_id else ("- 🔄 Google Task SKIPPED - duplicate detected" if duplicate_skipped else "- ⚠️ Google Task not created")}
```

**What changed**:
- Added clear messaging when task creation was skipped due to duplicate
- Distinguishes between:
  - ✅ Task created successfully (has google_task_id)
  - 🔄 Task skipped - duplicate detected (duplicate_skipped = True)
  - ⚠️ Task not created - other reason (Google Tasks disabled, error, etc.)

## How It Works Now

### Full Workflow

1. **User drops note in inbox** (`!inbox/note.md`)

2. **ai-inbox-processor.py runs** (every 6 hours or manually):
   - Reads note content
   - Calls `check_duplicate_tasks(task_title, content)`
   - Checks against:
     - All active Google Tasks (>70% similarity)
     - Recent processed notes (last 7 days)
   - If duplicate found:
     - Adds `⚠️ **DUPLICATE DETECTED**` to enhanced file
     - Sets `is_duplicate: true` in metadata
   - Saves enhanced file to `!inbox/ai-enhanced/enhanced-note.md`

3. **inbox-processor.py runs** (every 6 hours or manually):
   - Reads enhanced file
   - Extracts metadata including `duplicate_check`
   - **NEW**: Checks if `duplicate_check.found == True`
   - If duplicate:
     - **SKIPS Google Task creation** ✅
     - Logs: `🔄 SKIPPING Google Task creation - duplicate of: [similar task]`
     - Creates local todo file with "SKIPPED" status
   - If NOT duplicate:
     - Creates Google Task as normal
     - Creates local todo file with task ID

4. **Result**:
   - ✅ Duplicate tasks NO LONGER created in Google Tasks
   - ✅ Local todo file still created for audit trail
   - ✅ Clear messaging shows why task wasn't created
   - ✅ Original enhanced file metadata preserved

## Testing

### Manual Test

1. Create a test note in `!inbox/`:
   ```
   Test task for duplicate prevention
   ```

2. Run ai-inbox-processor:
   ```bash
   ANTHROPIC_API_KEY="your-key" agents/ai-inbox-processor/ai-inbox-processor.py
   ```

3. Check enhanced file has metadata

4. Run inbox-processor:
   ```bash
   agents/inbox-processor/inbox-processor.py
   ```

5. Verify Google Task created

6. Create similar note in `!inbox/`:
   ```
   Test task for duplicate prevention again
   ```

7. Run both processors again

8. **Expected result**:
   - Console shows: `🔄 SKIPPING Google Task creation - duplicate of: Test task for duplicate prevention`
   - No new Google Task created
   - Local todo file shows: `- 🔄 Google Task SKIPPED - duplicate detected`

### Integration Test

Check existing enhanced files in `!inbox/ai-enhanced/` that have duplicate warnings and verify they don't create new Google Tasks when re-processed.

## Impact

### Before Fix
- ~70+ tasks in Google Tasks, many duplicates
- Tasks from Nov 11-12 AI generation created multiple times
- No way to prevent duplicate creation short of manual cleanup

### After Fix
- Future AI task generation runs will NOT create duplicate Google Tasks
- Existing duplicates remain (need manual cleanup)
- System is now self-healing for duplicates

## Next Steps

1. **Manual cleanup required**: Remove existing duplicate tasks from Google Tasks
   - Use task deduplication script (if exists)
   - Or manually review and delete duplicates

2. **Monitor next AI generation run**:
   - Watch console output for `🔄 SKIPPING` messages
   - Verify no new duplicate tasks created in Google Tasks

3. **Consider tuning similarity threshold**:
   - Currently set to 70% in `check_duplicate_tasks()` (line 155 of ai-inbox-processor.py)
   - May need adjustment based on real-world usage
   - Too low: Misses legitimate duplicates
   - Too high: Flags similar but distinct tasks as duplicates

## Files Modified

- `/Users/administrator/Documents/PetesBrain/agents/inbox-processor/inbox-processor.py`
  - Lines 525-546: Added duplicate check before task creation
  - Line 527: Added `duplicate_skipped` flag
  - Lines 530-533: Duplicate detection and skip logic
  - Line 572: Updated status message to show skip reason

## Related Documentation

- `roksys/knowledge-base/rok-methodologies/experiment-logging-guide.md` - Task creation best practices
- `agents/ai-inbox-processor/README.md` - AI enhancement workflow
- `agents/inbox-processor/README.md` - Inbox processing workflow

---

**Fix Applied:** 2025-11-14
**Tested:** Pending
**Status:** Ready for next AI generation run
