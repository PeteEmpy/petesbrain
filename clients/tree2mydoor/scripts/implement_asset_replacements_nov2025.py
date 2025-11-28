#!/usr/bin/env python3
"""
Tree2mydoor PMAX Asset Text Replacement Script
November 2025

Replaces 16 underperforming text assets with optimised alternatives.

Strategy:
1. Pause old assets (don't delete - keep for reference)
2. Create new text assets with improved copy
3. Link new assets to same asset groups
4. Monitor for 14 days before removing old assets

Customer ID: 4941701449
Campaign ID: 15820346778
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Configuration
CUSTOMER_ID = "4941701449"
CAMPAIGN_ID = "15820346778"

# Asset replacements (old_asset_id, asset_group_id, field_type, new_text)
REPLACEMENTS = [
    # Anniversary Ads (Asset Group ID: 6443046142)
    {
        "asset_group_id": "6443046142",
        "asset_group_name": "Anniversary Ads",
        "old_asset_id": "250382365640",
        "field_type": "HEADLINE",
        "old_text": "Gifts That Grow & Bloom",
        "new_text": "Rose Bushes That Last Forever"
    },
    {
        "asset_group_id": "6443046142",
        "asset_group_name": "Anniversary Ads",
        "old_asset_id": "250382365643",
        "field_type": "HEADLINE",
        "old_text": "Scrap The Cut Flowers",
        "new_text": "Roses That Return Each Year"
    },
    {
        "asset_group_id": "6443046142",
        "asset_group_name": "Anniversary Ads",
        "old_asset_id": "250382365649",
        "field_type": "HEADLINE",
        "old_text": "Gifts That Actually Last",
        "new_text": "Roses That Bloom Every Year"
    },
    {
        "asset_group_id": "6443046142",
        "asset_group_name": "Anniversary Ads",
        "old_asset_id": "250382365658",
        "field_type": "LONG_HEADLINE",
        "old_text": "Why gift roses that wilt? Send living rose bushes that bloom every anniversary.!",
        "new_text": "Why gift roses that wilt? Send living rose bushes that bloom every anniversary."
    },

    # Fab Birthday Roses (Asset Group ID: 6449408517)
    {
        "asset_group_id": "6449408517",
        "asset_group_name": "Fab Birthday Roses",
        "old_asset_id": "101959862",
        "field_type": "HEADLINE",
        "old_text": "The Ultimate Green Gift",
        "new_text": "Birthday Rose Bush Gifts"
    },
    {
        "asset_group_id": "6449408517",
        "asset_group_name": "Fab Birthday Roses",
        "old_asset_id": "8328637908",
        "field_type": "HEADLINE",
        "old_text": "Big Choice - Affordable Prices",
        "new_text": "50+ Birthday Rose Varieties"
    },
    {
        "asset_group_id": "6449408517",
        "asset_group_name": "Fab Birthday Roses",
        "old_asset_id": "36386815660",
        "field_type": "HEADLINE",
        "old_text": "Great Selection To Choose From",
        "new_text": "Choose From 50+ Rose Bushes"
    },
    {
        "asset_group_id": "6449408517",
        "asset_group_name": "Fab Birthday Roses",
        "old_asset_id": "47180789641",
        "field_type": "HEADLINE",
        "old_text": "Fab Rose Bushes",
        "new_text": "Fabulous Birthday Rose Gifts"
    },

    # In Memoriam Roses (Asset Group ID: 6455482796)
    {
        "asset_group_id": "6455482796",
        "asset_group_name": "In Memoriam Roses",
        "old_asset_id": "8328637908",
        "field_type": "HEADLINE",
        "old_text": "Big Choice - Affordable Prices",
        "new_text": "Thoughtful Memorial Roses"
    },
    {
        "asset_group_id": "6455482796",
        "asset_group_name": "In Memoriam Roses",
        "old_asset_id": "9226636104",
        "field_type": "HEADLINE",
        "old_text": "The Perfect Sustainable Gift",
        "new_text": "Lasting Memorial Rose Gifts"
    },
    {
        "asset_group_id": "6455482796",
        "asset_group_name": "In Memoriam Roses",
        "old_asset_id": "13604507886",
        "field_type": "HEADLINE",
        "old_text": "Shop Online At Tree2MyDoor",
        "new_text": "Memorial Roses Delivered"
    },
    {
        "asset_group_id": "6455482796",
        "asset_group_name": "In Memoriam Roses",
        "old_asset_id": "36386815660",
        "field_type": "HEADLINE",
        "old_text": "Great Selection To Choose From",
        "new_text": "50+ Sympathy Rose Varieties"
    },
    {
        "asset_group_id": "6455482796",
        "asset_group_name": "In Memoriam Roses",
        "old_asset_id": "52328059412",
        "field_type": "HEADLINE",
        "old_text": "Fabulous Rose Bushes",
        "new_text": "Dignified Rose Bush Tributes"
    },
    {
        "asset_group_id": "6455482796",
        "asset_group_name": "In Memoriam Roses",
        "old_asset_id": "59852174882",
        "field_type": "HEADLINE",
        "old_text": "An Ethical Gift That Will Las",
        "new_text": "Ethical Memorial Rose Gifts"
    },
    {
        "asset_group_id": "6455482796",
        "asset_group_name": "In Memoriam Roses",
        "old_asset_id": "250382365490",
        "field_type": "HEADLINE",
        "old_text": "Fabulous Rose Bush Gifts",
        "new_text": "Dignified Memorial Rose Gifts"
    },
    {
        "asset_group_id": "6455482796",
        "asset_group_name": "In Memoriam Roses",
        "old_asset_id": "18275765034",
        "field_type": "LONG_HEADLINE",
        "old_text": "Carefully Selected Roses Expertly Packaged Will Ensure They'll Treasure Their Gift Forever",
        "new_text": "Carefully chosen memorial roses delivered with care and presented beautifully."
    },
    {
        "asset_group_id": "6455482796",
        "asset_group_name": "In Memoriam Roses",
        "old_asset_id": "36468001374",
        "field_type": "LONG_HEADLINE",
        "old_text": "The Rose Bush Specialists With A Huge Choice To Choose From - Next Day Delivery Available",
        "new_text": "Rose bush specialists with huge choice. Next day delivery available nationwide."
    },
]


def pause_old_asset(client, customer_id, asset_group_id, old_asset_id, field_type):
    """Pause (don't delete) the old asset"""

    asset_group_asset_service = client.get_service("AssetGroupAssetService")
    asset_group_asset_operation = client.get_type("AssetGroupAssetOperation")

    # Build resource name
    resource_name = asset_group_asset_service.asset_group_asset_path(
        customer_id,
        asset_group_id,
        old_asset_id,
        field_type
    )

    # Update to PAUSED status
    asset_group_asset_operation.update_mask.paths.append("status")
    asset_group_asset = asset_group_asset_operation.update
    asset_group_asset.resource_name = resource_name
    asset_group_asset.status = client.enums.AssetLinkStatusEnum.PAUSED

    try:
        response = asset_group_asset_service.mutate_asset_group_assets(
            customer_id=customer_id,
            operations=[asset_group_asset_operation]
        )
        return True
    except GoogleAdsException as ex:
        print(f"  ❌ Failed to pause asset {old_asset_id}: {ex}")
        return False


def create_new_text_asset(client, customer_id, text):
    """Create a new text asset"""

    asset_service = client.get_service("AssetService")
    asset_operation = client.get_type("AssetOperation")

    asset = asset_operation.create
    asset.text_asset.text = text

    try:
        response = asset_service.mutate_assets(
            customer_id=customer_id,
            operations=[asset_operation]
        )
        new_asset_id = response.results[0].resource_name.split('/')[-1]
        return new_asset_id
    except GoogleAdsException as ex:
        print(f"  ❌ Failed to create text asset '{text}': {ex}")
        return None


def link_asset_to_group(client, customer_id, asset_group_id, asset_id, field_type):
    """Link the new asset to the asset group"""

    asset_group_asset_service = client.get_service("AssetGroupAssetService")
    asset_group_asset_operation = client.get_type("AssetGroupAssetOperation")

    asset_group_asset = asset_group_asset_operation.create
    asset_group_asset.asset = asset_group_asset_service.asset_path(customer_id, asset_id)
    asset_group_asset.asset_group = asset_group_asset_service.asset_group_path(customer_id, asset_group_id)
    asset_group_asset.field_type = client.enums.AssetFieldTypeEnum[field_type]

    try:
        response = asset_group_asset_service.mutate_asset_group_assets(
            customer_id=customer_id,
            operations=[asset_group_asset_operation]
        )
        return True
    except GoogleAdsException as ex:
        print(f"  ❌ Failed to link asset {asset_id} to group {asset_group_id}: {ex}")
        return False


def implement_replacements(dry_run=True):
    """Main implementation function"""

    print("=" * 80)
    print("TREE2MYDOOR PMAX ASSET TEXT REPLACEMENT")
    print("=" * 80)
    print(f"Customer ID: {CUSTOMER_ID}")
    print(f"Campaign ID: {CAMPAIGN_ID}")
    print(f"Total Replacements: {len(REPLACEMENTS)}")
    print(f"Mode: {'DRY RUN (no changes will be made)' if dry_run else 'LIVE (changes will be made)'}")
    print("=" * 80)
    print()

    if not dry_run:
        confirm = input("⚠️  ARE YOU SURE? Type 'YES' to proceed with LIVE changes: ")
        if confirm != "YES":
            print("❌ Cancelled by user")
            return

    # Load Google Ads client
    client = GoogleAdsClient.load_from_storage('/Users/administrator/google-ads.yaml')

    success_count = 0
    failed_count = 0

    for idx, replacement in enumerate(REPLACEMENTS, 1):
        print(f"\n[{idx}/{len(REPLACEMENTS)}] {replacement['asset_group_name']} - {replacement['field_type']}")
        print(f"  OLD: {replacement['old_text']}")
        print(f"  NEW: {replacement['new_text']}")

        if dry_run:
            print("  ✓ DRY RUN - Would pause old asset and create new one")
            success_count += 1
            continue

        # Step 1: Pause old asset
        print("  → Pausing old asset...")
        pause_success = pause_old_asset(
            client,
            CUSTOMER_ID,
            replacement['asset_group_id'],
            replacement['old_asset_id'],
            replacement['field_type']
        )

        if not pause_success:
            failed_count += 1
            continue

        # Step 2: Create new text asset
        print("  → Creating new text asset...")
        new_asset_id = create_new_text_asset(
            client,
            CUSTOMER_ID,
            replacement['new_text']
        )

        if not new_asset_id:
            failed_count += 1
            continue

        print(f"  → New asset created: {new_asset_id}")

        # Step 3: Link to asset group
        print("  → Linking to asset group...")
        link_success = link_asset_to_group(
            client,
            CUSTOMER_ID,
            replacement['asset_group_id'],
            new_asset_id,
            replacement['field_type']
        )

        if link_success:
            print("  ✓ SUCCESS")
            success_count += 1
        else:
            failed_count += 1

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✓ Successful: {success_count}")
    print(f"✗ Failed: {failed_count}")
    print(f"Total: {len(REPLACEMENTS)}")

    if not dry_run and success_count > 0:
        print("\n📊 Next Steps:")
        print("1. Monitor performance in Google Ads for 14 days")
        print("2. Check asset performance labels (PENDING → LEARNING → GOOD/BEST)")
        print("3. Compare CTR and conversion rates vs old assets")
        print("4. If new assets perform well, remove old paused assets")
        print("\n📁 Old assets are PAUSED (not deleted) so you can revert if needed")


if __name__ == "__main__":
    import sys

    # Default to dry run unless --live flag is provided
    dry_run = "--live" not in sys.argv

    implement_replacements(dry_run=dry_run)
