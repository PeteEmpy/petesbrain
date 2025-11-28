# MCP Server Implementation Patterns - Detailed Analysis

## 1. Project Structure & Organization

### Standard Directory Layout
```
mcp-server-name/
├── server.py                          # Main FastMCP server definition
├── [service_module].py               # Service/API integration module
├── oauth/
│   ├── __init__.py
│   └── google_auth.py                # Authentication handling
├── requirements.txt                   # Python dependencies
├── pyproject.toml                    # Project metadata (optional)
├── .env                              # Environment variables configuration
├── credentials.json                  # OAuth credentials (local, not committed)
├── token.json                        # OAuth tokens (local, not committed)
├── manifest.json                     # MCP server manifest (optional)
└── README.md                         # Setup & usage documentation
```

### Real Examples:
- **google-sheets-mcp-server**: Uses `gsheet_service.py` for service layer
- **google-tasks-mcp-server**: Uses `tasks_service.py` with local OAuth token management
- **google-analytics-mcp-server**: Uses `oauth/google_auth.py` for OAuth handling + `.env` for configuration

---

## 2. Core Dependencies Pattern

### Universal Minimum Requirements
```
# requirements.txt or pyproject.toml

# Core MCP Framework
fastmcp>=0.3.0 to >=0.8.0      # Version varies by complexity

# Google API Integration
google-api-python-client>=2.108.0
google-auth>=2.25.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0

# For REST-based APIs (not service account)
requests>=2.31.0
python-dotenv>=1.0.0

# Optional additional utilities
urllib3>=2.0.0
typing-extensions>=4.0.0
```

### Two Authentication Patterns:
1. **Service Account (google-sheets)**: Credentials loaded from `GOOGLE_APPLICATION_CREDENTIALS` env var
2. **OAuth 2.0 User Auth (google-tasks, google-analytics)**: Interactive browser login with token refresh

---

## 3. Authentication Strategies

### Pattern A: Service Account (Read-only Services)
**Used by**: Google Sheets (service account with spreadsheet access)

```python
# gsheet_service.py structure
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def get_gsheet_service():
    """Load credentials from file and build service object."""
    creds = Credentials.from_service_account_file(
        filename=SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    return service

# Lazy initialization with caching
_gsheet_service = None

def gsheet_service():
    """Returns cached service, initializing if needed."""
    global _gsheet_service
    if _gsheet_service is None:
        _gsheet_service = get_gsheet_service()
    return _gsheet_service
```

**Configuration**: Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable pointing to service account JSON key

### Pattern B: OAuth 2.0 with Local Token Persistence
**Used by**: Google Tasks, Google Analytics

```python
# oauth/google_auth.py structure (Google Analytics example)
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/analytics',
    'https://www.googleapis.com/auth/analytics.readonly'
]

def get_oauth_credentials():
    """Get user credentials with automatic token refresh."""
    token_path = "token.json"
    creds = None
    
    # 1. Load existing token if available
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # 2. If no valid credentials, check if we can refresh
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Silently refresh expired token
            creds.refresh(Request())
        else:
            # Run interactive OAuth flow (opens browser)
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
    
    # 3. Save token for next time
    with open(token_path, "w") as token_file:
        token_file.write(creds.to_json())
    
    return creds

def get_headers_with_auto_token():
    """Generate API headers with current bearer token."""
    creds = get_oauth_credentials()
    return {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json'
    }
```

**Configuration**: 
- Place OAuth credentials JSON in server directory as `credentials.json`
- Set `GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH` environment variable (alternative)
- Token stored as `token.json` (generated after first authentication)

---

## 4. Server Implementation Pattern (FastMCP)

### Basic Server Structure
```python
# server.py
from fastmcp import FastMCP, Context
from typing import Any, Dict, List, Optional
import logging

# Initialize FastMCP server
mcp = FastMCP("Service Name Controller")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tool 1: Simple list operation
@mcp.tool(
    name="tool_name",
    description="Human-readable description of what tool does",
)
def tool_name(
    param1: str,
    param2: Optional[str] = None,
    ctx: Context = None  # Optional context for logging
) -> Dict[str, Any]:
    """Detailed docstring with Args and Returns sections."""
    if ctx:
        ctx.info(f"Executing tool with param1: {param1}")
    
    try:
        # Call service layer
        service = gsheet_service()
        result = service.some_api_call()
        
        if ctx:
            ctx.info(f"Operation completed successfully")
        
        return result
    except Exception as e:
        if ctx:
            ctx.error(f"Error: {str(e)}")
        raise

# Tool 2: With retry decorator
@mcp.tool()
@retry_with_backoff(max_retries=3)  # Decorator for resilience
def resilient_tool(param: str) -> str:
    """Tools handling rate limits should use retry decorator."""
    pass

# Resource (optional): Documentation/reference data
@mcp.resource("scheme://reference")
def reference_docs() -> str:
    """Provide API reference or documentation."""
    return """
    ## API Reference
    ### Available Metrics:
    - metric1
    - metric2
    """

# Server startup
if __name__ == "__main__":
    print("Starting Service MCP Server...")
    mcp.run(transport="stdio")  # Standard input/output for Claude Desktop
```

### Tool Definition Pattern
- **@mcp.tool()** decorator marks a function as an MCP tool
- **Description parameter** required for Claude to understand tool purpose
- **Context parameter (ctx)** optional but recommended for logging/debugging
- **Return types** should be Dict[str, Any] or List[Dict] for complex data
- **Error handling** should catch API errors and return user-friendly messages

---

## 5. Service Layer Pattern

### Single Service Pattern (Simple Services)
```python
# gsheet_service.py
def gsheet_service():
    """Cached service singleton."""
    global _service
    if _service is None:
        _service = build("sheets", "v4", credentials=creds)
    return _service
```

### Modular Service Functions (Complex Services)
```python
# tasks_service.py
def tasks_service():
    """Create and return service with OAuth."""
    # Handle token loading/refresh
    creds = handle_oauth()
    service = build("tasks", "v1", credentials=creds)
    return service
```

### REST API Pattern (google-analytics)
```python
# oauth/google_auth.py
def get_headers_with_auto_token():
    """Return headers with bearer token for REST calls."""
    creds = get_oauth_credentials()
    return {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json'
    }

# In server.py
headers = get_headers_with_auto_token()
response = requests.post(url, headers=headers, json=payload)
```

---

## 6. Resilience & Error Handling

### Retry with Exponential Backoff Pattern
```python
# gsheet_service.py - used by google-sheets
def retry_with_backoff(max_retries=3, initial_backoff=1, max_backoff=60):
    """Decorator to retry API calls with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            backoff = initial_backoff
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except HttpError as err:
                    status_code = err.resp.status if err.resp else None
                    
                    # Don't retry on client errors (4xx except 429)
                    RETRYABLE_STATUS_CODES = [429, 500, 502, 503, 504]
                    if status_code not in RETRYABLE_STATUS_CODES:
                        raise
                    
                    # On last attempt, raise
                    if attempt == max_retries:
                        raise
                    
                    # Calculate exponential backoff
                    wait_time = min(backoff * (2 ** attempt), max_backoff)
                    time.sleep(wait_time)
                except Exception:
                    raise  # Non-HTTP errors don't retry
        
        return wrapper
    return decorator
```

**Applied to**: Google Sheets tools
**Handles**: 429 (rate limit), 500-503 (server errors)
**Usage**: 
```python
@mcp.tool()
@retry_with_backoff(max_retries=3)
def read_cells(...):
    pass
```

### HTTP Error Handling Pattern
```python
# server.py - google-sheets
def _handle_http_error(err: HttpError, operation: str) -> str:
    """Convert technical errors to user-friendly messages."""
    status_code = err.resp.status if err.resp else None
    
    if status_code == 403:
        return "Permission denied. Share spreadsheet with service account."
    elif status_code == 404:
        return "Spreadsheet not found. Check the spreadsheet ID."
    elif status_code == 400:
        return "Bad request. Check range format (e.g., 'Sheet1!A1:B2')"
    elif status_code == 429:
        return "Rate limit exceeded. Retrying with backoff..."
    elif status_code == 500:
        return "Google Sheets API server error. Retrying..."
    
    return f"HTTP {status_code}: {str(err)}"

@mcp.tool()
def read_cells(...):
    try:
        return service.get(...)
    except HttpError as err:
        error_msg = _handle_http_error(err, "read_cells")
        return [[f"Error: {error_msg}"]]
```

---

## 7. Environment Configuration Pattern

### .env File Pattern (google-analytics)
```bash
# .env
GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH=/path/to/client_secret.json
```

### Environment Variables Used:

**Service Account Pattern**:
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to service account JSON key

**OAuth Pattern**:
- `GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH` - Path to OAuth credentials JSON
- `PLATFORM_IDS_HELPER` - Optional helper for client ID lookups (google-ads, google-analytics)
- `CLIENT_IDS_PATH` - Optional path to client IDs database

**Multi-Server Coordination**:
- `PYTHONPATH` - Include shared libraries from other MCP servers

### Loading Pattern
```python
# Load .env FIRST before importing other modules
from dotenv import load_dotenv
load_dotenv()

# THEN import modules that depend on env vars
from oauth.google_auth import get_headers_with_auto_token
```

---

## 8. Tool Definition Patterns

### Pattern 1: Simple CRUD Operations
```python
@mcp.tool()
def list_items(account_id: str = "", ctx: Context = None) -> List[Dict]:
    """Lists all items, optionally filtered by account.
    
    Args:
        account_id: Optional filter by account ID
        ctx: MCP context for logging
    
    Returns:
        List of items with their details
    """
    headers = get_headers_with_auto_token()
    response = requests.get(url, headers=headers)
    return response.json()
```

### Pattern 2: Complex Reports with Multiple Parameters
```python
@mcp.tool()
def run_report(
    property_id: str,
    start_date: str,
    end_date: str,
    metrics: List[str],
    dimensions: Optional[List[str]] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Execute comprehensive report with full customization.
    
    IMPORTANT: Use STRING ARRAYS for metrics and dimensions!
    
    CORRECT:
    - metrics: ["sessions", "totalUsers"]
    - dimensions: ["country", "deviceCategory"]
    
    INCORRECT (will fail):
    - metrics: [{"name": "sessions"}]
    """
    payload = {
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [{'name': metric.strip()} for metric in metrics]
    }
    
    if dimensions:
        payload['dimensions'] = [{'name': d.strip()} for d in dimensions]
    
    if limit:
        payload['limit'] = limit
    
    if offset is not None:
        payload['offset'] = offset
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### Pattern 3: Tools with Resources (Documentation)
```python
@mcp.resource("ga4://reference")
def ga4_reference() -> str:
    """Provide GA4 API reference for Claude's context."""
    return """
    ## Google Analytics 4 API Reference
    
    ### Common Metrics
    - sessions: Number of sessions
    - totalUsers: Total number of users
    - screenPageViews: Number of page views
    
    ### Common Dimensions
    - country: Country name
    - deviceCategory: Device (mobile/desktop/tablet)
    - pagePath: Page path
    """
```

---

## 9. Manifest Pattern (manifest.json)

### Structure
```json
{
  "dxt_version": "0.1",
  "name": "service-mcp-server",
  "display_name": "Service MCP Server",
  "version": "0.1.0",
  "description": "Brief description",
  "long_description": "Detailed description",
  "author": {
    "name": "Author Name",
    "email": "email@example.com"
  },
  "server": {
    "type": "python",
    "entry_point": "server.py",
    "mcp_config": {
      "command": "python",
      "args": ["${__dirname}/server.py"],
      "env": {
        "ENV_VAR_NAME": "${user_config.config_name}"
      }
    }
  },
  "tools": [
    {
      "name": "tool_name",
      "description": "Tool description"
    }
  ],
  "resources": [
    {
      "name": "scheme://resource",
      "description": "Resource description"
    }
  ],
  "user_config": {
    "oauth_config_path": {
      "type": "string",
      "title": "OAuth Configuration Path",
      "description": "Path to OAuth credentials JSON",
      "required": true
    }
  },
  "compatibility": {
    "claude_desktop": ">=0.10.0",
    "platforms": ["darwin", "win32", "linux"],
    "runtimes": {
      "python": ">=3.10.0 <4"
    }
  }
}
```

---

## 10. Configuration for Claude Desktop

### Pattern A: stdio (Standard Input/Output)
```python
# server.py
if __name__ == "__main__":
    mcp.run(transport="stdio")  # Default, works with Claude Desktop
```

### Pattern B: HTTP Transport (Development)
```python
# server.py
if __name__ == "__main__":
    if "--http" in sys.argv:
        mcp.run(
            transport="streamable-http",
            host="127.0.0.1",
            port=8000,
            path="/mcp"
        )
    else:
        mcp.run(transport="stdio")
```

### Claude Desktop Configuration
```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "/path/to/uv",
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account-key.json"
      },
      "args": ["--directory", "/path/to/google-sheets-mcp-server", "run", "server.py"]
    },
    "google-analytics": {
      "command": "python",
      "args": ["/path/to/google-analytics-mcp-server/server.py"],
      "env": {
        "GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH": "/path/to/client_secret.json"
      }
    }
  }
}
```

---

## 11. Logging & Debugging Pattern

### Standard Logging Setup
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use throughout:
logger.info(f"Successfully listed {len(titles)} sheets")
logger.warning(f"Deprecation warning...")
logger.error(f"Error details: {e}", exc_info=True)
```

### MCP Context Logging
```python
@mcp.tool()
def my_tool(param: str, ctx: Context = None) -> Dict:
    if ctx:
        ctx.info(f"Starting operation with param: {param}")
    
    try:
        result = api_call()
        if ctx:
            ctx.info(f"Operation successful, got {len(result)} items")
        return result
    except Exception as e:
        if ctx:
            ctx.error(f"Operation failed: {str(e)}")
        raise
```

---

## 12. Key Patterns Summary

| Aspect | Pattern | Example |
|--------|---------|---------|
| **Authentication** | Service account OR OAuth 2.0 | Sheets (service), Analytics (OAuth) |
| **Service Layer** | Cached singleton with initialization | `gsheet_service()` function |
| **Resilience** | Decorator-based retry with exponential backoff | `@retry_with_backoff(max_retries=3)` |
| **Error Handling** | Convert API errors to user-friendly messages | Status code specific handling |
| **Configuration** | .env file + environment variables | `GOOGLE_ANALYTICS_OAUTH_CONFIG_PATH` |
| **Tools** | FastMCP @mcp.tool() decorators | Named tools with descriptions |
| **Context** | Optional Context parameter for logging | `ctx: Context = None` |
| **Transport** | stdio (default) or HTTP | `mcp.run(transport="stdio")` |
| **Dependencies** | fastmcp + google-api-python-client | See requirements.txt examples |

---

## 13. Building a New Google Sheets MCP Server

### Key Learnings:
1. **Reuse existing google-sheets-mcp-server** as template - it's already well-structured
2. If building new features:
   - Use **Service Account authentication** (most secure for read/write operations)
   - Implement **retry_with_backoff** decorator (Google APIs are rate-limited)
   - Add **error conversion** function for user-friendly messages
   - Cache the service object with lazy initialization
   - Use **Context parameter** for logging in tools

### Minimum Files Needed:
- `server.py` - MCP server with @mcp.tool() definitions
- `service.py` - Google Sheets API service initialization
- `requirements.txt` - Dependencies (fastmcp, google-api-python-client, google-auth)
- `.env` - Environment configuration
- `README.md` - Setup instructions

### Advanced Features (from google-analytics):
- `oauth/google_auth.py` - Separate OAuth module for organization
- `manifest.json` - For marketplace/distribution
- Context logging in tools - Better debugging
- Resource documentation - `@mcp.resource()` for reference docs
