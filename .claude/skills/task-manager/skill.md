---
name: task-manager
description: Opens the PetesBrain Task Manager interface displaying all client tasks organized by priority. Use when user says "open task manager", "task manager", "show tasks", "view tasks", or wants to see their task list.
allowed-tools: Bash, Read
---

# Task Manager

---

## Instructions

When this skill is invoked:

1. **Generate the priority-based task overview**:
   ```bash
   cd /Users/administrator/Documents/PetesBrain
   python3 generate-tasks-overview-priority.py
   ```

2. **Open in browser**:
   ```bash
   open /Users/administrator/Documents/PetesBrain/tasks-overview-priority.html
   ```

3. **Confirm to user**:
   ```
   ✅ Task Manager opened - displaying all tasks by priority

   View: Priority-based view (P0 → P1 → P2 → P3)
   Location: tasks-overview-priority.html

   The task manager shows:
   - All internal client tasks (clients/*/tasks.json)
   - All Google Tasks (via Google Tasks API)
   - Total tasks from both sources combined
   - Organized by priority level (P0, P1, P2, P3)
   - Source clearly labeled (Internal vs Google Tasks)
   - Parent-child task relationships
   - Due dates, time estimates, and notes
   - Collapsible sections for easy navigation

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

---

**File**: tasks-overview-priority.html
**Generator**: generate-tasks-overview-priority.py
**Template**: tasks-overview-priority-template.html
