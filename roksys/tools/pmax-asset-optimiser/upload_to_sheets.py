#!/usr/bin/env python3
"""
Upload replacement candidates CSV to Google Sheets for review

This script:
1. Creates a new Google Sheet
2. Uploads the replacement-candidates.csv data
3. Formats the sheet for easy review
4. Returns the shareable URL

Author: PetesBrain
Created: 2025-11-26
"""

import csv
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

# Google Sheets API scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials():
    """Get Google Sheets API credentials"""
    creds = None
    token_path = Path.home() / '.credentials' / 'sheets_token.json'
    credentials_path = Path.home() / '.credentials' / 'sheets_credentials.json'

    # Check if token exists
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                print(f"❌ Credentials file not found: {credentials_path}")
                print("   Please download OAuth credentials from Google Cloud Console")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

def create_sheet(service, title):
    """Create a new Google Sheet"""
    spreadsheet = {
        'properties': {
            'title': title
        }
    }

    spreadsheet = service.spreadsheets().create(
        body=spreadsheet,
        fields='spreadsheetId,spreadsheetUrl'
    ).execute()

    return spreadsheet

def upload_csv_data(service, spreadsheet_id, csv_path):
    """Upload CSV data to the sheet"""
    # Read CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Upload data
    body = {
        'values': data
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='A1',
        valueInputOption='RAW',
        body=body
    ).execute()

    return result

def format_sheet(service, spreadsheet_id):
    """Format the sheet for easy review"""
    requests = [
        # Freeze header row
        {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': 0,
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        },
        # Bold header row
        {
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {
                            'bold': True
                        }
                    }
                },
                'fields': 'userEnteredFormat.textFormat.bold'
            }
        },
        # Auto-resize columns
        {
            'autoResizeDimensions': {
                'dimensions': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': 13
                }
            }
        }
    ]

    body = {
        'requests': requests
    }

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

def main():
    """Main execution"""
    print("=" * 80)
    print("UPLOAD REPLACEMENT CANDIDATES TO GOOGLE SHEETS")
    print("=" * 80)
    print()

    # Paths
    base_dir = Path(__file__).parent
    csv_path = base_dir / 'output' / 'replacement-candidates.csv'

    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}")
        sys.exit(1)

    print(f"📄 CSV file: {csv_path}")
    print(f"📊 Authenticating with Google Sheets API...")

    try:
        # Get credentials
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)

        # Create sheet
        print(f"📝 Creating new Google Sheet...")
        title = "Tree2mydoor PMAX Asset Replacement Candidates - 2025-11-26"
        spreadsheet = create_sheet(service, title)

        spreadsheet_id = spreadsheet['spreadsheetId']
        spreadsheet_url = spreadsheet['spreadsheetUrl']

        print(f"✅ Created: {title}")
        print(f"   ID: {spreadsheet_id}")

        # Upload data
        print(f"📤 Uploading CSV data...")
        upload_csv_data(service, spreadsheet_id, csv_path)
        print(f"✅ Data uploaded")

        # Format sheet
        print(f"🎨 Formatting sheet...")
        format_sheet(service, spreadsheet_id)
        print(f"✅ Formatting complete")

        print()
        print("=" * 80)
        print("✅ UPLOAD COMPLETE")
        print("=" * 80)
        print()
        print(f"📊 Google Sheet URL:")
        print(f"   {spreadsheet_url}")
        print()
        print("📝 Next steps:")
        print("   1. Open the sheet in your browser")
        print("   2. Review the 'Replacement_Text' column")
        print("   3. For each row, set 'Action' to SWAP or SKIP")
        print("   4. Download as CSV when done")
        print("   5. Replace the original replacement-candidates.csv")
        print("   6. Run: python3 execute_asset_optimisation.py")
        print()

    except HttpError as error:
        print(f"❌ An error occurred: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
