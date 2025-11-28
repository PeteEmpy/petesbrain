#!/usr/bin/env python3
"""Quick script to get all Phase 1 campaign IDs"""

from google.ads.googleads.client import GoogleAdsClient
import json

client = GoogleAdsClient.load_from_storage('/Users/administrator/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')

accounts = {
    'UK': ('8573235780', [
        ('Brand Exact', 1450),
        ('P Max H&S Christmas', 650),
        ('P Max H&S', 540),
        ('P Max Briefcases', 420),
        ('Shopping H&S', 650),
        ('Semi Brand Diaries', 350)
    ]),
    'USA': ('7808690871', [
        ('Brand Exact', 1285),
        ('Brand Stationery', 135),
        ('P Max H&S Christmas', 680),
        ('P Max H&S', 780)
    ]),
    'EUR': ('7679616761', [
        ('IT Brand AI', 100),
        ('ROEuro Brand AI', 480),
        ('DE Brand AI', 270),
        ('FR P Max Christmas', 70)
    ]),
    'ROW': ('5556710725', [
        ('ROW Search Brand Ai', 380)
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
        # Find matching campaign
        matched = None
        for row in campaigns:
            if pattern_name.lower() in row.campaign.name.lower():
                matched = row
                break

        if matched:
            budget_id = matched.campaign_budget.resource_name.split('/')[-1]
            current_budget = matched.campaign_budget.amount_micros / 1_000_000

            print(f"{matched.campaign.name:<60} | ID: {matched.campaign.id:<15} | Budget ID: {budget_id:<15} | £{current_budget:.2f} → £{new_budget}")

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
        print(f"\n✅ Saved {len(changes)} changes to {filename}")

print("\n" + "="*120)
print("✅ Phase 1 budget change files created")
print("="*120)
