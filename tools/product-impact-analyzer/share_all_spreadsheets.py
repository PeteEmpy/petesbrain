#!/usr/bin/env python3
"""
Programmatically share all client spreadsheets with the service account.
Uses user's OAuth credentials (same ones that created the spreadsheets).
"""

import json
import subprocess
from pathlib import Path

# Setup
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'
SERVICE_ACCOUNT_EMAIL = 'mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com'

print("="*80)
print("PROGRAMMATICALLY SHARE SPREADSHEETS")
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

print(f"\nFound {len(spreadsheets_to_share)} spreadsheets to share")

# Skip Tree2mydoor (already shared manually)
spreadsheets_to_share = [s for s in spreadsheets_to_share if s['name'] != 'Tree2mydoor']
print(f"Skipping Tree2mydoor (already shared)")
print(f"Remaining: {len(spreadsheets_to_share)} spreadsheets\n")

success_count = 0
error_count = 0

# Use npx @piotr-agier/google-drive-mcp to share each spreadsheet
# This uses the same OAuth credentials that created the spreadsheets
for item in spreadsheets_to_share:
    name = item['name']
    spreadsheet_id = item['spreadsheet_id']

    print(f"{name}")
    print(f"  ID: {spreadsheet_id}")

    # Create a temporary JSON file with the permission request
    permission_data = {
        "fileId": spreadsheet_id,
        "permission": {
            "type": "user",
            "role": "writer",
            "emailAddress": SERVICE_ACCOUNT_EMAIL
        }
    }

    # Use Google Drive API via npx command
    # The npx @piotr-agier/google-drive-mcp tool has OAuth credentials already set up
    cmd = f"""
GOOGLE_DRIVE_OAUTH_CREDENTIALS="/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json" \
npx -y @piotr-agier/google-drive-mcp@latest share \
    --file-id "{spreadsheet_id}" \
    --email "{SERVICE_ACCOUNT_EMAIL}" \
    --role writer
"""

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(f"  ✓ Shared successfully")
            success_count += 1
        else:
            # Try alternative method: use gcloud CLI if available
            print(f"  ⚠️  npx method failed, trying alternative...")

            # Alternative: use curl with OAuth token
            # This requires getting the OAuth token from the MCP server
            alt_cmd = f"""
python3 -c "
import subprocess
import json

# Get OAuth token from gcloud
token_result = subprocess.run(
    ['gcloud', 'auth', 'application-default', 'print-access-token'],
    capture_output=True,
    text=True
)
if token_result.returncode != 0:
    print('No gcloud auth available')
    exit(1)

token = token_result.stdout.strip()

# Make API call to share
import requests
response = requests.post(
    'https://www.googleapis.com/drive/v3/files/{spreadsheet_id}/permissions',
    headers={{'Authorization': f'Bearer {{token}}'}},
    json={{
        'type': 'user',
        'role': 'writer',
        'emailAddress': '{SERVICE_ACCOUNT_EMAIL}'
    }}
)

if response.status_code in [200, 201]:
    print('✓ Shared')
else:
    print(f'Error: {{response.text}}')
    exit(1)
"
"""
            result2 = subprocess.run(alt_cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result2.returncode == 0 and '✓' in result2.stdout:
                print(f"  ✓ Shared successfully (alternative method)")
                success_count += 1
            else:
                print(f"  ❌ Both methods failed")
                print(f"     Error: {result.stderr[:200]}")
                error_count += 1

    except Exception as e:
        print(f"  ❌ Error: {e}")
        error_count += 1

    print()

print("="*80)
print("COMPLETE")
print("="*80)
print(f"\n✓ Successfully shared: {success_count + 1} (including Tree2mydoor)")
print(f"❌ Failed: {error_count}")

if error_count > 0:
    print("\nFor failed spreadsheets, you can manually share them:")
    print(f"  1. Open the spreadsheet URL")
    print(f"  2. Click Share")
    print(f"  3. Add: {SERVICE_ACCOUNT_EMAIL}")
    print(f"  4. Set to Editor")
    print(f"  5. Uncheck 'Notify people' and click Share")

if success_count + 1 == len(spreadsheets_to_share) + 1:  # +1 for Tree2mydoor
    print("\nAll spreadsheets shared! Ready to copy data.")
    print("\nRun: GOOGLE_APPLICATION_CREDENTIALS=... .venv/bin/python3 create_and_populate_client_spreadsheets.py")
