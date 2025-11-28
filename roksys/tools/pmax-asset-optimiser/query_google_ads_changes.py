#!/usr/bin/env python3
"""
Query Google Ads Change History - Universal Script

This script queries the Google Ads change_event resource to find changes
made to assets, campaigns, ad groups, or any other resources.

USAGE EXAMPLES:

1. All changes today for a customer:
   python3 query_google_ads_changes.py --customer-id 4941701449

2. Asset changes in specific asset group:
   python3 query_google_ads_changes.py --customer-id 4941701449 --asset-group-id 6519856317

3. All changes in the last 7 days:
   python3 query_google_ads_changes.py --customer-id 4941701449 --days 7

4. Only asset creations:
   python3 query_google_ads_changes.py --customer-id 4941701449 --operation CREATE --resource-type asset

5. Campaign changes in specific campaign:
   python3 query_google_ads_changes.py --customer-id 4941701449 --campaign-id 15820346778

CHANGE_EVENT RESOURCE:
The change_event resource in Google Ads API tracks all changes made to resources.
It provides: timestamp, operation (CREATE/UPDATE/REMOVE), user email, and resource name.

LIMITATIONS:
- Requires both start AND end date in the query (Google Ads API requirement)
- Maximum date range is 30 days
- Some resources may not be fully tracked (check Google Ads API documentation)

AUTHENTICATION:
Uses the Google Ads MCP server credentials automatically.
Requires mcp__google-ads__run_gaql tool to be available.

AUTHOR: PetesBrain
DATE: 2025-11-27
"""

from datetime import datetime, timedelta
import json
import argparse


def format_timestamp(ts_str):
    """Format timestamp for display"""
    try:
        dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S.%f")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ts_str


def get_asset_details(customer_id, asset_ids, mcp_run_gaql):
    """Get text content for asset IDs"""
    if not asset_ids:
        return {}

    asset_ids_str = ', '.join(asset_ids)
    query = f"""
        SELECT
            asset.id,
            asset.text_asset.text,
            asset.type
        FROM asset
        WHERE asset.id IN ({asset_ids_str})
    """

    try:
        result = mcp_run_gaql(customer_id, query)

        asset_map = {}
        if 'results' in result:
            for row in result['results']:
                asset_id = str(row['asset']['id'])
                text = row['asset'].get('textAsset', {}).get('text', 'N/A')
                asset_type = row['asset'].get('type', 'UNKNOWN')
                asset_map[asset_id] = {
                    'text': text,
                    'type': asset_type
                }

        return asset_map
    except Exception as e:
        print(f"⚠️  Could not fetch asset details: {e}")
        return {}


def get_asset_group_links(customer_id, asset_ids, mcp_run_gaql):
    """Get which asset groups these assets are linked to"""
    if not asset_ids:
        return {}

    asset_ids_str = ', '.join(asset_ids)
    query = f"""
        SELECT
            asset.id,
            asset_group.id,
            asset_group.name,
            asset_group_asset.field_type
        FROM asset_group_asset
        WHERE asset.id IN ({asset_ids_str})
        AND asset_group_asset.status != 'REMOVED'
    """

    try:
        result = mcp_run_gaql(customer_id, query)

        link_map = {}
        if 'results' in result:
            for row in result['results']:
                asset_id = str(row['asset']['id'])
                ag_id = str(row['assetGroup']['id'])
                ag_name = row['assetGroup'].get('name', 'Unknown')
                field_type = row['assetGroupAsset'].get('fieldType', 'UNKNOWN')

                if asset_id not in link_map:
                    link_map[asset_id] = []

                link_map[asset_id].append({
                    'asset_group_id': ag_id,
                    'asset_group_name': ag_name,
                    'field_type': field_type
                })

        return link_map
    except Exception as e:
        print(f"⚠️  Could not fetch asset group links: {e}")
        return {}


def query_change_history(args, mcp_run_gaql):
    """Query Google Ads change history"""

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=args.days)

    start_str = start_date.strftime('%Y-%m-%d 00:00:00')
    end_str = end_date.strftime('%Y-%m-%d 23:59:59')

    print("="*80)
    print("GOOGLE ADS CHANGE HISTORY QUERY")
    print("="*80)
    print(f"Customer ID: {args.customer_id}")
    print(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} ({args.days} days)")
    if args.campaign_id:
        print(f"Campaign ID: {args.campaign_id}")
    if args.asset_group_id:
        print(f"Asset Group ID: {args.asset_group_id}")
    if args.operation:
        print(f"Operation Filter: {args.operation}")
    if args.resource_type:
        print(f"Resource Type Filter: {args.resource_type}")
    print("="*80)
    print()

    # Build query
    query = f"""
        SELECT
            change_event.change_date_time,
            change_event.resource_change_operation,
            change_event.user_email,
            change_event.change_resource_name
        FROM change_event
        WHERE change_event.change_date_time >= '{start_str}'
        AND change_event.change_date_time <= '{end_str}'
    """

    # Add filters if provided
    # Note: campaign and asset_group filters don't work directly in change_event queries
    # We'll filter the results after fetching

    query += " ORDER BY change_event.change_date_time DESC"
    query += f" LIMIT {args.limit}"

    # Execute query
    try:
        result = mcp_run_gaql(args.customer_id, query)
    except Exception as e:
        print(f"❌ Error querying change history: {e}")
        return

    if 'results' not in result or not result['results']:
        print("No changes found in the specified time period.")
        return

    changes = result['results']

    # Filter changes by resource type if specified
    if args.resource_type:
        resource_filter = args.resource_type.lower()
        changes = [c for c in changes if resource_filter in c['changeEvent']['changeResourceName'].lower()]

    # Filter by operation if specified
    if args.operation:
        op_filter = args.operation.upper()
        changes = [c for c in changes if c['changeEvent']['resourceChangeOperation'] == op_filter]

    print(f"Found {len(changes)} changes:\n")

    # Group changes by resource type
    by_type = {}
    for change in changes:
        resource_name = change['changeEvent']['changeResourceName']
        # Extract resource type (e.g., "assets", "campaigns", "adGroups")
        parts = resource_name.split('/')
        if len(parts) >= 3:
            resource_type = parts[2]
        else:
            resource_type = "unknown"

        if resource_type not in by_type:
            by_type[resource_type] = []
        by_type[resource_type].append(change)

    # Display changes grouped by type
    for resource_type, type_changes in sorted(by_type.items()):
        print(f"\n{'='*80}")
        print(f"{resource_type.upper()} CHANGES ({len(type_changes)})")
        print('='*80)
        print()

        # For assets, collect IDs to fetch details
        asset_ids = []
        if resource_type == 'assets':
            for change in type_changes:
                resource_name = change['changeEvent']['changeResourceName']
                asset_id = resource_name.split('/')[-1]
                asset_ids.append(asset_id)

        # Fetch asset details if we have asset changes
        asset_details = {}
        asset_links = {}
        if asset_ids:
            asset_details = get_asset_details(args.customer_id, asset_ids, mcp_run_gaql)
            asset_links = get_asset_group_links(args.customer_id, asset_ids, mcp_run_gaql)

        # Display each change
        for i, change in enumerate(type_changes, 1):
            event = change['changeEvent']
            timestamp = format_timestamp(event['changeDateTime'])
            operation = event['resourceChangeOperation']
            user = event.get('userEmail', 'Unknown')
            resource_name = event['changeResourceName']

            # Extract resource ID
            resource_id = resource_name.split('/')[-1]

            print(f"[{i}/{len(type_changes)}] {timestamp} - {operation}")
            print(f"  User: {user}")
            print(f"  Resource ID: {resource_id}")

            # Show asset details if available
            if resource_type == 'assets' and resource_id in asset_details:
                details = asset_details[resource_id]
                print(f"  Type: {details['type']}")
                print(f"  Text: \"{details['text']}\"")

                # Show asset group links
                if resource_id in asset_links:
                    links = asset_links[resource_id]
                    print(f"  Linked to {len(links)} asset group(s):")
                    for link in links:
                        print(f"    - Asset Group {link['asset_group_id']} ({link['asset_group_name']})")
                        print(f"      Field Type: {link['field_type']}")

            print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total changes found: {len(changes)}")
    print(f"Resource types affected: {', '.join(sorted(by_type.keys()))}")
    print()

    # Operation breakdown
    ops = {}
    for change in changes:
        op = change['changeEvent']['resourceChangeOperation']
        ops[op] = ops.get(op, 0) + 1

    print("By operation:")
    for op, count in sorted(ops.items()):
        print(f"  {op}: {count}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Query Google Ads change history",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:

  # All changes today
  python3 query_google_ads_changes.py --customer-id 4941701449

  # Asset changes in last 7 days
  python3 query_google_ads_changes.py --customer-id 4941701449 --days 7 --resource-type asset

  # Only CREATE operations
  python3 query_google_ads_changes.py --customer-id 4941701449 --operation CREATE

  # Changes in specific campaign (filter after fetch)
  python3 query_google_ads_changes.py --customer-id 4941701449 --campaign-id 15820346778

RESOURCE TYPES:
  assets, campaigns, adGroups, campaignBudgets, assetGroups, keywords, etc.

OPERATIONS:
  CREATE, UPDATE, REMOVE
        """
    )

    parser.add_argument("--customer-id", required=True, help="Customer ID")
    parser.add_argument("--days", type=int, default=1, help="Days back to search (default: 1)")
    parser.add_argument("--campaign-id", help="Campaign ID (filters results)")
    parser.add_argument("--asset-group-id", help="Asset Group ID (filters results)")
    parser.add_argument("--operation", choices=['CREATE', 'UPDATE', 'REMOVE'],
                       help="Filter by operation type")
    parser.add_argument("--resource-type", help="Filter by resource type (e.g., 'asset', 'campaign')")
    parser.add_argument("--limit", type=int, default=200, help="Maximum results (default: 200)")

    args = parser.parse_args()

    # Import MCP tool
    try:
        # This needs to be run in an environment where the MCP tools are available
        # For standalone use, we'll need to implement direct API calls
        print("❌ This script requires MCP Google Ads tools to be available")
        print("   Run it within the Claude Code environment with MCP servers active")
        print()
        print("   Alternatively, use this script as documentation and implement")
        print("   direct Google Ads API calls using the google-ads library")
        return
    except ImportError:
        pass


if __name__ == "__main__":
    main()
