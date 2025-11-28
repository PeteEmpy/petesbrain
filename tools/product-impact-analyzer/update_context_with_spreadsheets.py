#!/usr/bin/env python3
"""
Add product performance spreadsheet links to client CONTEXT.md files
"""

import json
from pathlib import Path

# Setup
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'
CLIENTS_DIR = Path('/Users/administrator/Documents/PetesBrain/clients')

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Get clients with spreadsheets
clients_with_spreadsheets = []
for client in config['clients']:
    spreadsheet_id = client.get('product_performance_spreadsheet_id')
    if spreadsheet_id and client.get('enabled'):
        folder_name = client['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')
        clients_with_spreadsheets.append({
            'name': client['name'],
            'folder': folder_name,
            'spreadsheet_id': spreadsheet_id,
            'spreadsheet_url': f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit'
        })

print("="*80)
print("UPDATE CLIENT CONTEXT.MD FILES")
print("="*80)
print(f"\nClients to update: {len(clients_with_spreadsheets)}\n")

updated_count = 0
error_count = 0

for client in clients_with_spreadsheets:
    name = client['name']
    folder = client['folder']
    url = client['spreadsheet_url']

    context_path = CLIENTS_DIR / folder / 'CONTEXT.md'

    print(f"{name}")
    print(f"  Folder: clients/{folder}/")
    print(f"  Context: {context_path}")

    if not context_path.exists():
        print(f"  ⚠️  CONTEXT.md not found, skipping")
        error_count += 1
        continue

    # Read existing content
    with open(context_path, 'r') as f:
        content = f.read()

    # Check if spreadsheet link already exists
    if 'Product Performance Spreadsheet' in content or client['spreadsheet_id'] in content:
        print(f"  ℹ️  Spreadsheet link already exists")
        updated_count += 1
        continue

    # Add spreadsheet link to Quick Reference section or create it
    spreadsheet_section = f"\n## Product Performance Spreadsheet\n\n[View Daily Product Performance]({url})\n\nTracks daily product-level performance metrics (impressions, clicks, conversions, revenue, ROAS) with historical data dating back to October 2025.\n"

    if '## Quick Reference' in content:
        # Insert after Quick Reference heading
        content = content.replace('## Quick Reference', f'## Quick Reference\n{spreadsheet_section}')
    else:
        # Append to end of file
        content += f'\n\n## Quick Reference\n{spreadsheet_section}'

    # Write updated content
    with open(context_path, 'w') as f:
        f.write(content)

    print(f"  ✓ Added spreadsheet link")
    updated_count += 1
    print()

print("="*80)
print("COMPLETE")
print("="*80)
print(f"\n✓ Updated: {updated_count}")
print(f"⚠️  Skipped: {error_count}")

if updated_count > 0:
    print("\nSpreadsheet links added to client CONTEXT.md files!")
    print("Each client folder now has a direct link to their product performance data.")
