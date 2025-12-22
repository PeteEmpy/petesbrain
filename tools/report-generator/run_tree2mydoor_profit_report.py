#!/usr/bin/env python3
"""
Generate comprehensive profit-focused report for Tree2mydoor
Uses Tree2mydoorProfitAnalyzer and Tree2mydoorHTMLGenerator
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from tree2mydoor_profit_analyzer import Tree2mydoorProfitAnalyzer
from tree2mydoor_html_generator import Tree2mydoorHTMLGenerator


# Real Tree2mydoor data from previous MCP query (Dec 7-13, 2025)
CAMPAIGN_DATA = {
    "results": [
        {
            "campaign": {
                "resourceName": "customers/4941701449/campaigns/15820346778",
                "id": "15820346778",
                "name": "T2MD | P Max | HP&P 150 5/9 140 23/10",
                "status": "ENABLED",
                "advertisingChannelType": "PERFORMANCE_MAX"
            },
            "metrics": {
                "costMicros": "1356584153",
                "conversionsValue": 1948.24986613,
                "conversions": 101.571985,
                "clicks": "1336",
                "impressions": "95834",
                "searchImpressionShare": 0.0,
                "searchBudgetLostImpressionShare": 0.0
            }
        },
        {
            "campaign": {
                "resourceName": "customers/4941701449/campaigns/22986754502",
                "id": "22986754502",
                "name": "T2MD | Shopping | Catch All 170 150 20/10 140 23/10",
                "status": "ENABLED",
                "advertisingChannelType": "SHOPPING"
            },
            "metrics": {
                "costMicros": "319690000",
                "conversionsValue": 498.127685649,
                "conversions": 29.743024,
                "clicks": "404",
                "impressions": "42166",
                "searchImpressionShare": 0.0,
                "searchBudgetLostImpressionShare": 0.0
            }
        },
        {
            "campaign": {
                "resourceName": "customers/4941701449/campaigns/598475433",
                "id": "598475433",
                "name": "T2MD | Search | Trees Port 150 16/6 Ai 4/8 Lemon paused 20/8 131 3/9",
                "status": "ENABLED",
                "advertisingChannelType": "SEARCH"
            },
            "metrics": {
                "costMicros": "218174750",
                "conversionsValue": 303.426671595,
                "conversions": 14.568833,
                "clicks": "292",
                "impressions": "3836",
                "searchImpressionShare": 0.0,
                "searchBudgetLostImpressionShare": 0.0
            }
        },
        {
            "campaign": {
                "resourceName": "customers/4941701449/campaigns/21610656469",
                "id": "21610656469",
                "name": "T2MD | P Max Shopping | Unprofitable 150 160 3/9 150 5/9 140 23/10",
                "status": "ENABLED",
                "advertisingChannelType": "PERFORMANCE_MAX"
            },
            "metrics": {
                "costMicros": "111423985",
                "conversionsValue": 130.75660092,
                "conversions": 6.870694,
                "clicks": "115",
                "impressions": "17294",
                "searchImpressionShare": 0.0,
                "searchBudgetLostImpressionShare": 0.0
            }
        },
        {
            "campaign": {
                "resourceName": "customers/4941701449/campaigns/17324490442",
                "id": "17324490442",
                "name": "T2MD | Search | Roses 152 29/8 140 14/1 155 16/6 Port 150 16/6 AI Max 1/7 160 3/7 150 23/10",
                "status": "ENABLED",
                "advertisingChannelType": "SEARCH"
            },
            "metrics": {
                "costMicros": "82865492",
                "conversionsValue": 76.942566,
                "conversions": 4.0,
                "clicks": "115",
                "impressions": "1284",
                "searchImpressionShare": 0.0,
                "searchBudgetLostImpressionShare": 0.0
            }
        },
        {
            "campaign": {
                "resourceName": "customers/4941701449/campaigns/10492045139",
                "id": "10492045139",
                "name": "T2MD | DSA 160 150 5/12 140 7/4",
                "status": "ENABLED",
                "advertisingChannelType": "SEARCH"
            },
            "metrics": {
                "costMicros": "76012110",
                "conversionsValue": 176.707869001,
                "conversions": 6.352664,
                "clicks": "90",
                "impressions": "1278",
                "searchImpressionShare": 0.0,
                "searchBudgetLostImpressionShare": 0.0
            }
        },
        {
            "campaign": {
                "resourceName": "customers/4941701449/campaigns/22122810626",
                "id": "22122810626",
                "name": "T2MD | Shopping | Low Traffic 150 13/1 140 7/4 150 18/5 160 3/9 150 5/9 140 23/10",
                "status": "ENABLED",
                "advertisingChannelType": "SHOPPING"
            },
            "metrics": {
                "costMicros": "69340000",
                "conversionsValue": 99.713329233,
                "conversions": 6.979778,
                "clicks": "93",
                "impressions": "13109",
                "searchImpressionShare": 0.0,
                "searchBudgetLostImpressionShare": 0.0
            }
        },
        {
            "campaign": {
                "resourceName": "customers/4941701449/campaigns/598474059",
                "id": "598474059",
                "name": "T2MD | Brand Inclusion  120  14/7 Ai Max 11/11",
                "status": "ENABLED",
                "advertisingChannelType": "SEARCH"
            },
            "metrics": {
                "costMicros": "46125627",
                "conversionsValue": 98.264533,
                "conversions": 5.0,
                "clicks": "62",
                "impressions": "214",
                "searchImpressionShare": 0.0,
                "searchBudgetLostImpressionShare": 0.0
            }
        },
        {
            "campaign": {
                "resourceName": "customers/4941701449/campaigns/18441497267",
                "id": "18441497267",
                "name": "T2MD | Search | Memorial Gift 150 20/5 140 7/4 Port 150  16/6 AI Max 28/7 144",
                "status": "ENABLED",
                "advertisingChannelType": "SEARCH"
            },
            "metrics": {
                "costMicros": "43541747",
                "conversionsValue": 23.1854915,
                "conversions": 0.5,
                "clicks": "95",
                "impressions": "1162",
                "searchImpressionShare": 0.0,
                "searchBudgetLostImpressionShare": 0.0
            }
        }
    ]
}


def transform_campaign_data(mcp_data: dict) -> list:
    """
    Transform MCP data format to analyzer format

    MCP returns {campaign: {...}, metrics: {...}} with camelCase keys
    Analyzer expects {name, status, metrics, ...} with snake_case keys
    """
    transformed_campaigns = []

    for result in mcp_data['results']:
        campaign_info = result['campaign']
        raw_metrics = result['metrics']

        # Transform metrics from camelCase to snake_case and proper types
        metrics = {
            'cost_micros': int(raw_metrics['costMicros']),
            'conversions_value': float(raw_metrics['conversionsValue']),
            'conversions': float(raw_metrics['conversions']),
            'clicks': int(raw_metrics['clicks']),
            'impressions': int(raw_metrics['impressions']),
            'search_impression_share': float(raw_metrics.get('searchImpressionShare', 0)),
            'search_budget_lost_impression_share': float(raw_metrics.get('searchBudgetLostImpressionShare', 0))
        }

        # Flatten structure
        transformed_campaign = {
            'name': campaign_info['name'],
            'id': campaign_info['id'],
            'status': campaign_info['status'],
            'type': campaign_info['advertisingChannelType'],
            'metrics': metrics
        }

        transformed_campaigns.append(transformed_campaign)

    return transformed_campaigns


def main():
    """Run comprehensive Tree2mydoor profit analysis"""

    print("=" * 80)
    print("🌳 TREE2MYDOOR COMPREHENSIVE PROFIT ANALYSIS")
    print("=" * 80)
    print()

    # Initialize analyzer and HTML generator
    print("⚙️  Initializing profit-focused analyzer...")
    analyzer = Tree2mydoorProfitAnalyzer()
    html_generator = Tree2mydoorHTMLGenerator()
    print("✅ Analyzer ready")
    print()

    # Transform campaign data
    print("📊 Processing campaign data...")
    transformed_campaigns = transform_campaign_data(CAMPAIGN_DATA)
    print(f"✅ {len(transformed_campaigns)} campaigns loaded")
    print()

    # Date range (Dec 7-13, 2025 - 3 day conversion lag applied)
    date_range = {
        'start_date': '2025-12-07',
        'end_date': '2025-12-13'
    }

    # Run analysis
    print("🔍 Running profit-focused analysis...")
    print(f"   Period: {date_range['start_date']} to {date_range['end_date']}")
    print(f"   Client: tree2mydoor")
    print()

    analysis = analyzer.analyze_campaigns(
        'tree2mydoor',
        transformed_campaigns,
        date_range
    )

    # Print analysis summary
    print("=" * 80)
    print("📈 ANALYSIS SUMMARY")
    print("=" * 80)
    print()

    # Calculate totals
    total_spend = sum(c['metrics']['spend'] for c in analysis['campaign_analyses'])
    total_profit = sum(c['metrics']['revenue'] for c in analysis['campaign_analyses'])  # Actually profit
    total_conversions = sum(c['metrics']['conversions'] for c in analysis['campaign_analyses'])
    account_poas = total_profit / total_spend if total_spend > 0 else 0

    print(f"Health Score: {analysis['health_score']}/100")
    print(f"Total Spend: £{total_spend:,.2f}")
    print(f"Total Profit: £{total_profit:,.2f} (conversions_value = PROFIT)")
    print(f"Account POAS: {account_poas:.2f}x (target: 1.60x)")
    print(f"Total Conversions: {total_conversions:.0f}")
    print()

    # Profit context
    print("💰 PROFIT CONTEXT:")
    profit_ctx = analysis.get('profit_context', {})
    print(f"   Uses ProfitMetrics: {profit_ctx.get('uses_profitmetrics')}")
    print(f"   Target POAS: {profit_ctx.get('target_poas'):.2f}x")
    print(f"   Optimization Focus: {profit_ctx.get('optimization_focus')}")
    print()

    # Tier distribution
    print("📊 TIER DISTRIBUTION:")
    tier_guidance = analysis.get('tier_guidance', {})
    tier_dist = tier_guidance.get('tier_distribution', {})
    for tier, count in tier_dist.items():
        print(f"   {tier}: {count} campaigns")
    print()

    # Seasonality
    print("🎄 SEASONALITY:")
    seasonality = analysis.get('seasonality_context', {})
    print(f"   Season: {seasonality.get('season_name')}")
    print(f"   Peak Season: {'YES' if seasonality.get('is_peak_season') else 'NO'}")
    print()

    # Recommendations
    print("🎯 RECOMMENDATIONS:")
    recommendations = analysis.get('recommendations', [])
    print(f"   Total: {len(recommendations)}")
    for i, rec in enumerate(recommendations, 1):
        priority = rec.get('priority', 'P?')
        title = rec.get('title', 'Unknown')
        print(f"   {i}. [{priority}] {title}")
    print()

    # Generate HTML report
    print("=" * 80)
    print("📄 GENERATING HTML REPORT")
    print("=" * 80)
    print()

    print("⚙️  Generating HTML...")
    html = html_generator.generate_html_report(
        analysis,
        'Tree2mydoor',
        (date_range['start_date'], date_range['end_date'])
    )
    print(f"✅ HTML generated ({len(html):,} bytes)")
    print()

    # Save report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f'tree2mydoor_profit_analysis_{timestamp}.html'
    output_path = Path(__file__).parent / 'reports' / output_filename

    print(f"💾 Saving report...")
    output_path.parent.mkdir(exist_ok=True, parents=True)
    output_path.write_text(html)
    print(f"✅ Saved to: {output_path}")
    print()

    # Also save JSON for reference
    json_filename = f'tree2mydoor_profit_analysis_{timestamp}.json'
    json_path = Path(__file__).parent / 'reports' / json_filename
    json_path.write_text(json.dumps(analysis, indent=2))
    print(f"✅ JSON saved to: {json_path}")
    print()

    # Open in browser
    print("🌐 Opening report in browser...")
    import subprocess
    subprocess.run(['open', str(output_path)], check=False)
    print("✅ Report opened")
    print()

    print("=" * 80)
    print("✅ PROFIT ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print("Key Features:")
    print("✓ POAS (Profit on Ad Spend) terminology throughout")
    print("✓ Tier A/B/C campaign assessment")
    print("✓ Product Hero optimization guidance")
    print("✓ Seasonality context (December peak season)")
    print("✓ Comprehensive profit-focused recommendations")
    print("✓ Client-specific considerations (Gareth's needs)")
    print()


if __name__ == '__main__':
    main()
