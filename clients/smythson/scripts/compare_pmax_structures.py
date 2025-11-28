#!/usr/bin/env python3
"""
Compare Performance Max campaign structures between Smythson UK and USA accounts.
Focus on gifting campaigns and asset group alignment.
"""

import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Account IDs from CONTEXT.md
UK_ACCOUNT = "8573235780"
USA_ACCOUNT = "7808690871"

def get_pmax_campaigns(client, customer_id):
    """Get all Performance Max campaigns for an account."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type
        FROM campaign
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
            AND campaign.status != 'REMOVED'
        ORDER BY campaign.name
    """

    campaigns = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            campaigns.append({
                'id': row.campaign.id,
                'name': row.campaign.name,
                'status': row.campaign.status.name
            })
    except GoogleAdsException as ex:
        print(f"Error fetching campaigns for {customer_id}: {ex}")
        return []

    return campaigns

def get_asset_groups(client, customer_id, campaign_id):
    """Get all asset groups for a Performance Max campaign."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            asset_group.id,
            asset_group.name,
            asset_group.status,
            asset_group.final_urls
        FROM asset_group
        WHERE campaign.id = {campaign_id}
            AND asset_group.status != 'REMOVED'
        ORDER BY asset_group.name
    """

    asset_groups = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            asset_groups.append({
                'id': row.asset_group.id,
                'name': row.asset_group.name,
                'status': row.asset_group.status.name,
                'final_urls': list(row.asset_group.final_urls) if row.asset_group.final_urls else []
            })
    except GoogleAdsException as ex:
        print(f"Error fetching asset groups for campaign {campaign_id}: {ex}")
        return []

    return asset_groups

def compare_structures(uk_data, usa_data):
    """Compare UK and USA structures and identify differences."""
    differences = []

    # Compare campaign counts
    uk_campaign_names = set(c['name'] for c in uk_data)
    usa_campaign_names = set(c['name'] for c in usa_data)

    # Campaigns in UK but not USA
    uk_only = uk_campaign_names - usa_campaign_names
    if uk_only:
        differences.append({
            'type': 'campaigns_uk_only',
            'items': sorted(uk_only)
        })

    # Campaigns in USA but not UK
    usa_only = usa_campaign_names - uk_campaign_names
    if usa_only:
        differences.append({
            'type': 'campaigns_usa_only',
            'items': sorted(usa_only)
        })

    # Compare asset groups for matching campaigns
    common_campaigns = uk_campaign_names & usa_campaign_names
    for campaign_name in sorted(common_campaigns):
        uk_campaign = next(c for c in uk_data if c['name'] == campaign_name)
        usa_campaign = next(c for c in usa_data if c['name'] == campaign_name)

        uk_ag_names = set(ag['name'] for ag in uk_campaign['asset_groups'])
        usa_ag_names = set(ag['name'] for ag in usa_campaign['asset_groups'])

        # Asset groups in UK but not USA
        uk_ag_only = uk_ag_names - usa_ag_names
        if uk_ag_only:
            differences.append({
                'type': 'asset_groups_uk_only',
                'campaign': campaign_name,
                'items': sorted(uk_ag_only)
            })

        # Asset groups in USA but not UK
        usa_ag_only = usa_ag_names - uk_ag_names
        if usa_ag_only:
            differences.append({
                'type': 'asset_groups_usa_only',
                'campaign': campaign_name,
                'items': sorted(usa_ag_only)
            })

    return differences

def main():
    # Initialize client
    google_ads_yaml = os.path.expanduser("~/google-ads.yaml")
    client = GoogleAdsClient.load_from_storage(google_ads_yaml)

    print("=" * 80)
    print("SMYTHSON PERFORMANCE MAX STRUCTURE COMPARISON")
    print("=" * 80)
    print()

    # Fetch UK campaigns
    print(f"Fetching UK Performance Max campaigns (Account: {UK_ACCOUNT})...")
    uk_campaigns = get_pmax_campaigns(client, UK_ACCOUNT)
    print(f"Found {len(uk_campaigns)} Performance Max campaigns in UK account\n")

    # Fetch USA campaigns
    print(f"Fetching USA Performance Max campaigns (Account: {USA_ACCOUNT})...")
    usa_campaigns = get_pmax_campaigns(client, USA_ACCOUNT)
    print(f"Found {len(usa_campaigns)} Performance Max campaigns in USA account\n")

    # Fetch asset groups for each campaign
    print("Fetching asset groups for UK campaigns...")
    uk_data = []
    for campaign in uk_campaigns:
        asset_groups = get_asset_groups(client, UK_ACCOUNT, campaign['id'])
        uk_data.append({
            **campaign,
            'asset_groups': asset_groups
        })
        print(f"  {campaign['name']}: {len(asset_groups)} asset groups")
    print()

    print("Fetching asset groups for USA campaigns...")
    usa_data = []
    for campaign in usa_campaigns:
        asset_groups = get_asset_groups(client, USA_ACCOUNT, campaign['id'])
        usa_data.append({
            **campaign,
            'asset_groups': asset_groups
        })
        print(f"  {campaign['name']}: {len(asset_groups)} asset groups")
    print()

    # Display UK structure
    print("=" * 80)
    print("UK ACCOUNT STRUCTURE")
    print("=" * 80)
    for campaign in uk_data:
        print(f"\nCampaign: {campaign['name']} (ID: {campaign['id']}, Status: {campaign['status']})")
        if campaign['asset_groups']:
            for ag in campaign['asset_groups']:
                print(f"  └─ Asset Group: {ag['name']} (ID: {ag['id']}, Status: {ag['status']})")
                if ag['final_urls']:
                    print(f"     URL: {ag['final_urls'][0]}")
        else:
            print("  └─ No asset groups")
    print()

    # Display USA structure
    print("=" * 80)
    print("USA ACCOUNT STRUCTURE")
    print("=" * 80)
    for campaign in usa_data:
        print(f"\nCampaign: {campaign['name']} (ID: {campaign['id']}, Status: {campaign['status']})")
        if campaign['asset_groups']:
            for ag in campaign['asset_groups']:
                print(f"  └─ Asset Group: {ag['name']} (ID: {ag['id']}, Status: {ag['status']})")
                if ag['final_urls']:
                    print(f"     URL: {ag['final_urls'][0]}")
        else:
            print("  └─ No asset groups")
    print()

    # Compare and display differences
    print("=" * 80)
    print("STRUCTURAL DIFFERENCES")
    print("=" * 80)
    differences = compare_structures(uk_data, usa_data)

    if not differences:
        print("\n✅ No structural differences found. UK and USA accounts have identical PMAX structures.")
    else:
        print()
        for diff in differences:
            if diff['type'] == 'campaigns_uk_only':
                print("❌ Campaigns in UK but NOT in USA:")
                for item in diff['items']:
                    print(f"   - {item}")
                print()
            elif diff['type'] == 'campaigns_usa_only':
                print("❌ Campaigns in USA but NOT in UK:")
                for item in diff['items']:
                    print(f"   - {item}")
                print()
            elif diff['type'] == 'asset_groups_uk_only':
                print(f"❌ Asset Groups in UK but NOT in USA (Campaign: {diff['campaign']}):")
                for item in diff['items']:
                    print(f"   - {item}")
                print()
            elif diff['type'] == 'asset_groups_usa_only':
                print(f"❌ Asset Groups in USA but NOT in UK (Campaign: {diff['campaign']}):")
                for item in diff['items']:
                    print(f"   - {item}")
                print()

    # Focus on gifting-related campaigns
    print("=" * 80)
    print("GIFTING CAMPAIGNS ANALYSIS")
    print("=" * 80)
    print()

    uk_gifting = [c for c in uk_data if 'gift' in c['name'].lower() or 'christmas' in c['name'].lower()]
    usa_gifting = [c for c in usa_data if 'gift' in c['name'].lower() or 'christmas' in c['name'].lower()]

    print(f"UK Gifting/Christmas Campaigns: {len(uk_gifting)}")
    for campaign in uk_gifting:
        print(f"  - {campaign['name']} ({len(campaign['asset_groups'])} asset groups)")
    print()

    print(f"USA Gifting/Christmas Campaigns: {len(usa_gifting)}")
    for campaign in usa_gifting:
        print(f"  - {campaign['name']} ({len(campaign['asset_groups'])} asset groups)")
    print()

    if len(uk_gifting) != len(usa_gifting):
        print("⚠️ ALERT: Different number of gifting campaigns between UK and USA")

    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
