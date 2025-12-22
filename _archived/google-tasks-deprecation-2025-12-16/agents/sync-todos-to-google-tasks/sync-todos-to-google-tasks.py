#!/usr/bin/env python3
"""
Sync Local Todos to Google Tasks

This script syncs changes from local todo files back to Google Tasks.
Runs periodically to keep Google Tasks in sync with local file changes.

What it syncs:
- Status changes (completed/incomplete)
- Title changes
- Notes/details changes
- Due date changes
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from shared.google_tasks_client import GoogleTasksClient
    GOOGLE_TASKS_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Google Tasks integration not available: {e}")
    GOOGLE_TASKS_AVAILABLE = False
    sys.exit(1)

TODO_DIR = PROJECT_ROOT / 'todo'
SYNC_STATE_FILE = PROJECT_ROOT / 'shared' / 'data' / 'todo-sync-state.json'

import json


def load_sync_state() -> Dict[str, Dict]:
    """Load last sync state for todos."""
    if not SYNC_STATE_FILE.exists():
        return {}
    
    try:
        with open(SYNC_STATE_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def save_sync_state(state: Dict[str, Dict]):
    """Save sync state."""
    SYNC_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SYNC_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def extract_task_id_from_file(file_path: Path) -> Optional[str]:
    """Extract Google Task ID from local todo file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for Google Task ID in various formats
        patterns = [
            r'\*\*Google Task ID:\*\*\s*([^\s\n]+)',
            r'Google Task ID:\s*([^\s\n]+)',
            r'`([a-zA-Z0-9_-]+)`',  # Task ID in backticks
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                task_id = match.group(1).strip()
                # Validate it looks like a task ID (alphanumeric with possible dashes/underscores)
                if re.match(r'^[a-zA-Z0-9_-]+$', task_id) and len(task_id) > 10:
                    return task_id
        
        return None
    except Exception:
        return None


def extract_task_info_from_file(file_path: Path) -> Dict:
    """Extract task information from local todo file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        info = {
            'title': None,
            'status': 'needsAction',  # Default to incomplete
            'notes': None,
            'due_date': None,
            'modified_time': file_path.stat().st_mtime,
        }
        
        # Extract title (first # heading)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            info['title'] = title_match.group(1).strip()
        
        # Extract status
        if re.search(r'- \[x\]', content, re.IGNORECASE):
            info['status'] = 'completed'
        else:
            info['status'] = 'needsAction'
        
        # Extract notes/details
        details_match = re.search(r'## Details\s*\n\s*(.*?)(?=\n## |$)', content, re.DOTALL)
        if details_match:
            info['notes'] = details_match.group(1).strip()
        
        # Extract due date
        due_match = re.search(r'\*\*(?:Due Date|Due):\*\*\s*(.+)', content)
        if due_match:
            due_str = due_match.group(1).strip()
            info['due_date'] = due_str
        
        return info
    except Exception as e:
        print(f"  ⚠️  Error reading {file_path.name}: {e}")
        return {}


def sync_local_todo_to_google_task(todo_file: Path, task_id: str, client: GoogleTasksClient, previous_state: Dict) -> bool:
    """
    Sync a local todo file to its corresponding Google Task.
    
    Returns True if sync was performed, False otherwise.
    """
    current_info = extract_task_info_from_file(todo_file)
    if not current_info:
        return False
    
    # Get previous state for this file
    file_key = str(todo_file)
    previous_info = previous_state.get(file_key, {})
    
    # Check if file was modified since last sync
    if previous_info.get('modified_time') == current_info['modified_time']:
        # File hasn't changed, skip
        return False
    
    # Determine what needs updating
    updates = {}
    
    # Check title
    if current_info.get('title') and current_info['title'] != previous_info.get('title'):
        updates['title'] = current_info['title']
    
    # Check status
    if current_info.get('status') != previous_info.get('status'):
        updates['status'] = current_info['status']
    
    # Check notes
    if current_info.get('notes') is not None and current_info['notes'] != previous_info.get('notes'):
        updates['notes'] = current_info['notes']
    
    # Check due date
    if current_info.get('due_date') is not None and current_info['due_date'] != previous_info.get('due_date'):
        updates['due_date'] = current_info['due_date']
    
    if not updates:
        return False
    
    # Update Google Task
    try:
        # Handle completion separately (it's a special operation)
        if 'status' in updates:
            if updates['status'] == 'completed':
                client.complete_task(task_id)
            else:
                # Uncompleting task
                client.uncomplete_task(task_id)
        
        # Update other fields (title, notes, due_date)
        title = updates.get('title')
        notes = updates.get('notes')
        due_date = updates.get('due_date')
        
        if title or notes or due_date:
            client.update_task(
                task_id=task_id,
                title=title,
                notes=notes,
                due_date=due_date
            )
        
        # Update sync state
        previous_state[file_key] = current_info
        save_sync_state(previous_state)
        
        change_list = ', '.join(updates.keys())
        print(f"  ✅ Synced {change_list} to Google Task: {current_info.get('title', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error syncing {todo_file.name} to Google Tasks: {e}")
        return False


def sync_all_todos():
    """Sync all local todos to Google Tasks."""
    print("=" * 60)
    print("  Sync Local Todos to Google Tasks")
    print("=" * 60)
    print()
    
    if not TODO_DIR.exists():
        print("❌ Todo directory not found")
        return
    
    if not GOOGLE_TASKS_AVAILABLE:
        print("❌ Google Tasks not available")
        return
    
    # Initialize client
    try:
        client = GoogleTasksClient()
        print("✅ Connected to Google Tasks")
    except Exception as e:
        print(f"❌ Could not connect to Google Tasks: {e}")
        return
    
    # Load previous sync state
    sync_state = load_sync_state()
    print(f"📊 Loaded sync state for {len(sync_state)} file(s)")
    
    # Get all todo files
    todo_files = list(TODO_DIR.glob('*.md'))
    
    if not todo_files:
        print("📭 No todos to sync")
        return
    
    print(f"📋 Found {len(todo_files)} todo file(s)\n")
    
    synced_count = 0
    skipped_count = 0
    error_count = 0
    
    for todo_file in todo_files:
        print(f"📄 Checking: {todo_file.name}")
        
        # Extract Google Task ID
        task_id = extract_task_id_from_file(todo_file)
        
        if not task_id:
            print(f"  ⏭️  No Google Task ID found, skipping")
            skipped_count += 1
            continue
        
        # Sync to Google Tasks
        if sync_local_todo_to_google_task(todo_file, task_id, client, sync_state):
            synced_count += 1
        else:
            skipped_count += 1
        
        print()
    
    print("=" * 60)
    print(f"✅ Synced: {synced_count}")
    print(f"⏭️  Skipped: {skipped_count}")
    if error_count > 0:
        print(f"❌ Errors: {error_count}")
    print("=" * 60)


if __name__ == '__main__':
    try:
        sync_all_todos()
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

