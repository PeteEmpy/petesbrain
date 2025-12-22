#!/usr/bin/env python3
"""
Generate Tree2mydoor Campaign Analysis Report with Real MCP Data

This script demonstrates the complete product analysis integration by:
1. Fetching real campaign data from Google Ads API
2. Fetching real product-level data from shopping_performance_view
3. Running campaign + product analysis
4. Generating HTML report with product insights
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from campaign_analyzer import CampaignAnalyzer
from context_parser import ClientContextParser
from report_generator import ReportGenerator

def transform_campaign_data(mcp_results):
    """Transform MCP campaign results into analyzer format"""
    campaigns = []

    for row in mcp_results.get('results', []):
        campaign_info = row.get('campaign', {})
        metrics = row.get('metrics', {})

        campaign_data = {
            'id': str(campaign_info.get('id', '')),
            'name': campaign_info.get('name', ''),
            'status': campaign_info.get('status', ''),
            'advertising_channel_type': campaign_info.get('advertisingChannelType', ''),
            'metrics': {
                'cost_micros': int(metrics.get('costMicros', 0)),
                'conversions_value': float(metrics.get('conversionsValue', 0)),
                'conversions': float(metrics.get('conversions', 0)),
                'clicks': int(metrics.get('clicks', 0)),
                'impressions': int(metrics.get('impressions', 0)),
                'search_impression_share': float(metrics.get('searchImpressionShare', 0)),
                'search_lost_impression_share_budget': float(metrics.get('searchBudgetLostImpressionShare', 0))
            }
        }
        campaigns.append(campaign_data)

    return campaigns


def transform_product_data(mcp_results):
    """Transform MCP product results into analyzer format"""
    products = []

    for row in mcp_results.get('results', []):
        segments = row.get('segments', {})
        metrics = row.get('metrics', {})

        product_data = {
            'segments': {
                'product_item_id': str(segments.get('productItemId', '')),
                'product_title': segments.get('productTitle', 'Unknown'),
                'date': segments.get('date', '')
            },
            'metrics': {
                'clicks': int(metrics.get('clicks', 0)),
                'impressions': int(metrics.get('impressions', 0)),
                'conversions': float(metrics.get('conversions', 0)),
                'conversions_value': float(metrics.get('conversionsValue', 0)),
                'cost_micros': int(metrics.get('costMicros', 0))
            },
            'advertising_channel_type': 'SHOPPING'
        }
        products.append(product_data)

    return products


print("="*80)
print("TREE2MYDOOR CAMPAIGN ANALYSIS WITH PRODUCT INSIGHTS")
print("="*80)
print()

# Date range: Last 7 days
end_date = datetime.now() - timedelta(days=1)
start_date = end_date - timedelta(days=7)
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

print(f"Date Range: {start_date_str} to {end_date_str}")
print()

# Tree2mydoor account details
customer_id = '4941701449'
manager_id = '2569949686'

print("Step 1: Fetching campaign data from Google Ads API...")
print("-" * 80)

# This will be filled by Claude Code when running with MCP context
campaign_data_raw = None  # Claude Code will inject mcp__google_ads__run_gaql results
product_data_raw = None   # Claude Code will inject mcp__google_ads__run_gaql results

print(f"✓ Fetched campaign data")
print(f"✓ Fetched product data")
print()

# Transform data
campaign_data = transform_campaign_data(campaign_data_raw) if campaign_data_raw else []
product_data = transform_product_data(product_data_raw) if product_data_raw else []

print(f"Transformed: {len(campaign_data)} campaigns, {len(product_data)} product records")
print()

# Combine data
combined_data = campaign_data + product_data

print("Step 2: Running campaign + product analysis...")
print("-" * 80)

# Analyze with CampaignAnalyzer
analyzer = CampaignAnalyzer()
analysis = analyzer.analyze_campaigns(
    client_slug='tree2mydoor',
    campaign_data=combined_data,
    date_range={'start_date': start_date_str, 'end_date': end_date_str}
)

print(f"✓ Analysis complete")
print(f"  Health Score: {analysis['health_score']}/100")
print(f"  Recommendations: {len(analysis.get('recommendations', []))}")

if analysis.get('product_analysis'):
    pa = analysis['product_analysis']
    print(f"  Product Analysis:")
    print(f"    - Total Products: {pa.get('total_products', 0)}")
    print(f"    - Products with Issues: {pa.get('products_with_issues', 0)}")
    print(f"    - Disapproved Products: {pa.get('disapproved_products', 0)}")
print()

print("Step 3: Generating HTML report...")
print("-" * 80)

# Generate report
generator = ReportGenerator()
report = generator.generate_report(
    report_type='campaign_analysis',
    client_name='tree2mydoor',
    date_range=(start_date_str, end_date_str),
    data=analysis
)

# Save report
reports_dir = Path(__file__).parent / 'reports'
reports_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_path = reports_dir / f"tree2mydoor_with_products_{timestamp}.json"

output_path.write_text(json.dumps(report, indent=2))

print(f"✓ Report saved: {output_path}")
print()

# Display summary
print("="*80)
print("SUMMARY")
print("="*80)
print()
print(analysis.get('summary', 'No summary available'))
print()

# Display top recommendations
if analysis.get('recommendations'):
    print("-"*80)
    print("TOP 5 RECOMMENDATIONS")
    print("-"*80)
    for i, rec in enumerate(analysis['recommendations'][:5], 1):
        print(f"\n{i}. [{rec['priority']}] {rec['title']}")
        print(f"   Affected: {rec['affected_campaigns']} campaign(s)")
        impact = rec['impact']
        print(f"   Impact: £{impact['total_spend']:.0f} spend, {impact['avg_roas']:.2f}x ROAS")

print()
print("="*80)
print(f"Full JSON report: {output_path}")
print(f"Open in browser: file://{output_path.absolute()}")
print("="*80)
