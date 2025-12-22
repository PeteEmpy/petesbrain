#!/usr/bin/env python3
"""
Deploy P9 Dec 22 Minimal Budgets (£2,000 total)
Applies budget changes from p9-dec-22-minimal.csv
"""

import csv
import sys
from pathlib import Path

# Add the shared utilities
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/shared')))

# Import MCP tools via subprocess (Claude Code pattern)
import subprocess
import json

def update_campaign_budget_via_mcp(customer_id, manager_id, campaign_id, new_budget_gbp):
    """Update campaign budget using Google Ads MCP server"""
    # Convert GBP to micros (£1 = 1,000,000 micros)
    budget_micros = int(float(new_budget_gbp) * 1_000_000)

    # Note: In Claude Code context, MCP tools are available directly
    # This script is meant to be run within Claude Code, not standalone
    print(f"  → Would update campaign {campaign_id} to £{new_budget_gbp}")
    print(f"     (Budget micros: {budget_micros})")
    return True

def deploy_budgets_from_csv(csv_path):
    """Read CSV and deploy all budget changes"""

    print("\n" + "=" * 80)
    print("P9 DEC 22 MINIMAL BUDGET DEPLOYMENT")
    print("Target: £2,000 total daily budget")
    print("=" * 80)

    changes = []
    total_new_budget = 0.0

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip comment lines
            if row['customer_id'].startswith('#'):
                print(f"\n{row['customer_id']}")
                continue

            changes.append(row)
            total_new_budget += float(row['new_budget_gbp'])

    print(f"\nTotal changes to deploy: {len(changes)}")
    print(f"Total new daily budget: £{total_new_budget:,.2f}")

    # Group by account
    uk_budget = sum(float(r['new_budget_gbp']) for r in changes if r['customer_id'] == '8573235780')
    usa_budget = sum(float(r['new_budget_gbp']) for r in changes if r['customer_id'] == '7808690871')
    eur_budget = sum(float(r['new_budget_gbp']) for r in changes if r['customer_id'] == '7679616761')
    row_budget = sum(float(r['new_budget_gbp']) for r in changes if r['customer_id'] == '5556710725')

    print(f"\nBreakdown by region:")
    print(f"  UK:  £{uk_budget:,.2f}")
    print(f"  USA: £{usa_budget:,.2f}")
    print(f"  EUR: £{eur_budget:,.2f}")
    print(f"  ROW: £{row_budget:,.2f}")

    print("\n" + "-" * 80)
    print("READY TO DEPLOY")
    print("-" * 80)
    print("\nThis script must be run within Claude Code to access MCP tools.")
    print("The actual API calls will be made via mcp__google-ads__update_campaign_budget")
    print("\nChanges to apply:")

    for i, change in enumerate(changes, 1):
        print(f"\n{i}. {change['campaign_name']}")
        print(f"   Customer: {change['customer_id']}")
        print(f"   Campaign: {change['campaign_id']}")
        print(f"   Current: £{change['current_budget_gbp']} → New: £{change['new_budget_gbp']}")
        print(f"   Note: {change['notes']}")

    return changes

if __name__ == '__main__':
    csv_path = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/spreadsheets/p9-dec-22-minimal.csv')

    if not csv_path.exists():
        print(f"ERROR: CSV file not found: {csv_path}")
        sys.exit(1)

    changes = deploy_budgets_from_csv(csv_path)

    print("\n" + "=" * 80)
    print("DEPLOYMENT COMPLETE (DRY RUN)")
    print("=" * 80)
    print("\nTo actually deploy these changes, run this via Claude Code")
    print("and Claude will make the MCP tool calls.")
