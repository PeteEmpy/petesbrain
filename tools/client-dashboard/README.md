# Client Dashboard

Browser-based dashboard for viewing all client information and managing tasks.

## Features

- **Client Dashboard**: View all clients at a glance with quick stats
- **Client Detail Pages**: Drill down into individual client information
- **Task Management**: Full CRUD operations for todos
- **File Browser**: Browse and view client files
- **Markdown Rendering**: View CONTEXT.md and other markdown files formatted

## Quick Start

```bash
cd tools/client-dashboard
./start.sh
```

Then open http://localhost:5002 in your browser.

## Usage

### Dashboard
- View all clients in a grid layout
- See pending task counts and recent activity
- Search/filter clients
- Click on any client to view details

### Client Detail Page
- **Overview Tab**: View CONTEXT.md content
- **Tasks Tab**: See all tasks for this client
- **Files Tab**: Browse client folder structure

### Task Management
- View all tasks across all clients
- Filter by client or status
- Create new tasks
- Mark tasks as complete
- Edit task details
- Delete tasks (archived to `todo/_archived/`)

## Integration

The dashboard integrates with existing systems:

- **Wispr Flow**: Tasks created via Wispr Flow appear in the dashboard
- **Inbox Processor**: New tasks can be processed by existing inbox system
- **File Organizer**: Respects organized folder structure
- **Tasks Monitor**: Completed tasks sync to `tasks-completed.md`

## Task Format

Tasks are stored as markdown files in the `todo/` directory:

```markdown
# Task Title

**Created:** 2025-11-09 12:00
**Client:** positive-bakes
**Due Date:** Friday

## Details

Task description here...

## Status

- [ ] Todo

## Notes

```

## API Endpoints

- `GET /` - Dashboard
- `GET /client/<name>` - Client detail page
- `GET /tasks` - Task management page
- `GET /api/tasks` - All tasks JSON
- `POST /api/task/create` - Create new task
- `PUT /api/task/<filename>/complete` - Mark task complete
- `PUT /api/task/<filename>/update` - Update task
- `DELETE /api/task/<filename>` - Delete task

## Development

### Requirements
- Python 3.6+
- Flask
- markdown

### Running in Development Mode

```bash
source venv/bin/activate
python3 app.py
```

The app runs on http://localhost:5002 by default.

## Security

- **Local Only**: App runs on localhost only (127.0.0.1)
- **Path Validation**: All file paths are validated to prevent directory traversal
- **Read-Only Default**: Only todo files can be modified, other files are read-only

## Future Enhancements

### High Priority
- **Manual Client Assignment**: Ability to manually assign/reassign clients to existing tasks that don't have client detection
  - Add "Assign Client" button/dropdown on task items
  - Update task markdown file with client metadata
  - Bulk assignment interface for multiple tasks

### Medium Priority
- Real-time updates (WebSockets)
- Task due date reminders
- Client activity timeline
- Search across all client files
- Task templates
- Bulk task operations
- File viewer modal for markdown/HTML files
- Edit task functionality in UI

### Low Priority
- Export tasks to CSV/JSON
- Task analytics and reporting
- Client comparison views
- Customizable dashboard widgets

