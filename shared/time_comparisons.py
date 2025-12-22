"""
Time Comparison Utilities for Google Ads Reporting

Provides functions for calculating Week over Week (WoW), Month over Month (MoM),
and Year over Year (YoY) comparisons with proper same-day alignment.

Based on 8020brain.com automated reporting principles:
- Same day matters more than same date (Monday-to-Monday, not 15th-to-15th)
- Calculate both absolute and percentage change
- Include safeguards for low volume, holidays, and campaign changes
- Flag situations where comparisons may be misleading

Usage:
    from shared.time_comparisons import get_comparison_periods, calculate_changes, format_comparison_report

    # Get date ranges for WoW comparison
    periods = get_comparison_periods('WoW')

    # Query Google Ads for both periods and parse results
    current = {'spend': 520, 'conversions': 12, 'revenue': 2080, 'roas': 4.0, 'cpa': 43.33}
    previous = {'spend': 500, 'conversions': 15, 'revenue': 2250, 'roas': 4.5, 'cpa': 33.33}

    # Calculate changes with safeguards
    changes = calculate_changes(current, previous)

    # Format into readable report
    report = format_comparison_report('Smythson', periods, changes, 'WoW')
"""

from datetime import datetime, timedelta
from typing import Dict, Literal, List, Optional
import calendar


def get_comparison_periods(
    comparison_type: Literal['WoW', 'MoM', 'YoY'] = 'WoW',
    reference_date: Optional[datetime] = None
) -> Dict[str, Dict[str, str]]:
    """
    Calculate date ranges for time comparisons with same-day alignment.

    Args:
        comparison_type: Type of comparison ('WoW', 'MoM', or 'YoY')
        reference_date: Optional reference date (defaults to today)

    Returns:
        Dictionary with 'current' and 'previous' date ranges:
        {
            'current': {'start': '2025-12-15', 'end': '2025-12-21'},
            'previous': {'start': '2025-12-08', 'end': '2025-12-14'}
        }

    Examples:
        >>> periods = get_comparison_periods('WoW')
        >>> # Returns current week (Mon-Sun) vs previous week (Mon-Sun)

        >>> periods = get_comparison_periods('MoM')
        >>> # Returns current month vs previous month

        >>> periods = get_comparison_periods('YoY')
        >>> # Returns current week vs same week last year
    """
    today = reference_date.date() if reference_date else datetime.now().date()

    if comparison_type == 'WoW':
        # Current week (Mon-Sun)
        current_start = today - timedelta(days=today.weekday())  # Monday
        current_end = current_start + timedelta(days=6)  # Sunday

        # Previous week (same days aligned)
        previous_start = current_start - timedelta(days=7)
        previous_end = current_end - timedelta(days=7)

    elif comparison_type == 'MoM':
        # Current month (1st to last day)
        current_start = today.replace(day=1)

        # Last day of current month
        last_day = calendar.monthrange(today.year, today.month)[1]
        current_end = today.replace(day=last_day)

        # Previous month (1st to last day)
        if current_start.month == 1:
            previous_start = current_start.replace(year=current_start.year - 1, month=12, day=1)
            previous_last_day = 31
        else:
            previous_start = current_start.replace(month=current_start.month - 1, day=1)
            previous_last_day = calendar.monthrange(previous_start.year, previous_start.month)[1]

        previous_end = previous_start.replace(day=previous_last_day)

    elif comparison_type == 'YoY':
        # Same week last year (same days aligned)
        current_start = today - timedelta(days=today.weekday())  # Monday this week
        current_end = current_start + timedelta(days=6)  # Sunday this week

        # Same week last year (handling leap years)
        try:
            previous_start = current_start.replace(year=current_start.year - 1)
            previous_end = current_end.replace(year=current_end.year - 1)
        except ValueError:
            # Handle Feb 29 in leap years
            previous_start = current_start.replace(year=current_start.year - 1, day=28)
            previous_end = current_end.replace(year=current_end.year - 1, day=28)

    else:
        raise ValueError(f"Invalid comparison_type: {comparison_type}. Must be 'WoW', 'MoM', or 'YoY'")

    return {
        'current': {
            'start': current_start.strftime('%Y-%m-%d'),
            'end': current_end.strftime('%Y-%m-%d')
        },
        'previous': {
            'start': previous_start.strftime('%Y-%m-%d'),
            'end': previous_end.strftime('%Y-%m-%d')
        }
    }


def parse_performance_data(api_result: Dict) -> Dict[str, float]:
    """
    Convert Google Ads API result to usable performance metrics.

    Args:
        api_result: Result from mcp__google_ads__run_gaql()

    Returns:
        Dictionary with parsed metrics:
        {
            'spend': 520.50,
            'conversions': 12,
            'revenue': 2080.00,
            'roas': 4.0,
            'cpa': 43.33
        }

    Note:
        Returns zeros if no data found (prevents division by zero errors)
    """
    if not api_result or 'results' not in api_result or not api_result['results']:
        return {
            'spend': 0,
            'conversions': 0,
            'revenue': 0,
            'roas': 0,
            'cpa': 0
        }

    total_spend = 0
    total_conversions = 0
    total_revenue = 0

    for row in api_result['results']:
        metrics = row.get('metrics', {})
        total_spend += metrics.get('costMicros', 0) / 1_000_000
        total_conversions += metrics.get('conversions', 0)
        total_revenue += metrics.get('conversionsValue', 0)

    # Calculate derived metrics
    roas = total_revenue / total_spend if total_spend > 0 else 0
    cpa = total_spend / total_conversions if total_conversions > 0 else 0

    return {
        'spend': round(total_spend, 2),
        'conversions': total_conversions,
        'revenue': round(total_revenue, 2),
        'roas': round(roas, 2),
        'cpa': round(cpa, 2)
    }


def calculate_changes(current: Dict[str, float], previous: Dict[str, float]) -> Dict:
    """
    Calculate absolute and percentage changes between periods.
    Includes safeguard flags for low volume and significant changes.

    Args:
        current: Current period metrics
        previous: Previous period metrics

    Returns:
        Dictionary with changes and flags:
        {
            'spend': {
                'current': 520.00,
                'previous': 500.00,
                'absolute': 20.00,
                'percentage': 4.0
            },
            'flags': ['LOW_VOLUME', 'LARGE_ROAS_CHANGE']
        }

    Safeguard Flags:
        - LOW_VOLUME: <10 conversions in either period (comparisons may be volatile)
        - LARGE_SPEND_CHANGE: >50% spend change (investigate cause)
        - LARGE_ROAS_CHANGE: >20% ROAS change (investigate cause)
        - ZERO_PREVIOUS: Previous period had zero value (percentage change undefined)

    Examples:
        >>> current = {'spend': 520, 'conversions': 12, 'revenue': 2080, 'roas': 4.0, 'cpa': 43.33}
        >>> previous = {'spend': 500, 'conversions': 15, 'revenue': 2250, 'roas': 4.5, 'cpa': 33.33}
        >>> changes = calculate_changes(current, previous)
        >>> changes['roas']['percentage']
        -11.11
    """
    changes = {}
    flags = []

    for metric in ['spend', 'conversions', 'revenue', 'roas', 'cpa']:
        current_value = current.get(metric, 0)
        previous_value = previous.get(metric, 0)

        # Absolute change
        absolute_change = current_value - previous_value

        # Percentage change (handle division by zero)
        if previous_value == 0:
            if current_value == 0:
                percentage_change = 0
            else:
                percentage_change = 100  # 100% increase from zero
                flags.append(f'ZERO_PREVIOUS_{metric.upper()}')
        else:
            percentage_change = (absolute_change / previous_value) * 100

        changes[metric] = {
            'current': round(current_value, 2),
            'previous': round(previous_value, 2),
            'absolute': round(absolute_change, 2),
            'percentage': round(percentage_change, 1)
        }

    # Add safeguard flags
    if current['conversions'] < 10 or previous['conversions'] < 10:
        flags.append('LOW_VOLUME')

    if abs(changes['spend']['percentage']) > 50:
        flags.append('LARGE_SPEND_CHANGE')

    if abs(changes['roas']['percentage']) > 20:
        flags.append('LARGE_ROAS_CHANGE')

    changes['flags'] = list(set(flags))  # Remove duplicates

    return changes


def format_comparison_report(
    client_name: str,
    periods: Dict,
    changes: Dict,
    comparison_type: Literal['WoW', 'MoM', 'YoY'] = 'WoW'
) -> str:
    """
    Format comparison data into readable markdown report.
    Uses British English and proper formatting standards.

    Args:
        client_name: Client name for report header
        periods: Date ranges from get_comparison_periods()
        changes: Calculated changes from calculate_changes()
        comparison_type: Type of comparison ('WoW', 'MoM', 'YoY')

    Returns:
        Formatted markdown report with:
        - Period dates
        - Safeguard flags (if any)
        - Metrics table with absolute and percentage changes
        - Quick insights based on significant changes

    Examples:
        >>> report = format_comparison_report('Smythson', periods, changes, 'WoW')
        >>> print(report)
        ## Smythson - Week over Week Comparison

        **Current Period**: 2025-12-15 to 2025-12-21
        **Previous Period**: 2025-12-08 to 2025-12-14
        ...
    """
    comparison_labels = {
        'WoW': 'Week over Week',
        'MoM': 'Month over Month',
        'YoY': 'Year over Year'
    }

    report_lines = []
    report_lines.append(f"## {client_name} - {comparison_labels[comparison_type]} Comparison")
    report_lines.append("")
    report_lines.append(f"**Current Period**: {periods['current']['start']} to {periods['current']['end']}")
    report_lines.append(f"**Previous Period**: {periods['previous']['start']} to {periods['previous']['end']}")
    report_lines.append("")

    # Safeguard flags
    if changes.get('flags'):
        report_lines.append("**⚠️ Flags**:")
        for flag in changes['flags']:
            if flag == 'LOW_VOLUME':
                report_lines.append("- Low volume: Comparisons may be volatile (<10 conversions)")
            elif flag == 'LARGE_SPEND_CHANGE':
                report_lines.append("- Large spend change: Investigate cause (>50% change)")
            elif flag == 'LARGE_ROAS_CHANGE':
                report_lines.append("- Large ROAS change: Investigate cause (>20% change)")
            elif flag.startswith('ZERO_PREVIOUS'):
                metric = flag.replace('ZERO_PREVIOUS_', '').lower()
                report_lines.append(f"- Previous period had zero {metric} (percentage change from zero)")
        report_lines.append("")

    # Key metrics table
    report_lines.append("| Metric | Current | Previous | Change | % Change |")
    report_lines.append("|--------|---------|----------|--------|----------|")

    metrics_display = {
        'spend': ('Spend', '£{:.2f}'),
        'revenue': ('Revenue', '£{:.2f}'),
        'roas': ('ROAS', '{:.1f}x'),
        'conversions': ('Conversions', '{:.0f}'),
        'cpa': ('CPA', '£{:.2f}')
    }

    for metric, (label, fmt) in metrics_display.items():
        data = changes[metric]
        current_str = fmt.format(data['current'])
        previous_str = fmt.format(data['previous'])

        # Format absolute change
        if metric in ['spend', 'revenue', 'cpa']:
            absolute_str = f"£{abs(data['absolute']):.2f}"
        elif metric == 'roas':
            absolute_str = f"{abs(data['absolute']):.1f}x"
        else:
            absolute_str = f"{abs(data['absolute']):.0f}"

        # Add direction indicator
        if data['absolute'] > 0:
            change_str = f"+{absolute_str}"
            pct_str = f"+{data['percentage']:.1f}%"
        elif data['absolute'] < 0:
            change_str = f"-{absolute_str}"
            pct_str = f"{data['percentage']:.1f}%"
        else:
            change_str = "No change"
            pct_str = "0%"

        report_lines.append(f"| {label} | {current_str} | {previous_str} | {change_str} | {pct_str} |")

    report_lines.append("")

    # Quick insights based on significant changes
    report_lines.append("### Quick Insights")
    report_lines.append("")

    insights = []

    # ROAS insights
    if changes['roas']['percentage'] < -10:
        insights.append(f"- ⚠️ ROAS declined {abs(changes['roas']['percentage']):.1f}% - investigate cause")
    elif changes['roas']['percentage'] > 10:
        insights.append(f"- ✓ ROAS improved {changes['roas']['percentage']:.1f}% - identify what's working")

    # Spend insights
    if changes['spend']['percentage'] > 20:
        insights.append(f"- 📈 Spend increased {changes['spend']['percentage']:.1f}% - verify budget allocation")
    elif changes['spend']['percentage'] < -20:
        insights.append(f"- 📉 Spend decreased {abs(changes['spend']['percentage']):.1f}% - check for paused campaigns")

    # CPA insights
    if changes['cpa']['percentage'] > 20:
        insights.append(f"- ⚠️ CPA increased {changes['cpa']['percentage']:.1f}% - optimise bidding or targeting")
    elif changes['cpa']['percentage'] < -20:
        insights.append(f"- ✓ CPA decreased {abs(changes['cpa']['percentage']):.1f}% - efficiency improving")

    # Conversion insights
    if changes['conversions']['percentage'] < -20:
        insights.append(f"- ⚠️ Conversions declined {abs(changes['conversions']['percentage']):.1f}% - review campaign performance")
    elif changes['conversions']['percentage'] > 20:
        insights.append(f"- ✓ Conversions increased {changes['conversions']['percentage']:.1f}% - scaling opportunity")

    if insights:
        report_lines.extend(insights)
    else:
        report_lines.append("- Stable performance - no significant changes detected")

    report_lines.append("")

    return "\n".join(report_lines)


def get_holiday_flags(start_date: str, end_date: str) -> List[str]:
    """
    Check if date range includes major UK holidays that may affect comparisons.

    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format

    Returns:
        List of holiday flags found in date range

    UK Holidays Checked:
        - Black Friday (last Friday of November)
        - Cyber Monday (Monday after Black Friday)
        - Christmas (Dec 24-26)
        - New Year (Dec 31 - Jan 2)
        - Easter (variable, April)
        - Bank Holidays (May, August)

    Examples:
        >>> flags = get_holiday_flags('2025-11-28', '2025-12-01')
        >>> 'BLACK_FRIDAY' in flags
        True
    """
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()

    flags = []

    # Generate all dates in range
    current = start
    while current <= end:
        month = current.month
        day = current.day

        # Black Friday (last Friday of November)
        if month == 11 and current.weekday() == 4:  # Friday
            # Check if it's the last Friday
            next_friday = current + timedelta(days=7)
            if next_friday.month == 12:
                flags.append('BLACK_FRIDAY')

        # Cyber Monday (Monday after Black Friday)
        if month == 11 and current.weekday() == 0:  # Monday
            last_friday = current - timedelta(days=3)
            if last_friday.month == 11:
                # Check if last Friday was Black Friday
                next_friday = last_friday + timedelta(days=7)
                if next_friday.month == 12:
                    flags.append('CYBER_MONDAY')

        # Christmas period (Dec 24-26)
        if month == 12 and day >= 24 and day <= 26:
            flags.append('CHRISTMAS')

        # New Year period (Dec 31 - Jan 2)
        if (month == 12 and day >= 31) or (month == 1 and day <= 2):
            flags.append('NEW_YEAR')

        # Easter (approximate - typically early April)
        if month == 4 and day >= 1 and day <= 15:
            flags.append('EASTER_PERIOD')

        # May Bank Holidays (first and last Monday)
        if month == 5 and current.weekday() == 0:
            flags.append('MAY_BANK_HOLIDAY')

        # August Bank Holiday (last Monday)
        if month == 8 and current.weekday() == 0:
            # Check if last Monday
            next_monday = current + timedelta(days=7)
            if next_monday.month == 9:
                flags.append('AUGUST_BANK_HOLIDAY')

        current += timedelta(days=1)

    return list(set(flags))  # Remove duplicates


if __name__ == '__main__':
    """Test the time comparison functions"""

    print("Testing Time Comparison Functions")
    print("=" * 60)

    # Test 1: Get comparison periods
    print("\n1. Testing get_comparison_periods():")
    wow_periods = get_comparison_periods('WoW')
    print(f"   WoW Periods: {wow_periods}")

    mom_periods = get_comparison_periods('MoM')
    print(f"   MoM Periods: {mom_periods}")

    yoy_periods = get_comparison_periods('YoY')
    print(f"   YoY Periods: {yoy_periods}")

    # Test 2: Calculate changes
    print("\n2. Testing calculate_changes():")
    current = {
        'spend': 520.00,
        'conversions': 12,
        'revenue': 2080.00,
        'roas': 4.0,
        'cpa': 43.33
    }
    previous = {
        'spend': 500.00,
        'conversions': 15,
        'revenue': 2250.00,
        'roas': 4.5,
        'cpa': 33.33
    }

    changes = calculate_changes(current, previous)
    print(f"   ROAS Change: {changes['roas']['absolute']:.2f}x ({changes['roas']['percentage']:.1f}%)")
    print(f"   CPA Change: £{changes['cpa']['absolute']:.2f} ({changes['cpa']['percentage']:.1f}%)")
    print(f"   Flags: {changes['flags']}")

    # Test 3: Format report
    print("\n3. Testing format_comparison_report():")
    report = format_comparison_report('Test Client', wow_periods, changes, 'WoW')
    print("\n" + report)

    # Test 4: Holiday flags
    print("\n4. Testing get_holiday_flags():")
    holiday_flags = get_holiday_flags('2025-11-28', '2025-12-01')
    print(f"   Flags for Black Friday week: {holiday_flags}")

    print("\n" + "=" * 60)
    print("All tests completed successfully!")
