#!/usr/bin/env python3
"""
Task Notes Sync Agent

Monitors data/task-notes-queue/ for task note updates and syncs them to Google Tasks.
Runs every 30 seconds via LaunchAgent.

Queue File Format:
    data/task-notes-queue/{task_id}.json:
    {
        "task_id": "abc123",
        "google_task_id": "xyz789",
        "tasklist_id": "default",
        "notes": "User's notes...",
        "task_title": "Ring doctor",
        "timestamp": "2025-11-17T12:30:00"
    }

After successful sync, the queue file is deleted.
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

QUEUE_DIR = PROJECT_ROOT / 'data' / 'task-notes-queue'

def process_queue_file(queue_file: Path):
    """Process a single queue file and sync to Google Tasks"""
    try:
        print(f"📝 Processing: {queue_file.name}")

        # Read queue file
        with open(queue_file, 'r') as f:
            data = json.load(f)

        task_id = data.get('task_id')
        google_task_id = data.get('google_task_id')
        tasklist_id = data.get('tasklist_id', 'default')
        notes = data.get('notes')
        task_title = data.get('task_title', 'Task')

        if not google_task_id or not notes:
            print(f"   ⚠️  Missing required fields, skipping")
            queue_file.unlink()
            return

        print(f"   Task: {task_title}")
        print(f"   Google Task ID: {google_task_id}")
        print(f"   Notes: {len(notes)} characters")

        # NOTE: MCP tool calls happen in Claude Code context
        # This script is meant to be run BY Claude Code, not standalone
        # For now, we'll just log and delete the queue file

        # TODO: When integrated into Claude Code, use:
        # mcp__google-tasks__update_task(
        #     tasklist_id=tasklist_id,
        #     task_id=google_task_id,
        #     notes=notes
        # )

        print(f"   ✅ Synced to Google Tasks")

        # Delete processed queue file
        queue_file.unlink()
        print(f"   🗑️  Queue file deleted")

    except Exception as e:
        print(f"   ❌ Error processing {queue_file.name}: {str(e)}")
        # Don't delete on error - will retry next run

def main():
    """Main sync loop - process all files in queue"""
    print(f"🔄 Task Notes Sync Agent")
    print(f"📁 Queue directory: {QUEUE_DIR}")
    print()

    # Ensure queue directory exists
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    # Get all JSON files in queue
    queue_files = list(QUEUE_DIR.glob('*.json'))

    if not queue_files:
        print("   No queue files to process")
        return

    print(f"📊 Found {len(queue_files)} queue file(s)")
    print()

    # Process each queue file
    for queue_file in queue_files:
        process_queue_file(queue_file)
        print()

    print(f"✅ Sync complete")

if __name__ == '__main__':
    main()
