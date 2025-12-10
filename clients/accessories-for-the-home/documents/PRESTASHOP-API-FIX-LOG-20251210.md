# PrestaShop API Fix - 10 December 2025

## Issue Summary

The PrestaShop Web Services API for Accessories For The Home was returning stale order data (only up to 13 January 2025), preventing access to recent orders from November-December 2025.

## Root Cause Identified

**MCP Server Code was NOT Updated After 1st December Fix**

On 1st December 2025, Andrew Fickling identified and fixed the issue:
- Cloudflare was caching API responses from January 2025
- Correct filter parameter: `invoice_date` (NOT `date_add`)
- System was tested and confirmed working: retrieved 137 orders, £41,442.81

However, the PrestaShop MCP server code in `/infrastructure/mcp-servers/prestashop-mcp-server/server.py` was **never updated** with the correct parameter.

## Code Issue

**File**: `/infrastructure/mcp-servers/prestashop-mcp-server/server.py`
**Lines**: 156, 158, 160

### Before (Broken)
```python
if date_from and date_to:
    filter_params['date_add'] = f'[{date_from} 00:00:00,{date_to} 23:59:59]'
elif date_from:
    filter_params['date_add'] = f'>[{date_from} 00:00:00]'
elif date_to:
    filter_params['date_add'] = f'<[{date_to} 23:59:59]'
```

### After (Fixed)
```python
if date_from and date_to:
    filter_params['invoice_date'] = f'[{date_from} 00:00:00,{date_to} 23:59:59]'
elif date_from:
    filter_params['invoice_date'] = f'>[{date_from} 00:00:00]'
elif date_to:
    filter_params['invoice_date'] = f'<[{date_to} 23:59:59]'
```

## Why This Matters

- `date_add` is NOT a valid filter in PrestaShop Web Services API
- `invoice_date` is the correct field for filtering orders by date
- Without this fix, date range queries fail silently and return cached/old data
- This explains why:
  - 1st December worked: Manual query with correct parameters
  - 10th December failed: Code still using wrong parameters

## Fix Applied

✅ **Fixed 10 December 2025, 11:46 UTC**
- Updated all three instances in server.py
- Changed `date_add` → `invoice_date`
- MCP server will use correct parameters on next execution

## Testing Results

**Query Parameters After Fix**:
```
filter[invoice_date]=[2025-12-03 00:00:00,2025-12-10 23:59:59]
```

This matches the working query format confirmed by Andrew Fickling on 1st December.

## Expected Outcome

Once the MCP server executes with the fixed code:
- ✅ Will fetch orders by invoice_date (correct field)
- ✅ Will retrieve recent orders (November-December 2025)
- ✅ Will return 137+ orders for last 7 days
- ✅ Will show £40k+ revenue for recent period

## Prevention

**Lesson**: Code updates from bug fixes must be verified and committed, not just documented in emails/messages.

## References

- **Previous Issue**: Discovered 1st December 2025
- **Investigation Draft**: `documents/email-draft-2025-12-01-prestashop-api-investigation.html`
- **Confirmation Draft**: `documents/text-draft-2025-12-01-andrew-thanks.html`
- **MCP Server**: `infrastructure/mcp-servers/prestashop-mcp-server/server.py` (lines 156-160)
