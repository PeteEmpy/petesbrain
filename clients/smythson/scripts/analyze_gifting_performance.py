#!/usr/bin/env python3
"""
Analyze gifting asset group performance to inform campaign structure decision.
Compare performance of gifting asset groups in different campaigns.
"""

import os
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

UK_ACCOUNT = "8573235780"
USA_ACCOUNT = "7808690871"

def analyze_asset_group_performance(client, customer_id, account_name):
    """Get performance data for gifting-related asset groups."""
    ga_service = client.get_service("GoogleAdsService")

    # Last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Split queries to avoid complex OR conditions
    queries = []

    # Query 1: Asset groups with "Gift" in name
    queries.append(f"""
        SELECT
            campaign.id,
            campaign.name,
            asset_group.id,
            asset_group.name,
            asset_group.status,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_micros
        FROM asset_group
        WHERE segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'
            AND campaign.advertising_channel_type = 'PERFORMANCE_MAX'
            AND campaign.status = 'ENABLED'
            AND asset_group.status = 'ENABLED'
            AND asset_group.name LIKE '%Gift%'
    """)

    # Query 2: Asset groups in Christmas campaigns
    queries.append(f"""
        SELECT
            campaign.id,
            campaign.name,
            asset_group.id,
            asset_group.name,
            asset_group.status,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_micros
        FROM asset_group
        WHERE segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}' AND '{end_date.strftime('%Y-%m-%d')}'
            AND campaign.advertising_channel_type = 'PERFORMANCE_MAX'
            AND campaign.status = 'ENABLED'
            AND asset_group.status = 'ENABLED'
            AND campaign.name LIKE '%Christmas%'
    """)

    results = []
    seen = set()  # Track unique asset groups

    for query in queries:
        try:
            response = ga_service.search(customer_id=customer_id, query=query)
            for row in response:
                # Use asset group ID as unique key
                ag_key = row.asset_group.id
                if ag_key in seen:
                    continue
                seen.add(ag_key)

                cost = row.metrics.cost_micros / 1_000_000
                revenue = row.metrics.conversions_value
                roas = (revenue / cost) if cost > 0 else 0

                results.append({
                    'campaign_id': row.campaign.id,
                    'campaign': row.campaign.name,
                    'asset_group_id': row.asset_group.id,
                    'asset_group': row.asset_group.name,
                    'status': row.asset_group.status.name,
                    'impressions': row.metrics.impressions,
                    'clicks': row.metrics.clicks,
                    'conversions': row.metrics.conversions,
                    'revenue': revenue,
                    'cost': cost,
                    'roas': roas
                })
        except GoogleAdsException as ex:
            print(f"Error: {ex}")
            continue

    return results

def print_analysis(account_name, results):
    """Print formatted analysis."""
    print(f"\n{'='*100}")
    print(f"{account_name} - GIFTING ASSET GROUP PERFORMANCE (Last 30 Days)")
    print(f"{'='*100}")

    if not results:
        print("No gifting asset groups found with performance data in the last 30 days.")
        return

    # Group by campaign
    campaigns = {}
    for r in results:
        camp = r['campaign']
        if camp not in campaigns:
            campaigns[camp] = []
        campaigns[camp].append(r)

    total_revenue = sum(r['revenue'] for r in results)
    total_cost = sum(r['cost'] for r in results)
    total_conversions = sum(r['conversions'] for r in results)

    for campaign, asset_groups in campaigns.items():
        print(f"\n📊 Campaign: {campaign}")
        print(f"{'─'*100}")

        campaign_revenue = sum(ag['revenue'] for ag in asset_groups)
        campaign_cost = sum(ag['cost'] for ag in asset_groups)
        campaign_roas = (campaign_revenue / campaign_cost) if campaign_cost > 0 else 0

        for ag in asset_groups:
            print(f"\n  Asset Group: {ag['asset_group']}")
            print(f"  Status: {ag['status']}")
            print(f"  Impressions: {ag['impressions']:,}")
            print(f"  Clicks: {ag['clicks']:,}")
            print(f"  Conversions: {ag['conversions']:.1f}")
            print(f"  Cost: £{ag['cost']:,.2f}" if 'UK' in account_name else f"  Cost: ${ag['cost']:,.2f}")
            print(f"  Revenue: £{ag['revenue']:,.2f}" if 'UK' in account_name else f"  Revenue: ${ag['revenue']:,.2f}")
            print(f"  ROAS: {ag['roas']:.2f}x ({ag['roas']*100:.0f}%)")

            # Show percentage of total gifting revenue
            pct = (ag['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            print(f"  % of Total Gifting Revenue: {pct:.1f}%")

        print(f"\n  Campaign Totals:")
        print(f"  Campaign Revenue: £{campaign_revenue:,.2f}" if 'UK' in account_name else f"  Campaign Revenue: ${campaign_revenue:,.2f}")
        print(f"  Campaign Cost: £{campaign_cost:,.2f}" if 'UK' in account_name else f"  Campaign Cost: ${campaign_cost:,.2f}")
        print(f"  Campaign ROAS: {campaign_roas:.2f}x ({campaign_roas*100:.0f}%)")

    print(f"\n{'─'*100}")
    print(f"TOTAL GIFTING PERFORMANCE:")
    print(f"Total Revenue: £{total_revenue:,.2f}" if 'UK' in account_name else f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Total Cost: £{total_cost:,.2f}" if 'UK' in account_name else f"Total Cost: ${total_cost:,.2f}")
    print(f"Total Conversions: {total_conversions:.1f}")
    total_roas = (total_revenue / total_cost) if total_cost > 0 else 0
    print(f"Overall ROAS: {total_roas:.2f}x ({total_roas*100:.0f}%)")
    print(f"{'='*100}\n")

def main():
    google_ads_yaml = os.path.expanduser("~/google-ads.yaml")
    client = GoogleAdsClient.load_from_storage(google_ads_yaml)

    print("\n" + "="*100)
    print("SMYTHSON GIFTING ASSET GROUP PERFORMANCE ANALYSIS")
    print("="*100)
    print("\nAnalyzing last 30 days of performance data...")
    print("This will show which gifting asset groups are performing and where they live.\n")

    # Analyze UK
    uk_results = analyze_asset_group_performance(client, UK_ACCOUNT, "UK")
    print_analysis("UK", uk_results)

    # Analyze USA
    usa_results = analyze_asset_group_performance(client, USA_ACCOUNT, "USA")
    print_analysis("USA", usa_results)

    # Comparison
    print("\n" + "="*100)
    print("STRATEGIC INSIGHTS")
    print("="*100)

    if uk_results and usa_results:
        uk_has_xmas_campaign = any('Christmas' in r['campaign'] for r in uk_results)
        usa_has_xmas_campaign = any('Christmas' in r['campaign'] for r in usa_results)

        uk_has_main_gifting = any('H&S' in r['campaign'] and 'Christmas' not in r['campaign'] for r in uk_results)
        usa_has_main_gifting = any('H&S' in r['campaign'] and 'Christmas' not in r['campaign'] for r in usa_results)

        print(f"\n📌 UK Structure:")
        print(f"  - Has Christmas Gifting Campaign: {'Yes' if uk_has_xmas_campaign else 'No'}")
        print(f"  - Has Gifting in Main H&S: {'Yes' if uk_has_main_gifting else 'No'}")

        print(f"\n📌 USA Structure:")
        print(f"  - Has Christmas Gifting Campaign: {'Yes' if usa_has_xmas_campaign else 'No'}")
        print(f"  - Has Gifting in Main H&S: {'Yes' if usa_has_main_gifting else 'No'}")

        # Calculate performance by campaign type
        uk_xmas_revenue = sum(r['revenue'] for r in uk_results if 'Christmas' in r['campaign'])
        uk_main_revenue = sum(r['revenue'] for r in uk_results if 'Christmas' not in r['campaign'])

        usa_xmas_revenue = sum(r['revenue'] for r in usa_results if 'Christmas' in r['campaign'])
        usa_main_revenue = sum(r['revenue'] for r in usa_results if 'Christmas' not in r['campaign'])

        print(f"\n💰 Revenue Split (Last 30 Days):")
        print(f"\n  UK:")
        print(f"    Christmas Campaign: £{uk_xmas_revenue:,.2f}")
        print(f"    Main H&S Campaign: £{uk_main_revenue:,.2f}")

        print(f"\n  USA:")
        print(f"    Christmas Campaign: ${usa_xmas_revenue:,.2f}")
        print(f"    Main H&S Campaign: ${usa_main_revenue:,.2f}")

        print("\n" + "="*100)
        print("\nRECOMMENDATION:")
        print("─"*100)
        print("\nBased on the performance data above:")
        print("1. If Christmas campaign is driving majority of gifting revenue → Keep separate")
        print("2. If main H&S gifting performs similarly → Consider consolidation")
        print("3. If both are strong → Hybrid approach (keep both, remove duplicates)")
        print("4. Look at ROAS differences between campaign types")
        print("\n" + "="*100)

if __name__ == "__main__":
    main()
