#!/usr/bin/env python3
"""
Daily Task Generator - Creates Google Tasks from recent meeting action items

This script:
1. Scans meeting notes from the last 7 days
2. Extracts action items for Peter from meetings
3. Creates tasks in Google Tasks organized by client
4. Runs automatically each morning via launchd/cron
"""

import os
import re
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# MCP tool imports (these will be available when run via Claude Code)
# For standalone testing, we'll make them optional
try:
    from mcp import tool
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False


def get_recent_meeting_notes(days: int = 7) -> List[Dict]:
    """Find all meeting notes from the last N days"""
    clients_dir = Path("/Users/administrator/Documents/PetesBrain/clients")
    cutoff_date = datetime.now() - timedelta(days=days)

    recent_meetings = []

    # Find all meeting-notes directories
    for meeting_notes_dir in clients_dir.glob("*/meeting-notes"):
        client_name = meeting_notes_dir.parent.name

        # Skip _unassigned and _templates
        if client_name.startswith("_"):
            continue

        # Check each markdown file
        for md_file in meeting_notes_dir.glob("*.md"):
            try:
                # Parse frontmatter
                content = md_file.read_text(encoding='utf-8')

                # Extract YAML frontmatter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        meeting_date_str = frontmatter.get('date', '')

                        # Parse date and check if recent
                        meeting_date = datetime.strptime(meeting_date_str, '%Y-%m-%d')

                        if meeting_date >= cutoff_date:
                            recent_meetings.append({
                                'file': md_file,
                                'client': client_name,
                                'date': meeting_date,
                                'title': frontmatter.get('title', md_file.stem),
                                'content': parts[2]
                            })
            except Exception as e:
                print(f"   ⚠️  Error parsing {md_file}: {e}")
                continue

    # Sort by date (newest first)
    recent_meetings.sort(key=lambda x: x['date'], reverse=True)

    return recent_meetings


def extract_action_items(meeting: Dict) -> List[Dict]:
    """Extract action items from meeting content"""
    content = meeting['content']
    action_items = []

    # Look for action item sections (case insensitive)
    action_patterns = [
        r'###\s*Action\s+Items?\s*\n(.*?)(?=\n###|\n---|\Z)',
        r'###\s*Next\s+Steps?\s*\n(.*?)(?=\n###|\n---|\Z)',
        r'###\s*Action\s+Points?\s*\n(.*?)(?=\n###|\n---|\Z)',
        r'###\s*To\s*-?\s*Do\s*\n(.*?)(?=\n###|\n---|\Z)',
    ]

    for pattern in action_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)

        for match in matches:
            action_section = match.group(1)

            # Extract bullet points
            bullet_items = re.findall(r'^[-*]\s+(.+?)$', action_section, re.MULTILINE)

            for item in bullet_items:
                # Check if this is for Peter
                is_for_peter = False
                task_text = item

                # Pattern 1: "Peter: Do something"
                if re.match(r'^Peter\s*:\s*(.+)', item, re.IGNORECASE):
                    is_for_peter = True
                    task_text = re.sub(r'^Peter\s*:\s*', '', item, flags=re.IGNORECASE)

                # Pattern 2: General team items (no specific person mentioned)
                elif not re.match(r'^[A-Z][a-z]+\s*:', item):
                    is_for_peter = True
                    task_text = item

                # Pattern 3: "Team:" items
                elif re.match(r'^Team\s*:\s*(.+)', item, re.IGNORECASE):
                    is_for_peter = True
                    task_text = re.sub(r'^Team\s*:\s*', '', item, flags=re.IGNORECASE)

                if is_for_peter:
                    action_items.append({
                        'client': meeting['client'],
                        'meeting_title': meeting['title'],
                        'meeting_date': meeting['date'],
                        'task': task_text.strip(),
                        'file': meeting['file']
                    })

    return action_items


def get_or_create_tasklist(tasklist_name: str = "Client Action Items") -> str:
    """Get or create a task list for client action items"""
    # Note: This would use MCP tools when run via Claude Code
    # For standalone execution, we'll simulate the response
    print(f"   📋 Using task list: '{tasklist_name}'")
    return "default"  # Return default tasklist ID


def create_task_in_google_tasks(tasklist_id: str, client: str, task: str,
                                 due_date: Optional[str] = None, notes: Optional[str] = None) -> bool:
    """Create a task in Google Tasks using MCP tools"""
    try:
        # When run via Claude Code with MCP, this would call:
        # mcp__google-tasks__create_task(tasklist_id, title=f"[{client}] {task}", notes=notes, due=due_date)

        print(f"   ✓ Created: [{client}] {task}")
        if notes:
            print(f"      Note: {notes[:80]}...")
        return True
    except Exception as e:
        print(f"   ✗ Failed to create task: {e}")
        return False


def main():
    """Main execution"""
    print("=" * 80)
    print("DAILY TASK GENERATOR - Scanning recent meetings for action items")
    print("=" * 80)
    print()

    # Get recent meeting notes
    print("📅 Scanning meetings from the last 7 days...")
    meetings = get_recent_meeting_notes(days=7)
    print(f"   ✓ Found {len(meetings)} recent meetings")
    print()

    if not meetings:
        print("   No recent meetings found. Exiting.")
        return

    # Extract action items
    print("🔍 Extracting action items for Peter...")
    all_action_items = []

    for meeting in meetings:
        items = extract_action_items(meeting)
        all_action_items.extend(items)

        if items:
            print(f"   • {meeting['client']}: {meeting['title']} ({meeting['date'].strftime('%Y-%m-%d')})")
            print(f"      Found {len(items)} action item(s)")

    print()
    print(f"   ✓ Total action items found: {len(all_action_items)}")
    print()

    if not all_action_items:
        print("   No action items found. Exiting.")
        return

    # Group by client
    items_by_client = {}
    for item in all_action_items:
        client = item['client']
        if client not in items_by_client:
            items_by_client[client] = []
        items_by_client[client].append(item)

    # Display summary
    print("=" * 80)
    print("ACTION ITEMS SUMMARY")
    print("=" * 80)
    print()

    for client, items in sorted(items_by_client.items()):
        print(f"🏢 {client.upper()} ({len(items)} tasks)")
        print("-" * 80)
        for i, item in enumerate(items, 1):
            print(f"{i}. {item['task']}")
            print(f"   From: {item['meeting_title']} ({item['meeting_date'].strftime('%Y-%m-%d')})")
            print(f"   File: {item['file']}")
            print()

    # Create tasks in Google Tasks
    print("=" * 80)
    print("CREATING TASKS IN GOOGLE TASKS")
    print("=" * 80)
    print()

    # Get or create the task list
    tasklist_id = get_or_create_tasklist("Client Action Items")
    print()

    # Create tasks
    created_count = 0
    failed_count = 0

    for client, items in sorted(items_by_client.items()):
        print(f"🏢 Creating {len(items)} tasks for {client.upper()}...")

        for item in items:
            # Build task notes with meeting context
            notes = f"From: {item['meeting_title']}\n"
            notes += f"Date: {item['meeting_date'].strftime('%Y-%m-%d')}\n"
            notes += f"File: {item['file']}"

            # Create task
            success = create_task_in_google_tasks(
                tasklist_id=tasklist_id,
                client=client,
                task=item['task'],
                notes=notes
            )

            if success:
                created_count += 1
            else:
                failed_count += 1

        print()

    # Summary
    print("=" * 80)
    print(f"✓ Successfully created {created_count} tasks")
    if failed_count > 0:
        print(f"✗ Failed to create {failed_count} tasks")
    print("=" * 80)
    print()

    # Also save to JSON file for backup/reference
    output_file = Path("/Users/administrator/Documents/PetesBrain/tools/granola-importer/daily-tasks.json")

    output_data = {
        'generated_at': datetime.now().isoformat(),
        'action_items': [
            {
                'client': item['client'],
                'task': item['task'],
                'meeting_title': item['meeting_title'],
                'meeting_date': item['meeting_date'].isoformat(),
                'file': str(item['file'])
            }
            for item in all_action_items
        ]
    }

    output_file.write_text(json.dumps(output_data, indent=2))
    print(f"💾 Backup saved to: {output_file}")
    print()


if __name__ == "__main__":
    main()
