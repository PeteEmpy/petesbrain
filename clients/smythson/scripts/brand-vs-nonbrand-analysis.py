#!/usr/bin/env python3
"""
Brand vs Non-Brand Search Term Analysis for Smythson UK
Analyzes search term performance from Google Ads API
"""

import json
import sys
import os

# Add parent directory to path for MCP imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

def categorize_search_term(term):
    """
    Categorize a search term as brand or non-brand
    Brand terms include: smythson, smyth, smith (common misspellings)
    """
    term_lower = term.lower()

    # Brand keywords
    brand_keywords = ['smythson', 'smyth', 'smith', 'smyson', 'symthson', 'frank smythson']

    for keyword in brand_keywords:
        if keyword in term_lower:
            return 'brand'

    return 'non-brand'

def analyze_search_terms(data):
    """
    Analyze search terms and calculate brand vs non-brand metrics
    """
    brand_spend = 0
    nonbrand_spend = 0
    brand_revenue = 0
    nonbrand_revenue = 0
    brand_terms = []
    nonbrand_terms = []

    for result in data.get('results', []):
        term = result['searchTermView']['searchTerm']
        spend = float(result['metrics']['costMicros']) / 1_000_000  # Convert micros to pounds
        revenue = float(result['metrics'].get('conversionsValue', 0))

        category = categorize_search_term(term)

        if category == 'brand':
            brand_spend += spend
            brand_revenue += revenue
            brand_terms.append({
                'term': term,
                'spend': spend,
                'revenue': revenue,
                'roas': (revenue / spend * 100) if spend > 0 else 0
            })
        else:
            nonbrand_spend += spend
            nonbrand_revenue += revenue
            nonbrand_terms.append({
                'term': term,
                'spend': spend,
                'revenue': revenue,
                'roas': (revenue / spend * 100) if spend > 0 else 0
            })

    total_spend = brand_spend + nonbrand_spend
    total_revenue = brand_revenue + nonbrand_revenue

    return {
        'brand': {
            'spend': brand_spend,
            'revenue': brand_revenue,
            'roas': (brand_revenue / brand_spend * 100) if brand_spend > 0 else 0,
            'spend_share': (brand_spend / total_spend * 100) if total_spend > 0 else 0,
            'revenue_share': (brand_revenue / total_revenue * 100) if total_revenue > 0 else 0,
            'terms_count': len(brand_terms),
            'top_terms': sorted(brand_terms, key=lambda x: x['spend'], reverse=True)[:10]
        },
        'non_brand': {
            'spend': nonbrand_spend,
            'revenue': nonbrand_revenue,
            'roas': (nonbrand_revenue / nonbrand_spend * 100) if nonbrand_spend > 0 else 0,
            'spend_share': (nonbrand_spend / total_spend * 100) if total_spend > 0 else 0,
            'revenue_share': (nonbrand_revenue / total_revenue * 100) if total_revenue > 0 else 0,
            'terms_count': len(nonbrand_terms),
            'top_terms': sorted(nonbrand_terms, key=lambda x: x['spend'], reverse=True)[:10]
        },
        'total': {
            'spend': total_spend,
            'revenue': total_revenue,
            'roas': (total_revenue / total_spend * 100) if total_spend > 0 else 0
        }
    }

def format_currency(amount):
    """Format as pounds"""
    return f"£{amount:,.2f}"

def format_percentage(value):
    """Format as percentage"""
    return f"{value:.1f}%"

def print_report(analysis):
    """Print formatted analysis report"""
    print("\n" + "="*80)
    print("SMYTHSON UK - BRAND VS NON-BRAND SEARCH TERM ANALYSIS")
    print("Last 30 Days - Search Campaigns Only")
    print("="*80 + "\n")

    # Summary Table
    print("SUMMARY:")
    print("-" * 80)
    print(f"{'Category':<20} {'Spend':<15} {'Revenue':<15} {'ROAS':<12} {'Terms':<10}")
    print("-" * 80)

    brand = analysis['brand']
    print(f"{'Brand':<20} {format_currency(brand['spend']):<15} {format_currency(brand['revenue']):<15} "
          f"{format_percentage(brand['roas']):<12} {brand['terms_count']:<10}")

    nonbrand = analysis['non_brand']
    print(f"{'Non-Brand':<20} {format_currency(nonbrand['spend']):<15} {format_currency(nonbrand['revenue']):<15} "
          f"{format_percentage(nonbrand['roas']):<12} {nonbrand['terms_count']:<10}")

    total = analysis['total']
    print("-" * 80)
    print(f"{'TOTAL':<20} {format_currency(total['spend']):<15} {format_currency(total['revenue']):<15} "
          f"{format_percentage(total['roas']):<12} {brand['terms_count'] + nonbrand['terms_count']:<10}")
    print("-" * 80 + "\n")

    # Spend & Revenue Share
    print("SPEND & REVENUE DISTRIBUTION:")
    print("-" * 80)
    print(f"{'Category':<20} {'Spend %':<15} {'Revenue %':<15}")
    print("-" * 80)
    print(f"{'Brand':<20} {format_percentage(brand['spend_share']):<15} {format_percentage(brand['revenue_share']):<15}")
    print(f"{'Non-Brand':<20} {format_percentage(nonbrand['spend_share']):<15} {format_percentage(nonbrand['revenue_share']):<15}")
    print("-" * 80 + "\n")

    # Top Brand Terms
    print("TOP 10 BRAND SEARCH TERMS (by spend):")
    print("-" * 80)
    print(f"{'Search Term':<40} {'Spend':<15} {'Revenue':<15} {'ROAS':<10}")
    print("-" * 80)
    for term in brand['top_terms']:
        print(f"{term['term']:<40} {format_currency(term['spend']):<15} "
              f"{format_currency(term['revenue']):<15} {format_percentage(term['roas']):<10}")
    print("-" * 80 + "\n")

    # Top Non-Brand Terms
    print("TOP 10 NON-BRAND SEARCH TERMS (by spend):")
    print("-" * 80)
    print(f"{'Search Term':<40} {'Spend':<15} {'Revenue':<15} {'ROAS':<10}")
    print("-" * 80)
    for term in nonbrand['top_terms']:
        print(f"{term['term']:<40} {format_currency(term['spend']):<15} "
              f"{format_currency(term['revenue']):<15} {format_percentage(term['roas']):<10}")
    print("-" * 80 + "\n")

if __name__ == '__main__':
    # Read search terms data from stdin (will be piped from GAQL query)
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    else:
        # Read from stdin
        data = json.load(sys.stdin)

    analysis = analyze_search_terms(data)
    print_report(analysis)
