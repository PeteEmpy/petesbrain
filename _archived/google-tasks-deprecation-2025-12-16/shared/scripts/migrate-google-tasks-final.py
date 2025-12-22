#!/usr/bin/env python3
"""
Final Google Tasks Migration

Migrates selected Google Tasks to internal task system before complete deprecation.
This script should be run ONCE before removing Google Tasks integration.

Usage:
    python3 migrate-google-tasks-final.py [--dry-run] [--export-only]

Options:
    --dry-run       Show what would be migrated without making changes
    --export-only   Only export Google Tasks to JSON, don't migrate
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.google_tasks_client import GoogleTasksClient
from shared.client_tasks_service import ClientTasksService

# Export directory
EXPORT_DIR = PROJECT_ROOT / '_archived' / 'google-tasks-final-export'
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def export_all_google_tasks() -> List[Dict]:
    """Export all active Google Tasks to JSON"""
    print("=" * 60)
    print("  Exporting Google Tasks")
    print("=" * 60)
    print()

    client = GoogleTasksClient()
    all_tasks = client.get_all_active_tasks()

    # Save to JSON file
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    export_file = EXPORT_DIR / f'google-tasks-export-{timestamp}.json'

    with open(export_file, 'w') as f:
        json.dump(all_tasks, f, indent=2, default=str)

    print(f"✅ Exported {len(all_tasks)} tasks to:")
    print(f"   {export_file}")
    print()

    # Print summary by list
    lists = {}
    for task in all_tasks:
        list_name = task.get('list_name', 'Unknown')
        if list_name not in lists:
            lists[list_name] = []
        lists[list_name].append(task)

    print("📊 Tasks by list:")
    for list_name, tasks in lists.items():
        print(f"   {list_name}: {len(tasks)} tasks")
    print()

    return all_tasks


def parse_client_from_title(title: str) -> Optional[str]:
    """Extract client slug from task title like '[Client Name] Task description'"""
    import re

    # Match pattern: [Client Name] or [CLIENT-SLUG]
    match = re.match(r'\[([^\]]+)\]', title)
    if not match:
        return None

    client_name = match.group(1).strip()

    # Map common client names to slugs
    CLIENT_SLUG_MAP = {
        'nma': 'national-design-academy',
        'national design academy': 'national-design-academy',
        'crowd control': 'crowd-control',
        'tree2mydoor': 'tree2mydoor',
        'smythson': 'smythson',
        'devonshire': 'devonshire-hotels',
        'devonshire hotels': 'devonshire-hotels',
        'grain guard': 'grain-guard',
        'superspace': 'superspace',
        'bright minds': 'bright-minds',
        'brightminds': 'bright-minds',
        'tree to my door': 'tree2mydoor',
        'uno': 'uno-lighting',
        'uno lighting': 'uno-lighting',
        'positive bakes': 'positive-bakes',
        'go glean': 'go-glean',
        'clear prospects': 'clear-prospects',
    }

    client_slug = CLIENT_SLUG_MAP.get(client_name.lower())
    if not client_slug:
        # Try exact match
        clients_dir = PROJECT_ROOT / 'clients'
        for client_dir in clients_dir.iterdir():
            if client_dir.is_dir() and not client_dir.name.startswith('_'):
                if client_dir.name.lower() == client_name.lower():
                    return client_dir.name
                # Try reading CONTEXT.md for client name
                context_file = client_dir / 'CONTEXT.md'
                if context_file.exists():
                    with open(context_file, 'r') as f:
                        first_line = f.readline()
                        if client_name.lower() in first_line.lower():
                            return client_dir.name

    return client_slug


def should_migrate_task(task: Dict) -> tuple[bool, str]:
    """
    Determine if a task should be migrated.

    Returns: (should_migrate: bool, reason: str)
    """
    title = task.get('title', '')
    due_date = task.get('due')
    status = task.get('status', 'needsAction')
    list_name = task.get('list_name', '')

    # Skip completed tasks
    if status == 'completed':
        return False, "Already completed"

    # Skip personal list (not client work)
    if list_name == "Peter's List":
        return False, "Personal task, not client work"

    # Skip if no client tag
    if not title.startswith('['):
        return False, "No client tag in title"

    # Skip if can't parse client
    client = parse_client_from_title(title)
    if not client:
        return False, "Could not identify client"

    # Check if overdue
    if due_date:
        try:
            due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            overdue_days = (datetime.now(due.tzinfo) - due).days
            if overdue_days > 14:
                return False, f"Overdue by {overdue_days} days (stale)"
        except:
            pass

    # Migrate if:
    # - Has future due date OR
    # - No due date (ongoing task) OR
    # - Overdue by <7 days (recent)
    return True, "Active or recent task"


def migrate_task(task: Dict, dry_run: bool = False) -> bool:
    """
    Migrate a single task from Google Tasks to internal system.

    Returns: True if migrated successfully, False otherwise
    """
    title = task.get('title', '')
    notes = task.get('notes', '')
    due_date = task.get('due')
    google_task_id = task.get('id')
    list_name = task.get('list_name', '')

    # Parse client
    client = parse_client_from_title(title)
    if not client:
        print(f"  ⚠️  Could not identify client from: {title}")
        return False

    # Determine priority (default P2)
    priority = 'P2'
    if 'urgent' in title.lower() or 'critical' in title.lower():
        priority = 'P1'
    if 'review' in title.lower() or 'check' in title.lower():
        priority = 'P2'
    if 'investigate' in title.lower():
        priority = 'P1'

    # Parse due date
    due_date_str = None
    if due_date:
        try:
            due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            due_date_str = due.strftime('%Y-%m-%d')
        except:
            pass

    # Add migration note to notes
    migration_note = f"[Migrated from Google Tasks on {datetime.now().date()}]"
    if notes:
        full_notes = f"{migration_note}\n\n{notes}"
    else:
        full_notes = migration_note

    if dry_run:
        print(f"  [DRY RUN] Would migrate to {client}:")
        print(f"    Title: {title}")
        print(f"    Priority: {priority}")
        print(f"    Due: {due_date_str or 'None'}")
        return True

    # Create in internal system
    try:
        service = ClientTasksService()
        service.create_task(
            title=title,
            client=client,
            priority=priority,
            due_date=due_date_str,
            notes=full_notes
        )
        print(f"  ✅ Migrated to {client}: {title}")
        return True
    except Exception as e:
        print(f"  ❌ Error migrating task: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Migrate Google Tasks to internal system')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be migrated without making changes')
    parser.add_argument('--export-only', action='store_true', help='Only export Google Tasks to JSON')
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  Final Google Tasks Migration")
    print("=" * 60)
    print()

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()

    # Step 1: Export all Google Tasks
    all_tasks = export_all_google_tasks()

    if args.export_only:
        print("✅ Export complete. Use --dry-run to see migration plan.")
        return

    # Step 2: Analyze and migrate
    print("=" * 60)
    print("  Analysing Tasks for Migration")
    print("=" * 60)
    print()

    to_migrate = []
    to_skip = []

    for task in all_tasks:
        should_migrate, reason = should_migrate_task(task)
        if should_migrate:
            to_migrate.append(task)
        else:
            to_skip.append((task, reason))

    print(f"📊 Analysis Results:")
    print(f"   Tasks to migrate: {len(to_migrate)}")
    print(f"   Tasks to skip: {len(to_skip)}")
    print()

    if to_skip:
        print("⏭️  Skipping tasks:")
        for task, reason in to_skip[:10]:  # Show first 10
            print(f"   - {task.get('title', 'Unknown')}: {reason}")
        if len(to_skip) > 10:
            print(f"   ... and {len(to_skip) - 10} more")
        print()

    if not to_migrate:
        print("✅ No tasks to migrate. All done!")
        return

    # Step 3: Migrate tasks
    print("=" * 60)
    print("  Migrating Tasks to Internal System")
    print("=" * 60)
    print()

    migrated_count = 0
    failed_count = 0

    for i, task in enumerate(to_migrate, 1):
        print(f"[{i}/{len(to_migrate)}] {task.get('title', 'Unknown')}")
        if migrate_task(task, dry_run=args.dry_run):
            migrated_count += 1
        else:
            failed_count += 1

    print()
    print("=" * 60)
    print(f"✅ Migration Complete")
    print("=" * 60)
    print(f"   Migrated: {migrated_count}")
    if failed_count > 0:
        print(f"   Failed: {failed_count}")
    print(f"   Skipped: {len(to_skip)}")
    print()

    if args.dry_run:
        print("🔍 This was a dry run. Run without --dry-run to actually migrate.")
    else:
        print("✅ Tasks migrated to internal system.")
        print("📋 Next steps:")
        print("   1. Verify tasks in clients/*/tasks.json")
        print("   2. Run system health check")
        print("   3. Proceed with Google Tasks deprecation")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
