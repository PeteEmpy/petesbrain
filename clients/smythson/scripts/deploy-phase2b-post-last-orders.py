#!/usr/bin/env python3
"""
Smythson P9 Phase 2B: Post Last Orders Budget Deployment (Dec 17-22)
Deploy after last orders close midnight 16th December

CRITICAL: Last orders closed for US/EUR/ROW at 11:59pm GMT on Dec 16th
- Reduce US/EUR/ROW to 70% of Phase 2A levels
- Reallocate saved budget to UK for final Christmas push
- No campaigns paused - all continue running at adjusted levels

FOLLOWS: Google Ads Change Protection Protocol
1. Load Phase 2A current state
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

# Phase 2B Target Daily Budgets (Post Last Orders)
PHASE_2B_TARGETS = {
    'UK': 3857,    # +£807 from reallocation (26% increase)
    'USA': 1208,   # 70% of Phase 2A (£1,725)
    'EUR': 483,    # 70% of Phase 2A (£690)
    'ROW': 202     # 70% of Phase 2A (£288)
}

# Phase 2A budgets (for reference)
PHASE_2A_BUDGETS = {
    'UK': 3050,
    'USA': 1725,
    'EUR': 690,
    'ROW': 288
}

print("=" * 100)
print("SMYTHSON P9 - PHASE 2B: POST LAST ORDERS BUDGET DEPLOYMENT")
print("Last Orders Closed: 11:59pm GMT Dec 16th (US/EUR/ROW)")
print("Deploy Date: Wednesday 17th December 2025, 8am")
print("Duration: Dec 17-22 (6 days)")
print("=" * 100)

print("\n📋 STRATEGY:")
print("   - Last orders CLOSED for US/EUR/ROW at midnight Dec 16th")
print("   - Reduce US/EUR/ROW to 70% of Last Order Week levels")
print("   - Reallocate saved budget (£810/day) to UK")
print("   - UK receives £807/day boost for final Christmas push")
print("   - NO campaigns paused - all continue at adjusted levels")

# Step 1: Load Current State from Phase 2A
print("\n" + "=" * 100)
print("STEP 1: LOADING CURRENT STATE FROM PHASE 2A")
print("=" * 100)

# Check if Phase 2A backup exists
phase_2a_backup = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports/backup-phase2a-last-order-period.json')

if phase_2a_backup.exists():
    print(f"\n✅ Found Phase 2A backup: {phase_2a_backup}")
    with open(phase_2a_backup, 'r') as f:
        phase_2a_data = json.load(f)
    print(f"   Created: {phase_2a_data.get('timestamp', 'Unknown')}")
else:
    print(f"\n⚠️  Phase 2A backup not found: {phase_2a_backup}")
    print("   Will query current state from Google Ads")
    phase_2a_data = None

# Query current state
print("\n" + "=" * 100)
print("STEP 2: QUERYING CURRENT BUDGET STATE")
print("=" * 100)

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
            'phase_2a_budget': PHASE_2A_BUDGETS[region],
            'phase_2b_target': PHASE_2B_TARGETS[region]
        }

        print(f"  Phase 2A Budget:      £{PHASE_2A_BUDGETS[region]:,.2f}")
        print(f"  Current Daily Budget: £{total_daily_budget:,.2f}")
        print(f"  Phase 2B Target:      £{PHASE_2B_TARGETS[region]:,.2f}")
        print(f"  Change Required:      £{PHASE_2B_TARGETS[region] - total_daily_budget:+,.2f}")
        print(f"  Campaigns Found:      {len(campaigns)}")

    except Exception as ex:
        print(f"  ERROR: {ex}")
        current_state[region] = {'error': str(ex)}

# Step 2: Create Backup
print("\n" + "=" * 100)
print("STEP 3: CREATING BACKUP")
print("=" * 100)

backup_file = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports/backup-phase2b-post-last-orders-dec17.json')

backup_data = {
    'timestamp': datetime.now().isoformat(),
    'phase': 'Phase 2B: Post Last Orders (Dec 17-22)',
    'deploy_date': '2025-12-17 08:00:00',
    'last_orders_closed': '2025-12-16 23:59:00 GMT (US/EUR/ROW)',
    'current_state': current_state,
    'phase_2a_budgets': PHASE_2A_BUDGETS,
    'phase_2b_targets': PHASE_2B_TARGETS,
    'strategy': {
        'us_eur_row_reduction': '30% reduction (to 70% of Phase 2A)',
        'uk_boost': '+£807/day (26% increase from reallocation)',
        'total_daily_maintained': '£5,750/day',
        'rationale': 'Last orders closed for international markets; reallocate to UK for final Christmas push'
    }
}

backup_file.parent.mkdir(parents=True, exist_ok=True)

with open(backup_file, 'w') as f:
    json.dump(backup_data, f, indent=2)

print(f"\n✅ Backup created: {backup_file}")
print(f"   Timestamp: {backup_data['timestamp']}")

# Step 3: Calculate Budget Changes Needed
print("\n" + "=" * 100)
print("STEP 4: BUDGET CHANGE PLAN")
print("=" * 100)

print("\n🔄 POST LAST ORDERS REALLOCATION:")
print(f"{'Account':<6} {'Phase 2A':<12} {'Phase 2B':<12} {'Change':<12} {'% Change':<10} {'Strategy':<30}")
print("-" * 90)

total_phase_2a = 0
total_phase_2b = 0

for region in ['UK', 'USA', 'EUR', 'ROW']:
    if region in current_state and 'error' not in current_state[region]:
        phase_2a = PHASE_2A_BUDGETS[region]
        phase_2b = PHASE_2B_TARGETS[region]
        change = phase_2b - phase_2a
        pct_change = (change / phase_2a * 100) if phase_2a > 0 else 0

        if region == 'UK':
            strategy = "BOOST (receives reallocation)"
        else:
            strategy = "REDUCE (last orders closed)"

        print(f"{region:<6} £{phase_2a:>10,.2f} £{phase_2b:>10,.2f} £{change:>10,.2f} {pct_change:>8.1f}% {strategy:<30}")

        total_phase_2a += phase_2a
        total_phase_2b += phase_2b

print("-" * 90)
print(f"{'TOTAL':<6} £{total_phase_2a:>10,.2f} £{total_phase_2b:>10,.2f} £{total_phase_2b - total_phase_2a:>10,.2f} {((total_phase_2b - total_phase_2a) / total_phase_2a * 100):>8.1f}%")

print("\n💡 BUDGET REALLOCATION BREAKDOWN:")
print(f"   US/EUR/ROW reduction saves: £{(PHASE_2A_BUDGETS['USA'] - PHASE_2B_TARGETS['USA']) + (PHASE_2A_BUDGETS['EUR'] - PHASE_2B_TARGETS['EUR']) + (PHASE_2A_BUDGETS['ROW'] - PHASE_2B_TARGETS['ROW']):,.2f}/day")
print(f"   UK receives additional:      £{PHASE_2B_TARGETS['UK'] - PHASE_2A_BUDGETS['UK']:,.2f}/day")
print(f"   Total daily budget:          £{total_phase_2b:,.2f}/day (maintained)")

# Step 4: Wait for Permission
print("\n" + "=" * 100)
print("STEP 5: PERMISSION REQUIRED")
print("=" * 100)

print("\n⚠️  PHASE 2B BUDGET CHANGES READY TO DEPLOY")
print(f"\nBackup saved to: {backup_file}")
print(f"\nChanges will affect {sum(len(s.get('campaigns', [])) for s in current_state.values() if 'error' not in s)} campaigns across 4 accounts")
print(f"\nRationale: Last orders closed for US/EUR/ROW at midnight Dec 16th")
print(f"           Reducing international budgets to 70%, reallocating to UK")

response = input("\n🔴 Type 'YES' to proceed with Phase 2B budget deployment: ")

if response.upper() != 'YES':
    print("\n❌ Deployment cancelled by user")
    sys.exit(0)

# Step 5: Execute Changes (placeholder - actual implementation needed)
print("\n" + "=" * 100)
print("STEP 6: EXECUTING BUDGET CHANGES")
print("=" * 100)

print("\n⚠️  IMPLEMENTATION NOTE:")
print("This script currently shows the plan and creates backups.")
print("Actual budget update implementation requires:")
print("1. Performance-based allocation logic from Phase 2A")
print("2. Apply 70% reduction to US/EUR/ROW campaigns")
print("3. Apply proportional increase to UK campaigns")
print("4. Google Ads API budget update calls")
print("5. Verification of changes")

print("\n📊 RECOMMENDED APPROACH:")
print("Option 1: Uniform percentage changes")
print("  - Reduce ALL US/EUR/ROW campaigns by 30%")
print("  - Increase ALL UK campaigns proportionally to absorb £807/day")
print("")
print("Option 2: Performance-weighted changes")
print("  - Use Phase 2A performance weights")
print("  - Reduce weaker international campaigns more aggressively")
print("  - Boost stronger UK campaigns more")

print("\n" + "=" * 100)
print("PHASE 2B DEPLOYMENT PLAN COMPLETE")
print("=" * 100)

print("\n✅ Next steps:")
print("1. Review backup file for accuracy")
print("2. Choose allocation approach (uniform vs performance-weighted)")
print("3. Implement campaign-level budget updates")
print("4. Execute budget updates via Google Ads API")
print("5. Verify actual changes match targets")
print("6. Monitor ROAS impact over 24-48 hours")
print("7. Confirm UK benefits from increased budget")
print("8. Verify US/EUR/ROW maintain acceptable performance at 70%")

print(f"\nBackup location: {backup_file}")
print(f"Target deployment: Wednesday Dec 17, 8am")
print(f"Duration: 6 days (Dec 17-22)")
print(f"Total budget: £34,500 (£5,750/day × 6 days)")
