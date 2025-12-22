#!/usr/bin/env python3
"""
Universal Budget Deployer
=========================

Deploys Google Ads budget changes from CSV for ANY client.

Usage:
    python deploy.py --client smythson --csv budgets.csv --dry-run
    python deploy.py --client smythson --csv budgets.csv --execute

Features:
- Change Protection Protocol (Backup → Permission → Execute → Verify → Rollback)
- Works for all clients
- Multi-account support
- Dry-run mode
- Audit trail logging

CSV Format:
-----------
customer_id,manager_id,campaign_id,campaign_name,current_budget_gbp,new_budget_gbp,action
8573235780,2569949686,8161289137,Brand Search | UK | Main,323.48,823.48,BUDGET_CHANGE
8573235780,2569949686,8166587577,Competitor Search | UK | Main,50.00,0.00,PAUSE

Actions:
- BUDGET_CHANGE: Update campaign budget
- PAUSE: Pause campaign (set status to PAUSED)
- ENABLE: Enable campaign (set status to ENABLED)
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class BudgetDeployer:
    def __init__(self, client: str, csv_file: Path, dry_run: bool = True):
        self.client = client
        self.csv_file = csv_file
        self.dry_run = dry_run
        self.changes = []
        self.backup_file = None

    def load_changes(self) -> List[Dict]:
        """Load budget changes from CSV"""
        print(f"\n📄 Loading changes from {self.csv_file}...\n")

        changes = []
        with open(self.csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                change = {
                    'customer_id': row['customer_id'].strip(),
                    'manager_id': row.get('manager_id', '').strip() or None,
                    'campaign_id': row['campaign_id'].strip(),
                    'campaign_name': row['campaign_name'].strip(),
                    'current_budget_gbp': float(row['current_budget_gbp']),
                    'new_budget_gbp': float(row['new_budget_gbp']),
                    'action': row.get('action', 'BUDGET_CHANGE').strip().upper(),
                    'current_budget_micros': int(float(row['current_budget_gbp']) * 1_000_000),
                    'new_budget_micros': int(float(row['new_budget_gbp']) * 1_000_000)
                }
                changes.append(change)

        self.changes = changes
        print(f"✓ Loaded {len(changes)} changes\n")
        return changes

    def print_summary(self):
        """Print summary of all changes"""
        print("=" * 100)
        print(f"BUDGET DEPLOYMENT SUMMARY - {self.client.upper()}")
        print("=" * 100)
        print(f"Mode: {'DRY RUN (preview only)' if self.dry_run else 'EXECUTE (will make changes)'}")
        print(f"Total changes: {len(self.changes)}")
        print("=" * 100)

        # Group by customer ID
        by_account = {}
        for change in self.changes:
            cid = change['customer_id']
            if cid not in by_account:
                by_account[cid] = []
            by_account[cid].append(change)

        total_current = 0
        total_new = 0
        budget_changes = 0
        pauses = 0
        enables = 0

        for customer_id, account_changes in by_account.items():
            print(f"\nAccount {customer_id}:")
            print("-" * 100)

            for change in account_changes:
                action = change['action']
                name = change['campaign_name']

                if action == 'BUDGET_CHANGE':
                    current = change['current_budget_gbp']
                    new = change['new_budget_gbp']
                    diff = new - current

                    total_current += current
                    total_new += new
                    budget_changes += 1

                    symbol = "↑" if diff > 0 else "↓" if diff < 0 else "="
                    print(f"  {symbol} {name}")
                    print(f"     £{current:,.2f}/day → £{new:,.2f}/day ({diff:+,.2f})")

                elif action == 'PAUSE':
                    pauses += 1
                    print(f"  ❌ PAUSE: {name}")

                elif action == 'ENABLE':
                    enables += 1
                    print(f"  ✅ ENABLE: {name}")

        print("\n" + "=" * 100)
        print("TOTALS")
        print("=" * 100)
        print(f"Budget changes: {budget_changes}")
        print(f"Campaigns to pause: {pauses}")
        print(f"Campaigns to enable: {enables}")

        if budget_changes > 0:
            print(f"\nTotal daily budget:")
            print(f"  Current: £{total_current:,.2f}")
            print(f"  New:     £{total_new:,.2f}")
            print(f"  Change:  £{total_new - total_current:+,.2f}")

        print("=" * 100)

    def create_backup(self) -> Path:
        """Create backup JSON with expected before/after values"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_dir = Path(f"/Users/administrator/Documents/PetesBrain.nosync/clients/{self.client}/reports")
        backup_dir.mkdir(parents=True, exist_ok=True)

        backup_file = backup_dir / f"budget-deployment-backup-{timestamp}.json"

        backup_data = {
            'timestamp': timestamp,
            'client': self.client,
            'csv_file': str(self.csv_file),
            'mode': 'DRY_RUN' if self.dry_run else 'EXECUTE',
            'accounts': {}
        }

        # Group by customer ID
        for change in self.changes:
            cid = change['customer_id']

            if cid not in backup_data['accounts']:
                backup_data['accounts'][cid] = {
                    'customer_id': cid,
                    'manager_id': change['manager_id'],
                    'campaigns': {}
                }

            backup_data['accounts'][cid]['campaigns'][change['campaign_id']] = {
                'campaign_name': change['campaign_name'],
                'action': change['action'],
                'expected_before': {
                    'budget_gbp': change['current_budget_gbp'],
                    'budget_micros': change['current_budget_micros']
                },
                'expected_after': {
                    'budget_gbp': change['new_budget_gbp'],
                    'budget_micros': change['new_budget_micros']
                }
            }

        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)

        self.backup_file = backup_file
        print(f"\n✓ Backup created: {backup_file}\n")
        return backup_file

    def generate_mcp_commands(self) -> List[Dict]:
        """Generate MCP command calls for execution"""
        print("\n" + "=" * 100)
        print("MCP COMMANDS TO EXECUTE")
        print("=" * 100)

        commands = []

        for change in self.changes:
            customer_id = change['customer_id']
            manager_id = change['manager_id']
            campaign_id = change['campaign_id']
            action = change['action']

            if action == 'BUDGET_CHANGE':
                cmd = {
                    'tool': 'mcp__google_ads__update_campaign_budget',
                    'params': {
                        'customer_id': customer_id,
                        'manager_id': manager_id,
                        'campaign_id': campaign_id,
                        'daily_budget_micros': change['new_budget_micros']
                    },
                    'description': f"{change['campaign_name']}: £{change['current_budget_gbp']:.2f} → £{change['new_budget_gbp']:.2f}"
                }
                commands.append(cmd)

                print(f"\n📊 {change['campaign_name']}")
                print(f"   £{change['current_budget_gbp']:,.2f}/day → £{change['new_budget_gbp']:,.2f}/day")
                print(f"   mcp__google_ads__update_campaign_budget(")
                print(f"       customer_id='{customer_id}',")
                if manager_id:
                    print(f"       manager_id='{manager_id}',")
                print(f"       campaign_id='{campaign_id}',")
                print(f"       daily_budget_micros={change['new_budget_micros']}")
                print(f"   )")

            elif action in ['PAUSE', 'ENABLE']:
                status = 'PAUSED' if action == 'PAUSE' else 'ENABLED'
                cmd = {
                    'tool': 'mcp__google_ads__update_campaign_status',
                    'params': {
                        'customer_id': customer_id,
                        'manager_id': manager_id,
                        'campaign_id': campaign_id,
                        'status': status
                    },
                    'description': f"{change['campaign_name']}: {action}"
                }
                commands.append(cmd)

                emoji = "❌" if action == 'PAUSE' else "✅"
                print(f"\n{emoji} {change['campaign_name']}")
                print(f"   mcp__google_ads__update_campaign_status(")
                print(f"       customer_id='{customer_id}',")
                if manager_id:
                    print(f"       manager_id='{manager_id}',")
                print(f"       campaign_id='{campaign_id}',")
                print(f"       status='{status}'")
                print(f"   )")

        print("\n" + "=" * 100)
        print(f"Total MCP commands: {len(commands)}")
        print("=" * 100)

        return commands

    def run(self):
        """Execute the deployment workflow"""
        print("\n" + "🚀" * 50)
        print("UNIVERSAL BUDGET DEPLOYER")
        print("🚀" * 50)

        # Step 1: Load changes
        self.load_changes()

        # Step 2: Print summary
        self.print_summary()

        # Step 3: Create backup
        self.create_backup()

        # Step 4: Generate MCP commands
        commands = self.generate_mcp_commands()

        # Step 5: Instructions
        print("\n" + "=" * 100)
        print("NEXT STEPS")
        print("=" * 100)

        if self.dry_run:
            print("✓ Dry-run complete - no changes made")
            print(f"✓ Backup created: {self.backup_file}")
            print(f"✓ {len(commands)} commands ready to execute")
            print("\nTo execute these changes:")
            print(f"  python deploy.py --client {self.client} --csv {self.csv_file} --execute")
        else:
            print("⚠️  EXECUTE MODE")
            print(f"✓ Backup created: {self.backup_file}")
            print(f"✓ {len(commands)} commands generated")
            print("\n⚠️  This script generates the commands but DOES NOT execute them.")
            print("   You must use Claude Code to execute MCP commands with Change Protection Protocol.")
            print("\nIn Claude Code, say:")
            print(f'  "Execute the budget deployment from {self.backup_file}"')

        print("=" * 100)

        return commands


def main():
    parser = argparse.ArgumentParser(description='Universal Budget Deployer')
    parser.add_argument('--client', required=True, help='Client name (e.g., smythson)')
    parser.add_argument('--csv', required=True, help='Path to CSV file with budget changes')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without executing')
    parser.add_argument('--execute', action='store_true', help='Generate execution commands')

    args = parser.parse_args()

    # Validate arguments
    if not args.dry_run and not args.execute:
        print("❌ Error: Must specify either --dry-run or --execute")
        sys.exit(1)

    if args.dry_run and args.execute:
        print("❌ Error: Cannot specify both --dry-run and --execute")
        sys.exit(1)

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"❌ Error: CSV file not found: {csv_path}")
        sys.exit(1)

    # Run deployment
    deployer = BudgetDeployer(
        client=args.client,
        csv_file=csv_path,
        dry_run=args.dry_run
    )

    commands = deployer.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
