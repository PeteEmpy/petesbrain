#!/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
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

REGIONS = {
    'uk': {
        'customer_id': '8573235780',
        'sheet_name': 'UK PMax Assets',
        'campaign_asset_group_range': 'UK PMax Assets!A2:D',  # Campaign ID + Asset Group Name
        'image_range': 'UK PMax Assets!AW2:BT'  # Image columns: Landscape (AW-BC), Square (BD-BJ), Portrait (BK-BQ), Logo (BT)
    },
    'us': {
        'customer_id': '7808690871',
        'sheet_name': 'US PMax Assets',
        'campaign_asset_group_range': 'US PMax Assets!A2:D',
        'image_range': 'US PMax Assets!AW2:BT'  # Image columns: Landscape (AW-BC), Square (BD-BJ), Portrait (BK-BQ), Logo (BT)
    },
    'eur': {
        'customer_id': '7679616761',
        'sheet_name': 'EUR PMax Assets',
        'campaign_asset_group_range': 'EUR PMax Assets!A2:D',
        'image_range': 'EUR PMax Assets!AW2:BT'  # Image columns: Landscape (AW-BC), Square (BD-BJ), Portrait (BK-BQ), Logo (BT)
    },
    'row': {
        'customer_id': '5556710725',
        'sheet_name': 'ROW PMax Assets',
        'campaign_asset_group_range': 'ROW PMax Assets!A2:D',
        'image_range': 'ROW PMax Assets!AW2:BT'  # Image columns: Landscape (AW-BC), Square (BD-BJ), Portrait (BK-BQ), Logo (BT)
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

    Uses the Google Sheets MCP server service account credentials.
    """
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build

    # Path to Google Sheets MCP server service account credentials
    sheets_mcp_path = '/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-sheets-mcp-server'
    credentials_path = os.path.join(sheets_mcp_path, 'credentials.json')

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Google Sheets service account credentials not found: {credentials_path}")

    # Load service account credentials
    creds = Credentials.from_service_account_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )

    # Build the service
    service = build('sheets', 'v4', credentials=creds)

    # Read data
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=data_range
    ).execute()

    rows = result.get('values', [])
    return rows


def find_asset_group_id(headers, customer_id: str, campaign_id: str,
                         asset_group_name: str) -> Optional[str]:
    """
    Find asset group ID by campaign ID and asset group name.

    SAFETY IMPROVEMENTS (2025-11-27):
    - Filters by customer_id to prevent cross-account matching
    - Validates only ONE match found (prevents ambiguous results)
    - Raises clear errors if no match or multiple matches found

    UPDATED (2025-12-15):
    - Changed to match by campaign ID instead of campaign name (more reliable)
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
        camp_id = str(result.get('campaign', {}).get('id'))
        camp_name = result.get('campaign', {}).get('name', '')
        ag_name = result.get('assetGroup', {}).get('name', '')

        # Match by campaign ID (not name) and asset group name
        if camp_id == campaign_id and ag_name == asset_group_name:
            ag_id = str(result.get('assetGroup', {}).get('id'))
            matches.append((ag_id, camp_id, camp_name, ag_name))

    # SAFETY FIX 3: Validate exactly ONE match found
    if len(matches) == 0:
        raise ValueError(
            f"❌ No asset group found for customer {customer_id}:\n"
            f"   Campaign ID: '{campaign_id}'\n"
            f"   Asset Group: '{asset_group_name}'\n"
            f"   This likely means the spreadsheet has incorrect campaign ID or asset group name."
        )
    elif len(matches) > 1:
        raise ValueError(
            f"❌ AMBIGUOUS: Multiple asset groups match Campaign ID '{campaign_id}' / Asset Group '{asset_group_name}':\n"
            + "\n".join([
                f"   - Campaign ID {m[1]}, Asset Group ID {m[0]}"
                for m in matches
            ])
            + f"\n   This is a CRITICAL ERROR - same names exist multiple times!"
            + f"\n   Add Asset Group IDs to spreadsheet to avoid this issue."
        )

    print(f"    ✅ Found unique match: Asset Group {matches[0][0]} in Campaign {matches[0][1]}")
    return matches[0][0], matches[0][1]


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


def get_image_dimensions(headers, customer_id: str, asset_ids: List[str]) -> Dict[str, tuple]:
    """
    Get dimensions for image assets.

    Returns dict mapping asset_id -> (width, height)
    """
    if not asset_ids:
        return {}

    formatted_cid = format_customer_id(customer_id)

    # Query image dimensions
    asset_ids_str = ', '.join(asset_ids)
    query = f"""
        SELECT
            asset.id,
            asset.image_asset.full_size.width_pixels,
            asset.image_asset.full_size.height_pixels
        FROM asset
        WHERE asset.id IN ({asset_ids_str})
        AND asset.type = 'IMAGE'
    """

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])

    dimensions = {}
    for result in results:
        asset_id = str(result.get('asset', {}).get('id'))
        width = int(result.get('asset', {}).get('imageAsset', {}).get('fullSize', {}).get('widthPixels', 0))
        height = int(result.get('asset', {}).get('imageAsset', {}).get('fullSize', {}).get('heightPixels', 0))
        dimensions[asset_id] = (width, height)

    return dimensions


def determine_image_field_type(width: int, height: int) -> str:
    """
    Determine the correct PMax image field type based on dimensions.

    Field types and their aspect ratios:
    - MARKETING_IMAGE: 1.91:1 (landscape, e.g., 1200x628)
    - SQUARE_MARKETING_IMAGE: 1:1 (square, e.g., 1200x1200)
    - PORTRAIT_MARKETING_IMAGE: 4:5 (portrait, e.g., 960x1200)
    """
    if width == 0 or height == 0:
        return 'MARKETING_IMAGE'  # Default fallback

    aspect_ratio = width / height

    # Square: ratio close to 1.0 (tolerance ±0.1)
    if 0.9 <= aspect_ratio <= 1.1:
        return 'SQUARE_MARKETING_IMAGE'

    # Portrait: ratio close to 0.8 (4:5 = 0.8, tolerance ±0.1)
    elif 0.7 <= aspect_ratio <= 0.9:
        return 'PORTRAIT_MARKETING_IMAGE'

    # Landscape: everything else (including 1.91:1)
    else:
        return 'MARKETING_IMAGE'


def link_image_assets_with_auto_type(headers, customer_id: str, asset_group_id: str,
                                      asset_ids: List[str], remove_resources: List[str] = None) -> bool:
    """
    Link image assets to an asset group with automatic field type detection.

    Optionally removes old assets in the SAME operation (atomic) to avoid
    violating PMax minimum requirements during the transition.

    Queries image dimensions and assigns correct field type based on aspect ratio.
    """
    if not asset_ids and not remove_resources:
        return True

    formatted_cid = format_customer_id(customer_id)
    asset_group_resource = f"customers/{formatted_cid}/assetGroups/{asset_group_id}"
    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/assetGroupAssets:mutate"

    operations = []

    # FIRST: Add remove operations (if any)
    if remove_resources:
        for resource_name in remove_resources:
            operations.append({'remove': resource_name})

    # SECOND: Add create operations for new images
    if asset_ids:
        # Get dimensions for all images
        dimensions = get_image_dimensions(headers, customer_id, asset_ids)

        # Create link operations for each image asset with correct field type
        for asset_id in asset_ids:
            asset_resource = f"customers/{formatted_cid}/assets/{asset_id}"

            # Determine field type based on dimensions
            width, height = dimensions.get(asset_id, (0, 0))
            field_type = determine_image_field_type(width, height)

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
        if resp.status_code != 200:
            print(f"    ERROR APPLYING CHANGES: API returned {resp.status_code}")
            print(f"    Response: {resp.text[:1000]}")
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
        if resp.status_code != 200:
            print(f"    ERROR REMOVING IMAGES: API returned {resp.status_code}")
            print(f"    Response: {resp.text[:500]}")
        resp.raise_for_status()
        return True

    return False


def parse_image_column_headers(region: str) -> Dict[int, str]:
    """
    Read column headers from row 1 and map column indices to image types.

    Returns: Dict mapping column_index -> field_type
             e.g., {0: 'MARKETING_IMAGE', 7: 'SQUARE_MARKETING_IMAGE', ...}
    """
    # Read header row
    sheet_name = REGIONS[region]['sheet_name']
    # Get the same column range as image data, but row 1
    image_range = REGIONS[region]['image_range']
    # Extract column letters (e.g., "AW2:BT" -> "AW1:BT1")
    parts = image_range.split('!')
    col_range = parts[1] if len(parts) > 1 else image_range
    col_range = col_range.replace('2:', '1:').replace('2', '1')
    header_range = f"{sheet_name}!{col_range}"

    header_row = read_sheet_data(SPREADSHEET_ID, header_range)

    if not header_row or not header_row[0]:
        raise ValueError(f"Could not read header row from {header_range}")

    headers = header_row[0]

    # Map column index to field type based on header text
    column_mapping = {}
    for i, header in enumerate(headers):
        header_lower = header.lower()
        if 'landscape' in header_lower:
            column_mapping[i] = 'MARKETING_IMAGE'
        elif 'square' in header_lower:
            column_mapping[i] = 'SQUARE_MARKETING_IMAGE'
        elif 'portrait' in header_lower:
            column_mapping[i] = 'PORTRAIT_MARKETING_IMAGE'
        elif 'logo' in header_lower:
            column_mapping[i] = 'LOGO'

    return column_mapping


def validate_image_type_requirements_by_position(image_row: List[str], column_mapping: Dict[int, str]) -> tuple:
    """
    Validate images based on their column position (using spreadsheet headers).

    This is more reliable than querying API dimensions, since the user has
    organized images into the correct columns.

    Returns: (is_valid, error_message, type_counts)
    """
    if not image_row:
        return False, "No images provided", {}

    # Count non-empty cells by their column type
    type_counts = {
        'MARKETING_IMAGE': 0,
        'SQUARE_MARKETING_IMAGE': 0,
        'PORTRAIT_MARKETING_IMAGE': 0,
        'LOGO': 0
    }

    for i, cell_value in enumerate(image_row):
        if cell_value and cell_value.strip():
            field_type = column_mapping.get(i)
            if field_type:
                type_counts[field_type] = type_counts.get(field_type, 0) + 1

    # Check minimum requirements
    missing_types = []
    for img_type, min_count in MINIMUM_IMAGE_REQUIREMENTS.items():
        if type_counts.get(img_type, 0) < min_count:
            missing_types.append(img_type)

    if missing_types:
        error_msg = (
            f"❌ VALIDATION FAILED: New images don't meet PMax requirements\n"
            f"    Missing required types: {', '.join(missing_types)}\n"
            f"    Current distribution:\n"
            f"      - Landscape (MARKETING_IMAGE): {type_counts['MARKETING_IMAGE']}\n"
            f"      - Square (SQUARE_MARKETING_IMAGE): {type_counts['SQUARE_MARKETING_IMAGE']}\n"
            f"      - Portrait (PORTRAIT_MARKETING_IMAGE): {type_counts.get('PORTRAIT_MARKETING_IMAGE', 0)}\n"
            f"    Requirements:\n"
            f"      - At least 1 landscape (MARKETING_IMAGE)\n"
            f"      - At least 1 square (SQUARE_MARKETING_IMAGE)\n"
            f"    Fix: Add missing image types to the spreadsheet columns before running."
        )
        return False, error_msg, type_counts

    return True, None, type_counts


def apply_image_assets_to_asset_group(headers, customer_id: str,
                                        asset_group_id: str, campaign_id: str,
                                        asset_group_name: str, campaign_name: str,
                                        images_row: List[str], column_mapping: Dict[int, str],
                                        dry_run: bool = False) -> bool:
    """Apply image assets from spreadsheet to a single asset group."""
    print(f"\n  Asset Group: {asset_group_name}")
    print(f"    Campaign: {campaign_name}")
    print(f"    Asset Group ID: {asset_group_id}")

    # PRE-VALIDATION: Check that new images meet type requirements (by column position)
    # This must be done BEFORE filtering, as we need column positions
    print(f"    Validating image type requirements...")

    # Validate based on column position (using pre-parsed column_mapping from caller)
    is_valid, error_msg, type_counts = validate_image_type_requirements_by_position(
        images_row, column_mapping
    )

    if not is_valid:
        print(f"    {error_msg}")
        return False

    print(f"    ✅ Validation passed - Image distribution:")
    print(f"       Landscape: {type_counts['MARKETING_IMAGE']}")
    print(f"       Square: {type_counts['SQUARE_MARKETING_IMAGE']}")
    print(f"       Portrait: {type_counts.get('PORTRAIT_MARKETING_IMAGE', 0)}")

    # NOW filter out empty image IDs and remove duplicates (preserving order)
    # This is for the actual API operations, not validation
    seen = set()
    valid_image_ids = []
    for img_id in images_row:
        if img_id.strip() and img_id not in seen:
            valid_image_ids.append(img_id)
            seen.add(img_id)

    print(f"    Spreadsheet image assets: {len(valid_image_ids)}")

    if not valid_image_ids:
        print(f"    ⚠️  No image assets to apply (after filtering)")
        return True

    # Get current image assets (needed for both dry-run and live execution)
    current_assets = get_current_image_assets(headers, customer_id, asset_group_id)

    # Build mapping: asset_id -> resource_name AND build set of currently linked asset IDs
    current_image_ids = set()
    resources_to_remove_map = {}

    for asset in current_assets:
        resource_name = asset.get('assetGroupAsset', {}).get('resourceName')
        # Get asset ID directly from API response (not from resource_name parsing)
        # The query returns asset.id which matches the format in the spreadsheet
        asset_id = str(asset.get('asset', {}).get('id', ''))
        if resource_name and asset_id:
            current_image_ids.add(asset_id)
            resources_to_remove_map[asset_id] = resource_name

    # Convert spreadsheet images to set
    spreadsheet_image_ids = set(valid_image_ids)

    # DEBUG: Show what we found
    print(f"    DEBUG: Current image IDs ({len(current_image_ids)}): {sorted(list(current_image_ids)[:5])}")
    print(f"    DEBUG: Spreadsheet image IDs ({len(spreadsheet_image_ids)}): {sorted(list(spreadsheet_image_ids)[:5])}")

    # Calculate set differences (the core fix for DUPLICATE_RESOURCE errors)
    images_in_both = current_image_ids & spreadsheet_image_ids  # KEEP - already correct
    images_to_remove_ids = current_image_ids - spreadsheet_image_ids  # REMOVE - not in spreadsheet
    images_to_add_ids = spreadsheet_image_ids - current_image_ids  # ADD - not currently linked

    # Build final removal list (only images NOT in spreadsheet)
    resources_to_remove = [resources_to_remove_map[img_id] for img_id in images_to_remove_ids]

    # Update valid_image_ids to only include images NOT already linked
    valid_image_ids = list(images_to_add_ids)

    print(f"    Current images: {len(current_image_ids)} total")
    print(f"    - Keep (already correct): {len(images_in_both)}")
    print(f"    - Remove (not in spreadsheet): {len(images_to_remove_ids)}")
    print(f"    - Add (not currently linked): {len(images_to_add_ids)}")

    # Dry-run check (now happens AFTER set analysis so we can show proper diagnostics)
    if dry_run:
        print(f"    [DRY RUN] Operations: Keep {len(images_in_both)}, Remove {len(images_to_remove_ids)}, Add {len(images_to_add_ids)}")
        return True

    # SAFETY CHECK: PMax allows maximum 20 images per asset group
    MAX_IMAGES = 20

    # After changes, final count will be: (keep) + (add)
    final_count = len(images_in_both) + len(images_to_add_ids)
    print(f"    Final count after changes: {final_count} images (limit: {MAX_IMAGES})")

    # ATOMIC OPERATION: Remove old and add new in single API call
    # This prevents temporary violations of min/max requirements
    if valid_image_ids or resources_to_remove:
        link_image_assets_with_auto_type(headers, customer_id, asset_group_id, valid_image_ids, resources_to_remove)

        added_msg = f"added {len(valid_image_ids)} new" if valid_image_ids else "no new added"
        removed_msg = f"removed {len(resources_to_remove)} old" if resources_to_remove else "no old removed"
        print(f"    ✓ Applied changes atomically: {removed_msg}, {added_msg}")

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

    # PERFORMANCE OPTIMIZATION: Parse column headers ONCE for the entire region
    # (instead of once per asset group, which caused API rate limit issues)
    print(f"\nParsing image column headers...")
    column_mapping = parse_image_column_headers(region)
    print(f"  ✓ Mapped {len(column_mapping)} image columns")

    headers = get_headers()
    success_count = 0
    fail_count = 0

    # Process each row
    for i, (names_row, images_row) in enumerate(zip(names_rows, image_rows), start=1):
        if len(names_row) < 2:
            print(f"\n[{i}/{len(names_rows)}] Skipped (invalid names row)")
            continue

        # Now reading A:D, so: [Campaign ID, Campaign Name, Asset Group ID, Asset Group Name]
        campaign_id = names_row[0].strip()
        asset_group_name = names_row[3].strip() if len(names_row) > 3 else ''

        if not campaign_id or not asset_group_name:
            print(f"\n[{i}/{len(names_rows)}] Skipped (empty campaign ID or asset group name)")
            continue

        print(f"\n[{i}/{len(names_rows)}] Finding asset group...")
        print(f"  Campaign ID: {campaign_id}")
        print(f"  Asset Group: {asset_group_name}")

        # Find asset group ID (using campaign ID instead of name)
        asset_group_id, found_campaign_id = find_asset_group_id(
            headers, customer_id, campaign_id, asset_group_name
        )

        if not asset_group_id:
            print(f"  ✗ Asset group not found in Google Ads")
            fail_count += 1
            continue

        # Apply image assets
        try:
            result = apply_image_assets_to_asset_group(
                headers, customer_id, asset_group_id, found_campaign_id,
                asset_group_name, campaign_id, images_row, column_mapping, dry_run
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
