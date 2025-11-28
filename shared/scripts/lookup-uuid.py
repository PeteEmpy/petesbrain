#!/usr/bin/env python3
"""
Lookup a UUID in Google Tasks
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from google_tasks_client import GoogleTasksClient

def lookup_task_by_id(task_id):
    """Try to find a task by ID across all task lists"""
    client = GoogleTasksClient()
    
    # Get all task lists
    try:
        results = client.service.tasklists().list().execute()
        lists = results.get('items', [])
        
        print(f"Searching for task ID: {task_id}")
        print(f"Checking {len(lists)} task lists...\n")
        
        for task_list in lists:
            list_id = task_list['id']
            list_name = task_list['title']
            
            try:
                # Try to get the task
                task = client.service.tasks().get(
                    tasklist=list_id,
                    task=task_id
                ).execute()
                
                print(f"✅ Found task in '{list_name}':")
                print(f"   Title: {task.get('title', 'N/A')}")
                print(f"   Status: {task.get('status', 'N/A')}")
                print(f"   Due: {task.get('due', 'No due date')}")
                print(f"   Notes: {task.get('notes', 'No notes')[:100]}...")
                return task
                
            except Exception as e:
                # Task not found in this list, continue
                continue
        
        print("❌ Task not found in any task list")
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lookup-uuid.py <task-id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    lookup_task_by_id(task_id)
































