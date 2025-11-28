#!/usr/bin/env python3
"""
Auto-upload all CSV data to Google Sheets in chunks
Uses direct write operations to avoid parameter size issues
"""

import csv
import time
from pathlib import Path

# Google Sheets MCP tool (imported if available)
try:
    # Try to use the MCP tools module if it exists in the environment
    # This would require being run in Claude Code's context
    print("Note: This script needs to be enhanced to call MCP tools")
    print("For now, it will create the upload data files")
except:
    pass

def main():
    SPREADSHEET_ID = "1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI"
    CHUNK_SIZE = 50

    # Read CSV
    csv_path = Path(__file__).parent / 'output' / 'replacement-candidates.csv'

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        all_rows = [[str(cell) for cell in row] for row in reader]

    print(f"=" * 80)
    print(f"AUTO-UPLOAD TO GOOGLE SHEETS")
    print(f"=" * 80)
    print(f"Total rows: {len(all_rows)}")
    print(f"Chunk size: {CHUNK_SIZE}")
    print(f"")

    # Split into chunks
    chunks = []
    for i in range(0, len(all_rows), CHUNK_SIZE):
        chunk = all_rows[i:i+CHUNK_SIZE]
        start_row = i + 1
        chunks.append({
            'start_row': start_row,
            'range': f"Replacement Candidates!A{start_row}",
            'data': chunk
        })

    print(f"Uploading {len(chunks)} chunks...")
    print(f"")

    # Save chunks to files for manual MCP calls
    for idx, chunk_info in enumerate(chunks):
        chunk_num = idx + 1
        filename = f"chunk_{chunk_num}_data.json"
        filepath = Path(__file__).parent / 'output' / filename

        import json
        with open(filepath, 'w') as f:
            json.dump(chunk_info['data'], f)

        print(f"Chunk {chunk_num}/{len(chunks)}: {len(chunk_info['data'])} rows → {chunk_info['range']}")
        print(f"  Saved to: {filename}")

    print(f"")
    print(f"=" * 80)
    print(f"CHUNKS PREPARED")
    print(f"=" * 80)
    print(f"")
    print(f"To upload these chunks, Claude Code needs to call the MCP tool for each:")
    print(f"")
    for idx, chunk_info in enumerate(chunks):
        chunk_num = idx + 1
        print(f"  Chunk {chunk_num}: mcp__google-sheets__write_cells(")
        print(f"    spreadsheet_id='{SPREADSHEET_ID}',")
        print(f"    range_name='{chunk_info['range']}',")
        print(f"    values=<data from chunk_{chunk_num}_data.json>")
        print(f"  )")
        print(f"")

if __name__ == "__main__":
    main()
