#!/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Export Smythson image asset catalog to Google Spreadsheet.

Creates a visual catalog of ALL images in the Asset Library for a region,
with thumbnails displayed in Google Sheets for easy browsing and selection.

Usage:
    python3 export-image-catalog-to-sheet.py --region uk
    python3 export-image-catalog-to-sheet.py --region us
"""

import argparse
import os
import sys
import requests
from datetime import datetime
from typing import Dict, List

# Add the MCP server to path to use its OAuth module
MCP_SERVER_PATH = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, MCP_SERVER_PATH)

# Load env vars from MCP server
from dotenv import load_dotenv
load_dotenv(os.path.join(MCP_SERVER_PATH, '.env'))

# Import the OAuth module
from oauth.google_auth import get_headers_with_auto_token, format_customer_id

# Google Sheets imports
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Configuration
MANAGER_ID = '2569949686'

REGIONS = {
    'uk': {
        'customer_id': '8573235780',
        'name': 'UK'
    },
    'us': {
        'customer_id': '7808690871',
        'name': 'US'
    },
    'eur': {
        'customer_id': '7679616761',
        'name': 'EUR'
    },
    'row': {
        'customer_id': '5556710725',
        'name': 'ROW'
    },
}


def get_headers():
    """Get headers for Google Ads API requests."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = format_customer_id(MANAGER_ID)
    return headers


def get_sheets_service():
    """Get authenticated Google Sheets API service."""
    sheets_mcp_path = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server'
    token_path = os.path.join(sheets_mcp_path, 'token.json')

    if not os.path.exists(token_path):
        raise FileNotFoundError(f"Google Sheets OAuth token not found: {token_path}")

    creds = Credentials.from_authorized_user_file(token_path)
    service = build('sheets', 'v4', credentials=creds)
    return service


def get_all_image_assets(customer_id: str) -> List[Dict]:
    """
    Get all image assets from the account with their URLs.

    Returns list of dicts with:
    - asset_id: Asset ID
    - name: Asset name
    - url: Full-size image URL
    - width: Width in pixels
    - height: Height in pixels
    - mime_type: Image format
    """
    headers = get_headers()
    formatted_cid = format_customer_id(customer_id)

    query = """
        SELECT
            asset.id,
            asset.name,
            asset.image_asset.full_size.url,
            asset.image_asset.full_size.width_pixels,
            asset.image_asset.full_size.height_pixels,
            asset.image_asset.mime_type
        FROM asset
        WHERE asset.type = 'IMAGE'
        ORDER BY asset.name
    """

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])

    assets = []
    for result in results:
        asset_data = result.get('asset', {})
        image_data = asset_data.get('imageAsset', {})
        full_size = image_data.get('fullSize', {})

        assets.append({
            'asset_id': str(asset_data.get('id', '')),
            'name': asset_data.get('name', 'Unnamed'),
            'url': full_size.get('url', ''),
            'width': full_size.get('widthPixels', 0),
            'height': full_size.get('heightPixels', 0),
            'mime_type': image_data.get('mimeType', 'UNKNOWN'),
        })

    return assets


def get_asset_usage(customer_id: str) -> Dict[str, List[str]]:
    """
    Get where each asset is currently used.

    Returns dict mapping asset_id -> list of "Campaign | Asset Group" strings.
    """
    headers = get_headers()
    formatted_cid = format_customer_id(customer_id)

    query = """
        SELECT
            asset.id,
            campaign.name,
            asset_group.name,
            asset_group_asset.field_type
        FROM asset_group_asset
        WHERE asset_group_asset.field_type IN ('MARKETING_IMAGE', 'SQUARE_MARKETING_IMAGE',
                                                 'PORTRAIT_MARKETING_IMAGE', 'LOGO')
        AND asset_group_asset.status = 'ENABLED'
        AND campaign.advertising_channel_type = 'PERFORMANCE_MAX'
    """

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])

    usage_map = {}
    for result in results:
        asset_id = str(result.get('asset', {}).get('id', ''))
        campaign_name = result.get('campaign', {}).get('name', '')
        asset_group_name = result.get('assetGroup', {}).get('name', '')
        field_type = result.get('assetGroupAsset', {}).get('fieldType', '')

        usage_str = f"{asset_group_name} ({field_type})"

        if asset_id not in usage_map:
            usage_map[asset_id] = []

        usage_map[asset_id].append(usage_str)

    return usage_map


def create_spreadsheet(service, title: str) -> str:
    """Create a new Google Spreadsheet and return its ID."""
    spreadsheet = {
        'properties': {
            'title': title
        },
        'sheets': [{
            'properties': {
                'title': 'Image Catalog',
                'gridProperties': {
                    'frozenRowCount': 1  # Freeze header row
                }
            }
        }]
    }

    result = service.spreadsheets().create(body=spreadsheet).execute()
    return result['spreadsheetId']


def write_catalog_to_sheet(service, spreadsheet_id: str, assets: List[Dict],
                            usage_map: Dict[str, List[str]]):
    """Write image catalog data to Google Sheet with IMAGE formulas."""

    # Prepare data rows
    rows = [
        ['Asset ID', 'Asset Name', 'Dimensions', 'Format', 'View Image', 'Usage Count', 'Currently Used In']
    ]

    for asset in assets:
        asset_id = asset['asset_id']
        name = asset['name']
        dimensions = f"{asset['width']}x{asset['height']}"
        mime_type = asset['mime_type'].replace('IMAGE_', '')
        image_url = asset['url']

        # Get usage info
        usage = usage_map.get(asset_id, [])
        usage_count = len(usage)
        # Limit usage string to first 3 uses to keep it readable
        usage_preview = usage[:3] if usage else []
        usage_str = ', '.join(usage_preview) if usage_preview else 'Not currently used'
        if len(usage) > 3:
            usage_str += f' ... and {len(usage) - 3} more'

        # We'll make column E a hyperlink instead of IMAGE formula
        rows.append([
            asset_id,
            name,
            dimensions,
            mime_type,
            image_url,  # We'll convert this to =HYPERLINK() formula below
            usage_count,
            usage_str
        ])

    # Write basic data first
    range_name = 'Image Catalog!A1:G' + str(len(rows))
    body = {
        'values': rows
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()

    print(f"  Wrote {len(rows)-1} image assets to spreadsheet")

    # Now update column E with HYPERLINK formulas for clickable image links
    formula_rows = []
    for i, asset in enumerate(assets, start=2):  # Start at row 2 (after header)
        image_url = asset['url']
        if image_url:
            # Create HYPERLINK formula - clickable "View Image" link
            formula = f'=HYPERLINK("{image_url}", "🖼️ View Image")'
            formula_rows.append([formula])
        else:
            formula_rows.append(['No image URL'])

    if formula_rows:
        formula_range = f'Image Catalog!E2:E{len(assets)+1}'
        formula_body = {
            'values': formula_rows
        }

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=formula_range,
            valueInputOption='USER_ENTERED',  # This processes formulas
            body=formula_body
        ).execute()

        print(f"  Added {len(formula_rows)} clickable image links")

    # Format the sheet
    format_sheet(service, spreadsheet_id)


def format_sheet(service, spreadsheet_id: str):
    """Apply formatting to make the sheet easier to use."""

    # Get the sheet ID first
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']

    requests = [
        # Make header row bold
        {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {
                            'bold': True
                        },
                        'backgroundColor': {
                            'red': 0.9,
                            'green': 0.9,
                            'blue': 0.9
                        }
                    }
                },
                'fields': 'userEnteredFormat(textFormat,backgroundColor)'
            }
        },
        # Set column widths
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': 1  # Column A (Asset ID)
                },
                'properties': {
                    'pixelSize': 120
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 1,
                    'endIndex': 2  # Column B (Name)
                },
                'properties': {
                    'pixelSize': 250
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 4,
                    'endIndex': 5  # Column E (View Image link)
                },
                'properties': {
                    'pixelSize': 120
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 5,
                    'endIndex': 6  # Column F (Usage Count)
                },
                'properties': {
                    'pixelSize': 80
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 6,
                    'endIndex': 7  # Column G (Currently Used In)
                },
                'properties': {
                    'pixelSize': 400
                },
                'fields': 'pixelSize'
            }
        },
        # Set row height for data rows
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'ROWS',
                    'startIndex': 1  # All rows after header
                },
                'properties': {
                    'pixelSize': 21  # Standard row height
                },
                'fields': 'pixelSize'
            }
        }
    ]

    body = {
        'requests': requests
    }

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    print(f"  Applied formatting to spreadsheet")


def export_region_catalog(region: str):
    """Export image catalog for a region to a new Google Spreadsheet."""
    customer_id = REGIONS[region]['customer_id']
    region_name = REGIONS[region]['name']

    print(f"\n{'='*80}")
    print(f"EXPORTING IMAGE CATALOG: {region_name}")
    print(f"Customer ID: {customer_id}")
    print(f"{'='*80}")

    # Get all image assets
    print(f"\nQuerying image assets from Google Ads...")
    assets = get_all_image_assets(customer_id)
    print(f"  Found {len(assets)} image assets")

    # Get asset usage
    print(f"\nQuerying where assets are currently used...")
    usage_map = get_asset_usage(customer_id)
    print(f"  Found usage data for {len(usage_map)} assets")

    # Create Google Spreadsheet
    print(f"\nCreating Google Spreadsheet...")
    sheets_service = get_sheets_service()

    timestamp = datetime.now().strftime('%Y-%m-%d')
    title = f"Smythson {region_name} Image Catalog - {timestamp}"

    spreadsheet_id = create_spreadsheet(sheets_service, title)
    print(f"  Created spreadsheet: {title}")
    print(f"  Spreadsheet ID: {spreadsheet_id}")

    # Write data to spreadsheet
    print(f"\nWriting image catalog to spreadsheet...")
    write_catalog_to_sheet(sheets_service, spreadsheet_id, assets, usage_map)

    # Generate shareable link
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"

    print(f"\n{'='*80}")
    print(f"✅ IMAGE CATALOG CREATED SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"Region: {region_name}")
    print(f"Total Images: {len(assets)}")
    print(f"Spreadsheet: {spreadsheet_url}")
    print(f"\nYou can now browse images visually and copy Asset IDs for your activation spreadsheet.")
    print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Export Smythson image asset catalog to Google Spreadsheet'
    )
    parser.add_argument(
        '--region',
        required=True,
        choices=['uk', 'us', 'eur', 'row'],
        help='Region to export image catalog for'
    )
    args = parser.parse_args()

    print(f"\nSmythson Image Catalog Export Tool")
    print(f"Started: {datetime.now().isoformat()}")

    export_region_catalog(args.region)

    print(f"\nCompleted: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
