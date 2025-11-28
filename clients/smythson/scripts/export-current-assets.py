#!/usr/bin/env python3
"""
Smythson Asset Export - Creates backup of current text assets
Run before Dec 2nd asset revert to create rollback snapshot
"""

import os
import sys
import json
from datetime import datetime

# Add the MCP server path to import OAuth helper
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')
from oauth.google_auth import execute_gaql

# Smythson account IDs
ACCOUNTS = {
    'UK': {'customer_id': '8573235780', 'manager_id': '2569949686'},
    'US': {'customer_id': '7808690871', 'manager_id': '2569949686'},
    'EUR': {'customer_id': '7679616761', 'manager_id': '2569949686'},
    'ROW': {'customer_id': '5556710725', 'manager_id': '2569949686'},
}

OUTPUT_DIR = '/Users/administrator/Documents/PetesBrain/clients/smythson/data/asset-backups'

def get_asset_groups(customer_id: str, manager_id: str) -> list:
    """Get all PMax asset groups for an account."""
    query = """
    SELECT
      campaign.name,
      campaign.id,
      asset_group.name,
      asset_group.id
    FROM asset_group
    WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
      AND campaign.status = 'ENABLED'
      AND asset_group.status = 'ENABLED'
    ORDER BY campaign.name, asset_group.name
    """
    result = execute_gaql(customer_id, query, manager_id)
    return result.get('results', [])

def get_text_assets_for_asset_group(customer_id: str, manager_id: str, asset_group_id: str) -> list:
    """Get all text assets for a specific asset group."""
    query = f"""
    SELECT
      asset_group.name,
      asset_group_asset.field_type,
      asset.text_asset.text,
      asset.id
    FROM asset_group_asset
    WHERE asset_group.id = {asset_group_id}
      AND asset_group_asset.field_type IN ('HEADLINE', 'LONG_HEADLINE', 'DESCRIPTION')
      AND asset_group_asset.status = 'ENABLED'
    ORDER BY asset_group_asset.field_type
    """
    result = execute_gaql(customer_id, query, manager_id)
    return result.get('results', [])

def get_image_assets_for_asset_group(customer_id: str, manager_id: str, asset_group_id: str) -> list:
    """Get all image assets for a specific asset group."""
    query = f"""
    SELECT
      asset_group.name,
      asset_group_asset.field_type,
      asset.id,
      asset.name,
      asset.image_asset.full_size.width_pixels,
      asset.image_asset.full_size.height_pixels
    FROM asset_group_asset
    WHERE asset_group.id = {asset_group_id}
      AND asset_group_asset.field_type IN ('MARKETING_IMAGE', 'SQUARE_MARKETING_IMAGE', 'PORTRAIT_MARKETING_IMAGE')
      AND asset_group_asset.status = 'ENABLED'
    ORDER BY asset_group_asset.field_type
    """
    result = execute_gaql(customer_id, query, manager_id)
    return result.get('results', [])

def export_account(region: str, customer_id: str, manager_id: str) -> dict:
    """Export all text and image assets for an account."""
    print(f"\n{'='*60}")
    print(f"Exporting {region} (Account: {customer_id})")
    print('='*60)

    export_data = {
        'region': region,
        'customer_id': customer_id,
        'export_date': datetime.now().isoformat(),
        'campaigns': {}
    }

    # Get all asset groups
    asset_groups = get_asset_groups(customer_id, manager_id)
    print(f"Found {len(asset_groups)} asset groups")

    for ag in asset_groups:
        campaign_name = ag.get('campaign', {}).get('name', 'Unknown')
        campaign_id = ag.get('campaign', {}).get('id', '')
        ag_name = ag.get('assetGroup', {}).get('name', 'Unknown')
        ag_id = ag.get('assetGroup', {}).get('id', '')

        # Initialize campaign if not exists
        if campaign_name not in export_data['campaigns']:
            export_data['campaigns'][campaign_name] = {
                'campaign_id': campaign_id,
                'asset_groups': {}
            }

        # Get text assets for this asset group
        text_assets = get_text_assets_for_asset_group(customer_id, manager_id, ag_id)

        # Get image assets for this asset group
        image_assets = get_image_assets_for_asset_group(customer_id, manager_id, ag_id)

        # Organize text assets by field type
        asset_data = {
            'asset_group_id': ag_id,
            'headlines': [],
            'long_headlines': [],
            'descriptions': [],
            'images': []
        }

        for asset in text_assets:
            field_type = asset.get('assetGroupAsset', {}).get('fieldType', '')
            text = asset.get('asset', {}).get('textAsset', {}).get('text', '')
            asset_id = asset.get('asset', {}).get('id', '')

            asset_entry = {'text': text, 'asset_id': asset_id}

            if field_type == 'HEADLINE':
                asset_data['headlines'].append(asset_entry)
            elif field_type == 'LONG_HEADLINE':
                asset_data['long_headlines'].append(asset_entry)
            elif field_type == 'DESCRIPTION':
                asset_data['descriptions'].append(asset_entry)

        # Organize image assets
        for asset in image_assets:
            field_type = asset.get('assetGroupAsset', {}).get('fieldType', '')
            asset_id = asset.get('asset', {}).get('id', '')
            asset_name = asset.get('asset', {}).get('name', '')
            width = asset.get('asset', {}).get('imageAsset', {}).get('fullSize', {}).get('widthPixels', '')
            height = asset.get('asset', {}).get('imageAsset', {}).get('fullSize', {}).get('heightPixels', '')

            image_entry = {
                'asset_id': asset_id,
                'field_type': field_type,
                'name': asset_name,
                'width': width,
                'height': height
            }
            asset_data['images'].append(image_entry)

        export_data['campaigns'][campaign_name]['asset_groups'][ag_name] = asset_data
        print(f"  ✓ {campaign_name} > {ag_name}: {len(asset_data['headlines'])}H / {len(asset_data['long_headlines'])}LH / {len(asset_data['descriptions'])}D / {len(asset_data['images'])}IMG")

    return export_data

def main():
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d')

    all_exports = {}

    for region, config in ACCOUNTS.items():
        try:
            export_data = export_account(region, config['customer_id'], config['manager_id'])
            all_exports[region] = export_data

            # Save individual region file
            region_file = os.path.join(OUTPUT_DIR, f'{timestamp}-{region.lower()}-assets.json')
            with open(region_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            print(f"\n✓ Saved: {region_file}")

        except Exception as e:
            print(f"\n✗ Error exporting {region}: {e}")

    # Save combined file
    combined_file = os.path.join(OUTPUT_DIR, f'{timestamp}-all-assets.json')
    with open(combined_file, 'w') as f:
        json.dump(all_exports, f, indent=2)
    print(f"\n✓ Saved combined: {combined_file}")

    # Print summary
    print("\n" + "="*60)
    print("EXPORT SUMMARY")
    print("="*60)
    for region, data in all_exports.items():
        campaigns = len(data.get('campaigns', {}))
        asset_groups = sum(len(c.get('asset_groups', {})) for c in data.get('campaigns', {}).values())
        print(f"  {region}: {campaigns} campaigns, {asset_groups} asset groups")

if __name__ == "__main__":
    main()
