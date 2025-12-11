#!/usr/bin/env python3
"""
Task Priority Updater
Automatically reassesses all task priorities daily based on due dates.

Priority Rules:
- P0: 0-2 days until due (urgent/immediate)
- P1: 3-14 days until due (this week/next week)
- P2: 15-30 days until due (next 2-4 weeks)
- P3: 30+ days until due (later)

Runs: Daily at 20:00 (8:00 PM)
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import sys
import re

# Import centralized path discovery
try:
    from shared.paths import get_project_root
    PROJECT_ROOT = get_project_root()
except ImportError:
    # Fallback: use PETESBRAIN_ROOT environment variable or relative path
    project_root_env = os.getenv('PETESBRAIN_ROOT')
    if project_root_env:
        PROJECT_ROOT = Path(project_root_env)
    else:
        PROJECT_ROOT = Path(__file__).parent.parent.parent

def parse_due_date(due_date_str):
    """Parse due date string into datetime object, supporting multiple formats."""
    if not due_date_str:
        return None

    today = datetime.now()

    # Try standard YYYY-MM-DD format first
    try:
        return datetime.strptime(due_date_str, '%Y-%m-%d')
    except ValueError:
        pass

    # Handle natural language dates
    due_date_lower = due_date_str.lower().strip()

    # "today"
    if due_date_lower in ['today', 'now']:
        return today

    # "tomorrow"
    if due_date_lower == 'tomorrow':
        return today + timedelta(days=1)

    # "within next week" / "next week" / "this week"
    if any(phrase in due_date_lower for phrase in ['within next week', 'next week', 'this week']):
        return today + timedelta(days=7)

    # "within X days" / "in X days"
    match = re.search(r'(?:within|in)\s+(\d+)\s+days?', due_date_lower)
    if match:
        days = int(match.group(1))
        return today + timedelta(days=days)

    # "X days from now"
    match = re.search(r'(\d+)\s+days?\s+from\s+now', due_date_lower)
    if match:
        days = int(match.group(1))
        return today + timedelta(days=days)

    # If we can't parse it, return None (will skip priority update)
    return None

def calculate_priority(due_date_str):
    """Calculate correct priority based on days until due."""
    if not due_date_str:
        return None  # Keep existing priority for tasks without due dates

    today = datetime.now()
    due_date = parse_due_date(due_date_str)

    if due_date is None:
        # Log warning but don't crash
        return None

    days_until = (due_date - today).days

    if days_until <= 2:
        return 'P0'
    elif days_until <= 14:
        return 'P1'
    elif days_until <= 30:
        return 'P2'
    else:
        return 'P3'

def update_task_priorities():
    """Update priorities for all active tasks across all clients."""
    clients_dir = PROJECT_ROOT / 'clients'
    roksys_dir = PROJECT_ROOT / 'roksys'

    total_tasks = 0
    updated_tasks = 0
    changes = []

    # Collect all task files to process
    task_files = []

    # 1. Client tasks (root location is primary)
    for client_dir in sorted(clients_dir.iterdir()):
        if client_dir.is_dir() and not client_dir.name.startswith('_'):
            # Check root location first (primary for all client work)
            direct_task_file = client_dir / 'tasks.json'
            if direct_task_file.exists():
                task_files.append((client_dir.name, direct_task_file))
            # Also check product-feeds (legacy location - should be migrated)
            pf_task_file = client_dir / 'product-feeds' / 'tasks.json'
            if pf_task_file.exists():
                task_files.append((client_dir.name, direct_task_file))

    # 2. Main clients queue
    main_queue = clients_dir / 'tasks.json'
    if main_queue.exists():
        task_files.append(('main-queue', main_queue))

    # 3. Roksys internal tasks
    roksys_tasks = roksys_dir / 'tasks.json'
    if roksys_tasks.exists():
        task_files.append(('roksys', roksys_tasks))

    for client_name, task_file in task_files:
        # Read tasks
        with open(task_file, 'r') as f:
            data = json.load(f)

        modified = False

        for task in data.get('tasks', []):
            if task.get('status') != 'active':
                continue

            total_tasks += 1

            # Calculate new priority
            new_priority = calculate_priority(task.get('due_date'))

            # Skip if no due date
            if new_priority is None:
                continue

            old_priority = task.get('priority')

            # Update if changed
            if old_priority != new_priority:
                task['priority'] = new_priority
                modified = True
                updated_tasks += 1

                changes.append({
                    'client': client_name,
                    'title': task['title'],
                    'due': task['due_date'],
                    'old': old_priority,
                    'new': new_priority
                })

        # Save if modified
        if modified:
            data['last_updated'] = datetime.now().isoformat()
            with open(task_file, 'w') as f:
                json.dump(data, f, indent=2)

    return {
        'total_tasks': total_tasks,
        'updated_tasks': updated_tasks,
        'changes': changes
    }

def main():
    """Main execution."""
    print(f"Task Priority Updater - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    result = update_task_priorities()

    print(f"\nProcessed: {result['total_tasks']} active tasks")
    print(f"Updated: {result['updated_tasks']} tasks")

    if result['changes']:
        print(f"\nPriority Changes:")
        print("-" * 80)
        for change in result['changes']:
            print(f"{change['old']} → {change['new']}: [{change['client']}] {change['title'][:50]}...")
            print(f"           Due: {change['due']}")
    else:
        print("\n✅ All priorities already correct - no changes needed")

    # Regenerate tasks overview
    import subprocess
    subprocess.run([
        'python3',
        str(PROJECT_ROOT / 'generate-tasks-overview.py')
    ], capture_output=True)

    print("\n✅ Task priorities updated and overview regenerated")

    return 0 if result['updated_tasks'] == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
