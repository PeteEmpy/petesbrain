#!/usr/bin/env python3
"""
Google Tasks Monitor
Polls Google Tasks every 6 hours to track task completions.
Stores newly completed tasks for integration with weekly review.
Detects whether tasks are client-specific or Roksys internal.
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional

# Add MCP server path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
MCP_SERVER_PATH = PROJECT_ROOT / "shared" / "mcp-servers" / "google-tasks-mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from tasks_service import tasks_service
except ImportError:
    print("Error: tasks_service module not found")
    print(f"Expected at: {MCP_SERVER_PATH}")
    sys.exit(1)

# Configuration
STATE_FILE = Path("/Users/administrator/Documents/PetesBrain/data/state/tasks-state.json")
COMPLETIONS_FILE = Path("/Users/administrator/Documents/PetesBrain/data/state/tasks-completed.json")
CLIENTS_DIR = Path("/Users/administrator/Documents/PetesBrain/clients")
ROKSYS_DIR = Path("/Users/administrator/Documents/PetesBrain/roksys")
TODO_DIR = Path("/Users/administrator/Documents/PetesBrain/todo")


def find_local_todo_by_task_id(task_id: str) -> Optional[Path]:
    """
    Find local todo file that contains the given Google Task ID.
    
    Args:
        task_id: Google Task ID to search for
        
    Returns:
        Path to local todo file or None if not found
    """
    if not TODO_DIR.exists():
        return None
    
    # Search all markdown files in todo directory
    for todo_file in TODO_DIR.glob('*.md'):
        try:
            with open(todo_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for Google Task ID in various formats
            patterns = [
                rf'\*\*Google Task ID:\*\*\s*{re.escape(task_id)}',
                rf'Google Task ID:\s*{re.escape(task_id)}',
                rf'`{re.escape(task_id)}`',
                rf'{re.escape(task_id)}',
            ]
            
            for pattern in patterns:
                if re.search(pattern, content):
                    return todo_file
        except Exception:
            continue
    
    return None


def update_local_todo_status(todo_file: Path, is_completed: bool, completed_date: Optional[str] = None):
    """
    Update the status section of a local todo file.
    
    Args:
        todo_file: Path to local todo file
        is_completed: Whether task is completed
        completed_date: Optional completion date string
    """
    try:
        with open(todo_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and update status section
        status_pattern = r'(## Status\s*\n\s*)(- \[[ x]\] Todo)'
        
        if is_completed:
            new_status = f"- [x] Completed"
            if completed_date:
                try:
                    # Parse and format date
                    completed_dt = datetime.fromisoformat(completed_date.replace('Z', '+00:00'))
                    date_str = completed_dt.strftime('%Y-%m-%d %H:%M')
                    new_status += f" ({date_str})"
                except:
                    pass
        else:
            new_status = "- [ ] Todo"
        
        # Replace status
        updated_content = re.sub(status_pattern, rf'\1{new_status}', content)
        
        # Also update any standalone status markers
        if is_completed:
            updated_content = re.sub(r'- \[ \] Todo', '- [x] Completed', updated_content)
        else:
            updated_content = re.sub(r'- \[x\] Completed', '- [ ] Todo', updated_content)
        
        # Write back
        with open(todo_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
    except Exception as e:
        print(f"  ⚠️  Error updating local todo file {todo_file.name}: {e}")
        return False


def update_local_todo_from_google_task(todo_file: Path, google_task: Dict):
    """
    Update local todo file with changes from Google Task.
    
    Updates:
    - Title (if changed)
    - Notes/details (if changed)
    - Due date (if changed)
    - Status (completed/incomplete)
    
    Args:
        todo_file: Path to local todo file
        google_task: Google Task dictionary with id, title, notes, due, status, etc.
    """
    try:
        with open(todo_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # Update title if different
        current_title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if current_title_match:
            current_title = current_title_match.group(1).strip()
            new_title = google_task.get('title', '').strip()
            if current_title != new_title and new_title:
                # Replace title
                content = re.sub(r'^#\s+.+$', f'# {new_title}', content, flags=re.MULTILINE)
                updated = True
        
        # Update status
        is_completed = google_task.get('status') == 'completed'
        completed_date = google_task.get('completed_at') or google_task.get('completed')
        
        # Update status in content
        status_pattern = r'(## Status\s*\n\s*)(- \[[ x]\][^\n]*)'
        if is_completed:
            new_status = f"- [x] Completed"
            if completed_date:
                try:
                    completed_dt = datetime.fromisoformat(completed_date.replace('Z', '+00:00'))
                    date_str = completed_dt.strftime('%Y-%m-%d %H:%M')
                    new_status += f" ({date_str})"
                except:
                    pass
        else:
            new_status = "- [ ] Todo"
        
        if re.search(status_pattern, content):
            content = re.sub(status_pattern, rf'\1{new_status}', content)
            updated = True
        
        # Update due date if present
        if google_task.get('due'):
            try:
                # Parse Google Tasks due date (RFC 3339)
                due_str = google_task['due']
                due_dt = datetime.fromisoformat(due_str.replace('Z', '+00:00'))
                formatted_due = due_dt.strftime('%Y-%m-%d')
                
                # Check if due date section exists
                if '**Due Date:**' in content or '**Due:**' in content:
                    # Update existing due date
                    content = re.sub(
                        r'\*\*(?:Due Date|Due):\*\*\s*.+',
                        f'**Due Date:** {formatted_due}',
                        content
                    )
                else:
                    # Add due date after Created line
                    created_match = re.search(r'(\*\*Created:\*\*\s*.+)', content)
                    if created_match:
                        content = content.replace(
                            created_match.group(1),
                            f"{created_match.group(1)}\n**Due Date:** {formatted_due}"
                        )
                updated = True
            except Exception:
                pass
        
        # Update notes/details if changed
        google_notes = google_task.get('notes', '').strip()
        if google_notes:
            # Find Details section
            details_match = re.search(r'(## Details\s*\n\s*)(.*?)(?=\n## |$)', content, re.DOTALL)
            if details_match:
                current_details = details_match.group(2).strip()
                if current_details != google_notes:
                    # Replace details section
                    content = re.sub(
                        r'(## Details\s*\n\s*)(.*?)(?=\n## |$)',
                        rf'\1{google_notes}\n',
                        content,
                        flags=re.DOTALL
                    )
                    updated = True
        
        # Write back if updated
        if updated:
            with open(todo_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"  ⚠️  Error updating local todo from Google Task: {e}")
        return False


def ensure_data_dir():
    """Ensure the data directory exists."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_client_names() -> List[str]:
    """
    Load list of client names from clients directory.

    Returns:
        List of client folder names (lowercase for matching)
    """
    if not CLIENTS_DIR.exists():
        return []

    clients = []
    for client_dir in CLIENTS_DIR.iterdir():
        if client_dir.is_dir() and not client_dir.name.startswith('_'):
            clients.append(client_dir.name.lower())

    return clients


def detect_client(task_title: str, task_notes: Optional[str], tasklist_name: str, clients: List[str]) -> Optional[str]:
    """
    Detect if a task is for a specific client or Roksys internal.

    Checks in order:
    1. Task list name for client mentions
    2. Task title for client mentions
    3. Task notes for client mentions

    Args:
        task_title: The task title
        task_notes: The task notes/description
        tasklist_name: The name of the task list
        clients: List of client names to check against

    Returns:
        Client name (as it appears in folder) or None if Roksys internal
    """
    # Combine all text to search
    search_text = f"{tasklist_name} {task_title}"
    if task_notes:
        search_text += f" {task_notes}"

    search_text_lower = search_text.lower()

    # Check for each client name
    # First try exact matches in task list name (higher confidence)
    for client in clients:
        client_display = client.replace('-', ' ')
        # Check task list name first (most reliable)
        if client in tasklist_name.lower() or client_display in tasklist_name.lower():
            return client

    # Then check title and notes
    for client in clients:
        client_display = client.replace('-', ' ')
        # Check for client name mentions
        if client in search_text_lower or client_display in search_text_lower:
            return client

        # Check for common variations
        # e.g., "tree2mydoor" might be written as "tree 2 my door" or "t2md"
        if client == "tree2mydoor":
            if re.search(r'\bt2md\b', search_text_lower) or 'tree 2 my door' in search_text_lower:
                return client
        elif client == "otc":
            if re.search(r'\botc\b', search_text_lower):
                return client

    # If no client detected, it's Roksys internal
    return None


def add_task_to_context_md(task: Dict, client_name: Optional[str], section: str = "Planned Work"):
    """
    Add task to client's CONTEXT.md file under specified section.

    Args:
        task: Task record with title, notes, status, etc.
        client_name: Client folder name or None for Roksys internal
        section: Section to add to ("Planned Work" or "Completed Work")
    """
    # Determine target folder
    if client_name:
        target_dir = CLIENTS_DIR / client_name
        context_file = target_dir / "CONTEXT.md"
    else:
        target_dir = ROKSYS_DIR
        context_file = target_dir / "CONTEXT.md"

    # Ensure directory and file exist
    if not target_dir.exists():
        print(f"Warning: Directory {target_dir} does not exist, skipping CONTEXT.md update")
        return

    if not context_file.exists():
        print(f"Warning: CONTEXT.md does not exist at {context_file}, skipping update")
        return

    # Read current CONTEXT.md
    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading CONTEXT.md: {e}")
        return

    # Format task entry
    title = task.get('title', 'Untitled')
    notes = task.get('notes', '')
    task_id = task.get('task_id', task.get('id', ''))

    # Create entry with task ID marker for tracking
    entry = f"\n### {title}\n"
    entry += f"<!-- task_id: {task_id} -->\n"

    if section == "Completed Work":
        completed_at = task.get('completed_at', '')
        detected_at = task.get('detected_at', '')
        try:
            if completed_at:
                completed_dt = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
                date_str = completed_dt.strftime('%Y-%m-%d')
            else:
                detected_dt = datetime.fromisoformat(detected_at.replace('Z', '+00:00'))
                date_str = detected_dt.strftime('%Y-%m-%d')
        except:
            date_str = "Recent"
        entry += f"**Status:** ✅ Completed ({date_str})  \n"
    else:
        entry += f"**Status:** 📋 In Progress  \n"

    if notes:
        entry += f"\n{notes}\n"

    entry += "\n"

    # Find or create section
    section_header = f"## {section}"

    if section_header in content:
        # Find where to insert (after section header, before next ## or end)
        section_start = content.find(section_header)
        next_section = content.find("\n## ", section_start + len(section_header))

        if next_section == -1:
            # No next section, append at end
            content = content + entry
        else:
            # Insert before next section
            content = content[:next_section] + entry + content[next_section:]
    else:
        # Create new section at end
        if not content.endswith('\n'):
            content += '\n'
        content += f"\n{section_header}\n"
        content += entry

    # Write back
    try:
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  → Added to CONTEXT.md ({section})")
    except Exception as e:
        print(f"Error writing CONTEXT.md: {e}")


def update_task_in_context_md(task_id: str, client_name: Optional[str], from_section: str, to_section: str, task: Dict):
    """
    Move a task from one section to another in CONTEXT.md (e.g., Planned Work → Completed Work).

    Args:
        task_id: The task ID to find
        client_name: Client folder name or None for Roksys
        from_section: Section to move from
        to_section: Section to move to
        task: Updated task data
    """
    # Determine target folder
    if client_name:
        target_dir = CLIENTS_DIR / client_name
        context_file = target_dir / "CONTEXT.md"
    else:
        target_dir = ROKSYS_DIR
        context_file = target_dir / "CONTEXT.md"

    if not context_file.exists():
        return

    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading CONTEXT.md: {e}")
        return

    # Find and remove old entry
    task_marker = f"<!-- task_id: {task_id} -->"
    if task_marker not in content:
        # Task not in CONTEXT.md, add it fresh
        add_task_to_context_md(task, client_name, to_section)
        return

    # Find the task entry (from ### to next ### or ##)
    marker_pos = content.find(task_marker)
    if marker_pos == -1:
        return

    # Find start of entry (### heading before marker)
    entry_start = content.rfind("\n### ", 0, marker_pos)
    if entry_start == -1:
        entry_start = 0
    else:
        entry_start += 1  # Keep the newline

    # Find end of entry (next ### or ##)
    entry_end = content.find("\n### ", marker_pos)
    next_section = content.find("\n## ", marker_pos)

    if entry_end == -1:
        entry_end = next_section if next_section != -1 else len(content)
    elif next_section != -1 and next_section < entry_end:
        entry_end = next_section

    # Remove old entry
    content = content[:entry_start] + content[entry_end:]

    # Write back
    try:
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing CONTEXT.md: {e}")
        return

    # Add to new section
    add_task_to_context_md(task, client_name, to_section)
    print(f"  → Moved in CONTEXT.md: {from_section} → {to_section}")


def save_task_to_client_folder(task: Dict, client_name: Optional[str]):
    """
    Save completed task to client's tasks-completed.md file or Roksys folder.

    Args:
        task: Task completion record with title, notes, completed_at, etc.
        client_name: Client folder name or None for Roksys internal
    """
    # Determine target folder and file
    if client_name:
        target_dir = CLIENTS_DIR / client_name
        tasks_file = target_dir / "tasks-completed.md"
        category = f"Client: {client_name.replace('-', ' ').title()}"
    else:
        target_dir = ROKSYS_DIR
        tasks_file = target_dir / "tasks-completed.md"
        category = "Roksys Internal"

    # Ensure directory exists
    if not target_dir.exists():
        print(f"Warning: Directory {target_dir} does not exist, skipping task save")
        return

    # Format task entry
    title = task.get('title', 'Untitled')
    notes = task.get('notes', '')
    completed_at = task.get('completed_at', '')
    detected_at = task.get('detected_at', '')
    tasklist_name = task.get('tasklist_name', 'Unknown List')

    # Parse completion date
    try:
        if completed_at:
            completed_dt = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
            date_str = completed_dt.strftime('%Y-%m-%d %H:%M')
        else:
            detected_dt = datetime.fromisoformat(detected_at.replace('Z', '+00:00'))
            date_str = detected_dt.strftime('%Y-%m-%d %H:%M')
    except:
        date_str = completed_at or detected_at

    # Create entry
    entry = f"\n## {title}\n"
    entry += f"**Completed:** {date_str}  \n"
    entry += f"**Source:** {tasklist_name}  \n"

    if notes:
        entry += f"\n{notes}\n"

    entry += "\n---\n"

    # Check if file exists, create with header if not
    if not tasks_file.exists():
        header = f"# Completed Tasks\n\n"
        header += f"This file tracks completed tasks for {category}.\n"
        header += f"Tasks are logged automatically by the Google Tasks monitoring system.\n"
        header += "\n---\n"

        with open(tasks_file, 'w', encoding='utf-8') as f:
            f.write(header)

        print(f"  Created {tasks_file}")

    # Append task
    with open(tasks_file, 'a', encoding='utf-8') as f:
        f.write(entry)

    print(f"  → Saved to {tasks_file.relative_to(target_dir.parent)}")


def load_state() -> Dict[str, Dict[str, str]]:
    """
    Load previous task states from file.

    Returns:
        Dict mapping task_id to {"status": str, "title": str, "tasklist_id": str, "tasklist_name": str}
    """
    if not STATE_FILE.exists():
        return {}

    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load state file: {e}")
        return {}


def save_state(state: Dict[str, Dict[str, str]]):
    """Save current task states to file."""
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error: Failed to save state file: {e}")


def load_completions() -> List[Dict]:
    """
    Load the log of completed tasks.

    Returns:
        List of completion records with timestamp, title, notes, etc.
    """
    if not COMPLETIONS_FILE.exists():
        return []

    try:
        with open(COMPLETIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load completions file: {e}")
        return []


def save_completions(completions: List[Dict]):
    """Save the log of completed tasks."""
    try:
        with open(COMPLETIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(completions, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error: Failed to save completions file: {e}")


def get_all_task_lists(service) -> List[Dict]:
    """Get all task lists from Google Tasks."""
    try:
        results = service.tasklists().list(maxResults=100).execute()
        items = results.get('items', [])
        return [{"id": item["id"], "title": item["title"]} for item in items]
    except Exception as e:
        print(f"Error listing task lists: {e}")
        return []


def get_tasks_from_list(service, tasklist_id: str, tasklist_name: str) -> List[Dict]:
    """Get all tasks (including completed) from a task list."""
    try:
        results = service.tasks().list(
            tasklist=tasklist_id,
            maxResults=100,
            showCompleted=True
        ).execute()

        items = results.get('items', [])
        tasks = []

        for item in items:
            task = {
                "id": item["id"],
                "title": item["title"],
                "status": item.get("status", "needsAction"),
                "tasklist_id": tasklist_id,
                "tasklist_name": tasklist_name,
            }

            if "notes" in item:
                task["notes"] = item["notes"]
            if "due" in item:
                task["due"] = item["due"]
            if "completed" in item:
                task["completed_at"] = item["completed"]

            tasks.append(task)

        return tasks

    except Exception as e:
        print(f"Error listing tasks from '{tasklist_name}': {e}")
        return []


def monitor_tasks():
    """Main monitoring function - check for newly completed tasks."""
    print("Google Tasks Monitor")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    # Ensure data directory exists
    ensure_data_dir()

    # Load client names
    clients = load_client_names()
    print(f"Loaded {len(clients)} client(s) for detection")

    # Load previous state
    previous_state = load_state()
    print(f"Loaded state: {len(previous_state)} tasks tracked")

    # Load completions log
    completions_log = load_completions()
    print(f"Completions log: {len(completions_log)} tasks completed (all time)")

    # Connect to Google Tasks
    try:
        service = tasks_service()
        print("✓ Connected to Google Tasks API")
    except Exception as e:
        print(f"✗ Failed to connect to Google Tasks API: {e}")
        return 1

    # Get all task lists
    task_lists = get_all_task_lists(service)
    if not task_lists:
        print("No task lists found")
        return 0

    print(f"Found {len(task_lists)} task list(s):")
    for tl in task_lists:
        print(f"  - {tl['title']}")

    # Current state, new tasks, and newly completed tasks
    current_state = {}
    newly_created = []
    newly_completed = []

    # Poll all tasks from all lists
    print("\nChecking tasks...")
    for task_list in task_lists:
        tasks = get_tasks_from_list(service, task_list["id"], task_list["title"])

        for task in tasks:
            task_id = task["id"]
            current_status = task["status"]

            # Store current state
            current_state[task_id] = {
                "status": current_status,
                "title": task["title"],
                "tasklist_id": task["tasklist_id"],
                "tasklist_name": task["tasklist_name"],
                "notes": task.get("notes", ""),
                "due": task.get("due", ""),
            }

            previous_task = previous_state.get(task_id)

            # Check if task is NEW (not in previous state)
            if not previous_task and current_status != "completed":
                # New task that's not yet completed
                notes = task.get("notes", "")

                # Only log if notes are substantial (>50 chars)
                if len(notes) > 50:
                    # Detect client
                    detected_client = detect_client(
                        task["title"],
                        notes,
                        task["tasklist_name"],
                        clients
                    )

                    new_task_record = {
                        "task_id": task_id,
                        "id": task_id,
                        "title": task["title"],
                        "tasklist_name": task["tasklist_name"],
                        "notes": notes,
                        "status": current_status,
                        "client": detected_client,
                    }

                    newly_created.append(new_task_record)

                    # Check if task already exists in CONTEXT.md before adding (prevent duplicates)
                    if detected_client:
                        context_file = CLIENTS_DIR / detected_client / "CONTEXT.md"
                    else:
                        context_file = ROKSYS_DIR / "CONTEXT.md"

                    task_already_in_context = False
                    if context_file.exists():
                        try:
                            with open(context_file, 'r', encoding='utf-8') as f:
                                content = f.read()

                            # Check if a task with this TITLE already exists (prevent duplicate content)
                            # This catches multiple Google Tasks with same title but different IDs
                            title_escaped = re.escape(task["title"])
                            if re.search(rf'### {title_escaped}\n', content):
                                task_already_in_context = True
                        except:
                            pass

                    if not task_already_in_context:
                        client_display = detected_client if detected_client else "Roksys"
                        print(f"  📋 New task: '{task['title']}' ({client_display}) - adding to CONTEXT.md")

                        # Add to CONTEXT.md
                        add_task_to_context_md(new_task_record, detected_client, "Planned Work")
                    else:
                        print(f"  ↷ Task '{task['title']}' already in CONTEXT.md, skipping duplicate")

            # Check if task was just completed
            elif current_status == "completed":
                # If we have no previous record, or previous status was not completed
                if not previous_task or previous_task.get("status") != "completed":
                    # Check if already in completions log (to avoid duplicates)
                    already_logged = any(
                        c["task_id"] == task_id and c.get("completed_at") == task.get("completed_at")
                        for c in completions_log
                    )

                    if not already_logged:
                        # Detect client
                        detected_client = detect_client(
                            task["title"],
                            task.get("notes"),
                            task["tasklist_name"],
                            clients
                        )

                        completion_record = {
                            "task_id": task_id,
                            "title": task["title"],
                            "tasklist_name": task["tasklist_name"],
                            "detected_at": datetime.now().isoformat(),
                            "completed_at": task.get("completed_at"),
                            "notes": task.get("notes"),
                            "due": task.get("due"),
                            "client": detected_client,  # None = Roksys internal
                        }

                        newly_completed.append(completion_record)
                        completions_log.append(completion_record)

                        client_display = detected_client if detected_client else "Roksys"
                        print(f"  ✓ Newly completed: '{task['title']}' ({client_display}) in '{task['tasklist_name']}'")

                        # Update local todo file if it exists
                        local_todo = find_local_todo_by_task_id(task_id)
                        if local_todo:
                            update_local_todo_from_google_task(local_todo, task)
                            print(f"    → Updated local todo: {local_todo.name}")

                        # Save to client folder (tasks-completed.md)
                        save_task_to_client_folder(completion_record, detected_client)

                        # Phase 2: Update AI tasks state file if this is an AI-generated task
                        try:
                            sys.path.insert(0, str(PROJECT_ROOT / "shared" / "scripts"))
                            from ai_tasks_state import (
                                get_ai_task_id,
                                update_task_status,
                                get_task_by_google_id
                            )
                            
                            # Check if this is an AI-generated task
                            ai_task_id = get_ai_task_id(task)
                            if ai_task_id:
                                # Update state file
                                update_task_status(
                                    task_id,
                                    "completed",
                                    None  # Priority unchanged
                                )
                                print(f"    → Updated AI tasks state file for task {ai_task_id[:8]}...")
                        except ImportError:
                            # ai_tasks_state module not available, skip
                            pass
                        except Exception as e:
                            print(f"    ⚠️  Error updating AI tasks state: {e}")

                        # Update or add to CONTEXT.md
                        # If task has substantial notes, update CONTEXT.md
                        notes = completion_record.get('notes', '')
                        if len(notes) > 50:
                            # Try to move from Planned Work to Completed Work
                            # If not in Planned Work, will add fresh to Completed Work
                            update_task_in_context_md(
                                task_id,
                                detected_client,
                                "Planned Work",
                                "Completed Work",
                                completion_record
                            )
            
            # Check if task was modified (title, notes, due date changed) but not completed
            elif previous_task and current_status != "completed":
                # Check if task was modified
                title_changed = previous_task.get("title") != task.get("title")
                notes_changed = previous_task.get("notes", "") != task.get("notes", "")
                due_changed = previous_task.get("due", "") != task.get("due", "")
                
                if title_changed or notes_changed or due_changed:
                    # Update local todo file if it exists
                    local_todo = find_local_todo_by_task_id(task_id)
                    if local_todo:
                        update_local_todo_from_google_task(local_todo, task)
                        changes = []
                        if title_changed:
                            changes.append("title")
                        if notes_changed:
                            changes.append("notes")
                        if due_changed:
                            changes.append("due date")
                        print(f"  🔄 Updated local todo from Google Task changes ({', '.join(changes)}): '{task['title']}'")
            
            # Check if task was uncompleted (moved from completed back to active)
            elif previous_task and previous_task.get("status") == "completed" and current_status != "completed":
                # Task was uncompleted - update local file
                local_todo = find_local_todo_by_task_id(task_id)
                if local_todo:
                    update_local_todo_from_google_task(local_todo, task)
                    print(f"  ↻ Task uncompleted: '{task['title']}' - updated local todo")

    # Save updated state
    save_state(current_state)
    print(f"\n✓ Updated state: {len(current_state)} tasks")

    # Report on new tasks
    if newly_created:
        print(f"✓ Added {len(newly_created)} new task(s) to CONTEXT.md")

    # Save completions log
    if newly_completed:
        save_completions(completions_log)
        print(f"✓ Logged {len(newly_completed)} newly completed task(s)")
        print(f"✓ Total completions: {len(completions_log)} tasks")

    if not newly_created and not newly_completed:
        print("No new or completed tasks")

    print("-" * 50)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return 0


if __name__ == "__main__":
    sys.exit(monitor_tasks())
