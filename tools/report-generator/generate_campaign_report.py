#!/usr/bin/env python3
"""
Generate Campaign Analysis Report with MCP Integration

This script runs in Claude Code context where MCP tools are available.
It fetches Google Ads data via MCP and generates an intelligent campaign analysis report.

Usage:
    python3 generate_campaign_report.py <client-slug> [--days 30]
    python3 generate_campaign_report.py tree2mydoor --days 7
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from campaign_analyzer import CampaignAnalyzer
from context_parser import ClientContextParser
from report_generator import ReportGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def fetch_product_data_mcp(customer_id: str, manager_id: str, start_date: str, end_date: str):
    """
    Fetch product-level performance data using MCP Google Ads tools

    NOTE: This fetches product-level metrics for Shopping and Performance Max campaigns.
    Only call this for e-commerce clients.

    Args:
        customer_id: Google Ads customer ID
        manager_id: Manager account ID
        start_date: Start date YYYY-MM-DD
        end_date: End date YYYY-MM-DD

    Returns:
        List of product dicts with metrics
    """
    logger.info(f"Fetching product-level data for {customer_id} ({start_date} to {end_date})")

    # GAQL query to fetch product-level performance data
    query = f"""
        SELECT
            segments.product_item_id,
            segments.product_title,
            segments.date,
            metrics.clicks,
            metrics.impressions,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_micros
        FROM shopping_performance_view
        WHERE
            segments.date >= '{start_date}'
            AND segments.date <= '{end_date}'
            AND metrics.cost_micros > 0
        ORDER BY metrics.cost_micros DESC
    """

    # Check if MCP is available (Claude Code context)
    try:
        import __main__
        if hasattr(__main__, 'mcp__google_ads__run_gaql'):
            mcp_run_gaql = getattr(__main__, 'mcp__google_ads__run_gaql')
            logger.info("MCP available - fetching product data")

            result = mcp_run_gaql(
                customer_id=customer_id,
                manager_id=manager_id,
                query=query
            )

            # Transform MCP result into expected format
            products = []
            for row in result:
                product_data = {
                    'segments': {
                        'product_item_id': str(row.get('segments', {}).get('product_item_id', '')),
                        'product_title': row.get('segments', {}).get('product_title', 'Unknown'),
                        'date': row.get('segments', {}).get('date', '')
                    },
                    'metrics': {
                        'clicks': int(row.get('metrics', {}).get('clicks', 0)),
                        'impressions': int(row.get('metrics', {}).get('impressions', 0)),
                        'conversions': float(row.get('metrics', {}).get('conversions', 0)),
                        'conversions_value': float(row.get('metrics', {}).get('conversions_value', 0)),
                        'cost_micros': int(row.get('metrics', {}).get('cost_micros', 0))
                    },
                    # Add channel type so product analyzer knows this is product data
                    'advertising_channel_type': 'SHOPPING'
                }
                products.append(product_data)

            logger.info(f"Fetched {len(products)} product records from MCP")
            return products

    except (ImportError, AttributeError) as e:
        logger.warning(f"MCP not available for product data: {e}")

    # Fallback: Return empty list (product analysis will be skipped)
    logger.info("No product data available (MCP not available)")
    return []


def fetch_campaign_data_mcp(customer_id: str, manager_id: str, start_date: str, end_date: str):
    """
    Fetch campaign data using MCP Google Ads tools

    NOTE: When run from Claude Code context, this function uses MCP tools to fetch real data.
    When run standalone (for testing), it returns mock data.

    Args:
        customer_id: Google Ads customer ID
        manager_id: Manager account ID
        start_date: Start date YYYY-MM-DD
        end_date: End date YYYY-MM-DD

    Returns:
        List of campaign dicts with metrics
    """
    logger.info(f"Fetching campaign data for {customer_id} ({start_date} to {end_date})")

    # GAQL query to fetch campaign performance data
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.cost_micros,
            metrics.conversions_value,
            metrics.conversions,
            metrics.clicks,
            metrics.impressions,
            metrics.search_impression_share,
            metrics.search_budget_lost_impression_share
        FROM campaign
        WHERE
            segments.date >= '{start_date}'
            AND segments.date <= '{end_date}'
            AND metrics.cost_micros > 0
        ORDER BY metrics.cost_micros DESC
    """

    # Check if MCP is available (Claude Code context)
    try:
        # This will only work when invoked from Claude Code with MCP available
        # The mcp__google_ads__run_gaql function is injected by Claude Code
        import __main__
        if hasattr(__main__, 'mcp__google_ads__run_gaql'):
            mcp_run_gaql = getattr(__main__, 'mcp__google_ads__run_gaql')
            logger.info("MCP available - fetching real data")

            result = mcp_run_gaql(
                customer_id=customer_id,
                manager_id=manager_id,
                query=query
            )

            # Transform MCP result into expected format
            campaigns = []
            for row in result:
                campaign_data = {
                    'id': str(row.get('campaign', {}).get('id', '')),
                    'name': row.get('campaign', {}).get('name', ''),
                    'status': row.get('campaign', {}).get('status', ''),
                    'advertising_channel_type': row.get('campaign', {}).get('advertising_channel_type', ''),
                    'metrics': {
                        'cost_micros': int(row.get('metrics', {}).get('cost_micros', 0)),
                        'conversions_value': float(row.get('metrics', {}).get('conversions_value', 0)),
                        'conversions': float(row.get('metrics', {}).get('conversions', 0)),
                        'clicks': int(row.get('metrics', {}).get('clicks', 0)),
                        'impressions': int(row.get('metrics', {}).get('impressions', 0)),
                        'search_impression_share': float(row.get('metrics', {}).get('search_impression_share', 0)),
                        'search_lost_impression_share_budget': float(row.get('metrics', {}).get('search_budget_lost_impression_share', 0))
                    }
                }
                campaigns.append(campaign_data)

            logger.info(f"Fetched {len(campaigns)} campaigns from MCP")
            return campaigns

    except (ImportError, AttributeError) as e:
        logger.warning(f"MCP not available: {e}")

    # Fallback: Return mock data for testing
    logger.info("Using mock data (MCP not available)")
    return [
        {
            'id': '12345',
            'name': 'Example Campaign 1',
            'status': 'ENABLED',
            'advertising_channel_type': 'SEARCH',
            'metrics': {
                'cost_micros': 150000000,  # £150
                'conversions_value': 450.00,  # £450
                'conversions': 15,
                'clicks': 250,
                'impressions': 5000,
                'search_lost_impression_share_budget': 0.15
            }
        },
        {
            'id': '67890',
            'name': 'Example Campaign 2',
            'status': 'ENABLED',
            'advertising_channel_type': 'PERFORMANCE_MAX',
            'metrics': {
                'cost_micros': 300000000,  # £300
                'conversions_value': 900.00,  # £900
                'conversions': 30,
                'clicks': 500,
                'impressions': 10000,
                'search_lost_impression_share_budget': 0.05
            }
        }
    ]


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Generate Campaign Analysis Report')
    parser.add_argument('client_slug', help='Client slug (e.g., smythson, tree2mydoor)')
    parser.add_argument('--days', type=int, default=30, help='Number of days to analyze (default: 30)')
    parser.add_argument('--output', help='Output file path (default: reports/<client>-<date>.json)')

    args = parser.parse_args()

    # Calculate date range
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=args.days)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    logger.info(f"Generating campaign analysis for {args.client_slug}")
    logger.info(f"Date range: {start_date_str} to {end_date_str}")

    # Load client context to get account IDs
    context_parser = ClientContextParser()
    client_context = context_parser.load_client_context(args.client_slug)

    if not client_context:
        logger.error(f"Could not load context for {args.client_slug}")
        sys.exit(1)

    # Get account IDs
    account_ids = client_context.get('account_ids', {})
    customer_ids = account_ids.get('customer_ids', [])
    manager_id = account_ids.get('manager_id', '')

    if not customer_ids:
        logger.warning(f"No customer IDs found in CONTEXT.md for {args.client_slug}")
        logger.info("Using mock data for testing...")
        customer_ids = ['0000000000']  # Mock ID

    # Fetch campaign data for each account
    all_campaigns = []
    all_product_data = []

    for customer_id in customer_ids:
        logger.info(f"Fetching campaign data for account {customer_id}")
        campaigns = fetch_campaign_data_mcp(customer_id, manager_id, start_date_str, end_date_str)
        all_campaigns.extend(campaigns)

        # Check if client has Shopping or Performance Max campaigns (indicates e-commerce)
        has_shopping = any(
            c.get('advertising_channel_type') in ['SHOPPING', 'PERFORMANCE_MAX']
            for c in campaigns
        )

        # Fetch product-level data for e-commerce clients
        if has_shopping:
            logger.info(f"E-commerce client detected - fetching product-level data")
            products = fetch_product_data_mcp(customer_id, manager_id, start_date_str, end_date_str)
            all_product_data.extend(products)

    logger.info(f"Fetched {len(all_campaigns)} campaigns")
    if all_product_data:
        logger.info(f"Fetched {len(all_product_data)} product records")

    # Combine campaign and product data for analysis
    # Product data is added to campaign_data so the product analyzer can access it
    combined_data = all_campaigns + all_product_data

    # Analyze campaigns (with product data if available)
    analyzer = CampaignAnalyzer()
    analysis = analyzer.analyze_campaigns(
        client_slug=args.client_slug,
        campaign_data=combined_data,
        date_range={'start_date': start_date_str, 'end_date': end_date_str}
    )

    # Generate report using ReportGenerator
    generator = ReportGenerator()
    report = generator.generate_report(
        report_type='campaign_analysis',
        client_name=args.client_slug,
        date_range=(start_date_str, end_date_str),
        data={'campaigns': all_campaigns}
    )

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        reports_dir = Path(__file__).parent / 'reports'
        reports_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = reports_dir / f"{args.client_slug}_campaign_analysis_{timestamp}.json"

    # Save report
    output_path.write_text(json.dumps(report, indent=2))
    logger.info(f"Report saved to: {output_path}")

    # Print summary
    print("\n" + "="*80)
    print(f"CAMPAIGN ANALYSIS REPORT - {args.client_slug.upper()}")
    print("="*80)
    print(f"\nDate Range: {start_date_str} to {end_date_str}")
    print(f"Account Health Score: {analysis['health_score']}/100")
    print(f"\n{analysis['summary']}")

    # Print recommendations
    if analysis['recommendations']:
        print("\n" + "-"*80)
        print("PRIORITIZED RECOMMENDATIONS")
        print("-"*80)
        for i, rec in enumerate(analysis['recommendations'][:5], 1):  # Top 5
            print(f"\n{i}. [{rec['priority']}] {rec['title']}")
            print(f"   Affected: {rec['affected_campaigns']} campaign(s)")
            print(f"   Impact: £{rec['impact']['total_spend']:.0f} spend, {rec['impact']['avg_roas']:.2f}x ROAS")
            if rec['kb_articles']:
                print(f"   KB Articles: {len(rec['kb_articles'])} found")

    print("\n" + "="*80)
    print(f"Full report saved to: {output_path}")
    print("="*80 + "\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
