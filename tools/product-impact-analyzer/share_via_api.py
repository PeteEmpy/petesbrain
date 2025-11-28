#!/usr/bin/env python3
"""
Share spreadsheets by calling MCP Google Drive repeatedly.
Uses the MCP server's OAuth credentials.
"""

import json
import time
from pathlib import Path

# Setup
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'
SERVICE_ACCOUNT_EMAIL = 'mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com'

print("="*80)
print("SHARE VIA MCP GOOGLE DRIVE API")
print("="*80)
print(f"\nService account: {SERVICE_ACCOUNT_EMAIL}")
print("\nThis script will make repeated API calls via the MCP Google Drive server.")
print("You'll need to run the corresponding MCP tool calls manually.\n")

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Get clients with spreadsheets (skip Tree2mydoor which is already shared)
spreadsheets_to_share = []
for client in config['clients']:
    spreadsheet_id = client.get('product_performance_spreadsheet_id')
    if spreadsheet_id and client['name'] != 'Tree2mydoor':
        spreadsheets_to_share.append({
            'name': client['name'],
            'spreadsheet_id': spreadsheet_id
        })

print(f"Spreadsheets to share: {len(spreadsheets_to_share)}\n")

# Generate the commands
print("="*80)
print("OPTION 1: Using Google Drive API via curl")
print("="*80)
print("\nFirst, get your OAuth token:")
print("1. Go to https://developers.google.com/oauthplayground")
print("2. In Step 1, select 'Drive API v3' and check 'https://www.googleapis.com/auth/drive'")
print("3. Click 'Authorize APIs' and sign in with your Google account")
print("4. In Step 2, click 'Exchange authorization code for tokens'")
print("5. Copy the 'Access token'\n")
print("Then run these commands (replace YOUR_ACCESS_TOKEN):\n")

for item in spreadsheets_to_share:
    print(f"# {item['name']}")
    print(f"""curl -X POST \\
  'https://www.googleapis.com/drive/v3/files/{item['spreadsheet_id']}/permissions' \\
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \\
  -H 'Content-Type: application/json' \\
  -d '{{
    "type": "user",
    "role": "writer",
    "emailAddress": "{SERVICE_ACCOUNT_EMAIL}"
  }}'
""")
    print()

print("\n" + "="*80)
print("OPTION 2: Python script with user input")
print("="*80)
print("\nWe can create an interactive script where you paste your OAuth token once,")
print("and it shares all spreadsheets automatically.")
print("\nWould you like me to create that script? (y/n)")
