"""
Date utility functions for PetesBrain reporting agents.

CRITICAL: Google Ads and GA4 have 24-48 hour data processing lag.
All date ranges MUST exclude today and yesterday to avoid incomplete data.

See: CLAUDE.md > Date Range Standards (MANDATORY - CRITICAL)
"""

from datetime import datetime, timedelta
from typing import Tuple


def get_complete_date_range(
    days: int = 7,
    lag_days: int = 2
) -> Tuple[str, str]:
    """
    Get complete date range excluding data processing lag.

    Args:
        days: Number of days in report period (default: 7)
        lag_days: Days to exclude for data processing lag (default: 2 for Google Ads 48hr lag)

    Returns:
        tuple: (start_date, end_date) as strings 'YYYY-MM-DD'

    Examples:
        >>> # Today is 2025-11-20
        >>> get_complete_date_range(days=7)
        ('2025-11-11', '2025-11-17')  # 7 complete days, ending 2 days ago

        >>> get_complete_date_range(days=30)
        ('2025-10-19', '2025-11-17')  # 30 complete days, ending 2 days ago
    """
    today = datetime.now().date()
    end_date = today - timedelta(days=lag_days)
    start_date = end_date - timedelta(days=days - 1)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def get_complete_week_range(
    weeks_ago: int = 1,
    lag_days: int = 2
) -> Tuple[str, str]:
    """
    Get complete week date range (Mon-Sun), excluding data processing lag.

    Args:
        weeks_ago: Which week to retrieve (1 = last complete week, 2 = week before that)
        lag_days: Days to exclude for data processing lag (default: 2)

    Returns:
        tuple: (monday_date, sunday_date) as strings 'YYYY-MM-DD'

    Examples:
        >>> # Today is Wed 2025-11-20
        >>> get_complete_week_range(weeks_ago=1)
        ('2025-11-04', '2025-11-10')  # Last complete Mon-Sun week

        >>> get_complete_week_range(weeks_ago=2)
        ('2025-10-28', '2025-11-03')  # Week before last
    """
    today = datetime.now().date()
    # Go back to account for lag
    effective_today = today - timedelta(days=lag_days)

    # Find the Monday of the target week
    days_since_monday = effective_today.weekday()  # 0 = Monday, 6 = Sunday
    this_monday = effective_today - timedelta(days=days_since_monday)

    # Go back N weeks
    target_monday = this_monday - timedelta(weeks=weeks_ago)
    target_sunday = target_monday + timedelta(days=6)

    return target_monday.strftime('%Y-%m-%d'), target_sunday.strftime('%Y-%m-%d')


def get_complete_month_range(
    months_ago: int = 1
) -> Tuple[str, str]:
    """
    Get complete month date range.

    Args:
        months_ago: Which month to retrieve (1 = last complete month, 2 = month before that)

    Returns:
        tuple: (first_day, last_day) as strings 'YYYY-MM-DD'

    Examples:
        >>> # Today is 2025-11-20
        >>> get_complete_month_range(months_ago=1)
        ('2025-10-01', '2025-10-31')  # October (last complete month)

        >>> get_complete_month_range(months_ago=2)
        ('2025-09-01', '2025-09-30')  # September
    """
    today = datetime.now().date()

    # Calculate target month
    target_month = today.month - months_ago
    target_year = today.year

    # Handle year rollover
    while target_month < 1:
        target_month += 12
        target_year -= 1

    # First day of target month
    first_day = datetime(target_year, target_month, 1).date()

    # Last day of target month
    if target_month == 12:
        last_day = datetime(target_year, 12, 31).date()
    else:
        last_day = datetime(target_year, target_month + 1, 1).date() - timedelta(days=1)

    return first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')


def get_comparison_periods(
    period_type: str = 'week',
    lag_days: int = 2
) -> Tuple[Tuple[str, str], Tuple[str, str]]:
    """
    Get two comparable periods for week-over-week or month-over-month analysis.

    Args:
        period_type: Either 'week', 'month', or 'custom'
        lag_days: Days to exclude for data processing lag (default: 2)

    Returns:
        tuple: ((current_start, current_end), (previous_start, previous_end))

    Examples:
        >>> # Today is Wed 2025-11-20
        >>> get_comparison_periods('week')
        (('2025-11-11', '2025-11-17'), ('2025-11-04', '2025-11-10'))
        # Current: 7 complete days, Previous: 7 complete days before that

        >>> get_comparison_periods('month')
        (('2025-10-01', '2025-10-31'), ('2025-09-01', '2025-09-30'))
        # October vs September
    """
    if period_type == 'week':
        # Get 7-day periods
        current_start, current_end = get_complete_date_range(days=7, lag_days=lag_days)
        current_start_dt = datetime.strptime(current_start, '%Y-%m-%d').date()
        previous_end_dt = current_start_dt - timedelta(days=1)
        previous_start_dt = previous_end_dt - timedelta(days=6)

        return (
            (current_start, current_end),
            (previous_start_dt.strftime('%Y-%m-%d'), previous_end_dt.strftime('%Y-%m-%d'))
        )

    elif period_type == 'month':
        current = get_complete_month_range(months_ago=1)
        previous = get_complete_month_range(months_ago=2)
        return current, previous

    else:
        raise ValueError(f"Invalid period_type: {period_type}. Use 'week' or 'month'.")


def format_gaql_date_range(
    start_date: str,
    end_date: str
) -> str:
    """
    Format date range for Google Ads GAQL queries.

    Args:
        start_date: Start date 'YYYY-MM-DD'
        end_date: End date 'YYYY-MM-DD'

    Returns:
        str: GAQL date filter clause

    Examples:
        >>> format_gaql_date_range('2025-11-11', '2025-11-17')
        "segments.date BETWEEN '2025-11-11' AND '2025-11-17'"
    """
    return f"segments.date BETWEEN '{start_date}' AND '{end_date}'"


def validate_date_range(
    start_date: str,
    end_date: str,
    min_lag_days: int = 2
) -> bool:
    """
    Validate that date range respects data processing lag.

    Args:
        start_date: Start date 'YYYY-MM-DD'
        end_date: End date 'YYYY-MM-DD'
        min_lag_days: Minimum days from today to end_date (default: 2)

    Returns:
        bool: True if valid, raises ValueError if invalid

    Examples:
        >>> # Today is 2025-11-20
        >>> validate_date_range('2025-11-11', '2025-11-17')  # Valid (ends 3 days ago)
        True

        >>> validate_date_range('2025-11-11', '2025-11-19')  # Invalid (ends yesterday)
        ValueError: End date must be at least 2 days before today to account for data lag
    """
    today = datetime.now().date()
    end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
    days_from_today = (today - end_dt).days

    if days_from_today < min_lag_days:
        raise ValueError(
            f"End date must be at least {min_lag_days} days before today to account for data lag. "
            f"Given end_date: {end_date} (only {days_from_today} days ago)"
        )

    return True


# Quick access functions for common use cases
def get_last_7_complete_days() -> Tuple[str, str]:
    """Get last 7 complete days (excluding today and yesterday)."""
    return get_complete_date_range(days=7)


def get_last_30_complete_days() -> Tuple[str, str]:
    """Get last 30 complete days (excluding today and yesterday)."""
    return get_complete_date_range(days=30)


def get_last_complete_week() -> Tuple[str, str]:
    """Get last complete Mon-Sun week."""
    return get_complete_week_range(weeks_ago=1)


def get_last_complete_month() -> Tuple[str, str]:
    """Get last complete calendar month."""
    return get_complete_month_range(months_ago=1)


if __name__ == '__main__':
    """Demo usage"""
    print("=== Date Range Utilities Demo ===\n")
    print(f"Today: {datetime.now().date()}\n")

    start, end = get_last_7_complete_days()
    print(f"Last 7 complete days: {start} to {end}")

    start, end = get_last_complete_week()
    print(f"Last complete week: {start} to {end}")

    start, end = get_last_complete_month()
    print(f"Last complete month: {start} to {end}")

    current, previous = get_comparison_periods('week')
    print(f"\nWeek-over-week comparison:")
    print(f"  Current:  {current[0]} to {current[1]}")
    print(f"  Previous: {previous[0]} to {previous[1]}")

    print(f"\nGAQL format: {format_gaql_date_range('2025-11-11', '2025-11-17')}")
