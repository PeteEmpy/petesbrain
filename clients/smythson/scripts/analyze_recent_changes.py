#!/usr/bin/env python3
"""
Analyze recent changes to Smythson PMax campaigns in the last 90 minutes.
Focus on H&S and Christmas Gifting campaigns.
"""

import os
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

UK_ACCOUNT = "8573235780"
USA_ACCOUNT = "7808690871"

def get_change_history(client, customer_id, account_name):
    """Get change history for the last 90 minutes."""
    ga_service = client.get_service("GoogleAdsService")

    # Last 90 minutes
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=90)

    # Format for Google Ads API (YYYY-MM-DD HH:MM:SS)
    start_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

    query = f"""
        SELECT
            change_event.change_date_time,
            change_event.change_resource_type,
            change_event.change_resource_name,
            change_event.user_email,
            change_event.client_type,
            change_event.old_resource,
            change_event.new_resource,
            change_event.resource_change_operation,
            campaign.id,
            campaign.name
        FROM change_event
        WHERE change_event.change_date_time >= '{start_str}'
            AND change_event.change_date_time <= '{end_str}'
            AND change_event.change_resource_type IN ('ASSET_GROUP', 'CAMPAIGN')
            AND (
                campaign.name LIKE '%H&S%'
                OR campaign.name LIKE '%Christmas%'
            )
        ORDER BY change_event.change_date_time DESC
    """

    changes = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            changes.append({
                'timestamp': row.change_event.change_date_time,
                'resource_type': row.change_event.change_resource_type.name,
                'resource_name': row.change_event.change_resource_name,
                'operation': row.change_event.resource_change_operation.name,
                'user_email': row.change_event.user_email,
                'campaign_id': row.campaign.id if hasattr(row, 'campaign') else None,
                'campaign_name': row.campaign.name if hasattr(row, 'campaign') else None,
                'old_resource': row.change_event.old_resource if hasattr(row.change_event, 'old_resource') else None,
                'new_resource': row.change_event.new_resource if hasattr(row.change_event, 'new_resource') else None,
            })
    except GoogleAdsException as ex:
        print(f"Error fetching change history for {account_name}: {ex}")
        return []

    return changes

def print_changes(account_name, changes):
    """Print formatted change history."""
    print(f"\n{'='*120}")
    print(f"{account_name} - CHANGE HISTORY (Last 90 Minutes)")
    print(f"{'='*120}")

    if not changes:
        print("\nNo changes found in the last 90 minutes for PMax H&S or Christmas campaigns.")
        return

    print(f"\nTotal Changes Found: {len(changes)}")
    print(f"{'─'*120}\n")

    for i, change in enumerate(changes, 1):
        timestamp = change['timestamp']
        print(f"#{i} | {timestamp} | {change['operation']}")
        print(f"    Resource Type: {change['resource_type']}")
        print(f"    Campaign: {change['campaign_name']} (ID: {change['campaign_id']})")
        print(f"    Resource: {change['resource_name']}")
        print(f"    User: {change['user_email']}")
        print(f"{'─'*120}\n")

def get_current_asset_groups(client, customer_id, campaign_name_filter):
    """Get current asset groups for comparison."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            asset_group.id,
            asset_group.name,
            asset_group.status
        FROM asset_group
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
            AND campaign.name LIKE '%{campaign_name_filter}%'
        ORDER BY campaign.name, asset_group.name
    """

    results = []
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        for row in response:
            results.append({
                'campaign_id': row.campaign.id,
                'campaign': row.campaign.name,
                'asset_group_id': row.asset_group.id,
                'asset_group': row.asset_group.name,
                'status': row.asset_group.status.name
            })
    except GoogleAdsException as ex:
        print(f"Error: {ex}")
        return []

    return results

def main():
    google_ads_yaml = os.path.expanduser("~/google-ads.yaml")
    client = GoogleAdsClient.load_from_storage(google_ads_yaml)

    print("\n" + "="*120)
    print("SMYTHSON PMAX CAMPAIGN CHANGES - LAST 90 MINUTES")
    print("="*120)
    print(f"\nAnalysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Focusing on: PMax H&S and PMax Christmas Gifting campaigns")

    # Get change history for UK
    print("\n\n" + "="*120)
    print("FETCHING UK CHANGE HISTORY...")
    print("="*120)
    uk_changes = get_change_history(client, UK_ACCOUNT, "UK")
    print_changes("UK", uk_changes)

    # Get change history for USA
    print("\n\n" + "="*120)
    print("FETCHING USA CHANGE HISTORY...")
    print("="*120)
    usa_changes = get_change_history(client, USA_ACCOUNT, "USA")
    print_changes("USA", usa_changes)

    # Get current state for comparison
    print("\n\n" + "="*120)
    print("CURRENT STATE - UK CAMPAIGNS")
    print("="*120)

    for campaign_filter in ['H&S', 'Christmas']:
        uk_current = get_current_asset_groups(client, UK_ACCOUNT, campaign_filter)
        if uk_current:
            print(f"\n{campaign_filter} Campaigns:")
            campaigns = {}
            for ag in uk_current:
                camp = ag['campaign']
                if camp not in campaigns:
                    campaigns[camp] = []
                campaigns[camp].append(ag)

            for camp, ags in campaigns.items():
                print(f"\n  Campaign: {camp}")
                for ag in ags:
                    status_emoji = "✅" if ag['status'] == 'ENABLED' else "⏸️" if ag['status'] == 'PAUSED' else "🔴"
                    print(f"    {status_emoji} {ag['asset_group']} (Status: {ag['status']})")

    print("\n\n" + "="*120)
    print("CURRENT STATE - USA CAMPAIGNS")
    print("="*120)

    for campaign_filter in ['H&S', 'Christmas']:
        usa_current = get_current_asset_groups(client, USA_ACCOUNT, campaign_filter)
        if usa_current:
            print(f"\n{campaign_filter} Campaigns:")
            campaigns = {}
            for ag in usa_current:
                camp = ag['campaign']
                if camp not in campaigns:
                    campaigns[camp] = []
                campaigns[camp].append(ag)

            for camp, ags in campaigns.items():
                print(f"\n  Campaign: {camp}")
                for ag in ags:
                    status_emoji = "✅" if ag['status'] == 'ENABLED' else "⏸️" if ag['status'] == 'PAUSED' else "🔴"
                    print(f"    {status_emoji} {ag['asset_group']} (Status: {ag['status']})")

    print("\n" + "="*120)
    print("ANALYSIS COMPLETE")
    print("="*120)

if __name__ == "__main__":
    main()
