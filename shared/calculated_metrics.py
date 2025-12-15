"""
Calculated Metrics Helper for Google Ads Automation

Provides safe calculation of Google Ads metrics with proper handling of:
- Division by zero (returns None instead of error/inf)
- Context comparison (variance from target, previous period)
- Proper aggregation (sum first, calculate second - never average percentages)

Usage:
    from shared.calculated_metrics import calculate_roas, format_metric, aggregate_metrics

    roas = calculate_roas(conversions_value=5400, cost=1200)
    display = format_metric(roas, 'roas')  # "4.50x"

Based on Mike Rhodes' "Calculated Metrics" teaching from 8020brain.com
Part of Ads to AI Skill Map - Phase 1: Automated Reporting

Author: PetesBrain
Created: 2025-12-14
"""


def calculate_roas(conversions_value, cost):
    """
    Calculate Return on Ad Spend (ROAS)

    Args:
        conversions_value: Total conversion value (revenue) in £
        cost: Total cost (spend) in £

    Returns:
        float: ROAS as a multiplier (e.g., 4.5 for 4.5x ROAS)
        None: If cost is 0 or None (prevents division by zero)

    Example:
        >>> calculate_roas(5400, 1200)
        4.5
        >>> calculate_roas(0, 0)
        None
    """
    if not cost or cost == 0:
        return None
    return conversions_value / cost


def calculate_cpa(cost, conversions):
    """
    Calculate Cost per Acquisition (CPA)

    Args:
        cost: Total cost (spend) in £
        conversions: Total number of conversions

    Returns:
        float: CPA in £ (e.g., 45.50 for £45.50 CPA)
        None: If conversions is 0 or None (prevents division by zero)

    Example:
        >>> calculate_cpa(1200, 28)
        42.857142857142854
        >>> calculate_cpa(1200, 0)
        None
    """
    if not conversions or conversions == 0:
        return None
    return cost / conversions


def calculate_ctr(clicks, impressions):
    """
    Calculate Click-Through Rate (CTR) as decimal

    Args:
        clicks: Total number of clicks
        impressions: Total number of impressions

    Returns:
        float: CTR as decimal (e.g., 0.035 for 3.5% CTR)
        None: If impressions is 0 or None (prevents division by zero)

    Example:
        >>> calculate_ctr(350, 10000)
        0.035
        >>> calculate_ctr(0, 0)
        None
    """
    if not impressions or impressions == 0:
        return None
    return clicks / impressions


def calculate_conversion_rate(conversions, clicks):
    """
    Calculate Conversion Rate as decimal

    Args:
        conversions: Total number of conversions
        clicks: Total number of clicks

    Returns:
        float: Conversion rate as decimal (e.g., 0.08 for 8% conversion rate)
        None: If clicks is 0 or None (prevents division by zero)

    Example:
        >>> calculate_conversion_rate(28, 350)
        0.08
        >>> calculate_conversion_rate(0, 0)
        None
    """
    if not clicks or clicks == 0:
        return None
    return conversions / clicks


def format_metric(value, metric_type='currency', show_na=True, decimal_places=2):
    """
    Format metric for display with N/A handling

    Args:
        value: Calculated metric value (or None)
        metric_type: Format type - 'currency', 'roas', 'percentage', 'decimal', 'integer'
        show_na: If True, return 'N/A' for None values; if False, return '—'
        decimal_places: Number of decimal places (default 2)

    Returns:
        str: Formatted metric string

    Examples:
        >>> format_metric(4.567, 'roas')
        '4.57x'
        >>> format_metric(None, 'roas')
        'N/A'
        >>> format_metric(0.0345, 'percentage')
        '3.45%'
        >>> format_metric(1234.56, 'currency')
        '£1,234.56'
    """
    if value is None:
        return 'N/A' if show_na else '—'

    if metric_type == 'currency':
        return f'£{value:,.{decimal_places}f}'
    elif metric_type == 'roas':
        return f'{value:.{decimal_places}f}x'
    elif metric_type == 'percentage':
        return f'{value * 100:.{decimal_places}f}%'
    elif metric_type == 'decimal':
        return f'{value:.{decimal_places}f}'
    elif metric_type == 'integer':
        return f'{int(value):,}'
    else:
        return str(value)


def calculate_variance(actual, target):
    """
    Calculate variance from target as percentage

    Args:
        actual: Actual value
        target: Target value

    Returns:
        float: Percentage variance (e.g., -20.0 for 20% below target, +15.0 for 15% above)
        None: If target is 0 or None (prevents division by zero)

    Examples:
        >>> calculate_variance(3.2, 4.0)
        -20.0
        >>> calculate_variance(4.8, 4.0)
        20.0
        >>> calculate_variance(4.0, 0)
        None
    """
    if not target or target == 0:
        return None
    if actual is None:
        return None
    return ((actual - target) / target) * 100


def format_variance(variance, include_sign=True):
    """
    Format variance with colour indicators and sign

    Args:
        variance: Percentage variance (positive = good, negative = bad)
        include_sign: If True, include + or - sign

    Returns:
        str: Formatted variance with emoji indicator

    Examples:
        >>> format_variance(20.5)
        '✓ +20.5%'
        >>> format_variance(-15.3)
        '⚠️ -15.3%'
        >>> format_variance(-5.2)
        '◆ -5.2%'
    """
    if variance is None:
        return 'N/A'

    # Determine indicator based on magnitude
    if variance >= 10:
        indicator = '✓'  # Significantly above target
    elif variance >= 0:
        indicator = '◆'  # Slightly above target
    elif variance >= -10:
        indicator = '◆'  # Slightly below target
    else:
        indicator = '⚠️'  # Significantly below target

    sign = '+' if variance >= 0 else ''
    return f'{indicator} {sign}{variance:.1f}%'


def aggregate_metrics(campaigns, cost_key='cost', revenue_key='conversions_value', conversions_key='conversions'):
    """
    Aggregate campaign data to account level with proper calculation

    CRITICAL: Never average ROAS or CPA - calculate from summed totals.

    Campaign 1: £100 spend, £500 revenue = 5.0x ROAS
    Campaign 2: £900 spend, £2,700 revenue = 3.0x ROAS
    Average ROAS: (5.0 + 3.0) / 2 = 4.0x ❌ WRONG
    Actual ROAS: £3,200 / £1,000 = 3.2x ✓ CORRECT

    Args:
        campaigns: List of campaign dicts with cost, revenue, conversions
        cost_key: Key name for cost field (default 'cost')
        revenue_key: Key name for revenue field (default 'conversions_value')
        conversions_key: Key name for conversions field (default 'conversions')

    Returns:
        dict: {
            'total_cost': float,
            'total_revenue': float,
            'total_conversions': int,
            'roas': float or None,
            'cpa': float or None
        }

    Example:
        >>> campaigns = [
        ...     {'cost': 100, 'conversions_value': 500, 'conversions': 10},
        ...     {'cost': 900, 'conversions_value': 2700, 'conversions': 90}
        ... ]
        >>> result = aggregate_metrics(campaigns)
        >>> result['roas']
        3.2
        >>> result['cpa']
        10.0
    """
    total_cost = sum(c.get(cost_key, 0) for c in campaigns if c.get(cost_key) is not None)
    total_revenue = sum(c.get(revenue_key, 0) for c in campaigns if c.get(revenue_key) is not None)
    total_conversions = sum(c.get(conversions_key, 0) for c in campaigns if c.get(conversions_key) is not None)

    return {
        'total_cost': total_cost,
        'total_revenue': total_revenue,
        'total_conversions': total_conversions,
        'roas': calculate_roas(total_revenue, total_cost),
        'cpa': calculate_cpa(total_cost, total_conversions)
    }


def add_context(current_metric, target=None, previous=None, account_average=None):
    """
    Add context to a metric with comparisons

    Args:
        current_metric: Current metric value
        target: Target value (from CONTEXT.md)
        previous: Previous period value
        account_average: Account-wide average

    Returns:
        dict: {
            'value': current_metric,
            'vs_target': percentage variance,
            'vs_previous': percentage variance,
            'vs_account': percentage variance
        }

    Example:
        >>> context = add_context(
        ...     current_metric=3.8,
        ...     target=4.0,
        ...     previous=4.2,
        ...     account_average=4.5
        ... )
        >>> context['vs_target']
        -5.0
        >>> context['vs_previous']
        -9.523809523809524
    """
    return {
        'value': current_metric,
        'vs_target': calculate_variance(current_metric, target) if target else None,
        'vs_previous': calculate_variance(current_metric, previous) if previous else None,
        'vs_account': calculate_variance(current_metric, account_average) if account_average else None
    }


def format_metric_with_context(metric_dict, metric_type='roas', metric_name='ROAS'):
    """
    Format a metric with all context in readable text

    Args:
        metric_dict: Dict from add_context() with value and comparisons
        metric_type: Format type for the metric value
        metric_name: Display name for the metric

    Returns:
        str: Formatted multi-line string with metric and context

    Example:
        >>> context = add_context(3.8, target=4.0, previous=4.2)
        >>> print(format_metric_with_context(context, 'roas', 'ROAS'))
        ROAS: 3.80x
        vs Target (4.00x): ◆ -5.0%
        vs Last Week: ⚠️ -9.5%
    """
    lines = []

    # Main metric value
    value_str = format_metric(metric_dict['value'], metric_type)
    lines.append(f"{metric_name}: {value_str}")

    # Target comparison
    if metric_dict['vs_target'] is not None:
        target_indicator = format_variance(metric_dict['vs_target'])
        lines.append(f"vs Target: {target_indicator}")

    # Previous period comparison
    if metric_dict['vs_previous'] is not None:
        previous_indicator = format_variance(metric_dict['vs_previous'])
        lines.append(f"vs Previous: {previous_indicator}")

    # Account average comparison
    if metric_dict['vs_account'] is not None:
        account_indicator = format_variance(metric_dict['vs_account'])
        lines.append(f"vs Account: {account_indicator}")

    return '\n'.join(lines)


def convert_micros_to_currency(micros):
    """
    Convert Google Ads micros to currency (£)

    Google Ads API returns cost and revenue in micros (1/1,000,000 of currency unit)

    Args:
        micros: Value in micros (e.g., 1200000000 for £1,200)

    Returns:
        float: Value in £ (e.g., 1200.00)

    Example:
        >>> convert_micros_to_currency(1200000000)
        1200.0
        >>> convert_micros_to_currency(0)
        0.0
    """
    if micros is None:
        return 0.0
    return micros / 1_000_000


# Convenience function for common workflow
def process_campaign_metrics(raw_data, target_roas=None, previous_data=None):
    """
    Complete workflow: convert micros, calculate metrics, add context

    Args:
        raw_data: Dict with cost_micros, conversions_value_micros, conversions from API
        target_roas: Target ROAS from CONTEXT.md
        previous_data: Previous period raw data for comparison

    Returns:
        dict: Fully processed metrics with context

    Example:
        >>> raw = {
        ...     'cost_micros': 1200000000,
        ...     'conversions_value_micros': 5400000000,
        ...     'conversions': 28
        ... }
        >>> result = process_campaign_metrics(raw, target_roas=4.0)
        >>> result['cost']
        1200.0
        >>> result['revenue']
        5400.0
        >>> result['roas']['value']
        4.5
    """
    # Convert micros to currency
    cost = convert_micros_to_currency(raw_data.get('cost_micros', 0))
    revenue = convert_micros_to_currency(raw_data.get('conversions_value_micros', 0))
    conversions = raw_data.get('conversions', 0)

    # Calculate current metrics
    roas = calculate_roas(revenue, cost)
    cpa = calculate_cpa(cost, conversions)

    # Calculate previous metrics if provided
    previous_roas = None
    previous_cpa = None
    if previous_data:
        prev_cost = convert_micros_to_currency(previous_data.get('cost_micros', 0))
        prev_revenue = convert_micros_to_currency(previous_data.get('conversions_value_micros', 0))
        prev_conversions = previous_data.get('conversions', 0)
        previous_roas = calculate_roas(prev_revenue, prev_cost)
        previous_cpa = calculate_cpa(prev_cost, prev_conversions)

    return {
        'cost': cost,
        'revenue': revenue,
        'conversions': conversions,
        'roas': add_context(roas, target=target_roas, previous=previous_roas),
        'cpa': add_context(cpa, previous=previous_cpa)
    }
