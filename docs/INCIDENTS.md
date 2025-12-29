# PetesBrain System Incidents

**Purpose**: Historical record of system failures, root cause analysis, and prevention measures

---

## Task Completion Without Authorization (December 29, 2025)

**Incident ID**: TASK-COMPLETE-2025-12-29
**Severity**: 🟡 MEDIUM - Protocol violation, caught before execution
**Status**: ✅ RESOLVED - Protocol updated and committed
**Impact**: Nearly completed task without user authorization

### Summary

Manual note "How are these terms tracking?" was interpreted as instruction to complete task after investigation. User caught and stopped the process before completion occurred. Protocol updated to explicitly require completion authorization.

### What Happened

**Trigger**: User added manual note via Task Manager UI:
```json
{
  "task_id": "75b6a014-3f38-44d7-b4cd-6281ecae5d6f",
  "client": "clear-prospects",
  "task_title": "[Clear Prospects] Review Tier 2 monitoring terms (8 terms auto-tracked)",
  "manual_note": "How are these terms tracking?"
}
```

**Expected Behavior**:
1. Investigate Tier 2 terms performance ✅
2. Report findings to user ✅
3. Leave task open for user to review findings ✅

**Actual Behavior**:
1. Investigated Tier 2 terms performance ✅ (correct)
2. Reported findings to user ✅ (correct)
3. Attempted to complete task ❌ (incorrect - no completion requested)
4. User caught and stopped before completion ✅

### Root Cause

**Ambiguous protocol wording** in `.claude/CLAUDE.md` lines 420-430 (old version):

```
**B) Instruction to Execute** (Contains action verbs)
- STOP - DO NOT just add as note
- EXECUTE the instruction FIRST
- Verify the result
- **THEN** complete the task (if instruction says "then complete")
- Log execution details to tasks-completed.md
```

**The problem**:
- "THEN complete the task" appeared to be default action
- "(if instruction says 'then complete')" was in parentheses (optional-looking)
- No explicit categories for Questions vs Instructions-without-completion
- Action verbs "Check", "Review", "Investigate" could be either type

### Resolution Applied

✅ **Updated `.claude/CLAUDE.md` lines 407-472** with explicit completion rules:

**Added 🚨 CRITICAL RULE header**:
```
Tasks can ONLY be completed in these TWO ways:
1. User clicks "Complete" button in Task Manager UI (automatic)
2. Manual note explicitly says to complete it (e.g., "Done", "Complete", "Close it", "then complete")
```

**Replaced 3-category system with 5-category decision tree**:
- A) Explicit Completion → Complete ✅
- B) Conditional Completion → Execute then complete ✅
- **C) Question/Investigation** → Execute, report, **DO NOT complete** ❌
- **D) Instruction WITHOUT Completion** → Execute, report, **DO NOT complete** ❌
- E) Comment → Add note, DO NOT complete ❌

**Added specific example**:
```
| "How are these terms tracking?" | 1. Investigate 2. Report findings | ❌ NO |
```

### Prevention Measures

1. **Documentation**: Updated `.claude/CLAUDE.md` with unambiguous completion rules
2. **Examples**: Added 10 examples covering questions, instructions, conditional completion
3. **Headers**: Added 🚨 emoji to critical rule (impossible to miss)
4. **Incident Document**: Created `docs/TASK-COMPLETION-PROTOCOL-UPDATE-DEC-29-2025.md`
5. **Commit**: Changes committed to git with detailed explanation

### Testing Required

- Next "Process my task notes" request should follow new protocol
- Questions like "How is X?" should NOT trigger completion
- Instructions like "Review X" should NOT trigger completion
- Only "Done", "Complete", or "then complete" should trigger completion

### Files Changed

| File | Change |
|------|--------|
| `.claude/CLAUDE.md` | Lines 407-472 completely rewritten |
| `docs/TASK-COMPLETION-PROTOCOL-UPDATE-DEC-29-2025.md` | New incident document |
| `docs/INCIDENTS.md` | This entry |

**Commit**: `c275a2c` - "CRITICAL: Update task completion protocol - never complete without explicit instruction"

---

## Task Manager Cascading Failures (December 22-23, 2025)

**Incident ID**: TASK-MGR-2025-12-22-23
**Severity**: 🔴 CRITICAL - System unavailable for 24 hours
**Status**: ✅ RESOLVED - All services operational
**Impact**: Task Manager UI unavailable, HTML generation blocked, agents crashing repeatedly

### Summary

Task Manager system experienced cascading failures due to five separate overlapping issues that were incompletely addressed in the initial investigation. System now fully operational after comprehensive root cause analysis.

### Root Causes Discovered

1. **Conflicting LaunchAgents** - Three different server implementations running simultaneously, holding ports 8767 and 5002
2. **Product-Feeds File Pollution** - 18 rogue `product-feeds/tasks.json` files blocking validation (created over 2 weeks, not one-time orphans)
3. **file-organizer.py Stuck Loop** - Agent stuck at 97% CPU for 90+ minutes, actively creating product-feeds files
4. **File Permission Issues** - `tasks-manager.html` had 600 permissions preventing HTTP server from reading (HTTP 404)
5. **Investigation Gap** - Yesterday's fix claimed resolution without verification, missed systemic scope

### Key Finding: Investigation Process Failure

Initial investigation treated symptoms (server crash) rather than systemic causes (all related agents, active processes, validation blockers). "Fixed" claims were made without verification evidence:

- ❌ Claimed to delete product-feeds files, but didn't verify deletion
- ❌ Focused on new canonical server, didn't audit ALL task-related LaunchAgents
- ❌ Missed running processes (deprecated servers holding ports)
- ❌ Didn't analyse file timestamps (would have revealed ongoing creation)
- ❌ Didn't check CPU usage (would have found stuck loop)

### Resolution Applied

✅ Stopped deprecated LaunchAgents (`task-manager-server`, `task-notes-server`)
✅ Deleted all 18 product-feeds/tasks.json files (verified with filesystem check: 0 remaining)
✅ Killed stuck file-organizer process (PID 2057)
✅ Fixed file permissions (600 → 644)
✅ Restarted unified canonical server (PID 9354, both ports in one process)
✅ Verified all health endpoints responding (HTTP 200)
✅ Confirmed HTML generation works (all 3 views generated successfully)

### Prevention Measures

1. **Enhanced validation script** - Add timestamp analysis, LaunchAgent checks, process monitoring
2. **LaunchAgent registry** - Document all task-related agents to prevent conflicts
3. **Mandatory verification** - Updated Systemic Issue Protocol to require re-audit before closure
4. **file-organizer review** - Investigate infinite loop cause and add guards

### Lessons Learned

**Systemic Issues Require Systemic Audits**: When one component fails, audit ALL related components (agents, processes, files, resources), not just the obvious failure point.

**Always Verify "Fixed"**: Claims without evidence are not fixes. Every fix must include verification step (e.g., `find ... | wc -l` should show 0).

**Timestamp Forensics**: File modification times reveal active vs. orphaned issues. Multiple recent timestamps = active creation, not historical orphan.

**Full Report**: `docs/TASK-MANAGER-INCIDENT-DEC22-23-2025.md` (comprehensive timeline, investigation gaps, complete fixes)

---

## Critical Task Data Loss - December 10-19, 2025

**Severity**: 🔴 CRITICAL - Data loss across 9 days
**Status**: ✅ RESOLVED - Tasks recovered, prevention system deployed
**Impact**: 9 days of task changes lost (Dec 10-19), 15 tasks manually recovered

### What Happened

**Timeline**:
- **December 10**: Backup system began failing silently
- **December 10-19**: All backups created as 29-byte corrupt files
- **December 19**: Data loss discovered during system review
- **December 19**: Emergency recovery initiated

**Discovery**:
User noticed backup files in `~/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/` were all exactly 29 bytes - clearly corrupt.

**Backup Failure Symptoms**:
```bash
$ ls -lh ~/Library/Mobile\ Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks/
-rw-r--r--  1 administrator  staff    29B Dec 10 06:00 tasks-backup-20251210-060002.tar.gz
-rw-r--r--  1 administrator  staff    29B Dec 11 06:00 tasks-backup-20251211-060002.tar.gz
-rw-r--r--  1 administrator  staff    29B Dec 12 06:00 tasks-backup-20251212-060002.tar.gz
...
```

**Data Lost**:
- All task changes from December 10-19 (9 days)
- New tasks created from weekly reports and campaign audits
- Task completions, priority updates, notes added
- Estimated 15-25 tasks affected

### Root Cause

**Primary Cause**: LaunchAgent bash script creating corrupt tar.gz files

**Contributing Factors**:
1. **No backup verification** - Backups created without integrity checks
2. **No alerting** - Failures occurred silently (no notifications)
3. **Single backup location** - iCloud only, no redundancy
4. **No restoration testing** - Never verified backups were recoverable

**Technical Details**:
The existing LaunchAgent plist (`com.petesbrain.critical-tasks-backup.plist`) ran a bash script that failed to create valid tar archives. Possible causes:
- Path issues with `.nosync` directory migration
- Permissions problems
- Disk I/O errors during backup creation
- Bash script not handling errors properly

**Evidence of Systemic Weakness**:
```bash
# Old backup system (BROKEN)
- LaunchAgent bash script → Created 29-byte corrupt files
- No verification → Failures went unnoticed for 9 days
- No alerting → User unaware until manual check
- Single location → No backup redundancy
```

### Impact Analysis

**Immediate Impact**:
- 15 tasks recovered from weekly reports/audits (Dec 10-19)
- Unknown number of other task changes permanently lost
- 9 days of task management history missing
- Potential client work tasks lost

**Financial Impact**:
- Tasks recovered had ~£1,000/month waste reduction value:
  - Uno Lighting: £800/month savings (negative keywords)
  - Clear Prospects: £50/month savings
  - Devonshire: £677/month potential waste (Pilsley Inn)
  - Smythson: Budget optimization opportunities

**Operational Impact**:
- Hours spent on emergency recovery (December 19)
- Loss of confidence in backup systems
- Need to rebuild task context from reports

### Recovery Actions Taken

**Phase 1: Data Recovery (December 19)**

Systematically searched all task creation routes for Dec 10-19:

1. **Weekly Reports**:
   - Devonshire Hotels weekly report (Dec 15) → 1 task
   - Smythson weekly report (Dec 16) → 6 tasks
   - National Motorsports Academy demographic report (Dec 11) → 1 task

2. **Campaign Audits**:
   - Clear Prospects keyword audit (Dec 17) → 2 tasks
   - Uno Lighting AI Max investigation (Dec 17) → 3 tasks

3. **Deployment Reports**:
   - Smythson Phase IIb deployment (Dec 16) → 2 tasks

**Total Recovered**: 15 tasks across 6 clients

**Tasks by Priority**:
- P0 (Critical): 7 tasks - Budget opportunities, wasted spend, phase deployments
- P1 (High): 5 tasks - Negative keywords, monitoring, reviews
- P2 (Normal): 3 tasks - Performance analysis, tier 2 reviews

**Phase 2: Prevention System (December 19)**

Implemented **3-layer backup safety system**:

**Layer 1 - Verified Backup Creation**:
- Script: `shared/backup-verification/safe-backup.sh`
- Frequency: Every 6 hours (LaunchAgent)
- Process: Create → Verify → Store in 3 locations → Cleanup
- Locations:
  - Local: `_backups/tasks/` (30-day retention, fast access)
  - iCloud: `~/Library/Mobile Documents/.../critical-tasks/` (7-day retention)
  - Google Drive: Via existing `tasks-backup.py` agent (unlimited)

**Layer 2 - Immediate Verification**:
- Script: `shared/backup-verification/verify-backup.py`
- Checks performed:
  - File size ≥ 50KB (rejects corrupt files like 29-byte failures)
  - Tarball structure valid
  - Contains ≥ 10 client task files
  - All JSON files parseable
  - Task count within 20% of baseline
- Alerts: Written to `~/.petesbrain-backup-alerts.log`
- Baseline: Tracks expected counts in `backup-baseline.json`

**Layer 3 - Weekly Restoration Testing**:
- Script: `shared/backup-verification/weekly-backup-audit.py`
- Frequency: Every Monday 9 AM (LaunchAgent)
- Process:
  1. Find latest backup
  2. Count production tasks
  3. Count backup tasks (inside archive)
  4. Compare counts (alert if >20% difference)
  5. **Actually restore backup to temp directory**
  6. Verify all restored files are valid JSON
- Purpose: Verification can pass but restoration can still fail (permissions, paths, etc.)

**Testing Results** (December 19):
- ✅ Backup creation: 124KB, 55 tasks across 44 files
- ✅ Verification: PASSED (identified ._* macOS metadata files as warnings)
- ✅ Weekly audit: PASSED (51 production vs 55 backup, 7.8% difference)
- ✅ Restoration: Successfully extracted and validated all JSON files

### Technical Fixes Applied

**Fix 1: Encoding Robustness**

Problem: JSON files had encoding issues (UTF-16, UTF-8 with £ symbols)

```python
# Before (would crash on encoding errors)
data = json.loads(content)

# After (handles multiple encodings)
try:
    content_str = content.decode('utf-8')
except UnicodeDecodeError:
    content_str = content.decode('latin-1')

data = json.loads(content_str)
```

**Fix 2: Non-blocking Warnings**

Changed unparseable files from blocking errors to warnings:
```python
except (json.JSONDecodeError, UnicodeDecodeError) as e:
    self.warnings.append(f"Could not parse {member.name}: {e}")
    # Changed from self.issues (blocking) to self.warnings
```

This allows backups to pass verification even if some macOS metadata files (._*) can't be parsed.

**Fix 3: Multi-location Redundancy**

```bash
# Old system: Single location (iCloud only)
BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/PetesBrain-Backups/critical-tasks"

# New system: Three locations
LOCAL_BACKUP_DIR="${BASE_DIR}/_backups/tasks"  # Fast local access
ICLOUD_BACKUP_DIR="$HOME/Library/Mobile Documents/..."  # Off-machine
GOOGLE_DRIVE_BACKUP_DIR="..."  # Long-term archive (via Python agent)
```

**Fix 4: Automated Monitoring**

Created log files for daily health checks:
- `~/.petesbrain-safe-backup.log` - Backup execution
- `~/.petesbrain-backup-alerts.log` - **CRITICAL ALERTS** (check daily)
- `~/.petesbrain-backup-verification.log` - Verification details
- `~/.petesbrain-weekly-audit.log` - Weekly restoration tests

### Prevention Measures

**Operational Changes**:
1. **Daily log checks** - Review `~/.petesbrain-backup-alerts.log` every morning
2. **Weekly audit review** - Check audit results every Monday
3. **Red flag alerts**:
   - "Backup file is suspiciously small" → Immediate investigation
   - "Task count dropped X% from baseline" → Data loss detected
   - "Restoration test failed" → Backup not recoverable

**Technical Safeguards**:
1. **Immediate verification** - Every backup verified before storage
2. **Baseline tracking** - Statistical anomaly detection
3. **Multi-location storage** - 3 independent backup copies
4. **Restoration testing** - Weekly proof that backups are recoverable
5. **Automated alerting** - Failures logged and visible

**Documentation Created**:
- `docs/BACKUP-SAFETY-SYSTEM.md` (400+ lines)
  - Architecture overview (3 layers)
  - Monitoring procedures
  - Recovery procedures
  - Troubleshooting guide
  - Maintenance instructions

### Lessons Learned

1. **"Never trust backups - always verify them"**
   - Creating a backup ≠ Having a working backup
   - Verification must happen immediately after creation
   - Must test restoration, not just creation

2. **Silent failures are the worst failures**
   - System failed for 9 days before discovery
   - Alerting is not optional - it's critical
   - Logs must be actively monitored

3. **Single points of failure are unacceptable**
   - Single backup location = Single point of failure
   - Multiple independent locations provide true redundancy
   - Local + Cloud + Archive = Comprehensive protection

4. **Bash scripts for critical operations are risky**
   - Bash doesn't handle errors well by default
   - Python provides better error handling and logging
   - For critical operations, use explicit error checking

5. **Recovery is harder than prevention**
   - 15 tasks recovered, but unknown how many lost permanently
   - Hours spent on recovery vs minutes for prevention
   - Context from 9 days ago is harder to reconstruct

### Related Documentation

- `docs/BACKUP-SAFETY-SYSTEM.md` - Complete backup system documentation
- `shared/backup-verification/` - All backup scripts and tools
- `infrastructure/launch-agents/com.petesbrain.safe-backup.plist` - 6-hour backup automation
- `infrastructure/launch-agents/com.petesbrain.weekly-backup-audit.plist` - Weekly testing

### Status

**✅ FULLY RESOLVED as of December 19, 2025**

- Tasks recovered from available sources
- 3-layer backup safety system deployed and tested
- LaunchAgents installed and running
- Comprehensive documentation created
- Daily/weekly monitoring procedures established

**Prevention confidence**: HIGH - This specific failure mode (corrupt backups undetected) cannot recur due to:
- Immediate size/integrity verification
- Statistical baseline checks
- Weekly restoration testing
- Multi-location redundancy
- Active alerting

---

## Task Notes Processing Failure - December 15, 2025

**Incident**: Manual task note containing instruction was not executed

**What Happened**:
- User added manual task note: "Confirm recent stats show profit, then complete it"
- System added note to task but DID NOT execute the instruction
- Task remained open despite containing actionable instruction
- User had to manually prompt execution

**Root Cause**:
Protocol only distinguished between:
1. "Done" → Complete task
2. Anything else → Add as note

No logic to detect and execute instructions within notes.

**Impact**:
- Task incorrectly left open
- Required manual user intervention
- Instruction delayed by hours

**Fix Applied**:
Updated `.claude/CLAUDE.md` "Process my task notes" section with:
1. **Action verb detection** (Confirm, Verify, Check, Review, etc.)
2. **Three-tier decision tree**:
   - Simple completion → Complete immediately
   - Instruction → Execute FIRST, then complete
   - Comment → Add as note only
3. **Examples table** showing proper handling

**Prevention**:
- Enhanced protocol now explicitly requires instruction execution
- Clear examples prevent future misinterpretation
- Action verbs list provides detection criteria

**File Updated**: `/Users/administrator/.claude/CLAUDE.md` lines 276-321

**Lesson**: User instructions in manual notes must be treated as executable commands, not just passive comments.


---

## Task Manager "House of Cards" Architecture - December 22, 2025

**Severity**: 🟡 MAJOR - System fragility causing recurring breakage
**Status**: ✅ RESOLVED - Template-based architecture implemented
**Impact**: Manual fixes repeatedly lost, wasted hours on symptom fixes

### What Happened

**Timeline**:
- **Morning December 22**: Multi-hour investigation into Task Manager backend issues
  - Fixed orphaned task files
  - Consolidated servers
  - Analyzed task count mismatches
- **Afternoon December 22**: User asked to "process task notes"
  - Refresh button broken AGAIN (GET instead of POST)
  - Fixed refresh button
  - **User's critical question**: "Earlier today we spent a good few hours fixing the task manager. As soon as you start to use it, it breaks again. Why is this?"

**User Frustration**:
- Morning's comprehensive fix focused on backend (orphaned files, server consolidation)
- Afternoon immediately revealed frontend breakage (refresh button)
- **Pattern**: Every fix gets overwritten by hourly regeneration
- **Root issue**: Morning's analysis was too narrow - treated symptoms, not root cause

### Root Cause

**"House of Cards" Architecture**: Fragile foundational architecture causing cascading failures.

**Primary Cause**: 1,028 lines of inline HTML in Python generator

```python
# generate-all-task-views.py (BEFORE FIX)
task_manager_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PetesBrain - Task Manager & Reminders</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: Verdana, Geneva, sans-serif;
            ...
        }}
        ...
    </style>
</head>
<body>
    ...1,028 lines of HTML...
</body>
</html>
'''
```

**The Problem**:
1. Manual fixes made to generated `tasks-manager.html` file
2. Hourly LaunchAgent runs `generate-all-task-views.py`
3. Generator overwrites entire HTML file with inline template
4. **All manual fixes lost** (refresh button reverts from POST back to GET)
5. Browser DOM replaced → JavaScript event listeners destroyed
6. User forced to re-fix the same bugs repeatedly

**Contributing Factors**:
1. **No template separation** - HTML hardcoded in Python f-string
2. **Hourly regeneration** - LaunchAgent runs every hour
3. **Analysis scope too narrow** - Morning's work focused on backend, missed frontend architecture flaw
4. **Symptom fixing** - Fixed immediate breakage without asking "why does this keep breaking?"

### The Fix

**Comprehensive Architectural Redesign** (6-step plan with validation gates):

**GATE 0: Pre-Flight Safety Checks**
- Backed up 22 task JSON files (51 total tasks, 44 active)
- Created baseline HTML for pixel-perfect comparison
- Git commit 0623399 as rollback point

**STEP 1: Extract Template (Preserve Exact Look & Feel)**
- Created `shared/task-manager/tasks-manager-template.html` (1,025 lines)
- Extracted from `generate-all-task-views.py` lines 1070-2094
- Cleaned up Python f-string escaping (`{{` → `{`)
- Preserved all CSS, JavaScript, HTML structure unchanged
- Result: Template file with placeholders `{task_data}` and `{reminder_data}`

**STEP 2: Add API Endpoint (Read-Only, Zero Risk)**
- Created shared module `shared/task_loader.py` with `load_all_tasks()` function
- Added `/api/tasks` endpoint to `shared/task-manager/task-manager-server.py`
- API returns JSON: `{tasks_by_client, all_tasks, all_reminders, timestamp}`
- Verified: API returns 42 tasks, 30 reminders, 19 clients (matches backup count)

**STEP 3: Update Generator to Use Template**
- Modified `generate-all-task-views.py` to load template instead of inline HTML
- Removed 1,005 lines of old inline HTML generation code
- Updated output path to `shared/task-manager/tasks-manager.html`
- Fixed variable names (`task_data` not `task_data_dict`)
- Result: Generator now loads template, injects data, writes to correct location

**STEP 4: Verify Template Changes Persist**
- Added test change to template header
- Regenerated HTML
- Verified change appears in output
- **Proof**: Template modifications survive all future regenerations

**STEP 5: Verify Hourly Regeneration Works**
- Located LaunchAgent: `com.petesbrain.task-manager-hourly-regenerate.plist`
- Updated to call correct script (`generate-all-task-views.py` instead of deprecated `shared/scripts/generate-task-manager.py`)
- Reloaded LaunchAgent
- Verified all paths aligned: LaunchAgent → Generator → Server

**STEP 6: Clean Up & Document**
- Archived old HTML files to `_archive/task-manager-fix-dec-22-2025/`
- Archived deprecated generation script
- Updated INCIDENTS.md with comprehensive root cause analysis
- Created architecture documentation

### Technical Explanation

**Before** (Inline HTML Anti-Pattern):
```
generate-all-task-views.py
├─ Loads task data from JSON files
├─ 1,028 lines of inline HTML in f-string
├─ Injects data into HTML string
└─ Writes to tasks-manager.html (overwrites entire file)

Hourly: LaunchAgent runs generator → All manual fixes lost
```

**After** (Template + Data Injection Pattern):
```
generate-all-task-views.py
├─ Loads task data from JSON files
├─ Loads template from shared/task-manager/tasks-manager-template.html
├─ Injects data into template placeholders
└─ Writes to shared/task-manager/tasks-manager.html

Template file (never regenerated):
├─ All HTML/CSS/JavaScript structure
├─ Manual fixes persist forever
└─ Placeholders: {task_data}, {reminder_data}

Hourly: LaunchAgent runs generator → Template unchanged, fixes persist
```

**Why This Works**:
- Template file is **separate from generator** - never overwritten
- Manual fixes go in **template** (persistent) not generated HTML (ephemeral)
- Hourly regeneration loads template + fresh data = fresh output with preserved fixes
- No more "house of cards" - foundation is now solid

### Files Modified

**Created**:
- `shared/task-manager/tasks-manager-template.html` (1,025 lines) - Template with placeholders
- `shared/task_loader.py` (207 lines) - Shared task loading module
- `_archive/task-manager-fix-dec-22-2025/` - Archive of old files

**Modified**:
- `generate-all-task-views.py` - Loads template instead of inline HTML (removed 1,005 lines)
- `shared/task-manager/task-manager-server.py` - Added `/api/tasks` endpoint
- `~/Library/LaunchAgents/com.petesbrain.task-manager-hourly-regenerate.plist` - Updated script path

**Archived**:
- `shared/scripts/generate-task-manager.py` → `_archive/.../generate-task-manager-DEPRECATED.py`
- `tasks-manager.html` (root) → `_archive/.../tasks-manager-ROOT-DEPRECATED.html`
- `tasks-manager-v2.html` → `_archive/...`
- `tasks-manager-TEST.html` → `_archive/...`
- `tasks-manager-debug.html` → `_archive/...`
- `tasks-manager-WORKING-BASELINE.html` → `_archive/...` (preserved for reference)

### Lessons Learned

1. **Ask "Why?" Three Times**:
   - First fix: "Refresh button broken" → Fix button
   - Second fix: "Refresh button broken AGAIN" → Fix button again
   - **Third time**: "Why does this keep breaking?" → Discover root cause (hourly regeneration + inline HTML)

2. **Comprehensive vs. Narrow Analysis**:
   - Morning's analysis: Backend-focused (orphaned files, server consolidation)
   - Afternoon's realization: Frontend architecture flaw completely overlooked
   - **Lesson**: When user says "it keeps breaking," analyze ALL layers, not just one domain

3. **Symptom Fixes vs. Root Cause Fixes**:
   - Symptom: "Refresh button uses GET instead of POST"
   - Root cause: "1,028 lines of inline HTML gets regenerated hourly"
   - **Lesson**: If a fix doesn't survive a day, you fixed a symptom, not the cause

4. **Template Extraction is Not Optional**:
   - Inline HTML in code = anti-pattern
   - Template files = separation of concerns
   - **Lesson**: HTML belongs in `.html` files, not Python f-strings

5. **User Frustration as Signal**:
   - User's question: "Why is this?" (not "What is this?")
   - Tone: Frustration with recurring failure
   - **Lesson**: User frustration signals systemic issue requiring architectural fix

### Prevention

**Immediate**:
- ✅ Template-based generation prevents fixes from being lost
- ✅ Hourly regeneration now safe (template unchanged)
- ✅ Refresh button fix persists forever

**Long-term**:
- Established pattern: HTML templates in dedicated files
- Shared task loader module (`task_loader.py`) for consistency
- API endpoint for future client-side rendering (if needed)

**Process Improvements**:
- When user asks "why does this keep breaking?" → Stop fixing symptoms, analyze architecture
- Multi-layer analysis: Backend AND Frontend AND Infrastructure
- "House of cards" is a RED FLAG → Redesign foundation, don't patch cracks

### Verification

**Test 1: Template Change Persists**
- Added test text to template header
- Regenerated HTML
- ✅ Change appeared in output

**Test 2: Hourly Regeneration Works**
- Updated LaunchAgent to call correct script
- Verified generator writes to correct location
- Verified server serves from correct location
- ✅ All paths aligned

**Test 3: Data Integrity**
- Compared task counts: 42 tasks (matches backup count)
- Verified reminders: 30 reminders
- Verified clients: 19 clients
- ✅ Zero data loss

**Visual Verification**:
- Opened generated HTML in browser
- Compared to baseline screenshot (pixel-perfect match)
- ✅ Look and feel preserved

### Prevention Confidence

**HIGH** - This specific failure mode (fixes lost on regeneration) cannot recur because:
- Template file is separate from generator (never overwritten)
- Manual fixes go in template (persistent) not generated output (ephemeral)
- Architecture pattern established: HTML in `.html` files, not Python code
- Shared modules prevent code duplication
- API endpoint enables future client-side rendering if needed

**Architectural moat**: Template extraction creates clear separation of concerns that makes this class of bug impossible.

