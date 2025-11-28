#!/usr/bin/env python3
"""
Complete Brand vs Non-Brand Analysis Script
Queries Google Ads API directly and analyzes search terms
"""

import sys
import os
from collections import defaultdict

# Google Ads API setup
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')

try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
except ImportError:
    print("Error: Google Ads API client not found. Install with: pip install google-ads")
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
    """Format as pounds"""
    return f"£{amount:,.2f}"

def format_percentage(value):
    """Format as percentage"""
    return f"{value:.1f}%"

def main():
    # Initialize Google Ads client
    try:
        client = GoogleAdsClient.load_from_storage("/Users/administrator/google-ads.yaml")
    except Exception as e:
        print(f"Error loading Google Ads client: {e}")
        sys.exit(1)

    # Set login customer ID (manager account)
    client.login_customer_id = MANAGER_ID

    # Build query
    query = """
        SELECT
            search_term_view.search_term,
            metrics.cost_micros,
            metrics.conversions_value,
            metrics.impressions,
            metrics.clicks
        FROM search_term_view
        WHERE
            campaign.advertising_channel_type = 'SEARCH'
            AND segments.date DURING LAST_30_DAYS
    """

    # Query API
    ga_service = client.get_service("GoogleAdsService")

    brand_data = {'spend': 0, 'revenue': 0, 'impressions': 0, 'clicks': 0, 'terms': []}
    nonbrand_data = {'spend': 0, 'revenue': 0, 'impressions': 0, 'clicks': 0, 'terms': []}

    print("Querying Google Ads API...")
    print("This may take a moment for large datasets...\n")

    try:
        response = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)

        for batch in response:
            for row in batch.results:
                term = row.search_term_view.search_term
                spend = float(row.metrics.cost_micros) / 1_000_000
                revenue = float(row.metrics.conversions_value)
                impressions = int(row.metrics.impressions)
                clicks = int(row.metrics.clicks)

                category = categorize_search_term(term)

                if category == 'brand':
                    brand_data['spend'] += spend
                    brand_data['revenue'] += revenue
                    brand_data['impressions'] += impressions
                    brand_data['clicks'] += clicks
                    brand_data['terms'].append({
                        'term': term,
                        'spend': spend,
                        'revenue': revenue,
                        'impressions': impressions,
                        'clicks': clicks
                    })
                else:
                    nonbrand_data['spend'] += spend
                    nonbrand_data['revenue'] += revenue
                    nonbrand_data['impressions'] += impressions
                    nonbrand_data['clicks'] += clicks
                    nonbrand_data['terms'].append({
                        'term': term,
                        'spend': spend,
                        'revenue': revenue,
                        'impressions': impressions,
                        'clicks': clicks
                    })

    except GoogleAdsException as ex:
        print(f"Request failed with status {ex.error.code().name}")
        for error in ex.failure.errors:
            print(f'\tError: {error.message}')
        sys.exit(1)

    # Calculate totals
    total_spend = brand_data['spend'] + nonbrand_data['spend']
    total_revenue = brand_data['revenue'] + nonbrand_data['revenue']
    total_impressions = brand_data['impressions'] + nonbrand_data['impressions']
    total_clicks = brand_data['clicks'] + nonbrand_data['clicks']

    # Print report
    print("\n" + "="*90)
    print("SMYTHSON UK - BRAND VS NON-BRAND SEARCH TERM ANALYSIS")
    print("Last 30 Days - Search Campaigns Only")
    print("="*90 + "\n")

    # Summary
    print("SUMMARY:")
    print("-" * 90)
    print(f"{'Category':<15} {'Spend':<15} {'Revenue':<15} {'ROAS':<12} {'Impr.':<12} {'Clicks':<10} {'Terms':<8}")
    print("-" * 90)

    brand_roas = (brand_data['revenue'] / brand_data['spend'] * 100) if brand_data['spend'] > 0 else 0
    print(f"{'Brand':<15} {format_currency(brand_data['spend']):<15} {format_currency(brand_data['revenue']):<15} "
          f"{format_percentage(brand_roas):<12} {brand_data['impressions']:>10,}  {brand_data['clicks']:>8,}  {len(brand_data['terms']):>6,}")

    nonbrand_roas = (nonbrand_data['revenue'] / nonbrand_data['spend'] * 100) if nonbrand_data['spend'] > 0 else 0
    print(f"{'Non-Brand':<15} {format_currency(nonbrand_data['spend']):<15} {format_currency(nonbrand_data['revenue']):<15} "
          f"{format_percentage(nonbrand_roas):<12} {nonbrand_data['impressions']:>10,}  {nonbrand_data['clicks']:>8,}  {len(nonbrand_data['terms']):>6,}")

    print("-" * 90)
    total_roas = (total_revenue / total_spend * 100) if total_spend > 0 else 0
    print(f"{'TOTAL':<15} {format_currency(total_spend):<15} {format_currency(total_revenue):<15} "
          f"{format_percentage(total_roas):<12} {total_impressions:>10,}  {total_clicks:>8,}  "
          f"{len(brand_data['terms']) + len(nonbrand_data['terms']):>6,}")
    print("-" * 90 + "\n")

    # Share percentages
    print("SPEND & REVENUE DISTRIBUTION:")
    print("-" * 90)
    print(f"{'Category':<15} {'Spend %':<15} {'Revenue %':<15} {'Impr. %':<15} {'Clicks %':<15}")
    print("-" * 90)

    brand_spend_pct = (brand_data['spend'] / total_spend * 100) if total_spend > 0 else 0
    brand_revenue_pct = (brand_data['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
    brand_impr_pct = (brand_data['impressions'] / total_impressions * 100) if total_impressions > 0 else 0
    brand_clicks_pct = (brand_data['clicks'] / total_clicks * 100) if total_clicks > 0 else 0

    print(f"{'Brand':<15} {format_percentage(brand_spend_pct):<15} {format_percentage(brand_revenue_pct):<15} "
          f"{format_percentage(brand_impr_pct):<15} {format_percentage(brand_clicks_pct):<15}")

    nonbrand_spend_pct = (nonbrand_data['spend'] / total_spend * 100) if total_spend > 0 else 0
    nonbrand_revenue_pct = (nonbrand_data['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
    nonbrand_impr_pct = (nonbrand_data['impressions'] / total_impressions * 100) if total_impressions > 0 else 0
    nonbrand_clicks_pct = (nonbrand_data['clicks'] / total_clicks * 100) if total_clicks > 0 else 0

    print(f"{'Non-Brand':<15} {format_percentage(nonbrand_spend_pct):<15} {format_percentage(nonbrand_revenue_pct):<15} "
          f"{format_percentage(nonbrand_impr_pct):<15} {format_percentage(nonbrand_clicks_pct):<15}")
    print("-" * 90 + "\n")

    # Top brand terms
    brand_data['terms'].sort(key=lambda x: x['spend'], reverse=True)
    print("TOP 10 BRAND SEARCH TERMS (by spend):")
    print("-" * 90)
    print(f"{'Search Term':<35} {'Spend':<15} {'Revenue':<15} {'ROAS':<12} {'Clicks':<8}")
    print("-" * 90)
    for term in brand_data['terms'][:10]:
        term_roas = (term['revenue'] / term['spend'] * 100) if term['spend'] > 0 else 0
        print(f"{term['term']:<35} {format_currency(term['spend']):<15} {format_currency(term['revenue']):<15} "
              f"{format_percentage(term_roas):<12} {term['clicks']:>6,}")
    print("-" * 90 + "\n")

    # Top non-brand terms
    nonbrand_data['terms'].sort(key=lambda x: x['spend'], reverse=True)
    print("TOP 10 NON-BRAND SEARCH TERMS (by spend):")
    print("-" * 90)
    print(f"{'Search Term':<35} {'Spend':<15} {'Revenue':<15} {'ROAS':<12} {'Clicks':<8}")
    print("-" * 90)
    for term in nonbrand_data['terms'][:10]:
        term_roas = (term['revenue'] / term['spend'] * 100) if term['spend'] > 0 else 0
        print(f"{term['term']:<35} {format_currency(term['spend']):<15} {format_currency(term['revenue']):<15} "
              f"{format_percentage(term_roas):<12} {term['clicks']:>6,}")
    print("-" * 90 + "\n")

if __name__ == '__main__':
    main()
