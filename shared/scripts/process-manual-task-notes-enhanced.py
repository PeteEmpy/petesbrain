#!/usr/bin/env python3
"""
Enhanced Process Manual Task Notes - Handles Both Internal and Google Tasks

Processes manual notes added via tasks-overview.html interface.
Detects task type (internal vs Google) and updates appropriately.

Usage:
    python3 process-manual-task-notes-enhanced.py
"""

import json
import sys
import re
import base64
from pathlib import Path
from datetime import datetime

# Import Google Tasks service
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server')
from tasks_service import tasks_service

NOTES_FILE = "/Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json"

class EnhancedTaskProcessor:
    def __init__(self):
        self.notes_file = Path(NOTES_FILE)
        self.notes = self.load_notes()
        self.google_service = None

    def load_notes(self):
        """Load manual notes from JSON file"""
        if not self.notes_file.exists():
            return []
        with open(self.notes_file, 'r') as f:
            return json.load(f)

    def is_google_task_id(self, task_id):
        """
        Detect if task ID is from Google Tasks.
        Google Tasks IDs are base64-like strings (e.g., "bVdZZURmdjZmQ0ZwV2QyUg")
        Internal task IDs are UUIDs (e.g., "80ddcc31-8ec5-471a-b6da-414e314252cb")
        """
        # UUID format: 8-4-4-4-12 hex characters with dashes
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if re.match(uuid_pattern, task_id, re.IGNORECASE):
            return False

        # If it doesn't match UUID format and looks like base64, assume Google Tasks
        # Google Tasks IDs are typically 20-30 chars with mixed case and no dashes
        if len(task_id) > 15 and '-' not in task_id:
            return True

        return False

    def get_google_service(self):
        """Initialize Google Tasks service (lazy loading)"""
        if self.google_service is None:
            self.google_service = tasks_service()
        return self.google_service

    def find_google_task_list(self, task_id):
        """Find which Google Tasks list contains the task"""
        service = self.get_google_service()

        # Get all task lists
        task_lists_response = service.tasklists().list().execute()
        task_lists = task_lists_response.get('items', [])

        for task_list in task_lists:
            list_id = task_list['id']

            # Try to get the task from this list
            try:
                task = service.tasks().get(
                    tasklist=list_id,
                    task=task_id
                ).execute()

                if task:
                    return list_id, task_list['title']
            except Exception:
                # Task not in this list, continue
                continue

        return None, None

    def update_google_task(self, task_id, updates):
        """
        Update a Google Task with new information

        Args:
            task_id: Google Tasks ID
            updates: Dict with keys: 'notes', 'status', 'title'
        """
        service = self.get_google_service()

        # Find which list the task is in
        list_id, list_name = self.find_google_task_list(task_id)

        if not list_id:
            print(f"   ❌ Could not find Google Task with ID: {task_id}")
            return False

        print(f"   📋 Found task in list: {list_name}")

        # Get current task
        task = service.tasks().get(tasklist=list_id, task=task_id).execute()

        # Build update payload
        update_payload = {
            'id': task_id,
            'title': task.get('title'),
            'notes': task.get('notes', ''),
            'status': task.get('status')
        }

        # Apply updates
        if 'notes' in updates:
            # Append new note to existing notes
            existing_notes = task.get('notes', '')
            new_note = updates['notes']

            if existing_notes:
                # Add timestamp and separator
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                update_payload['notes'] = f"{existing_notes}\n\n---\n**Manual Note ({timestamp}):**\n{new_note}"
            else:
                update_payload['notes'] = new_note

        if 'status' in updates:
            update_payload['status'] = updates['status']

        if 'title' in updates:
            update_payload['title'] = updates['title']

        # Execute update
        try:
            service.tasks().update(
                tasklist=list_id,
                task=task_id,
                body=update_payload
            ).execute()

            print(f"   ✅ Updated Google Task: {task.get('title')}")
            return True

        except Exception as e:
            print(f"   ❌ Error updating Google Task: {e}")
            return False

    def process_notes(self):
        """Process all manual notes"""
        if not self.notes:
            print("\n📭 No manual notes to process.\n")
            return

        print(f"\n{'='*80}")
        print(f"PROCESSING {len(self.notes)} MANUAL TASK NOTE(S)")
        print(f"{'='*80}\n")

        results = []

        for i, note_data in enumerate(self.notes, 1):
            print(f"\n{'─'*80}")
            print(f"NOTE {i}/{len(self.notes)}")
            print(f"{'─'*80}\n")

            task_id = note_data['task_id']
            manual_note = note_data['manual_note']
            task_title = note_data['task_title']

            print(f"📋 Task: {task_title}")
            print(f"✍️  Note: \"{manual_note}\"")
            print(f"🔍 Task ID: {task_id}\n")

            # Detect task type
            is_google = self.is_google_task_id(task_id)

            if is_google:
                print(f"   🔷 Detected: Google Task")

                # Update Google Task with manual note
                success = self.update_google_task(task_id, {
                    'notes': f"**Manual Note:**\n{manual_note}"
                })

                if success:
                    results.append({
                        'task': task_title,
                        'type': 'google',
                        'action': 'Updated with manual note',
                        'success': True
                    })
                else:
                    results.append({
                        'task': task_title,
                        'type': 'google',
                        'action': 'Failed to update',
                        'success': False
                    })

            else:
                print(f"   🔶 Detected: Internal Task")
                print(f"   ⚠️  Internal task processing requires Claude's judgment")
                print(f"   💡 Claude should manually update: clients/{note_data['client']}/tasks.json")

                results.append({
                    'task': task_title,
                    'type': 'internal',
                    'action': 'Requires manual processing',
                    'success': None
                })

        # Summary
        print(f"\n{'='*80}")
        print(f"PROCESSING SUMMARY")
        print(f"{'='*80}\n")

        google_updated = len([r for r in results if r['type'] == 'google' and r['success']])
        google_failed = len([r for r in results if r['type'] == 'google' and not r['success']])
        internal_pending = len([r for r in results if r['type'] == 'internal'])

        print(f"✅ Google Tasks updated: {google_updated}")
        if google_failed > 0:
            print(f"❌ Google Tasks failed: {google_failed}")
        if internal_pending > 0:
            print(f"⏳ Internal tasks pending Claude's review: {internal_pending}")

        print(f"\n{'='*80}\n")

        return results

def main():
    processor = EnhancedTaskProcessor()
    processor.process_notes()

    # Ask if notes should be cleared
    print("To clear processed notes: echo '[]' > data/state/manual-task-notes.json")
    print("To regenerate HTML: python3 generate-tasks-overview.py\n")

if __name__ == "__main__":
    main()
