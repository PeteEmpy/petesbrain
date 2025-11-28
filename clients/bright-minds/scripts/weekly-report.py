#!/usr/bin/env python3
"""
Weekly Google Ads Report Generator for Bright Minds

Generates Monday morning performance reports for Barry and Sharon.
Compares previous week to:
- Last 3-4 weeks (trend analysis)
- Same week last year (YoY comparison)
- ROAS target (£4.00 goal)

Usage:
    python3 weekly-report.py [--week-offset N]

Options:
    --week-offset N    Report on week N weeks ago (default: 0 = last complete week)
"""

import sys
import os
from datetime import datetime, timedelta
import json

# Add shared scripts directory to path for MCP access
sys.path.append('/Users/administrator/Documents/PetesBrain/shared/scripts')

ACCOUNT_ID = "1404868570"
TARGET_ROAS = 4.00
RESTRUCTURE_DATE = datetime(2025, 10, 8)


def get_week_dates(weeks_ago=0):
    """Get start and end dates for a complete week (Mon-Sun)"""
    today = datetime.now().date()

    # Find the most recent Sunday (end of last complete week)
    days_since_sunday = (today.weekday() + 1) % 7
    if days_since_sunday == 0 and datetime.now().hour < 12:
        # If it's Sunday morning, use the previous week
        days_since_sunday = 7

    last_sunday = today - timedelta(days=days_since_sunday)

    # Calculate the week we want
    target_sunday = last_sunday - timedelta(weeks=weeks_ago)
    target_monday = target_sunday - timedelta(days=6)

    return target_monday, target_sunday


def format_date_gaql(date):
    """Format date for GAQL query (YYYY-MM-DD)"""
    return date.strftime('%Y-%m-%d')


def format_date_display(date):
    """Format date for display (Mon DD)"""
    return date.strftime('%b %d')


def query_google_ads(start_date, end_date):
    """Query Google Ads for week performance"""
    # This is a placeholder - in actual implementation, you would use the MCP Google Ads API
    # For now, return sample structure
    query = f"""
    SELECT
        metrics.conversions_value,
        metrics.cost_micros,
        metrics.conversions,
        metrics.clicks,
        metrics.impressions
    FROM customer
    WHERE segments.date BETWEEN '{format_date_gaql(start_date)}' AND '{format_date_gaql(end_date)}'
    """

    print(f"GAQL Query for {start_date} to {end_date}:")
    print(query)
    print()

    # TODO: Execute via MCP
    # For now, return placeholder
    return {
        'conversion_value': 0,
        'cost': 0,
        'roas': 0,
        'conversions': 0,
        'clicks': 0,
        'impressions': 0
    }


def calculate_metrics(data):
    """Calculate key metrics from raw data"""
    cost = data['cost'] / 1_000_000  # Convert from micros
    conversion_value = data['conversion_value']

    roas = (conversion_value / cost) if cost > 0 else 0

    return {
        'conversion_value': conversion_value,
        'cost': cost,
        'roas': roas,
        'conversions': data['conversions'],
        'clicks': data['clicks'],
        'impressions': data['impressions']
    }


def format_currency(value):
    """Format value as GBP currency"""
    return f"£{value:,.2f}"


def format_percent(value):
    """Format value as percentage"""
    return f"{value:+.1f}%"


def generate_report(week_offset=0):
    """Generate weekly report"""
    # Get date ranges
    current_week_start, current_week_end = get_week_dates(week_offset)

    # Previous 3 weeks for trend analysis
    week_ranges = []
    for i in range(4):
        start, end = get_week_dates(week_offset + i)
        week_ranges.append((start, end))

    # Same week last year
    lly_start = current_week_start - timedelta(days=365)
    lly_end = current_week_end - timedelta(days=365)

    print("=" * 70)
    print(f"BRIGHT MINDS - WEEKLY GOOGLE ADS REPORT")
    print(f"Week of {format_date_display(current_week_start)} - {format_date_display(current_week_end)}")
    print("=" * 70)
    print()

    print("DATE RANGES:")
    print(f"  Current Week:  {format_date_gaql(current_week_start)} to {format_date_gaql(current_week_end)}")
    print(f"  Last Year:     {format_date_gaql(lly_start)} to {format_date_gaql(lly_end)}")
    print()

    print("QUERIES TO RUN:")
    print()

    # Query for each week
    for i, (start, end) in enumerate(week_ranges):
        label = "CURRENT WEEK" if i == 0 else f"WEEK -{i}"
        print(f"{label}: {format_date_gaql(start)} to {format_date_gaql(end)}")
        data = query_google_ads(start, end)

    print(f"LAST YEAR SAME WEEK: {format_date_gaql(lly_start)} to {format_date_gaql(lly_end)}")
    lly_data = query_google_ads(lly_start, lly_end)

    print()
    print("=" * 70)
    print("EMAIL TEMPLATE:")
    print("=" * 70)
    print()

    email_template = f"""
Subject: Bright Minds - Weekly Google Ads Update ({format_date_display(current_week_start)} - {format_date_display(current_week_end)})

Hi Barry and Sharon,

Here's your weekly Google Ads performance update for the week ending {format_date_display(current_week_end)}.

📊 WEEK SUMMARY ({format_date_display(current_week_start)} - {format_date_display(current_week_end)})

Revenue:     [CONVERSION_VALUE]
Ad Spend:    [COST]
ROAS:        [ROAS] (target: £{TARGET_ROAS:.2f})
Conversions: [CONVERSIONS]

📈 TREND ANALYSIS (Last 4 Weeks)

Week ending {format_date_display(week_ranges[0][1])}: [ROAS_0]
Week ending {format_date_display(week_ranges[1][1])}: [ROAS_1]
Week ending {format_date_display(week_ranges[2][1])}: [ROAS_2]
Week ending {format_date_display(week_ranges[3][1])}: [ROAS_3]

[TREND_COMMENTARY]

📅 YEAR-OVER-YEAR COMPARISON

Same week last year ({format_date_display(lly_start)} - {format_date_display(lly_end)}):
Revenue:  [LLY_REVENUE]
ROAS:     [LLY_ROAS]

Year-over-year change:
Revenue:  [YOY_REVENUE_CHANGE]
ROAS:     [YOY_ROAS_CHANGE]

[YOY_COMMENTARY]

🎄 CHRISTMAS TRAJECTORY

[CHRISTMAS_ANALYSIS]

💡 KEY INSIGHTS

[INSIGHTS]

Let me know if you have any questions!

Best regards,
Peter

---
Peter Empson | Rok Systems
petere@roksys.co.uk | 07932 454652
"""

    print(email_template)

    print()
    print("=" * 70)
    print("TO COMPLETE THIS REPORT:")
    print("=" * 70)
    print()
    print("1. Run the GAQL queries above via MCP Google Ads API")
    print("2. Fill in the bracketed placeholders with actual data")
    print("3. Write trend commentary comparing the 4 weeks")
    print("4. Write YoY commentary explaining the comparison")
    print("5. Analyze Christmas trajectory based on current performance")
    print("6. Add 2-3 key insights or recommendations")
    print()
    print("REMEMBER:")
    print("- Client is cautious due to previous agency experience")
    print("- Emphasize positive trends and ROI (£ back per £1 spent)")
    print("- Explain any anomalies with context")
    print("- Reassure about ROAS progression toward £4.00 target")
    print("- Reference Christmas seasonality for educational toys")
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Bright Minds weekly report")
    parser.add_argument('--week-offset', type=int, default=0,
                       help='Report on week N weeks ago (default: 0 = last complete week)')

    args = parser.parse_args()

    generate_report(week_offset=args.week_offset)
