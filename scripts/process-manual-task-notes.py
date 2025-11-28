#!/usr/bin/env python3
"""
Process manual task notes and complete tasks
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.client_tasks_service import ClientTasksService

# Load manual notes
notes_file = Path('/Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json')
with open(notes_file, 'r') as f:
    manual_notes = json.load(f)

service = ClientTasksService()

for note in manual_notes:
    task_id = note['task_id']
    client = note['client']
    manual_note = note['manual_note']
    task_title = note['task_title']

    print(f"\n📝 Processing: {task_title}")
    print(f"   Client: {client}")
    print(f"   Note: {manual_note}")

    # Complete the task with the manual note
    service.complete_task(
        task_id=task_id,
        client=client,
        completion_notes=manual_note
    )

    print(f"   ✅ Task completed and logged to {client}/tasks-completed.md")

# Clear the manual notes file
with open(notes_file, 'w') as f:
    json.dump([], f, indent=2)

print(f"\n✅ Processed {len(manual_notes)} manual task notes")
print(f"✅ Cleared manual-task-notes.json")
