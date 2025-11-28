#!/usr/bin/env python3
"""
Fetch weekly Google Ads performance data for all active clients.
Runs every Monday at 8:00 AM before the weekly summary email.

Outputs: data/cache/weekly-client-performance.json
"""

import os
import sys
import json
import statistics
from pathlib import Path
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "cache" / "weekly-client-performance.json"
GOOGLE_ADS_YAML = Path.home() / "google-ads.yaml"

# Active client configuration
ACTIVE_CLIENTS = {
    'Bright Minds': '1404868570',
    'Tree2mydoor': '4941701449',
    'National Design Academy': '1994728449',
    'Accessories for the Home': '7972994730',
    'Devonshire Hotels': '5898250490',
    'Go Glean': '8492163737',
    'Godshot': '9922220205',
    'Grain Guard': '4391940141',
    'Just Bin Bags': '9697059148',
    'Smythson UK': '8573235780',
    'Superspace': '7482100090',
    'Uno Lighting': '6413338364',
    # 'Positive Bakes': 'TBD',  # TODO: Add customer ID once Google Ads account is set up
}

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def fetch_client_performance(client, customer_id, start_date, end_date):
    """Fetch performance data for a single client"""
    try:
        query = f"""
            SELECT
                segments.date,
                metrics.conversions_value,
                metrics.cost_micros,
                metrics.conversions,
                metrics.clicks,
                metrics.impressions
            FROM customer
            WHERE segments.date >= '{start_date.strftime('%Y-%m-%d')}'
              AND segments.date <= '{end_date.strftime('%Y-%m-%d')}'
            ORDER BY segments.date
        """

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search(customer_id=customer_id, query=query)

        daily_data = []
        for row in response:
            daily_data.append({
                'date': row.segments.date,
                'revenue': row.metrics.conversions_value,
                'cost': row.metrics.cost_micros / 1_000_000,  # Convert micros to currency
                'conversions': row.metrics.conversions,
                'clicks': row.metrics.clicks,
                'impressions': row.metrics.impressions
            })

        return daily_data

    except Exception as e:
        log(f"  Error fetching data for {customer_id}: {e}")
        return []

def analyze_performance(current_week_data, prev_week_data, client_name):
    """Analyze performance and detect outliers"""
    if not current_week_data:
        return None

    # Calculate weekly totals
    current_revenue = sum(d['revenue'] for d in current_week_data)
    current_cost = sum(d['cost'] for d in current_week_data)
    current_conversions = sum(d['conversions'] for d in current_week_data)
    current_roas = (current_revenue / current_cost * 100) if current_cost > 0 else 0

    prev_revenue = sum(d['revenue'] for d in prev_week_data) if prev_week_data else 0
    prev_cost = sum(d['cost'] for d in prev_week_data) if prev_week_data else 0
    prev_conversions = sum(d['conversions'] for d in prev_week_data) if prev_week_data else 0
    prev_roas = (prev_revenue / prev_cost * 100) if prev_cost > 0 else 0

    # Calculate changes
    revenue_change_pct = ((current_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    roas_change_pct = ((current_roas - prev_roas) / prev_roas * 100) if prev_roas > 0 else 0

    # Detect outliers (days with unusually high/low performance)
    revenues = [d['revenue'] for d in current_week_data]
    avg_revenue = statistics.mean(revenues) if revenues else 0
    std_revenue = statistics.stdev(revenues) if len(revenues) > 1 else 0

    outliers = []
    for day_data in current_week_data:
        if std_revenue > 0:
            z_score = (day_data['revenue'] - avg_revenue) / std_revenue
            if abs(z_score) > 1.5:  # More than 1.5 standard deviations
                deviation_pct = ((day_data['revenue'] - avg_revenue) / avg_revenue * 100) if avg_revenue > 0 else 0
                outliers.append({
                    'date': day_data['date'],
                    'metric': 'revenue',
                    'value': round(day_data['revenue'], 2),
                    'deviation': f"{'+' if deviation_pct > 0 else ''}{int(deviation_pct)}%",
                    'note': f"{'Above' if deviation_pct > 0 else 'Below'} week average of £{int(avg_revenue)}"
                })

    # Generate one-sentence summary
    trend_emoji = "↑" if revenue_change_pct > 5 else ("↓" if revenue_change_pct < -5 else "→")
    roas_trend = "improved" if roas_change_pct > 0 else "declined"

    if abs(revenue_change_pct) < 5:
        summary = f"{trend_emoji} Stable performance (£{int(current_revenue)} revenue, {int(current_roas)}% ROAS)."
    else:
        summary = f"{trend_emoji} Revenue {('up' if revenue_change_pct > 0 else 'down')} {abs(int(revenue_change_pct))}% week-over-week (£{int(current_revenue)} vs £{int(prev_revenue)}). ROAS {roas_trend} to {int(current_roas)}%."

    if outliers:
        outlier_dates = ', '.join([o['date'] for o in outliers[:2]])
        summary += f" Notable: {outlier_dates} performance spike."

    return {
        'name': client_name,
        'current_week': {
            'revenue': round(current_revenue, 2),
            'cost': round(current_cost, 2),
            'roas': round(current_roas, 0),
            'conversions': round(current_conversions, 1)
        },
        'previous_week': {
            'revenue': round(prev_revenue, 2),
            'cost': round(prev_cost, 2),
            'roas': round(prev_roas, 0),
            'conversions': round(prev_conversions, 1)
        },
        'changes': {
            'revenue_pct': round(revenue_change_pct, 1),
            'roas_pct': round(roas_change_pct, 1),
            'trend': 'up' if revenue_change_pct > 5 else ('down' if revenue_change_pct < -5 else 'stable')
        },
        'outliers': outliers[:3],  # Top 3 outliers
        'summary': summary
    }

def main():
    log("=" * 60)
    log("Fetching Weekly Client Performance Data")
    log("=" * 60)

    # Check for Google Ads config
    if not GOOGLE_ADS_YAML.exists():
        log(f"ERROR: Google Ads config not found at {GOOGLE_ADS_YAML}")
        return 1

    # Initialize Google Ads client
    try:
        ads_client = GoogleAdsClient.load_from_storage(str(GOOGLE_ADS_YAML))
    except Exception as e:
        log(f"ERROR: Failed to initialize Google Ads client: {e}")
        return 1

    # Calculate date ranges
    today = datetime.now().date()
    current_week_end = today - timedelta(days=1)  # Yesterday
    current_week_start = current_week_end - timedelta(days=6)  # 7 days ago
    prev_week_end = current_week_start - timedelta(days=1)
    prev_week_start = prev_week_end - timedelta(days=6)

    log(f"Current week: {current_week_start} to {current_week_end}")
    log(f"Previous week: {prev_week_start} to {prev_week_end}")

    # Fetch performance for all clients
    results = []
    for client_name, customer_id in ACTIVE_CLIENTS.items():
        log(f"Fetching data for {client_name} ({customer_id})...")

        try:
            current_week_data = fetch_client_performance(
                ads_client, customer_id, current_week_start, current_week_end
            )
            prev_week_data = fetch_client_performance(
                ads_client, customer_id, prev_week_start, prev_week_end
            )

            analysis = analyze_performance(current_week_data, prev_week_data, client_name)

            if analysis:
                results.append(analysis)
                log(f"  ✓ {client_name}: {analysis['summary'][:80]}...")

        except Exception as e:
            log(f"  ✗ Error processing {client_name}: {e}")

    # Sort by revenue (highest first)
    results.sort(key=lambda x: x['current_week']['revenue'], reverse=True)

    # Create output
    output = {
        'generated_at': datetime.now().isoformat(),
        'period': {
            'current_week': {
                'start': current_week_start.isoformat(),
                'end': current_week_end.isoformat()
            },
            'previous_week': {
                'start': prev_week_start.isoformat(),
                'end': prev_week_end.isoformat()
            }
        },
        'clients': results
    }

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save to JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    log(f"\n✅ Performance data saved to {OUTPUT_FILE}")
    log(f"   Processed {len(results)} clients")
    log("=" * 60)

    return 0

if __name__ == '__main__':
    sys.exit(main())
