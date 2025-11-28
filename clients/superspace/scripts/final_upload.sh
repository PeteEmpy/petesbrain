#!/bin/bash
# Upload US data using CSV to Google Sheets write_cells

cd /Users/administrator/Documents/PetesBrain/clients/superspace

echo "Converting CSV to format for Google Sheets..."
python3 << 'PYEND'
import csv
import json

# Read US data
with open('us-data-new.csv', 'r') as f:
    reader = csv.reader(f)
    us_data = list(reader)

print(f"Total rows: {len(us_data)}")

# The mcp__google-sheets__write_cells tool expects a specific format
# Let's create the properly formatted data structure

# Save as plain JSON array for easier handling
with open('us-final.json', 'w') as f:
    json.dump(us_data, f)

print("Data ready for upload")
print("Please use the Claude Code MCP tool to upload this data:")
print("  spreadsheet_id: 138tHMTm16uwBMfbJv9UNPYoVb3gX7geEuDgvVY8_pOo")
print("  range_name: US!A1")
print("  values: (from us-final.json)")
PYEND
