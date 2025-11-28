#!/usr/bin/env python3
"""
Copy data from consolidated spreadsheet to per-client spreadsheets.
Uses service account to read, then writes via Google Sheets API with OAuth token.
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
# OAuth token from google-drive MCP server
OAUTH_TOKEN_PATH = Path('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/token.json')
SOURCE_SPREADSHEET_ID = '1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q'

print("="*80)
print("COPY DATA TO CLIENT SPREADSHEETS")
print("="*80)

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Get clients with spreadsheets
clients_to_copy = []
for client in config['clients']:
    merchant_id = client.get('merchant_id')
    spreadsheet_id = client.get('product_performance_spreadsheet_id')
    if merchant_id and merchant_id != 'UNKNOWN' and client.get('enabled') and spreadsheet_id:
        clients_to_copy.append({
            'name': client['name'],
            'merchant_id': merchant_id,
            'spreadsheet_id': spreadsheet_id
        })

print(f"\nFound {len(clients_to_copy)} clients with spreadsheets:")
for c in clients_to_copy:
    print(f"  - {c['name']} ({c['merchant_id']})")

# Initialize Google Sheets API with service account (for reading source)
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
sheets_service = build('sheets', 'v4', credentials=credentials)

# Load OAuth token for writing
with open(OAUTH_TOKEN_PATH) as f:
    token_data = json.load(f)

print(f"\n{'='*80}")
print("COPYING DATA")
print("="*80)

for client in clients_to_copy:
    client_name = client['name']
    merchant_id = client['merchant_id']
    dest_spreadsheet_id = client['spreadsheet_id']
    sheet_name = f"Daily Performance - {client_name} ({merchant_id})"

    print(f"\n{client_name}")
    print(f"  Source sheet: {sheet_name}")
    print(f"  Destination: {dest_spreadsheet_id}")

    # Read from source
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

        # Write to destination using service account
        # We'll write in large batches to minimize API calls
        print(f"  Writing to destination...")

        batch_size = 5000
        num_batches = (len(values) + batch_size - 1) // batch_size

        for batch_num in range(num_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(values))
            batch_values = values[start_idx:end_idx]

            if batch_num == 0:
                # First batch - overwrite from A1
                range_name = 'Sheet1!A1'
            else:
                # Subsequent batches - append starting at next row
                range_name = f'Sheet1!A{start_idx + 1}'

            # Try to write using service account
            try:
                sheets_service.spreadsheets().values().update(
                    spreadsheetId=dest_spreadsheet_id,
                    range=range_name,
                    valueInputOption='USER_ENTERED',
                    body={'values': batch_values}
                ).execute()

                print(f"    Batch {batch_num + 1}/{num_batches}: Rows {start_idx + 1:,}-{end_idx:,} ✓")
            except Exception as e:
                print(f"    Batch {batch_num + 1}/{num_batches}: FAILED - {e}")
                print(f"    Need to share spreadsheet with service account or use OAuth")
                break

            time.sleep(0.5)  # Rate limiting

        else:  # No break occurred
            print(f"  ✓ Wrote {len(values):,} rows")
            print(f"  URL: https://docs.google.com/spreadsheets/d/{dest_spreadsheet_id}/edit")

    except Exception as e:
        print(f"  ❌ Error: {e}")
        continue

    time.sleep(1)  # Rate limiting between clients

print(f"\n{'='*80}")
print("COMPLETE")
print("="*80)
print(f"\nProcessed {len(clients_to_copy)} clients")
print("\nIf errors occurred due to permissions:")
print("  Solution: Share each spreadsheet with the service account email")
print("  or use MCP Google Drive updateGoogleSheet tool")
