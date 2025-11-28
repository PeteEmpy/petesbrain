#!/usr/bin/env python3
"""
Setup Script for AI Tasks Integration

Creates or finds the "Client Work" task list in Google Tasks
and saves the list ID to the configuration file.
"""

import json
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
    print(f"Expected at: {MCP_SERVER_PATH}")
    sys.exit(1)

CONFIG_FILE = PROJECT_ROOT / "shared" / "config" / "ai-tasks-config.json"
TASK_LIST_NAME = "Client Work"


def find_or_create_task_list():
    """
    Find existing "Client Work" task list or create it if it doesn't exist.
    
    Returns:
        Task list ID
    """
    try:
        service = tasks_service()
        
        # List all task lists
        print("📋 Fetching task lists...")
        results = service.tasklists().list(maxResults=100).execute()
        items = results.get('items', [])
        
        # Look for existing "Client Work" list
        for item in items:
            if item.get('title') == TASK_LIST_NAME:
                list_id = item.get('id')
                print(f"✅ Found existing task list: '{TASK_LIST_NAME}' (ID: {list_id})")
                return list_id
        
        # Create new task list if not found
        print(f"📝 Creating new task list: '{TASK_LIST_NAME}'...")
        task_list = {"title": TASK_LIST_NAME}
        result = service.tasklists().insert(body=task_list).execute()
        
        list_id = result.get('id')
        print(f"✅ Created task list: '{TASK_LIST_NAME}' (ID: {list_id})")
        return list_id
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def update_config_file(task_list_id: str):
    """Update configuration file with task list ID."""
    # Load existing config
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "task_list_name": TASK_LIST_NAME,
            "duplicate_detection": {
                "enabled": True,
                "similarity_threshold": 0.80,
                "lookback_days": 7,
                "completed_grace_period_days": 3
            },
            "due_date_mapping": {
                "P0": 0,
                "P1": 1,
                "P2": 3
            }
        }
    
    # Update task list ID
    config['task_list_id'] = task_list_id
    
    # Ensure config directory exists
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Save config
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"💾 Configuration saved to: {CONFIG_FILE}")


def main():
    """Main setup function."""
    print("=" * 80)
    print("AI TASKS INTEGRATION SETUP")
    print("=" * 80)
    print()
    
    # Find or create task list
    task_list_id = find_or_create_task_list()
    
    # Update config file
    update_config_file(task_list_id)
    
    print()
    print("=" * 80)
    print("SETUP COMPLETE")
    print("=" * 80)
    print()
    print(f"Task list ID: {task_list_id}")
    print(f"Config file: {CONFIG_FILE}")
    print()
    print("Next steps:")
    print("1. Run daily-client-work-generator.py to test task creation")
    print("2. Check Google Tasks for the 'Client Work' list")
    print("3. Verify tasks are created correctly")


if __name__ == "__main__":
    main()

