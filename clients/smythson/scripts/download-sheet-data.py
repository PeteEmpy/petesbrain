#!/usr/bin/env python3
"""
Download Smythson copy sheet data to local CSV files
"""

import os
import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CREDENTIALS_FILE = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'
SPREADSHEET_ID = '1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g'
OUTPUT_DIR = '/Users/administrator/Documents/PetesBrain/clients/smythson/data/replacement-copy'

SHEETS = {
    'UK ad copy': 'uk-replacement-copy.csv',
    'US ad copy': 'us-replacement-copy.csv',
    'EUR ad copy': 'eur-replacement-copy.csv',
    'ROW ad copy': 'row-replacement-copy.csv',
}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    for sheet_name, output_file in SHEETS.items():
        print(f"Downloading {sheet_name}...")

        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{sheet_name}'!A:AZ"
        ).execute()

        values = result.get('values', [])

        output_path = os.path.join(OUTPUT_DIR, output_file)
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for row in values:
                writer.writerow(row)

        print(f"  ✓ Saved {len(values)} rows to {output_file}")

    print("\nDone!")

if __name__ == "__main__":
    main()
