#!/usr/bin/env python3
"""
Shared Drives Monitor - Client Document Scanner

Scans "Shared with Me" Google Drive for client-related documents.
Filters out images, focuses on documents, spreadsheets, and presentations.
Updates client CONTEXT.md files with new findings.

Usage:
  - Automated: Runs daily via LaunchAgent
  - Manual: python3 shared-drives-monitor.py [--client CLIENT_NAME] [--days DAYS]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Add Google Drive MCP path
sys.path.insert(0, str(Path(__file__).parent.parent / "infrastructure" / "mcp-servers" / "google-drive-mcp-server"))

# Configuration
CLIENTS_DIR = Path("/Users/administrator/Documents/PetesBrain/clients")
STATE_FILE = Path("/Users/administrator/Documents/PetesBrain/data/state/shared-drives-state.json")
LOG_FILE = Path.home() / ".petesbrain-shared-drives.log"

# Client name variations to match against
CLIENT_KEYWORDS = {
    "devonshire-hotels": ["devonshire", "dev |", "daba", "cavendish", "beeley", "pilsley", "fell", "hide", "highwayman"],
    "smythson": ["smythson", "smy |"],
    "clear-prospects": ["clear prospects", "clearprospects"],
    "tree2mydoor": ["tree2mydoor", "tree 2 my door", "t2md"],
    "superspace": ["superspace"],
    "uno-lighting": ["uno lighting", "uno-lighting"],
    "national-design-academy": ["nda", "national design academy"],
    "godshot": ["godshot"],
    "print-my-pdf": ["print my pdf", "printmypdf", "pmypdf"],
    "bright-minds": ["bright minds"],
    "otc": ["otc", "online tech club"],
}

# Document types to include (exclude images)
INCLUDE_TYPES = [
    "application/vnd.google-apps.document",      # Google Docs
    "application/vnd.google-apps.spreadsheet",   # Google Sheets
    "application/vnd.google-apps.presentation",  # Google Slides
    "application/pdf",                            # PDFs
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # Word
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",        # Excel
    "application/vnd.openxmlformats-officedocument.presentationml.presentation", # PowerPoint
]

EXCLUDE_KEYWORDS = [
    ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",  # Images
    "image", "photo", "picture", "screenshot",
]


def log(message, level="INFO"):
    """Write to log file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    print(log_message)

    with open(LOG_FILE, "a") as f:
        f.write(log_message + "\n")


def load_state():
    """Load previous scan state"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_scan": None, "processed_files": []}


def save_state(state):
    """Save scan state"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def is_document(file_name, mime_type):
    """Check if file is a document (not an image)"""
    # Check mime type
    if mime_type not in INCLUDE_TYPES:
        return False

    # Check file name doesn't contain image keywords
    name_lower = file_name.lower()
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in name_lower:
            return False

    return True


def match_client(file_name, owner_email=""):
    """Match file to client based on name/keywords"""
    name_lower = file_name.lower()
    owner_lower = owner_email.lower() if owner_email else ""

    for client_folder, keywords in CLIENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in name_lower or keyword.lower() in owner_lower:
                return client_folder

    return None


def search_shared_files(days=7):
    """Search for files shared with me, modified in last N days"""
    log(f"Searching for files modified in last {days} days...")

    # Use MCP Google Drive listFolder to get shared files
    # Note: This requires the Google Drive MCP server to be configured
    try:
        import subprocess

        # Calculate date threshold
        threshold_date = datetime.now() - timedelta(days=days)

        # This would use the MCP tool - for now using API approach
        # In production, this should call mcp__google-drive__search
        log("Note: Google Drive MCP integration required - returning empty for now")
        return []

    except Exception as e:
        log(f"Error searching shared files: {e}", "ERROR")
        return []


def update_client_context(client_folder, new_files):
    """Update client CONTEXT.md with new shared files"""
    context_file = CLIENTS_DIR / client_folder / "CONTEXT.md"

    if not context_file.exists():
        log(f"No CONTEXT.md found for {client_folder}", "WARNING")
        return

    # Read current context
    with open(context_file, "r") as f:
        content = f.read()

    # Find or create Shared Drive Resources section
    section_marker = "### Shared Drive Resources"

    if section_marker not in content:
        # Add new section before Quick Reference
        quick_ref_marker = "## Quick Reference"
        if quick_ref_marker in content:
            insert_pos = content.find(quick_ref_marker)
            new_section = f"\n---\n\n## Shared Drive Resources\n\n{section_marker}\n\n**Last Scanned:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            content = content[:insert_pos] + new_section + content[insert_pos:]
        else:
            # Add at end
            content += f"\n\n---\n\n## Shared Drive Resources\n\n{section_marker}\n\n**Last Scanned:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    # Add new files to the section
    # TODO: Implement file listing format

    # Write back
    with open(context_file, "w") as f:
        f.write(content)

    log(f"Updated CONTEXT.md for {client_folder}")


def generate_summary_email(findings):
    """Generate email summary of new shared files"""
    # TODO: Integrate with weekly-meeting-review.py email system
    pass


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description="Monitor shared Google Drive for client documents")
    parser.add_argument("--client", help="Specific client to scan for")
    parser.add_argument("--days", type=int, default=7, help="Days to look back (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Don't update files, just report")

    args = parser.parse_args()

    log("=" * 60)
    log("SHARED DRIVES MONITOR - STARTING")
    log("=" * 60)

    # Load previous state
    state = load_state()
    log(f"Last scan: {state.get('last_scan', 'Never')}")

    # Search for shared files
    # NOTE: This needs to be implemented using Google Drive MCP
    # For now, this is a skeleton

    log("Searching shared drives...")
    shared_files = search_shared_files(days=args.days)

    log(f"Found {len(shared_files)} files")

    # Group by client
    client_files = {}
    for file in shared_files:
        client = match_client(file.get("name", ""), file.get("owner", ""))
        if client:
            if client not in client_files:
                client_files[client] = []
            client_files[client].append(file)

    log(f"Matched files to {len(client_files)} clients")

    # Update each client's CONTEXT.md
    if not args.dry_run:
        for client, files in client_files.items():
            if args.client and client != args.client:
                continue

            log(f"Processing {len(files)} files for {client}")
            update_client_context(client, files)

    # Save state
    state["last_scan"] = datetime.now().isoformat()
    state["processed_files"].extend([f.get("id") for f in shared_files])
    save_state(state)

    log("=" * 60)
    log("SCAN COMPLETE")
    log("=" * 60)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log(f"FATAL ERROR: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)
