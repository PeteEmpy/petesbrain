#!/usr/bin/env python3
"""
Google Ads ID formatting utilities

Handles conversion between different Google Ads ID formats.
"""

import re


def format_customer_id_with_dashes(customer_id):
    """
    Format a Google Ads customer ID with dashes for Google Ads Editor Account column.

    Google Ads Editor requires Account column in XXX-XXX-XXXX format.

    Args:
        customer_id (str): 10-digit customer ID (e.g., "7808690871")

    Returns:
        str: Formatted customer ID with dashes (e.g., "780-869-0871")

    Raises:
        ValueError: If customer_id is not 10 digits

    Examples:
        >>> format_customer_id_with_dashes("7808690871")
        "780-869-0871"

        >>> format_customer_id_with_dashes("7679616761")
        "767-961-6761"

        >>> format_customer_id_with_dashes("5556710725")
        "555-671-0725"
    """
    # Remove any existing dashes/spaces
    clean_id = re.sub(r'[^\d]', '', str(customer_id))

    if len(clean_id) != 10:
        raise ValueError(f"Customer ID must be 10 digits, got {len(clean_id)}: {customer_id}")

    # Format as XXX-XXX-XXXX
    return f"{clean_id[:3]}-{clean_id[3:6]}-{clean_id[6:]}"


def parse_dashed_customer_id(dashed_id):
    """
    Parse a dashed customer ID back to raw 10-digit format.

    Args:
        dashed_id (str): Customer ID with dashes (e.g., "780-869-0871")

    Returns:
        str: Raw 10-digit customer ID (e.g., "7808690871")

    Raises:
        ValueError: If format is invalid

    Examples:
        >>> parse_dashed_customer_id("780-869-0871")
        "7808690871"

        >>> parse_dashed_customer_id("767-961-6761")
        "7679616761"
    """
    # Remove all non-digit characters
    clean_id = re.sub(r'[^\d]', '', str(dashed_id))

    if len(clean_id) != 10:
        raise ValueError(f"Customer ID must be 10 digits, got {len(clean_id)}: {dashed_id}")

    return clean_id


def validate_customer_id(customer_id):
    """
    Validate that a customer ID is a 10-digit number.

    Args:
        customer_id (str): Customer ID to validate

    Returns:
        bool: True if valid, False otherwise

    Examples:
        >>> validate_customer_id("7808690871")
        True

        >>> validate_customer_id("780-869-0871")
        True

        >>> validate_customer_id("12345")
        False

        >>> validate_customer_id("abc1234567")
        False
    """
    # Remove any dashes/spaces
    clean_id = re.sub(r'[^\d]', '', str(customer_id))

    # Check if 10 digits
    return len(clean_id) == 10 and clean_id.isdigit()


def format_manager_id(manager_id):
    """
    Format a manager account ID (same logic as customer ID).

    Args:
        manager_id (str): 10-digit manager account ID

    Returns:
        str: Formatted manager ID with dashes

    Examples:
        >>> format_manager_id("2569949686")
        "256-994-9686"
    """
    return format_customer_id_with_dashes(manager_id)


def get_account_id_from_context(context_data, region=None):
    """
    Extract customer ID from CONTEXT.md data structure.

    Args:
        context_data (dict): Parsed CONTEXT.md data (from MCP or manual parse)
        region (str, optional): Region identifier if multi-region client (e.g., "USA", "EUR")

    Returns:
        str: Customer ID

    Raises:
        ValueError: If customer ID not found

    Examples:
        # Single-region client
        >>> context = {"google_ads_customer_id": "7808690871"}
        >>> get_account_id_from_context(context)
        "7808690871"

        # Multi-region client
        >>> context = {
        ...     "google_ads_customer_id": {
        ...         "USA": "7808690871",
        ...         "EUR": "7679616761"
        ...     }
        ... }
        >>> get_account_id_from_context(context, "USA")
        "7808690871"
    """
    customer_id = context_data.get('google_ads_customer_id')

    if not customer_id:
        raise ValueError("google_ads_customer_id not found in CONTEXT.md data")

    # Handle multi-region
    if isinstance(customer_id, dict):
        if not region:
            raise ValueError(f"Multi-region client requires region parameter. Available: {list(customer_id.keys())}")
        if region not in customer_id:
            raise ValueError(f"Region '{region}' not found. Available: {list(customer_id.keys())}")
        return customer_id[region]

    # Single region
    return customer_id


# Example usage and testing
if __name__ == '__main__':
    # Test formatting
    print("Testing format_customer_id_with_dashes:")
    test_ids = ["7808690871", "7679616761", "5556710725", "2569949686"]
    for customer_id in test_ids:
        formatted = format_customer_id_with_dashes(customer_id)
        print(f"  {customer_id} → {formatted}")

    print("\nTesting parse_dashed_customer_id:")
    test_dashed = ["780-869-0871", "767-961-6761", "555-671-0725"]
    for dashed_id in test_dashed:
        parsed = parse_dashed_customer_id(dashed_id)
        print(f"  {dashed_id} → {parsed}")

    print("\nTesting validation:")
    test_valid = ["7808690871", "780-869-0871", "12345", "abc1234567", ""]
    for test_id in test_valid:
        is_valid = validate_customer_id(test_id)
        print(f"  {test_id!r} → {is_valid}")

    print("\nTesting round-trip:")
    original = "7808690871"
    formatted = format_customer_id_with_dashes(original)
    parsed = parse_dashed_customer_id(formatted)
    print(f"  {original} → {formatted} → {parsed}")
    assert original == parsed, "Round-trip failed!"
    print("  ✓ Round-trip successful")
