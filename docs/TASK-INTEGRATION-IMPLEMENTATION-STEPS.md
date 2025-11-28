# Task Integration Implementation Steps

**Quick Reference Guide for Developers**

This document provides step-by-step implementation instructions for the task system integration. For full architectural details, see [TASK-INTEGRATION-ARCHITECTURE.md](TASK-INTEGRATION-ARCHITECTURE.md).

---

## Phase 1: Core Integration (Week 1)

### Step 1: Create "Client Work" Task List

**Action:** Manually create task list in Google Tasks or via script

```bash
# Option A: Manual (via Google Tasks web/mobile app)
# 1. Open Google Tasks
# 2. Create new list called "Client Work"
# 3. Note the list ID from URL or API

# Option B: Automated setup script
python3 shared/scripts/setup_ai_task_list.py
```

**Expected Output:**
- Task list "Client Work" created
- List ID stored in `shared/data/ai-task-list-id.txt`

---

### Step 2: Create Configuration File

**File:** `shared/config/ai-tasks-config.json`

```bash
cat > shared/config/ai-tasks-config.json << 'JSONEOF'
{
  "task_list_id": "REPLACE_WITH_ACTUAL_ID",
  "task_list_name": "Client Work",
  "duplicate_detection": {
    "enabled": true,
    "similarity_threshold": 0.80,
    "lookback_days": 7,
    "completed_grace_period_days": 3
  },
  "due_date_mapping": {
    "P0": 0,
    "P1": 1,
    "P2": 3
  }
}
JSONEOF
```

Replace `REPLACE_WITH_ACTUAL_ID` with actual list ID.

---

### Step 3: Create Duplicate Detection Module

**File:** `shared/scripts/duplicate_task_detector.py`

Key functions to implement:

1. `calculate_similarity(str1: str, str2: str) -> float`
   - Uses `difflib.SequenceMatcher`
   - Returns 0.0 to 1.0

2. `is_same_client(task: Dict, client_name: str) -> bool`
   - Checks if task belongs to client
   - Looks for `**Client:** {client_name}` in notes

3. `is_duplicate_task(new_task: Dict, existing_tasks: List[Dict], config: Dict) -> tuple[bool, Optional[Dict]]`
   - Main duplicate detection logic
   - Returns (is_duplicate, matching_task)

4. `get_recent_tasks(task_list_id: str, lookback_days: int) -> List[Dict]`
   - Queries Google Tasks for recent tasks
   - Filters by creation date

**Testing:**

```bash
# Run unit tests
python3 -m pytest tests/test_duplicate_detection.py -v
```

---

### Step 4: Create AI Task Creator Module

**File:** `shared/scripts/ai_task_creator.py`

Key functions to implement:

1. `format_task_metadata(task: Dict) -> str`
   - Formats notes with AI metadata
   - Includes: Source, Client, Priority, Time Estimate, Reason, AI Task ID

2. `assign_due_date(task: Dict) -> str`
   - Maps priority to due date
   - P0=today, P1=tomorrow, P2=3 days
   - Checks for urgency keywords

3. `create_ai_generated_task(task: Dict, task_list_id: str, google_tasks_client) -> Dict`
   - Creates task in Google Tasks
   - Formats title with client prefix: `[Client Name] Task description`
   - Returns created task with ID

**Testing:**

```bash
# Run unit tests
python3 -m pytest tests/test_ai_task_creator.py -v
```

---

### Step 5: Modify Daily Client Work Generator

**File:** `shared/scripts/daily-client-work-generator.py`

**Changes:**

1. Add imports at top of file:

```python
import sys
from pathlib import Path
import json

# Add MCP imports
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-servers" / "google-tasks-mcp-server"))
from tasks_service import tasks_service

# Add new module imports
from duplicate_task_detector import is_duplicate_task, get_recent_tasks
from ai_task_creator import create_ai_generated_task

# Load config
CONFIG_FILE = Path(__file__).parent.parent / "config" / "ai-tasks-config.json"
with open(CONFIG_FILE, 'r') as f:
    AI_TASKS_CONFIG = json.load(f)
```

2. After line 315 (after saving JSON), add:

```python
# Create Google Tasks (Phase 1 integration)
CREATE_GOOGLE_TASKS = True  # Set to False to disable

if CREATE_GOOGLE_TASKS:
    print()
    print("=" * 80)
    print("CREATING GOOGLE TASKS")
    print("=" * 80)
    print()
    
    try:
        # Connect to Google Tasks
        tasks_client = tasks_service()
        task_list_id = AI_TASKS_CONFIG['task_list_id']
        
        # Get recent tasks for duplicate detection
        lookback_days = AI_TASKS_CONFIG['duplicate_detection']['lookback_days']
        existing_tasks = get_recent_tasks(task_list_id, lookback_days)
        print(f"📋 Found {len(existing_tasks)} recent tasks for duplicate detection")
        print()
        
        # Create tasks
        tasks_created = 0
        duplicates_skipped = 0
        
        for task in all_tasks:
            # Check for duplicates
            is_dup, matching_task = is_duplicate_task(task, existing_tasks, AI_TASKS_CONFIG)
            
            if is_dup:
                duplicates_skipped += 1
                print(f"   ⏭  Skipped duplicate: [{task['client']}] {task['task']}")
                continue
            
            # Create task
            try:
                created_task = create_ai_generated_task(task, task_list_id, tasks_client)
                tasks_created += 1
                print(f"   ✓ Created: [{task['client']}] {task['task']} (Due: {created_task.get('due', 'N/A')})")
            except Exception as e:
                print(f"   ⚠️  Error creating task: {e}")
        
        print()
        print(f"✅ {tasks_created} task(s) created in Google Tasks")
        print(f"⏭  {duplicates_skipped} duplicate(s) skipped")
        
    except Exception as e:
        print(f"❌ Error creating Google Tasks: {e}")
        print("   Falling back to JSON-only mode")
```

3. Test run:

```bash
# Run manually to test
python3 shared/scripts/daily-client-work-generator.py
```

---

### Step 6: Modify Daily Briefing

**File:** `agents/reporting/daily-briefing.py`

**Changes:**

1. Modify `get_client_work_for_today()` function (around line 159):

```python
def get_client_work_for_today():
    """Get AI-generated client work from Google Tasks."""
    
    # Try Google Tasks first (Phase 1 integration)
    try:
        sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-tasks-mcp-server'))
        from tasks_service import tasks_service
        
        # Load config
        config_file = PROJECT_ROOT / 'shared' / 'config' / 'ai-tasks-config.json'
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        task_list_id = config['task_list_id']
        service = tasks_service()
        
        # Get tasks from "Client Work" list
        results = service.tasks().list(
            tasklist=task_list_id,
            showCompleted=False,  # Only show incomplete
            maxResults=100
        ).execute()
        
        items = results.get('items', [])
        
        if not items:
            return ""
        
        # Filter to today's tasks (due date = today)
        today = datetime.now().date()
        today_tasks = []
        
        for item in items:
            due = item.get('due')
            if due:
                try:
                    due_date = datetime.fromisoformat(due.replace('Z', '+00:00')).date()
                    if due_date == today:
                        today_tasks.append(item)
                except:
                    pass
        
        if not today_tasks:
            return ""
        
        # Format output (similar to current JSON format)
        output = "## 🎯 Client Work for Today\n\n"
        output += f"**{len(today_tasks)} AI-generated task(s)** from Google Tasks\n\n"
        
        # Group by priority (extract from notes)
        p0_tasks = []
        p1_tasks = []
        p2_tasks = []
        
        for task in today_tasks:
            notes = task.get('notes', '')
            if '**Priority:** P0' in notes:
                p0_tasks.append(task)
            elif '**Priority:** P1' in notes:
                p1_tasks.append(task)
            else:
                p2_tasks.append(task)
        
        if p0_tasks:
            output += "### 🔴 URGENT (P0)\n\n"
            for task in p0_tasks:
                title = task.get('title', 'Untitled')
                output += f"- {title}\n"
            output += "\n"
        
        if p1_tasks:
            output += "### 🟡 HIGH PRIORITY (P1)\n\n"
            for task in p1_tasks:
                title = task.get('title', 'Untitled')
                output += f"- {title}\n"
            output += "\n"
        
        if p2_tasks:
            output += "### ⚪ NORMAL PRIORITY (P2)\n\n"
            for task in p2_tasks:
                title = task.get('title', 'Untitled')
                output += f"- {title}\n"
        
        return output
        
    except Exception as e:
        print(f"  ⚠️  Error loading from Google Tasks: {e}")
        print("  → Falling back to JSON")
    
    # Fallback to JSON (existing code)
    work_file = PROJECT_ROOT / 'shared' / 'data' / 'daily-client-work.json'
    
    if not work_file.exists():
        return ""
    
    # ... rest of existing JSON code ...
```

2. Test briefing generation:

```bash
# Run manually
python3 agents/reporting/daily-briefing.py
```

---

### Step 7: Update LaunchAgent

**File:** `~/Library/LaunchAgents/com.petesbrain.daily-client-work.plist`

No changes needed - script should run as normal but now creates Google Tasks.

**Verify:**

```bash
# Check LaunchAgent is loaded
launchctl list | grep daily-client-work

# View logs
tail -f ~/Library/Logs/PetesBrain/daily-client-work.log
```

---

## Testing Phase 1

### Manual Testing Checklist

- [ ] **Setup Complete**
  - [ ] "Client Work" task list created
  - [ ] Config file created with correct list ID
  - [ ] Duplicate detection module created
  - [ ] AI task creator module created

- [ ] **Daily Generator**
  - [ ] Run manually: `python3 shared/scripts/daily-client-work-generator.py`
  - [ ] Verify tasks created in Google Tasks
  - [ ] Check no duplicates on second run
  - [ ] Verify client prefixes in titles
  - [ ] Verify due dates assigned correctly (P0=today, P1=tomorrow, P2=3 days)

- [ ] **Daily Briefing**
  - [ ] Run manually: `python3 agents/reporting/daily-briefing.py`
  - [ ] Verify shows tasks from Google Tasks
  - [ ] Check fallback to JSON works if API fails

- [ ] **Integration**
  - [ ] Complete one AI task in Google Tasks
  - [ ] Verify `tasks-monitor.py` detects completion
  - [ ] Check task saved to `clients/{client}/tasks-completed.md`
  - [ ] Verify CONTEXT.md updated

### Automated Testing

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test suites
python3 -m pytest tests/test_duplicate_detection.py -v
python3 -m pytest tests/test_ai_task_creator.py -v
python3 -m pytest tests/integration/test_daily_generation.py -v
```

---

## Phase 1 Success Criteria

✅ **Checklist:**

- [ ] 100% of AI tasks created in Google Tasks
- [ ] <5% duplicate rate
- [ ] Daily briefing shows tasks from Google Tasks (with JSON fallback)
- [ ] Tasks have correct due dates
- [ ] Completed tasks update CONTEXT.md
- [ ] No errors in logs for 3 consecutive days
- [ ] User reports workflow improvement

---

## Rollback Procedure

If Phase 1 fails:

1. **Immediate:**
   ```python
   # In daily-client-work-generator.py
   CREATE_GOOGLE_TASKS = False  # Disable Google Tasks creation
   ```

2. **Revert daily briefing:**
   - Remove Google Tasks integration
   - Use JSON-only version

3. **Clean up:**
   ```bash
   # Manually delete all tasks from "Client Work" list
   # Or run cleanup script
   python3 shared/scripts/cleanup_ai_tasks.py
   ```

4. **Investigate:**
   - Check logs: `~/Library/Logs/PetesBrain/daily-client-work.log`
   - Check daily briefing logs
   - Review Google Tasks API quota usage

---

## Next Steps

After Phase 1 is stable (1 week):

1. **Phase 2: Enhanced Features**
   - Implement semantic similarity (fuzzy matching)
   - Add AI Task ID tracking
   - Improve CONTEXT.md integration

2. **Phase 3: Advanced Intelligence**
   - Task priority escalation
   - Client context integration
   - Weekly task review

3. **Phase 4: Cleanup**
   - Deprecate JSON system
   - Add monitoring dashboard
   - Performance optimization

---

## Troubleshooting

### Issue: Duplicate tasks created

**Diagnosis:**
```bash
# Check duplicate detection config
cat shared/config/ai-tasks-config.json | grep similarity_threshold
```

**Fix:**
- Lower threshold: `0.80` → `0.75`
- Increase lookback days: `7` → `14`

---

### Issue: Tasks not appearing in daily briefing

**Diagnosis:**
```bash
# Check if tasks exist in Google Tasks
python3 -c "
from tasks_service import tasks_service
import json
with open('shared/config/ai-tasks-config.json') as f:
    config = json.load(f)
service = tasks_service()
results = service.tasks().list(tasklist=config['task_list_id']).execute()
print(f\"Found {len(results.get('items', []))} tasks\")
"
```

**Fix:**
- Verify task list ID in config
- Check API credentials
- Review daily briefing logs

---

### Issue: API quota exceeded

**Diagnosis:**
```bash
# Check API usage
# View logs for rate limit errors
grep "quota" ~/Library/Logs/PetesBrain/*.log
```

**Fix:**
- Implement caching
- Reduce polling frequency
- Batch operations

---

## Support & Questions

**Documentation:**
- Architecture: `docs/TASK-INTEGRATION-ARCHITECTURE.md`
- Troubleshooting: `docs/AI-TASK-TROUBLESHOOTING.md` (TBD)

**Contact:**
- System Owner: Peter Empson (petere@roksys.co.uk)

---

**Last Updated:** 2025-11-11
