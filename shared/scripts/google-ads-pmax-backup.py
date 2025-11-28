#!/usr/bin/env python3
"""
Universal Google Ads Performance Max Backup Script

Creates complete backup of PMax asset groups (text + images) for any Google Ads account.

Usage:
    # Backup single account
    python3 google-ads-pmax-backup.py --customer-id 8573235780 --manager-id 2569949686 \\
        --output-file smythson-uk-backup.json

    # Backup without manager
    python3 google-ads-pmax-backup.py --customer-id 1234567890 \\
        --output-file tree2mydoor-backup.json

    # Custom output directory
    python3 google-ads-pmax-backup.py --customer-id 8573235780 --manager-id 2569949686 \\
        --output-dir /path/to/backups --output-file uk-assets.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Optional

# Add the MCP server path to import OAuth helper
MCP_SERVER_PATH = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, MCP_SERVER_PATH)

# Load env vars from MCP server
from dotenv import load_dotenv
load_dotenv(os.path.join(MCP_SERVER_PATH, '.env'))

from oauth.google_auth import execute_gaql


def get_asset_groups(customer_id: str, manager_id: Optional[str] = None) -> list:
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
    result = execute_gaql(customer_id, query, manager_id or '')
    return result.get('results', [])


def get_text_assets_for_asset_group(customer_id: str, manager_id: Optional[str], asset_group_id: str) -> list:
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
    result = execute_gaql(customer_id, query, manager_id or '')
    return result.get('results', [])


def get_image_assets_for_asset_group(customer_id: str, manager_id: Optional[str], asset_group_id: str) -> list:
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
    result = execute_gaql(customer_id, query, manager_id or '')
    return result.get('results', [])


def backup_account(customer_id: str, manager_id: Optional[str] = None,
                   account_name: str = "Account") -> dict:
    """Backup all text and image assets for an account."""
    print(f"\n{'='*80}")
    print(f"Backing up {account_name} (Customer ID: {customer_id})")
    print('='*80)

    export_data = {
        'account_name': account_name,
        'customer_id': customer_id,
        'manager_id': manager_id or '',
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

        # Get text assets
        text_assets = get_text_assets_for_asset_group(customer_id, manager_id, ag_id)

        # Get image assets
        image_assets = get_image_assets_for_asset_group(customer_id, manager_id, ag_id)

        # Organise assets by field type
        asset_data = {
            'asset_group_id': ag_id,
            'headlines': [],
            'long_headlines': [],
            'descriptions': [],
            'images': []
        }

        # Process text assets
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

        # Process image assets
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

        h_count = len(asset_data['headlines'])
        lh_count = len(asset_data['long_headlines'])
        d_count = len(asset_data['descriptions'])
        i_count = len(asset_data['images'])

        print(f"  ✓ {campaign_name} > {ag_name}: {h_count}H / {lh_count}LH / {d_count}D / {i_count}IMG")

    return export_data


def main():
    parser = argparse.ArgumentParser(
        description='Universal Google Ads PMax Backup - Backup text + images for any account',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Backup single account
  %(prog)s --customer-id 8573235780 --manager-id 2569949686 --output-file smythson-uk.json

  # Backup without manager account
  %(prog)s --customer-id 1234567890 --output-file tree2mydoor.json

  # Custom output directory
  %(prog)s --customer-id 8573235780 --output-dir /path/to/backups --output-file uk.json
        """
    )
    parser.add_argument(
        '--customer-id',
        required=True,
        help='Google Ads customer ID (10 digits, no dashes)'
    )
    parser.add_argument(
        '--manager-id',
        help='Manager account ID (if accessing via manager account)'
    )
    parser.add_argument(
        '--output-file',
        required=True,
        help='Output filename (e.g., smythson-uk-backup.json)'
    )
    parser.add_argument(
        '--output-dir',
        default=None,
        help='Output directory (default: current directory)'
    )
    parser.add_argument(
        '--account-name',
        default='Account',
        help='Friendly name for this account (e.g., "Smythson UK")'
    )
    args = parser.parse_args()

    print(f"\nGoogle Ads PMax Backup Tool")
    print(f"Started: {datetime.now().isoformat()}")

    # Backup the account
    try:
        backup_data = backup_account(
            args.customer_id,
            args.manager_id,
            args.account_name
        )

        # Determine output path
        if args.output_dir:
            os.makedirs(args.output_dir, exist_ok=True)
            output_path = os.path.join(args.output_dir, args.output_file)
        else:
            output_path = args.output_file

        # Save to file
        with open(output_path, 'w') as f:
            json.dump(backup_data, f, indent=2)

        print(f"\n{'='*80}")
        print(f"✅ BACKUP SUCCESSFUL")
        print(f"{'='*80}")

        campaigns = len(backup_data.get('campaigns', {}))
        asset_groups = sum(
            len(c.get('asset_groups', {}))
            for c in backup_data.get('campaigns', {}).values()
        )

        print(f"Account: {args.account_name}")
        print(f"Customer ID: {args.customer_id}")
        print(f"Campaigns: {campaigns}")
        print(f"Asset Groups: {asset_groups}")
        print(f"Saved to: {output_path}")
        print(f"{'='*80}\n")

    except Exception as e:
        print(f"\n{'='*80}")
        print(f"❌ BACKUP FAILED")
        print(f"{'='*80}")
        print(f"Error: {str(e)}")
        print(f"{'='*80}\n")
        sys.exit(1)

    print(f"Completed: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
