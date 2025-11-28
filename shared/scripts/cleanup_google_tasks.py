#!/usr/bin/env python3
"""
Clean up Google Tasks "Client Work" list after migration

This script deletes all tasks from the "Client Work" list since they've
been successfully migrated to the internal task system.

The list itself remains (can be repurposed), but all tasks are deleted.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'shared'))

from google_tasks_client import GoogleTasksClient


def cleanup_client_work_list(dry_run=True):
    """
    Delete all tasks from the "Client Work" Google Tasks list.

    Args:
        dry_run: If True, only show what would be deleted (don't actually delete)
    """
    print("=" * 70)
    print("GOOGLE TASKS CLEANUP: Delete migrated tasks from 'Client Work'")
    print("=" * 70)

    if dry_run:
        print("\n⚠️  DRY RUN MODE - No tasks will be deleted\n")
    else:
        print("\n🚨 LIVE MODE - Tasks will be permanently deleted\n")

    # Initialize Google Tasks client
    client = GoogleTasksClient()

    # Get tasks from "Client Work" list
    print("📥 Fetching tasks from 'Client Work' list...")
    try:
        tasks = client.list_tasks('Client Work', show_completed=False)
        print(f"   Found {len(tasks)} active tasks\n")

        if len(tasks) == 0:
            print("✅ No tasks to delete - list is already clean!")
            return

    except Exception as e:
        print(f"❌ Error fetching tasks: {e}")
        return

    # Show tasks that will be deleted
    print("📋 Tasks to delete:\n")
    for i, task in enumerate(tasks, 1):
        title = task.get('title', 'Untitled')
        print(f"{i}. {title}")

    print(f"\n{'─' * 70}")
    print(f"Total: {len(tasks)} tasks will be deleted")
    print(f"{'─' * 70}\n")

    if dry_run:
        print("⚠️  This was a DRY RUN. No tasks were deleted.")
        print("   Run with --live to actually delete these tasks.")
        return

    # Confirm deletion
    print("⚠️  WARNING: This will permanently delete all tasks shown above!")
    print("   The tasks are already migrated to the internal system.")
    print("   The 'Client Work' list itself will remain (empty).\n")

    # Delete tasks
    print("🗑️  Deleting tasks...")
    deleted_count = 0
    errors = []

    for task in tasks:
        title = task.get('title', 'Untitled')
        task_id = task.get('id')

        try:
            # Delete the task
            success = client.delete_task(task_id, list_name='Client Work')
            if success:
                deleted_count += 1
                print(f"   ✅ Deleted: {title}")
            else:
                errors.append((title, "Delete returned False"))
                print(f"   ❌ Failed: {title}")
        except Exception as e:
            errors.append((title, str(e)))
            print(f"   ❌ Error deleting {title}: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("CLEANUP SUMMARY")
    print("=" * 70)
    print(f"✅ Deleted: {deleted_count}/{len(tasks)}")

    if errors:
        print(f"❌ Errors: {len(errors)}")
        for title, error in errors:
            print(f"   - {title}: {error}")

    print("\n✅ Cleanup complete!")
    print("   All client tasks now managed by internal system")
    print("   'Client Work' list remains empty and available for reuse")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Clean up migrated tasks from Google Tasks')
    parser.add_argument('--live', action='store_true', help='Actually delete tasks (default is dry run)')
    args = parser.parse_args()

    cleanup_client_work_list(dry_run=not args.live)
