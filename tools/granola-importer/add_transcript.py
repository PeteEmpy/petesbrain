#!/usr/bin/env python3
"""
Add Transcript to Meeting Notes

Quick script to manually add transcripts to meeting notes that were imported without them.

Usage:
    python3 add_transcript.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta


def find_meetings_without_transcripts(days=14):
    """Find recent meeting notes without transcripts."""
    meetings = []

    # Base paths
    base_path = Path(__file__).parent.parent.parent / "clients"
    cutoff_date = datetime.now() - timedelta(days=days)

    # Search all client folders for meeting notes
    for client_dir in base_path.iterdir():
        if not client_dir.is_dir() or client_dir.name.startswith('.'):
            continue

        meeting_notes_dir = client_dir / "meeting-notes"
        if not meeting_notes_dir.exists():
            continue

        # Check each meeting file
        for meeting_file in meeting_notes_dir.glob("*.md"):
            # Check if recent (based on filename date)
            try:
                date_str = meeting_file.stem[:10]  # YYYY-MM-DD
                meeting_date = datetime.strptime(date_str, "%Y-%m-%d")

                if meeting_date < cutoff_date:
                    continue
            except:
                continue

            # Check if it has a transcript
            with open(meeting_file, 'r') as f:
                content = f.read()

            if "## Full Transcript" not in content:
                meetings.append({
                    'path': meeting_file,
                    'date': date_str,
                    'client': client_dir.name,
                    'content': content
                })

    # Also check roksys folder
    roksys_dir = base_path.parent / "roksys" / "meeting-notes"
    if roksys_dir.exists():
        for meeting_file in roksys_dir.glob("*.md"):
            try:
                date_str = meeting_file.stem[:10]
                meeting_date = datetime.strptime(date_str, "%Y-%m-%d")

                if meeting_date < cutoff_date:
                    continue
            except:
                continue

            with open(meeting_file, 'r') as f:
                content = f.read()

            if "## Full Transcript" not in content:
                meetings.append({
                    'path': meeting_file,
                    'date': date_str,
                    'client': 'roksys',
                    'content': content
                })

    # Sort by date (newest first)
    meetings.sort(key=lambda x: x['date'], reverse=True)

    return meetings


def extract_title(content):
    """Extract meeting title from content."""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
        if line.startswith('title:'):
            return line.split(':', 1)[1].strip().strip('"\'')
    return "Unknown"


def add_transcript_to_file(file_path, transcript_text):
    """Add transcript section to meeting file."""
    with open(file_path, 'r') as f:
        content = f.read()

    # Add transcript section at the end
    transcript_section = f"\n\n---\n\n## Full Transcript\n\n{transcript_text}\n"

    # Write updated content
    with open(file_path, 'w') as f:
        f.write(content + transcript_section)

    print(f"\n✓ Transcript added successfully!")


def main():
    print("=" * 70)
    print("Add Transcript to Meeting Notes")
    print("=" * 70)
    print()

    # Find meetings without transcripts
    print("Searching for recent meetings without transcripts...")
    meetings = find_meetings_without_transcripts(days=14)

    if not meetings:
        print("\n✓ All recent meetings already have transcripts!")
        return

    print(f"\nFound {len(meetings)} meetings without transcripts:\n")

    # Display meetings
    for i, meeting in enumerate(meetings, 1):
        title = extract_title(meeting['content'])
        print(f"{i}. [{meeting['date']}] {title}")
        print(f"   Client: {meeting['client']}")
        print()

    # Let user select a meeting
    while True:
        try:
            selection = input("Select meeting number (or 'q' to quit): ").strip()

            if selection.lower() == 'q':
                print("\nCancelled.")
                return

            meeting_idx = int(selection) - 1

            if 0 <= meeting_idx < len(meetings):
                break
            else:
                print(f"Please enter a number between 1 and {len(meetings)}")
        except ValueError:
            print("Please enter a valid number or 'q' to quit")

    selected_meeting = meetings[meeting_idx]
    title = extract_title(selected_meeting['content'])

    print()
    print("=" * 70)
    print(f"Selected: {title}")
    print(f"Client: {selected_meeting['client']}")
    print(f"Date: {selected_meeting['date']}")
    print("=" * 70)
    print()
    print("Now:")
    print("1. Open this meeting in Granola desktop app")
    print("2. Click the up arrow (bottom left) to show transcript")
    print("3. Select all the transcript text (Cmd+A)")
    print("4. Copy it (Cmd+C)")
    print("5. Come back here")
    print()

    input("Press Enter when you've copied the transcript to clipboard...")

    print()
    print("Reading transcript from clipboard...")

    # Read directly from macOS clipboard (no paste buffer limit!)
    import subprocess
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True)
        transcript_text = result.stdout.strip()
    except Exception as e:
        print(f"\n✗ Error reading from clipboard: {e}")
        print("\nTrying alternative method...")
        print("Paste the transcript below and press Ctrl+D when done:")
        print("-" * 70)

        # Fallback to reading from stdin
        transcript_lines = []
        try:
            while True:
                line = input()
                transcript_lines.append(line)
        except EOFError:
            pass

        transcript_text = '\n'.join(transcript_lines).strip()

    if not transcript_text:
        print("\n✗ No transcript entered. Cancelled.")
        return

    print()
    print(f"Transcript length: {len(transcript_text)} characters")
    print()

    # Confirm
    confirm = input("Add this transcript to the meeting file? (y/n): ").strip().lower()

    if confirm != 'y':
        print("\nCancelled.")
        return

    # Add transcript
    add_transcript_to_file(selected_meeting['path'], transcript_text)
    print(f"File updated: {selected_meeting['path']}")
    print()
    print("Would you like to add another transcript? (y/n): ", end='')

    if input().strip().lower() == 'y':
        print()
        main()  # Recursive call to add another


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
