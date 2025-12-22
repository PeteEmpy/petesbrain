#!/usr/bin/env python3
"""
Diagnose asset ID mismatch between spreadsheet and Google Ads for US region.
Uses MCP server for Google Ads queries and Google Sheets API for spreadsheet.
"""
import sys
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# MCP configuration
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server')
from mcp_google_ads import run_gaql

CREDENTIALS_PATH = '/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'
SPREADSHEET_ID = '1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g'

# US region settings
CUSTOMER_ID = '7808690871'
MANAGER_ID = '2569949686'

def read_spreadsheet_data():
    """Read all data from US PMax Assets tab."""
    creds = Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )

    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='US PMax Assets!A2:Z'
    ).execute()

    return result.get('values', [])

def get_current_image_assets(asset_group_id: str):
    """Query current image assets in an asset group using MCP."""
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

    result = run_gaql(CUSTOMER_ID, query, MANAGER_ID)
    return result.get('results', [])

def main():
    print("=" * 80)
    print("DIAGNOSE ASSET ID MISMATCH - US REGION")
    print("=" * 80)
    print()

    # Read spreadsheet
    print("Reading spreadsheet data...")
    rows = read_spreadsheet_data()
    print(f"Found {len(rows)} rows")
    print()

    # Process each row
    mismatches = []

    for i, row in enumerate(rows, 1):
        if len(row) < 4:
            continue

        campaign_id = row[0].strip() if row[0] else ''
        asset_group_id = row[2].strip() if len(row) > 2 and row[2] else ''
        asset_group_name = row[3].strip() if len(row) > 3 and row[3] else ''

        if not asset_group_id or not asset_group_name:
            continue

        # Get spreadsheet asset IDs (columns E onwards)
        spreadsheet_ids = set()
        for col in range(4, len(row)):
            if row[col] and row[col].strip():
                spreadsheet_ids.add(row[col].strip())

        print(f"[{i}/{len(rows)}] {asset_group_name}")
        print(f"  Asset Group ID: {asset_group_id}")
        print(f"  Spreadsheet IDs: {sorted(spreadsheet_ids)}")

        try:
            # Get current Google Ads assets
            current_assets = get_current_image_assets(asset_group_id)

            # Extract IDs using same logic as main script
            current_ids = set()
            for asset in current_assets:
                asset_id = str(asset.get('asset', {}).get('id', ''))
                if asset_id:
                    current_ids.add(asset_id)

            print(f"  Current IDs:     {sorted(current_ids)}")

            # Check overlap
            overlap = spreadsheet_ids & current_ids
            spreadsheet_only = spreadsheet_ids - current_ids
            google_ads_only = current_ids - spreadsheet_ids

            print(f"  Overlap:         {sorted(overlap)} ({len(overlap)} IDs)")

            if spreadsheet_only:
                print(f"  SPREADSHEET ONLY: {sorted(spreadsheet_only)}")
            if google_ads_only:
                print(f"  GOOGLE ADS ONLY:  {sorted(google_ads_only)}")

            if spreadsheet_ids == current_ids:
                print(f"  ✓ MATCH - Should skip (but got DUPLICATE_RESOURCE error)")
                mismatches.append({
                    'name': asset_group_name,
                    'id': asset_group_id,
                    'spreadsheet_ids': sorted(spreadsheet_ids),
                    'current_ids': sorted(current_ids),
                    'issue': 'Should skip but got error'
                })

            print()

        except Exception as e:
            print(f"  ERROR: {str(e)}")
            print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if mismatches:
        print(f"\nFound {len(mismatches)} asset groups that should have been skipped:")
        for m in mismatches:
            print(f"\n{m['name']} (ID: {m['id']})")
            print(f"  Spreadsheet: {m['spreadsheet_ids']}")
            print(f"  Current:     {m['current_ids']}")
    else:
        print("\nNo perfect matches found - this explains the DUPLICATE_RESOURCE errors")

if __name__ == '__main__':
    main()
