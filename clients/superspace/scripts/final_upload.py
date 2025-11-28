#!/usr/bin/env python3
"""
Final upload script - prepares US data in the exact format needed.
"""
import json

# Load the data
with open('us-data-for-upload.json', 'r') as f:
    us_data = json.load(f)

print(f"Loaded {len(us_data)} rows")
print(f"First row: {us_data[0]}")
print(f"Last row: {us_data[-1]}")

# Output the data structure needed for the MCP tool
print("\nData is ready for mcp__google-drive__updateGoogleSheet")
print(f"spreadsheetId: 138tHMTm16uwBMfbJv9UNPYoVb3gX7geEuDgvVY8_pOo")
print(f"range: US!A1")
print(f"data: {len(us_data)} rows x {len(us_data[0])} columns")

# Save in a format that's easy to copy-paste if needed
with open('us_upload_cmd.txt', 'w') as f:
    f.write(f"{len(us_data)} rows ready for upload\n")
