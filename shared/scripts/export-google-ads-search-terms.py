#!/usr/bin/env python3
"""
Simple Google Ads Search Term Export
Usage: python3 export-google-ads-search-terms.py --customer-id XXXXX --start-date 2025-10-01 --end-date 2025-11-25
       Exports search term reports with metrics for negative keyword mining and expansion opportunities
"""

import sys
import json
import argparse
import csv
from pathlib import Path
from datetime import datetime

# Add MCP server to path
mcp_path = Path(__file__).parent.parent.parent / 'infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, str(mcp_path))

from google.ads.googleads.client import GoogleAdsClient

MANAGER_ID = "2569949686"  # Rok Systems MCC


def export_search_terms(customer_id: str, start_date: str, end_date: str,
                        min_clicks: int = 0, min_cost: float = 0,
                        campaign_name: str = None, limit: int = 5000):
    """Export search terms with metrics."""
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
            'roas_pct': round(roas_pct, 0)
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

  # Export all search terms from last 30 days
  python3 export-google-ads-search-terms.py --customer-id 8573235780 --start-date 2025-10-26 --end-date 2025-11-25 --output csv --file search-terms.csv

  # Find wastage candidates (terms with clicks but no conversions)
  python3 export-google-ads-search-terms.py --customer-id 8573235780 --start-date 2025-10-01 --end-date 2025-11-25 --min-clicks 5 --output summary

  # Export only high-spend terms (£50+)
  python3 export-google-ads-search-terms.py --customer-id 8573235780 --start-date 2025-10-01 --end-date 2025-11-25 --min-cost 50 --output csv --file high-spend-terms.csv

  # Filter by specific campaign
  python3 export-google-ads-search-terms.py --customer-id 8573235780 --start-date 2025-10-01 --end-date 2025-11-25 --campaign "Brand" --output summary
"""
    )

    parser.add_argument('--customer-id', required=True, help='Google Ads customer ID')
    parser.add_argument('--start-date', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('--campaign', help='Filter by campaign name (partial match)')
    parser.add_argument('--min-clicks', type=int, default=0, help='Minimum clicks (default: 0)')
    parser.add_argument('--min-cost', type=float, default=0, help='Minimum spend in GBP (default: 0)')
    parser.add_argument('--limit', type=int, default=5000, help='Maximum terms to return (default: 5000)')
    parser.add_argument('--output', choices=['summary', 'csv', 'json'], default='summary', help='Output format (default: summary)')
    parser.add_argument('--file', help='Output file path (optional)')

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
        args.limit
    )

    if not results:
        print("❌ No search terms found matching criteria")
        return 1

    # Output results
    if args.output == 'csv':
        output_csv(results, args.file)
    elif args.output == 'json':
        output_json(results, args.file)
    else:
        output_summary(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
