#!/usr/bin/env python3
"""
Cleanup Duplicate Tasks Script

Removes duplicate tasks from Google Tasks "Client Work" list.
Keeps the oldest open task (or newest completed if all are completed).
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Add MCP server path
MCP_SERVER_PATH = PROJECT_ROOT / "shared" / "mcp-servers" / "google-tasks-mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from tasks_service import tasks_service
except ImportError as e:
    print(f"Error importing tasks_service: {e}")
    print("Make sure you're running this from the project root with proper Python environment")
    sys.exit(1)


def normalize_title(title: str) -> str:
    """Normalize task title for comparison."""
    import re
    # Remove client prefix if present
    title = re.sub(r'^\[.+?\]\s*', '', title).strip()
    # Lowercase and normalize whitespace
    return ' '.join(title.lower().split())


def find_duplicate_groups(task_list_id: str, client_filter: str = None) -> Dict:
    """Find duplicate task groups."""
    try:
        service = tasks_service()
        
        # Get all tasks
        results = service.tasks().list(
            tasklist=task_list_id,
            showCompleted=True,
            maxResults=100
        ).execute()
        
        items = results.get('items', [])
        print(f"Found {len(items)} total tasks")
        
        # Group by client and normalized title
        groups = defaultdict(list)
        
        for item in items:
            title = item.get('title', '')
            notes = item.get('notes', '')
            task_id = item.get('id')
            status = item.get('status', 'needsAction')
            updated = item.get('updated', '')
            
            # Detect client
            client = None
            if '[Smythson]' in title or 'smythson' in title.lower():
                client = 'smythson'
            elif '**Client:**' in notes:
                for line in notes.split('\n'):
                    if '**Client:**' in line:
                        client = line.split('**Client:**')[1].strip().lower()
                        break
            
            if not client:
                import re
                title_match = re.match(r'^\[(.+?)\]\s*', title)
                if title_match:
                    potential_client = title_match.group(1).lower().replace(' ', '-')
                    if not client_filter or potential_client == client_filter:
                        client = potential_client
            
            if client and (not client_filter or client == client_filter):
                normalized = normalize_title(title)
                groups[(client, normalized)].append({
                    'id': task_id,
                    'title': title,
                    'status': status,
                    'updated': updated
                })
        
        # Filter to only duplicates
        duplicates = {k: v for k, v in groups.items() if len(v) > 1}
        
        return {
            'duplicates': duplicates,
            'total_groups': len(duplicates),
            'total_duplicate_tasks': sum(len(v) for v in duplicates.values())
        }
    
    except Exception as e:
        print(f"Error finding duplicates: {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}


def cleanup_duplicates(task_list_id: str, client_filter: str = None, dry_run: bool = True) -> Dict:
    """
    Clean up duplicate tasks.
    
    Args:
        task_list_id: Google Tasks list ID
        client_filter: Optional client name filter
        dry_run: If True, only report what would be deleted (default: True)
    
    Returns:
        Dict with cleanup results
    """
    result = find_duplicate_groups(task_list_id, client_filter)
    
    if 'error' in result:
        return result
    
    duplicates = result['duplicates']
    
    if not duplicates:
        print("\nNo duplicates found!")
        return {'deleted': 0, 'kept': 0, 'groups_processed': 0}
    
    print(f"\nFound {result['total_groups']} duplicate groups")
    print(f"Total duplicate tasks: {result['total_duplicate_tasks']}")
    
    if dry_run:
        print("\n" + "=" * 80)
        print("DRY RUN MODE - No tasks will be deleted")
        print("=" * 80)
    
    try:
        service = tasks_service()
    except Exception as e:
        return {'error': f"Failed to connect to Google Tasks: {e}"}
    
    deleted_count = 0
    kept_count = 0
    errors = []
    
    for (client, normalized_title), tasks in sorted(duplicates.items()):
        print(f"\n[{client}] {normalized_title}")
        print(f"  Found {len(tasks)} duplicate(s)")
        
        # Sort by updated date
        sorted_tasks = sorted(tasks, key=lambda x: x['updated'])
        
        # Find open tasks first
        open_tasks = [t for t in sorted_tasks if t['status'] != 'completed']
        
        if open_tasks:
            # Keep oldest open task
            keep_task = open_tasks[0]
            delete_tasks = [t for t in sorted_tasks if t['id'] != keep_task['id']]
        else:
            # All completed - keep newest
            keep_task = sorted_tasks[-1]
            delete_tasks = sorted_tasks[:-1]
        
        print(f"  → Keep: {keep_task['title']} (ID: {keep_task['id']}, Status: {keep_task['status']})")
        kept_count += 1
        
        for task in delete_tasks:
            print(f"  → Delete: {task['title']} (ID: {task['id']}, Status: {task['status']})")
            
            if not dry_run:
                try:
                    service.tasks().delete(
                        tasklist=task_list_id,
                        task=task['id']
                    ).execute()
                    deleted_count += 1
                    print(f"     ✓ Deleted")
                except Exception as e:
                    error_msg = f"Failed to delete {task['id']}: {e}"
                    errors.append(error_msg)
                    print(f"     ✗ Error: {error_msg}")
            else:
                deleted_count += 1
    
    result = {
        'deleted': deleted_count,
        'kept': kept_count,
        'groups_processed': len(duplicates),
        'errors': errors
    }
    
    if dry_run:
        print("\n" + "=" * 80)
        print(f"DRY RUN COMPLETE")
        print(f"Would delete: {deleted_count} tasks")
        print(f"Would keep: {kept_count} tasks")
        print("=" * 80)
        print("\nRun with --execute to actually delete duplicates")
    else:
        print("\n" + "=" * 80)
        print(f"CLEANUP COMPLETE")
        print(f"Deleted: {deleted_count} tasks")
        print(f"Kept: {kept_count} tasks")
        if errors:
            print(f"Errors: {len(errors)}")
        print("=" * 80)
    
    return result


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Clean up duplicate tasks in Google Tasks')
    parser.add_argument('--client', help='Filter by client name (e.g., smythson)')
    parser.add_argument('--execute', action='store_true', help='Actually delete duplicates (default is dry-run)')
    parser.add_argument('--list-only', action='store_true', help='Only list duplicates, don\'t clean up')
    
    args = parser.parse_args()
    
    # Load config
    config_file = PROJECT_ROOT / "shared" / "config" / "ai-tasks-config.json"
    if not config_file.exists():
        print(f"Error: Config file not found: {config_file}")
        sys.exit(1)
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    task_list_id = config.get('task_list_id')
    if not task_list_id or task_list_id == "PLACEHOLDER_WILL_BE_SET_ON_FIRST_RUN":
        print("Error: Task list ID not configured")
        sys.exit(1)
    
    print(f"Task List: {config.get('task_list_name', 'Unknown')} ({task_list_id})")
    if args.client:
        print(f"Filter: {args.client}")
    
    if args.list_only:
        result = find_duplicate_groups(task_list_id, args.client)
        if 'error' not in result:
            duplicates = result['duplicates']
            print(f"\nFound {len(duplicates)} duplicate groups:")
            for (client, title), tasks in sorted(duplicates.items()):
                print(f"\n[{client}] {title}: {len(tasks)} duplicates")
                for task in tasks:
                    print(f"  - {task['title']} ({task['id']}, {task['status']})")
    else:
        cleanup_duplicates(task_list_id, args.client, dry_run=not args.execute)


if __name__ == "__main__":
    main()

