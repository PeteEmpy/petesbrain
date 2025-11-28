#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Apply Smythson PMax text assets from Google Spreadsheet to Google Ads.

Reads text assets from the master Google Spreadsheet and applies them to
Performance Max asset groups via the Google Ads API.

Usage:
    python3 apply-text-assets-from-sheet.py --region uk --dry-run
    python3 apply-text-assets-from-sheet.py --region all --dry-run
    python3 apply-text-assets-from-sheet.py --region uk  # live execution
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime
from typing import Dict, List, Optional

# Add the MCP server to path to use its OAuth module
MCP_SERVER_PATH = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, MCP_SERVER_PATH)

# Load env vars from MCP server
from dotenv import load_dotenv
load_dotenv(os.path.join(MCP_SERVER_PATH, '.env'))

# Import the OAuth module
from oauth.google_auth import get_headers_with_auto_token, format_customer_id

# Configuration
SPREADSHEET_ID = '1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g'
MANAGER_ID = '2569949686'

REGIONS = {
    'uk': {
        'customer_id': '8573235780',
        'sheet_name': 'UK ad copy',
        'data_range': 'UK ad copy!A2:AA'  # Skip header row
    },
    'us': {
        'customer_id': '7808690871',
        'sheet_name': 'US ad copy',
        'data_range': 'US ad copy!A2:AA'
    },
    'eur': {
        'customer_id': '7679616761',
        'sheet_name': 'EUR ad copy',
        'data_range': 'EUR ad copy!A2:AA'
    },
    'row': {
        'customer_id': '5556710725',
        'sheet_name': 'ROW ad copy',
        'data_range': 'ROW ad copy!A2:AA'
    },
}

# Minimum requirements per Google Ads API
MINIMUM_REQUIREMENTS = {
    'HEADLINE': 3,
    'LONG_HEADLINE': 1,
    'DESCRIPTION': 2
}

# Maximum limits per Google Ads API
MAXIMUM_LIMITS = {
    'HEADLINE': 15,
    'LONG_HEADLINE': 5,
    'DESCRIPTION': 5
}


def get_headers():
    """Get headers for Google Ads API requests."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = format_customer_id(MANAGER_ID)
    return headers


def read_sheet_data(region: str) -> List[List[str]]:
    """
    Read text asset data from Google Spreadsheet using Google Sheets API.

    Uses the Google Sheets MCP server OAuth credentials.
    """
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    # Path to Google Sheets MCP server OAuth token
    sheets_mcp_path = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server'
    token_path = os.path.join(sheets_mcp_path, 'token.json')

    if not os.path.exists(token_path):
        raise FileNotFoundError(f"Google Sheets OAuth token not found: {token_path}")

    # Load credentials
    creds = Credentials.from_authorized_user_file(token_path)

    # Build the service
    service = build('sheets', 'v4', credentials=creds)

    # Read data
    data_range = REGIONS[region]['data_range']
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=data_range
    ).execute()

    rows = result.get('values', [])
    print(f"  Read {len(rows)} rows from spreadsheet")
    return rows


def parse_text_assets_from_row(row: List[str]) -> Dict:
    """
    Parse text assets from a spreadsheet row.

    Column mapping (0-indexed):
    - A (0): Campaign Name
    - B (1): Asset Group Name
    - C-Q (2-16): Headlines 1-15
    - R-V (17-21): Long Headlines 1-5
    - W-AA (22-26): Descriptions 1-5
    """
    if len(row) < 2:
        return None

    campaign_name = row[0].strip() if len(row) > 0 else ""
    asset_group_name = row[1].strip() if len(row) > 1 else ""

    if not campaign_name or not asset_group_name:
        return None

    # Extract headlines (columns C-Q, indices 2-16, max 15)
    headlines = []
    for i in range(2, min(17, len(row))):
        text = row[i].strip() if i < len(row) else ""
        if text:
            headlines.append(text)

    # Extract long headlines (columns R-V, indices 17-21, max 5)
    long_headlines = []
    for i in range(17, min(22, len(row))):
        text = row[i].strip() if i < len(row) else ""
        if text:
            long_headlines.append(text)

    # Extract descriptions (columns W-AA, indices 22-26, max 5)
    descriptions = []
    for i in range(22, min(27, len(row))):
        text = row[i].strip() if i < len(row) else ""
        if text:
            descriptions.append(text)

    return {
        'campaign_name': campaign_name,
        'asset_group_name': asset_group_name,
        'headlines': headlines,
        'long_headlines': long_headlines,
        'descriptions': descriptions
    }


def find_asset_group_id(headers, customer_id: str, campaign_name: str,
                         asset_group_name: str) -> Optional[str]:
    """
    Find asset group ID by campaign name and asset group name.

    SAFETY IMPROVEMENTS (2025-11-27):
    - Filters by customer_id to prevent cross-account matching
    - Validates only ONE match found (prevents ambiguous results)
    - Raises clear errors if no match or multiple matches found
    """
    formatted_cid = format_customer_id(customer_id)

    # SAFETY NOTE: Customer ID is already filtered by the API endpoint URL
    # The URL includes /customers/{formatted_cid}/ which scopes all results to that customer
    # No need to filter by customer ID in the query - that field doesn't exist in GAQL
    query = f"""
        SELECT
            asset_group.id,
            asset_group.name,
            campaign.id,
            campaign.name
        FROM asset_group
        WHERE campaign.status != 'REMOVED'
        AND asset_group.status != 'REMOVED'
    """

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])

    # SAFETY FIX 2: Collect ALL matches first (don't return on first match)
    matches = []
    for result in results:
        camp_name = result.get('campaign', {}).get('name', '')
        ag_name = result.get('assetGroup', {}).get('name', '')

        if camp_name == campaign_name and ag_name == asset_group_name:
            ag_id = str(result.get('assetGroup', {}).get('id'))
            camp_id = str(result.get('campaign', {}).get('id'))
            matches.append((ag_id, camp_id, camp_name, ag_name))

    # SAFETY FIX 3: Validate exactly ONE match found
    if len(matches) == 0:
        raise ValueError(
            f"❌ No asset group found for customer {customer_id}:\n"
            f"   Campaign: '{campaign_name}'\n"
            f"   Asset Group: '{asset_group_name}'\n"
            f"   This likely means the spreadsheet has incorrect campaign/asset group names."
        )
    elif len(matches) > 1:
        raise ValueError(
            f"❌ AMBIGUOUS: Multiple asset groups match '{campaign_name} / {asset_group_name}':\n"
            + "\n".join([
                f"   - Campaign ID {m[1]}, Asset Group ID {m[0]}"
                for m in matches
            ])
            + f"\n   This is a CRITICAL ERROR - same names exist multiple times!"
            + f"\n   Add Asset Group IDs to spreadsheet to avoid this issue."
        )

    print(f"    ✅ Found unique match: Asset Group {matches[0][0]} in Campaign {matches[0][1]}")
    return matches[0][0], matches[0][1]


def get_current_text_assets(headers, customer_id: str, asset_group_id: str):
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

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])
    return results


def create_text_assets(headers, customer_id: str, texts: List[str]) -> List[str]:
    """Create new text assets and return their resource names."""
    if not texts:
        return []

    formatted_cid = format_customer_id(customer_id)
    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/assets:mutate"

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
    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/assetGroupAssets:mutate"

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


def apply_text_assets_to_asset_group(headers, customer_id: str,
                                       asset_group_id: str, campaign_id: str,
                                       asset_group_name: str, campaign_name: str,
                                       text_data: Dict, dry_run: bool = False) -> bool:
    """Apply text assets from spreadsheet to a single asset group."""
    print(f"\n  Asset Group: {asset_group_name}")
    print(f"    Campaign: {campaign_name}")
    print(f"    Asset Group ID: {asset_group_id}")

    # Validate asset counts
    headlines = text_data.get('headlines', [])
    long_headlines = text_data.get('long_headlines', [])
    descriptions = text_data.get('descriptions', [])

    print(f"    Spreadsheet assets:")
    print(f"      Headlines: {len(headlines)}")
    print(f"      Long Headlines: {len(long_headlines)}")
    print(f"      Descriptions: {len(descriptions)}")

    # Validate minimums
    if len(headlines) < MINIMUM_REQUIREMENTS['HEADLINE']:
        print(f"    ⚠️  ERROR: Not enough headlines ({len(headlines)} < {MINIMUM_REQUIREMENTS['HEADLINE']})")
        return False

    if len(long_headlines) < MINIMUM_REQUIREMENTS['LONG_HEADLINE']:
        print(f"    ⚠️  ERROR: Not enough long headlines ({len(long_headlines)} < {MINIMUM_REQUIREMENTS['LONG_HEADLINE']})")
        return False

    if len(descriptions) < MINIMUM_REQUIREMENTS['DESCRIPTION']:
        print(f"    ⚠️  ERROR: Not enough descriptions ({len(descriptions)} < {MINIMUM_REQUIREMENTS['DESCRIPTION']})")
        return False

    # Validate maximums
    if len(headlines) > MAXIMUM_LIMITS['HEADLINE']:
        print(f"    ⚠️  WARNING: Too many headlines ({len(headlines)} > {MAXIMUM_LIMITS['HEADLINE']}), truncating")
        headlines = headlines[:MAXIMUM_LIMITS['HEADLINE']]

    if len(long_headlines) > MAXIMUM_LIMITS['LONG_HEADLINE']:
        print(f"    ⚠️  WARNING: Too many long headlines ({len(long_headlines)} > {MAXIMUM_LIMITS['LONG_HEADLINE']}), truncating")
        long_headlines = long_headlines[:MAXIMUM_LIMITS['LONG_HEADLINE']]

    if len(descriptions) > MAXIMUM_LIMITS['DESCRIPTION']:
        print(f"    ⚠️  WARNING: Too many descriptions ({len(descriptions)} > {MAXIMUM_LIMITS['DESCRIPTION']}), truncating")
        descriptions = descriptions[:MAXIMUM_LIMITS['DESCRIPTION']]

    if dry_run:
        print(f"    [DRY RUN] Would apply {len(headlines)} headlines, {len(long_headlines)} long headlines, {len(descriptions)} descriptions")
        return True

    # Get current assets
    current_assets = get_current_text_assets(headers, customer_id, asset_group_id)

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

    print(f"    ✓ Applied successfully")
    return True


def apply_region_text_assets(region: str, dry_run: bool = False) -> tuple:
    """Apply text assets for an entire region from the spreadsheet."""
    customer_id = REGIONS[region]['customer_id']

    print(f"\n{'='*80}")
    print(f"APPLY TEXT ASSETS: {region.upper()}")
    print(f"Customer ID: {customer_id}")
    print(f"Spreadsheet: {SPREADSHEET_ID}")
    print(f"{'='*80}")

    if dry_run:
        print("[DRY RUN MODE - No changes will be made]")

    # Read spreadsheet data
    print(f"\nReading spreadsheet data...")
    rows = read_sheet_data(region)

    # Parse rows
    parsed_rows = []
    for i, row in enumerate(rows, start=2):  # Start at 2 because we skip header
        data = parse_text_assets_from_row(row)
        if data:
            parsed_rows.append(data)
        else:
            print(f"  Row {i}: Skipped (empty or invalid)")

    print(f"\nParsed {len(parsed_rows)} valid rows")

    headers = get_headers()
    success_count = 0
    fail_count = 0

    # Process each row
    for i, text_data in enumerate(parsed_rows, start=1):
        campaign_name = text_data['campaign_name']
        asset_group_name = text_data['asset_group_name']

        print(f"\n[{i}/{len(parsed_rows)}] Finding asset group...")
        print(f"  Campaign: {campaign_name}")
        print(f"  Asset Group: {asset_group_name}")

        # Find asset group ID
        asset_group_id, campaign_id = find_asset_group_id(
            headers, customer_id, campaign_name, asset_group_name
        )

        if not asset_group_id:
            print(f"  ✗ Asset group not found in Google Ads")
            fail_count += 1
            continue

        # Apply text assets
        try:
            result = apply_text_assets_to_asset_group(
                headers, customer_id, asset_group_id, campaign_id,
                asset_group_name, campaign_name, text_data, dry_run
            )
            if result:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            fail_count += 1

    return success_count, fail_count


def main():
    parser = argparse.ArgumentParser(
        description='Apply Smythson text assets from Google Spreadsheet to Google Ads'
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
    args = parser.parse_args()

    print(f"\nSmythson Text Asset Application Tool")
    print(f"Started: {datetime.now().isoformat()}")

    regions_to_process = list(REGIONS.keys()) if args.region == 'all' else [args.region]

    total_success = 0
    total_fail = 0

    for region in regions_to_process:
        success, fail = apply_region_text_assets(region, args.dry_run)
        total_success += success
        total_fail += fail

    print(f"\n{'='*80}")
    print(f"APPLICATION SUMMARY")
    print(f"{'='*80}")
    print(f"Regions processed: {', '.join(regions_to_process)}")
    print(f"Successful: {total_success}")
    print(f"Failed: {total_fail}")
    print(f"Completed: {datetime.now().isoformat()}")

    if args.dry_run:
        print(f"\n[DRY RUN COMPLETE - Run without --dry-run to apply changes]")

    sys.exit(0 if total_fail == 0 else 1)


if __name__ == "__main__":
    main()
