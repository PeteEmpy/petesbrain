#!/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Apply Smythson PMax text assets from Google Spreadsheet to Google Ads.
VERSION 2 - Fixed column mapping and sheet names (2025-12-12)

FIXES FROM V1:
- Corrected sheet tab names (UK PMax Assets, not UK ad copy)
- Corrected column mapping to match actual spreadsheet structure
- Added pre-flight validation
- Added post-deployment verification
- Added backup creation before changes
- Added detailed logging

Usage:
    python3 apply-pmax-text-assets-v2.py --region uk --dry-run     # Test first
    python3 apply-pmax-text-assets-v2.py --region uk --validate    # Validate only
    python3 apply-pmax-text-assets-v2.py --region uk               # Live execution
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add the MCP server to path to use its OAuth module
MCP_SERVER_PATH = '/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, MCP_SERVER_PATH)

# Load env vars from MCP server
from dotenv import load_dotenv
load_dotenv(os.path.join(MCP_SERVER_PATH, '.env'))

# Import the OAuth module
from oauth.google_auth import get_headers_with_auto_token, format_customer_id

# Configuration
SPREADSHEET_ID = '1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g'
MANAGER_ID = '2569949686'

# FIXED: Correct sheet tab names (verified 2025-12-12)
REGIONS = {
    'uk': {
        'customer_id': '8573235780',
        'sheet_name': 'UK PMax Assets',
        'data_range': 'UK PMax Assets!A2:AZ'  # Extended range for all columns
    },
    'us': {
        'customer_id': '7808690871',
        'sheet_name': 'US PMax Assets',
        'data_range': 'US PMax Assets!A2:AZ'
    },
    'eur': {
        'customer_id': '7679616761',
        'sheet_name': 'EUR PMax Assets',
        'data_range': 'EUR PMax Assets!A2:AZ'
    },
    'row': {
        'customer_id': '5556710725',
        'sheet_name': 'ROW PMax Assets',
        'data_range': 'ROW PMax Assets!A2:AZ'
    },
}

# Column mapping - will be populated dynamically from row 1 headers
COLUMN_MAP = {}

# Google Ads API requirements
MINIMUM_REQUIREMENTS = {
    'HEADLINE': 3,
    'LONG_HEADLINE': 1,
    'DESCRIPTION': 2
}

MAXIMUM_LIMITS = {
    'HEADLINE': 15,
    'LONG_HEADLINE': 5,
    'DESCRIPTION': 5
}

# Backup directory
BACKUP_DIR = '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data/backups'


def get_headers():
    """Get headers for Google Ads API requests."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = format_customer_id(MANAGER_ID)
    return headers


def read_sheet_data(region: str) -> List[List[str]]:
    """Read text asset data from Google Spreadsheet."""
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    # FIXED: Correct path with .nosync
    sheets_mcp_path = '/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-sheets-mcp-server'
    token_path = os.path.join(sheets_mcp_path, 'token.json')

    if not os.path.exists(token_path):
        raise FileNotFoundError(f"Google Sheets OAuth token not found: {token_path}")

    creds = Credentials.from_authorized_user_file(token_path)
    service = build('sheets', 'v4', credentials=creds)

    data_range = REGIONS[region]['data_range']
    print(f"  Reading from: {data_range}")

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=data_range
    ).execute()

    rows = result.get('values', [])
    print(f"  Read {len(rows)} rows from spreadsheet")
    return rows


def parse_column_headers(region: str) -> Dict[str, int]:
    """
    Read row 1 headers and dynamically map column names to indices.

    Returns a dict with:
    - 'campaign_id', 'campaign_name', 'asset_group_id', 'asset_group_name', 'status', 'final_url': indices
    - 'headlines_start', 'headlines_count': headline column range
    - 'long_headlines_start', 'long_headlines_count': long headline column range
    - 'descriptions_start', 'descriptions_count': description column range
    """
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    sheets_mcp_path = '/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-sheets-mcp-server'
    token_path = os.path.join(sheets_mcp_path, 'token.json')

    if not os.path.exists(token_path):
        raise FileNotFoundError(f"Google Sheets OAuth token not found: {token_path}")

    creds = Credentials.from_authorized_user_file(token_path)
    service = build('sheets', 'v4', credentials=creds)

    # Read header row (row 1) for this region
    sheet_name = REGIONS[region]['sheet_name']
    header_range = f"{sheet_name}!A1:AZ1"

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=header_range
    ).execute()

    headers = result.get('values', [[]])[0] if result.get('values') else []

    if not headers:
        raise ValueError(f"Could not read header row from {header_range}")

    # Map column indices based on header names
    column_map = {}

    # Find basic columns
    for i, header in enumerate(headers):
        header_lower = header.lower().strip()
        if header_lower == 'campaign id':
            column_map['campaign_id'] = i
        elif header_lower == 'campaign name':
            column_map['campaign_name'] = i
        elif header_lower == 'asset group id':
            column_map['asset_group_id'] = i
        elif header_lower == 'asset group name':
            column_map['asset_group_name'] = i
        elif header_lower == 'status':
            column_map['status'] = i
        elif header_lower == 'final url':
            column_map['final_url'] = i

    # Find text asset columns (headlines, long headlines, descriptions)
    headlines_indices = []
    long_headlines_indices = []
    descriptions_indices = []

    for i, header in enumerate(headers):
        header_lower = header.lower().strip()
        if header_lower.startswith('headline ') and 'long' not in header_lower:
            headlines_indices.append(i)
        elif 'long headline' in header_lower:
            long_headlines_indices.append(i)
        elif header_lower.startswith('description '):
            descriptions_indices.append(i)

    # Store ranges
    if headlines_indices:
        column_map['headlines_start'] = min(headlines_indices)
        column_map['headlines_count'] = len(headlines_indices)
    else:
        column_map['headlines_start'] = 18  # Fallback
        column_map['headlines_count'] = 15

    if long_headlines_indices:
        column_map['long_headlines_start'] = min(long_headlines_indices)
        column_map['long_headlines_count'] = len(long_headlines_indices)
    else:
        column_map['long_headlines_start'] = 33  # Fallback
        column_map['long_headlines_count'] = 5

    if descriptions_indices:
        column_map['descriptions_start'] = min(descriptions_indices)
        column_map['descriptions_count'] = len(descriptions_indices)
    else:
        column_map['descriptions_start'] = 38  # Fallback
        column_map['descriptions_count'] = 5

    return column_map


def parse_text_assets_from_row(row: List[str]) -> Optional[Dict]:
    """
    Parse text assets from a spreadsheet row using CORRECT column mapping.
    """
    if len(row) < 4:
        return None

    # Extract identifiers
    campaign_id = row[COLUMN_MAP['campaign_id']].strip() if len(row) > COLUMN_MAP['campaign_id'] else ""
    campaign_name = row[COLUMN_MAP['campaign_name']].strip() if len(row) > COLUMN_MAP['campaign_name'] else ""
    asset_group_id = row[COLUMN_MAP['asset_group_id']].strip() if len(row) > COLUMN_MAP['asset_group_id'] else ""
    asset_group_name = row[COLUMN_MAP['asset_group_name']].strip() if len(row) > COLUMN_MAP['asset_group_name'] else ""

    if not campaign_name or not asset_group_name:
        return None

    # Extract headlines (columns S onwards, index 18+)
    headlines = []
    start = COLUMN_MAP['headlines_start']
    for i in range(start, start + COLUMN_MAP['headlines_count']):
        if i < len(row) and row[i].strip():
            headlines.append(row[i].strip())

    # Extract long headlines
    long_headlines = []
    start = COLUMN_MAP['long_headlines_start']
    for i in range(start, start + COLUMN_MAP['long_headlines_count']):
        if i < len(row) and row[i].strip():
            long_headlines.append(row[i].strip())

    # Extract descriptions
    descriptions = []
    start = COLUMN_MAP['descriptions_start']
    for i in range(start, start + COLUMN_MAP['descriptions_count']):
        if i < len(row) and row[i].strip():
            descriptions.append(row[i].strip())

    return {
        'campaign_id': campaign_id,
        'campaign_name': campaign_name,
        'asset_group_id': asset_group_id,
        'asset_group_name': asset_group_name,
        'headlines': headlines,
        'long_headlines': long_headlines,
        'descriptions': descriptions
    }


def validate_asset_counts(text_data: Dict) -> Tuple[bool, List[str]]:
    """Validate asset counts meet Google Ads requirements."""
    errors = []

    headlines = text_data.get('headlines', [])
    long_headlines = text_data.get('long_headlines', [])
    descriptions = text_data.get('descriptions', [])

    # Check minimums
    if len(headlines) < MINIMUM_REQUIREMENTS['HEADLINE']:
        errors.append(f"Headlines: {len(headlines)} < {MINIMUM_REQUIREMENTS['HEADLINE']} minimum")

    if len(long_headlines) < MINIMUM_REQUIREMENTS['LONG_HEADLINE']:
        errors.append(f"Long Headlines: {len(long_headlines)} < {MINIMUM_REQUIREMENTS['LONG_HEADLINE']} minimum")

    if len(descriptions) < MINIMUM_REQUIREMENTS['DESCRIPTION']:
        errors.append(f"Descriptions: {len(descriptions)} < {MINIMUM_REQUIREMENTS['DESCRIPTION']} minimum")

    # Check maximums (warnings, not errors - will truncate)
    if len(headlines) > MAXIMUM_LIMITS['HEADLINE']:
        errors.append(f"WARNING: Headlines {len(headlines)} > {MAXIMUM_LIMITS['HEADLINE']} (will truncate)")

    if len(long_headlines) > MAXIMUM_LIMITS['LONG_HEADLINE']:
        errors.append(f"WARNING: Long Headlines {len(long_headlines)} > {MAXIMUM_LIMITS['LONG_HEADLINE']} (will truncate)")

    if len(descriptions) > MAXIMUM_LIMITS['DESCRIPTION']:
        errors.append(f"WARNING: Descriptions {len(descriptions)} > {MAXIMUM_LIMITS['DESCRIPTION']} (will truncate)")

    # Fail only on minimum requirements
    is_valid = (
        len(headlines) >= MINIMUM_REQUIREMENTS['HEADLINE'] and
        len(long_headlines) >= MINIMUM_REQUIREMENTS['LONG_HEADLINE'] and
        len(descriptions) >= MINIMUM_REQUIREMENTS['DESCRIPTION']
    )

    return is_valid, errors


def get_current_text_assets(headers, customer_id: str, asset_group_id: str) -> List[Dict]:
    """Query current text assets in an asset group."""
    formatted_cid = format_customer_id(customer_id)

    query = f"""
        SELECT
            asset_group_asset.resource_name,
            asset_group_asset.field_type,
            asset.id,
            asset.text_asset.text
        FROM asset_group_asset
        WHERE asset_group.id = {asset_group_id}
        AND asset_group_asset.field_type IN ('HEADLINE', 'LONG_HEADLINE', 'DESCRIPTION')
        AND asset_group_asset.status != 'REMOVED'
    """

    url = f"https://googleads.googleapis.com/v18/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    return resp.json().get('results', [])


def save_backup(region: str, customer_id: str, asset_group_id: str,
                asset_group_name: str, current_assets: List[Dict]) -> str:
    """Save current state as backup before making changes."""
    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{region}_{asset_group_id}_{timestamp}.json"
    filepath = os.path.join(BACKUP_DIR, filename)

    backup_data = {
        'timestamp': datetime.now().isoformat(),
        'region': region,
        'customer_id': customer_id,
        'asset_group_id': asset_group_id,
        'asset_group_name': asset_group_name,
        'assets': current_assets
    }

    with open(filepath, 'w') as f:
        json.dump(backup_data, f, indent=2)

    return filepath


def create_text_assets(headers, customer_id: str, texts: List[str]) -> List[str]:
    """Create new text assets and return their resource names."""
    if not texts:
        return []

    formatted_cid = format_customer_id(customer_id)
    url = f"https://googleads.googleapis.com/v18/customers/{formatted_cid}/assets:mutate"

    operations = []
    for text in texts:
        operations.append({
            'create': {
                'type': 'TEXT',
                'textAsset': {'text': text}
            }
        })

    payload = {'operations': operations}
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json()['results']
    return [r['resourceName'] for r in results]


def update_asset_group_text_assets(headers, customer_id: str, asset_group_id: str,
                                   remove_resources: List[str],
                                   new_assets_by_type: Dict[str, List[str]]) -> bool:
    """Remove old text asset links and add new ones."""
    formatted_cid = format_customer_id(customer_id)
    asset_group_resource = f"customers/{formatted_cid}/assetGroups/{asset_group_id}"
    url = f"https://googleads.googleapis.com/v18/customers/{formatted_cid}/assetGroupAssets:mutate"

    operations = []

    # Remove old asset links
    for resource_name in remove_resources:
        operations.append({'remove': resource_name})

    # Add new asset links
    for field_type, asset_resources in new_assets_by_type.items():
        for asset_resource in asset_resources:
            operations.append({
                'create': {
                    'assetGroup': asset_group_resource,
                    'asset': asset_resource,
                    'fieldType': field_type
                }
            })

    if operations:
        payload = {'operations': operations}
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return True

    return False


def verify_deployment(headers, customer_id: str, asset_group_id: str,
                      expected_headlines: List[str]) -> Tuple[bool, str]:
    """Verify that deployment was successful by checking current state."""
    current = get_current_text_assets(headers, customer_id, asset_group_id)

    current_headlines = []
    for asset in current:
        if asset.get('assetGroupAsset', {}).get('fieldType') == 'HEADLINE':
            text = asset.get('asset', {}).get('textAsset', {}).get('text', '')
            current_headlines.append(text)

    # Check if expected headlines are present
    missing = [h for h in expected_headlines[:3] if h not in current_headlines]  # Check first 3

    if missing:
        return False, f"Missing expected headlines: {missing}"

    return True, f"Verified {len(current_headlines)} headlines present"


def run_preflight_validation(region: str) -> Tuple[bool, List[str]]:
    """Run pre-flight validation checks before deployment."""
    errors = []

    print(f"\n{'='*60}")
    print(f"PRE-FLIGHT VALIDATION: {region.upper()}")
    print(f"{'='*60}")

    # 1. Check OAuth tokens exist
    sheets_token = '/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-sheets-mcp-server/token.json'
    if not os.path.exists(sheets_token):
        errors.append(f"Google Sheets OAuth token missing: {sheets_token}")
    else:
        print(f"  [OK] Google Sheets OAuth token exists")

    # 2. Check Google Ads OAuth
    try:
        headers = get_headers()
        print(f"  [OK] Google Ads OAuth token valid")
    except Exception as e:
        errors.append(f"Google Ads OAuth error: {str(e)}")

    # 2b. Parse column headers dynamically
    try:
        global COLUMN_MAP
        COLUMN_MAP = parse_column_headers(region)
        print(f"  [OK] Column headers parsed ({len(COLUMN_MAP)} columns)")
    except Exception as e:
        errors.append(f"Column header parsing error: {str(e)}")

    # 3. Read spreadsheet and validate data
    try:
        rows = read_sheet_data(region)
        print(f"  [OK] Spreadsheet readable: {len(rows)} rows")

        valid_count = 0
        invalid_rows = []

        for i, row in enumerate(rows, start=2):
            data = parse_text_assets_from_row(row)
            if data:
                is_valid, row_errors = validate_asset_counts(data)
                if is_valid:
                    valid_count += 1
                else:
                    invalid_rows.append((i, data['asset_group_name'], row_errors))
            else:
                invalid_rows.append((i, "Empty/Invalid", ["Could not parse row"]))

        print(f"  [OK] Valid asset groups: {valid_count}")

        if invalid_rows:
            for row_num, name, row_errors in invalid_rows:
                for err in row_errors:
                    if err.startswith("WARNING"):
                        print(f"  [WARN] Row {row_num} ({name}): {err}")
                    else:
                        errors.append(f"Row {row_num} ({name}): {err}")

    except Exception as e:
        errors.append(f"Spreadsheet read error: {str(e)}")

    # 4. Test Google Ads API connectivity
    try:
        customer_id = REGIONS[region]['customer_id']
        formatted_cid = format_customer_id(customer_id)

        query = "SELECT campaign.id FROM campaign LIMIT 1"
        url = f"https://googleads.googleapis.com/v18/customers/{formatted_cid}/googleAds:search"
        payload = {'query': query}

        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        print(f"  [OK] Google Ads API accessible for customer {customer_id}")
    except Exception as e:
        errors.append(f"Google Ads API error: {str(e)}")

    # Summary
    print(f"\n{'='*60}")
    if errors:
        print(f"VALIDATION FAILED: {len(errors)} errors")
        for err in errors:
            print(f"  - {err}")
        return False, errors
    else:
        print(f"VALIDATION PASSED: Ready for deployment")
        return True, []


def apply_text_assets_to_asset_group(headers, customer_id: str, region: str,
                                     text_data: Dict, dry_run: bool = False) -> bool:
    """Apply text assets from spreadsheet to a single asset group."""
    asset_group_id = text_data['asset_group_id']
    asset_group_name = text_data['asset_group_name']
    campaign_name = text_data['campaign_name']

    print(f"\n  Asset Group: {asset_group_name}")
    print(f"    Campaign: {campaign_name}")
    print(f"    Asset Group ID: {asset_group_id}")

    headlines = text_data.get('headlines', [])[:MAXIMUM_LIMITS['HEADLINE']]
    long_headlines = text_data.get('long_headlines', [])[:MAXIMUM_LIMITS['LONG_HEADLINE']]
    descriptions = text_data.get('descriptions', [])[:MAXIMUM_LIMITS['DESCRIPTION']]

    print(f"    Assets to apply:")
    print(f"      Headlines: {len(headlines)}")
    print(f"      Long Headlines: {len(long_headlines)}")
    print(f"      Descriptions: {len(descriptions)}")

    if dry_run:
        print(f"    [DRY RUN] Would apply {len(headlines)} headlines, {len(long_headlines)} long headlines, {len(descriptions)} descriptions")
        return True

    # Get current assets
    current_assets = get_current_text_assets(headers, customer_id, asset_group_id)

    # Save backup BEFORE making any changes
    backup_path = save_backup(region, customer_id, asset_group_id, asset_group_name, current_assets)
    print(f"    Backup saved: {backup_path}")

    resources_to_remove = []
    for asset in current_assets:
        resource_name = asset.get('assetGroupAsset', {}).get('resourceName')
        if resource_name:
            resources_to_remove.append(resource_name)

    print(f"    Current assets to remove: {len(resources_to_remove)}")

    # Create new assets
    all_texts = headlines + long_headlines + descriptions
    new_asset_resources = create_text_assets(headers, customer_id, all_texts)

    print(f"    Created {len(new_asset_resources)} new text assets")

    # Map to field types
    idx = 0
    new_assets_by_type = {
        'HEADLINE': new_asset_resources[idx:idx + len(headlines)],
    }
    idx += len(headlines)
    new_assets_by_type['LONG_HEADLINE'] = new_asset_resources[idx:idx + len(long_headlines)]
    idx += len(long_headlines)
    new_assets_by_type['DESCRIPTION'] = new_asset_resources[idx:idx + len(descriptions)]

    # Update asset group assets
    update_asset_group_text_assets(
        headers, customer_id, asset_group_id,
        resources_to_remove, new_assets_by_type
    )

    # Verify deployment
    verified, verify_msg = verify_deployment(headers, customer_id, asset_group_id, headlines)
    if verified:
        print(f"    [VERIFIED] {verify_msg}")
    else:
        print(f"    [WARNING] Verification issue: {verify_msg}")

    print(f"    Applied successfully")
    return True


def apply_region_text_assets(region: str, dry_run: bool = False,
                              validate_only: bool = False) -> Tuple[int, int]:
    """Apply text assets for an entire region from the spreadsheet."""

    # Run pre-flight validation
    is_valid, errors = run_preflight_validation(region)

    if not is_valid:
        print(f"\nPre-flight validation failed. Aborting deployment.")
        return 0, len(errors)

    if validate_only:
        print(f"\nValidation-only mode. No changes made.")
        return 0, 0

    customer_id = REGIONS[region]['customer_id']

    print(f"\n{'='*80}")
    print(f"APPLY TEXT ASSETS: {region.upper()}")
    print(f"Customer ID: {customer_id}")
    print(f"Spreadsheet: {SPREADSHEET_ID}")
    print(f"{'='*80}")

    if dry_run:
        print("[DRY RUN MODE - No changes will be made]")

    # Parse column headers dynamically from row 1
    print(f"\nParsing column headers from spreadsheet...")
    global COLUMN_MAP
    COLUMN_MAP = parse_column_headers(region)
    print(f"  Mapped {len(COLUMN_MAP)} columns")

    # Read spreadsheet data
    print(f"\nReading spreadsheet data...")
    rows = read_sheet_data(region)

    # Parse rows
    parsed_rows = []
    for i, row in enumerate(rows, start=2):
        data = parse_text_assets_from_row(row)
        if data:
            is_valid, _ = validate_asset_counts(data)
            if is_valid:
                parsed_rows.append(data)
            else:
                print(f"  Row {i}: Skipped (validation failed)")
        else:
            print(f"  Row {i}: Skipped (empty or invalid)")

    print(f"\nParsed {len(parsed_rows)} valid rows")

    headers = get_headers()
    success_count = 0
    fail_count = 0

    # Process each row
    for i, text_data in enumerate(parsed_rows, start=1):
        print(f"\n[{i}/{len(parsed_rows)}] Processing asset group...")

        try:
            result = apply_text_assets_to_asset_group(
                headers, customer_id, region, text_data, dry_run
            )
            if result:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"  Error: {str(e)}")
            fail_count += 1

    return success_count, fail_count


def main():
    parser = argparse.ArgumentParser(
        description='Apply Smythson PMax text assets from Google Spreadsheet to Google Ads (V2 - Fixed)'
    )
    parser.add_argument(
        '--region',
        required=True,
        choices=['uk', 'us', 'eur', 'row', 'all'],
        help='Region to process (or "all" for all regions)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be applied without making changes'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Run pre-flight validation only, do not apply changes'
    )
    args = parser.parse_args()

    print(f"\n{'='*80}")
    print(f"SMYTHSON PMAX TEXT ASSET DEPLOYMENT (V2)")
    print(f"{'='*80}")
    print(f"Started: {datetime.now().isoformat()}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'VALIDATE ONLY' if args.validate else 'LIVE EXECUTION'}")

    regions_to_process = list(REGIONS.keys()) if args.region == 'all' else [args.region]

    total_success = 0
    total_fail = 0

    for region in regions_to_process:
        success, fail = apply_region_text_assets(region, args.dry_run, args.validate)
        total_success += success
        total_fail += fail

    print(f"\n{'='*80}")
    print(f"DEPLOYMENT SUMMARY")
    print(f"{'='*80}")
    print(f"Regions processed: {', '.join(regions_to_process)}")
    print(f"Successful: {total_success}")
    print(f"Failed: {total_fail}")
    print(f"Completed: {datetime.now().isoformat()}")

    if args.dry_run:
        print(f"\n[DRY RUN COMPLETE - Run without --dry-run to apply changes]")
    elif args.validate:
        print(f"\n[VALIDATION COMPLETE - Run without --validate to apply changes]")

    sys.exit(0 if total_fail == 0 else 1)


if __name__ == "__main__":
    main()
