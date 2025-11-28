# Google Sheets MCP Server - Quick Reference Guide

## Overview
The existing `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/` is a fully-functional Google Sheets MCP server implementing industry best practices.

## Key Implementation Details

### 1. Authentication Type: Service Account
```
Use Case: Long-lived, automated access to specific spreadsheets
Credentials: JSON service account key file
Configuration: GOOGLE_APPLICATION_CREDENTIALS environment variable
```

### 2. Core Files
```
server.py                  # FastMCP server with 3 tools:
                          # - list_sheets()
                          # - read_cells()
                          # - write_cells()

gsheet_service.py         # Service layer with:
                          # - Credential loading
                          # - Service caching
                          # - Retry logic with exponential backoff
                          # - Error handling
```

### 3. Three Key Patterns Implemented

#### Pattern A: Service Initialization with Caching
```python
# From gsheet_service.py
_gsheet_service = None

def gsheet_service():
    """Lazy initialization - creates service once, reuses it."""
    global _gsheet_service
    if _gsheet_service is None:
        _gsheet_service = get_gsheet_service()
    return _gsheet_service

def reset_service():
    """Reset cache if connection fails."""
    global _gsheet_service
    _gsheet_service = None
```

#### Pattern B: Resilience with Exponential Backoff
```python
@retry_with_backoff(max_retries=3)
def list_sheets(spreadsheet_id: str) -> list[str]:
    """Auto-retries on rate limit (429) and server errors (500-503)."""
    service = gsheet_service()
    return service.spreadsheets().get(...).execute()
```

#### Pattern C: User-Friendly Error Messages
```python
def _handle_http_error(err: HttpError, operation: str) -> str:
    """Convert technical error codes to actionable messages."""
    if status_code == 403:
        return "Permission denied. Share spreadsheet with service account."
    elif status_code == 404:
        return "Spreadsheet not found. Check spreadsheet ID."
    # ... more error handling
```

### 4. Tool Interface Pattern

Each tool follows this structure:
```python
@mcp.tool(
    name="tool_name",
    description="User-facing description for Claude"
)
@retry_with_backoff(max_retries=3)
def tool_name(
    param1: str,
    param2: Optional[str] = None,
    ctx: Context = None
) -> ReturnType:
    """Detailed docstring explaining usage."""
    try:
        service = gsheet_service()
        result = service.api_call()
        if ctx:
            ctx.info("Success message")
        return result
    except HttpError as err:
        error_msg = _handle_http_error(err, "tool_name")
        return error_response
```

### 5. Dependencies
```
fastmcp>=0.3.0
google-api-python-client>=2.108.0
google-auth>=2.25.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0
```

## Building New Tools for Google Sheets

### Step 1: Add Tool to server.py
```python
@mcp.tool(
    name="append_rows",
    description="Append new rows to a spreadsheet"
)
@retry_with_backoff(max_retries=3)
def append_rows(
    spreadsheet_id: str,
    range_name: str,
    values: list[list[str]],
    ctx: Context = None
) -> dict:
    """Append rows to spreadsheet at specified range."""
    try:
        service = gsheet_service()
        body = {"values": values}
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        
        if ctx:
            ctx.info(f"Appended {result.get('updates', {}).get('updatedRows', 0)} rows")
        
        return {
            "message": f"Successfully appended rows",
            "updated_rows": result.get('updates', {}).get('updatedRows', 0),
            "updated_range": result.get('updates', {}).get('updatedRange')
        }
    except HttpError as err:
        error_msg = _handle_http_error(err, "append_rows")
        return {"error": error_msg}
```

### Step 2: Test Pattern
```bash
# Start MCP inspector
mcp dev server.py

# Or run with stdio
python server.py
```

### Step 3: Configure for Claude Desktop
```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "python",
      "args": ["/path/to/google-sheets-mcp-server/server.py"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account-key.json"
      }
    }
  }
}
```

## Testing Common Scenarios

### Test 1: Permission Denied (403)
```python
# Try reading a spreadsheet the service account doesn't have access to
# Expected: User-friendly error about sharing the spreadsheet
```

### Test 2: Rate Limiting (429)
```python
# Make many rapid requests
# Expected: Decorator should retry with exponential backoff
# No errors should surface to user after ~30 seconds
```

### Test 3: Invalid Range
```python
# Call read_cells with malformed range like "InvalidSheet!A1:B"
# Expected: Clear error message about range format
```

## Advanced: Adding to Existing Services

### If Integrating with Google Drive:
- Keep file management separate from sheet content operations
- Use two separate scopes: sheets and drive
- Implement caching for drive operations (slower)

### If Adding Batch Operations:
- Google Sheets API supports batch requests
- Can reduce API calls by combining multiple operations
- Update retry decorator to handle batch response errors

### If Adding Format/Styling:
- Use spreadsheets().batchUpdate() instead of values().update()
- More complex but enables cell formatting, charts, filters
- Retry logic remains the same

## Common Pitfalls to Avoid

1. **Not caching the service** - Creates new connection for each tool call
2. **Missing retry logic** - Google APIs rate-limit frequently
3. **Generic error messages** - Users need to know why operations fail
4. **Not resetting service on unexpected errors** - Connection may become stale
5. **Hardcoding credentials** - Always use environment variables

## Performance Notes

- Service caching reduces startup time by ~90%
- Exponential backoff prevents hammering the API
- Error conversion happens on client side (fast)
- Batch operations are ~5x faster than sequential calls

## Files to Study

1. `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/server.py`
   - Tool definitions, error handling patterns

2. `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/gsheet_service.py`
   - Service initialization, caching, retries

3. `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/server.py`
   - Advanced tool patterns with Context logging

4. `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/oauth/google_auth.py`
   - OAuth pattern (if building user auth instead of service account)
