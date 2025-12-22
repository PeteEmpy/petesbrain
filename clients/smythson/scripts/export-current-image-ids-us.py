#!/usr/bin/env python3
"""
Export current image asset IDs from US region to CSV for comparison with spreadsheet.
This will help diagnose why the script isn't detecting overlaps.
"""
import sys
import os
import csv
import json
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Add shared directory to path
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain.nosync')
from shared.google_ads_helpers import get_headers_with_auto_token

CREDENTIALS_PATH = '/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'
SPREADSHEET_ID = '1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g'
CLIENT_SECRET_FILE = os.path.expanduser('~/.google-ads/client_secret.json')

# US region settings
CUSTOMER_ID = '7808690871'
MANAGER_ID = '2569949686'

def format_customer_id(customer_id: str) -> str:
    """Remove hyphens from customer ID."""
    return customer_id.replace('-', '')

def get_headers():
    """Get Google Ads API headers."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = format_customer_id(MANAGER_ID)
    return headers

def read_spreadsheet_asset_groups():
    """Read asset group names and IDs from spreadsheet."""
    creds = Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )

    service = build('sheets', 'v4', credentials=creds)

    # Read campaign and asset group info from US PMax Assets tab
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='US PMax Assets!A2:D'
    ).execute()

    rows = result.get('values', [])

    asset_groups = []
    for row in rows:
        if len(row) >= 4:
            campaign_id = row[0].strip()
            asset_group_id = row[2].strip() if len(row) > 2 else ''
            asset_group_name = row[3].strip() if len(row) > 3 else ''

            if campaign_id and asset_group_name:
                asset_groups.append({
                    'campaign_id': campaign_id,
                    'asset_group_id': asset_group_id,
                    'asset_group_name': asset_group_name
                })

    return asset_groups

def get_current_image_assets(headers, asset_group_id: str):
    """Query current image assets in an asset group."""
    formatted_cid = format_customer_id(CUSTOMER_ID)

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

def main():
    print("=" * 80)
    print("EXPORT CURRENT IMAGE ASSET IDs - US REGION")
    print("=" * 80)
    print()

    # Read asset groups from spreadsheet
    print("Reading asset groups from spreadsheet...")
    asset_groups = read_spreadsheet_asset_groups()
    print(f"Found {len(asset_groups)} asset groups")
    print()

    # Get headers
    headers = get_headers()

    # Prepare CSV output
    output_file = '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports/us-current-image-ids.csv'

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow([
            'Campaign ID',
            'Asset Group ID',
            'Asset Group Name',
            'Current Image IDs (comma-separated)',
            'Count',
            'Field Types'
        ])

        # Process each asset group
        for i, ag in enumerate(asset_groups, 1):
            print(f"[{i}/{len(asset_groups)}] {ag['asset_group_name']}...")

            try:
                current_assets = get_current_image_assets(headers, ag['asset_group_id'])

                # Extract asset IDs using the SAME logic as the main script
                asset_ids = []
                field_types = []

                for asset in current_assets:
                    # This is the FIXED logic from apply-image-assets-from-sheet.py
                    asset_id = str(asset.get('asset', {}).get('id', ''))
                    field_type = asset.get('assetGroupAsset', {}).get('fieldType', '')

                    if asset_id:
                        asset_ids.append(asset_id)
                        field_types.append(field_type)

                # Write to CSV
                writer.writerow([
                    ag['campaign_id'],
                    ag['asset_group_id'],
                    ag['asset_group_name'],
                    ','.join(asset_ids),
                    len(asset_ids),
                    ','.join(field_types)
                ])

                print(f"  Found {len(asset_ids)} current images")

            except Exception as e:
                print(f"  ERROR: {str(e)}")
                writer.writerow([
                    ag['campaign_id'],
                    ag['asset_group_id'],
                    ag['asset_group_name'],
                    f'ERROR: {str(e)}',
                    0,
                    ''
                ])

    print()
    print("=" * 80)
    print(f"Export complete: {output_file}")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Open the CSV file")
    print("2. Compare 'Current Image IDs' with spreadsheet column E onwards")
    print("3. Check if IDs match exactly (format, whitespace, etc.)")

if __name__ == '__main__':
    main()
