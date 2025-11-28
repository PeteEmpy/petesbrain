#!/usr/bin/env python3
"""
Deduplicate Google Tasks

Identifies and removes duplicate tasks based on title similarity.
Keeps the oldest task (earliest creation date) and deletes duplicates.

Usage:
    python3 deduplicate-google-tasks.py                # Interactive mode
    python3 deduplicate-google-tasks.py --auto-confirm  # Auto-delete duplicates
"""

import sys
from pathlib import Path
import difflib
from datetime import datetime
import argparse

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.google_tasks_client import GoogleTasksClient

def normalize_title(title):
    """Normalize task title for comparison"""
    # Remove AI task IDs, dates, and common variations
    title = title.lower().strip()
    # Remove date patterns
    import re
    title = re.sub(r'\d{4}-\d{2}-\d{2}', '', title)
    title = re.sub(r'\(\d+% roas.*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'ai task id:.*', '', title, flags=re.IGNORECASE)
    return title.strip()

def are_similar(title1, title2, threshold=0.85):
    """Check if two titles are similar"""
    norm1 = normalize_title(title1)
    norm2 = normalize_title(title2)

    # Exact match after normalization
    if norm1 == norm2:
        return True

    # Fuzzy match
    ratio = difflib.SequenceMatcher(None, norm1, norm2).ratio()
    return ratio >= threshold

def find_duplicates(tasks):
    """Find duplicate tasks"""
    duplicates = []
    seen = []

    for i, task in enumerate(tasks):
        task_title = task.get('title', '')
        task_id = task.get('id')

        # Check against all previously seen tasks
        for j, seen_task in enumerate(seen):
            if are_similar(task_title, seen_task.get('title', '')):
                # Found a duplicate
                # Keep the first one (older), mark current as duplicate
                duplicates.append({
                    'keep': seen_task,
                    'delete': task,
                    'reason': f"Duplicate of '{seen_task.get('title')[:60]}...'"
                })
                break
        else:
            # Not a duplicate, add to seen list
            seen.append(task)

    return duplicates

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Deduplicate Google Tasks')
    parser.add_argument('--auto-confirm', action='store_true',
                       help='Automatically delete duplicates without prompting')
    args = parser.parse_args()

    print("=" * 80)
    print("GOOGLE TASKS DEDUPLICATION")
    print("=" * 80)
    if args.auto_confirm:
        print("🤖 AUTO-CONFIRM MODE: Will delete duplicates without prompting")
    print()

    client = GoogleTasksClient()

    # Get all tasks
    print("📋 Fetching all tasks...")
    all_tasks = client.get_all_active_tasks()

    # Group by list
    tasks_by_list = {}
    for task in all_tasks:
        list_name = task.get('list_name', 'Unknown')
        if list_name not in tasks_by_list:
            tasks_by_list[list_name] = []
        tasks_by_list[list_name].append(task)

    # Get list IDs mapping
    lists_result = client.service.tasklists().list().execute()
    list_id_map = {lst['title']: lst['id'] for lst in lists_result.get('items', [])}

    total_duplicates = 0
    deleted_count = 0

    for list_name, tasks in tasks_by_list.items():
        print(f"\n{'=' * 80}")
        print(f"📝 List: {list_name}")
        print(f"{'=' * 80}")
        print(f"Total tasks: {len(tasks)}")

        # Find duplicates in this list
        duplicates = find_duplicates(tasks)

        if not duplicates:
            print("✅ No duplicates found")
            continue

        print(f"\n🔍 Found {len(duplicates)} duplicate(s):")
        print()

        for i, dup in enumerate(duplicates, 1):
            keep_task = dup['keep']
            delete_task = dup['delete']

            print(f"{i}. KEEPING:")
            print(f"   Title: {keep_task.get('title')[:80]}")
            print(f"   ID: {keep_task.get('id')}")
            print(f"   Status: {keep_task.get('status')}")
            print()
            print(f"   DELETING:")
            print(f"   Title: {delete_task.get('title')[:80]}")
            print(f"   ID: {delete_task.get('id')}")
            print(f"   Status: {delete_task.get('status')}")
            print(f"   Reason: {dup['reason']}")
            print()

        # Ask for confirmation (or auto-confirm)
        if args.auto_confirm:
            response = 'yes'
            print(f"\n🤖 AUTO-CONFIRMING: Deleting {len(duplicates)} duplicate task(s)...")
        else:
            response = input(f"\n❓ Delete {len(duplicates)} duplicate task(s) from '{list_name}'? (yes/no): ").strip().lower()

        if response == 'yes':
            list_id = list_id_map.get(list_name)
            if not list_id:
                print(f"   ❌ Could not find list ID for '{list_name}'")
                continue

            for dup in duplicates:
                delete_task = dup['delete']
                task_id = delete_task.get('id')

                try:
                    client.service.tasks().delete(tasklist=list_id, task=task_id).execute()
                    print(f"   ✅ Deleted: {delete_task.get('title')[:60]}...")
                    deleted_count += 1
                except Exception as e:
                    print(f"   ❌ Error deleting task: {e}")

            total_duplicates += len(duplicates)
        else:
            print(f"   ⏭️  Skipped {len(duplicates)} duplicate(s)")

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total duplicates found: {total_duplicates}")
    print(f"Total tasks deleted: {deleted_count}")
    print()

if __name__ == '__main__':
    main()
