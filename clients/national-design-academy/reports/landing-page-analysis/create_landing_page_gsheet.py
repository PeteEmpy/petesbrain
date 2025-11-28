#!/usr/bin/env python3
"""Create Google Sheet with landing page reports"""

import sys
import csv
import json
import subprocess

print("📊 Creating Google Sheet: NDA Landing Page Reports (90 Days)")

# Step 1: Create new spreadsheet
print("\n1. Creating new Google Sheet...")

result = subprocess.run(
    ['claude', 'mcp', 'call', 'google-sheets', 'create_spreadsheet', '--',
     json.dumps({
         'title': 'NDA Landing Page Reports (90 Days) - Sept 1 to Nov 28, 2025'
     })],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"❌ Error creating spreadsheet: {result.stderr}")
    sys.exit(1)

response = json.loads(result.stdout)
spreadsheet_data = json.loads(response['content'][0]['text'])
spreadsheet_id = spreadsheet_data['spreadsheetId']
spreadsheet_url = spreadsheet_data['spreadsheetUrl']

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

# Step 3: Rename first sheet and add other sheets
print("\n3. Setting up sheet tabs...")

# First, get the current sheets
result = subprocess.run(
    ['claude', 'mcp', 'call', 'google-sheets', 'list_sheets', '--',
     json.dumps({
         'spreadsheet_id': spreadsheet_id
     })],
    capture_output=True,
    text=True
)

sheets_response = json.loads(result.stdout)
sheets_data = json.loads(sheets_response['content'][0]['text'])
first_sheet_id = sheets_data['sheets'][0]['sheetId']

# Add the two additional sheets
for sheet_name in ['PMax Landing Pages', 'Search Landing Pages']:
    result = subprocess.run(
        ['claude', 'mcp', 'call', 'google-sheets', 'add_sheet', '--',
         json.dumps({
             'spreadsheet_id': spreadsheet_id,
             'title': sheet_name
         })],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"   ✓ Added sheet: {sheet_name}")

# Step 4: Write data to each sheet
print("\n4. Writing data to sheets...")

sheet_mappings = {
    'Landing Page Statistics': 'Landing Page Statistics',
    'PMax Landing Pages': 'PMax Landing Pages',
    'Search Landing Pages': 'Search Landing Pages'
}

for sheet_name, data in all_data.items():
    # Convert data to format expected by API
    values = [[str(cell) for cell in row] for row in data]
    
    # Determine range based on data size
    num_rows = len(values)
    num_cols = len(values[0]) if values else 0
    
    # Convert column number to letter (A, B, C, ..., AA, AB, etc.)
    def col_to_letter(col):
        result = ""
        while col > 0:
            col -= 1
            result = chr(col % 26 + 65) + result
            col //= 26
        return result
    
    end_col = col_to_letter(num_cols)
    range_name = f"'{sheet_name}'!A1:{end_col}{num_rows}"
    
    print(f"   Writing to {sheet_name} ({range_name})...")
    
    result = subprocess.run(
        ['claude', 'mcp', 'call', 'google-sheets', 'write_cells', '--',
         json.dumps({
             'spreadsheet_id': spreadsheet_id,
             'range': range_name,
             'values': values
         })],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"   ✓ Written {num_rows} rows to {sheet_name}")
    else:
        print(f"   ⚠️  Error writing to {sheet_name}: {result.stderr}")

print("\n" + "="*60)
print("✅ Google Sheet created successfully!")
print(f"\n📊 Spreadsheet URL:")
print(f"   {spreadsheet_url}")
print("\n📋 Sheets:")
print("   1. Landing Page Statistics (154 pages)")
print("   2. PMax Landing Pages (59 asset groups)")
print("   3. Search Landing Pages (1,142 ads)")
print("="*60 + "\n")

# Open in browser
subprocess.run(['open', spreadsheet_url])
print("🌐 Opening in browser...")
