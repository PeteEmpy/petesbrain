#!/usr/bin/env python3
"""
Find Duplicate Tasks Script

Identifies duplicate tasks in Google Tasks "Client Work" list.
Groups duplicates by client and title similarity.
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Add MCP server path
MCP_SERVER_PATH = PROJECT_ROOT / "shared" / "mcp-servers" / "google-tasks-mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from tasks_service import tasks_service
    from duplicate_task_detector import calculate_similarity, is_same_client
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)


def normalize_title(title: str) -> str:
    """Normalize task title for comparison."""
    # Remove client prefix if present
    import re
    title = re.sub(r'^\[.+?\]\s*', '', title).strip()
    # Lowercase and remove extra whitespace
    return ' '.join(title.lower().split())


def find_duplicates(task_list_id: str, client_filter: str = None) -> Dict:
    """
    Find duplicate tasks in Google Tasks.
    
    Args:
        task_list_id: Google Tasks list ID
        client_filter: Optional client name to filter by (e.g., "smythson")
    
    Returns:
        Dict with duplicate groups and statistics
    """
    try:
        service = tasks_service()
        
        # Get all tasks (including completed for context)
        results = service.tasks().list(
            tasklist=task_list_id,
            showCompleted=True,
            maxResults=100
        ).execute()
        
        items = results.get('items', [])
        print(f"Found {len(items)} total tasks in list")
        
        # Group by client and normalized title
        client_groups = defaultdict(list)
        
        for item in items:
            title = item.get('title', '')
            notes = item.get('notes', '')
            task_id = item.get('id')
            status = item.get('status', 'needsAction')
            updated = item.get('updated', '')
            
            # Detect client from title or notes
            client = None
            if '[Smythson]' in title or 'smythson' in title.lower():
                client = 'smythson'
            elif '[Devonshire' in title or 'devonshire' in title.lower():
                client = 'devonshire-hotels'
            elif '**Client:**' in notes:
                # Extract client from notes
                for line in notes.split('\n'):
                    if '**Client:**' in line:
                        client = line.split('**Client:**')[1].strip().lower()
                        break
            
            # Apply client filter if specified
            if client_filter and client != client_filter:
                continue
            
            if not client:
                # Try to detect from other patterns
                import re
                title_match = re.match(r'^\[(.+?)\]\s*', title)
                if title_match:
                    potential_client = title_match.group(1).lower().replace(' ', '-')
                    if client_filter and potential_client == client_filter:
                        client = potential_client
            
            if client:
                normalized = normalize_title(title)
                client_groups[(client, normalized)].append({
                    'id': task_id,
                    'title': title,
                    'status': status,
                    'updated': updated,
                    'notes': notes[:100] if notes else ''  # First 100 chars
                })
        
        # Find duplicates (groups with more than 1 task)
        duplicates = {}
        stats = {
            'total_tasks': len(items),
            'unique_tasks': 0,
            'duplicate_groups': 0,
            'duplicate_tasks': 0,
            'by_client': defaultdict(lambda: {'unique': 0, 'duplicates': 0, 'groups': 0})
        }
        
        for (client, normalized_title), tasks in client_groups.items():
            if len(tasks) > 1:
                duplicates[(client, normalized_title)] = tasks
                stats['duplicate_groups'] += 1
                stats['duplicate_tasks'] += len(tasks)
                stats['by_client'][client]['duplicates'] += len(tasks)
                stats['by_client'][client]['groups'] += 1
            else:
                stats['unique_tasks'] += 1
                stats['by_client'][client]['unique'] += 1
        
        return {
            'duplicates': duplicates,
            'stats': dict(stats),
            'client_groups': {str(k): v for k, v in client_groups.items()}
        }
    
    except Exception as e:
        print(f"Error finding duplicates: {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}


def print_duplicate_report(result: Dict, client_filter: str = None):
    """Print a formatted report of duplicates."""
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    stats = result['stats']
    duplicates = result['duplicates']
    
    print("\n" + "=" * 80)
    print("DUPLICATE TASK REPORT")
    print("=" * 80)
    print(f"\nTotal tasks analyzed: {stats['total_tasks']}")
    print(f"Unique tasks: {stats['unique_tasks']}")
    print(f"Duplicate groups: {stats['duplicate_groups']}")
    print(f"Total duplicate tasks: {stats['duplicate_tasks']}")
    
    if client_filter:
        print(f"\nFiltered by client: {client_filter}")
    
    # Print by client
    print("\n" + "-" * 80)
    print("BREAKDOWN BY CLIENT:")
    print("-" * 80)
    for client, client_stats in stats['by_client'].items():
        if client_stats['groups'] > 0:
            print(f"\n{client.upper()}:")
            print(f"  Unique tasks: {client_stats['unique']}")
            print(f"  Duplicate groups: {client_stats['groups']}")
            print(f"  Duplicate tasks: {client_stats['duplicates']}")
    
    # Print duplicate groups
    if duplicates:
        print("\n" + "-" * 80)
        print("DUPLICATE GROUPS:")
        print("-" * 80)
        
        for (client, normalized_title), tasks in sorted(duplicates.items()):
            print(f"\n[{client}] {normalized_title}")
            print(f"  Found {len(tasks)} duplicate(s):")
            
            # Sort by updated date (newest first)
            sorted_tasks = sorted(tasks, key=lambda x: x['updated'], reverse=True)
            
            for i, task in enumerate(sorted_tasks, 1):
                status_icon = "✓" if task['status'] == 'completed' else "○"
                print(f"    {i}. {status_icon} {task['title']}")
                print(f"       ID: {task['id']}")
                print(f"       Status: {task['status']}")
                print(f"       Updated: {task['updated']}")
                if task['notes']:
                    print(f"       Notes: {task['notes'][:80]}...")
            
            # Recommend which to keep (oldest open task, or newest if all completed)
            open_tasks = [t for t in sorted_tasks if t['status'] != 'completed']
            if open_tasks:
                keep_task = min(open_tasks, key=lambda x: x['updated'])  # Oldest open
                print(f"\n  → RECOMMEND: Keep task ID {keep_task['id']} (oldest open task)")
                print(f"     Delete others: {', '.join([t['id'] for t in sorted_tasks if t['id'] != keep_task['id']])}")
            else:
                keep_task = sorted_tasks[0]  # Newest completed
                print(f"\n  → RECOMMEND: Keep task ID {keep_task['id']} (newest completed)")
                print(f"     Delete others: {', '.join([t['id'] for t in sorted_tasks if t['id'] != keep_task['id']])}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Find duplicate tasks in Google Tasks')
    parser.add_argument('--client', help='Filter by client name (e.g., smythson)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
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
    
    print(f"Task List ID: {task_list_id}")
    print(f"Task List Name: {config.get('task_list_name', 'Unknown')}")
    
    # Find duplicates
    result = find_duplicates(task_list_id, args.client)
    
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print_duplicate_report(result, args.client)
        
        # Save report to file
        report_file = PROJECT_ROOT / "shared" / "data" / f"duplicate-tasks-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n\nReport saved to: {report_file}")


if __name__ == "__main__":
    main()

