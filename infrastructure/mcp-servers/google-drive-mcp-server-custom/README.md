# Google Drive MCP Server (Custom Build)

Custom-built Google Drive MCP server with lazy-loading OAuth to prevent startup popups.

## Features

- ✅ **Lazy Loading OAuth** - No browser popups at startup
- ✅ **Automatic Token Refresh** - Tokens refresh automatically when needed
- ✅ **Comprehensive Tools** - Search, create, read, update, delete, move, rename files
- ✅ **Context Logging** - Full logging for debugging

## Available Tools

| Tool | Description |
|------|-------------|
| `search` | Search for files with query |
| `create_text_file` | Create new text/markdown file |
| `update_text_file` | Update existing text file |
| `create_folder` | Create new folder |
| `list_folder` | List folder contents |
| `delete_item` | Move file/folder to trash |
| `rename_item` | Rename file/folder |
| `move_item` | Move file/folder |
| `get_file_content` | Get text file content |

## Setup

### 1. Create OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Enable Google Drive API
3. Create OAuth 2.0 Client ID (Desktop application)
4. Download JSON credentials file

### 2. Install Dependencies

```bash
cd google-drive-mcp-server-custom
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file:

```bash
GOOGLE_DRIVE_OAUTH_CONFIG_PATH=/path/to/your/client_secret.json
```

Or export as environment variable:

```bash
export GOOGLE_DRIVE_OAUTH_CONFIG_PATH=/path/to/your/client_secret.json
```

### 4. Add to Claude Code

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "google-drive-custom": {
      "command": "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-drive-mcp-server-custom/.venv/bin/python",
      "args": [
        "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-drive-mcp-server-custom/server.py"
      ],
      "env": {
        "GOOGLE_DRIVE_OAUTH_CONFIG_PATH": "/path/to/your/client_secret.json"
      }
    }
  }
}
```

### 5. First Authentication

When you first use a Drive tool in Claude Code:
1. Browser will open automatically for OAuth
2. Grant permission to access Drive
3. Token saved to `token.json` for future use

**After initial auth, no more browser popups!**

## Usage Examples

**Search for files:**
```
Search Google Drive for files containing "budget"
```

**Create a file:**
```
Create a text file called "notes.md" with content "# Meeting Notes"
```

**List folder contents:**
```
List all files in my Drive root folder
```

**Get file content:**
```
Read the content of file ID abc123xyz
```

## Architecture

### Lazy Loading OAuth Pattern

**Problem**: Traditional MCP servers import OAuth modules at startup, triggering credential checks and browser popups every time Claude Code starts.

**Solution**: This server uses **lazy loading** - OAuth modules are imported **inside tool functions** only when actually called.

```python
# ❌ OLD WAY (causes startup popups)
from oauth.google_auth import get_headers_with_auto_token

@mcp.tool
def my_tool():
    headers = get_headers_with_auto_token()

# ✅ NEW WAY (no startup popups)
@mcp.tool
def my_tool():
    from oauth.google_auth import get_headers_with_auto_token  # Lazy import
    headers = get_headers_with_auto_token()
```

### Token Auto-Refresh

Tokens automatically refresh when expired:
- Access token expires after 1 hour
- Refresh token valid for ~6 months
- As long as you use the server regularly, tokens never expire
- No browser popup for refresh (automatic)

## Troubleshooting

**OAuth popup appears at startup:**
- Restart Claude Code completely
- Verify lazy loading pattern in server.py (OAuth imported inside tool functions)

**Permission denied errors:**
- Check OAuth credentials have Drive API enabled
- Share files with your Google account

**Token refresh failed:**
- Delete `token.json` and re-authenticate
- Check internet connection

## Differences from NPX Package

| Feature | NPX Package (@piotr-agier/google-drive-mcp) | Custom Server |
|---------|---------------------------------------------|---------------|
| OAuth Loading | Eager (startup popups) | Lazy (no popups) |
| Customisation | None (external package) | Full control |
| Logging | Limited | Comprehensive |
| Maintenance | Third-party | In-house |

## File Structure

```
google-drive-mcp-server-custom/
├── server.py                    # Main FastMCP server (lazy OAuth)
├── oauth/
│   ├── __init__.py
│   └── google_auth.py          # OAuth handling
├── requirements.txt
├── .env                         # Environment config (gitignored)
├── token.json                   # OAuth token (generated, gitignored)
├── credentials.json             # OAuth credentials (gitignored)
└── README.md                    # This file
```

## License

MIT

## Author

PetesBrain Contributors
