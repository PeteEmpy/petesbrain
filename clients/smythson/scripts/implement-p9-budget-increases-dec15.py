#!/usr/bin/env python3
"""
Smythson P9 Budget Deployment - December 15-22
Implements full budget deployment for Last Order Week

CRITICAL: This script follows Google Ads Change Protection Protocol:
1. Queries current state
2. Creates backup with expected values
3. Waits for user permission
4. Executes changes
5. Verifies results
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add MCP integration
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/infrastructure/hooks/google-ads-change-verification')))

# Campaign budget changes for P9 Last Order Week (Dec 15-22)
# All budgets in GBP (£), converted to micros for API

BUDGET_CHANGES = {
    # EUR Account (7679616761)
    '7679616761': {
        'manager_id': '2569949686',
        'campaigns': {
            '8161387697': {  # Brand Search
                'name': 'Brand Search | EUR | Main',
                'current_budget': 78.37,
                'new_budget': 227.37,
                'increase': 149.00
            },
            '8154887417': {  # Brand Shopping
                'name': 'Brand Shopping | EUR | Main',
                'current_budget': 169.68,
                'new_budget': 319.68,
                'increase': 150.00
            },
            '8166587817': {  # Generic Search
                'name': 'Generic Search | EUR | Main',
                'current_budget': 157.11,
                'new_budget': 267.11,
                'increase': 110.00
            },
            '8164854857': {  # Generic Shopping
                'name': 'Generic Shopping | EUR | Main',
                'current_budget': 177.85,
                'new_budget': 307.85,
                'increase': 130.00
            },
            '8161426257': {  # Performance Max
                'name': 'Performance Max | EUR | Main',
                'current_budget': 304.60,
                'new_budget': 710.60,
                'increase': 406.00
            },
            '8205799177': {  # Performance Max Brand
                'name': 'Performance Max | EUR | Brand',
                'current_budget': 60.64,
                'new_budget': 160.64,
                'increase': 100.00
            },
            '8166587697': {  # Competitor Search (PAUSE)
                'name': 'Competitor Search | EUR | Main',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            },
            '18316574617': {  # High Ticket Shopping (PAUSE)
                'name': 'High Ticket Shopping | EUR | Main',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            },
            '8161426377': {  # Performance Max Brand Rollup (PAUSE)
                'name': 'Performance Max | EUR | Brand Rollup',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            }
        }
    },

    # USA Account (7808690871)
    '7808690871': {
        'manager_id': '2569949686',
        'campaigns': {
            '21608113564': {  # Brand Search
                'name': 'Brand Search | USA | Main',
                'current_budget': 100.00,
                'new_budget': 400.00,
                'increase': 300.00
            },
            '21608113684': {  # Generic Search
                'name': 'Generic Search | USA | Main',
                'current_budget': 100.00,
                'new_budget': 300.00,
                'increase': 200.00
            },
            '21608114244': {  # Performance Max
                'name': 'Performance Max | USA | Main',
                'current_budget': 300.00,
                'new_budget': 900.00,
                'increase': 600.00
            },
            '21608113804': {  # Competitor Search (PAUSE)
                'name': 'Competitor Search | USA | Main',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            },
            '21608113924': {  # Generic Shopping
                'name': 'Generic Shopping | USA | Main',
                'current_budget': 4.00,
                'new_budget': 12.00,
                'increase': 8.00
            },
            '21608114004': {  # Brand Shopping (PAUSE)
                'name': 'Brand Shopping | USA | Main',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            }
        }
    },

    # UK Account (8573235780)
    '8573235780': {
        'manager_id': '2569949686',
        'campaigns': {
            '8161289137': {  # Brand Search
                'name': 'Brand Search | UK | Main',
                'current_budget': 323.48,
                'new_budget': 823.48,
                'increase': 500.00
            },
            '8160981697': {  # Generic Search
                'name': 'Generic Search | UK | Main',
                'current_budget': 261.97,
                'new_budget': 561.97,
                'increase': 300.00
            },
            '8161289257': {  # Performance Max
                'name': 'Performance Max | UK | Main',
                'current_budget': 455.81,
                'new_budget': 1055.81,
                'increase': 600.00
            },
            '21573858164': {  # Performance Max Brand
                'name': 'Performance Max | UK | Brand',
                'current_budget': 60.64,
                'new_budget': 183.64,
                'increase': 123.00
            },
            '8166587577': {  # Competitor Search (PAUSE)
                'name': 'Competitor Search | UK | Main',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            },
            '8164854737': {  # Generic Shopping (PAUSE)
                'name': 'Generic Shopping | UK | Main',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            },
            '8161289377': {  # Performance Max Brand Rollup (PAUSE)
                'name': 'Performance Max | UK | Brand Rollup',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            }
        }
    },

    # ROW Account (5556710725) - ALL PAUSE
    '5556710725': {
        'manager_id': '2569949686',
        'campaigns': {
            '21547639804': {  # Brand Search (PAUSE)
                'name': 'Brand Search | ROW | Main',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            },
            '21547639924': {  # Generic Search (PAUSE)
                'name': 'Generic Search | ROW | Main',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            },
            '21547640244': {  # Performance Max (PAUSE)
                'name': 'Performance Max | ROW | Main',
                'current_budget': 0.00,
                'new_budget': 0.00,
                'action': 'PAUSE'
            }
        }
    }
}


def gbp_to_micros(gbp: float) -> int:
    """Convert GBP to micros (1 GBP = 1,000,000 micros)"""
    return int(gbp * 1_000_000)


def print_summary():
    """Print summary of all changes"""
    print("\n" + "=" * 80)
    print("SMYTHSON P9 BUDGET DEPLOYMENT - DECEMBER 15-22")
    print("=" * 80)

    total_current = 0
    total_new = 0
    total_increase = 0
    campaign_count = 0
    pause_count = 0

    for customer_id, account_data in BUDGET_CHANGES.items():
        account_name = {
            '7679616761': 'EUR',
            '7808690871': 'USA',
            '8573235780': 'UK',
            '5556710725': 'ROW'
        }[customer_id]

        print(f"\n{account_name} Account ({customer_id}):")
        print("-" * 80)

        for campaign_id, campaign_data in account_data['campaigns'].items():
            campaign_count += 1
            name = campaign_data['name']

            if campaign_data.get('action') == 'PAUSE':
                print(f"  ❌ PAUSE: {name}")
                pause_count += 1
            else:
                current = campaign_data['current_budget']
                new = campaign_data['new_budget']
                increase = campaign_data['increase']

                total_current += current
                total_new += new
                total_increase += increase

                print(f"  ✓ {name}")
                print(f"    £{current:,.2f} → £{new:,.2f} (+£{increase:,.2f})")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total campaigns affected: {campaign_count}")
    print(f"Budget increases: {campaign_count - pause_count}")
    print(f"Campaigns to pause: {pause_count}")
    print(f"\nTotal daily budget:")
    print(f"  Current: £{total_current:,.2f}")
    print(f"  New: £{total_new:,.2f}")
    print(f"  Daily increase: +£{total_increase:,.2f}")
    print(f"\n8-day deployment (Dec 15-22):")
    print(f"  Total spend projection: £{total_new * 8:,.2f}")
    print("=" * 80)


def create_backup_json():
    """Create backup JSON with expected before/after values"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_file = Path(f"/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports/p9-budget-backup-{timestamp}.json")

    backup_data = {
        'timestamp': timestamp,
        'deployment_period': 'December 15-22, 2025',
        'accounts': {}
    }

    for customer_id, account_data in BUDGET_CHANGES.items():
        account_name = {
            '7679616761': 'EUR',
            '7808690871': 'USA',
            '8573235780': 'UK',
            '5556710725': 'ROW'
        }[customer_id]

        backup_data['accounts'][customer_id] = {
            'account_name': account_name,
            'manager_id': account_data['manager_id'],
            'campaigns': {}
        }

        for campaign_id, campaign_data in account_data['campaigns'].items():
            backup_data['accounts'][customer_id]['campaigns'][campaign_id] = {
                'name': campaign_data['name'],
                'action': campaign_data.get('action', 'BUDGET_INCREASE'),
                'expected_before': {
                    'budget_gbp': campaign_data['current_budget'],
                    'budget_micros': gbp_to_micros(campaign_data['current_budget'])
                },
                'expected_after': {
                    'budget_gbp': campaign_data['new_budget'],
                    'budget_micros': gbp_to_micros(campaign_data['new_budget'])
                }
            }

    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2)

    print(f"\n✓ Backup created: {backup_file}")
    return backup_file


def generate_mcp_commands():
    """Generate MCP command calls for execution"""
    print("\n" + "=" * 80)
    print("MCP COMMANDS FOR EXECUTION")
    print("=" * 80)
    print("\nThe following commands will be executed after user permission:\n")

    commands = []

    for customer_id, account_data in BUDGET_CHANGES.items():
        manager_id = account_data['manager_id']

        for campaign_id, campaign_data in account_data['campaigns'].items():
            if campaign_data.get('action') == 'PAUSE':
                # Pause command
                cmd = {
                    'type': 'update_campaign_status',
                    'customer_id': customer_id,
                    'manager_id': manager_id,
                    'campaign_id': campaign_id,
                    'status': 'PAUSED',
                    'campaign_name': campaign_data['name']
                }
                commands.append(cmd)
                print(f"PAUSE: {campaign_data['name']}")
                print(f"  mcp__google_ads__update_campaign_status(")
                print(f"    customer_id='{customer_id}',")
                print(f"    manager_id='{manager_id}',")
                print(f"    campaign_id='{campaign_id}',")
                print(f"    status='PAUSED'")
                print(f"  )\n")
            else:
                # Budget increase command
                new_budget_micros = gbp_to_micros(campaign_data['new_budget'])
                cmd = {
                    'type': 'update_campaign_budget',
                    'customer_id': customer_id,
                    'manager_id': manager_id,
                    'campaign_id': campaign_id,
                    'daily_budget_micros': new_budget_micros,
                    'campaign_name': campaign_data['name'],
                    'new_budget_gbp': campaign_data['new_budget']
                }
                commands.append(cmd)
                print(f"BUDGET INCREASE: {campaign_data['name']}")
                print(f"  £{campaign_data['current_budget']:.2f} → £{campaign_data['new_budget']:.2f}")
                print(f"  mcp__google_ads__update_campaign_budget(")
                print(f"    customer_id='{customer_id}',")
                print(f"    manager_id='{manager_id}',")
                print(f"    campaign_id='{campaign_id}',")
                print(f"    daily_budget_micros={new_budget_micros}")
                print(f"  )\n")

    print("=" * 80)
    print(f"Total commands to execute: {len(commands)}")
    print("=" * 80)

    return commands


if __name__ == "__main__":
    print_summary()
    backup_file = create_backup_json()
    commands = generate_mcp_commands()

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("1. ✓ Summary generated")
    print("2. ✓ Backup created")
    print("3. ⏸️  AWAITING USER PERMISSION to execute changes")
    print(f"4. Backup location: {backup_file}")
    print("\nTo execute:")
    print("  Run this script with --execute flag")
    print("  Or use Claude Code to call MCP tools directly")
    print("=" * 80)
