#!/usr/bin/env python3
"""
Test Campaign Analyzer with Real MCP Data

This script demonstrates how to use the campaign analyzer with real Google Ads data
fetched via MCP from Claude Code.
"""

import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from campaign_analyzer import CampaignAnalyzer
from context_parser import ClientContextParser

def transform_mcp_data_to_analyzer_format(mcp_results):
    """
    Transform MCP Google Ads results into format expected by CampaignAnalyzer

    Args:
        mcp_results: Raw MCP results dict with 'results' key

    Returns:
        List of campaign dicts in analyzer format
    """
    campaigns = []

    for row in mcp_results.get('results', []):
        campaign_info = row.get('campaign', {})
        metrics = row.get('metrics', {})

        campaign_data = {
            'id': campaign_info.get('id', ''),
            'name': campaign_info.get('name', ''),
            'status': campaign_info.get('status', ''),
            'advertising_channel_type': campaign_info.get('advertisingChannelType', ''),
            'metrics': {
                # Convert string values to appropriate types
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


def main():
    """Test with real Tree2mydoor data"""

    # Real MCP data from Tree2mydoor (2025-12-08 to 2025-12-15)
    mcp_data = {
        "results": [
            {"campaign": {"resourceName": "customers/4941701449/campaigns/15820346778", "status": "ENABLED", "advertisingChannelType": "PERFORMANCE_MAX", "name": "T2MD | P Max | HP&P 150 5/9 140 23/10", "id": "15820346778"}, "metrics": {"clicks": "1411", "searchBudgetLostImpressionShare": 0.0063900817695158535, "searchImpressionShare": 0.3959350550032355, "conversionsValue": 2357.457950454, "conversions": 111.317844, "costMicros": "1452631485", "impressions": "99101"}},
            {"campaign": {"resourceName": "customers/4941701449/campaigns/22986754502", "status": "ENABLED", "advertisingChannelType": "SHOPPING", "name": "T2MD | Shopping | Catch All 170 150 20/10 140 23/10", "id": "22986754502"}, "metrics": {"clicks": "614", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.581711229946524, "conversionsValue": 671.751151649, "conversions": 38.743024, "costMicros": "549330000", "impressions": "67519"}},
            {"campaign": {"resourceName": "customers/4941701449/campaigns/598475433", "status": "ENABLED", "advertisingChannelType": "SEARCH", "name": "T2MD | Search | Trees Port 150 16/6 Ai 4/8 Lemon paused 20/8 131 3/9", "id": "598475433"}, "metrics": {"clicks": "425", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.0999, "conversionsValue": 342.269149873, "conversions": 15.500001, "costMicros": "327654345", "impressions": "5727"}},
            {"campaign": {"resourceName": "customers/4941701449/campaigns/17324490442", "status": "ENABLED", "advertisingChannelType": "SEARCH", "name": "T2MD | Search | Roses 152 29/8 140 14/1 155 16/6 Port 150 16/6 AI Max 1/7 160 3/7 150 23/10", "id": "17324490442"}, "metrics": {"clicks": "166", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.0999, "conversionsValue": 64.712266, "conversions": 3, "costMicros": "120797622", "impressions": "1619"}},
            {"campaign": {"resourceName": "customers/4941701449/campaigns/10492045139", "status": "ENABLED", "advertisingChannelType": "SEARCH", "name": "T2MD | DSA 160 150 5/12 140 7/4", "id": "10492045139"}, "metrics": {"clicks": "126", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.0999, "conversionsValue": 194.11681104, "conversions": 7.285755, "costMicros": "103624846", "impressions": "1587"}},
            {"campaign": {"resourceName": "customers/4941701449/campaigns/21610656469", "status": "ENABLED", "advertisingChannelType": "PERFORMANCE_MAX", "name": "T2MD | P Max Shopping | Unprofitable 150 160 3/9 150 5/9 140 23/10", "id": "21610656469"}, "metrics": {"clicks": "89", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.622912674514098, "conversionsValue": 118.33046792, "conversions": 5.870694, "costMicros": "96941342", "impressions": "13506"}},
            {"campaign": {"resourceName": "customers/4941701449/campaigns/22122810626", "status": "ENABLED", "advertisingChannelType": "SHOPPING", "name": "T2MD | Shopping | Low Traffic 150 13/1 140 7/4 150 18/5 160 3/9 150 5/9 140 23/10", "id": "22122810626"}, "metrics": {"clicks": "100", "searchBudgetLostImpressionShare": 0.5788034737857832, "searchImpressionShare": 0.42087487938243806, "conversionsValue": 110.981962233, "conversions": 7.979778, "costMicros": "77140000", "impressions": "14943"}},
            {"campaign": {"resourceName": "customers/4941701449/campaigns/598474059", "status": "ENABLED", "advertisingChannelType": "SEARCH", "name": "T2MD | Brand Inclusion  120  14/7 Ai Max 11/11", "id": "598474059"}, "metrics": {"clicks": "80", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.8867924528301887, "conversionsValue": 93.7914665, "conversions": 4.5, "costMicros": "64897286", "impressions": "264"}},
            {"campaign": {"resourceName": "customers/4941701449/campaigns/18441497267", "status": "ENABLED", "advertisingChannelType": "SEARCH", "name": "T2MD | Search | Memorial Gift 150 20/5 140 7/4 Port 150  16/6 AI Max 28/7 144", "id": "18441497267"}, "metrics": {"clicks": "122", "searchBudgetLostImpressionShare": 0.0005074854097944684, "searchImpressionShare": 0.0999, "conversionsValue": 35.7341245, "conversions": 1.5, "costMicros": "63670828", "impressions": "1528"}}
        ]
    }

    # Transform to analyzer format
    campaigns = transform_mcp_data_to_analyzer_format(mcp_data)

    print(f"Transformed {len(campaigns)} campaigns from MCP format")
    print(f"\nTotal spend: £{sum(c['metrics']['cost_micros'] for c in campaigns) / 1_000_000:.2f}")
    print(f"Total revenue: £{sum(c['metrics']['conversions_value'] for c in campaigns):.2f}")

    # Load client context
    context_parser = ClientContextParser()
    client_context = context_parser.load_client_context('tree2mydoor')

    if client_context:
        print(f"\nLoaded Tree2mydoor context:")
        print(f"  Target ROAS: {client_context.get('performance_targets', {}).get('target_roas', 'Not set')}")
        print(f"  Known issues: {len(client_context.get('known_issues', []))} found")

    # Analyze with CampaignAnalyzer
    analyzer = CampaignAnalyzer()
    analysis = analyzer.analyze_campaigns(
        client_slug='tree2mydoor',
        campaign_data=campaigns,
        date_range={'start_date': '2025-12-08', 'end_date': '2025-12-15'}
    )

    # Display results
    print("\n" + "="*80)
    print(f"CAMPAIGN ANALYSIS - TREE2MYDOOR")
    print("="*80)
    print(f"\nDate Range: 2025-12-08 to 2025-12-15")
    print(f"Health Score: {analysis['health_score']}/100")
    print(f"\n{analysis['summary']}")

    # Show recommendations
    if analysis['recommendations']:
        print("\n" + "-"*80)
        print("PRIORITIZED RECOMMENDATIONS")
        print("-"*80)
        for i, rec in enumerate(analysis['recommendations'][:5], 1):
            print(f"\n{i}. [{rec['priority']}] {rec['title']}")
            print(f"   Affected: {rec['affected_campaigns']} campaign(s)")
            impact = rec['impact']
            print(f"   Impact: £{impact['total_spend']:.2f} spend, {impact['avg_roas']:.2f}x ROAS")

            # Show recommendation text (indented)
            print(f"\n   Recommendation:")
            for line in rec['recommendation'].split('\n'):
                print(f"   {line}")

            # Show next steps
            if rec.get('next_steps'):
                print(f"\n   Next Steps:")
                for step in rec['next_steps']:
                    print(f"   • {step}")

            # Show KB articles
            if rec.get('kb_articles'):
                print(f"\n   KB Articles ({len(rec['kb_articles'])} found):")
                for article in rec['kb_articles'][:3]:
                    print(f"   • {article['title']}")

    # Save full report
    output_path = Path(__file__).parent / 'reports' / 'tree2mydoor_real_data_test.json'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(analysis, indent=2))
    print(f"\n\nFull report saved to: {output_path}")


if __name__ == '__main__':
    main()
