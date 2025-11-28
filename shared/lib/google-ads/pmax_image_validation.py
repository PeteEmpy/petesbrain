"""
Google Ads Performance Max Image Validation Module

Reusable functions for validating PMax image assets against requirements.

Key Features:
- Auto-detect image field types from dimensions
- Validate minimum image requirements
- Check aspect ratios
- Report missing types with actionable feedback

Usage:
    from pmax_image_validation import (
        determine_image_field_type,
        validate_image_type_requirements,
        get_image_dimensions
    )

    # Get dimensions from API
    dimensions = get_image_dimensions(headers, customer_id, ['123', '456', '789'])

    # Auto-detect field types
    for img_id, (width, height) in dimensions.items():
        field_type = determine_image_field_type(width, height)
        print(f"{img_id}: {field_type} ({width}×{height})")

    # Validate requirements
    is_valid, error_msg, type_counts = validate_image_type_requirements(
        headers, customer_id, ['123', '456', '789']
    )

    if not is_valid:
        print(error_msg)
"""

import requests
from typing import Dict, List, Tuple

# PMax minimum image requirements
MINIMUM_IMAGE_REQUIREMENTS = {
    'MARKETING_IMAGE': 1,         # At least 1 landscape
    'SQUARE_MARKETING_IMAGE': 1,  # At least 1 square
    # PORTRAIT_MARKETING_IMAGE is optional (0 required)
}


def determine_image_field_type(width: int, height: int) -> str:
    """
    Determine the correct PMax image field type based on dimensions.

    Args:
        width: Image width in pixels
        height: Image height in pixels

    Returns:
        Field type: MARKETING_IMAGE, SQUARE_MARKETING_IMAGE, or PORTRAIT_MARKETING_IMAGE

    Aspect Ratio Thresholds:
        - Square (0.9 - 1.1): SQUARE_MARKETING_IMAGE (e.g., 1200×1200, 1:1)
        - Portrait (0.7 - 0.9): PORTRAIT_MARKETING_IMAGE (e.g., 960×1200, 4:5 = 0.8)
        - Landscape (anything else): MARKETING_IMAGE (e.g., 1200×628, 1.91:1)

    Examples:
        >>> determine_image_field_type(1200, 1200)
        'SQUARE_MARKETING_IMAGE'

        >>> determine_image_field_type(1200, 628)
        'MARKETING_IMAGE'

        >>> determine_image_field_type(960, 1200)
        'PORTRAIT_MARKETING_IMAGE'
    """
    if width == 0 or height == 0:
        return 'MARKETING_IMAGE'  # Default fallback

    aspect_ratio = width / height

    if 0.9 <= aspect_ratio <= 1.1:
        return 'SQUARE_MARKETING_IMAGE'
    elif 0.7 <= aspect_ratio <= 0.9:
        return 'PORTRAIT_MARKETING_IMAGE'
    else:
        return 'MARKETING_IMAGE'


def get_image_dimensions(headers: dict, customer_id: str, asset_ids: List[str]) -> Dict[str, Tuple[int, int]]:
    """
    Query Google Ads API for image dimensions.

    Args:
        headers: HTTP headers with OAuth token
        customer_id: Google Ads customer ID (formatted with dashes)
        asset_ids: List of asset IDs to query

    Returns:
        Dictionary mapping asset_id -> (width, height)

    Example:
        >>> dimensions = get_image_dimensions(headers, '857-323-5780', ['123', '456'])
        >>> dimensions
        {'123': (1200, 628), '456': (1200, 1200)}
    """
    if not asset_ids:
        return {}

    asset_ids_str = ', '.join(asset_ids)

    query = f"""
        SELECT
            asset.id,
            asset.image_asset.full_size.width_pixels,
            asset.image_asset.full_size.height_pixels
        FROM asset
        WHERE asset.id IN ({asset_ids_str})
        AND asset.type = 'IMAGE'
    """

    url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/googleAds:search"
    payload = {'query': query}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    results = resp.json().get('results', [])

    dimensions = {}
    for result in results:
        asset_id = str(result.get('asset', {}).get('id'))
        width = int(result.get('asset', {}).get('imageAsset', {}).get('fullSize', {}).get('widthPixels', 0))
        height = int(result.get('asset', {}).get('imageAsset', {}).get('fullSize', {}).get('heightPixels', 0))
        dimensions[asset_id] = (width, height)

    return dimensions


def validate_image_type_requirements(headers: dict, customer_id: str,
                                     image_ids: List[str]) -> Tuple[bool, str, dict]:
    """
    Validate that image IDs meet PMax minimum requirements.

    Checks:
    - At least 1 landscape (MARKETING_IMAGE)
    - At least 1 square (SQUARE_MARKETING_IMAGE)
    - Portrait is optional

    Args:
        headers: HTTP headers with OAuth token
        customer_id: Google Ads customer ID (formatted with dashes)
        image_ids: List of asset IDs to validate

    Returns:
        Tuple of (is_valid, error_message, type_counts)
        - is_valid: True if requirements met, False otherwise
        - error_message: Detailed error message if invalid (None if valid)
        - type_counts: Dictionary of field_type -> count

    Example:
        >>> is_valid, error, counts = validate_image_type_requirements(
        ...     headers, '857-323-5780', ['123', '456', '789']
        ... )
        >>> if not is_valid:
        ...     print(error)
        >>> counts
        {'MARKETING_IMAGE': 2, 'SQUARE_MARKETING_IMAGE': 1, 'PORTRAIT_MARKETING_IMAGE': 0}
    """
    if not image_ids:
        return False, "No images provided", {}

    # Get dimensions for all images
    dimensions = get_image_dimensions(headers, customer_id, image_ids)

    # Count by type
    type_counts = {
        'MARKETING_IMAGE': 0,
        'SQUARE_MARKETING_IMAGE': 0,
        'PORTRAIT_MARKETING_IMAGE': 0
    }

    for img_id in image_ids:
        width, height = dimensions.get(img_id, (0, 0))
        field_type = determine_image_field_type(width, height)
        type_counts[field_type] = type_counts.get(field_type, 0) + 1

    # Check minimum requirements
    missing_types = []
    for img_type, min_count in MINIMUM_IMAGE_REQUIREMENTS.items():
        if type_counts.get(img_type, 0) < min_count:
            missing_types.append(img_type)

    if missing_types:
        # Build detailed error message
        type_names = {
            'MARKETING_IMAGE': 'landscape',
            'SQUARE_MARKETING_IMAGE': 'square',
            'PORTRAIT_MARKETING_IMAGE': 'portrait'
        }

        missing_names = [type_names[t] for t in missing_types]

        error_msg = (
            f"❌ VALIDATION FAILED: New images don't meet PMax requirements\n"
            f"    Missing required types: {', '.join(missing_types)}\n"
            f"    Current distribution:\n"
            f"      - Landscape (MARKETING_IMAGE): {type_counts['MARKETING_IMAGE']}\n"
            f"      - Square (SQUARE_MARKETING_IMAGE): {type_counts['SQUARE_MARKETING_IMAGE']}\n"
            f"      - Portrait (PORTRAIT_MARKETING_IMAGE): {type_counts.get('PORTRAIT_MARKETING_IMAGE', 0)}\n"
            f"    Requirements:\n"
            f"      - At least 1 landscape (MARKETING_IMAGE)\n"
            f"      - At least 1 square (SQUARE_MARKETING_IMAGE)\n"
            f"    Fix: Add missing {' and '.join(missing_names)} image(s) before continuing."
        )
        return False, error_msg, type_counts

    # Validation passed
    return True, None, type_counts


def format_validation_success(type_counts: dict) -> str:
    """
    Format validation success message showing image distribution.

    Args:
        type_counts: Dictionary of field_type -> count

    Returns:
        Formatted success message

    Example:
        >>> counts = {'MARKETING_IMAGE': 3, 'SQUARE_MARKETING_IMAGE': 2, 'PORTRAIT_MARKETING_IMAGE': 1}
        >>> print(format_validation_success(counts))
        ✅ Validation passed - Image distribution:
           Landscape: 3
           Square: 2
           Portrait: 1
    """
    msg = "✅ Validation passed - Image distribution:\n"
    msg += f"   Landscape: {type_counts.get('MARKETING_IMAGE', 0)}\n"
    msg += f"   Square: {type_counts.get('SQUARE_MARKETING_IMAGE', 0)}\n"
    msg += f"   Portrait: {type_counts.get('PORTRAIT_MARKETING_IMAGE', 0)}"
    return msg


def check_aspect_ratio(width: int, height: int) -> Tuple[float, str]:
    """
    Calculate aspect ratio and return classification.

    Args:
        width: Image width in pixels
        height: Image height in pixels

    Returns:
        Tuple of (aspect_ratio, classification)
        - aspect_ratio: Width/height ratio
        - classification: 'landscape', 'square', or 'portrait'

    Example:
        >>> check_aspect_ratio(1200, 628)
        (1.91, 'landscape')

        >>> check_aspect_ratio(1200, 1200)
        (1.0, 'square')
    """
    if height == 0:
        return 0.0, 'unknown'

    ratio = width / height

    if 0.9 <= ratio <= 1.1:
        return ratio, 'square'
    elif ratio < 0.9:
        return ratio, 'portrait'
    else:
        return ratio, 'landscape'


# Example usage and testing
if __name__ == "__main__":
    print("PMax Image Validation Module")
    print("=" * 60)

    # Test aspect ratio detection
    test_cases = [
        (1200, 628, "MARKETING_IMAGE"),      # 1.91:1 landscape
        (1200, 1200, "SQUARE_MARKETING_IMAGE"),  # 1:1 square
        (960, 1200, "PORTRAIT_MARKETING_IMAGE"), # 4:5 portrait
        (1600, 900, "MARKETING_IMAGE"),      # 16:9 landscape
        (1080, 1080, "SQUARE_MARKETING_IMAGE"),  # 1:1 square
    ]

    print("\nAspect Ratio Detection Tests:")
    for width, height, expected in test_cases:
        result = determine_image_field_type(width, height)
        ratio, classification = check_aspect_ratio(width, height)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {width}×{height} ({ratio:.2f}:1) → {result} ({classification})")

    print("\n" + "=" * 60)
    print("Module loaded successfully. Import functions to use in your scripts.")
