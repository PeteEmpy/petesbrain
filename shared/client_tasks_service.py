"""
Client Tasks Service for PetesBrain

Internal task management system for client work.
Per-client storage with parent/child task support.

Storage: clients/{client-slug}/tasks.json (per client)
Completed: clients/{client-slug}/tasks-completed.md (via existing system)
"""

import json
import uuid
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from difflib import SequenceMatcher
import re

# Default similarity threshold for duplicate detection (0-100)
DEFAULT_DUPLICATE_THRESHOLD = 75


class ClientTasksService:
    """Service for managing client tasks in per-client JSON stores"""

    def __init__(self):
        """Initialize the task service"""
        self.project_root = Path(__file__).parent.parent
        self.clients_dir = self.project_root / 'clients'
        self.audit_log = self.project_root / 'data' / 'state' / 'tasks-audit.log'

        # Ensure audit log directory exists
        self.audit_log.parent.mkdir(parents=True, exist_ok=True)

    def _get_client_task_file(self, client: str) -> Path:
        """Get the task file path for a specific client"""
        client_dir = self.clients_dir / client
        client_dir.mkdir(parents=True, exist_ok=True)
        task_file = client_dir / 'tasks.json'

        # PERMANENT GUARD: Prevent any attempts to write to product-feeds locations
        if 'product-feeds' in str(task_file):
            raise ValueError(
                f"❌ PERMANENT GUARD (2025-12-11): Refusing to write tasks to product-feeds location.\n"
                f"   Path: {task_file}\n"
                f"   All tasks have been consolidated to: {client_dir}/tasks.json\n"
                f"   Product-feeds/tasks.json is a LEGACY ARTIFACT and must not be used.\n"
                f"   See: docs/ARCHITECTURAL-MIGRATION-DEC10-2025.md"
            )

        return task_file

    def _load_client_tasks(self, client: str) -> Dict[str, Any]:
        """Load tasks for a specific client and clean up orphaned references"""
        task_file = self._get_client_task_file(client)

        if not task_file.exists():
            return {'tasks': [], 'last_updated': datetime.now().isoformat()}

        try:
            with open(task_file, 'r') as f:
                data = json.load(f)

            # Clean up orphaned child references in parent tasks
            data = self._cleanup_orphaned_children(data, client)

            return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {'tasks': [], 'last_updated': datetime.now().isoformat()}

    def _cleanup_orphaned_children(self, data: Dict[str, Any], client: str) -> Dict[str, Any]:
        """Remove child IDs from parent tasks if the child no longer exists"""
        task_ids = {task['id'] for task in data.get('tasks', [])}
        fixed = False

        for task in data.get('tasks', []):
            if task.get('type') == 'parent' and task.get('children'):
                original_children = task['children']
                # Keep only children that still exist
                task['children'] = [child_id for child_id in original_children if child_id in task_ids]

                if len(task['children']) != len(original_children):
                    removed = len(original_children) - len(task['children'])
                    print(f"⚠️  Cleaned up {removed} orphaned child reference(s) in parent task: {task['title']}")
                    fixed = True

        # Save the cleaned data if we fixed anything
        if fixed:
            self._save_client_tasks(client, data)

        return data

    def _log_audit(self, client: str, action: str, old_count: int, new_count: int):
        """Log task file modifications to audit trail"""
        import inspect

        # Get calling function/script info
        caller_frame = inspect.currentframe().f_back.f_back
        caller_file = caller_frame.f_code.co_filename if caller_frame else 'unknown'
        caller_function = caller_frame.f_code.co_name if caller_frame else 'unknown'

        timestamp = datetime.now().isoformat()
        log_entry = f"{timestamp} | {client:30} | {action:20} | {old_count:3} → {new_count:3} | {caller_function} ({Path(caller_file).name})\n"

        with open(self.audit_log, 'a') as f:
            f.write(log_entry)

    def _save_client_tasks(self, client: str, data: Dict[str, Any]):
        """Save tasks for a specific client with safety checks and audit logging"""
        import tempfile
        import shutil
        task_file = self._get_client_task_file(client)

        # SAFETY CHECK: Prevent accidental data loss
        # If file exists with tasks, don't allow saving empty array unless explicitly confirmed
        existing_count = 0
        if task_file.exists():
            try:
                with open(task_file, 'r') as f:
                    existing_data = json.load(f)
                existing_count = len(existing_data.get('tasks', []))
                new_count = len(data.get('tasks', []))

                # Alert if we're about to remove all tasks from a file that had tasks
                if existing_count > 0 and new_count == 0:
                    print(f"⚠️  SAFETY BLOCK: Refusing to save empty tasks array to {client}/tasks.json")
                    print(f"    File currently has {existing_count} tasks")
                    print(f"    This looks like accidental data loss. Aborting save.")
                    self._log_audit(client, 'BLOCKED_EMPTY_SAVE', existing_count, 0)
                    return  # Don't save - this prevents data loss

                # Warn if removing more than 50% of tasks in one operation
                if existing_count > 5 and new_count < existing_count * 0.5:
                    print(f"⚠️  WARNING: Large task reduction in {client}/tasks.json")
                    print(f"    Reducing from {existing_count} to {new_count} tasks")
                    self._log_audit(client, 'LARGE_REDUCTION', existing_count, new_count)
                    # Still allow but log warning
            except (json.JSONDecodeError, FileNotFoundError):
                pass  # File is new or corrupted, allow save

        data['last_updated'] = datetime.now().isoformat()

        # ATOMIC WRITE: Write to temp file first, then rename
        # This prevents corruption if write is interrupted
        temp_fd, temp_path = tempfile.mkstemp(suffix='.json', dir=task_file.parent, text=True)
        try:
            with os.fdopen(temp_fd, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Atomic rename (on POSIX systems)
            shutil.move(temp_path, task_file)

            # Log successful save to audit trail
            new_count = len(data.get('tasks', []))
            self._log_audit(client, 'SAVE', existing_count, new_count)

        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise

    def _get_all_clients_with_tasks(self) -> List[str]:
        """Get list of all clients that have task files"""
        clients = []

        if not self.clients_dir.exists():
            return clients

        for client_dir in self.clients_dir.iterdir():
            if client_dir.is_dir() and not client_dir.name.startswith('_'):
                task_file = client_dir / 'tasks.json'
                if task_file.exists():
                    clients.append(client_dir.name)

        return clients

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity score between two texts (0-100).
        Uses SequenceMatcher for fuzzy matching.
        """
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio() * 100

    def find_duplicate_task(
        self,
        title: str,
        client: str,
        notes: Optional[str] = None,
        threshold: int = DEFAULT_DUPLICATE_THRESHOLD
    ) -> Tuple[bool, Optional[Dict], float]:
        """
        Check if a similar task already exists for this client.

        Args:
            title: Task title to check
            client: Client slug
            notes: Optional notes to include in similarity check
            threshold: Similarity threshold (0-100), default 75%

        Returns:
            tuple: (is_duplicate, matching_task, score) - matching_task is None if no duplicate
        """
        try:
            data = self._load_client_tasks(client)
            active_tasks = [t for t in data.get('tasks', []) if t.get('status') == 'active']

            best_match = None
            best_score = 0.0

            for task in active_tasks:
                existing_title = task.get('title', '')
                existing_notes = task.get('notes', '')

                # Calculate title similarity
                title_sim = self._calculate_similarity(title, existing_title)

                # Also check notes if provided
                notes_sim = 0.0
                if notes and existing_notes:
                    notes_sim = self._calculate_similarity(notes, existing_notes)

                # Use the higher of the two scores
                score = max(title_sim, notes_sim)

                if score > best_score:
                    best_score = score
                    best_match = task

            is_duplicate = best_score >= threshold
            return (is_duplicate, best_match if is_duplicate else None, best_score)

        except Exception as e:
            print(f"Error checking for duplicates: {e}")
            return (False, None, 0.0)

    def create_task(
        self,
        title: str,
        client: Optional[str] = None,
        priority: str = 'P2',
        due_date: Optional[str] = None,
        time_estimate_mins: Optional[int] = None,
        notes: Optional[str] = None,
        source: str = 'Manual',
        tags: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
        task_type: str = 'standalone',  # 'parent', 'child', or 'standalone'
        parent_id: Optional[str] = None,
        skip_duplicate_check: bool = False,
        duplicate_threshold: int = DEFAULT_DUPLICATE_THRESHOLD
    ) -> Dict[str, Any]:
        """
        Create a new client task with duplicate prevention.

        Args:
            title: Task title (can include [Client] prefix)
            client: Client slug (e.g., 'superspace', 'uno-lighting')
            priority: P0 (urgent), P1 (high), P2 (normal), P3 (low)
            due_date: ISO date string (YYYY-MM-DD) or None
            time_estimate_mins: Estimated time in minutes
            notes: Additional notes/context
            source: How task was created (e.g., 'AI Generated', 'Email', 'Meeting')
            tags: List of tags for categorization
            context: Additional structured data (verification, Google Ads data, etc.)
            task_type: 'parent', 'child', or 'standalone'
            parent_id: If type='child', the parent task ID
            skip_duplicate_check: If True, skip duplicate checking (default: False)
            duplicate_threshold: Similarity threshold for duplicate detection (0-100)

        Returns:
            Created task object, or existing task if duplicate found

        Note:
            If a duplicate is found, returns the existing task with an added
            '_duplicate_skipped' key set to True.
        """
        # Extract client from title if not provided
        if not client and title.startswith('['):
            match = re.match(r'\[([^\]]+)\]', title)
            if match:
                client_name = match.group(1).lower()
                # Normalize client name to slug format
                client = client_name.replace(' ', '-')

        if not client:
            raise ValueError("Client must be specified or extractable from title")

        # Check for duplicates unless explicitly skipped
        if not skip_duplicate_check:
            is_duplicate, existing_task, score = self.find_duplicate_task(
                title, client, notes, threshold=duplicate_threshold
            )
            if is_duplicate:
                print(f"  [Duplicate] Skipping task creation - {score:.0f}% similar to: '{existing_task.get('title', 'Unknown')}'")
                existing_task['_duplicate_skipped'] = True
                existing_task['_duplicate_score'] = score
                return existing_task

        # Extract priority from title/notes if marked as P0/P1/etc
        detected_priority = self._detect_priority(title, notes or '')
        if detected_priority:
            priority = detected_priority

        # Generate task ID
        task_id = str(uuid.uuid4())

        # Create task object
        task = {
            'id': task_id,
            'title': title,
            'type': task_type,
            'parent_id': parent_id,
            'children': [] if task_type == 'parent' else None,
            'priority': priority,
            'due_date': due_date,
            'time_estimate_mins': time_estimate_mins,
            'notes': notes,
            'source': source,
            'tags': tags or [],
            'context': context or {},
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'completed_at': None
        }

        # Add to client's task file
        data = self._load_client_tasks(client)
        data['tasks'].append(task)

        # If this is a child task, add to parent's children list
        if parent_id:
            for parent_task in data['tasks']:
                if parent_task['id'] == parent_id:
                    if parent_task.get('children') is None:
                        parent_task['children'] = []
                    parent_task['children'].append(task_id)
                    break

        self._save_client_tasks(client, data)

        return task

    def create_parent_with_children(
        self,
        parent_title: str,
        client: str,
        children_data: List[Dict[str, Any]],
        parent_due_date: Optional[str] = None,
        parent_notes: Optional[str] = None,
        parent_source: str = 'Manual',
        parent_tags: Optional[List[str]] = None,
        parent_priority: str = 'P1'
    ) -> Dict[str, Any]:
        """
        Create a parent task and multiple children in one operation.

        Args:
            parent_title: Title for parent task
            client: Client slug
            children_data: List of dicts with child task data (title, due_date, time_estimate_mins, notes, etc.)
            parent_due_date: Due date for parent (usually latest child due date)
            parent_notes: Notes for parent
            parent_source: Source for parent
            parent_tags: Tags for parent
            parent_priority: Priority for parent

        Returns:
            Parent task object with children populated
        """
        # Create parent task first
        parent_task = self.create_task(
            title=parent_title,
            client=client,
            priority=parent_priority,
            due_date=parent_due_date,
            time_estimate_mins=sum(c.get('time_estimate_mins', 0) for c in children_data),
            notes=parent_notes,
            source=parent_source,
            tags=parent_tags,
            task_type='parent'
        )

        parent_id = parent_task['id']

        # Create all child tasks
        for child_data in children_data:
            self.create_task(
                title=child_data.get('title'),
                client=client,
                priority=child_data.get('priority', 'P2'),
                due_date=child_data.get('due_date'),
                time_estimate_mins=child_data.get('time_estimate_mins'),
                notes=child_data.get('notes'),
                source=child_data.get('source', parent_source),
                tags=child_data.get('tags', []),
                task_type='child',
                parent_id=parent_id
            )

        # Reload parent to get updated children list
        return self.get_task(parent_id, client)

    def _detect_priority(self, title: str, notes: str) -> Optional[str]:
        """Detect priority from title/notes"""
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

        return None

    def get_task(self, task_id: str, client: str) -> Optional[Dict[str, Any]]:
        """Get a task by ID from a specific client"""
        data = self._load_client_tasks(client)
        for task in data['tasks']:
            if task['id'] == task_id:
                return task
        return None

    def get_task_any_client(self, task_id: str) -> Optional[tuple[Dict[str, Any], str]]:
        """
        Get a task by ID, searching all clients.

        Returns:
            Tuple of (task, client_slug) or None if not found
        """
        for client in self._get_all_clients_with_tasks():
            task = self.get_task(task_id, client)
            if task:
                return (task, client)
        return None

    def update_task(
        self,
        task_id: str,
        client: str,
        title: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
        time_estimate_mins: Optional[int] = None,
        notes: Optional[str] = None,
        tags: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None,
        completion_notes: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Update an existing task.

        Returns:
            Updated task object or None if not found
        """
        data = self._load_client_tasks(client)

        for task in data['tasks']:
            if task['id'] == task_id:
                # Update fields if provided
                if title is not None:
                    task['title'] = title
                if priority is not None:
                    task['priority'] = priority
                if due_date is not None:
                    task['due_date'] = due_date
                if time_estimate_mins is not None:
                    task['time_estimate_mins'] = time_estimate_mins
                if notes is not None:
                    task['notes'] = notes
                if tags is not None:
                    task['tags'] = tags
                if context is not None:
                    # Merge context rather than replace
                    task['context'].update(context)
                if status is not None:
                    task['status'] = status
                    if status == 'completed':
                        task['completed_at'] = datetime.now().isoformat()
                        # Store completion notes if provided
                        if completion_notes is not None:
                            task['completion_notes'] = completion_notes

                        # If this is a parent, check if all children are complete
                        if task.get('type') == 'parent' and task.get('children'):
                            all_children_complete = True
                            for child_id in task['children']:
                                child = self.get_task(child_id, client)
                                if child and child['status'] != 'completed':
                                    all_children_complete = False
                                    break

                            # Only mark parent complete if all children complete
                            if not all_children_complete:
                                task['status'] = 'active'
                                task['completed_at'] = None

                task['updated_at'] = datetime.now().isoformat()
                self._save_client_tasks(client, data)
                return task

        return None

    def _calculate_next_due_date(self, current_due_date: Optional[str], recurrence_pattern: str) -> str:
        """
        Calculate the next due date based on recurrence pattern.

        Args:
            current_due_date: Current due date in YYYY-MM-DD format (or None)
            recurrence_pattern: daily, weekly, fortnightly, monthly

        Returns:
            Next due date in YYYY-MM-DD format
        """
        # Use current due date if available, otherwise use today
        if current_due_date:
            try:
                base_date = datetime.strptime(current_due_date, '%Y-%m-%d')
            except ValueError:
                base_date = datetime.now()
        else:
            base_date = datetime.now()

        pattern = recurrence_pattern.lower()

        if pattern == 'daily':
            next_date = base_date + timedelta(days=1)
        elif pattern == 'weekly':
            next_date = base_date + timedelta(weeks=1)
        elif pattern == 'fortnightly':
            next_date = base_date + timedelta(weeks=2)
        elif pattern == 'monthly':
            # Add one month (handle edge cases like Jan 31 -> Feb 28)
            month = base_date.month
            year = base_date.year
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
            # Handle day overflow (e.g., Jan 31 -> Feb 28/29)
            day = base_date.day
            while True:
                try:
                    next_date = base_date.replace(year=year, month=month, day=day)
                    break
                except ValueError:
                    day -= 1
        else:
            # Default to weekly if pattern not recognized
            next_date = base_date + timedelta(weeks=1)

        return next_date.strftime('%Y-%m-%d')

    def complete_task(self, task_id: str, client: str, completion_notes: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Complete a task: Remove from tasks.json and log to tasks-completed.md.
        If task has a recurring tag, automatically creates next occurrence.

        Args:
            task_id: Task UUID
            client: Client slug
            completion_notes: Optional notes describing what was done to complete the task

        Returns:
            Completed task object
        """
        # Get the task before completing it
        task = self.get_task(task_id, client)
        if not task:
            return None

        # Check if task has a recurring tag (format: "recurring:pattern")
        recurrence_pattern = None
        for tag in task.get('tags', []):
            if tag.startswith('recurring:'):
                recurrence_pattern = tag.split(':', 1)[1]
                break

        # CRITICAL: Remove from tasks.json (not just mark as completed)
        data = self._load_client_tasks(client)

        # Find and remove the task
        completed_task = None
        for i, t in enumerate(data['tasks']):
            if t['id'] == task_id:
                completed_task = data['tasks'].pop(i)
                break

        if not completed_task:
            return None

        # Add completion metadata
        completed_task['completed_at'] = datetime.now().isoformat()
        if completion_notes:
            completed_task['completion_notes'] = completion_notes

        # Save updated tasks.json (with task removed)
        data['last_updated'] = datetime.now().isoformat()
        self._save_client_tasks(client, data)

        # Log to tasks-completed.md
        self._log_to_completed_file(client, completed_task, completion_notes)

        # Rebuild cache so task manager updates immediately
        self._rebuild_cache()

        # If recurring, create next occurrence
        if recurrence_pattern:
            next_due_date = self._calculate_next_due_date(task.get('due_date'), recurrence_pattern)

            # Create new task with same properties
            new_task = self.create_task(
                title=task['title'],
                client=client,
                priority=task.get('priority'),
                due_date=next_due_date,
                time_estimate_mins=task.get('time_estimate_mins'),
                notes=task.get('notes'),
                source=task.get('source', 'Recurring task'),
                tags=task.get('tags', []),
                task_type=task.get('type', 'standalone')
            )

            print(f"\n✅ Recurring task: Created next occurrence for {next_due_date}")
            print(f"   New task ID: {new_task['id']}")

        return completed_task

    def _log_to_completed_file(self, client: str, task: Dict[str, Any], completion_notes: Optional[str] = None):
        """Log completed task to tasks-completed.md"""
        from datetime import datetime

        client_dir = self.clients_dir / client
        completed_file = client_dir / 'tasks-completed.md'

        # Create completion entry
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        entry = f"""## {task['title']}
**Completed:** {timestamp}
**Source:** {task.get('source', 'Unknown')}

"""

        if completion_notes:
            entry += f"{completion_notes}\n\n"
        elif task.get('notes'):
            entry += f"{task['notes']}\n\n"

        entry += "---\n"

        # Append to tasks-completed.md
        with open(completed_file, 'a') as f:
            f.write(entry)

    def _rebuild_cache(self):
        """Rebuild the client-tasks.json cache file after task changes"""
        from datetime import datetime
        import json
        import subprocess

        all_tasks = []

        for client_dir in sorted(self.clients_dir.iterdir()):
            if not client_dir.is_dir() or client_dir.name.startswith('_'):
                continue

            task_file = client_dir / 'tasks.json'
            if task_file.exists():
                try:
                    with open(task_file, 'r') as f:
                        data = json.load(f)

                    for task in data.get('tasks', []):
                        task['client'] = client_dir.name
                        all_tasks.append(task)
                except Exception:
                    pass  # Skip files that can't be read

        # Save to cached file
        cache_file = Path('/Users/administrator/Documents/PetesBrain/data/state/client-tasks.json')
        cache_data = {
            'tasks': all_tasks,
            'last_updated': datetime.now().isoformat(),
            'total_count': len(all_tasks)
        }

        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)

        # Regenerate HTML task manager
        try:
            html_generator = Path('/Users/administrator/Documents/PetesBrain/generate-tasks-overview.py')
            if html_generator.exists():
                subprocess.run(
                    ['/usr/local/bin/python3', str(html_generator)],
                    cwd=Path('/Users/administrator/Documents/PetesBrain'),
                    capture_output=True,
                    timeout=10
                )
        except Exception:
            pass  # Don't fail task completion if HTML generation fails

    def delete_task(self, task_id: str, client: str) -> bool:
        """Delete a task"""
        data = self._load_client_tasks(client)
        original_count = len(data['tasks'])

        # Find the task to delete
        task_to_delete = None
        for task in data['tasks']:
            if task['id'] == task_id:
                task_to_delete = task
                break

        if not task_to_delete:
            return False

        # If deleting a parent, also delete all children
        if task_to_delete.get('type') == 'parent' and task_to_delete.get('children'):
            child_ids = task_to_delete['children']
            data['tasks'] = [t for t in data['tasks'] if t['id'] not in child_ids and t['id'] != task_id]
        else:
            # If deleting a child, remove from parent's children list
            if task_to_delete.get('parent_id'):
                for parent in data['tasks']:
                    if parent['id'] == task_to_delete['parent_id'] and parent.get('children'):
                        parent['children'] = [c for c in parent['children'] if c != task_id]

            # Delete the task
            data['tasks'] = [t for t in data['tasks'] if t['id'] != task_id]

        if len(data['tasks']) < original_count:
            self._save_client_tasks(client, data)
            return True
        return False

    def get_active_tasks(
        self,
        client: Optional[str] = None,
        priority: Optional[str] = None,
        due_before: Optional[str] = None,
        tags: Optional[List[str]] = None,
        include_children: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get all active tasks with optional filters.

        Args:
            client: Filter by client slug (if None, gets all clients)
            priority: Filter by priority (P0, P1, P2, P3)
            due_before: Filter by due date (ISO string)
            tags: Filter by tags (task must have ALL specified tags)
            include_children: If False, only return parent/standalone tasks

        Returns:
            List of matching tasks
        """
        all_tasks = []

        # Get tasks from specific client or all clients
        if client:
            clients = [client]
        else:
            clients = self._get_all_clients_with_tasks()

        for client_slug in clients:
            data = self._load_client_tasks(client_slug)
            client_tasks = [t for t in data['tasks'] if t['status'] == 'active']

            # Add client slug to each task for reference
            for task in client_tasks:
                task['_client'] = client_slug

            all_tasks.extend(client_tasks)

        # Apply filters
        if not include_children:
            all_tasks = [t for t in all_tasks if t.get('type') != 'child']

        if priority:
            all_tasks = [t for t in all_tasks if t['priority'] == priority]

        if due_before:
            all_tasks = [t for t in all_tasks if t.get('due_date') and t['due_date'] <= due_before]

        if tags:
            all_tasks = [t for t in all_tasks if all(tag in t.get('tags', []) for tag in tags)]

        return all_tasks

    def get_tasks_by_priority(self, client: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Get all active tasks grouped by priority"""
        tasks = self.get_active_tasks(client=client)

        grouped = {
            'P0': [],
            'P1': [],
            'P2': [],
            'P3': []
        }

        for task in tasks:
            priority = task.get('priority', 'P2')
            if priority in grouped:
                grouped[priority].append(task)

        return grouped

    def get_upcoming_tasks(self, days: int = 7, client: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get tasks due in the next N days"""
        today = datetime.now().date()
        future_date = today + timedelta(days=days)

        tasks = self.get_active_tasks(client=client)
        upcoming = []

        for task in tasks:
            if task.get('due_date'):
                try:
                    due_date = datetime.fromisoformat(task['due_date']).date()
                    if today <= due_date <= future_date:
                        upcoming.append(task)
                except ValueError:
                    pass

        # Sort by due date
        upcoming.sort(key=lambda t: t.get('due_date', '9999-12-31'))
        return upcoming

    def get_overdue_tasks(self, client: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get tasks that are past their due date"""
        today = datetime.now().date().isoformat()

        tasks = self.get_active_tasks(client=client)
        overdue = []

        for task in tasks:
            if task.get('due_date') and task['due_date'] < today:
                overdue.append(task)

        # Sort by due date (oldest first)
        overdue.sort(key=lambda t: t.get('due_date', ''))
        return overdue

    def get_completed_tasks(
        self,
        client: Optional[str] = None,
        since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get completed tasks.

        Args:
            client: Filter by client
            since: ISO date string - only return tasks completed after this date

        Returns:
            List of completed tasks
        """
        all_tasks = []

        if client:
            clients = [client]
        else:
            clients = self._get_all_clients_with_tasks()

        for client_slug in clients:
            data = self._load_client_tasks(client_slug)
            client_tasks = [t for t in data['tasks'] if t['status'] == 'completed']

            # Add client slug
            for task in client_tasks:
                task['_client'] = client_slug

            all_tasks.extend(client_tasks)

        if since:
            all_tasks = [t for t in all_tasks if t.get('completed_at', '') >= since]

        # Sort by completion date (newest first)
        all_tasks.sort(key=lambda t: t.get('completed_at', ''), reverse=True)
        return all_tasks

    def archive_completed_tasks(self, older_than_days: int = 30, client: Optional[str] = None) -> int:
        """
        Archive (delete) completed tasks older than N days.

        Note: Completed tasks should already be in tasks-completed.md
        via the existing completion workflow.

        Returns:
            Number of tasks archived
        """
        cutoff_date = (datetime.now() - timedelta(days=older_than_days)).isoformat()
        total_archived = 0

        if client:
            clients = [client]
        else:
            clients = self._get_all_clients_with_tasks()

        for client_slug in clients:
            data = self._load_client_tasks(client_slug)
            original_count = len(data['tasks'])

            # Keep only: active tasks OR recently completed tasks
            data['tasks'] = [
                t for t in data['tasks']
                if t['status'] == 'active' or t.get('completed_at', '9999') > cutoff_date
            ]

            archived_count = original_count - len(data['tasks'])
            total_archived += archived_count

            if archived_count > 0:
                self._save_client_tasks(client_slug, data)

        return total_archived

    def get_stats(self, client: Optional[str] = None) -> Dict[str, Any]:
        """Get task statistics"""
        all_tasks = []

        if client:
            clients = [client]
        else:
            clients = self._get_all_clients_with_tasks()

        for client_slug in clients:
            data = self._load_client_tasks(client_slug)
            for task in data['tasks']:
                task['_client'] = client_slug
            all_tasks.extend(data['tasks'])

        active = [t for t in all_tasks if t['status'] == 'active']
        completed = [t for t in all_tasks if t['status'] == 'completed']

        # Count by priority
        priority_counts = {
            'P0': len([t for t in active if t.get('priority') == 'P0']),
            'P1': len([t for t in active if t.get('priority') == 'P1']),
            'P2': len([t for t in active if t.get('priority') == 'P2']),
            'P3': len([t for t in active if t.get('priority') == 'P3']),
        }

        # Count by client
        client_counts = {}
        for task in active:
            client_name = task.get('_client', 'unassigned')
            client_counts[client_name] = client_counts.get(client_name, 0) + 1

        # Count by type
        type_counts = {
            'parent': len([t for t in active if t.get('type') == 'parent']),
            'child': len([t for t in active if t.get('type') == 'child']),
            'standalone': len([t for t in active if t.get('type') == 'standalone']),
        }

        return {
            'total_tasks': len(all_tasks),
            'active_tasks': len(active),
            'completed_tasks': len(completed),
            'priority_counts': priority_counts,
            'type_counts': type_counts,
            'client_counts': client_counts,
            'overdue_count': len(self.get_overdue_tasks(client=client)),
            'clients_with_tasks': len(clients)
        }


# Standalone helper functions for easy import
def create_task(**kwargs) -> Dict[str, Any]:
    """Create a task (standalone function)"""
    service = ClientTasksService()
    return service.create_task(**kwargs)


def get_active_tasks(**kwargs) -> List[Dict[str, Any]]:
    """Get active tasks (standalone function)"""
    service = ClientTasksService()
    return service.get_active_tasks(**kwargs)


def complete_task(task_id: str, client: str, completion_notes: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Complete a task (standalone function)"""
    service = ClientTasksService()
    return service.complete_task(task_id, client, completion_notes=completion_notes)


def get_stats(**kwargs) -> Dict[str, Any]:
    """Get task stats (standalone function)"""
    service = ClientTasksService()
    return service.get_stats(**kwargs)


# Quick test
if __name__ == "__main__":
    print("Testing Client Tasks Service (Per-Client Architecture)...")

    service = ClientTasksService()

    # Create test parent task with children
    parent = service.create_parent_with_children(
        parent_title="[Superspace] Q4 Campaign Optimization",
        client="superspace",
        children_data=[
            {
                'title': '[Superspace] Update ad copy for Black Friday',
                'due_date': '2025-11-25',
                'time_estimate_mins': 60,
                'priority': 'P1'
            },
            {
                'title': '[Superspace] Increase budgets for peak period',
                'due_date': '2025-11-24',
                'time_estimate_mins': 30,
                'priority': 'P1'
            }
        ],
        parent_due_date='2025-11-25',
        parent_notes='Complete Q4 optimization before Black Friday',
        parent_priority='P1'
    )

    print(f"\n✅ Created parent task: {parent['title']}")
    print(f"   ID: {parent['id']}")
    print(f"   Type: {parent['type']}")
    print(f"   Children: {len(parent['children'])} tasks")

    # Get active tasks
    active = service.get_active_tasks(client='superspace')
    print(f"\n📋 Active Superspace tasks: {len(active)}")

    # Get stats
    stats = service.get_stats()
    print(f"\n📊 Stats:")
    print(f"   Total: {stats['total_tasks']}")
    print(f"   Active: {stats['active_tasks']}")
    print(f"   By priority: {stats['priority_counts']}")
    print(f"   By type: {stats['type_counts']}")
    print(f"   Clients with tasks: {stats['clients_with_tasks']}")

    # Clean up test tasks
    service.delete_task(parent['id'], 'superspace')
    print(f"\n🗑️  Deleted test tasks")
