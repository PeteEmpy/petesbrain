#!/usr/bin/env python3
"""
Microsoft Ads Client ID Finder

Searches Microsoft Ads accounts to find client account IDs.
Similar to get_client_ids.py for Google Ads.

Usage:
    python3 get_client_ids.py "Client Name"
    python3 get_client_ids.py --all
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import server functions
from server import list_accounts, get_campaigns

def find_client_account(client_name: str) -> Optional[Dict]:
    """
    Find Microsoft Ads account ID for a client.
    
    Args:
        client_name: Client name to search for
        
    Returns:
        Dictionary with account info or None if not found
    """
    print(f"🔍 Searching for '{client_name}'...\n", file=sys.stderr)
    
    try:
        # List all accounts
        accounts_response = list_accounts()
        accounts = accounts_response.get('accounts', [])
        
        if not accounts:
            print("⚠️  No Microsoft Ads accounts found", file=sys.stderr)
            return None
        
        print(f"   Found {len(accounts)} account(s)\n", file=sys.stderr)
        
        # Search for matching account (case-insensitive, partial match)
        client_lower = client_name.lower()
        
        for account in accounts:
            account_name = account.get('name', '').lower()
            account_id = account.get('id')
            account_number = account.get('number', '')
            
            # Check if client name appears in account name
            if client_lower in account_name or account_name in client_lower:
                print(f"✅ Match found!\n", file=sys.stderr)
                print(f"Account Name: {account.get('name')}")
                print(f"Account ID: {account_id}")
                print(f"Account Number: {account_number}")
                print(f"Status: {account.get('account_life_cycle_status')}")
                print(f"Currency: {account.get('currency_code')}")
                
                return {
                    'name': account.get('name'),
                    'id': account_id,
                    'number': account_number,
                    'status': account.get('account_life_cycle_status'),
                    'currency': account.get('currency_code')
                }
        
        print(f"❌ No account found matching '{client_name}'", file=sys.stderr)
        print("\nAvailable accounts:", file=sys.stderr)
        for account in accounts:
            print(f"  - {account.get('name')} (ID: {account.get('id')})", file=sys.stderr)
        
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return None

def list_all_accounts() -> List[Dict]:
    """List all Microsoft Ads accounts."""
    print("📋 Listing all Microsoft Ads accounts...\n", file=sys.stderr)
    
    try:
        accounts_response = list_accounts()
        accounts = accounts_response.get('accounts', [])
        
        if not accounts:
            print("⚠️  No accounts found", file=sys.stderr)
            return []
        
        print(f"Found {len(accounts)} account(s):\n", file=sys.stderr)
        
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account.get('name')}")
            print(f"   ID: {account.get('id')}")
            print(f"   Number: {account.get('number')}")
            print(f"   Status: {account.get('account_life_cycle_status')}")
            print(f"   Currency: {account.get('currency_code')}")
            print()
        
        return accounts
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return []

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Find Microsoft Ads account IDs for clients'
    )
    
    parser.add_argument(
        'client_name',
        nargs='?',
        help='Client name to search for'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='List all accounts'
    )
    
    args = parser.parse_args()
    
    if args.all:
        list_all_accounts()
    elif args.client_name:
        result = find_client_account(args.client_name)
        if not result:
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

