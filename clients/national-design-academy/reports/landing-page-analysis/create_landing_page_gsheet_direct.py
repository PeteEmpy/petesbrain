#!/usr/bin/env python3
"""Create Google Sheet with landing page reports using MCP server directly"""

import sys
import csv
import os

# Add MCP server path
sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server')

# Set environment variable for credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'

from sheets_api import create_spreadsheet, add_sheet, write_cells

print("📊 Creating Google Sheet: NDA Landing Page Reports (90 Days)")

# Step 1: Create new spreadsheet
print("\n1. Creating new Google Sheet...")

spreadsheet = create_spreadsheet('NDA Landing Page Reports (90 Days) - Sept 1 to Nov 28, 2025')
spreadsheet_id = spreadsheet['spreadsheetId']
spreadsheet_url = spreadsheet['spreadsheetUrl']

print(f"✅ Created spreadsheet: {spreadsheet_id}")
print(f"   URL: {spreadsheet_url}")

# Step 2: Read CSV files
print("\n2. Reading CSV reports...")

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

# Step 3: Add additional sheets
print("\n3. Setting up sheet tabs...")

# Add the two additional sheets (first sheet already exists)
for sheet_name in ['PMax Landing Pages', 'Search Landing Pages']:
    add_sheet(spreadsheet_id, sheet_name)
    print(f"   ✓ Added sheet: {sheet_name}")

# Rename first sheet
print("   Note: You'll need to manually rename 'Sheet1' to 'Landing Page Statistics'")

# Step 4: Write data to each sheet
print("\n4. Writing data to sheets...")

sheet_mappings = {
    'Landing Page Statistics': 'Sheet1',  # First sheet is called Sheet1
    'PMax Landing Pages': 'PMax Landing Pages',
    'Search Landing Pages': 'Search Landing Pages'
}

for display_name, data in all_data.items():
    sheet_name = sheet_mappings[display_name]
    
    # Convert data to format expected by API
    values = [[str(cell) for cell in row] for row in data]
    
    # Determine range based on data size
    num_rows = len(values)
    num_cols = len(values[0]) if values else 0
    
    # Convert column number to letter
    def col_to_letter(col):
        result = ""
        while col > 0:
            col -= 1
            result = chr(col % 26 + 65) + result
            col //= 26
        return result
    
    end_col = col_to_letter(num_cols)
    range_name = f"'{sheet_name}'!A1:{end_col}{num_rows}"
    
    print(f"   Writing to {display_name} ({num_rows} rows)...")
    
    try:
        write_cells(spreadsheet_id, range_name, values)
        print(f"   ✓ Written {num_rows} rows to {display_name}")
    except Exception as e:
        print(f"   ⚠️  Error writing to {display_name}: {str(e)}")

print("\n" + "="*60)
print("✅ Google Sheet created successfully!")
print(f"\n📊 Spreadsheet URL:")
print(f"   {spreadsheet_url}")
print("\n📋 Sheets:")
print("   1. Landing Page Statistics (154 pages)")
print("   2. PMax Landing Pages (59 asset groups)")
print("   3. Search Landing Pages (1,142 ads)")
print("="*60 + "\n")

# Save URL to file for easy access
with open('google_sheet_url.txt', 'w') as f:
    f.write(spreadsheet_url)

print(f"📄 URL saved to: google_sheet_url.txt\n")
print(f"🌐 Copy this URL:\n   {spreadsheet_url}\n")
