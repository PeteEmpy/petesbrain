#!/usr/bin/env python3
"""
Migrate Client Tasks from Google Tasks to Internal System

This script:
1. Fetches all tasks from Google Tasks "Client Work" list
2. Converts them to the internal task format
3. Imports them into client-tasks.json
4. Generates a report of what was migrated

Run once to migrate, then switch to internal system.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'shared'))

from google_tasks_client import GoogleTasksClient
from client_tasks_service import ClientTasksService
import re


def extract_client_from_title(title: str) -> tuple[str | None, str]:
    """
    Extract client name from task title.
    Returns (client_slug, cleaned_title)
    """
    # Check for [Client Name] format
    match = re.match(r'\[([^\]]+)\]\s*(.*)', title)
    if match:
        client_name = match.group(1).strip()
        remaining_title = match.group(2).strip() or title

        # Skip if it's a priority marker (not a client)
        if client_name.upper() in ['LOW', 'MEDIUM', 'HIGH', 'URGENT', 'P0', 'P1', 'P2', 'P3']:
            # Try to extract client from the remaining title
            remaining_match = re.match(r'([A-Za-z0-9\s&-]+?)\s*-', remaining_title)
            if remaining_match:
                client_name = remaining_match.group(1).strip()
                client_slug = client_name.lower().replace(' ', '-').replace('&', '-and-')
                return client_slug, title
            return None, title

        # Normalize to slug
        client_slug = client_name.lower().replace(' ', '-')

        return client_slug, remaining_title

    return None, title


def extract_priority_from_text(title: str, notes: str) -> str:
    """Extract priority from title or notes"""
    combined = f"{title} {notes}".upper()

    # Check for explicit P0/P1/P2/P3
    for priority in ['P0', 'P1', 'P2', 'P3']:
        if priority in combined:
            return priority

    # Check for keywords
    if any(word in combined for word in ['CRITICAL', 'URGENT', 'ASAP']):
        return 'P0'
    elif any(word in combined for word in ['HIGH', 'IMPORTANT', 'THIS WEEK']):
        return 'P1'
    elif any(word in combined for word in ['LOW', 'SOMEDAY']):
        return 'P3'

    return 'P2'  # Default


def extract_time_estimate(notes: str) -> int | None:
    """Extract time estimate from notes (returns minutes)"""
    if not notes:
        return None

    # Look for patterns like "30 mins", "1-2 hours", "1 hour"
    patterns = [
        (r'(\d+)\s*min', 1),          # "30 mins" -> 30
        (r'(\d+)-(\d+)\s*hour', 60),  # "1-2 hours" -> avg * 60
        (r'(\d+)\s*hour', 60),         # "1 hour" -> 60
    ]

    for pattern, multiplier in patterns:
        match = re.search(pattern, notes, re.IGNORECASE)
        if match:
            if len(match.groups()) == 2:
                # Range like "1-2 hours"
                avg = (int(match.group(1)) + int(match.group(2))) / 2
                return int(avg * multiplier)
            else:
                return int(match.group(1)) * multiplier

    return None


def extract_source(notes: str) -> str:
    """Extract source from notes"""
    if not notes:
        return 'Google Tasks Import'

    # Look for common patterns
    if 'AI Generated' in notes:
        return 'AI Generated'
    elif 'Email' in notes:
        return 'Email'
    elif 'Meeting' in notes:
        return 'Meeting'
    elif 'Client' in notes:
        return 'Client Request'
    else:
        return 'Google Tasks Import'


def migrate_tasks(dry_run: bool = True):
    """
    Migrate tasks from Google Tasks to internal system.

    Args:
        dry_run: If True, only show what would be migrated (don't actually import)
    """
    print("=" * 70)
    print("CLIENT TASKS MIGRATION: Google Tasks → Internal System")
    print("=" * 70)

    if dry_run:
        print("\n⚠️  DRY RUN MODE - No tasks will be imported\n")
    else:
        print("\n🚀 LIVE MODE - Tasks will be imported\n")

    # Initialize services
    google_tasks = GoogleTasksClient()
    internal_tasks = ClientTasksService()

    # Get all tasks from "Client Work" list
    print("📥 Fetching tasks from Google Tasks 'Client Work' list...")
    try:
        tasks = google_tasks.list_tasks('Client Work', show_completed=False)
        print(f"   Found {len(tasks)} active tasks\n")
    except Exception as e:
        print(f"❌ Error fetching tasks: {e}")
        return

    # Track stats
    migrated = 0
    skipped = 0
    errors = []

    # Process each task
    for gtask in tasks:
        title = gtask.get('title', '')
        notes = gtask.get('notes', '')
        due_date = gtask.get('due', '')

        # Convert due date format (Google Tasks uses RFC 3339)
        if due_date:
            try:
                # Parse RFC 3339 and convert to YYYY-MM-DD
                dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                due_date = dt.strftime('%Y-%m-%d')
            except ValueError:
                due_date = None

        # Extract metadata
        client, cleaned_title = extract_client_from_title(title)
        priority = extract_priority_from_text(title, notes)
        time_estimate = extract_time_estimate(notes)
        source = extract_source(notes)

        # Build task data
        task_data = {
            'title': title,  # Keep original title with [Client] prefix
            'client': client,
            'priority': priority,
            'due_date': due_date,
            'time_estimate_mins': time_estimate,
            'notes': notes,
            'source': source,
            'tags': ['migrated-from-google-tasks'],
            'context': {
                'google_task_id': gtask.get('id'),
                'google_list': 'Client Work',
                'migrated_at': datetime.now().isoformat()
            }
        }

        # Show what will be migrated
        print(f"📋 {title}")
        print(f"   Client: {client or 'UNASSIGNED'}")
        print(f"   Priority: {priority}")
        if due_date:
            print(f"   Due: {due_date}")
        if time_estimate:
            print(f"   Time: {time_estimate} mins")
        print(f"   Source: {source}")

        # Import task (if not dry run)
        if not dry_run:
            try:
                internal_tasks.create_task(**task_data)
                print(f"   ✅ Migrated")
                migrated += 1
            except Exception as e:
                print(f"   ❌ Error: {e}")
                errors.append((title, str(e)))
        else:
            print(f"   ⏭️  Would migrate")
            migrated += 1

        print()

    # Summary
    print("=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"✅ Migrated: {migrated}")
    print(f"⏭️  Skipped: {skipped}")
    if errors:
        print(f"❌ Errors: {len(errors)}")
        for title, error in errors:
            print(f"   - {title}: {error}")

    if dry_run:
        print("\n⚠️  This was a DRY RUN. No tasks were actually imported.")
        print("   Run with --live to perform the actual migration.")
    else:
        print("\n✅ Migration complete!")
        print(f"   Tasks saved to: {internal_tasks.tasks_file}")

        # Show stats
        stats = internal_tasks.get_stats()
        print(f"\n📊 Current task stats:")
        print(f"   Total active: {stats['active_tasks']}")
        print(f"   By priority: {stats['priority_counts']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Migrate tasks from Google Tasks to internal system')
    parser.add_argument('--live', action='store_true', help='Actually perform migration (default is dry run)')
    args = parser.parse_args()

    migrate_tasks(dry_run=not args.live)
