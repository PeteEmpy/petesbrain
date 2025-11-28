#!/usr/bin/env python3
"""
Migrate Existing Todos to Google Tasks

One-time script to migrate existing local todos to Google Tasks.
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.google_tasks_client import GoogleTasksClient

TODO_DIR = PROJECT_ROOT / 'todo'


def extract_todo_metadata(content):
    """Extract title, details, and due date from todo markdown"""
    lines = content.split('\n')
    
    title = None
    details = []
    due_date = None
    google_task_id = None
    in_details = False
    
    for line in lines:
        # Extract title (first # heading)
        if line.startswith('# ') and not title:
            title = line[2:].strip()
            continue
        
        # Check if already has Google Task ID
        if line.startswith('**Google Task ID:**'):
            google_task_id = line.split(':', 1)[1].strip()
            continue
        
        # Check for due date in content
        if re.match(r'(due|deadline|by):?\s*', line, re.IGNORECASE):
            match = re.search(r'(due|deadline|by):?\s*(.+)', line, re.IGNORECASE)
            if match and not due_date:
                due_date = match.group(2).strip()
        
        # Collect details section
        if line.strip() == '## Details':
            in_details = True
            continue
        
        if line.strip().startswith('## ') and line.strip() != '## Details':
            in_details = False
        
        if in_details and line.strip():
            details.append(line)
    
    details_text = '\n'.join(details).strip()
    
    return title, details_text, due_date, google_task_id


def update_todo_with_google_id(todo_path, google_task_id):
    """Add Google Task ID to existing todo file"""
    with open(todo_path, 'r') as f:
        content = f.read()
    
    # Find the location after **Source:** line
    lines = content.split('\n')
    new_lines = []
    added = False
    
    for line in lines:
        new_lines.append(line)
        if line.startswith('**Source:**') and not added:
            new_lines.append(f"**Google Task ID:** {google_task_id}")
            added = True
    
    new_content = '\n'.join(new_lines)
    
    with open(todo_path, 'w') as f:
        f.write(new_content)


def migrate_todos():
    """Migrate all existing todos to Google Tasks"""
    print("=" * 60)
    print("  Migrate Todos to Google Tasks")
    print("=" * 60)
    print()
    
    if not TODO_DIR.exists():
        print("❌ Todo directory not found")
        return
    
    # Initialize Google Tasks client
    try:
        client = GoogleTasksClient()
        print("✅ Connected to Google Tasks")
        print()
    except Exception as e:
        print(f"❌ Could not connect to Google Tasks: {e}")
        return
    
    # Get all todo files
    todo_files = list(TODO_DIR.glob('*.md'))
    
    if not todo_files:
        print("📭 No todos to migrate")
        return
    
    print(f"📋 Found {len(todo_files)} todo file(s)")
    print()
    
    migrated = 0
    skipped = 0
    errors = 0
    
    for todo_file in todo_files:
        print(f"📄 Processing: {todo_file.name}")
        
        try:
            with open(todo_file, 'r') as f:
                content = f.read()
            
            # Extract metadata
            title, details, due_date, existing_google_id = extract_todo_metadata(content)
            
            if not title:
                print(f"  ⚠️  Could not extract title, skipping")
                skipped += 1
                continue
            
            # Skip if already has Google Task ID
            if existing_google_id:
                print(f"  ⏭️  Already has Google Task ID, skipping")
                skipped += 1
                continue
            
            # Create Google Task
            task = client.create_task(
                title=title,
                notes=details if details else None,
                due_date=due_date
            )
            
            if task:
                # Update local todo with Google Task ID
                update_todo_with_google_id(todo_file, task['id'])
                print(f"  ✅ Migrated: {title}")
                if due_date:
                    print(f"     Due: {due_date}")
                migrated += 1
            else:
                print(f"  ❌ Failed to create Google Task")
                errors += 1
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            errors += 1
        
        print()
    
    print("=" * 60)
    print(f"✅ Migrated: {migrated}")
    print(f"⏭️  Skipped: {skipped}")
    if errors > 0:
        print(f"❌ Errors: {errors}")
    print("=" * 60)


if __name__ == '__main__':
    try:
        migrate_todos()
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

