"""
Example: Using Calculated Metrics in Weekly Google Ads Reports

This demonstrates how to integrate the calculated_metrics module
into the google-ads-weekly-report skill.

Shows:
- Safe metric calculation with division-by-zero handling
- Context addition (vs target, vs previous)
- Proper aggregation (account-level from campaign totals)
- Formatting for display

Usage in skill:
    from shared.weekly_report_example import process_weekly_report_data

Author: PetesBrain
Created: 2025-12-14
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Import the calculated metrics module
sys.path.insert(0, str(Path(__file__).parent))
from calculated_metrics import (
    process_campaign_metrics,
    aggregate_metrics,
    add_context,
    format_metric,
    format_metric_with_context,
    format_variance,
    convert_micros_to_currency
)


def process_weekly_report_data(current_data, previous_data, target_roas=None):
    """
    Complete workflow for weekly report data processing

    Args:
        current_data: List of campaign dicts from current week GAQL query
        previous_data: List of campaign dicts from previous week GAQL query
        target_roas: Target ROAS from client CONTEXT.md (e.g., 4.0 for 4.0x)

    Returns:
        dict: Fully processed report data with context and formatting
    """

    # Step 1: Process each current campaign with calculated metrics
    processed_campaigns = []

    for current_campaign in current_data:
        campaign_name = current_campaign['campaign']['name']

        # Find matching previous campaign
        previous_campaign = None
        for prev in previous_data:
            if prev['campaign']['name'] == campaign_name:
                previous_campaign = prev
                break

        # Process with calculated metrics
        # (handles micros conversion, calculation, context addition)
        metrics = process_campaign_metrics(
            raw_data=current_campaign['metrics'],
            target_roas=target_roas,
            previous_data=previous_campaign['metrics'] if previous_campaign else None
        )

        # Add campaign identification
        metrics['campaign_name'] = campaign_name
        metrics['campaign_id'] = current_campaign['campaign']['id']

        processed_campaigns.append(metrics)

    # Step 2: Calculate account-level totals (AGGREGATE FIRST!)
    account_current = aggregate_metrics(
        campaigns=processed_campaigns,
        cost_key='cost',
        revenue_key='revenue',
        conversions_key='conversions'
    )

    # Step 3: Calculate previous account totals
    account_previous = aggregate_metrics(
        campaigns=[{
            'cost': convert_micros_to_currency(p['metrics']['cost_micros']),
            'revenue': convert_micros_to_currency(p['metrics']['conversions_value_micros']),
            'conversions': p['metrics']['conversions']
        } for p in previous_data],
        cost_key='cost',
        revenue_key='revenue',
        conversions_key='conversions'
    )

    # Step 4: Add context to account metrics
    account_roas_context = add_context(
        current_metric=account_current['roas'],
        target=target_roas,
        previous=account_previous['roas']
    )

    account_cpa_context = add_context(
        current_metric=account_current['cpa'],
        previous=account_previous['cpa']
    )

    # Step 5: Return fully processed data
    return {
        'campaigns': processed_campaigns,
        'account': {
            'current': account_current,
            'previous': account_previous,
            'roas_context': account_roas_context,
            'cpa_context': account_cpa_context
        }
    }


def generate_executive_summary(report_data, client_name):
    """
    Generate executive summary section with formatted metrics

    Args:
        report_data: Output from process_weekly_report_data()
        client_name: Client name for display

    Returns:
        str: Formatted markdown executive summary
    """
    account = report_data['account']
    current = account['current']
    previous = account['previous']
    roas_ctx = account['roas_context']
    cpa_ctx = account['cpa_context']

    # Format current values
    current_spend = format_metric(current['total_cost'], 'currency')
    current_revenue = format_metric(current['total_revenue'], 'currency')
    current_conversions = format_metric(current['total_conversions'], 'integer')
    current_roas = format_metric(current['roas'], 'roas')
    current_cpa = format_metric(current['cpa'], 'currency')

    # Format previous values
    previous_spend = format_metric(previous['total_cost'], 'currency')
    previous_revenue = format_metric(previous['total_revenue'], 'currency')
    previous_conversions = format_metric(previous['total_conversions'], 'integer')
    previous_roas = format_metric(previous['roas'], 'roas')
    previous_cpa = format_metric(previous['cpa'], 'currency')

    # Calculate WoW changes
    spend_change = format_variance(roas_ctx['vs_previous']) if roas_ctx['vs_previous'] else 'N/A'
    roas_change = format_variance(roas_ctx['vs_previous']) if roas_ctx['vs_previous'] else 'N/A'
    conversions_change = format_variance(
        ((current['total_conversions'] - previous['total_conversions']) / previous['total_conversions'] * 100)
        if previous['total_conversions'] > 0 else None
    )
    cpa_change = format_variance(cpa_ctx['vs_previous']) if cpa_ctx['vs_previous'] else 'N/A'

    # Generate summary
    summary = f"""# Google Ads Weekly Report: {client_name}
**Period:** {datetime.now().strftime('%Y-%m-%d')}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## ✓ Executive Summary

### Account Performance

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| **Spend** | {current_spend} | {previous_spend} | {spend_change} |
| **Revenue** | {current_revenue} | {previous_revenue} | {spend_change} |
| **Conversions** | {current_conversions} | {previous_conversions} | {conversions_change} |
| **ROAS** | {current_roas} | {previous_roas} | {roas_change} |
| **CPA** | {current_cpa} | {previous_cpa} | {cpa_change} |

### ROAS Performance vs Target

{format_metric_with_context(roas_ctx, 'roas', 'ROAS')}

### Key Observations

"""

    # Add automatic insights based on variance
    if roas_ctx['vs_target'] is not None:
        if roas_ctx['vs_target'] >= 10:
            summary += f"✓ **Strong Performance**: ROAS is {abs(roas_ctx['vs_target']):.0f}% above target\n"
        elif roas_ctx['vs_target'] >= 0:
            summary += f"◆ **On Target**: ROAS slightly above target (+{abs(roas_ctx['vs_target']):.0f}%)\n"
        elif roas_ctx['vs_target'] >= -10:
            summary += f"◆ **Near Target**: ROAS slightly below target ({roas_ctx['vs_target']:.0f}%)\n"
        else:
            summary += f"⚠️ **Below Target**: ROAS is {abs(roas_ctx['vs_target']):.0f}% below target - requires attention\n"

    if roas_ctx['vs_previous'] is not None:
        if roas_ctx['vs_previous'] >= 10:
            summary += f"✓ **Improving**: ROAS up {abs(roas_ctx['vs_previous']):.0f}% vs last week\n"
        elif roas_ctx['vs_previous'] <= -10:
            summary += f"⚠️ **Declining**: ROAS down {abs(roas_ctx['vs_previous']):.0f}% vs last week\n"

    return summary


def generate_campaign_breakdown(report_data):
    """
    Generate campaign performance table with context

    Args:
        report_data: Output from process_weekly_report_data()

    Returns:
        str: Formatted markdown campaign table
    """
    campaigns = sorted(report_data['campaigns'], key=lambda x: x['cost'], reverse=True)

    breakdown = """
---

## ✓ Campaign Performance

| Campaign | Spend | ROAS | vs Target | vs Previous | Status |
|----------|-------|------|-----------|-------------|--------|
"""

    for campaign in campaigns:
        name = campaign['campaign_name']
        spend = format_metric(campaign['cost'], 'currency')
        roas = format_metric(campaign['roas']['value'], 'roas')

        # Format context
        vs_target = format_variance(campaign['roas']['vs_target']) if campaign['roas']['vs_target'] else '—'
        vs_previous = format_variance(campaign['roas']['vs_previous']) if campaign['roas']['vs_previous'] else '—'

        # Determine status
        if campaign['roas']['vs_target']:
            if campaign['roas']['vs_target'] >= 0:
                status = '✓'
            elif campaign['roas']['vs_target'] >= -10:
                status = '◆'
            else:
                status = '⚠️'
        else:
            status = '—'

        breakdown += f"| {name} | {spend} | {roas} | {vs_target} | {vs_previous} | {status} |\n"

    return breakdown


# Example usage demonstration
if __name__ == '__main__':
    print("=" * 60)
    print("CALCULATED METRICS - WEEKLY REPORT INTEGRATION")
    print("=" * 60 + "\n")

    # Simulate GAQL query results (with micros)
    current_week_raw = [
        {
            'campaign': {'name': 'Performance Max | UK', 'id': '123'},
            'metrics': {
                'cost_micros': 1200000000,  # £1,200
                'conversions_value_micros': 5400000000,  # £5,400
                'conversions': 28
            }
        },
        {
            'campaign': {'name': 'Brand Search | UK', 'id': '456'},
            'metrics': {
                'cost_micros': 800000000,  # £800
                'conversions_value_micros': 3200000000,  # £3,200
                'conversions': 24
            }
        },
        {
            'campaign': {'name': 'Shopping | UK', 'id': '789'},
            'metrics': {
                'cost_micros': 600000000,  # £600
                'conversions_value_micros': 1800000000,  # £1,800
                'conversions': 12
            }
        }
    ]

    previous_week_raw = [
        {
            'campaign': {'name': 'Performance Max | UK', 'id': '123'},
            'metrics': {
                'cost_micros': 1100000000,  # £1,100
                'conversions_value_micros': 4400000000,  # £4,400
                'conversions': 25
            }
        },
        {
            'campaign': {'name': 'Brand Search | UK', 'id': '456'},
            'metrics': {
                'cost_micros': 750000000,  # £750
                'conversions_value_micros': 3000000000,  # £3,000
                'conversions': 22
            }
        },
        {
            'campaign': {'name': 'Shopping | UK', 'id': '789'},
            'metrics': {
                'cost_micros': 550000000,  # £550
                'conversions_value_micros': 1650000000,  # £1,650
                'conversions': 11
            }
        }
    ]

    # Process data with calculated metrics
    report_data = process_weekly_report_data(
        current_data=current_week_raw,
        previous_data=previous_week_raw,
        target_roas=4.0  # From CONTEXT.md
    )

    # Generate report sections
    executive_summary = generate_executive_summary(report_data, client_name='Example Client')
    campaign_breakdown = generate_campaign_breakdown(report_data)

    # Display
    print(executive_summary)
    print(campaign_breakdown)

    print("\n" + "=" * 60)
    print("KEY BENEFITS OF CALCULATED METRICS:")
    print("=" * 60)
    print("✓ No division-by-zero errors (reports never crash)")
    print("✓ Proper aggregation (account ROAS calculated correctly)")
    print("✓ Context included (vs target, vs previous)")
    print("✓ Consistent formatting (N/A for missing data)")
    print("✓ Automatic variance indicators (✓ ◆ ⚠️)")
    print("\nThis data can now be handed to AI for Phase 2 analysis.")
