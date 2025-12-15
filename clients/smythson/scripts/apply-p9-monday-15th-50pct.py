#!/usr/bin/env python3
"""
Smythson P9 Monday 15th December Deployment
50% budget increases across all 4 accounts

Apply tonight (Sunday 14th) for Monday morning effectiveness
"""

import json

# Budget changes for all accounts
BUDGET_CHANGES = {
    '7679616761': {  # EUR Account
        'account_name': 'EUR',
        'manager_id': '2569949686',
        'budgets': {
            '15134675617': {'current': 50000000, 'new': 75000000, 'campaigns': ['SMY | EUR | IT | P Max | Diaries']},
            '15134675031': {'current': 90000000, 'new': 135000000, 'campaigns': ['SMY | EUR | P Max | Christmas Gifting']},
            '15161693768': {'current': 30000000, 'new': 45000000, 'campaigns': ['SMY | EUR | CH | Search | Brand Ai']},
            '15134674263': {'current': 16000000, 'new': 24000000, 'campaigns': ['SMY | EUR | DE | P Max | Christmas Gifting']},
            '15134675205': {'current': 40000000, 'new': 60000000, 'campaigns': ['SMY | EUR | DE | P Max | Diaries']},
            '1693293924': {'current': 79000000, 'new': 118500000, 'campaigns': ['SMY | EUR | DE | Search | Brand Ai']},
            '14467064419': {'current': 79000000, 'new': 118500000, 'campaigns': ['SMY | EUR | DE | Search | Brand Max Conv Value']},
            '15114773693': {'current': 11000000, 'new': 16500000, 'campaigns': ['SMY | EUR | DE | Search | Competitor | Ai']},
            '13750754882': {'current': 29000000, 'new': 43500000, 'campaigns': ['SMY | EUR | DE | Shopping']},
            '15126675606': {'current': 66000000, 'new': 99000000, 'campaigns': ['SMY | EUR | FR | P Max | Christmas Gifting']},
            '1693293960': {'current': 50000000, 'new': 75000000, 'campaigns': ['SMY | EUR | FR | Search | Brand Ai']},
            '15134674673': {'current': 20000000, 'new': 30000000, 'campaigns': ['SMY | EUR | IT | P Max | Christmas Gifting']},
            '1711970218': {'current': 110000000, 'new': 165000000, 'campaigns': ['SMY | EUR | IT | Search Brand Ai']},
            '14489155324': {'current': 153000000, 'new': 229500000, 'campaigns': ['SMY | EUR | ROEuro | Search | Brand Ai']},
            '14485065127': {'current': 64000000, 'new': 96000000, 'campaigns': ['SMY | EUR | Search | Brand ES+PT | Ai']},
        }
    },
    '7808690871': {  # USA Account
        'account_name': 'USA',
        'manager_id': '2569949686',
        'budgets': {
            '14764145494': {'current': 104000000, 'new': 156000000, 'campaigns': ['SMY | US | P Max | Bags']},
            '15095915233': {'current': 150000000, 'new': 225000000, 'campaigns': ['SMY | US | P Max | Diaries']},
            '11405146786': {'current': 250000000, 'new': 375000000, 'campaigns': ['SMY | US | P Max | H&S']},
            '15118117815': {'current': 187000000, 'new': 280500000, 'campaigns': ['SMY | US | P Max | H&S Christmas Gifting']},
            '14551157402': {'current': 100000000, 'new': 150000000, 'campaigns': ['SMY | US | PMax | Zombies']},
            '11422372952': {'current': 561000000, 'new': 841500000, 'campaigns': ['SMY | US | Search | Brand Exact + 4 others (SHARED)']},
            '12929893890': {'current': 90000000, 'new': 135000000, 'campaigns': ['SMY | US | Search | Brand Plus']},
            '14919994754': {'current': 114000000, 'new': 171000000, 'campaigns': ['SMY | US | Search | Brand Plus Diaries']},
            '13390322534': {'current': 52000000, 'new': 78000000, 'campaigns': ['SMY | US | Search | Brand | Leather Accessories']},
            '13343381269': {'current': 30000000, 'new': 45000000, 'campaigns': ['SMY | US | Search | Brand | Stationery']},
            '1659506859': {'current': 36000000, 'new': 54000000, 'campaigns': ['Target CPA Experiment - USA - brand - misspellings']},
            '1736951227': {'current': 52000000, 'new': 78000000, 'campaigns': ['USA - brand - core [EX]']},
            '11971109509': {'current': 200000000, 'new': 300000000, 'campaigns': ['USA - brand - locations']},
            '11425294476': {'current': 20000000, 'new': 30000000, 'campaigns': ['USA - brand - misspellings']},
        }
    },
    '8573235780': {  # UK Account
        'account_name': 'UK',
        'manager_id': '2569949686',
        'budgets': {
            '15088625616': {'current': 264000000, 'new': 396000000, 'campaigns': ['SMY | UK | P Max | Diaries']},
            '14725890813': {'current': 250000000, 'new': 375000000, 'campaigns': ['SMY | UK | P Max | H&S'], 'note': 'Dec 11 reallocation - will revert to £450 on Dec 18'},
            '14936434754': {'current': 143000000, 'new': 214500000, 'campaigns': ['SMY | UK | P Max | H&S - Men\'s Briefcases'], 'note': 'Dec 11 reallocation - will revert to £179 on Dec 18'},
            '15118652001': {'current': 231000000, 'new': 346500000, 'campaigns': ['SMY | UK | P Max | H&S Christmas Gifting'], 'note': 'Dec 11 reallocation - will revert to £243 on Dec 18'},
            '8971023857': {'current': 860000000, 'new': 1290000000, 'campaigns': ['SMY | UK | Search | Brand Exact']},
            '8971024039': {'current': 50000000, 'new': 75000000, 'campaigns': ['SMY | UK | Search | Brand Plus'], 'note': 'Dec 11 reallocation - will revert to £100 on Dec 18'},
            '8971024375': {'current': 32000000, 'new': 48000000, 'campaigns': ['SMY | UK | Search | Brand Stationery'], 'note': 'Dec 11 reallocation - will revert to £91 on Dec 18'},
            '15103654059': {'current': 20000000, 'new': 30000000, 'campaigns': ['SMY | UK | Search | Competitor | Ai']},
            '14989352959': {'current': 10000000, 'new': 15000000, 'campaigns': ['SMY | UK | Search | Generic | Ai']},
            '8971022865': {'current': 250000000, 'new': 375000000, 'campaigns': ['SMY | UK | Search | Semi Brand - Diaries']},
            '14938542175': {'current': 62000000, 'new': 93000000, 'campaigns': ['SMY | UK | Search | Semi Brand - Leather']},
            '11427695878': {'current': 45000000, 'new': 67500000, 'campaigns': ['SMY | UK | Shopping | Brand | Fashion']},
            '7249862016': {'current': 75000000, 'new': 112500000, 'campaigns': ['SMY | UK | Shopping | Brand | Stationery']},
            '11463479378': {'current': 450000000, 'new': 675000000, 'campaigns': ['SMY | UK | Shopping | Generic | Fashion High Priority']},
            '11427696170': {'current': 75000000, 'new': 112500000, 'campaigns': ['SMY | UK | Shopping | Generic | High Value | Stationery']},
            '11491994946': {'current': 284000000, 'new': 426000000, 'campaigns': ['SMY | UK | Shopping | Generic | Medium Value']},
        }
    },
    '5556710725': {  # ROW Account
        'account_name': 'ROW',
        'manager_id': '2569949686',
        'budgets': {
            '11370644814': {'current': 40000000, 'new': 60000000, 'campaigns': ['SMY | ROW | AUS | Search | Brand Ai + 1 other (SHARED)']},
            '11370644370': {'current': 2500000, 'new': 3750000, 'campaigns': ['ROW - CA - brand']},
            '11365331684': {'current': 2500000, 'new': 3750000, 'campaigns': ['ROW - HK - brand']},
            '11370644109': {'current': 2500000, 'new': 3750000, 'campaigns': ['ROW - MEX - brand']},
            '11376421816': {'current': 2500000, 'new': 3750000, 'campaigns': ['ROW - SG - brand']},
            '11376425032': {'current': 52000000, 'new': 78000000, 'campaigns': ['ROW - brand test to reduce cpc']},
            '15134692206': {'current': 100000000, 'new': 150000000, 'campaigns': ['SMY | ROW | P Max | Christmas Gifting']},
            '15134691735': {'current': 5000000, 'new': 7500000, 'campaigns': ['SMY | ROW | P Max | Diaries']},
            '14528371083': {'current': 100000000, 'new': 150000000, 'campaigns': ['SMY | ROW | Search | Brand Ai']},
            '12929903025': {'current': 15000000, 'new': 22500000, 'campaigns': ['SMY | ROW | Search | Brand Diaries']},
            '15122745964': {'current': 3000000, 'new': 4500000, 'campaigns': ['SMY | ROW | Search | Competitor | Ai']},
        }
    }
}

def generate_mcp_commands():
    """Generate MCP commands for all budget changes"""

    print("\n" + "=" * 80)
    print("SMYTHSON P9 - MONDAY 15TH DECEMBER BUDGET DEPLOYMENT")
    print("50% increases across all accounts")
    print("=" * 80)

    for customer_id, account_data in BUDGET_CHANGES.items():
        account_name = account_data['account_name']
        manager_id = account_data['manager_id']

        print(f"\n\n{'=' * 80}")
        print(f"{account_name} ACCOUNT ({customer_id})")
        print(f"{'=' * 80}\n")

        for budget_id, budget_data in account_data['budgets'].items():
            current_gbp = budget_data['current'] / 1000000
            new_gbp = budget_data['new'] / 1000000
            increase_gbp = new_gbp - current_gbp
            increase_pct = ((new_gbp - current_gbp) / current_gbp) * 100
            campaigns = budget_data['campaigns']
            note = budget_data.get('note', '')

            print(f"Budget ID: {budget_id}")
            print(f"Campaigns: {', '.join(campaigns)}")
            print(f"Current:   £{current_gbp:,.2f}/day")
            print(f"New:       £{new_gbp:,.2f}/day")
            print(f"Increase:  +£{increase_gbp:,.2f} (+{increase_pct:.0f}%)")
            if note:
                print(f"NOTE:      {note}")

            print(f"\nMCP Command:")
            print(f"mcp__google-ads__update_campaign_budget(")
            print(f"    customer_id='{customer_id}',")
            print(f"    manager_id='{manager_id}',")
            print(f"    budget_id='{budget_id}',")
            print(f"    daily_budget_micros={budget_data['new']}")
            print(f")")
            print("-" * 80 + "\n")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    for customer_id, account_data in BUDGET_CHANGES.items():
        account_name = account_data['account_name']
        total_current = sum(b['current'] for b in account_data['budgets'].values()) / 1000000
        total_new = sum(b['new'] for b in account_data['budgets'].values()) / 1000000
        total_increase = total_new - total_current

        print(f"\n{account_name}:")
        print(f"  Current daily:  £{total_current:,.2f}")
        print(f"  New daily:      £{total_new:,.2f}")
        print(f"  Increase:       +£{total_increase:,.2f}")

    # Overall totals
    grand_total_current = sum(
        sum(b['current'] for b in account_data['budgets'].values())
        for account_data in BUDGET_CHANGES.values()
    ) / 1000000

    grand_total_new = sum(
        sum(b['new'] for b in account_data['budgets'].values())
        for account_data in BUDGET_CHANGES.values()
    ) / 1000000

    grand_total_increase = grand_total_new - grand_total_current

    print(f"\n{'=' * 80}")
    print(f"ALL ACCOUNTS TOTAL:")
    print(f"  Current daily:  £{grand_total_current:,.2f}")
    print(f"  New daily:      £{grand_total_new:,.2f}")
    print(f"  Increase:       +£{grand_total_increase:,.2f} (+50%)")
    print(f"{'=' * 80}\n")

    print("\nCRITICAL NOTES:")
    print("1. All campaigns remain ACTIVE throughout P9 period (Dec 15-28)")
    print("2. UK campaigns affected by Dec 11 reallocation will be REVERSED Thursday Dec 18")
    print("3. After Dec 18 reversal, UK budgets will differ from these new budgets")
    print("4. Sale launch: Wednesday Dec 24")
    print("=" * 80)

if __name__ == '__main__':
    generate_mcp_commands()
