#!/usr/bin/env python3
"""
Get campaign and budget IDs for Smythson Phase 1 Black Friday campaigns.
"""

import sys
from pathlib import Path

# Add google_ads_query to path
mcp_path = Path(__file__).parent.parent.parent.parent / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server'
sys.path.insert(0, str(mcp_path))

from google_ads_query import run_gaql_query

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
        'Brand Exact',
        'P Max H&S Christmas',
        'P Max H&S',
        'P Max Briefcases',
        'Shopping H&S',
        'Semi Brand Diaries'
    ],
    'USA': [
        'Brand Exact',
        'Brand Stationery',
        'P Max H&S Christmas',
        'P Max H&S'
    ],
    'EUR': [
        'IT Brand AI',
        'ROEuro Brand AI',
        'DE Brand AI',
        'FR P Max Christmas'
    ],
    'ROW': [
        'ROW Search Brand Ai'
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

print("Fetching campaign details for Phase 1...\n")

for region, customer_id in accounts.items():
    print(f"\n{'='*80}")
    print(f"{region} Account ({customer_id})")
    print(f"{'='*80}\n")

    result = run_gaql_query(customer_id, query)

    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        continue

    # Filter for Phase 1 campaigns
    relevant_campaigns = []
    for row in result['results']:
        campaign_name = row['campaign']['name']

        # Check if this campaign matches any Phase 1 pattern
        for pattern in phase1_campaigns.get(region, []):
            if pattern.lower() in campaign_name.lower():
                relevant_campaigns.append(row)
                break

    if not relevant_campaigns:
        print(f"No Phase 1 campaigns found")
        continue

    print(f"{'Campaign Name':<50} {'Campaign ID':<15} {'Budget ID':<15} {'Current Budget'}")
    print("-" * 120)

    for row in relevant_campaigns:
        campaign_name = row['campaign']['name']
        campaign_id = row['campaign']['resourceName'].split('/')[-1]
        budget_id = row['campaignBudget']['resourceName'].split('/')[-1]
        current_budget_micros = row['campaignBudget']['amountMicros']
        current_budget_pounds = current_budget_micros / 1_000_000

        print(f"{campaign_name:<50} {campaign_id:<15} {budget_id:<15} £{current_budget_pounds:.2f}/day")

print("\n" + "="*80)
print("✅ Campaign details retrieved")
print("="*80)
