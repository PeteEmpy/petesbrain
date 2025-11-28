#!/usr/bin/env python3
"""
AI Max Impact Analysis for Devonshire Hotels
Analyzes the impact of AI Max implementation on August 5th, 2025

Campaigns analyzed:
1. Chatsworth Escapes Self Catering (AI Max added 8/5)
2. Chatsworth Escapes Locations (AI Max added 8/5)
"""

import json
from datetime import datetime

# Pre-AI Max data (June 1 - August 4, 2025) from Google Ads API
# This data was queried and shows the baseline performance

def calculate_campaign_metrics(data, campaign_name, date_range):
    """Calculate aggregated metrics for a campaign in a date range"""
    metrics = {
        'impressions': 0,
        'clicks': 0,
        'cost': 0,
        'conversions': 0,
        'conv_value': 0,
        'days': 0
    }

    for row in data:
        if campaign_name in row['campaign']['name']:
            metrics['impressions'] += int(row['metrics']['impressions'])
            metrics['clicks'] += int(row['metrics']['clicks'])
            metrics['cost'] += int(row['metrics']['costMicros']) / 1_000_000
            metrics['conversions'] += float(row['metrics'].get('conversionsByConversionDate', 0))
            metrics['conv_value'] += float(row['metrics'].get('conversionsValueByConversionDate', 0))
            metrics['days'] += 1

    # Calculate derived metrics
    if metrics['impressions'] > 0:
        metrics['ctr'] = (metrics['clicks'] / metrics['impressions']) * 100
    else:
        metrics['ctr'] = 0

    if metrics['clicks'] > 0:
        metrics['cpc'] = metrics['cost'] / metrics['clicks']
    else:
        metrics['cpc'] = 0

    if metrics['cost'] > 0:
        metrics['roas'] = (metrics['conv_value'] / metrics['cost']) * 100
    else:
        metrics['roas'] = 0

    if metrics['conversions'] > 0:
        metrics['cpa'] = metrics['cost'] / metrics['conversions']
    else:
        metrics['cpa'] = 0

    # Daily averages
    if metrics['days'] > 0:
        metrics['daily_impressions'] = metrics['impressions'] / metrics['days']
        metrics['daily_clicks'] = metrics['clicks'] / metrics['days']
        metrics['daily_cost'] = metrics['cost'] / metrics['days']
        metrics['daily_conversions'] = metrics['conversions'] / metrics['days']

    return metrics


def format_metrics_summary(metrics, period_name):
    """Format metrics into a readable summary"""
    return f"""
{period_name}:
- Period: {metrics['days']} days
- Impressions: {metrics['impressions']:,} (avg {metrics['daily_impressions']:.0f}/day)
- Clicks: {metrics['clicks']:,} (avg {metrics['daily_clicks']:.1f}/day)
- CTR: {metrics['ctr']:.2f}%
- Cost: £{metrics['cost']:,.2f} (avg £{metrics['daily_cost']:.2f}/day)
- CPC: £{metrics['cpc']:.2f}
- Conversions: {metrics['conversions']:.1f} (avg {metrics['daily_conversions']:.2f}/day)
- Conv Value: £{metrics['conv_value']:,.2f}
- ROAS: {metrics['roas']:.0f}%
- CPA: £{metrics['cpa']:.2f}
"""


def calculate_change(before, after, metric):
    """Calculate percentage change between before and after"""
    if before[metric] == 0:
        return None
    return ((after[metric] - before[metric]) / before[metric]) * 100


def main():
    print("="*80)
    print("AI MAX IMPACT ANALYSIS - DEVONSHIRE HOTELS")
    print("="*80)
    print()
    print("RESEARCH QUESTION:")
    print("Can we prove there's been any impact of adding AI Max to the")
    print("Chatsworth Escapes campaigns on August 5th, 2025?")
    print()
    print("="*80)

    # Load the pre-AI Max data from the JSON response
    # This would be populated from the Google Ads API query
    # For now, we'll need to manually calculate from the query results

    print("\nNOTE: This script needs to be run with actual data from Google Ads API")
    print("Run the following queries:")
    print()
    print("1. PRE-AI MAX (June 1 - August 4, 2025):")
    print("   - Baseline performance without AI Max")
    print()
    print("2. POST-AI MAX (August 5 - November 6, 2025):")
    print("   - Performance with AI Max enabled")
    print()
    print("Campaigns to analyze:")
    print("  1. DEV | Properties CE | Chatsworth Escapes Self Catering")
    print("  2. DEV | Properties | Chatsworth Escapes Locations")
    print()
    print("="*80)


if __name__ == "__main__":
    main()
