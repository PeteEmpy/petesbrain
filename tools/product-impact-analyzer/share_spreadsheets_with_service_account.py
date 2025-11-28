#!/usr/bin/env python3
"""
Share all client spreadsheets with the service account so it can write data.
Uses OAuth token from Google Drive MCP to grant permissions.
"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Setup
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'
OAUTH_TOKEN_PATH = Path('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/token.json')
SERVICE_ACCOUNT_EMAIL = 'mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com'

print("="*80)
print("SHARE SPREADSHEETS WITH SERVICE ACCOUNT")
print("="*80)
print(f"\nService account: {SERVICE_ACCOUNT_EMAIL}")

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Get clients with spreadsheets
spreadsheets_to_share = []
for client in config['clients']:
    spreadsheet_id = client.get('product_performance_spreadsheet_id')
    if spreadsheet_id:
        spreadsheets_to_share.append({
            'name': client['name'],
            'spreadsheet_id': spreadsheet_id
        })

print(f"\nFound {len(spreadsheets_to_share)} spreadsheets to share:")
for s in spreadsheets_to_share:
    print(f"  - {s['name']}: {s['spreadsheet_id']}")

# Load OAuth token
with open(OAUTH_TOKEN_PATH) as f:
    token_data = json.load(f)

# Create credentials from token
credentials = Credentials(
    token=token_data['access_token'],
    refresh_token=token_data.get('refresh_token'),
    token_uri='https://oauth2.googleapis.com/token',
    client_id=token_data.get('client_id'),
    client_secret=token_data.get('client_secret')
)

# Initialize Drive API
drive_service = build('drive', 'v3', credentials=credentials)

print(f"\n{'='*80}")
print("GRANTING PERMISSIONS")
print("="*80)

success_count = 0
error_count = 0

for item in spreadsheets_to_share:
    name = item['name']
    spreadsheet_id = item['spreadsheet_id']

    print(f"\n{name}")
    print(f"  Spreadsheet ID: {spreadsheet_id}")

    try:
        # Grant Editor permission to service account
        permission = {
            'type': 'user',
            'role': 'writer',  # Editor permissions
            'emailAddress': SERVICE_ACCOUNT_EMAIL
        }

        drive_service.permissions().create(
            fileId=spreadsheet_id,
            body=permission,
            fields='id'
        ).execute()

        print(f"  ✓ Granted Editor permissions to service account")
        success_count += 1

    except Exception as e:
        print(f"  ❌ Error: {e}")
        error_count += 1

print(f"\n{'='*80}")
print("COMPLETE")
print("="*80)
print(f"\n✓ Successfully shared: {success_count}")
print(f"❌ Failed: {error_count}")

if success_count > 0:
    print("\nNext step: Run create_and_populate_client_spreadsheets.py to copy data")
