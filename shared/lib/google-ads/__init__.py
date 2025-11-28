"""
Google Ads Shared Library

Reusable modules for Google Ads Performance Max campaign management.

Modules:
    - pmax_image_validation: Image type validation and aspect ratio detection
    - pmax_safety_checks: Safety patterns for asset management

Usage:
    from google_ads.pmax_image_validation import determine_image_field_type
    from google_ads.pmax_safety_checks import deduplicate_asset_ids
"""

__version__ = '1.0.0'
__author__ = 'PetesBrain'

# Import key functions for easier access
from .pmax_image_validation import (
    determine_image_field_type,
    validate_image_type_requirements,
    get_image_dimensions,
    format_validation_success,
    check_aspect_ratio,
)

from .pmax_safety_checks import (
    deduplicate_asset_ids,
    check_overflow_protection,
    validate_minimum_text_requirements,
    validate_maximum_text_requirements,
    safe_add_remove_strategy,
    filter_empty_strings,
    validate_character_limits,
)

__all__ = [
    # Image validation
    'determine_image_field_type',
    'validate_image_type_requirements',
    'get_image_dimensions',
    'format_validation_success',
    'check_aspect_ratio',
    # Safety checks
    'deduplicate_asset_ids',
    'check_overflow_protection',
    'validate_minimum_text_requirements',
    'validate_maximum_text_requirements',
    'safe_add_remove_strategy',
    'filter_empty_strings',
    'validate_character_limits',
]
