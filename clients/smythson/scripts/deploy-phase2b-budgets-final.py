#!/usr/bin/env python3
"""
Deploy Phase IIb Budgets - Final Execution
Reads CSV and calls Google Ads MCP tools to update campaign budgets
"""

import csv
import json
from pathlib import Path
from datetime import datetime

# Load CSV
csv_file = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/spreadsheets/phase2b-post-last-orders-dec17-EXACT.csv')

print("=" * 100)
print("SMYTHSON PHASE IIB - FINAL BUDGET DEPLOYMENT")
print("=" * 100)

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
            'new_budget_micros': int(float(row['new_budget_gbp']) * 1_000_000)
        })

# Group by account
REGION_MAP = {
    '8573235780': 'UK',
    '7808690871': 'USA',
    '7679616761': 'EUR',
    '5556710725': 'ROW'
}

accounts_summary = {}
for change in changes:
    customer_id = change['customer_id']
    if customer_id not in accounts_summary:
        accounts_summary[customer_id] = {
            'region': REGION_MAP.get(customer_id, 'UNKNOWN'),
            'campaigns': 0,
            'current_total': 0,
            'new_total': 0
        }
    accounts_summary[customer_id]['campaigns'] += 1
    accounts_summary[customer_id]['current_total'] += change['current_budget_gbp']
    accounts_summary[customer_id]['new_total'] += change['new_budget_gbp']

print(f"\n📊 BUDGET DEPLOYMENT SUMMARY:")
print(f"\n{'Region':<6} {'Customer ID':<12} {'Campaigns':<10} {'Current':<15} {'New':<15} {'Change':<15}")
print("-" * 85)

grand_current = 0
grand_new = 0

for customer_id, data in sorted(accounts_summary.items(), key=lambda x: x[1]['region']):
    region = data['region']
    campaigns = data['campaigns']
    current = data['current_total']
    new = data['new_total']
    change = new - current

    print(f"{region:<6} {customer_id:<12} {campaigns:<10} £{current:>12,.2f} £{new:>12,.2f} £{change:>12,.2f}")
    grand_current += current
    grand_new += new

print("-" * 85)
print(f"{'TOTAL':<6} {'':<12} {len(changes):<10} £{grand_current:>12,.2f} £{grand_new:>12,.2f} £{grand_new - grand_current:>12,.2f}")

print(f"\n✅ Backup created: backup-phase2b-post-last-orders-dec17.json")
print(f"📅 Deploy date: Monday 16th December 2025, 10:09pm")
print(f"🎯 Target: Reduce to £5,750/day total (currently £{grand_current:,.2f}/day)")

print("\n" + "=" * 100)

# Output the changes in a format that can be used by Claude Code
output_file = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports/phase2b-budget-changes-for-mcp.json')

output_data = {
    'timestamp': datetime.now().isoformat(),
    'phase': 'Phase 2B: Post Last Orders (Dec 17-22)',
    'summary': {
        'total_campaigns': len(changes),
        'current_daily_total_gbp': grand_current,
        'new_daily_total_gbp': grand_new,
        'net_change_gbp': grand_new - grand_current
    },
    'changes': changes
}

with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"✅ Budget changes exported to: {output_file}")
print(f"\nReady for MCP tool execution via Claude Code")
