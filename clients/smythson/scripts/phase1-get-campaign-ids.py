#!/usr/bin/env python3
"""
Get campaign and budget IDs for Smythson Phase 1 Black Friday campaigns.
"""

import os
import json
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Account IDs
accounts = {
    'UK': '8573235780',
    'USA': '7808690871',
    'EUR': '7679616761',
    'ROW': '5556710725'
}

# Campaign name patterns for Phase 1
phase1_campaigns = {
    'UK': [
        ('Brand Exact', 1450),
        ('P Max H&S Christmas', 650),
        ('P Max H&S', 540),
        ('P Max Briefcases', 420),
        ('Shopping H&S', 650),
        ('Semi Brand Diaries', 350)
    ],
    'USA': [
        ('Brand Exact', 1285),
        ('Brand Stationery', 135),
        ('P Max H&S Christmas', 680),
        ('P Max H&S', 780)
    ],
    'EUR': [
        ('IT Brand AI', 100),
        ('ROEuro Brand AI', 480),
        ('DE Brand AI', 270),
        ('FR P Max Christmas', 70)
    ],
    'ROW': [
        ('ROW Search Brand Ai', 380)
    ]
}

query = """
SELECT
    campaign.id,
    campaign.name,
    campaign_budget.id,
    campaign_budget.amount_micros,
    campaign.status
FROM campaign
WHERE campaign.status = 'ENABLED'
ORDER BY campaign.name
"""

def main():
    # Load Google Ads client
    config_file = os.path.expanduser('~/google-ads.yaml')
    client = GoogleAdsClient.load_from_storage(config_file)

    print("=" * 120)
    print("SMYTHSON PHASE 1 - CAMPAIGN AND BUDGET IDS")
    print("=" * 120)
    print()

    all_changes = []

    for region, customer_id in accounts.items():
        print(f"\n{'='*120}")
        print(f"{region} Account ({customer_id})")
        print(f"{'='*120}\n")

        try:
            ga_service = client.get_service("GoogleAdsService")
            response = ga_service.search(customer_id=customer_id, query=query)

            # Get list of campaigns
            campaigns = []
            for row in response:
                campaigns.append({
                    'name': row.campaign.name,
                    'id': row.campaign.id,
                    'budget_id': row.campaign_budget.resource_name.split('/')[-1],
                    'current_budget_micros': row.campaign_budget.amount_micros,
                    'current_budget_pounds': row.campaign_budget.amount_micros / 1_000_000
                })

            # Filter for Phase 1 campaigns and match with new budgets
            print(f"{'Campaign Name':<50} {'Campaign ID':<15} {'Budget ID':<15} {'Current':<12} {'New Budget'}")
            print("-" * 125)

            phase1_patterns = phase1_campaigns.get(region, [])

            for pattern, new_budget in phase1_patterns:
                # Find matching campaign
                matched = None
                for camp in campaigns:
                    if pattern.lower() in camp['name'].lower():
                        matched = camp
                        break

                if matched:
                    print(f"{matched['name']:<50} {matched['id']:<15} {matched['budget_id']:<15} £{matched['current_budget_pounds']:<10.2f} £{new_budget}/day")

                    # Add to changes list
                    all_changes.append({
                        'account': region,
                        'customer_id': customer_id,
                        'campaign_id': str(matched['id']),
                        'budget_id': matched['budget_id'],
                        'campaign_name': matched['name'],
                        'current_daily_budget': matched['current_budget_pounds'],
                        'new_daily_budget': float(new_budget),
                        'reason': f'Phase 1 BF increase'
                    })
                else:
                    print(f"⚠️  NOT FOUND: {pattern}")

        except GoogleAdsException as ex:
            print(f"❌ Error: {ex}")
            continue

    # Save changes to JSON file
    output_file = '/Users/administrator/Documents/PetesBrain/clients/smythson/scripts/phase1-budget-changes.json'

    # Group by account for separate files
    for region in accounts.keys():
        region_changes = [c for c in all_changes if c['account'] == region]
        if region_changes:
            region_file = f'/Users/administrator/Documents/PetesBrain/clients/smythson/scripts/phase1-budget-changes-{region.lower()}.json'
            with open(region_file, 'w') as f:
                json.dump(region_changes, f, indent=2)
            print(f"\n✅ Saved {region} changes to: {region_file}")

    print("\n" + "="*120)
    print(f"✅ Found {len(all_changes)} campaigns for Phase 1")
    print("="*120)

if __name__ == "__main__":
    main()
