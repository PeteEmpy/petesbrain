#!/usr/bin/env python3
"""
Google Ads Search Term Export with Three-Tier Classification
Usage: python3 export-google-ads-search-terms.py --customer-id XXXXX --start-date 2025-10-01 --end-date 2025-11-25
       Exports search term reports with metrics and classifies into three tiers:
       - Tier 1: High confidence negative keywords (≥30 clicks, 0 conversions, ≥£20 spend)
       - Tier 2: Medium confidence negative keywords (10-29 clicks, 0 conversions)
       - Tier 3: Insufficient data (<10 clicks, 0 conversions)
       - Converting: Terms with conversions (keep active)
"""

import sys
import json
import argparse
import csv
from pathlib import Path
from datetime import datetime, timedelta

# Add MCP server to path
mcp_path = Path(__file__).parent.parent.parent / 'infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, str(mcp_path))

from google.ads.googleads.client import GoogleAdsClient

MANAGER_ID = "2569949686"  # Rok Systems MCC


def classify_search_term(clicks, conversions, spend, conversions_value, period_days=60):
    """
    Classify search term into three-tier system based on statistical significance.

    Args:
        clicks: Total clicks in period
        conversions: Total conversions in period
        spend: Total spend in period (GBP)
        conversions_value: Total conversion value (GBP)
        period_days: Analysis period length (default: 60)

    Returns:
        dict with tier, confidence, daily_click_rate, recommendation
    """
    daily_click_rate = clicks / period_days if period_days > 0 else 0

    # Tier 1: High Confidence Negative Keywords
    if clicks >= 30 and conversions == 0 and spend >= 20:
        return {
            'tier': 1,
            'tier_name': 'Tier 1 - High Confidence',
            'confidence': 'very_high',
            'daily_click_rate': round(daily_click_rate, 2),
            'false_positive_risk': '<5%',
            'recommendation': 'Add as exact match negative keyword immediately',
            'action': 'immediate'
        }

    # Tier 2: Medium Confidence Negative Keywords
    elif 10 <= clicks < 30 and conversions == 0:
        next_review = datetime.now().date() + timedelta(days=7)
        return {
            'tier': 2,
            'tier_name': 'Tier 2 - Medium Confidence',
            'confidence': 'moderate',
            'daily_click_rate': round(daily_click_rate, 2),
            'false_positive_risk': '10-20%',
            'recommendation': f'Monitor closely - review on {next_review.strftime("%Y-%m-%d")}',
            'action': 'monitor',
            'next_review_date': next_review.strftime('%Y-%m-%d')
        }

    # Tier 3: Insufficient Data
    elif clicks < 10 and conversions == 0:
        return {
            'tier': 3,
            'tier_name': 'Tier 3 - Insufficient Data',
            'confidence': 'low',
            'daily_click_rate': round(daily_click_rate, 2),
            'false_positive_risk': 'N/A',
            'recommendation': 'No action - insufficient data',
            'action': 'none'
        }

    # Converting term
    elif conversions > 0:
        roas = ((conversions_value / spend) * 100) if spend > 0 else 0
        return {
            'tier': 'converting',
            'tier_name': 'Converting',
            'confidence': 'N/A',
            'daily_click_rate': round(daily_click_rate, 2),
            'recommendation': 'Performing well - no action needed',
            'action': 'none',
            'roas': f'{roas:.0f}%'
        }

    return None


def export_search_terms(customer_id: str, start_date: str, end_date: str,
                        min_clicks: int = 0, min_cost: float = 0,
                        campaign_name: str = None, limit: int = 5000, period_days: int = 60):
    """Export search terms with metrics and tier classification."""
    client = GoogleAdsClient.load_from_storage(Path.home() / 'google-ads.yaml')
    ga_service = client.get_service('GoogleAdsService')

    # Build WHERE clause
    where_clauses = [f"segments.date BETWEEN '{start_date}' AND '{end_date}'"]
    where_clauses.append("metrics.impressions > 0")

    if min_clicks > 0:
        where_clauses.append(f"metrics.clicks >= {min_clicks}")

    if campaign_name:
        where_clauses.append(f"campaign.name LIKE '%{campaign_name}%'")

    where_clause = " AND ".join(where_clauses)

    query = f'''
        SELECT
            campaign.name,
            campaign.id,
            ad_group.name,
            ad_group.id,
            search_term_view.search_term,
            search_term_view.status,
            segments.keyword.info.match_type,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.ctr,
            metrics.average_cpc
        FROM search_term_view
        WHERE {where_clause}
        ORDER BY metrics.cost_micros DESC
        LIMIT {limit}
    '''

    response = ga_service.search(customer_id=customer_id, query=query)

    results = []
    for row in response:
        cost = row.metrics.cost_micros / 1_000_000
        avg_cpc = row.metrics.average_cpc / 1_000_000 if row.metrics.average_cpc else 0

        # Skip if below min cost threshold
        if cost < min_cost:
            continue

        # Calculate derived metrics
        roas = (row.metrics.conversions_value / cost) if cost > 0 else 0
        roas_pct = roas * 100
        cpa = (cost / row.metrics.conversions) if row.metrics.conversions > 0 else 0

        # Classify search term
        classification = classify_search_term(
            clicks=row.metrics.clicks,
            conversions=row.metrics.conversions,
            spend=cost,
            conversions_value=row.metrics.conversions_value,
            period_days=period_days
        )

        result = {
            'campaign_name': row.campaign.name,
            'campaign_id': row.campaign.id,
            'ad_group_name': row.ad_group.name,
            'ad_group_id': row.ad_group.id,
            'search_term': row.search_term_view.search_term,
            'status': row.search_term_view.status.name,
            'match_type': row.segments.keyword.info.match_type.name,
            'impressions': row.metrics.impressions,
            'clicks': row.metrics.clicks,
            'cost': round(cost, 2),
            'conversions': row.metrics.conversions,
            'revenue': round(row.metrics.conversions_value, 2),
            'ctr': round(row.metrics.ctr * 100, 2),
            'avg_cpc': round(avg_cpc, 2),
            'cpa': round(cpa, 2),
            'roas': round(roas, 2),
            'roas_pct': round(roas_pct, 0),
            # Classification data
            'tier': classification['tier'] if classification else 'N/A',
            'tier_name': classification['tier_name'] if classification else 'N/A',
            'confidence': classification['confidence'] if classification else 'N/A',
            'daily_click_rate': classification['daily_click_rate'] if classification else 0,
            'recommendation': classification['recommendation'] if classification else 'N/A',
            'action': classification['action'] if classification else 'N/A'
        }
        results.append(result)

    return results


def output_csv(results: list, output_file: str = None):
    """Output results as CSV."""
    if not results:
        print("No results to output")
        return

    fieldnames = list(results[0].keys())

    if output_file:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"✅ Saved {len(results)} search terms to {output_file}")
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def output_json(results: list, output_file: str = None):
    """Output results as JSON."""
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"✅ Saved {len(results)} search terms to {output_file}")
    else:
        print(json.dumps(results, indent=2, default=str))


def output_tier_csvs(results: list, output_dir: str, client_slug: str = None):
    """
    Output four separate tier-specific CSV files.

    Generates:
    - tier1_negative_keywords.csv (High confidence - immediate action)
    - tier2_negative_keywords.csv (Medium confidence - monitor)
    - tier3_insufficient_data.csv (Low confidence - continue monitoring)
    - converting_search_terms.csv (Performing well - keep active)
    """
    if not results:
        print("No results to output")
        return

    # Separate results by tier
    tier1_terms = [r for r in results if r['tier'] == 1]
    tier2_terms = [r for r in results if r['tier'] == 2]
    tier3_terms = [r for r in results if r['tier'] == 3]
    converting_terms = [r for r in results if r['tier'] == 'converting']

    # Sort by spend (descending) within each tier
    tier1_terms.sort(key=lambda x: x['cost'], reverse=True)
    tier2_terms.sort(key=lambda x: x['cost'], reverse=True)
    tier3_terms.sort(key=lambda x: x['cost'], reverse=True)
    converting_terms.sort(key=lambda x: x['revenue'], reverse=True)

    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime('%Y-%m-%d')
    prefix = f"{client_slug}-" if client_slug else ""

    # Tier 1 CSV (High Confidence)
    if tier1_terms:
        tier1_file = output_path / f"{prefix}keyword-audit-{today}-tier1.csv"
        fieldnames = ['search_term', 'clicks', 'cost', 'conversions', 'daily_click_rate',
                     'tier', 'confidence', 'recommendation', 'campaign_name', 'match_type']
        with open(tier1_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(tier1_terms)
        print(f"✅ Tier 1 (High Confidence): {len(tier1_terms)} terms → {tier1_file}")

    # Tier 2 CSV (Medium Confidence)
    if tier2_terms:
        tier2_file = output_path / f"{prefix}keyword-audit-{today}-tier2.csv"
        # Add next_review_date from classification if present
        for term in tier2_terms:
            if 'next_review_date' not in term:
                next_review = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                term['next_review_date'] = next_review
        fieldnames = ['search_term', 'clicks', 'cost', 'conversions', 'daily_click_rate',
                     'tier', 'confidence', 'next_review_date', 'campaign_name', 'match_type']
        with open(tier2_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(tier2_terms)
        print(f"🟡 Tier 2 (Medium Confidence): {len(tier2_terms)} terms → {tier2_file}")

    # Tier 3 CSV (Insufficient Data)
    if tier3_terms:
        tier3_file = output_path / f"{prefix}keyword-audit-{today}-tier3.csv"
        fieldnames = ['search_term', 'clicks', 'cost', 'conversions', 'daily_click_rate',
                     'tier', 'confidence', 'action', 'campaign_name', 'match_type']
        with open(tier3_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(tier3_terms)
        print(f"🔵 Tier 3 (Insufficient Data): {len(tier3_terms)} terms → {tier3_file}")

    # Converting terms CSV
    if converting_terms:
        converting_file = output_path / f"{prefix}keyword-audit-{today}-converting.csv"
        fieldnames = ['search_term', 'clicks', 'conversions', 'cost', 'revenue', 'roas_pct',
                     'daily_click_rate', 'recommendation', 'campaign_name', 'match_type']
        with open(converting_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writerows(converting_terms)
        print(f"✅ Converting Terms: {len(converting_terms)} terms → {converting_file}")

    # Summary
    total_waste = sum(r['cost'] for r in tier1_terms)
    print(f"\n📊 Summary:")
    print(f"   Tier 1 (Immediate Action): {len(tier1_terms)} terms, £{total_waste:.2f} waste identified")
    print(f"   Tier 2 (Monitor): {len(tier2_terms)} terms")
    print(f"   Tier 3 (Insufficient Data): {len(tier3_terms)} terms")
    print(f"   Converting: {len(converting_terms)} terms")


def output_summary(results: list):
    """Output a summary with wastage candidates."""
    if not results:
        print("No results")
        return

    # Calculate totals
    total_cost = sum(r['cost'] for r in results)
    total_revenue = sum(r['revenue'] for r in results)
    total_conversions = sum(r['conversions'] for r in results)
    total_clicks = sum(r['clicks'] for r in results)
    total_impressions = sum(r['impressions'] for r in results)

    overall_roas = (total_revenue / total_cost) if total_cost > 0 else 0
    overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0

    print("\n" + "="*120)
    print("SEARCH TERM REPORT SUMMARY")
    print("="*120)
    print(f"Total Search Terms: {len(results)}")
    print(f"Total Spend: £{total_cost:,.2f}")
    print(f"Total Revenue: £{total_revenue:,.2f}")
    print(f"Overall ROAS: {overall_roas*100:.0f}%")
    print(f"Total Conversions: {total_conversions:.1f}")
    print(f"Total Clicks: {total_clicks:,}")
    print(f"Overall CTR: {overall_ctr:.2f}%")

    # Identify wastage candidates (high spend, low/no conversions)
    wastage = [r for r in results if r['cost'] > 10 and r['conversions'] == 0]
    if wastage:
        wastage_cost = sum(r['cost'] for r in wastage)
        print(f"\n⚠️  WASTAGE CANDIDATES (£10+ spend, 0 conversions): {len(wastage)} terms")
        print(f"   Total wastage: £{wastage_cost:,.2f} ({wastage_cost/total_cost*100:.1f}% of spend)")

        print(f"\n{'Search Term':<50} {'Spend':>10} {'Clicks':>8} {'Match Type':>12}")
        print("-"*120)
        for term in sorted(wastage, key=lambda x: x['cost'], reverse=True)[:10]:
            print(f"{term['search_term'][:48]:<50} £{term['cost']:>9.2f} {term['clicks']:>8} {term['match_type']:>12}")

        if len(wastage) > 10:
            print(f"\n   ... and {len(wastage) - 10} more wastage terms")

    # Identify expansion opportunities (high ROAS)
    expansion = [r for r in results if r['roas'] > 4.0 and r['conversions'] >= 2]
    if expansion:
        expansion_revenue = sum(r['revenue'] for r in expansion)
        print(f"\n✅ EXPANSION OPPORTUNITIES (ROAS >400%, 2+ conversions): {len(expansion)} terms")
        print(f"   Total revenue: £{expansion_revenue:,.2f}")

        print(f"\n{'Search Term':<50} {'ROAS':>8} {'Revenue':>12} {'Match Type':>12}")
        print("-"*120)
        for term in sorted(expansion, key=lambda x: x['revenue'], reverse=True)[:10]:
            print(f"{term['search_term'][:48]:<50} {term['roas_pct']:>7.0f}% £{term['revenue']:>11.2f} {term['match_type']:>12}")

        if len(expansion) > 10:
            print(f"\n   ... and {len(expansion) - 10} more expansion terms")

    print("="*120 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Export Google Ads search term reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Generate four tier-specific CSV files (recommended for 60-day analysis)
  python3 export-google-ads-search-terms.py --customer-id 6413338364 --start-date 2025-10-18 --end-date 2025-12-17 --output tiers --file ./reports --client-slug uno-lighting --period-days 60

  # Export all search terms from last 30 days (single CSV)
  python3 export-google-ads-search-terms.py --customer-id 8573235780 --start-date 2025-10-26 --end-date 2025-11-25 --output csv --file search-terms.csv

  # Find wastage candidates with summary (includes tier analysis)
  python3 export-google-ads-search-terms.py --customer-id 8573235780 --start-date 2025-10-01 --end-date 2025-11-25 --min-clicks 5 --output summary

  # Export only high-spend terms (£50+)
  python3 export-google-ads-search-terms.py --customer-id 8573235780 --start-date 2025-10-01 --end-date 2025-11-25 --min-cost 50 --output csv --file high-spend-terms.csv

  # Filter by specific campaign
  python3 export-google-ads-search-terms.py --customer-id 8573235780 --start-date 2025-10-01 --end-date 2025-11-25 --campaign "Brand" --output summary

Tier Classification System:
  - Tier 1 (High Confidence): ≥30 clicks, 0 conversions, ≥£20 spend → Immediate negative keywords
  - Tier 2 (Medium Confidence): 10-29 clicks, 0 conversions → Monitor for 7 days
  - Tier 3 (Insufficient Data): <10 clicks, 0 conversions → Continue monitoring
  - Converting: Terms with conversions → Keep active

Recommended Period:
  - Use --period-days 60 for statistically significant analysis (default)
  - Minimum 30 days for Tier 1 identification
"""
    )

    parser.add_argument('--customer-id', required=True, help='Google Ads customer ID')
    parser.add_argument('--start-date', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('--campaign', help='Filter by campaign name (partial match)')
    parser.add_argument('--min-clicks', type=int, default=0, help='Minimum clicks (default: 0)')
    parser.add_argument('--min-cost', type=float, default=0, help='Minimum spend in GBP (default: 0)')
    parser.add_argument('--limit', type=int, default=5000, help='Maximum terms to return (default: 5000)')
    parser.add_argument('--period-days', type=int, default=60, help='Analysis period length for tier classification (default: 60)')
    parser.add_argument('--output', choices=['summary', 'csv', 'json', 'tiers'], default='summary', help='Output format: summary, csv, json, or tiers (four tier-specific CSVs)')
    parser.add_argument('--file', help='Output file path (for csv/json) or directory (for tiers)')
    parser.add_argument('--client-slug', help='Client slug for tier CSV filenames (e.g., uno-lighting)')

    args = parser.parse_args()

    print(f"\n📊 Exporting search terms...")
    print(f"Customer ID: {args.customer_id}")
    print(f"Date range: {args.start_date} to {args.end_date}")
    if args.campaign:
        print(f"Campaign filter: {args.campaign}")
    if args.min_clicks > 0:
        print(f"Min clicks: {args.min_clicks}")
    if args.min_cost > 0:
        print(f"Min spend: £{args.min_cost}")
    print()

    # Export data
    results = export_search_terms(
        args.customer_id,
        args.start_date,
        args.end_date,
        args.min_clicks,
        args.min_cost,
        args.campaign,
        args.limit,
        args.period_days
    )

    if not results:
        print("❌ No search terms found matching criteria")
        return 1

    # Output results
    if args.output == 'tiers':
        # Generate four tier-specific CSV files
        output_dir = args.file if args.file else '.'
        output_tier_csvs(results, output_dir, args.client_slug)
    elif args.output == 'csv':
        output_csv(results, args.file)
    elif args.output == 'json':
        output_json(results, args.file)
    else:
        output_summary(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
