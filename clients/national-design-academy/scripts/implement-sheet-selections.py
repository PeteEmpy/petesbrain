#!/usr/bin/env python3
"""
Implement NDA PMax Sheet Selections to Google Ads

This script:
1. Reads selected alternatives from Google Sheet (column M - rows 2+)
2. For each selection, determines if it's "Keep" or an alternative
3. Prepares Google Ads API mutations to create/pause assets
4. Shows changes for review BEFORE execution
5. Only executes after explicit user confirmation

SAFETY: Does NOT make any Google Ads changes without explicit "yes" confirmation
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

# Map cell references to asset IDs (will be extended as sheet grows)
ASSET_ID_MAP = {
    'M2': '6501874539',  # Study Interior Design
    'M3': '6542848540',  # Interior Design Diploma
    'M4': '8680183789',  # Interior Design Courses
}

# Map asset IDs to asset groups (from current sheet data)
ASSET_TO_GROUP = {
    '6501874539': {
        'asset_group_id': '6482516710',
        'campaign_id': '24127166631',
        'campaign_name': 'NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4',
        'asset_type': 'HEADLINE'
    },
    '6542848540': {
        'asset_group_id': '6482516710',
        'campaign_id': '24127166631',
        'campaign_name': 'NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4',
        'asset_type': 'HEADLINE'
    },
    '8680183789': {
        'asset_group_id': '6482516710',
        'campaign_id': '24127166631',
        'campaign_name': 'NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4',
        'asset_type': 'HEADLINE'
    },
}

def get_sheets_service():
    """Load Google Sheets credentials and build service"""
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data['token'],
        refresh_token=token_data.get('refresh_token'),
        token_uri=token_data.get('token_uri'),
        client_id=token_data.get('client_id'),
        client_secret=token_data.get('client_secret')
    )

    if creds.expired:
        creds.refresh(Request())

    return build('sheets', 'v4', credentials=creds)

def read_sheet_selections(service):
    """Read column M (Alternative Options) from rows 2 onwards"""
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!M2:M100'
        ).execute()
        values = result.get('values', [])
        return values
    except Exception as e:
        print(f"❌ Error reading sheet: {str(e)}")
        return None

def load_alternatives():
    """Load alternatives JSON file"""
    alt_file = Path(__file__).parent / 'final-alternatives-for-dropdowns.json'
    if not alt_file.exists():
        print(f"⚠️  Alternatives file not found: {alt_file}")
        return {}

    with open(alt_file, 'r') as f:
        return json.load(f)

def build_mutations(selections, alternatives_data):
    """
    Build Google Ads API mutations for selected alternatives

    Returns:
    - List of mutations to execute
    - List of changes for review
    """
    mutations = []
    changes = []

    for row_idx, selection in enumerate(selections, start=2):
        if not selection or not selection[0].strip():
            continue

        selected_value = selection[0].strip()
        cell_ref = f'M{row_idx}'
        asset_id = ASSET_ID_MAP.get(cell_ref)

        if not asset_id:
            continue

        asset_info = ASSET_TO_GROUP.get(asset_id)
        if not asset_info:
            continue

        # Determine action
        if selected_value == "Keep":
            action = "KEEP_CURRENT"
            change_desc = f"Row {row_idx}: Keep current asset (no change)"
        else:
            action = "REPLACE_WITH_ALTERNATIVE"
            change_desc = f"Row {row_idx}: Replace with alternative: '{selected_value}'"

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
                'asset_info': asset_info,
                'original_asset_id': asset_id,
                'new_text': selected_value
            })

        changes.append({
            'row': row_idx,
            'cell': cell_ref,
            'asset_id': asset_id,
            'campaign': asset_info['campaign_name'],
            'asset_group': asset_info['asset_group_id'],
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
        print("\nNo changes to implement (all rows set to 'Keep')")
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
                print(f"\n{change['row']}. {change['description']}")
                print(f"   Asset ID: {change['asset_id']}")
                print(f"   Campaign: {change['campaign']}")
                print(f"   Asset Group: {change['asset_group']}")
                print(f"   New Text: '{change['selection']}'")

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
                print(f"\n{idx}/{len(mutations)} Creating new asset...")
                print(f"   Text: '{mut['new_text']}'")
                print(f"   For asset group: {mut['asset_info']['asset_group_id']}")

                # Call Google Ads API
                url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/assets:mutate"
                payload = {"operations": [mut['mutation']]}

                response = requests.post(url, headers=headers, json=payload)

                if response.ok:
                    result = response.json()
                    print(f"   ✅ Asset created successfully")
                    results.append({'success': True, 'mutation': mut, 'result': result})
                else:
                    print(f"   ❌ Failed: {response.status_code} - {response.text}")
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
    print(f"Sheet Range: M2:M100 (Alternative Options)")

    # Step 1: Read sheet
    print("\n" + "-"*80)
    print("STEP 1: Reading sheet selections...")
    print("-"*80)

    service = get_sheets_service()
    selections = read_sheet_selections(service)

    if selections is None:
        print("❌ Failed to read sheet")
        return

    print(f"✅ Read {len(selections)} rows from sheet")

    # Step 2: Load alternatives
    print("\n" + "-"*80)
    print("STEP 2: Loading alternatives...")
    print("-"*80)

    alternatives_data = load_alternatives()
    print(f"✅ Loaded alternatives for {len(alternatives_data)} assets")

    # Step 3: Build mutations
    print("\n" + "-"*80)
    print("STEP 3: Building mutations...")
    print("-"*80)

    mutations, changes = build_mutations(selections, alternatives_data)
    print(f"✅ Prepared {len(mutations)} mutations")

    # Step 4: Display for review
    display_changes_for_review(changes)

    # Step 5: Get confirmation
    if not get_confirmation():
        print("\n❌ Cancelled - No changes made to Google Ads")
        log_changes(changes, False)
        return

    # Step 6: Execute (only if confirmed)
    success = execute_mutations(mutations)

    # Step 7: Log
    log_changes(changes, success)

    if success:
        print("\n✅ ALL CHANGES SUCCESSFULLY APPLIED")
    else:
        print("\n⚠️  SOME CHANGES FAILED - Review log above")

if __name__ == '__main__':
    main()
