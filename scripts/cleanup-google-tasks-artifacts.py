#!/usr/bin/env python3
"""
Clean up Google Tasks migration artifacts from client task files.

This script removes:
- google_task_id from context
- google_list from context
- migrated_at from context
- "Google Tasks Import" source (changes to "Manual")
- "migrated-from-google-tasks" tags

Run with --dry-run to see changes without applying them.
Run with --live to actually clean up the files.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def cleanup_task(task: Dict[str, Any]) -> tuple[Dict[str, Any], List[str]]:
    """
    Remove Google Tasks artifacts from a single task.

    Returns:
        (cleaned_task, changes_made)
    """
    changes = []
    cleaned = task.copy()

    # Clean context
    if 'context' in cleaned and isinstance(cleaned['context'], dict):
        context = cleaned['context']

        if 'google_task_id' in context:
            del context['google_task_id']
            changes.append(f"Removed google_task_id from context")

        if 'google_list' in context:
            del context['google_list']
            changes.append(f"Removed google_list from context")

        if 'migrated_at' in context:
            del context['migrated_at']
            changes.append(f"Removed migrated_at from context")

        # If context is now empty, keep it as empty dict (not remove entirely)
        cleaned['context'] = context

    # Clean source
    if cleaned.get('source') == 'Google Tasks Import':
        cleaned['source'] = 'Migrated from Google Tasks (Nov 18, 2025)'
        changes.append(f"Changed source from 'Google Tasks Import' to 'Migrated from Google Tasks'")

    # Clean tags
    if 'tags' in cleaned and isinstance(cleaned['tags'], list):
        original_tags = cleaned['tags'].copy()
        cleaned['tags'] = [tag for tag in cleaned['tags'] if tag != 'migrated-from-google-tasks']

        if len(cleaned['tags']) != len(original_tags):
            changes.append(f"Removed 'migrated-from-google-tasks' tag")

    return cleaned, changes


def cleanup_client_tasks(client_name: str, task_file: Path, dry_run: bool = True) -> tuple[int, List[str]]:
    """
    Clean up all tasks for a specific client.

    Returns:
        (num_tasks_cleaned, all_changes)
    """
    # Load tasks
    try:
        with open(task_file, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"  ❌ Error reading {task_file}: {e}")
        return 0, []

    tasks = data.get('tasks', [])
    all_changes = []
    num_cleaned = 0

    # Clean each task
    cleaned_tasks = []
    for task in tasks:
        cleaned_task, changes = cleanup_task(task)
        cleaned_tasks.append(cleaned_task)

        if changes:
            num_cleaned += 1
            all_changes.extend([f"  Task '{task.get('title', 'Unknown')[:50]}': {change}" for change in changes])

    # Save if not dry run
    if not dry_run and num_cleaned > 0:
        data['tasks'] = cleaned_tasks
        data['last_updated'] = datetime.now().isoformat()

        with open(task_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return num_cleaned, all_changes


def main():
    # Parse arguments
    dry_run = '--live' not in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print("   Run with --live to actually clean up files\n")
    else:
        print("🔴 LIVE MODE - Files will be modified\n")

    clients_dir = Path('/Users/administrator/Documents/PetesBrain/clients')

    if not clients_dir.exists():
        print(f"❌ Clients directory not found: {clients_dir}")
        return 1

    # Find all client task files
    total_clients = 0
    total_tasks_cleaned = 0
    clients_with_artifacts = []

    for client_dir in sorted(clients_dir.iterdir()):
        if client_dir.is_dir() and not client_dir.name.startswith('_'):
            task_file = client_dir / 'tasks.json'

            if task_file.exists():
                total_clients += 1
                num_cleaned, changes = cleanup_client_tasks(client_dir.name, task_file, dry_run)

                if num_cleaned > 0:
                    clients_with_artifacts.append(client_dir.name)
                    total_tasks_cleaned += num_cleaned

                    print(f"📋 {client_dir.name}")
                    print(f"   Tasks with artifacts: {num_cleaned}")
                    for change in changes:
                        print(f"   {change}")
                    print()

    # Summary
    print("=" * 80)
    print(f"\n📊 Summary:")
    print(f"   Total clients scanned: {total_clients}")
    print(f"   Clients with Google Tasks artifacts: {len(clients_with_artifacts)}")
    print(f"   Total tasks cleaned: {total_tasks_cleaned}")

    if clients_with_artifacts:
        print(f"\n   Clients affected:")
        for client in clients_with_artifacts:
            print(f"     - {client}")

    if dry_run:
        print(f"\n⚠️  DRY RUN - No changes were made")
        print(f"   Run with --live to apply these changes")
    else:
        print(f"\n✅ LIVE RUN - All changes applied")
        print(f"   Backup recommendation: Check git status and commit before this run")

    return 0


if __name__ == '__main__':
    sys.exit(main())
