#!/usr/bin/env python3
"""Create CLEAN Google Sheet with filtered landing page reports"""

import sys
import csv

sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server')
from gsheet_service import get_gsheet_service

print("📊 Creating CLEAN Google Sheet: NDA Landing Page Reports")
print("🧹 ENABLED campaigns only, no URL parameters\n")

# Get Sheets service
service = get_gsheet_service()

# Create spreadsheet
spreadsheet_body = {
    'properties': {
        'title': 'NDA Landing Page Reports (CLEAN) - ENABLED Only - Sept 1 to Nov 28, 2025'
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

print(f"✅ Created spreadsheet")
print(f"   URL: {spreadsheet_url}\n")

# Read clean CSV files
reports = {
    'Landing Page Statistics': '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report1-landing-page-statistics-clean-90d.csv',
    'PMax Landing Pages': '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report2-pmax-landing-pages-clean-90d.csv',
    'Search Landing Pages': '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/report3-search-landing-pages-clean-90d.csv'
}

all_data = {}
for sheet_name, file_path in reports.items():
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        all_data[sheet_name] = data

# Write data to sheets
for sheet_name, data in all_data.items():
    num_rows = len(data)
    
    range_name = f"'{sheet_name}'!A1"
    body = {'values': data}
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f"   ✓ Written {num_rows} rows to {sheet_name}")

print("\n" + "="*70)
print("✅ CLEAN Google Sheet created successfully!")
print(f"\n📊 Spreadsheet URL:")
print(f"   {spreadsheet_url}")
print("\n📋 Contents:")
print("   1. Landing Page Statistics (134 unique base URLs)")
print("   2. PMax Landing Pages (16 ENABLED asset groups)")
print("   3. Search Landing Pages (64 aggregated URLs)")
print("\n🧹 Filters Applied:")
print("   ✓ URL parameters removed")
print("   ✓ Only ENABLED campaigns/asset groups/ads")
print("   ✓ Aggregated by base URL")
print("="*70 + "\n")

# Save URL
url_file = '/Users/administrator/Documents/PetesBrain/clients/national-design-academy/reports/landing-page-analysis/google-sheet-clean-url.txt'
with open(url_file, 'w') as f:
    f.write(spreadsheet_url)

# Open in browser
import subprocess
subprocess.run(['open', spreadsheet_url])
print("🌐 Opening in browser...\n")
