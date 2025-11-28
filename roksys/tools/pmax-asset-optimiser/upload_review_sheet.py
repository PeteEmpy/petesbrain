#!/usr/bin/env python3
"""
Upload review sheet to Google Sheets
"""

import csv
import sys
from pathlib import Path

# Import Google Sheets API libraries
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

SPREADSHEET_ID = "1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI"
SHEET_NAME = "Tree2mydoor Review"
RANGE_NAME = f"{SHEET_NAME}!A1"

MCP_TOKEN_PATH = Path('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/token.json')

def get_credentials():
    """Load OAuth credentials from MCP server"""
    if not MCP_TOKEN_PATH.exists():
        print(f"❌ MCP token not found at {MCP_TOKEN_PATH}")
        return None

    print(f"✅ Found OAuth token: {MCP_TOKEN_PATH}")
    creds = Credentials.from_authorized_user_file(str(MCP_TOKEN_PATH))

    if creds and creds.expired and creds.refresh_token:
        print("🔄 Refreshing expired token...")
        creds.refresh(Request())

    return creds

def create_or_clear_sheet(service, spreadsheet_id, sheet_name):
    """Create sheet if it doesn't exist, or clear it if it does"""
    try:
        # Get existing sheets
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = spreadsheet.get('sheets', [])

        sheet_exists = False
        sheet_id = None

        for sheet in sheets:
            if sheet['properties']['title'] == sheet_name:
                sheet_exists = True
                sheet_id = sheet['properties']['sheetId']
                break

        if sheet_exists:
            print(f"✅ Sheet '{sheet_name}' exists - clearing data...")
            # Clear existing data
            service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet_name}!A1:Z1000"
            ).execute()
        else:
            print(f"📝 Creating new sheet '{sheet_name}'...")
            # Create new sheet
            request = {
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }
            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={'requests': [request]}
            ).execute()

        return True

    except HttpError as error:
        print(f"❌ Error managing sheet: {error}")
        return False

def upload_data(creds, values):
    """Upload data to Google Sheets"""
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Create or clear the sheet
        if not create_or_clear_sheet(service, SPREADSHEET_ID, SHEET_NAME):
            return None

        body = {'values': values}

        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        return result

    except HttpError as error:
        print(f"❌ API Error: {error}")
        return None

def main():
    print("=" * 80)
    print("UPLOAD REVIEW SHEET TO GOOGLE SHEETS")
    print("=" * 80)
    print()

    # Read CSV
    csv_path = Path(__file__).parent / 'output' / 'tree2mydoor-review-sheet.csv'

    if not csv_path.exists():
        print(f"❌ CSV not found: {csv_path}")
        print("   Run create_review_sheet.py first")
        sys.exit(1)

    print(f"📄 Reading CSV: {csv_path.name}")

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        values = [[str(cell) for cell in row] for row in reader]

    print(f"✅ Loaded {len(values)} rows with {len(values[0])} columns")
    print()

    # Get credentials
    print("🔐 Loading Google API credentials...")
    creds = get_credentials()

    if not creds:
        print("❌ No credentials available")
        sys.exit(1)

    # Upload with credentials
    print(f"📤 Uploading {len(values)} rows to Google Sheets...")
    print(f"   Spreadsheet ID: {SPREADSHEET_ID}")
    print(f"   Sheet: {SHEET_NAME}")
    print()

    result = upload_data(creds, values)

    if result:
        updated_cells = result.get('updatedCells', 0)
        updated_range = result.get('updatedRange', '')

        print("=" * 80)
        print("✅ UPLOAD SUCCESSFUL")
        print("=" * 80)
        print()
        print(f"📊 Updated: {updated_cells} cells")
        print(f"📍 Range: {updated_range}")
        print()
        print(f"🔗 View sheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0")
        print()

        return True
    else:
        print("❌ Upload failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
