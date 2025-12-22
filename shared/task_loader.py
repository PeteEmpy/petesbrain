"""
Shared Task Loading Module
Used by both generate-all-task-views.py and task-manager-server.py

This module provides a single source of truth for loading tasks from:
- clients/*/tasks.json (client tasks)
- roksys/tasks.json (personal/business tasks)
"""

import json
from pathlib import Path
from datetime import datetime

# Determine project root
PROJECT_ROOT = Path(__file__).parent.parent


def escape_template_strings(text):
    """Escape backticks and dollar signs to prevent template string breakage"""
    if not isinstance(text, str):
        return text
    return text.replace('`', '\\`').replace('${', '$\\{')


def get_client_display_name(client_dir):
    """Convert client directory name to display name"""
    # Convert snake-case/kebab-case to Title Case
    name = client_dir.name.replace('-', ' ').replace('_', ' ')
    return ' '.join(word.capitalize() for word in name.split())


def parse_completed_tasks_from_markdown(md_file):
    """Parse completed tasks from tasks-completed.md"""
    if not md_file.exists():
        return []

    # Implementation simplified - just return empty for now
    # Full implementation would parse the markdown file
    return []


def load_all_tasks():
    """
    Load all tasks from client task.json files and roksys/tasks.json

    Returns:
        tuple: (tasks_by_client, all_tasks, all_reminders)
    """
    tasks_by_client = {}
    all_tasks = []
    all_reminders = []
    seen_task_ids = set()

    clients_dir = PROJECT_ROOT / 'clients'

    # Load client tasks (excluding clients/roksys/)
    for client_dir in sorted(clients_dir.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith('_'):
            continue

        # SPECIAL CASE: Skip clients/roksys/ folder
        if client_dir.name == 'roksys':
            continue

        task_file = client_dir / 'tasks.json'
        completed_md_file = client_dir / 'tasks-completed.md'

        # Skip if client has neither tasks.json nor tasks-completed.md
        if not task_file.exists() and not completed_md_file.exists():
            continue

        # Load active tasks from tasks.json (if exists)
        active_tasks = []
        last_updated = 'Unknown'
        if task_file.exists():
            with open(task_file, 'r') as f:
                data = json.load(f)
            active_tasks = [
                t for t in data.get('tasks', [])
                if t.get('status', 'pending') in ['active', 'pending', 'in_progress']
            ]
            last_updated = data.get('last_updated', 'Unknown')

        # Load completed tasks
        completed_tasks = parse_completed_tasks_from_markdown(completed_md_file)

        # Process active tasks
        for task in active_tasks:
            if 'type' not in task:
                task['type'] = 'standalone'

            # Escape template-breaking characters
            if 'notes' in task and task['notes']:
                task['notes'] = escape_template_strings(task['notes'])
            if 'title' in task:
                task['title'] = escape_template_strings(task['title'])

            # Add client context
            task['client_name'] = client_dir.name
            task['client_display'] = get_client_display_name(client_dir)
            task['source'] = 'internal'

            # Add to all_tasks if unique
            task_id = task.get('id')
            if task_id and task_id not in seen_task_ids:
                seen_task_ids.add(task_id)
                all_tasks.append(task)

                # Create reminder entry if has due_date
                if task.get('due_date'):
                    reminder = {
                        'id': task_id,
                        'title': task['title'],
                        'due_date': task['due_date'],
                        'client': client_dir.name,
                        'task_data': task
                    }
                    all_reminders.append(reminder)

        # Sort completed tasks
        completed_tasks.sort(key=lambda x: x.get('completed_at', ''), reverse=True)

        # Separate by type
        parent_tasks = [t for t in active_tasks if t.get('type') == 'parent']
        child_tasks = [t for t in active_tasks if t.get('type') == 'child']
        standalone_tasks = [t for t in active_tasks if t.get('type') == 'standalone']

        # Get P0 count
        p0_count = len([t for t in active_tasks if t.get('priority') == 'P0'])

        # Store client data
        tasks_by_client[client_dir.name] = {
            'name': client_dir.name,
            'display': get_client_display_name(client_dir),
            'path': str(client_dir),
            'active_count': len(active_tasks),
            'completed_count': len(completed_tasks),
            'p0_count': p0_count,
            'parent_tasks': parent_tasks,
            'child_tasks': child_tasks,
            'standalone_tasks': standalone_tasks,
            'completed_tasks': completed_tasks,
            'last_updated': last_updated,
            'all_active_tasks': active_tasks
        }

    # Load roksys tasks from root-level roksys/ directory (SPECIAL CASE)
    roksys_tasks_file = PROJECT_ROOT / 'roksys' / 'tasks.json'
    if roksys_tasks_file.exists():
        roksys_personal_tasks = []
        with open(roksys_tasks_file, 'r') as f:
            data = json.load(f)

        for task in data.get('tasks', []):
            if task.get('status', 'pending') in ['active', 'pending', 'in_progress']:
                task['client_name'] = 'roksys-personal'
                task['client_display'] = 'Roksys (Personal/Business)'
                task['source'] = 'internal'

                if 'type' not in task:
                    task['type'] = 'standalone'
                if 'notes' in task and task['notes']:
                    task['notes'] = escape_template_strings(task['notes'])
                if 'title' in task:
                    task['title'] = escape_template_strings(task['title'])

                task_id = task.get('id')
                if task_id and task_id not in seen_task_ids:
                    seen_task_ids.add(task_id)
                    all_tasks.append(task)
                    roksys_personal_tasks.append(task)

                    # Create reminder entry
                    if task.get('due_date'):
                        reminder = {
                            'id': task_id,
                            'title': task['title'],
                            'due_date': task['due_date'],
                            'client': 'roksys-personal',
                            'task_data': task
                        }
                        all_reminders.append(reminder)

        # Add roksys-personal to client list
        if roksys_personal_tasks:
            p0_count = len([t for t in roksys_personal_tasks if t.get('priority') == 'P0'])
            parent_tasks = [t for t in roksys_personal_tasks if t.get('type') == 'parent']
            child_tasks = [t for t in roksys_personal_tasks if t.get('type') == 'child']
            standalone_tasks = [t for t in roksys_personal_tasks if t.get('type') == 'standalone']

            tasks_by_client['roksys-personal'] = {
                'name': 'roksys-personal',
                'display': 'Roksys (Personal/Business)',
                'path': str(roksys_tasks_file.parent),
                'active_count': len(roksys_personal_tasks),
                'completed_count': 0,
                'p0_count': p0_count,
                'parent_tasks': parent_tasks,
                'child_tasks': child_tasks,
                'standalone_tasks': standalone_tasks,
                'completed_tasks': [],
                'last_updated': datetime.now().isoformat(),
                'all_active_tasks': roksys_personal_tasks
            }

    return tasks_by_client, all_tasks, all_reminders
