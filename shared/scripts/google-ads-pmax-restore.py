#!/usr/bin/env python3
"""
Universal Google Ads Performance Max Restore Script

Restores PMax asset groups from backup JSON (text + images).

Usage:
    # Dry-run first (preview changes)
    python3 google-ads-pmax-restore.py --customer-id 8573235780 --manager-id 2569949686 \\
        --backup-file smythson-uk-backup.json --dry-run

    # Live restore
    python3 google-ads-pmax-restore.py --customer-id 8573235780 --manager-id 2569949686 \\
        --backup-file smythson-uk-backup.json

    # Restore without manager
    python3 google-ads-pmax-restore.py --customer-id 1234567890 \\
        --backup-file tree2mydoor-backup.json
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime
from typing import Optional

# Add the MCP server to path to use its OAuth module
MCP_SERVER_PATH = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, MCP_SERVER_PATH)

# Load env vars from MCP server
from dotenv import load_dotenv
load_dotenv(os.path.join(MCP_SERVER_PATH, '.env'))

# Import the OAuth module
from oauth.google_auth import get_headers_with_auto_token, format_customer_id


def get_headers(manager_id: Optional[str] = None):
    """Get headers for Google Ads API requests."""
    headers = get_headers_with_auto_token()
    if manager_id:
        headers['login-customer-id'] = format_customer_id(manager_id)
    return headers


def get_current_text_assets(headers, customer_id, asset_group_id):
    """Query current text asset group assets to get resource names for removal."""
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
    """

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])
    return results


def get_current_image_assets(headers, customer_id, asset_group_id):
    """Query current image assets to get resource names for removal."""
    formatted_cid = format_customer_id(customer_id)

    query = f"""
        SELECT
            asset_group_asset.resource_name,
            asset_group_asset.field_type,
            asset.id
        FROM asset_group_asset
        WHERE asset_group.id = {asset_group_id}
        AND asset_group_asset.field_type IN ('MARKETING_IMAGE', 'SQUARE_MARKETING_IMAGE', 'PORTRAIT_MARKETING_IMAGE')
    """

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])
    return results


def create_text_assets(headers, customer_id, texts):
    """Create new text assets and return their resource names."""
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


def link_image_assets(headers, customer_id, asset_group_resource, images):
    """Link image assets to asset group (images already exist, just need linking)."""
    formatted_cid = format_customer_id(customer_id)
    url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/assetGroupAssets:mutate"

    operations = []

    for img in images:
        asset_id = img['asset_id']
        field_type = img['field_type']
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
        return resp.json()

    return None


def update_asset_group_assets(headers, customer_id, asset_group_resource,
                               remove_resources, new_assets_by_type):
    """Remove old asset links and add new ones."""
    formatted_cid = format_customer_id(customer_id)
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
        return resp.json()

    return None


def restore_asset_group(headers, customer_id, campaign_id, asset_group_id,
                        asset_group_name, backup_data, dry_run=False):
    """Restore a single asset group to backup state (text AND images)."""
    formatted_cid = format_customer_id(customer_id)
    asset_group_resource = f"customers/{formatted_cid}/assetGroups/{asset_group_id}"

    print(f"\n  Processing: {asset_group_name} (ID: {asset_group_id})")

    # ===== TEXT ASSETS =====
    # Get current text assets
    current_assets = get_current_text_assets(headers, customer_id, asset_group_id)

    resources_to_remove = []
    for asset in current_assets:
        resource_name = asset.get('assetGroupAsset', {}).get('resourceName')
        if resource_name:
            resources_to_remove.append(resource_name)

    print(f"    Current text assets to remove: {len(resources_to_remove)}")

    # Get backup texts
    headlines = [h['text'] for h in backup_data.get('headlines', [])]
    long_headlines = [h['text'] for h in backup_data.get('long_headlines', [])]
    descriptions = [d['text'] for d in backup_data.get('descriptions', [])]

    print(f"    Backup headlines: {len(headlines)}")
    print(f"    Backup long headlines: {len(long_headlines)}")
    print(f"    Backup descriptions: {len(descriptions)}")

    # ===== IMAGE ASSETS =====
    # Get current image assets
    current_images = get_current_image_assets(headers, customer_id, asset_group_id)

    image_resources_to_remove = []
    for asset in current_images:
        resource_name = asset.get('assetGroupAsset', {}).get('resourceName')
        if resource_name:
            image_resources_to_remove.append(resource_name)

    print(f"    Current image assets to remove: {len(image_resources_to_remove)}")

    # Get backup images
    backup_images = backup_data.get('images', [])
    print(f"    Backup images: {len(backup_images)}")

    if dry_run:
        print(f"    [DRY RUN] Would restore:")
        print(f"      - Text: {len(headlines) + len(long_headlines) + len(descriptions)} assets")
        print(f"      - Images: {len(backup_images)} assets")
        return True

    # ===== RESTORE TEXT ASSETS =====
    all_texts = headlines + long_headlines + descriptions
    if all_texts:
        new_asset_resources = create_text_assets(headers, customer_id, all_texts)

        # Map to field types
        idx = 0
        new_assets_by_type = {
            'HEADLINE': new_asset_resources[idx:idx + len(headlines)],
        }
        idx += len(headlines)
        new_assets_by_type['LONG_HEADLINE'] = new_asset_resources[idx:idx + len(long_headlines)]
        idx += len(long_headlines)
        new_assets_by_type['DESCRIPTION'] = new_asset_resources[idx:idx + len(descriptions)]

        # Update text asset group assets
        update_asset_group_assets(
            headers, customer_id, asset_group_resource,
            resources_to_remove, new_assets_by_type
        )
        print(f"    ✓ Text assets restored")
    else:
        print(f"    ⚠️  No backup text data - skipping text restore")

    # ===== RESTORE IMAGE ASSETS =====
    if backup_images:
        # Remove current image links (separate operation)
        if image_resources_to_remove:
            formatted_cid = format_customer_id(customer_id)
            url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/assetGroupAssets:mutate"
            remove_ops = [{'remove': r} for r in image_resources_to_remove]
            payload = {'operations': remove_ops}
            resp = requests.post(url, headers=headers, json=payload)
            resp.raise_for_status()

        # Link backup images
        link_image_assets(headers, customer_id, asset_group_resource, backup_images)
        print(f"    ✓ Image assets restored ({len(backup_images)} images)")
    else:
        print(f"    ⚠️  No backup image data - skipping image restore")

    print(f"    ✓ Rollback complete")
    return True


def restore_from_backup(customer_id: str, manager_id: Optional[str],
                        backup_file: str, dry_run: bool = False):
    """Restore all assets from backup file."""

    # Load backup
    if not os.path.exists(backup_file):
        raise FileNotFoundError(f"Backup file not found: {backup_file}")

    with open(backup_file, 'r') as f:
        backup = json.load(f)

    print(f"\n{'='*80}")
    print(f"RESTORE FROM BACKUP")
    print(f"Customer ID: {customer_id}")
    print(f"Backup file: {backup_file}")
    print(f"Backup date: {backup.get('export_date', 'Unknown')}")
    print(f"{'='*80}")

    if dry_run:
        print("[DRY RUN MODE - No changes will be made]")

    headers = get_headers(manager_id)

    success_count = 0
    fail_count = 0

    for campaign_name, campaign_data in backup.get('campaigns', {}).items():
        campaign_id = campaign_data.get('campaign_id')
        print(f"\nCampaign: {campaign_name} (ID: {campaign_id})")

        for asset_group_name, group_data in campaign_data.get('asset_groups', {}).items():
            asset_group_id = group_data.get('asset_group_id')

            try:
                result = restore_asset_group(
                    headers, customer_id, campaign_id, asset_group_id,
                    asset_group_name, group_data, dry_run
                )
                if result:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
                fail_count += 1

    return success_count, fail_count


def main():
    parser = argparse.ArgumentParser(
        description='Universal Google Ads PMax Restore - Restore text + images from backup',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry-run first (preview changes)
  %(prog)s --customer-id 8573235780 --manager-id 2569949686 --backup-file uk.json --dry-run

  # Live restore
  %(prog)s --customer-id 8573235780 --manager-id 2569949686 --backup-file uk.json

  # Restore without manager account
  %(prog)s --customer-id 1234567890 --backup-file backup.json
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
        '--backup-file',
        required=True,
        help='Path to backup JSON file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be restored without making changes'
    )
    args = parser.parse_args()

    print(f"\nGoogle Ads PMax Restore Tool")
    print(f"Started: {datetime.now().isoformat()}")

    try:
        success, fail = restore_from_backup(
            args.customer_id,
            args.manager_id,
            args.backup_file,
            args.dry_run
        )

        print(f"\n{'='*80}")
        print(f"RESTORE SUMMARY")
        print(f"{'='*80}")
        print(f"Successful: {success}")
        print(f"Failed: {fail}")
        print(f"Completed: {datetime.now().isoformat()}")

        if args.dry_run:
            print(f"\n[DRY RUN COMPLETE - Run without --dry-run to apply changes]")

        print(f"{'='*80}\n")

        if fail > 0:
            sys.exit(1)

    except Exception as e:
        print(f"\n{'='*80}")
        print(f"❌ RESTORE FAILED")
        print(f"{'='*80}")
        print(f"Error: {str(e)}")
        print(f"{'='*80}\n")
        sys.exit(1)

    print(f"Completed: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
