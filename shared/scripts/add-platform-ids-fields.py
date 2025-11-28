#!/usr/bin/env python3
"""
Add Microsoft Ads and Facebook Ads ID fields to all client CONTEXT.md files.

This script updates the Platform IDs section in each client's CONTEXT.md to include:
- Microsoft Ads Account ID
- Facebook Ads Account ID
"""

import re
from pathlib import Path

# Base paths
BASE_PATH = Path(__file__).parent.parent.parent
CLIENTS_PATH = BASE_PATH / "clients"

def update_context_file(context_path: Path) -> bool:
    """
    Add Microsoft Ads and Facebook Ads ID fields to a CONTEXT.md file.

    Returns True if file was updated, False if already had the fields or couldn't update.
    """
    if not context_path.exists():
        return False

    content = context_path.read_text()

    # Check if already has Microsoft Ads or Facebook Ads fields
    if 'Microsoft Ads Account ID' in content or 'Facebook Ads Account ID' in content:
        print(f"  ✓ Already has new fields: {context_path.parent.name}")
        return False

    # Find Platform IDs section
    platform_section_match = re.search(
        r'(\*\*Platform IDs\*\*:.*?)(?=\n\n|\n\*\*[A-Z]|\Z)',
        content,
        re.DOTALL
    )

    if not platform_section_match:
        print(f"  ✗ No Platform IDs section found: {context_path.parent.name}")
        return False

    old_section = platform_section_match.group(1)

    # Add new fields at the end of Platform IDs section
    # Find the last line with content (not empty line)
    lines = old_section.split('\n')

    # Insert new fields before any trailing empty lines
    new_fields = [
        "- **Microsoft Ads Account ID**: [TBD]",
        "- **Facebook Ads Account ID**: [TBD]"
    ]

    # Find where to insert (after last non-empty line)
    insert_index = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip():
            insert_index = i + 1
            break

    # Insert new fields
    for field in new_fields:
        lines.insert(insert_index, field)
        insert_index += 1

    new_section = '\n'.join(lines)

    # Replace old section with new section
    new_content = content.replace(old_section, new_section)

    # Write back to file
    context_path.write_text(new_content)
    print(f"  ✓ Updated: {context_path.parent.name}")
    return True

def main():
    """Update all client CONTEXT.md files."""
    print("Adding Microsoft Ads and Facebook Ads ID fields to client CONTEXT.md files...\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    # Process all client folders
    for client_dir in sorted(CLIENTS_PATH.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith(('_', '.')):
            continue

        context_path = client_dir / "CONTEXT.md"

        if not context_path.exists():
            print(f"  ⚠ No CONTEXT.md: {client_dir.name}")
            error_count += 1
            continue

        try:
            if update_context_file(context_path):
                updated_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"  ✗ Error updating {client_dir.name}: {e}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped (already had fields): {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
