#!/usr/bin/env python3
"""
Deep diagnostic analysis for P-Max H&S Unbeast campaign Search impression share drop
Investigates: Search terms, placements, budget vs rank loss, asset performance, quality signals
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server'))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / '.env')
    load_dotenv(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env')
    load_dotenv(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env 2')
except ImportError:
    env_files = [
        PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env',
        PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env 2',
        PROJECT_ROOT / '.env'
    ]
    for env_file in env_files:
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            break

try:
    from oauth.google_auth import execute_gaql
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️  Google Ads MCP not available")

CUSTOMER_ID = "7972994730"
MANAGER_ID = "2569949686"
CAMPAIGN_ID = "20276730131"  # Main P Max (Furniture H&S/Zombies)

def format_micros(micros):
    return micros / 1_000_000

def query_search_terms(customer_id: str, campaign_id: str, start_date: str, end_date: str):
    """Query search terms that triggered the campaign"""
    query = f"""
    SELECT
      campaign.id,
      segments.search_term,
      segments.date,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value,
      metrics.ctr,
      metrics.average_cpc,
      metrics.search_impression_share,
      metrics.search_rank_lost_impression_share,
      metrics.search_budget_lost_impression_share
    FROM search_term_view
    WHERE campaign.id = {campaign_id}
      AND segments.date BETWEEN '{start_date}' AND '{end_date}'
      AND metrics.impressions > 0
    ORDER BY metrics.cost_micros DESC
    LIMIT 100
    """
    
    if not MCP_AVAILABLE:
        return []
    
    try:
        result = execute_gaql(customer_id, query, manager_id=MANAGER_ID)
        return result.get('results', [])
    except Exception as e:
        print(f"❌ Error querying search terms: {e}")
        return []

def query_placements(customer_id: str, campaign_id: str, start_date: str, end_date: str):
    """Query placement performance (where ads are showing)"""
    query = f"""
    SELECT
      campaign.id,
      group_placement_view.placement,
      group_placement_view.placement_type,
      segments.date,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value,
      metrics.ctr,
      metrics.average_cpc
    FROM group_placement_view
    WHERE campaign.id = {campaign_id}
      AND segments.date BETWEEN '{start_date}' AND '{end_date}'
      AND metrics.impressions > 0
    ORDER BY metrics.cost_micros DESC
    LIMIT 50
    """
    
    if not MCP_AVAILABLE:
        return []
    
    try:
        result = execute_gaql(customer_id, query, manager_id=MANAGER_ID)
        return result.get('results', [])
    except Exception as e:
        print(f"❌ Error querying placements: {e}")
        return []

def query_device_performance(customer_id: str, campaign_id: str, start_date: str, end_date: str):
    """Query performance by device"""
    query = f"""
    SELECT
      campaign.id,
      segments.device,
      segments.date,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value,
      metrics.ctr,
      metrics.average_cpc,
      metrics.search_impression_share,
      metrics.search_rank_lost_impression_share,
      metrics.search_budget_lost_impression_share
    FROM campaign
    WHERE campaign.id = {campaign_id}
      AND segments.date BETWEEN '{start_date}' AND '{end_date}'
      AND segments.device IS NOT NULL
    ORDER BY metrics.cost_micros DESC
    """
    
    if not MCP_AVAILABLE:
        return []
    
    try:
        result = execute_gaql(customer_id, query, manager_id=MANAGER_ID)
        return result.get('results', [])
    except Exception as e:
        print(f"❌ Error querying device performance: {e}")
        return []

def query_daily_breakdown(customer_id: str, campaign_id: str, start_date: str, end_date: str):
    """Query daily performance breakdown"""
    query = f"""
    SELECT
      campaign.id,
      segments.date,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value,
      metrics.ctr,
      metrics.average_cpc,
      metrics.search_impression_share,
      metrics.search_rank_lost_impression_share,
      metrics.search_budget_lost_impression_share,
      metrics.search_exact_match_impression_share
    FROM campaign
    WHERE campaign.id = {campaign_id}
      AND segments.date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY segments.date
    """
    
    if not MCP_AVAILABLE:
        return []
    
    try:
        result = execute_gaql(customer_id, query, manager_id=MANAGER_ID)
        return result.get('results', [])
    except Exception as e:
        print(f"❌ Error querying daily breakdown: {e}")
        return []

def analyze_search_terms(data_before: list, data_after: list):
    """Analyze search term performance changes"""
    print("\n" + "="*80)
    print("SEARCH TERMS ANALYSIS")
    print("="*80)
    
    # Aggregate by search term
    before_terms = defaultdict(lambda: {'impressions': 0, 'clicks': 0, 'cost': 0, 'conversions': 0, 'revenue': 0, 'rank_lost_is': 0, 'count': 0})
    after_terms = defaultdict(lambda: {'impressions': 0, 'clicks': 0, 'cost': 0, 'conversions': 0, 'revenue': 0, 'rank_lost_is': 0, 'count': 0})
    
    for row in data_before:
        term = row.get('segments', {}).get('searchTerm', 'Unknown')
        metrics = row.get('metrics', {})
        before_terms[term]['impressions'] += int(metrics.get('impressions', 0))
        before_terms[term]['clicks'] += int(metrics.get('clicks', 0))
        before_terms[term]['cost'] += format_micros(int(metrics.get('costMicros', 0)))
        before_terms[term]['conversions'] += float(metrics.get('conversions', 0))
        before_terms[term]['revenue'] += float(metrics.get('conversionsValue', 0))
        rank_lost = float(metrics.get('searchRankLostImpressionShare', 0))
        if rank_lost > 0:
            before_terms[term]['rank_lost_is'] = max(before_terms[term]['rank_lost_is'], rank_lost)
        before_terms[term]['count'] += 1
    
    for row in data_after:
        term = row.get('segments', {}).get('searchTerm', 'Unknown')
        metrics = row.get('metrics', {})
        after_terms[term]['impressions'] += int(metrics.get('impressions', 0))
        after_terms[term]['clicks'] += int(metrics.get('clicks', 0))
        after_terms[term]['cost'] += format_micros(int(metrics.get('costMicros', 0)))
        after_terms[term]['conversions'] += float(metrics.get('conversions', 0))
        after_terms[term]['revenue'] += float(metrics.get('conversionsValue', 0))
        rank_lost = float(metrics.get('searchRankLostImpressionShare', 0))
        if rank_lost > 0:
            after_terms[term]['rank_lost_is'] = max(after_terms[term]['rank_lost_is'], rank_lost)
        after_terms[term]['count'] += 1
    
    # Find terms that dropped significantly
    print("\n🔍 Top Search Terms - Before vs After Comparison:")
    print(f"{'Search Term':<50} {'Before Cost':<15} {'After Cost':<15} {'Rank Lost':<12} {'Status'}")
    print("-"*105)
    
    all_terms = set(list(before_terms.keys()) + list(after_terms.keys()))
    significant_drops = []
    
    for term in sorted(all_terms, key=lambda t: after_terms.get(t, {}).get('cost', 0), reverse=True)[:25]:
        before = before_terms.get(term, {})
        after = after_terms.get(term, {})
        
        before_cost = before.get('cost', 0)
        after_cost = after.get('cost', 0)
        rank_lost = after.get('rank_lost_is', 0) * 100 if after.get('rank_lost_is') else None
        
        if rank_lost:
            status = "🔴" if rank_lost > 70 else "🟡" if rank_lost > 50 else "🟢"
        else:
            status = "⚪"
        
        if before_cost > 0 and after_cost > 0:
            cost_change_pct = ((after_cost - before_cost) / before_cost) * 100
            print(f"{term[:48]:<50} £{before_cost:<14.2f} £{after_cost:<14.2f} {str(rank_lost) + '%' if rank_lost else 'N/A':<12} {status}")
            
            if rank_lost and rank_lost > 70:
                significant_drops.append({
                    'term': term,
                    'rank_lost': rank_lost,
                    'cost': after_cost,
                    'cost_change': cost_change_pct
                })
    
    if significant_drops:
        print(f"\n⚠️  Terms with Critical Rank Loss (>70%):")
        for drop in sorted(significant_drops, key=lambda x: x['cost'], reverse=True)[:10]:
            print(f"  - {drop['term']}: {drop['rank_lost']:.1f}% rank loss, £{drop['cost']:.2f} spend ({drop['cost_change']:+.1f}%)")

def analyze_placements(data_before: list, data_after: list):
    """Analyze placement performance changes"""
    print("\n" + "="*80)
    print("PLACEMENT ANALYSIS")
    print("="*80)
    
    before_placements = defaultdict(lambda: {'impressions': 0, 'clicks': 0, 'cost': 0, 'conversions': 0, 'revenue': 0})
    after_placements = defaultdict(lambda: {'impressions': 0, 'clicks': 0, 'cost': 0, 'conversions': 0, 'revenue': 0})
    
    for row in data_before:
        placement = row.get('groupPlacementView', {}).get('placement', 'Unknown')
        placement_type = row.get('groupPlacementView', {}).get('placementType', 'Unknown')
        key = f"{placement_type}: {placement}"
        metrics = row.get('metrics', {})
        before_placements[key]['impressions'] += int(metrics.get('impressions', 0))
        before_placements[key]['clicks'] += int(metrics.get('clicks', 0))
        before_placements[key]['cost'] += format_micros(int(metrics.get('costMicros', 0)))
        before_placements[key]['conversions'] += float(metrics.get('conversions', 0))
        before_placements[key]['revenue'] += float(metrics.get('conversionsValue', 0))
    
    for row in data_after:
        placement = row.get('groupPlacementView', {}).get('placement', 'Unknown')
        placement_type = row.get('groupPlacementView', {}).get('placementType', 'Unknown')
        key = f"{placement_type}: {placement}"
        metrics = row.get('metrics', {})
        after_placements[key]['impressions'] += int(metrics.get('impressions', 0))
        after_placements[key]['clicks'] += int(metrics.get('clicks', 0))
        after_placements[key]['cost'] += format_micros(int(metrics.get('costMicros', 0)))
        after_placements[key]['conversions'] += float(metrics.get('conversions', 0))
        after_placements[key]['revenue'] += float(metrics.get('conversionsValue', 0))
    
    print("\n📍 Top Placements - Before vs After:")
    print(f"{'Placement':<60} {'Before Cost':<15} {'After Cost':<15} {'Change':<15}")
    print("-"*105)
    
    all_placements = set(list(before_placements.keys()) + list(after_placements.keys()))
    for placement in sorted(all_placements, key=lambda p: after_placements.get(p, {}).get('cost', 0), reverse=True)[:15]:
        before = before_placements.get(placement, {})
        after = after_placements.get(placement, {})
        before_cost = before.get('cost', 0)
        after_cost = after.get('cost', 0)
        change = after_cost - before_cost
        change_pct = ((after_cost - before_cost) / before_cost * 100) if before_cost > 0 else 0
        
        status = "🔴" if change < -50 else "🟡" if change < 0 else "🟢"
        print(f"{placement[:58]:<60} £{before_cost:<14.2f} £{after_cost:<14.2f} {change_pct:+.1f}% {status}")

def analyze_daily_trends(data: list):
    """Analyze daily trends to see when the drop occurred"""
    print("\n" + "="*80)
    print("DAILY TREND ANALYSIS")
    print("="*80)
    
    daily_data = []
    for row in data:
        date = row.get('segments', {}).get('date', '')
        metrics = row.get('metrics', {})
        daily_data.append({
            'date': date,
            'impressions': int(metrics.get('impressions', 0)),
            'clicks': int(metrics.get('clicks', 0)),
            'cost': format_micros(int(metrics.get('costMicros', 0))),
            'conversions': float(metrics.get('conversions', 0)),
            'revenue': float(metrics.get('conversionsValue', 0)),
            'impression_share': float(metrics.get('searchImpressionShare', 0)) * 100 if metrics.get('searchImpressionShare') else None,
            'rank_lost_is': float(metrics.get('searchRankLostImpressionShare', 0)) * 100 if metrics.get('searchRankLostImpressionShare') else None,
            'budget_lost_is': float(metrics.get('searchBudgetLostImpressionShare', 0)) * 100 if metrics.get('searchBudgetLostImpressionShare') else None
        })
    
    daily_data.sort(key=lambda x: x['date'])
    
    print(f"\n{'Date':<12} {'IS':<8} {'Rank Lost':<12} {'Budget Lost':<12} {'Impressions':<12} {'Cost':<12} {'ROAS':<8}")
    print("-"*80)
    
    for day in daily_data:
        roas = (day['revenue'] / day['cost']) if day['cost'] > 0 else 0
        is_str = f"{day['impression_share']:.1f}%" if day['impression_share'] else "N/A"
        rank_str = f"{day['rank_lost_is']:.1f}%" if day['rank_lost_is'] else "N/A"
        budget_str = f"{day['budget_lost_is']:.1f}%" if day['budget_lost_is'] else "N/A"
        
        print(f"{day['date']:<12} {is_str:<8} {rank_str:<12} {budget_str:<12} {day['impressions']:<12} £{day['cost']:<11.2f} {roas:.2f}x")

def analyze_device_performance(data_before: list, data_after: list):
    """Analyze device performance changes"""
    print("\n" + "="*80)
    print("DEVICE PERFORMANCE ANALYSIS")
    print("="*80)
    
    before_devices = defaultdict(lambda: {'impressions': 0, 'clicks': 0, 'cost': 0, 'conversions': 0, 'revenue': 0, 'impression_share': None, 'rank_lost_is': None})
    after_devices = defaultdict(lambda: {'impressions': 0, 'clicks': 0, 'cost': 0, 'conversions': 0, 'revenue': 0, 'impression_share': None, 'rank_lost_is': None})
    
    for row in data_before:
        device = row.get('segments', {}).get('device', 'Unknown')
        metrics = row.get('metrics', {})
        before_devices[device]['impressions'] += int(metrics.get('impressions', 0))
        before_devices[device]['clicks'] += int(metrics.get('clicks', 0))
        before_devices[device]['cost'] += format_micros(int(metrics.get('costMicros', 0)))
        before_devices[device]['conversions'] += float(metrics.get('conversions', 0))
        before_devices[device]['revenue'] += float(metrics.get('conversionsValue', 0))
        if metrics.get('searchImpressionShare'):
            before_devices[device]['impression_share'] = float(metrics.get('searchImpressionShare', 0)) * 100
        if metrics.get('searchRankLostImpressionShare'):
            before_devices[device]['rank_lost_is'] = float(metrics.get('searchRankLostImpressionShare', 0)) * 100
    
    for row in data_after:
        device = row.get('segments', {}).get('device', 'Unknown')
        metrics = row.get('metrics', {})
        after_devices[device]['impressions'] += int(metrics.get('impressions', 0))
        after_devices[device]['clicks'] += int(metrics.get('clicks', 0))
        after_devices[device]['cost'] += format_micros(int(metrics.get('costMicros', 0)))
        after_devices[device]['conversions'] += float(metrics.get('conversions', 0))
        after_devices[device]['revenue'] += float(metrics.get('conversionsValue', 0))
        if metrics.get('searchImpressionShare'):
            after_devices[device]['impression_share'] = float(metrics.get('searchImpressionShare', 0)) * 100
        if metrics.get('searchRankLostImpressionShare'):
            after_devices[device]['rank_lost_is'] = float(metrics.get('searchRankLostImpressionShare', 0)) * 100
    
    print(f"\n{'Device':<15} {'Before IS':<12} {'After IS':<12} {'Before Rank Lost':<18} {'After Rank Lost':<18} {'Cost Change':<15}")
    print("-"*90)
    
    for device in ['MOBILE', 'DESKTOP', 'TABLET']:
        before = before_devices.get(device, {})
        after = after_devices.get(device, {})
        
        before_is = f"{before['impression_share']:.1f}%" if before.get('impression_share') else "N/A"
        after_is = f"{after['impression_share']:.1f}%" if after.get('impression_share') else "N/A"
        before_rank = f"{before['rank_lost_is']:.1f}%" if before.get('rank_lost_is') else "N/A"
        after_rank = f"{after['rank_lost_is']:.1f}%" if after.get('rank_lost_is') else "N/A"
        cost_change = after.get('cost', 0) - before.get('cost', 0)
        cost_change_pct = ((cost_change / before['cost']) * 100) if before.get('cost', 0) > 0 else 0
        
        status = "🔴" if after.get('rank_lost_is', 0) > 70 else "🟡" if after.get('rank_lost_is', 0) > 50 else "🟢"
        print(f"{device:<15} {before_is:<12} {after_is:<12} {before_rank:<18} {after_rank:<18} {cost_change_pct:+.1f}% {status}")

def main():
    print("="*80)
    print("P-MAX H&S UNBEAST CAMPAIGN - SEARCH IMPRESSION SHARE DIAGNOSTIC")
    print("="*80)
    print(f"\nCampaign ID: {CAMPAIGN_ID}")
    print(f"Campaign: Main P Max (Furniture H&S/Zombies)")
    print(f"\nAnalysis Periods:")
    print(f"  Before: Oct 29 - Nov 5 (7 days)")
    print(f"  After:  Nov 5 - Nov 9 (4 days)")
    print()
    
    # Query all data
    print("📊 Querying data...")
    
    print("  - Search terms...")
    search_terms_before = query_search_terms(CUSTOMER_ID, CAMPAIGN_ID, "2025-10-29", "2025-11-05")
    search_terms_after = query_search_terms(CUSTOMER_ID, CAMPAIGN_ID, "2025-11-05", "2025-11-09")
    print(f"     Found {len(search_terms_before)} terms (before), {len(search_terms_after)} terms (after)")
    
    print("  - Placements...")
    placements_before = query_placements(CUSTOMER_ID, CAMPAIGN_ID, "2025-10-29", "2025-11-05")
    placements_after = query_placements(CUSTOMER_ID, CAMPAIGN_ID, "2025-11-05", "2025-11-09")
    print(f"     Found {len(placements_before)} placements (before), {len(placements_after)} placements (after)")
    
    print("  - Device performance...")
    devices_before = query_device_performance(CUSTOMER_ID, CAMPAIGN_ID, "2025-10-29", "2025-11-05")
    devices_after = query_device_performance(CUSTOMER_ID, CAMPAIGN_ID, "2025-11-05", "2025-11-09")
    print(f"     Found {len(devices_before)} device records (before), {len(devices_after)} device records (after)")
    
    print("  - Daily breakdown...")
    daily_before = query_daily_breakdown(CUSTOMER_ID, CAMPAIGN_ID, "2025-10-29", "2025-11-05")
    daily_after = query_daily_breakdown(CUSTOMER_ID, CAMPAIGN_ID, "2025-11-05", "2025-11-09")
    print(f"     Found {len(daily_before)} days (before), {len(daily_after)} days (after)")
    
    # Calculate summary metrics
    before_total = {
        'impressions': 0,
        'cost': 0,
        'impression_share': None,
        'rank_lost_is': None,
        'budget_lost_is': None
    }
    
    after_total = {
        'impressions': 0,
        'cost': 0,
        'impression_share': None,
        'rank_lost_is': None,
        'budget_lost_is': None
    }
    
    if daily_before:
        for row in daily_before:
            metrics = row.get('metrics', {})
            before_total['impressions'] += int(metrics.get('impressions', 0))
            before_total['cost'] += format_micros(int(metrics.get('costMicros', 0)))
            if metrics.get('searchImpressionShare') and not before_total['impression_share']:
                before_total['impression_share'] = float(metrics.get('searchImpressionShare', 0)) * 100
            if metrics.get('searchRankLostImpressionShare') and not before_total['rank_lost_is']:
                before_total['rank_lost_is'] = float(metrics.get('searchRankLostImpressionShare', 0)) * 100
            if metrics.get('searchBudgetLostImpressionShare') and not before_total['budget_lost_is']:
                before_total['budget_lost_is'] = float(metrics.get('searchBudgetLostImpressionShare', 0)) * 100
    
    if daily_after:
        for row in daily_after:
            metrics = row.get('metrics', {})
            after_total['impressions'] += int(metrics.get('impressions', 0))
            after_total['cost'] += format_micros(int(metrics.get('costMicros', 0)))
            if metrics.get('searchImpressionShare') and not after_total['impression_share']:
                after_total['impression_share'] = float(metrics.get('searchImpressionShare', 0)) * 100
            if metrics.get('searchRankLostImpressionShare') and not after_total['rank_lost_is']:
                after_total['rank_lost_is'] = float(metrics.get('searchRankLostImpressionShare', 0)) * 100
            if metrics.get('searchBudgetLostImpressionShare') and not after_total['budget_lost_is']:
                after_total['budget_lost_is'] = float(metrics.get('searchBudgetLostImpressionShare', 0)) * 100
    
    # Print summary
    print("\n" + "="*80)
    print("KEY FINDINGS SUMMARY")
    print("="*80)
    
    print(f"\n📊 Impression Share Breakdown:")
    if before_total['impression_share'] and after_total['impression_share']:
        print(f"  Before: {before_total['impression_share']:.1f}%")
        print(f"  After:  {after_total['impression_share']:.1f}%")
        print(f"  Change: {after_total['impression_share'] - before_total['impression_share']:.1f}pp")
    
    print(f"\n📊 Rank-Lost Impression Share:")
    if before_total['rank_lost_is'] and after_total['rank_lost_is']:
        print(f"  Before: {before_total['rank_lost_is']:.1f}%")
        print(f"  After:  {after_total['rank_lost_is']:.1f}%")
        print(f"  Change: +{after_total['rank_lost_is'] - before_total['rank_lost_is']:.1f}pp")
        print(f"  ⚠️  Losing {after_total['rank_lost_is']:.1f}% of auctions to rank (competitors outbidding)")
    
    print(f"\n📊 Budget-Lost Impression Share:")
    if before_total['budget_lost_is'] and after_total['budget_lost_is']:
        print(f"  Before: {before_total['budget_lost_is']:.1f}%")
        print(f"  After:  {after_total['budget_lost_is']:.1f}%")
        print(f"  Change: +{after_total['budget_lost_is'] - before_total['budget_lost_is']:.1f}pp")
        if after_total['budget_lost_is'] > 10:
            print(f"  ⚠️  Budget constraints also contributing to impression loss")
    
    print(f"\n📊 Impressions & Spend:")
    print(f"  Impressions: {before_total['impressions']:,} → {after_total['impressions']:,} ({((after_total['impressions'] - before_total['impressions']) / before_total['impressions'] * 100) if before_total['impressions'] > 0 else 0:.1f}%)")
    print(f"  Cost: £{before_total['cost']:.2f} → £{after_total['cost']:.2f} ({((after_total['cost'] - before_total['cost']) / before_total['cost'] * 100) if before_total['cost'] > 0 else 0:.1f}%)")
    
    # Detailed analyses
    if search_terms_before and search_terms_after:
        analyze_search_terms(search_terms_before, search_terms_after)
    
    if placements_before and placements_after:
        analyze_placements(placements_before, placements_after)
    
    if devices_before and devices_after:
        analyze_device_performance(devices_before, devices_after)
    
    if daily_after:
        print("\n" + "="*80)
        print("DAILY BREAKDOWN (AFTER PERIOD - Nov 5-9)")
        print("="*80)
        analyze_daily_trends(daily_after)
    
    # Root cause analysis
    print("\n" + "="*80)
    print("ROOT CAUSE ANALYSIS")
    print("="*80)
    
    print("\n🔍 Key Deficiencies Identified:")
    
    if after_total.get('rank_lost_is', 0) > 70:
        print(f"\n1. 🔴 CRITICAL: Rank-Lost Impression Share at {after_total['rank_lost_is']:.1f}%")
        print("   - Losing 77% of auctions to competitors")
        print("   - Possible causes:")
        print("     • Quality score issues (ad relevance, landing page experience)")
        print("     • Competitors increased bids/quality scores")
        print("     • Ad creative fatigue")
        print("     • Product feed quality problems")
        print("     • ROAS target too restrictive (190% may be limiting bid flexibility)")
    
    if after_total.get('budget_lost_is', 0) > 15:
        print(f"\n2. 🟡 MODERATE: Budget-Lost Impression Share at {after_total['budget_lost_is']:.1f}%")
        print("   - Budget constraints preventing full participation")
        print("   - Possible causes:")
        print("     • Daily budget too low for competitive auctions")
        print("     • Budget pacing issues")
        print("     • Campaign spending budget too quickly")
    
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    
    print("\n🔧 Immediate Actions:")
    print("1. Review Quality Score Components:")
    print("   - Check Google Ads UI for quality score warnings")
    print("   - Review ad relevance scores")
    print("   - Check landing page experience scores")
    print("   - Verify expected CTR signals")
    
    print("\n2. Investigate Competitive Pressure:")
    print("   - Review Auction Insights for competitor bid increases")
    print("   - Check if competitors improved quality scores")
    print("   - Monitor competitor activity (Cox & Cox, Dunelm, etc.)")
    
    print("\n3. Review Product Feed:")
    print("   - Check for product data quality issues")
    print("   - Verify product availability/stock")
    print("   - Review product images quality")
    print("   - Check for feed errors in Merchant Center")
    
    print("\n4. Consider Bid Strategy:")
    print("   - 190% ROAS target may be too restrictive")
    print("   - Algorithm may need more flexibility to compete")
    print("   - Consider testing 185% or monitoring longer")
    
    print("\n5. Asset Performance:")
    print("   - Review Performance Max asset performance")
    print("   - Check which assets are underperforming")
    print("   - Consider refreshing creative assets")
    
    # Save results
    output_file = PROJECT_ROOT / 'clients' / 'accessories-for-the-home' / 'audits' / f'{datetime.now().strftime("%Y%m%d")}-pmax-search-is-diagnostic.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    results = {
        'campaign_id': CAMPAIGN_ID,
        'campaign_name': 'Main P Max (Furniture H&S/Zombies)',
        'analysis_date': datetime.now().strftime('%Y-%m-%d'),
        'before_period': {'start': '2025-10-29', 'end': '2025-11-05'},
        'after_period': {'start': '2025-11-05', 'end': '2025-11-09'},
        'summary': {
            'before': before_total,
            'after': after_total
        },
        'search_terms_before_count': len(search_terms_before),
        'search_terms_after_count': len(search_terms_after),
        'placements_before_count': len(placements_before),
        'placements_after_count': len(placements_after)
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Diagnostic data saved to: {output_file}")

if __name__ == "__main__":
    main()

