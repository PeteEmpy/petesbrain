#!/usr/bin/env python3
"""
Create per-client spreadsheets and populate them with data.

Uses MCP Google Drive to create spreadsheets (OAuth permissions),
then Google Sheets API directly to copy large amounts of data.
"""

import json
import time
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Setup
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'
CREDENTIALS_PATH = Path('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json')
SOURCE_SPREADSHEET_ID = '1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q'

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Get enabled clients with merchants
clients_with_merchants = []
for client in config['clients']:
    merchant_id = client.get('merchant_id')
    if merchant_id and merchant_id != 'UNKNOWN' and client.get('enabled'):
        # Include all clients with spreadsheet IDs
        if 'product_performance_spreadsheet_id' in client:
            clients_with_merchants.append({
                'name': client['name'],
                'merchant_id': merchant_id,
                'config_index': config['clients'].index(client)
            })

if not clients_with_merchants:
    print("All clients already have spreadsheets!")
    print("\nExisting spreadsheets:")
    for client in config['clients']:
        if 'product_performance_spreadsheet_id' in client:
            sid = client['product_performance_spreadsheet_id']
            print(f"  {client['name']}: https://docs.google.com/spreadsheets/d/{sid}/edit")
    exit(0)

print("="*80)
print("POPULATE CLIENT SPREADSHEETS")
print("="*80)
print(f"\nClients needing data population: {len(clients_with_merchants)}")
for c in clients_with_merchants:
    print(f"  - {c['name']} ({c['merchant_id']})")

# Initialize Google Sheets API
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
sheets_service = build('sheets', 'v4', credentials=credentials)

print("\n" + "="*80)
print("POPULATING SPREADSHEETS")
print("="*80)

for client in clients_with_merchants:
    client_name = client['name']
    merchant_id = client['merchant_id']
    sheet_name = f"Daily Performance - {client_name} ({merchant_id})"

    # Get spreadsheet ID from config
    client_config = config['clients'][client['config_index']]
    spreadsheet_id = client_config.get('product_performance_spreadsheet_id')

    if not spreadsheet_id:
        print(f"\n⚠️  {client_name}: No spreadsheet ID in config, skipping")
        continue

    print(f"\n{client_name}")
    print(f"  Spreadsheet ID: {spreadsheet_id}")
    print(f"  Source sheet: {sheet_name}")

    # Read data from source
    print(f"  Reading source data...")
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SOURCE_SPREADSHEET_ID,
            range=f"'{sheet_name}'!A:M"
        ).execute()

        values = result.get('values', [])
        print(f"  Read {len(values):,} rows")

        if not values or len(values) <= 1:
            print(f"  ⚠️  No data to copy")
            continue

        # Write to destination in batches
        print(f"  Writing to destination...")
        batch_size = 10000
        num_batches = (len(values) + batch_size - 1) // batch_size

        for batch_num in range(num_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(values))
            batch_values = values[start_idx:end_idx]

            if batch_num == 0:
                # First batch - overwrite from A1
                sheets_service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range='Sheet1!A1',
                    valueInputOption='USER_ENTERED',
                    body={'values': batch_values}
                ).execute()
            else:
                # Subsequent batches - append
                sheets_service.spreadsheets().values().append(
                    spreadsheetId=spreadsheet_id,
                    range='Sheet1!A1',
                    valueInputOption='USER_ENTERED',
                    insertDataOption='INSERT_ROWS',
                    body={'values': batch_values}
                ).execute()

            print(f"    Batch {batch_num + 1}/{num_batches}: {start_idx + 1:,}-{end_idx:,}")
            time.sleep(0.5)  # Rate limiting

        print(f"  ✓ Wrote {len(values):,} rows")
        print(f"  URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")

    except Exception as e:
        print(f"  ❌ Error: {e}")
        continue

    time.sleep(1)  # Rate limiting between clients

print("\n" + "="*80)
print("COMPLETE")
print("="*80)
print(f"\n✓ Populated {len(clients_with_merchants)} spreadsheets")
print("\nNext: Run update_context_with_spreadsheets.py to add links to CONTEXT.md files")
