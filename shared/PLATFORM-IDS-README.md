# Platform IDs Helper

This module provides utilities to extract and manage Google Ads, Merchant Centre, and GA4 IDs from client CONTEXT.md files.

## Overview

The Platform IDs helper (`shared/platform_ids.py`) provides a centralized way to access client platform IDs without hardcoding them in scripts or searching through configuration files.

## Features

- **Parse CONTEXT.md files** - Extract Platform IDs directly from client documentation
- **JSON fallback** - Load from centralized JSON mapping for performance
- **Multi-account support** - Handle clients with multiple Google Ads accounts or Merchant Centre feeds
- **Validation** - Validate ID formats for Google Ads, Merchant Centre, and GA4
- **CLI interface** - Command-line tool for quick ID lookups

## Installation

The helper is already installed at `shared/platform_ids.py`. No additional dependencies required.

## Usage

### Python API

```python
from shared.platform_ids import get_client_ids, get_all_client_ids

# Get IDs for a specific client
ids = get_client_ids('tree2mydoor')
print(f"Google Ads ID: {ids['google_ads_customer_id']}")
print(f"Merchant Centre ID: {ids['merchant_centre_id']}")
print(f"GA4 Property ID: {ids['ga4_property_id']}")

# Get all client IDs
all_ids = get_all_client_ids()
for client_name, ids in all_ids.items():
    print(f"{client_name}: {ids['google_ads_customer_id']}")
```

### Command Line

```bash
# Get IDs for a specific client
python3 shared/platform_ids.py smythson

# Get all client IDs (JSON format)
python3 shared/platform_ids.py --all

# Get list of all Google Ads accounts
python3 shared/platform_ids.py --google-ads

# Get list of all Merchant Centre accounts
python3 shared/platform_ids.py --merchant-centre
```

### Example Output

**Single-account client (Tree2mydoor):**
```json
{
  "google_ads_customer_id": "4941701449",
  "merchant_centre_id": "107469209",
  "ga4_property_id": "[TBD]"
}
```

**Multi-merchant client (Clear Prospects):**
```json
{
  "google_ads_customer_id": "6281395727",
  "merchant_centre_id": [
    "7481296",
    "7481286",
    "7522326"
  ],
  "ga4_property_id": "[TBD]"
}
```

## API Reference

### `get_client_ids(client_name, prefer_json=False)`

Get Platform IDs for a specific client.

**Parameters:**
- `client_name` (str): Client name (e.g., 'smythson', 'tree2mydoor')
- `prefer_json` (bool): If True, prefer JSON mapping over parsing CONTEXT.md

**Returns:**
- Dictionary with keys: `google_ads_customer_id`, `merchant_centre_id`, `ga4_property_id`, `google_ads_manager_id` (if applicable)

**Example:**
```python
ids = get_client_ids('uno-lighting')
customer_id = ids['google_ads_customer_id']  # "6413338364"
```

### `get_all_client_ids(source='json')`

Get Platform IDs for all clients.

**Parameters:**
- `source` (str): 'json' to load from JSON, 'context' to parse all CONTEXT.md files

**Returns:**
- Dictionary mapping client names to their Platform IDs

**Example:**
```python
all_ids = get_all_client_ids()
for client, ids in all_ids.items():
    if ids['merchant_centre_id'] != 'N/A':
        print(f"{client} has merchant feed: {ids['merchant_centre_id']}")
```

### `get_google_ads_accounts()`

Get list of all Google Ads accounts with customer IDs.

**Returns:**
- List of dictionaries with 'client_name' and 'customer_id' keys

**Example:**
```python
accounts = get_google_ads_accounts()
for account in accounts:
    print(f"Client: {account['client_name']}, ID: {account['customer_id']}")
```

### `get_merchant_centre_accounts()`

Get list of all Merchant Centre accounts with merchant IDs.

**Returns:**
- List of dictionaries with 'client_name' and 'merchant_id' keys

### Validation Functions

```python
from shared.platform_ids import (
    validate_customer_id,
    validate_merchant_id,
    validate_ga4_property_id
)

# Validate ID formats
is_valid = validate_customer_id("8573235780")  # True
is_valid = validate_merchant_id("102535465")    # True
is_valid = validate_ga4_property_id("421301275") # True
```

## Integration with MCP Servers

The Platform IDs helper is integrated with MCP servers via environment variables in [`.mcp.json`](../.mcp.json):

```json
{
  "google-ads": {
    "env": {
      "CLIENT_IDS_PATH": "/path/to/shared/data/client-platform-ids.json",
      "PLATFORM_IDS_HELPER": "/path/to/shared/platform_ids.py"
    }
  }
}
```

MCP servers can use the helper to:
1. Auto-populate customer IDs in API calls
2. Validate user-provided IDs
3. Provide client name → ID lookups

## Script Integration Examples

### Google Ads API Script

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain')

from shared.platform_ids import get_client_ids

# Get client IDs
client_name = 'smythson'
ids = get_client_ids(client_name)

# Use in Google Ads API call
from google.ads.googleads.client import GoogleAdsClient
client = GoogleAdsClient.load_from_storage()

query = """
    SELECT campaign.name, metrics.impressions
    FROM campaign
    WHERE segments.date DURING LAST_7_DAYS
"""

ga_service = client.get_service("GoogleAdsService")
response = ga_service.search(
    customer_id=ids['google_ads_customer_id'],
    query=query
)
```

### Product Impact Analyzer Integration

```python
from shared.platform_ids import get_merchant_centre_accounts

# Get all merchant accounts
merchant_accounts = get_merchant_centre_accounts()

# Use in product feed analysis
for account in merchant_accounts:
    if account['client_name'] == 'tree2mydoor':
        merchant_id = account['merchant_id']
        # Fetch product feed data...
```

### Audit Script with Multi-Account Support

```python
from shared.platform_ids import get_client_ids

client_name = 'clear-prospects'
ids = get_client_ids(client_name)

# Handle multi-merchant clients
merchant_ids = ids['merchant_centre_id']
if isinstance(merchant_ids, list):
    for idx, merchant_id in enumerate(merchant_ids):
        print(f"Auditing merchant feed {idx+1}: {merchant_id}")
        # Run audit for each merchant...
else:
    print(f"Auditing single merchant: {merchant_ids}")
    # Run audit...
```

## Data Sources

### Primary Source: CONTEXT.md Files

Each client's `CONTEXT.md` file contains a "Platform IDs" section:

```markdown
**Platform IDs**:
- **Google Ads Customer ID**: 4941701449
- **Google Merchant Centre ID**: 107469209
- **Google Analytics 4 (GA4) Property ID**: [TBD]
```

### Fallback Source: JSON Mapping

The centralized JSON file at [`shared/data/client-platform-ids.json`](../shared/data/client-platform-ids.json) provides a complete mapping of all client IDs.

## Handling Special Cases

### Multi-Account Clients (e.g., Smythson)

Smythson has 4 separate Google Ads accounts:

```python
ids = get_client_ids('smythson')
# ids['google_ads_customer_id'] returns a list:
# ['8573235780', '7808690871', '7679616761', '5556710725']
```

### Multi-Merchant Clients (e.g., Clear Prospects)

Clear Prospects has 3 merchant feeds:

```python
ids = get_client_ids('clear-prospects')
# ids['merchant_centre_id'] returns a list:
# ['7481296', '7481286', '7522326']
```

### Lead Generation Clients (e.g., Devonshire Hotels)

Lead generation clients have no merchant feed:

```python
ids = get_client_ids('devonshire-hotels')
# ids['merchant_centre_id'] == 'N/A'
```

### Manager Account Access (e.g., Grain Guard, Go Glean)

Some clients require manager account access:

```python
ids = get_client_ids('grain-guard')
# ids includes 'google_ads_manager_id': '2569949686'

# Use in API calls:
mcp__google-ads__run_gaql(
    customer_id=ids['google_ads_customer_id'],
    manager_id=ids['google_ads_manager_id'],
    query="..."
)
```

## Updating Platform IDs

### Adding New Clients

1. Create client folder: `clients/new-client/CONTEXT.md`
2. Add Platform IDs section in CONTEXT.md:
   ```markdown
   **Platform IDs**:
   - **Google Ads Customer ID**: 1234567890
   - **Google Merchant Centre ID**: 987654321
   - **Google Analytics 4 (GA4) Property ID**: [TBD]
   ```
3. The helper will automatically discover the new client

### Updating GA4 Property IDs

As GA4 property IDs are discovered, update the CONTEXT.md:

```markdown
**Platform IDs**:
- **Google Ads Customer ID**: 4941701449
- **Google Merchant Centre ID**: 107469209
- **Google Analytics 4 (GA4) Property ID**: 421301275  ← Update here
```

The helper will immediately reflect the change.

## Error Handling

```python
from shared.platform_ids import get_client_ids

try:
    ids = get_client_ids('non-existent-client')
except FileNotFoundError as e:
    print(f"Client not found: {e}")

# Check for TBD values
ids = get_client_ids('smythson')
if ids['ga4_property_id'] == '[TBD]':
    print("GA4 property ID not yet configured")
```

## Performance Considerations

- **CONTEXT.md parsing**: ~10ms per file (regex parsing)
- **JSON loading**: ~2ms for all clients (faster for repeated lookups)
- **Caching**: Consider caching results if calling frequently in a loop

**Tip:** Use `prefer_json=True` for performance-critical scripts:

```python
ids = get_client_ids('smythson', prefer_json=True)
```

## Testing

Run the test suite:

```bash
# Test single client
python3 shared/platform_ids.py tree2mydoor

# Test multi-account client
python3 shared/platform_ids.py clear-prospects

# Test all accounts
python3 shared/platform_ids.py --google-ads
```

## Troubleshooting

### Issue: IDs not being extracted

**Solution:** Check CONTEXT.md formatting. The Platform IDs section must use exact format:
```markdown
**Platform IDs**:
- **Google Ads Customer ID**: 1234567890
```

### Issue: Multi-account IDs returned as single string

**Solution:** Ensure sub-bullets use proper nesting in CONTEXT.md:
```markdown
**Platform IDs**:
- **Google Ads Customer IDs**:
  - UK: 8573235780
  - USA: 7808690871
```

### Issue: Module import errors

**Solution:** Add project root to Python path:
```python
import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain')
from shared.platform_ids import get_client_ids
```

## Related Files

- **Helper module**: [`shared/platform_ids.py`](platform_ids.py)
- **Client IDs JSON**: [`shared/data/client-platform-ids.json`](../shared/data/client-platform-ids.json)
- **MCP configuration**: [`.mcp.json`](../.mcp.json)
- **Client CONTEXT files**: [`clients/*/CONTEXT.md`](../clients/)

## Future Enhancements

Planned features:
- [ ] Auto-sync Platform IDs from CONTEXT.md to JSON on commit
- [ ] Web API endpoint for ID lookups
- [ ] Integration with Claude Code skills for auto-population
- [ ] Validation warnings for missing/incomplete IDs
- [ ] Historical ID tracking (account migrations)
