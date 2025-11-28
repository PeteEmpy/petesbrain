#!/usr/bin/env python3
"""
Download review selections from Google Sheets and prepare execution-ready CSV

This script:
1. Downloads the reviewed data from Google Sheets
2. Filters rows where Action is "One", "Two", or "Three"
3. Maps the selection to the correct replacement text
4. Outputs execution-ready CSV with SWAP actions
"""

import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import csv

SPREADSHEET_ID = "1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI"
SHEET_NAME = "Replacement Candidates"  # The correct sheet with Selected Option column
MCP_TOKEN_PATH = Path('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/token.json')

def download_from_sheets():
    """Download data from Google Sheets"""
    print("📥 Downloading review selections from Google Sheets...")
    print(f"   Spreadsheet ID: {SPREADSHEET_ID}")
    print(f"   Sheet: {SHEET_NAME}\n")

    # Load credentials
    creds = Credentials.from_authorized_user_file(str(MCP_TOKEN_PATH))
    service = build('sheets', 'v4', credentials=creds)

    # Get all data (explicitly request up to column Z to ensure we get all columns)
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:Z"
    ).execute()

    rows = result.get('values', [])
    print(f"✅ Downloaded {len(rows)} rows\n")

    return rows

def prepare_execution_csv(rows):
    """Prepare execution-ready CSV from review selections"""
    print("🔧 Processing selections...")

    if not rows:
        print("❌ No data found")
        return []

    # Header row
    header = rows[0]
    data_rows = rows[1:]

    # Find column indices
    try:
        campaign_idx = header.index('Campaign')
        asset_group_idx = header.index('Asset Group')
        asset_type_idx = header.index('Asset Type')
        current_text_idx = header.index('Current Text')
        option1_idx = header.index('Option 1')
        option2_idx = header.index('Option 2')
        option3_idx = header.index('Option 3')
        selected_idx = header.index('Selected Option (1/2/3 or blank to skip)')
    except ValueError as e:
        print(f"❌ Missing column: {e}")
        print(f"Available columns: {header}")
        return []

    # Process selections
    execution_rows = []

    for row in data_rows:
        if len(row) <= selected_idx:
            continue

        selected = row[selected_idx].strip() if selected_idx < len(row) else ""

        if selected in ["1", "2", "3"]:
            # Get the selected replacement text
            if selected == "1":
                replacement = row[option1_idx] if option1_idx < len(row) else ""
            elif selected == "2":
                replacement = row[option2_idx] if option2_idx < len(row) else ""
            else:  # selected == "3"
                replacement = row[option3_idx] if option3_idx < len(row) else ""

            # We need Campaign_ID and Asset_Group_ID which aren't in this sheet
            # We'll need to look them up from replacement-candidates.csv
            campaign = row[campaign_idx] if campaign_idx < len(row) else ""
            asset_group = row[asset_group_idx] if asset_group_idx < len(row) else ""
            asset_type = row[asset_type_idx] if asset_type_idx < len(row) else ""
            original_text = row[current_text_idx] if current_text_idx < len(row) else ""

            execution_rows.append({
                'Campaign': campaign,
                'Asset_Group': asset_group,
                'Asset_Type': asset_type,
                'Original_Text': original_text,
                'Replacement_Text': replacement,
                'Selected_Option': selected
            })

    print(f"✅ Found {len(execution_rows)} assets selected for execution\n")

    # Show summary
    if execution_rows:
        print("📊 Selections:")
        for row in execution_rows:
            print(f"   {row['Asset_Group']} | {row['Asset_Type']}")
            print(f"      Original: {row['Original_Text'][:50]}...")
            print(f"      New (Option {row['Selected_Option']}): {row['Replacement_Text'][:50]}...")
        print()

    return execution_rows

def lookup_ids_from_candidates(execution_rows):
    """Look up Campaign_ID and Asset_Group_ID from replacement-candidates.csv"""
    print("🔍 Looking up Campaign and Asset Group IDs...")

    # Read replacement-candidates.csv
    candidates_path = Path('output/replacement-candidates.csv')
    if not candidates_path.exists():
        print(f"❌ Cannot find {candidates_path}")
        return []

    # Build lookup map
    lookup = {}
    with open(candidates_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (
                row['Campaign'],
                row['Asset_Group'],
                row['Asset_Type'],
                row['Original_Text']
            )
            lookup[key] = {
                'Campaign_ID': row['Campaign_ID'],
                'Asset_Group_ID': row['Asset_Group_ID']
            }

    # Add IDs to execution rows
    enriched_rows = []
    for row in execution_rows:
        key = (
            row['Campaign'],
            row['Asset_Group'],
            row['Asset_Type'],
            row['Original_Text']
        )

        if key in lookup:
            enriched_rows.append({
                'Campaign_ID': lookup[key]['Campaign_ID'],
                'Asset_Group_ID': lookup[key]['Asset_Group_ID'],
                'Campaign': row['Campaign'],
                'Asset_Group': row['Asset_Group'],
                'Original_Text': row['Original_Text'],
                'Asset_Type': row['Asset_Type'],
                'Replacement_Text': row['Replacement_Text'],
                'Action': 'SWAP'
            })
        else:
            print(f"⚠️  Could not find IDs for: {row['Asset_Group']} | {row['Original_Text'][:40]}")

    print(f"✅ Enriched {len(enriched_rows)} rows with IDs\n")
    return enriched_rows

def write_execution_csv(execution_rows, output_path):
    """Write execution-ready CSV"""
    print(f"💾 Writing execution-ready CSV to: {output_path}")

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Campaign_ID', 'Asset_Group_ID', 'Campaign', 'Asset_Group',
            'Original_Text', 'Asset_Type', 'Replacement_Text', 'Action'
        ])
        writer.writeheader()
        writer.writerows(execution_rows)

    print(f"✅ Wrote {len(execution_rows)} rows\n")

def main():
    print("="*80)
    print("DOWNLOAD & PREPARE EXECUTION CSV")
    print("="*80)
    print()

    # Download from sheets
    rows = download_from_sheets()

    # Prepare execution CSV
    execution_rows = prepare_execution_csv(rows)

    if not execution_rows:
        print("⚠️  No assets selected for execution (all selections blank)")
        print("   Please select assets in Google Sheets (set Selected Option to 1, 2, or 3)")
        return

    # Look up Campaign_ID and Asset_Group_ID
    enriched_rows = lookup_ids_from_candidates(execution_rows)

    if not enriched_rows:
        print("❌ Failed to enrich rows with IDs")
        return

    # Write output
    output_path = Path('output/execution-ready.csv')
    write_execution_csv(enriched_rows, output_path)

    print("="*80)
    print("✅ READY FOR EXECUTION")
    print("="*80)
    print()
    print(f"📁 Execution CSV: {output_path}")
    print()
    print("Next steps:")
    print("1. DRY RUN: .venv/bin/python3 execute_asset_optimisation.py --csv output/execution-ready.csv --dry-run")
    print("2. LIVE RUN: .venv/bin/python3 execute_asset_optimisation.py --csv output/execution-ready.csv")
    print()

if __name__ == "__main__":
    main()
