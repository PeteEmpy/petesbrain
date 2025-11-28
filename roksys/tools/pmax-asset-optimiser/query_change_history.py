#!/usr/bin/env python3
"""
Query Google Ads Change History to find asset changes

This script queries the change_event resource to find recent changes
to assets in a specific campaign or asset group.
"""

import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

from google.ads.googleads.client import GoogleAdsClient
from oauth.google_auth import get_oauth_credentials
from datetime import datetime, timedelta

def query_change_history(customer_id, campaign_id=None, asset_group_id=None, days_back=1):
    """Query change history for assets"""

    # Get credentials
    creds = get_oauth_credentials()
    client = GoogleAdsClient.load_from_dict({
        'developer_token': 'VrzEP-PTSY01pm1BJidERQ',
        'use_proto_plus': True
    }, credentials=creds)

    ga_service = client.get_service("GoogleAdsService")

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    date_filter = f"change_date_time >= '{start_date.strftime('%Y-%m-%d')}' AND change_date_time <= '{end_date.strftime('%Y-%m-%d')}'"

    # Build query
    query = f"""
        SELECT
            change_event.change_date_time,
            change_event.change_resource_type,
            change_event.change_resource_name,
            change_event.user_email,
            change_event.old_resource.asset_group_asset.asset,
            change_event.new_resource.asset_group_asset.asset,
            change_event.old_resource.asset_group_asset.asset_group,
            change_event.new_resource.asset_group_asset.asset_group,
            change_event.old_resource.asset_group_asset.field_type,
            change_event.new_resource.asset_group_asset.field_type,
            change_event.resource_change_operation
        FROM change_event
        WHERE {date_filter}
        AND change_event.change_resource_type = 'ASSET_GROUP_ASSET'
    """

    if campaign_id:
        query += f" AND campaign.id = {campaign_id}"

    if asset_group_id:
        query += f" AND asset_group.id = {asset_group_id}"

    query += " ORDER BY change_event.change_date_time DESC"

    print("="*80)
    print("GOOGLE ADS CHANGE HISTORY - ASSET CHANGES")
    print("="*80)
    print(f"Customer ID: {customer_id}")
    if campaign_id:
        print(f"Campaign ID: {campaign_id}")
    if asset_group_id:
        print(f"Asset Group ID: {asset_group_id}")
    print(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print("="*80)
    print()

    try:
        response = ga_service.search(customer_id=customer_id, query=query)

        changes = []
        for row in response:
            changes.append(row)

        if not changes:
            print("No asset changes found in the specified time period.")
            return

        print(f"Found {len(changes)} asset changes:\n")

        for i, row in enumerate(changes, 1):
            event = row.change_event

            timestamp = event.change_date_time
            operation = event.resource_change_operation
            user = event.user_email if event.user_email else "Unknown"

            print(f"Change #{i}")
            print(f"  Timestamp: {timestamp}")
            print(f"  Operation: {operation}")
            print(f"  User: {user}")

            # Get asset information
            if operation == "CREATE":
                new_asset = event.new_resource.asset_group_asset.asset if hasattr(event.new_resource, 'asset_group_asset') else None
                asset_group = event.new_resource.asset_group_asset.asset_group if hasattr(event.new_resource, 'asset_group_asset') else None
                field_type = event.new_resource.asset_group_asset.field_type if hasattr(event.new_resource, 'asset_group_asset') else None

                if new_asset:
                    asset_id = new_asset.split('/')[-1]
                    print(f"  Asset ID: {asset_id}")
                if asset_group:
                    ag_id = asset_group.split('/')[-1]
                    print(f"  Asset Group: {ag_id}")
                if field_type:
                    print(f"  Field Type: {field_type}")

            elif operation == "REMOVE":
                old_asset = event.old_resource.asset_group_asset.asset if hasattr(event.old_resource, 'asset_group_asset') else None
                asset_group = event.old_resource.asset_group_asset.asset_group if hasattr(event.old_resource, 'asset_group_asset') else None
                field_type = event.old_resource.asset_group_asset.field_type if hasattr(event.old_resource, 'asset_group_asset') else None

                if old_asset:
                    asset_id = old_asset.split('/')[-1]
                    print(f"  Asset ID: {asset_id}")
                if asset_group:
                    ag_id = asset_group.split('/')[-1]
                    print(f"  Asset Group: {ag_id}")
                if field_type:
                    print(f"  Field Type: {field_type}")

            print()

        # Now get the actual asset text for the IDs we found
        print("\n" + "="*80)
        print("ASSET DETAILS")
        print("="*80)
        print()

        asset_ids = set()
        for row in changes:
            event = row.change_event
            operation = event.resource_change_operation

            if operation == "CREATE" and hasattr(event.new_resource, 'asset_group_asset'):
                asset_path = event.new_resource.asset_group_asset.asset
                if asset_path:
                    asset_ids.add(asset_path.split('/')[-1])
            elif operation == "REMOVE" and hasattr(event.old_resource, 'asset_group_asset'):
                asset_path = event.old_resource.asset_group_asset.asset
                if asset_path:
                    asset_ids.add(asset_path.split('/')[-1])

        if asset_ids:
            asset_query = f"""
                SELECT
                    asset.id,
                    asset.text_asset.text,
                    asset.type
                FROM asset
                WHERE asset.id IN ({','.join(asset_ids)})
            """

            asset_response = ga_service.search(customer_id=customer_id, query=asset_query)

            for row in asset_response:
                asset_id = row.asset.id
                text = row.asset.text_asset.text if hasattr(row.asset, 'text_asset') else "N/A"
                print(f"Asset {asset_id}:")
                print(f"  Text: \"{text}\"")
                print()

    except Exception as e:
        print(f"❌ Error querying change history: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Query Google Ads change history for asset changes")
    parser.add_argument("--customer-id", required=True, help="Customer ID")
    parser.add_argument("--campaign-id", help="Campaign ID (optional)")
    parser.add_argument("--asset-group-id", help="Asset Group ID (optional)")
    parser.add_argument("--days", type=int, default=1, help="Days back to search (default: 1)")

    args = parser.parse_args()

    query_change_history(
        args.customer_id,
        args.campaign_id,
        args.asset_group_id,
        args.days
    )
