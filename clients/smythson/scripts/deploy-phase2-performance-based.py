#!/usr/bin/env python3
"""
Smythson P9 Phase 2: Last Order Week Budget Deployment (Dec 15-22)
Performance-based allocation using December 2024 ROAS weights

CRITICAL: Follows Google Ads Change Protection Protocol
1. Load calculated allocations
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
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-ads-mcp-server'))
from oauth.google_auth import execute_gaql

# Account details
ACCOUNTS = {
    'UK': '8573235780',
    'USA': '7808690871',
    'EUR': '7679616761',
    'ROW': '5556710725'
}
MANAGER_ID = '2569949686'

print("=" * 100)
print("SMYTHSON P9 - PHASE 2: LAST ORDER WEEK BUDGET DEPLOYMENT")
print("Performance-Based Allocation (December 2024 ROAS Weights)")
print("Deploy Date: Monday 15th December 2025, 3pm")
print("Duration: Dec 15-22 (8 days)")
print("=" * 100)

# Step 1: Load Calculated Allocations
print("\n" + "=" * 100)
print("STEP 1: LOADING CALCULATED ALLOCATIONS")
print("=" * 100)

allocation_file = Path('/tmp/phase2-performance-allocation-dec15.json')

if not allocation_file.exists():
    print(f"\n❌ ERROR: Allocation file not found: {allocation_file}")
    print("Run apply_performance_allocation_phase2.py first to generate allocations")
    sys.exit(1)

with open(allocation_file, 'r') as f:
    allocations = json.load(f)

print(f"\n✅ Loaded allocations from: {allocation_file}")

# Display summary
print(f"\n{'Account':<10} {'Campaigns':<12} {'Current':<12} {'Target':<12} {'Change':<12}")
print("-" * 60)

for region in ['UK', 'USA', 'EUR', 'ROW']:
    if region in allocations and 'error' not in allocations[region]:
        campaigns = allocations[region]
        enabled = [c for c in campaigns if c['status'] == 'ENABLED']
        current = sum(c['current_budget'] for c in enabled)
        target = sum(c['new_budget'] for c in campaigns)
        change = target - current

        print(f"{region:<10} {len(campaigns):>10} £{current:>10,.2f} £{target:>10,.2f} £{change:>10,.2f}")

# Step 2: Create Backup
print("\n" + "=" * 100)
print("STEP 2: CREATING BACKUP")
print("=" * 100)

backup_dir = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports')
backup_file = backup_dir / 'backup-phase2-performance-based-dec15.json'

backup_data = {
    'timestamp': datetime.now().isoformat(),
    'phase': 'Phase 2: Last Order Week (Dec 15-22)',
    'deploy_date': '2025-12-15 15:00:00',
    'allocation_method': 'Performance-based (December 2024 ROAS weights)',
    'allocations': allocations
}

backup_dir.mkdir(parents=True, exist_ok=True)

with open(backup_file, 'w') as f:
    json.dump(backup_data, f, indent=2)

print(f"\n✅ Backup created: {backup_file}")
print(f"   Timestamp: {backup_data['timestamp']}")

# Step 3: Show Changes for Each Account
print("\n" + "=" * 100)
print("STEP 3: BUDGET CHANGES BY ACCOUNT")
print("=" * 100)

total_changes = 0

for region in ['UK', 'USA', 'EUR', 'ROW']:
    if region not in allocations or 'error' in allocations[region]:
        print(f"\n{region}: SKIPPED - {allocations.get(region, {}).get('error', 'No data')}")
        continue

    campaigns = allocations[region]
    enabled = [c for c in campaigns if c['status'] == 'ENABLED']

    # Only show enabled campaigns with budget changes
    changes = [c for c in enabled if abs(c['budget_change']) > 0.01]

    if not changes:
        print(f"\n{region}: No budget changes needed (already at target)")
        continue

    print(f"\n{region} Account - {len(changes)} budget changes:")
    print(f"{'Campaign':<60} {'Current':<10} {'New':<10} {'Change':<10} {'%':<8}")
    print("-" * 100)

    # Sort by absolute change (biggest first)
    changes.sort(key=lambda x: abs(x['budget_change']), reverse=True)

    for camp in changes[:20]:  # Show top 20 changes
        print(f"{camp['name'][:58]:<60} £{camp['current_budget']:>8,.0f} £{camp['new_budget']:>8,.0f} £{camp['budget_change']:>8,.0f} {camp['pct_change']:>6.1f}%")

    if len(changes) > 20:
        print(f"... and {len(changes) - 20} more changes")

    total_changes += len(changes)

# Step 4: Wait for Permission
print("\n" + "=" * 100)
print("STEP 4: PERMISSION REQUIRED")
print("=" * 100)

print(f"\n⚠️  READY TO DEPLOY {total_changes} BUDGET CHANGES")
print(f"\nBackup saved to: {backup_file}")
print(f"\nThis will update campaign budgets across all 4 Smythson accounts")
print(f"Allocation method: Performance-based (December 2024 ROAS weights)")

response = input("\n🔴 Type 'YES' to proceed with budget deployment: ")

if response.upper() != 'YES':
    print("\n❌ Deployment cancelled by user")
    sys.exit(0)

# Step 5: Execute Changes
print("\n" + "=" * 100)
print("STEP 5: EXECUTING BUDGET CHANGES")
print("=" * 100)

print("\n⚠️  IMPLEMENTATION REQUIRED:")
print("This script shows the plan and creates backups.")
print("\nTo execute actual budget changes, use Google Ads MCP server:")
print("  mcp__google-ads__update_campaign_budget()")
print("\nFor each campaign with budget change:")
print("  1. Get campaign_id and budget_id from allocation data")
print("  2. Call update_campaign_budget with new amount_micros")
print("  3. Verify change was applied")
print("  4. Log any errors")

print("\n" + "=" * 100)
print("NEXT STEPS")
print("=" * 100)

print("\n1. Review backup file for accuracy")
print("2. Implement budget update API calls")
print("3. Execute updates sequentially with verification")
print("4. Monitor ROAS impact over 24-48 hours")
print("5. Refine in January based on actual 2025 campaign performance")

print(f"\nBackup location: {backup_file}")
print(f"Allocation data: {allocation_file}")
print(f"\nTarget deployment: Monday Dec 15, 3pm (after Alex approval)")

# Save execution log
log_file = backup_dir / 'deployment-log-phase2-dec15.txt'
with open(log_file, 'w') as f:
    f.write(f"Phase 2 Deployment Plan - {datetime.now().isoformat()}\n")
    f.write("=" * 100 + "\n\n")
    f.write(f"Backup: {backup_file}\n")
    f.write(f"Allocations: {allocation_file}\n")
    f.write(f"Total changes: {total_changes}\n")
    f.write(f"Status: Ready for implementation\n")

print(f"\n📝 Deployment log saved: {log_file}")
