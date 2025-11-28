#!/usr/bin/env python3
"""Create Google Sheet with landing page reports"""

import sys
import csv

# Add MCP server path
sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server')

from gsheet_service import get_gsheet_service

print("📊 Creating Google Sheet: NDA Landing Page Reports (90 Days)")

# Get Sheets service
print("\n1. Authenticating with Google Sheets...")
service = get_gsheet_service()
print("   ✓ Authenticated")

# Step 2: Create new spreadsheet
print("\n2. Creating new Google Sheet...")

spreadsheet_body = {
    'properties': {
        'title': 'NDA Landing Page Reports (90 Days) - Sept 1 to Nov 28, 2025'
    },
    'sheets': [
        {'properties': {'title': 'Landing Page Statistics'}},
        {'properties': {'title': 'PMax Landing Pages'}},
        {'properties': {'title': 'Search Landing Pages'}}
    ]
}

spreadsheet = service.spreadsheets().create(body=spreadsheet_body).execute()
spreadsheet_id = spreadsheet['spreadsheetId']
spreadsheet_url = spreadsheet['spreadsheetUrl']

print(f"✅ Created spreadsheet: {spreadsheet_id}")
print(f"   URL: {spreadsheet_url}")

# Step 3: Read CSV files
print("\n3. Reading CSV reports...")

reports = {
    'Landing Page Statistics': '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report1-landing-page-statistics-90d.csv',
    'PMax Landing Pages': '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report2-pmax-landing-pages-90d.csv',
    'Search Landing Pages': '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report3-search-landing-pages-90d.csv'
}

all_data = {}
for sheet_name, file_path in reports.items():
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        all_data[sheet_name] = data
        print(f"   ✓ Loaded {sheet_name}: {len(data)} rows")

# Step 4: Write data to each sheet
print("\n4. Writing data to sheets...")

for sheet_name, data in all_data.items():
    num_rows = len(data)
    num_cols = len(data[0]) if data else 0
    
    print(f"   Writing to {sheet_name} ({num_rows} rows x {num_cols} cols)...")
    
    # Write data
    range_name = f"'{sheet_name}'!A1"
    body = {
        'values': data
    }
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f"   ✓ Written {num_rows} rows to {sheet_name}")

print("\n" + "="*60)
print("✅ Google Sheet created successfully!")
print(f"\n📊 Spreadsheet URL:")
print(f"   {spreadsheet_url}")
print("\n📋 Sheets:")
print("   1. Landing Page Statistics (154 pages)")
print("   2. PMax Landing Pages (59 asset groups)")
print("   3. Search Landing Pages (1,142 ads)")
print("="*60 + "\n")

# Save URL to file
url_file = '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/google-sheet-url.txt'
with open(url_file, 'w') as f:
    f.write(spreadsheet_url)

print(f"📄 URL saved to: google-sheet-url.txt\n")

# Open in browser
import subprocess
subprocess.run(['open', spreadsheet_url])
print(f"🌐 Opening in browser...\n")
