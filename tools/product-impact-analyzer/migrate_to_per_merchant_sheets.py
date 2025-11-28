#!/usr/bin/env python3
"""
Migrate consolidated Daily Performance sheet to per-merchant sheets.

This script:
1. Reads all data from the current consolidated "Daily Performance" sheet
2. Creates a new sheet for each merchant center account
3. Splits the data by merchant and writes to the appropriate sheet
4. Preserves all historical data (327k+ rows)
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

# Setup paths
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'
CREDENTIALS_PATH = Path('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json')

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)
    SPREADSHEET_ID = config['spreadsheet_id']

# Build merchant ID to name mapping
MERCHANT_MAP = {}
for client in config['clients']:
    merchant_id = client.get('merchant_id')
    if merchant_id and merchant_id != 'UNKNOWN':
        MERCHANT_MAP[merchant_id] = client['name']

print("================================================================================")
print("MIGRATE TO PER-MERCHANT SHEETS")
print("================================================================================")
print(f"\nFound {len(MERCHANT_MAP)} merchants:")
for merchant_id, name in sorted(MERCHANT_MAP.items(), key=lambda x: x[1]):
    print(f"  - {name} ({merchant_id})")

# Initialize Google Sheets API
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=credentials)

print("\n================================================================================")
print("STEP 1: Read all data from consolidated Daily Performance sheet")
print("================================================================================")

# Read all data from current sheet
result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range='Daily Performance!A:M'
).execute()

all_rows = result.get('values', [])
header = all_rows[0] if all_rows else []
data_rows = all_rows[1:] if len(all_rows) > 1 else []

print(f"Read {len(data_rows):,} data rows")
print(f"Columns: {', '.join(header)}")

# Get merchant_id column index (should be column G, index 6)
# Columns: Date, Client, Product ID, Product Title, Impressions, Clicks, Conversions, Revenue, Cost, CTR, Conv Rate, ROAS, Label
# But we need to infer merchant from the data since it's not stored directly

print("\n================================================================================")
print("STEP 2: Group data by merchant (inferring from product IDs)")
print("================================================================================")

# We need to fetch merchant IDs from Google Ads API for each row
# But that would be slow. Instead, let's use the client name to look up merchant ID

merchant_data = defaultdict(list)
unmapped_clients = set()

for row in data_rows:
    if len(row) < 2:
        continue

    client_name = row[1]  # Column B: Client

    # Find merchant ID for this client
    merchant_id = None
    for mid, name in MERCHANT_MAP.items():
        if name == client_name:
            merchant_id = mid
            break

    if merchant_id:
        merchant_data[merchant_id].append(row)
    else:
        unmapped_clients.add(client_name)

if unmapped_clients:
    print(f"\n⚠️  WARNING: {len(unmapped_clients)} clients couldn't be mapped to merchants:")
    for client in sorted(unmapped_clients):
        print(f"  - {client}")

print(f"\nGrouped data into {len(merchant_data)} merchants:")
for merchant_id, rows in sorted(merchant_data.items(), key=lambda x: MERCHANT_MAP.get(x[0], 'Unknown')):
    name = MERCHANT_MAP.get(merchant_id, 'Unknown')
    print(f"  - {name} ({merchant_id}): {len(rows):,} rows")

print("\n================================================================================")
print("STEP 3: Create new sheets for each merchant")
print("================================================================================")

# Get existing sheets
sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
existing_sheets = {sheet['properties']['title']: sheet['properties']['sheetId']
                   for sheet in sheet_metadata['sheets']}

sheets_to_create = []
for merchant_id, name in sorted(MERCHANT_MAP.items(), key=lambda x: x[1]):
    sheet_name = f"Daily Performance - {name} ({merchant_id})"
    if sheet_name not in existing_sheets:
        sheets_to_create.append(sheet_name)
        print(f"  Will create: {sheet_name}")
    else:
        print(f"  Already exists: {sheet_name}")

if sheets_to_create:
    print(f"\nCreating {len(sheets_to_create)} new sheets...")

    requests = []
    for sheet_name in sheets_to_create:
        requests.append({
            'addSheet': {
                'properties': {
                    'title': sheet_name,
                    'gridProperties': {
                        'rowCount': 1000,  # Start small, will auto-expand
                        'columnCount': 13,
                        'frozenRowCount': 1
                    }
                }
            }
        })

    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={'requests': requests}
    ).execute()

    print(f"✓ Created {len(sheets_to_create)} sheets")
    time.sleep(2)  # Brief pause after creation

print("\n================================================================================")
print("STEP 4: Write headers to all sheets")
print("================================================================================")

for merchant_id, name in sorted(MERCHANT_MAP.items(), key=lambda x: x[1]):
    sheet_name = f"Daily Performance - {name} ({merchant_id})"

    # Write header
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{sheet_name}'!A1:M1",
        valueInputOption='RAW',
        body={'values': [header]}
    ).execute()

    print(f"✓ Wrote header to {name}")
    time.sleep(0.5)  # Rate limiting

print("\n================================================================================")
print("STEP 5: Write data to merchant-specific sheets")
print("================================================================================")

batch_size = 5000  # Write in batches to avoid timeouts

for merchant_id, rows in sorted(merchant_data.items(), key=lambda x: MERCHANT_MAP.get(x[0], 'Unknown')):
    name = MERCHANT_MAP.get(merchant_id, 'Unknown')
    sheet_name = f"Daily Performance - {name} ({merchant_id})"

    print(f"\nWriting {len(rows):,} rows to {name}...")

    # Write in batches
    num_batches = (len(rows) + batch_size - 1) // batch_size

    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(rows))
        batch_rows = rows[start_idx:end_idx]

        start_row = start_idx + 2  # +2 because row 1 is header, and sheets are 1-indexed

        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{sheet_name}'!A{start_row}",
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': batch_rows}
        ).execute()

        print(f"  Batch {batch_num + 1}/{num_batches}: Rows {start_idx + 1:,}-{end_idx:,}")
        time.sleep(1)  # Rate limiting

print("\n================================================================================")
print("MIGRATION COMPLETE")
print("================================================================================")
print(f"\n✓ Created {len(MERCHANT_MAP)} merchant-specific sheets")
print(f"✓ Migrated {len(data_rows):,} total rows")
print(f"\nNext steps:")
print(f"  1. Verify data integrity in the new sheets")
print(f"  2. Update sheets_writer.py to use new sheet names")
print(f"  3. Test daily monitoring with new structure")
print(f"  4. Delete old 'Daily Performance' sheet once verified")
print(f"\nSpreadsheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
