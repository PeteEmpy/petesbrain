#!/usr/bin/env python3
"""
Check for Friday impression share dips across multiple client accounts
Investigates whether impression share drops on Fridays are due to data reporting delays
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
    sys.exit(1)

# Load client config
CLIENTS_CONFIG = PROJECT_ROOT / 'shared' / 'data' / 'google-ads-clients.json'
with open(CLIENTS_CONFIG, 'r') as f:
    clients_data = json.load(f)

def get_day_of_week(date_str):
    """Get day of week name from date string"""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%A')

def query_campaign_impression_share(customer_id: str, manager_id: str, start_date: str, end_date: str):
    """Query campaign-level impression share data"""
    query = f"""
    SELECT
      campaign.id,
      campaign.name,
      segments.date,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.search_impression_share,
      metrics.search_rank_lost_impression_share,
      metrics.search_budget_lost_impression_share
    FROM campaign
    WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
      AND campaign.status = 'ENABLED'
      AND metrics.impressions > 0
    ORDER BY segments.date, campaign.id
    """
    
    try:
        result = execute_gaql(customer_id, query, manager_id=manager_id)
        return result.get('results', [])
    except Exception as e:
        print(f"  ❌ Error querying: {e}")
        return []

def analyze_friday_patterns(client_slug: str, customer_id: str, manager_id: str, days: int = 14):
    """Analyze impression share patterns by day of week"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    print(f"\n📊 Analyzing {client_slug} ({customer_id})...")
    print(f"   Date range: {start_date} to {end_date}")
    
    data = query_campaign_impression_share(
        customer_id, 
        manager_id or "2569949686",
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )
    
    if not data:
        print(f"   ⚠️  No data returned")
        return None
    
    # Group by day of week
    by_day = defaultdict(lambda: {'impression_share': [], 'rank_lost': [], 'budget_lost': [], 'dates': []})
    
    for row in data:
        date_str = row.get('segments', {}).get('date', '')
        if not date_str:
            continue
        
        day_name = get_day_of_week(date_str)
        metrics = row.get('metrics', {})
        
        if metrics.get('searchImpressionShare'):
            is_value = float(metrics.get('searchImpressionShare', 0)) * 100
            by_day[day_name]['impression_share'].append(is_value)
            by_day[day_name]['dates'].append(date_str)
        
        if metrics.get('searchRankLostImpressionShare'):
            rank_lost = float(metrics.get('searchRankLostImpressionShare', 0)) * 100
            by_day[day_name]['rank_lost'].append(rank_lost)
        
        if metrics.get('searchBudgetLostImpressionShare'):
            budget_lost = float(metrics.get('searchBudgetLostImpressionShare', 0)) * 100
            by_day[day_name]['budget_lost'].append(budget_lost)
    
    # Calculate averages
    day_averages = {}
    for day_name in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        if day_name in by_day:
            is_values = by_day[day_name]['impression_share']
            rank_values = by_day[day_name]['rank_lost']
            budget_values = by_day[day_name]['budget_lost']
            
            if is_values:
                day_averages[day_name] = {
                    'avg_is': sum(is_values) / len(is_values),
                    'min_is': min(is_values),
                    'max_is': max(is_values),
                    'count': len(is_values),
                    'avg_rank_lost': sum(rank_values) / len(rank_values) if rank_values else None,
                    'avg_budget_lost': sum(budget_values) / len(budget_values) if budget_values else None,
                    'dates': sorted(set(by_day[day_name]['dates']))
                }
    
    return day_averages

def main():
    print("="*80)
    print("FRIDAY IMPRESSION SHARE PATTERN ANALYSIS")
    print("="*80)
    print("\nChecking for Friday dips across multiple client accounts...")
    print("(This helps identify if drops are due to data reporting delays)")
    
    results = {}
    
    # Check multiple clients
    clients_to_check = [
        'accessories-for-the-home',
        'smythson',
        'devonshire-hotels',
        'tree2mydoor',
        'uno-lighting',
        'superspace',
        'positive-bakes',
        'just-bin-bags'
    ]
    
    for client_slug in clients_to_check:
        if client_slug not in clients_data.get('clients', {}):
            continue
        
        client_info = clients_data['clients'][client_slug]
        customer_id = client_info['customer_id']
        manager_id = client_info.get('manager_id')
        
        try:
            day_averages = analyze_friday_patterns(client_slug, customer_id, manager_id, days=14)
            if day_averages:
                results[client_slug] = day_averages
        except Exception as e:
            print(f"  ❌ Error analyzing {client_slug}: {e}")
            continue
    
    # Print summary
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    
    friday_dips = []
    
    for client_slug, day_data in results.items():
        print(f"\n📊 {client_slug.replace('-', ' ').title()}:")
        print(f"{'Day':<12} {'Avg IS':<12} {'Min IS':<12} {'Max IS':<12} {'Count':<8} {'Status'}")
        print("-"*70)
        
        friday_is = None
        other_days_avg = []
        
        for day_name in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            if day_name in day_data:
                data = day_data[day_name]
                avg_is = data['avg_is']
                min_is = data['min_is']
                max_is = data['max_is']
                count = data['count']
                
                if day_name == 'Friday':
                    friday_is = avg_is
                else:
                    other_days_avg.append(avg_is)
                
                # Check if Friday is significantly lower
                status = ""
                if day_name == 'Friday' and other_days_avg:
                    avg_other = sum(other_days_avg) / len(other_days_avg)
                    if friday_is < avg_other - 10:  # More than 10pp lower
                        status = "🔴 FRIDAY DIP"
                        friday_dips.append({
                            'client': client_slug,
                            'friday_is': friday_is,
                            'other_avg': avg_other,
                            'difference': avg_other - friday_is
                        })
                    elif friday_is < avg_other - 5:
                        status = "🟡 Minor dip"
                
                print(f"{day_name:<12} {avg_is:<12.1f} {min_is:<12.1f} {max_is:<12.1f} {count:<8} {status}")
    
    # Summary of Friday dips
    print("\n" + "="*80)
    print("FRIDAY DIP ANALYSIS")
    print("="*80)
    
    if friday_dips:
        print(f"\n⚠️  Found {len(friday_dips)} client(s) with Friday impression share dips:")
        for dip in friday_dips:
            print(f"\n  🔴 {dip['client'].replace('-', ' ').title()}:")
            print(f"     Friday avg IS: {dip['friday_is']:.1f}%")
            print(f"     Other days avg: {dip['other_avg']:.1f}%")
            print(f"     Difference: {dip['difference']:.1f}pp lower on Friday")
        
        print("\n💡 Interpretation:")
        print("   - Friday dips across multiple accounts suggest DATA REPORTING DELAY")
        print("   - Impression share data may not be fully populated on Fridays")
        print("   - Wait 48-72 hours before analyzing Friday impression share data")
        print("   - This is a known Google Ads reporting behavior")
    else:
        print("\n✅ No significant Friday dips detected across checked accounts")
        print("   (This doesn't rule out reporting delays - may need more data)")
    
    # Save results
    output_file = PROJECT_ROOT / 'clients' / 'accessories-for-the-home' / 'audits' / f'{datetime.now().strftime("%Y%m%d")}-friday-is-pattern-analysis.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump({
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'period_days': 14,
            'friday_dips_detected': len(friday_dips),
            'friday_dips': friday_dips,
            'client_results': results
        }, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")

if __name__ == "__main__":
    main()

