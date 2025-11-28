#!/usr/bin/env python3
"""
Import CSV to Google Sheets using the Google Sheets API directly
This script uploads the replacement candidates CSV to the pre-created sheet
"""

import csv
import sys
from pathlib import Path

# For Google Sheets API via googleapiclient
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                   "google-auth", "google-auth-oauthlib", "google-auth-httplib2",
                   "google-api-python-client"])
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

# Use the credentials from the MCP server
import os
import json

SPREADSHEET_ID = "1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI"
RANGE_NAME = "Replacement Candidates!A1"

def main():
    print("=" * 80)
    print("IMPORTING CSV TO GOOGLE SHEETS")
    print("=" * 80)
    print()

    # Read CSV
    csv_path = Path(__file__).parent / 'output' / 'replacement-candidates.csv'

    if not csv_path.exists():
        print(f"❌ CSV not found: {csv_path}")
        sys.exit(1)

    print(f"📄 Reading CSV: {csv_path}")

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        values = [[str(cell) for cell in row] for row in reader]

    print(f"✅ Loaded {len(values)} rows with {len(values[0])} columns")
    print()
    print(f"📊 Spreadsheet ID: {SPREADSHEET_ID}")
    print(f"📝 Range: {RANGE_NAME}")
    print()
    print("⚠️  Note: This script requires Google Sheets API credentials")
    print("   For now, please manually import the CSV:")
    print()
    print("   1. Open: https://docs.google.com/spreadsheets/d/{}/edit".format(SPREADSHEET_ID))
    print("   2. File → Import")
    print("   3. Upload tab → Select file")
    print(f"   4. Choose: {csv_path}")
    print("   5. Import location: Replace current sheet")
    print("   6. Separator: Comma")
    print("   7. Click 'Import data'")
    print()
    print(f"✅ CSV is ready at: {csv_path}")

    # Copy path to clipboard if possible
    try:
        import subprocess
        subprocess.run(['pbcopy'], input=str(csv_path).encode(), check=True)
        print("📋 CSV path copied to clipboard!")
    except:
        pass

if __name__ == "__main__":
    main()
