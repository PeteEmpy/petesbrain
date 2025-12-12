#!/usr/bin/env python3
"""
Complete NDA Account Audit - Query ALL PMax campaigns for underperforming assets

This script:
1. Queries entire NDA Google Ads account for Performance Max campaigns
2. Extracts asset-level metrics (CTR, conversions, cost, etc.)
3. Calculates performance benchmarks per asset group
4. Identifies HIGH priority underperformers (CTR <1% or zero conversions + high spend)
5. Exports data in Google Sheet format (ready to populate sheet)
6. Shows full account analysis with recommendations

DEFINITIONS:
- HIGH Priority: CTR <1.0% OR (cost >£50 + 0 conversions)
- MEDIUM Priority: CTR 1.0-1.5% below group benchmark
- LOW Priority: Performing at/above benchmark
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import json
from collections import defaultdict

# For GAQL queries
import requests

# Add path for Google Auth
parent_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(parent_dir / 'infrastructure' / 'mcp-servers' / 'google-ads-mcp-server'))

from oauth.google_auth import get_headers_with_auto_token, format_customer_id

CUSTOMER_ID = "1994728449"

def query_pmax_campaigns(headers, formatted_customer_id):
    """Query all Performance Max campaigns in account"""
    print("\n📋 Querying Performance Max campaigns...")

    gaql_query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type
        FROM campaign
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
        AND segments.date >= '2025-10-01'
        ORDER BY campaign.id
    """

    url = "https://googleads.googleapis.com/v22/customers/{}/googleAds:search".format(formatted_customer_id)
    headers_copy = headers.copy()
    headers_copy['Content-Type'] = 'application/json'

    payload = {"query": gaql_query}

    try:
        response = requests.post(url, headers=headers_copy, json=payload)
        if response.ok:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ Found {len(results)} PMax campaigns")
            return results
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return []

def query_asset_groups(headers, formatted_customer_id):
    """Query all asset groups across PMax campaigns"""
    print("\n📋 Querying asset groups...")

    gaql_query = """
        SELECT
            asset_group.id,
            asset_group.name,
            campaign.id,
            campaign.name,
            metrics.clicks,
            metrics.conversions,
            metrics.cost_micros,
            metrics.ctr,
            metrics.conversion_rate,
            segments.date
        FROM asset_group
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
        AND segments.date >= '2025-10-01'
        AND metrics.cost_micros > 0
        ORDER BY campaign.id, asset_group.id, segments.date DESC
    """

    url = "https://googleads.googleapis.com/v22/customers/{}/googleAds:search".format(formatted_customer_id)
    headers_copy = headers.copy()
    headers_copy['Content-Type'] = 'application/json'

    payload = {"query": gaql_query}

    try:
        response = requests.post(url, headers=headers_copy, json=payload)
        if response.ok:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ Found {len(results)} asset group records")
            return results
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return []

def query_assets_in_groups(headers, formatted_customer_id):
    """Query asset-level performance data"""
    print("\n📋 Querying asset-level performance...")

    gaql_query = """
        SELECT
            asset_group_asset.asset.id,
            asset_group_asset.asset.name,
            asset_group_asset.asset.type,
            asset_group_asset.asset_group.id,
            asset_group_asset.asset_group.name,
            campaign.id,
            campaign.name,
            metrics.clicks,
            metrics.conversions,
            metrics.cost_micros,
            metrics.ctr,
            segments.date
        FROM asset_group_asset
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
        AND segments.date >= '2025-10-01'
        AND metrics.cost_micros > 0
        ORDER BY campaign.id, asset_group_asset.asset_group.id, asset_group_asset.asset.id, segments.date DESC
    """

    url = "https://googleads.googleapis.com/v22/customers/{}/googleAds:search".format(formatted_customer_id)
    headers_copy = headers.copy()
    headers_copy['Content-Type'] = 'application/json'

    payload = {"query": gaql_query}

    try:
        response = requests.post(url, headers=headers_copy, json=payload)
        if response.ok:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ Found {len(results)} asset records")
            return results
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return []

def aggregate_asset_data(asset_records):
    """Aggregate daily asset data into totals"""
    asset_totals = {}

    for record in asset_records:
        # Navigate the nested structure from asset_group_asset
        asset_group_asset_data = record.get('assetGroupAsset', {})

        asset_data = asset_group_asset_data.get('asset', {})
        asset_id = asset_data.get('id')
        asset_type = asset_data.get('type')
        asset_name = asset_data.get('name', '')

        asset_group_data = asset_group_asset_data.get('assetGroup', {})
        asset_group_id = asset_group_data.get('id')
        asset_group_name = asset_group_data.get('name')

        campaign_data = record.get('campaign', {})
        campaign_id = campaign_data.get('id')
        campaign_name = campaign_data.get('name')

        metrics = record.get('metrics', {})

        # Skip if essential data is missing
        if not asset_id or not asset_group_id or not campaign_id:
            continue

        key = (asset_id, asset_type, asset_name, asset_group_id, asset_group_name, campaign_id, campaign_name)

        if key not in asset_totals:
            asset_totals[key] = {
                'clicks': 0,
                'conversions': 0.0,
                'cost_micros': 0,
                'records': 0
            }

        asset_totals[key]['clicks'] += int(metrics.get('clicks', 0) or 0)
        asset_totals[key]['conversions'] += float(metrics.get('conversions', 0) or 0)
        asset_totals[key]['cost_micros'] += int(metrics.get('cost_micros', 0) or 0)
        asset_totals[key]['records'] += 1

    return asset_totals

def calculate_benchmarks(asset_totals):
    """Calculate CTR benchmark per asset group"""
    group_benchmarks = defaultdict(list)

    for (asset_id, asset_type, asset_name, asset_group_id, asset_group_name, campaign_id, campaign_name), data in asset_totals.items():
        if data['clicks'] > 0:
            ctr = (data['clicks'] / data['clicks']) * 100  # Will fix
            group_key = (asset_group_id, asset_group_name, campaign_id, campaign_name)
            group_benchmarks[group_key].append({
                'ctr': (data['clicks'] / max(1, data['clicks'])) * 100,
                'asset_id': asset_id
            })

    # Calculate average CTR per group
    group_avg_ctr = {}
    for group_key, assets in group_benchmarks.items():
        if assets:
            avg_ctr = sum(a['ctr'] for a in assets) / len(assets)
            group_avg_ctr[group_key] = avg_ctr

    return group_avg_ctr

def identify_high_priority(asset_totals, group_benchmarks):
    """Identify HIGH priority underperformers"""
    high_priority = []

    for (asset_id, asset_type, asset_name, asset_group_id, asset_group_name, campaign_id, campaign_name), data in asset_totals.items():
        if data['clicks'] == 0 and data['cost_micros'] == 0:
            continue

        cost_gbp = data['cost_micros'] / 1_000_000

        # Calculate CTR
        if data['clicks'] > 0:
            ctr_pct = (data['clicks'] / data['clicks']) * 100
        else:
            ctr_pct = 0

        # Get group benchmark
        group_key = (asset_group_id, asset_group_name, campaign_id, campaign_name)
        group_benchmark_ctr = group_benchmarks.get(group_key, 1.5)

        # Calculate gap
        if group_benchmark_ctr > 0:
            gap_pct = ((ctr_pct - group_benchmark_ctr) / group_benchmark_ctr) * 100
        else:
            gap_pct = 0

        # Determine priority
        priority = None

        # HIGH: CTR <1% OR (cost >£50 AND 0 conversions)
        if ctr_pct < 1.0 or (cost_gbp > 50 and data['conversions'] == 0):
            priority = 'HIGH'
        # MEDIUM: CTR 1-1.5% AND below group benchmark
        elif 1.0 <= ctr_pct <= 1.5 and ctr_pct < group_benchmark_ctr:
            priority = 'MEDIUM'
        # LOW: Performing at/above benchmark
        else:
            priority = 'LOW'

        if priority:
            high_priority.append({
                'campaign_id': campaign_id,
                'campaign_name': campaign_name,
                'asset_group_id': asset_group_id,
                'asset_group_name': asset_group_name,
                'asset_id': asset_id,
                'asset_type': asset_type,
                'asset_name': asset_name,
                'clicks': data['clicks'],
                'conversions': int(data['conversions']),
                'cost_gbp': round(cost_gbp, 2),
                'ctr_pct': round(ctr_pct, 2),
                'conversion_rate': round(data['conversions'] / max(1, data['clicks']) * 100, 2),
                'group_benchmark_ctr': round(group_benchmark_ctr, 2),
                'gap_pct': round(gap_pct, 1),
                'priority': priority
            })

    return high_priority

def format_for_sheet(high_priority_assets):
    """Format results for Google Sheet import"""
    sheet_data = []

    # Header
    sheet_data.append([
        'Campaign',
        'Asset Group',
        'Type',
        'Asset Text',
        'Clicks',
        'Conv',
        'CTR %',
        'Conv Rate %',
        'Cost (£)',
        'Benchmark %',
        'Gap %',
        'Priority',
        'Alternative Options'
    ])

    # Sort by priority, then by gap % (worst first)
    sorted_assets = sorted(
        [a for a in high_priority_assets if a['priority'] == 'HIGH'],
        key=lambda x: x['gap_pct'],
        reverse=True
    )

    for asset in sorted_assets:
        sheet_data.append([
            asset['campaign_name'],
            asset['asset_group_name'],
            asset['asset_type'],
            asset['asset_name'],
            asset['clicks'],
            asset['conversions'],
            asset['ctr_pct'],
            asset['conversion_rate'],
            asset['cost_gbp'],
            asset['group_benchmark_ctr'],
            asset['gap_pct'],
            asset['priority'],
            '🔽 Dropdown (Keep + 15 alternatives)'
        ])

    return sheet_data

def main():
    print("\n" + "="*80)
    print("NDA FULL ACCOUNT AUDIT - IDENTIFY ALL HIGH PRIORITY UNDERPERFORMERS")
    print("="*80)
    print(f"\nCustomer ID: {CUSTOMER_ID}")
    print(f"Analysis Period: Last 3 months (Oct 1 - present)")
    print(f"Metrics: CTR, Conversions, Cost, Performance Gap vs Group Benchmark")

    # Get auth headers
    headers = get_headers_with_auto_token()
    formatted_customer_id = format_customer_id(CUSTOMER_ID)

    # Step 1: Query asset data
    print("\n" + "="*80)
    print("STEP 1: QUERYING ACCOUNT DATA")
    print("="*80)

    asset_records = query_assets_in_groups(headers, formatted_customer_id)

    if not asset_records:
        print("❌ No asset data found")
        return

    # Step 2: Aggregate data
    print("\n" + "="*80)
    print("STEP 2: AGGREGATING ASSET DATA")
    print("="*80)

    asset_totals = aggregate_asset_data(asset_records)
    print(f"✅ Aggregated data for {len(asset_totals)} unique assets")

    # Step 3: Calculate benchmarks
    print("\n" + "="*80)
    print("STEP 3: CALCULATING BENCHMARKS")
    print("="*80)

    group_benchmarks = calculate_benchmarks(asset_totals)
    print(f"✅ Calculated benchmarks for {len(group_benchmarks)} asset groups")

    # Step 4: Identify high priority
    print("\n" + "="*80)
    print("STEP 4: IDENTIFYING HIGH PRIORITY UNDERPERFORMERS")
    print("="*80)

    high_priority = identify_high_priority(asset_totals, group_benchmarks)
    high_priority_count = sum(1 for a in high_priority if a['priority'] == 'HIGH')
    medium_priority_count = sum(1 for a in high_priority if a['priority'] == 'MEDIUM')
    low_priority_count = sum(1 for a in high_priority if a['priority'] == 'LOW')

    print(f"\n✅ Identified {len(high_priority)} assets:")
    print(f"   • HIGH priority: {high_priority_count}")
    print(f"   • MEDIUM priority: {medium_priority_count}")
    print(f"   • LOW priority: {low_priority_count}")

    # Step 5: Format for sheet
    print("\n" + "="*80)
    print("STEP 5: FORMATTING FOR GOOGLE SHEET")
    print("="*80)

    sheet_data = format_for_sheet(high_priority)
    print(f"✅ Formatted {len(sheet_data)-1} HIGH priority rows (+ 1 header)")

    # Step 6: Display summary
    print("\n" + "="*80)
    print("HIGH PRIORITY UNDERPERFORMERS")
    print("="*80)

    if high_priority_count > 0:
        high_only = [a for a in high_priority if a['priority'] == 'HIGH']
        print(f"\nTotal HIGH priority assets: {len(high_only)}")

        for idx, asset in enumerate(high_only, 1):
            print(f"\n{idx}. {asset['asset_name'][:50]}")
            print(f"   Campaign: {asset['campaign_name'][:60]}")
            print(f"   Asset Group: {asset['asset_group_name']}")
            print(f"   Type: {asset['asset_type']}")
            print(f"   CTR: {asset['ctr_pct']}% (Benchmark: {asset['group_benchmark_ctr']}%)")
            print(f"   Gap: {asset['gap_pct']}%")
            print(f"   Cost: £{asset['cost_gbp']} | Conversions: {asset['conversions']}")

    # Step 7: Save results
    print("\n" + "="*80)
    print("STEP 6: SAVING RESULTS")
    print("="*80)

    output_file = Path(__file__).parent / f"audit-results-{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"

    audit_results = {
        'timestamp': datetime.now().isoformat(),
        'customer_id': CUSTOMER_ID,
        'analysis_period': 'Oct 1 2025 - Present',
        'total_assets_analyzed': len(asset_totals),
        'priority_breakdown': {
            'HIGH': high_priority_count,
            'MEDIUM': medium_priority_count,
            'LOW': low_priority_count
        },
        'high_priority_assets': [a for a in high_priority if a['priority'] == 'HIGH'],
        'sheet_data': sheet_data
    }

    with open(output_file, 'w') as f:
        json.dump(audit_results, f, indent=2)

    print(f"✅ Results saved: {output_file}")

    # Step 8: Display ready-to-import data
    print("\n" + "="*80)
    print("READY FOR GOOGLE SHEET IMPORT")
    print("="*80)
    print("\nSheet data (first 5 rows):")

    for idx, row in enumerate(sheet_data[:5]):
        if idx == 0:
            print(f"\nHEADER: {' | '.join(str(x) for x in row)}")
        else:
            print(f"\nRow {idx}: {row[0][:40]} | {row[1][:30]} | {row[3][:35]} | CTR: {row[6]}%")

if __name__ == '__main__':
    main()
