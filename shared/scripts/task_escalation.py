#!/usr/bin/env python3
"""
Task Priority Escalation Module

Phase 3: Automatically escalates stale tasks:
- P2 task open for 5+ days → Escalate to P1
- P1 task open for 3+ days → Escalate to P0

Also updates Google Tasks priority via API.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent
MCP_SERVER_PATH = PROJECT_ROOT / "infrastructure" / "mcp-servers" / "google-tasks-mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))
sys.path.insert(0, str(PROJECT_ROOT / "shared" / "scripts"))

try:
    from tasks_service import tasks_service
    from ai_tasks_state import (
        check_priority_escalation,
        escalate_task_priority,
        load_state
    )
except ImportError as e:
    print(f"Error: Required modules not found: {e}")
    sys.exit(1)


def update_google_task_priority(google_task_id: str, new_priority: str, task_list_id: str) -> bool:
    """
    Update task priority in Google Tasks.
    
    Note: Google Tasks API doesn't have a direct priority field.
    We'll update the due date based on priority instead.
    
    Args:
        google_task_id: Google Task ID
        new_priority: New priority (P0/P1/P2)
        task_list_id: Task list ID
    
    Returns:
        True if updated, False otherwise
    """
    try:
        service = tasks_service()
        
        # Get current task
        task = service.tasks().get(
            tasklist=task_list_id,
            task=google_task_id
        ).execute()
        
        # Calculate new due date based on priority
        from datetime import timedelta
        now = datetime.now()
        
        if new_priority == "P0":
            new_due = (now + timedelta(days=0)).strftime('%Y-%m-%dT00:00:00Z')  # Today
        elif new_priority == "P1":
            new_due = (now + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')  # Tomorrow
        else:  # P2
            new_due = (now + timedelta(days=3)).strftime('%Y-%m-%dT00:00:00Z')  # 3 days
        
        # Update task
        task['due'] = new_due
        
        service.tasks().update(
            tasklist=task_list_id,
            task=google_task_id,
            body=task
        ).execute()
        
        return True
    except Exception as e:
        print(f"Error updating Google Task priority: {e}")
        return False


def escalate_tasks(config: Optional[Dict] = None) -> List[Dict]:
    """
    Check for and escalate stale tasks.
    
    Args:
        config: Configuration dict
    
    Returns:
        List of escalated tasks
    """
    if config is None:
        config = {
            "p2_to_p1_days": 5,
            "p1_to_p0_days": 3
        }
    
    # Load task list ID from config
    config_file = PROJECT_ROOT / "shared" / "config" / "ai-tasks-config.json"
    try:
        import json
        with open(config_file, 'r') as f:
            ai_config = json.load(f)
        task_list_id = ai_config.get('task_list_id')
    except Exception:
        print("Warning: Could not load task list ID from config")
        task_list_id = None
    
    # Check for escalations
    escalations = check_priority_escalation(config)
    
    if not escalations:
        return []
    
    escalated = []
    
    for esc in escalations:
        ai_task_id = esc["ai_task_id"]
        google_task_id = esc["google_task_id"]
        new_priority = esc["new_priority"]
        
        # Update state file
        if escalate_task_priority(ai_task_id, new_priority):
            # Update Google Tasks if we have task list ID
            if task_list_id and google_task_id:
                update_google_task_priority(google_task_id, new_priority, task_list_id)
            
            escalated.append(esc)
            print(f"  ✓ Escalated: [{esc['client']}] {esc['task_title']}")
            print(f"    {esc['current_priority']} → {new_priority} ({esc['days_open']} days open)")
    
    return escalated


if __name__ == "__main__":
    print("=" * 80)
    print("TASK PRIORITY ESCALATION CHECK")
    print("=" * 80)
    print()
    
    escalated = escalate_tasks()
    
    if escalated:
        print()
        print(f"✅ Escalated {len(escalated)} task(s)")
    else:
        print("✅ No tasks need escalation")
    
    print()

