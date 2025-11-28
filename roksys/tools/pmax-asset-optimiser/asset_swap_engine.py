#!/usr/bin/env python3
"""
Asset Swap Engine - Core logic for safely swapping PMAX text assets

This module provides reusable functions for swapping text assets in Performance Max
campaigns while respecting Google Ads API minimum requirements.

Minimum Requirements (enforced by Google):
- Headlines: 3 minimum
- Long headlines: 1 minimum
- Descriptions: 2 minimum

Author: PetesBrain
Created: 2025-11-25
"""

import os
import sys
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Add MCP server path for Google Ads imports
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf import field_mask_pb2


# Google Ads minimum asset requirements
MINIMUM_REQUIREMENTS = {
    'HEADLINE': 3,
    'LONG_HEADLINE': 1,
    'DESCRIPTION': 2
}

# Google Ads configuration
GOOGLE_ADS_YAML = os.path.expanduser("~/google-ads.yaml")


class AssetSwapEngine:
    """Handles safe swapping of Performance Max text assets"""

    def __init__(self, customer_id: str, dry_run: bool = True):
        """
        Initialise the asset swap engine

        Args:
            customer_id: Google Ads customer ID (10 digits)
            dry_run: If True, simulates operations without executing
        """
        self.customer_id = customer_id
        self.dry_run = dry_run
        self.client = None
        self.log = []

    def initialise_client(self) -> bool:
        """
        Initialise Google Ads API client

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
            self._log_operation('INFO', f'Google Ads client initialised for {self.customer_id}')
            return True
        except Exception as e:
            self._log_operation('ERROR', f'Failed to initialise Google Ads client: {e}')
            return False

    def get_current_asset_counts(self, asset_group_id: str) -> Dict[str, int]:
        """
        Query Google Ads to count current assets by type in an asset group

        Args:
            asset_group_id: Asset group ID

        Returns:
            Dictionary with counts by field type: {'HEADLINE': 5, 'LONG_HEADLINE': 2, 'DESCRIPTION': 3}
        """
        if not self.client:
            raise RuntimeError("Client not initialised. Call initialise_client() first.")

        ga_service = self.client.get_service("GoogleAdsService")

        query = f"""
            SELECT
                asset_group_asset.field_type,
                asset.id,
                asset.text_asset.text
            FROM asset_group_asset
            WHERE asset_group.id = {asset_group_id}
              AND asset_group_asset.status = 'ENABLED'
              AND asset.type = 'TEXT'
        """

        try:
            response = ga_service.search(customer_id=self.customer_id, query=query)

            counts = {
                'HEADLINE': 0,
                'LONG_HEADLINE': 0,
                'DESCRIPTION': 0
            }

            for row in response:
                field_type = row.asset_group_asset.field_type.name
                if field_type in counts:
                    counts[field_type] += 1

            self._log_operation('INFO', f'Asset group {asset_group_id} counts: {counts}')
            return counts

        except GoogleAdsException as ex:
            self._log_operation('ERROR', f'Failed to get asset counts for {asset_group_id}: {ex}')
            raise

    def validate_swap_safety(
        self,
        asset_group_id: str,
        field_type: str,
        removal_count: int
    ) -> Tuple[bool, str]:
        """
        Check if we can safely remove N assets without violating minimums

        Args:
            asset_group_id: Asset group ID
            field_type: HEADLINE, LONG_HEADLINE, or DESCRIPTION
            removal_count: Number of assets to remove

        Returns:
            Tuple of (is_safe, message)
        """
        if field_type not in MINIMUM_REQUIREMENTS:
            return False, f"Invalid field type: {field_type}"

        current_counts = self.get_current_asset_counts(asset_group_id)
        current_count = current_counts.get(field_type, 0)
        minimum = MINIMUM_REQUIREMENTS[field_type]

        after_removal = current_count - removal_count

        if after_removal < minimum:
            return False, (
                f"Cannot remove {removal_count} {field_type} assets. "
                f"Current: {current_count}, Minimum: {minimum}, "
                f"After removal: {after_removal}"
            )

        return True, f"Safe to remove {removal_count} {field_type} assets"

    def find_asset_by_text(
        self,
        asset_group_id: str,
        asset_text: str,
        field_type: str
    ) -> Optional[str]:
        """
        Find an asset ID by its text content

        Args:
            asset_group_id: Asset group ID
            asset_text: Exact text to match
            field_type: HEADLINE, LONG_HEADLINE, or DESCRIPTION

        Returns:
            Asset ID if found, None otherwise
        """
        if not self.client:
            raise RuntimeError("Client not initialised")

        ga_service = self.client.get_service("GoogleAdsService")

        # Map field type to API enum value
        field_type_map = {
            'HEADLINE': 'HEADLINE',
            'LONG_HEADLINE': 'LONG_HEADLINE',
            'DESCRIPTION': 'DESCRIPTION'
        }

        if field_type not in field_type_map:
            self._log_operation('ERROR', f'Invalid field type: {field_type}')
            return None

        query = f"""
            SELECT
                asset.id,
                asset.text_asset.text,
                asset_group_asset.field_type
            FROM asset_group_asset
            WHERE asset_group.id = {asset_group_id}
              AND asset_group_asset.status = 'ENABLED'
              AND asset.type = 'TEXT'
              AND asset_group_asset.field_type = '{field_type_map[field_type]}'
        """

        try:
            response = ga_service.search(customer_id=self.customer_id, query=query)

            for row in response:
                if row.asset.text_asset.text == asset_text:
                    asset_id = str(row.asset.id)
                    self._log_operation('INFO', f'Found asset ID {asset_id} for text: "{asset_text[:50]}..."')
                    return asset_id

            self._log_operation('WARNING', f'Asset not found: "{asset_text[:50]}..."')
            return None

        except GoogleAdsException as ex:
            self._log_operation('ERROR', f'Failed to find asset: {ex}')
            return None

    def execute_swap(
        self,
        asset_group_id: str,
        old_asset_id: str,
        new_text: str,
        field_type: str
    ) -> bool:
        """
        Perform single asset swap with smart ordering based on current count

        Args:
            asset_group_id: Asset group ID
            old_asset_id: Asset ID to remove
            new_text: New text content
            field_type: HEADLINE, LONG_HEADLINE, or DESCRIPTION

        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            self._log_operation(
                'DRY-RUN',
                f'Would swap asset {old_asset_id} with "{new_text}" in group {asset_group_id}'
            )
            return True

        if not self.client:
            raise RuntimeError("Client not initialised")

        # Check if we're at maximum limit for this field type
        MAX_LIMITS = {
            'HEADLINE': 15,
            'LONG_HEADLINE': 5,
            'DESCRIPTION': 5
        }

        current_counts = self.get_current_asset_counts(asset_group_id)
        current_count = current_counts.get(field_type, 0)
        max_limit = MAX_LIMITS.get(field_type, 15)
        at_limit = current_count >= max_limit

        if at_limit:
            # At limit: REMOVE → CREATE → LINK
            # Step 1: Remove old asset first to make room
            if not self._remove_asset(asset_group_id, old_asset_id, field_type):
                self._log_operation('ERROR', 'Failed to remove old asset')
                return False

            # Step 2: Create new text asset
            new_asset_id = self._create_text_asset(new_text)
            if not new_asset_id:
                self._log_operation('ERROR', 'Failed to create new asset after removing old one')
                # Can't recover easily - old asset is gone
                return False

            # Step 3: Link new asset to asset group
            if not self._link_asset_to_group(asset_group_id, new_asset_id, field_type):
                self._log_operation('ERROR', 'Failed to link new asset after removal')
                # Old asset is removed, new asset couldn't be linked - this is bad
                return False
        else:
            # Below limit: CREATE → LINK → REMOVE
            # Step 1: Create new text asset FIRST (before removing old one)
            new_asset_id = self._create_text_asset(new_text)
            if not new_asset_id:
                self._log_operation('ERROR', 'Failed to create new asset')
                return False

            # Step 2: Link new asset to asset group
            if not self._link_asset_to_group(asset_group_id, new_asset_id, field_type):
                self._log_operation('ERROR', 'Failed to link new asset, cleanup needed')
                # TODO: Delete the created asset
                return False

            # Step 3: Remove old asset (now that new one is active)
            if not self._remove_asset(asset_group_id, old_asset_id, field_type):
                self._log_operation('WARNING', 'Failed to remove old asset, but new asset is active')
                # Don't fail - new asset is already working
                return True

        self._log_operation(
            'SUCCESS',
            f'Swapped asset {old_asset_id} → {new_asset_id} in group {asset_group_id}'
        )
        return True

    def _remove_asset(self, asset_group_id: str, asset_id: str, field_type: str) -> bool:
        """Remove an asset from an asset group using the remove operation"""
        try:
            ga_service = self.client.get_service("GoogleAdsService")

            # Find the asset_group_asset resource name
            query = f"""
                SELECT asset_group_asset.resource_name
                FROM asset_group_asset
                WHERE asset_group.id = {asset_group_id}
                  AND asset.id = {asset_id}
                  AND asset_group_asset.field_type = '{field_type}'
                  AND asset_group_asset.status IN ('ENABLED', 'PAUSED')
            """

            response = ga_service.search(customer_id=self.customer_id, query=query)
            resource_names = [row.asset_group_asset.resource_name for row in response]

            if not resource_names:
                self._log_operation('WARNING', f'Asset {asset_id} not found or already removed')
                return False

            # Remove the asset using the remove operation (not update)
            asset_group_asset_service = self.client.get_service("AssetGroupAssetService")

            for resource_name in resource_names:
                operation = self.client.get_type("AssetGroupAssetOperation")
                # Use the 'remove' field instead of 'update' to delete the asset link
                operation.remove = resource_name

                asset_group_asset_service.mutate_asset_group_assets(
                    customer_id=self.customer_id,
                    operations=[operation]
                )

                self._log_operation('INFO', f'Removed asset {asset_id} from group ({resource_name})')

            return True

        except GoogleAdsException as ex:
            self._log_operation('ERROR', f'Failed to remove asset {asset_id}: {ex}')
            return False

    def _create_text_asset(self, text: str) -> Optional[str]:
        """Create a new text asset"""
        try:
            asset_service = self.client.get_service("AssetService")
            asset_operation = self.client.get_type("AssetOperation")

            asset = asset_operation.create
            asset.text_asset.text = text
            asset.type_ = self.client.enums.AssetTypeEnum.TEXT

            response = asset_service.mutate_assets(
                customer_id=self.customer_id,
                operations=[asset_operation]
            )

            new_asset_resource_name = response.results[0].resource_name
            new_asset_id = new_asset_resource_name.split('/')[-1]

            self._log_operation('INFO', f'Created text asset: "{text}" (ID: {new_asset_id})')
            return new_asset_id

        except GoogleAdsException as ex:
            self._log_operation('ERROR', f'Failed to create text asset: {ex}')
            return None

    def _link_asset_to_group(
        self,
        asset_group_id: str,
        asset_id: str,
        field_type: str
    ) -> bool:
        """Link an asset to an asset group"""
        try:
            asset_group_asset_service = self.client.get_service("AssetGroupAssetService")
            operation = self.client.get_type("AssetGroupAssetOperation")

            asset_group_asset = operation.create
            asset_group_asset.asset = f"customers/{self.customer_id}/assets/{asset_id}"
            asset_group_asset.asset_group = f"customers/{self.customer_id}/assetGroups/{asset_group_id}"

            # Set field type
            field_type_enum = getattr(self.client.enums.AssetFieldTypeEnum, field_type)
            asset_group_asset.field_type = field_type_enum

            asset_group_asset_service.mutate_asset_group_assets(
                customer_id=self.customer_id,
                operations=[operation]
            )

            self._log_operation('INFO', f'Linked asset {asset_id} to group {asset_group_id}')
            return True

        except GoogleAdsException as ex:
            self._log_operation('ERROR', f'Failed to link asset to group: {ex}')
            return False

    def batch_swap_assets(
        self,
        asset_group_id: str,
        swap_list: List[Dict],
        validate_first: bool = True
    ) -> Dict:
        """
        Process multiple asset swaps while maintaining minimums

        Args:
            asset_group_id: Asset group ID
            swap_list: List of dicts with keys: old_asset_id, new_text, field_type
            validate_first: If True, validates safety before executing

        Returns:
            Dictionary with results: {successful: int, failed: int, details: [...]}
        """
        results = {
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'details': []
        }

        # Validate safety if requested
        if validate_first:
            # Count removals by field type
            removal_counts = {'HEADLINE': 0, 'LONG_HEADLINE': 0, 'DESCRIPTION': 0}
            for swap in swap_list:
                field_type = swap.get('field_type')
                if field_type in removal_counts:
                    removal_counts[field_type] += 1

            # Check each field type
            for field_type, count in removal_counts.items():
                if count > 0:
                    is_safe, message = self.validate_swap_safety(asset_group_id, field_type, count)
                    if not is_safe:
                        self._log_operation('ERROR', f'Batch swap validation failed: {message}')
                        results['details'].append({
                            'status': 'VALIDATION_FAILED',
                            'message': message
                        })
                        return results

        # Execute swaps
        for swap in swap_list:
            old_asset_id = swap.get('old_asset_id')
            new_text = swap.get('new_text')
            field_type = swap.get('field_type')

            if not all([old_asset_id, new_text, field_type]):
                self._log_operation('WARNING', f'Skipping invalid swap: {swap}')
                results['skipped'] += 1
                continue

            success = self.execute_swap(asset_group_id, old_asset_id, new_text, field_type)

            if success:
                results['successful'] += 1
            else:
                results['failed'] += 1

            results['details'].append({
                'old_asset_id': old_asset_id,
                'new_text': new_text[:50],
                'field_type': field_type,
                'status': 'SUCCESS' if success else 'FAILED'
            })

        return results

    def _log_operation(self, level: str, message: str):
        """Log an operation with timestamp"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        self.log.append(entry)

        # Also print to console
        prefix = {
            'INFO': 'ℹ️ ',
            'SUCCESS': '✅',
            'WARNING': '⚠️ ',
            'ERROR': '❌',
            'DRY-RUN': '🔍'
        }.get(level, '')

        print(f"{prefix} [{level}] {message}")

    def get_log(self) -> List[Dict]:
        """Get operation log"""
        return self.log

    def save_log(self, filepath: str):
        """Save operation log to file"""
        with open(filepath, 'w') as f:
            json.dump(self.log, f, indent=2)
        self._log_operation('INFO', f'Log saved to {filepath}')


# Convenience functions for quick usage

def quick_swap(
    customer_id: str,
    asset_group_id: str,
    old_asset_text: str,
    new_text: str,
    field_type: str,
    dry_run: bool = True
) -> bool:
    """
    Quick single asset swap by text matching

    Args:
        customer_id: Google Ads customer ID
        asset_group_id: Asset group ID
        old_asset_text: Current asset text to find and replace
        new_text: New text
        field_type: HEADLINE, LONG_HEADLINE, or DESCRIPTION
        dry_run: If True, simulates operation

    Returns:
        True if successful
    """
    engine = AssetSwapEngine(customer_id, dry_run=dry_run)

    if not engine.initialise_client():
        return False

    # Find asset by text
    old_asset_id = engine.find_asset_by_text(asset_group_id, old_asset_text, field_type)
    if not old_asset_id:
        print(f"❌ Could not find asset with text: {old_asset_text}")
        return False

    # Execute swap
    return engine.execute_swap(asset_group_id, old_asset_id, new_text, field_type)


if __name__ == "__main__":
    # Example usage
    print("Asset Swap Engine - Test Mode")
    print("=" * 60)

    # Test with Tree2mydoor
    customer_id = "4941701449"
    asset_group_id = "6443046142"  # Example asset group

    engine = AssetSwapEngine(customer_id, dry_run=True)

    if engine.initialise_client():
        print("\n✅ Client initialised successfully")

        # Test: Get current counts
        print("\n📊 Getting current asset counts...")
        counts = engine.get_current_asset_counts(asset_group_id)
        print(f"Current counts: {counts}")

        # Test: Validate safety
        print("\n🔒 Testing safety validation...")
        is_safe, message = engine.validate_swap_safety(asset_group_id, 'HEADLINE', 1)
        print(f"Safety check: {message}")
    else:
        print("\n❌ Failed to initialise client")
