#!/usr/bin/env python3
"""
Analyse Asset Performance from API Export - Customer-Specific Metrics

This script analyzes PMAX asset performance using customer-specific benchmarks.
All thresholds are calculated from the customer's own campaign data.
"""

import json
import statistics
from collections import defaultdict

def calculate_customer_benchmarks(assets):
    """Calculate customer-specific performance benchmarks"""

    # Filter to assets with sufficient data for benchmark calculation
    valid_for_benchmark = [
        a for a in assets
        if int(a['metrics']['impressions']) >= 100  # Minimum for benchmark
    ]

    if not valid_for_benchmark:
        print("❌ Not enough asset data to calculate benchmarks")
        return None

    # Calculate campaign-wide averages
    ctrs = [float(a['metrics']['ctr']) for a in valid_for_benchmark]

    # Conversion rate = conversions / clicks (only if clicks > 0)
    conv_rates = []
    cpas = []

    for a in valid_for_benchmark:
        clicks = int(a['metrics']['clicks'])
        conversions = float(a['metrics']['conversions'])
        cost_micros = int(a['metrics']['costMicros'])
        cost = cost_micros / 1_000_000

        if clicks > 0:
            conv_rate = (conversions / clicks) * 100
            conv_rates.append(conv_rate)

        if conversions > 0:
            cpa = cost / conversions
            cpas.append(cpa)

    benchmarks = {
        'avg_ctr': statistics.mean(ctrs) if ctrs else 0,
        'median_ctr': statistics.median(ctrs) if ctrs else 0,
        'avg_conv_rate': statistics.mean(conv_rates) if conv_rates else 0,
        'median_conv_rate': statistics.median(conv_rates) if conv_rates else 0,
        'avg_cpa': statistics.mean(cpas) if cpas else 0,
        'median_cpa': statistics.median(cpas) if cpas else 0,
        'total_assets': len(assets),
        'assets_with_conversions': len([a for a in valid_for_benchmark if float(a['metrics']['conversions']) > 0]),
        'assets_in_benchmark': len(valid_for_benchmark)
    }

    return benchmarks


def classify_asset(asset, benchmarks):
    """
    Classify asset using CUSTOMER-SPECIFIC benchmarks

    Returns: (classification, priority, reasons)
    """

    impressions = int(asset['metrics']['impressions'])
    clicks = int(asset['metrics']['clicks'])
    ctr = float(asset['metrics']['ctr']) * 100  # Convert to percentage
    conversions = float(asset['metrics']['conversions'])
    cost_micros = int(asset['metrics']['costMicros'])
    cost = cost_micros / 1_000_000

    # Calculate asset-specific metrics
    conv_rate = (conversions / clicks * 100) if clicks > 0 else 0
    cpa = (cost / conversions) if conversions > 0 else 0

    reasons = []

    # 1. INSUFFICIENT DATA
    if impressions < 500:
        return 'TOO_EARLY', 'N/A', ['Insufficient impressions (<500) for reliable judgment']

    # 2. WINNERS (KEEP) - Any strong metric keeps it
    if ctr > benchmarks['avg_ctr'] * 1.2:
        return 'KEEP', 'WINNER', [f"Strong CTR ({ctr:.2f}% vs avg {benchmarks['avg_ctr']:.2f}%)"]

    if clicks >= 20 and conv_rate > benchmarks['avg_conv_rate'] * 1.2:
        return 'KEEP', 'WINNER', [f"Strong conversion rate ({conv_rate:.2f}% vs avg {benchmarks['avg_conv_rate']:.2f}%)"]

    if conversions > 0 and cpa < benchmarks['avg_cpa'] * 0.8:
        return 'KEEP', 'WINNER', [f"Low CPA (£{cpa:.2f} vs avg £{benchmarks['avg_cpa']:.2f})"]

    # 3. HIGH PRIORITY REPLACEMENTS

    # Terrible CTR with high waste
    if impressions > 5000 and clicks > 50 and ctr < benchmarks['avg_ctr'] * 0.5:
        reasons.append(f"Terrible CTR ({ctr:.2f}% vs avg {benchmarks['avg_ctr']:.2f}%) - only {(ctr/benchmarks['avg_ctr']*100):.0f}% of average")
        reasons.append(f"High impression waste ({impressions:,} impressions)")
        return 'REPLACE', 'HIGH', reasons

    # Zero conversions despite plenty of clicks
    if clicks > 30 and conversions == 0:
        reasons.append(f"Zero conversions despite {clicks} clicks")
        reasons.append(f"Wasted £{cost:.2f} with no return")
        return 'REPLACE', 'HIGH', reasons

    # Click trap: Good CTR but terrible conversion rate
    if clicks > 50 and ctr > benchmarks['avg_ctr'] * 1.1:
        if conv_rate < benchmarks['avg_conv_rate'] * 0.5:
            reasons.append(f"Click trap: Good CTR ({ctr:.2f}%) but terrible conv rate ({conv_rate:.2f}% vs avg {benchmarks['avg_conv_rate']:.2f}%)")
            reasons.append(f"Misleading message - attracts clicks but doesn't convert")
            return 'REPLACE', 'MEDIUM', reasons

    # 4. MEDIUM PRIORITY REPLACEMENTS

    # Moderate underperformance with sufficient data
    if impressions > 2000 and clicks > 20:
        if ctr < benchmarks['avg_ctr'] * 0.7:
            reasons.append(f"Low CTR ({ctr:.2f}% vs avg {benchmarks['avg_ctr']:.2f}%)")

        if conv_rate < benchmarks['avg_conv_rate'] * 0.7 and benchmarks['avg_conv_rate'] > 0:
            reasons.append(f"Low conversion rate ({conv_rate:.2f}% vs avg {benchmarks['avg_conv_rate']:.2f}%)")

        if reasons:
            reasons.append(f"Sufficient data to be confident ({impressions:,} impressions, {clicks} clicks)")
            return 'REPLACE', 'MEDIUM', reasons

    # 5. LOW PRIORITY REPLACEMENTS

    # Slight underperformance with very high impressions
    if impressions > 10000 and clicks > 50:
        if ctr < benchmarks['avg_ctr'] * 0.85 or (conv_rate < benchmarks['avg_conv_rate'] * 0.85 and benchmarks['avg_conv_rate'] > 0):
            reasons.append(f"Slightly below average performance at scale")
            reasons.append(f"CTR: {ctr:.2f}% (avg: {benchmarks['avg_ctr']:.2f}%)")
            if conv_rate > 0:
                reasons.append(f"Conv rate: {conv_rate:.2f}% (avg: {benchmarks['avg_conv_rate']:.2f}%)")
            return 'REPLACE', 'LOW', reasons

    # 6. MONITOR (Not bad enough to replace yet)
    if clicks < 20 and ctr > benchmarks['avg_ctr'] * 0.8:
        return 'MONITOR', 'POTENTIAL', [f"Decent CTR ({ctr:.2f}%), needs more clicks for conv rate judgment"]

    return 'MONITOR', 'NEUTRAL', ['Performance within acceptable range']


def analyse_bright_minds_api(api_results):
    """Analyse Bright Minds API export with customer-specific benchmarks"""

    print("=" * 80)
    print("BRIGHT MINDS - PMAX ASSET ANALYSIS (API EXPORT)")
    print("=" * 80)
    print()

    # Calculate customer-specific benchmarks
    print("📊 Calculating Bright Minds campaign benchmarks...")
    benchmarks = calculate_customer_benchmarks(api_results)

    if not benchmarks:
        return

    print(f"✅ Benchmarks calculated from {benchmarks['assets_in_benchmark']} assets:")
    print(f"   Average CTR: {benchmarks['avg_ctr']:.2f}%")
    print(f"   Average Conv Rate: {benchmarks['avg_conv_rate']:.2f}%")
    print(f"   Average CPA: £{benchmarks['avg_cpa']:.2f}")
    print(f"   Assets with conversions: {benchmarks['assets_with_conversions']} / {benchmarks['total_assets']}")
    print()

    # Classify all assets
    print("🔍 Classifying assets using Bright Minds benchmarks...")
    print()

    classifications = {
        'KEEP': [],
        'REPLACE': {'HIGH': [], 'MEDIUM': [], 'LOW': []},
        'MONITOR': [],
        'TOO_EARLY': []
    }

    for asset in api_results:
        classification, priority, reasons = classify_asset(asset, benchmarks)

        asset_info = {
            'text': asset['asset']['textAsset']['text'],
            'type': asset['assetGroupAsset']['fieldType'],
            'asset_group': asset['assetGroup']['name'],
            'impressions': int(asset['metrics']['impressions']),
            'clicks': int(asset['metrics']['clicks']),
            'ctr': float(asset['metrics']['ctr']) * 100,
            'conversions': float(asset['metrics']['conversions']),
            'priority': priority,
            'reasons': reasons
        }

        if classification == 'REPLACE':
            classifications['REPLACE'][priority].append(asset_info)
        elif classification == 'KEEP':
            classifications['KEEP'].append(asset_info)
        elif classification == 'MONITOR':
            classifications['MONITOR'].append(asset_info)
        else:
            classifications['TOO_EARLY'].append(asset_info)

    # Summary
    total_replace = sum(len(classifications['REPLACE'][p]) for p in ['HIGH', 'MEDIUM', 'LOW'])

    print("=" * 80)
    print("CLASSIFICATION RESULTS")
    print("=" * 80)
    print()
    print(f"✅ KEEP (Winners): {len(classifications['KEEP'])}")
    print(f"🔴 REPLACE: {total_replace}")
    print(f"   - HIGH priority: {len(classifications['REPLACE']['HIGH'])}")
    print(f"   - MEDIUM priority: {len(classifications['REPLACE']['MEDIUM'])}")
    print(f"   - LOW priority: {len(classifications['REPLACE']['LOW'])}")
    print(f"👁️  MONITOR: {len(classifications['MONITOR'])}")
    print(f"⏳ TOO EARLY: {len(classifications['TOO_EARLY'])}")
    print()

    # Show top replacements
    if classifications['REPLACE']['HIGH']:
        print("=" * 80)
        print("TOP 5 HIGH PRIORITY REPLACEMENTS")
        print("=" * 80)
        print()

        high_priority = sorted(
            classifications['REPLACE']['HIGH'],
            key=lambda x: x['impressions'],
            reverse=True
        )[:5]

        for i, asset in enumerate(high_priority, 1):
            print(f"{i}. [{asset['type']}] {asset['text'][:70]}...")
            print(f"   Asset Group: {asset['asset_group']}")
            print(f"   Impressions: {asset['impressions']:,} | Clicks: {asset['clicks']} | CTR: {asset['ctr']:.2f}%")
            print(f"   Conversions: {asset['conversions']:.2f}")
            print(f"   Reasons:")
            for reason in asset['reasons']:
                print(f"     - {reason}")
            print()

    # Show winners
    if classifications['KEEP']:
        print("=" * 80)
        print("TOP 5 WINNERS (Keep These!)")
        print("=" * 80)
        print()

        winners = sorted(
            classifications['KEEP'],
            key=lambda x: x['impressions'],
            reverse=True
        )[:5]

        for i, asset in enumerate(winners, 1):
            print(f"{i}. [{asset['type']}] {asset['text'][:70]}...")
            print(f"   Asset Group: {asset['asset_group']}")
            print(f"   Impressions: {asset['impressions']:,} | Clicks: {asset['clicks']} | CTR: {asset['ctr']:.2f}%")
            print(f"   Conversions: {asset['conversions']:.2f}")
            print(f"   Why keep: {asset['reasons'][0]}")
            print()

    return classifications, benchmarks


if __name__ == "__main__":
    print("This script requires Bright Minds API results to be provided")
    print("Use with the 97 text assets retrieved from the Google Ads API")
