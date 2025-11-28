#!/usr/bin/env python3
"""
AI Task Creator Module

Formats and creates AI-generated tasks in Google Tasks with:
- Client prefix in title
- Metadata in notes (source, client, priority, time estimate, reason, AI Task ID)
- Automatic due date assignment based on priority
"""

import uuid
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import sys
from pathlib import Path

# Add MCP server path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
MCP_SERVER_PATH = PROJECT_ROOT / "shared" / "mcp-servers" / "google-tasks-mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from tasks_service import tasks_service
except ImportError:
    print("Error: tasks_service module not found")
    sys.exit(1)


def format_task_metadata(task: Dict, ai_task_id: Optional[str] = None) -> Tuple[str, str]:
    """
    Format task metadata for Google Tasks notes field.
    
    Creates a structured metadata block with:
    - Source (AI Generated with timestamp)
    - Client
    - Priority
    - Time Estimate
    - Reason
    - AI Task ID (UUID)
    
    Args:
        task: Task dict with keys: 'client', 'task', 'priority', 'time_estimate', 'reason'
        ai_task_id: Optional AI Task ID (generates new UUID if not provided)
    
    Returns:
        Tuple of (formatted_notes_string, ai_task_id)
    """
    if ai_task_id is None:
        ai_task_id = str(uuid.uuid4())
    
    metadata_lines = [
        "---",
        f"**Source:** AI Generated ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
        f"**Client:** {task.get('client', 'unknown')}",
        f"**Priority:** {task.get('priority', 'P2')}",
        f"**Time Estimate:** {task.get('time_estimate', 'Unknown')}",
        f"**Reason:** {task.get('reason', '')}",
        f"**AI Task ID:** {ai_task_id}",
        "---",
        "",
    ]
    
    # Add additional details from reason
    reason = task.get('reason', '')
    if reason:
        metadata_lines.append(reason)
    
    return '\n'.join(metadata_lines), ai_task_id


def validate_priority_due_date(priority: str, due_date_str: str) -> tuple[bool, str]:
    """
    Validate that a task's priority matches its due date.

    Priority rules:
    - P0: Due in 0-2 days (urgent/immediate)
    - P1: Due in 3-14 days (this week/next week)
    - P2: Due in 15-30 days (next 2-4 weeks)
    - P3: Due in 30+ days (later)

    Args:
        priority: Task priority (P0, P1, P2, P3)
        due_date_str: Due date string in YYYY-MM-DD or RFC 3339 format

    Returns:
        Tuple of (is_valid, suggested_priority)
    """
    if not due_date_str or not priority:
        return (True, priority)

    # Parse due date
    try:
        if 'T' in due_date_str:
            # RFC 3339 format
            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        else:
            # YYYY-MM-DD format
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
    except (ValueError, AttributeError):
        return (True, priority)  # Can't validate, assume valid

    today = datetime.now()
    days_until = (due_date.replace(tzinfo=None) - today).days

    # Calculate expected priority
    if days_until <= 2:
        expected = 'P0'
    elif days_until <= 14:
        expected = 'P1'
    elif days_until <= 30:
        expected = 'P2'
    else:
        expected = 'P3'

    return (priority == expected, expected)

def assign_due_date(task: Dict, config: Optional[Dict] = None) -> str:
    """
    Assign due date based on priority and reason.

    Priority mapping:
    - P0 → Today
    - P1 → Tomorrow
    - P2 → In 3 days

    Special cases:
    - Explicit dates in reason override priority
    - Urgency keywords ("today", "urgent", "critical") → P0

    Args:
        task: Task dict with 'priority' and 'reason' keys
        config: Configuration dict with due_date_mapping

    Returns:
        Due date string in RFC 3339 format (YYYY-MM-DDTHH:MM:SSZ)
    """
    if config is None:
        config = {
            'due_date_mapping': {
                'P0': 0,
                'P1': 1,
                'P2': 3
            }
        }
    
    priority = task.get('priority', 'P2')
    reason = task.get('reason', '').lower()
    
    # Check for explicit dates in reason (YYYY-MM-DD format)
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', reason)
    if date_match:
        date_str = date_match.group(1)
        # Convert to RFC 3339 format (midnight UTC)
        return f"{date_str}T00:00:00Z"
    
    # Check for urgency keywords
    urgency_keywords = ['today', 'urgent', 'immediate', 'critical', 'asap', 'as soon as possible']
    if any(keyword in reason for keyword in urgency_keywords):
        priority = 'P0'
    
    # Priority-based mapping
    due_date_map = config.get('due_date_mapping', {
        'P0': 0,
        'P1': 1,
        'P2': 3,
        'P3': 7
    })
    
    days_offset = due_date_map.get(priority, 3)
    due_date = datetime.now() + timedelta(days=days_offset)
    
    # Format as RFC 3339 (midnight UTC)
    return due_date.strftime('%Y-%m-%dT00:00:00Z')


def create_ai_generated_task(
    task: Dict,
    task_list_id: str,
    google_tasks_client=None,
    config: Optional[Dict] = None,
    ai_task_id: Optional[str] = None
) -> Dict:
    """
    Create AI-generated task in Google Tasks.
    
    Args:
        task: Task dict from daily generator with keys:
              'client', 'task', 'priority', 'time_estimate', 'reason'
        task_list_id: Google Tasks list ID
        google_tasks_client: Optional tasks_service instance (creates if None)
        config: Optional configuration dict
        ai_task_id: Optional AI Task ID (generates new UUID if not provided)
    
    Returns:
        Created task dict with ID and metadata, including 'ai_task_id'
    """
    if google_tasks_client is None:
        google_tasks_client = tasks_service()
    
    # Generate AI Task ID if not provided
    if ai_task_id is None:
        ai_task_id = str(uuid.uuid4())
    
    # Format title with client prefix
    client_name = task.get('client', 'unknown').replace('-', ' ').title()
    task_description = task.get('task', 'Untitled task')
    title = f"[{client_name}] {task_description}"
    
    # Format notes with metadata
    notes, _ = format_task_metadata(task, ai_task_id)
    
    # Assign due date
    due_date = assign_due_date(task, config)
    
    # Create task via Google Tasks API
    try:
        task_body = {
            'title': title,
            'notes': notes,
            'due': due_date
        }
        
        result = google_tasks_client.tasks().insert(
            tasklist=task_list_id,
            body=task_body
        ).execute()
        
        # Return created task with additional metadata
        return {
            'id': result.get('id'),
            'title': result.get('title'),
            'status': result.get('status', 'needsAction'),
            'due': result.get('due', due_date),
            'notes': result.get('notes', notes),
            'created': result.get('updated', ''),
            'client': task.get('client'),
            'priority': task.get('priority'),
            'ai_task_id': ai_task_id,
        }
    
    except Exception as e:
        raise Exception(f"Failed to create task in Google Tasks: {e}")


if __name__ == "__main__":
    # Test task creation
    print("Testing AI task creation...")
    
    test_task = {
        'client': 'smythson',
        'task': 'Review budget pacing',
        'priority': 'P1',
        'time_estimate': '30 mins',
        'reason': 'Check budget pacing for November campaign'
    }
    
    print("Task metadata:")
    notes, ai_id = format_task_metadata(test_task)
    print(notes)
    print()
    print("AI Task ID:", ai_id)
    print("Due date:", assign_due_date(test_task))

