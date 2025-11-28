#!/usr/bin/env python3
"""
Helper script to update Google Tasks by title.

Usage:
    python3 shared/scripts/update_google_task.py "Devonshire month end" --due "Friday"
    python3 shared/scripts/update_google_task.py "Task title" --due "2025-11-07"
    python3 shared/scripts/update_google_task.py "Task title" --complete
"""

import sys
from pathlib import Path

# Add parent directory to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "shared"))

from google_tasks_client import GoogleTasksClient
import argparse
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        description="Update Google Tasks by searching for text in the title"
    )
    parser.add_argument(
        "search_term",
        help="Text to search for in task title (partial match)"
    )
    parser.add_argument(
        "--due",
        help="New due date (e.g., 'Friday', '2025-11-07', 'tomorrow')"
    )
    parser.add_argument(
        "--title",
        help="New task title"
    )
    parser.add_argument(
        "--notes",
        help="New task notes"
    )
    parser.add_argument(
        "--complete",
        action="store_true",
        help="Mark task as completed"
    )
    parser.add_argument(
        "--list",
        default="Peter's List",
        help="Task list name (default: 'Peter's List')"
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Require exact title match (default: partial match)"
    )

    args = parser.parse_args()

    # Initialize client
    try:
        client = GoogleTasksClient()
    except Exception as e:
        print(f"❌ Error connecting to Google Tasks: {e}")
        sys.exit(1)

    # Find the task
    print(f"🔍 Searching for task containing: '{args.search_term}'")
    task = client.get_task_by_title(
        args.search_term,
        list_name=args.list,
        exact_match=args.exact
    )

    if not task:
        print(f"❌ Task not found matching '{args.search_term}' in '{args.list}'")
        print(f"\n💡 Try searching with a partial match, or list all tasks:")
        print(f"   python3 -c \"from shared.google_tasks_client import GoogleTasksClient; client = GoogleTasksClient(); tasks = client.list_tasks('{args.list}'); [print(f'  - {{t.get(\\\"title\\\")}}') for t in tasks]\"")
        sys.exit(1)

    print(f"✅ Found task: '{task.get('title')}'")
    print(f"   ID: {task.get('id')}")
    if task.get('due'):
        print(f"   Current due date: {task.get('due')}")

    # Prepare update
    task_id = task['id']
    due_date = args.due
    title_new = args.title
    notes_new = args.notes

    # Handle completion
    if args.complete:
        print(f"\n📝 Marking task as completed...")
        result = client.complete_task(task_id, list_name=args.list)
        if result:
            print(f"✅ Task marked as completed!")
        else:
            print(f"❌ Failed to complete task")
            sys.exit(1)
        return

    # Handle updates
    if not any([due_date, title_new, notes_new]):
        print(f"\n⚠️  No updates specified. Use --due, --title, or --notes to update the task.")
        sys.exit(1)

    print(f"\n📝 Updating task...")
    result = client.update_task(
        task_id=task_id,
        title=title_new,
        notes=notes_new,
        due_date=due_date,
        list_name=args.list
    )

    if result:
        print(f"✅ Task updated successfully!")
        print(f"   Title: {result.get('title')}")
        if result.get('due'):
            print(f"   Due date: {result.get('due')}")
    else:
        print(f"❌ Failed to update task")
        sys.exit(1)


if __name__ == "__main__":
    main()

