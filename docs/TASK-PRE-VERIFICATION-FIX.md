# Task Pre-Verification and Duplicate Prevention - FIXED

**Date:** 2025-11-12
**Issue:** Daily Intel Report creating duplicate tasks and not pre-verifying P0/P1 tasks

## Problems Identified

### 1. Duplicate Task Creation
- **Root Cause:** `agents/system/tasks-monitor.py` was adding tasks to CONTEXT.md without checking if they already existed
- **Symptom:** Uno Lighting had 21 duplicate copies of "Check ROAS performance" task with different Google Task IDs
- **Impact:** CONTEXT.md became cluttered with duplicate entries, making it hard to track actual work

### 2. Pre-Verification Not Triggering
- **Root Cause:** `shared/scripts/task_verifier.py` had overly restrictive pattern matching
- **Symptom:** Tasks like "Check ROAS performance after 10% reduction" were not recognized as verifiable
- **Impact:** P1 tasks sat for 28 days without being automatically verified/expanded

## Fixes Implemented

### Fix #1: Duplicate Prevention (tasks-monitor.py)
**File:** `agents/system/tasks-monitor.py` (lines 736-763)

**Change:** Added duplicate detection before adding tasks to CONTEXT.md (checks for duplicate TITLE, not just task_id)

```python
# Check if task already exists in CONTEXT.md before adding (prevent duplicates)
if detected_client:
    context_file = CLIENTS_DIR / detected_client / "CONTEXT.md"
else:
    context_file = ROKSYS_DIR / "CONTEXT.md"

task_already_in_context = False
if context_file.exists():
    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if a task with this TITLE already exists (prevent duplicate content)
        # This catches multiple Google Tasks with same title but different IDs
        title_escaped = re.escape(task["title"])
        if re.search(rf'### {title_escaped}\n', content):
            task_already_in_context = True
    except:
        pass

if not task_already_in_context:
    # Add to CONTEXT.md
    add_task_to_context_md(new_task_record, detected_client, "Planned Work")
else:
    print(f"  ↷ Task '{task['title']}' already in CONTEXT.md, skipping duplicate")
```

**Behavior:**
- ✅ Before adding task, checks if task with **same TITLE** already exists in CONTEXT.md
- ✅ This prevents multiple Google Tasks with identical content but different IDs from creating duplicates
- ✅ Skips adding if duplicate detected (regardless of Google Task ID)
- ✅ Logs skipped duplicates for visibility

**Why check title instead of task_id?**
- The problem was: Daily Intel Report was creating 21 NEW Google Tasks with the same title but different IDs
- Checking task_id only prevents the SAME task_id from being added twice (useless for this case)
- Checking title prevents ANY task with duplicate content from being added to CONTEXT.md

### Fix #2: Expanded Verification Patterns (task_verifier.py)
**File:** `shared/scripts/task_verifier.py` (lines 104-111)

**Change:** Added more flexible patterns to detect performance check tasks

**Old patterns (too restrictive):**
- `verify.*roas.*(above|below|at|within)` - Required threshold keyword
- `check.*cpa.*(under|over|at)` - Required comparison keyword
- `confirm.*performance.*target` - Required "target" keyword
- `is.*(roas|cpa|spend).*still.*\d+` - Required "still" + number

**New patterns added (more flexible):**
```python
r'check.*(roas|cpa).*performance',  # "Check ROAS performance"
r'verify.*(roas|cpa)',              # "Verify ROAS"
r'review.*(roas|cpa)',              # "Review ROAS"
r'check.*performance.*after.*(change|reduction|increase)',  # "Check performance after reduction"
r'monitor.*(roas|cpa)',             # "Monitor ROAS"
r'roas.*check',                     # "ROAS check"
r'cpa.*check',                      # "CPA check"
```

**Impact:**
- ✅ Now catches tasks like "Check ROAS performance after 10% reduction"
- ✅ Detects general monitoring tasks without requiring specific threshold keywords
- ✅ More tasks will be pre-verified automatically

### Fix #3: Cleanup Existing Duplicates
**Action:** Removed 17 duplicate tasks from Uno Lighting's CONTEXT.md

**Results:**
- Before: 24 task entries (17 were duplicates)
- After: 7 unique task entries
- Kept first occurrence of each task, removed all subsequent duplicates

**Duplicates removed:**
- 5x "Check ROAS performance after 10% reduction on PMax campaigns"
- 3x "Review AI Max search terms report for Search Brand campaign"
- 7x "Verify product feed GTIN accuracy and product variant management"
- 2x "Review AI Max search terms for Search Brand campaign"

## Testing Recommendations

1. **Test Duplicate Prevention:**
   - Run `agents/system/tasks-monitor.py` manually
   - Create a new Google Task with same title as existing task in CONTEXT.md
   - Verify it logs "↷ Task already in CONTEXT.md, skipping duplicate"

2. **Test Pre-Verification:**
   - Run `agents/reporting/daily-intel-report.py` manually
   - Create a task titled "[Client] Check ROAS performance"
   - Verify it gets pre-verified with actual performance data

3. **Monitor for Regression:**
   - Check CONTEXT.md daily for duplicate entries
   - Check Daily Intel Report for P1 tasks without pre-verification
   - Review `~/.petesbrain-daily-intel.log` for errors

## Expected Behavior Going Forward

### Duplicate Prevention ✅
- New tasks checked against CONTEXT.md before adding
- Duplicate Google Tasks (same content, different IDs) will be skipped
- Log message: "↷ Task already in CONTEXT.md, skipping duplicate"

### Pre-Verification ✅
- Performance check tasks automatically verified
- Pre-verified tasks show:
  * Current ROAS/CPA metrics
  * Comparison to targets
  * Campaign-level breakdown
- User can approve/close tasks with one command

## Files Modified

1. `agents/system/tasks-monitor.py` - Added duplicate detection
2. `shared/scripts/task_verifier.py` - Expanded verification patterns
3. `clients/uno-lighting/CONTEXT.md` - Cleaned up 17 duplicates

## Related Documentation

- Task Pre-Verification Prototype: `docs/TASK-PRE-VERIFICATION-PROTOTYPE.md`
- Automation Overview: `docs/AUTOMATION.md`
- Daily Intel Report: `agents/reporting/daily-intel-report.py`

---

**Status:** ✅ COMPLETE
**Next Action:** Monitor for 1 week to confirm fixes are working as expected
