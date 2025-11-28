#!/usr/bin/env python3
"""
Retroactive Task Creator

Creates Google Tasks for items that were processed while the Google Tasks
integration was down or not working properly.

Scans:
1. Todo files without Google Task IDs
2. Processed inbox files that contain "task:" keyword but may not have created tasks
3. AI-enhanced notes (both unprocessed and processed) with task directives
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
PROCESSED_DIR = PROJECT_ROOT / '!inbox' / 'processed'
AI_ENHANCED_DIR = PROJECT_ROOT / '!inbox' / 'ai-enhanced'


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
    
    # If no details section, try to extract from content
    if not details:
        # Look for content after metadata
        in_content = False
        for line in lines:
            if line.strip().startswith('**') and '**' in line:
                in_content = True
                continue
            if in_content and line.strip() and not line.startswith('#'):
                if not line.startswith('**') and not line.startswith('- ['):
                    details.append(line)
    
    details_text = '\n'.join(details).strip()
    
    return title, details_text, due_date, google_task_id


def extract_task_from_processed_file(content):
    """Extract task information from processed inbox file"""
    lines = content.split('\n')
    
    task_title = None
    task_content = []
    due_date = None
    in_task_section = False
    
    # Look for "task:" keyword
    for i, line in enumerate(lines):
        if line.strip().lower().startswith('task:'):
            task_title = re.sub(r'^task:\s*', '', line, flags=re.IGNORECASE).strip()
            # Get content after task: line
            task_content = lines[i+1:]
            break
    
    # Extract due date
    for line in task_content:
        if re.match(r'(due|deadline|by):?\s*', line, re.IGNORECASE):
            match = re.search(r'(due|deadline|by):?\s*(.+)', line, re.IGNORECASE)
            if match:
                due_date = match.group(2).strip()
                break
    
    # Clean up task content (remove empty lines at start, stop at next section)
    cleaned_content = []
    for line in task_content:
        if line.strip().startswith('---') or line.strip().startswith('##'):
            break
        if line.strip():
            cleaned_content.append(line)
    
    return task_title, '\n'.join(cleaned_content).strip(), due_date


def update_todo_with_google_id(todo_path, google_task_id):
    """Add Google Task ID to existing todo file"""
    with open(todo_path, 'r') as f:
        content = f.read()
    
    # Check if already has Google Task ID
    if '**Google Task ID:**' in content:
        return
    
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


def process_todos():
    """Process todos without Google Task IDs"""
    print("=" * 80)
    print("PROCESSING TODOS WITHOUT GOOGLE TASK IDs")
    print("=" * 80)
    print()
    
    if not TODO_DIR.exists():
        print("❌ Todo directory not found")
        return 0, 0, 0
    
    # Initialize Google Tasks client
    try:
        client = GoogleTasksClient()
        print("✅ Connected to Google Tasks")
        print()
    except Exception as e:
        print(f"❌ Could not connect to Google Tasks: {e}")
        return 0, 0, 0
    
    # Get all todo files
    todo_files = list(TODO_DIR.glob('*.md'))
    
    if not todo_files:
        print("📭 No todos to process")
        return 0, 0, 0
    
    print(f"📋 Found {len(todo_files)} todo file(s)")
    print()
    
    created = 0
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
                print(f"  ✅ Created task: {title}")
                if due_date:
                    print(f"     Due: {due_date}")
                created += 1
            else:
                print(f"  ❌ Failed to create Google Task")
                errors += 1
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            errors += 1
        
        print()
    
    return created, skipped, errors


def check_task_exists(client, task_title):
    """Check if a task with similar title already exists"""
    try:
        existing_tasks = client.list_tasks()
        # Check for exact match (case-insensitive)
        task_exists = any(t.get('title', '').lower().strip() == task_title.lower().strip() for t in existing_tasks)
        return task_exists
    except Exception as e:
        print(f"  ⚠️  Error checking existing tasks: {e}")
        return False


def extract_task_from_enhanced_note(content):
    """Extract task information from AI-enhanced note"""
    lines = content.split('\n')
    
    task_title = None
    task_content = []
    due_date = None
    note_type = None
    client_name = None
    
    # Extract type
    for line in lines:
        if line.startswith('**Type:**'):
            note_type = line.split(':', 1)[1].strip()
            break
    
    # Look for "task:" directive
    for i, line in enumerate(lines):
        if line.strip().lower().startswith('task:'):
            task_title = re.sub(r'^task:\s*', '', line, flags=re.IGNORECASE).strip()
            # Get content after task: line
            task_content = lines[i+1:]
            break
    
    # Extract due date
    for line in task_content:
        if re.match(r'^due:\s*', line, re.IGNORECASE):
            due_date = re.sub(r'^due:\s*', '', line, flags=re.IGNORECASE).strip()
            break
    
    # Extract client if present
    for line in lines:
        if line.strip().lower().startswith('client:'):
            client_name = re.sub(r'^client:\s*', '', line, flags=re.IGNORECASE).strip()
            if client_name.lower() in ['n/a', 'none', '']:
                client_name = None
            break
    
    # Clean up task content (remove empty lines at start, stop at next section)
    cleaned_content = []
    for line in task_content:
        if line.strip().startswith('---') or (line.strip().startswith('**') and 'Original Note' in line):
            break
        if line.strip() and not line.strip().lower().startswith(('due:', 'time:', 'urgent:', 'client:')):
            cleaned_content.append(line)
    
    return task_title, '\n'.join(cleaned_content).strip(), due_date, note_type, client_name


def process_inbox_files():
    """Process processed inbox files that contain tasks"""
    print("=" * 80)
    print("PROCESSING PROCESSED INBOX FILES WITH TASKS")
    print("=" * 80)
    print()
    
    if not PROCESSED_DIR.exists():
        print("❌ Processed inbox directory not found")
        return 0, 0, 0
    
    # Initialize Google Tasks client
    try:
        client = GoogleTasksClient()
        print("✅ Connected to Google Tasks")
        print()
    except Exception as e:
        print(f"❌ Could not connect to Google Tasks: {e}")
        return 0, 0, 0
    
    # Find files with "task:" keyword
    task_files = []
    for file in PROCESSED_DIR.glob('*.md'):
        try:
            content = file.read_text(encoding='utf-8')
            if re.search(r'^task:\s*', content, re.IGNORECASE | re.MULTILINE):
                task_files.append(file)
        except Exception as e:
            print(f"  ⚠️  Error reading {file.name}: {e}")
            continue
    
    if not task_files:
        print("📭 No processed inbox files with tasks found")
        return 0, 0, 0
    
    print(f"📋 Found {len(task_files)} processed file(s) with tasks")
    print()
    
    created = 0
    skipped = 0
    errors = 0
    
    for file in task_files:
        print(f"📄 Processing: {file.name}")
        
        try:
            content = file.read_text(encoding='utf-8')
            
            # Extract task information
            task_title, task_content, due_date = extract_task_from_processed_file(content)
            
            if not task_title:
                print(f"  ⚠️  Could not extract task title, skipping")
                skipped += 1
                continue
            
            # Check if task already exists
            if check_task_exists(client, task_title):
                print(f"  ⏭️  Task already exists: {task_title}")
                skipped += 1
                continue
            
            # Create Google Task
            task = client.create_task(
                title=task_title,
                notes=task_content if task_content else None,
                due_date=due_date
            )
            
            if task:
                print(f"  ✅ Created task: {task_title}")
                if due_date:
                    print(f"     Due: {due_date}")
                created += 1
            else:
                print(f"  ❌ Failed to create Google Task")
                errors += 1
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            errors += 1
        
        print()
    
    return created, skipped, errors


def process_ai_enhanced_notes():
    """Process AI-enhanced notes (both unprocessed and processed) that contain tasks"""
    print("=" * 80)
    print("PROCESSING AI-ENHANCED NOTES WITH TASKS")
    print("=" * 80)
    print()
    
    if not AI_ENHANCED_DIR.exists():
        print("❌ AI-enhanced directory not found")
        return 0, 0, 0
    
    # Initialize Google Tasks client
    try:
        client = GoogleTasksClient()
        print("✅ Connected to Google Tasks")
        print()
    except Exception as e:
        print(f"❌ Could not connect to Google Tasks: {e}")
        return 0, 0, 0
    
    # Find all enhanced notes
    enhanced_files = list(AI_ENHANCED_DIR.glob('*.md'))
    
    if not enhanced_files:
        print("📭 No AI-enhanced notes found")
        return 0, 0, 0
    
    print(f"📋 Found {len(enhanced_files)} AI-enhanced note(s)")
    print()
    
    created = 0
    skipped = 0
    errors = 0
    
    for file in enhanced_files:
        print(f"📄 Processing: {file.name}")
        
        try:
            content = file.read_text(encoding='utf-8')
            
            # Extract task information
            task_title, task_content, due_date, note_type, client_name = extract_task_from_enhanced_note(content)
            
            # Only process if it's a task type or has a task directive
            if note_type == 'completion':
                print(f"  ⏭️  Completion note (not a task), skipping")
                skipped += 1
                continue
            
            if not task_title:
                # Check if it's misclassified - look for action words or task-like content
                action_words = ['do', 'check', 'review', 'audit', 'fix', 'investigate', 'need to', 'should', 'must', 'create', 'update', 'change', 'implement']
                is_task_like = any(word in content.lower() for word in action_words)
                
                if (note_type == 'general' and is_task_like) or (note_type and note_type != 'completion' and note_type != 'knowledge'):
                    # Try to extract a task from the content
                    # First try to find the original note section
                    original_match = re.search(r'\*\*Original Note:\*\*\s*\n(.*?)(?=\n---|\Z)', content, re.DOTALL)
                    if not original_match:
                        # Try finding content after the metadata
                        lines = content.split('\n')
                        in_content = False
                        content_lines = []
                        for line in lines:
                            if line.strip().startswith('# Wispr Flow Note') or (line.strip() and not line.startswith('**') and not line.startswith('---')):
                                in_content = True
                            if in_content and line.strip() and not line.startswith('**') and not line.startswith('---'):
                                content_lines.append(line)
                        if content_lines:
                            original_content = '\n'.join(content_lines)
                        else:
                            original_content = None
                    else:
                        original_content = original_match.group(1).strip()
                    
                    if original_content:
                        # Extract meaningful task title
                        # Look for the main action in the first few lines
                        first_lines = [l.strip() for l in original_content.split('\n')[:3] if l.strip() and not l.startswith('#')]
                        if first_lines:
                            # Use the first substantial line as task title
                            potential_title = first_lines[0]
                            # Clean up the title
                            potential_title = re.sub(r'^#\s*', '', potential_title)
                            potential_title = re.sub(r'^Wispr Flow Note', '', potential_title, flags=re.IGNORECASE)
                            potential_title = potential_title.strip()
                            
                            if potential_title and len(potential_title) < 150 and len(potential_title) > 5:
                                task_title = potential_title
                                task_content = original_content
                                print(f"  🔍 Misclassified note detected, creating task: {task_title}")
                            else:
                                print(f"  ⚠️  No clear task directive, skipping")
                                skipped += 1
                                continue
                        else:
                            print(f"  ⚠️  No clear task directive, skipping")
                            skipped += 1
                            continue
                    else:
                        print(f"  ⚠️  No task directive found, skipping")
                        skipped += 1
                        continue
                else:
                    print(f"  ⚠️  No task directive found, skipping")
                    skipped += 1
                    continue
            
            # Check if task already exists
            if check_task_exists(client, task_title):
                print(f"  ⏭️  Task already exists: {task_title}")
                skipped += 1
                continue
            
            # Build notes with client context if available
            notes = task_content if task_content else None
            if client_name and client_name.lower() not in ['n/a', 'none', '']:
                if notes:
                    notes = f"Client: {client_name}\n\n{notes}"
                else:
                    notes = f"Client: {client_name}"
            
            # Create Google Task
            task = client.create_task(
                title=task_title,
                notes=notes,
                due_date=due_date
            )
            
            if task:
                print(f"  ✅ Created task: {task_title}")
                if client_name:
                    print(f"     Client: {client_name}")
                if due_date:
                    print(f"     Due: {due_date}")
                created += 1
            else:
                print(f"  ❌ Failed to create Google Task")
                errors += 1
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            errors += 1
        
        print()
    
    return created, skipped, errors


def main():
    """Main execution"""
    print("=" * 80)
    print("RETROACTIVE TASK CREATOR")
    print("=" * 80)
    print()
    print("This script will create Google Tasks for items that were")
    print("processed while the Google Tasks integration was down.")
    print()
    
    # Process todos
    todo_created, todo_skipped, todo_errors = process_todos()
    
    print()
    
    # Process inbox files
    inbox_created, inbox_skipped, inbox_errors = process_inbox_files()
    
    print()
    
    # Process AI-enhanced notes
    enhanced_created, enhanced_skipped, enhanced_errors = process_ai_enhanced_notes()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("Todos:")
    print(f"  ✅ Created: {todo_created}")
    print(f"  ⏭️  Skipped: {todo_skipped}")
    if todo_errors > 0:
        print(f"  ❌ Errors: {todo_errors}")
    print()
    print("Processed Inbox Files:")
    print(f"  ✅ Created: {inbox_created}")
    print(f"  ⏭️  Skipped: {inbox_skipped}")
    if inbox_errors > 0:
        print(f"  ❌ Errors: {inbox_errors}")
    print()
    print("AI-Enhanced Notes:")
    print(f"  ✅ Created: {enhanced_created}")
    print(f"  ⏭️  Skipped: {enhanced_skipped}")
    if enhanced_errors > 0:
        print(f"  ❌ Errors: {enhanced_errors}")
    print()
    print(f"Total tasks created: {todo_created + inbox_created + enhanced_created}")
    print("=" * 80)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

