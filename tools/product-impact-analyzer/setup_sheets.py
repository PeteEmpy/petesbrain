#!/usr/bin/env python3
"""
Setup Google Sheets for Product Impact Analyzer - New Format

This script prepares the spreadsheet for historical data accumulation by:
1. Creating instructions for manual sheet creation (Google Sheets API doesn't support adding sheets via MCP)
2. Writing headers to the new sheets
3. Populating initial test data
4. Verifying the data flow works

Run this after manually creating the 3 new sheets in Google Sheets.
"""

import json
from pathlib import Path
from datetime import datetime

def main():
    print("\n" + "="*80)
    print("PRODUCT IMPACT ANALYZER - GOOGLE SHEETS SETUP")
    print("="*80)
    print()

    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)

    spreadsheet_id = config['spreadsheet_id']
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

    print("STEP 1: CREATE NEW SHEETS")
    print("-" * 80)
    print(f"\n1. Open this spreadsheet in Google Sheets:")
    print(f"   {spreadsheet_url}")
    print()
    print("2. Create 3 new sheets (click the + button at the bottom):")
    print("   - Daily Performance")
    print("   - Impact Analysis")
    print("   - Product Summary")
    print()
    print("3. Once created, come back here and press ENTER to continue...")
    input()

    print("\nSTEP 2: WRITE HEADERS TO NEW SHEETS")
    print("-" * 80)
    print("\nGenerating header write requests...")

    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    # Daily Performance headers
    daily_headers = [
        ["Date", "Client", "Product ID", "Product Title", "Impressions",
         "Clicks", "Conversions", "Revenue (£)", "Cost (£)", "CTR (%)",
         "Conv Rate (%)", "ROAS", "Label"]
    ]

    daily_request = {
        "spreadsheet_id": spreadsheet_id,
        "range": "Daily Performance!A1:M1",
        "values": daily_headers,
        "timestamp": datetime.now().isoformat()
    }

    with open(data_dir / "setup_daily_headers.json", 'w') as f:
        json.dump(daily_request, f, indent=2)

    print("  ✓ Daily Performance headers prepared")

    # Impact Analysis headers
    impact_headers = [
        ["Analysis Date", "Client", "Product ID", "Product Title", "Change Type",
         "Date Changed", "Days Since", "Before Clicks", "After Clicks",
         "Click Change %", "Before Revenue", "After Revenue", "Revenue Change £",
         "Revenue Change %", "Impact Flag", "Label"]
    ]

    impact_request = {
        "spreadsheet_id": spreadsheet_id,
        "range": "Impact Analysis!A1:P1",
        "values": impact_headers,
        "timestamp": datetime.now().isoformat()
    }

    with open(data_dir / "setup_impact_headers.json", 'w') as f:
        json.dump(impact_request, f, indent=2)

    print("  ✓ Impact Analysis headers prepared")

    # Product Summary headers
    summary_headers = [
        ["Client", "Product ID", "Product Title", "Current Label",
         "Last 7D Clicks", "Last 7D Revenue", "Last 30D Clicks",
         "Last 30D Revenue", "ROAS", "Status"]
    ]

    summary_request = {
        "spreadsheet_id": spreadsheet_id,
        "range": "Product Summary!A1:J1",
        "values": summary_headers,
        "timestamp": datetime.now().isoformat()
    }

    with open(data_dir / "setup_summary_headers.json", 'w') as f:
        json.dump(summary_request, f, indent=2)

    print("  ✓ Product Summary headers prepared")
    print()

    print("STEP 3: EXECUTE HEADER WRITES VIA CLAUDE CODE")
    print("-" * 80)
    print("\nClaude Code should now execute these MCP calls:")
    print()
    print("mcp__google-sheets__write_cells(")
    print(f"  spreadsheet_id='{spreadsheet_id}',")
    print("  range_name='Daily Performance!A1:M1',")
    print("  values=[['Date', 'Client', 'Product ID', ...]]")
    print(")")
    print()
    print("mcp__google-sheets__write_cells(")
    print(f"  spreadsheet_id='{spreadsheet_id}',")
    print("  range_name='Impact Analysis!A1:P1',")
    print("  values=[['Analysis Date', 'Client', 'Product ID', ...]]")
    print(")")
    print()
    print("mcp__google-sheets__write_cells(")
    print(f"  spreadsheet_id='{spreadsheet_id}',")
    print("  range_name='Product Summary!A1:J1',")
    print("  values=[['Client', 'Product ID', 'Product Title', ...]]")
    print(")")
    print()
    print("After Claude Code executes these, press ENTER to continue...")
    input()

    print("\nSTEP 4: TEST DATA FLOW")
    print("-" * 80)
    print("\nRunning test to verify data can be written...")
    print()
    print("Run: python3 sheets_writer.py")
    print()
    print("This will generate a test write request that Claude Code should execute.")
    print()

    print("\n" + "="*80)
    print("SETUP COMPLETE")
    print("="*80)
    print()
    print("Next steps:")
    print("1. The daily monitor (10 AM) will now append to 'Daily Performance'")
    print("2. The weekly analyzer (Tuesday 9 AM) will append to 'Impact Analysis'")
    print("3. Monitor the accumulation over the next week")
    print()
    print("Old per-client sheets (Current/Previous/Changes) can be:")
    print("- Left as-is (they won't be updated anymore)")
    print("- Moved to an 'Archive' folder in the spreadsheet")
    print("- Deleted if you don't need them")
    print()
    print("Documentation: See SHEETS-PERSISTENCE.md for details")
    print()


if __name__ == "__main__":
    main()
