#!/usr/bin/env python3
"""
Populate NDA PMax sheet with underperforming assets - ONE ROW PER ASSET TYPE

Each row represents a specific underperforming asset (HEADLINE, LONG_HEADLINE, or DESCRIPTION)
with alternatives matching that asset type only.

Analysis Period: 90 days (Sep 14 - Dec 12, 2025)
"""

import sys
from pathlib import Path
import json
import requests

# Add shared path for imports
parent_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(parent_dir / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server'))

from oauth.google_auth import get_headers_with_auto_token, format_customer_id
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

CUSTOMER_ID = "1994728449"
SPREADSHEET_ID = "1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto"
TOKEN_FILE = '/Users/administrator/.config/google-drive-mcp/tokens.json'
ALTERNATIVES_FILE = Path(__file__).parent / 'final-alternatives-for-dropdowns.json'

# Date range for 30-day analysis (fresh, actionable data)
START_DATE = '2025-11-12'  # Last 30 days
END_DATE = '2025-12-12'

# Relative performance thresholds
MIN_IMPRESSIONS = 1000  # 1,000 impressions = ~33/day over 30 days (statistically valid)
RELATIVE_CTR_THRESHOLD = 0.5  # Flag assets below 50% of group median CTR


def get_sheets_service():
    """Load Google Sheets credentials and build service"""
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


def query_assets_by_type(field_type: str) -> list:
    """Query underperforming assets by specific field type"""
    headers = get_headers_with_auto_token()
    formatted_customer_id = format_customer_id(CUSTOMER_ID)

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            asset_group.id,
            asset_group.name,
            asset_group_asset.field_type,
            asset.id,
            asset.text_asset.text,
            metrics.clicks,
            metrics.impressions,
            metrics.cost_micros,
            metrics.conversions
        FROM asset_group_asset
        WHERE segments.date >= '{START_DATE}'
          AND segments.date <= '{END_DATE}'
          AND asset_group_asset.field_type = '{field_type}'
          AND metrics.impressions > 0
        ORDER BY metrics.cost_micros DESC
        LIMIT 200
    """

    url = f"https://googleads.googleapis.com/v22/customers/{formatted_customer_id}/googleAds:search"
    payload = {"query": query}

    response = requests.post(url, headers=headers, json=payload)

    if not response.ok:
        print(f"Error querying {field_type}: {response.status_code}")
        print(f"  Response: {response.text[:500]}")
        return []

    data = response.json()
    results = []

    for row in data.get('results', []):
        campaign = row.get('campaign', {})
        asset_group = row.get('assetGroup', {})
        asset = row.get('asset', {})
        metrics = row.get('metrics', {})

        cost = int(metrics.get('costMicros', 0)) / 1_000_000
        conversions = float(metrics.get('conversions', 0))
        clicks = int(metrics.get('clicks', 0))
        impressions = int(metrics.get('impressions', 0))
        ctr = (clicks / impressions * 100) if impressions > 0 else 0

        results.append({
            'campaign_id': campaign.get('id'),
            'campaign_name': campaign.get('name', ''),
            'asset_group_id': asset_group.get('id'),
            'asset_group_name': asset_group.get('name', ''),
            'asset_id': asset.get('id'),
            'asset_text': asset.get('textAsset', {}).get('text', ''),
            'field_type': field_type,
            'clicks': clicks,
            'impressions': impressions,
            'ctr': ctr,
            'cost': cost,
            'conversions': conversions
        })

    return results


def identify_relative_underperformers(all_assets: list) -> list:
    """Identify underperformers relative to their asset group performance"""

    # Group assets by (asset_group_id, field_type)
    groups = {}
    for asset in all_assets:
        key = (asset['asset_group_id'], asset['field_type'])
        if key not in groups:
            groups[key] = []
        groups[key].append(asset)

    underperformers = []

    for (ag_id, field_type), assets in groups.items():
        # Calculate median CTR for this group (only assets with sufficient impressions)
        ctrs = [a['ctr'] for a in assets if a['impressions'] >= MIN_IMPRESSIONS]

        if not ctrs:
            # Skip groups without sufficient data
            continue

        # Sort and get median
        ctrs_sorted = sorted(ctrs)
        median_ctr = ctrs_sorted[len(ctrs_sorted) // 2]
        threshold = median_ctr * RELATIVE_CTR_THRESHOLD  # 50% of median

        # Flag underperformers in this group
        for asset in assets:
            if (asset['impressions'] >= MIN_IMPRESSIONS and
                asset['ctr'] < threshold and
                asset['conversions'] == 0):

                # Calculate relative performance
                if median_ctr > 0:
                    relative_perf = ((asset['ctr'] / median_ctr) - 1) * 100
                else:
                    relative_perf = -100

                asset['priority'] = 'HIGH'
                asset['median_ctr'] = median_ctr
                asset['relative_performance'] = relative_perf
                asset['issue'] = f"{relative_perf:.0f}% vs group median, 0 conv"
                underperformers.append(asset)

    return underperformers


def load_alternatives():
    """Load alternatives JSON"""
    if not ALTERNATIVES_FILE.exists():
        print(f"⚠️ Alternatives file not found: {ALTERNATIVES_FILE}")
        return {}

    with open(ALTERNATIVES_FILE, 'r') as f:
        return json.load(f)


def get_alternatives_for_text(asset_text: str, field_type: str, alternatives_data: dict) -> list:
    """Get alternatives matching the asset type for a given text"""

    # Find matching asset by text
    for asset_id, asset_data in alternatives_data.items():
        if asset_data.get('current', '').lower() == asset_text.lower():
            # Get the right alternatives based on field type
            if field_type == 'HEADLINE':
                # Flatten section_breakdown (short headlines)
                sections = asset_data.get('section_breakdown', {})
            elif field_type == 'LONG_HEADLINE':
                sections = asset_data.get('long_headlines', {})
            elif field_type == 'DESCRIPTION':
                sections = asset_data.get('descriptions', {})
            else:
                return []

            # Flatten all sections into single list
            all_options = []
            for section_name in ['Benefits', 'Technical', 'Quirky', 'CTA', 'Brand']:
                if section_name in sections:
                    all_options.extend(sections[section_name])

            return all_options

    return []


def populate_sheet(service, all_underperformers: list, alternatives_data: dict):
    """Populate Google Sheet with underperforming assets"""

    # Clear existing data (keep header)
    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A2:O100'
    ).execute()

    # Prepare rows
    rows = []
    dropdown_configs = []  # (row_num, alternatives)

    for idx, asset in enumerate(all_underperformers, start=2):
        # Get alternatives for this specific asset type
        alternatives = get_alternatives_for_text(
            asset['asset_text'],
            asset['field_type'],
            alternatives_data
        )

        # Create row data
        median_ctr = asset.get('median_ctr', 0)
        relative_perf = asset.get('relative_performance', 0)

        row = [
            asset['campaign_name'][:50] if len(asset['campaign_name']) > 50 else asset['campaign_name'],  # A: Campaign
            asset['asset_group_name'],  # B: Asset Group
            asset['field_type'],  # C: Asset Type (HEADLINE, LONG_HEADLINE, DESCRIPTION)
            asset['asset_text'],  # D: Asset Text
            asset['clicks'],  # E: Clicks
            asset['conversions'],  # F: Conversions
            f"{asset['ctr']:.2f}%",  # G: CTR
            "0.00%",  # H: Conv Rate
            f"£{asset['cost']:.2f}",  # I: Cost
            f"{median_ctr:.2f}%",  # J: Group Median CTR
            f"{relative_perf:.0f}%",  # K: Gap from median
            asset['priority'],  # L: Priority
            "",  # M: Alternative (dropdown will be added)
            asset['asset_id'],  # N: Asset ID (for implementation)
            asset['asset_group_id'],  # O: Asset Group ID
        ]
        rows.append(row)

        if alternatives:
            dropdown_configs.append((idx, alternatives))

    # Write all rows
    if rows:
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A2',
            valueInputOption='USER_ENTERED',
            body={'values': rows}
        ).execute()
        print(f"✅ Wrote {len(rows)} rows to sheet")

    # Update headers
    headers = [
        'Campaign', 'Asset Group', 'Asset Type', 'Asset Text',
        'Clicks', 'Conversions', 'CTR', 'Conv Rate', 'Cost',
        'Group Median CTR', 'Gap vs Median', 'Priority', 'Alternative', 'Asset ID', 'Asset Group ID'
    ]
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A1:O1',
        valueInputOption='USER_ENTERED',
        body={'values': [headers]}
    ).execute()

    return dropdown_configs


def add_dropdowns(service, dropdown_configs: list):
    """Add dropdowns for each row with type-appropriate alternatives"""

    for row_num, alternatives in dropdown_configs:
        col_index = 12  # Column M (0-indexed)
        row_index = row_num - 1  # 0-indexed

        options = ["Keep"] + alternatives[:15]  # Max 15 alternatives + Keep

        request = {
            "setDataValidation": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": row_index,
                    "endRowIndex": row_index + 1,
                    "startColumnIndex": col_index,
                    "endColumnIndex": col_index + 1
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": [{"userEnteredValue": opt} for opt in options]
                    },
                    "inputMessage": "Select alternative or Keep current",
                    "showCustomUi": True,
                    "strict": False
                }
            }
        }

        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": [request]}
        ).execute()

    print(f"✅ Added dropdowns to {len(dropdown_configs)} rows")


def main():
    print("\n" + "="*70)
    print("NDA PMAX - POPULATE BY ASSET TYPE")
    print("="*70)
    print(f"\nAnalysis Period: {START_DATE} to {END_DATE} (30 days)")
    print(f"Min Impressions: {MIN_IMPRESSIONS} (~{MIN_IMPRESSIONS/30:.0f}/day)")
    print(f"Threshold: CTR < {RELATIVE_CTR_THRESHOLD*100:.0f}% of group median")

    # Query each asset type separately
    print("\n" + "-"*70)
    print("QUERYING ASSETS BY TYPE...")
    print("-"*70)

    headlines = query_assets_by_type('HEADLINE')
    print(f"  HEADLINE: {len(headlines)} assets found")

    long_headlines = query_assets_by_type('LONG_HEADLINE')
    print(f"  LONG_HEADLINE: {len(long_headlines)} assets found")

    descriptions = query_assets_by_type('DESCRIPTION')
    print(f"  DESCRIPTION: {len(descriptions)} assets found")

    # Combine all assets for relative analysis
    all_assets = headlines + long_headlines + descriptions
    print(f"\nTotal assets: {len(all_assets)}")

    # Identify relative underperformers
    print("\n" + "-"*70)
    print("IDENTIFYING RELATIVE UNDERPERFORMERS...")
    print("-"*70)
    print(f"Criteria: CTR < 50% of group median, 0 conversions, ≥{MIN_IMPRESSIONS:,} impressions (~{MIN_IMPRESSIONS/30:.0f}/day)")

    all_underperformers = identify_relative_underperformers(all_assets)

    # Count by type for summary
    headline_under = [a for a in all_underperformers if a['field_type'] == 'HEADLINE']
    long_headline_under = [a for a in all_underperformers if a['field_type'] == 'LONG_HEADLINE']
    description_under = [a for a in all_underperformers if a['field_type'] == 'DESCRIPTION']

    print(f"  HEADLINE: {len(headline_under)} relative underperformers")
    print(f"  LONG_HEADLINE: {len(long_headline_under)} relative underperformers")
    print(f"  DESCRIPTION: {len(description_under)} relative underperformers")

    # Sort by cost descending
    all_underperformers.sort(key=lambda x: x['cost'], reverse=True)

    print(f"\nTotal underperformers: {len(all_underperformers)}")

    if not all_underperformers:
        print("No underperforming assets found matching criteria")
        return

    # Show summary
    print("\n" + "-"*70)
    print("TOP UNDERPERFORMERS:")
    print("-"*70)

    for asset in all_underperformers[:10]:
        print(f"  [{asset['field_type']:15}] £{asset['cost']:>7.0f} | {asset['asset_text'][:40]}...")

    # Load alternatives
    print("\n" + "-"*70)
    print("LOADING ALTERNATIVES...")
    print("-"*70)

    alternatives_data = load_alternatives()
    print(f"✅ Loaded alternatives for {len(alternatives_data)} asset texts")

    # Populate sheet
    print("\n" + "-"*70)
    print("POPULATING GOOGLE SHEET...")
    print("-"*70)

    service = get_sheets_service()
    dropdown_configs = populate_sheet(service, all_underperformers, alternatives_data)

    # Add dropdowns
    print("\n" + "-"*70)
    print("ADDING DROPDOWNS...")
    print("-"*70)

    add_dropdowns(service, dropdown_configs)

    # Summary
    print("\n" + "="*70)
    print("COMPLETE")
    print("="*70)

    print(f"\n✅ {len(all_underperformers)} underperforming assets populated")
    print(f"  • {len(headline_under)} HEADLINES (30 char alternatives)")
    print(f"  • {len(long_headline_under)} LONG_HEADLINES (90 char alternatives)")
    print(f"  • {len(description_under)} DESCRIPTIONS (90 char alternatives)")
    print(f"\nSheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
    print("\nEach row has its own dropdown with alternatives matching that asset type.")


if __name__ == '__main__':
    main()
