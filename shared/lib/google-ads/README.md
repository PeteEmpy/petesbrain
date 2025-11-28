# Google Ads Shared Library

Reusable modules for Google Ads Performance Max campaign management, extracted from the Smythson asset swap project.

## Overview

This library provides battle-tested patterns and functions for managing PMax campaigns at scale, with emphasis on safety, validation, and error prevention.

## Modules

### 1. `pmax_image_validation.py`

**Purpose:** Validate PMax image assets against requirements

**Key Functions:**
- `determine_image_field_type(width, height)` - Auto-detect field type from dimensions
- `validate_image_type_requirements(headers, customer_id, image_ids)` - Check minimum requirements
- `get_image_dimensions(headers, customer_id, asset_ids)` - Query dimensions from API
- `format_validation_success(type_counts)` - Format success message

**Usage:**
```python
from google_ads.pmax_image_validation import (
    determine_image_field_type,
    validate_image_type_requirements
)

# Auto-detect field type
field_type = determine_image_field_type(1200, 628)
# Returns: 'MARKETING_IMAGE' (landscape)

# Validate requirements
is_valid, error, counts = validate_image_type_requirements(
    headers, customer_id, ['123', '456', '789']
)

if not is_valid:
    print(error)  # Detailed error with missing types
```

**Aspect Ratio Thresholds:**
- **Square (0.9 - 1.1):** SQUARE_MARKETING_IMAGE (e.g., 1200×1200, 1:1)
- **Portrait (0.7 - 0.9):** PORTRAIT_MARKETING_IMAGE (e.g., 960×1200, 4:5)
- **Landscape (anything else):** MARKETING_IMAGE (e.g., 1200×628, 1.91:1)

**PMax Requirements:**
- Minimum: 1 landscape + 1 square (portrait optional)
- Maximum: 20 images per asset group

---

### 2. `pmax_safety_checks.py`

**Purpose:** Safety patterns to prevent common PMax errors

**Key Functions:**
- `deduplicate_asset_ids(asset_ids)` - Remove duplicates while preserving order
- `check_overflow_protection(current_count, new_count, max_limit)` - Calculate safe batch removal
- `validate_minimum_text_requirements(headlines, long_headlines, descriptions)` - Check PMax minimums
- `validate_maximum_text_requirements(...)` - Check PMax maximums
- `validate_character_limits(headlines, long_headlines, descriptions)` - Check character limits
- `safe_add_remove_strategy(current, new, max_limit)` - Generate safe operation sequence

**Usage:**
```python
from google_ads.pmax_safety_checks import (
    deduplicate_asset_ids,
    check_overflow_protection,
    validate_minimum_text_requirements
)

# Remove duplicates (prevents DUPLICATE_RESOURCE error)
unique_ids = deduplicate_asset_ids(['123', '456', '123', '789'])
# Returns: ['123', '456', '789']

# Check overflow (prevents exceeding maximum)
needs_batch, to_remove_first = check_overflow_protection(
    current_count=15,
    new_count=8,
    max_limit=20
)
# Returns: (True, 3) - remove 3 first to make room

# Validate minimums
is_valid, error = validate_minimum_text_requirements(
    headlines=10,
    long_headlines=3,
    descriptions=4
)
# Returns: (True, None) - all minimums met
```

**PMax Text Requirements:**
- Minimum: 3 headlines, 1 long headline, 2 descriptions
- Maximum: 15 headlines, 5 long headlines, 5 descriptions
- Character limits: 30 (headlines), 90 (long headlines/descriptions)

**Safety Patterns:**
1. **Add-Before-Remove:** Never leave asset groups empty
2. **Overflow Protection:** Batch removal when current + new > limit
3. **Deduplication:** Prevent DUPLICATE_RESOURCE errors
4. **Validation Gates:** Check requirements before mutations

---

### 3. `spreadsheet_to_ads_framework.py`

**Purpose:** Generic framework for applying Google Sheets data to Google Ads

**Status:** Framework structure complete, implementation in progress

**Architecture:**
```
Google Sheet → SheetReader → EntityMapper → Validator → Mutator → Google Ads API
```

**Key Classes:**
- `SpreadsheetToAdsApplication` - Main application class
- `EntityType` - Enum of supported entities (PMAX_ASSET_GROUP, CAMPAIGN, etc.)
- `ValidationMode` - STRICT, LENIENT, or SKIP
- `ValidationResult` - Validation outcome
- `ApplicationResult` - Application outcome

**Planned Usage:**
```python
from google_ads.spreadsheet_to_ads_framework import (
    SpreadsheetToAdsApplication,
    EntityType
)

# Setup application
app = SpreadsheetToAdsApplication(
    customer_id='8573235780',
    manager_id='2569949686',
    spreadsheet_id='1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g'
)

# Configure
app.configure_entity_type(EntityType.PMAX_ASSET_GROUP)
app.add_validator(validate_pmax_text_assets)
app.add_validator(validate_pmax_image_assets)

# Preview
matches = app.preview_changes(sheet_name='UK')

# Apply
results = app.apply_changes(sheet_name='UK', dry_run=False)
```

**Note:** This is a framework structure showing the desired interface. Implementation is in progress and will be completed in future iterations.

---

## Installation

Add the library to your Python path:

```python
import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/shared/lib')

# Now you can import
from google_ads import pmax_image_validation, pmax_safety_checks
```

Or use relative imports if your script is in the PetesBrain structure:

```python
# From /clients/{client}/scripts/
sys.path.insert(0, '../../../shared/lib')
from google_ads import pmax_image_validation
```

---

## Examples

### Example 1: Validate Images Before Applying

```python
import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/shared/lib')

from google_ads.pmax_image_validation import validate_image_type_requirements
from google_ads.pmax_safety_checks import deduplicate_asset_ids

# Your image IDs from spreadsheet
image_ids = ['123', '456', '789', '123']  # Has duplicate

# Deduplicate first
unique_ids = deduplicate_asset_ids(image_ids)
print(f"Deduplication: {len(image_ids)} → {len(unique_ids)} unique")

# Validate requirements
is_valid, error, counts = validate_image_type_requirements(
    headers, customer_id, unique_ids
)

if is_valid:
    print("✅ Validation passed!")
    print(f"  Landscape: {counts['MARKETING_IMAGE']}")
    print(f"  Square: {counts['SQUARE_MARKETING_IMAGE']}")
    print(f"  Portrait: {counts['PORTRAIT_MARKETING_IMAGE']}")

    # Safe to apply images...
else:
    print(error)
    # Fix spreadsheet before continuing
```

### Example 2: Safe Add-Remove with Overflow Protection

```python
from google_ads.pmax_safety_checks import check_overflow_protection

current_images = 15  # Currently in asset group
new_images = 8       # Want to add
max_limit = 20

needs_overflow, to_remove_first = check_overflow_protection(
    current_images, new_images, max_limit
)

if needs_overflow:
    print(f"⚠️  Overflow detected!")
    print(f"Strategy: Remove {to_remove_first} first, add {new_images}, remove remaining")

    # Implementation:
    # 1. Remove first batch (to_remove_first images)
    # 2. Add all new images
    # 3. Remove remaining old images
else:
    print(f"✓ Safe to add all new first, then remove old")

    # Implementation:
    # 1. Add all new images
    # 2. Remove all old images
```

### Example 3: Complete Validation Pipeline

```python
from google_ads.pmax_image_validation import validate_image_type_requirements
from google_ads.pmax_safety_checks import (
    deduplicate_asset_ids,
    validate_minimum_text_requirements,
    validate_character_limits
)

def validate_asset_group_data(sheet_row):
    """Validate a complete asset group row from spreadsheet."""

    errors = []

    # 1. Deduplicate images
    unique_images = deduplicate_asset_ids(sheet_row['images'])
    if len(unique_images) < len(sheet_row['images']):
        print(f"⚠️  Removed {len(sheet_row['images']) - len(unique_images)} duplicate images")

    # 2. Validate text minimums
    is_valid, error = validate_minimum_text_requirements(
        len(sheet_row['headlines']),
        len(sheet_row['long_headlines']),
        len(sheet_row['descriptions'])
    )
    if not is_valid:
        errors.append(error)

    # 3. Validate character limits
    is_valid, error = validate_character_limits(
        sheet_row['headlines'],
        sheet_row['long_headlines'],
        sheet_row['descriptions']
    )
    if not is_valid:
        errors.append(error)

    # 4. Validate image requirements
    is_valid, error, counts = validate_image_type_requirements(
        headers, customer_id, unique_images
    )
    if not is_valid:
        errors.append(error)

    # Return results
    if errors:
        return False, errors
    else:
        return True, None
```

---

## Integration with Existing Scripts

These modules are designed to be dropped into existing scripts with minimal changes:

### Before (Smythson-specific):
```python
# Hardcoded validation in script
if len(image_ids) < 2:
    print("Not enough images")
    return False

# Manual deduplication
seen = set()
unique_ids = []
for img_id in image_ids:
    if img_id not in seen:
        unique_ids.append(img_id)
        seen.add(img_id)
```

### After (Using shared library):
```python
from google_ads.pmax_image_validation import validate_image_type_requirements
from google_ads.pmax_safety_checks import deduplicate_asset_ids

# Reusable validation
unique_ids = deduplicate_asset_ids(image_ids)
is_valid, error, counts = validate_image_type_requirements(
    headers, customer_id, unique_ids
)

if not is_valid:
    print(error)
    return False
```

---

## Testing

Each module includes self-test functionality:

```bash
# Test image validation
python3 /Users/administrator/Documents/PetesBrain/shared/lib/google-ads/pmax_image_validation.py

# Test safety checks
python3 /Users/administrator/Documents/PetesBrain/shared/lib/google-ads/pmax_safety_checks.py
```

Expected output shows test cases passing/failing with examples.

---

## Future Enhancements

**Planned additions:**
1. Complete `spreadsheet_to_ads_framework` implementation
2. Budget management validation module
3. Bid strategy safety checks module
4. Multi-account batch operations
5. Performance threshold validation

**Requested features:**
- Submit issues or feature requests to the PetesBrain project

---

## Version History

**v1.0.0 (2025-11-28)**
- Initial release
- Image validation module (complete)
- Safety checks module (complete)
- Spreadsheet framework (structure only)

---

## Credits

Extracted from Smythson Asset Swap project (November 2025) which successfully managed 56 asset groups across 4 regional accounts with zero errors using these patterns.

## License

Internal use only - PetesBrain project
