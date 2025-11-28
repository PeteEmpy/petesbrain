#!/usr/bin/env python3
"""
Meeting Importer

Main script for importing Granola meeting notes into client folders.

Usage with venv:
    source venv/bin/activate
    python3 import_meeting.py [options]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import yaml

from granola_api import GranolaAPI
from prosemirror_converter import ProseMirrorConverter, extract_transcript, fetch_external_content, fetch_granola_notes
from client_detector import ClientDetector

# Email reporter (optional)
try:
    from email_reporter import EmailReporter
    EMAIL_AVAILABLE = True
except:
    EMAIL_AVAILABLE = False


class MeetingImporter:
    """Handles importing meetings from Granola to client folders."""

    def __init__(self, clients_dir: Optional[Path] = None, enable_email: bool = True):
        """
        Initialize importer.

        Args:
            clients_dir: Path to clients directory (defaults to ../../clients)
            enable_email: Whether to send email alerts (requires config.yaml)
        """
        self.tool_dir = Path(__file__).parent
        if clients_dir is None:
            self.clients_dir = self.tool_dir.parent.parent / "clients"
        else:
            self.clients_dir = Path(clients_dir)

        self.api = GranolaAPI()
        self.converter = ProseMirrorConverter()
        self.detector = ClientDetector(self.clients_dir)
        self.history_file = self.tool_dir / ".import_history.json"
        self.history = self._load_history()

        # Initialize email reporter if available and enabled
        self.email_reporter = None
        if enable_email and EMAIL_AVAILABLE:
            try:
                self.email_reporter = EmailReporter()
            except (FileNotFoundError, ValueError):
                # Config not found or email disabled - continue without email
                pass

    def _load_history(self) -> Dict:
        """Load import history to track which meetings have been imported."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {"imported": {}}

    def _save_history(self):
        """Save import history."""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def _is_imported(self, document_id: str) -> bool:
        """Check if a document has already been imported."""
        return document_id in self.history["imported"]

    def _mark_imported(self, document_id: str, file_path: str, client_slug: Optional[str]):
        """Mark a document as imported."""
        self.history["imported"][document_id] = {
            "file_path": file_path,
            "client": client_slug,
            "imported_at": datetime.now().isoformat()
        }
        self._save_history()

    def _extract_metadata(self, document: Dict) -> Dict:
        """
        Extract metadata from a Granola document.

        Args:
            document: Granola document dictionary

        Returns:
            Metadata dictionary
        """
        metadata = {
            "granola_id": document.get("id"),
            "title": document.get("title", "Untitled Meeting"),
            "date": None,
            "time": None,
            "duration": None,
            "participants": [],
            "imported_at": datetime.now().isoformat()
        }

        # Parse created_at timestamp
        created_at = document.get("created_at")
        if created_at:
            try:
                dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                metadata["date"] = dt.strftime("%Y-%m-%d")
                metadata["time"] = dt.strftime("%H:%M")
            except ValueError:
                pass

        # Extract participants if available
        participants = document.get("participants", [])
        if isinstance(participants, list):
            metadata["participants"] = participants

        # Extract duration if available
        duration = document.get("duration")
        if duration:
            metadata["duration"] = duration

        return metadata

    def _generate_filename(self, metadata: Dict, client_slug: Optional[str]) -> str:
        """
        Generate filename for meeting notes.

        Args:
            metadata: Meeting metadata
            client_slug: Client slug (or None)

        Returns:
            Filename string
        """
        date = metadata.get("date", datetime.now().strftime("%Y-%m-%d"))
        title = metadata.get("title", "meeting")

        # Slugify title (lowercase, replace spaces with hyphens)
        title_slug = title.lower()
        title_slug = "".join(c if c.isalnum() or c in " -" else "" for c in title_slug)
        title_slug = "-".join(title_slug.split())[:50]  # Max 50 chars

        if client_slug:
            return f"{date}-{title_slug}-{client_slug}.md"
        else:
            return f"{date}-{title_slug}.md"

    def _create_markdown_file(self, document: Dict, client_slug: Optional[str],
                             output_dir: Path) -> str:
        """
        Create markdown file from Granola document.

        Args:
            document: Granola document
            client_slug: Client slug (or None for unassigned)
            output_dir: Directory to save file

        Returns:
            Path to created file
        """
        # Extract metadata
        metadata = self._extract_metadata(document)
        metadata["client"] = client_slug

        # Fetch Granola AI-generated notes from notes.granola.ai
        document_id = document.get("id")
        granola_notes = None
        if document_id:
            print(f"   📥 Fetching Granola AI notes...")
            granola_notes = fetch_granola_notes(document_id)
            if granola_notes:
                print(f"   ✓ Fetched {len(granola_notes)} characters of AI notes")

        # Convert basic notes (what you typed during meeting)
        notes_content = document.get("notes", {})
        ai_notes = self.converter.convert(notes_content)

        # Extract transcript
        transcript = extract_transcript(document)

        # Check for external content (notes_markdown URL - user-uploaded files)
        external_content = None
        notes_markdown_url = document.get("notes_markdown")
        if notes_markdown_url and isinstance(notes_markdown_url, str) and notes_markdown_url.startswith("http"):
            # Only fetch if it's different from Granola notes
            print(f"   📎 Fetching linked document...")
            external_content = fetch_external_content(notes_markdown_url)
            if external_content:
                print(f"   ✓ Fetched {len(external_content)} characters from linked document")

        # Generate filename
        filename = self._generate_filename(metadata, client_slug)
        file_path = output_dir / filename

        # Build markdown content
        content_parts = []

        # YAML frontmatter
        content_parts.append("---")
        content_parts.append(yaml.dump(metadata, default_flow_style=False, sort_keys=False).strip())
        content_parts.append("---")
        content_parts.append("")

        # Meeting title
        content_parts.append(f"# {metadata['title']}")
        content_parts.append("")

        # Granola AI-generated notes (main content)
        if granola_notes:
            content_parts.append(granola_notes)
            content_parts.append("")

        # Manual notes (what you typed during meeting)
        if ai_notes and ai_notes.strip() != granola_notes:
            content_parts.append("---")
            content_parts.append("")
            content_parts.append("## Manual Notes")
            content_parts.append("")
            content_parts.append(ai_notes)
            content_parts.append("")

        # External linked documents (from notes_markdown URL)
        if external_content:
            content_parts.append("---")
            content_parts.append("")
            content_parts.append("## Linked Document")
            content_parts.append("")
            content_parts.append(external_content)
            content_parts.append("")

        # Full transcript
        if transcript:
            content_parts.append("---")
            content_parts.append("")
            content_parts.append("## Full Transcript")
            content_parts.append("")
            content_parts.append(transcript)
            content_parts.append("")

        # Write file
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content_parts))

        return str(file_path)

    def import_document(self, document: Dict, skip_duplicates: bool = True) -> Optional[str]:
        """
        Import a single Granola document.

        Args:
            document: Granola document dictionary
            skip_duplicates: Skip if already imported

        Returns:
            Path to created file or None if skipped
        """
        document_id = document.get("id")
        title = document.get("title", "Untitled")

        # Check if already imported
        if skip_duplicates and self._is_imported(document_id):
            print(f"⊘ Skipping '{title}' (already imported)")
            return None

        print(f"\n📄 Processing: '{title}'")

        # Convert to get content for detection
        notes_content = document.get("notes", {})
        ai_notes = self.converter.convert(notes_content)
        transcript = extract_transcript(document)
        full_content = f"{ai_notes}\n\n{transcript or ''}"

        # Extract attendee emails from Granola document
        attendee_emails = []
        people = document.get("people", {})
        if isinstance(people, dict):
            attendees = people.get("attendees", [])
            for attendee in attendees:
                if isinstance(attendee, dict):
                    email = attendee.get("email")
                    if email:
                        attendee_emails.append(email)

        # Detect client (prioritizes email domains!)
        client_slug, confidence, method = self.detector.detect_with_confidence(
            title,
            meeting_content=full_content if full_content.strip() else None,
            attendee_emails=attendee_emails if attendee_emails else None
        )

        if client_slug:
            client_display = self.detector.get_client_display_name(client_slug)
            print(f"   ✓ Detected client: {client_display} ({confidence}% via {method})")
            output_dir = self.clients_dir / client_slug / "meeting-notes"
        else:
            print(f"   ⚠ No client detected - saving to _unassigned")
            output_dir = self.clients_dir / "_unassigned" / "meeting-notes"
            client_slug = None

        # Create markdown file
        file_path = self._create_markdown_file(document, client_slug, output_dir)
        print(f"   ✓ Saved to: {file_path}")

        # Mark as imported
        self._mark_imported(document_id, file_path, client_slug)

        # Send email alert if meeting is unassigned
        if not client_slug and self.email_reporter:
            try:
                self.email_reporter.send_unassigned_alert(title, file_path)
            except Exception as e:
                # Don't fail import if email fails
                print(f"   ⚠ Could not send email alert: {e}")

        return file_path

    def import_by_id(self, document_id: str) -> Optional[str]:
        """
        Import a specific meeting by Granola document ID.

        Args:
            document_id: Granola document ID

        Returns:
            Path to created file or None if not found
        """
        document = self.api.get_document_by_id(document_id)
        if not document:
            print(f"✗ Document '{document_id}' not found")
            return None

        return self.import_document(document)

    def import_recent(self, days: int = 7, limit: Optional[int] = None) -> int:
        """
        Import recent meetings from the last N days.

        Args:
            days: Number of days to look back
            limit: Maximum number of meetings to import

        Returns:
            Number of meetings imported
        """
        print(f"\n🔍 Fetching meetings from last {days} days...")
        documents = self.api.get_recent_documents(days=days)

        if limit:
            documents = documents[:limit]

        print(f"   Found {len(documents)} meetings")

        imported_count = 0
        for document in documents:
            result = self.import_document(document)
            if result:
                imported_count += 1

        return imported_count

    def import_all_new(self, limit: int = 100) -> int:
        """
        Import all new (not yet imported) meetings.

        Args:
            limit: Maximum number of meetings to fetch

        Returns:
            Number of meetings imported
        """
        print(f"\n🔍 Fetching up to {limit} meetings...")
        documents = self.api.get_documents(limit=limit)
        print(f"   Found {len(documents)} total meetings")

        imported_count = 0
        for document in documents:
            result = self.import_document(document)
            if result:
                imported_count += 1

        return imported_count


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Import Granola meeting notes into client folders"
    )

    parser.add_argument(
        "--meeting-id",
        help="Import a specific meeting by Granola document ID"
    )

    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Import meetings from last N days (default: 7)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of meetings to import"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Import all new meetings (not yet imported)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-import meetings even if already imported"
    )

    args = parser.parse_args()

    try:
        importer = MeetingImporter()

        if args.meeting_id:
            # Import specific meeting
            importer.import_by_id(args.meeting_id)

        elif args.all:
            # Import all new meetings
            count = importer.import_all_new(limit=args.limit or 100)
            print(f"\n✓ Imported {count} new meetings")

        else:
            # Import recent meetings
            count = importer.import_recent(days=args.days, limit=args.limit)
            print(f"\n✓ Imported {count} meetings from last {args.days} days")

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease ensure Granola desktop app is installed and you're logged in.")
        sys.exit(1)

    except PermissionError as e:
        print(f"\n✗ Error: {e}")
        print("\nTry logging out and back into Granola app.")
        sys.exit(1)

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
