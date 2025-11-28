#!/usr/bin/env python3
"""
Programmatically share all spreadsheets with the service account.
Gets OAuth token from user and uses it to grant permissions.
"""

import json
import requests
from pathlib import Path

# Setup
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'
SERVICE_ACCOUNT_EMAIL = 'mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com'

print("="*80)
print("PROGRAMMATIC SPREADSHEET SHARING")
print("="*80)
print(f"\nService account: {SERVICE_ACCOUNT_EMAIL}\n")

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Get spreadsheets to share (skip Tree2mydoor)
spreadsheets = []
for client in config['clients']:
    sid = client.get('product_performance_spreadsheet_id')
    if sid and client['name'] != 'Tree2mydoor':
        spreadsheets.append({'name': client['name'], 'id': sid})

print(f"Spreadsheets to share: {len(spreadsheets)}\n")

# Get OAuth token from user
print("To get an OAuth token:")
print("1. Run: gcloud auth application-default print-access-token")
print("   OR")
print("2. Go to: https://developers.google.com/oauthplayground")
print("   - Select 'Drive API v3' → 'https://www.googleapis.com/auth/drive'")
print("   - Authorize and get access token\n")

token = input("Paste your OAuth access token here: ").strip()

if not token:
    print("\n❌ No token provided. Exiting.")
    exit(1)

print(f"\n{'='*80}")
print("SHARING SPREADSHEETS")
print("="*80)

success = 0
failed = 0

for item in spreadsheets:
    name = item['name']
    file_id = item['id']

    print(f"\n{name}")
    print(f"  ID: {file_id}")

    try:
        response = requests.post(
            f'https://www.googleapis.com/drive/v3/files/{file_id}/permissions',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'type': 'user',
                'role': 'writer',
                'emailAddress': SERVICE_ACCOUNT_EMAIL
            },
            timeout=30
        )

        if response.status_code in [200, 201]:
            print(f"  ✓ Shared successfully")
            success += 1
        else:
            print(f"  ❌ Failed: {response.status_code} - {response.text[:200]}")
            failed += 1

    except Exception as e:
        print(f"  ❌ Error: {e}")
        failed += 1

print(f"\n{'='*80}")
print("COMPLETE")
print("="*80)
print(f"\n✓ Successfully shared: {success + 1} (including Tree2mydoor)")
print(f"❌ Failed: {failed}")

if failed == 0:
    print("\n🎉 All spreadsheets shared! Ready to copy data.")
    print("\nNext step:")
    print("  cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer")
    print("  GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json .venv/bin/python3 create_and_populate_client_spreadsheets.py")
