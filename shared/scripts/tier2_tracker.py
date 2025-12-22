#!/usr/bin/env python3
"""
Tier 2 Negative Keyword Tracker with 7-Day Auto-Flagging

Tracks Tier 2 search terms (10-29 clicks, 0 conversions) and automatically
flags them for promotion to Tier 1 when they reach 30+ clicks with 0 conversions.

Usage:
    python3 tier2_tracker.py --add-from-csv clients/uno-lighting/reports/uno-lighting-keyword-audit-2025-12-17-tier2.csv
    python3 tier2_tracker.py --check-all
    python3 tier2_tracker.py --check-client uno-lighting
    python3 tier2_tracker.py --report uno-lighting

Features:
    - Adds Tier 2 terms from CSV exports
    - Checks terms after 7 days via Google Ads API
    - Auto-promotes to Tier 1 when threshold reached
    - Generates promotion alerts
    - Maintains historical tracking data
"""

import sys
import json
import argparse
import csv
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# Add MCP server to path
mcp_path = Path(__file__).parent.parent.parent / 'infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, str(mcp_path))

from google.ads.googleads.client import GoogleAdsClient

# Tracker data file location
TRACKER_FILE = Path(__file__).parent.parent / 'data' / 'tier2_tracker.json'
MANAGER_ID = "2569949686"  # Rok Systems MCC


def load_tracker_data() -> Dict:
    """Load existing tracker data from JSON file."""
    if not TRACKER_FILE.exists():
        return {'clients': {}, 'last_updated': None}

    with open(TRACKER_FILE, 'r') as f:
        return json.load(f)


def save_tracker_data(data: Dict):
    """Save tracker data to JSON file."""
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    data['last_updated'] = datetime.now().isoformat()

    with open(TRACKER_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

    print(f"✅ Tracker data saved to {TRACKER_FILE}")


def add_terms_from_csv(csv_file: str, client_slug: str, customer_id: str):
    """
    Add Tier 2 terms from CSV export to tracker.

    Args:
        csv_file: Path to tier2 CSV file
        client_slug: Client identifier (e.g., 'uno-lighting')
        customer_id: Google Ads customer ID
    """
    tracker_data = load_tracker_data()

    if client_slug not in tracker_data['clients']:
        tracker_data['clients'][client_slug] = {
            'customer_id': customer_id,
            'terms': []
        }

    client_data = tracker_data['clients'][client_slug]
    client_data['customer_id'] = customer_id

    # Load CSV
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        terms_added = 0
        terms_updated = 0

        for row in reader:
            search_term = row['search_term']

            # Check if term already exists
            existing_term = next((t for t in client_data['terms'] if t['search_term'] == search_term), None)

            if existing_term:
                # Update existing term
                existing_term['clicks'] = int(row['clicks'])
                existing_term['cost'] = float(row['cost'])
                existing_term['campaign_name'] = row.get('campaign_name', existing_term.get('campaign_name', 'Unknown'))
                existing_term['match_type'] = row.get('match_type', existing_term.get('match_type', 'Unknown'))
                existing_term['last_checked'] = datetime.now().isoformat()
                terms_updated += 1
            else:
                # Add new term
                new_term = {
                    'search_term': search_term,
                    'clicks': int(row['clicks']),
                    'cost': float(row['cost']),
                    'conversions': 0,
                    'campaign_name': row.get('campaign_name', 'Unknown'),
                    'match_type': row.get('match_type', 'Unknown'),
                    'added_date': datetime.now().isoformat(),
                    'next_review_date': row.get('next_review_date', (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')),
                    'status': 'monitoring',
                    'last_checked': datetime.now().isoformat()
                }
                client_data['terms'].append(new_term)
                terms_added += 1

    save_tracker_data(tracker_data)

    print(f"\n✅ Import complete for {client_slug}:")
    print(f"   New terms added: {terms_added}")
    print(f"   Existing terms updated: {terms_updated}")
    print(f"   Total terms tracked: {len(client_data['terms'])}")


def check_term_status(customer_id: str, search_term: str, start_date: str, end_date: str) -> Dict:
    """
    Check current status of a search term via Google Ads API.

    Args:
        customer_id: Google Ads customer ID
        search_term: Search term to check
        start_date: Start date for query (YYYY-MM-DD)
        end_date: End date for query (YYYY-MM-DD)

    Returns:
        Dict with current clicks, conversions, spend
    """
    client = GoogleAdsClient.load_from_storage(Path.home() / 'google-ads.yaml')
    ga_service = client.get_service('GoogleAdsService')

    query = f"""
        SELECT
            search_term_view.search_term,
            metrics.clicks,
            metrics.conversions,
            metrics.cost_micros
        FROM search_term_view
        WHERE search_term_view.search_term = '{search_term}'
          AND segments.date >= '{start_date}'
          AND segments.date <= '{end_date}'
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=query)

        total_clicks = 0
        total_conversions = 0
        total_cost = 0

        for row in response:
            total_clicks += row.metrics.clicks
            total_conversions += row.metrics.conversions
            total_cost += row.metrics.cost_micros / 1_000_000

        return {
            'clicks': total_clicks,
            'conversions': total_conversions,
            'cost': round(total_cost, 2),
            'found': total_clicks > 0
        }
    except Exception as e:
        print(f"⚠️  Error checking term '{search_term}': {e}")
        return {'clicks': 0, 'conversions': 0, 'cost': 0, 'found': False}


def check_client_terms(client_slug: str, force_check: bool = False):
    """
    Check all Tier 2 terms for a client and flag promotions.

    Args:
        client_slug: Client identifier
        force_check: Check all terms regardless of next_review_date
    """
    tracker_data = load_tracker_data()

    if client_slug not in tracker_data['clients']:
        print(f"❌ Client '{client_slug}' not found in tracker")
        return

    client_data = tracker_data['clients'][client_slug]
    customer_id = client_data['customer_id']

    print(f"\n🔍 Checking Tier 2 terms for {client_slug} (Customer ID: {customer_id})")

    # Calculate date range (last 60 days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=60)

    terms_to_check = []
    today = datetime.now().date()

    for term in client_data['terms']:
        if term['status'] != 'monitoring':
            continue

        next_review = datetime.fromisoformat(term['next_review_date']).date()

        if force_check or today >= next_review:
            terms_to_check.append(term)

    if not terms_to_check:
        print(f"✅ No terms due for review (0/{len(client_data['terms'])} terms)")
        return

    print(f"📊 Checking {len(terms_to_check)} terms (out of {len(client_data['terms'])} total tracked)")

    promoted_terms = []
    still_monitoring = []

    for term in terms_to_check:
        print(f"   Checking: {term['search_term'][:50]}...", end=' ')

        status = check_term_status(
            customer_id,
            term['search_term'],
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )

        if not status['found']:
            print("❌ Not found")
            term['status'] = 'not_found'
            term['last_checked'] = datetime.now().isoformat()
            continue

        # Update term data
        term['clicks'] = status['clicks']
        term['conversions'] = status['conversions']
        term['cost'] = status['cost']
        term['last_checked'] = datetime.now().isoformat()

        # Check for promotion to Tier 1
        if status['clicks'] >= 30 and status['conversions'] == 0 and status['cost'] >= 20:
            print(f"🔴 PROMOTE TO TIER 1 ({status['clicks']} clicks, £{status['cost']:.2f})")
            term['status'] = 'promoted_tier1'
            term['promoted_date'] = datetime.now().isoformat()
            promoted_terms.append(term)
        elif status['conversions'] > 0:
            print(f"✅ Converting ({status['conversions']} conv)")
            term['status'] = 'converting'
        else:
            print(f"🟡 Still monitoring ({status['clicks']} clicks, £{status['cost']:.2f})")
            term['next_review_date'] = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            still_monitoring.append(term)

    save_tracker_data(tracker_data)

    # Summary
    print(f"\n📊 Review Summary:")
    print(f"   Promoted to Tier 1: {len(promoted_terms)} terms")
    print(f"   Still monitoring: {len(still_monitoring)} terms")
    print(f"   Converted: {len([t for t in terms_to_check if t.get('status') == 'converting'])} terms")
    print(f"   Not found: {len([t for t in terms_to_check if t.get('status') == 'not_found'])} terms")

    # Show promoted terms
    if promoted_terms:
        print(f"\n🔴 TIER 1 PROMOTION ALERT - {len(promoted_terms)} terms ready for immediate negative keyword addition:")
        for term in promoted_terms:
            print(f"   [{term['search_term']}] - {term['clicks']} clicks, £{term['cost']:.2f}, 0 conversions")

        # Save promotion report
        promotion_file = Path(f"clients/{client_slug}/reports/tier1-promotions-{datetime.now().strftime('%Y-%m-%d')}.txt")
        promotion_file.parent.mkdir(parents=True, exist_ok=True)

        with open(promotion_file, 'w') as f:
            f.write(f"Tier 1 Promotion Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Client: {client_slug}\n")
            f.write(f"Customer ID: {customer_id}\n\n")
            f.write(f"The following {len(promoted_terms)} search terms have been promoted from Tier 2 to Tier 1:\n\n")

            for term in promoted_terms:
                f.write(f"Search Term: {term['search_term']}\n")
                f.write(f"  Clicks: {term['clicks']}\n")
                f.write(f"  Spend: £{term['cost']:.2f}\n")
                f.write(f"  Conversions: 0\n")
                f.write(f"  Campaign: {term['campaign_name']}\n")
                f.write(f"  Match Type: {term['match_type']}\n")
                f.write(f"  Daily Click Rate: {term['clicks']/60:.2f} clicks/day\n")
                f.write(f"  Recommendation: Add as [exact] match negative keyword immediately\n\n")

            f.write(f"\nNext Steps:\n")
            f.write(f"1. Review the promoted terms above\n")
            f.write(f"2. Add as negative keywords using:\n")
            f.write(f"   python3 clients/{client_slug}/scripts/add-negative-keywords.py --campaign-id [ID] --from-file tier1-keywords.txt\n")
            f.write(f"3. Or use the universal script in shared/scripts/add-negative-keywords-universal.py\n")

        print(f"\n✅ Promotion report saved to {promotion_file}")


def check_all_clients(force_check: bool = False):
    """Check all clients in tracker."""
    tracker_data = load_tracker_data()

    if not tracker_data['clients']:
        print("❌ No clients in tracker")
        return

    print(f"📊 Checking {len(tracker_data['clients'])} clients")

    for client_slug in tracker_data['clients']:
        check_client_terms(client_slug, force_check)


def generate_report(client_slug: str):
    """Generate a status report for a client."""
    tracker_data = load_tracker_data()

    if client_slug not in tracker_data['clients']:
        print(f"❌ Client '{client_slug}' not found in tracker")
        return

    client_data = tracker_data['clients'][client_slug]

    # Count terms by status
    monitoring = [t for t in client_data['terms'] if t['status'] == 'monitoring']
    promoted = [t for t in client_data['terms'] if t['status'] == 'promoted_tier1']
    converting = [t for t in client_data['terms'] if t['status'] == 'converting']
    not_found = [t for t in client_data['terms'] if t['status'] == 'not_found']

    print(f"\n{'='*80}")
    print(f"TIER 2 TRACKER REPORT: {client_slug}")
    print(f"{'='*80}")
    print(f"Customer ID: {client_data['customer_id']}")
    print(f"Total tracked terms: {len(client_data['terms'])}")
    print(f"\nStatus Breakdown:")
    print(f"  🟡 Monitoring: {len(monitoring)} terms")
    print(f"  🔴 Promoted to Tier 1: {len(promoted)} terms")
    print(f"  ✅ Converting: {len(converting)} terms")
    print(f"  ❌ Not found: {len(not_found)} terms")

    # Show terms due for review
    today = datetime.now().date()
    due_for_review = [t for t in monitoring if datetime.fromisoformat(t['next_review_date']).date() <= today]

    if due_for_review:
        print(f"\n⚠️  {len(due_for_review)} terms due for review:")
        for term in due_for_review[:10]:
            print(f"   - {term['search_term'][:60]} (next review: {term['next_review_date']})")
        if len(due_for_review) > 10:
            print(f"   ... and {len(due_for_review) - 10} more")

    # Show recently promoted terms
    if promoted:
        print(f"\n🔴 Recently Promoted to Tier 1:")
        for term in promoted[:10]:
            print(f"   - {term['search_term'][:60]} ({term['clicks']} clicks, £{term['cost']:.2f})")
        if len(promoted) > 10:
            print(f"   ... and {len(promoted) - 10} more")

    print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Tier 2 negative keyword tracker with auto-flagging',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Add Tier 2 terms from CSV export
  python3 tier2_tracker.py --add-from-csv clients/uno-lighting/reports/uno-lighting-keyword-audit-2025-12-17-tier2.csv --client-slug uno-lighting --customer-id 6413338364

  # Check all terms for a specific client
  python3 tier2_tracker.py --check-client uno-lighting

  # Check all clients (run daily via cron/LaunchAgent)
  python3 tier2_tracker.py --check-all

  # Force check all terms regardless of review date
  python3 tier2_tracker.py --check-client uno-lighting --force

  # Generate status report
  python3 tier2_tracker.py --report uno-lighting

Workflow:
  1. Run keyword audit to generate tier2.csv
  2. Add terms to tracker with --add-from-csv
  3. Check terms after 7 days with --check-client
  4. Promoted terms saved to tier1-promotions-{date}.txt
  5. Add promoted terms as negative keywords
"""
    )

    parser.add_argument('--add-from-csv', help='Add terms from tier2 CSV file')
    parser.add_argument('--client-slug', help='Client slug (required with --add-from-csv)')
    parser.add_argument('--customer-id', help='Google Ads customer ID (required with --add-from-csv)')
    parser.add_argument('--check-client', help='Check terms for specific client')
    parser.add_argument('--check-all', action='store_true', help='Check all clients')
    parser.add_argument('--force', action='store_true', help='Force check all terms regardless of review date')
    parser.add_argument('--report', help='Generate status report for client')

    args = parser.parse_args()

    if args.add_from_csv:
        if not args.client_slug or not args.customer_id:
            print("❌ --client-slug and --customer-id required with --add-from-csv")
            return 1
        add_terms_from_csv(args.add_from_csv, args.client_slug, args.customer_id)

    elif args.check_client:
        check_client_terms(args.check_client, args.force)

    elif args.check_all:
        check_all_clients(args.force)

    elif args.report:
        generate_report(args.report)

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
