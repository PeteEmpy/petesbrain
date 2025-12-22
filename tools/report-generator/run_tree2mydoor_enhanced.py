#!/usr/bin/env python3
"""
Run Tree2mydoor Campaign Insights with Enhanced Analysis
Dec 7-13, 2025 (with 3-day conversion lag)
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from campaign_analyzer import CampaignAnalyzer
from report_html_generator import HTMLReportGenerator

# Real MCP data from Dec 7-13, 2025
CAMPAIGN_DATA = {"results":[{"campaign":{"resourceName":"customers/4941701449/campaigns/15820346778","status":"ENABLED","advertisingChannelType":"PERFORMANCE_MAX","name":"T2MD | P Max | HP&P 150 5/9 140 23/10","id":"15820346778"},"metrics":{"clicks":"1336","searchBudgetLostImpressionShare":0.005434782608695652,"searchImpressionShare":0.41052546077504726,"conversionsValue":1948.24986613,"conversions":101.571985,"costMicros":"1356584153","impressions":"95834"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/22986754502","status":"ENABLED","advertisingChannelType":"SHOPPING","name":"T2MD | Shopping | Catch All 170 150 20/10 140 23/10","id":"22986754502"},"metrics":{"clicks":"404","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.5741788769155232,"conversionsValue":498.127685649,"conversions":29.743024,"costMicros":"319690000","impressions":"42166"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/598475433","status":"ENABLED","advertisingChannelType":"SEARCH","name":"T2MD | Search | Trees Port 150 16/6 Ai 4/8 Lemon paused 20/8 131 3/9","id":"598475433"},"metrics":{"clicks":"292","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.0999,"conversionsValue":303.426671595,"conversions":14.568833,"costMicros":"218174750","impressions":"3836"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/21610656469","status":"ENABLED","advertisingChannelType":"PERFORMANCE_MAX","name":"T2MD | P Max Shopping | Unprofitable 150 160 3/9 150 5/9 140 23/10","id":"21610656469"},"metrics":{"clicks":"115","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.6453696343402225,"conversionsValue":130.75660092,"conversions":6.870694,"costMicros":"111423985","impressions":"17294"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/17324490442","status":"ENABLED","advertisingChannelType":"SEARCH","name":"T2MD | Search | Roses 152 29/8 140 14/1 155 16/6 Port 150 16/6 AI Max 1/7 160 3/7 150 23/10","id":"17324490442"},"metrics":{"clicks":"115","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.0999,"conversionsValue":76.942566,"conversions":4,"costMicros":"82865492","impressions":"1284"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/10492045139","status":"ENABLED","advertisingChannelType":"SEARCH","name":"T2MD | DSA 160 150 5/12 140 7/4","id":"10492045139"},"metrics":{"clicks":"90","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.0999,"conversionsValue":176.707869001,"conversions":6.352664,"costMicros":"76012110","impressions":"1278"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/22122810626","status":"ENABLED","advertisingChannelType":"SHOPPING","name":"T2MD | Shopping | Low Traffic 150 13/1 140 7/4 150 18/5 160 3/9 150 5/9 140 23/10","id":"22122810626"},"metrics":{"clicks":"93","searchBudgetLostImpressionShare":0.5896853967757083,"searchImpressionShare":0.4100015651901706,"conversionsValue":99.713329233,"conversions":6.979778,"costMicros":"69340000","impressions":"13109"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/598474059","status":"ENABLED","advertisingChannelType":"SEARCH","name":"T2MD | Brand Inclusion  120  14/7 Ai Max 11/11","id":"598474059"},"metrics":{"clicks":"62","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.9126984126984127,"conversionsValue":98.264533,"conversions":5,"costMicros":"46125627","impressions":"214"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/18441497267","status":"ENABLED","advertisingChannelType":"SEARCH","name":"T2MD | Search | Memorial Gift 150 20/5 140 7/4 Port 150  16/6 AI Max 28/7 144","id":"18441497267"},"metrics":{"clicks":"95","searchBudgetLostImpressionShare":0.0006349710294467815,"searchImpressionShare":0.0999,"conversionsValue":23.1854915,"conversions":0.5,"costMicros":"43541747","impressions":"1162"}}],"query":"SELECT\n    campaign.id,\n    campaign.name,\n    campaign.status,\n    campaign.advertising_channel_type,\n    metrics.cost_micros,\n    metrics.conversions_value,\n    metrics.conversions,\n    metrics.clicks,\n    metrics.impressions,\n    metrics.search_impression_share,\n    metrics.search_budget_lost_impression_share\nFROM campaign\nWHERE\n    segments.date >= '2025-12-07'\n    AND segments.date <= '2025-12-13'\n    AND metrics.cost_micros > 0\nORDER BY metrics.cost_micros DESC","totalRows":9}

# Product data (aggregated)
PRODUCT_DATA = {"results": [
    {"segments": {"productItemId": "01090", "productTitle": "The Olive Tree Gift - 2L pot, 50cm Height"}, "metrics": {"clicks": "296", "conversionsValue": 440.53, "conversions": 24, "costMicros": "280450000", "impressions": "10000"}},
    {"segments": {"productItemId": "00287", "productTitle": "The Olive Tree Gift - Large (5L pot, 80cm height)"}, "metrics": {"clicks": "148", "conversionsValue": 299.54, "conversions": 12, "costMicros": "257500000", "impressions": "8000"}},
    {"segments": {"productItemId": "00593", "productTitle": "Lemon Tree Gift - Large 5L pot, 50-60cm High"}, "metrics": {"clicks": "40", "conversionsValue": 96.45, "conversions": 3, "costMicros": "77330000", "impressions": "3000"}},
    {"segments": {"productItemId": "aprbg", "productTitle": "At Peace Rose Bush Gift - The Perfect Memorial"}, "metrics": {"clicks": "34", "conversionsValue": 18.99, "conversions": 3, "costMicros": "25230000", "impressions": "2000"}}
]}

def main():
    print("=" * 100)
    print("TREE2MYDOOR CAMPAIGN INSIGHTS REPORT")
    print("=" * 100)
    print("Date Range: 2025-12-07 to 2025-12-13 (with 3-day conversion lag)")
    print()

    # Initialize analyzer
    analyzer = CampaignAnalyzer()

    # Client slug and date range
    client_slug = 'tree2mydoor'
    date_range = {
        'start_date': '2025-12-07',
        'end_date': '2025-12-13'
    }

    # Transform MCP data format to analyzer format
    # MCP returns {campaign: {...}, metrics: {...}} with camelCase keys
    # Analyzer expects {name, status, metrics, ...} with snake_case keys
    transformed_campaigns = []
    for result in CAMPAIGN_DATA['results']:
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

    print("Analysing campaigns and products...")
    analysis = analyzer.analyze_campaigns(client_slug, transformed_campaigns, date_range)

    # Display summary
    print("\n" + "=" * 100)
    print("CAMPAIGN PERFORMANCE SUMMARY")
    print("=" * 100)

    print(f"\nTotal Campaigns: {len(analysis['campaign_analyses'])}")
    total_spend = sum(c['metrics']['spend'] for c in analysis['campaign_analyses'])
    total_revenue = sum(c['metrics']['revenue'] for c in analysis['campaign_analyses'])
    total_conversions = sum(c['metrics']['conversions'] for c in analysis['campaign_analyses'])
    blended_roas = total_revenue / total_spend if total_spend > 0 else 0

    # Calculate health status label
    health_score = analysis['health_score']
    health_status = "Excellent" if health_score >= 90 else \
                   "Good" if health_score >= 75 else \
                   "Fair" if health_score >= 60 else \
                   "Poor" if health_score >= 40 else "Critical"

    print(f"Total Spend: £{total_spend:,.2f}")
    print(f"Total Revenue: £{total_revenue:,.2f}")
    print(f"Blended ROAS: {blended_roas:.2f}x")
    print(f"Total Conversions: {total_conversions:.0f}")
    print(f"Health Score: {health_score}/100 ({health_status})")

    # Display recommendations
    print("\n" + "=" * 100)
    print("PRIORITY RECOMMENDATIONS")
    print("=" * 100)

    for i, rec in enumerate(analysis['recommendations'][:5], 1):  # Top 5
        print(f"\n[{rec['priority']}] {rec['title']}")
        print(f"Affected Campaigns: {rec['affected_campaigns']}")
        print(f"Total Spend: £{rec['impact']['total_spend']:,.2f}")
        print(f"Average ROAS: {rec['impact']['avg_roas']:.2f}x")
        print("\nRecommendation:")
        # Print first 500 chars of recommendation
        rec_text = rec['recommendation']
        if len(rec_text) > 500:
            print(rec_text[:500] + "...")
        else:
            print(rec_text)
        print("\nNext Steps:")
        for step in rec['next_steps']:
            print(f"  ✓ {step}")

    # Save JSON report
    print("\n" + "=" * 100)
    print("SAVING REPORTS")
    print("=" * 100)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save JSON
    output_path = Path(__file__).parent / 'reports' / f"tree2mydoor_insights_{timestamp}.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(analysis, indent=2))
    print(f"✓ JSON report saved: {output_path}")

    # Generate and open HTML report
    html_generator = HTMLReportGenerator()
    html_content = html_generator.generate_html_report(
        analysis,
        'Tree2mydoor',
        ('2025-12-07', '2025-12-13')
    )

    html_path = output_path.parent / f"tree2mydoor_insights_{timestamp}.html"
    html_generator.save_and_open_report(html_content, html_path)
    print(f"✓ HTML report generated: {html_path}")
    print(f"✓ Opening in browser...")

    print("\n" + "=" * 100)
    print("REPORT GENERATION COMPLETE")
    print("=" * 100)

if __name__ == '__main__':
    main()
