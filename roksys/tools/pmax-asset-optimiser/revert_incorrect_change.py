#!/usr/bin/env python3
"""
Revert Incorrect Asset Change - Remove wrongly added asset and restore original

This script reverts the incorrect change made to Lemon Trees asset group:
- Remove: "Mediterranean Olive Trees" (305359271122) from group 6512862214
- Restore: "Big Choice - Affordable Prices" to group 6512862214

Author: PetesBrain
Created: 2025-11-27
"""

from asset_swap_engine import AssetSwapEngine

def main():
    print("="*80)
    print("REVERTING INCORRECT ASSET CHANGE")
    print("="*80)
    print("Customer ID: 4941701449")
    print("Asset Group: 6512862214 (Lemon Trees)")
    print()
    print("Action:")
    print("  1. Remove: Mediterranean Olive Trees (305359271122)")
    print("  2. Restore: Big Choice - Affordable Prices")
    print("="*80)
    print()

    # Ask for confirmation
    response = input("Proceed with revert? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Revert cancelled")
        return

    # Initialize engine in LIVE mode
    engine = AssetSwapEngine('4941701449', dry_run=False)
    if not engine.initialise_client():
        print("❌ Failed to initialize Google Ads client")
        return

    asset_group_id = '6512862214'
    field_type = 'HEADLINE'

    # Step 1: Remove incorrect asset
    print("\n🗑️  Step 1: Removing incorrect asset...")
    print("   Asset: Mediterranean Olive Trees (305359271122)")

    if engine._remove_asset(asset_group_id, '305359271122', field_type):
        print("   ✅ Successfully removed incorrect asset")
    else:
        print("   ❌ Failed to remove incorrect asset")
        return

    # Step 2: Restore original asset
    print("\n📝 Step 2: Restoring original asset...")
    print("   Asset: Big Choice - Affordable Prices")

    # Create the asset
    new_asset_id = engine._create_text_asset("Big Choice - Affordable Prices")
    if not new_asset_id:
        print("   ❌ Failed to create asset")
        return

    print(f"   ✅ Created asset (ID: {new_asset_id})")

    # Link to group
    if engine._link_asset_to_group(asset_group_id, new_asset_id, field_type):
        print(f"   ✅ Successfully linked asset to group")
    else:
        print(f"   ❌ Failed to link asset to group")
        return

    print("\n" + "="*80)
    print("✅ REVERT COMPLETE")
    print("="*80)
    print()
    print("Summary:")
    print("  - Removed: Mediterranean Olive Trees (305359271122)")
    print(f"  - Restored: Big Choice - Affordable Prices ({new_asset_id})")
    print()
    print("The Lemon Trees asset group has been restored to its original state.")
    print("="*80)

if __name__ == '__main__':
    main()
