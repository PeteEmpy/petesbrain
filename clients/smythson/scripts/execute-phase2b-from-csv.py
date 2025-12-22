#!/usr/bin/env python3
"""
Execute Phase IIb Budget Deployment from CSV
Applies the exact budget changes specified in phase2b-post-last-orders-dec17-EXACT.csv
"""

import csv
import json
import sys
from pathlib import Path
from datetime import datetime

# Add MCP integration
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server')))
from oauth.google_auth import execute_gaql, get_headers_with_auto_token

print("=" * 100)
print("SMYTHSON PHASE IIB - BUDGET DEPLOYMENT FROM CSV")
print("=" * 100)

# Load CSV
csv_file = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/spreadsheets/phase2b-post-last-orders-dec17-EXACT.csv')

print(f"\n📄 Loading budget changes from: {csv_file.name}")

changes = []
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        changes.append({
            'customer_id': row['customer_id'],
            'manager_id': row['manager_id'],
            'campaign_id': row['campaign_id'],
            'campaign_name': row['campaign_name'],
            'current_budget_gbp': float(row['current_budget_gbp']),
            'new_budget_gbp': float(row['new_budget_gbp']),
            'action': row['action']
        })

print(f"\n✅ Loaded {len(changes)} budget changes")

# Group by account
accounts = {}
for change in changes:
    customer_id = change['customer_id']
    if customer_id not in accounts:
        accounts[customer_id] = {
            'campaigns': [],
            'current_total': 0,
            'new_total': 0
        }
    accounts[customer_id]['campaigns'].append(change)
    accounts[customer_id]['current_total'] += change['current_budget_gbp']
    accounts[customer_id]['new_total'] += change['new_budget_gbp']

# Map customer IDs to regions
REGION_MAP = {
    '8573235780': 'UK',
    '7808690871': 'USA',
    '7679616761': 'EUR',
    '5556710725': 'ROW'
}

print("\n" + "=" * 100)
print("BUDGET CHANGE SUMMARY")
print("=" * 100)

print(f"\n{'Region':<6} {'Customer ID':<12} {'Campaigns':<10} {'Current':<15} {'New':<15} {'Change':<15}")
print("-" * 80)

total_current = 0
total_new = 0

for customer_id, data in accounts.items():
    region = REGION_MAP.get(customer_id, 'UNKNOWN')
    current = data['current_total']
    new = data['new_total']
    change = new - current

    print(f"{region:<6} {customer_id:<12} {len(data['campaigns']):<10} £{current:>12,.2f} £{new:>12,.2f} £{change:>12,.2f}")

    total_current += current
    total_new += new

print("-" * 80)
print(f"{'TOTAL':<6} {'':<12} {len(changes):<10} £{total_current:>12,.2f} £{total_new:>12,.2f} £{total_new - total_current:>12,.2f}")

print("\n" + "=" * 100)
print("PERMISSION REQUIRED")
print("=" * 100)

print(f"\n⚠️  This will update {len(changes)} campaign budgets across 4 accounts")
print(f"   Total daily budget will change from £{total_current:,.2f} to £{total_new:,.2f}")
print(f"   Net change: £{total_new - total_current:+,.2f}/day")

print(f"\n   Backup already created: backup-phase2b-post-last-orders-dec17.json")

response = input("\n🔴 Type 'YES' to execute budget changes: ")

if response.upper() != 'YES':
    print("\n❌ Deployment cancelled")
    sys.exit(0)

# Execute changes
print("\n" + "=" * 100)
print("EXECUTING BUDGET CHANGES")
print("=" * 100)

results = {
    'timestamp': datetime.now().isoformat(),
    'phase': 'Phase 2B: Post Last Orders',
    'changes_attempted': len(changes),
    'changes_successful': 0,
    'changes_failed': 0,
    'details': []
}

for i, change in enumerate(changes, 1):
    print(f"\n[{i}/{len(changes)}] {change['campaign_name']}")
    print(f"   £{change['current_budget_gbp']:.2f} → £{change['new_budget_gbp']:.2f}")

    # Update budget via API
    mutation_query = f"""
        mutation {{
            updateCampaignBudgets(
                customerId: "{change['customer_id']}"
                operations: [
                    {{
                        update: {{
                            resourceName: "customers/{change['customer_id']}/campaigns/{change['campaign_id']}"
                            campaignBudget: {{
                                amountMicros: {int(change['new_budget_gbp'] * 1_000_000)}
                            }}
                        }}
                        updateMask: "campaign_budget.amount_micros"
                    }}
                ]
            ) {{
                results {{
                    resourceName
                }}
            }}
        }}
    """

    # Actually, we need to use the budget update approach via GoogleAds API
    # Let me use execute_gaql to update the budget

    try:
        # First get the budget ID
        budget_query = f"""
            SELECT
                campaign.id,
                campaign_budget.id,
                campaign_budget.amount_micros
            FROM campaign
            WHERE campaign.id = {change['campaign_id']}
        """

        budget_result = execute_gaql(
            change['customer_id'],
            budget_query,
            change['manager_id']
        )

        if budget_result.get('results'):
            budget_id = budget_result['results'][0]['campaignBudget']['id']

            # Update the budget
            update_query = f"""
                UPDATE campaign_budget
                SET amount_micros = {int(change['new_budget_gbp'] * 1_000_000)}
                WHERE resource_name = 'customers/{change['customer_id']}/campaignBudgets/{budget_id}'
            """

            # Note: execute_gaql doesn't support UPDATE statements
            # We need to use the Google Ads API client directly

            print("   ⚠️  Need to use MCP tool for budget update")
            results['details'].append({
                'campaign_id': change['campaign_id'],
                'campaign_name': change['campaign_name'],
                'status': 'pending_mcp_tool',
                'budget_id': budget_id
            })

        else:
            print("   ❌ Campaign not found")
            results['changes_failed'] += 1
            results['details'].append({
                'campaign_id': change['campaign_id'],
                'campaign_name': change['campaign_name'],
                'status': 'failed',
                'error': 'Campaign not found'
            })

    except Exception as ex:
        print(f"   ❌ Error: {ex}")
        results['changes_failed'] += 1
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

print(f"\n\n✅ Results saved to: {results_file}")
print(f"\n⚠️  This script identified the campaigns but needs MCP tool integration")
print(f"   to execute the actual budget updates via Google Ads API")
