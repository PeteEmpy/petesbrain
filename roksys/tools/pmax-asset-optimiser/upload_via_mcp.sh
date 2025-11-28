#!/bin/bash
# Upload CSV to Google Sheets using MCP CLI

SPREADSHEET_ID="1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI"

echo "📤 Uploading CSV to Google Sheets..."
echo "   This may take 30-60 seconds..."

# Use the Google Sheets MCP server directly
python3 << 'EOF'
import csv
import json
import subprocess

# Read CSV
with open('output/replacement-candidates.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    values = [[str(cell) for cell in row] for row in reader]

# Try to write all at once
print(f"Uploading {len(values)} rows...")

# Create JSON payload
payload = json.dumps({
    "spreadsheet_id": "1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI",
    "range_name": "Replacement Candidates!A1",
    "values": values
})

# Save to temp file
with open('/tmp/sheets_upload.json', 'w') as f:
    f.write(payload)

print("✅ Data prepared")
print("⚠️  MCP upload not available via CLI")
print("")
print("Please use Google Sheets UI to import:")
print("1. File → Import → Upload")
print("2. Select: output/replacement-candidates.csv")  
print("3. Import location: Replace current sheet")
print("4. Click Import data")
EOF

