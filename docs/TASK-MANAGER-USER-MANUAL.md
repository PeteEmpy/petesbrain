# Task Manager User Manual

**Version**: 2.0
**Last Updated**: December 19, 2025
**For**: Daily task management and planning

---

## 🎯 What is the Task Manager?

The Task Manager is your central dashboard for viewing and managing all client work tasks across PetesBrain. It provides multiple views of your tasks organised by priority, client, and status.

**What you can do**:
- ✅ View all active tasks across all clients
- ✅ See tasks organised by priority (P0 urgent → P3 low priority)
- ✅ View tasks grouped by client
- ✅ Check due dates and time estimates
- ✅ See parent tasks with nested action items
- ✅ Mark tasks as complete with notes
- ✅ Add quick task notes for later processing

**What it shows**:
- Internal client tasks from `clients/*/tasks.json`
- Personal reminders from Roksys folder
- Total task counts and priority breakdown
- Parent-child task relationships
- Due dates, priorities, and time estimates

---

## 🚀 Opening the Task Manager

### Quick Launch

**Via Claude Code** (recommended):
```
"Open task manager"
"Show tasks"
"Task manager"
```

**Manually**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync
python3 generate-all-task-views.py
```

This will:
1. Generate fresh HTML views from all task files
2. Start HTTP server (if not already running)
3. Open browser to `http://localhost:8767/tasks-manager.html`

**Expected Output**:
```
✅ Task Manager & Reminders opened

View: Task Manager & Reminders
URL: http://localhost:8767/tasks-manager.html

Total: 67 active tasks
  Internal tasks: 32
  Google Tasks: 35

Default view: Opens on P0 (highest priority) tasks
```

---

## 📊 Understanding the Interface

### Three Available Views

**1. Task Manager & Reminders** (`tasks-manager.html`)
- **Best for**: Daily work planning and priority focus
- **Shows**: All tasks organised by priority (P0 → P3)
- **Use when**: Planning your day, checking urgent work

**2. Tasks by Client** (`tasks-overview.html`)
- **Best for**: Client-specific focus
- **Shows**: Tasks grouped by client with collapsible sections
- **Use when**: Working on a specific client's account

**3. Tasks by Priority** (`tasks-overview-priority.html`)
- **Best for**: Priority-based workflow
- **Shows**: Separate sections for P0, P1, P2, P3
- **Use when**: Triaging and prioritising work

### Switching Between Views

**In the browser**: Click the view switcher buttons at the top
- 📋 Task Manager & Reminders
- 👥 By Client
- 🎯 By Priority

**Direct URLs**:
- `http://localhost:8767/tasks-manager.html`
- `http://localhost:8767/tasks-overview.html`
- `http://localhost:8767/tasks-overview-priority.html`

---

## 🎨 Reading the Task Manager

### Priority Levels (Colour-Coded)

| Priority | Label | Colour | Meaning | Example |
|----------|-------|--------|---------|---------|
| **P0** | Critical/Urgent | 🔴 Red | Do today, blocking issues | Campaign down, budget exhausted |
| **P1** | High Priority | 🟠 Orange | Do this week | Client request, optimisation opportunity |
| **P2** | Normal | 🟡 Yellow | Do this month | Improvements, reviews |
| **P3** | Low Priority | 🟢 Green | Someday/backlog | Nice-to-have, future work |

### Task Information Display

Each task shows:

```
┌─────────────────────────────────────────────────┐
│ 🔴 P0 | [Client Name]                          │
│                                                 │
│ Task Title                                      │
│                                                 │
│ 📅 Due: 2025-12-20 (Tomorrow)                  │
│ ⏱️ Estimate: 30 mins                           │
│ 📝 Notes: Context about this task              │
│ 🏷️ Tags: campaign-audit, wasted-spend          │
│                                                 │
│ [Mark as Complete] [Add Note]                  │
└─────────────────────────────────────────────────┘
```

**Icons & Indicators**:
- 🔄 **Recurring badge**: Task repeats weekly/monthly
- 📌 **Parent task**: Contains child action items
- ↳ **Child task**: Action item within a parent
- ⏰ **Overdue**: Red date indicator
- ✅ **Completed**: Greyed out with checkmark

### Parent-Child Tasks

**Parent tasks** represent larger initiatives with multiple steps:
```
📌 [NMA] 3-Week Improvement Plan (Parent)
  ↳ Week 1: Increase budgets by 15%
  ↳ Week 2: Add negative keywords
  ↳ Week 3: Review performance and adjust
```

**How they work**:
- Parent task shows overall project
- Child tasks are individual action items
- Only **overdue** child tasks appear in daily briefing
- Complete child tasks independently
- Parent task remains until all children completed

**Use cases**:
- Meeting action items (1 parent = meeting, children = actions)
- Multi-week projects (1 parent = project, children = weekly tasks)
- Related initiatives (1 parent = theme, children = specific tasks)

---

## ✅ Common Operations

### Marking Tasks as Complete

**Method 1: Via Task Manager UI** (recommended)

1. Find the task in the Task Manager
2. Click **"Mark as Complete"** button
3. Enter completion notes (optional but recommended):
   ```
   Deployed new budgets. Monitoring performance.
   ```
4. Click **"Save to Manual Tasks"**
5. Process task notes later via Claude Code

**Method 2: Via Claude Code** (for technical users)

```
"Process my task notes"
```

This will:
- Read all manual task notes
- Execute completion instructions
- Archive to `tasks-completed.md`
- Update task views

**What happens when you complete a task**:
1. Task removed from `tasks.json`
2. Task logged to `clients/{client}/tasks-completed.md` with:
   - Completion date
   - Original task details
   - Completion notes
3. HTML views updated
4. Task no longer appears in Task Manager

### Adding Quick Notes to Tasks

**Use the "Add Note" feature for**:
- Progress updates: "Budget increased, monitoring results"
- Context additions: "Client confirmed via email"
- Completion markers: "Done"
- Instructions: "Verify performance first, then complete"

**How it works**:
1. Click **"Add Note"** on any task
2. Enter your note in the text field
3. Click **"Save to Manual Tasks"**
4. Process notes later with `"Process my task notes"`

**Note types**:
- **Simple completion**: "Done" → Task marked complete immediately
- **Instruction**: "Confirm stats show profit, then complete" → Executes instruction THEN completes
- **Comment**: "Reminder to follow up next week" → Adds note, keeps task open

---

## 🔍 Finding Tasks

### By Priority

**In Task Manager view**: Tasks automatically sorted P0 → P3

**Finding urgent work**:
1. Open Task Manager (defaults to P0 tasks at top)
2. Look for 🔴 Red priority tags
3. Check due dates (⏰ overdue tasks shown first)

### By Client

**In Tasks by Client view**:
1. Open `tasks-overview.html`
2. Scroll to client section or use Ctrl+F (Cmd+F)
3. Click client header to expand/collapse section

**Quick filter**:
- Browser search (Ctrl+F): Type client name
- Use filter buttons if available
- Check total task count per client

### By Due Date

**Finding overdue tasks**:
- Look for red date indicators: ⏰
- Overdue tasks appear at top of priority groups
- Check "Due: X days ago" in task card

**Finding today's tasks**:
- Filter by P0 (usually today's urgent work)
- Check "Due: Today" labels
- Look at task estimates to plan your day

### By Tag

Tasks can have tags like:
- `campaign-audit` - Audit-related tasks
- `wasted-spend` - Budget waste opportunities
- `client-request` - Direct client asks
- `recurring` - Repeating tasks

**How to search by tag**:
- Browser search (Ctrl+F): Type tag name
- Tags shown as: 🏷️ campaign-audit, wasted-spend

---

## 📅 Understanding Due Dates

### Due Date Display

| Display | Meaning | Action Required |
|---------|---------|-----------------|
| **Due: Today** | Due today | Do today |
| **Due: Tomorrow** | Due 2025-12-20 | Plan for tomorrow |
| **Due: In 3 days** | Due 2025-12-22 | Upcoming this week |
| **Due: 2 days ago** ⏰ | Overdue | Urgent - do ASAP |
| **No due date** | Flexible timing | Do when capacity allows |

### Task Estimates

Time estimates help you plan your day:

```
⏱️ Estimate: 30 mins   → Quick task
⏱️ Estimate: 2 hours   → Block time
⏱️ Estimate: 4 hours   → Half-day project
⏱️ No estimate         → Unknown duration
```

**Planning your day**:
1. Check P0 tasks with today's due dates
2. Sum time estimates
3. Allocate your available time
4. Move non-urgent tasks if needed

---

## 🔄 Recurring Tasks

### What are Recurring Tasks?

Tasks that repeat on a schedule:
- Weekly: "Review Smythson Performance Max campaigns"
- Monthly: "Send Devonshire monthly report"
- Custom: "Check experiment results every 2 weeks"

### How They Work

**Visual indicator**: 🔄 badge on task card

**Behaviour**:
1. Task appears in your list at scheduled time
2. You complete the task
3. Task automatically recreates for next occurrence
4. Completion logged to `tasks-completed.md`
5. New instance appears with next due date

**Example**:
```
Today: [Smythson] Review Performance Max (Due: Monday)
Complete it → Logged to archive
Next Monday: Task reappears automatically
```

### Managing Recurring Tasks

**To complete**: Mark as complete normally - it will recreate

**To stop recurring**: Via Claude Code:
```
"Stop the recurring task for [Client] [Task Name]"
```

**To change frequency**: Via Claude Code:
```
"Change [Task Name] from weekly to monthly"
```

---

## 🛠️ Troubleshooting

### Task Manager Won't Open

**Symptoms**: Browser shows "Can't connect to localhost:8767"

**Fix**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync
python3 generate-all-task-views.py
```

This regenerates the HTML and restarts the server.

**Check if server is running**:
```bash
lsof -ti :8767
```
If no output, server is not running - regenerate views.

---

### Tasks Not Showing

**Symptoms**: Task Manager opens but missing tasks you know exist

**Check**:
1. **Regenerate views** (data may be stale):
   ```bash
   python3 generate-all-task-views.py
   ```

2. **Verify task file location**:
   ```bash
   # Should be here:
   ls clients/{client}/tasks.json

   # NOT here (wrong location):
   ls clients/{client}/product-feeds/tasks.json
   ```

3. **Check JSON validity**:
   ```bash
   python3 -m json.tool clients/{client}/tasks.json
   ```
   If error, file is corrupt - restore from backup.

---

### Task Appearing Twice

**Symptoms**: Same task shows up in multiple places

**Cause**: Task files in wrong locations (rare after 2025-11-26 migration)

**Fix**:
```bash
# Find duplicate task files
find clients/{client} -name "tasks.json"
```

If found in both root and product-feeds:
1. Keep the one in root (`clients/{client}/tasks.json`)
2. Merge any unique tasks from product-feeds version
3. Delete the product-feeds version
4. Regenerate: `python3 generate-all-task-views.py`

---

### Completed Task Still Showing

**Symptoms**: Marked task as complete but it's still in the list

**Causes**:
1. **Views not regenerated** - Run `python3 generate-all-task-views.py`
2. **Task notes not processed** - Say `"Process my task notes"` to Claude Code
3. **Browser cache** - Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

**Proper completion workflow**:
1. Mark as complete → "Save to Manual Tasks"
2. Say "Process my task notes" to Claude Code
3. Views automatically regenerate
4. Refresh browser to see update

---

### "Save to Manual Tasks" Button Not Working

**Symptoms**: Click button, nothing happens

**Cause**: Backend server not running (port 8766)

**Fix**:
```bash
# Check if backend server is running
lsof -ti :8766

# If not running, check LaunchAgent
launchctl list | grep task-notes-server

# If not loaded, load it
launchctl load ~/Library/LaunchAgents/com.petesbrain.task-notes-server.plist
```

**Why this matters**: Task Manager MUST be served via HTTP (not file://) to connect to backend. Browser security blocks file:// → http://localhost connections.

---

### Total Task Count Seems Wrong

**Symptoms**: Task Manager shows 67 tasks but you expected different count

**Understanding the count**:
```
Total: 67 active tasks
  Internal tasks: 32   ← From clients/*/tasks.json
  Google Tasks: 35     ← From Google Tasks API (deprecated Dec 16, 2025)
```

**If count seems low**:
1. Check if tasks in wrong location (run validation):
   ```bash
   python3 scripts/validate-task-system.py
   ```
2. Check `tasks-completed.md` - tasks may have been completed
3. Regenerate views from fresh data

**If count seems high**:
- May include old Google Tasks (system deprecated Dec 16, 2025)
- Check for duplicate tasks across clients
- Run validation script

---

## 💡 Tips & Best Practices

### Daily Workflow

**Morning routine**:
1. Open Task Manager (`http://localhost:8767/tasks-manager.html`)
2. Check P0 (red) tasks - these are urgent
3. Look at due dates - prioritise overdue tasks ⏰
4. Check time estimates - plan your day
5. Start with highest priority, earliest due date

**Throughout the day**:
- Mark tasks complete as you finish them
- Add progress notes for partial completion
- Create new tasks as issues arise (via Claude Code)

**End of day**:
- Complete any finished tasks
- Update notes on in-progress work
- Check tomorrow's P0 tasks
- Process task notes: "Process my task notes"

### Task Organisation

**Use priorities effectively**:
- **P0**: Only for truly urgent work (client down, critical issue)
- **P1**: Important client requests, this week's work
- **P2**: Regular improvements, non-urgent optimisations
- **P3**: Nice-to-have, backlog, future ideas

**Don't overload P0**:
- If everything is urgent, nothing is urgent
- Move completed P0s down to P1/P2 if not truly critical
- Reserve P0 for blocking issues

**Use parent-child for projects**:
```
Parent: [Client] Q4 Campaign Restructure
  ↳ Week 1: Audit current structure
  ↳ Week 2: Design new structure
  ↳ Week 3: Implement changes
  ↳ Week 4: Monitor and optimise
```

### Staying Organised

**Review regularly**:
- **Daily**: Check P0 tasks
- **Weekly**: Review all P1/P2 tasks, reprioritise
- **Monthly**: Clean up P3 backlog, archive completed

**Use completion notes**:
- Brief but meaningful: "Deployed, monitoring results"
- Include outcomes: "ROAS improved from 320% to 380%"
- Note next steps: "Follow up in 1 week to verify"

**Keep tasks specific**:
- ❌ "Optimise Smythson campaigns"
- ✅ "Add 5 negative keywords from search term report"

---

## 🔐 Backup & Safety

### Task Data Protection

**Automatic backups** (every 6 hours):
- Location: `_backups/tasks/`
- Also backed up to iCloud and Google Drive
- Verified for integrity after each backup

**Check last backup**:
```bash
ls -lht ~/Documents/PetesBrain.nosync/_backups/tasks/ | head -5
```

**Manual backup** (before major changes):
```bash
cd ~/Documents/PetesBrain.nosync
./shared/backup-verification/safe-backup.sh
```

### What's Protected

**NEVER manually edit these files** without backup:
- `clients/*/tasks.json` - Active tasks
- `clients/*/tasks-completed.md` - Completed task archive

**Safe operations**:
- ✅ Complete tasks via Task Manager UI
- ✅ Create tasks via Claude Code
- ✅ Add notes via "Add Note" button

**Unsafe operations** (ask Claude Code first):
- ❌ Directly editing JSON files
- ❌ Deleting task files
- ❌ Moving tasks between clients manually

### Recovery

**If you accidentally delete a task**:
1. Check `tasks-completed.md` - may have been completed
2. Restore from backup:
   ```
   "Restore tasks from backup" (via Claude Code)
   ```
3. Check most recent backup in `_backups/tasks/`

**Full system**: See `docs/BACKUP-SAFETY-SYSTEM.md`

---

## 📞 Getting Help

### Quick Checks

**Before asking for help**:
1. ✅ Regenerate views: `python3 generate-all-task-views.py`
2. ✅ Hard refresh browser: Ctrl+Shift+R (Cmd+Shift+R)
3. ✅ Check for errors: Look in browser console (F12)
4. ✅ Run validation: `python3 scripts/validate-task-system.py`

### Via Claude Code

**Task Manager issues**:
```
"Task Manager not showing my tasks"
"How do I mark a task as complete?"
"Why is my task appearing twice?"
```

**Task operations**:
```
"Create a task for [Client] to [action]"
"Mark task [ID] as complete"
"Process my task notes"
```

### Common Questions

**Q: Can I edit tasks directly in the Task Manager?**
A: Not yet - use "Add Note" button and process notes via Claude Code. Direct editing coming in future version.

**Q: Why do I see both Internal and Google Tasks?**
A: Historical - Google Tasks integration was deprecated Dec 16, 2025. You'll only see Internal tasks going forward.

**Q: Can I create tasks in the Task Manager UI?**
A: Not yet - create via Claude Code with `"Create task for [Client]"`. UI creation planned for future.

**Q: How often should I process task notes?**
A: Daily, or whenever you mark multiple tasks as complete. Keeps views fresh.

**Q: Can I customise priority colours?**
A: Not currently - standard colours (red/orange/yellow/green) for consistency.

---

## 📚 Related Documentation

**For daily use** (this document):
- Task Manager User Manual (you are here)

**For deeper understanding**:
- `TASK-SYSTEM-README.md` - Quick start guide
- `TASK-SYSTEM-COMPLETE-GUIDE.md` - Technical architecture
- `INTERNAL-TASK-SYSTEM.md` - Internal system details

**For developers**:
- `TASK-SYSTEM-ARCHITECTURE.md` - Technical specs
- `shared/client_tasks_service.py` - Core service code
- `.claude/skills/task-manager/skill.md` - Skill documentation

**For safety**:
- `BACKUP-SAFETY-SYSTEM.md` - Backup procedures (NEW - Dec 19, 2025)
- `INCIDENTS.md` - Historical issues and fixes (NEW - Dec 19, 2025)

---

## 🎯 Quick Reference Card

### Opening Task Manager
```
Via Claude Code: "Open task manager"
Manually: python3 generate-all-task-views.py
URL: http://localhost:8767/tasks-manager.html
```

### Priority System
```
🔴 P0 = Critical/Urgent (today)
🟠 P1 = High Priority (this week)
🟡 P2 = Normal (this month)
🟢 P3 = Low Priority (backlog)
```

### Common Operations
```
Mark complete: Click "Mark as Complete" → Add note → "Save to Manual Tasks"
Process notes: "Process my task notes" (via Claude Code)
Add quick note: Click "Add Note" → Enter text → "Save to Manual Tasks"
Create task: "Create task for [Client] to [action]" (via Claude Code)
```

### File Locations
```
Active tasks: clients/{client}/tasks.json
Completed: clients/{client}/tasks-completed.md
Backups: _backups/tasks/
```

### Troubleshooting
```
Not showing: python3 generate-all-task-views.py
Still wrong: python3 scripts/validate-task-system.py
Backend broken: launchctl list | grep task-notes-server
```

---

**Last Updated**: December 19, 2025
**Version**: 2.0
**Next Review**: January 19, 2026

**Maintained By**: PetesBrain Documentation Team
**Feedback**: Report issues via Claude Code
