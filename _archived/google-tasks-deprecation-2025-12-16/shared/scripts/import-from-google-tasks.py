#!/usr/bin/env python3
"""
Import tasks from Google Tasks into per-client tasks.json structure.
"""

import sys
from pathlib import Path
import re

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from client_tasks_service import ClientTasksService


def extract_client_from_title(title: str) -> tuple[str, str]:
    """
    Extract client name from task title like '[Superspace] Task name'
    Returns: (client_slug, cleaned_title)
    """
    # Match [Client Name] at start of title
    match = re.match(r'^\[([^\]]+)\]\s*(.+)$', title)

    if match:
        client_name = match.group(1).strip()
        task_title = match.group(2).strip()

        # Convert client name to slug
        client_slug = client_name.lower().replace(' ', '-')

        # Handle common variations
        slug_map = {
            'accessories-for-the-home': 'accessories-for-the-home',
            'bright-minds': 'bright-minds',
            'clear-prospects': 'clear-prospects',
            'crowd-control': 'crowd-control',
            'devonshire-hotels': 'devonshire-hotels',
            'go-glean': 'go-glean',
            'godshot': 'godshot',
            'grain-guard': 'grain-guard',
            'just-bin-bags': 'just-bin-bags',
            'superspace': 'superspace',
            'tree2mydoor': 'tree2mydoor',
            'uno-lighting': 'uno-lighting',
            'national-motorsports-academy': 'national-motorsports-academy',
            'nma': 'national-motorsports-academy',
        }

        client_slug = slug_map.get(client_slug, client_slug)

        return (client_slug, f"[{client_name}] {task_title}")

    return (None, title)


def import_from_google_tasks():
    """Import all tasks from Google Tasks"""

    # Initialize service
    service = ClientTasksService()

    # Import MCP tools
    print("Importing tasks from Google Tasks...")

    # Note: You'll need to call the MCP tool from Claude Code directly
    # This script is meant to be run with the task data passed in

    print("\nThis script needs to be run from Claude Code with MCP access.")
    print("It will process the Google Tasks data structure.")


if __name__ == '__main__':
    import_from_google_tasks()
