"""
Generic Spreadsheet → Google Ads Framework

Universal framework for applying Google Sheets data to Google Ads campaigns.

Based on the Smythson asset swap implementation, this provides a reusable
pattern for:
- Reading data from Google Sheets
- Mapping spreadsheet rows to Google Ads entities
- Applying changes with validation and safety checks
- Dry-run and preview capabilities

Key Features:
- Client-agnostic (works for any Google Ads account)
- Validation-before-mutation pattern
- Add-before-remove safety
- Comprehensive error handling
- Progress tracking and reporting

Architecture:
    Google Sheet → SheetReader → EntityMapper → Validator → Mutator → Google Ads API

Usage:
    from spreadsheet_to_ads_framework import (
        SpreadsheetToAdsApplication,
        EntityType,
        ValidationMode
    )

    # Create application instance
    app = SpreadsheetToAdsApplication(
        customer_id='8573235780',
        manager_id='2569949686',
        spreadsheet_id='1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g'
    )

    # Configure entity mapping
    app.configure_entity_type(EntityType.PMAX_ASSET_GROUP)

    # Add validation rules
    app.add_validator(validate_image_requirements)
    app.add_validator(validate_text_requirements)

    # Preview changes
    preview = app.preview_changes(sheet_name='UK')

    # Apply changes
    results = app.apply_changes(sheet_name='UK', dry_run=False)
"""

import sys
import os
from enum import Enum
from typing import List, Dict, Callable, Optional, Tuple, Any
from dataclasses import dataclass
import requests

# Add MCP server to path for OAuth
MCP_SERVER_PATH = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server'
sys.path.insert(0, MCP_SERVER_PATH)

from dotenv import load_dotenv
load_dotenv(os.path.join(MCP_SERVER_PATH, '.env'))

from oauth.google_auth import get_headers_with_auto_token, format_customer_id


class EntityType(Enum):
    """Supported Google Ads entity types."""
    PMAX_ASSET_GROUP = "pmax_asset_group"
    CAMPAIGN = "campaign"
    AD_GROUP = "ad_group"
    KEYWORD = "keyword"


class ValidationMode(Enum):
    """Validation strictness levels."""
    STRICT = "strict"      # Fail on any validation error
    LENIENT = "lenient"    # Warn on validation errors, continue
    SKIP = "skip"          # No validation


@dataclass
class EntityMatch:
    """Represents a matched entity from spreadsheet to Google Ads."""
    sheet_row: int
    campaign_name: str
    entity_name: str
    entity_id: str
    data: Dict[str, Any]


@dataclass
class ValidationResult:
    """Result of entity validation."""
    is_valid: bool
    entity_name: str
    errors: List[str]
    warnings: List[str]


@dataclass
class ApplicationResult:
    """Result of applying changes to Google Ads."""
    entity_name: str
    success: bool
    operations_performed: int
    error_message: Optional[str]


class SpreadsheetToAdsApplication:
    """
    Generic framework for applying Google Sheets data to Google Ads.

    Provides a reusable pattern for spreadsheet-driven bulk updates with
    safety checks, validation, and dry-run capabilities.
    """

    def __init__(self, customer_id: str, manager_id: Optional[str],
                 spreadsheet_id: str, validation_mode: ValidationMode = ValidationMode.STRICT):
        """
        Initialize the application framework.

        Args:
            customer_id: Google Ads customer ID
            manager_id: Manager account ID (optional)
            spreadsheet_id: Google Sheets spreadsheet ID
            validation_mode: How strict to be with validation
        """
        self.customer_id = customer_id
        self.manager_id = manager_id
        self.spreadsheet_id = spreadsheet_id
        self.validation_mode = validation_mode

        self.entity_type = None
        self.validators: List[Callable] = []
        self.preprocessors: List[Callable] = []
        self.postprocessors: List[Callable] = []

        # Setup headers
        self.headers = get_headers_with_auto_token()
        if manager_id:
            self.headers['login-customer-id'] = format_customer_id(manager_id)

    def configure_entity_type(self, entity_type: EntityType):
        """Set the entity type this application will work with."""
        self.entity_type = entity_type

    def add_validator(self, validator_func: Callable):
        """
        Add a validation function.

        Validator signature: func(entity_data) -> ValidationResult
        """
        self.validators.append(validator_func)

    def add_preprocessor(self, preprocessor_func: Callable):
        """
        Add a preprocessor function (runs before validation).

        Preprocessor signature: func(sheet_data) -> processed_data
        """
        self.preprocessors.append(preprocessor_func)

    def add_postprocessor(self, postprocessor_func: Callable):
        """
        Add a postprocessor function (runs after successful application).

        Postprocessor signature: func(results) -> None
        """
        self.postprocessors.append(postprocessor_func)

    def read_sheet_data(self, sheet_name: str, range_spec: str) -> List[List[str]]:
        """
        Read data from Google Sheets.

        Args:
            sheet_name: Name of the sheet tab
            range_spec: Range specification (e.g., 'A2:BU100')

        Returns:
            List of rows, each row is a list of cell values

        Note:
            Requires MCP Google Sheets server or direct API access
        """
        # TODO: Implement via MCP Google Sheets server
        # For now, this is a placeholder showing the interface
        raise NotImplementedError(
            "Sheet reading not yet implemented. "
            "Use MCP Google Sheets server or implement direct API access."
        )

    def find_entity_by_name(self, campaign_name: str, entity_name: str) -> Optional[str]:
        """
        Find a Google Ads entity by campaign and entity name.

        Args:
            campaign_name: Campaign name to search within
            entity_name: Entity name (e.g., asset group name)

        Returns:
            Entity ID if found, None otherwise
        """
        formatted_cid = format_customer_id(self.customer_id)

        if self.entity_type == EntityType.PMAX_ASSET_GROUP:
            query = f"""
                SELECT
                    campaign.name,
                    asset_group.name,
                    asset_group.id
                FROM asset_group
                WHERE campaign.name = '{campaign_name}'
                AND asset_group.name = '{entity_name}'
                AND campaign.advertising_channel_type = 'PERFORMANCE_MAX'
            """
        else:
            raise NotImplementedError(f"Entity type {self.entity_type} not yet supported")

        url = f"https://googleads.googleapis.com/v22/customers/{formatted_cid}/googleAds:search"
        payload = {'query': query}

        resp = requests.post(url, headers=self.headers, json=payload)
        resp.raise_for_status()

        results = resp.json().get('results', [])

        if len(results) == 0:
            return None
        elif len(results) == 1:
            if self.entity_type == EntityType.PMAX_ASSET_GROUP:
                return str(results[0].get('assetGroup', {}).get('id'))
        else:
            raise ValueError(f"Multiple matches found for {campaign_name} / {entity_name}")

    def validate_entity(self, entity_data: Dict) -> ValidationResult:
        """
        Run all validators on an entity.

        Args:
            entity_data: Entity data to validate

        Returns:
            ValidationResult with any errors/warnings
        """
        errors = []
        warnings = []

        for validator in self.validators:
            result = validator(entity_data)
            errors.extend(result.errors)
            warnings.extend(result.warnings)

        is_valid = len(errors) == 0 if self.validation_mode == ValidationMode.STRICT else True

        return ValidationResult(
            is_valid=is_valid,
            entity_name=entity_data.get('entity_name', 'Unknown'),
            errors=errors,
            warnings=warnings
        )

    def preview_changes(self, sheet_name: str) -> List[EntityMatch]:
        """
        Preview what changes would be made without applying them.

        Args:
            sheet_name: Sheet tab to process

        Returns:
            List of EntityMatch objects showing what would be updated
        """
        # Read sheet data
        # Map to entities
        # Return matches
        raise NotImplementedError("Preview not yet implemented")

    def apply_changes(self, sheet_name: str, dry_run: bool = False) -> List[ApplicationResult]:
        """
        Apply changes from spreadsheet to Google Ads.

        Args:
            sheet_name: Sheet tab to process
            dry_run: If True, validate and preview but don't apply

        Returns:
            List of ApplicationResult objects showing outcomes
        """
        raise NotImplementedError("Apply changes not yet implemented")


# Example validator functions
def validate_pmax_text_assets(entity_data: Dict) -> ValidationResult:
    """Validate PMax text asset requirements."""
    errors = []
    warnings = []

    headlines = entity_data.get('headlines', [])
    long_headlines = entity_data.get('long_headlines', [])
    descriptions = entity_data.get('descriptions', [])

    if len(headlines) < 3:
        errors.append(f"Not enough headlines: {len(headlines)} (minimum: 3)")

    if len(long_headlines) < 1:
        errors.append(f"Not enough long headlines: {len(long_headlines)} (minimum: 1)")

    if len(descriptions) < 2:
        errors.append(f"Not enough descriptions: {len(descriptions)} (minimum: 2)")

    if len(headlines) > 15:
        warnings.append(f"Too many headlines: {len(headlines)} (maximum: 15)")

    return ValidationResult(
        is_valid=len(errors) == 0,
        entity_name=entity_data.get('entity_name', 'Unknown'),
        errors=errors,
        warnings=warnings
    )


def validate_pmax_image_assets(entity_data: Dict) -> ValidationResult:
    """Validate PMax image asset requirements."""
    errors = []
    warnings = []

    images = entity_data.get('images', [])

    if len(images) == 0:
        errors.append("No images provided")

    # Check for minimum types (would need actual dimension data)
    # This is a placeholder - real implementation would use pmax_image_validation module

    return ValidationResult(
        is_valid=len(errors) == 0,
        entity_name=entity_data.get('entity_name', 'Unknown'),
        errors=errors,
        warnings=warnings
    )


# Documentation and usage examples
USAGE_EXAMPLE = """
Example Usage:
--------------

from spreadsheet_to_ads_framework import SpreadsheetToAdsApplication, EntityType

# Setup application
app = SpreadsheetToAdsApplication(
    customer_id='8573235780',
    manager_id='2569949686',
    spreadsheet_id='1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g'
)

# Configure for PMax asset groups
app.configure_entity_type(EntityType.PMAX_ASSET_GROUP)

# Add validators
app.add_validator(validate_pmax_text_assets)
app.add_validator(validate_pmax_image_assets)

# Preview changes
print("Previewing changes...")
matches = app.preview_changes(sheet_name='UK')
print(f"Found {len(matches)} entities to update")

# Dry run
print("Running validation...")
results = app.apply_changes(sheet_name='UK', dry_run=True)

for result in results:
    if result.success:
        print(f"✓ {result.entity_name} - validation passed")
    else:
        print(f"✗ {result.entity_name} - {result.error_message}")

# Apply changes
if input("Apply changes? (yes/no): ") == "yes":
    results = app.apply_changes(sheet_name='UK', dry_run=False)
    print(f"Applied changes to {sum(1 for r in results if r.success)} entities")
"""


if __name__ == "__main__":
    print("=" * 80)
    print("Spreadsheet → Google Ads Framework")
    print("=" * 80)
    print("\nThis is a framework module, not a standalone script.")
    print("Import and use in your application scripts.")
    print(USAGE_EXAMPLE)
    print("=" * 80)
