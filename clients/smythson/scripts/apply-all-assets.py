#!/usr/bin/env python3
"""
Apply ALL Smythson PMax assets from Google Spreadsheet to Google Ads.

Orchestration script that runs both text and image asset application in sequence.

This is the main entry point for applying complete asset updates to Smythson's
Performance Max campaigns.

Usage:
    python3 apply-all-assets.py --region uk --dry-run     # Test UK only
    python3 apply-all-assets.py --region all --dry-run    # Test all regions
    python3 apply-all-assets.py --region uk               # Apply UK live
    python3 apply-all-assets.py --region all              # Apply all regions live
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Script paths
SCRIPT_DIR = Path(__file__).parent
TEXT_ASSET_SCRIPT = SCRIPT_DIR / 'apply-text-assets-from-sheet.py'
IMAGE_ASSET_SCRIPT = SCRIPT_DIR / 'apply-image-assets-from-sheet.py'

REGIONS = ['uk', 'us', 'eur', 'row']


def run_script(script_path: Path, region: str, dry_run: bool = False) -> bool:
    """
    Run a script and return True if successful, False otherwise.
    """
    # Use the Google Ads MCP server venv Python
    python_path = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3'
    cmd = [python_path, str(script_path), '--region', region]
    if dry_run:
        cmd.append('--dry-run')

    print(f"\n{'='*80}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*80}\n")

    result = subprocess.run(cmd, cwd=SCRIPT_DIR)
    return result.returncode == 0


def apply_all_assets(region: str, dry_run: bool = False) -> dict:
    """
    Apply both text and image assets for a region.

    Returns:
        dict: Results with success/failure status for each step
    """
    results = {
        'region': region,
        'text_assets': False,
        'image_assets': False,
        'overall': False
    }

    print(f"\n{'#'*80}")
    print(f"# APPLYING ALL ASSETS: {region.upper()}")
    print(f"# Mode: {'DRY RUN' if dry_run else 'LIVE EXECUTION'}")
    print(f"# Started: {datetime.now().isoformat()}")
    print(f"{'#'*80}")

    # Step 1: Apply text assets
    print(f"\n{'='*80}")
    print(f"STEP 1: APPLYING TEXT ASSETS")
    print(f"{'='*80}")

    text_success = run_script(TEXT_ASSET_SCRIPT, region, dry_run)
    results['text_assets'] = text_success

    if not text_success:
        print(f"\n❌ Text asset application FAILED for {region.upper()}")
        print(f"⚠️  Skipping image asset application for safety")
        return results

    print(f"\n✅ Text asset application SUCCEEDED for {region.upper()}")

    # Step 2: Apply image assets
    print(f"\n{'='*80}")
    print(f"STEP 2: APPLYING IMAGE ASSETS")
    print(f"{'='*80}")

    image_success = run_script(IMAGE_ASSET_SCRIPT, region, dry_run)
    results['image_assets'] = image_success

    if not image_success:
        print(f"\n❌ Image asset application FAILED for {region.upper()}")
        return results

    print(f"\n✅ Image asset application SUCCEEDED for {region.upper()}")

    # Overall success
    results['overall'] = True
    print(f"\n{'#'*80}")
    print(f"# ✅ ALL ASSETS APPLIED SUCCESSFULLY: {region.upper()}")
    print(f"# Completed: {datetime.now().isoformat()}")
    print(f"{'#'*80}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Apply all Smythson PMax assets (text + images) from Google Spreadsheet to Google Ads'
    )
    parser.add_argument(
        '--region',
        required=True,
        choices=['uk', 'us', 'eur', 'row', 'all'],
        help='Region to process (or "all" for all regions)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test mode - show what would be applied without making changes'
    )
    args = parser.parse_args()

    # Validate scripts exist
    if not TEXT_ASSET_SCRIPT.exists():
        print(f"❌ ERROR: Text asset script not found: {TEXT_ASSET_SCRIPT}")
        sys.exit(1)

    if not IMAGE_ASSET_SCRIPT.exists():
        print(f"❌ ERROR: Image asset script not found: {IMAGE_ASSET_SCRIPT}")
        sys.exit(1)

    print(f"\n{'#'*80}")
    print(f"# SMYTHSON PMAX ASSET APPLICATION")
    print(f"# Orchestration Script")
    print(f"# Started: {datetime.now().isoformat()}")
    print(f"# Mode: {'DRY RUN' if args.dry_run else 'LIVE EXECUTION'}")
    print(f"{'#'*80}")

    if not args.dry_run:
        print(f"\n⚠️  WARNING: LIVE EXECUTION MODE")
        print(f"⚠️  This will modify Google Ads Performance Max campaigns")
        print(f"⚠️  Press Ctrl+C within 5 seconds to cancel...\n")
        import time
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print(f"\n\nCancelled by user")
            sys.exit(0)
        print(f"Proceeding with live execution...\n")

    # Determine regions to process
    regions_to_process = REGIONS if args.region == 'all' else [args.region]

    # Process each region
    all_results = []
    for region in regions_to_process:
        results = apply_all_assets(region, args.dry_run)
        all_results.append(results)

    # Print overall summary
    print(f"\n{'#'*80}")
    print(f"# OVERALL SUMMARY")
    print(f"{'#'*80}")

    successful_regions = []
    failed_regions = []

    for result in all_results:
        region = result['region']
        if result['overall']:
            successful_regions.append(region)
            status = '✅ SUCCESS'
        else:
            failed_regions.append(region)
            status = '❌ FAILED'

        print(f"\n{region.upper()}: {status}")
        print(f"  Text assets: {'✅' if result['text_assets'] else '❌'}")
        print(f"  Image assets: {'✅' if result['image_assets'] else '❌'}")

    print(f"\n{'='*80}")
    print(f"Regions processed: {len(all_results)}")
    print(f"Successful: {len(successful_regions)} {successful_regions}")
    print(f"Failed: {len(failed_regions)} {failed_regions}")
    print(f"Completed: {datetime.now().isoformat()}")
    print(f"{'='*80}")

    if args.dry_run:
        print(f"\n✅ DRY RUN COMPLETE - All checks passed")
        print(f"🚀 Ready for live execution on Tuesday")
        print(f"\n💡 To execute live: python3 apply-all-assets.py --region all")

    # Exit with appropriate code
    if failed_regions:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
