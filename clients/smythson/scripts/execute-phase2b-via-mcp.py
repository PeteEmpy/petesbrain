#!/usr/bin/env python3
"""
Execute Phase IIb budget changes via direct API calls
Uses the Google Ads API client to update campaign budgets
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add Google Ads API path
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server')))

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from oauth.google_auth import get_credentials

# Load budget changes
changes_file = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports/phase2b-budget-changes-for-mcp.json')

with open(changes_file, 'r') as f:
    data = json.load(f)

changes = data['changes']

print("=" * 100)
print("EXECUTING PHASE IIB BUDGET CHANGES")
print("=" * 100)
print(f"\nTotal campaigns: {len(changes)}")
print(f"Current total: £{data['summary']['current_daily_total_gbp']:,.2f}/day")
print(f"New total: £{data['summary']['new_daily_total_gbp']:,.2f}/day")
print(f"Net change: £{data['summary']['net_change_gbp']:,.2f}/day")

# Initialize Google Ads client
credentials = get_credentials()
client = GoogleAdsClient(
    credentials=credentials,
    developer_token="qJnu7KFWSohkACUINZCuRw",  # From google-ads.yaml
    login_customer_id="2569949686"  # Manager ID
)

results = {
    'timestamp': datetime.now().isoformat(),
    'phase': 'Phase 2B: Post Last Orders',
    'total_campaigns': len(changes),
    'successful': 0,
    'failed': 0,
    'details': []
}

print("\n" + "=" * 100)
print("EXECUTING BUDGET UPDATES")
print("=" * 100)

for i, change in enumerate(changes, 1):
    print(f"\n[{i}/{len(changes)}] {change['campaign_name']}")
    print(f"   Customer: {change['customer_id']}")
    print(f"   Campaign: {change['campaign_id']}")
    print(f"   Budget: £{change['current_budget_gbp']:.2f} → £{change['new_budget_gbp']:.2f}")

    try:
        # Get campaign budget service
        campaign_budget_service = client.get_service("CampaignBudgetService")
        campaign_service = client.get_service("CampaignService")

        # First, get the campaign to find its budget
        campaign_query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign_budget.id,
                campaign_budget.amount_micros
            FROM campaign
            WHERE campaign.id = {change['campaign_id']}
        """

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search(
            customer_id=change['customer_id'],
            query=campaign_query
        )

        budget_id = None
        for row in response:
            budget_id = row.campaign_budget.id
            current_budget_micros = row.campaign_budget.amount_micros
            print(f"   Found budget ID: {budget_id}")
            print(f"   Current API budget: £{current_budget_micros / 1_000_000:.2f}")

        if not budget_id:
            print("   ❌ Budget not found")
            results['failed'] += 1
            results['details'].append({
                'campaign_id': change['campaign_id'],
                'campaign_name': change['campaign_name'],
                'status': 'failed',
                'error': 'Budget not found'
            })
            continue

        # Update the budget
        campaign_budget_operation = client.get_type("CampaignBudgetOperation")
        campaign_budget = campaign_budget_operation.update

        campaign_budget.resource_name = campaign_budget_service.campaign_budget_path(
            change['customer_id'],
            budget_id
        )
        campaign_budget.amount_micros = change['new_budget_micros']

        client.copy_from(
            campaign_budget_operation.update_mask,
            client.get_type("FieldMask", version="v18"),
            paths=["amount_micros"]
        )

        # Execute the update
        campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=change['customer_id'],
            operations=[campaign_budget_operation]
        )

        print(f"   ✅ Budget updated successfully")

        results['successful'] += 1
        results['details'].append({
            'campaign_id': change['campaign_id'],
            'campaign_name': change['campaign_name'],
            'status': 'success',
            'old_budget_gbp': change['current_budget_gbp'],
            'new_budget_gbp': change['new_budget_gbp']
        })

    except GoogleAdsException as ex:
        print(f"   ❌ Google Ads API Error: {ex}")
        results['failed'] += 1
        results['details'].append({
            'campaign_id': change['campaign_id'],
            'campaign_name': change['campaign_name'],
            'status': 'failed',
            'error': str(ex)
        })

    except Exception as ex:
        print(f"   ❌ Error: {ex}")
        results['failed'] += 1
        results['details'].append({
            'campaign_id': change['campaign_id'],
            'campaign_name': change['campaign_name'],
            'status': 'failed',
            'error': str(ex)
        })

# Save results
results_file = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports/phase2b-deployment-results.json')
with open(results_file, 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "=" * 100)
print("DEPLOYMENT COMPLETE")
print("=" * 100)
print(f"\n✅ Successful: {results['successful']}/{len(changes)}")
print(f"❌ Failed: {results['failed']}/{len(changes)}")
print(f"\n📄 Results saved to: {results_file}")

if results['failed'] == 0:
    print("\n🎉 All budget changes applied successfully!")
else:
    print(f"\n⚠️  {results['failed']} campaigns failed - review results file")
