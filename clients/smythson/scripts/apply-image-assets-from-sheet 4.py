#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Apply Smythson PMax image assets from Google Spreadsheet to Google Ads.

Reads image asset IDs from the master Google Spreadsheet and links them to
Performance Max asset groups via the Google Ads API.

NOTE: This script only LINKS existing image assets. It does not create new images.
Image assets must already exist in the Google Ads account.

Usage:
    python3 apply-image-assets-from-sheet.py --region uk --dry-run
    python3 apply-image-assets-from-sheet.py --region all --dry-run
    python3 apply-image-assets-from-sheet.py --region uk  # live execution
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
        'campaign_asset_group_range': 'UK ad copy!A2:B',  # Campaign + Asset Group names
        'image_range': 'UK ad copy!BA2:BU'  # Image columns (21 max)
    },
    'us': {
        'customer_id': '7808690871',
        'sheet_name': 'US ad copy',
        'campaign_asset_group_range': 'US ad copy!A2:B',
        'image_range': 'US ad copy!BA2:BU'
    },
    'eur': {
        'customer_id': '7679616761',
        'sheet_name': 'EUR ad copy',
        'campaign_asset_group_range': 'EUR ad copy!A2:B',
        'image_range': 'EUR ad copy!BA2:BU'
    },
    'row': {
        'customer_id': '5556710725',
        'sheet_name': 'ROW ad copy',
        'campaign_asset_group_range': 'ROW ad copy!A2:B',
        'image_range': 'ROW ad copy!BA2:BU'
    },
}

# Minimum requirements per Google Ads API
MINIMUM_IMAGE_REQUIREMENTS = {
    'MARKETING_IMAGE': 1,
    'SQUARE_MARKETING_IMAGE': 1,
}


def get_headers():
    """Get headers for Google Ads API requests."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = format_customer_id(MANAGER_ID)
    return headers


def read_sheet_data(spreadsheet_id: str, data_range: str) -> List[List[str]]:
    """
    Read data from Google Spreadsheet using Google Sheets API.

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
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=data_range
    ).execute()

    rows = result.get('values', [])
    return rows


def find_asset_group_id(headers, customer_id: str, campaign_name: str,
                         asset_group_name: str) -> Optional[str]:
    """Find asset group ID by campaign name and asset group name."""
    formatted_cid = format_customer_id(customer_id)

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

    for result in results:
        camp_name = result.get('campaign', {}).get('name', '')
        ag_name = result.get('assetGroup', {}).get('name', '')

        if camp_name == campaign_name and ag_name == asset_group_name:
            ag_id = str(result.get('assetGroup', {}).get('id'))
            camp_id = str(result.get('campaign', {}).get('id'))
            return ag_id, camp_id

    return None, None


def get_current_image_assets(headers, customer_id: str, asset_group_id: str):
    """Query current image assets in an asset group."""
    formatted_cid = format_customer_id(customer_id)

    query = f"""
        SELECT
            asset_group_asset.resource_name,
            asset_group_asset.field_type,
            asset.id,
            asset.name
        FROM asset_group_asset
        WHERE asset_group.id = {asset_group_id}
        AND asset_group_asset.field_type IN ('MARKETING_IMAGE', 'SQUARE_MARKETING_IMAGE',
                                               'PORTRAIT_MARKETING_IMAGE', 'LOGO')
        AND asset_group_asset.status != 'REMOVED'
    """

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])
    return results


def link_image_assets(headers, customer_id: str, asset_group_id: str,
                       asset_ids: List[str], field_type: str = 'MARKETING_IMAGE') -> bool:
    """Link image assets to an asset group."""
    if not asset_ids:
        return True

    formatted_cid = format_customer_id(customer_id)
    asset_group_resource = f"customers/{formatted_cid}/assetGroups/{asset_group_id}"
    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/assetGroupAssets:mutate"

    operations = []

    # Create link operations for each image asset
    for asset_id in asset_ids:
        asset_resource = f"customers/{formatted_cid}/assets/{asset_id}"
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


def remove_image_assets(headers, customer_id: str, remove_resources: List[str]) -> bool:
    """Remove image asset links from an asset group."""
    if not remove_resources:
        return True

    formatted_cid = format_customer_id(customer_id)
    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/assetGroupAssets:mutate"

    operations = []

    for resource_name in remove_resources:
        operations.append({'remove': resource_name})

    if operations:
        payload = {'operations': operations}
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return True

    return False


def apply_image_assets_to_asset_group(headers, customer_id: str,
                                        asset_group_id: str, campaign_id: str,
                                        asset_group_name: str, campaign_name: str,
                                        image_ids: List[str], dry_run: bool = False) -> bool:
    """Apply image assets from spreadsheet to a single asset group."""
    print(f"\n  Asset Group: {asset_group_name}")
    print(f"    Campaign: {campaign_name}")
    print(f"    Asset Group ID: {asset_group_id}")

    # Filter out empty image IDs
    valid_image_ids = [img_id for img_id in image_ids if img_id.strip()]

    print(f"    Spreadsheet image assets: {len(valid_image_ids)}")

    if not valid_image_ids:
        print(f"    ⚠️  No image assets to apply")
        return True

    if dry_run:
        print(f"    [DRY RUN] Would link {len(valid_image_ids)} image assets")
        return True

    # Get current image assets
    current_assets = get_current_image_assets(headers, customer_id, asset_group_id)

    resources_to_remove = []
    for asset in current_assets:
        resource_name = asset.get('assetGroupAsset', {}).get('resourceName')
        if resource_name:
            resources_to_remove.append(resource_name)

    print(f"    Current image assets to remove: {len(resources_to_remove)}")

    # Remove old image assets
    if resources_to_remove:
        remove_image_assets(headers, customer_id, resources_to_remove)
        print(f"    Removed {len(resources_to_remove)} old image assets")

    # Link new image assets (as MARKETING_IMAGE - generic image type)
    link_image_assets(headers, customer_id, asset_group_id, valid_image_ids, 'MARKETING_IMAGE')

    print(f"    Linked {len(valid_image_ids)} new image assets")
    print(f"    ✓ Applied successfully")
    return True


def apply_region_image_assets(region: str, dry_run: bool = False) -> tuple:
    """Apply image assets for an entire region from the spreadsheet."""
    customer_id = REGIONS[region]['customer_id']

    print(f"\n{'='*80}")
    print(f"APPLY IMAGE ASSETS: {region.upper()}")
    print(f"Customer ID: {customer_id}")
    print(f"Spreadsheet: {SPREADSHEET_ID}")
    print(f"{'='*80}")

    if dry_run:
        print("[DRY RUN MODE - No changes will be made]")

    # Read campaign/asset group names
    print(f"\nReading campaign and asset group names...")
    names_range = REGIONS[region]['campaign_asset_group_range']
    names_rows = read_sheet_data(SPREADSHEET_ID, names_range)
    print(f"  Read {len(names_rows)} rows")

    # Read image asset IDs
    print(f"\nReading image asset IDs...")
    image_range = REGIONS[region]['image_range']
    image_rows = read_sheet_data(SPREADSHEET_ID, image_range)
    print(f"  Read {len(image_rows)} rows")

    # Ensure same number of rows
    if len(names_rows) != len(image_rows):
        print(f"  ⚠️  WARNING: Row count mismatch (names: {len(names_rows)}, images: {len(image_rows)})")
        min_rows = min(len(names_rows), len(image_rows))
        names_rows = names_rows[:min_rows]
        image_rows = image_rows[:min_rows]

    headers = get_headers()
    success_count = 0
    fail_count = 0

    # Process each row
    for i, (names_row, images_row) in enumerate(zip(names_rows, image_rows), start=1):
        if len(names_row) < 2:
            print(f"\n[{i}/{len(names_rows)}] Skipped (invalid names row)")
            continue

        campaign_name = names_row[0].strip()
        asset_group_name = names_row[1].strip()

        if not campaign_name or not asset_group_name:
            print(f"\n[{i}/{len(names_rows)}] Skipped (empty campaign or asset group name)")
            continue

        print(f"\n[{i}/{len(names_rows)}] Finding asset group...")
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

        # Apply image assets
        try:
            result = apply_image_assets_to_asset_group(
                headers, customer_id, asset_group_id, campaign_id,
                asset_group_name, campaign_name, images_row, dry_run
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
        description='Apply Smythson image assets from Google Spreadsheet to Google Ads'
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

    print(f"\nSmythson Image Asset Application Tool")
    print(f"Started: {datetime.now().isoformat()}")

    regions_to_process = list(REGIONS.keys()) if args.region == 'all' else [args.region]

    total_success = 0
    total_fail = 0

    for region in regions_to_process:
        success, fail = apply_region_image_assets(region, args.dry_run)
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
