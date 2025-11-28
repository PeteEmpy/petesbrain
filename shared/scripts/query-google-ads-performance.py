#!/usr/bin/env python3
"""
Simple Google Ads Performance Query Tool
Usage: python3 query-google-ads-performance.py --customer-id XXXXX --start-date 2025-11-01 --end-date 2025-11-25
       Outputs performance data in CSV or JSON format
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


def query_performance(customer_id: str, start_date: str, end_date: str, campaigns: list = None, level: str = 'campaign'):
    """Query performance data from Google Ads."""
    client = GoogleAdsClient.load_from_storage(Path.home() / 'google-ads.yaml')
    ga_service = client.get_service('GoogleAdsService')

    # Build WHERE clause
    where_clauses = [f"segments.date BETWEEN '{start_date}' AND '{end_date}'"]

    if campaigns and level == 'campaign':
        # For single campaign, use simple LIKE
        if len(campaigns) == 1:
            where_clauses.append(f"campaign.name LIKE '%{campaigns[0]}%'")
        else:
            # For multiple, use IN with exact names (need to find them first)
            # For now, just use first campaign
            where_clauses.append(f"campaign.name LIKE '%{campaigns[0]}%'")

    where_clause = " AND ".join(where_clauses)

    # Build query based on level
    if level == 'campaign':
        query = f'''
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                metrics.cost_micros,
                metrics.impressions,
                metrics.clicks,
                metrics.conversions,
                metrics.conversions_value,
                metrics.ctr,
                metrics.average_cpc
            FROM campaign
            WHERE {where_clause}
        '''
    elif level == 'account':
        query = f'''
            SELECT
                segments.date,
                metrics.cost_micros,
                metrics.impressions,
                metrics.clicks,
                metrics.conversions,
                metrics.conversions_value,
                metrics.ctr,
                metrics.average_cpc
            FROM customer
            WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        '''
    else:
        raise ValueError(f"Unknown level: {level}")

    response = ga_service.search(customer_id=customer_id, query=query)

    results = []
    for row in response:
        if level == 'campaign':
            result = {
                'campaign_id': row.campaign.id,
                'campaign_name': row.campaign.name,
                'status': row.campaign.status.name,
                'cost': row.metrics.cost_micros / 1_000_000,
                'impressions': row.metrics.impressions,
                'clicks': row.metrics.clicks,
                'conversions': row.metrics.conversions,
                'revenue': row.metrics.conversions_value,
                'ctr': row.metrics.ctr,
                'avg_cpc': row.metrics.average_cpc / 1_000_000 if row.metrics.average_cpc else 0
            }
            # Calculate derived metrics
            if result['cost'] > 0:
                result['roas'] = (result['revenue'] / result['cost']) if result['cost'] > 0 else 0
                result['roas_pct'] = result['roas'] * 100
            else:
                result['roas'] = 0
                result['roas_pct'] = 0

        else:  # account level
            result = {
                'date': row.segments.date,
                'cost': row.metrics.cost_micros / 1_000_000,
                'impressions': row.metrics.impressions,
                'clicks': row.metrics.clicks,
                'conversions': row.metrics.conversions,
                'revenue': row.metrics.conversions_value,
                'ctr': row.metrics.ctr,
                'avg_cpc': row.metrics.average_cpc / 1_000_000 if row.metrics.average_cpc else 0
            }
            if result['cost'] > 0:
                result['roas'] = result['revenue'] / result['cost']
                result['roas_pct'] = result['roas'] * 100
            else:
                result['roas'] = 0
                result['roas_pct'] = 0

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
        print(f"✅ Saved to {output_file}")
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def output_json(results: list, output_file: str = None):
    """Output results as JSON."""
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"✅ Saved to {output_file}")
    else:
        print(json.dumps(results, indent=2, default=str))


def output_summary(results: list):
    """Output a summary table."""
    if not results:
        print("No results")
        return

    # Calculate totals
    total_cost = sum(r['cost'] for r in results)
    total_revenue = sum(r['revenue'] for r in results)
    total_conversions = sum(r['conversions'] for r in results)
    total_impressions = sum(r['impressions'] for r in results)
    total_clicks = sum(r['clicks'] for r in results)

    overall_roas = (total_revenue / total_cost) if total_cost > 0 else 0
    overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    overall_cpc = (total_cost / total_clicks) if total_clicks > 0 else 0

    print("\n" + "="*100)
    print("PERFORMANCE SUMMARY")
    print("="*100)

    if 'campaign_name' in results[0]:
        # Campaign-level summary
        print(f"\n{'Campaign':<50} {'Spend':>10} {'Revenue':>12} {'ROAS':>8} {'Conv':>6}")
        print("-"*100)

        # Sort by spend
        sorted_results = sorted(results, key=lambda x: x['cost'], reverse=True)

        for r in sorted_results:
            print(f"{r['campaign_name'][:48]:<50} £{r['cost']:>9.2f} £{r['revenue']:>11.2f} {r['roas_pct']:>7.0f}% {r['conversions']:>6.1f}")

        print("-"*100)

    print(f"{'TOTAL':<50} £{total_cost:>9.2f} £{total_revenue:>11.2f} {overall_roas*100:>7.0f}% {total_conversions:>6.1f}")
    print(f"\nClicks: {total_clicks:,} | Impressions: {total_impressions:,} | CTR: {overall_ctr:.2f}% | Avg CPC: £{overall_cpc:.2f}")
    print("="*100 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Query Google Ads performance data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Account-level performance
  python3 query-google-ads-performance.py --customer-id 8573235780 --start-date 2025-11-01 --end-date 2025-11-25

  # Specific campaigns
  python3 query-google-ads-performance.py --customer-id 8573235780 --start-date 2025-11-01 --end-date 2025-11-25 --campaigns "Brand,Shopping,P Max"

  # Export to CSV
  python3 query-google-ads-performance.py --customer-id 8573235780 --start-date 2025-11-01 --end-date 2025-11-25 --output csv --file performance.csv

  # Summary view (default)
  python3 query-google-ads-performance.py --customer-id 8573235780 --start-date 2025-11-01 --end-date 2025-11-25 --output summary
"""
    )

    parser.add_argument('--customer-id', required=True, help='Google Ads customer ID')
    parser.add_argument('--start-date', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('--campaigns', help='Comma-separated campaign names (partial match)')
    parser.add_argument('--level', choices=['campaign', 'account'], default='campaign', help='Query level (default: campaign)')
    parser.add_argument('--output', choices=['summary', 'csv', 'json'], default='summary', help='Output format (default: summary)')
    parser.add_argument('--file', help='Output file path (optional)')

    args = parser.parse_args()

    # Parse campaigns
    campaigns = None
    if args.campaigns:
        campaigns = [c.strip() for c in args.campaigns.split(',')]

    print(f"\n📊 Querying Google Ads performance...")
    print(f"Customer ID: {args.customer_id}")
    print(f"Date range: {args.start_date} to {args.end_date}")
    if campaigns:
        print(f"Campaigns: {', '.join(campaigns)}")
    print()

    # Query data
    results = query_performance(args.customer_id, args.start_date, args.end_date, campaigns, args.level)

    if not results:
        print("❌ No results found")
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
