# Task Scripts Audit - 2025-11-26

## Summary

Audited 29 task-related Python scripts. Found that **most scripts already use correct architecture** (root tasks.json only), but **5 scripts need updating** to match the new standard.

---

## Correct Architecture (Already Implemented)

### ✅ ClientTasksService (Authoritative)
**File**: `shared/client_tasks_service.py`
**Status**: **CORRECT** - Uses root `tasks.json` only
**Code**:
```python
def _get_client_task_file(self, client: str) -> Path:
    return client_dir / 'tasks.json'  # ROOT ONLY
```

**This is the authoritative service** - all task creation, completion, and management goes through this.

---

## Scripts That Need Updating

### 1. ❌ generate-all-task-views.py
**File**: `/Users/administrator/Documents/PetesBrain/generate-all-task-views.py`
**Status**: **FIXED** (updated 2025-11-26)
**Issue**: Checked product-feeds first, called root "legacy"
**Fix**: Updated to check root first

```python
# BEFORE
task_file = client_dir / 'product-feeds' / 'tasks.json'  # PRIMARY
if not task_file.exists():
    task_file = client_dir / 'tasks.json'  # LEGACY

# AFTER
task_file = client_dir / 'tasks.json'  # PRIMARY
if not task_file.exists():
    task_file = client_dir / 'product-feeds' / 'tasks.json'  # FALLBACK
```

---

### 2. ❌ inbox-processor.py
**File**: `/Users/administrator/Documents/PetesBrain/agents/inbox-processor/inbox-processor.py`
**Line**: 604-608
**Status**: NEEDS FIX

**Current code:**
```python
# Check product-feeds location first, then direct
for task_path in [
    client_dir / 'product-feeds' / 'tasks.json',  # WRONG ORDER
    client_dir / 'tasks.json'
]:
```

**Should be:**
```python
# Check root location first (primary for all client work)
for task_path in [
    client_dir / 'tasks.json',  # CORRECT ORDER
    client_dir / 'product-feeds' / 'tasks.json'  # FALLBACK
]:
```

---

### 3. ❌ task-priority-updater.py
**File**: `/Users/administrator/Documents/PetesBrain/agents/task-priority-updater/task-priority-updater.py`
**Line**: 99-108
**Status**: NEEDS FIX

**Current code:**
```python
# Check product-feeds subdirectory first (where most tasks are)
pf_task_file = client_dir / 'product-feeds' / 'tasks.json'
if pf_task_file.exists():
    task_files.append((client_dir.name, pf_task_file))
# Also check direct client tasks.json (legacy/fallback)
direct_task_file = client_dir / 'tasks.json'
```

**Issues:**
- Comment says "where most tasks are" - no longer true
- Calls root "legacy/fallback" - should be primary

**Should be:**
```python
# Check root location first (primary for all client work)
direct_task_file = client_dir / 'tasks.json'
if direct_task_file.exists():
    task_files.append((client_dir.name, direct_task_file))
# Also check product-feeds (legacy location - should be migrated)
pf_task_file = client_dir / 'product-feeds' / 'tasks.json'
```

---

### 4. ❌ tasks-backup.py
**File**: `/Users/administrator/Documents/PetesBrain/agents/tasks-backup/tasks-backup.py`
**Line**: 98-104
**Status**: NEEDS FIX

**Current code:**
```python
# Check product-feeds subdirectory (primary location)
pf_tasks_file = client_dir / 'product-feeds' / 'tasks.json'
if pf_tasks_file.exists():
    task_files.append(pf_tasks_file)
# Also check direct client tasks.json (legacy/fallback)
tasks_file = client_dir / 'tasks.json'
```

**Should be:**
```python
# Check root location first (primary for all client work)
tasks_file = client_dir / 'tasks.json'
if tasks_file.exists():
    task_files.append(tasks_file)
# Also check product-feeds (legacy location - should be migrated)
pf_tasks_file = client_dir / 'product-feeds' / 'tasks.json'
```

---

### 5. ⚠️ cleanup-completed-tasks.py
**File**: `/Users/administrator/Documents/PetesBrain/shared/scripts/cleanup-completed-tasks.py`
**Line**: 122-125
**Status**: NEEDS REVIEW

**Current code:**
```python
# Also check product-feeds/tasks.json
product_feeds_dir = client_dir / 'product-feeds'
if product_feeds_dir.exists() and product_feeds_dir.is_dir():
    result = cleanup_client_tasks(product_feeds_dir, dry_run=dry_run)
```

**Issue**: Script explicitly cleans up product-feeds/tasks.json

**Decision needed**:
- Should this script ONLY clean root tasks.json?
- Or should it clean both but prioritise root?
- Since product-feeds shouldn't have tasks, probably should skip it entirely or just check for fallback

---

## Scripts That Are Already Correct

### ✅ All other scripts (24 scripts)
The remaining 24 scripts either:
1. Use `ClientTasksService` (which is correct)
2. Don't directly reference file paths
3. Read from consolidated cache files

**Examples:**
- `shared/complete_task.py` - Uses ClientTasksService ✅
- `shared/retroactive-task-creator.py` - Uses ClientTasksService ✅
- `tools/granola-importer/create_tasks_mcp.py` - Uses ClientTasksService ✅
- `agents/daily-intel-report/daily-intel-report.py` - Reads from cache ✅

---

## Migration Checklist

### Immediate (Already Done)
- [x] NMA: Migrate tasks.json from product-feeds to root
- [x] Update `generate-all-task-views.py` to prioritise root

### High Priority (Do Now)
- [ ] Update `inbox-processor.py` - Fix search order
- [ ] Update `task-priority-updater.py` - Fix search order + comments
- [ ] Update `tasks-backup.py` - Fix search order + comments
- [ ] Review `cleanup-completed-tasks.py` - Decide on product-feeds handling

### Medium Priority (After Script Fixes)
- [ ] Migrate remaining 9 clients from product-feeds to root:
  - accessories-for-the-home
  - bright-minds
  - clear-prospects
  - crowd-control
  - grain-guard
  - roksys
  - superspace
  - tree2mydoor
  - uno-lighting

### Low Priority (Post-Migration)
- [ ] Remove product-feeds fallback logic from all scripts
- [ ] Add validation to prevent future misplacement

---

## Testing Plan

After updating scripts:

1. **Test tasks overview generation**:
   ```bash
   python3 generate-all-task-views.py
   ```
   Verify all clients appear correctly

2. **Test inbox processor**:
   Process a test email that creates a task
   Verify task goes to correct location

3. **Test task backup**:
   ```bash
   python3 agents/tasks-backup/tasks-backup.py
   ```
   Verify all tasks.json files are backed up

4. **Test priority updater**:
   ```bash
   python3 agents/task-priority-updater/task-priority-updater.py
   ```
   Verify it updates correct files

---

## Conclusion

**Good news**: The core system (`ClientTasksService`) is already correct and has been all along. Only 4-5 peripheral scripts need updating to match the correct architecture.

**Root cause**: The scripts were written to match the actual (incorrect) file locations, not the intended architecture.

**Next steps**: Update the 4 scripts, then migrate remaining clients.
