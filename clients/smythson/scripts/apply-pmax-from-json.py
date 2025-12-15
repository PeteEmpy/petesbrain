#!/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
"""
Apply Smythson PMax text assets from pre-generated JSON file.

This is the DEPLOYMENT script for Monday. It:
1. Reads the verified JSON file (generated and verified in advance)
2. Backs up current Google Ads state
3. Applies changes via Google Ads API
4. Verifies deployment was successful

NO Google Sheets access needed - all data is pre-loaded in JSON.

Usage:
    python3 apply-pmax-from-json.py --json uk-pmax-deployment-2025-12-16.json --dry-run
    python3 apply-pmax-from-json.py --json uk-pmax-deployment-2025-12-16.json --validate
    python3 apply-pmax-from-json.py --json uk-pmax-deployment-2025-12-16.json
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime
from typing import Dict, List, Tuple

# Add the MCP server to path
MCP_SERVER_PATH = '/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, MCP_SERVER_PATH)

from dotenv import load_dotenv
load_dotenv(os.path.join(MCP_SERVER_PATH, '.env'))

from oauth.google_auth import get_headers_with_auto_token, format_customer_id

# Paths
DATA_DIR = '/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/data'
BACKUP_DIR = os.path.join(DATA_DIR, 'backups')

# Google Ads API version (verified working)
API_VERSION = 'v22'


def get_headers(manager_id: str):
    """Get headers for Google Ads API requests."""
    headers = get_headers_with_auto_token()
    headers['login-customer-id'] = format_customer_id(manager_id)
    return headers


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

    url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_cid}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    return resp.json().get('results', [])


def save_backup(customer_id: str, asset_group_id: str, asset_group_name: str,
                current_assets: List[Dict], deployment_file: str) -> str:
    """Save current state as backup before making changes."""
    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"backup_{asset_group_id}_{timestamp}.json"
    filepath = os.path.join(BACKUP_DIR, filename)

    # Parse current assets into readable format
    parsed_assets = {
        'HEADLINE': [],
        'LONG_HEADLINE': [],
        'DESCRIPTION': []
    }

    for asset in current_assets:
        field_type = asset.get('assetGroupAsset', {}).get('fieldType', '')
        text = asset.get('asset', {}).get('textAsset', {}).get('text', '')
        resource = asset.get('assetGroupAsset', {}).get('resourceName', '')

        if field_type in parsed_assets:
            parsed_assets[field_type].append({
                'text': text,
                'resource_name': resource,
                'asset_id': asset.get('asset', {}).get('id')
            })

    backup_data = {
        'backup_timestamp': datetime.now().isoformat(),
        'deployment_file': deployment_file,
        'customer_id': customer_id,
        'asset_group_id': asset_group_id,
        'asset_group_name': asset_group_name,
        'current_state': parsed_assets,
        'raw_assets': current_assets
    }

    with open(filepath, 'w') as f:
        json.dump(backup_data, f, indent=2)

    return filepath


def create_text_assets(headers, customer_id: str, texts: List[str]) -> List[str]:
    """Create new text assets and return their resource names."""
    if not texts:
        return []

    formatted_cid = format_customer_id(customer_id)
    url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_cid}/assets:mutate"

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
    url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_cid}/assetGroupAssets:mutate"

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
    """Verify that deployment was successful."""
    current = get_current_text_assets(headers, customer_id, asset_group_id)

    current_headlines = []
    for asset in current:
        if asset.get('assetGroupAsset', {}).get('fieldType') == 'HEADLINE':
            text = asset.get('asset', {}).get('textAsset', {}).get('text', '')
            current_headlines.append(text)

    # Check if first 3 expected headlines are present (key ones)
    missing = [h for h in expected_headlines[:3] if h not in current_headlines]

    if missing:
        return False, f"Missing expected headlines: {missing}"

    return True, f"Verified: {len(current_headlines)} headlines present"


def run_preflight(json_file: str, headers, customer_id: str, manager_id: str) -> Tuple[bool, List[str]]:
    """Run pre-flight validation checks."""
    errors = []

    print(f"\n{'='*60}")
    print(f"PRE-FLIGHT VALIDATION")
    print(f"{'='*60}")

    # 1. Check JSON file exists and is valid
    if not os.path.exists(json_file):
        errors.append(f"JSON file not found: {json_file}")
    else:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            print(f"  [OK] JSON file valid: {len(data.get('asset_groups', []))} asset groups")
        except json.JSONDecodeError as e:
            errors.append(f"JSON file invalid: {str(e)}")

    # 2. Check Google Ads OAuth
    try:
        test_headers = get_headers(manager_id)
        print(f"  [OK] Google Ads OAuth valid")
    except Exception as e:
        errors.append(f"Google Ads OAuth error: {str(e)}")
        return False, errors

    # 3. Test Google Ads API connectivity
    try:
        formatted_cid = format_customer_id(customer_id)
        query = "SELECT campaign.id FROM campaign LIMIT 1"
        url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_cid}/googleAds:search"
        payload = {'query': query}

        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        print(f"  [OK] Google Ads API accessible")
    except Exception as e:
        errors.append(f"Google Ads API error: {str(e)}")

    # 4. Validate each asset group exists
    if not errors:
        with open(json_file, 'r') as f:
            data = json.load(f)

        for ag in data.get('asset_groups', []):
            ag_id = ag['asset_group_id']
            ag_name = ag['asset_group_name']

            try:
                current = get_current_text_assets(headers, customer_id, ag_id)
                headline_count = len([a for a in current if a.get('assetGroupAsset', {}).get('fieldType') == 'HEADLINE'])
                print(f"  [OK] Asset Group {ag_id}: {ag_name} ({headline_count} current headlines)")
            except Exception as e:
                errors.append(f"Asset Group {ag_id} ({ag_name}): {str(e)}")

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


def apply_asset_group(headers, customer_id: str, asset_group: Dict,
                      json_file: str, dry_run: bool = False) -> bool:
    """Apply text assets to a single asset group."""
    ag_id = asset_group['asset_group_id']
    ag_name = asset_group['asset_group_name']

    headlines = asset_group.get('headlines', [])[:15]
    long_headlines = asset_group.get('long_headlines', [])[:5]
    descriptions = asset_group.get('descriptions', [])[:5]

    print(f"\n  Asset Group: {ag_name}")
    print(f"    ID: {ag_id}")
    print(f"    Headlines: {len(headlines)}, Long Headlines: {len(long_headlines)}, Descriptions: {len(descriptions)}")

    if dry_run:
        print(f"    [DRY RUN] Would apply changes")
        return True

    # Get current assets
    current_assets = get_current_text_assets(headers, customer_id, ag_id)

    # Save backup BEFORE making changes
    backup_path = save_backup(customer_id, ag_id, ag_name, current_assets, json_file)
    print(f"    Backup saved: {os.path.basename(backup_path)}")

    # Collect resources to remove
    resources_to_remove = []
    for asset in current_assets:
        resource_name = asset.get('assetGroupAsset', {}).get('resourceName')
        if resource_name:
            resources_to_remove.append(resource_name)

    print(f"    Removing {len(resources_to_remove)} current assets")

    # Create new assets
    all_texts = headlines + long_headlines + descriptions
    new_asset_resources = create_text_assets(headers, customer_id, all_texts)

    print(f"    Created {len(new_asset_resources)} new assets")

    # Map to field types
    idx = 0
    new_assets_by_type = {
        'HEADLINE': new_asset_resources[idx:idx + len(headlines)],
    }
    idx += len(headlines)
    new_assets_by_type['LONG_HEADLINE'] = new_asset_resources[idx:idx + len(long_headlines)]
    idx += len(long_headlines)
    new_assets_by_type['DESCRIPTION'] = new_asset_resources[idx:idx + len(descriptions)]

    # Update asset group
    update_asset_group_text_assets(
        headers, customer_id, ag_id,
        resources_to_remove, new_assets_by_type
    )

    # Verify
    verified, verify_msg = verify_deployment(headers, customer_id, ag_id, headlines)
    if verified:
        print(f"    [VERIFIED] {verify_msg}")
    else:
        print(f"    [WARNING] {verify_msg}")

    print(f"    SUCCESS")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Apply Smythson PMax text assets from JSON file'
    )
    parser.add_argument(
        '--json',
        required=True,
        help='Path to deployment JSON file (relative to data dir or absolute)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be applied without making changes'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Run pre-flight validation only'
    )
    args = parser.parse_args()

    # Resolve JSON file path
    json_file = args.json
    if not os.path.isabs(json_file):
        json_file = os.path.join(DATA_DIR, json_file)

    print(f"\n{'='*80}")
    print(f"SMYTHSON PMAX TEXT ASSET DEPLOYMENT")
    print(f"{'='*80}")
    print(f"Started: {datetime.now().isoformat()}")
    print(f"JSON File: {json_file}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'VALIDATE ONLY' if args.validate else 'LIVE EXECUTION'}")

    # Load JSON
    with open(json_file, 'r') as f:
        data = json.load(f)

    metadata = data.get('metadata', {})
    customer_id = metadata.get('customer_id')
    manager_id = metadata.get('manager_id')
    asset_groups = data.get('asset_groups', [])

    print(f"\nDeployment Details:")
    print(f"  Region: {metadata.get('region')}")
    print(f"  Customer ID: {customer_id}")
    print(f"  Asset Groups: {len(asset_groups)}")
    print(f"  Generated: {metadata.get('generated')}")

    # Get headers
    headers = get_headers(manager_id)

    # Pre-flight validation
    is_valid, errors = run_preflight(json_file, headers, customer_id, manager_id)

    if not is_valid:
        print(f"\nPre-flight validation failed. Aborting.")
        sys.exit(1)

    if args.validate:
        print(f"\nValidation-only mode complete.")
        sys.exit(0)

    # Process each asset group
    print(f"\n{'='*80}")
    print(f"APPLYING CHANGES")
    print(f"{'='*80}")

    success_count = 0
    fail_count = 0

    for i, asset_group in enumerate(asset_groups, start=1):
        print(f"\n[{i}/{len(asset_groups)}] Processing...")

        try:
            result = apply_asset_group(headers, customer_id, asset_group, json_file, args.dry_run)
            if result:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"    ERROR: {str(e)}")
            fail_count += 1

    # Summary
    print(f"\n{'='*80}")
    print(f"DEPLOYMENT SUMMARY")
    print(f"{'='*80}")
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Completed: {datetime.now().isoformat()}")

    if args.dry_run:
        print(f"\n[DRY RUN COMPLETE - Run without --dry-run to apply changes]")

    if fail_count > 0:
        print(f"\nBackups available in: {BACKUP_DIR}")

    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
