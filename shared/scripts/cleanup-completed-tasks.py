#!/usr/bin/env python3
"""
Cleanup Completed Tasks Script

Removes tasks marked as 'completed' from tasks.json files.
These should have already been logged to tasks-completed.md.

Run this weekly to keep tasks.json files clean.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
CLIENTS_DIR = PROJECT_ROOT / 'clients'
ROKSYS_DIR = PROJECT_ROOT / 'roksys'


def cleanup_client_tasks(client_dir: Path, dry_run: bool = False) -> dict:
    """
    Clean up completed tasks from a client's tasks.json file.

    Args:
        client_dir: Path to client directory
        dry_run: If True, don't actually remove tasks, just report

    Returns:
        dict with statistics
    """
    task_file = client_dir / 'tasks.json'

    if not task_file.exists():
        return {'client': client_dir.name, 'removed': 0, 'active': 0}

    # Load tasks
    try:
        with open(task_file, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {'client': client_dir.name, 'removed': 0, 'active': 0, 'error': 'Failed to load tasks.json'}

    original_count = len(data.get('tasks', []))
    completed_tasks = [t for t in data.get('tasks', []) if t.get('status') == 'completed']
    active_tasks = [t for t in data.get('tasks', []) if t.get('status') != 'completed']

    if not completed_tasks:
        return {'client': client_dir.name, 'removed': 0, 'active': len(active_tasks)}

    # Report what will be removed
    result = {
        'client': client_dir.name,
        'removed': len(completed_tasks),
        'active': len(active_tasks),
        'tasks': []
    }

    for task in completed_tasks:
        result['tasks'].append({
            'id': task.get('id'),
            'title': task.get('title'),
            'completed_at': task.get('completed_at', 'unknown')
        })

    # Remove completed tasks
    if not dry_run:
        data['tasks'] = active_tasks
        data['last_updated'] = datetime.now().isoformat()

        with open(task_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return result


def main():
    """Main cleanup function"""
    print("Completed Tasks Cleanup Script")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    # Check for dry-run mode
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print("-" * 60)

    total_removed = 0
    total_active = 0
    clients_affected = 0

    # Process all client directories
    if CLIENTS_DIR.exists():
        for client_dir in sorted(CLIENTS_DIR.iterdir()):
            if not client_dir.is_dir() or client_dir.name.startswith('_'):
                continue

            # Check main tasks.json
            result = cleanup_client_tasks(client_dir, dry_run=dry_run)

            if result.get('error'):
                print(f"⚠️  {result['client']}: {result['error']}")
                continue

            if result['removed'] > 0:
                clients_affected += 1
                total_removed += result['removed']
                total_active += result['active']

                print(f"\n{'[DRY RUN] ' if dry_run else ''}📁 {result['client']}")
                print(f"   Completed tasks to remove: {result['removed']}")
                print(f"   Active tasks remaining: {result['active']}")

                if result.get('tasks'):
                    print(f"   Tasks being removed:")
                    for task in result['tasks']:
                        print(f"      - {task['title'][:60]}...")
                        print(f"        Completed: {task['completed_at']}")

    # Process Roksys directory
    if ROKSYS_DIR.exists():
        result = cleanup_client_tasks(ROKSYS_DIR, dry_run=dry_run)

        if result['removed'] > 0:
            clients_affected += 1
            total_removed += result['removed']
            total_active += result['active']

            print(f"\n{'[DRY RUN] ' if dry_run else ''}📁 Roksys (Internal)")
            print(f"   Completed tasks to remove: {result['removed']}")
            print(f"   Active tasks remaining: {result['active']}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"{'[DRY RUN] ' if dry_run else ''}Clients affected: {clients_affected}")
    print(f"{'[DRY RUN] ' if dry_run else ''}Completed tasks removed: {total_removed}")
    print(f"Active tasks remaining: {total_active}")

    if dry_run:
        print("\n💡 Run without --dry-run to actually remove tasks")
    else:
        print("\n✅ Cleanup complete")

    print("-" * 60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
