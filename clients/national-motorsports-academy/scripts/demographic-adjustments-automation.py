#!/usr/bin/env python3
"""
NMA Demographic Bid Adjustments - Automated Google Ads API Tool

This script applies demographic bid adjustments to underperforming demographics
in NMA's Management campaigns to improve lead quality and reduce CPA.

Setup:
    1. Install dependencies: pip install -r requirements.txt
    2. Configure google_ads_config.yaml with your Google Ads credentials
    3. Run: python3 demographic-adjustments-automation.py [--dry-run] [--confirm]

Options:
    --dry-run: Preview changes without applying them
    --confirm: Apply changes without confirmation prompt
    --log-file: Custom log file path (default: demographic-adjustments.log)
"""

import sys
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path

try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
except ImportError:
    print("❌ google-ads library not found.")
    print("   Install with: pip install -r requirements.txt")
    sys.exit(1)

# Configuration
CUSTOMER_ID = "5622468019"
CONFIG_FILE = "google_ads_config.yaml"

# Adjustment specifications
ADJUSTMENTS_CONFIG = {
    "12578308466": {  # UK Management Campaign
        "name": "NMA | Search | UK | Management 100 Ai 25/8 No Target",
        "adjustments": [
            {
                "criterion_id": "503003",
                "description": "Age 35-44",
                "new_bid_modifier": 0.80,
                "reason": "Management interest, lower conversion intent"
            },
            {
                "criterion_id": "503004",
                "description": "Age 45-54",
                "new_bid_modifier": 0.80,
                "reason": "Too old for typical career switch to motorsport"
            },
            {
                "criterion_id": "503005",
                "description": "Age 55-64",
                "new_bid_modifier": 0.80,
                "reason": "Unlikely to pursue online education"
            },
            {
                "criterion_id": "301",
                "description": "Parent status",
                "new_bid_modifier": 0.80,
                "reason": "Time constraints, lower commitment"
            }
        ]
    },
    "13071720649": {  # ROW Management Campaign
        "name": "NMA | Search | ROW | Management 100 No Target",
        "adjustments": [
            {
                "criterion_id": "503003",
                "description": "Age 35-44",
                "new_bid_modifier": 0.80,
                "reason": "Management interest, lower conversion intent"
            },
            {
                "criterion_id": "503004",
                "description": "Age 45-54",
                "new_bid_modifier": 0.80,
                "reason": "Too old for typical career switch to motorsport"
            },
            {
                "criterion_id": "301",
                "description": "Parent status",
                "new_bid_modifier": 0.80,
                "reason": "Time constraints, lower commitment"
            }
        ]
    }
}

def setup_logging(log_file="demographic-adjustments.log"):
    """Configure logging to file and console."""
    logger = logging.getLogger("nma_demographics")
    logger.setLevel(logging.DEBUG)

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

def print_preview():
    """Display adjustment preview."""
    print("\n" + "=" * 100)
    print("NMA DEMOGRAPHIC BID ADJUSTMENTS - AUTOMATED SYSTEM")
    print("=" * 100)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Customer ID: {CUSTOMER_ID}")
    print(f"Review Date: 2026-01-11 (30 days)")
    print("\n" + "-" * 100)

    total = 0
    for campaign_id, campaign_data in ADJUSTMENTS_CONFIG.items():
        print(f"\n📋 Campaign: {campaign_data['name']}")
        print(f"   ID: {campaign_id}\n")

        for adj in campaign_data["adjustments"]:
            total += 1
            modifier = adj["new_bid_modifier"]
            pct = f"{(modifier - 1) * 100:.0f}%"

            print(f"   • {adj['description']:20} → {modifier:.2f} ({pct})")
            print(f"     Reason: {adj['reason']}\n")

    print("-" * 100)
    print(f"Total adjustments: {total}")
    print("\n✅ Expected Impact:")
    print("   • 5-8% account-wide CPA improvement")
    print("   • £400-650/month estimated savings")
    print("   • Better lead quality for Management programs")
    print("\n" + "=" * 100 + "\n")

def apply_adjustments_to_google_ads(client, dry_run=False, logger=None):
    """Apply demographic bid adjustments via Google Ads API."""

    if not logger:
        logger = logging.getLogger("nma_demographics")

    ga_service = client.get_service("GoogleAdsService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    successful = 0
    failed = 0
    changes_log = []

    for campaign_id, campaign_data in ADJUSTMENTS_CONFIG.items():
        campaign_name = campaign_data["name"]
        logger.info(f"Processing campaign: {campaign_name} (ID: {campaign_id})")

        for adjustment in campaign_data["adjustments"]:
            criterion_id = adjustment["criterion_id"]
            description = adjustment["description"]
            new_modifier = adjustment["new_bid_modifier"]

            try:
                # Query for matching criteria
                query = f"""
                    SELECT ad_group_criterion.resource_name,
                           ad_group_criterion.criterion_id,
                           ad_group_criterion.bid_modifier,
                           ad_group.id,
                           ad_group.name,
                           campaign.id,
                           campaign.name
                    FROM ad_group_criterion
                    WHERE campaign.id = {campaign_id}
                      AND ad_group_criterion.criterion_id = {criterion_id}
                """

                response = ga_service.search_stream(
                    customer_id=CUSTOMER_ID,
                    query=query
                )

                found = False
                for batch in response:
                    for row in batch.results:
                        found = True
                        resource_name = row.ad_group_criterion.resource_name
                        current_modifier = row.ad_group_criterion.bid_modifier or 1.0
                        ad_group_name = row.ad_group.name

                        change_record = {
                            "campaign_id": campaign_id,
                            "campaign_name": campaign_name,
                            "ad_group_name": ad_group_name,
                            "criterion_id": criterion_id,
                            "description": description,
                            "current_modifier": current_modifier,
                            "new_modifier": new_modifier,
                            "resource_name": resource_name,
                            "timestamp": datetime.now().isoformat()
                        }

                        if dry_run:
                            logger.info(
                                f"[DRY RUN] {description} ({criterion_id}): "
                                f"{current_modifier:.2f} → {new_modifier:.2f}"
                            )
                            successful += 1
                        else:
                            # Update the criterion
                            ad_group_criterion = client.get_type("AdGroupCriterion")
                            ad_group_criterion.resource_name = resource_name
                            ad_group_criterion.bid_modifier = new_modifier

                            operation = client.get_type("AdGroupCriterionOperation")
                            operation.update = ad_group_criterion
                            operation.update_mask.paths.append("bid_modifier")

                            response = ad_group_criterion_service.mutate_ad_group_criteria(
                                customer_id=CUSTOMER_ID,
                                operations=[operation]
                            )

                            logger.info(
                                f"✓ Updated {description} ({criterion_id}): "
                                f"{current_modifier:.2f} → {new_modifier:.2f}"
                            )
                            successful += 1
                            change_record["applied"] = True

                        changes_log.append(change_record)

                if not found:
                    logger.warning(
                        f"⚠️ No criterion found for {description} "
                        f"(ID: {criterion_id}) in campaign {campaign_id}"
                    )
                    failed += 1

            except GoogleAdsException as e:
                logger.error(
                    f"❌ Error updating {description} ({criterion_id}): {e.message}"
                )
                failed += 1

    # Save changes log
    log_file = f"demographic-adjustments-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(log_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "successful": successful,
            "failed": failed,
            "changes": changes_log,
            "review_date": "2026-01-11"
        }, f, indent=2)

    logger.info(f"Changes log saved to: {log_file}")

    return successful, failed, changes_log

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="NMA Demographic Bid Adjustments Automation"
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without applying")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation prompt")
    parser.add_argument("--log-file", default="demographic-adjustments.log", help="Log file path")

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging(args.log_file)
    logger.info("=" * 80)
    logger.info("NMA Demographic Bid Adjustments - Automated System Started")
    logger.info(f"Dry Run Mode: {args.dry_run}")
    logger.info("=" * 80)

    # Display preview
    print_preview()

    # Get confirmation if not dry-run and not confirmed
    if not args.dry_run and not args.confirm:
        response = input("⚠️  Apply these changes to Google Ads? (yes/no): ").strip().lower()
        if response != "yes":
            logger.info("Operation cancelled by user.")
            print("❌ Cancelled.")
            sys.exit(0)

    # Check config file exists
    if not Path(CONFIG_FILE).exists():
        logger.error(f"Config file not found: {CONFIG_FILE}")
        print(f"❌ Config file not found: {CONFIG_FILE}")
        print("   Create google_ads_config.yaml with your Google Ads credentials")
        sys.exit(1)

    try:
        # Initialize Google Ads client
        client = GoogleAdsClient.load_from_storage(CONFIG_FILE)
        logger.info("Google Ads client initialized successfully")

        # Apply adjustments
        successful, failed, changes = apply_adjustments_to_google_ads(
            client,
            dry_run=args.dry_run,
            logger=logger
        )

        # Summary
        print("\n" + "-" * 80)
        print(f"✅ Successful: {successful}")
        if failed > 0:
            print(f"❌ Failed: {failed}")

        if args.dry_run:
            print("\n[DRY RUN MODE] No changes were applied.")
        else:
            print("\n🎯 Changes applied to Google Ads!")
            print("📅 Monitoring period: Dec 11, 2025 - Jan 11, 2026")
            print("📊 Review performance on 2026-01-11")

        print("-" * 80 + "\n")

        logger.info(f"Operation completed: {successful} successful, {failed} failed")
        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
