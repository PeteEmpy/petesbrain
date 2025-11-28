#!/usr/bin/env python3
"""
Task Completion Script with Automatic Routing
Completes tasks in the appropriate system (Google Tasks or internal CONTEXT.md)
and logs completion to tasks-completed.md
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Add paths
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain')
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server')

def determine_task_source(task_id=None, task_title=None, client_name=None):
    """
    Automatically determine if a task is from Google Tasks or internal tasks

    Args:
        task_id: Task ID (if known)
        task_title: Task title
        client_name: Client name

    Returns:
        tuple: (source, details) where source is 'google-tasks' or 'internal'
    """
    # If task_id is provided, try to find it
    if task_id:
        # Check Google Tasks first
        try:
            from tasks_service import tasks_service
            service = tasks_service()

            # Get all task lists
            task_lists_response = service.tasklists().list().execute()
            task_lists = task_lists_response.get('items', [])

            for task_list in task_lists:
                try:
                    task = service.tasks().get(
                        tasklist=task_list['id'],
                        task=task_id
                    ).execute()

                    return ('google-tasks', {
                        'task_list_id': task_list['id'],
                        'task_list_title': task_list['title'],
                        'task': task
                    })
                except:
                    continue
        except Exception as e:
            print(f"⚠️  Error checking Google Tasks: {e}")

        # Check internal tasks
        clients_dir = Path('/Users/administrator/Documents/PetesBrain/clients')
        for client_dir in clients_dir.iterdir():
            if client_dir.is_dir():
                task_file = client_dir / 'tasks.json'
                if task_file.exists():
                    with open(task_file, 'r') as f:
                        data = json.load(f)

                    for task in data['tasks']:
                        if task.get('id') == task_id:
                            return ('internal', {
                                'client_name': client_dir.name,
                                'task': task,
                                'task_file': task_file
                            })

    # Fallback: determine by client name or keywords
    if client_name:
        # Check if client directory exists
        client_dir = Path(f'/Users/administrator/Documents/PetesBrain/clients/{client_name}')
        if client_dir.exists():
            return ('internal', {'client_name': client_name})

    # Check for keywords that suggest Google Tasks
    google_keywords = [
        'meeting',
        'call',
        'email',
        'reminder',
        'follow up',
        'check in'
    ]

    if task_title:
        title_lower = task_title.lower()
        for keyword in google_keywords:
            if keyword in title_lower:
                return ('google-tasks', {})

    # Default to internal if client-specific, Google Tasks otherwise
    if client_name:
        return ('internal', {'client_name': client_name})
    else:
        return ('google-tasks', {})

def complete_google_task(task_id, task_list_id, completion_notes=None):
    """Mark a Google Task as completed"""
    try:
        from tasks_service import tasks_service
        service = tasks_service()

        # Mark task as completed
        task = service.tasks().get(
            tasklist=task_list_id,
            task=task_id
        ).execute()

        task['status'] = 'completed'
        task['completed'] = datetime.now().isoformat() + 'Z'

        # Add completion notes if provided
        if completion_notes:
            existing_notes = task.get('notes', '')
            task['notes'] = f"{existing_notes}\n\nCompleted: {completion_notes}" if existing_notes else f"Completed: {completion_notes}"

        service.tasks().update(
            tasklist=task_list_id,
            task=task_id,
            body=task
        ).execute()

        return True
    except Exception as e:
        print(f"❌ Error completing Google Task: {e}")
        return False

def complete_internal_task(client_name, task_id, completion_notes=None):
    """Mark an internal task as completed and move to tasks-completed.md"""
    try:
        client_dir = Path(f'/Users/administrator/Documents/PetesBrain/clients/{client_name}')
        task_file = client_dir / 'tasks.json'

        if not task_file.exists():
            print(f"❌ Task file not found: {task_file}")
            return False

        # Load tasks
        with open(task_file, 'r') as f:
            data = json.load(f)

        # Find and remove the completed task
        completed_task = None
        for i, task in enumerate(data['tasks']):
            if task.get('id') == task_id:
                completed_task = data['tasks'].pop(i)
                break

        if not completed_task:
            print(f"❌ Task not found: {task_id}")
            return False

        # Save updated tasks.json
        with open(task_file, 'w') as f:
            json.dump(data, f, indent=2)

        # Log to tasks-completed.md
        completed_file = client_dir / 'tasks-completed.md'

        # Create completion entry
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        entry = f"""
## {completed_task['title']}
**Completed:** {timestamp}
**Source:** Manual completion (via complete_task.py)

"""

        if completion_notes:
            entry += f"{completion_notes}\n\n"

        entry += "---\n"

        # Append to tasks-completed.md
        with open(completed_file, 'a') as f:
            f.write(entry)

        return True
    except Exception as e:
        print(f"❌ Error completing internal task: {e}")
        return False

def main():
    """Main completion routine"""
    import argparse

    parser = argparse.ArgumentParser(description='Complete a task with automatic routing')
    parser.add_argument('--task-id', help='Task ID (required for auto-detection)')
    parser.add_argument('--title', help='Task title (for context)')
    parser.add_argument('--client', help='Client name (for internal tasks)')
    parser.add_argument('--notes', help='Completion notes')
    parser.add_argument('--source', choices=['google-tasks', 'internal'], help='Force source (skip auto-detection)')
    parser.add_argument('--list-id', help='Google Tasks list ID (if known)')

    args = parser.parse_args()

    if not args.task_id and not args.title:
        print("❌ Error: Must provide either --task-id or --title")
        return 1

    # Determine source
    if args.source:
        source = args.source
        details = {}
    else:
        source, details = determine_task_source(
            task_id=args.task_id,
            task_title=args.title,
            client_name=args.client
        )

    print(f"Task source: {source}")

    # Complete the task
    if source == 'google-tasks':
        if not args.task_id or not args.list_id:
            print("❌ Error: Google Tasks require --task-id and --list-id")
            return 1

        success = complete_google_task(
            task_id=args.task_id,
            task_list_id=args.list_id,
            completion_notes=args.notes
        )

        if success:
            print(f"✅ Google Task completed: {args.title}")

    elif source == 'internal':
        if not args.client:
            client = details.get('client_name')
            if not client:
                print("❌ Error: Internal tasks require --client")
                return 1
        else:
            client = args.client

        if not args.task_id:
            print("❌ Error: Internal tasks require --task-id")
            return 1

        success = complete_internal_task(
            client_name=client,
            task_id=args.task_id,
            completion_notes=args.notes
        )

        if success:
            print(f"✅ Internal task completed: {args.title}")
            print(f"   Logged to: clients/{client}/tasks-completed.md")

    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
