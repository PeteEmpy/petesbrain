#!/usr/bin/env python3
"""
Interactive Tier 1 Negative Keyword Deployment

Consolidated batch deployment workflow for all clients.
Run from bi-weekly task to review and deploy Tier 1 terms.

Usage:
    python3 deploy-tier1-interactive.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'infrastructure/mcp-servers/google-ads-mcp-server'))

from tier2_tracker import load_tracker_data, save_tracker_data
from google.ads.googleads.client import GoogleAdsClient
from oauth.google_auth import get_headers_with_auto_token, format_customer_id
import requests

API_VERSION = "v22"
MANAGER_ID = "2569949686"


def get_tier1_terms_by_client() -> Dict[str, List[Dict]]:
    """
    Get all Tier 1 terms grouped by client from tracker.

    Returns dict: {client_slug: [list of tier1 terms]}
    """
    tracker_data = load_tracker_data()
    tier1_by_client = {}

    for client_slug, client_data in tracker_data.get('clients', {}).items():
        tier1_terms = [
            t for t in client_data.get('terms', [])
            if t.get('status') == 'promoted_tier1' and not t.get('deployed', False)
        ]

        if tier1_terms:
            tier1_by_client[client_slug] = {
                'customer_id': client_data.get('customer_id'),
                'terms': tier1_terms
            }

    return tier1_by_client


def calculate_annual_waste(terms: List[Dict]) -> float:
    """Calculate projected annual waste from 60-day data"""
    total_60day = sum(t.get('cost', 0) for t in terms)
    return total_60day * 6  # Annualize


def get_campaigns_for_account(customer_id: str, manager_id: str = MANAGER_ID) -> List[Dict]:
    """Get list of active campaigns for account"""
    try:
        headers = get_headers_with_auto_token()
        if manager_id:
            headers['login-customer-id'] = format_customer_id(manager_id)

        formatted_customer_id = format_customer_id(customer_id)
        url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_customer_id}/googleAds:searchStream"

        query = """
            SELECT campaign.id, campaign.name, campaign.status
            FROM campaign
            WHERE campaign.status IN ('ENABLED', 'PAUSED')
            ORDER BY campaign.name
        """

        response = requests.post(url, headers=headers, json={"query": query})
        response.raise_for_status()

        campaigns = []
        for line in response.text.strip().split('\n'):
            if line:
                result = eval(line)
                if 'results' in result:
                    for row in result['results']:
                        campaigns.append({
                            'id': row['campaign']['id'],
                            'name': row['campaign']['name'],
                            'status': row['campaign']['status']
                        })

        return campaigns
    except Exception as e:
        print(f"⚠️  Error fetching campaigns: {e}")
        return []


def add_campaign_negative_keywords(
    customer_id: str,
    campaign_id: str,
    keywords: List[str],
    manager_id: str = MANAGER_ID
) -> bool:
    """Add negative keywords to campaign"""
    try:
        formatted_customer_id = format_customer_id(customer_id)
        headers = get_headers_with_auto_token()
        if manager_id:
            headers['login-customer-id'] = format_customer_id(manager_id)

        campaign_resource = f"customers/{formatted_customer_id}/campaigns/{campaign_id}"
        operations = []

        for keyword_text in keywords:
            operations.append({
                "create": {
                    "campaign": campaign_resource,
                    "negative": True,
                    "keyword": {
                        "text": keyword_text,
                        "matchType": "EXACT"
                    }
                }
            })

        url = f"https://googleads.googleapis.com/{API_VERSION}/customers/{formatted_customer_id}/campaignCriteria:mutate"
        payload = {"operations": operations}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        results = result.get('results', [])

        print(f"   ✅ Deployed {len(results)} negative keywords")
        return True

    except Exception as e:
        print(f"   ❌ Error deploying: {e}")
        return False


def deploy_client_batch(client_slug: str, client_data: Dict) -> Tuple[int, int]:
    """
    Deploy all Tier 1 terms for a client.

    Returns: (deployed_count, failed_count)
    """
    customer_id = client_data['customer_id']
    terms = client_data['terms']

    print(f"\n{'='*80}")
    print(f"CLIENT: {client_slug.upper()}")
    print(f"{'='*80}")
    print(f"Customer ID: {customer_id}")
    print(f"Tier 1 Terms: {len(terms)}")
    print(f"Projected Annual Waste: £{calculate_annual_waste(terms):,.0f}")
    print()

    # Show terms
    for i, term in enumerate(terms[:10], 1):
        print(f"  {i}. [{term['search_term']}] - {term['clicks']} clicks, £{term['cost']:.2f}")

    if len(terms) > 10:
        print(f"  ... and {len(terms) - 10} more terms")

    print()

    # Ask to proceed
    response = input(f"Deploy {len(terms)} terms to {client_slug}? (y/n/skip): ").strip().lower()

    if response == 'skip':
        print("⏭️  Skipped")
        return (0, 0)

    if response != 'y':
        print("❌ Cancelled")
        return (0, 0)

    # Ask for mode
    mode = input("Mode: (batch/review): ").strip().lower()

    if mode == 'batch':
        return deploy_batch_mode(client_slug, customer_id, terms)
    elif mode == 'review':
        return deploy_review_mode(client_slug, customer_id, terms)
    else:
        print("❌ Invalid mode")
        return (0, 0)


def deploy_batch_mode(client_slug: str, customer_id: str, terms: List[Dict]) -> Tuple[int, int]:
    """Deploy all terms to one campaign in batch"""
    print("\n🚀 Batch Mode")

    # Get campaigns
    print("Fetching campaigns...")
    campaigns = get_campaigns_for_account(customer_id)

    if not campaigns:
        print("❌ No campaigns found")
        return (0, len(terms))

    # Show campaigns
    print("\nAvailable campaigns:")
    for i, camp in enumerate(campaigns[:20], 1):
        status_icon = "✅" if camp['status'] == 'ENABLED' else "⏸️"
        print(f"  {i}. {status_icon} {camp['name'][:60]} (ID: {camp['id']})")

    if len(campaigns) > 20:
        print(f"  ... and {len(campaigns) - 20} more")

    # Get campaign selection
    campaign_input = input("\nEnter campaign number or ID (or 'all' for account-level): ").strip()

    if campaign_input == 'all':
        print("❌ Account-level negatives not yet supported")
        return (0, len(terms))

    # Parse campaign ID
    try:
        if campaign_input.isdigit() and int(campaign_input) <= len(campaigns):
            campaign_id = campaigns[int(campaign_input) - 1]['id']
        else:
            campaign_id = campaign_input
    except:
        print("❌ Invalid campaign selection")
        return (0, len(terms))

    # Deploy
    keywords = [t['search_term'] for t in terms]
    print(f"\nDeploying {len(keywords)} terms to campaign {campaign_id}...")

    success = add_campaign_negative_keywords(customer_id, campaign_id, keywords)

    if success:
        # Mark as deployed in tracker
        mark_terms_deployed(client_slug, [t['search_term'] for t in terms], campaign_id)
        return (len(terms), 0)
    else:
        return (0, len(terms))


def deploy_review_mode(client_slug: str, customer_id: str, terms: List[Dict]) -> Tuple[int, int]:
    """Review each term individually"""
    print("\n🔍 Review Mode")

    # Get campaigns once
    print("Fetching campaigns...")
    campaigns = get_campaigns_for_account(customer_id)

    if not campaigns:
        print("❌ No campaigns found")
        return (0, len(terms))

    deployed = 0
    failed = 0
    skipped = 0

    for i, term in enumerate(terms, 1):
        print(f"\n--- Term {i}/{len(terms)} ---")
        print(f"Search Term: [{term['search_term']}]")
        print(f"  Clicks: {term['clicks']}")
        print(f"  Spend: £{term['cost']:.2f}")
        print(f"  Campaign: {term.get('campaign_name', 'Unknown')}")

        action = input("Action: (d)eploy / (s)kip / (q)uit: ").strip().lower()

        if action == 'q':
            print("Exiting review mode")
            break

        if action == 's':
            skipped += 1
            continue

        if action == 'd':
            # Show campaigns (compact)
            print("\nCampaigns:")
            for j, camp in enumerate(campaigns[:10], 1):
                print(f"  {j}. {camp['name'][:50]}")

            camp_input = input("Campaign # or ID: ").strip()

            try:
                if camp_input.isdigit() and int(camp_input) <= len(campaigns):
                    campaign_id = campaigns[int(camp_input) - 1]['id']
                else:
                    campaign_id = camp_input

                success = add_campaign_negative_keywords(customer_id, campaign_id, [term['search_term']])

                if success:
                    mark_terms_deployed(client_slug, [term['search_term']], campaign_id)
                    deployed += 1
                else:
                    failed += 1
            except:
                print("❌ Invalid selection")
                failed += 1

    return (deployed, failed)


def mark_terms_deployed(client_slug: str, search_terms: List[str], campaign_id: str):
    """Mark terms as deployed in tracker"""
    tracker_data = load_tracker_data()

    if client_slug not in tracker_data.get('clients', {}):
        return

    client_data = tracker_data['clients'][client_slug]

    for term_data in client_data.get('terms', []):
        if term_data['search_term'] in search_terms:
            term_data['deployed'] = True
            term_data['deployed_date'] = datetime.now().isoformat()
            term_data['deployed_campaign_id'] = campaign_id

    save_tracker_data(tracker_data)


def generate_deployment_report(results: Dict[str, Tuple[int, int]]):
    """Generate summary report"""
    print("\n" + "="*80)
    print("DEPLOYMENT SUMMARY")
    print("="*80)

    total_deployed = 0
    total_failed = 0

    for client_slug, (deployed, failed) in results.items():
        total_deployed += deployed
        total_failed += failed

        if deployed > 0 or failed > 0:
            print(f"\n{client_slug}:")
            print(f"  ✅ Deployed: {deployed}")
            print(f"  ❌ Failed: {failed}")

    print(f"\n{'='*80}")
    print(f"TOTAL DEPLOYED: {total_deployed}")
    print(f"TOTAL FAILED: {total_failed}")
    print(f"{'='*80}")

    # Save report
    report_file = Path(__file__).parent.parent / 'data' / 'state' / f'deployment-report-{datetime.now():%Y-%m-%d}.json'
    report_file.parent.mkdir(parents=True, exist_ok=True)

    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_deployed': total_deployed,
            'total_failed': total_failed,
            'results': {k: {'deployed': v[0], 'failed': v[1]} for k, v in results.items()}
        }, f, indent=2)

    print(f"\n📄 Report saved: {report_file}")


def main():
    """Main interactive workflow"""
    print("\n" + "="*80)
    print("TIER 1 NEGATIVE KEYWORD DEPLOYMENT")
    print("="*80)
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Get all Tier 1 terms
    tier1_by_client = get_tier1_terms_by_client()

    if not tier1_by_client:
        print("✅ No Tier 1 terms pending deployment")
        return

    # Show summary
    print(f"SUMMARY: {len(tier1_by_client)} client(s) with Tier 1 terms\n")

    total_terms = 0
    total_waste = 0

    for client_slug, data in tier1_by_client.items():
        terms = data['terms']
        waste = calculate_annual_waste(terms)
        total_terms += len(terms)
        total_waste += waste

        print(f"  - {client_slug}: {len(terms)} terms (£{waste:,.0f}/year)")

    print(f"\nTOTAL: {total_terms} terms, £{total_waste:,.0f}/year projected waste")
    print()

    input("Press Enter to begin deployment review...")

    # Process each client
    results = {}

    for client_slug, data in tier1_by_client.items():
        deployed, failed = deploy_client_batch(client_slug, data)
        results[client_slug] = (deployed, failed)

    # Generate report
    generate_deployment_report(results)

    print("\n✅ Deployment complete!")
    print("💡 Mark your bi-weekly deployment task as complete in Task Manager")


if __name__ == "__main__":
    main()
