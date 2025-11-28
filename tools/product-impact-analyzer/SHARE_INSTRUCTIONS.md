# Manual Sharing Instructions

## Problem

The 15 client spreadsheets were created via OAuth (MCP Google Drive) but the service account (`mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`) doesn't have write permissions to them.

## Solution

Manually share each spreadsheet with the service account email to grant Editor permissions.

## Service Account Email

```
mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com
```

## Spreadsheets to Share

1. **Tree2mydoor**: https://docs.google.com/spreadsheets/d/1fQ_OO48IzoojEi2nlcDRQAA9Me6vWzvRi7nyJ0YvycA/edit
2. **Smythson UK**: https://docs.google.com/spreadsheets/d/1DtK0MX5qwISwO8blvbBT9rEQWqn-uVFp5hS3xBR-glo/edit
3. **BrightMinds**: https://docs.google.com/spreadsheets/d/12jpLRhbMmZ-cIhmI53dY6hB520GhZGoKN_NTDxfX3ks/edit
4. **Accessories for the Home**: https://docs.google.com/spreadsheets/d/1V23MwIeSDTj5ECBJAOIukENzy3YMxUoOEMiSP2IZAWM/edit
5. **Go Glean UK**: https://docs.google.com/spreadsheets/d/1Jqy3Y4jQGUQFwyvjTHAb0JCOAxwndaIvZItvkU-xaqw/edit
6. **Superspace UK**: https://docs.google.com/spreadsheets/d/1N8H0n1qL3jWHdWxKlbyF0ywjQ1Hn5YSbgxgC4Ig2B6s/edit
7. **Uno Lights**: https://docs.google.com/spreadsheets/d/1vQAD5xOA-u2LWwB1AzxJJd1RJIBbqHpHHmlseO0Ko-A/edit
8. **Godshot**: https://docs.google.com/spreadsheets/d/1Hrr27rAc1PpVxefSLja5TlEAD4Dg1rqNxbqn4FeaYCk/edit
9. **HappySnapGifts**: https://docs.google.com/spreadsheets/d/1nTJyS3I5GlkRJfTeoTWBX3ehV-EDYnHOIn7Yq7raXd0/edit
10. **WheatyBags**: https://docs.google.com/spreadsheets/d/1htjYR0YM5TFmd1NwIS6M6jSev86VsEJ5-okkX-5MOdI/edit
11. **BMPM**: https://docs.google.com/spreadsheets/d/1EenJFkPWGZ6c_ZhsKKYudDcW2Nt8Jeamc1m55BPR5dU/edit
12. **Grain Guard**: https://docs.google.com/spreadsheets/d/1VFyGERR0OHX12CwP76YUWexegrEoyhAaReGGRX9kMjw/edit
13. **Crowd Control**: https://docs.google.com/spreadsheets/d/1V3RY5Kw5b22nzveWfDNQfjzsJ8CVdV4km0pXE3Nfofw/edit
14. **Just Bin Bags**: https://docs.google.com/spreadsheets/d/1zEiKnU-jJjEqchmXIX3QhML-g3H3v6ZstLFfz69CJyA/edit
15. **Just Bin Bags JHD**: https://docs.google.com/spreadsheets/d/1p7hVR4bwMVTiBj8za6pVv3kmnVr8v3YEz2fhGun2YSk/edit

## Steps to Share

For each spreadsheet:

1. Open the spreadsheet URL in your browser
2. Click the **Share** button (top right)
3. Paste the service account email: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
4. Set permission level to **Editor**
5. Uncheck "Notify people" (it's a service account, not a real person)
6. Click **Share**

## After Sharing

Once all spreadsheets are shared with the service account, run:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json .venv/bin/python3 create_and_populate_client_spreadsheets.py
```

This will copy all 277,875 rows of historical data from the source spreadsheet to the 15 client spreadsheets.

## Quick Test

After sharing just Tree2mydoor spreadsheet, test with:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json .venv/bin/python3 -c "
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(
    '/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
sheets = build('sheets', 'v4', credentials=credentials)

# Test write to Tree2mydoor
sheets.spreadsheets().values().update(
    spreadsheetId='1fQ_OO48IzoojEi2nlcDRQAA9Me6vWzvRi7nyJ0YvycA',
    range='Sheet1!A1',
    valueInputOption='USER_ENTERED',
    body={'values': [['TEST', 'SUCCESS']]}
).execute()

print('✓ Write successful!')
"
```

If this succeeds, the sharing worked and you can proceed to share all 15 spreadsheets.
