# Duplicate Task Detection Improvements

**Date:** 2025-11-12  
**Status:** ✅ Implemented

## Problem

The duplicate task detection system was not preventing duplicate tasks from being created, particularly for Smythson. Multiple instances of the same tasks were appearing in Google Tasks, cluttering the task list and making it difficult to track actual work.

## Root Causes Identified

1. **Exact title matching only** - State file check used exact string comparison, missing near-duplicates
2. **No title normalization** - Tasks with slight formatting differences weren't caught
3. **No duplicate checking in registration** - `register_ai_task()` didn't check for existing duplicates
4. **Race conditions** - Tasks could be created before state file was updated
5. **Limited error handling** - Failures in state registration didn't prevent duplicate creation

## Solutions Implemented

### 1. Enhanced State File Check (`ai_tasks_state.py`)

**File:** `shared/scripts/ai_tasks_state.py`

**Changes:**
- Added `normalize_title()` helper function to normalize titles for comparison
- Enhanced `check_should_regenerate()` to use fuzzy matching (85% similarity threshold)
- Normalizes titles by removing client prefixes and normalizing whitespace
- Falls back to exact match if fuzzy matching module unavailable

**Key improvements:**
```python
# Before: Exact match only
if stored_title.lower().strip() != task_title.lower().strip():
    continue

# After: Normalized + fuzzy matching
normalized_new_title = normalize_title(task_title)
normalized_stored_title = normalize_title(stored_title)

if normalized_stored_title == normalized_new_title:
    match_found = True
else:
    similarity = calculate_similarity(normalized_stored_title, normalized_new_title)
    match_found = similarity >= similarity_threshold
```

### 2. Improved Duplicate Detection (`duplicate_task_detector.py`)

**File:** `shared/scripts/duplicate_task_detector.py`

**Changes:**
- Added `normalize_title()` function for consistent title normalization
- Improved title comparison to handle client prefix variations
- Better whitespace normalization

### 3. Enhanced Task Registration (`ai_tasks_state.py`)

**File:** `shared/scripts/ai_tasks_state.py`

**Changes:**
- Added duplicate checking in `register_ai_task()`
- Checks for duplicate Google Task IDs
- Checks for duplicate task titles (normalized) for same client
- Updates existing entry instead of creating duplicate if found

**Key improvements:**
```python
# Check if Google Task ID already exists
for existing_id, existing_data in state["tasks"].items():
    if existing_data.get("google_task_id") == google_task_id:
        return state  # Already registered

# Check for duplicate titles
normalized_new_title = normalize_title(task_title)
for existing_id, existing_data in state["tasks"].items():
    if existing_data.get("client") == client:
        normalized_existing_title = normalize_title(existing_data.get("task_title", ""))
        if normalized_new_title == normalized_existing_title:
            # Update existing instead of creating new
            existing_data["google_task_id"] = google_task_id
            return state
```

### 4. Better Error Handling (`daily-client-work-generator.py`)

**File:** `shared/scripts/daily-client-work-generator.py`

**Changes:**
- Added validation after task creation
- Improved error handling for state file registration
- Better logging with reasons for skipping duplicates
- State registration failures don't fail task creation (but are logged)

### 5. New Utility Scripts

#### Find Duplicate Tasks Script

**File:** `shared/scripts/find-duplicate-tasks.py`

**Purpose:** Identify duplicate tasks in Google Tasks

**Usage:**
```bash
# Find all duplicates
python3 shared/scripts/find-duplicate-tasks.py

# Find duplicates for specific client
python3 shared/scripts/find-duplicate-tasks.py --client smythson

# Output as JSON
python3 shared/scripts/find-duplicate-tasks.py --json
```

**Features:**
- Groups tasks by client and normalized title
- Shows duplicate groups with task IDs and status
- Recommends which tasks to keep/delete
- Saves report to `shared/data/duplicate-tasks-report-*.json`

#### Cleanup Duplicate Tasks Script

**File:** `shared/scripts/cleanup-duplicate-tasks.py`

**Purpose:** Remove duplicate tasks from Google Tasks

**Usage:**
```bash
# Dry run (preview what would be deleted)
python3 shared/scripts/cleanup-duplicate-tasks.py --client smythson

# Actually delete duplicates
python3 shared/scripts/cleanup-duplicate-tasks.py --client smythson --execute

# List duplicates only
python3 shared/scripts/cleanup-duplicate-tasks.py --client smythson --list-only
```

**Features:**
- Keeps oldest open task (or newest completed if all completed)
- Deletes other duplicates
- Dry-run mode by default (safe)
- Requires `--execute` flag to actually delete

## How It Works Now

### Task Creation Flow

1. **State File Check** (`check_should_regenerate`)
   - Normalizes new task title
   - Checks all existing tasks for same client
   - Uses fuzzy matching (85% threshold) to catch near-duplicates
   - Returns `False` if duplicate found (prevents creation)

2. **Google Tasks Check** (`is_duplicate_task`)
   - Fetches recent tasks from Google Tasks (last 7 days)
   - Normalizes titles for comparison
   - Checks exact match first, then fuzzy match (80% threshold)
   - Returns `True` if duplicate found (prevents creation)

3. **Task Creation**
   - Creates task in Google Tasks
   - Validates creation succeeded

4. **State Registration** (`register_ai_task`)
   - Checks for duplicate Google Task ID
   - Checks for duplicate normalized title for same client
   - Updates existing entry if duplicate found
   - Creates new entry only if no duplicates

### Title Normalization

All titles are normalized using this process:
1. Remove client prefix: `[Smythson] Task title` → `Task title`
2. Strip whitespace
3. Lowercase
4. Normalize whitespace: `"Task   title"` → `"task title"`

This ensures these are treated as duplicates:
- `[Smythson] Move diary asset group`
- `Move diary asset group`
- `move diary asset group`
- `Move  diary  asset  group`

## Testing

### Test Duplicate Detection

1. Run daily client work generator:
   ```bash
   python3 shared/scripts/daily-client-work-generator.py
   ```

2. Check output for duplicate detection:
   ```
   ⏭  Skipped (state check): [smythson] Move diary asset group to new standalone PMAX campaign
      Reason: Task still open with same priority
   
   ⏭  Skipped duplicate: [smythson] Review and prepare PMAX Christmas campaign 1-week performance update
      Matches: [Smythson] Review and prepare PMAX Christmas campaign 1-week performance update
   ```

### Find Existing Duplicates

```bash
# Find all Smythson duplicates
python3 shared/scripts/find-duplicate-tasks.py --client smythson
```

### Clean Up Existing Duplicates

```bash
# Preview cleanup (dry run)
python3 shared/scripts/cleanup-duplicate-tasks.py --client smythson

# Actually clean up
python3 shared/scripts/cleanup-duplicate-tasks.py --client smythson --execute
```

## Configuration

Duplicate detection settings in `shared/config/ai-tasks-config.json`:

```json
{
  "duplicate_detection": {
    "enabled": true,
    "similarity_threshold": 0.8,  // 80% for Google Tasks check
    "lookback_days": 7,
    "completed_grace_period_days": 3
  }
}
```

**Note:** State file check uses 85% threshold (stricter) to reduce false positives.

## Expected Behavior

### Before Fix
- Same task created multiple times
- No detection of near-duplicates
- State file didn't prevent duplicates
- Manual cleanup required

### After Fix
- Duplicates detected before creation
- Near-duplicates caught (85% similarity)
- State file prevents regeneration
- Automatic cleanup scripts available
- Better logging and error handling

## Next Steps

1. **Run cleanup script** to remove existing duplicates:
   ```bash
   python3 shared/scripts/cleanup-duplicate-tasks.py --client smythson --execute
   ```

2. **Monitor task creation** - Check daily client work generator output for duplicate detection messages

3. **Verify state file** - Ensure all tasks are properly registered in `shared/data/ai-tasks-state.json`

4. **Regular cleanup** - Run cleanup script periodically if duplicates appear

## Files Modified

- `shared/scripts/ai_tasks_state.py` - Enhanced state file check and registration
- `shared/scripts/duplicate_task_detector.py` - Improved title normalization
- `shared/scripts/daily-client-work-generator.py` - Better error handling and logging

## Files Created

- `shared/scripts/find-duplicate-tasks.py` - Identify duplicates
- `shared/scripts/cleanup-duplicate-tasks.py` - Remove duplicates
- `docs/DUPLICATE-TASK-DETECTION-IMPROVEMENTS.md` - This document

## Related Documentation

- `docs/TASK-INTEGRATION-ARCHITECTURE.md` - Overall task system architecture
- `docs/TASK-PRE-VERIFICATION-FIX.md` - Previous duplicate prevention fixes

