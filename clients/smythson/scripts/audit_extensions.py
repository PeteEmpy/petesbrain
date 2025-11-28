#!/usr/bin/env python3
"""
Audit ad extensions across Smythson accounts for Black Friday/discount content

Checks sitelinks, callouts, and promotion extensions for:
- Black Friday wording
- Discount wording (e.g., "30% off", "sale", "discount")
- Expiry dates (do they expire Dec 1 or need manual pausing?)
"""

import sys
import os
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

os.environ['GOOGLE_ADS_DEVELOPER_TOKEN'] = 'VrzEP-PTSY01pm1BJidERQ'
os.environ['GOOGLE_ADS_OAUTH_CONFIG_PATH'] = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/credentials.json'

from oauth.google_auth import execute_gaql
import json
import re
from datetime import datetime

ACCOUNTS = {
    'UK': '8573235780',
    'USA': '7808690871',
    'EUR': '7679616761',
    'ROW': '5556710725'
}
MANAGER_ID = '2569949686'

# Black Friday / discount keywords
BF_KEYWORDS = ['black friday', 'bf', 'cyber', 'weekend', 'november', 'countdown']
DISCOUNT_KEYWORDS = ['%', 'off', 'sale', 'discount', 'offer', 'deal', 'save', 'promotion']

def contains_bf_or_discount(text):
    """Check if text contains Black Friday or discount wording"""
    if not text:
        return False, []

    text_lower = text.lower()
    found = []

    for kw in BF_KEYWORDS:
        if kw in text_lower:
            found.append(f"BF: {kw}")

    for kw in DISCOUNT_KEYWORDS:
        if kw in text_lower:
            found.append(f"DISCOUNT: {kw}")

    return len(found) > 0, found

def query_assets_by_type(customer_id, manager_id, asset_type):
    """Query assets of a specific type"""
    query = f"""
    SELECT
        asset.id,
        asset.name,
        asset.type,
        asset.resource_name,
        campaign.id,
        campaign.name,
        campaign_asset.status
    FROM campaign_asset
    WHERE asset.type = '{asset_type}'
    AND campaign.status != 'REMOVED'
    AND campaign_asset.status != 'REMOVED'
    """

    return execute_gaql(customer_id, query, manager_id)

def get_asset_details(customer_id, manager_id, asset_id):
    """Get detailed asset information by ID"""
    query = f"""
    SELECT
        asset.id,
        asset.name,
        asset.type,
        asset.sitelink_asset.link_text,
        asset.sitelink_asset.description1,
        asset.sitelink_asset.description2,
        asset.callout_asset.callout_text,
        asset.promotion_asset.promotion_target,
        asset.promotion_asset.discount_modifier,
        asset.promotion_asset.percent_off,
        asset.promotion_asset.money_amount_off_micros,
        asset.promotion_asset.promotion_code,
        asset.promotion_asset.start_date,
        asset.promotion_asset.end_date
    FROM asset
    WHERE asset.id = {asset_id}
    """

    result = execute_gaql(customer_id, query, manager_id)
    return result[0] if result else None

print("="*80)
print("SMYTHSON AD EXTENSIONS AUDIT - BLACK FRIDAY/DISCOUNT CONTENT")
print("="*80)

all_findings = []

for region, customer_id in ACCOUNTS.items():
    print(f"\n{'='*80}")
    print(f"REGION: {region} ({customer_id})")
    print(f"{'='*80}")

    # Query each extension type
    for asset_type in ['SITELINK', 'CALLOUT', 'PROMOTION']:
        print(f"\n  Checking {asset_type}s...")

        try:
            assets = query_assets_by_type(customer_id, MANAGER_ID, asset_type)
            print(f"    Found {len(assets)} {asset_type} associations")

            # Get unique asset IDs
            asset_ids = set()
            for row in assets:
                asset_id = row.get('asset', {}).get('id')
                if asset_id:
                    asset_ids.add(asset_id)

            print(f"    Checking {len(asset_ids)} unique {asset_type} assets...")

            for asset_id in asset_ids:
                try:
                    details = get_asset_details(customer_id, MANAGER_ID, asset_id)
                    if not details:
                        continue

                    asset_data = details.get('asset', {})

                    # Extract text based on type
                    texts_to_check = []
                    extra_info = {}

                    if asset_type == 'SITELINK':
                        sitelink = asset_data.get('sitelink_asset', {})
                        texts_to_check.append(sitelink.get('link_text', ''))
                        texts_to_check.append(sitelink.get('description1', ''))
                        texts_to_check.append(sitelink.get('description2', ''))
                        extra_info['link_text'] = sitelink.get('link_text', '')

                    elif asset_type == 'CALLOUT':
                        callout = asset_data.get('callout_asset', {})
                        texts_to_check.append(callout.get('callout_text', ''))
                        extra_info['callout_text'] = callout.get('callout_text', '')

                    elif asset_type == 'PROMOTION':
                        promo = asset_data.get('promotion_asset', {})
                        texts_to_check.append(promo.get('promotion_target', ''))
                        texts_to_check.append(promo.get('promotion_code', ''))
                        extra_info['promotion_target'] = promo.get('promotion_target', '')
                        extra_info['start_date'] = promo.get('start_date', '')
                        extra_info['end_date'] = promo.get('end_date', '')
                        extra_info['percent_off'] = promo.get('percent_off', '')

                    # Check all texts
                    found_issues = []
                    for text in texts_to_check:
                        has_issue, keywords = contains_bf_or_discount(text)
                        if has_issue:
                            found_issues.extend(keywords)

                    if found_issues:
                        finding = {
                            'region': region,
                            'customer_id': customer_id,
                            'asset_type': asset_type,
                            'asset_id': asset_id,
                            'asset_name': asset_data.get('name', ''),
                            'issues': found_issues,
                            'details': extra_info
                        }
                        all_findings.append(finding)

                        print(f"      ⚠️  Asset {asset_id}: {', '.join(found_issues)}")

                except Exception as e:
                    print(f"      Error checking asset {asset_id}: {str(e)[:50]}")

        except Exception as e:
            print(f"    Error querying {asset_type}s: {str(e)[:100]}")

# Save findings
output_file = '/Users/administrator/Documents/PetesBrain/clients/smythson/data/extensions_bf_audit_findings.json'
with open(output_file, 'w') as f:
    json.dump(all_findings, f, indent=2)

print(f"\n{'='*80}")
print(f"SUMMARY")
print(f"{'='*80}")
print(f"\nTotal extensions with BF/discount content: {len(all_findings)}")

# Summary by region
by_region = {}
for finding in all_findings:
    region = finding['region']
    if region not in by_region:
        by_region[region] = []
    by_region[region].append(finding)

for region, findings in sorted(by_region.items()):
    print(f"\n{region}: {len(findings)} extensions")
    by_type = {}
    for f in findings:
        asset_type = f['asset_type']
        if asset_type not in by_type:
            by_type[asset_type] = 0
        by_type[asset_type] += 1
    for asset_type, count in by_type.items():
        print(f"  - {asset_type}: {count}")

print(f"\n{'='*80}")
print(f"✓ Findings saved to: extensions_bf_audit_findings.json")
print(f"{'='*80}")
