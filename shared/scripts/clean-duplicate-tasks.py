#!/usr/bin/env python3
"""
Clean Duplicate AI-Generated Tasks in Google Tasks

Removes duplicate tasks from "Client Work" list based on:
- Same client
- Similar task title (>85% similarity)
- Keeps only the most recent version
- Preserves Product Impact Analyzer tasks (they're legitimate)
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from difflib import SequenceMatcher

# Add MCP server path
PROJECT_ROOT = Path(__file__).parent.parent.parent
MCP_SERVER_PATH = PROJECT_ROOT / "shared" / "mcp-servers" / "google-tasks-mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from tasks_service import tasks_service
except ImportError:
    print("Error: tasks_service module not found")
    sys.exit(1)


def calculate_similarity(str1, str2):
    """Calculate similarity between two strings (0.0 to 1.0)"""
    return SequenceMatcher(None, str1.lower().strip(), str2.lower().strip()).ratio()


def extract_client_from_task(task):
    """Extract client name from task title"""
    title = task.get('title', '')
    # Check for [Client Name] pattern
    import re
    match = re.match(r'^\[(.+?)\]', title)
    if match:
        return match.group(1).lower().replace(' ', '-')
    return None


def is_product_analyzer_task(task):
    """Check if task is from Product Impact Analyzer (preserve these)"""
    title = task.get('title', '')
    # Product Impact Analyzer tasks have priority prefixes like [URGENT], [HIGH], [MEDIUM], [LOW]
    if title.startswith('[URGENT]') or title.startswith('[HIGH]') or \
       title.startswith('[MEDIUM]') or title.startswith('[LOW]'):
        return True
    return False


def get_task_creation_date(task):
    """Get task creation/update date"""
    updated = task.get('updated', '')
    if updated:
        try:
            return datetime.fromisoformat(updated.replace('Z', '+00:00'))
        except:
            pass
    return datetime.min


def find_duplicate_groups(tasks):
    """Group duplicate tasks together"""
    # Group by client first
    client_groups = {}

    for task in tasks:
        # Skip Product Impact Analyzer tasks
        if is_product_analyzer_task(task):
            continue

        client = extract_client_from_task(task)
        if not client:
            continue

        if client not in client_groups:
            client_groups[client] = []
        client_groups[client].append(task)

    # Find duplicates within each client group
    duplicate_groups = []

    for client, client_tasks in client_groups.items():
        # Compare all tasks pairwise
        processed = set()

        for i, task1 in enumerate(client_tasks):
            if task1['id'] in processed:
                continue

            # Find all similar tasks
            group = [task1]
            title1 = task1.get('title', '')

            for j, task2 in enumerate(client_tasks):
                if i == j or task2['id'] in processed:
                    continue

                title2 = task2.get('title', '')
                similarity = calculate_similarity(title1, title2)

                # 85% similarity threshold
                if similarity >= 0.85:
                    group.append(task2)
                    processed.add(task2['id'])

            if len(group) > 1:
                # Sort by creation date (newest first)
                group.sort(key=get_task_creation_date, reverse=True)
                duplicate_groups.append({
                    'client': client,
                    'tasks': group,
                    'title': group[0].get('title', 'Untitled')
                })
                processed.add(task1['id'])

    return duplicate_groups


def main():
    print("🧹 Cleaning Duplicate AI-Generated Tasks")
    print("=" * 60)

    # Load config
    config_file = PROJECT_ROOT / 'shared' / 'config' / 'ai-tasks-config.json'
    if not config_file.exists():
        print("Error: Config file not found")
        return 1

    with open(config_file, 'r') as f:
        config = json.load(f)

    task_list_id = config.get('task_list_id')
    if not task_list_id:
        print("Error: Task list ID not configured")
        return 1

    # Connect to Google Tasks
    print("\n📡 Connecting to Google Tasks...")
    try:
        service = tasks_service()
        print("✓ Connected")
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        return 1

    # Get all tasks
    print("\n📋 Fetching tasks from 'Client Work' list...")
    try:
        results = service.tasks().list(
            tasklist=task_list_id,
            showCompleted=False,
            maxResults=100
        ).execute()

        tasks = results.get('items', [])
        print(f"✓ Found {len(tasks)} tasks")
    except Exception as e:
        print(f"✗ Failed to fetch tasks: {e}")
        return 1

    # Find duplicates
    print("\n🔍 Analyzing for duplicates...")
    duplicate_groups = find_duplicate_groups(tasks)

    if not duplicate_groups:
        print("✓ No duplicates found!")
        return 0

    print(f"\n⚠️  Found {len(duplicate_groups)} duplicate groups:")
    print()

    total_to_delete = 0
    for group in duplicate_groups:
        print(f"📦 {group['client'].upper()}")
        print(f"   Task: {group['title'][:80]}")
        print(f"   Duplicates: {len(group['tasks'])} copies")
        print()

        # Show which will be kept vs deleted
        kept = group['tasks'][0]
        to_delete = group['tasks'][1:]
        total_to_delete += len(to_delete)

        kept_date = get_task_creation_date(kept)
        print(f"   ✅ KEEP (newest): {kept_date.strftime('%Y-%m-%d %H:%M')}")

        for task in to_delete:
            task_date = get_task_creation_date(task)
            print(f"   ❌ DELETE: {task_date.strftime('%Y-%m-%d %H:%M')}")
        print()

    print(f"💡 Summary: Keep {len(duplicate_groups)} tasks, delete {total_to_delete} duplicates")
    print()

    # Confirm deletion
    response = input("❓ Proceed with deletion? (yes/no): ").strip().lower()

    if response != 'yes':
        print("\n❌ Cancelled - no tasks deleted")
        return 0

    # Delete duplicates
    print("\n🗑️  Deleting duplicate tasks...")
    deleted_count = 0

    for group in duplicate_groups:
        to_delete = group['tasks'][1:]  # Keep first (newest)

        for task in to_delete:
            try:
                service.tasks().delete(
                    tasklist=task_list_id,
                    task=task['id']
                ).execute()
                deleted_count += 1
                print(f"   ✓ Deleted: {task.get('title', 'Untitled')[:60]}")
            except Exception as e:
                print(f"   ✗ Failed to delete {task['id']}: {e}")

    print()
    print(f"✅ Cleanup complete! Deleted {deleted_count} duplicate tasks")
    print(f"✅ Kept {len(duplicate_groups)} most recent versions")

    return 0


if __name__ == "__main__":
    sys.exit(main())
