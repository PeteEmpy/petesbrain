#!/usr/bin/env python3
"""
AI Tasks State Tracker

Tracks AI-generated tasks to enable:
- Context-aware regeneration (don't recreate if still open)
- Completion tracking (prevent regeneration of completed tasks)
- Priority change detection (respect user overrides)
- Task ID mapping (link AI task IDs to Google Task IDs)
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import uuid

PROJECT_ROOT = Path(__file__).parent.parent.parent
STATE_FILE = PROJECT_ROOT / "shared" / "data" / "ai-tasks-state.json"


def load_state() -> Dict:
    """Load AI tasks state from file."""
    if not STATE_FILE.exists():
        return {
            "tasks": {},
            "last_updated": datetime.now().isoformat(),
            "version": "1.0"
        }
    
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        return state
    except Exception as e:
        print(f"Warning: Error loading AI tasks state: {e}")
        return {
            "tasks": {},
            "last_updated": datetime.now().isoformat(),
            "version": "1.0"
        }


def save_state(state: Dict):
    """Save AI tasks state to file."""
    state["last_updated"] = datetime.now().isoformat()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Warning: Error saving AI tasks state: {e}")


def get_ai_task_id(task: Dict) -> Optional[str]:
    """
    Extract AI Task ID from task notes.
    
    Args:
        task: Task dict with 'notes' field
    
    Returns:
        AI Task ID if found, None otherwise
    """
    notes = task.get('notes', '')
    import re
    match = re.search(r'\*\*AI Task ID:\*\* ([a-f0-9\-]+)', notes)
    if match:
        return match.group(1)
    return None


def normalize_title(title: str) -> str:
    """Normalize title for comparison (shared helper)."""
    import re
    # Remove client prefix if present
    title = re.sub(r'^\[.+?\]\s*', '', title).strip()
    # Lowercase and normalize whitespace
    return ' '.join(title.lower().split())


def register_ai_task(
    ai_task_id: str,
    google_task_id: str,
    client: str,
    task_title: str,
    priority: str,
    due_date: str,
    check_duplicates: bool = True
) -> Dict:
    """
    Register a new AI-generated task in state file.
    
    Args:
        ai_task_id: UUID of the AI task
        google_task_id: Google Tasks task ID
        client: Client name
        task_title: Task title
        priority: Priority (P0/P1/P2)
        due_date: Due date string
        check_duplicates: If True, check for duplicate Google Task IDs (default: True)
    
    Returns:
        Updated state dict
    """
    state = load_state()
    
    # Check if Google Task ID already exists (prevent duplicate registration)
    if check_duplicates:
        for existing_id, existing_data in state["tasks"].items():
            if existing_data.get("google_task_id") == google_task_id:
                # Task already registered, return existing state
                return state
        
        # Also check for duplicate task titles for same client (fuzzy match)
        normalized_new_title = normalize_title(task_title)
        for existing_id, existing_data in state["tasks"].items():
            if existing_data.get("client") == client:
                existing_title = existing_data.get("task_title", "")
                normalized_existing_title = normalize_title(existing_title)
                if normalized_new_title == normalized_existing_title:
                    # Found duplicate title - update existing instead of creating new
                    existing_data["google_task_id"] = google_task_id
                    existing_data["due_date"] = due_date
                    existing_data["priority"] = priority
                    save_state(state)
                    return state
    
    state["tasks"][ai_task_id] = {
        "google_task_id": google_task_id,
        "client": client,
        "task_title": task_title,
        "priority": priority,
        "due_date": due_date,
        "created": datetime.now().isoformat(),
        "status": "open",
        "regenerated_count": 0,
        "last_regenerated": None,
        "user_modified_priority": False,
        "completed_date": None
    }
    
    save_state(state)
    return state


def update_task_status(
    google_task_id: str,
    status: str,
    priority: Optional[str] = None
) -> bool:
    """
    Update task status in state file.
    
    Args:
        google_task_id: Google Tasks task ID
        status: New status ("open" or "completed")
        priority: Optional new priority (if user changed it)
    
    Returns:
        True if task found and updated, False otherwise
    """
    state = load_state()
    
    # Find task by Google Task ID
    for ai_task_id, task_data in state["tasks"].items():
        if task_data.get("google_task_id") == google_task_id:
            task_data["status"] = status
            if status == "completed":
                task_data["completed_date"] = datetime.now().isoformat()
            if priority and priority != task_data.get("priority"):
                task_data["priority"] = priority
                task_data["user_modified_priority"] = True
            save_state(state)
            return True
    
    return False


def check_should_regenerate(
    client: str,
    task_title: str,
    priority: str,
    config: Optional[Dict] = None
) -> Tuple[bool, Optional[str]]:
    """
    Check if task should be regenerated based on state.
    
    Rules:
    - Don't regenerate if same task still open with same priority
    - Don't regenerate if completed within grace period
    - Don't regenerate if user modified priority (respect override)
    - Use fuzzy matching to catch near-duplicates
    
    Args:
        client: Client name
        task_title: Task title
        priority: Priority (P0/P1/P2)
        config: Configuration dict
    
    Returns:
        Tuple of (should_regenerate: bool, reason: Optional[str])
    """
    if config is None:
        config = {
            "completed_grace_period_days": 3,
            "similarity_threshold": 0.85  # Higher threshold for state file (stricter)
        }
    
    state = load_state()
    grace_period = config.get("completed_grace_period_days", 3)
    similarity_threshold = config.get("similarity_threshold", 0.85)
    
    # Normalize titles for comparison (using module-level function)
    normalized_new_title = normalize_title(task_title)
    
    # Import similarity function
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from duplicate_task_detector import calculate_similarity
    except ImportError:
        # Fallback to simple string comparison if module not available
        def calculate_similarity(str1: str, str2: str) -> float:
            from difflib import SequenceMatcher
            return SequenceMatcher(None, str1.lower().strip(), str2.lower().strip()).ratio()
    
    # Check all tasks for this client
    for ai_task_id, task_data in state["tasks"].items():
        if task_data.get("client") != client:
            continue
        
        # Check if same task title (exact match first, then fuzzy)
        stored_title = task_data.get("task_title", "")
        normalized_stored_title = normalize_title(stored_title)
        
        # Exact match
        if normalized_stored_title == normalized_new_title:
            match_found = True
        else:
            # Fuzzy match
            similarity = calculate_similarity(normalized_stored_title, normalized_new_title)
            match_found = similarity >= similarity_threshold
        
        if not match_found:
            continue
        
        # Check if user modified priority - respect override
        if task_data.get("user_modified_priority", False):
            stored_priority = task_data.get("priority")
            if stored_priority != priority:
                # User changed priority, allow regeneration
                continue
            else:
                # Same priority, user override - don't regenerate
                return (False, "User modified priority, respecting override")
        
        # Check status
        status = task_data.get("status", "open")
        
        if status == "open":
            stored_priority = task_data.get("priority")
            if stored_priority == priority:
                # Same task, same priority, still open - don't regenerate
                return (False, "Task still open with same priority")
        
        elif status == "completed":
            completed_date = task_data.get("completed_date")
            if completed_date:
                try:
                    completed_dt = datetime.fromisoformat(completed_date)
                    days_ago = (datetime.now() - completed_dt).days
                    if days_ago <= grace_period:
                        return (False, f"Task completed {days_ago} days ago (within grace period)")
                except (ValueError, AttributeError):
                    pass
    
    return (True, None)


def get_task_by_google_id(google_task_id: str) -> Optional[Dict]:
    """Get AI task data by Google Task ID."""
    state = load_state()
    for ai_task_id, task_data in state["tasks"].items():
        if task_data.get("google_task_id") == google_task_id:
            return task_data
    return None


def get_open_tasks_by_client(client: Optional[str] = None) -> List[Dict]:
    """
    Get all open tasks, optionally filtered by client.
    
    Args:
        client: Optional client name to filter by
    
    Returns:
        List of task dicts with 'ai_task_id' added
    """
    state = load_state()
    open_tasks = []
    
    for ai_task_id, task_data in state["tasks"].items():
        if task_data.get("status") != "open":
            continue
        
        if client and task_data.get("client") != client:
            continue
        
        task_dict = task_data.copy()
        task_dict["ai_task_id"] = ai_task_id
        open_tasks.append(task_dict)
    
    return open_tasks


def check_priority_escalation(
    config: Optional[Dict] = None
) -> List[Dict]:
    """
    Check for tasks that need priority escalation.
    
    Rules:
    - P2 task open for 5+ days → Escalate to P1
    - P1 task open for 3+ days → Escalate to P0
    
    Args:
        config: Configuration dict with escalation thresholds
    
    Returns:
        List of escalation records with:
        - ai_task_id
        - google_task_id
        - client
        - task_title
        - current_priority
        - new_priority
        - days_open
    """
    if config is None:
        config = {
            "p2_to_p1_days": 5,
            "p1_to_p0_days": 3
        }
    
    state = load_state()
    now = datetime.now()
    escalations = []
    
    p2_threshold = config.get("p2_to_p1_days", 5)
    p1_threshold = config.get("p1_to_p0_days", 3)
    
    for ai_task_id, task_data in state["tasks"].items():
        if task_data.get("status") != "open":
            continue
        
        # Skip if user modified priority (respect override)
        if task_data.get("user_modified_priority", False):
            continue
        
        priority = task_data.get("priority", "P2")
        created = task_data.get("created")
        
        if not created:
            continue
        
        try:
            created_dt = datetime.fromisoformat(created)
            days_open = (now - created_dt).days
            
            new_priority = None
            
            if priority == "P2" and days_open >= p2_threshold:
                new_priority = "P1"
            elif priority == "P1" and days_open >= p1_threshold:
                new_priority = "P0"
            
            if new_priority:
                escalations.append({
                    "ai_task_id": ai_task_id,
                    "google_task_id": task_data.get("google_task_id"),
                    "client": task_data.get("client"),
                    "task_title": task_data.get("task_title"),
                    "current_priority": priority,
                    "new_priority": new_priority,
                    "days_open": days_open
                })
        except (ValueError, AttributeError):
            continue
    
    return escalations


def escalate_task_priority(ai_task_id: str, new_priority: str) -> bool:
    """
    Escalate a task's priority in state file.
    
    Args:
        ai_task_id: AI Task ID
        new_priority: New priority (P0/P1/P2)
    
    Returns:
        True if escalated, False otherwise
    """
    state = load_state()
    
    if ai_task_id not in state["tasks"]:
        return False
    
    task_data = state["tasks"][ai_task_id]
    
    # Don't escalate if user modified priority
    if task_data.get("user_modified_priority", False):
        return False
    
    old_priority = task_data.get("priority")
    task_data["priority"] = new_priority
    task_data["last_escalated"] = datetime.now().isoformat()
    
    save_state(state)
    return True


def get_client_completion_stats(
    client: str,
    days: int = 7
) -> Dict:
    """
    Get completion statistics for a client.
    
    Args:
        client: Client name
        days: Number of days to look back
    
    Returns:
        Dict with:
        - completions_this_week: int
        - completions_last_week: int
        - open_tasks: int
        - completion_rate: float (completions / (completions + open))
    """
    state = load_state()
    now = datetime.now()
    cutoff_date = now - timedelta(days=days)
    
    completions = 0
    open_count = 0
    
    for ai_task_id, task_data in state["tasks"].items():
        if task_data.get("client") != client:
            continue
        
        status = task_data.get("status", "open")
        created = task_data.get("created")
        
        if not created:
            continue
        
        try:
            created_dt = datetime.fromisoformat(created)
            if created_dt < cutoff_date:
                continue
            
            if status == "completed":
                completed_date = task_data.get("completed_date")
                if completed_date:
                    completed_dt = datetime.fromisoformat(completed_date)
                    if completed_dt >= cutoff_date:
                        completions += 1
            elif status == "open":
                open_count += 1
        except (ValueError, AttributeError):
            continue
    
    total = completions + open_count
    completion_rate = completions / total if total > 0 else 0.0
    
    return {
        "completions_this_week": completions,
        "open_tasks": open_count,
        "completion_rate": completion_rate,
        "total_tasks": total
    }


def cleanup_old_tasks(days_to_keep: int = 30):
    """Remove tasks older than specified days from state file."""
    state = load_state()
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    tasks_to_remove = []
    for ai_task_id, task_data in state["tasks"].items():
        created = task_data.get("created")
        if created:
            try:
                created_dt = datetime.fromisoformat(created)
                if created_dt < cutoff_date:
                    tasks_to_remove.append(ai_task_id)
            except (ValueError, AttributeError):
                pass
    
    for ai_task_id in tasks_to_remove:
        del state["tasks"][ai_task_id]
    
    if tasks_to_remove:
        save_state(state)
        print(f"Cleaned up {len(tasks_to_remove)} old tasks from state file")
    
    return len(tasks_to_remove)


if __name__ == "__main__":
    # Test state tracking
    print("Testing AI tasks state tracker...")
    
    # Create test task
    test_ai_id = str(uuid.uuid4())
    register_ai_task(
        test_ai_id,
        "test_google_id_123",
        "smythson",
        "Review budget pacing",
        "P1",
        "2025-11-12"
    )
    
    print(f"Registered task: {test_ai_id}")
    
    # Check regeneration
    should_regen, reason = check_should_regenerate(
        "smythson",
        "Review budget pacing",
        "P1"
    )
    print(f"Should regenerate: {should_regen} (reason: {reason})")
    
    # Mark as completed
    update_task_status("test_google_id_123", "completed")
    print("Marked task as completed")
    
    # Check again
    should_regen, reason = check_should_regenerate(
        "smythson",
        "Review budget pacing",
        "P1"
    )
    print(f"Should regenerate after completion: {should_regen} (reason: {reason})")

