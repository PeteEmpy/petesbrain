#!/usr/bin/env python3
"""
Comprehensive brand vs non-brand analysis for UK + USA
Includes revenue, cost, clicks, and CPC for 2024 vs 2025
"""

import sys
import os

# Add MCP server path for OAuth imports
sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')
sys.path.append('/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/oauth')

from dotenv import load_dotenv
load_dotenv(dotenv_path='/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.env')

from google_auth import execute_gaql

def analyze_account(customer_id, manager_id, start_date, end_date, conversion_filter=None):
    """
    Analyze a single account for brand vs non-brand split
    """
    # Build query - we need separate queries for conversion-filtered vs full data
    if conversion_filter:
        # For conversion-filtered data, we can only get conversions_value
        query_revenue = f"""
        SELECT
          campaign.name,
          campaign.id,
          segments.conversion_action_name,
          metrics.conversions_value
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
          AND segments.conversion_action_name = '{conversion_filter}'
        """

        # Separate query for cost and clicks (all campaigns)
        query_cost = f"""
        SELECT
          campaign.name,
          campaign.id,
          metrics.cost_micros,
          metrics.clicks
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        """

        result_revenue = execute_gaql(customer_id, query_revenue, manager_id=manager_id)
        result_cost = execute_gaql(customer_id, query_cost, manager_id=manager_id)

        # Merge results
        campaigns = {}

        # Process revenue data
        for row in result_revenue.get('results', []):
            campaign_data = row.get('campaign', {})
            metrics = row.get('metrics', {})
            campaign_id = str(campaign_data.get('id', ''))
            campaign_name = campaign_data.get('name', '')

            if campaign_id not in campaigns:
                campaigns[campaign_id] = {
                    'name': campaign_name,
                    'revenue': 0,
                    'cost': 0,
                    'clicks': 0
                }

            campaigns[campaign_id]['revenue'] += float(metrics.get('conversionsValue', 0))

        # Process cost/click data
        for row in result_cost.get('results', []):
            campaign_data = row.get('campaign', {})
            metrics = row.get('metrics', {})
            campaign_id = str(campaign_data.get('id', ''))
            campaign_name = campaign_data.get('name', '')

            if campaign_id not in campaigns:
                campaigns[campaign_id] = {
                    'name': campaign_name,
                    'revenue': 0,
                    'cost': 0,
                    'clicks': 0
                }

            campaigns[campaign_id]['cost'] += float(metrics.get('costMicros', 0)) / 1_000_000
            campaigns[campaign_id]['clicks'] += int(metrics.get('clicks', 0))

        rows = []  # Already processed
    else:
        query = f"""
        SELECT
          campaign.name,
          campaign.id,
          metrics.conversions_value,
          metrics.cost_micros,
          metrics.clicks
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        """
        result = execute_gaql(customer_id, query, manager_id=manager_id)
        rows = result.get('results', [])
        campaigns = {}

        # Process non-filtered rows
        for row in rows:
            campaign_data = row.get('campaign', {})
            metrics = row.get('metrics', {})

            campaign_id = str(campaign_data.get('id', ''))
            campaign_name = campaign_data.get('name', '')

            if campaign_id not in campaigns:
                campaigns[campaign_id] = {
                    'name': campaign_name,
                    'revenue': 0,
                    'cost': 0,
                    'clicks': 0
                }

            campaigns[campaign_id]['revenue'] += float(metrics.get('conversionsValue', 0))
            campaigns[campaign_id]['cost'] += float(metrics.get('costMicros', 0)) / 1_000_000
            campaigns[campaign_id]['clicks'] += int(metrics.get('clicks', 0))

    # Categorize as brand or non-brand
    brand = {'revenue': 0, 'cost': 0, 'clicks': 0, 'campaigns': []}
    non_brand = {'revenue': 0, 'cost': 0, 'clicks': 0, 'campaigns': []}

    for cid, data in campaigns.items():
        # Check if "brand" appears in the campaign name (case insensitive)
        if 'brand' in data['name'].lower():
            brand['revenue'] += data['revenue']
            brand['cost'] += data['cost']
            brand['clicks'] += data['clicks']
            if data['revenue'] > 0 or data['cost'] > 0:
                brand['campaigns'].append({
                    'name': data['name'],
                    'revenue': data['revenue'],
                    'cost': data['cost'],
                    'clicks': data['clicks']
                })
        else:
            non_brand['revenue'] += data['revenue']
            non_brand['cost'] += data['cost']
            non_brand['clicks'] += data['clicks']
            if data['revenue'] > 0 or data['cost'] > 0:
                non_brand['campaigns'].append({
                    'name': data['name'],
                    'revenue': data['revenue'],
                    'cost': data['cost'],
                    'clicks': data['clicks']
                })

    return brand, non_brand

def print_summary(label, brand, non_brand):
    """Print formatted summary"""
    total_revenue = brand['revenue'] + non_brand['revenue']
    total_cost = brand['cost'] + non_brand['cost']
    total_clicks = brand['clicks'] + non_brand['clicks']

    brand_pct = (brand['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
    non_brand_pct = (non_brand['revenue'] / total_revenue * 100) if total_revenue > 0 else 0

    brand_cpc = (brand['cost'] / brand['clicks']) if brand['clicks'] > 0 else 0
    non_brand_cpc = (non_brand['cost'] / non_brand['clicks']) if non_brand['clicks'] > 0 else 0

    print(f"\n{'='*80}")
    print(f"{label}")
    print(f"{'='*80}")

    print(f"\nBRAND:")
    print(f"  Revenue:     £{brand['revenue']:>15,.2f} ({brand_pct:>5.1f}%)")
    print(f"  Cost:        £{brand['cost']:>15,.2f}")
    print(f"  Clicks:      {brand['clicks']:>17,}")
    print(f"  Avg CPC:     £{brand_cpc:>15.2f}")
    print(f"  ROAS:        {(brand['revenue']/brand['cost'] if brand['cost'] > 0 else 0):>16.2f}x")

    print(f"\nNON-BRAND:")
    print(f"  Revenue:     £{non_brand['revenue']:>15,.2f} ({non_brand_pct:>5.1f}%)")
    print(f"  Cost:        £{non_brand['cost']:>15,.2f}")
    print(f"  Clicks:      {non_brand['clicks']:>17,}")
    print(f"  Avg CPC:     £{non_brand_cpc:>15.2f}")
    print(f"  ROAS:        {(non_brand['revenue']/non_brand['cost'] if non_brand['cost'] > 0 else 0):>16.2f}x")

    print(f"\nTOTAL:")
    print(f"  Revenue:     £{total_revenue:>15,.2f}")
    print(f"  Cost:        £{total_cost:>15,.2f}")
    print(f"  Clicks:      {total_clicks:>17,}")
    print(f"  Avg CPC:     £{(total_cost/total_clicks if total_clicks > 0 else 0):>15.2f}")
    print(f"  ROAS:        {(total_revenue/total_cost if total_cost > 0 else 0):>16.2f}x")

def main():
    manager_id = "2569949686"
    uk_customer_id = "8573235780"
    usa_customer_id = "7808690871"

    print("\n" + "="*80)
    print("SMYTHSON BRAND vs NON-BRAND ANALYSIS (UK + USA)")
    print("="*80)

    # 2025 UK
    print("\n\nAnalyzing 2025 UK...")
    uk_brand_2025, uk_non_brand_2025 = analyze_account(
        uk_customer_id,
        manager_id,
        "2025-11-01",
        "2025-11-24"
    )

    # 2025 USA
    print("Analyzing 2025 USA...")
    usa_brand_2025, usa_non_brand_2025 = analyze_account(
        usa_customer_id,
        manager_id,
        "2025-11-01",
        "2025-11-24"
    )

    # 2024 UK (with conversion filter)
    print("Analyzing 2024 UK...")
    uk_brand_2024, uk_non_brand_2024 = analyze_account(
        uk_customer_id,
        manager_id,
        "2024-11-01",
        "2024-11-24",
        conversion_filter="Purchase ( Google Ads)"
    )

    # 2024 USA (with conversion filter)
    print("Analyzing 2024 USA...")
    usa_brand_2024, usa_non_brand_2024 = analyze_account(
        usa_customer_id,
        manager_id,
        "2024-11-01",
        "2024-11-24",
        conversion_filter="Purchase US ( Google Ads)"
    )

    # Combine UK + USA for 2025
    combined_brand_2025 = {
        'revenue': uk_brand_2025['revenue'] + usa_brand_2025['revenue'],
        'cost': uk_brand_2025['cost'] + usa_brand_2025['cost'],
        'clicks': uk_brand_2025['clicks'] + usa_brand_2025['clicks'],
        'campaigns': uk_brand_2025['campaigns'] + usa_brand_2025['campaigns']
    }

    combined_non_brand_2025 = {
        'revenue': uk_non_brand_2025['revenue'] + usa_non_brand_2025['revenue'],
        'cost': uk_non_brand_2025['cost'] + usa_non_brand_2025['cost'],
        'clicks': uk_non_brand_2025['clicks'] + usa_non_brand_2025['clicks'],
        'campaigns': uk_non_brand_2025['campaigns'] + usa_non_brand_2025['campaigns']
    }

    # Combine UK + USA for 2024
    combined_brand_2024 = {
        'revenue': uk_brand_2024['revenue'] + usa_brand_2024['revenue'],
        'cost': uk_brand_2024['cost'] + usa_brand_2024['cost'],
        'clicks': uk_brand_2024['clicks'] + usa_brand_2024['clicks'],
        'campaigns': uk_brand_2024['campaigns'] + usa_brand_2024['campaigns']
    }

    combined_non_brand_2024 = {
        'revenue': uk_non_brand_2024['revenue'] + usa_non_brand_2024['revenue'],
        'cost': uk_non_brand_2024['cost'] + usa_non_brand_2024['cost'],
        'clicks': uk_non_brand_2024['clicks'] + usa_non_brand_2024['clicks'],
        'campaigns': uk_non_brand_2024['campaigns'] + usa_non_brand_2024['campaigns']
    }

    # Print results
    print_summary("2025 UK (Nov 1-24)", uk_brand_2025, uk_non_brand_2025)
    print_summary("2025 USA (Nov 1-24)", usa_brand_2025, usa_non_brand_2025)
    print_summary("2025 UK + USA COMBINED", combined_brand_2025, combined_non_brand_2025)

    print("\n\n")

    print_summary("2024 UK (Nov 1-24)", uk_brand_2024, uk_non_brand_2024)
    print_summary("2024 USA (Nov 1-24)", usa_brand_2024, usa_non_brand_2024)
    print_summary("2024 UK + USA COMBINED", combined_brand_2024, combined_non_brand_2024)

    # Year over year comparison
    print("\n\n" + "="*80)
    print("YEAR OVER YEAR COMPARISON (UK + USA)")
    print("="*80)

    revenue_change = combined_brand_2025['revenue'] + combined_non_brand_2025['revenue'] - \
                     (combined_brand_2024['revenue'] + combined_non_brand_2024['revenue'])
    revenue_change_pct = (revenue_change / (combined_brand_2024['revenue'] + combined_non_brand_2024['revenue']) * 100) \
                         if (combined_brand_2024['revenue'] + combined_non_brand_2024['revenue']) > 0 else 0

    cost_change = combined_brand_2025['cost'] + combined_non_brand_2025['cost'] - \
                  (combined_brand_2024['cost'] + combined_non_brand_2024['cost'])
    cost_change_pct = (cost_change / (combined_brand_2024['cost'] + combined_non_brand_2024['cost']) * 100) \
                      if (combined_brand_2024['cost'] + combined_non_brand_2024['cost']) > 0 else 0

    brand_revenue_change = combined_brand_2025['revenue'] - combined_brand_2024['revenue']
    brand_revenue_change_pct = (brand_revenue_change / combined_brand_2024['revenue'] * 100) \
                                if combined_brand_2024['revenue'] > 0 else 0

    non_brand_revenue_change = combined_non_brand_2025['revenue'] - combined_non_brand_2024['revenue']
    non_brand_revenue_change_pct = (non_brand_revenue_change / combined_non_brand_2024['revenue'] * 100) \
                                    if combined_non_brand_2024['revenue'] > 0 else 0

    print(f"\nTotal Revenue Change:     £{revenue_change:>12,.2f} ({revenue_change_pct:+.1f}%)")
    print(f"Total Cost Change:        £{cost_change:>12,.2f} ({cost_change_pct:+.1f}%)")
    print(f"\nBrand Revenue Change:     £{brand_revenue_change:>12,.2f} ({brand_revenue_change_pct:+.1f}%)")
    print(f"Non-Brand Revenue Change: £{non_brand_revenue_change:>12,.2f} ({non_brand_revenue_change_pct:+.1f}%)")

    brand_pct_2024 = (combined_brand_2024['revenue'] / (combined_brand_2024['revenue'] + combined_non_brand_2024['revenue']) * 100) \
                     if (combined_brand_2024['revenue'] + combined_non_brand_2024['revenue']) > 0 else 0
    brand_pct_2025 = (combined_brand_2025['revenue'] / (combined_brand_2025['revenue'] + combined_non_brand_2025['revenue']) * 100) \
                     if (combined_brand_2025['revenue'] + combined_non_brand_2025['revenue']) > 0 else 0

    print(f"\nBrand Mix Shift:          {brand_pct_2024:.1f}% (2024) → {brand_pct_2025:.1f}% (2025) = {brand_pct_2025 - brand_pct_2024:+.1f} pp")

    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
