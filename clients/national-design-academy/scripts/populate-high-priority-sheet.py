#!/usr/bin/env python3
"""
Populate NDA PMax Sheet with HIGH Priority Underperformers
Based on 90-day analysis (Sep 14 - Dec 12, 2025)

HIGH Priority Criteria:
- CTR < 1% AND cost > £50
- OR 0 conversions AND cost > £100
"""

import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SPREADSHEET_ID = '1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto'
TOKEN_FILE = '/Users/administrator/.config/google-drive-mcp/tokens.json'

# 90-day asset data from Google Ads API query
ASSET_DATA = [
    # HIGH PRIORITY UNDERPERFORMERS (CTR <1% or 0 conv + high spend)

    # Oman/Saudi - £965 spend, 0 conversions - ENTIRE ASSET GROUP
    {
        'campaign': 'NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4',
        'asset_group': 'Interior Design Diploma',
        'asset_group_id': '6574589596',
        'asset_type': 'HEADLINE',
        'asset_text': 'Study Interior Design',
        'asset_id': '6501874539',
        'clicks': 196,
        'impressions': 48820,
        'conversions': 0,
        'cost_gbp': 18.34,
        'ctr': 0.40,
        'benchmark': 1.20,
        'gap': 66.7,
        'priority': 'HIGH',
        'reason': 'CTR 0.40% (<1%), 0 conversions'
    },
    {
        'campaign': 'NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4',
        'asset_group': 'Interior Design Diploma',
        'asset_group_id': '6574589596',
        'asset_type': 'HEADLINE',
        'asset_text': 'Interior Design Diploma',
        'asset_id': '6542848540',
        'clicks': 69,
        'impressions': 14375,
        'conversions': 0,
        'cost_gbp': 6.26,
        'ctr': 0.48,
        'benchmark': 1.20,
        'gap': 60.0,
        'priority': 'HIGH',
        'reason': 'CTR 0.48% (<1%), 0 conversions'
    },
    {
        'campaign': 'NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4',
        'asset_group': 'Interior Design Diploma',
        'asset_group_id': '6574589596',
        'asset_type': 'HEADLINE',
        'asset_text': 'Interior Design Courses',
        'asset_id': '8680183789',
        'clicks': 51,
        'impressions': 13421,
        'conversions': 0,
        'cost_gbp': 8.56,
        'ctr': 0.38,
        'benchmark': 1.20,
        'gap': 68.3,
        'priority': 'HIGH',
        'reason': 'CTR 0.38% (<1%), 0 conversions'
    },

    # UAE campaign - HIGH spend, 0 conversions on these headlines
    {
        'campaign': 'NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5',
        'asset_group': 'Interior Design Diploma',
        'asset_group_id': '6574552905',
        'asset_type': 'HEADLINE',
        'asset_text': 'Interior Design Courses',
        'asset_id': '8680183789',
        'clicks': 828,
        'impressions': 141454,
        'conversions': 0,
        'cost_gbp': 874.84,
        'ctr': 0.59,
        'benchmark': 1.28,
        'gap': 53.9,
        'priority': 'HIGH',
        'reason': 'CTR 0.59% (<1%), 0 conversions, £875 spend'
    },
    {
        'campaign': 'NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5',
        'asset_group': 'Interior Design Diploma',
        'asset_group_id': '6574552905',
        'asset_type': 'HEADLINE',
        'asset_text': 'Interior Design Diploma',
        'asset_id': '6542848540',
        'clicks': 504,
        'impressions': 59631,
        'conversions': 0,
        'cost_gbp': 588.57,
        'ctr': 0.85,
        'benchmark': 1.28,
        'gap': 33.6,
        'priority': 'HIGH',
        'reason': 'CTR 0.85% (<1%), 0 conversions, £589 spend'
    },

    # Oman/Saudi DEGREE campaign - £1,112 spend, 0 conversions
    {
        'campaign': 'NDA | P Max | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target',
        'asset_group': 'Interior Design Degree',
        'asset_group_id': '6559669612',
        'asset_type': 'HEADLINE',
        'asset_text': 'Online Interior Design Degrees',
        'asset_id': '8680134790',
        'clicks': 2272,
        'impressions': 465818,
        'conversions': 0,
        'cost_gbp': 762.11,
        'ctr': 0.49,
        'benchmark': 0.89,
        'gap': 44.9,
        'priority': 'HIGH',
        'reason': 'CTR 0.49% (<1%), 0 conversions, £762 spend'
    },
    {
        'campaign': 'NDA | P Max | Interior Design Degree - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target',
        'asset_group': 'Interior Design Degree',
        'asset_group_id': '6559669612',
        'asset_type': 'HEADLINE',
        'asset_text': 'Interior Design Degree',
        'asset_id': '6503351051',
        'clicks': 2137,
        'impressions': 435813,
        'conversions': 0,
        'cost_gbp': 605.12,
        'ctr': 0.49,
        'benchmark': 0.89,
        'gap': 44.9,
        'priority': 'HIGH',
        'reason': 'CTR 0.49% (<1%), 0 conversions, £605 spend'
    },

    # USA/Canada - £1,164 spend, 0 conversions
    {
        'campaign': 'NDA | P Max | Interior Design Diploma - USA/Canada 250 Split 11/3 No Target 29/5',
        'asset_group': 'Interior Design Diploma',
        'asset_group_id': '6510182149',
        'asset_type': 'HEADLINE',
        'asset_text': 'Price-Match Guarantee',
        'asset_id': '10422358209',
        'clicks': 322,
        'impressions': 105201,
        'conversions': 0,
        'cost_gbp': 902.11,
        'ctr': 0.31,
        'benchmark': 0.39,
        'gap': 20.5,
        'priority': 'HIGH',
        'reason': 'CTR 0.31% (<1%), 0 conversions, £902 spend'
    },
    {
        'campaign': 'NDA | P Max | Interior Design Diploma - USA/Canada 250 Split 11/3 No Target 29/5',
        'asset_group': 'Interior Design Diploma',
        'asset_group_id': '6510182149',
        'asset_type': 'HEADLINE',
        'asset_text': 'Interior Design Courses',
        'asset_id': '8680183789',
        'clicks': 155,
        'impressions': 39616,
        'conversions': 0,
        'cost_gbp': 426.03,
        'ctr': 0.39,
        'benchmark': 0.39,
        'gap': 0.0,
        'priority': 'HIGH',
        'reason': 'CTR 0.39% (<1%), 0 conversions, £426 spend'
    },
    {
        'campaign': 'NDA | P Max | Interior Design Diploma - USA/Canada 250 Split 11/3 No Target 29/5',
        'asset_group': 'Interior Design Diploma',
        'asset_group_id': '6510182149',
        'asset_type': 'HEADLINE',
        'asset_text': 'Intensive Fast-Track Diplomas',
        'asset_id': '182887527317',
        'clicks': 204,
        'impressions': 67889,
        'conversions': 0,
        'cost_gbp': 562.91,
        'ctr': 0.30,
        'benchmark': 0.39,
        'gap': 23.1,
        'priority': 'HIGH',
        'reason': 'CTR 0.30% (<1%), 0 conversions, £563 spend'
    },

    # USA/Canada DEGREE - £540 spend, 0 conversions
    {
        'campaign': 'NDA | P Max | Interior Design Degree - USA/Canada 250 Split 11/3',
        'asset_group': 'Interior Design Degree',
        'asset_group_id': '6559669429',
        'asset_type': 'HEADLINE',
        'asset_text': 'Online Interior Design Degrees',
        'asset_id': '8680134790',
        'clicks': 354,
        'impressions': 52009,
        'conversions': 0,
        'cost_gbp': 404.32,
        'ctr': 0.68,
        'benchmark': 0.69,
        'gap': 1.4,
        'priority': 'HIGH',
        'reason': 'CTR 0.68% (<1%), 0 conversions, £404 spend'
    },

    # UAE DEGREE - some with 0 conversions
    {
        'campaign': 'NDA | P Max | Interior Design Degree - UAE 175 No Target 24/4',
        'asset_group': 'Interior Design Degree',
        'asset_group_id': '6557276329',
        'asset_type': 'HEADLINE',
        'asset_text': 'Online Interior Design Degrees',
        'asset_id': '8680134790',
        'clicks': 846,
        'impressions': 143897,
        'conversions': 3,
        'cost_gbp': 760.76,
        'ctr': 0.59,
        'benchmark': 0.61,
        'gap': 3.3,
        'priority': 'HIGH',
        'reason': 'CTR 0.59% (<1%), £761 spend'
    },
]

def get_sheets_service():
    """Load credentials and build Google Sheets service"""
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data.get('access_token') or token_data.get('token'),
        refresh_token=token_data.get('refresh_token'),
        token_uri=token_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
        client_id=token_data.get('client_id'),
        client_secret=token_data.get('client_secret')
    )

    if creds.expired:
        creds.refresh(Request())

    return build('sheets', 'v4', credentials=creds)

def clear_sheet(service):
    """Clear existing data (keep header)"""
    print("Clearing existing data...")
    try:
        service.spreadsheets().values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A2:M100'
        ).execute()
        print("✅ Cleared existing data")
    except Exception as e:
        print(f"⚠️  Clear warning: {str(e)}")

def populate_sheet(service):
    """Populate sheet with HIGH priority assets"""

    # Build rows
    rows = []
    for asset in ASSET_DATA:
        rows.append([
            asset['campaign'],
            asset['asset_group'],
            asset['asset_type'],
            asset['asset_text'],
            asset['clicks'],
            asset['conversions'],
            f"{asset['ctr']:.2f}%",
            f"{(asset['conversions'] / max(1, asset['clicks']) * 100):.2f}%",
            f"£{asset['cost_gbp']:.2f}",
            f"{asset['benchmark']:.2f}%",
            f"{asset['gap']:.1f}%",
            asset['priority'],
            '🔽 Select alternative'  # Placeholder for dropdown
        ])

    print(f"\nPopulating sheet with {len(rows)} HIGH priority assets...")

    # Write data
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A2',
            valueInputOption='USER_ENTERED',
            body={'values': rows}
        ).execute()
        print(f"✅ Populated {result.get('updatedRows', 0)} rows")
        return True
    except Exception as e:
        print(f"❌ Error populating sheet: {str(e)}")
        return False

def main():
    print("="*80)
    print("NDA PMax Sheet Population - HIGH Priority Underperformers")
    print("="*80)
    print(f"\nAnalysis Period: 90 days (Sep 14 - Dec 12, 2025)")
    print(f"HIGH Priority Criteria:")
    print(f"  • CTR < 1% AND cost > £50")
    print(f"  • OR 0 conversions AND cost > £100")
    print(f"\nTotal HIGH priority assets found: {len(ASSET_DATA)}")

    # Summary by campaign
    campaigns = {}
    for asset in ASSET_DATA:
        camp = asset['campaign'][:50]
        if camp not in campaigns:
            campaigns[camp] = 0
        campaigns[camp] += 1

    print("\nBreakdown by campaign:")
    for camp, count in campaigns.items():
        print(f"  • {camp}... : {count} assets")

    print("\n" + "-"*80)

    service = get_sheets_service()

    # Clear and populate
    clear_sheet(service)
    populate_sheet(service)

    print("\n" + "="*80)
    print("COMPLETE")
    print("="*80)
    print(f"\nGoogle Sheet updated with {len(ASSET_DATA)} HIGH priority assets")
    print(f"Sheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
    print("\nNext steps:")
    print("  1. Run add-dropdowns-final.py to add alternative dropdowns")
    print("  2. Make selections in column M")
    print("  3. Run implement-sheet-selections.py to push to Google Ads")

if __name__ == '__main__':
    main()
