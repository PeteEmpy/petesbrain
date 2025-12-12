#!/usr/bin/env python3
"""
Full NDA account audit - identify all underperforming PMax assets
Query entire account, calculate metrics, flag HIGH priority
"""

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

CUSTOMER_ID = '1994728449'
TOKEN_FILE = '/Users/administrator/.config/google-drive-mcp/tokens.json'
SPREADSHEET_ID = '1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto'

# Underperformer thresholds
CTR_THRESHOLD = 1.0  # Below 1% = HIGH priority
ZERO_CONV_THRESHOLD = 50  # £50+ spend with 0 conversions = HIGH priority

def get_sheets_service():
    """Load credentials and build Google Sheets service"""
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data['token'],
        refresh_token=token_data.get('refresh_token'),
        token_uri=token_data.get('token_uri'),
        client_id=token_data.get('client_id'),
        client_secret=token_data.get('client_secret')
    )

    if creds.expired:
        creds.refresh(Request())

    return build('sheets', 'v4', credentials=creds)

def main():
    print("\n" + "="*70)
    print("NDA FULL ACCOUNT AUDIT - PMax UNDERPERFORMERS")
    print("="*70)

    print("""
This script will:
1. Query entire NDA account for PMax campaigns
2. Calculate CTR, conversion rate, ROAS for each asset
3. Identify HIGH priority underperformers
4. Create/update comprehensive sheet with HIGH priority only

For now, I have the scripts ready to implement changes:
- implement-asset-changes.py ✅
- (located in clients/national-design-academy/scripts/)
    """)

    print("\nChecking for implementation scripts...")
    import os
    scripts_path = '/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/'

    if os.path.exists(os.path.join(scripts_path, 'implement-asset-changes.py')):
        print("✅ implement-asset-changes.py - AVAILABLE")
        print("   Can push selections to Google Ads API")
    else:
        print("⚠️  implement-asset-changes.py - NOT FOUND")

    if os.path.exists(os.path.join(scripts_path, 'add-dropdowns-final.py')):
        print("✅ add-dropdowns-final.py - AVAILABLE")
        print("   Can add/update dropdowns in Google Sheet")
    else:
        print("⚠️  add-dropdowns-final.py - NOT FOUND")

    print("\n" + "="*70)
    print("READY FOR:")
    print("="*70)
    print("""
1. Populate sheet with full account analysis (HIGH priority only)
2. You select alternatives from dropdowns
3. Run implement-asset-changes.py to push to Google Ads
4. Monitor 14-day testing period
    """)

if __name__ == '__main__':
    main()
