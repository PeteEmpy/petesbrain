# Automated CSV to Google Sheets Upload

**Category**: Technical / Data Export
**Status**: Active
**Created**: 2025-11-26
**Last Updated**: 2025-11-26

---

## Overview

Fully automated Python script to upload CSV files to Google Sheets using the Google Sheets API with OAuth authentication from the MCP server.

**Key Benefit**: Zero manual intervention - no need for manual CSV imports through the Google Sheets UI.

---

## When to Use This

Use this approach when you need to:
- Upload large CSV files (100+ rows) to Google Sheets automatically
- Avoid manual "File → Import" steps in Google Sheets UI
- Integrate Google Sheets upload into automated workflows
- Replace data in existing Google Sheets programmatically

**Don't Use This When**:
- The MCP `write_cells` tool works (small datasets <100 rows)
- You need to append data (this overwrites from the specified range)
- You don't have the MCP Google Sheets server configured

---

## The Solution

### Key Insight

The MCP Google Sheets server at `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/` has already authenticated with Google and has a valid OAuth token at `token.json`.

We can reuse this token directly with the Google Sheets API to bypass all manual upload steps.

### Python Script Template

```python
#!/usr/bin/env python3
"""
Automated CSV to Google Sheets upload using MCP server's OAuth token
"""

import csv
import sys
from pathlib import Path

# Auto-install dependencies if needed
try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Installing Google Sheets API dependencies...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                   "google-auth", "google-auth-oauthlib", "google-auth-httplib2",
                   "google-api-python-client"])
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

# CONFIGURATION - Change these for your use case
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"  # From the Google Sheets URL
RANGE_NAME = "Sheet1!A1"  # Starting cell (will expand automatically)
CSV_FILE_PATH = Path(__file__).parent / 'your-file.csv'

# OAuth token from MCP server (don't change this)
MCP_TOKEN_PATH = Path('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/token.json')

def get_credentials():
    """Load OAuth credentials from MCP server"""
    if not MCP_TOKEN_PATH.exists():
        print(f"❌ MCP token not found at {MCP_TOKEN_PATH}")
        print("   Make sure the Google Sheets MCP server is configured")
        return None

    print(f"✅ Found OAuth token: {MCP_TOKEN_PATH}")
    creds = Credentials.from_authorized_user_file(str(MCP_TOKEN_PATH))

    # Refresh token if expired
    if creds and creds.expired and creds.refresh_token:
        print("🔄 Refreshing expired token...")
        creds.refresh(Request())

    return creds

def upload_csv_to_sheets(csv_path, spreadsheet_id, range_name):
    """Upload CSV data to Google Sheets"""

    # Read CSV file
    if not csv_path.exists():
        print(f"❌ CSV not found: {csv_path}")
        return False

    print(f"📄 Reading CSV: {csv_path.name}")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        values = [[str(cell) for cell in row] for row in reader]

    print(f"✅ Loaded {len(values)} rows with {len(values[0]) if values else 0} columns")

    # Get credentials
    print("🔐 Loading Google API credentials...")
    creds = get_credentials()
    if not creds:
        return False

    # Upload to Google Sheets
    try:
        print(f"📤 Uploading to Google Sheets...")
        print(f"   Spreadsheet ID: {spreadsheet_id}")
        print(f"   Range: {range_name}")

        service = build('sheets', 'v4', credentials=creds)

        body = {'values': values}

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        updated_cells = result.get('updatedCells', 0)
        updated_range = result.get('updatedRange', '')

        print("\n" + "=" * 80)
        print("✅ UPLOAD SUCCESSFUL")
        print("=" * 80)
        print(f"📊 Updated: {updated_cells} cells")
        print(f"📍 Range: {updated_range}")
        print(f"🔗 View: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
        print()

        return True

    except HttpError as error:
        print(f"❌ API Error: {error}")
        return False

def main():
    success = upload_csv_to_sheets(CSV_FILE_PATH, SPREADSHEET_ID, RANGE_NAME)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

---

## How to Use

### 1. Configuration

Update these three variables at the top of the script:

```python
SPREADSHEET_ID = "1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI"  # From URL
RANGE_NAME = "Sheet1!A1"  # Sheet name + starting cell
CSV_FILE_PATH = Path(__file__).parent / 'your-data.csv'
```

**Finding the Spreadsheet ID**:
From URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit`

**Range Name Format**:
- `Sheet1!A1` - Starts at A1 on Sheet1
- `Data!A5` - Starts at A5 on the "Data" sheet
- `Replacement Candidates!A1` - Works with spaces in sheet names

### 2. Run the Script

```bash
python3 automated_upload.py
```

The script will:
1. Auto-install dependencies if needed
2. Read the CSV file
3. Load OAuth token from MCP server
4. Upload all data to Google Sheets
5. Display success message with cell count and link

### 3. Expected Output

```
📄 Reading CSV: replacement-candidates.csv
✅ Loaded 277 rows with 13 columns
🔐 Loading Google API credentials...
✅ Found OAuth token: /Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/token.json
📤 Uploading to Google Sheets...
   Spreadsheet ID: 1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI
   Range: Replacement Candidates!A1

================================================================================
✅ UPLOAD SUCCESSFUL
================================================================================
📊 Updated: 3601 cells
📍 Range: 'Replacement Candidates'!A1:M277
🔗 View: https://docs.google.com/spreadsheets/d/1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI/edit
```

---

## How It Works

### Authentication Flow

1. Script looks for MCP server's OAuth token at fixed path
2. Loads credentials using `Credentials.from_authorized_user_file()`
3. Checks if token is expired, refreshes if needed
4. Uses token to authenticate with Google Sheets API

### Upload Process

1. CSV file is read into 2D array: `[[row1], [row2], ...]`
2. Array is wrapped in `{'values': array}` body
3. `spreadsheets().values().update()` replaces data starting at specified range
4. API returns updated cell count and range

### Key Design Decisions

**Why use MCP server's token?**
- Already authenticated with correct scopes
- No need for separate service account setup
- Reuses existing trusted credentials

**Why not use MCP `write_cells` tool?**
- MCP tool has parameter size limits (~100 rows max)
- Direct API call handles unlimited rows
- Faster single operation vs. multiple chunked calls

**Why `valueInputOption='RAW'`?**
- Preserves CSV data exactly as-is
- No formula interpretation
- No automatic formatting

---

## Troubleshooting

### Error: "MCP token not found"

**Cause**: Google Sheets MCP server not configured
**Fix**: Ensure MCP server is installed and authenticated at:
```
/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/
```

### Error: "HttpError 403: Forbidden"

**Cause**: Token doesn't have write permission to spreadsheet
**Fix**:
1. Open the Google Sheet in browser
2. Check you're logged in with the same Google account used by MCP server
3. Verify sheet isn't protected or read-only

### Error: "HttpError 400: Unable to parse range"

**Cause**: Invalid `RANGE_NAME` format
**Fix**: Use format `SheetName!A1` (sheet name can have spaces)

### Upload succeeds but sheet is empty

**Cause**: CSV file is empty or malformed
**Fix**: Check CSV has data and proper formatting:
```bash
head -5 your-file.csv  # View first 5 lines
```

---

## Real-World Example

**Context**: PMAX Asset Optimizer for Tree2mydoor

**Files**:
- Script: `/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/automated_sheets_upload.py`
- CSV: `output/replacement-candidates.csv` (277 rows × 13 columns)
- Sheet: `https://docs.google.com/spreadsheets/d/1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI/edit`

**Configuration**:
```python
SPREADSHEET_ID = "1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI"
RANGE_NAME = "Replacement Candidates!A1"
CSV_FILE_PATH = Path(__file__).parent / 'output' / 'replacement-candidates.csv'
```

**Result**: Successfully uploaded 3,601 cells (277 rows × 13 columns) in single automated operation.

---

## Limitations

1. **Overwrites data** - Replaces from specified range, doesn't append
2. **Requires MCP server** - Needs Google Sheets MCP server with valid OAuth token
3. **No formatting** - Uploads raw values only, no cell formatting/colours
4. **Single sheet** - Each run updates one range, not multiple sheets
5. **Sheet must exist** - Won't create new sheets, only updates existing ones

---

## Related Resources

- **MCP Google Sheets Server**: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/`
- **Google Sheets API Docs**: https://developers.google.com/sheets/api/guides/values
- **OAuth Token Location**: `token.json` in MCP server directory

---

## Version History

- **2025-11-26**: Initial playbook created based on Tree2mydoor PMAX Asset Optimizer implementation
