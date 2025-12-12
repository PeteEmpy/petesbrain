#!/usr/bin/env python3
"""
National Design Academy PMax Asset Analysis
- Extract asset performance metrics from Google Ads
- Analyse CTR% and conversion rate% within asset groups
- Identify underperformers
- Assign priority levels (HIGH/MEDIUM/LOW)
- Generate alternatives using text generator
"""

import json
import statistics
from collections import defaultdict
from datetime import datetime

# Asset performance data (from Google Ads API query, Nov 1 - Dec 11, 2025)
raw_data = [
    {"campaign": "NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4", "asset_group": "Interior Design Diploma", "asset_id": "6501874539", "text": "Study Interior Design", "field_type": "HEADLINE", "ctr": 0.003951612903225807, "clicks": 196, "conversions": 0, "impressions": 49600, "cost_micros": 18340302},
    {"campaign": "NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4", "asset_group": "Interior Design Diploma", "asset_id": "6501874548", "text": "National Design Academy", "field_type": "HEADLINE", "ctr": 0.018867924528301886, "clicks": 6, "conversions": 0, "impressions": 318, "cost_micros": 1829176},
    {"campaign": "NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4", "asset_group": "Interior Design Diploma", "asset_id": "6542848540", "text": "Interior Design Diploma", "field_type": "HEADLINE", "ctr": 0.004846867097499297, "clicks": 69, "conversions": 0, "impressions": 14236, "cost_micros": 6264357},
    {"campaign": "NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4", "asset_group": "Interior Design Diploma", "asset_id": "6542848621", "text": "Become an Interior Designer", "field_type": "HEADLINE", "ctr": 0.02197802197802198, "clicks": 10, "conversions": 0, "impressions": 455, "cost_micros": 2146354},
    {"campaign": "NDA | P Max Reboot | Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4", "asset_group": "Interior Design Diploma", "asset_id": "8680183789", "text": "Interior Design Courses", "field_type": "HEADLINE", "ctr": 0.0038134350249339984, "clicks": 51, "conversions": 0, "impressions": 13636, "cost_micros": 8563952},
    {"campaign": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "asset_group": "Interior Design Diploma", "asset_id": "6501874539", "text": "Study Interior Design", "field_type": "HEADLINE", "ctr": 0.03333998802156119, "clicks": 334, "conversions": 6, "impressions": 10018, "cost_micros": 164458861},
    {"campaign": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "asset_group": "Interior Design Diploma", "asset_id": "6501874548", "text": "National Design Academy", "field_type": "HEADLINE", "ctr": 0.058058638396554584, "clicks": 701, "conversions": 7, "impressions": 12074, "cost_micros": 393986538},
    {"campaign": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "asset_group": "Interior Design Diploma", "asset_id": "89763931644", "text": "No Qualifications Required", "field_type": "HEADLINE", "ctr": 0.02653527062025372, "clicks": 1209, "conversions": 8, "impressions": 45562, "cost_micros": 432325160},
    {"campaign": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "asset_group": "Interior Design Diploma", "asset_id": "182887527341", "text": "Worlds Leading Provider of Accredited Interior Design Courses. Join 35,000+ Graduates NOW", "field_type": "DESCRIPTION", "ctr": 0.053589006575579794, "clicks": 1361, "conversions": 10, "impressions": 25397, "cost_micros": 572154181},
    {"campaign": "NDA | P Max Reboot | Interior Design Diploma - ROTW 200 13/1 No target 28/5", "asset_group": "Remarketing", "asset_id": "6501874539", "text": "Study Interior Design", "field_type": "HEADLINE", "ctr": 0.010194174757281554, "clicks": 1680, "conversions": 2.980736, "impressions": 164800, "cost_micros": 49940720},
]

def analyse_assets():
    """Analyse assets by asset group and identify underperformers"""

    # Group by asset group
    asset_groups = defaultdict(list)
    for row in raw_data:
        asset_groups[row['asset_group']].append(row)

    analysis = []

    for group_name, assets in asset_groups.items():
        print(f"\n=== {group_name} ===")

        # Calculate metrics for each asset
        group_analysis = []
        for asset in assets:
            ctr_percent = asset['ctr'] * 100  # Convert to percentage

            # Calculate conversion rate %
            if asset['clicks'] > 0:
                conv_rate = (asset['conversions'] / asset['clicks']) * 100
            else:
                conv_rate = 0

            group_analysis.append({
                'asset_id': asset['asset_id'],
                'text': asset['text'],
                'field_type': asset['field_type'],
                'campaign': asset['campaign'],
                'ctr_percent': round(ctr_percent, 2),
                'conv_rate_percent': round(conv_rate, 2),
                'clicks': asset['clicks'],
                'conversions': asset['conversions'],
                'impressions': asset['impressions'],
                'cost_gbp': round(asset['cost_micros'] / 1000000, 2)
            })

        # Calculate group benchmarks
        group_ctrs = [a['ctr_percent'] for a in group_analysis if a['clicks'] > 5]  # Only assets with meaningful data
        group_convs = [a['conv_rate_percent'] for a in group_analysis if a['clicks'] > 5]

        if group_ctrs:
            avg_ctr = statistics.mean(group_ctrs)
            median_ctr = statistics.median(group_ctrs)
        else:
            avg_ctr = median_ctr = 0

        if group_convs:
            avg_conv = statistics.mean(group_convs)
        else:
            avg_conv = 0

        print(f"  Benchmark CTR%: {round(avg_ctr, 2)}% | Median: {round(median_ctr, 2)}%")
        print(f"  Benchmark Conv Rate%: {round(avg_conv, 2)}%")

        # Assign priority based on performance
        for asset in group_analysis:
            # Priority logic: compare to group benchmark
            ctr_gap = ((avg_ctr - asset['ctr_percent']) / avg_ctr * 100) if avg_ctr > 0 else 0

            # HIGH priority: >30% below benchmark and has some spend
            # MEDIUM priority: 15-30% below benchmark
            # LOW priority: better than or within 15% of benchmark

            if ctr_gap > 30 and asset['cost_gbp'] > 5:
                priority = 'HIGH'
            elif ctr_gap > 15 and asset['cost_gbp'] > 2:
                priority = 'MEDIUM'
            else:
                priority = 'LOW'

            asset['priority'] = priority
            asset['ctr_gap_percent'] = round(ctr_gap, 1)
            asset['group_benchmark_ctr'] = round(avg_ctr, 2)
            asset['group_name'] = group_name

            if priority in ['HIGH', 'MEDIUM']:
                print(f"  [{priority}] {asset['text'][:40]}... CTR: {asset['ctr_percent']}% (Benchmark: {asset['group_benchmark_ctr']}%, Gap: {asset['ctr_gap_percent']}%)")

            analysis.append(asset)

    return analysis

if __name__ == '__main__':
    results = analyse_assets()

    # Save to JSON for review
    with open('/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/asset-analysis-results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n\n✅ Analysis complete. {len(results)} assets analysed")
    print(f"   HIGH priority: {sum(1 for r in results if r['priority'] == 'HIGH')}")
    print(f"   MEDIUM priority: {sum(1 for r in results if r['priority'] == 'MEDIUM')}")
    print(f"   LOW priority: {sum(1 for r in results if r['priority'] == 'LOW')}")
