# Task System Documentation Index

**Created**: 2025-11-26
**Purpose**: Master index for all task system documentation

---

## 📚 Documentation Files

### 1. Task Manager User Manual (Start Here) ⭐ NEW
**File**: [TASK-MANAGER-USER-MANUAL.md](TASK-MANAGER-USER-MANUAL.md)

**Contains**:
- What the Task Manager is and how to open it
- Understanding the interface (priorities, due dates, task types)
- Common operations (completing tasks, adding notes, finding tasks)
- Parent-child task relationships
- Recurring tasks explained
- Troubleshooting guide (user-friendly)
- Daily workflow tips and best practices
- Quick reference card

**Read this if**: You're using the Task Manager UI daily and want to understand all its features.

**Created**: December 19, 2025

---

### 2. Quick Start (Technical Reference)
**File**: [TASK-SYSTEM-README.md](TASK-SYSTEM-README.md)

**Contains**:
- Golden rules
- Quick commands
- Common troubleshooting
- 5-minute overview

**Read this if**: You need a quick technical refresher or are using the system programmatically.

---

### 3. Complete Guide (Deep Dive)
**File**: [TASK-SYSTEM-COMPLETE-GUIDE.md](TASK-SYSTEM-COMPLETE-GUIDE.md)

**Contains**:
- Complete architecture explanation
- File structure details
- All scripts reference
- Troubleshooting guide
- Migration history
- Validation instructions

**Read this if**: You need to understand how everything works, troubleshoot complex issues, or modify the system.

---

### 4. Migration History
**File**: [MIGRATION-COMPLETE-2025-11-26.md](MIGRATION-COMPLETE-2025-11-26.md)

**Contains**:
- What was migrated on 2025-11-26
- Before/after counts
- Scripts updated
- Backup information

**Read this if**: You want to understand what changed during the 2025-11-26 migration.

---

### 5. Architecture Issue Analysis
**File**: [TASKS-ARCHITECTURE-ISSUE-2025-11-26.md](TASKS-ARCHITECTURE-ISSUE-2025-11-26.md)

**Contains**:
- Original problem analysis
- Why tasks were in wrong locations
- Migration plan that was executed

**Read this if**: You want historical context on why the migration was needed.

---

### 6. Scripts Audit
**File**: [TASKS-SCRIPTS-AUDIT-2025-11-26.md](TASKS-SCRIPTS-AUDIT-2025-11-26.md)

**Contains**:
- Analysis of all 29 task-related scripts
- Which scripts needed updating
- Before/after code comparisons

**Read this if**: You're modifying task-related scripts and want to understand the ecosystem.

---

## 🛠️ Tools & Scripts

### Validation Script
**File**: `scripts/validate-task-system.py`

**Purpose**: Check task system health and flag issues

**Run**:
```bash
python3 scripts/validate-task-system.py
```

**Output**:
- ✅ Validation passed (exit code 0)
- ⚠️ Warnings found (exit code 0, review recommended)
- ❌ Critical issues (exit code 1, fix immediately)

---

### Core Service
**File**: `shared/client_tasks_service.py`

**Purpose**: Authoritative service for all task operations

**Usage**:
```python
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()

# See TASK-SYSTEM-COMPLETE-GUIDE.md for full API reference
```

---

### Task Manager HTML
**Files**:
- `tasks-overview.html` (by client)
- `tasks-overview-priority.html` (by priority)

**Generate**:
```bash
python3 generate-all-task-views.py
```

**View**:
```bash
open tasks-overview.html
```

---

## 📋 Quick Reference

### File Locations
```
✅ clients/{client}/tasks.json        ← All tasks go here
✅ clients/{client}/tasks-completed.md ← Completed tasks archive
❌ clients/{client}/product-feeds/...  ← Never put tasks here
```

### Two Independent Systems
```
Internal Task System (tasks.json)
  - Purpose: Client work
  - Storage: JSON files
  - Service: ClientTasksService
  - No sync with Google Tasks

Google Tasks (via API)
  - Purpose: Personal reminders
  - Storage: Google Tasks API
  - Service: MCP server
  - No sync with internal system
```

### Priority Levels
- **P0**: Urgent (today)
- **P1**: High (this week)
- **P2**: Normal (this month)
- **P3**: Low (someday)

---

## 🔍 Common Issues & Solutions

| Issue | Solution | Documentation |
|-------|----------|---------------|
| Tasks not appearing | Check file location & regenerate HTML | [README](TASK-SYSTEM-README.md#troubleshooting) |
| Tasks in wrong folder | Run validation script, migrate if needed | [Complete Guide](TASK-SYSTEM-COMPLETE-GUIDE.md#troubleshooting) |
| Completed tasks still showing | Use `complete_task()` not `update_task()` | [README](TASK-SYSTEM-README.md#completed-task-still-showing) |
| Task appearing twice | Check for duplicate files | [Complete Guide](TASK-SYSTEM-COMPLETE-GUIDE.md#problem-tasks-appearing-twice) |
| JSON validation errors | Use `python3 -m json.tool` | [Complete Guide](TASK-SYSTEM-COMPLETE-GUIDE.md#check-2-is-the-json-valid) |

---

## 🚨 Critical Don'ts

1. **DON'T** put tasks in `product-feeds/` folders
2. **DON'T** assume internal tasks sync with Google Tasks
3. **DON'T** edit `client_tasks_service.py` unless fixing bugs
4. **DON'T** manually mark tasks as completed (use `complete_task()`)
5. **DON'T** commit tasks.json files in product-feeds folders

---

## ✅ Best Practices

1. **DO** use `ClientTasksService` for all programmatic operations
2. **DO** run validation regularly: `python3 scripts/validate-task-system.py`
3. **DO** complete tasks properly so they're archived to `tasks-completed.md`
4. **DO** check backup daily: tasks are backed up to `backups/tasks/` at 6am
5. **DO** use internal tasks for client work, Google Tasks for personal

---

## 📞 Getting Help

### Step 1: Check Documentation
1. Quick issue? → [README](TASK-SYSTEM-README.md)
2. Complex issue? → [Complete Guide](TASK-SYSTEM-COMPLETE-GUIDE.md)
3. Script question? → [Scripts Audit](TASKS-SCRIPTS-AUDIT-2025-11-26.md)

### Step 2: Run Validation
```bash
python3 scripts/validate-task-system.py
```

### Step 3: Check Backups
```bash
ls -lh backups/tasks/
```

### Step 4: Search History
```bash
# Search completed tasks
grep -r "search term" clients/*/tasks-completed.md

# Check migration docs
cat docs/MIGRATION-COMPLETE-2025-11-26.md
```

---

## 📅 Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Validate system | Weekly | `python3 scripts/validate-task-system.py` |
| Review completed tasks | Monthly | Check `tasks-completed.md` files |
| Clean up old completed | Quarterly | `python3 shared/scripts/cleanup-completed-tasks.py` |
| Verify backups | Weekly | Check `backups/tasks/` folder |

---

## 🔄 Update History

| Date | Change | Documentation |
|------|--------|---------------|
| 2025-12-19 | **Task Manager User Manual** created | [User Manual](TASK-MANAGER-USER-MANUAL.md) ⭐ |
| 2025-12-19 | Backup Safety System documented | [Backup System](BACKUP-SAFETY-SYSTEM.md) |
| 2025-12-19 | Critical data loss incident documented | [Incidents](INCIDENTS.md) |
| 2025-11-26 | Complete documentation created | All files in this index |
| 2025-11-26 | Migration from product-feeds to root | [Migration doc](MIGRATION-COMPLETE-2025-11-26.md) |
| 2025-11-26 | Validation script created | `scripts/validate-task-system.py` |

---

**Next Review**: 2026-01-19 (or after any structural changes)
**Maintained By**: Claude Code & PetesBrain Documentation Team
**Contact**: See main README for support
