#!/usr/bin/env python3
"""
Add ProcessType=Background to all PetesBrain LaunchAgent plists
This suppresses macOS background activity notifications
"""

import os
import glob
from pathlib import Path

def add_process_type(plist_path):
    """Add ProcessType key to a plist file if it doesn't exist"""
    with open(plist_path, 'r') as f:
        content = f.read()

    # Check if ProcessType already exists
    if '<key>ProcessType</key>' in content:
        print(f"✓ {os.path.basename(plist_path)} - already has ProcessType")
        return False

    # Find the closing </dict> before </plist>
    # Insert ProcessType before the final </dict>
    lines = content.split('\n')

    # Find the last </dict> line (before </plist>)
    insert_index = None
    for i in range(len(lines) - 1, -1, -1):
        if '</dict>' in lines[i]:
            insert_index = i
            break

    if insert_index is None:
        print(f"✗ {os.path.basename(plist_path)} - couldn't find </dict>")
        return False

    # Get the indentation from the </dict> line
    indent = lines[insert_index].replace('</dict>', '')

    # Insert ProcessType before </dict>
    process_type_lines = [
        '',
        f'{indent}<key>ProcessType</key>',
        f'{indent}<string>Background</string>'
    ]

    lines = lines[:insert_index] + process_type_lines + lines[insert_index:]

    # Write back
    with open(plist_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"✓ {os.path.basename(plist_path)} - added ProcessType")
    return True

def main():
    base_path = Path('/Users/administrator/Documents/PetesBrain')

    # Find all plist files
    plist_files = []

    # Agent config.plist files
    plist_files.extend(glob.glob(str(base_path / 'agents' / '*' / 'config.plist')))

    # LaunchAgents directory plists
    plist_files.extend(glob.glob(str(base_path / 'agents' / 'launchagents' / '*.plist')))

    # Installed plists in ~/Library/LaunchAgents
    plist_files.extend(glob.glob(os.path.expanduser('~/Library/LaunchAgents/com.petesbrain.*.plist')))

    print(f"Found {len(plist_files)} plist files\n")

    updated = 0
    for plist_path in sorted(plist_files):
        if add_process_type(plist_path):
            updated += 1

    print(f"\nUpdated {updated} plist files")
    print("\nTo reload all LaunchAgents, run:")
    print("  launchctl unload ~/Library/LaunchAgents/com.petesbrain.*.plist")
    print("  launchctl load ~/Library/LaunchAgents/com.petesbrain.*.plist")

if __name__ == '__main__':
    main()
