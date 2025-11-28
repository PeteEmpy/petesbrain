#!/usr/bin/env python3
"""
Update Campaign Budgets via Google Ads API

Standard utility for updating daily budgets across campaigns.
Uses Google Ads API v18 with direct HTTP requests via MCP oauth.

Usage:
    python3 update-campaign-budgets.py --customer-id CUSTOMER_ID --changes changes.json

Changes JSON format:
    [
        {
            "campaign_id": "12345",
            "budget_id": "67890",
            "new_daily_budget": 100.00,
            "campaign_name": "Campaign Name",
            "reason": "Optional reason for change"
        },
        ...
    ]

Example:
    python3 update-campaign-budgets.py \\
        --customer-id 5898250490 \\
        --changes devonshire-budget-changes.json

Author: Peter Empson
Created: 2025-11-20
"""

import sys
import os
import json
import argparse
import requests
from datetime import datetime
from pathlib import Path

# Add MCP server oauth directory to path for authentication
mcp_oauth_path = Path(__file__).parent.parent.parent / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server' / 'oauth'
sys.path.insert(0, str(mcp_oauth_path))

# Load environment variables from .env file
env_file = Path(__file__).parent.parent.parent / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server' / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from google_auth import get_headers_with_auto_token, format_customer_id

# Google Ads API endpoint
API_VERSION = "v18"
BASE_URL = f"https://googleads.googleapis.com/{API_VERSION}"


def pounds_to_micros(pounds):
    """Convert pounds to micros (£1 = 1,000,000 micros)"""
    return int(pounds * 1_000_000)


def micros_to_pounds(micros):
    """Convert micros to pounds"""
    return float(micros) / 1_000_000


def update_campaign_budget(customer_id, budget_id, new_amount_micros, dry_run=False):
    """
    Update a campaign budget via Google Ads API.

    Args:
        customer_id: Google Ads customer ID
        budget_id: Campaign budget ID
        new_amount_micros: New daily budget amount in micros
        dry_run: If True, don't actually make the change

    Returns:
        (success: bool, message: str)
    """
    if dry_run:
        return True, f"DRY RUN - Would update budget {budget_id} to £{micros_to_pounds(new_amount_micros):.2f}/day"

    # Format customer ID
    formatted_customer_id = format_customer_id(customer_id)

    # Construct resource name
    resource_name = f"customers/{formatted_customer_id}/campaignBudgets/{budget_id}"

    # Prepare mutation
    operation = {
        "update": {
            "resourceName": resource_name,
            "amountMicros": str(new_amount_micros)
        },
        "updateMask": "amountMicros"
    }

    # API endpoint
    url = f"{BASE_URL}/customers/{formatted_customer_id}/campaignBudgets:mutate"

    # Get authenticated headers
    headers = get_headers_with_auto_token()

    # Request body
    body = {
        "operations": [operation]
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()

        result = response.json()
        return True, f"✓ Updated budget {budget_id} to £{micros_to_pounds(new_amount_micros):.2f}/day"

    except requests.exceptions.HTTPError as e:
        error_msg = f"✗ Failed to update budget {budget_id}: {e.response.text}"
        return False, error_msg
    except Exception as e:
        error_msg = f"✗ Error updating budget {budget_id}: {str(e)}"
        return False, error_msg


def validate_changes(changes):
    """
    Validate changes JSON structure.

    Args:
        changes: List of change dictionaries

    Returns:
        (valid: bool, errors: list)
    """
    errors = []

    if not isinstance(changes, list):
        errors.append("Changes must be a list")
        return False, errors

    required_fields = ["campaign_id", "budget_id", "new_daily_budget"]

    for i, change in enumerate(changes):
        if not isinstance(change, dict):
            errors.append(f"Change {i}: Must be a dictionary")
            continue

        for field in required_fields:
            if field not in change:
                errors.append(f"Change {i}: Missing required field '{field}'")

        # Validate budget is positive number
        if "new_daily_budget" in change:
            try:
                budget = float(change["new_daily_budget"])
                if budget <= 0:
                    errors.append(f"Change {i}: Budget must be positive (got {budget})")
            except (ValueError, TypeError):
                errors.append(f"Change {i}: Invalid budget value '{change['new_daily_budget']}'")

    return len(errors) == 0, errors


def print_summary(changes):
    """Print a summary table of changes to be made"""
    print()
    print("=" * 100)
    print("BUDGET CHANGES SUMMARY")
    print("=" * 100)
    print()
    print(f"{'Campaign Name':<40} {'Campaign ID':<15} {'New Budget':<15} Reason")
    print("-" * 100)

    for change in changes:
        campaign_name = change.get("campaign_name", "Unknown")[:38]
        campaign_id = change.get("campaign_id", "")
        new_budget = f"£{change['new_daily_budget']:.2f}/day"
        reason = change.get("reason", "")[:30]

        print(f"{campaign_name:<40} {campaign_id:<15} {new_budget:<15} {reason}")

    print("-" * 100)
    print(f"Total campaigns to update: {len(changes)}")
    print("=" * 100)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Update campaign budgets via Google Ads API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Update budgets from JSON file
  python3 update-campaign-budgets.py --customer-id 5898250490 --changes budgets.json

  # Dry run (preview changes without applying)
  python3 update-campaign-budgets.py --customer-id 5898250490 --changes budgets.json --dry-run

  # Provide changes via stdin
  echo '[{"campaign_id":"123","budget_id":"456","new_daily_budget":100}]' | \\
    python3 update-campaign-budgets.py --customer-id 5898250490 --changes -

Changes JSON format:
  [
    {
      "campaign_id": "12345",
      "budget_id": "67890",
      "new_daily_budget": 100.00,
      "campaign_name": "Optional: Campaign Name",
      "reason": "Optional: Reason for change"
    }
  ]
"""
    )

    parser.add_argument(
        "--customer-id",
        required=True,
        help="Google Ads customer ID (10 digits, no dashes)"
    )

    parser.add_argument(
        "--changes",
        required=True,
        help="Path to JSON file with budget changes (or '-' for stdin)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )

    args = parser.parse_args()

    # Load changes
    try:
        if args.changes == "-":
            changes = json.load(sys.stdin)
        else:
            with open(args.changes, 'r') as f:
                changes = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Changes file not found: {args.changes}")
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in changes file: {e}")
        return 1

    # Validate changes
    valid, errors = validate_changes(changes)
    if not valid:
        print("ERROR: Invalid changes format:")
        for error in errors:
            print(f"  - {error}")
        return 1

    # Print summary
    print()
    print("=" * 100)
    print(f"BUDGET UPDATE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    print(f"Customer ID: {args.customer_id}")
    print(f"Mode: {'DRY RUN (no changes will be made)' if args.dry_run else 'LIVE (changes will be applied)'}")

    print_summary(changes)

    # Confirm if not dry run
    if not args.dry_run:
        response = input("Proceed with budget updates? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            return 0
        print()

    # Execute updates
    print("=" * 100)
    print("EXECUTING UPDATES")
    print("=" * 100)
    print()

    successful = 0
    failed = 0

    for i, change in enumerate(changes, 1):
        campaign_name = change.get("campaign_name", f"Campaign {change['campaign_id']}")
        new_amount_micros = pounds_to_micros(change["new_daily_budget"])

        if args.verbose:
            print(f"[{i}/{len(changes)}] Updating {campaign_name}...")

        success, message = update_campaign_budget(
            args.customer_id,
            change["budget_id"],
            new_amount_micros,
            dry_run=args.dry_run
        )

        print(f"[{i}/{len(changes)}] {message}")

        if success:
            successful += 1
        else:
            failed += 1

    # Final summary
    print()
    print("=" * 100)
    print("RESULTS")
    print("=" * 100)
    print(f"Successful: {successful}/{len(changes)}")
    print(f"Failed: {failed}/{len(changes)}")

    if args.dry_run:
        print()
        print("DRY RUN COMPLETE - No changes were made")
        print("Remove --dry-run flag to apply changes")
    elif successful == len(changes):
        print()
        print("✅ ALL BUDGET CHANGES SUCCESSFULLY APPLIED")
    else:
        print()
        print(f"⚠️  {failed} CHANGES FAILED - Review errors above")

    print("=" * 100)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
