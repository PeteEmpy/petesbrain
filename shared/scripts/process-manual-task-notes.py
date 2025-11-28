#!/usr/bin/env python3
"""
Process Manual Task Notes - Intelligent Task Management
Processes manual notes added via tasks-overview.html interface.

This script analyzes notes and makes intelligent decisions:
- Completes tasks when appropriate
- Converts standalone → parent when follow-ups are needed
- Creates child tasks for follow-up work
- Expands notes with context
- Preserves task hierarchy

Usage:
    Called by Claude after user clicks "Save All Notes" in tasks-overview.html
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import re

class TaskProcessor:
    def __init__(self, notes_file):
        self.notes_file = Path(notes_file)
        self.notes = self.load_notes()
        self.changes = []

    def load_notes(self):
        """Load the manual notes from JSON file."""
        with open(self.notes_file, 'r') as f:
            return json.load(f)

    def load_task_file(self, client):
        """Load tasks.json for a client (main location only)."""
        task_file = Path(f'/Users/administrator/Documents/PetesBrain/clients/{client}/tasks.json')
        if not task_file.exists():
            return None, None
        with open(task_file, 'r') as f:
            return json.load(f), task_file

    def save_task_file(self, task_data, task_file):
        """Save updated tasks.json."""
        task_data['last_updated'] = datetime.now().isoformat()
        with open(task_file, 'w') as f:
            json.dump(task_data, f, indent=2, ensure_ascii=False)

    def find_task(self, task_data, task_id):
        """Find a task by ID."""
        for task in task_data['tasks']:
            if task['id'] == task_id:
                return task
        return None

    def analyze_note_for_completion(self, note_text):
        """
        Analyze note to determine if task is complete.
        Returns: (is_complete, confidence, reasoning)
        """
        note_lower = note_text.lower()

        # Strong completion signals
        strong_complete = [
            'done', 'completed', 'finished', 'implemented', 'added',
            'created', 'set up', 'sent', 'emailed', 'called'
        ]

        # Incomplete signals
        incomplete = [
            'started', 'working on', 'in progress', 'blocked',
            'waiting', 'need to', 'todo', 'partially'
        ]

        # Check for incomplete signals first
        for signal in incomplete:
            if signal in note_lower:
                return False, 0.9, f"Contains incomplete signal: '{signal}'"

        # Check for completion signals
        for signal in strong_complete:
            if signal in note_lower:
                return True, 0.8, f"Contains completion signal: '{signal}'"

        return False, 0.3, "Unclear - needs Claude's judgment"

    def extract_follow_up_timing(self, note_text):
        """
        Extract follow-up timing from note.
        Returns: (has_follow_up, timing_description, days)
        """
        note_lower = note_text.lower()

        # Look for review/revisit language
        follow_up_patterns = [
            (r'review in (\d+) days?', lambda m: int(m.group(1))),
            (r'revisit in (\d+) days?', lambda m: int(m.group(1))),
            (r'check back in (\d+) days?', lambda m: int(m.group(1))),
            (r'follow up in (\d+) days?', lambda m: int(m.group(1))),
            (r'in (\d+) days?', lambda m: int(m.group(1))),
            (r'next week', lambda m: 7),
            (r'next monday', lambda m: self.days_until_next_monday()),
            (r'weekly review', lambda m: 7),
            (r'monthly review', lambda m: 30),
        ]

        for pattern, days_func in follow_up_patterns:
            match = re.search(pattern, note_lower)
            if match:
                try:
                    days = days_func(match)
                    return True, match.group(0), days
                except:
                    continue

        # Check for general review language
        if any(word in note_lower for word in ['review', 'revisit', 'check', 'monitor', 'follow']):
            return True, "review needed (timing unclear)", 7  # Default 7 days

        return False, None, None

    def days_until_next_monday(self):
        """Calculate days until next Monday."""
        today = datetime.now().weekday()  # 0=Monday, 6=Sunday
        days = (7 - today) % 7
        return days if days > 0 else 7

    def present_for_analysis(self):
        """Present all notes for Claude to analyze."""
        print(f"\n{'='*80}")
        print(f"MANUAL TASK NOTES - READY FOR PROCESSING")
        print(f"{'='*80}\n")
        print(f"Found {len(self.notes)} notes to process.\n")

        for i, note_data in enumerate(self.notes, 1):
            print(f"\n{'─'*80}")
            print(f"NOTE {i}/{len(self.notes)}")
            print(f"{'─'*80}\n")

            # Task context
            print(f"📋 TASK CONTEXT:")
            print(f"   Client: {note_data['client']}")
            print(f"   Title: {note_data['task_title']}")
            print(f"   Type: {note_data['task_type']}")
            print(f"   Priority: {note_data['task_priority']}")
            print(f"   ID: {note_data['task_id']}\n")

            # Original notes (truncated)
            if note_data.get('task_notes'):
                notes_preview = note_data['task_notes'][:150]
                print(f"📄 ORIGINAL NOTES: {notes_preview}...\n")

            # User's manual note
            print(f"✍️  USER'S NOTE:")
            print(f"   \"{note_data['manual_note']}\"\n")

            # Automated analysis
            is_complete, confidence, reasoning = self.analyze_note_for_completion(note_data['manual_note'])
            has_follow_up, follow_timing, days = self.extract_follow_up_timing(note_data['manual_note'])

            print(f"🤖 AUTOMATED ANALYSIS:")
            print(f"   Complete? {is_complete} (confidence: {confidence:.0%})")
            print(f"   Reasoning: {reasoning}")
            if has_follow_up:
                print(f"   Follow-up detected: {follow_timing} ({days} days)")
            print()

            # Action recommendation
            print(f"💡 RECOMMENDED ACTIONS:")

            if is_complete and has_follow_up:
                if note_data['task_type'] == 'standalone':
                    print(f"   1. Convert to PARENT task (broader scope)")
                    print(f"   2. Create COMPLETED CHILD (the work just done)")
                    print(f"   3. Create FOLLOW-UP CHILD (review in {days} days)")
                elif note_data['task_type'] == 'child':
                    print(f"   1. Mark this child task as COMPLETED")
                    print(f"   2. Create SIBLING CHILD for follow-up")
                else:  # parent
                    print(f"   1. Update parent notes")
                    print(f"   2. Create new CHILD for follow-up")

            elif is_complete:
                print(f"   1. Mark task as COMPLETED")
                print(f"   2. Expand notes with details from manual note")

            elif has_follow_up:
                print(f"   1. Update notes with progress")
                print(f"   2. Create follow-up task for {days} days")

            else:
                print(f"   1. Append manual note to task notes")
                print(f"   2. Keep task active")

            print(f"\n🎯 CLAUDE: Please review and execute appropriate actions.")
            print(f"{'─'*80}\n")

def main():
    # Check for explicit path argument, otherwise default to Downloads
    if len(sys.argv) >= 2:
        notes_file = sys.argv[1]
    else:
        # Default to Downloads folder
        home = Path.home()
        notes_file = home / 'Downloads' / 'manual-task-notes.json'

        if not notes_file.exists():
            print("\n❌ No notes file found in Downloads folder.\n")
            print("Usage: python3 process-manual-task-notes.py <path-to-manual-task-notes.json>\n")
            print("Or click 'Process All Notes' button in tasks-overview.html\n")
            sys.exit(1)

    if not Path(notes_file).exists():
        print(f"\n❌ Error: File not found: {notes_file}\n")
        sys.exit(1)

    processor = TaskProcessor(notes_file)
    processor.present_for_analysis()

    print(f"\n{'='*80}")
    print(f"AWAITING CLAUDE'S PROCESSING")
    print(f"{'='*80}\n")
    print("Claude will now:")
    print("• Read each note with full context")
    print("• Make intelligent decisions about completion")
    print("• Convert standalone → parent when creating follow-ups")
    print("• Create child tasks with proper hierarchy")
    print("• Update all tasks.json files")
    print("• Provide a summary of all changes\n")

if __name__ == "__main__":
    main()
