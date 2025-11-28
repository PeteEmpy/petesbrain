#!/usr/bin/env python3
"""
Shared Drives Monitor - WORKING VERSION

Scans "Shared with Me" Google Drive for client-related documents.
Updates client CONTEXT.md files with new findings.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
CLIENTS_DIR = Path("/Users/administrator/Documents/PetesBrain/clients")
STATE_FILE = Path("/Users/administrator/Documents/PetesBrain/data/state/shared-drives-state.json")
LOG_FILE = Path.home() / ".petesbrain-shared-drives.log"

# Categorization keywords for shared files
# Files can match to: clients, roksys (knowledge base), or personal

CLIENT_KEYWORDS = {
    # Client-specific
    "devonshire-hotels": ["devonshire", "dev |", "daba", "cavendish", "beeley", "pilsley", "fell", "hide", "highwayman"],
    "smythson": ["smythson", "smy |"],
    "clear-prospects": ["clear prospects", "clearprospects", "cp |"],
    "tree2mydoor": ["tree2mydoor", "tree 2 my door", "t2md"],
    "superspace": ["superspace"],
    "uno-lighting": ["uno lighting", "uno-lighting"],
    "national-design-academy": ["nda", "national design academy"],
    "godshot": ["godshot"],
    "print-my-pdf": ["print my pdf", "printmypdf", "pmypdf"],
    "bright-minds": ["bright minds"],
    "otc": ["otc", "online tech club"],
    "accessories-for-the-home": ["afh", "accessories for the home"],
    "crowd-control": ["crowd control"],
    "go-glean": ["go glean", "go-glean"],
    "grain-guard": ["grain guard", "grain-guard"],
    "just-bin-bags": ["just bin bags", "jbb"],
}

# Roksys knowledge base keywords (industry insights, platform updates, best practices)
ROKSYS_KEYWORDS = [
    "google ads", "ppc", "performance max", "pmax", "shopping campaigns",
    "smart bidding", "troas", "roas", "conversion tracking",
    "google analytics", "ga4", "gtm", "google tag manager",
    "seo", "search engine", "adwords", "merchant center",
    "facebook ads", "meta ads", "social advertising",
    "digital marketing", "paid search", "sem",
    "ai in marketing", "automation", "machine learning",
    "industry insights", "platform updates", "best practices",
    "rok", "roksys", "methodology", "strategy", "playbook"
]

# Personal knowledge keywords (your own learning, notes, strategies)
PERSONAL_KEYWORDS = [
    "peter empson", "petere", "personal", "notes to self",
    "learning", "training", "course", "tutorial",
    "book", "reading", "research", "ideas"
]

# Document types to include (exclude images)
INCLUDE_TYPES = [
    "application/vnd.google-apps.document",      # Google Docs
    "application/vnd.google-apps.spreadsheet",   # Google Sheets
    "application/vnd.google-apps.presentation",  # Google Slides
    "application/pdf",
]


def log(message, level="INFO"):
    """Write to log file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    print(log_message)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_message + "\n")


def load_state():
    """Load previous scan state"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "last_scan": None,
        "recent_updates": {},  # client: [files] for weekly email
        "all_tracked_files": {}  # file_id: metadata for deduplication
    }


def save_state(state):
    """Save scan state"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def is_document(mime_type):
    """Check if file is a document type we want"""
    return mime_type in INCLUDE_TYPES


def categorize_file(file_name, owner_email=""):
    """
    Categorize file into: client, roksys, personal, or unknown
    Returns tuple: (category_type, category_name)

    Examples:
    - ("client", "devonshire-hotels")
    - ("roksys", "knowledge-base")
    - ("personal", "personal")
    - (None, None) if no match
    """
    name_lower = file_name.lower()
    owner_lower = owner_email.lower() if owner_email else ""

    # Priority 1: Check for client match (most specific)
    for client_folder, keywords in CLIENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in name_lower or keyword.lower() in owner_lower:
                return ("client", client_folder)

    # Priority 2: Check for Roksys/industry knowledge
    for keyword in ROKSYS_KEYWORDS:
        if keyword.lower() in name_lower:
            return ("roksys", "knowledge-base")

    # Priority 3: Check for personal knowledge
    for keyword in PERSONAL_KEYWORDS:
        if keyword.lower() in name_lower or keyword.lower() in owner_lower:
            return ("personal", "personal")

    # No match
    return (None, None)


def format_file_entry(file_info):
    """Format a file entry for CONTEXT.md"""
    name = file_info.get('name', 'Unknown')
    file_type = file_info.get('type', '')
    modified = file_info.get('modified', 'Unknown')
    url = file_info.get('url', '#')

    # Icon based on type
    if 'spreadsheet' in file_type:
        icon = '📊'
        type_name = 'Google Sheets'
    elif 'document' in file_type:
        icon = '📄'
        type_name = 'Google Docs'
    elif 'presentation' in file_type:
        icon = '📊'
        type_name = 'Google Slides'
    elif 'pdf' in file_type:
        icon = '📑'
        type_name = 'PDF'
    else:
        icon = '📁'
        type_name = 'Document'

    return f"- {icon} **[{name}]({url})** ({type_name})\n  - Last modified: {modified}\n"


def update_client_context(client_folder, new_files, all_files):
    """Update client CONTEXT.md with shared files"""
    context_file = CLIENTS_DIR / client_folder / "CONTEXT.md"

    if not context_file.exists():
        log(f"No CONTEXT.md found for {client_folder}", "WARNING")
        return

    # Read current content
    with open(context_file, "r") as f:
        content = f.read()

    # Find the Shared Drive Resources section
    section_start = content.find("## Shared Drive Resources")

    if section_start == -1:
        log(f"No Shared Drive Resources section in {client_folder}/CONTEXT.md", "WARNING")
        return

    # Find the next section (Document History or end of file)
    next_section_pattern = r'\n##\s+(?!Shared Drive Resources)'
    match = re.search(next_section_pattern, content[section_start:])

    if match:
        section_end = section_start + match.start()
        before_section = content[:section_start]
        after_section = content[section_end:]
    else:
        # Section goes to end of file
        section_end = len(content)
        before_section = content[:section_start]
        after_section = ""

    # Build new section content
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    new_section = f"## Shared Drive Resources\n\n**Last Scanned:** {now}\n\n"

    if all_files:
        new_section += "### Key Shared Documents\n\n"

        # Group files by type
        docs = [f for f in all_files if 'document' in f.get('type', '')]
        sheets = [f for f in all_files if 'spreadsheet' in f.get('type', '')]
        slides = [f for f in all_files if 'presentation' in f.get('type', '')]
        pdfs = [f for f in all_files if 'pdf' in f.get('type', '')]

        if slides:
            new_section += "**Presentations:**\n"
            for file_info in slides:
                new_section += format_file_entry(file_info)
            new_section += "\n"

        if sheets:
            new_section += "**Spreadsheets:**\n"
            for file_info in sheets:
                new_section += format_file_entry(file_info)
            new_section += "\n"

        if docs:
            new_section += "**Documents:**\n"
            for file_info in docs:
                new_section += format_file_entry(file_info)
            new_section += "\n"

        if pdfs:
            new_section += "**PDFs:**\n"
            for file_info in pdfs:
                new_section += format_file_entry(file_info)
            new_section += "\n"

        if new_files:
            new_section += f"_({len(new_files)} new/updated in last 7 days)_\n\n"
    else:
        new_section += "_Automatic monitoring via \"Shared with Me\" in Google Drive_\n"
        new_section += "_Updated documents will appear here when detected by daily scans_\n\n"

    # Reconstruct file
    new_content = before_section + new_section + after_section

    # Write back
    with open(context_file, "w") as f:
        f.write(new_content)

    log(f"✓ Updated {client_folder}/CONTEXT.md ({len(all_files)} total files, {len(new_files)} new)")


# NOTE: This script is designed to be called BY Claude Code using MCP tools
# It does not directly call Google Drive API - instead Claude Code will:
# 1. Use mcp__google-drive__search to find shared files
# 2. Filter and match to clients
# 3. Call this script's functions to update CONTEXT.md files

def main():
    """
    This script should be CALLED by Claude Code with file data.
    It does NOT directly access Google Drive API.

    Usage pattern:
    1. Claude Code uses mcp__google-drive__search to get shared files
    2. Claude Code filters and matches to clients
    3. Claude Code calls update_client_context() for each client
    """

    log("=" * 60)
    log("SHARED DRIVES MONITOR")
    log("=" * 60)
    log("This script should be called by Claude Code with file data")
    log("For manual scanning, use Claude Code directly with:")
    log("  'Scan shared drives and update client CONTEXT files'")
    log("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
