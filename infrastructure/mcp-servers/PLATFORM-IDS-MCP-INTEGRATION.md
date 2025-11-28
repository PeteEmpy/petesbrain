# Platform IDs MCP Integration

This document explains how the Platform IDs helper is integrated with MCP servers to provide automatic ID lookups from CONTEXT.md files.

## Overview

The MCP servers (Google Ads, Google Analytics) now have direct access to client platform IDs stored in CONTEXT.md files through the `platform_ids.py` helper module. This enables:

1. **Automatic ID lookups** - Query customer IDs by client name
2. **Validation** - Verify ID formats before API calls
3. **Multi-account support** - Handle clients with multiple accounts
4. **Single source of truth** - All IDs maintained in CONTEXT.md

## Configuration

The integration is configured via environment variables in [`.mcp.json`](../../.mcp.json):

```json
{
  "google-ads": {
    "env": {
      "CLIENT_IDS_PATH": "/path/to/shared/data/client-platform-ids.json",
      "PLATFORM_IDS_HELPER": "/path/to/shared/platform_ids.py"
    }
  },
  "google-analytics": {
    "env": {
      "CLIENT_IDS_PATH": "/path/to/shared/data/client-platform-ids.json",
      "PLATFORM_IDS_HELPER": "/path/to/shared/platform_ids.py"
    }
  }
}
```

## New MCP Tool: `get_client_platform_ids`

### Usage in Claude Code

You can now look up client IDs directly through the MCP:

```
"Get the Google Ads customer ID for Tree2mydoor"
```

Claude will use:
```python
mcp__google-ads__get_client_platform_ids(client_name="tree2mydoor")
```

**Returns:**
```json
{
  "google_ads_customer_id": "4941701449",
  "merchant_centre_id": "107469209",
  "ga4_property_id": "[TBD]"
}
```

### Multi-Account Clients

For clients with multiple accounts (like Clear Prospects or Smythson):

```python
mcp__google-ads__get_client_platform_ids(client_name="clear-prospects")
```

**Returns:**
```json
{
  "google_ads_customer_id": "6281395727",
  "merchant_centre_id": ["7481296", "7481286", "7522326"],
  "ga4_property_id": "[TBD]"
}
```

### Clients with Manager Access

For clients requiring manager account access (like Grain Guard):

```python
mcp__google-ads__get_client_platform_ids(client_name="grain-guard")
```

**Returns:**
```json
{
  "google_ads_customer_id": "4391940141",
  "google_ads_manager_id": "2569949686",
  "merchant_centre_id": "5354444061",
  "ga4_property_id": "[TBD]"
}
```

## Workflow Examples

### Example 1: Running a GAQL Query

**Before (manual lookup):**
```
User: "Show me Tree2mydoor campaign performance"
Claude: *searches for customer ID in config files*
Claude: Uses run_gaql with hardcoded customer_id="4941701449"
```

**After (automatic lookup):**
```
User: "Show me Tree2mydoor campaign performance"
Claude: Uses get_client_platform_ids("tree2mydoor")
Claude: Extracts customer_id from result
Claude: Uses run_gaql with the extracted customer_id
```

### Example 2: Multi-Account Analysis

```
User: "Analyze Smythson performance across all regions"
Claude: Uses get_client_platform_ids("smythson")
Claude: Detects multiple customer IDs in response
Claude: Loops through all 4 accounts (UK, USA, EUR, ROW)
Claude: Aggregates results and presents unified analysis
```

### Example 3: Manager Account Access

```
User: "Query Go Glean performance"
Claude: Uses get_client_platform_ids("go-glean")
Claude: Detects google_ads_manager_id in response
Claude: Uses run_gaql with both customer_id AND manager_id parameters
```

## Integration with Skills

Claude Code skills can now leverage the MCP tool for automatic ID resolution:

### Campaign Audit Skill

```markdown
**Skill: google-ads-campaign-audit**

When user requests an audit for a client:
1. Use get_client_platform_ids(client_name) to get IDs
2. Check for manager_id in response
3. Use run_gaql with appropriate parameters
4. Parse results and generate audit report
```

### Email Draft Generator Skill

```markdown
**Skill: email-draft-generator**

When drafting client emails:
1. Use get_client_platform_ids(client_name) to verify client exists
2. Load CONTEXT.md from clients/{client_name}/CONTEXT.md
3. Extract strategic context and communication preferences
4. Generate email with appropriate tone and content
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ User Request: "Get Tree2mydoor performance"                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Claude Code invokes MCP tool:                               │
│ mcp__google-ads__get_client_platform_ids("tree2mydoor")     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ MCP Server loads platform_ids.py helper                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Helper reads: clients/tree2mydoor/CONTEXT.md                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Helper parses Platform IDs section using regex              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Returns JSON:                                                │
│ {                                                            │
│   "google_ads_customer_id": "4941701449",                   │
│   "merchant_centre_id": "107469209",                        │
│   "ga4_property_id": "[TBD]"                                │
│ }                                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Claude Code uses customer_id in subsequent run_gaql call    │
└─────────────────────────────────────────────────────────────┘
```

## Error Handling

### Client Not Found

```python
mcp__google-ads__get_client_platform_ids("non-existent-client")
# Error: Client not found: non-existent-client.
# Check that clients/non-existent-client/CONTEXT.md exists.
```

### Platform IDs Helper Not Available

If the helper module is not properly configured:

```
Error: Platform IDs helper not available.
Check PLATFORM_IDS_HELPER environment variable.
```

**Solution:** Verify `.mcp.json` contains correct paths to `platform_ids.py`

### IDs Not Populated in CONTEXT.md

If Platform IDs section is missing or incomplete:

```python
ids = mcp__google-ads__get_client_platform_ids("positive-bakes")
# Returns: {
#   "google_ads_customer_id": "2401439541",
#   "merchant_centre_id": "[TBD]",
#   "ga4_property_id": "[TBD]"
# }
```

Claude should recognize `[TBD]` and inform the user that the ID needs to be added to CONTEXT.md.

## Testing the Integration

### Test 1: Single Account Client

```bash
# In Claude Code, ask:
"Get platform IDs for tree2mydoor"

# Expected tool call:
mcp__google-ads__get_client_platform_ids(client_name="tree2mydoor")

# Expected result:
{
  "google_ads_customer_id": "4941701449",
  "merchant_centre_id": "107469209",
  "ga4_property_id": "[TBD]"
}
```

### Test 2: Multi-Merchant Client

```bash
# In Claude Code, ask:
"Get platform IDs for clear-prospects"

# Expected result includes multiple merchant IDs:
{
  "google_ads_customer_id": "6281395727",
  "merchant_centre_id": ["7481296", "7481286", "7522326"],
  "ga4_property_id": "[TBD]"
}
```

### Test 3: Manager Account Access

```bash
# In Claude Code, ask:
"Get platform IDs for go-glean"

# Expected result includes manager_id:
{
  "google_ads_customer_id": "8492163737",
  "google_ads_manager_id": "2569949686",
  "merchant_centre_id": "5320484948",
  "ga4_property_id": "[TBD]"
}
```

## Benefits

### Before Integration

❌ Manual ID lookups in config files
❌ Hardcoded customer IDs in queries
❌ No validation of ID formats
❌ Repeated searches for multi-account clients
❌ Risk of using wrong IDs

### After Integration

✅ Automatic ID lookups from CONTEXT.md
✅ Single source of truth for all IDs
✅ Built-in validation and error handling
✅ Multi-account support out of the box
✅ Skills can auto-populate customer IDs
✅ Consistent ID usage across all tools

## Future Enhancements

Planned improvements to the MCP integration:

1. **Auto-populate customer_id parameter** - When run_gaql is called without customer_id, prompt for client name and auto-populate
2. **Validation warnings** - Alert when using [TBD] IDs or invalid formats
3. **GA4 integration** - Once GA4 property IDs are populated, enable analytics queries by client name
4. **Caching** - Cache ID lookups within a session to reduce file reads
5. **Account switching** - For multi-account clients, allow specifying which account to use (e.g., "smythson-uk" vs "smythson-usa")

## Related Documentation

- **Helper Module**: [`shared/platform_ids.py`](../../shared/platform_ids.py)
- **Helper README**: [`shared/PLATFORM-IDS-README.md`](../../shared/PLATFORM-IDS-README.md)
- **Client IDs JSON**: [`shared/data/client-platform-ids.json`](../../shared/data/client-platform-ids.json)
- **MCP Configuration**: [`.mcp.json`](../../.mcp.json)
- **Google Ads MCP Server**: [`server.py`](google-ads-mcp-server/server.py)

## Troubleshooting

### Issue: MCP tool not showing up

**Solution:** Restart Claude Desktop to reload MCP server configuration

### Issue: Import errors in MCP server

**Check:**
1. `PLATFORM_IDS_HELPER` env var points to correct path
2. Python path includes project root
3. `shared/platform_ids.py` file exists and is readable

### Issue: IDs not being found

**Check:**
1. Client name matches folder name (lowercase, hyphens)
2. CONTEXT.md exists in client folder
3. Platform IDs section uses exact format from template
4. Client is included in `client-platform-ids.json`

## Support

For issues or questions about the MCP integration:
1. Check this documentation
2. Review helper module README: [`shared/PLATFORM-IDS-README.md`](../../shared/PLATFORM-IDS-README.md)
3. Test helper directly: `python3 shared/platform_ids.py <client_name>`
4. Check MCP server logs for import errors
