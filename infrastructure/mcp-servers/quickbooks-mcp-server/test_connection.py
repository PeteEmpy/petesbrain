#!/usr/bin/env python3
"""
Test QuickBooks connection and OAuth tokens

Run this script to verify your QuickBooks authentication is working.
"""

import os
import sys
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from oauth.quickbooks_auth import (
    load_tokens,
    is_token_expired,
    get_valid_token,
    get_realm_id,
    get_headers_with_auto_token
)
import requests


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_environment():
    """Test environment variables"""
    print_section("Environment Variables")
    
    client_id = os.getenv('QUICKBOOKS_CLIENT_ID')
    client_secret = os.getenv('QUICKBOOKS_CLIENT_SECRET')
    
    if not client_id:
        print("❌ QUICKBOOKS_CLIENT_ID not set")
        return False
    else:
        print(f"✓ QUICKBOOKS_CLIENT_ID: {client_id[:10]}...{client_id[-5:]}")
    
    if not client_secret:
        print("❌ QUICKBOOKS_CLIENT_SECRET not set")
        return False
    else:
        print(f"✓ QUICKBOOKS_CLIENT_SECRET: {client_secret[:10]}...{client_secret[-5:]}")
    
    return True


def test_token_file():
    """Test token file exists and is valid"""
    print_section("OAuth Tokens")
    
    try:
        tokens = load_tokens()
        print("✓ Token file found")
        
        # Check token contents
        if 'access_token' in tokens:
            print(f"✓ Access Token: {tokens['access_token'][:20]}...")
        else:
            print("❌ No access token in file")
            return False
        
        if 'refresh_token' in tokens:
            print(f"✓ Refresh Token: {tokens['refresh_token'][:20]}...")
        else:
            print("❌ No refresh token in file")
            return False
        
        if 'realmId' in tokens:
            print(f"✓ Realm ID: {tokens['realmId']}")
        else:
            print("❌ No realm ID in file")
            return False
        
        # Check expiration
        if 'expires_at' in tokens:
            expires_at = datetime.fromisoformat(tokens['expires_at'])
            now = datetime.now()
            
            if is_token_expired(tokens):
                time_until_refresh = "Needs refresh now"
                print(f"⚠️  Access Token Status: {time_until_refresh}")
            else:
                time_left = expires_at - now
                minutes_left = int(time_left.total_seconds() / 60)
                print(f"✓ Access Token Valid: {minutes_left} minutes remaining")
        
        return True
        
    except FileNotFoundError:
        print("❌ Token file not found")
        print("\nPlease run: python setup_oauth.py")
        return False
    except Exception as e:
        print(f"❌ Error reading token file: {str(e)}")
        return False


def test_token_refresh():
    """Test token refresh if needed"""
    print_section("Token Refresh Test")
    
    try:
        tokens = load_tokens()
        
        if is_token_expired(tokens):
            print("⏳ Token expired, attempting refresh...")
            access_token = get_valid_token()
            print("✓ Token refreshed successfully")
            print(f"✓ New Access Token: {access_token[:20]}...")
        else:
            print("✓ Token is valid, no refresh needed")
        
        return True
        
    except Exception as e:
        print(f"❌ Token refresh failed: {str(e)}")
        return False


def test_api_connection():
    """Test actual API connection"""
    print_section("QuickBooks API Connection")
    
    try:
        # Get authenticated headers
        headers = get_headers_with_auto_token()
        realm_id = get_realm_id()
        
        # Test API call - get company info
        url = f"https://quickbooks.api.intuit.com/v3/company/{realm_id}/companyinfo/{realm_id}"
        
        print(f"⏳ Testing API endpoint: /companyinfo/{realm_id}")
        response = requests.get(url, headers=headers)
        
        if response.ok:
            company_info = response.json().get('CompanyInfo', {})
            company_name = company_info.get('CompanyName', 'Unknown')
            legal_name = company_info.get('LegalName', 'N/A')
            
            print(f"✓ API Connection Successful!")
            print(f"✓ Company Name: {company_name}")
            print(f"✓ Legal Name: {legal_name}")
            
            # Show some additional info if available
            if 'Email' in company_info:
                print(f"✓ Email: {company_info['Email'].get('Address', 'N/A')}")
            
            return True
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API connection test failed: {str(e)}")
        return False


def test_report_access():
    """Test report access"""
    print_section("Report Access Test")
    
    try:
        headers = get_headers_with_auto_token()
        realm_id = get_realm_id()
        
        # Test P&L report access
        url = f"https://quickbooks.api.intuit.com/v3/company/{realm_id}/reports/ProfitAndLoss"
        params = {
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'accounting_method': 'Accrual'
        }
        
        print("⏳ Testing Profit & Loss report access...")
        response = requests.get(url, headers=headers, params=params)
        
        if response.ok:
            data = response.json()
            header = data.get('Header', {})
            report_name = header.get('ReportName', 'Unknown')
            
            print(f"✓ Report Access Successful!")
            print(f"✓ Report Name: {report_name}")
            print(f"✓ Time Period: {header.get('StartPeriod', 'N/A')} to {header.get('EndPeriod', 'N/A')}")
            
            return True
        else:
            print(f"❌ Report request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Report access test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  QuickBooks MCP Server - Connection Test")
    print("=" * 60)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_environment()
    all_passed &= test_token_file()
    all_passed &= test_token_refresh()
    all_passed &= test_api_connection()
    all_passed &= test_report_access()
    
    # Summary
    print_section("Test Summary")
    
    if all_passed:
        print("✅ All tests passed!")
        print("\n🎉 Your QuickBooks connection is working perfectly.")
        print("\nYou can now:")
        print("  1. Add the server to your Cursor MCP configuration")
        print("  2. Restart Cursor")
        print("  3. Start asking for QuickBooks reports!")
        print("\nExample queries:")
        print("  - 'Get the P&L report for this year'")
        print("  - 'Show me the current balance sheet'")
        print("  - 'What's our accounts receivable aging?'")
    else:
        print("❌ Some tests failed")
        print("\nTroubleshooting:")
        print("  1. Make sure .env file has correct credentials")
        print("  2. Run: python setup_oauth.py (to re-authenticate)")
        print("  3. Check README.md for detailed setup instructions")
        print("  4. Verify your app has 'Accounting' scope enabled")
    
    print("\n" + "=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

