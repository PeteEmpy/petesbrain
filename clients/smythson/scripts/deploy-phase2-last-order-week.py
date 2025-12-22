#!/usr/bin/env python3
"""
Smythson P9 Phase 2: Last Order Week Budget Deployment (Dec 15-22)
Deploy after Alex approval (planned 3pm Dec 15)

CRITICAL: Follows Google Ads Change Protection Protocol
1. Query current state
2. Create backup
3. Wait for permission
4. Execute changes
5. Verify results
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add MCP integration
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server')))
from oauth.google_auth import execute_gaql

# Account details
ACCOUNTS = {
    'UK': '8573235780',
    'USA': '7808690871',
    'EUR': '7679616761',
    'ROW': '5556710725'
}
MANAGER_ID = '2569949686'

# Phase 2 Target Daily Budgets (in GBP)
PHASE_2_TARGETS = {
    'UK': 3050,
    'USA': 1725,
    'EUR': 690,
    'ROW': 288
}

print("=" * 80)
print("SMYTHSON P9 - PHASE 2: LAST ORDER WEEK BUDGET DEPLOYMENT")
print("Deploy Date: Monday 15th December 2025, 3pm")
print("Duration: Dec 15-22 (8 days)")
print("Total Phase Budget: £46,000 (£5,750/day)")
print("=" * 80)

# Step 1: Query Current State
print("\n" + "=" * 80)
print("STEP 1: QUERYING CURRENT BUDGET STATE")
print("=" * 80)

current_state = {}

for region, customer_id in ACCOUNTS.items():
    print(f"\n{region} Account ({customer_id}):")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign_budget.id,
            campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.status IN ('ENABLED', 'PAUSED')
        ORDER BY campaign.name
    """

    try:
        result = execute_gaql(customer_id, query, MANAGER_ID)

        campaigns = []
        total_daily_budget = 0

        for row in result.get('results', []):
            campaign = row.get('campaign', {})
            budget = row.get('campaignBudget', {})

            campaign_id = campaign.get('id', '')
            campaign_name = campaign.get('name', '')
            status = campaign.get('status', '')
            budget_id = budget.get('id', '')
            budget_micros = int(budget.get('amountMicros', 0))
            budget_gbp = budget_micros / 1_000_000

            campaigns.append({
                'campaign_id': campaign_id,
                'campaign_name': campaign_name,
                'status': status,
                'budget_id': budget_id,
                'current_budget_gbp': budget_gbp,
                'current_budget_micros': budget_micros
            })

            if status == 'ENABLED':
                total_daily_budget += budget_gbp

        current_state[region] = {
            'customer_id': customer_id,
            'campaigns': campaigns,
            'total_daily_budget': total_daily_budget,
            'target_daily_budget': PHASE_2_TARGETS[region]
        }

        print(f"  Current Daily Budget: £{total_daily_budget:,.2f}")
        print(f"  Target Daily Budget:  £{PHASE_2_TARGETS[region]:,.2f}")
        print(f"  Change Required:      £{PHASE_2_TARGETS[region] - total_daily_budget:+,.2f}")
        print(f"  Campaigns Found:      {len(campaigns)}")

    except Exception as ex:
        print(f"  ERROR: {ex}")
        current_state[region] = {'error': str(ex)}

# Step 2: Create Backup
print("\n" + "=" * 80)
print("STEP 2: CREATING BACKUP")
print("=" * 80)

backup_file = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports/backup-phase2-last-order-week-dec15.json')

backup_data = {
    'timestamp': datetime.now().isoformat(),
    'phase': 'Phase 2: Last Order Week (Dec 15-22)',
    'deploy_date': '2025-12-15 15:00:00',
    'current_state': current_state,
    'target_budgets': PHASE_2_TARGETS
}

backup_file.parent.mkdir(parents=True, exist_ok=True)

with open(backup_file, 'w') as f:
    json.dump(backup_data, f, indent=2)

print(f"\n✅ Backup created: {backup_file}")
print(f"   Timestamp: {backup_data['timestamp']}")

# Step 3: Calculate Budget Changes Needed
print("\n" + "=" * 80)
print("STEP 3: BUDGET CHANGE PLAN")
print("=" * 80)

print("\nTarget Daily Budgets by Account:")
print(f"{'Account':<6} {'Current':<12} {'Target':<12} {'Change':<12} {'% Change':<10}")
print("-" * 60)

total_current = 0
total_target = 0

for region in ['UK', 'USA', 'EUR', 'ROW']:
    if region in current_state and 'error' not in current_state[region]:
        current = current_state[region]['total_daily_budget']
        target = PHASE_2_TARGETS[region]
        change = target - current
        pct_change = (change / current * 100) if current > 0 else 0

        print(f"{region:<6} £{current:>10,.2f} £{target:>10,.2f} £{change:>10,.2f} {pct_change:>8.1f}%")

        total_current += current
        total_target += target

print("-" * 60)
print(f"{'TOTAL':<6} £{total_current:>10,.2f} £{total_target:>10,.2f} £{total_target - total_current:>10,.2f} {((total_target - total_current) / total_current * 100):>8.1f}%")

# Step 4: Wait for Permission
print("\n" + "=" * 80)
print("STEP 4: PERMISSION REQUIRED")
print("=" * 80)

print("\n⚠️  BUDGET CHANGES READY TO DEPLOY")
print(f"\nBackup saved to: {backup_file}")
print(f"\nChanges will affect {sum(len(s.get('campaigns', [])) for s in current_state.values() if 'error' not in s)} campaigns across 4 accounts")
print(f"\nTotal daily budget: £{total_current:,.2f} → £{total_target:,.2f} ({((total_target - total_current) / total_current * 100):+.1f}%)")

response = input("\n🔴 Type 'YES' to proceed with budget deployment: ")

if response.upper() != 'YES':
    print("\n❌ Deployment cancelled by user")
    sys.exit(0)

# Step 5: Execute Changes (placeholder - actual implementation needed)
print("\n" + "=" * 80)
print("STEP 5: EXECUTING BUDGET CHANGES")
print("=" * 80)

print("\n⚠️  IMPLEMENTATION NOTE:")
print("This script currently shows the plan and creates backups.")
print("Actual budget update implementation requires:")
print("1. Campaign-level budget allocation logic")
print("2. Google Ads API budget update calls")
print("3. Smart Bidding consideration for budget changes")
print("\nRecommended approach:")
print("- Query each account's campaigns")
print("- Identify which campaigns to scale up/down")
print("- Apply proportional changes to reach target daily total")
print("- Use mcp__google-ads__update_campaign_budget() for each change")

print("\n" + "=" * 80)
print("PHASE 2 DEPLOYMENT PLAN COMPLETE")
print("=" * 80)

print("\nNext steps:")
print("1. Review backup file for accuracy")
print("2. Implement campaign-level budget allocation")
print("3. Execute budget updates via Google Ads API")
print("4. Verify actual spend matches targets over 24-48 hours")
print("5. Monitor ROAS impact of budget changes")

print(f"\nBackup location: {backup_file}")
print(f"Target deployment: Monday Dec 15, 3pm (after Alex approval)")
