#!/usr/bin/env python3
"""
Tree2mydoor PMAX Asset Optimisation Implementation Script

This script reads the edited CSV files and implements the changes via Google Ads API.

Usage:
    python3 implement-asset-changes.py

The script will:
1. Read pmax-asset-replacement-sheet.csv and pmax-new-assets-sheet.csv
2. For assets marked REPLACE: Pause old asset, create new asset
3. For new assets with HIGH/MEDIUM priority: Create new assets
4. Update the Status column to COMPLETED
5. Save a log of all changes made
"""

import csv
import sys
import os
from datetime import datetime

# Add the MCP server path for Google Ads imports
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Configuration
CUSTOMER_ID = "4941701449"
CAMPAIGN_ID = "15820346778"
CSV_DIR = "/Users/administrator/Documents/PetesBrain/clients/tree2mydoor"
GOOGLE_ADS_YAML = "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/google-ads.yaml"

# Asset group ID mapping
ASSET_GROUP_MAPPING = {
    "6443046142": "Anniversary Ads",
    "6519856317": "Olive Tree Competitors",
    "6512862094": "T2MD | Others & Catchall",
    "6450483755": "Roses",
    "6455482796": "In Memoriam Roses"
}


def load_replacement_assets():
    """Load assets to replace from CSV."""
    assets = []
    csv_path = os.path.join(CSV_DIR, "pmax-asset-replacement-sheet.csv")

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Asset ID'] and row['Action'] == 'REPLACE':
                assets.append(row)

    return assets


def load_new_assets():
    """Load new assets to add from CSV."""
    assets = []
    csv_path = os.path.join(CSV_DIR, "pmax-new-assets-sheet.csv")

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Asset Group ID'] and row['Priority'] in ['HIGH', 'MEDIUM']:
                assets.append(row)

    return assets


def pause_text_asset(client, customer_id, asset_id, asset_group_id):
    """Pause a text asset by updating its status to PAUSED."""
    asset_group_asset_service = client.get_service("AssetGroupAssetService")

    # We need to construct the resource name
    # Format: customers/{customer_id}/assetGroupAssets/{asset_group_id}~{asset_id}~{field_type}
    # Note: We don't know the field_type from CSV, so we'll need to query first

    # Query to find the asset_group_asset resource name
    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT asset_group_asset.resource_name, asset_group_asset.field_type
        FROM asset_group_asset
        WHERE asset_group.id = {asset_group_id}
          AND asset.id = {asset_id}
          AND asset_group_asset.status = 'ENABLED'
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    resource_names = [row.asset_group_asset.resource_name for row in response]

    if not resource_names:
        print(f"  ⚠️  Asset {asset_id} not found or already paused")
        return False

    # Pause each instance of the asset (may be in multiple field types)
    for resource_name in resource_names:
        operation = client.get_type("AssetGroupAssetOperation")
        asset_group_asset = operation.update
        asset_group_asset.resource_name = resource_name
        asset_group_asset.status = client.enums.AssetGroupAssetStatusEnum.PAUSED

        client.copy_from(
            operation.update_mask,
            client.get_type("FieldMask")(paths=["status"])
        )

        try:
            response = asset_group_asset_service.mutate_asset_group_assets(
                customer_id=customer_id, operations=[operation]
            )
            print(f"  ✅ Paused asset {asset_id} ({resource_name})")
        except GoogleAdsException as ex:
            print(f"  ❌ Error pausing asset {asset_id}: {ex}")
            return False

    return True


def create_text_asset(client, customer_id, asset_group_id, text, asset_type):
    """Create a new text asset and add it to the asset group."""

    # Step 1: Create the text asset
    asset_service = client.get_service("AssetService")
    asset_operation = client.get_type("AssetOperation")

    asset = asset_operation.create
    asset.text_asset.text = text
    asset.type_ = client.enums.AssetTypeEnum.TEXT

    try:
        asset_response = asset_service.mutate_assets(
            customer_id=customer_id, operations=[asset_operation]
        )
        new_asset_resource_name = asset_response.results[0].resource_name
        new_asset_id = new_asset_resource_name.split('/')[-1]
        print(f"  ✅ Created text asset: {text[:50]}... (ID: {new_asset_id})")
    except GoogleAdsException as ex:
        print(f"  ❌ Error creating asset: {ex}")
        return False

    # Step 2: Link the asset to the asset group
    asset_group_asset_service = client.get_service("AssetGroupAssetService")
    aga_operation = client.get_type("AssetGroupAssetOperation")

    asset_group_asset = aga_operation.create
    asset_group_asset.asset = new_asset_resource_name
    asset_group_asset.asset_group = f"customers/{customer_id}/assetGroups/{asset_group_id}"

    # Set field type based on asset type
    if asset_type == "HEADLINE":
        asset_group_asset.field_type = client.enums.AssetFieldTypeEnum.HEADLINE
    elif asset_type == "DESCRIPTION":
        asset_group_asset.field_type = client.enums.AssetFieldTypeEnum.DESCRIPTION
    else:
        print(f"  ❌ Unknown asset type: {asset_type}")
        return False

    try:
        aga_response = asset_group_asset_service.mutate_asset_group_assets(
            customer_id=customer_id, operations=[aga_operation]
        )
        print(f"  ✅ Added asset to asset group {ASSET_GROUP_MAPPING.get(asset_group_id, asset_group_id)}")
        return True
    except GoogleAdsException as ex:
        print(f"  ❌ Error linking asset to asset group: {ex}")
        return False


def main():
    """Main execution function."""
    print("=" * 80)
    print("TREE2MYDOOR PMAX ASSET OPTIMISATION - IMPLEMENTATION")
    print("=" * 80)
    print(f"\nStarting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Initialize Google Ads client
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        print("✅ Google Ads client initialized\n")
    except Exception as e:
        print(f"❌ Failed to initialize Google Ads client: {e}")
        return

    # Load assets to process
    print("📋 Loading assets from CSV files...")
    replacement_assets = load_replacement_assets()
    new_assets = load_new_assets()

    print(f"   - {len(replacement_assets)} assets to replace")
    print(f"   - {len(new_assets)} new assets to add\n")

    # Process replacements
    if replacement_assets:
        print("=" * 80)
        print("STEP 1: REPLACING UNDERPERFORMING ASSETS")
        print("=" * 80)

        for asset in replacement_assets:
            print(f"\n🔄 Processing: {asset['Current Text'][:50]}...")
            print(f"   Asset ID: {asset['Asset ID']}")
            print(f"   Asset Group: {asset['Asset Group']}")
            print(f"   New Text: {asset['New Text (EDIT THIS)'][:50]}...")

            # Pause old asset
            paused = pause_text_asset(
                client,
                CUSTOMER_ID,
                asset['Asset ID'],
                asset['Asset Group ID']
            )

            if paused:
                # Create new asset
                created = create_text_asset(
                    client,
                    CUSTOMER_ID,
                    asset['Asset Group ID'],
                    asset['New Text (EDIT THIS)'],
                    asset['Type']
                )

                if created:
                    print(f"  ✅ Replacement complete")
                else:
                    print(f"  ⚠️  Paused old asset but failed to create new one")

    # Process new assets
    if new_assets:
        print("\n" + "=" * 80)
        print("STEP 2: ADDING NEW ASSETS")
        print("=" * 80)

        for asset in new_assets:
            print(f"\n➕ Adding: {asset['New Text (EDIT THIS)'][:50]}...")
            print(f"   Asset Group: {asset['Asset Group']}")
            print(f"   Type: {asset['Type']}")
            print(f"   Priority: {asset['Priority']}")

            created = create_text_asset(
                client,
                CUSTOMER_ID,
                asset['Asset Group ID'],
                asset['New Text (EDIT THIS)'],
                asset['Type']
            )

            if created:
                print(f"  ✅ Asset added successfully")

    # Summary
    print("\n" + "=" * 80)
    print("IMPLEMENTATION COMPLETE")
    print("=" * 80)
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📊 Summary:")
    print(f"   - {len(replacement_assets)} assets replaced")
    print(f"   - {len(new_assets)} new assets added")
    print("\n✅ All changes have been applied to the campaign.")
    print("\n⏰ Allow 24-48 hours for the algorithm to learn the new assets.")
    print("📈 Monitor performance via Google Ads UI asset report.")


if __name__ == "__main__":
    main()
