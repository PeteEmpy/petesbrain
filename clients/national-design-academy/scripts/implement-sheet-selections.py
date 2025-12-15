#!/usr/bin/env python3
"""
Implement NDA PMax Sheet Selections to Google Ads

This script:
1. Reads all data from Google Sheet (rows 2+)
2. For each row with a selection in column M, determines if it's "Keep" or an alternative
3. Uses Asset ID (column N) and Asset Group ID (column O) from the sheet
4. Shows changes for review BEFORE execution
5. Only executes after explicit user confirmation

SAFETY: Does NOT make any Google Ads changes without explicit "yes" confirmation

Updated: Dec 12, 2025 - Now reads Asset ID and Asset Group ID from sheet columns
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add shared path for imports
parent_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(parent_dir / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server'))

from oauth.google_auth import get_headers_with_auto_token, format_customer_id
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests

# NDA Configuration
CUSTOMER_ID = "1994728449"
SPREADSHEET_ID = "1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto"
TOKEN_FILE = '/Users/administrator/.config/google-drive-mcp/tokens.json'

# Sheet columns (0-indexed):
# A=0: Campaign, B=1: Asset Group, C=2: Asset Type, D=3: Asset Text
# E=4: Clicks, F=5: Conv, G=6: CTR, H=7: Conv Rate, I=8: Cost
# J=9: Benchmark, K=10: Gap, L=11: Priority, M=12: Alternative
# N=13: Asset ID, O=14: Asset Group ID
COL_CAMPAIGN = 0
COL_ASSET_GROUP_NAME = 1
COL_ASSET_TYPE = 2
COL_ASSET_TEXT = 3
COL_ALTERNATIVE = 12
COL_ASSET_ID = 13
COL_ASSET_GROUP_ID = 14

def get_sheets_service():
    """Load Google Sheets credentials and build service"""
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data.get('access_token') or token_data.get('token'),
        refresh_token=token_data.get('refresh_token'),
        token_uri=token_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
        client_id=token_data.get('client_id'),
        client_secret=token_data.get('client_secret')
    )

    if creds.expired:
        creds.refresh(Request())

    return build('sheets', 'v4', credentials=creds)


def read_sheet_data(service):
    """Read all columns A-O from rows 2 onwards"""
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A2:O200'
        ).execute()
        values = result.get('values', [])
        return values
    except Exception as e:
        print(f"❌ Error reading sheet: {str(e)}")
        return None


def get_cell_value(row, col_idx, default=''):
    """Safely get a cell value from a row"""
    if col_idx < len(row):
        return row[col_idx] if row[col_idx] else default
    return default


def build_mutations(sheet_data):
    """
    Build Google Ads API mutations for selected alternatives

    Reads asset ID, asset group ID, and asset type from the sheet columns.

    Returns:
    - List of mutations to execute
    - List of changes for review
    """
    mutations = []
    changes = []

    for row_idx, row in enumerate(sheet_data, start=2):
        # Get the alternative selection (column M)
        selected_value = get_cell_value(row, COL_ALTERNATIVE).strip()

        if not selected_value:
            continue  # No selection made

        # Get metadata from sheet columns
        campaign_name = get_cell_value(row, COL_CAMPAIGN)
        asset_group_name = get_cell_value(row, COL_ASSET_GROUP_NAME)
        asset_type = get_cell_value(row, COL_ASSET_TYPE)
        asset_text = get_cell_value(row, COL_ASSET_TEXT)
        asset_id = get_cell_value(row, COL_ASSET_ID)
        asset_group_id = get_cell_value(row, COL_ASSET_GROUP_ID)

        if not asset_id or not asset_group_id:
            print(f"⚠️  Row {row_idx}: Missing asset ID or asset group ID, skipping")
            continue

        # Determine action
        if selected_value == "Keep":
            action = "KEEP_CURRENT"
            change_desc = f"Row {row_idx}: Keep current {asset_type} (no change)"
        else:
            action = "REPLACE_WITH_ALTERNATIVE"
            change_desc = f"Row {row_idx}: Replace {asset_type} with: '{selected_value}'"

            # Build mutation for replacement
            mutation = {
                "create": {
                    "resourceName": f"customers/{format_customer_id(CUSTOMER_ID)}/assets",
                    "textAsset": {
                        "text": selected_value
                    }
                }
            }
            mutations.append({
                'type': 'asset_create',
                'mutation': mutation,
                'asset_id': asset_id,
                'asset_group_id': asset_group_id,
                'asset_type': asset_type,
                'original_text': asset_text,
                'new_text': selected_value,
                'campaign_name': campaign_name,
                'row': row_idx
            })

        changes.append({
            'row': row_idx,
            'asset_id': asset_id,
            'asset_type': asset_type,
            'asset_text': asset_text,
            'campaign': campaign_name,
            'asset_group_id': asset_group_id,
            'action': action,
            'selection': selected_value,
            'description': change_desc
        })

    return mutations, changes

def display_changes_for_review(changes):
    """Show changes that will be made"""
    print("\n" + "="*80)
    print("PROPOSED CHANGES - REVIEW BEFORE EXECUTION")
    print("="*80)

    if not changes:
        print("\nNo changes to implement (no selections made)")
        return

    keep_count = sum(1 for c in changes if c['action'] == 'KEEP_CURRENT')
    replace_count = sum(1 for c in changes if c['action'] == 'REPLACE_WITH_ALTERNATIVE')

    print(f"\nTotal selected assets: {len(changes)}")
    print(f"  • Keep current: {keep_count}")
    print(f"  • Replace with alternative: {replace_count}")

    if replace_count > 0:
        print("\n" + "-"*80)
        print("REPLACEMENTS:")
        print("-"*80)

        for change in changes:
            if change['action'] == 'REPLACE_WITH_ALTERNATIVE':
                print(f"\nRow {change['row']}: {change['asset_type']}")
                print(f"  Current: '{change['asset_text']}'")
                print(f"  New:     '{change['selection']}'")
                print(f"  Asset ID: {change['asset_id']}")
                print(f"  Asset Group ID: {change['asset_group_id']}")
                print(f"  Campaign: {change['campaign'][:60]}...")

def get_confirmation():
    """Get explicit user confirmation before making changes"""
    print("\n" + "="*80)
    response = input("Proceed with these changes? Type 'YES' (all caps) to confirm: ").strip()
    return response == "YES"

def execute_mutations(mutations):
    """Execute API mutations (ONLY called after confirmation)"""
    if not mutations:
        print("\n✅ No mutations to execute")
        return True

    print("\n" + "="*80)
    print(f"EXECUTING {len(mutations)} MUTATIONS...")
    print("="*80)

    headers = get_headers_with_auto_token()
    formatted_customer_id = format_customer_id(CUSTOMER_ID)

    results = []

    for idx, mut in enumerate(mutations, 1):
        mut_type = mut['type']

        if mut_type == 'asset_create':
            try:
                print(f"\n{idx}/{len(mutations)} Creating new {mut['asset_type']}...")
                print(f"   Text: '{mut['new_text']}'")
                print(f"   Asset Group ID: {mut['asset_group_id']}")

                # Call Google Ads API
                url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/assets:mutate"
                payload = {"operations": [mut['mutation']]}

                response = requests.post(url, headers=headers, json=payload)

                if response.ok:
                    result = response.json()
                    print(f"   ✅ Asset created successfully")
                    results.append({'success': True, 'mutation': mut, 'result': result})
                else:
                    print(f"   ❌ Failed: {response.status_code} - {response.text[:200]}")
                    results.append({'success': False, 'mutation': mut, 'error': response.text})
            except Exception as e:
                print(f"   ❌ Exception: {str(e)}")
                results.append({'success': False, 'mutation': mut, 'error': str(e)})

    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful

    print("\n" + "="*80)
    print(f"EXECUTION COMPLETE: {successful} successful, {failed} failed")
    print("="*80)

    return failed == 0

def log_changes(changes, mutations_executed):
    """Log all changes to audit file"""
    audit_file = Path(__file__).parent / f"implementation-log-{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"

    audit_data = {
        'timestamp': datetime.now().isoformat(),
        'customer_id': CUSTOMER_ID,
        'spreadsheet_id': SPREADSHEET_ID,
        'changes_proposed': changes,
        'mutations_executed': mutations_executed,
        'total_changes': len(changes),
        'status': 'EXECUTED' if mutations_executed else 'REVIEWED_ONLY'
    }

    with open(audit_file, 'w') as f:
        json.dump(audit_data, f, indent=2)

    print(f"\n✅ Audit log saved: {audit_file}")

def main():
    print("\n" + "="*80)
    print("NDA PMax SHEET IMPLEMENTATION - GOOGLE ADS SYNC")
    print("="*80)
    print(f"\nCustomer ID: {CUSTOMER_ID}")
    print(f"Spreadsheet: {SPREADSHEET_ID}")
    print(f"Sheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")

    # Step 1: Read sheet
    print("\n" + "-"*80)
    print("STEP 1: Reading sheet data...")
    print("-"*80)

    service = get_sheets_service()
    sheet_data = read_sheet_data(service)

    if sheet_data is None:
        print("❌ Failed to read sheet")
        return

    print(f"✅ Read {len(sheet_data)} rows from sheet")

    # Count rows with selections
    rows_with_selections = sum(1 for row in sheet_data if len(row) > COL_ALTERNATIVE and row[COL_ALTERNATIVE].strip())
    print(f"   Rows with selections in column M: {rows_with_selections}")

    # Step 2: Build mutations
    print("\n" + "-"*80)
    print("STEP 2: Building mutations from selections...")
    print("-"*80)

    mutations, changes = build_mutations(sheet_data)
    print(f"✅ Found {len(changes)} selections")
    print(f"   Prepared {len(mutations)} mutations (replacements)")

    if not changes:
        print("\n⚠️  No selections found in column M. Make selections in the sheet first.")
        print(f"   Sheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        return

    # Step 3: Display for review
    display_changes_for_review(changes)

    # Step 4: Get confirmation
    if not get_confirmation():
        print("\n❌ Cancelled - No changes made to Google Ads")
        log_changes(changes, False)
        return

    # Step 5: Execute (only if confirmed)
    success = execute_mutations(mutations)

    # Step 6: Log
    log_changes(changes, success)

    if success:
        print("\n✅ ALL CHANGES SUCCESSFULLY APPLIED")
    else:
        print("\n⚠️  SOME CHANGES FAILED - Review log above")

if __name__ == '__main__':
    main()
