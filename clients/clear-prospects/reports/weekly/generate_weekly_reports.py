#!/usr/bin/env python3
"""
Clear Prospects Multi-Brand Weekly Report Generator
Generates separate weekly reports for HSG, WBS, and BMPM brands
"""

import json
from datetime import datetime
from pathlib import Path

# Report period
PERIOD_START = "2025-11-16"
PERIOD_END = "2025-11-23"
PREV_PERIOD_START = "2025-11-09"
PREV_PERIOD_END = "2025-11-15"
REPORT_DATE = "2025-11-25"

# Brand configurations
BRANDS = {
    'hsg': {
        'name': 'HappySnapGifts',
        'short_name': 'HSG',
        'campaign_prefix': 'CPL | HSG |',
        'merchant_centre_id': '7481296',
        'website': 'https://happysnapgifts.co.uk/',
        'target_roas': 115,
        'color': '#FF6B6B'
    },
    'wbs': {
        'name': 'WheatyBags',
        'short_name': 'WBS',
        'campaign_prefix': 'CPL | WBS |',
        'merchant_centre_id': '7481286',
        'website': 'https://wheatybags.co.uk/',
        'target_roas': 130,
        'color': '#4ECDC4'
    },
    'bmpm': {
        'name': 'British Made Promotional Merchandise',
        'short_name': 'BMPM',
        'campaign_prefix': 'CPL | BMPM |',
        'merchant_centre_id': '7522326',
        'website': 'https://bmpm.trade/',
        'target_roas': 70,
        'color': '#95E1D3'
    }
}

def micros_to_pounds(micros):
    """Convert micros to pounds"""
    return float(micros) / 1_000_000

def calculate_roas(conv_value, cost):
    """Calculate ROAS as percentage"""
    if cost == 0:
        return 0
    return (conv_value / cost) * 100

def calculate_cpa(cost, conversions):
    """Calculate cost per acquisition"""
    if conversions == 0:
        return 0
    return cost / conversions

def percent_change(current, previous):
    """Calculate percentage change"""
    if previous == 0:
        return 0 if current == 0 else 100
    return ((current - previous) / previous) * 100

def generate_brand_report_markdown(brand_key, this_week_campaigns, last_week_campaigns, this_week_products=None):
    """Generate markdown report for a specific brand"""

    brand = BRANDS[brand_key]

    # Calculate totals for this week (only ENABLED campaigns)
    enabled_campaigns_this = [c for c in this_week_campaigns if c['campaign']['status'] == 'ENABLED']
    enabled_campaigns_last = [c for c in last_week_campaigns if c['campaign']['status'] == 'ENABLED']

    this_cost = sum(micros_to_pounds(c['metrics']['costMicros']) for c in enabled_campaigns_this)
    this_convs = sum(float(c['metrics']['conversions']) for c in enabled_campaigns_this)
    this_conv_value = sum(float(c['metrics']['conversionsValue']) for c in enabled_campaigns_this)
    this_clicks = sum(int(c['metrics']['clicks']) for c in enabled_campaigns_this)
    this_imps = sum(int(c['metrics']['impressions']) for c in enabled_campaigns_this)

    last_cost = sum(micros_to_pounds(c['metrics']['costMicros']) for c in enabled_campaigns_last)
    last_convs = sum(float(c['metrics']['conversions']) for c in enabled_campaigns_last)
    last_conv_value = sum(float(c['metrics']['conversionsValue']) for c in enabled_campaigns_last)
    last_clicks = sum(int(c['metrics']['clicks']) for c in enabled_campaigns_last)
    last_imps = sum(int(c['metrics']['impressions']) for c in enabled_campaigns_last)

    this_roas = calculate_roas(this_conv_value, this_cost)
    last_roas = calculate_roas(last_conv_value, last_cost)

    this_cpa = calculate_cpa(this_cost, this_convs)
    last_cpa = calculate_cpa(last_cost, last_convs)

    this_ctr = (this_clicks / this_imps * 100) if this_imps > 0 else 0
    last_ctr = (last_clicks / last_imps * 100) if last_imps > 0 else 0

    this_cpc = (this_cost / this_clicks) if this_clicks > 0 else 0
    last_cpc = (last_cost / last_clicks) if last_clicks > 0 else 0

    # Build markdown
    md = f"""# Google Ads Weekly Report: {brand['name']}

**Period:** {PERIOD_START} - {PERIOD_END}
**Website:** {brand['website']}
**Generated:** {REPORT_DATE}

---

## Executive Summary

### Account Performance ({brand['short_name']})

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Spend | £{this_cost:,.2f} | £{last_cost:,.2f} | {percent_change(this_cost, last_cost):+.1f}% |
| Conversions | {this_convs:.1f} | {last_convs:.1f} | {percent_change(this_convs, last_convs):+.1f}% |
| Conv Value | £{this_conv_value:,.2f} | £{last_conv_value:,.2f} | {percent_change(this_conv_value, last_conv_value):+.1f}% |
| ROAS | {this_roas:.0f}% | {last_roas:.0f}% | {(this_roas - last_roas):+.0f}pp |
| CPA | £{this_cpa:.2f} | £{last_cpa:.2f} | {percent_change(this_cpa, last_cpa):+.1f}% |
| CTR | {this_ctr:.2f}% | {last_ctr:.2f}% | {(this_ctr - last_ctr):+.2f}pp |
| Avg CPC | £{this_cpc:.2f} | £{last_cpc:.2f}% | {percent_change(this_cpc, last_cpc):+.1f}% |

**Key Takeaway:** """

    # Add key takeaway based on performance
    if this_roas >= brand['target_roas']:
        md += f"{brand['short_name']} achieved {this_roas:.0f}% ROAS (target: {brand['target_roas']}%), performing {(this_roas - brand['target_roas']):.0f}pp above target with {this_convs:.0f} conversions."
    else:
        md += f"{brand['short_name']} delivered {this_roas:.0f}% ROAS, {(brand['target_roas'] - this_roas):.0f}pp below target of {brand['target_roas']}%, with {this_convs:.0f} conversions."

    md += "\n\n---\n\n## Campaign Breakdown\n\n### Active Campaigns\n\n"

    # Sort campaigns by spend
    campaigns_sorted = sorted(enabled_campaigns_this, key=lambda x: int(x['metrics']['costMicros']), reverse=True)

    for camp in campaigns_sorted[:5]:  # Top 5 campaigns
        camp_cost = micros_to_pounds(camp['metrics']['costMicros'])
        camp_convs = float(camp['metrics']['conversions'])
        camp_value = float(camp['metrics']['conversionsValue'])
        camp_roas = calculate_roas(camp_value, camp_cost)
        camp_cpa = calculate_cpa(camp_cost, camp_convs)

        md += f"**{camp['campaign']['name']}**\n"
        md += f"- Spend: £{camp_cost:,.2f} | Conversions: {camp_convs:.1f} | ROAS: {camp_roas:.0f}% | CPA: £{camp_cpa:.2f}\n\n"

    md += "---\n\n## Recommendations\n\n"

    # Add brand-specific recommendations
    recommendations = generate_recommendations(brand_key, this_roas, brand['target_roas'], this_cost, this_convs, enabled_campaigns_this)

    for i, rec in enumerate(recommendations, 1):
        md += f"### {i}. {rec['title']} [{rec['priority']}]\n\n"
        md += f"{rec['description']}\n\n"
        md += f"**Impact:** {rec['impact']}\n\n"

    md += "---\n\n**Next Review:** 2025-12-02\n"

    return md

def generate_recommendations(brand_key, roas, target_roas, spend, conversions, campaigns):
    """Generate prioritised recommendations for a brand"""
    recs = []

    # Check if ROAS is below target
    if roas < target_roas:
        roas_gap = target_roas - roas
        recs.append({
            'priority': 'P0',
            'title': f'ROAS Below Target ({roas:.0f}% vs {target_roas}% target)',
            'description': f'Current ROAS is {roas_gap:.0f}pp below the {target_roas}% target. Review campaign settings, bidding strategies, and product segmentation to improve efficiency.',
            'impact': f'Closing the ROAS gap could improve profitability by {roas_gap:.0f}pp'
        })

    # Check for campaigns with zero conversions
    zero_conv_campaigns = [c for c in campaigns if float(c['metrics']['conversions']) == 0 and micros_to_pounds(c['metrics']['costMicros']) > 50]
    if zero_conv_campaigns:
        total_waste = sum(micros_to_pounds(c['metrics']['costMicros']) for c in zero_conv_campaigns)
        recs.append({
            'priority': 'P0',
            'title': f'{len(zero_conv_campaigns)} Campaign(s) with Zero Conversions',
            'description': f'Campaigns spending £{total_waste:.2f} this week without generating conversions. Consider pausing or restructuring.',
            'impact': f'Potential saving: £{total_waste:.2f}/week = £{total_waste * 52:.2f}/year'
        })

    # Check average CPA
    if conversions > 0:
        avg_cpa = spend / conversions
        if avg_cpa > 15:
            recs.append({
                'priority': 'P1',
                'title': f'High CPA (£{avg_cpa:.2f})',
                'description': f'Average CPA of £{avg_cpa:.2f} exceeds recommended threshold of £15. Review bidding strategies and audience targeting.',
                'impact': 'Reducing CPA to £15 would improve account efficiency'
            })

    return recs

# This script will be called with the actual data
# For now, it provides the structure

if __name__ == "__main__":
    print("Clear Prospects Weekly Report Generator")
    print("This script provides the framework for generating multi-brand reports.")
    print("Run with actual GAQL data to generate reports.")
