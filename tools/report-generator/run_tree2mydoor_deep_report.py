#!/usr/bin/env python3
"""
Generate Deep Audit Report for Tree2mydoor

This uses the Tree2mydoorDeepAuditor which provides:
- Configuration audits (not just metrics)
- Root cause analysis
- Best practice validation
- Knowledge base insights
- Specific actionable fixes
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import subprocess

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from tree2mydoor_deep_auditor import Tree2mydoorDeepAuditor
from tree2mydoor_deep_html_standalone import generate_deep_audit_html


# Real Tree2mydoor data from Dec 7-13, 2025
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
    """Transform MCP data format to analyzer format"""

    transformed_campaigns = []

    for result in mcp_data['results']:
        campaign_info = result['campaign']
        raw_metrics = result['metrics']

        metrics = {
            'cost_micros': int(raw_metrics['costMicros']),
            'conversions_value': float(raw_metrics['conversionsValue']),
            'conversions': float(raw_metrics['conversions']),
            'clicks': int(raw_metrics['clicks']),
            'impressions': int(raw_metrics['impressions']),
            'search_impression_share': float(raw_metrics.get('searchImpressionShare', 0)),
            'search_budget_lost_impression_share': float(raw_metrics.get('searchBudgetLostImpressionShare', 0))
        }

        # Calculate derived metrics
        spend = metrics['cost_micros'] / 1_000_000
        revenue = metrics['conversions_value']  # Actually profit for Tree2mydoor
        roas = revenue / spend if spend > 0 else 0

        metrics['spend'] = spend
        metrics['revenue'] = revenue  # Called revenue but actually profit
        metrics['roas'] = roas  # Called ROAS but actually POAS

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
    """Run deep audit analysis"""

    print("=" * 80)
    print("🌳 TREE2MYDOOR DEEP ACCOUNT AUDIT")
    print("=" * 80)
    print()

    # Initialize deep auditor
    print("⚙️  Initializing deep auditor...")
    auditor = Tree2mydoorDeepAuditor()
    print("✅ Deep auditor ready")
    print()

    # Transform campaign data
    print("📊 Processing campaign data...")
    transformed_campaigns = transform_campaign_data(CAMPAIGN_DATA)
    print(f"✅ {len(transformed_campaigns)} campaigns loaded")
    print()

    # Date range
    date_range = {
        'start_date': '2025-12-07',
        'end_date': '2025-12-13'
    }

    # Run deep analysis
    print("🔍 Running deep account audit...")
    print(f"   Period: {date_range['start_date']} to {date_range['end_date']}")
    print(f"   This includes:")
    print("   • Configuration auditing")
    print("   • Root cause analysis")
    print("   • Best practice validation")
    print("   • Knowledge base insights")
    print()

    analysis = auditor.analyze_campaigns(
        'tree2mydoor',
        transformed_campaigns,
        date_range
    )

    # Print summary
    print("=" * 80)
    print("📈 AUDIT SUMMARY")
    print("=" * 80)
    print()

    # Totals
    total_spend = sum(c['metrics']['spend'] for c in analysis['campaign_analyses'])
    total_profit = sum(c['metrics']['revenue'] for c in analysis['campaign_analyses'])
    total_conversions = sum(c['metrics']['conversions'] for c in analysis['campaign_analyses'])
    account_poas = total_profit / total_spend if total_spend > 0 else 0

    print(f"Health Score: {analysis['health_score']}/100")
    print(f"Total Spend: £{total_spend:,.2f}")
    print(f"Total Profit: £{total_profit:,.2f} (conversions_value = PROFIT)")
    print(f"Account POAS: {account_poas:.2f}x (target: 1.60x)")
    print(f"Total Conversions: {total_conversions:.0f}")
    print()

    # Deep audits
    print("🔍 DEEP AUDITS:")
    deep_audits = analysis.get('deep_audits', {})

    perf_issues = deep_audits.get('performance_issues', [])
    budget_issues = deep_audits.get('budget_issues', [])
    hero_recs = deep_audits.get('product_hero_recommendations', [])
    seasonal_issues = deep_audits.get('seasonal_issues', [])

    print(f"   Performance Issues: {len(perf_issues)}")
    print(f"   Budget Issues: {len(budget_issues)}")
    print(f"   Product Hero Recommendations: {len(hero_recs)}")
    print(f"   Seasonal Issues: {len(seasonal_issues)}")
    print()

    # Root causes
    print("🎯 ROOT CAUSE ANALYSES:")
    root_causes = analysis.get('root_cause_analyses', [])
    print(f"   {len(root_causes)} campaigns analyzed for root causes")
    for rc in root_causes:
        print(f"   • {rc['campaign']}: {len(rc.get('likely_causes', []))} causes identified")
    print()

    # KB insights
    print("💡 KNOWLEDGE BASE INSIGHTS:")
    kb_insights = analysis.get('kb_insights', {})
    key_recs = kb_insights.get('key_recommendations', [])
    print(f"   {len(key_recs)} strategic insights from knowledge base")
    for insight in key_recs:
        print(f"   • {insight['topic']}")
    print()

    # Recommendations
    print("🎯 RECOMMENDATIONS:")
    recommendations = analysis.get('recommendations', [])
    p0_count = len([r for r in recommendations if r.get('priority') == 'P0'])
    p1_count = len([r for r in recommendations if r.get('priority') == 'P1'])
    p2_count = len([r for r in recommendations if r.get('priority') == 'P2'])

    print(f"   Total: {len(recommendations)}")
    print(f"   P0 (Critical): {p0_count}")
    print(f"   P1 (Important): {p1_count}")
    print(f"   P2 (Normal): {p2_count}")
    print()

    # Generate HTML report
    print("=" * 80)
    print("📄 GENERATING HTML REPORT")
    print("=" * 80)
    print()

    print("⚙️  Generating HTML with deep audit sections...")
    html = generate_deep_audit_html(
        analysis,
        'Tree2mydoor',
        (date_range['start_date'], date_range['end_date'])
    )
    print(f"✅ HTML generated ({len(html):,} bytes)")
    print()

    # Save report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f'tree2mydoor_deep_audit_{timestamp}.html'
    output_path = Path(__file__).parent / 'reports' / output_filename

    print(f"💾 Saving report...")
    output_path.parent.mkdir(exist_ok=True, parents=True)
    output_path.write_text(html)
    print(f"✅ Saved to: {output_path}")
    print()

    # Save JSON
    json_filename = f'tree2mydoor_deep_audit_{timestamp}.json'
    json_path = Path(__file__).parent / 'reports' / json_filename
    json_path.write_text(json.dumps(analysis, indent=2, default=str))
    print(f"✅ JSON saved to: {json_path}")
    print()

    # Open in browser
    print("🌐 Opening report in browser...")
    subprocess.run(['open', str(output_path)], check=False)
    print("✅ Report opened")
    print()

    print("=" * 80)
    print("✅ DEEP AUDIT COMPLETE")
    print("=" * 80)
    print()
    print("Key Features:")
    print("✓ Configuration auditing (not just metrics)")
    print("✓ Root cause analysis for underperformers")
    print("✓ Best practice validation")
    print("✓ Knowledge base-informed insights")
    print("✓ Specific actionable fixes with expected outcomes")
    print("✓ POAS (Profit on Ad Spend) terminology throughout")
    print("✓ Product Hero optimization guidance")
    print("✓ Seasonality awareness (December peak season)")
    print()


if __name__ == '__main__':
    main()
