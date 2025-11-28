#!/usr/bin/env python3
"""Upload CSV to Google Sheets in batches using Claude Code MCP"""
import csv
import sys

# Read CSV
with open('output/replacement-candidates.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Convert to strings
values = [[str(cell) for cell in row] for row in rows]

print(f"Total rows: {len(values)}")
print(f"Total columns: {len(values[0])}")

# Print in format that can be copied to MCP call
print("\nData ready for mcp__google-sheets__write_cells:")
print(f"spreadsheet_id: 1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI")
print(f"range_name: Replacement Candidates!A1")
print(f"rows: {len(values)}")
print(f"columns: {len(values[0])}")

# Export smaller chunks for manual upload if needed
batch_size = 50
for i in range(0, len(values), batch_size):
    batch = values[i:i+batch_size]
    start_row = i + 1
    end_row = min(i + batch_size, len(values))
    print(f"\nBatch {i//batch_size + 1}: Rows {start_row}-{end_row} ({len(batch)} rows)")
