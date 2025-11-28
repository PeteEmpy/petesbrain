#!/usr/bin/env python3
import json
import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load config
config_path = Path("config.json")
with open(config_path) as f:
    config = json.load(f)

spreadsheet_id = config['spreadsheet_id']

# Get credentials
creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(
    creds_path,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

service = build('sheets', 'v4', credentials=credentials)

# Get all sheets with properties
spreadsheet = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    includeGridData=False
).execute()

sheets = spreadsheet.get('sheets', [])

print(f"\nAnalyzing spreadsheet: {spreadsheet['properties']['title']}")
print(f"Spreadsheet ID: {spreadsheet_id}\n")
print("="*80)
print(f"{'Sheet Name':<40} {'Rows':<10} {'Cols':<6} {'Cells':>12}")
print("="*80)

total_cells = 0

for sheet in sheets:
    props = sheet['properties']
    title = props['title']
    grid_props = props.get('gridProperties', {})
    rows = grid_props.get('rowCount', 0)
    cols = grid_props.get('columnCount', 0)
    cells = rows * cols
    
    total_cells += cells
    
    print(f"{title:<40} {rows:<10} {cols:<6} {cells:>12,}")

print("="*80)
print(f"{'TOTAL':<40} {'':<10} {'':<6} {total_cells:>12,}")
print(f"{'Limit':<40} {'':<10} {'':<6} {'10,000,000':>12}")
print(f"{'Used':<40} {'':<10} {'':<6} {f'{total_cells/10000000*100:.1f}%':>12}")
print("="*80)
