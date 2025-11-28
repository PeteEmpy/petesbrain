#!/usr/bin/env python3
"""
Year-over-Year Brand vs Non-Brand Comparison
Compares last 30 days this year vs last year (same period)
"""

import sys
from datetime import datetime, timedelta

sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
except ImportError:
    print("Error: Google Ads API client not found")
    sys.exit(1)

CUSTOMER_ID = "8573235780"
MANAGER_ID = "2569949686"

def categorize_search_term(term):
    """Categorize a search term as brand or non-brand"""
    term_lower = term.lower()
    brand_keywords = ['smythson', 'smyth', 'smith', 'smyson', 'symthson', 'frank smythson']
    for keyword in brand_keywords:
        if keyword in term_lower:
            return 'brand'
    return 'non-brand'

def format_currency(amount):
    return f"£{amount:,.2f}"

def format_number(num):
    return f"{num:,}"

def format_percentage(value):
    return f"{value:.1f}%"

def format_change(old, new):
    """Format change with + or - indicator"""
    if old == 0:
        return "N/A"
    change = ((new - old) / old) * 100
    sign = "+" if change > 0 else ""
    return f"{sign}{change:.1f}%"

def query_basic_metrics(client, start_date, end_date, period_name):
    """Query clicks and spend data"""
    query = f"""
        SELECT
            search_term_view.search_term,
            metrics.cost_micros,
            metrics.clicks
        FROM search_term_view
        WHERE
            campaign.advertising_channel_type = 'SEARCH'
            AND segments.date BETWEEN '{start_date}' AND '{end_date}'
    """

    ga_service = client.get_service("GoogleAdsService")

    brand_data = {'spend': 0, 'clicks': 0}
    nonbrand_data = {'spend': 0, 'clicks': 0}

    print(f"Querying {period_name} clicks/spend data ({start_date} to {end_date})...")

    try:
        response = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)

        for batch in response:
            for row in batch.results:
                term = row.search_term_view.search_term
                spend = float(row.metrics.cost_micros) / 1_000_000
                clicks = int(row.metrics.clicks)

                category = categorize_search_term(term)

                if category == 'brand':
                    brand_data['spend'] += spend
                    brand_data['clicks'] += clicks
                else:
                    nonbrand_data['spend'] += spend
                    nonbrand_data['clicks'] += clicks

    except GoogleAdsException as ex:
        print(f"Request failed: {ex.error.code().name}")
        for error in ex.failure.errors:
            print(f'Error: {error.message}')
        sys.exit(1)

    return brand_data, nonbrand_data

def query_conversion_metrics(client, start_date, end_date, period_name, year):
    """Query conversion data - for 2024 filter by web purchase action"""

    # For 2024, we'll use a campaign-level query to get web purchase conversions
    if year == 2024:
        query = f"""
            SELECT
                campaign.name,
                segments.conversion_action_name,
                metrics.conversions,
                metrics.conversions_value
            FROM campaign
            WHERE
                campaign.advertising_channel_type = 'SEARCH'
                AND segments.date BETWEEN '{start_date}' AND '{end_date}'
                AND segments.conversion_action_name = 'Purchase ( Google Ads)'
        """
    else:
        # For 2025, get all conversions from search term view
        query = f"""
            SELECT
                search_term_view.search_term,
                metrics.conversions,
                metrics.conversions_value
            FROM search_term_view
            WHERE
                campaign.advertising_channel_type = 'SEARCH'
                AND segments.date BETWEEN '{start_date}' AND '{end_date}'
        """

    ga_service = client.get_service("GoogleAdsService")

    brand_data = {'conversions': 0, 'revenue': 0}
    nonbrand_data = {'conversions': 0, 'revenue': 0}

    print(f"Querying {period_name} conversion data ({start_date} to {end_date})...")

    try:
        response = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)

        if year == 2024:
            # For 2024, we get campaign-level data, so can't split brand/non-brand accurately
            # We'll get total and apply the brand/non-brand split from clicks
            total_conversions = 0
            total_revenue = 0

            for batch in response:
                for row in batch.results:
                    total_conversions += float(row.metrics.conversions)
                    total_revenue += float(row.metrics.conversions_value)

            # Return total only - we'll split later based on click proportions
            return {'conversions': total_conversions, 'revenue': total_revenue}
        else:
            # For 2025, split by search term
            for batch in response:
                for row in batch.results:
                    term = row.search_term_view.search_term
                    conversions = float(row.metrics.conversions)
                    revenue = float(row.metrics.conversions_value)

                    category = categorize_search_term(term)

                    if category == 'brand':
                        brand_data['conversions'] += conversions
                        brand_data['revenue'] += revenue
                    else:
                        nonbrand_data['conversions'] += conversions
                        nonbrand_data['revenue'] += revenue

            return brand_data, nonbrand_data

    except GoogleAdsException as ex:
        print(f"Request failed: {ex.error.code().name}")
        for error in ex.failure.errors:
            print(f'Error: {error.message}')
        sys.exit(1)

def main():
    # Initialize client
    try:
        client = GoogleAdsClient.load_from_storage("/Users/administrator/google-ads.yaml")
    except Exception as e:
        print(f"Error loading Google Ads client: {e}")
        sys.exit(1)

    client.login_customer_id = MANAGER_ID

    # Calculate date ranges
    today = datetime.now().date()
    this_year_end = today - timedelta(days=1)
    this_year_start = this_year_end - timedelta(days=29)

    last_year_end = this_year_end.replace(year=this_year_end.year - 1)
    last_year_start = this_year_start.replace(year=this_year_start.year - 1)

    print("\n" + "="*100)
    print("SMYTHSON UK - YEAR-OVER-YEAR BRAND VS NON-BRAND COMPARISON")
    print("="*100)
    print(f"\nThis Year Period: {this_year_start} to {this_year_end}")
    print(f"Last Year Period: {last_year_start} to {last_year_end}")
    print(f"\nNote: Last year data filtered for 'Purchase ( Google Ads)' conversion action only")
    print(f"      Last year brand/non-brand conversion split estimated from click distribution\n")

    # Query 2025 data (both queries work)
    brand_2025_basic, nonbrand_2025_basic = query_basic_metrics(
        client,
        this_year_start.strftime('%Y-%m-%d'),
        this_year_end.strftime('%Y-%m-%d'),
        "2025"
    )

    brand_2025_conv, nonbrand_2025_conv = query_conversion_metrics(
        client,
        this_year_start.strftime('%Y-%m-%d'),
        this_year_end.strftime('%Y-%m-%d'),
        "2025",
        2025
    )

    # Merge 2025 data
    brand_2025 = {**brand_2025_basic, **brand_2025_conv}
    nonbrand_2025 = {**nonbrand_2025_basic, **nonbrand_2025_conv}

    # Query 2024 data
    brand_2024_basic, nonbrand_2024_basic = query_basic_metrics(
        client,
        last_year_start.strftime('%Y-%m-%d'),
        last_year_end.strftime('%Y-%m-%d'),
        "2024"
    )

    total_2024_conv = query_conversion_metrics(
        client,
        last_year_start.strftime('%Y-%m-%d'),
        last_year_end.strftime('%Y-%m-%d'),
        "2024",
        2024
    )

    # Split 2024 conversions based on click proportions
    total_2024_clicks = brand_2024_basic['clicks'] + nonbrand_2024_basic['clicks']
    brand_click_proportion = brand_2024_basic['clicks'] / total_2024_clicks if total_2024_clicks > 0 else 0
    nonbrand_click_proportion = nonbrand_2024_basic['clicks'] / total_2024_clicks if total_2024_clicks > 0 else 0

    brand_2024 = {
        **brand_2024_basic,
        'conversions': total_2024_conv['conversions'] * brand_click_proportion,
        'revenue': total_2024_conv['revenue'] * brand_click_proportion
    }

    nonbrand_2024 = {
        **nonbrand_2024_basic,
        'conversions': total_2024_conv['conversions'] * nonbrand_click_proportion,
        'revenue': total_2024_conv['revenue'] * nonbrand_click_proportion
    }

    # Calculate derived metrics
    def calculate_metrics(data):
        cpc = data['spend'] / data['clicks'] if data['clicks'] > 0 else 0
        cpa = data['spend'] / data['conversions'] if data['conversions'] > 0 else 0
        roas = (data['revenue'] / data['spend'] * 100) if data['spend'] > 0 else 0
        conv_rate = (data['conversions'] / data['clicks'] * 100) if data['clicks'] > 0 else 0
        return cpc, cpa, roas, conv_rate

    brand_2025_cpc, brand_2025_cpa, brand_2025_roas, brand_2025_cvr = calculate_metrics(brand_2025)
    brand_2024_cpc, brand_2024_cpa, brand_2024_roas, brand_2024_cvr = calculate_metrics(brand_2024)
    nonbrand_2025_cpc, nonbrand_2025_cpa, nonbrand_2025_roas, nonbrand_2025_cvr = calculate_metrics(nonbrand_2025)
    nonbrand_2024_cpc, nonbrand_2024_cpa, nonbrand_2024_roas, nonbrand_2024_cvr = calculate_metrics(nonbrand_2024)

    # Print Brand Comparison
    print("\n" + "="*100)
    print("BRAND SEARCH TERMS")
    print("="*100)
    print(f"\n{'Metric':<25} {'2024':<20} {'2025':<20} {'Change':<15}")
    print("-"*100)
    print(f"{'Spend':<25} {format_currency(brand_2024['spend']):<20} {format_currency(brand_2025['spend']):<20} {format_change(brand_2024['spend'], brand_2025['spend']):<15}")
    print(f"{'Clicks':<25} {format_number(brand_2024['clicks']):<20} {format_number(brand_2025['clicks']):<20} {format_change(brand_2024['clicks'], brand_2025['clicks']):<15}")
    print(f"{'CPC':<25} {format_currency(brand_2024_cpc):<20} {format_currency(brand_2025_cpc):<20} {format_change(brand_2024_cpc, brand_2025_cpc):<15}")
    print(f"{'Conversions':<25} {format_number(int(brand_2024['conversions'])):<20} {format_number(int(brand_2025['conversions'])):<20} {format_change(brand_2024['conversions'], brand_2025['conversions']):<15}")
    print(f"{'Conversion Rate':<25} {format_percentage(brand_2024_cvr):<20} {format_percentage(brand_2025_cvr):<20} {format_change(brand_2024_cvr, brand_2025_cvr):<15}")
    print(f"{'CPA':<25} {format_currency(brand_2024_cpa):<20} {format_currency(brand_2025_cpa):<20} {format_change(brand_2024_cpa, brand_2025_cpa):<15}")
    print(f"{'Conversion Value':<25} {format_currency(brand_2024['revenue']):<20} {format_currency(brand_2025['revenue']):<20} {format_change(brand_2024['revenue'], brand_2025['revenue']):<15}")
    print(f"{'ROAS':<25} {format_percentage(brand_2024_roas):<20} {format_percentage(brand_2025_roas):<20} {format_change(brand_2024_roas, brand_2025_roas):<15}")

    # Print Non-Brand Comparison
    print("\n" + "="*100)
    print("NON-BRAND SEARCH TERMS")
    print("="*100)
    print(f"\n{'Metric':<25} {'2024':<20} {'2025':<20} {'Change':<15}")
    print("-"*100)
    print(f"{'Spend':<25} {format_currency(nonbrand_2024['spend']):<20} {format_currency(nonbrand_2025['spend']):<20} {format_change(nonbrand_2024['spend'], nonbrand_2025['spend']):<15}")
    print(f"{'Clicks':<25} {format_number(nonbrand_2024['clicks']):<20} {format_number(nonbrand_2025['clicks']):<20} {format_change(nonbrand_2024['clicks'], nonbrand_2025['clicks']):<15}")
    print(f"{'CPC':<25} {format_currency(nonbrand_2024_cpc):<20} {format_currency(nonbrand_2025_cpc):<20} {format_change(nonbrand_2024_cpc, nonbrand_2025_cpc):<15}")
    print(f"{'Conversions':<25} {format_number(int(nonbrand_2024['conversions'])):<20} {format_number(int(nonbrand_2025['conversions'])):<20} {format_change(nonbrand_2024['conversions'], nonbrand_2025['conversions']):<15}")
    print(f"{'Conversion Rate':<25} {format_percentage(nonbrand_2024_cvr):<20} {format_percentage(nonbrand_2025_cvr):<20} {format_change(nonbrand_2024_cvr, nonbrand_2025_cvr):<15}")
    print(f"{'CPA':<25} {format_currency(nonbrand_2024_cpa):<20} {format_currency(nonbrand_2025_cpa):<20} {format_change(nonbrand_2024_cpa, nonbrand_2025_cpa):<15}")
    print(f"{'Conversion Value':<25} {format_currency(nonbrand_2024['revenue']):<20} {format_currency(nonbrand_2025['revenue']):<20} {format_change(nonbrand_2024['revenue'], nonbrand_2025['revenue']):<15}")
    print(f"{'ROAS':<25} {format_percentage(nonbrand_2024_roas):<20} {format_percentage(nonbrand_2025_roas):<20} {format_change(nonbrand_2024_roas, nonbrand_2025_roas):<15}")

    # Print Total Comparison
    total_2024_spend = brand_2024['spend'] + nonbrand_2024['spend']
    total_2025_spend = brand_2025['spend'] + nonbrand_2025['spend']
    total_2024_clicks = brand_2024['clicks'] + nonbrand_2024['clicks']
    total_2025_clicks = brand_2025['clicks'] + nonbrand_2025['clicks']
    total_2024_conversions = brand_2024['conversions'] + nonbrand_2024['conversions']
    total_2025_conversions = brand_2025['conversions'] + nonbrand_2025['conversions']
    total_2024_revenue = brand_2024['revenue'] + nonbrand_2024['revenue']
    total_2025_revenue = brand_2025['revenue'] + nonbrand_2025['revenue']

    total_2024_cpc = total_2024_spend / total_2024_clicks if total_2024_clicks > 0 else 0
    total_2025_cpc = total_2025_spend / total_2025_clicks if total_2025_clicks > 0 else 0
    total_2024_cpa = total_2024_spend / total_2024_conversions if total_2024_conversions > 0 else 0
    total_2025_cpa = total_2025_spend / total_2025_conversions if total_2025_conversions > 0 else 0
    total_2024_roas = (total_2024_revenue / total_2024_spend * 100) if total_2024_spend > 0 else 0
    total_2025_roas = (total_2025_revenue / total_2025_spend * 100) if total_2025_spend > 0 else 0
    total_2024_cvr = (total_2024_conversions / total_2024_clicks * 100) if total_2024_clicks > 0 else 0
    total_2025_cvr = (total_2025_conversions / total_2025_clicks * 100) if total_2025_clicks > 0 else 0

    print("\n" + "="*100)
    print("TOTAL (BRAND + NON-BRAND)")
    print("="*100)
    print(f"\n{'Metric':<25} {'2024':<20} {'2025':<20} {'Change':<15}")
    print("-"*100)
    print(f"{'Spend':<25} {format_currency(total_2024_spend):<20} {format_currency(total_2025_spend):<20} {format_change(total_2024_spend, total_2025_spend):<15}")
    print(f"{'Clicks':<25} {format_number(total_2024_clicks):<20} {format_number(total_2025_clicks):<20} {format_change(total_2024_clicks, total_2025_clicks):<15}")
    print(f"{'CPC':<25} {format_currency(total_2024_cpc):<20} {format_currency(total_2025_cpc):<20} {format_change(total_2024_cpc, total_2025_cpc):<15}")
    print(f"{'Conversions':<25} {format_number(int(total_2024_conversions)):<20} {format_number(int(total_2025_conversions)):<20} {format_change(total_2024_conversions, total_2025_conversions):<15}")
    print(f"{'Conversion Rate':<25} {format_percentage(total_2024_cvr):<20} {format_percentage(total_2025_cvr):<20} {format_change(total_2024_cvr, total_2025_cvr):<15}")
    print(f"{'CPA':<25} {format_currency(total_2024_cpa):<20} {format_currency(total_2025_cpa):<20} {format_change(total_2024_cpa, total_2025_cpa):<15}")
    print(f"{'Conversion Value':<25} {format_currency(total_2024_revenue):<20} {format_currency(total_2025_revenue):<20} {format_change(total_2024_revenue, total_2025_revenue):<15}")
    print(f"{'ROAS':<25} {format_percentage(total_2024_roas):<20} {format_percentage(total_2025_roas):<20} {format_change(total_2024_roas, total_2025_roas):<15}")

    # Key Insights
    print("\n" + "="*100)
    print("KEY INSIGHTS")
    print("="*100)

    cpc_increase_pct = ((brand_2025_cpc - brand_2024_cpc) / brand_2024_cpc * 100) if brand_2024_cpc > 0 else 0
    print(f"\n1. BRAND CPC INCREASE: {format_change(brand_2024_cpc, brand_2025_cpc)}")
    print(f"   2024: {format_currency(brand_2024_cpc)} → 2025: {format_currency(brand_2025_cpc)}")
    if cpc_increase_pct > 10:
        print(f"   ⚠️  Significant CPC increase suggests increased competition on brand terms")

    print(f"\n2. BRAND ROAS CHANGE: {format_change(brand_2024_roas, brand_2025_roas)}")
    print(f"   2024: {format_percentage(brand_2024_roas)} → 2025: {format_percentage(brand_2025_roas)}")
    roas_change_pct = ((brand_2025_roas - brand_2024_roas) / brand_2024_roas * 100) if brand_2024_roas > 0 else 0
    if roas_change_pct < -10:
        print(f"   ⚠️  ROAS decline confirms reduced efficiency despite higher spend")

    revenue_per_click_2024 = brand_2024['revenue'] / brand_2024['clicks'] if brand_2024['clicks'] > 0 else 0
    revenue_per_click_2025 = brand_2025['revenue'] / brand_2025['clicks'] if brand_2025['clicks'] > 0 else 0
    print(f"\n3. REVENUE PER CLICK:")
    print(f"   2024: {format_currency(revenue_per_click_2024)} → 2025: {format_currency(revenue_per_click_2025)}")
    print(f"   Change: {format_change(revenue_per_click_2024, revenue_per_click_2025)}")

    spend_increase_pct = ((brand_2025['spend'] - brand_2024['spend']) / brand_2024['spend'] * 100) if brand_2024['spend'] > 0 else 0
    revenue_increase_pct = ((brand_2025['revenue'] - brand_2024['revenue']) / brand_2024['revenue'] * 100) if brand_2024['revenue'] > 0 else 0
    print(f"\n4. SPEND EFFICIENCY:")
    print(f"   Spend increased: {format_change(brand_2024['spend'], brand_2025['spend'])}")
    print(f"   Revenue increased: {format_change(brand_2024['revenue'], brand_2025['revenue'])}")
    if spend_increase_pct > revenue_increase_pct:
        efficiency_gap = spend_increase_pct - revenue_increase_pct
        print(f"   ⚠️  Spend growing {efficiency_gap:.1f}% faster than revenue - confirming reduced efficiency")

    print("\n" + "="*100 + "\n")

if __name__ == '__main__':
    main()
