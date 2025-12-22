---
name: task-manager
description: Opens the PetesBrain Task Manager interface displaying all client tasks organized by priority. Use when user says "open task manager", "task manager", "show tasks", "view tasks", or wants to see their task list.
allowed-tools: Bash, Read
---

# Task Manager

---

## Instructions

When this skill is invoked:

1. **Generate all task views** (consolidated script):
   ```bash
   cd /Users/administrator/Documents/PetesBrain.nosync
   python3 generate-all-task-views.py
   ```

2. **Check if HTTP server is already running**:
   ```bash
   lsof -ti :8767 > /dev/null 2>&1
   ```

3. **Start HTTP server if not running** (in background):
   ```bash
   if [ $? -ne 0 ]; then
     python3 /Users/administrator/Documents/PetesBrain.nosync/shared/scripts/serve-task-manager.py > /dev/null 2>&1 &
     sleep 1
   fi
   ```

4. **Open in browser via HTTP** (not file://):
   ```bash
   open "http://localhost:8767/tasks-manager.html"
   ```

5. **Confirm to user**:
   ```
   ✅ Task Manager & Reminders opened

   View: Task Manager & Reminders
   URL: http://localhost:8767/tasks-manager.html

   The task manager shows:
   - All client tasks (organized by client)
   - Personal reminders (roksys section)
   - All tasks from clients/*/tasks.json
   - Organized by client with collapsible sections
   - Parent-child task relationships
   - Due dates, time estimates, and notes
   - Recurring tasks clearly marked
   - Collapsible sections for easy navigation

   ✅ Backend notes server connected (localhost:8766)
   "Save to Manual Tasks" button will work correctly

   Example output:
   Total: 67 active tasks
     Internal tasks: 32
     Google Tasks: 35

   Default view: Opens on P0 (highest priority) tasks
   ```

---

## What the Task Manager Shows

**Priority Levels**:
- **P0**: Critical/urgent tasks (default view)
- **P1**: High priority tasks
- **P2**: Medium priority tasks
- **P3**: Low priority tasks

**Task Types**:
- **Parent tasks**: Contain multiple related child tasks (meetings, projects)
- **Child tasks**: Individual action items within a parent task
- **Standalone tasks**: Independent tasks not part of a group

**Information Displayed**:
- Client name
- Task title
- Due date
- Time estimate
- Priority level
- Task notes
- Source (meeting, email, etc.)
- Tags
- Parent-child relationships

---

## Notes

- Internal tasks are read from `clients/*/tasks.json` files
- Google Tasks are fetched via Google Tasks API
- Both sources are merged and displayed together
- Source is clearly labeled (Internal vs Google Tasks)
- Only active tasks are displayed (completed tasks are in `tasks-completed.md`)
- Child tasks appear nested under their parent tasks
- Sections are collapsible for easy navigation
- Data refreshes each time the generator is run
- Google Tasks priority is extracted from title tags: [P0], [P1], [P2], [P3]

**HTTP Server & Backend Connection**:
- Task Manager MUST be served via HTTP (not file://) to connect to backend
- HTTP server runs on port 8767 (serves HTML files)
- Backend notes server runs on port 8766 (saves manual task notes)
- Browser security blocks file:// → http://localhost connections
- HTTP → HTTP connections work correctly
- "Save to Manual Tasks" button requires both servers running

**Server Status**:
- HTTP server: Check with `lsof -ti :8767`
- Backend server: Check with `lsof -ti :8766`
- Backend LaunchAgent: `launchctl list | grep task-notes-server`

---

**Files**:
- Consolidated Generator: `generate-all-task-views.py` (generates all 3 views)
- HTML Views: `tasks-overview.html`, `tasks-overview-priority.html`, `tasks-manager.html`
- Templates: `tasks-overview-template.html`, `tasks-overview-priority-template.html`
- HTTP Server: `shared/scripts/serve-task-manager.py`
- Backend Server: `shared/scripts/save-task-notes.py`
