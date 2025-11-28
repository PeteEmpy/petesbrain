#!/usr/bin/env python3
"""
Cleanup test swaps - Remove the paused assets and new assets from test execution
"""

import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

from asset_swap_engine import AssetSwapEngine

# Initialize engine
engine = AssetSwapEngine("4941701449", dry_run=False)
if not engine.initialise_client():
    print("Failed to initialize client")
    sys.exit(1)

print("Cleaning up test swaps...")

# Asset Group 1: 6512862055 (Olive Trees)
# Remove NEW asset: "Olive Trees With Lifetime Care" (311708177231)
# Re-enable OLD asset: "Buy Olive Trees Online" (243829330268)

print("\n1. Asset Group 6512862055:")
print("   Removing NEW: Olive Trees With Lifetime Care (311708177231)")
success1 = engine._remove_asset("6512862055", "311708177231", "HEADLINE")

print("   Re-enabling OLD: Buy Olive Trees Online (243829330268)")
# Change status from PAUSED to ENABLED
ga_service = engine.client.get_service("GoogleAdsService")
asset_group_asset_service = engine.client.get_service("AssetGroupAssetService")

from google.protobuf import field_mask_pb2

# Find the paused asset
query = """
    SELECT asset_group_asset.resource_name
    FROM asset_group_asset
    WHERE asset_group.id = 6512862055
      AND asset.id = 243829330268
      AND asset_group_asset.field_type = 'HEADLINE'
      AND asset_group_asset.status = 'PAUSED'
"""

response = ga_service.search(customer_id="4941701449", query=query)
resource_names = [row.asset_group_asset.resource_name for row in response]

if resource_names:
    for resource_name in resource_names:
        operation = engine.client.get_type("AssetGroupAssetOperation")
        asset_group_asset = operation.update
        asset_group_asset.resource_name = resource_name
        asset_group_asset.status = engine.client.enums.AssetLinkStatusEnum.ENABLED

        field_mask = field_mask_pb2.FieldMask(paths=["status"])
        operation.update_mask.CopyFrom(field_mask)

        asset_group_asset_service.mutate_asset_group_assets(
            customer_id="4941701449",
            operations=[operation]
        )
        print(f"   ✅ Re-enabled: {resource_name}")
else:
    print("   ⚠️  Old asset not found or not paused")

# Asset Group 2: 6512845613 (Bay Trees)
print("\n2. Asset Group 6512845613:")
print("   Removing NEW: Premium UK Bay Tree Gifts (311708181638)")
success2 = engine._remove_asset("6512845613", "311708181638", "HEADLINE")

print("   Re-enabling OLD: UK Grown Bay Trees (268224962765)")

query = """
    SELECT asset_group_asset.resource_name
    FROM asset_group_asset
    WHERE asset_group.id = 6512845613
      AND asset.id = 268224962765
      AND asset_group_asset.field_type = 'HEADLINE'
      AND asset_group_asset.status = 'PAUSED'
"""

response = ga_service.search(customer_id="4941701449", query=query)
resource_names = [row.asset_group_asset.resource_name for row in response]

if resource_names:
    for resource_name in resource_names:
        operation = engine.client.get_type("AssetGroupAssetOperation")
        asset_group_asset = operation.update
        asset_group_asset.resource_name = resource_name
        asset_group_asset.status = engine.client.enums.AssetLinkStatusEnum.ENABLED

        field_mask = field_mask_pb2.FieldMask(paths=["status"])
        operation.update_mask.CopyFrom(field_mask)

        asset_group_asset_service.mutate_asset_group_assets(
            customer_id="4941701449",
            operations=[operation]
        )
        print(f"   ✅ Re-enabled: {resource_name}")
else:
    print("   ⚠️  Old asset not found or not paused")

print("\n✅ Cleanup complete!")
print("Both asset groups should now be back to original state")
