# Task System Architecture

**Last Updated**: December 12, 2025  
**Status**: ✅ Active - Final Architecture

---

## Overview

PetesBrain uses a **per-client JSON-based task system** for managing client work, with special handling for Roksys/internal tasks.

**Google Tasks** is used for: Personal tasks only ("Peter's List")  
**Internal system** is used for: All client-related tasks

---

## Task Storage Locations

### Correct Locations (Definitive)

| Task Type | Location | Example |
|-----------|----------|---------|
| Client work tasks | `clients/{client}/tasks.json` | `clients/smythson/tasks.json` |
| Roksys/Personal tasks | `roksys/tasks.json` | `roksys/tasks.json` |
| Completed tasks (client) | `clients/{client}/tasks-completed.md` | `clients/smythson/tasks-completed.md` |
| Completed tasks (roksys) | `roksys/tasks-completed.md` | `roksys/tasks-completed.md` |
| Google Tasks | Google Tasks API | "Peter's List" |

### Forbidden Locations

❌ **NEVER use these locations:**
- `clients/{client}/product-feeds/tasks.json` - LEGACY ARTIFACT
- `clients/{client}/product-feeds/tasks_*.json` - LEGACY ARTIFACT
- `clients/roksys/tasks.json` - WRONG (use `roksys/tasks.json`)

**Why**: Product-feeds folders are for product feed management only. Tasks should never be stored there. Roksys is a special case and uses the `roksys/` directory, not `clients/roksys/`.

---

## Roksys Tasks (Special Case)

**Important**: Roksys tasks are NOT client tasks.

**Correct Location**: `roksys/tasks.json`  
**Incorrect Location**: `clients/roksys/tasks.json` ❌

**Why**: Roksys is internal/personal work, not a client. It has its own directory structure separate from clients.

**How ClientTasksService Handles It**:
```python
if client == 'roksys':
    return PROJECT_ROOT / 'roksys' / 'tasks.json'
else:
    return CLIENTS_DIR / client / 'tasks.json'
```

---

## Protection Layers

### 1. Service Layer (`ClientTasksService`)

**Write-Side Guard**:
- Blocks any attempt to write to product-feeds locations
- Blocks Roksys tasks from being written to `clients/roksys/`
- Raises `ValueError` with clear error message

**Read-Side Guard**:
- Blocks any attempt to read from product-feeds locations
- Raises `ValueError` if product-feeds path detected

**Location**: `shared/client_tasks_service.py`

### 2. Validation Layer (`validate-task-locations.py`)

**What it does**:
- Scans all client directories for product-feeds/tasks*.json files
- Detects violations immediately
- Logs to audit trail
- **Fail-fast**: Exits with error code if violations found

**Integration**:
- Runs before task manager generation
- Can run on system startup (LaunchAgent)
- Can run periodically

**Location**: `shared/scripts/validate-task-locations.py`

### 3. Git Layer (Pre-Commit Hook)

**What it does**:
- Blocks commits that include product-feeds/tasks*.json files
- Provides clear error message with fix instructions
- Prevents accidental commits of legacy files

**Location**: `.git/hooks/pre-commit`

### 4. Code Layer

**No Fallback Logic**:
- All reading code only checks correct locations
- No "check product-feeds if main doesn't exist" logic
- Explicit Roksys handling in all task reading code

---

## Creating Tasks

### Always Use ClientTasksService

```python
from shared.client_tasks_service import ClientTasksService

service = ClientTasksService()

# Client task
service.create_task(
    title='[Smythson] Review Black Friday performance',
    client='smythson',
    priority='P1',
    due_date='2025-12-02',
    source='Manual'
)

# Roksys task
service.create_task(
    title='[Roksys] Update documentation',
    client='roksys',  # Special case - goes to roksys/tasks.json
    priority='P2',
    source='Manual'
)
```

### Never Write Directly

❌ **DON'T DO THIS**:
```python
# Direct file write - bypasses all guards
with open('clients/client/tasks.json', 'w') as f:
    json.dump(data, f)
```

✅ **DO THIS**:
```python
# Use ClientTasksService - includes all guards
service.create_task(...)
```

---

## Reading Tasks

### Task Manager Generation

**File**: `generate-all-task-views.py` (consolidated script)

**Process**:
1. Runs validation (fail-fast if violations)
2. Reads from `clients/{client}/tasks.json` only
3. Reads from `roksys/tasks.json` for Roksys tasks
4. **Never** reads from product-feeds
5. Generates all three HTML views in single execution

### Other Scripts

All task reading scripts follow the same pattern:
- Check `clients/{client}/tasks.json`
- Check `roksys/tasks.json` for Roksys
- **Never** check product-feeds

---

## Completing Tasks

### Process

1. **Log to tasks-completed.md** ✅
   - Include original task notes
   - Include manual notes (if any)
   - Include completion summary

2. **Remove from tasks.json** ✅
   - Tasks are REMOVED, not marked as completed
   - Use `ClientTasksService.complete_task()`

3. **Regenerate task manager** ✅
   - Run `python3 generate-all-task-views.py`

### Example

```python
service.complete_task(
    task_id='abc-123',
    client='smythson',
    completion_notes='Task completed successfully. Results: ...'
)
```

This:
- Removes task from `clients/smythson/tasks.json`
- Logs to `clients/smythson/tasks-completed.md`
- Includes all notes (original + manual + completion)

---

## Validation & Monitoring

### Run Validation

```bash
python3 shared/scripts/validate-task-locations.py
```

**Expected Output**:
```
✅ Task location validation passed (2025-12-12 15:11:31)
   No product-feeds/tasks.json files detected
```

**If Violations Found**:
- Script exits with error code 1
- Logs to `data/state/tasks-audit.log`
- Provides fix instructions

### Audit Product-Feeds

```bash
python3 shared/scripts/audit-product-feeds-tasks.py
```

**What it does**:
- Scans for all product-feeds/tasks*.json files
- Analyzes contents
- Detects duplicates
- Finds code references
- Generates comprehensive report

---

## Migration History

### Nov 25, 2025
- First fix attempt
- Migrated 41 tasks
- Updated inbox processors
- **Issue**: Fallback code remained

### Dec 11, 2025
- "Permanent fix" attempt
- Added ClientTasksService guard
- Created validation script
- **Issue**: Incomplete - missed fallback code, validation optional

### Dec 12, 2025
- **Final comprehensive fix**
- Complete audit (found 30 files, 101 tasks)
- Removed ALL fallback code
- Enhanced guards (write + read side)
- Fail-fast validation
- Git pre-commit hook
- Fixed Roksys location
- Migrated 35 unique tasks
- Deleted all product-feeds files
- **Status**: ✅ Complete

---

## Troubleshooting

### Tasks Not Showing in Task Manager

1. **Check location**: `clients/{client}/tasks.json` (not product-feeds)
2. **Check Roksys**: `roksys/tasks.json` (not clients/roksys/)
3. **Run validation**: `python3 shared/scripts/validate-task-locations.py`
4. **Regenerate**: `python3 generate-all-task-views.py`

### Validation Fails

1. **Check audit log**: `data/state/tasks-audit.log`
2. **Run audit**: `python3 shared/scripts/audit-product-feeds-tasks.py`
3. **Delete product-feeds files**: `find clients -path '*/product-feeds/tasks*.json' ! -path '*/_archived*' -delete`
4. **Verify**: Run validation again

### Guard Triggers

If ClientTasksService guard raises an error:

1. **Check the error message** - it explains what's wrong
2. **Verify client name** - is it "roksys"? Use `roksys/tasks.json`
3. **Check path** - ensure no product-feeds in path
4. **Review calling code** - should use ClientTasksService

---

## Related Documentation

- `docs/PRODUCT-FEEDS-FINAL-FIX-2025-12-12.md` - This fix
- `docs/TASK-SYSTEM-README.md` - Quick reference
- `docs/TASK-COMPLETION-WORKFLOW.md` - Completion process
- `docs/MANUAL-NOTES-WORKFLOW.md` - Manual notes handling
- `shared/client_tasks_service.py` - Service implementation

---

**Key Principle**: Tasks belong in canonical locations only. Product-feeds is forbidden. Roksys is special. Guards enforce this at multiple layers.


