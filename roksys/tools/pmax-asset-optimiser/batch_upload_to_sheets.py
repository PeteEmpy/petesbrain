#!/usr/bin/env python3
"""
Batch upload CSV to Google Sheets via subprocess calls to claude mcp
Since we can't call MCP tools directly from Python, we'll output instructions
"""

import csv
import json
from pathlib import Path

SPREADSHEET_ID = "1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI"
BATCH_SIZE = 50

def main():
    # Read CSV
    csv_path = Path(__file__).parent / 'output' / 'replacement-candidates.csv'

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        all_rows = [[str(cell) for cell in row] for row in reader]

    print(f"Total rows: {len(all_rows)}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Number of batches: {(len(all_rows) + BATCH_SIZE - 1) // BATCH_SIZE}")
    print()

    # Create batch files
    for i in range(0, len(all_rows), BATCH_SIZE):
        batch_num = (i // BATCH_SIZE) + 1
        batch = all_rows[i:i+BATCH_SIZE]
        start_row = i + 1

        # Save batch to JSON file
        batch_file = Path(__file__).parent / 'output' / f'batch_{batch_num}.json'
        with open(batch_file, 'w') as f:
            json.dump(batch, f, indent=2)

        print(f"Batch {batch_num}: Rows {start_row}-{start_row + len(batch) - 1} ({len(batch)} rows)")
        print(f"   Saved to: {batch_file.name}")
        print(f"   Range: Replacement Candidates!A{start_row}")
        print()

    print("=" * 80)
    print("BATCH FILES CREATED")
    print("=" * 80)
    print()
    print("To upload, you would need to call the MCP tool for each batch.")
    print("However, since there are 277 rows, the easiest approach is:")
    print()
    print("📋 RECOMMENDED: Use Google Sheets UI Import")
    print("   1. Open the sheet (already open in browser)")
    print("   2. File → Import → Upload")
    print(f"   3. Select: {csv_path}")
    print("   4. Import location: Replace current sheet")
    print("   5. Click 'Import data'")
    print()
    print("This will upload all 277 rows in one step.")

if __name__ == "__main__":
    main()
