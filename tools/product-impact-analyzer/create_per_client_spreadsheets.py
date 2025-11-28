#!/usr/bin/env python3
"""
Create separate Google Spreadsheet for each client and migrate their data.

This creates fully isolated spreadsheets that can be stored in client folders
and shared independently.
"""

import json
import os
import time
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Setup
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'
CREDENTIALS_PATH = Path('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json')
SOURCE_SPREADSHEET_ID = '1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q'
PROJECT_ROOT = Path('/Users/administrator/Documents/PetesBrain')

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Build merchant to client mapping
clients_with_merchants = []
for client in config['clients']:
    merchant_id = client.get('merchant_id')
    if merchant_id and merchant_id != 'UNKNOWN' and client.get('enabled'):
        clients_with_merchants.append({
            'name': client['name'],
            'merchant_id': merchant_id,
            'folder': client['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')
        })

print("="*80)
print("CREATE PER-CLIENT SPREADSHEETS")
print("="*80)
print(f"\nFound {len(clients_with_merchants)} enabled clients with merchant centers:")
for c in clients_with_merchants:
    print(f"  - {c['name']} ({c['merchant_id']})")

# Initialize Google Sheets API
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
sheets_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

print("\n" + "="*80)
print("STEP 1: Read data from source spreadsheet")
print("="*80)

# Get all per-merchant sheet names from source
source_metadata = sheets_service.spreadsheets().get(spreadsheetId=SOURCE_SPREADSHEET_ID).execute()
source_sheets = {sheet['properties']['title']: sheet['properties']['sheetId']
                 for sheet in source_metadata['sheets']}

print(f"Source spreadsheet has {len(source_sheets)} sheets")

# Map clients to their sheet names
client_sheet_map = {}
for client in clients_with_merchants:
    sheet_name = f"Daily Performance - {client['name']} ({client['merchant_id']})"
    if sheet_name in source_sheets:
        client_sheet_map[client['name']] = sheet_name
        print(f"  ✓ {client['name']} → {sheet_name}")
    else:
        print(f"  ✗ {client['name']} → Sheet not found!")

print("\n" + "="*80)
print("STEP 2: Create new spreadsheets for each client")
print("="*80)

# Store new spreadsheet IDs
new_spreadsheets = {}

for client in clients_with_merchants:
    client_name = client['name']
    sheet_name = client_sheet_map.get(client_name)

    if not sheet_name:
        print(f"\n⚠️  Skipping {client_name} - no source sheet")
        continue

    print(f"\n{client_name}")
    print(f"  Creating new spreadsheet...")

    # Create new spreadsheet
    spreadsheet_body = {
        'properties': {
            'title': f'{client_name} - Product Performance'
        },
        'sheets': [{
            'properties': {
                'title': 'Daily Performance',
                'gridProperties': {
                    'rowCount': 1000,
                    'columnCount': 13,
                    'frozenRowCount': 1
                }
            }
        }]
    }

    new_spreadsheet = sheets_service.spreadsheets().create(body=spreadsheet_body).execute()
    new_spreadsheet_id = new_spreadsheet['spreadsheetId']
    new_spreadsheets[client_name] = new_spreadsheet_id

    print(f"  ✓ Created: {new_spreadsheet_id}")

    # Read data from source sheet
    print(f"  Reading data from source...")
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=SOURCE_SPREADSHEET_ID,
        range=f"'{sheet_name}'!A:M"
    ).execute()

    values = result.get('values', [])
    if not values:
        print(f"  ⚠️  No data found")
        continue

    print(f"  Read {len(values)} rows")

    # Write data to new spreadsheet
    print(f"  Writing data to new spreadsheet...")

    # Write in batches
    batch_size = 10000
    num_batches = (len(values) + batch_size - 1) // batch_size

    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(values))
        batch_values = values[start_idx:end_idx]

        if batch_num == 0:
            # First batch - overwrite from A1
            sheets_service.spreadsheets().values().update(
                spreadsheetId=new_spreadsheet_id,
                range='Daily Performance!A1',
                valueInputOption='USER_ENTERED',
                body={'values': batch_values}
            ).execute()
        else:
            # Subsequent batches - append
            sheets_service.spreadsheets().values().append(
                spreadsheetId=new_spreadsheet_id,
                range='Daily Performance!A1',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body={'values': batch_values}
            ).execute()

        print(f"    Batch {batch_num + 1}/{num_batches}: Rows {start_idx + 1}-{end_idx}")
        time.sleep(0.5)  # Rate limiting

    print(f"  ✓ Wrote {len(values)} rows")
    print(f"  URL: https://docs.google.com/spreadsheets/d/{new_spreadsheet_id}/edit")

    time.sleep(1)  # Rate limiting between clients

print("\n" + "="*80)
print("STEP 3: Save spreadsheet IDs to config")
print("="*80)

# Update config with new spreadsheet IDs
for client_config in config['clients']:
    client_name = client_config['name']
    if client_name in new_spreadsheets:
        client_config['product_performance_spreadsheet_id'] = new_spreadsheets[client_name]
        print(f"  ✓ {client_name}: {new_spreadsheets[client_name]}")

# Save updated config
with open(CONFIG_PATH, 'w') as f:
    json.dump(config, f, indent=2)

print(f"\n✓ Updated {CONFIG_PATH}")

print("\n" + "="*80)
print("STEP 4: Create spreadsheet links file")
print("="*80)

# Create a reference file with all spreadsheet links
links_file = SCRIPT_DIR / 'client_spreadsheet_links.json'
with open(links_file, 'w') as f:
    links_data = {
        client_name: {
            'spreadsheet_id': spreadsheet_id,
            'url': f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit',
            'folder': next((c['folder'] for c in clients_with_merchants if c['name'] == client_name), None)
        }
        for client_name, spreadsheet_id in new_spreadsheets.items()
    }
    json.dump(links_data, f, indent=2)

print(f"✓ Created {links_file}")

print("\n" + "="*80)
print("MIGRATION COMPLETE")
print("="*80)
print(f"\n✓ Created {len(new_spreadsheets)} client-specific spreadsheets")
print(f"✓ Updated config.json with spreadsheet IDs")
print(f"\nNext steps:")
print(f"  1. Update CONTEXT.md files with spreadsheet links")
print(f"  2. Update sheets_writer.py to use per-client spreadsheets")
print(f"  3. Test daily monitoring with new structure")
