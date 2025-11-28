#!/usr/bin/env python3
"""
Execute Asset Optimisation - Process reviewed CSV and swap underperforming assets

This script processes the reviewed replacement-candidates.csv file and executes
asset swaps for rows marked with Action=SWAP.

Usage:
    python3 execute_asset_optimisation.py [--dry-run] [--csv path/to/reviewed.csv]

Author: PetesBrain
Created: 2025-11-25
"""

import sys
import csv
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# Import the asset swap engine
from asset_swap_engine import AssetSwapEngine

# Configuration
DEFAULT_CSV_PATH = "output/replacement-candidates.csv"
OUTPUT_DIR = Path("output")
LOGS_DIR = Path("logs")
BACKUPS_DIR = Path("backups")

# Asset type mapping from CSV to API field types
ASSET_TYPE_MAP = {
    'Headline': 'HEADLINE',
    'Long headline': 'LONG_HEADLINE',
    'Description': 'DESCRIPTION'
}


class AssetOptimisationExecutor:
    """Orchestrates asset swap execution from reviewed CSV"""

    def __init__(self, customer_id: str, csv_path: str, dry_run: bool = True):
        """
        Initialise executor

        Args:
            customer_id: Google Ads customer ID
            csv_path: Path to reviewed CSV file
            dry_run: If True, simulates operations without executing
        """
        self.customer_id = customer_id
        self.csv_path = Path(csv_path)
        self.dry_run = dry_run
        self.engine = AssetSwapEngine(customer_id, dry_run)
        self.results = {
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }

    def load_reviewed_csv(self) -> List[Dict]:
        """
        Load and parse reviewed CSV file

        Returns:
            List of dictionaries containing asset swap instructions
        """
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        swap_instructions = []

        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Only process rows marked as SWAP
                if row.get('Action', '').upper() == 'SWAP':
                    swap_instructions.append({
                        'campaign_id': row['Campaign_ID'],
                        'asset_group_id': row['Asset_Group_ID'],
                        'asset_group': row['Asset_Group'],
                        'original_text': row['Original_Text'],
                        'asset_type': row['Asset_Type'],
                        'replacement_text': row['Replacement_Text'],
                        # Optional columns (for logging/reporting only)
                        'option_number': row.get('Option_Number', ''),
                        'impressions': row.get('Impressions', '0'),
                        'ctr': row.get('CTR', '0'),
                        'conv_rate': row.get('Conv_Rate', '0'),
                        'priority': row.get('Priority', 'MEDIUM')
                    })

        print(f"✅ Loaded {len(swap_instructions)} asset swap instructions from CSV")
        return swap_instructions

    def find_asset_group_id_for_asset(
        self,
        campaign_id: str,
        asset_text: str,
        field_type: str
    ) -> Optional[str]:
        """
        Find the asset group ID containing a specific asset

        Args:
            campaign_id: Campaign ID to search within
            asset_text: Text content of the asset
            field_type: HEADLINE, LONG_HEADLINE, or DESCRIPTION

        Returns:
            Asset group ID if found, None otherwise
        """
        if not self.engine.client:
            raise RuntimeError("Engine client not initialised")

        ga_service = self.engine.client.get_service("GoogleAdsService")

        # Query all asset groups in the campaign
        query = f"""
            SELECT
                asset_group.id,
                asset.id,
                asset.text_asset.text,
                asset_group_asset.field_type
            FROM asset_group_asset
            WHERE campaign.id = {campaign_id}
              AND asset_group_asset.status = 'ENABLED'
              AND asset.type = 'TEXT'
              AND asset_group_asset.field_type = '{field_type}'
        """

        try:
            response = ga_service.search(customer_id=self.customer_id, query=query)

            for row in response:
                if row.asset.text_asset.text == asset_text:
                    asset_group_id = str(row.asset_group.id)
                    print(f"   ✅ Found asset in group {asset_group_id}")
                    return asset_group_id

            print(f"   ⚠️  Asset not found in campaign {campaign_id}")
            return None

        except Exception as ex:
            print(f"   ❌ Error finding asset group: {ex}")
            return None

    def execute_single_swap(
        self,
        campaign_id: str,
        instruction: Dict
    ) -> bool:
        """
        Execute a single asset swap

        Args:
            campaign_id: Campaign ID containing the asset (not used, kept for compatibility)
            instruction: Swap instruction dictionary

        Returns:
            True if successful, False otherwise
        """
        original_text = instruction['original_text']
        replacement_text = instruction['replacement_text']
        asset_type = instruction['asset_type']
        asset_group_id = instruction['asset_group_id']
        asset_group_name = instruction.get('asset_group', 'Unknown')
        field_type = ASSET_TYPE_MAP.get(asset_type)

        if not field_type:
            print(f"   ❌ Invalid asset type: {asset_type}")
            self.results['errors'].append(f"Invalid asset type: {asset_type}")
            return False

        print(f"\n🔄 Processing swap:")
        print(f"   Asset Group: {asset_group_name} ({asset_group_id})")
        print(f"   Original: {original_text[:70]}...")
        print(f"   Replacement: {replacement_text}")
        print(f"   Type: {asset_type}")

        # Step 1: Find old asset ID (using asset_group_id from CSV)
        print(f"   🔍 Finding old asset ID in group {asset_group_id}...")
        old_asset_id = self.engine.find_asset_by_text(
            asset_group_id,
            original_text,
            field_type
        )

        if not old_asset_id:
            print(f"   ❌ Could not find old asset ID in group {asset_group_id}")
            self.results['errors'].append(f"Asset ID not found: {original_text[:50]}")
            return False

        # Step 2: Validate safety
        print(f"   🛡️  Validating safety...")
        is_safe, message = self.engine.validate_swap_safety(
            asset_group_id,
            field_type,
            removal_count=1
        )

        if not is_safe:
            print(f"   ❌ Safety check failed: {message}")
            self.results['errors'].append(f"Safety check failed: {message}")
            return False

        print(f"   ✅ Safety check passed")

        # Step 3: Execute swap
        print(f"   🔄 Executing swap...")
        success = self.engine.execute_swap(
            asset_group_id,
            old_asset_id,
            replacement_text,
            field_type
        )

        if success:
            mode = "DRY-RUN" if self.dry_run else "EXECUTED"
            print(f"   ✅ Swap {mode} successfully!")
            return True
        else:
            print(f"   ❌ Swap failed")
            self.results['errors'].append(f"Swap execution failed: {original_text[:50]}")
            return False

    def group_swaps_by_asset_group(
        self,
        campaign_id: str,
        instructions: List[Dict]
    ) -> Dict[Tuple[str, str], List[Dict]]:
        """
        Group swap instructions by asset group and field type

        Args:
            campaign_id: Campaign ID (not used anymore, kept for compatibility)
            instructions: List of swap instructions

        Returns:
            Dictionary mapping (asset_group_id, field_type) -> list of instructions
        """
        grouped = defaultdict(list)

        for instruction in instructions:
            asset_type = instruction['asset_type']
            field_type = ASSET_TYPE_MAP.get(asset_type)

            if not field_type:
                print(f"   ⚠️  Skipping invalid asset type: {asset_type}")
                continue

            # Use asset_group_id directly from CSV (no more searching!)
            asset_group_id = instruction['asset_group_id']
            asset_group_name = instruction.get('asset_group', 'Unknown')

            print(f"   ✅ Using asset group {asset_group_id} ({asset_group_name}) from CSV")

            key = (asset_group_id, field_type)
            grouped[key].append(instruction)

        return grouped

    def execute_batch_swap(
        self,
        asset_group_id: str,
        field_type: str,
        instructions: List[Dict]
    ) -> Tuple[int, int]:
        """
        Execute a batch of swaps in the same asset group

        Args:
            asset_group_id: Asset group ID
            field_type: HEADLINE, LONG_HEADLINE, or DESCRIPTION
            instructions: List of swap instructions for this group

        Returns:
            Tuple of (successful_count, failed_count)
        """
        batch_size = len(instructions)
        print(f"\n{'='*80}")
        print(f"📦 BATCH SWAP: {batch_size} {field_type}s in asset group {asset_group_id}")
        print(f"{'='*80}")

        # Step 1: Validate batch safety
        print(f"   🛡️  Validating batch safety...")
        current_counts = self.engine.get_current_asset_counts(asset_group_id)
        current_count = current_counts.get(field_type, 0)

        # Import minimum requirements
        from asset_swap_engine import MINIMUM_REQUIREMENTS
        minimum = MINIMUM_REQUIREMENTS.get(field_type, 0)

        # Check if we can safely remove this many assets
        # We'll add new ones first, so check: current + batch - batch >= minimum
        # Which simplifies to: current >= minimum (always true if assets exist)
        # But we need to ensure we have enough to remove
        if current_count - batch_size < minimum:
            print(f"   ⚠️  Batch too large! Would violate minimums.")
            print(f"   Current: {current_count}, Batch: {batch_size}, Minimum: {minimum}")
            print(f"   Falling back to one-by-one execution...")
            return self._execute_batch_one_by_one(asset_group_id, field_type, instructions)

        print(f"   ✅ Batch is safe (current: {current_count}, removing: {batch_size}, minimum: {minimum})")

        # Check Google Ads limits (15 max for headlines, 5 for long headlines, 5 for descriptions)
        MAX_LIMITS = {
            'HEADLINE': 15,
            'LONG_HEADLINE': 5,
            'DESCRIPTION': 5
        }
        max_limit = MAX_LIMITS.get(field_type, 15)

        # If we're at or near the limit, we need to remove first, then add
        at_limit = current_count >= max_limit
        if at_limit:
            print(f"   ⚠️  At maximum limit ({current_count}/{max_limit})")
            print(f"   🔄 Will REMOVE old assets first, then CREATE and LINK new ones")
            return self._execute_batch_remove_first(asset_group_id, field_type, instructions)

        # Otherwise, safer to add first then remove (avoids violating minimums)
        print(f"   📝 Below limit ({current_count}/{max_limit}), will CREATE→LINK→REMOVE")

        # Step 2: Create all new assets
        print(f"\n   📝 Creating {batch_size} new assets...")
        new_asset_ids = []
        for idx, instruction in enumerate(instructions, 1):
            replacement_text = instruction['replacement_text']
            print(f"   [{idx}/{batch_size}] Creating: {replacement_text[:50]}...")

            new_asset_id = self.engine._create_text_asset(replacement_text)
            if new_asset_id:
                new_asset_ids.append((instruction, new_asset_id))
            else:
                print(f"      ❌ Failed to create asset")
                self.results['errors'].append(f"Failed to create: {replacement_text[:50]}")

        if len(new_asset_ids) != batch_size:
            print(f"   ⚠️  Only created {len(new_asset_ids)}/{batch_size} assets")
            print(f"   Falling back to one-by-one for safety...")
            return self._execute_batch_one_by_one(asset_group_id, field_type, instructions)

        # Step 3: Link all new assets to asset group
        print(f"\n   🔗 Linking {batch_size} new assets to asset group...")
        linked_assets = []
        for idx, (instruction, new_asset_id) in enumerate(new_asset_ids, 1):
            replacement_text = instruction['replacement_text']
            print(f"   [{idx}/{batch_size}] Linking: {replacement_text[:50]}...")

            if self.engine._link_asset_to_group(asset_group_id, new_asset_id, field_type):
                linked_assets.append((instruction, new_asset_id))
            else:
                print(f"      ❌ Failed to link asset {new_asset_id}")
                self.results['errors'].append(f"Failed to link: {replacement_text[:50]}")

        # Step 4: Find and remove all old assets
        print(f"\n   🗑️  Removing {batch_size} old assets...")
        successful = 0
        failed = 0

        for idx, (instruction, new_asset_id) in enumerate(linked_assets, 1):
            original_text = instruction['original_text']
            print(f"   [{idx}/{len(linked_assets)}] Removing: {original_text[:50]}...")

            old_asset_id = self.engine.find_asset_by_text(
                asset_group_id,
                original_text,
                field_type
            )

            if old_asset_id:
                if self.engine._remove_asset(asset_group_id, old_asset_id, field_type):
                    print(f"      ✅ Removed asset {old_asset_id}")
                    successful += 1
                else:
                    print(f"      ⚠️  Failed to remove asset {old_asset_id} (but new asset is live)")
                    successful += 1  # Still count as success since new asset is active
            else:
                print(f"      ⚠️  Old asset not found (but new asset is live)")
                successful += 1  # Still count as success

        mode = "DRY-RUN" if self.dry_run else "EXECUTED"
        print(f"\n   ✅ Batch {mode}: {successful} successful, {failed} failed")
        return successful, failed

    def _execute_batch_remove_first(
        self,
        asset_group_id: str,
        field_type: str,
        instructions: List[Dict]
    ) -> Tuple[int, int]:
        """
        Execute batch swap when at maximum limit: REMOVE→CREATE→LINK

        This is necessary when the asset group is at Google's maximum limit
        and we can't add more assets before removing old ones.
        """
        batch_size = len(instructions)
        print(f"\n   🗑️  Step 1: Removing {batch_size} old assets first...")

        removed_assets = []
        for idx, instruction in enumerate(instructions, 1):
            original_text = instruction['original_text']
            print(f"   [{idx}/{batch_size}] Removing: {original_text[:50]}...")

            old_asset_id = self.engine.find_asset_by_text(
                asset_group_id,
                original_text,
                field_type
            )

            if old_asset_id:
                if self.engine._remove_asset(asset_group_id, old_asset_id, field_type):
                    print(f"      ✅ Removed asset {old_asset_id}")
                    removed_assets.append((instruction, old_asset_id))
                else:
                    print(f"      ❌ Failed to remove asset {old_asset_id}")
                    self.results['errors'].append(f"Failed to remove: {original_text[:50]}")
            else:
                print(f"      ⚠️  Old asset not found")
                self.results['errors'].append(f"Asset not found: {original_text[:50]}")

        if not removed_assets:
            print(f"   ❌ Failed to remove any assets, aborting batch")
            return 0, batch_size

        # Step 2: Create new assets
        print(f"\n   📝 Step 2: Creating {len(removed_assets)} new assets...")
        created_assets = []
        for idx, (instruction, old_asset_id) in enumerate(removed_assets, 1):
            replacement_text = instruction['replacement_text']
            print(f"   [{idx}/{len(removed_assets)}] Creating: {replacement_text[:50]}...")

            new_asset_id = self.engine._create_text_asset(replacement_text)
            if new_asset_id:
                created_assets.append((instruction, old_asset_id, new_asset_id))
                print(f"      ✅ Created asset {new_asset_id}")
            else:
                print(f"      ❌ Failed to create asset")
                self.results['errors'].append(f"Failed to create: {replacement_text[:50]}")

        # Step 3: Link new assets
        print(f"\n   🔗 Step 3: Linking {len(created_assets)} new assets...")
        successful = 0
        failed = 0

        for idx, (instruction, old_asset_id, new_asset_id) in enumerate(created_assets, 1):
            replacement_text = instruction['replacement_text']
            print(f"   [{idx}/{len(created_assets)}] Linking: {replacement_text[:50]}...")

            if self.engine._link_asset_to_group(asset_group_id, new_asset_id, field_type):
                print(f"      ✅ Linked asset {new_asset_id}")
                successful += 1
            else:
                print(f"      ❌ Failed to link asset {new_asset_id}")
                self.results['errors'].append(f"Failed to link: {replacement_text[:50]}")
                failed += 1

        mode = "DRY-RUN" if self.dry_run else "EXECUTED"
        print(f"\n   ✅ Batch {mode} (REMOVE-FIRST): {successful} successful, {failed} failed")
        return successful, failed

    def _execute_batch_one_by_one(
        self,
        asset_group_id: str,
        field_type: str,
        instructions: List[Dict]
    ) -> Tuple[int, int]:
        """Fallback: Execute swaps one-by-one if batch is unsafe"""
        successful = 0
        failed = 0

        for idx, instruction in enumerate(instructions, 1):
            print(f"\n   [{idx}/{len(instructions)}] One-by-one swap...")
            original_text = instruction['original_text']
            replacement_text = instruction['replacement_text']

            old_asset_id = self.engine.find_asset_by_text(
                asset_group_id,
                original_text,
                field_type
            )

            if not old_asset_id:
                print(f"      ❌ Old asset not found")
                failed += 1
                continue

            success = self.engine.execute_swap(
                asset_group_id,
                old_asset_id,
                replacement_text,
                field_type
            )

            if success:
                successful += 1
            else:
                failed += 1

        return successful, failed

    def execute_all_swaps(self, campaign_id: str) -> Dict:
        """
        Execute all swaps from the reviewed CSV

        Args:
            campaign_id: Campaign ID to execute swaps in

        Returns:
            Dictionary with execution results
        """
        print("="*80)
        print("PMAX ASSET OPTIMISATION EXECUTION")
        print("="*80)
        mode = "DRY-RUN MODE" if self.dry_run else "LIVE EXECUTION"
        print(f"Mode: {mode}")
        print(f"Customer ID: {self.customer_id}")
        print(f"Campaign ID: {campaign_id}")
        print(f"CSV: {self.csv_path}")
        print("="*80)

        # Initialise engine
        if not self.engine.initialise_client():
            raise RuntimeError("Failed to initialise Google Ads client")

        # Load swap instructions
        instructions = self.load_reviewed_csv()

        if not instructions:
            print("\n⚠️  No assets marked for swapping (Action=SWAP)")
            return self.results

        print(f"\n📋 Processing {len(instructions)} asset swaps...")
        print(f"🔄 Grouping swaps by asset group for batch processing...")

        # Group swaps by asset group and field type
        grouped_swaps = self.group_swaps_by_asset_group(campaign_id, instructions)

        if not grouped_swaps:
            print("\n❌ No valid swaps found after grouping")
            return self.results

        print(f"\n✅ Grouped into {len(grouped_swaps)} batches")

        # Execute each batch
        batch_num = 0
        for (asset_group_id, field_type), batch_instructions in grouped_swaps.items():
            batch_num += 1
            batch_size = len(batch_instructions)

            print(f"\n{'='*80}")
            print(f"BATCH {batch_num}/{len(grouped_swaps)}: {batch_size} swap(s)")
            print(f"Asset Group: {asset_group_id}, Type: {field_type}")
            print(f"{'='*80}")

            self.results['processed'] += batch_size

            # Execute batch swap
            successful, failed = self.execute_batch_swap(
                asset_group_id,
                field_type,
                batch_instructions
            )

            self.results['successful'] += successful
            self.results['failed'] += failed

        # Generate summary
        print("\n" + "="*80)
        print("EXECUTION SUMMARY")
        print("="*80)
        print(f"Total processed: {self.results['processed']}")
        print(f"Successful: {self.results['successful']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Skipped: {self.results['skipped']}")

        if self.results['errors']:
            print(f"\n❌ Errors encountered:")
            for error in self.results['errors']:
                print(f"   - {error}")

        # Save execution report
        self.save_execution_report()

        return self.results

    def save_execution_report(self):
        """Save execution report to JSON file"""
        LOGS_DIR.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        mode = "dry-run" if self.dry_run else "live"
        report_path = LOGS_DIR / f"execution-report-{mode}-{timestamp}.json"

        report = {
            'timestamp': timestamp,
            'mode': 'dry-run' if self.dry_run else 'live',
            'customer_id': self.customer_id,
            'csv_path': str(self.csv_path),
            'results': self.results,
            'engine_log': self.engine.log
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Execution report saved: {report_path}")


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Execute PMAX asset optimisation from reviewed CSV"
    )
    parser.add_argument(
        '--csv',
        default=DEFAULT_CSV_PATH,
        help=f'Path to reviewed CSV file (default: {DEFAULT_CSV_PATH})'
    )
    parser.add_argument(
        '--customer-id',
        required=True,
        help='Google Ads customer ID (10 digits)'
    )
    parser.add_argument(
        '--campaign-id',
        required=True,
        help='Campaign ID to execute swaps in'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=True,
        help='Run in dry-run mode (default: True)'
    )
    parser.add_argument(
        '--live',
        action='store_true',
        help='Execute live swaps (overrides --dry-run)'
    )

    args = parser.parse_args()

    # Determine dry-run mode
    dry_run = not args.live

    # Create executor
    executor = AssetOptimisationExecutor(
        customer_id=args.customer_id,
        csv_path=args.csv,
        dry_run=dry_run
    )

    # Execute swaps
    try:
        results = executor.execute_all_swaps(args.campaign_id)

        # Exit with appropriate code
        if results['failed'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
