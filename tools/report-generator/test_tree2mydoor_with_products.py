#!/usr/bin/env python3
"""
Test Tree2mydoor Campaign Analysis with Real Product Data

Demonstrates complete product analysis integration using real MCP data.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from campaign_analyzer import CampaignAnalyzer

# Real campaign data from Tree2mydoor (2025-12-08 to 2025-12-15)
campaign_data_raw = {"results":[{"campaign":{"resourceName":"customers/4941701449/campaigns/15820346778","status":"ENABLED","advertisingChannelType":"PERFORMANCE_MAX","name":"T2MD | P Max | HP&P 150 5/9 140 23/10","id":"15820346778"},"metrics":{"clicks":"1411","searchBudgetLostImpressionShare":0.0063900817695158535,"searchImpressionShare":0.3959350550032355,"conversionsValue":2357.457950454,"conversions":111.317844,"costMicros":"1452631485","impressions":"99100"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/22986754502","status":"ENABLED","advertisingChannelType":"SHOPPING","name":"T2MD | Shopping | Catch All 170 150 20/10 140 23/10","id":"22986754502"},"metrics":{"clicks":"614","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.581711229946524,"conversionsValue":671.751151649,"conversions":38.743024,"costMicros":"549330000","impressions":"67519"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/598475433","status":"ENABLED","advertisingChannelType":"SEARCH","name":"T2MD | Search | Trees Port 150 16/6 Ai 4/8 Lemon paused 20/8 131 3/9","id":"598475433"},"metrics":{"clicks":"425","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.0999,"conversionsValue":388.959299873,"conversions":16.500001,"costMicros":"327654345","impressions":"5727"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/17324490442","status":"ENABLED","advertisingChannelType":"SEARCH","name":"T2MD | Search | Roses 152 29/8 140 14/1 155 16/6 Port 150 16/6 AI Max 1/7 160 3/7 150 23/10","id":"17324490442"},"metrics":{"clicks":"166","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.0999,"conversionsValue":64.712266,"conversions":3,"costMicros":"120797622","impressions":"1619"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/10492045139","status":"ENABLED","advertisingChannelType":"SEARCH","name":"T2MD | DSA 160 150 5/12 140 7/4","id":"10492045139"},"metrics":{"clicks":"126","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.0999,"conversionsValue":194.11681104,"conversions":7.285755,"costMicros":"103624846","impressions":"1587"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/21610656469","status":"ENABLED","advertisingChannelType":"PERFORMANCE_MAX","name":"T2MD | P Max Shopping | Unprofitable 150 160 3/9 150 5/9 140 23/10","id":"21610656469"},"metrics":{"clicks":"89","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.622912674514098,"conversionsValue":118.33046792,"conversions":5.870694,"costMicros":"96941342","impressions":"13506"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/22122810626","status":"ENABLED","advertisingChannelType":"SHOPPING","name":"T2MD | Shopping | Low Traffic 150 13/1 140 7/4 150 18/5 160 3/9 150 5/9 140 23/10","id":"22122810626"},"metrics":{"clicks":"100","searchBudgetLostImpressionShare":0.5788034737857832,"searchImpressionShare":0.42087487938243806,"conversionsValue":110.981962233,"conversions":7.979778,"costMicros":"77140000","impressions":"14943"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/598474059","status":"ENABLED","advertisingChannelType":"SEARCH","name":"T2MD | Brand Inclusion  120  14/7 Ai Max 11/11","id":"598474059"},"metrics":{"clicks":"80","searchBudgetLostImpressionShare":0,"searchImpressionShare":0.8867924528301887,"conversionsValue":93.7914665,"conversions":4.5,"costMicros":"64897286","impressions":"264"}},{"campaign":{"resourceName":"customers/4941701449/campaigns/18441497267","status":"ENABLED","advertisingChannelType":"SEARCH","name":"T2MD | Search | Memorial Gift 150 20/5 140 7/4 Port 150  16/6 AI Max 28/7 144","id":"18441497267"},"metrics":{"clicks":"122","searchBudgetLostImpressionShare":0.0005074854097944684,"searchImpressionShare":0.0999,"conversionsValue":35.7341245,"conversions":1.5,"costMicros":"63670828","impressions":"1528"}}]}

# Real product data from Tree2mydoor (top 50 products by spend, 2025-12-08 to 2025-12-15)
product_data_raw = {"results":[{"metrics":{"clicks":"69","conversionsValue":116.096949,"conversions":7.5,"costMicros":"62380000","impressions":"4228"},"segments":{"date":"2025-12-10","productItemId":"01090","productTitle":"The Olive Tree Gift - 2L pot, 50cm Height - Suitable For Potted Or Planted Growth - Fragrant, White Blossoms Appear In Spring"}},{"metrics":{"clicks":"25","conversionsValue":55.7556,"conversions":3,"costMicros":"59340000","impressions":"1413"},"segments":{"date":"2025-12-10","productItemId":"00287","productTitle":"The Olive Tree Gift - Large (5L pot, 80cm height) - Suitable For Potted Or Planted Growth - Gift Wrapped"}},{"metrics":{"clicks":"45","conversionsValue":105.775216,"conversions":4,"costMicros":"53933873","impressions":"4951"},"segments":{"date":"2025-12-12","productItemId":"01090","productTitle":"The Olive Tree Gift - 2L pot, 50cm Height - Suitable For Potted Or Planted Growth - Fragrant, White Blossoms Appear In Spring"}},{"metrics":{"clicks":"57","conversionsValue":144.822064456,"conversions":7.636448,"costMicros":"48840000","impressions":"4316"},"segments":{"date":"2025-12-08","productItemId":"01090","productTitle":"The Olive Tree Gift - 2L pot, 50cm Height - Suitable For Potted Or Planted Growth - Fragrant, White Blossoms Appear In Spring"}},{"metrics":{"clicks":"24","conversionsValue":71.24545,"conversions":3,"costMicros":"45230000","impressions":"1835"},"segments":{"date":"2025-12-14","productItemId":"00287","productTitle":"The Olive Tree Gift - Large (5L pot, 80cm height) - Suitable For Potted Or Planted Growth - Gift Wrapped"}},{"metrics":{"clicks":"43","conversionsValue":166.587482,"conversions":9,"costMicros":"42980000","impressions":"4507"},"segments":{"date":"2025-12-14","productItemId":"01090","productTitle":"The Olive Tree Gift - 2L pot, 50cm Height - Suitable For Potted Or Planted Growth - Fragrant, White Blossoms Appear In Spring"}},{"metrics":{"clicks":"22","conversionsValue":0,"conversions":0,"costMicros":"38120000","impressions":"1498"},"segments":{"date":"2025-12-15","productItemId":"00287","productTitle":"The Olive Tree Gift - Large (5L pot, 80cm height) - Suitable For Potted Or Planted Growth - Gift Wrapped"}},{"metrics":{"clicks":"38","conversionsValue":0,"conversions":0,"costMicros":"36616180","impressions":"3920"},"segments":{"date":"2025-12-15","productItemId":"01090","productTitle":"The Olive Tree Gift - 2L pot, 50cm Height - Suitable For Potted Or Planted Growth - Fragrant, White Blossoms Appear In Spring"}},{"metrics":{"clicks":"24","conversionsValue":52.957001015,"conversions":1.95377,"costMicros":"35610000","impressions":"1457"},"segments":{"date":"2025-12-08","productItemId":"00287","productTitle":"The Olive Tree Gift - Large (5L pot, 80cm height) - Suitable For Potted Or Planted Growth - Gift Wrapped"}},{"metrics":{"clicks":"19","conversionsValue":77.3853,"conversions":2,"costMicros":"32820000","impressions":"1634"},"segments":{"date":"2025-12-12","productItemId":"00287","productTitle":"The Olive Tree Gift - Large (5L pot, 80cm height) - Suitable For Potted Or Planted Growth - Gift Wrapped"}},{"metrics":{"clicks":"20","conversionsValue":45.3203,"conversions":2,"costMicros":"32780000","impressions":"1740"},"segments":{"date":"2025-12-13","productItemId":"00287","productTitle":"The Olive Tree Gift - Large (5L pot, 80cm height) - Suitable For Potted Or Planted Growth - Gift Wrapped"}},{"metrics":{"clicks":"34","conversionsValue":22.66515,"conversions":1,"costMicros":"32020938","impressions":"4351"},"segments":{"date":"2025-12-13","productItemId":"01090","productTitle":"The Olive Tree Gift - 2L pot, 50cm Height - Suitable For Potted Or Planted Growth - Fragrant, White Blossoms Appear In Spring"}},{"metrics":{"clicks":"16","conversionsValue":96.4531,"conversions":3,"costMicros":"31208967","impressions":"1589"},"segments":{"date":"2025-12-14","productItemId":"00593","productTitle":"Lemon Tree Gift - Large 5L pot, 50-60cm High - Leaves All Year - With Ripening Citrus Fruits - Suitable For Pot Growing Indoors"}},{"metrics":{"clicks":"33","conversionsValue":29.40045,"conversions":2,"costMicros":"26622138","impressions":"3047"},"segments":{"date":"2025-12-09","productItemId":"01090","productTitle":"The Olive Tree Gift - 2L pot, 50cm Height - Suitable For Potted Or Planted Growth - Fragrant, White Blossoms Appear In Spring"}},{"metrics":{"clicks":"34","conversionsValue":0,"conversions":0,"costMicros":"25901208","impressions":"3049"},"segments":{"date":"2025-12-11","productItemId":"01090","productTitle":"The Olive Tree Gift - 2L pot, 50cm Height - Suitable For Potted Or Planted Growth - Fragrant, White Blossoms Appear In Spring"}},{"metrics":{"clicks":"34","conversionsValue":18.986733,"conversions":3,"costMicros":"25229332","impressions":"2542"},"segments":{"date":"2025-12-12","productItemId":"aprbg","productTitle":"At Peace Rose Bush Gift - The Perfect Memorial - Plant In Memory Of Someone Special - Gone but not forgotten"}},{"metrics":{"clicks":"14","conversionsValue":0,"conversions":0,"costMicros":"24748467","impressions":"1190"},"segments":{"date":"2025-12-10","productItemId":"00593","productTitle":"Lemon Tree Gift - Large 5L pot, 50-60cm High - Leaves All Year - With Ripening Citrus Fruits - Suitable For Pot Growing Indoors"}},{"metrics":{"clicks":"18","conversionsValue":25.92515,"conversions":1,"costMicros":"24650000","impressions":"1269"},"segments":{"date":"2025-12-11","productItemId":"00287","productTitle":"The Olive Tree Gift - Large (5L pot, 80cm height) - Suitable For Potted Or Planted Growth - Gift Wrapped"}},{"metrics":{"clicks":"20","conversionsValue":23.91015,"conversions":1,"costMicros":"24560000","impressions":"1266"},"segments":{"date":"2025-12-09","productItemId":"00287","productTitle":"The Olive Tree Gift - Large (5L pot, 80cm height) - Suitable For Potted Or Planted Growth - Gift Wrapped"}},{"metrics":{"clicks":"10","conversionsValue":0,"conversions":0,"costMicros":"21372783","impressions":"1432"},"segments":{"date":"2025-12-15","productItemId":"00593","productTitle":"Lemon Tree Gift - Large 5L pot, 50-60cm High - Leaves All Year - With Ripening Citrus Fruits - Suitable For Pot Growing Indoors"}}]}

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

print("="*80)
print("TREE2MYDOOR CAMPAIGN ANALYSIS WITH PRODUCT INSIGHTS")
print("="*80)
print()

# Transform data
campaign_data = transform_campaign_data(campaign_data_raw)
product_data = transform_product_data(product_data_raw)

print(f"✓ Loaded {len(campaign_data)} campaigns")
print(f"✓ Loaded {len(product_data)} product records")
print()

# Calculate totals
total_spend = sum(c['metrics']['cost_micros'] for c in campaign_data) / 1_000_000
total_revenue = sum(c['metrics']['conversions_value'] for c in campaign_data)
print(f"Campaign Totals: £{total_spend:.2f} spend, £{total_revenue:.2f} revenue")
print()

# Combine data
combined_data = campaign_data + product_data

# Analyze
analyzer = CampaignAnalyzer()
analysis = analyzer.analyze_campaigns(
    client_slug='tree2mydoor',
    campaign_data=combined_data,
    date_range={'start_date': '2025-12-08', 'end_date': '2025-12-15'}
)

# Display results
print("-"*80)
print("ANALYSIS RESULTS")
print("-"*80)
print()
print(f"Health Score: {analysis['health_score']}/100")
print()
print(analysis['summary'])
print()

# Product analysis
if analysis.get('product_analysis'):
    pa = analysis['product_analysis']
    print("-"*80)
    print("PRODUCT ANALYSIS")
    print("-"*80)
    print(f"Total Products: {pa.get('total_products', 0)}")
    print(f"Products with Issues: {pa.get('products_with_issues', 0)}")
    print(f"Disapproved Products: {pa.get('disapproved_products', 0)}")
    print()

    if pa.get('product_issues'):
        print("Product-Level Issues:")
        for issue in pa['product_issues'][:5]:
            print(f"  [{issue['severity']}] {issue['product_title']} ({issue['product_id']})")
            print(f"      {issue['description']}")
            print(f"      → {issue['recommendation']}")
            print()

# Recommendations
if analysis.get('recommendations'):
    print("-"*80)
    print("TOP RECOMMENDATIONS")
    print("-"*80)
    for i, rec in enumerate(analysis['recommendations'][:5], 1):
        print(f"\n{i}. [{rec['priority']}] {rec['title']}")
        print(f"   Affected: {rec['affected_campaigns']} campaign(s)")
        impact = rec['impact']
        print(f"   Impact: £{impact['total_spend']:.0f} spend, {impact['avg_roas']:.2f}x ROAS")
        if rec.get('kb_articles'):
            print(f"   KB Articles: {len(rec['kb_articles'])} found")

# Save report
output_path = Path(__file__).parent / 'reports' / f"tree2mydoor_with_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
output_path.parent.mkdir(exist_ok=True)
output_path.write_text(json.dumps(analysis, indent=2))

print()
print("="*80)
print(f"Full report saved: {output_path}")
print("="*80)
