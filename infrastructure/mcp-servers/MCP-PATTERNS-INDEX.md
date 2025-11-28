# MCP Implementation Patterns - Index & Quick Links

## Generated Documentation

This directory contains comprehensive documentation of MCP server implementation patterns discovered through analysis of existing servers.

### 1. MCP-IMPLEMENTATION-PATTERNS.md
**Comprehensive 13-section guide covering all aspects of MCP server development**

Sections:
1. Project Structure & Organisation
2. Core Dependencies Pattern
3. Authentication Strategies (Service Account vs OAuth)
4. Server Implementation Pattern (FastMCP)
5. Service Layer Pattern
6. Resilience & Error Handling
7. Environment Configuration
8. Tool Definition Patterns
9. Manifest Pattern
10. Configuration for Claude Desktop
11. Logging & Debugging
12. Key Patterns Summary
13. Building a New Google Sheets Server

**Use this for**: Complete understanding of MCP patterns, detailed code examples

### 2. GOOGLE-SHEETS-PATTERNS.md
**Quick reference guide for Google Sheets MCP server specifics**

Sections:
- Overview of google-sheets-mcp-server
- Key implementation details
- Three core patterns
- Tool interface pattern
- Building new tools (example: append_rows)
- Testing scenarios
- Advanced extensions
- Common pitfalls
- Performance notes
- Files to study

**Use this for**: Extending google-sheets-mcp-server, quick pattern lookup

---

## Existing MCP Servers Analysed

### Production-Ready Implementations

1. **google-sheets-mcp-server**
   - Location: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/`
   - Auth: Service Account
   - Tools: list_sheets, read_cells, write_cells
   - Pattern: Cached service + exponential backoff retry
   - Key Files:
     - `server.py` - Tool definitions
     - `gsheet_service.py` - Service layer with caching/retry

2. **google-tasks-mcp-server**
   - Location: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server/`
   - Auth: OAuth 2.0 with local token persistence
   - Tools: list/create/update/complete/delete tasks + task lists
   - Pattern: Direct OAuth flow with browser authentication
   - Key Files:
     - `server.py` - Tool definitions
     - `tasks_service.py` - OAuth and service initialization

3. **google-analytics-mcp-server**
   - Location: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/`
   - Auth: OAuth 2.0 with auto token refresh
   - Tools: list_properties, get_page_views, get_active_users, get_events, get_traffic_sources, get_device_metrics, run_report
   - Pattern: REST API with Bearer token + .env config
   - Key Files:
     - `server.py` - Tool definitions with Context logging
     - `oauth/google_auth.py` - OAuth module with auto-refresh
     - `.env` - Environment configuration
     - `manifest.json` - Server metadata

4. **google-ads-mcp-server**
   - Location: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/`
   - Auth: OAuth 2.0
   - Pattern: GAQL execution + Platform ID helper
   - Advanced: Integrates with platform_ids helper for client lookups

5. **facebook-ads-mcp-server**
   - Location: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/facebook-ads-mcp-server/`
   - Auth: OAuth 2.0
   - Pattern: Meta/Facebook Ads API integration

6. **meta-ads-mcp-server**
   - Location: `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/meta-ads-mcp-server/`
   - Auth: OAuth 2.0
   - Pattern: Modern FastMCP implementation (v0.8.0+)

---

## Key Patterns Summary

### Authentication Patterns
- **Service Account**: For read/write access to shared resources (Sheets)
- **OAuth 2.0 User**: For user-specific operations with browser auth (Tasks, Analytics)

### Resilience Patterns
- **Retry Decorator**: Exponential backoff for 429, 500-503 errors
- **Error Conversion**: Convert HTTP codes to user-friendly messages
- **Service Caching**: Lazy initialization with singleton pattern

### Tool Definition Patterns
- **@mcp.tool()**: FastMCP decorator for marking functions as tools
- **Context Parameter**: Optional ctx for logging/debugging
- **Error Handling**: Try/catch with API-specific error messages

### Configuration Patterns
- **Environment Variables**: GOOGLE_APPLICATION_CREDENTIALS or .env file
- **Claude Desktop**: JSON configuration in settings
- **Token Management**: Local token.json for OAuth persistence

### Code Structure Patterns
```
server.py              # @mcp.tool() definitions
[service_name].py      # Service layer, caching, retry logic
oauth/                 # Auth module (if OAuth)
requirements.txt       # Python dependencies
.env                   # Config (if OAuth)
manifest.json          # Server metadata (optional)
README.md             # Documentation
```

---

## Quick Reference Tables

### Authentication Comparison
| Aspect | Service Account | OAuth 2.0 |
|--------|-----------------|-----------|
| Use Case | Automated, long-lived access | User-delegated permissions |
| Credentials | JSON key file | Browser OAuth + token file |
| Scopes | Single set | User-specific |
| Token Refresh | N/A | Automatic if expired |
| Best For | Sheets (shared resources) | Tasks, Analytics (user-specific) |

### Resilience Patterns
| Error Type | Code | Retry | Conversion |
|-----------|------|-------|-----------|
| Rate Limit | 429 | Yes (60s+) | "Rate limit exceeded" |
| Unauthorised | 401 | No | "Check credentials" |
| Forbidden | 403 | No | "Check permissions/sharing" |
| Not Found | 404 | No | "Check resource ID" |
| Bad Request | 400 | No | "Check request format" |
| Server Error | 500-503 | Yes (exponential) | "Retrying..." |

### Dependencies Versions
| Package | Min Version | Usage |
|---------|-------------|-------|
| fastmcp | 0.3.0 | MCP framework |
| google-api-python-client | 2.108.0 | Google API access |
| google-auth | 2.25.0 | Authentication |
| google-auth-oauthlib | 1.2.0 | OAuth flow |
| requests | 2.31.0 | REST API calls |
| python-dotenv | 1.0.0 | .env configuration |

---

## How to Use These Guides

### For Learning MCP Patterns
1. Start with **MCP-IMPLEMENTATION-PATTERNS.md**
2. Read sections 1-6 for fundamentals
3. Study a real server implementation (google-sheets or google-tasks)
4. Review section 12 (Key Patterns Summary)

### For Building New Tools
1. Check if a server already exists for your service
2. If extending existing: Read **GOOGLE-SHEETS-PATTERNS.md**
3. Copy the tool pattern from similar existing tool
4. Apply @retry_with_backoff decorator
5. Test with `mcp dev server.py`

### For Understanding Authentication
1. Service Account needed? → Study google-sheets-mcp-server
2. OAuth with browser auth? → Study google-tasks-mcp-server
3. OAuth with token refresh? → Study google-analytics-mcp-server

### For Debugging Issues
1. Check error codes in Resilience Patterns table
2. Verify retry logic is applied (@retry_with_backoff)
3. Check environment variables are set correctly
4. Review error conversion function for clarity
5. Use MCP context logging (ctx.info/error) for debugging

---

## Important Files to Study

### Core Pattern Examples
- `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/gsheet_service.py` - Service caching pattern
- `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/server.py` - Error handling pattern
- `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/oauth/google_auth.py` - OAuth pattern
- `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server/tasks_service.py` - Token persistence pattern

### Configuration Examples
- `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/.env` - Environment config
- `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-analytics-mcp-server/manifest.json` - Server manifest
- `/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/README.md` - Setup documentation

---

## Recommendations

### For Google Sheets Specifically
**DO NOT BUILD NEW** - A production-ready google-sheets-mcp-server already exists.

To extend it:
1. Add tools to `server.py`
2. All tools use `@retry_with_backoff(max_retries=3)`
3. Implement error conversion for common HTTP codes
4. Add Context parameter for logging
5. Test with `mcp dev server.py`

### For Building Other Google Services
- Use google-analytics pattern if REST API-based
- Use google-tasks pattern if using google-api-python-client
- Always implement retry logic for rate-limit resilience
- Convert API errors to user-friendly messages

### For OAuth Implementation
- Store credentials in `credentials.json` (obtained from Google Cloud)
- Generate `token.json` on first auth (automatic)
- Use auto-refresh pattern for token expiry
- Test OAuth flow manually before deploying

---

## Version Information

Analysis Date: November 24, 2025
FastMCP Versions Used: 0.3.0 to 0.8.0
Python Version: 3.10+
Google APIs: v4 (Sheets), v1 (Tasks), v1beta (Analytics)

---

Generated with analysis of existing MCP server implementations.
For questions, refer to the comprehensive guide or existing server code.
