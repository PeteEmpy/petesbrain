# Task System Safety Rules

**CRITICAL: READ BEFORE ANY TASK OPERATIONS**

## Rules for Claude Code

### 1. NEVER Restore from Backups Without User Approval
- If task files are missing, STOP and ask the user
- If data seems corrupted, STOP and ask the user
- NEVER blindly restore from old backups
- ALWAYS show the user what will be overwritten before proceeding

### 2. ALWAYS Create Backup Before Destructive Operations
Before any operation that modifies multiple task files:
```python
# Create timestamped backup
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_dir = Path(f'/Users/administrator/Documents/PetesBrain/data/backups/tasks-{timestamp}')
backup_dir.mkdir(parents=True, exist_ok=True)

# Copy ALL task files
for task_file in clients_dir.glob('*/tasks.json'):
    shutil.copy2(task_file, backup_dir / f'{task_file.parent.name}.json')
```

### 3. Source of Truth: Per-Client Files
- **CORRECT**: `clients/{client}/tasks.json` (one file per client)
- **LEGACY**: `data/state/client-tasks.json` (OLD, do not use)
- **Authority**: ClientTasksService at `shared/client_tasks_service.py`

### 4. Before Processing Manual Notes
```python
# 1. List tasks that will be modified
print("Tasks to be completed:")
for note in manual_notes:
    print(f"  - {note['client']}: {note['task_title']}")

# 2. Create backup
# (see rule #2)

# 3. Process notes

# 4. Verify success
print("\nVerify these completions in the UI before clearing manual-task-notes.json")
```

### 5. Generator Scripts Must Be Defensive
```python
# ALWAYS handle missing 'type' field
if 'type' not in task:
    task['type'] = 'standalone'

# ALWAYS use .get() for optional fields
task.get('priority', 'P2')
task.get('due_date') or '9999-12-31'
```

### 6. Data Loss Prevention Checklist
Before running ANY script that touches tasks:
- [ ] Do I understand what data currently exists?
- [ ] Do I need to back it up first?
- [ ] Am I about to overwrite current data with old data?
- [ ] Have I asked the user for approval if uncertain?

## What Went Wrong (Nov 19, 2025)

1. User provided 4 manual task notes to process
2. I completed 3 tasks using ClientTasksService (wrote to per-client files)
3. I ran the generator scripts which expected per-client files
4. Generator failed because files were missing/empty
5. **CRITICAL ERROR**: I found an old centralized backup from Nov 18
6. **CRITICAL ERROR**: I restored from it WITHOUT checking timestamps
7. **CRITICAL ERROR**: I overwrote the 3 task completions just made
8. Result: Data loss, user frustration, broken trust

## Never Again

**Stop. Think. Ask. Backup. Then act.**
