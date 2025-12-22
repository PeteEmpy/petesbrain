#!/usr/bin/env python3
"""
P9 Budget Verification Script
Verifies that budget changes have been applied correctly
"""

import sys
import os
from datetime import datetime
from typing import Dict, List

# Add path to MCP servers
sys.path.append('/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server')

def verify_campaign_budgets(expected_budgets: Dict[str, Dict[str, float]]) -> Dict:
    """
    Verify campaign budgets match expected values

    Args:
        expected_budgets: Dict of campaign_id -> {name, expected_budget}

    Returns:
        Dict with verification results
    """
    from google_ads_service import GoogleAdsService

    service = GoogleAdsService()
    results = {
        'timestamp': datetime.now().isoformat(),
        'campaigns_checked': 0,
        'campaigns_correct': 0,
        'campaigns_incorrect': [],
        'total_expected': 0,
        'total_actual': 0
    }

    # Group campaigns by customer_id
    campaigns_by_customer = {}
    for campaign_id, details in expected_budgets.items():
        customer_id = details['customer_id']
        if customer_id not in campaigns_by_customer:
            campaigns_by_customer[customer_id] = []
        campaigns_by_customer[customer_id].append({
            'campaign_id': campaign_id,
            'name': details['name'],
            'expected_budget': details['expected_budget']
        })

    # Query each account
    for customer_id, campaigns in campaigns_by_customer.items():
        campaign_ids = [c['campaign_id'] for c in campaigns]

        query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.id IN ({','.join(campaign_ids)})
        """

        try:
            response = service.search(customer_id, query)

            for row in response:
                campaign_id = str(row.campaign.id)
                actual_budget = row.campaign_budget.amount_micros / 1_000_000

                # Find expected budget
                expected = next((c for c in campaigns if c['campaign_id'] == campaign_id), None)
                if expected:
                    results['campaigns_checked'] += 1
                    results['total_expected'] += expected['expected_budget']
                    results['total_actual'] += actual_budget

                    # Allow 1% tolerance for rounding
                    if abs(actual_budget - expected['expected_budget']) <= expected['expected_budget'] * 0.01:
                        results['campaigns_correct'] += 1
                    else:
                        results['campaigns_incorrect'].append({
                            'campaign_id': campaign_id,
                            'name': row.campaign.name,
                            'expected': expected['expected_budget'],
                            'actual': actual_budget,
                            'difference': actual_budget - expected['expected_budget']
                        })

        except Exception as e:
            print(f"Error querying customer {customer_id}: {e}")

    return results

def print_verification_report(results: Dict):
    """Print a formatted verification report"""

    print("\n" + "=" * 60)
    print("P9 BUDGET VERIFICATION REPORT")
    print("=" * 60)
    print(f"Timestamp: {results['timestamp']}")
    print(f"Campaigns checked: {results['campaigns_checked']}")
    print(f"Campaigns correct: {results['campaigns_correct']}")
    print(f"Success rate: {results['campaigns_correct'] / results['campaigns_checked'] * 100:.1f}%")
    print(f"\nTotal expected budget: £{results['total_expected']:,.2f}")
    print(f"Total actual budget: £{results['total_actual']:,.2f}")
    print(f"Difference: £{results['total_actual'] - results['total_expected']:,.2f}")

    if results['campaigns_incorrect']:
        print("\n" + "=" * 60)
        print("⚠️ CAMPAIGNS WITH INCORRECT BUDGETS:")
        print("=" * 60)
        for campaign in results['campaigns_incorrect']:
            print(f"\nCampaign: {campaign['name']}")
            print(f"  ID: {campaign['campaign_id']}")
            print(f"  Expected: £{campaign['expected']:,.2f}")
            print(f"  Actual: £{campaign['actual']:,.2f}")
            print(f"  Difference: £{campaign['difference']:+,.2f}")
    else:
        print("\n✅ All campaigns have correct budgets!")

    print("\n" + "=" * 60)

def verify_top_performers():
    """Verify the top ROAS performers have adequate budgets"""

    print("\n" + "=" * 60)
    print("TOP PERFORMER BUDGET CHECK")
    print("=" * 60)

    top_performers = [
        {'customer_id': '7808690871', 'campaign_id': '22796857828', 'name': 'US P Max Bags', 'min_budget': 400},
        {'customer_id': '7808690871', 'campaign_id': '22546298306', 'name': 'US PMax Zombies', 'min_budget': 250},
        {'customer_id': '7679616761', 'campaign_id': '1599767262', 'name': 'EUR IT Search Brand', 'min_budget': 200},
        {'customer_id': '8573235780', 'campaign_id': '13810745002', 'name': 'UK Semi Brand Diaries', 'min_budget': 250},
        {'customer_id': '8573235780', 'campaign_id': '13811031042', 'name': 'UK Brand Exact', 'min_budget': 200},
    ]

    from google_ads_service import GoogleAdsService
    service = GoogleAdsService()

    for performer in top_performers:
        query = f"""
        SELECT
            campaign.name,
            campaign_budget.amount_micros,
            campaign.status
        FROM campaign
        WHERE campaign.id = {performer['campaign_id']}
        """

        try:
            response = service.search(performer['customer_id'], query)
            for row in response:
                actual_budget = row.campaign_budget.amount_micros / 1_000_000
                status = row.campaign.status.name

                if actual_budget >= performer['min_budget']:
                    print(f"✅ {performer['name']}: £{actual_budget:,.2f} ({status})")
                else:
                    print(f"⚠️ {performer['name']}: £{actual_budget:,.2f} - BELOW MINIMUM £{performer['min_budget']} ({status})")
        except Exception as e:
            print(f"❌ Error checking {performer['name']}: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Verify P9 budget changes')
    parser.add_argument('--date', help='Date to verify (dec22, dec24, dec26)', default='current')
    parser.add_argument('--top-performers', action='store_true', help='Check top performer budgets')

    args = parser.parse_args()

    if args.top_performers:
        verify_top_performers()
    else:
        # Load expected budgets based on date
        if args.date == 'dec22':
            expected_budgets = {
                '13810745002': {'customer_id': '8573235780', 'name': 'UK Semi Brand Diaries', 'expected_budget': 250.00},
                '13811031042': {'customer_id': '8573235780', 'name': 'UK Brand Exact', 'expected_budget': 200.00},
                '22796857828': {'customer_id': '7808690871', 'name': 'US P Max Bags', 'expected_budget': 150.00},
                '22546298306': {'customer_id': '7808690871', 'name': 'US PMax Zombies', 'expected_budget': 100.00},
                '1599767262': {'customer_id': '7679616761', 'name': 'EUR IT Search Brand', 'expected_budget': 100.00},
                # Add more as needed
            }
        elif args.date == 'dec24':
            expected_budgets = {
                '13810745002': {'customer_id': '8573235780', 'name': 'UK Semi Brand Diaries', 'expected_budget': 500.00},
                '13811031042': {'customer_id': '8573235780', 'name': 'UK Brand Exact', 'expected_budget': 400.00},
                '22796857828': {'customer_id': '7808690871', 'name': 'US P Max Bags', 'expected_budget': 400.00},
                '22546298306': {'customer_id': '7808690871', 'name': 'US PMax Zombies', 'expected_budget': 250.00},
                '1599767262': {'customer_id': '7679616761', 'name': 'EUR IT Search Brand', 'expected_budget': 200.00},
                # Add more as needed
            }
        elif args.date == 'dec26':
            expected_budgets = {
                '13810745002': {'customer_id': '8573235780', 'name': 'UK Semi Brand Diaries', 'expected_budget': 1500.00},
                '13811031042': {'customer_id': '8573235780', 'name': 'UK Brand Exact', 'expected_budget': 1200.00},
                '22796857828': {'customer_id': '7808690871', 'name': 'US P Max Bags', 'expected_budget': 1500.00},
                '22546298306': {'customer_id': '7808690871', 'name': 'US PMax Zombies', 'expected_budget': 800.00},
                '1599767262': {'customer_id': '7679616761', 'name': 'EUR IT Search Brand', 'expected_budget': 800.00},
                # Add more as needed
            }
        else:
            print("Please specify --date (dec22, dec24, dec26) or use --top-performers")
            sys.exit(1)

        results = verify_campaign_budgets(expected_budgets)
        print_verification_report(results)