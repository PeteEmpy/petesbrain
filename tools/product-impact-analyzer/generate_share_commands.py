#!/usr/bin/env python3
"""Generate curl commands to share all spreadsheets"""

import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / 'config.json'
SERVICE_ACCOUNT_EMAIL = 'mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com'

with open(CONFIG_PATH) as f:
    config = json.load(f)

# Get spreadsheets (skip Tree2mydoor)
spreadsheets = []
for client in config['clients']:
    sid = client.get('product_performance_spreadsheet_id')
    if sid and client['name'] != 'Tree2mydoor':
        spreadsheets.append({'name': client['name'], 'id': sid})

print("# Share All Spreadsheets with Service Account")
print(f"# Service account: {SERVICE_ACCOUNT_EMAIL}")
print(f"# Spreadsheets: {len(spreadsheets)}")
print()
print("# First, get your OAuth token:")
print("# Visit: https://developers.google.com/oauthplayground")
print("# 1. Select 'Drive API v3' → check 'https://www.googleapis.com/auth/drive'")
print("# 2. Click 'Authorize APIs' and sign in")
print("# 3. Click 'Exchange authorization code for tokens'")
print("# 4. Copy the 'Access token'")
print("# 5. Replace YOUR_TOKEN_HERE below with your token")
print()
print("TOKEN='YOUR_TOKEN_HERE'")
print()

for item in spreadsheets:
    print(f"# {item['name']}")
    print(f"""curl -X POST \\
  'https://www.googleapis.com/drive/v3/files/{item['id']}/permissions' \\
  -H "Authorization: Bearer $TOKEN" \\
  -H 'Content-Type: application/json' \\
  -d '{{
    "type": "user",
    "role": "writer",
    "emailAddress": "{SERVICE_ACCOUNT_EMAIL}"
  }}'
echo " ✓ {item['name']}"
""")

print("\necho 'All spreadsheets shared!'")
