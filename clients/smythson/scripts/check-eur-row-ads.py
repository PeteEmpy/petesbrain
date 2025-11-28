#!/usr/bin/env python3
"""
Check EUR and ROW Google Ads accounts for:
1. Currency issues in delivery thresholds (£ vs €)
2. "New Arrivals" messaging that shouldn't be in winter sale
"""

import os
import sys
import json
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Account IDs
EUR_ACCOUNT = "7679616761"
ROW_ACCOUNT = "5556710725"

# Initialize client
client = GoogleAdsClient.load_from_storage(os.path.expanduser("~/google-ads.yaml"))

def get_responsive_search_ads(customer_id):
    """Get all responsive search ads with their headlines and descriptions"""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.name,
            ad_group.name,
            ad_group_ad.ad.id,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.ad.responsive_search_ad.descriptions,
            ad_group_ad.status
        FROM ad_group_ad
        WHERE ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
        AND ad_group_ad.status != 'REMOVED'
        AND campaign.status != 'REMOVED'
    """

    ads = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            headlines = [h.text for h in row.ad_group_ad.ad.responsive_search_ad.headlines]
            descriptions = [d.text for d in row.ad_group_ad.ad.responsive_search_ad.descriptions]
            ads.append({
                'type': 'Responsive Search Ad',
                'campaign': row.campaign.name,
                'ad_group': row.ad_group.name,
                'ad_id': row.ad_group_ad.ad.id,
                'status': row.ad_group_ad.status.name,
                'headlines': headlines,
                'descriptions': descriptions
            })
    except GoogleAdsException as ex:
        print(f"Error getting RSAs: {ex}")

    return ads

def get_pmax_asset_groups(customer_id):
    """Get Performance Max asset groups with their text assets"""
    ga_service = client.get_service("GoogleAdsService")

    # First get asset groups
    query = """
        SELECT
            campaign.name,
            asset_group.name,
            asset_group.id,
            asset_group.status
        FROM asset_group
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
        AND asset_group.status != 'REMOVED'
        AND campaign.status != 'REMOVED'
    """

    asset_groups = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            asset_groups.append({
                'campaign': row.campaign.name,
                'asset_group': row.asset_group.name,
                'asset_group_id': row.asset_group.id,
                'status': row.asset_group.status.name
            })
    except GoogleAdsException as ex:
        print(f"Error getting asset groups: {ex}")

    # Now get text assets for each asset group
    for ag in asset_groups:
        ag['headlines'] = []
        ag['long_headlines'] = []
        ag['descriptions'] = []

        query = f"""
            SELECT
                asset.text_asset.text,
                asset_group_asset.field_type
            FROM asset_group_asset
            WHERE asset_group.id = {ag['asset_group_id']}
            AND asset_group_asset.status = 'ENABLED'
            AND asset.type = 'TEXT'
        """

        try:
            response = ga_service.search(customer_id=customer_id, query=query)
            for row in response:
                text = row.asset.text_asset.text
                field_type = row.asset_group_asset.field_type.name

                if field_type == 'HEADLINE':
                    ag['headlines'].append(text)
                elif field_type == 'LONG_HEADLINE':
                    ag['long_headlines'].append(text)
                elif field_type == 'DESCRIPTION':
                    ag['descriptions'].append(text)
        except GoogleAdsException as ex:
            print(f"Error getting assets for {ag['asset_group']}: {ex}")

    return asset_groups

def get_extensions(customer_id):
    """Get ad extensions - sitelinks, callouts, structured snippets"""
    ga_service = client.get_service("GoogleAdsService")
    extensions = []

    # Sitelinks
    query = """
        SELECT
            campaign.name,
            asset.sitelink_asset.link_text,
            asset.sitelink_asset.description1,
            asset.sitelink_asset.description2,
            campaign_asset.status
        FROM campaign_asset
        WHERE asset.type = 'SITELINK'
        AND campaign_asset.status != 'REMOVED'
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            extensions.append({
                'type': 'Sitelink',
                'campaign': row.campaign.name,
                'text': row.asset.sitelink_asset.link_text,
                'desc1': row.asset.sitelink_asset.description1,
                'desc2': row.asset.sitelink_asset.description2,
                'status': row.campaign_asset.status.name
            })
    except GoogleAdsException as ex:
        print(f"Error getting sitelinks: {ex}")

    # Callouts
    query = """
        SELECT
            campaign.name,
            asset.callout_asset.callout_text,
            campaign_asset.status
        FROM campaign_asset
        WHERE asset.type = 'CALLOUT'
        AND campaign_asset.status != 'REMOVED'
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            extensions.append({
                'type': 'Callout',
                'campaign': row.campaign.name,
                'text': row.asset.callout_asset.callout_text,
                'status': row.campaign_asset.status.name
            })
    except GoogleAdsException as ex:
        print(f"Error getting callouts: {ex}")

    # Structured Snippets
    query = """
        SELECT
            campaign.name,
            asset.structured_snippet_asset.header,
            asset.structured_snippet_asset.values,
            campaign_asset.status
        FROM campaign_asset
        WHERE asset.type = 'STRUCTURED_SNIPPET'
        AND campaign_asset.status != 'REMOVED'
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            extensions.append({
                'type': 'Structured Snippet',
                'campaign': row.campaign.name,
                'header': row.asset.structured_snippet_asset.header,
                'values': list(row.asset.structured_snippet_asset.values),
                'status': row.campaign_asset.status.name
            })
    except GoogleAdsException as ex:
        print(f"Error getting structured snippets: {ex}")

    return extensions

def check_issues(text, account_type):
    """Check text for currency and new arrivals issues"""
    issues = []
    text_lower = text.lower()

    # Currency check
    if account_type == 'EUR':
        if '£300' in text or '£ 300' in text:
            issues.append('CURRENCY: Has £300 (should be €300 for EUR)')

    # New arrivals check (applies to both)
    if 'new arrival' in text_lower:
        issues.append('NEW ARRIVALS: Contains "new arrival" messaging')

    return issues

def analyze_account(customer_id, account_name):
    """Analyze an account and return issues found"""
    print(f"\n{'='*60}")
    print(f"Checking {account_name} Account ({customer_id})")
    print('='*60)

    all_issues = []

    # Check RSAs
    print("\nFetching Responsive Search Ads...")
    ads = get_responsive_search_ads(customer_id)
    print(f"Found {len(ads)} RSAs")

    for ad in ads:
        all_texts = ad['headlines'] + ad['descriptions']
        for text in all_texts:
            issues = check_issues(text, account_name)
            if issues:
                for issue in issues:
                    all_issues.append({
                        'account': account_name,
                        'campaign': ad['campaign'],
                        'location': f"Ad Group: {ad['ad_group']}",
                        'type': 'Responsive Search Ad',
                        'text': text,
                        'issue': issue,
                        'is_extension': 'No'
                    })

    # Check PMax Asset Groups
    print("\nFetching PMax Asset Groups...")
    asset_groups = get_pmax_asset_groups(customer_id)
    print(f"Found {len(asset_groups)} asset groups")

    for ag in asset_groups:
        all_texts = ag['headlines'] + ag['long_headlines'] + ag['descriptions']
        for text in all_texts:
            issues = check_issues(text, account_name)
            if issues:
                for issue in issues:
                    all_issues.append({
                        'account': account_name,
                        'campaign': ag['campaign'],
                        'location': f"Asset Group: {ag['asset_group']}",
                        'type': 'PMax Asset',
                        'text': text,
                        'issue': issue,
                        'is_extension': 'No'
                    })

    # Check Extensions
    print("\nFetching Ad Extensions...")
    extensions = get_extensions(customer_id)
    print(f"Found {len(extensions)} extensions")

    for ext in extensions:
        texts_to_check = []
        if ext['type'] == 'Sitelink':
            texts_to_check = [ext['text'], ext.get('desc1', ''), ext.get('desc2', '')]
        elif ext['type'] == 'Callout':
            texts_to_check = [ext['text']]
        elif ext['type'] == 'Structured Snippet':
            texts_to_check = ext.get('values', [])

        for text in texts_to_check:
            if text:
                issues = check_issues(text, account_name)
                if issues:
                    for issue in issues:
                        all_issues.append({
                            'account': account_name,
                            'campaign': ext['campaign'],
                            'location': ext['type'],
                            'type': ext['type'],
                            'text': text,
                            'issue': issue,
                            'is_extension': 'Yes'
                        })

    return all_issues

def main():
    all_issues = []

    # Check EUR account
    eur_issues = analyze_account(EUR_ACCOUNT, 'EUR')
    all_issues.extend(eur_issues)

    # Check ROW account
    row_issues = analyze_account(ROW_ACCOUNT, 'ROW')
    all_issues.extend(row_issues)

    # Output results
    print(f"\n{'='*60}")
    print(f"TOTAL ISSUES FOUND: {len(all_issues)}")
    print('='*60)

    if all_issues:
        # Save to JSON for processing
        output_file = '/Users/administrator/Documents/PetesBrain/clients/smythson/documents/eur-row-issues-from-api.json'
        with open(output_file, 'w') as f:
            json.dump(all_issues, f, indent=2)
        print(f"\nDetailed results saved to: {output_file}")

        # Print summary
        for issue in all_issues:
            print(f"\n{issue['account']} | {issue['campaign']}")
            print(f"  {issue['location']} | {issue['type']} | Extension: {issue['is_extension']}")
            print(f"  Text: {issue['text'][:60]}..." if len(issue['text']) > 60 else f"  Text: {issue['text']}")
            print(f"  Issue: {issue['issue']}")
    else:
        print("\nNo issues found!")

    return all_issues

if __name__ == "__main__":
    issues = main()
