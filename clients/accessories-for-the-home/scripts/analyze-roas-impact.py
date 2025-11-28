#!/usr/bin/env python3
"""
Analyze the impact of ROAS target change from 200% to 190% on Nov 5, 2025
Compares performance before (Oct 29 - Nov 5) vs after (Nov 5 - Nov 9)
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server'))

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / '.env')
    load_dotenv(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env')
    load_dotenv(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server' / '.env 2')
except ImportError:
    # Fallback: manually load .env file if dotenv not available
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
CHANGE_DATE = "2025-11-05"
TODAY = datetime.now().strftime('%Y-%m-%d')

# Campaign IDs that changed
CAMPAIGNS_TO_ANALYZE = {
    "20276730131": "Main P Max (Furniture H&S/Zombies)",
    "21527979308": "Shopping Furniture (Villains)"
}

def format_micros(micros):
    """Convert micros to currency"""
    return micros / 1_000_000

def format_percent(value):
    """Format as percentage"""
    return f"{value * 100:.2f}%"

def query_campaign_performance(customer_id: str, start_date: str, end_date: str, campaign_ids: list = None, use_conversion_time: bool = False):
    """Query campaign performance data
    
    Args:
        use_conversion_time: If True, uses conversion_date for attribution (conversion-time)
                            If False, uses date for attribution (click-time, default)
    """
    
    campaign_filter = ""
    if campaign_ids:
        campaign_ids_str = ", ".join(campaign_ids)
        campaign_filter = f"AND campaign.id IN ({campaign_ids_str})"
    
    # For conversion-time attribution, we need to use segments.conversion_date
    # But note: conversion_date requires querying from a resource that supports it
    # For campaign-level, we'll query both ways and compare
    
    if use_conversion_time:
        # Query by conversion date - this shows when conversions actually happened
        # Note: This may require a different approach or resource
        query = f"""
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          campaign.advertising_channel_type,
          campaign.maximize_conversion_value.target_roas,
          segments.conversion_date,
          metrics.impressions,
          metrics.clicks,
          metrics.ctr,
          metrics.cost_micros,
          metrics.conversions,
          metrics.conversions_value,
          metrics.cost_per_conversion,
          metrics.average_cpc,
          metrics.search_impression_share,
          metrics.search_budget_lost_impression_share,
          metrics.search_rank_lost_impression_share
        FROM campaign
        WHERE segments.conversion_date BETWEEN '{start_date}' AND '{end_date}'
          AND campaign.status = 'ENABLED'
          {campaign_filter}
        ORDER BY campaign.id, segments.conversion_date
        """
    else:
        # Default: query by click date (when the ad was clicked)
        query = f"""
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          campaign.advertising_channel_type,
          campaign.maximize_conversion_value.target_roas,
          segments.date,
          metrics.impressions,
          metrics.clicks,
          metrics.ctr,
          metrics.cost_micros,
          metrics.conversions,
          metrics.conversions_value,
          metrics.cost_per_conversion,
          metrics.average_cpc,
          metrics.search_impression_share,
          metrics.search_budget_lost_impression_share,
          metrics.search_rank_lost_impression_share
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
          AND campaign.status = 'ENABLED'
          {campaign_filter}
        ORDER BY campaign.id, segments.date
        """
    
    if not MCP_AVAILABLE:
        print(f"❌ Cannot query - MCP not available")
        return []
    
    try:
        print(f"📊 Querying {start_date} to {end_date}...")
        result = execute_gaql(customer_id, query, manager_id=MANAGER_ID)
        return result.get('results', [])
    except Exception as e:
        print(f"❌ Error querying: {e}")
        import traceback
        traceback.print_exc()
        return []

def aggregate_campaign_data(raw_data: list, campaign_id: str, use_conversion_time: bool = False):
    """Aggregate daily data into campaign totals"""
    campaign_data = {
        'id': campaign_id,
        'name': '',
        'days': 0,
        'impressions': 0,
        'clicks': 0,
        'cost_micros': 0,
        'conversions': 0.0,
        'conversions_value': 0.0,
        'impression_share': None,
        'budget_lost_is': None,
        'rank_lost_is': None
    }
    
    for row in raw_data:
        if row.get('campaign', {}).get('id') == campaign_id:
            metrics = row.get('metrics', {})
            campaign = row.get('campaign', {})
            segments = row.get('segments', {})
            
            if not campaign_data['name']:
                campaign_data['name'] = campaign.get('name', 'Unknown')
            
            # For conversion-time attribution, impressions/clicks/cost are still from click date
            # Only conversions/conversions_value are attributed to conversion date
            # So we need to handle this differently
            
            campaign_data['days'] += 1
            
            # Impressions, clicks, cost are always from click date
            campaign_data['impressions'] += int(metrics.get('impressions', 0))
            campaign_data['clicks'] += int(metrics.get('clicks', 0))
            campaign_data['cost_micros'] += int(metrics.get('costMicros', 0))
            
            # Conversions and conversion value depend on attribution method
            campaign_data['conversions'] += float(metrics.get('conversions', 0))
            campaign_data['conversions_value'] += float(metrics.get('conversionsValue', 0))
            
            # Use latest impression share values (they're cumulative)
            if metrics.get('searchImpressionShare'):
                campaign_data['impression_share'] = float(metrics.get('searchImpressionShare', 0))
            if metrics.get('searchBudgetLostImpressionShare'):
                campaign_data['budget_lost_is'] = float(metrics.get('searchBudgetLostImpressionShare', 0))
            if metrics.get('searchRankLostImpressionShare'):
                campaign_data['rank_lost_is'] = float(metrics.get('searchRankLostImpressionShare', 0))
    
    return campaign_data

def calculate_metrics(data: dict):
    """Calculate derived metrics"""
    cost = format_micros(data['cost_micros'])
    conv_value = data['conversions_value']
    conversions = data['conversions']
    
    roas = (conv_value / cost) if cost > 0 else 0
    cpa = (cost / conversions) if conversions > 0 else 0
    cvr = (conversions / data['clicks']) if data['clicks'] > 0 else 0
    ctr = (data['clicks'] / data['impressions']) if data['impressions'] > 0 else 0
    
    return {
        'cost': round(cost, 2),
        'revenue': round(conv_value, 2),
        'roas': round(roas, 2),
        'conversions': round(conversions, 2),
        'cpa': round(cpa, 2),
        'cvr': round(cvr * 100, 2),
        'ctr': round(ctr * 100, 2),
        'impressions': data['impressions'],
        'clicks': data['clicks'],
        'impression_share': round(data['impression_share'] * 100, 1) if data['impression_share'] else None,
        'budget_lost_is': round(data['budget_lost_is'] * 100, 1) if data['budget_lost_is'] else None,
        'rank_lost_is': round(data['rank_lost_is'] * 100, 1) if data['rank_lost_is'] else None
    }

def compare_periods(before_data: dict, after_data: dict):
    """Compare before and after metrics"""
    comparison = {}
    
    for metric in ['cost', 'revenue', 'roas', 'conversions', 'cpa', 'cvr', 'ctr', 'impressions', 'clicks']:
        before_val = before_data.get(metric, 0)
        after_val = after_data.get(metric, 0)
        
        if before_val == 0:
            pct_change = None
        else:
            pct_change = ((after_val - before_val) / before_val) * 100
        
        comparison[metric] = {
            'before': before_val,
            'after': after_val,
            'change': after_val - before_val,
            'pct_change': round(pct_change, 1) if pct_change is not None else None
        }
    
    # Impression share comparison
    for metric in ['impression_share', 'budget_lost_is', 'rank_lost_is']:
        before_val = before_data.get(metric)
        after_val = after_data.get(metric)
        
        if before_val is not None and after_val is not None:
            comparison[metric] = {
                'before': before_val,
                'after': after_val,
                'change': round(after_val - before_val, 1)
            }
    
    return comparison

def main():
    print("=" * 80)
    print("ROAS Target Change Impact Analysis")
    print("Accessories for the Home")
    print("=" * 80)
    print(f"\nChange Date: {CHANGE_DATE} (200% → 190%)")
    print(f"Analysis Date: {TODAY}")
    print(f"\nPeriods:")
    print(f"  Before: Oct 29 - Nov 5 (7 days)")
    print(f"  After:  Nov 5 - Nov 9 ({datetime.strptime(TODAY, '%Y-%m-%d').day - 5} days)")
    print()
    
    print("📊 Querying by CLICK TIME (default attribution)...")
    # Query before period - click time
    before_data_raw_click = query_campaign_performance(
        CUSTOMER_ID,
        "2025-10-29",
        "2025-11-05",
        list(CAMPAIGNS_TO_ANALYZE.keys()),
        use_conversion_time=False
    )
    
    # Query after period - click time
    after_data_raw_click = query_campaign_performance(
        CUSTOMER_ID,
        "2025-11-05",
        TODAY,
        list(CAMPAIGNS_TO_ANALYZE.keys()),
        use_conversion_time=False
    )
    
    print("\n📊 Querying with EXTENDED DATE RANGE to capture delayed conversions...")
    # For conversion-time analysis, we query clicks from Nov 5-9 but extend the end date
    # to capture conversions that happened later (typical conversion lag is 1-3 days for e-commerce)
    # We'll query clicks from Nov 5-9 but look for conversions up to Nov 12 (3 days later)
    extended_end_date = (datetime.strptime(TODAY, '%Y-%m-%d') + timedelta(days=3)).strftime('%Y-%m-%d')
    
    print(f"   Extended end date: {extended_end_date} (to capture conversions from Nov 5-9 clicks)")
    
    # Query clicks from Nov 5-9 but with extended window for conversions
    after_data_raw_extended = query_campaign_performance(
        CUSTOMER_ID,
        "2025-11-05",
        extended_end_date,
        list(CAMPAIGNS_TO_ANALYZE.keys()),
        use_conversion_time=False
    )
    
    # Filter extended data to only include clicks from Nov 5-9 period
    # (conversions may have happened later, but clicks are from our period)
    after_data_raw_extended_filtered = []
    for row in after_data_raw_extended:
        click_date = row.get('segments', {}).get('date', '')
        if click_date and click_date >= "2025-11-05" and click_date <= TODAY:
            after_data_raw_extended_filtered.append(row)
    
    # Use click-time data for primary analysis
    before_data_raw = before_data_raw_click
    after_data_raw = after_data_raw_click
    
    print(f"\n📊 Comparison:")
    print(f"   Click-time attribution: Conversions attributed to click date")
    print(f"   Extended window: Clicks Nov 5-9, conversions may happen up to {extended_end_date}")
    print(f"   This helps identify conversion lag effects")
    
    if not before_data_raw and not after_data_raw:
        print("\n❌ No data retrieved. Check MCP connection and credentials.")
        return
    
    # Process data for each campaign - compare click-time vs extended window
    results = {}
    
    # Also process extended window data for comparison
    after_extended_agg = {}
    for campaign_id in CAMPAIGNS_TO_ANALYZE.keys():
        after_extended_agg[campaign_id] = aggregate_campaign_data(after_data_raw_extended_filtered, campaign_id)
    
    for campaign_id, campaign_name in CAMPAIGNS_TO_ANALYZE.items():
        print(f"\n{'='*80}")
        print(f"Campaign: {campaign_name} (ID: {campaign_id})")
        print(f"{'='*80}")
        
        # Aggregate before period
        before_raw = [r for r in before_data_raw if r.get('campaign', {}).get('id') == campaign_id]
        before_agg = aggregate_campaign_data(before_raw, campaign_id)
        before_metrics = calculate_metrics(before_agg)
        
        # Aggregate after period (click-time attribution)
        after_raw = [r for r in after_data_raw if r.get('campaign', {}).get('id') == campaign_id]
        after_agg = aggregate_campaign_data(after_raw, campaign_id)
        after_metrics = calculate_metrics(after_agg)
        
        # Also calculate with extended window (to see delayed conversions)
        after_extended_raw = [r for r in after_data_raw_extended_filtered if r.get('campaign', {}).get('id') == campaign_id]
        after_extended_agg = aggregate_campaign_data(after_extended_raw, campaign_id)
        after_extended_metrics = calculate_metrics(after_extended_agg)
        
        # Compare
        comparison = compare_periods(before_metrics, after_metrics)
        
        # Compare with extended window to check for conversion lag
        conv_lag_revenue = after_extended_metrics['revenue'] - after_metrics['revenue']
        conv_lag_conversions = after_extended_metrics['conversions'] - after_metrics['conversions']
        
        results[campaign_id] = {
            'name': campaign_name,
            'before': before_metrics,
            'after': after_metrics,
            'after_extended': after_extended_metrics,
            'comparison': comparison,
            'conversion_lag': {
                'revenue': conv_lag_revenue,
                'conversions': conv_lag_conversions
            }
        }
        
        # Print summary
        print(f"\n📊 BEFORE (Oct 29 - Nov 5):")
        print(f"  Spend:        £{before_metrics['cost']:.2f}")
        print(f"  Revenue:     £{before_metrics['revenue']:.2f}")
        print(f"  ROAS:        {before_metrics['roas']:.2f}x")
        print(f"  Conversions:  {before_metrics['conversions']:.1f}")
        print(f"  CPA:         £{before_metrics['cpa']:.2f}")
        print(f"  CVR:         {before_metrics['cvr']:.2f}%")
        print(f"  CTR:         {before_metrics['ctr']:.2f}%")
        if before_metrics.get('impression_share'):
            print(f"  Imp Share:   {before_metrics['impression_share']:.1f}%")
        if before_metrics.get('rank_lost_is'):
            print(f"  Rank Lost:   {before_metrics['rank_lost_is']:.1f}%")
        
        print(f"\n📊 AFTER (Nov 5 - Nov 9):")
        print(f"  Spend:        £{after_metrics['cost']:.2f}")
        print(f"  Revenue:     £{after_metrics['revenue']:.2f}")
        print(f"  ROAS:        {after_metrics['roas']:.2f}x")
        print(f"  Conversions:  {after_metrics['conversions']:.1f}")
        print(f"  CPA:         £{after_metrics['cpa']:.2f}")
        print(f"  CVR:         {after_metrics['cvr']:.2f}%")
        print(f"  CTR:         {after_metrics['ctr']:.2f}%")
        if after_metrics.get('impression_share'):
            print(f"  Imp Share:   {after_metrics['impression_share']:.1f}%")
        if after_metrics.get('rank_lost_is'):
            print(f"  Rank Lost:   {after_metrics['rank_lost_is']:.1f}%")
        
        print(f"\n📈 CHANGE (Click-Time Attribution):")
        roas_change = comparison['roas']['pct_change']
        roas_emoji = "🟢" if roas_change and roas_change > -5 else "🟡" if roas_change and roas_change > -10 else "🔴"
        print(f"  ROAS:        {roas_emoji} {comparison['roas']['change']:+.2f}x ({comparison['roas']['pct_change']:+.1f}%)")
        print(f"  Revenue:     {'🟢' if comparison['revenue']['change'] > 0 else '🔴'} £{comparison['revenue']['change']:+.2f} ({comparison['revenue']['pct_change']:+.1f}%)")
        print(f"  Conversions: {'🟢' if comparison['conversions']['change'] > 0 else '🔴'} {comparison['conversions']['change']:+.1f} ({comparison['conversions']['pct_change']:+.1f}%)")
        print(f"  Spend:       {'🟢' if comparison['cost']['change'] > 0 else '🔴'} £{comparison['cost']['change']:+.2f} ({comparison['cost']['pct_change']:+.1f}%)")
        print(f"  CPA:         {'🟢' if comparison['cpa']['change'] < 0 else '🔴'} £{comparison['cpa']['change']:+.2f} ({comparison['cpa']['pct_change']:+.1f}%)")
        print(f"  CVR:         {'🟢' if comparison['cvr']['change'] > 0 else '🔴'} {comparison['cvr']['change']:+.2f}pp ({comparison['cvr']['pct_change']:+.1f}%)")
        if 'impression_share' in comparison:
            print(f"  Imp Share:   {'🟢' if comparison['impression_share']['change'] > 0 else '🔴'} {comparison['impression_share']['change']:+.1f}pp")
        if 'rank_lost_is' in comparison:
            print(f"  Rank Lost:   {'🟢' if comparison['rank_lost_is']['change'] < 0 else '🔴'} {comparison['rank_lost_is']['change']:+.1f}pp")
        
        # Compare with extended window to check for conversion lag
        conv_lag_revenue = after_extended_metrics['revenue'] - after_metrics['revenue']
        conv_lag_conversions = after_extended_metrics['conversions'] - after_metrics['conversions']
        
        if conv_lag_revenue > 0 or conv_lag_conversions > 0:
            print(f"\n⏱️  CONVERSION LAG ANALYSIS (clicks Nov 5-9, conversions through {extended_end_date}):")
            print(f"  Additional Revenue (delayed): £{conv_lag_revenue:+.2f}")
            print(f"  Additional Conversions (delayed): {conv_lag_conversions:+.1f}")
            if after_extended_metrics['cost'] > 0:
                extended_roas = after_extended_metrics['revenue'] / after_extended_metrics['cost']
                print(f"  Extended Window ROAS: {extended_roas:.2f}x (vs {after_metrics['roas']:.2f}x click-time)")
                print(f"  ⚠️  Note: This suggests conversions are still coming in from Nov 5-9 clicks")
    
    # Save results
    output_file = PROJECT_ROOT / 'clients' / 'accessories-for-the-home' / 'audits' / f'{TODAY.replace("-", "")}-roas-impact-analysis.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump({
            'analysis_date': TODAY,
            'change_date': CHANGE_DATE,
            'before_period': {'start': '2025-10-29', 'end': '2025-11-05', 'days': 7},
            'after_period': {'start': '2025-11-05', 'end': TODAY, 'days': (datetime.strptime(TODAY, '%Y-%m-%d') - datetime.strptime('2025-11-05', '%Y-%m-%d')).days},
            'campaigns': results
        }, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    main()

