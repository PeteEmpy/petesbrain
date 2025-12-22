# Google Tasks Deprecation Plan

**Date**: 2025-12-16
**Status**: Planning Phase
**Risk Level**: Medium (affects multiple agents, minimal user-facing impact)

---

## Executive Summary

This document outlines the complete deprecation of Google Tasks integration in PetesBrain. The internal task system (`clients/{client}/tasks.json`) has become the single source of truth for client work, making the Google Tasks integration redundant and potentially confusing.

**Key Decision**: Migrate to internal tasks-only system, deprecate all Google Tasks functionality.

**Timeline**: 2-3 hours implementation + 1 week monitoring

**Risk**: Low - Google Tasks was only used for AI suggestions and personal reminders, never for critical client work

---

## Current State Analysis

### Google Tasks Content (As of 2025-12-16)

**Total Active Tasks**: 34 tasks across 3 lists

#### List: "Client Work" (10 tasks)

| Task | Due Date | Status | Action |
|------|----------|--------|--------|
| [NMA] Review Demographic Bid Adjustments | 2026-01-11 | Active | **MIGRATE** - Future due date |
| [Crowd Control] Check Feed Re-approval Status | 2025-12-11 | Overdue 5d | **MIGRATE** - Recent overdue |
| [Tree2mydoor] Re-analyse ROAS experiment | 2025-12-04 | Overdue 12d | **DISCARD** - Stale |
| [Tree2mydoor] REVERT ROAS | 2025-12-02 | Completed | **DISCARD** - Already done |
| [Superspace] Regenerate orders timeline chart | 2025-11-25 | Overdue 21d | **DISCARD** - Stale |
| [Tree2mydoor] Review brand campaign consolidation | 2025-12-24 | Active | **MIGRATE** - Future due date |
| [Devonshire] Investigate zero conversion tracking | 2025-11-29 | Overdue 17d | **DISCARD** - Stale |
| [Devonshire] Analyse Beeley Inn keywords | 2025-11-27 | Overdue 19d | **DISCARD** - Stale |
| [Smythson] Remove Black Friday messaging | 2025-12-02 | Overdue 14d | **DISCARD** - Event passed |
| [Grain Guard] run weekly report | No due date | Active | **MIGRATE** - Recurring task |

**Tasks to Migrate from "Client Work"**: 4 tasks
**Tasks to Discard**: 6 tasks

#### List: "Client Action Items" (24 tasks)

**Analysis**: Mostly meeting action items from Dec 10, 2025 meetings. Need individual review.

**Estimated**: 8-10 tasks to migrate, 14-16 to discard (duplicates or already in internal system)

#### List: "Peter's List" (Unknown count)

**Status**: Not yet retrieved
**Expected**: Personal tasks, medication reminders, non-client work

**Action**: Export for archive, then delete (personal reminders can use Apple Reminders instead)

---

## Agents Affected

### 1. **granola-google-docs-importer** (MEDIUM IMPACT)

**File**: `/agents/granola-google-docs-importer/granola-google-docs-importer.py`

**Current Behaviour**:
- Imports Granola meeting notes from Google Docs
- Extracts action items
- Creates Google Tasks in "Client Action Items" list

**Required Changes**:
- Remove `GoogleTasksClient` import
- Remove `create_google_tasks()` method (lines 48-88 approx)
- Remove Google Tasks creation logic from main flow
- Action items will be saved to markdown files only

**Risk**: LOW - Meeting notes still saved to client folders, just no automatic task creation

---

### 2. **ai-inbox-processor** (LOW IMPACT)

**File**: `/agents/ai-inbox-processor/ai-inbox-processor.py`

**Current Behaviour**:
- Processes notes from `!inbox/`
- Can create tasks in BOTH Google Tasks and internal system
- Uses Google Tasks for AI-suggested tasks

**Required Changes**:
- Remove `GoogleTasksClient` import (line 58)
- Remove Google Tasks creation code paths
- Keep internal task creation only
- Update logic to use `ClientTasksService` exclusively

**Risk**: LOW - Internal task system already primary

---

### 3. **sync-todos-to-google-tasks** (HIGH IMPACT - DEPRECATE)

**File**: `/agents/sync-todos-to-google-tasks/sync-todos-to-google-tasks.py`
**LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.sync-todos-to-google-tasks.plist`

**Current Behaviour**:
- Syncs local `todo/*.md` files to Google Tasks
- Runs every hour via LaunchAgent
- Tracks sync state in `shared/data/todo-sync-state.json`

**Required Changes**:
- **DEPRECATE ENTIRE AGENT** - No replacement needed
- Unload LaunchAgent
- Archive agent code
- Delete sync state file

**Risk**: MEDIUM - Agent currently running (exit code 0), but `todo/` directory contains 52 files (mostly old enhanced wispr notes, not active todos)

---

### 4. **tasks-backup** (LOW IMPACT)

**File**: `/agents/tasks-backup/tasks-backup.py`

**Current Behaviour**:
- Backs up `clients/*/tasks.json` files
- Also exports Google Tasks to JSON for backup

**Required Changes**:
- Remove `export_google_tasks()` function
- Remove Google Tasks from tarball creation
- Keep internal tasks backup only

**Risk**: LOW - Google Tasks backup was secondary, internal tasks remain backed up

---

### 5. **daily-intel-report** (LOW IMPACT)

**File**: `/agents/daily-intel-report/daily-intel-report.py`

**Current Behaviour**:
- Generates morning briefing
- May reference Google Tasks in some versions

**Required Changes**:
- Remove any Google Tasks imports/references
- Use internal task system only for task counts

**Risk**: LOW - Internal task system already used for client work

---

## Skills Affected

### 1. **granola-importer** skill

**File**: `.claude/skills/granola-importer/skill.md`

**Current**: Includes `mcp__google-tasks__create_task` in allowed tools

**Change**: Remove Google Tasks MCP tool from allowed list

---

### 2. **messaging-processor** skill

**File**: `.claude/skills/messaging-processor/skill.md`

**Current**: Includes Google Tasks MCP tools

**Change**: Remove Google Tasks MCP tools, use internal tasks only

---

### 3. **google-ads-weekly-report** skill

**File**: `.claude/skills/google-ads-weekly-report/skill.md`

**Current**: Creates tasks using `service.create_task()` (ClientTasksService)

**Change**: NONE - Already using internal system correctly

---

## Utility Scripts Affected

**Scripts to archive** (no longer needed):

1. `shared/retroactive-task-creator.py` - Creates Google Tasks retroactively
2. `shared/deduplicate-google-tasks.py` - Deduplicates Google Tasks
3. `shared/migrate-todos-to-google-tasks.py` - Migrates todos to Google Tasks
4. `shared/scripts/cleanup_google_tasks.py` - Cleans up Google Tasks
5. `shared/scripts/migrate_tasks_from_google.py` - Migrates FROM Google Tasks
6. `shared/scripts/update_google_task.py` - Updates Google Tasks
7. `shared/scripts/lookup-uuid.py` - Looks up Google Task IDs
8. `tools/granola-importer/generate_daily_tasks.py` - Creates Google Tasks
9. `tools/granola-importer/create_tasks_mcp.py` - MCP task creation examples
10. `tools/product-impact-analyzer/create_disapproval_tasks.py` - Creates Google Tasks for disapprovals

**Action**: Move to `_archived/google-tasks-scripts/` directory

---

## GoogleTasksClient Module

**File**: `shared/google_tasks_client.py` (588 lines)

**Action**:
- Archive to `_archived/google-tasks-client/`
- Remove from active codebase
- Update any import statements

---

## Migration Steps

### Phase 1: Pre-Migration (30 mins)

1. **Export Current Google Tasks Data**
   ```python
   # Export all Google Tasks to JSON for historical archive
   from shared.google_tasks_client import GoogleTasksClient
   client = GoogleTasksClient()

   all_tasks = client.get_all_active_tasks()

   with open('_archived/google-tasks-final-export-2025-12-16.json', 'w') as f:
       json.dump(all_tasks, f, indent=2)
   ```

2. **Analyse Tasks for Migration**
   - Review 34 tasks individually
   - Identify which need migration to internal system
   - Create migration list (estimated 12-15 tasks)

3. **Create Backup**
   - Backup current state of internal `tasks.json` files
   - Backup Google Tasks data
   - Document current LaunchAgent states

---

### Phase 2: Task Migration (45 mins)

**Migration Script**: `shared/scripts/migrate-google-tasks-final.py`

```python
#!/usr/bin/env python3
"""
Final Google Tasks Migration
Migrates selected Google Tasks to internal task system before deprecation.
"""

from shared.google_tasks_client import GoogleTasksClient
from shared.client_tasks_service import ClientTasksService

# Tasks to migrate (based on manual review)
TASKS_TO_MIGRATE = [
    {
        'google_task_id': 'xxx',
        'title': '[NMA] Review Demographic Bid Adjustments',
        'client': 'national-design-academy',
        'priority': 'P2',
        'due_date': '2026-01-11',
        'notes': 'Check if demographic bid adjustments are working correctly'
    },
    {
        'google_task_id': 'xxx',
        'title': '[Crowd Control] Check Feed Re-approval Status',
        'client': 'crowd-control',
        'priority': 'P1',
        'due_date': '2025-12-20',  # Reset to future date
        'notes': 'Check if product feed was re-approved after rejection'
    },
    # ... rest of migration list
]

def migrate_task(task_data):
    """Migrate single task from Google Tasks to internal system"""
    service = ClientTasksService()

    # Create in internal system
    service.create_task(
        title=task_data['title'],
        client=task_data['client'],
        priority=task_data['priority'],
        due_date=task_data.get('due_date'),
        notes=task_data.get('notes')
    )

    # Mark as migrated in Google Tasks (add note)
    google_client = GoogleTasksClient()
    google_client.update_task(
        task_id=task_data['google_task_id'],
        notes=f"[MIGRATED TO INTERNAL SYSTEM - {datetime.now().date()}]\n\n{task_data.get('notes', '')}"
    )

def main():
    print("=" * 60)
    print("  Final Google Tasks Migration")
    print("=" * 60)

    for i, task in enumerate(TASKS_TO_MIGRATE, 1):
        print(f"\n[{i}/{len(TASKS_TO_MIGRATE)}] Migrating: {task['title']}")
        migrate_task(task)
        print("  ✅ Migrated successfully")

    print("\n" + "=" * 60)
    print(f"✅ Migrated {len(TASKS_TO_MIGRATE)} tasks")
    print("=" * 60)

if __name__ == '__main__':
    main()
```

---

### Phase 3: Code Changes (60 mins)

**Step 1: Update Granola Importer**
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/granola-google-docs-importer
# Edit granola-google-docs-importer.py
# Remove GoogleTasksClient import and create_google_tasks() method
```

**Step 2: Update AI Inbox Processor**
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/ai-inbox-processor
# Edit ai-inbox-processor.py
# Remove GoogleTasksClient import and Google Tasks creation logic
```

**Step 3: Deprecate Sync Agent**
```bash
# Unload LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.petesbrain.sync-todos-to-google-tasks.plist

# Archive agent
mkdir -p _archived/google-tasks-agents
mv agents/sync-todos-to-google-tasks _archived/google-tasks-agents/

# Archive plist
mv ~/Library/LaunchAgents/com.petesbrain.sync-todos-to-google-tasks.plist \
   _archived/google-tasks-agents/
```

**Step 4: Update Tasks Backup**
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/tasks-backup
# Edit tasks-backup.py
# Remove export_google_tasks() function
```

**Step 5: Update Skills**
```bash
# Edit .claude/skills/granola-importer/skill.md
# Remove mcp__google-tasks__create_task from allowed tools

# Edit .claude/skills/messaging-processor/skill.md
# Remove Google Tasks MCP tools
```

**Step 6: Archive Utility Scripts**
```bash
mkdir -p _archived/google-tasks-scripts
mv shared/retroactive-task-creator.py _archived/google-tasks-scripts/
mv shared/deduplicate-google-tasks.py _archived/google-tasks-scripts/
mv shared/migrate-todos-to-google-tasks.py _archived/google-tasks-scripts/
mv shared/scripts/cleanup_google_tasks.py _archived/google-tasks-scripts/
mv shared/scripts/migrate_tasks_from_google.py _archived/google-tasks-scripts/
mv shared/scripts/update_google_task.py _archived/google-tasks-scripts/
mv shared/scripts/lookup-uuid.py _archived/google-tasks-scripts/
mv tools/granola-importer/generate_daily_tasks.py _archived/google-tasks-scripts/
mv tools/granola-importer/create_tasks_mcp.py _archived/google-tasks-scripts/
mv tools/product-impact-analyzer/create_disapproval_tasks.py _archived/google-tasks-scripts/
```

**Step 7: Archive GoogleTasksClient**
```bash
mkdir -p _archived/google-tasks-client
mv shared/google_tasks_client.py _archived/google-tasks-client/
```

---

### Phase 4: Verification (30 mins)

1. **Test Agent Health**
   ```bash
   # Check all affected agents still run
   launchctl list | grep petesbrain

   # Check logs for errors
   tail -50 ~/.petesbrain-granola-google-docs-importer.log
   tail -50 ~/.petesbrain-ai-inbox-processor.log
   tail -50 ~/.petesbrain-tasks-backup.log
   ```

2. **Verify Internal Tasks Work**
   ```python
   from shared.client_tasks_service import ClientTasksService
   service = ClientTasksService()

   # Create test task
   service.create_task(
       title='[TEST] Verify internal tasks work',
       client='roksys',
       priority='P3'
   )

   # List tasks
   tasks = service.list_tasks(client='roksys')
   print(f"Found {len(tasks)} tasks")

   # Complete test task
   test_task = [t for t in tasks if 'TEST' in t['title']][0]
   service.complete_task(client='roksys', task_id=test_task['id'])
   ```

3. **Check Skills Still Work**
   ```bash
   # Test granola-importer skill (should work without Google Tasks)
   # Test messaging-processor skill (should use internal tasks only)
   ```

---

### Phase 5: Documentation Updates (15 mins)

1. **Update CLAUDE.md**
   - Remove Google Tasks references from task management section
   - Update dual task system note to reflect deprecation
   - Update task-related examples

2. **Update Task System Documentation**
   - Update `docs/TASK-SYSTEM-DECISION-GUIDE.md`
   - Update `docs/INTERNAL-TASK-SYSTEM.md`
   - Remove Google Tasks sections

3. **Update Skills Documentation**
   - Update `.claude/skills/README.md`
   - Remove Google Tasks MCP tool references

---

## Rollback Plan

**If issues occur during migration:**

1. **Restore Google Tasks Client**
   ```bash
   mv _archived/google-tasks-client/google_tasks_client.py shared/
   ```

2. **Restore Sync Agent**
   ```bash
   mv _archived/google-tasks-agents/sync-todos-to-google-tasks agents/
   mv _archived/google-tasks-agents/com.petesbrain.sync-todos-to-google-tasks.plist \
      ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.petesbrain.sync-todos-to-google-tasks.plist
   ```

3. **Restore Agent Code**
   - Revert changes to granola-google-docs-importer.py
   - Revert changes to ai-inbox-processor.py
   - Revert changes to tasks-backup.py

4. **Restore Skills**
   - Revert changes to granola-importer/skill.md
   - Revert changes to messaging-processor/skill.md

---

## Post-Migration Cleanup

**After 1 week of successful operation:**

1. **Delete Google Tasks Data** (Optional - keep for historical archive)
   - Export final snapshot
   - Delete all tasks from Google Tasks UI
   - Keep archived JSON export

2. **Remove Google Tasks MCP Server** (Optional)
   ```bash
   # Remove from .mcp.json
   # Delete infrastructure/mcp-servers/google-tasks-mcp-server/
   ```

3. **Clean Up State Files**
   ```bash
   rm shared/data/todo-sync-state.json
   ```

---

## Risk Assessment

### Low Risk Areas

- **Internal task system**: Already stable and in active use
- **Tasks backup**: Only removes Google Tasks export (internal backup remains)
- **Skills**: Minimal changes (just remove unused tools)

### Medium Risk Areas

- **Granola importer**: Loses automatic task creation, but meeting notes still saved
- **AI inbox processor**: Dual functionality being simplified
- **Sync agent deprecation**: Agent currently running, but syncing to unused `todo/` directory

### High Risk Areas

- **None identified** - No critical dependencies on Google Tasks

### Mitigation Strategies

1. **Test in dev environment first** (if available)
2. **Migrate tasks in small batches** (not all at once)
3. **Keep Google Tasks data for 1 month** before deletion
4. **Monitor agent logs closely** for 1 week post-migration
5. **Keep rollback plan ready** for 2 weeks

---

## Success Criteria

Migration is successful when:

1. ✅ All relevant tasks migrated to internal system
2. ✅ All affected agents running without errors
3. ✅ No Google Tasks references in active code
4. ✅ Skills work correctly with internal tasks only
5. ✅ Task creation/completion/listing all work
6. ✅ No agent failures for 1 week post-migration

---

## Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| **Pre-Migration** | 30 mins | Export data, analyse tasks, create backups |
| **Task Migration** | 45 mins | Run migration script, verify migrations |
| **Code Changes** | 60 mins | Update agents, skills, archive scripts |
| **Verification** | 30 mins | Test agents, verify functionality |
| **Documentation** | 15 mins | Update docs, CLAUDE.md |
| **Monitoring** | 1 week | Watch logs, verify stability |
| **Cleanup** | 15 mins | Remove archived code (after 1 week) |

**Total Active Time**: ~3 hours
**Total Timeline**: 1-2 weeks (including monitoring period)

---

## Appendices

### Appendix A: Complete File List

**Files to Modify**:
- `/agents/granola-google-docs-importer/granola-google-docs-importer.py`
- `/agents/ai-inbox-processor/ai-inbox-processor.py`
- `/agents/tasks-backup/tasks-backup.py`
- `/.claude/skills/granola-importer/skill.md`
- `/.claude/skills/messaging-processor/skill.md`
- `/.claude/CLAUDE.md`
- `/docs/TASK-SYSTEM-DECISION-GUIDE.md`
- `/docs/INTERNAL-TASK-SYSTEM.md`
- `/.claude/skills/README.md`

**Files to Archive**:
- `/shared/google_tasks_client.py` → `_archived/google-tasks-client/`
- `/agents/sync-todos-to-google-tasks/` → `_archived/google-tasks-agents/`
- `~/Library/LaunchAgents/com.petesbrain.sync-todos-to-google-tasks.plist` → `_archived/`
- 10 utility scripts → `_archived/google-tasks-scripts/`

**Files to Delete** (after 1 week):
- `/shared/data/todo-sync-state.json`
- (Optional) Google Tasks MCP server

---

### Appendix B: Migration Script Template

See **Phase 2: Task Migration** above for complete migration script.

---

### Appendix C: Google Tasks Export Format

```json
{
  "task_id": "xxx",
  "title": "[Client] Task title",
  "notes": "Task notes/details",
  "due": "2025-12-20T00:00:00.000Z",
  "status": "needsAction",
  "list_name": "Client Work",
  "list_id": "xxx",
  "updated": "2025-12-16T10:00:00.000Z",
  "created": "2025-12-10T15:00:00.000Z"
}
```

---

## Conclusion

This deprecation plan provides a safe, methodical approach to removing Google Tasks from PetesBrain. The internal task system is already the primary source of truth, making this migration low-risk. By following the phased approach and maintaining rollback capability, we can safely consolidate to a single task management system.

**Next Steps**:

1. User review and approval of this plan
2. Schedule migration window (recommended: weekend morning)
3. Execute Phase 1 (Pre-Migration)
4. Proceed with remaining phases sequentially

---

**Document Version**: 1.0
**Last Updated**: 2025-12-16
**Author**: Claude (PetesBrain AI Assistant)
