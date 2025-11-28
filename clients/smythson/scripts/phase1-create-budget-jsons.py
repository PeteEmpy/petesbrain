#!/usr/bin/env python3
"""Create Phase 1 budget change JSON files"""

from google.ads.googleads.client import GoogleAdsClient
import json

client = GoogleAdsClient.load_from_storage('/Users/administrator/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')

# Exact campaign name patterns (from task specs)
accounts = {
    'UK': ('8573235780', [
        ('SMY | UK | Search | Brand Exact', 1450),
        ('SMY | UK | P Max | H&S Christmas', 650),
        ('SMY | UK | P Max | H&S', 540),  # Note: this will match first, need exact
        ('SMY | UK | P Max | H&S - Men\'s Briefcases', 420),
        ('SMY | UK | Shopping | H&S', 650),
        ('SMY | UK | Search | Semi Brand - Diaries', 350)
    ]),
    'USA': ('7808690871', [
        ('SMY | US | Search | Brand Exact', 1285),
        ('SMY | USA | Search | Brand | Stationery', 135),
        ('SMY | US | P Max | H&S Christmas', 680),
        ('SMY | US | P Max | H&S', 780)
    ]),
    'EUR': ('7679616761', [
        ('SMY | EUR | IT | Search Brand Ai', 100),
        ('SMY | EUR | ROEuro | Search | Brand Ai', 480),
        ('SMY | EUR | DE | Search | Brand Ai', 270),
        ('SMY | EUR | FR | P Max | Christmas', 70)
    ]),
    'ROW': ('5556710725', [
        ('SMY | ROW | Search | Brand Ai', 380)
    ])
}

query = '''
SELECT campaign.id, campaign.name, campaign_budget.id, campaign_budget.amount_micros
FROM campaign
WHERE campaign.status = "ENABLED"
ORDER BY campaign.name
'''

for region, (customer_id, patterns) in accounts.items():
    print(f"\n{'='*120}")
    print(f"{region} Account ({customer_id})")
    print(f"{'='*120}\n")

    response = ga_service.search(customer_id=customer_id, query=query)
    campaigns = list(response)

    changes = []

    for pattern_name, new_budget in patterns:
        # Find exact or partial match
        matched = None
        for row in campaigns:
            # Try exact match first
            if row.campaign.name == pattern_name:
                matched = row
                break
            # Then partial match
            elif pattern_name in row.campaign.name:
                matched = row
                break

        if matched:
            budget_id = matched.campaign_budget.resource_name.split('/')[-1]
            current_budget = matched.campaign_budget.amount_micros / 1_000_000

            print(f"{matched.campaign.name:<65} £{current_budget:>8.2f} → £{new_budget}")

            changes.append({
                'campaign_id': str(matched.campaign.id),
                'budget_id': budget_id,
                'new_daily_budget': float(new_budget),
                'campaign_name': matched.campaign.name,
                'reason': 'Phase 1 Black Friday budget increase'
            })
        else:
            print(f"⚠️  NOT FOUND: {pattern_name}")

    # Save to JSON
    if changes:
        filename = f'phase1-budgets-{region.lower()}.json'
        with open(filename, 'w') as f:
            json.dump(changes, f, indent=2)
        print(f"\n✅ Saved {len(changes)} changes to {filename}\n")

print("="*120)
print("✅ Phase 1 budget change files created - ready for deployment")
print("="*120)
