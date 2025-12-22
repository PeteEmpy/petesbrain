#!/usr/bin/env python3
"""
Verification Script: Check for Cross-Asset-Group Contamination
Verifies that assets added during optimisation are ONLY in their intended asset groups.

Usage:
    python3 verify-pmax-asset-integrity.py

Returns:
    - List of assets that appear in multiple asset groups
    - Verification that recent changes are isolated correctly
"""

import sys
from pathlib import Path

# Add infrastructure path for MCP access
sys.path.insert(0, str(Path.home() / 'Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server'))

# Import MCP tool (will be available when run via Claude Code MCP context)
# For standalone execution, we'll use direct API calls

CUSTOMER_ID = '5898250490'
MANAGER_ID = '2569949686'
CAMPAIGN_ID = '18899261254'  # DEV | Core Properties CE & BE | P Max

# Asset groups in the campaign
ASSET_GROUPS = {
    '6456703966': 'The Devonshire Arms Hotel',
    '6456682937': 'The Cavendish Hotel',
    '6456682997': 'The Fell',
    '6456676629': 'The Beeley Inn',
    '6456703957': 'The Pilsley Inn'
}

# Assets added during December 3-4 optimisation (from asset-changes-complete-view.html)
NEWLY_ADDED_ASSETS = {
    '238389082105': {
        'text': 'Yorkshire Dales Boutique Hotel',
        'field_type': 'HEADLINE',
        'intended_asset_group': '6456703966',  # The Devonshire Arms Hotel
        'intended_property': 'The Devonshire Arms Hotel'
    },
    '314323946359': {
        'text': 'Yorkshire Country Hotel Escape',
        'field_type': 'HEADLINE',
        'intended_asset_group': '6456703966',
        'intended_property': 'The Devonshire Arms Hotel'
    },
    '314363493552': {
        'text': 'Charming Dales Hotel Rooms',
        'field_type': 'HEADLINE',
        'intended_asset_group': '6456703966',
        'intended_property': 'The Devonshire Arms Hotel'
    },
    '314363493675': {
        'text': 'Yorkshire Dales hotel with award-winning dining & luxury spa experiences.',
        'field_type': 'DESCRIPTION',
        'intended_asset_group': '6456703966',
        'intended_property': 'The Devonshire Arms Hotel'
    },
    '314323956613': {
        'text': 'Luxury Yorkshire Dales Hotel - Award-Winning Dining & Spa at Devonshire Arms',
        'field_type': 'LONG_HEADLINE',
        'intended_asset_group': '6456703966',
        'intended_property': 'The Devonshire Arms Hotel'
    },
    '314245501727': {
        'text': 'Peak District Luxury Hotel',
        'field_type': 'HEADLINE',
        'intended_asset_group': '6456682937',
        'intended_property': 'The Cavendish Hotel'
    },
    '314363541732': {
        'text': 'Luxury Peak District Hotel - Historic Charm Meets Modern Elegance at The Cavendish',
        'field_type': 'LONG_HEADLINE',
        'intended_asset_group': '6456682937',
        'intended_property': 'The Cavendish Hotel'
    },
    '314245502354': {
        'text': 'Indulge in Fine Dining & Luxury Accommodation at The Cavendish Hotel, Peak District',
        'field_type': 'LONG_HEADLINE',
        'intended_asset_group': '6456682937',
        'intended_property': 'The Cavendish Hotel'
    },
    '13877305644': {
        'text': 'Luxury Yorkshire Dales Hotel',
        'field_type': 'HEADLINE',
        'intended_asset_group': '6456682997',
        'intended_property': 'The Fell'
    },
    '314363561244': {
        'text': 'Yorkshire Dales Luxury Stay',
        'field_type': 'HEADLINE',
        'intended_asset_group': '6456682997',
        'intended_property': 'The Fell'
    },
    '314323984528': {
        'text': 'Luxury Yorkshire Dales hotel with spa & fine dining near Bolton Abbey Estate',
        'field_type': 'LONG_HEADLINE',
        'intended_asset_group': '6456682997',
        'intended_property': 'The Fell'
    },
    '314363562018': {
        'text': 'Luxury fell hotel in Yorkshire Dales with award-winning spa & gourmet dining',
        'field_type': 'LONG_HEADLINE',
        'intended_asset_group': '6456682997',
        'intended_property': 'The Fell'
    },
    '314363569227': {
        'text': 'Peak District Inn Getaways',
        'field_type': 'HEADLINE',
        'intended_asset_group': '6456676629',
        'intended_property': 'The Beeley Inn'
    },
    '314363572653': {
        'text': 'Traditional Peak District Inn with Cozy Rooms & Award-Winning Local Cuisine',
        'field_type': 'LONG_HEADLINE',
        'intended_asset_group': '6456676629',
        'intended_property': 'The Beeley Inn'
    },
    '314323998340': {
        'text': 'Traditional Peak District Inn with Cosy Rooms Near Chatsworth House',
        'field_type': 'LONG_HEADLINE',
        'intended_asset_group': '6456703957',
        'intended_property': 'The Pilsley Inn'
    },
    '314363576451': {
        'text': 'Peak District Inn & Restaurant',
        'field_type': 'HEADLINE',
        'intended_asset_group': '6456703957',
        'intended_property': 'The Pilsley Inn'
    },
    '314363580918': {
        'text': 'Cozy Peak District Inn Stay',
        'field_type': 'HEADLINE',
        'intended_asset_group': '6456703957',
        'intended_property': 'The Pilsley Inn'
    },
    '314323985695': {
        'text': 'Peak District Inn Getaway',
        'field_type': 'HEADLINE',
        'intended_asset_group': '6456703957',
        'intended_property': 'The Pilsley Inn'
    },
    '314245521437': {
        'text': 'Traditional Peak District inn with cozy rooms, hearty meals & countryside charm.',
        'field_type': 'DESCRIPTION',
        'intended_asset_group': '6456703957',
        'intended_property': 'The Pilsley Inn'
    }
}


def query_asset_group_assets(customer_id, manager_id, asset_group_id):
    """
    Query all text assets in a specific asset group.

    Returns list of dicts with asset_id, text, field_type, performance_label
    """
    query = f"""
        SELECT
            asset_group_asset.asset,
            asset_group_asset.asset_group,
            asset_group_asset.field_type,
            asset_group_asset.performance_label,
            asset.text_asset.text
        FROM asset_group_asset
        WHERE asset_group_asset.asset_group = 'customers/{customer_id}/assetGroups/{asset_group_id}'
            AND asset_group_asset.status = 'ENABLED'
        ORDER BY asset_group_asset.field_type
    """

    # This will use the MCP tool when run via Claude Code
    # When run standalone, this would need direct API implementation
    from mcp_tools import run_gaql

    result = run_gaql(customer_id=customer_id, manager_id=manager_id, query=query)

    assets = []
    for row in result:
        # Extract asset ID from resource name
        asset_resource = row.get('asset_group_asset.asset', '')
        asset_id = asset_resource.split('/')[-1]

        assets.append({
            'asset_id': asset_id,
            'asset_group_id': asset_group_id,
            'field_type': row.get('asset_group_asset.field_type', ''),
            'performance_label': row.get('asset_group_asset.performance_label', ''),
            'text': row.get('asset.text_asset.text', '')
        })

    return assets


def verify_asset_isolation():
    """
    Main verification function.
    Checks that newly added assets only appear in their intended asset groups.
    """
    print("=" * 80)
    print("DEVONSHIRE HOTELS - PMAX ASSET INTEGRITY VERIFICATION")
    print("=" * 80)
    print()

    # Step 1: Query all asset groups
    print("Step 1: Querying all asset groups...")
    print()

    all_assets_by_group = {}
    for asset_group_id, property_name in ASSET_GROUPS.items():
        print(f"  Querying: {property_name} (ID: {asset_group_id})...")
        assets = query_asset_group_assets(CUSTOMER_ID, MANAGER_ID, asset_group_id)
        all_assets_by_group[asset_group_id] = assets
        print(f"    ✓ Found {len(assets)} enabled assets")

    print()
    print("-" * 80)

    # Step 2: Build reverse index (asset_id -> list of asset groups)
    print("\nStep 2: Building asset-to-group index...")
    print()

    asset_to_groups = {}
    for asset_group_id, assets in all_assets_by_group.items():
        for asset in assets:
            asset_id = asset['asset_id']
            if asset_id not in asset_to_groups:
                asset_to_groups[asset_id] = []
            asset_to_groups[asset_id].append({
                'asset_group_id': asset_group_id,
                'property_name': ASSET_GROUPS[asset_group_id],
                'field_type': asset['field_type'],
                'text': asset['text']
            })

    print(f"  ✓ Indexed {len(asset_to_groups)} unique assets")
    print()
    print("-" * 80)

    # Step 3: Check newly added assets for cross-contamination
    print("\nStep 3: Checking newly added assets for cross-contamination...")
    print()

    issues_found = []
    assets_verified = 0

    for asset_id, asset_info in NEWLY_ADDED_ASSETS.items():
        intended_group = asset_info['intended_asset_group']
        intended_property = asset_info['intended_property']
        text = asset_info['text']
        field_type = asset_info['field_type']

        # Find where this asset appears
        if asset_id in asset_to_groups:
            appearances = asset_to_groups[asset_id]

            # Check if it appears ONLY in intended group
            if len(appearances) == 1 and appearances[0]['asset_group_id'] == intended_group:
                print(f"  ✅ CORRECT: Asset {asset_id}")
                print(f"     Text: \"{text}\"")
                print(f"     In: {intended_property} ONLY (as intended)")
                print()
                assets_verified += 1
            else:
                # Found in multiple groups or wrong group
                print(f"  ❌ ISSUE: Asset {asset_id}")
                print(f"     Text: \"{text}\"")
                print(f"     Field: {field_type}")
                print(f"     INTENDED: {intended_property}")
                print(f"     ACTUAL:")
                for appearance in appearances:
                    status = "✓ CORRECT" if appearance['asset_group_id'] == intended_group else "✗ UNINTENDED"
                    print(f"       {status}: {appearance['property_name']} ({appearance['field_type']})")
                print()

                issues_found.append({
                    'asset_id': asset_id,
                    'text': text,
                    'field_type': field_type,
                    'intended': intended_property,
                    'actual': [a['property_name'] for a in appearances]
                })
        else:
            print(f"  ⚠️  WARNING: Asset {asset_id} not found in any asset group")
            print(f"     Text: \"{text}\"")
            print(f"     Expected in: {intended_property}")
            print(f"     This asset may have been removed or is not ENABLED")
            print()

    print("-" * 80)

    # Step 4: Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"Total newly added assets checked: {len(NEWLY_ADDED_ASSETS)}")
    print(f"Assets correctly isolated: {assets_verified}")
    print(f"Cross-contamination issues found: {len(issues_found)}")
    print()

    if issues_found:
        print("🚨 ISSUES REQUIRING MANUAL REMOVAL:")
        print()
        for issue in issues_found:
            print(f"Asset ID: {issue['asset_id']}")
            print(f"Text: \"{issue['text']}\"")
            print(f"Field: {issue['field_type']}")
            print(f"Should be in: {issue['intended']}")
            print(f"Currently in: {', '.join(issue['actual'])}")
            print(f"Action: Remove from: {', '.join([p for p in issue['actual'] if p != issue['intended']])}")
            print()
    else:
        print("✅ All assets correctly isolated - no cross-contamination detected!")

    print("=" * 80)

    return len(issues_found) == 0


if __name__ == '__main__':
    try:
        # Note: This script requires MCP context to run
        # If run standalone, you'd need to implement direct API calls
        success = verify_asset_isolation()
        sys.exit(0 if success else 1)
    except ImportError:
        print("ERROR: This script must be run via Claude Code MCP context")
        print("It requires access to the google-ads MCP server tools")
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
