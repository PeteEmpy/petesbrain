#!/usr/bin/env python3
"""
Wispr Flow Notes Importer

Extracts notes from Wispr Flow SQLite database and routes them to PetesBrain inbox.

Usage:
    python3 agents/wispr-flow-importer/wispr-flow-importer.py

Schedule:
    Run via LaunchAgent every hour or as needed
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

# Paths
PETESBRAIN_ROOT = Path(__file__).parent.parent.parent
WISPR_FLOW_DIR = Path.home() / "Library/Application Support/Wispr Flow"
WISPR_DB_PATH = WISPR_FLOW_DIR / "flow.sqlite"  # Use live database
INBOX_PATH = PETESBRAIN_ROOT / "!inbox"
STATE_FILE = PETESBRAIN_ROOT / "data/state/wispr-flow-state.json"

def get_database():
    """Get the Wispr Flow live database."""
    if not WISPR_DB_PATH.exists():
        print(f"❌ Wispr Flow database not found: {WISPR_DB_PATH}")
        print(f"   Is Wispr Flow installed?")
        return None

    print(f"✓ Using live database: {WISPR_DB_PATH.name}")
    return WISPR_DB_PATH

def load_state():
    """Load the last processed timestamp."""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            return state.get('last_processed_timestamp')
    return None

def save_state(timestamp):
    """Save the last processed timestamp."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump({
            'last_processed_timestamp': timestamp,
            'last_run': datetime.now().isoformat()
        }, f, indent=2)

def extract_notes(db_path, since_timestamp=None):
    """Extract notes from Wispr Flow database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query for notes
    if since_timestamp:
        # Get notes created or modified since last run
        query = """
            SELECT id, title, content, createdAt, modifiedAt, isDeleted
            FROM Notes
            WHERE isDeleted = 0
              AND (createdAt >= ? OR modifiedAt >= ?)
            ORDER BY createdAt ASC
        """
        cursor.execute(query, (since_timestamp, since_timestamp))
    else:
        # First run - get recent notes (last 7 days)
        query = """
            SELECT id, title, content, createdAt, modifiedAt, isDeleted
            FROM Notes
            WHERE isDeleted = 0
              AND datetime(createdAt) > datetime('now', '-7 days')
            ORDER BY createdAt ASC
        """
        cursor.execute(query)

    notes = cursor.fetchall()
    conn.close()

    return notes

def sanitize_filename(text):
    """Create a safe filename from text."""
    # Take first 50 chars of title/content
    text = text[:50].strip()
    # Replace invalid chars
    safe = "".join(c if c.isalnum() or c in (' ', '-', '_') else '-' for c in text)
    # Collapse multiple dashes
    safe = '-'.join(filter(None, safe.split('-')))
    return safe.lower()


def normalize_content_for_dedup(content):
    """Normalize note content for duplicate detection."""
    import re
    # Lowercase and strip
    content = content.lower().strip()
    # Remove common prefixes/markers
    content = re.sub(r'^(quick\s*note[:\s]*)', '', content)
    # Remove punctuation
    content = re.sub(r'[^\w\s]', ' ', content)
    # Collapse whitespace
    content = ' '.join(content.split())
    return content.strip()


def is_duplicate_note(note_content, note_id):
    """
    Check if a similar note already exists in inbox or has been processed.
    Also checks existing tasks to prevent creating duplicate tasks.

    Returns: (is_duplicate, reason)
    """
    import difflib

    normalized_new = normalize_content_for_dedup(note_content)

    # Check existing inbox files
    for inbox_file in INBOX_PATH.glob('*.md'):
        if inbox_file.name == 'README.md':
            continue
        try:
            with open(inbox_file, 'r') as f:
                existing_content = f.read()

            # Check if same note ID already imported
            if note_id and f"Note ID: {note_id}" in existing_content:
                return True, f"Same note ID already in inbox: {inbox_file.name}"

            # Normalize and compare content
            normalized_existing = normalize_content_for_dedup(existing_content)
            ratio = difflib.SequenceMatcher(None, normalized_new, normalized_existing).ratio()
            if ratio > 0.85:
                return True, f"Similar content in inbox ({ratio:.0%}): {inbox_file.name}"

        except Exception:
            continue

    # Check processed files (to prevent re-importing old notes)
    processed_dir = INBOX_PATH / 'processed'
    if processed_dir.exists():
        for processed_file in processed_dir.glob('*.md'):
            try:
                with open(processed_file, 'r') as f:
                    existing_content = f.read()

                # Check if same note ID
                if note_id and f"Note ID: {note_id}" in existing_content:
                    return True, f"Note ID already processed: {processed_file.name}"

            except Exception:
                continue

    return False, None

def save_to_inbox(note):
    """Save a Wispr Flow note to the inbox."""
    note_id, title, content, created_at, modified_at, is_deleted = note

    # Check for duplicates FIRST
    is_dup, reason = is_duplicate_note(content, note_id)
    if is_dup:
        print(f"⏭️  Skipping duplicate: {reason}")
        return None  # Return None to indicate skipped

    # Parse timestamp
    try:
        created_dt = datetime.fromisoformat(created_at.replace(' +00:00', ''))
        timestamp = created_dt.strftime('%Y%m%d-%H%M%S')
    except:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    # Generate filename
    if title:
        base_name = sanitize_filename(title)
    else:
        base_name = sanitize_filename(content)

    filename = f"{timestamp}-wispr-{base_name}.md"
    filepath = INBOX_PATH / filename

    # Avoid filename collisions (different from content duplicates)
    counter = 1
    while filepath.exists():
        filename = f"{timestamp}-wispr-{base_name}-{counter}.md"
        filepath = INBOX_PATH / filename
        counter += 1

    # Format content
    markdown_content = f"""# {title if title else 'Wispr Flow Note'}

{content}

---
*Source: Wispr Flow*
*Created: {created_at}*
*Note ID: {note_id}*
"""

    # Write to inbox
    with open(filepath, 'w') as f:
        f.write(markdown_content)

    print(f"✓ Saved: {filename}")
    return filepath

def main():
    """Main importer logic."""
    print("\n" + "="*60)
    print("Wispr Flow Notes Importer")
    print("="*60 + "\n")

    # Get database
    db_path = get_database()
    if not db_path:
        print("❌ Could not find Wispr Flow database")
        return

    # Load last processed timestamp
    last_timestamp = load_state()
    if last_timestamp:
        print(f"✓ Last processed: {last_timestamp}")
    else:
        print("✓ First run - will import notes from last 7 days")

    # Extract notes
    notes = extract_notes(db_path, last_timestamp)

    if not notes:
        print("\n✓ No new notes to import")
        return

    print(f"\n✓ Found {len(notes)} new note(s)\n")

    # Process each note
    imported_count = 0
    skipped_count = 0
    latest_timestamp = last_timestamp

    for note in notes:
        note_id, title, content, created_at, modified_at, is_deleted = note

        try:
            # Save to inbox (returns None if duplicate)
            result = save_to_inbox(note)
            if result is None:
                skipped_count += 1
            else:
                imported_count += 1

            # Track latest timestamp regardless (so we don't re-check old notes)
            for timestamp in [created_at, modified_at]:
                if not latest_timestamp or timestamp > latest_timestamp:
                    latest_timestamp = timestamp

        except Exception as e:
            print(f"❌ Error processing note {note_id}: {e}")

    # Save state
    if latest_timestamp:
        save_state(latest_timestamp)

    print(f"\n" + "="*60)
    print(f"✓ Imported {imported_count} note(s) to inbox")
    if skipped_count > 0:
        print(f"⏭️  Skipped {skipped_count} duplicate note(s)")
    print("="*60 + "\n")

    if imported_count > 0:
        print("Next steps:")
        print("  1. Review notes in !inbox/")
        print("  2. Add routing keywords (client:, task:, knowledge:)")
        print("  3. Run inbox processor or wait for daily run")
        print(f"\nManual processing: python3 agents/system/inbox-processor.py\n")

if __name__ == "__main__":
    main()
