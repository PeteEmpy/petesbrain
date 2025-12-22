"""
Google Tasks Client for PetesBrain

Simple wrapper around Google Tasks API for creating and managing tasks
from PetesBrain agents.
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from difflib import SequenceMatcher
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/tasks"
]

# Default similarity threshold for duplicate detection (0-100)
DEFAULT_DUPLICATE_THRESHOLD = 75


class GoogleTasksClient:
    """Client for interacting with Google Tasks API"""
    
    def __init__(self):
        """Initialize the Google Tasks client with OAuth credentials"""
        self.service = self._get_service()
        self.default_list_id = None
    
    def _get_service(self):
        """Create and return a Google Tasks service instance using OAuth"""
        # Path to credentials (in infrastructure directory)
        project_root = Path(__file__).parent.parent
        token_path = project_root / "infrastructure" / "mcp-servers" / "google-tasks-mcp-server" / "token.json"
        credentials_path = project_root / "infrastructure" / "mcp-servers" / "google-tasks-mcp-server" / "credentials.json"
        
        creds = None
        
        # Load existing token if available
        if token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            except Exception as e:
                # Token file exists but is invalid - will re-authenticate
                print(f"Warning: Could not load existing token: {e}")
                creds = None
        
        # Refresh token if expired
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    # Try to refresh the token
                    creds.refresh(Request())
                    # Save refreshed token immediately
                    with open(token_path, "w") as token_file:
                        token_file.write(creds.to_json())
                except Exception as e:
                    # Refresh failed - need to re-authenticate
                    raise ValueError(
                        f"OAuth credentials not valid. Token refresh failed: {e}\n"
                        f"Token path: {token_path}\n"
                        f"Please run setup_oauth.py to re-authenticate."
                    )
            else:
                raise ValueError(
                    f"OAuth credentials not valid. Please run setup_oauth.py first.\n"
                    f"Token path: {token_path}"
                )
        
        return build("tasks", "v1", credentials=creds)
    
    def get_or_create_list(self, list_name="Peter's List"):
        """
        Get or create a task list by name.
        Returns the list ID.
        """
        try:
            # Get all task lists
            results = self.service.tasklists().list().execute()
            lists = results.get('items', [])
            
            # Check if list already exists
            for task_list in lists:
                if task_list['title'] == list_name:
                    return task_list['id']
            
            # Create new list if it doesn't exist
            new_list = {
                'title': list_name
            }
            result = self.service.tasklists().insert(body=new_list).execute()
            return result['id']
        
        except Exception as e:
            print(f"Error getting/creating task list: {e}")
            return None
    
    def _calculate_similarity(self, text1, text2):
        """
        Calculate similarity score between two texts (0-100).
        Uses SequenceMatcher for fuzzy matching.
        """
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio() * 100

    def find_duplicate_task(self, title, notes=None, threshold=DEFAULT_DUPLICATE_THRESHOLD, list_name=None):
        """
        Check if a similar task already exists in Google Tasks.

        Args:
            title (str): Task title to check
            notes (str): Optional notes to include in similarity check
            threshold (int): Similarity threshold (0-100), default 75%
            list_name (str): Specific list to check, or None for all lists

        Returns:
            tuple: (is_duplicate, matching_task) - matching_task is None if no duplicate
        """
        try:
            # Get existing tasks
            if list_name:
                existing_tasks = self.list_tasks(list_name, show_completed=False)
            else:
                existing_tasks = self.get_all_active_tasks()

            best_match = None
            best_score = 0.0

            for task in existing_tasks:
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

    def create_task(self, title, notes=None, due_date=None, list_name="Peter's List",
                    skip_duplicate_check=False, duplicate_threshold=DEFAULT_DUPLICATE_THRESHOLD):
        """
        Create a new task in Google Tasks with duplicate prevention.

        Args:
            title (str): Task title
            notes (str): Task notes/details
            due_date (str): Due date in format "Thursday this week", "2025-11-07", or datetime object
            list_name (str): Name of the task list (default: "Peter's List")
            skip_duplicate_check (bool): If True, skip duplicate checking (default: False)
            duplicate_threshold (int): Similarity threshold for duplicate detection (0-100)

        Returns:
            dict: Created task object, or existing task if duplicate found, or None if error

        Note:
            If a duplicate is found, returns the existing task with an added
            '_duplicate_skipped' key set to True.
        """
        try:
            # Check for duplicates unless explicitly skipped
            if not skip_duplicate_check:
                is_duplicate, existing_task, score = self.find_duplicate_task(
                    title, notes, threshold=duplicate_threshold, list_name=list_name
                )
                if is_duplicate:
                    print(f"  [Duplicate] Skipping task creation - {score:.0f}% similar to: '{existing_task.get('title', 'Unknown')}'")
                    existing_task['_duplicate_skipped'] = True
                    existing_task['_duplicate_score'] = score
                    return existing_task

            # Get or create the task list
            list_id = self.get_or_create_list(list_name)
            if not list_id:
                return None

            # Build task object
            task = {
                'title': title,
            }

            if notes:
                task['notes'] = notes

            # Parse due date
            if due_date:
                parsed_date = self._parse_due_date(due_date)
                if parsed_date:
                    # Google Tasks expects RFC 3339 timestamp
                    task['due'] = parsed_date.strftime('%Y-%m-%dT00:00:00.000Z')

            # Create the task
            result = self.service.tasks().insert(
                tasklist=list_id,
                body=task
            ).execute()

            return result

        except Exception as e:
            print(f"Error creating task: {e}")
            return None
    
    def _parse_due_date(self, due_input):
        """
        Parse various due date formats into datetime object.
        
        Supports:
        - "Thursday this week"
        - "Friday next week"
        - "2025-11-07"
        - datetime object
        """
        if isinstance(due_input, datetime):
            return due_input
        
        if isinstance(due_input, str):
            # Try parsing ISO date format
            try:
                return datetime.strptime(due_input, '%Y-%m-%d')
            except ValueError:
                pass
            
            # Parse natural language
            due_lower = due_input.lower()
            today = datetime.now()
            
            # "tomorrow"
            if 'tomorrow' in due_lower:
                return today + timedelta(days=1)
            
            # "next week"
            if 'next week' in due_lower:
                return today + timedelta(days=7)
            
            # "thursday this week", "friday", etc.
            weekdays = {
                'monday': 0, 'tuesday': 1, 'wednesday': 2,
                'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
            }
            
            for day_name, day_num in weekdays.items():
                if day_name in due_lower:
                    # Calculate days until target day
                    current_day = today.weekday()
                    days_ahead = day_num - current_day
                    
                    # If day has passed this week or is today, use next week
                    if days_ahead <= 0:
                        days_ahead += 7
                    
                    return today + timedelta(days=days_ahead)
            
            # "end of week" (Friday)
            if 'end of week' in due_lower or 'end of the week' in due_lower:
                current_day = today.weekday()
                days_to_friday = (4 - current_day) % 7
                if days_to_friday == 0 and today.weekday() != 4:
                    days_to_friday = 7
                return today + timedelta(days=days_to_friday)
        
        return None
    
    def uncomplete_task(self, task_id, list_name="Peter's List"):
        """Mark a completed task as incomplete (uncomplete it)"""
        try:
            list_id = self.get_or_create_list(list_name)
            if not list_id:
                return False
            
            task = self.service.tasks().get(
                tasklist=list_id,
                task=task_id
            ).execute()
            
            task['status'] = 'needsAction'
            # Remove completed timestamp if present
            if 'completed' in task:
                del task['completed']
            
            result = self.service.tasks().update(
                tasklist=list_id,
                task=task_id,
                body=task
            ).execute()
            
            return True
        
        except Exception as e:
            print(f"Error uncompleting task: {e}")
            return False
    
    def complete_task(self, task_id, list_name="Peter's List"):
        """Mark a task as completed"""
        try:
            list_id = self.get_or_create_list(list_name)
            if not list_id:
                return False
            
            task = self.service.tasks().get(
                tasklist=list_id,
                task=task_id
            ).execute()
            
            task['status'] = 'completed'
            
            result = self.service.tasks().update(
                tasklist=list_id,
                task=task_id,
                body=task
            ).execute()
            
            return True
        
        except Exception as e:
            print(f"Error completing task: {e}")
            return False
    
    def update_task(self, task_id, title=None, notes=None, due_date=None, list_name="Peter's List"):
        """
        Update an existing task in Google Tasks.
        
        Args:
            task_id (str): ID of the task to update
            title (str): New task title (optional)
            notes (str): New task notes/details (optional)
            due_date (str): New due date (optional)
            list_name (str): Name of the task list
            
        Returns:
            dict: Updated task object or None if error
        """
        try:
            list_id = self.get_or_create_list(list_name)
            if not list_id:
                return None
            
            # Get existing task
            task = self.service.tasks().get(
                tasklist=list_id,
                task=task_id
            ).execute()
            
            # Update fields if provided
            if title is not None:
                task['title'] = title
            
            if notes is not None:
                task['notes'] = notes
            
            if due_date is not None:
                # Parse due date
                due_datetime = self._parse_due_date(due_date)
                if due_datetime:
                    # Format as RFC 3339
                    task['due'] = due_datetime.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            
            # Update the task
            result = self.service.tasks().update(
                tasklist=list_id,
                task=task_id,
                body=task
            ).execute()
            
            return result
        
        except Exception as e:
            print(f"Error updating task: {e}")
            return None

    def delete_task(self, task_id, list_name="Peter's List"):
        """
        Delete a task from Google Tasks.

        Args:
            task_id (str): ID of the task to delete
            list_name (str): Name of the task list

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            list_id = self.get_or_create_list(list_name)
            if not list_id:
                return False

            # Delete the task
            self.service.tasks().delete(
                tasklist=list_id,
                task=task_id
            ).execute()

            return True

        except Exception as e:
            print(f"Error deleting task: {e}")
            return False

    def list_tasks(self, list_name="Peter's List", show_completed=False):
        """List all tasks in a given list"""
        try:
            list_id = self.get_or_create_list(list_name)
            if not list_id:
                return []
            
            results = self.service.tasks().list(
                tasklist=list_id,
                showCompleted=show_completed
            ).execute()
            
            return results.get('items', [])
        
        except Exception as e:
            print(f"Error listing tasks: {e}")
            return []
    
    def get_task_by_title(self, title, list_name="Peter's List", exact_match=True):
        """
        Find a task by its title.
        
        Args:
            title (str): Task title to search for
            list_name (str): Name of the task list (default: "Peter's List")
            exact_match (bool): If True, match exact title. If False, match if title contains search string.
        
        Returns:
            dict: Task object or None if not found
        """
        tasks = self.list_tasks(list_name, show_completed=False)
        for task in tasks:
            task_title = task.get('title', '')
            if exact_match:
                if task_title == title:
                    return task
            else:
                # Case-insensitive partial match
                if title.lower() in task_title.lower():
                    return task
        return None
    
    def find_tasks_by_title(self, search_term, list_name="Peter's List"):
        """
        Find all tasks matching a search term in the title.
        
        Args:
            search_term (str): Text to search for in task titles
            list_name (str): Name of the task list (default: "Peter's List")
        
        Returns:
            list: List of matching task objects
        """
        tasks = self.list_tasks(list_name, show_completed=False)
        matches = []
        search_lower = search_term.lower()
        for task in tasks:
            task_title = task.get('title', '')
            if search_lower in task_title.lower():
                matches.append(task)
        return matches
    
    def update_task_by_title(self, title, title_new=None, notes=None, due_date=None, list_name="Peter's List", exact_match=False):
        """
        Find and update a task by its title.
        
        This is a convenience method that combines finding and updating.
        
        Args:
            title (str): Current task title (or partial match if exact_match=False)
            title_new (str): New task title (optional)
            notes (str): New task notes (optional)
            due_date (str): New due date (optional)
            list_name (str): Name of the task list (default: "Peter's List")
            exact_match (bool): Whether to match exact title or allow partial match
        
        Returns:
            dict: Updated task object or None if not found or error
        """
        # Find the task
        task = self.get_task_by_title(title, list_name, exact_match=exact_match)
        if not task:
            print(f"Task not found: '{title}' in '{list_name}'")
            return None
        
        # Update using the task ID
        return self.update_task(
            task_id=task['id'],
            title=title_new,
            notes=notes,
            due_date=due_date,
            list_name=list_name
        )

    def get_all_active_tasks(self):
        """Get all active (incomplete) tasks from all task lists"""
        try:
            all_tasks = []

            # Get all task lists
            results = self.service.tasklists().list().execute()
            lists = results.get('items', [])

            for task_list in lists:
                list_id = task_list['id']
                list_name = task_list['title']

                # Get tasks from this list with pagination
                page_token = None
                while True:
                    tasks_result = self.service.tasks().list(
                        tasklist=list_id,
                        showCompleted=False,
                        showHidden=False,
                        maxResults=100,
                        pageToken=page_token
                    ).execute()

                    tasks = tasks_result.get('items', [])

                    # Add list name to each task for context
                    for task in tasks:
                        task['list_name'] = list_name
                        task['list_id'] = list_id  # Add list_id for deletion
                        all_tasks.append(task)

                    # Check for next page
                    page_token = tasks_result.get('nextPageToken')
                    if not page_token:
                        break

            return all_tasks

        except Exception as e:
            print(f"Error fetching all active tasks: {e}")
            return []


def get_all_active_tasks():
    """Standalone function to get all active tasks - for use by other scripts"""
    client = GoogleTasksClient()
    return client.get_all_active_tasks()


# Quick test function
if __name__ == "__main__":
    print("Testing Google Tasks Client...")
    
    client = GoogleTasksClient()
    
    # Test: Create a task
    task = client.create_task(
        title="Test task from PetesBrain",
        notes="This is a test task created by the Google Tasks integration",
        due_date="tomorrow"
    )
    
    if task:
        print(f"✅ Created task: {task['title']}")
        print(f"   ID: {task['id']}")
        print(f"   Due: {task.get('due', 'No due date')}")
    else:
        print("❌ Failed to create task")
    
    # Test: List tasks
    print("\n📋 Current tasks:")
    tasks = client.list_tasks()
    for t in tasks:
        print(f"   - {t['title']}")

