#!/usr/bin/env python3
"""
Migrate tasks from global client-tasks.json to per-client task files.

This script:
1. Reads all tasks from data/state/client-tasks.json
2. Groups by client
3. Creates clients/{client}/tasks.json for each client
4. Preserves all task data and metadata
5. Backs up old file
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add shared to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'shared'))

def migrate_tasks(dry_run=True):
    """Migrate tasks from global to per-client files"""

    print("=" * 80)
    print("TASK MIGRATION: Global → Per-Client Architecture")
    print("=" * 80)

    if dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be modified\n")
    else:
        print("\n🚨 LIVE MODE - Files will be modified\n")

    # Paths
    old_file = PROJECT_ROOT / 'data' / 'state' / 'client-tasks.json'
    backup_file = PROJECT_ROOT / 'data' / 'state' / 'client-tasks.json.backup'
    clients_dir = PROJECT_ROOT / 'clients'

    # Load old tasks
    print(f"📥 Loading tasks from: {old_file}")

    if not old_file.exists():
        print("❌ No global task file found - nothing to migrate")
        return

    with open(old_file, 'r') as f:
        old_data = json.load(f)

    old_tasks = old_data.get('tasks', [])
    print(f"   Found {len(old_tasks)} tasks\n")

    if len(old_tasks) == 0:
        print("✅ No tasks to migrate")
        return

    # Group by client
    tasks_by_client = {}
    for task in old_tasks:
        client = task.get('client') or task.get('_client') or 'unassigned'
        if client not in tasks_by_client:
            tasks_by_client[client] = []
        tasks_by_client[client].append(task)

    print(f"📊 Tasks grouped by client:")
    for client, tasks in sorted(tasks_by_client.items()):
        print(f"   {client}: {len(tasks)} tasks")

    print(f"\n{'─' * 80}")
    print("MIGRATION PLAN")
    print(f"{'─' * 80}\n")

    # Show migration plan
    for client, tasks in sorted(tasks_by_client.items()):
        client_file = clients_dir / client / 'tasks.json'
        print(f"➜ {client}")
        print(f"   Target: {client_file}")
        print(f"   Tasks: {len(tasks)}")

        if client_file.exists():
            print(f"   ⚠️  File exists - will merge")
        else:
            print(f"   ✨ New file")
        print()

    if dry_run:
        print("⚠️  This was a DRY RUN. No files were modified.")
        print("   Run with --live to perform migration.")
        return

    # Backup old file
    print(f"\n💾 Backing up old file to: {backup_file}")
    with open(backup_file, 'w') as f:
        json.dump(old_data, f, indent=2, ensure_ascii=False)

    # Migrate tasks
    print(f"\n🔄 Migrating tasks...")

    for client, tasks in sorted(tasks_by_client.items()):
        client_dir = clients_dir / client
        client_file = client_dir / 'tasks.json'

        # Create client directory if needed
        client_dir.mkdir(parents=True, exist_ok=True)

        # Load existing tasks if file exists
        if client_file.exists():
            with open(client_file, 'r') as f:
                client_data = json.load(f)
            existing_tasks = client_data.get('tasks', [])
            print(f"   Merging with {len(existing_tasks)} existing tasks for {client}")
        else:
            client_data = {'tasks': []}
            existing_tasks = []

        # Add migrated tasks (with type='standalone' if not set)
        for task in tasks:
            # Add missing fields for new schema
            if 'type' not in task:
                task['type'] = 'standalone'
            if 'parent_id' not in task:
                task['parent_id'] = None
            if 'children' not in task and task['type'] == 'parent':
                task['children'] = []

            # Remove temporary _client field if present
            if '_client' in task:
                del task['_client']

            client_data['tasks'].append(task)

        # Save
        client_data['last_updated'] = datetime.now().isoformat()
        client_data['migrated_from_global'] = datetime.now().isoformat()

        with open(client_file, 'w') as f:
            json.dump(client_data, f, indent=2, ensure_ascii=False)

        print(f"   ✅ Migrated {len(tasks)} tasks to {client_file}")

    print(f"\n{'=' * 80}")
    print("MIGRATION COMPLETE")
    print(f"{'=' * 80}")
    print(f"\n✅ Migrated {len(old_tasks)} tasks to {len(tasks_by_client)} client files")
    print(f"💾 Backup saved to: {backup_file}")
    print(f"\n📁 Old file location: {old_file}")
    print(f"   You can delete this after verifying migration")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Migrate tasks to per-client architecture')
    parser.add_argument('--live', action='store_true', help='Actually migrate tasks (default is dry run)')
    args = parser.parse_args()

    migrate_tasks(dry_run=not args.live)
