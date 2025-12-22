#!/usr/bin/env python3
"""Process manual task notes from the Task Manager UI."""

import sys
import json
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent / 'shared'))

from client_tasks_service import ClientTasksService

def main():
    # Read manual notes
    notes_file = Path('/Users/administrator/Documents/PetesBrain.nosync/data/state/manual-task-notes.json')

    with open(notes_file, 'r') as f:
        notes = json.load(f)

    if not notes:
        print("No task notes to process")
        return

    service = ClientTasksService()

    print(f"Processing {len(notes)} task note(s)...\n")

    for note in notes:
        task_id = note['task_id']
        client = note['client']
        manual_note = note['manual_note']
        task_title = note['task_title']

        print(f"Processing: {task_title}")
        print(f"  Client: {client}")
        print(f"  Note: {manual_note}")

        if manual_note.lower() in ['done', 'complete', 'finished', 'completed']:
            # Simple completion - complete the task
            try:
                service.complete_task(client=client, task_id=task_id)
                print(f"  ✅ Task completed and logged to {client}/tasks-completed.md\n")
            except Exception as e:
                print(f"  ❌ Error completing task: {e}\n")
        else:
            print(f"  ⚠️ Note is not a completion marker - would need manual handling\n")

    # Clear the notes file
    with open(notes_file, 'w') as f:
        json.dump([], f)

    print("✅ Manual notes file cleared")
    print("\nNext: Regenerating task overview HTML...")

if __name__ == '__main__':
    main()
