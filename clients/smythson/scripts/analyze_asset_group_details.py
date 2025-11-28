#!/usr/bin/env python3
"""
Analyze detailed asset group configuration including:
- Listing groups (product groups)
- Search themes
- Audience signals
- Final URLs
For Smythson PMax H&S and Christmas Gifting campaigns.
"""

import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

UK_ACCOUNT = "8573235780"
USA_ACCOUNT = "7808690871"

def get_asset_group_details(client, customer_id, account_name):
    """Get detailed configuration for H&S and Christmas asset groups."""
    ga_service = client.get_service("GoogleAdsService")

    # Get asset groups - split queries to avoid OR issues
    queries = []

    queries.append("""
        SELECT
            campaign.id,
            campaign.name,
            asset_group.id,
            asset_group.name,
            asset_group.status,
            asset_group.final_urls,
            asset_group.final_mobile_urls,
            asset_group.path1,
            asset_group.path2
        FROM asset_group
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
            AND campaign.name LIKE '%H&S%'
            AND asset_group.status != 'REMOVED'
        ORDER BY campaign.name, asset_group.name
    """)

    queries.append("""
        SELECT
            campaign.id,
            campaign.name,
            asset_group.id,
            asset_group.name,
            asset_group.status,
            asset_group.final_urls,
            asset_group.final_mobile_urls,
            asset_group.path1,
            asset_group.path2
        FROM asset_group
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
            AND campaign.name LIKE '%Christmas%'
            AND asset_group.status != 'REMOVED'
        ORDER BY campaign.name, asset_group.name
    """)

    asset_groups = {}
    for query in queries:
        try:
            response = ga_service.search(customer_id=customer_id, query=query)
            for row in response:
                ag_id = row.asset_group.id
                if ag_id not in asset_groups:  # Avoid duplicates
                    asset_groups[ag_id] = {
                        'campaign_id': row.campaign.id,
                        'campaign': row.campaign.name,
                        'asset_group_id': ag_id,
                        'asset_group': row.asset_group.name,
                        'status': row.asset_group.status.name,
                        'final_urls': list(row.asset_group.final_urls) if row.asset_group.final_urls else [],
                        'final_mobile_urls': list(row.asset_group.final_mobile_urls) if row.asset_group.final_mobile_urls else [],
                        'path1': row.asset_group.path1 if hasattr(row.asset_group, 'path1') else '',
                        'path2': row.asset_group.path2 if hasattr(row.asset_group, 'path2') else '',
                        'listing_groups': [],
                        'search_themes': [],
                        'audience_signals': []
                    }
        except GoogleAdsException as ex:
            print(f"Error fetching asset groups: {ex}")
            continue

    # Get listing groups (product groups) - only for asset groups we have
    if not asset_groups:
        return asset_groups

    ag_ids = ','.join(str(ag_id) for ag_id in asset_groups.keys())
    listing_groups_query = f"""
        SELECT
            asset_group.id,
            asset_group_listing_group_filter.type
        FROM asset_group_listing_group_filter
        WHERE asset_group.id IN ({ag_ids})
        ORDER BY asset_group.id
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=listing_groups_query)
        for row in response:
            ag_id = row.asset_group.id
            if ag_id in asset_groups:
                filter_type = row.asset_group_listing_group_filter.type.name
                listing_info = {'type': filter_type}
                asset_groups[ag_id]['listing_groups'].append(listing_info)
    except GoogleAdsException as ex:
        print(f"Error fetching listing groups: {ex}")

    # Get search themes
    search_themes_query = f"""
        SELECT
            asset_group.id,
            asset_group_signal.search_theme.text
        FROM asset_group_signal
        WHERE asset_group.id IN ({ag_ids})
            AND asset_group_signal.search_theme.text IS NOT NULL
        ORDER BY asset_group.id
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=search_themes_query)
        for row in response:
            ag_id = row.asset_group.id
            if ag_id in asset_groups:
                theme_text = row.asset_group_signal.search_theme.text
                if theme_text and theme_text not in asset_groups[ag_id]['search_themes']:
                    asset_groups[ag_id]['search_themes'].append(theme_text)
    except GoogleAdsException as ex:
        print(f"Error fetching search themes: {ex}")

    # Get audience signals
    audience_query = f"""
        SELECT
            asset_group.id,
            asset_group_signal.audience.audience
        FROM asset_group_signal
        WHERE asset_group.id IN ({ag_ids})
            AND asset_group_signal.audience.audience IS NOT NULL
        ORDER BY asset_group.id
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=audience_query)
        for row in response:
            ag_id = row.asset_group.id
            if ag_id in asset_groups:
                audience = row.asset_group_signal.audience.audience
                if audience and audience not in asset_groups[ag_id]['audience_signals']:
                    asset_groups[ag_id]['audience_signals'].append(audience)
    except GoogleAdsException as ex:
        print(f"Error fetching audience signals: {ex}")

    return asset_groups

def print_detailed_analysis(account_name, asset_groups):
    """Print detailed asset group configuration."""
    print(f"\n{'='*120}")
    print(f"{account_name} - DETAILED ASSET GROUP CONFIGURATION")
    print(f"{'='*120}")

    if not asset_groups:
        print("\nNo asset groups found.")
        return

    # Group by campaign
    campaigns = {}
    for ag_id, ag_data in asset_groups.items():
        camp = ag_data['campaign']
        if camp not in campaigns:
            campaigns[camp] = []
        campaigns[camp].append(ag_data)

    for campaign, ags in sorted(campaigns.items()):
        print(f"\n{'─'*120}")
        print(f"📊 Campaign: {campaign}")
        print(f"{'─'*120}")

        for ag in sorted(ags, key=lambda x: x['asset_group']):
            status_emoji = "✅" if ag['status'] == 'ENABLED' else "⏸️" if ag['status'] == 'PAUSED' else "🔴"
            print(f"\n  {status_emoji} Asset Group: {ag['asset_group']} (ID: {ag['asset_group_id']})")
            print(f"     Status: {ag['status']}")

            # Final URLs
            if ag['final_urls']:
                print(f"     Final URL: {ag['final_urls'][0]}")
            if ag['path1'] or ag['path2']:
                print(f"     Display Path: /{ag['path1']}/{ag['path2']}")

            # Listing Groups (Product Groups)
            if ag['listing_groups']:
                print(f"\n     📦 Listing Groups: {len(ag['listing_groups'])} filters configured")
                types = [lg['type'] for lg in ag['listing_groups']]
                print(f"        Types: {', '.join(set(types))}")
            else:
                print(f"\n     📦 Listing Groups: None (all products)")

            # Search Themes
            if ag['search_themes']:
                print(f"\n     🔍 Search Themes ({len(ag['search_themes'])}):")
                for i, theme in enumerate(ag['search_themes'], 1):
                    print(f"        {i}. {theme}")
            else:
                print(f"\n     🔍 Search Themes: None")

            # Audience Signals
            if ag['audience_signals']:
                print(f"\n     👥 Audience Signals ({len(ag['audience_signals'])}):")
                for i, aud in enumerate(ag['audience_signals'], 1):
                    print(f"        {i}. {aud}")
            else:
                print(f"\n     👥 Audience Signals: None")

def compare_listing_groups(uk_data, usa_data):
    """Compare listing group configurations between UK and USA."""
    print(f"\n{'='*120}")
    print("LISTING GROUP COMPARISON - UK vs USA")
    print(f"{'='*120}")

    # Compare by asset group name (since they should align now)
    uk_by_name = {}
    for ag_id, ag_data in uk_data.items():
        name = ag_data['asset_group']
        uk_by_name[name] = ag_data

    usa_by_name = {}
    for ag_id, ag_data in usa_data.items():
        name = ag_data['asset_group']
        usa_by_name[name] = ag_data

    all_names = sorted(set(uk_by_name.keys()) | set(usa_by_name.keys()))

    for name in all_names:
        uk_ag = uk_by_name.get(name)
        usa_ag = usa_by_name.get(name)

        if uk_ag and usa_ag:
            # Both have this asset group - compare
            uk_lg_count = len(uk_ag['listing_groups'])
            usa_lg_count = len(usa_ag['listing_groups'])

            uk_st_count = len(uk_ag['search_themes'])
            usa_st_count = len(usa_ag['search_themes'])

            if uk_lg_count != usa_lg_count or uk_st_count != usa_st_count:
                print(f"\n⚠️  DIFFERENCE: {name}")
                print(f"   UK:  {uk_lg_count} listing groups, {uk_st_count} search themes")
                print(f"   USA: {usa_lg_count} listing groups, {usa_st_count} search themes")

                if uk_lg_count != usa_lg_count:
                    print(f"\n   UK Listing Groups:")
                    for lg in uk_ag['listing_groups']:
                        print(f"      - {lg['type']}: {lg.get('custom_label', 'N/A')} = {lg.get('custom_label_value', 'ALL')}")
                    print(f"\n   USA Listing Groups:")
                    for lg in usa_ag['listing_groups']:
                        print(f"      - {lg['type']}: {lg.get('custom_label', 'N/A')} = {lg.get('custom_label_value', 'ALL')}")

def main():
    google_ads_yaml = os.path.expanduser("~/google-ads.yaml")
    client = GoogleAdsClient.load_from_storage(google_ads_yaml)

    print("\n" + "="*120)
    print("SMYTHSON PMAX ASSET GROUP DETAILED ANALYSIS")
    print("="*120)
    print("\nAnalyzing:")
    print("  - Listing Groups (Product Groups)")
    print("  - Search Themes")
    print("  - Audience Signals")
    print("  - Final URLs")

    # Get UK details
    print("\n\nFetching UK asset group details...")
    uk_data = get_asset_group_details(client, UK_ACCOUNT, "UK")
    print_detailed_analysis("UK", uk_data)

    # Get USA details
    print("\n\nFetching USA asset group details...")
    usa_data = get_asset_group_details(client, USA_ACCOUNT, "USA")
    print_detailed_analysis("USA", usa_data)

    # Compare
    compare_listing_groups(uk_data, usa_data)

    print("\n" + "="*120)
    print("ANALYSIS COMPLETE")
    print("="*120)

if __name__ == "__main__":
    main()
