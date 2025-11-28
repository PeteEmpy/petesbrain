"""
Task Helper - Simplified interface for creating client tasks

This provides a simple interface for AI agents to create client tasks
without worrying about the underlying storage mechanism.
"""

from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'shared'))

from client_tasks_service import ClientTasksService


def create_client_task(
    title: str,
    client: str = None,
    priority: str = 'P2',
    due_date: str = None,
    time_estimate_mins: int = None,
    notes: str = None,
    source: str = 'AI Generated',
    tags: list = None
):
    """
    Create a client task - Simple wrapper for AI agents.

    Args:
        title: Task title (can include [Client] prefix)
        client: Client slug (auto-detected from title if not provided)
        priority: P0/P1/P2/P3 (default: P2)
        due_date: YYYY-MM-DD or natural language (default: None)
        time_estimate_mins: Estimated time in minutes
        notes: Additional context/notes
        source: How task was created (default: 'AI Generated')
        tags: List of tags

    Returns:
        Created task dict or None if error

    Examples:
        # Simple task
        create_client_task(
            title="[Superspace] Review campaign performance",
            priority="P1",
            due_date="2025-11-20"
        )

        # With full details
        create_client_task(
            title="[Godshot] Fix conversion tracking",
            priority="P0",
            due_date="2025-11-18",
            time_estimate_mins=60,
            notes="Critical: 80% conversion mismatch detected",
            source="Anomaly Detection",
            tags=["conversion-tracking", "urgent"]
        )
    """
    try:
        service = ClientTasksService()

        # Parse natural language due dates
        import re
        if due_date and not re.match(r'^\d{4}-\d{2}-\d{2}$', due_date):
            due_date = _parse_natural_due_date(due_date)

        task = service.create_task(
            title=title,
            client=client,
            priority=priority,
            due_date=due_date,
            time_estimate_mins=time_estimate_mins,
            notes=notes,
            source=source,
            tags=tags or []
        )

        print(f"✅ Created task: {task['title']} (Priority: {task['priority']})")
        return task

    except Exception as e:
        print(f"❌ Error creating task: {e}")
        return None


def _parse_natural_due_date(natural_date: str) -> str:
    """Parse natural language dates to YYYY-MM-DD format"""
    from datetime import datetime, timedelta

    natural_date = natural_date.lower().strip()
    today = datetime.now().date()

    # Handle common patterns
    if natural_date in ['today', 'now']:
        return today.isoformat()
    elif natural_date == 'tomorrow':
        return (today + timedelta(days=1)).isoformat()
    elif 'next week' in natural_date:
        return (today + timedelta(days=7)).isoformat()
    elif 'this week' in natural_date:
        # Find next occurrence of the day
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for i, day in enumerate(days):
            if day in natural_date:
                days_ahead = i - today.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return (today + timedelta(days=days_ahead)).isoformat()
        # Default to end of week
        return (today + timedelta(days=(6 - today.weekday()))).isoformat()
    elif natural_date.endswith(' days'):
        # "3 days", "7 days"
        try:
            days = int(natural_date.split()[0])
            return (today + timedelta(days=days)).isoformat()
        except:
            pass

    # If we can't parse it, return None
    return None


def get_client_tasks(client: str = None, priority: str = None):
    """Get active client tasks (optionally filtered by client/priority)"""
    try:
        service = ClientTasksService()
        return service.get_active_tasks(client=client, priority=priority)
    except Exception as e:
        print(f"❌ Error fetching tasks: {e}")
        return []


def complete_client_task(task_id: str):
    """Mark a client task as complete"""
    try:
        service = ClientTasksService()
        task = service.complete_task(task_id)
        if task:
            print(f"✅ Completed task: {task['title']}")
        return task
    except Exception as e:
        print(f"❌ Error completing task: {e}")
        return None


# Quick test
if __name__ == "__main__":
    print("Testing Task Helper...")

    # Create test task
    task = create_client_task(
        title="[Test Client] Test task from helper",
        priority="P2",
        due_date="tomorrow",
        time_estimate_mins=30,
        notes="This is a test task",
        tags=["test"]
    )

    if task:
        print(f"\n✅ Task created successfully!")
        print(f"   ID: {task['id']}")
        print(f"   Due: {task['due_date']}")

        # Clean up
        complete_client_task(task['id'])
        print(f"\n🗑️  Test task completed")
