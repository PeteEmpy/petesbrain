#!/usr/bin/env python3
"""
Generate Tree2mydoor Campaign Analysis Report with Real MCP Data
Produces actionable insights and recommendations for campaign optimisation
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from campaign_analyzer import CampaignAnalyzer
from report_html_generator import HTMLReportGenerator

# Real campaign data from Tree2mydoor (2025-12-09 to 2025-12-15)
CAMPAIGN_DATA = {
    "results": [
        {"campaign": {"id": "15820346778", "name": "T2MD | P Max | HP&P 150 5/9 140 23/10", "status": "ENABLED", "advertisingChannelType": "PERFORMANCE_MAX"}, "metrics": {"clicks": "1150", "searchBudgetLostImpressionShare": 0.007762185917304583, "searchImpressionShare": 0.3901012031834788, "conversionsValue": 1886.852265593, "conversions": 86.530741, "costMicros": "1185222677", "impressions": "82121"}},
        {"campaign": {"id": "22986754502", "name": "T2MD | Shopping | Catch All 170 150 20/10 140 23/10", "status": "ENABLED", "advertisingChannelType": "SHOPPING"}, "metrics": {"clicks": "586", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.5879894612519306, "conversionsValue": 651.010549013, "conversions": 36.793093, "costMicros": "536230000", "impressions": "65103"}},
        {"campaign": {"id": "598475433", "name": "T2MD | Search | Trees Port 150 16/6 Ai 4/8 Lemon paused 20/8 131 3/9", "status": "ENABLED", "advertisingChannelType": "SEARCH"}, "metrics": {"clicks": "382", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.0999, "conversionsValue": 369.180326779, "conversions": 15.431168, "costMicros": "296928774", "impressions": "5134"}},
        {"campaign": {"id": "17324490442", "name": "T2MD | Search | Roses 152 29/8 140 14/1 155 16/6 Port 150 16/6 AI Max 1/7 160 3/7 150 23/10", "status": "ENABLED", "advertisingChannelType": "SEARCH"}, "metrics": {"clicks": "157", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.0999, "conversionsValue": 64.712266, "conversions": 3, "costMicros": "115313518", "impressions": "1445"}},
        {"campaign": {"id": "10492045139", "name": "T2MD | DSA 160 150 5/12 140 7/4", "status": "ENABLED", "advertisingChannelType": "SEARCH"}, "metrics": {"clicks": "113", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.0999, "conversionsValue": 164.450653498, "conversions": 6.384349, "costMicros": "93023033", "impressions": "1397"}},
        {"campaign": {"id": "21610656469", "name": "T2MD | P Max Shopping | Unprofitable 150 160 3/9 150 5/9 140 23/10", "status": "ENABLED", "advertisingChannelType": "PERFORMANCE_MAX"}, "metrics": {"clicks": "56", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.6152491192752894, "conversionsValue": 57.335467728, "conversions": 2.94752, "costMicros": "67975763", "impressions": "8352"}},
        {"campaign": {"id": "22122810626", "name": "T2MD | Shopping | Low Traffic 150 13/1 140 7/4 150 18/5 160 3/9 150 5/9 140 23/10", "status": "ENABLED", "advertisingChannelType": "SHOPPING"}, "metrics": {"clicks": "87", "searchBudgetLostImpressionShare": 0.5715539947322212, "searchImpressionShare": 0.4281826163301141, "conversionsValue": 87.114533, "conversions": 5, "costMicros": "67220000", "impressions": "13992"}},
        {"campaign": {"id": "598474059", "name": "T2MD | Brand Inclusion  120  14/7 Ai Max 11/11", "status": "ENABLED", "advertisingChannelType": "SEARCH"}, "metrics": {"clicks": "70", "searchBudgetLostImpressionShare": 0, "searchImpressionShare": 0.8857142857142857, "conversionsValue": 89.3184, "conversions": 4, "costMicros": "57847286", "impressions": "230"}},
        {"campaign": {"id": "18441497267", "name": "T2MD | Search | Memorial Gift 150 20/5 140 7/4 Port 150  16/6 AI Max 28/7 144", "status": "ENABLED", "advertisingChannelType": "SEARCH"}, "metrics": {"clicks": "100", "searchBudgetLostImpressionShare": 0.0005843254692863925, "searchImpressionShare": 0.0999, "conversionsValue": 12.548633, "conversions": 1, "costMicros": "54423616", "impressions": "1298"}}
    ]
}

# Real product data (top 100 by spend)
PRODUCT_DATA = {
    "results": [
        {"segments": {"date": "2025-12-10", "productItemId": "01090", "productTitle": "The Olive Tree Gift - 2L pot, 50cm Height"}, "metrics": {"clicks": "69", "conversionsValue": 116.096949, "conversions": 7.5, "costMicros": "62380000", "impressions": "4228"}},
        {"segments": {"date": "2025-12-10", "productItemId": "00287", "productTitle": "The Olive Tree Gift - Large (5L pot, 80cm height)"}, "metrics": {"clicks": "25", "conversionsValue": 55.7556, "conversions": 3, "costMicros": "59340000", "impressions": "1413"}},
        {"segments": {"date": "2025-12-12", "productItemId": "01090", "productTitle": "The Olive Tree Gift - 2L pot, 50cm Height"}, "metrics": {"clicks": "45", "conversionsValue": 105.775216, "conversions": 4, "costMicros": "53933873", "impressions": "4951"}},
        {"segments": {"date": "2025-12-14", "productItemId": "00287", "productTitle": "The Olive Tree Gift - Large (5L pot, 80cm height)"}, "metrics": {"clicks": "24", "conversionsValue": 71.24545, "conversions": 3, "costMicros": "45230000", "impressions": "1835"}},
        {"segments": {"date": "2025-12-14", "productItemId": "01090", "productTitle": "The Olive Tree Gift - 2L pot, 50cm Height"}, "metrics": {"clicks": "43", "conversionsValue": 166.587482, "conversions": 9, "costMicros": "42980000", "impressions": "4507"}},
        {"segments": {"date": "2025-12-15", "productItemId": "00287", "productTitle": "The Olive Tree Gift - Large (5L pot, 80cm height)"}, "metrics": {"clicks": "22", "conversionsValue": 0, "conversions": 0, "costMicros": "38120000", "impressions": "1498"}},
        {"segments": {"date": "2025-12-15", "productItemId": "01090", "productTitle": "The Olive Tree Gift - 2L pot, 50cm Height"}, "metrics": {"clicks": "38", "conversionsValue": 0, "conversions": 0, "costMicros": "36616180", "impressions": "3920"}},
        {"segments": {"date": "2025-12-12", "productItemId": "00287", "productTitle": "The Olive Tree Gift - Large (5L pot, 80cm height)"}, "metrics": {"clicks": "19", "conversionsValue": 77.3853, "conversions": 2, "costMicros": "32820000", "impressions": "1634"}},
        {"segments": {"date": "2025-12-13", "productItemId": "00287", "productTitle": "The Olive Tree Gift - Large (5L pot, 80cm height)"}, "metrics": {"clicks": "20", "conversionsValue": 45.3203, "conversions": 2, "costMicros": "32780000", "impressions": "1740"}},
        {"segments": {"date": "2025-12-13", "productItemId": "01090", "productTitle": "The Olive Tree Gift - 2L pot, 50cm Height"}, "metrics": {"clicks": "34", "conversionsValue": 22.66515, "conversions": 1, "costMicros": "32020938", "impressions": "4351"}},
        {"segments": {"date": "2025-12-14", "productItemId": "00593", "productTitle": "Lemon Tree Gift - Large 5L pot, 50-60cm High"}, "metrics": {"clicks": "16", "conversionsValue": 96.4531, "conversions": 3, "costMicros": "31208967", "impressions": "1589"}},
        {"segments": {"date": "2025-12-09", "productItemId": "01090", "productTitle": "The Olive Tree Gift - 2L pot, 50cm Height"}, "metrics": {"clicks": "33", "conversionsValue": 29.40045, "conversions": 2, "costMicros": "26622138", "impressions": "3047"}},
        {"segments": {"date": "2025-12-11", "productItemId": "01090", "productTitle": "The Olive Tree Gift - 2L pot, 50cm Height"}, "metrics": {"clicks": "34", "conversionsValue": 0, "conversions": 0, "costMicros": "25901208", "impressions": "3049"}},
        {"segments": {"date": "2025-12-12", "productItemId": "aprbg", "productTitle": "At Peace Rose Bush Gift - The Perfect Memorial"}, "metrics": {"clicks": "34", "conversionsValue": 18.986733, "conversions": 3, "costMicros": "25229332", "impressions": "2542"}},
        {"segments": {"date": "2025-12-10", "productItemId": "00593", "productTitle": "Lemon Tree Gift - Large 5L pot, 50-60cm High"}, "metrics": {"clicks": "14", "conversionsValue": 0, "conversions": 0, "costMicros": "24748467", "impressions": "1190"}},
        {"segments": {"date": "2025-12-11", "productItemId": "00287", "productTitle": "The Olive Tree Gift - Large (5L pot, 80cm height)"}, "metrics": {"clicks": "18", "conversionsValue": 25.92515, "conversions": 1, "costMicros": "24650000", "impressions": "1269"}},
        {"segments": {"date": "2025-12-09", "productItemId": "00287", "productTitle": "The Olive Tree Gift - Large (5L pot, 80cm height)"}, "metrics": {"clicks": "20", "conversionsValue": 23.91015, "conversions": 1, "costMicros": "24560000", "impressions": "1266"}},
        {"segments": {"date": "2025-12-15", "productItemId": "00593", "productTitle": "Lemon Tree Gift - Large 5L pot, 50-60cm High"}, "metrics": {"clicks": "10", "conversionsValue": 0, "conversions": 0, "costMicros": "21372783", "impressions": "1432"}}
    ]
}


def transform_campaign_data(raw_data):
    """Transform MCP campaign data to analyzer format"""
    campaigns = []
    for row in raw_data['results']:
        campaign = row['campaign']
        metrics = row['metrics']
        campaigns.append({
            'id': str(campaign['id']),
            'name': campaign['name'],
            'status': campaign['status'],
            'advertising_channel_type': campaign['advertisingChannelType'],
            'metrics': {
                'cost_micros': int(metrics['costMicros']),
                'conversions_value': float(metrics['conversionsValue']),
                'conversions': float(metrics['conversions']),
                'clicks': int(metrics['clicks']),
                'impressions': int(metrics['impressions']),
                'search_impression_share': float(metrics.get('searchImpressionShare', 0)),
                'search_lost_impression_share_budget': float(metrics.get('searchBudgetLostImpressionShare', 0))
            }
        })
    return campaigns


def transform_product_data(raw_data):
    """Transform MCP product data to analyzer format"""
    products = []
    for row in raw_data['results']:
        segments = row['segments']
        metrics = row['metrics']
        products.append({
            'segments': {
                'product_item_id': str(segments['productItemId']),
                'product_title': segments['productTitle'],
                'date': segments['date']
            },
            'metrics': {
                'clicks': int(metrics['clicks']),
                'impressions': int(metrics['impressions']),
                'conversions': float(metrics['conversions']),
                'conversions_value': float(metrics['conversionsValue']),
                'cost_micros': int(metrics['costMicros'])
            },
            'advertising_channel_type': 'SHOPPING'
        })
    return products


print("=" * 100)
print("TREE2MYDOOR CAMPAIGN ANALYSIS WITH ACTIONABLE INSIGHTS")
print("=" * 100)
print()

# Transform data
campaign_data = transform_campaign_data(CAMPAIGN_DATA)
product_data = transform_product_data(PRODUCT_DATA)

print(f"✓ Loaded {len(campaign_data)} campaigns")
print(f"✓ Loaded {len(product_data)} product records (top 18 by spend)")
print()

# Calculate totals
total_spend = sum(c['metrics']['cost_micros'] for c in campaign_data) / 1_000_000
total_revenue = sum(c['metrics']['conversions_value'] for c in campaign_data)
total_conversions = sum(c['metrics']['conversions'] for c in campaign_data)
blended_roas = total_revenue / total_spend if total_spend > 0 else 0

print(f"📊 Campaign Performance (Dec 9-15, 2025):")
print(f"   Total Spend: £{total_spend:,.2f}")
print(f"   Total Revenue: £{total_revenue:,.2f}")
print(f"   Conversions: {total_conversions:.0f}")
print(f"   Blended ROAS: {blended_roas:.2f}x")
print()

# Combine data
combined_data = campaign_data + product_data

# Analyze
print("🔍 Running campaign + product analysis...")
analyzer = CampaignAnalyzer()
analysis = analyzer.analyze_campaigns(
    client_slug='tree2mydoor',
    campaign_data=combined_data,
    date_range={'start_date': '2025-12-09', 'end_date': '2025-12-15'}
)

print(f"✓ Analysis complete")
print()

# Display analysis
print("=" * 100)
print("HEALTH SCORE & SUMMARY")
print("=" * 100)
print(f"Health Score: {analysis['health_score']}/100")
print()
print(analysis['summary'])
print()

# Product analysis
if analysis.get('product_analysis'):
    pa = analysis['product_analysis']
    print("=" * 100)
    print("PRODUCT-LEVEL INSIGHTS")
    print("=" * 100)
    print(f"Total Unique Products: {pa.get('total_products', 0)}")
    print(f"Products with Issues: {pa.get('products_with_issues', 0)}")
    print(f"Disapproved Products: {pa.get('disapproved_products', 0)}")
    print()

    # Top products by spend
    if pa.get('product_metrics'):
        products = list(pa['product_metrics'].values())
        top_products = sorted(products, key=lambda p: p['cost'], reverse=True)[:5]

        print("Top 5 Products by Spend:")
        for i, product in enumerate(top_products, 1):
            roas = (product['revenue'] / product['cost']) if product['cost'] > 0 else 0
            print(f"  {i}. {product['product_title'][:60]}")
            print(f"     Spend: £{product['cost']:.2f} | Revenue: £{product['revenue']:.2f} | ROAS: {roas:.2f}x")
            print(f"     Conversions: {product['conversions']:.0f} | Clicks: {product['clicks']}")
            print()

    # Product issues
    if pa.get('product_issues'):
        print(f"⚠️  Product Issues Detected ({len(pa['product_issues'])}):")
        for issue in pa['product_issues'][:5]:
            print(f"  [{issue['severity']}] {issue['product_title'][:50]} ({issue['product_id']})")
            print(f"      {issue['description']}")
            print(f"      → {issue['recommendation']}")
            print()

# Recommendations
if analysis.get('recommendations'):
    print("=" * 100)
    print("PRIORITISED ACTIONABLE RECOMMENDATIONS")
    print("=" * 100)
    for i, rec in enumerate(analysis['recommendations'], 1):
        print()
        print(f"{i}. [{rec['priority']}] {rec['title']}")
        print(f"   Affected Campaigns: {rec['affected_campaigns']} ({', '.join(rec['campaign_names'][:2])}{', ...' if len(rec['campaign_names']) > 2 else ''})")
        print()

        impact = rec['impact']
        print(f"   💰 Impact: £{impact['total_spend']:.0f} spend | {impact['avg_roas']:.2f}x ROAS")
        print()

        # Recommendation details
        print("   📋 Recommendation:")
        for line in rec['recommendation'].split('\n')[:10]:  # First 10 lines
            if line.strip():
                print(f"   {line}")
        print()

        # Next steps
        if rec.get('next_steps'):
            print("   ✅ Next Steps:")
            for step in rec['next_steps'][:3]:
                print(f"      • {step}")
            print()

        # KB articles
        if rec.get('kb_articles'):
            print(f"   📚 Related KB Articles ({len(rec['kb_articles'])}):")
            for article in rec['kb_articles'][:2]:
                print(f"      • {article['title']}")
            print()

# Save JSON report
output_path = Path(__file__).parent / 'reports' / f"tree2mydoor_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
output_path.parent.mkdir(exist_ok=True)
output_path.write_text(json.dumps(analysis, indent=2))

# Generate and open HTML report
print()
print("=" * 100)
print("GENERATING HTML REPORT FOR BROWSER...")
print("=" * 100)

html_generator = HTMLReportGenerator()
html_content = html_generator.generate_html_report(
    analysis,
    'Tree2mydoor',
    ('2025-12-09', '2025-12-15')
)

html_path = output_path.parent / f"tree2mydoor_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
html_generator.save_and_open_report(html_content, html_path)

print(f"✓ HTML report generated: {html_path}")
print(f"✓ JSON report saved: {output_path}")
print(f"✓ Opening in browser...")
print("=" * 100)
