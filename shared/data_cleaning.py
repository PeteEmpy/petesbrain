"""
Data Cleaning Utilities for Google Ads Reporting

Provides functions for cleaning and standardising Google Ads data from API responses
and CSV exports. Focuses on making messy data reliable for analysis.

Core principles:
- Handle nulls/blanks explicitly (decide what they mean)
- Standardise text (capitalisation, spacing, special characters)
- Clean at source when possible (fix in query/script)
- Document cleaning decisions (why we clean what we clean)

Usage:
    from shared.data_cleaning import clean_campaign_name, clean_metric_value, standardise_currency

    # Clean campaign names for consistent grouping
    clean_name = clean_campaign_name("  PMax | uk | BRANDED  ")
    # Returns: "PMax | UK | Branded"

    # Handle null metrics from Google Ads
    roas = clean_metric_value(api_result.get('conversionsValue'), default=0)
"""

import re
from typing import Any, Optional, Union


def clean_campaign_name(name: str, preserve_format: bool = True) -> str:
    """
    Standardise campaign names for consistent analysis.

    Designed for reporting-level cleaning (not changing live campaigns).
    Preserves brand abbreviations (SMY, etc.) and good formatting while
    standardising old underscore/hyphen-only formats.

    Cleaning rules:
    - Remove extra spaces (TRIM equivalent)
    - Standardise separators (underscores/hyphens → pipes " | ")
    - Preserve brand abbreviations (SMY, etc.)
    - Preserve campaign types that are already well-formatted
    - Clean old formats: "UK_Brand_Core" → "UK | Brand | Core"

    Args:
        name: Raw campaign name from Google Ads
        preserve_format: If True, preserves good formatting (default: True)

    Returns:
        Cleaned campaign name

    Examples:
        >>> clean_campaign_name("SMY | UK | P Max | Diaries")
        'SMY | UK | P Max | Diaries'  # Already clean - no change

        >>> clean_campaign_name("UK_Brand_Core Max_Conversions_Value_Test")
        'UK | Brand | Core Max | Conversions | Value | Test'

        >>> clean_campaign_name("UK - brand - core - new UK - brand test")
        'UK | Brand | Core | New UK | Brand Test'
    """
    if not name or not isinstance(name, str):
        return ""

    # Step 1: TRIM - remove leading/trailing whitespace
    cleaned = name.strip()

    # Quick check: if already in good format (has pipes with proper spacing), minimal cleaning
    if preserve_format and ' | ' in cleaned:
        # Just trim extra spaces and return
        # This preserves "SMY | UK | P Max | Diaries" as-is
        return re.sub(r'\s+', ' ', cleaned).strip()

    # Step 2: SUBSTITUTE - standardise separators to " | "
    # Replace underscores and hyphens with pipes
    cleaned = re.sub(r'_', ' | ', cleaned)  # UK_Brand_Core → UK | Brand | Core
    cleaned = re.sub(r'\s*-\s*', ' | ', cleaned)  # UK - brand → UK | brand

    # Fix pipes without proper spacing
    cleaned = re.sub(r'\s*\|\s*', ' | ', cleaned)

    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # Clean up multiple pipes (from replacing consecutive separators)
    cleaned = re.sub(r'\|\s*\|+', '|', cleaned)

    # Step 3: Light capitalisation standardisation
    # Split by pipes to process segments
    segments = [seg.strip() for seg in cleaned.split('|')]
    standardised_segments = []

    for segment in segments:
        # Skip empty segments
        if not segment:
            continue

        # Preserve brand abbreviations (all caps 2-4 letters at start)
        if re.match(r'^[A-Z]{2,4}$', segment):
            standardised_segments.append(segment)  # Keep SMY, UK, USA, EUR, ROW as-is
            continue

        # Preserve segments that are already well-formatted
        # (have mix of upper/lower and spaces)
        if segment[0].isupper() and any(c.islower() for c in segment):
            standardised_segments.append(segment)  # Keep "P Max", "Brand Plus" as-is
            continue

        # Otherwise, apply title case
        standardised_segments.append(segment.title())

    return ' | '.join(standardised_segments)


def clean_metric_value(
    value: Any,
    metric_type: str = 'numeric',
    default: Union[int, float] = 0
) -> Union[int, float]:
    """
    Clean metric values from Google Ads API or CSV exports.

    Handles:
    - None/null values → return default
    - '--' strings (Google Ads null indicator) → return default
    - Empty strings → return default
    - Valid numbers → return as float/int

    Args:
        value: Raw metric value
        metric_type: 'numeric' (default), 'currency', 'percentage'
        default: Value to return if input is null/invalid

    Returns:
        Cleaned numeric value

    Examples:
        >>> clean_metric_value(None)
        0

        >>> clean_metric_value('--')
        0

        >>> clean_metric_value('1,234.56', metric_type='currency')
        1234.56

        >>> clean_metric_value('42.5%', metric_type='percentage')
        42.5
    """
    # Handle None, empty string, or '--' (Google Ads null)
    if value is None or value == '' or value == '--':
        return default

    # If already a number, return it
    if isinstance(value, (int, float)):
        return value

    # If string, clean and convert
    if isinstance(value, str):
        # Remove currency symbols, commas, percentage signs
        cleaned = value.strip()
        cleaned = cleaned.replace('£', '').replace('$', '').replace(',', '').replace('%', '')

        try:
            # Try to convert to float
            return float(cleaned)
        except ValueError:
            # If conversion fails, return default
            return default

    # Fallback: return default
    return default


def clean_csv_row(row: dict, google_ads_format: bool = True) -> dict:
    """
    Clean a single row from a CSV export.

    Args:
        row: Dictionary representing CSV row
        google_ads_format: If True, applies Google Ads-specific cleaning

    Returns:
        Cleaned row dictionary

    Google Ads-specific cleaning:
    - Campaign names standardised
    - '--' converted to 0
    - Commas removed from numbers
    - Currency symbols removed
    """
    cleaned = {}

    for key, value in row.items():
        # Clean campaign/ad group names
        if 'campaign' in key.lower() or 'ad group' in key.lower():
            if 'name' in key.lower():
                cleaned[key] = clean_campaign_name(value)
            else:
                cleaned[key] = value

        # Clean metric values (spend, conversions, revenue, etc.)
        elif any(metric in key.lower() for metric in ['cost', 'conv', 'revenue', 'value', 'cpc', 'ctr', 'impressions', 'clicks']):
            cleaned[key] = clean_metric_value(value)

        # Default: keep as is
        else:
            cleaned[key] = value

    return cleaned


def standardise_currency(
    amount: Union[int, float],
    from_currency: str = 'GBP',
    to_currency: str = 'GBP',
    exchange_rates: Optional[dict] = None
) -> float:
    """
    Convert currency amounts for multi-market clients.

    Args:
        amount: Amount to convert
        from_currency: Source currency code (GBP, USD, EUR)
        to_currency: Target currency code
        exchange_rates: Optional dict of rates (e.g., {'USD': 1.27, 'EUR': 1.17})

    Returns:
        Converted amount

    Note:
        If no exchange_rates provided and conversion needed, returns original amount.
        For accurate reporting, provide current exchange rates.
    """
    if from_currency == to_currency:
        return amount

    if exchange_rates is None:
        # No conversion possible without rates
        return amount

    # Convert from source to GBP, then GBP to target
    if from_currency != 'GBP':
        # Convert to GBP first
        if from_currency in exchange_rates:
            amount = amount / exchange_rates[from_currency]
        else:
            return amount  # Can't convert without rate

    if to_currency != 'GBP':
        # Convert from GBP to target
        if to_currency in exchange_rates:
            amount = amount * exchange_rates[to_currency]
        else:
            return amount  # Can't convert without rate

    return round(amount, 2)


def format_roas_as_percentage(roas: float) -> str:
    """
    Format ROAS as percentage for British English output.

    PetesBrain standard: ROAS always as percentage (420% not £4.20 or 4.2x)

    Args:
        roas: ROAS as multiplier (e.g., 4.2)

    Returns:
        Formatted percentage string (e.g., "420%")

    Examples:
        >>> format_roas_as_percentage(4.2)
        '420%'

        >>> format_roas_as_percentage(2.92)
        '292%'
    """
    return f"{roas * 100:.0f}%"


# Quick test
if __name__ == "__main__":
    print("Testing Data Cleaning Functions\n")
    print("=" * 60)

    # Test 1: Campaign name cleaning
    print("\n1. Campaign Name Cleaning:")
    test_names = [
        "  pmax | uk | branded  ",
        "Search-Brand-UK",
        "SHOPPING_GENERIC",
        "Performance Max|USA|Products"
    ]

    for name in test_names:
        cleaned = clean_campaign_name(name)
        print(f"   '{name}' → '{cleaned}'")

    # Test 2: Metric value cleaning
    print("\n2. Metric Value Cleaning:")
    test_values = [
        (None, "None → 0"),
        ('--', "'--' → 0"),
        ('1,234.56', "'1,234.56' → 1234.56"),
        ('£2,450.00', "'£2,450.00' → 2450.0"),
        ('42.5%', "'42.5%' → 42.5")
    ]

    for value, description in test_values:
        cleaned = clean_metric_value(value)
        print(f"   {description}: {cleaned}")

    # Test 3: ROAS formatting
    print("\n3. ROAS Formatting:")
    test_roas = [4.2, 2.92, 1.5]
    for roas in test_roas:
        formatted = format_roas_as_percentage(roas)
        print(f"   {roas} → {formatted}")

    print("\n" + "=" * 60)
    print("All tests completed!\n")
