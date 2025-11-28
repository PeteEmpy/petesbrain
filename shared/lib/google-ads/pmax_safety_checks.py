"""
Google Ads Performance Max Asset Group Safety Checks Module

Reusable safety functions to prevent common PMax asset management errors.

Key Safety Patterns:
- Deduplication (prevent DUPLICATE_RESOURCE errors)
- Overflow protection (prevent exceeding maximum limits)
- Add-before-remove (never leave asset groups empty)
- Minimum requirement checks (ensure PMax minimums met)

Usage:
    from pmax_safety_checks import (
        deduplicate_asset_ids,
        check_overflow_protection,
        validate_minimum_text_requirements
    )

    # Remove duplicates
    unique_ids = deduplicate_asset_ids(['123', '456', '123', '789'])
    # Returns: ['123', '456', '789']

    # Check overflow
    needs_batch_removal, to_remove_first = check_overflow_protection(
        current_count=15,
        new_count=8,
        max_limit=20
    )

    # Validate text minimums
    is_valid, error = validate_minimum_text_requirements(
        headlines=10,
        long_headlines=3,
        descriptions=4
    )
"""

from typing import List, Tuple, Optional


# PMax text asset requirements
MINIMUM_TEXT_REQUIREMENTS = {
    'HEADLINE': 3,           # Minimum 3 headlines
    'LONG_HEADLINE': 1,      # Minimum 1 long headline
    'DESCRIPTION': 2,        # Minimum 2 descriptions
}

MAXIMUM_TEXT_REQUIREMENTS = {
    'HEADLINE': 15,          # Maximum 15 headlines
    'LONG_HEADLINE': 5,      # Maximum 5 long headlines
    'DESCRIPTION': 5,        # Maximum 5 descriptions (actually 4, but API allows 5)
}

# PMax image requirements
MAXIMUM_IMAGES = 20


def deduplicate_asset_ids(asset_ids: List[str]) -> List[str]:
    """
    Remove duplicate asset IDs while preserving order.

    Prevents DUPLICATE_RESOURCE errors when linking assets to asset groups.

    Args:
        asset_ids: List of asset IDs (may contain duplicates)

    Returns:
        List of unique asset IDs in original order

    Example:
        >>> deduplicate_asset_ids(['123', '456', '123', '789', '456'])
        ['123', '456', '789']
    """
    seen = set()
    unique_ids = []

    for asset_id in asset_ids:
        # Clean and validate
        clean_id = asset_id.strip()
        if clean_id and clean_id not in seen:
            unique_ids.append(clean_id)
            seen.add(clean_id)

    return unique_ids


def check_overflow_protection(current_count: int, new_count: int,
                              max_limit: int = MAXIMUM_IMAGES) -> Tuple[bool, int]:
    """
    Check if adding new assets would exceed maximum limit.

    If adding all new assets first would cause overflow, calculates how many
    current assets to remove first to make room.

    Args:
        current_count: Number of current assets in asset group
        new_count: Number of new assets to add
        max_limit: Maximum allowed (default: 20 for images)

    Returns:
        Tuple of (needs_batch_removal, to_remove_first)
        - needs_batch_removal: True if overflow protection needed
        - to_remove_first: Number of current assets to remove first (0 if no overflow)

    Strategy:
        - If current + new <= max: Add all new, then remove old (safe)
        - If current + new > max: Remove some old first, add new, remove remaining old

    Example:
        >>> check_overflow_protection(current_count=15, new_count=8, max_limit=20)
        (True, 3)  # Remove 3 first to make room

        >>> check_overflow_protection(current_count=10, new_count=5, max_limit=20)
        (False, 0)  # No overflow, safe to add all first
    """
    total_if_add_first = current_count + new_count

    if total_if_add_first <= max_limit:
        # Safe: no overflow
        return False, 0
    else:
        # Overflow: calculate how many to remove first
        excess = total_if_add_first - max_limit
        to_remove_first = excess
        return True, to_remove_first


def validate_minimum_text_requirements(headlines: int, long_headlines: int,
                                       descriptions: int) -> Tuple[bool, Optional[str]]:
    """
    Validate that text asset counts meet PMax minimum requirements.

    Args:
        headlines: Number of headlines
        long_headlines: Number of long headlines
        descriptions: Number of descriptions

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if all minimums met
        - error_message: Detailed error if invalid (None if valid)

    Example:
        >>> validate_minimum_text_requirements(10, 3, 4)
        (True, None)

        >>> validate_minimum_text_requirements(2, 1, 4)
        (False, '❌ Not enough headlines: 2 (minimum: 3)')
    """
    errors = []

    if headlines < MINIMUM_TEXT_REQUIREMENTS['HEADLINE']:
        errors.append(
            f"Not enough headlines: {headlines} "
            f"(minimum: {MINIMUM_TEXT_REQUIREMENTS['HEADLINE']})"
        )

    if long_headlines < MINIMUM_TEXT_REQUIREMENTS['LONG_HEADLINE']:
        errors.append(
            f"Not enough long headlines: {long_headlines} "
            f"(minimum: {MINIMUM_TEXT_REQUIREMENTS['LONG_HEADLINE']})"
        )

    if descriptions < MINIMUM_TEXT_REQUIREMENTS['DESCRIPTION']:
        errors.append(
            f"Not enough descriptions: {descriptions} "
            f"(minimum: {MINIMUM_TEXT_REQUIREMENTS['DESCRIPTION']})"
        )

    if errors:
        error_msg = "❌ Text asset validation failed:\n    " + "\n    ".join(errors)
        return False, error_msg

    return True, None


def validate_maximum_text_requirements(headlines: int, long_headlines: int,
                                       descriptions: int) -> Tuple[bool, Optional[str]]:
    """
    Validate that text asset counts don't exceed PMax maximum limits.

    Args:
        headlines: Number of headlines
        long_headlines: Number of long headlines
        descriptions: Number of descriptions

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if all within limits
        - error_message: Detailed error if invalid (None if valid)

    Example:
        >>> validate_maximum_text_requirements(10, 3, 4)
        (True, None)

        >>> validate_maximum_text_requirements(20, 3, 4)
        (False, '❌ Too many headlines: 20 (maximum: 15)')
    """
    errors = []

    if headlines > MAXIMUM_TEXT_REQUIREMENTS['HEADLINE']:
        errors.append(
            f"Too many headlines: {headlines} "
            f"(maximum: {MAXIMUM_TEXT_REQUIREMENTS['HEADLINE']})"
        )

    if long_headlines > MAXIMUM_TEXT_REQUIREMENTS['LONG_HEADLINE']:
        errors.append(
            f"Too many long headlines: {long_headlines} "
            f"(maximum: {MAXIMUM_TEXT_REQUIREMENTS['LONG_HEADLINE']})"
        )

    if descriptions > MAXIMUM_TEXT_REQUIREMENTS['DESCRIPTION']:
        errors.append(
            f"Too many descriptions: {descriptions} "
            f"(maximum: {MAXIMUM_TEXT_REQUIREMENTS['DESCRIPTION']})"
        )

    if errors:
        error_msg = "❌ Text asset limit exceeded:\n    " + "\n    ".join(errors)
        return False, error_msg

    return True, None


def safe_add_remove_strategy(current_resources: List[str], new_resources: List[str],
                             max_limit: int = MAXIMUM_IMAGES) -> List[dict]:
    """
    Generate safe add-before-remove operation sequence.

    Ensures asset group never drops below minimum by adding new assets first,
    then removing old ones. Handles overflow protection automatically.

    Args:
        current_resources: List of current asset resource names to remove
        new_resources: List of new asset resource names to add
        max_limit: Maximum allowed assets (default: 20)

    Returns:
        List of operation dictionaries in safe execution order

    Example:
        >>> ops = safe_add_remove_strategy(
        ...     current_resources=['customers/123/assets/old1', 'customers/123/assets/old2'],
        ...     new_resources=['customers/123/assets/new1', 'customers/123/assets/new2']
        ... )
        >>> # Returns operations in safe order: add new, remove old
    """
    operations = []

    current_count = len(current_resources)
    new_count = len(new_resources)

    needs_overflow, to_remove_first = check_overflow_protection(
        current_count, new_count, max_limit
    )

    if needs_overflow:
        # OVERFLOW CASE: Remove some first to make room
        # 1. Remove just enough to make room
        first_batch = current_resources[:to_remove_first]
        for resource in first_batch:
            operations.append({'remove': resource})

        # 2. Add all new
        for resource in new_resources:
            operations.append({'create': resource})

        # 3. Remove remaining old
        remaining_batch = current_resources[to_remove_first:]
        for resource in remaining_batch:
            operations.append({'remove': resource})

    else:
        # SAFE CASE: Add all new first, then remove old
        # 1. Add all new
        for resource in new_resources:
            operations.append({'create': resource})

        # 2. Remove all old
        for resource in current_resources:
            operations.append({'remove': resource})

    return operations


def filter_empty_strings(items: List[str]) -> List[str]:
    """
    Filter out empty, None, or whitespace-only strings.

    Args:
        items: List of strings (may contain empty/None values)

    Returns:
        List of non-empty strings

    Example:
        >>> filter_empty_strings(['hello', '', '  ', None, 'world'])
        ['hello', 'world']
    """
    return [item.strip() for item in items if item and item.strip()]


def validate_character_limits(headlines: List[str], long_headlines: List[str],
                              descriptions: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate that text assets meet character length requirements.

    Requirements:
    - Headlines: max 30 characters
    - Long headlines: max 90 characters
    - Descriptions: max 90 characters

    Args:
        headlines: List of headline texts
        long_headlines: List of long headline texts
        descriptions: List of description texts

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if all within limits
        - error_message: Detailed error if invalid (None if valid)

    Example:
        >>> validate_character_limits(
        ...     ['Short headline'],
        ...     ['This is a longer headline'],
        ...     ['Product description']
        ... )
        (True, None)
    """
    errors = []

    # Check headlines (max 30 chars)
    for i, text in enumerate(headlines):
        if len(text) > 30:
            errors.append(f"Headline {i+1} too long: {len(text)} chars (max: 30) - \"{text[:40]}...\"")

    # Check long headlines (max 90 chars)
    for i, text in enumerate(long_headlines):
        if len(text) > 90:
            errors.append(f"Long headline {i+1} too long: {len(text)} chars (max: 90) - \"{text[:40]}...\"")

    # Check descriptions (max 90 chars)
    for i, text in enumerate(descriptions):
        if len(text) > 90:
            errors.append(f"Description {i+1} too long: {len(text)} chars (max: 90) - \"{text[:40]}...\"")

    if errors:
        error_msg = "❌ Character limit validation failed:\n    " + "\n    ".join(errors)
        return False, error_msg

    return True, None


# Example usage and testing
if __name__ == "__main__":
    print("PMax Safety Checks Module")
    print("=" * 60)

    # Test deduplication
    print("\nDeduplication Test:")
    test_ids = ['123', '456', '123', '789', '456', '  ', '999']
    unique = deduplicate_asset_ids(test_ids)
    print(f"  Input: {test_ids}")
    print(f"  Output: {unique}")
    print(f"  ✓ Removed {len(test_ids) - len(unique)} duplicates/empty")

    # Test overflow protection
    print("\nOverflow Protection Tests:")
    test_cases = [
        (10, 5, 20, "Safe - no overflow"),
        (15, 8, 20, "Overflow - batch removal needed"),
        (18, 10, 20, "Large overflow"),
    ]

    for current, new, max_val, desc in test_cases:
        needs_overflow, to_remove = check_overflow_protection(current, new, max_val)
        status = "⚠️ OVERFLOW" if needs_overflow else "✓ SAFE"
        print(f"  {status} {desc}")
        print(f"    Current: {current}, New: {new}, Max: {max_val}")
        if needs_overflow:
            print(f"    → Remove {to_remove} first, add {new} new, remove remaining {current - to_remove}")

    # Test minimum text validation
    print("\nMinimum Text Validation Tests:")
    test_cases = [
        (10, 3, 4, "Valid - all minimums met"),
        (2, 1, 4, "Invalid - not enough headlines"),
        (5, 0, 2, "Invalid - no long headlines"),
    ]

    for h, lh, d, desc in test_cases:
        is_valid, error = validate_minimum_text_requirements(h, lh, d)
        status = "✓" if is_valid else "✗"
        print(f"  {status} {desc}")
        print(f"    H: {h}, LH: {lh}, D: {d}")
        if error:
            print(f"    Error: {error.split(':', 1)[1].strip()}")

    print("\n" + "=" * 60)
    print("Module loaded successfully. Import functions to use in your scripts.")
