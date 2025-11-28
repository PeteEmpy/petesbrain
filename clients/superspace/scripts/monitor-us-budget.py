#!/usr/bin/env python3
"""
Superspace US Budget Monitoring Script

Tracks daily spend against new budget targets (Nov 13, 2025 increase: £12,010/day).
Monitors pacing, conversions, and revenue without ROAS calculations.

Usage:
    GOOGLE_ADS_CONFIGURATION_FILE_PATH=~/google-ads.yaml python3 monitor-us-budget.py [--days 7]

Author: Rok Systems
Date: 2025-11-13
"""

import sys
import os
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Budget targets (as of Nov 13, 2025)
BUDGET_TARGETS = {
    'Shopping Branded': 4500,
    'P Max Brand Excluded': 2700,
    'Shopping Brand Excluded': 2200,
    'Search Brand Inclusion': 1200,
    'Search Generics': 790,
    'Demand Gen': 450,
    'Demand Gen Retargeting': 150
}
TOTAL_DAILY_BUDGET = 12010  # GBP

# Customer ID
CUSTOMER_ID = '7482100090'

def get_daily_spend_data(client, customer_id, days_back=7):
    """Pull daily spend data from Google Ads API."""
    ga_service = client.get_service("GoogleAdsService")

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    query = f"""
        SELECT
            segments.date,
            campaign.name,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE campaign.status = 'ENABLED'
            AND campaign.name LIKE '%US%'
            AND segments.date BETWEEN '{start_date.strftime('%Y-%m-%d')}'
                AND '{end_date.strftime('%Y-%m-%d')}'
        ORDER BY segments.date DESC, campaign.name
    """

    try:
        response = ga_service.search_stream(customer_id=customer_id, query=query)

        daily_data = {}
        campaign_totals = {}

        for batch in response:
            for row in batch.results:
                date = row.segments.date
                campaign = row.campaign.name
                cost_gbp = row.metrics.cost_micros / 1_000_000
                conversions = row.metrics.conversions
                conv_value = row.metrics.conversions_value

                # Aggregate by date
                if date not in daily_data:
                    daily_data[date] = {
                        'cost': 0,
                        'conversions': 0,
                        'revenue': 0,
                        'campaigns': {}
                    }

                daily_data[date]['cost'] += cost_gbp
                daily_data[date]['conversions'] += conversions
                daily_data[date]['revenue'] += conv_value
                daily_data[date]['campaigns'][campaign] = {
                    'cost': cost_gbp,
                    'conversions': conversions,
                    'revenue': conv_value
                }

                # Campaign totals
                if campaign not in campaign_totals:
                    campaign_totals[campaign] = {
                        'cost': 0,
                        'conversions': 0,
                        'revenue': 0
                    }
                campaign_totals[campaign]['cost'] += cost_gbp
                campaign_totals[campaign]['conversions'] += conversions
                campaign_totals[campaign]['revenue'] += conv_value

        return daily_data, campaign_totals

    except GoogleAdsException as ex:
        print(f"Google Ads API Error: {ex}")
        sys.exit(1)

def calculate_pacing(actual_spend, target_budget, days_elapsed, days_in_period):
    """Calculate spend pacing percentage."""
    expected_spend = target_budget * days_elapsed
    if expected_spend == 0:
        return 0
    pacing = (actual_spend / expected_spend) * 100
    return pacing

def format_currency(value):
    """Format number as GBP currency."""
    return f"£{value:,.2f}"

def print_report(daily_data, campaign_totals, days_back):
    """Print formatted monitoring report."""
    print("\n" + "="*80)
    print("SUPERSPACE US BUDGET MONITORING REPORT")
    print(f"Report Period: Last {days_back} days")
    print(f"Budget Implementation Date: November 13, 2025")
    print(f"Target Daily Budget: {format_currency(TOTAL_DAILY_BUDGET)}")
    print("="*80)

    # Daily breakdown
    print("\n📊 DAILY SPEND BREAKDOWN")
    print("-" * 80)
    print(f"{'Date':<12} {'Spend':<15} {'vs Target':<15} {'Pacing':<10} {'Conversions':<12} {'Revenue':<15}")
    print("-" * 80)

    total_spend = 0
    total_conversions = 0
    total_revenue = 0

    sorted_dates = sorted(daily_data.keys(), reverse=True)
    for date in sorted_dates:
        data = daily_data[date]
        cost = data['cost']
        conversions = data['conversions']
        revenue = data['revenue']

        variance = cost - TOTAL_DAILY_BUDGET
        pacing = (cost / TOTAL_DAILY_BUDGET) * 100

        total_spend += cost
        total_conversions += conversions
        total_revenue += revenue

        pacing_indicator = "✅" if 90 <= pacing <= 110 else "⚠️" if 80 <= pacing <= 120 else "🔴"

        print(f"{date:<12} {format_currency(cost):<15} {format_currency(variance):>14} {pacing:>8.1f}% {pacing_indicator} {conversions:>10.1f} {format_currency(revenue):<15}")

    print("-" * 80)
    avg_daily_spend = total_spend / len(daily_data)
    avg_pacing = (avg_daily_spend / TOTAL_DAILY_BUDGET) * 100
    print(f"{'AVERAGE':<12} {format_currency(avg_daily_spend):<15} {'':<15} {avg_pacing:>8.1f}% {'':>2} {total_conversions/len(daily_data):>10.1f} {format_currency(total_revenue/len(daily_data)):<15}")
    print(f"{'TOTAL':<12} {format_currency(total_spend):<15} {'':<27} {'':>2} {total_conversions:>10.1f} {format_currency(total_revenue):<15}")

    # Campaign breakdown
    print("\n\n📈 CAMPAIGN PERFORMANCE (Period Total)")
    print("-" * 80)
    print(f"{'Campaign':<35} {'Spend':<15} {'Budget':<12} {'%':<8} {'Conversions':<12}")
    print("-" * 80)

    for campaign, data in sorted(campaign_totals.items(), key=lambda x: x[1]['cost'], reverse=True):
        cost = data['cost']
        conversions = data['conversions']

        # Match to budget targets (simplified matching)
        budget = None
        for key in BUDGET_TARGETS:
            if key.lower() in campaign.lower():
                budget = BUDGET_TARGETS[key]
                break

        if budget:
            pct = (cost / (budget * days_back)) * 100
            print(f"{campaign[:35]:<35} {format_currency(cost):<15} {format_currency(budget):<12} {pct:>6.1f}% {conversions:>10.1f}")
        else:
            print(f"{campaign[:35]:<35} {format_currency(cost):<15} {'N/A':<12} {'':>8} {conversions:>10.1f}")

    print("-" * 80)
    print(f"{'TOTAL':<35} {format_currency(total_spend):<15} {format_currency(TOTAL_DAILY_BUDGET * days_back):<12} {'':>8} {total_conversions:>10.1f}")

    # Summary insights
    print("\n\n💡 KEY INSIGHTS")
    print("-" * 80)

    if avg_pacing < 90:
        print(f"⚠️  UNDERSPENDING: Average daily spend {format_currency(avg_daily_spend)} is {90-avg_pacing:.1f}% below target")
        print(f"   Action: Check campaign statuses and budget constraints")
    elif avg_pacing > 110:
        print(f"⚠️  OVERSPENDING: Average daily spend {format_currency(avg_daily_spend)} is {avg_pacing-110:.1f}% above target")
        print(f"   Action: Review budget settings and pacing controls")
    else:
        print(f"✅ ON TARGET: Average daily spend {format_currency(avg_daily_spend)} is within acceptable range")

    print(f"\n📊 Average Daily Conversions: {total_conversions/len(daily_data):.1f}")
    print(f"📊 Average Daily Revenue: {format_currency(total_revenue/len(daily_data))}")
    print(f"📊 Cost per Conversion: {format_currency(total_spend/total_conversions if total_conversions > 0 else 0)}")

    print("\n" + "="*80)
    print("END OF REPORT")
    print("="*80 + "\n")

def main():
    """Main execution."""
    # Check for days argument
    days_back = 7
    if len(sys.argv) > 1 and sys.argv[1].startswith('--days'):
        try:
            days_back = int(sys.argv[1].split('=')[1] if '=' in sys.argv[1] else sys.argv[2])
        except (IndexError, ValueError):
            print("Usage: monitor-us-budget.py [--days N]")
            sys.exit(1)

    # Check for config file
    config_path = os.environ.get('GOOGLE_ADS_CONFIGURATION_FILE_PATH')
    if not config_path:
        print("Error: GOOGLE_ADS_CONFIGURATION_FILE_PATH environment variable not set")
        print("Usage: GOOGLE_ADS_CONFIGURATION_FILE_PATH=~/google-ads.yaml python3 monitor-us-budget.py")
        sys.exit(1)

    # Initialize client
    try:
        client = GoogleAdsClient.load_from_storage(config_path)
    except Exception as e:
        print(f"Error loading Google Ads client: {e}")
        sys.exit(1)

    # Pull data and generate report
    print(f"\nFetching data for last {days_back} days...")
    daily_data, campaign_totals = get_daily_spend_data(client, CUSTOMER_ID, days_back)

    if not daily_data:
        print("No data found for the specified period.")
        sys.exit(0)

    print_report(daily_data, campaign_totals, days_back)

if __name__ == "__main__":
    main()
