# Google Chat MCP Server

Model Context Protocol (MCP) server providing direct access to Google Chat API for reading messages, listing spaces, sending messages, and managing conversations.

## Features

### Available Tools

- **`list_spaces`** - List all Google Chat spaces (conversations) with pagination
- **`get_space`** - Get details for a specific space
- **`list_messages`** - List messages in a space with filtering and pagination
- **`get_message`** - Get a specific message by ID
- **`create_message`** - Send a message to a space or thread
- **`list_members`** - List members of a space
- **`search_spaces`** - Search spaces by display name

### Authentication

Uses **OAuth 2.0 User Authentication** with automatic token refresh. Requires Google Chat API scopes:

- `https://www.googleapis.com/auth/chat.spaces.readonly` - Read spaces
- `https://www.googleapis.com/auth/chat.messages.readonly` - Read messages
- `https://www.googleapis.com/auth/chat.messages` - Send/create messages
- `https://www.googleapis.com/auth/chat.spaces` - Manage spaces

## Setup

### 1. Google Cloud Project Configuration

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project
3. Enable **Google Chat API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Chat API"
   - Click "Enable"

4. Create OAuth 2.0 Credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Google Chat MCP Server"
   - Download the JSON file

5. Save the downloaded JSON as `credentials.json` in this directory

### 2. Python Environment Setup

```bash
cd /Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-chat-mcp-server

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `.env.template` to `.env` and configure:

```bash
cp .env.template .env
```

Edit `.env`:

```bash
GOOGLE_CHAT_OAUTH_CONFIG_PATH=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-chat-mcp-server/credentials.json
```

### 4. Claude Desktop Configuration

Add to your `.mcp.json` (located at `/Users/administrator/.claude/.mcp.json`):

```json
{
  "mcpServers": {
    "google-chat": {
      "command": "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-chat-mcp-server/.venv/bin/python",
      "args": [
        "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-chat-mcp-server/server.py"
      ],
      "env": {
        "GOOGLE_CHAT_OAUTH_CONFIG_PATH": "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-chat-mcp-server/credentials.json"
      }
    }
  }
}
```

Or use the `claude mcp add` command:

```bash
claude mcp add -s user google-chat \
  "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-chat-mcp-server/.venv/bin/python" \
  "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-chat-mcp-server/server.py"
```

### 5. First Run Authentication

On first use, the server will:
1. Open your browser for OAuth consent
2. Ask you to sign in with Google
3. Request permission to access Google Chat
4. Save the token to `token.json` for future use

**Token Location**: `token.json` (stored in this directory, auto-refreshed)

## Usage Examples

### List All Spaces

```python
mcp__google_chat__list_spaces(page_size=50)
```

### Get Space Details

```python
mcp__google_chat__get_space(space_name="spaces/AAAAAAAAAAA")
```

### List Messages in a Space

```python
mcp__google_chat__list_messages(
    space_name="spaces/AAAAAAAAAAA",
    page_size=100,
    order_by="createTime desc"
)
```

### Send a Message

```python
mcp__google_chat__create_message(
    space_name="spaces/AAAAAAAAAAA",
    text="Hello from Claude Code!"
)
```

### Search for Spaces

```python
mcp__google_chat__search_spaces(query="Project")
```

### List Space Members

```python
mcp__google_chat__list_members(space_name="spaces/AAAAAAAAAAA")
```

## Common Patterns

### Reading Recent Messages

```python
# Get a space
space = mcp__google_chat__get_space(space_name="spaces/AAAAAAAAAAA")

# List recent messages
messages = mcp__google_chat__list_messages(
    space_name="spaces/AAAAAAAAAAA",
    page_size=50,
    order_by="createTime desc"
)

# Process each message
for msg in messages.get('messages', []):
    sender = msg.get('sender', {}).get('displayName', 'Unknown')
    text = msg.get('text', '')
    print(f"{sender}: {text}")
```

### Finding Client Conversations

```python
# Search for client spaces
results = mcp__google_chat__search_spaces(query="Smythson")

# List messages in the space
for space in results.get('spaces', []):
    messages = mcp__google_chat__list_messages(
        space_name=space['name'],
        page_size=20
    )
```

## Integration with messaging-processor Skill

The `messaging-processor` skill can now use this MCP server to:

1. **Read Google Chat messages** - Process incoming client messages
2. **Route to clients** - Identify which client a message belongs to
3. **Create tasks** - Extract action items from conversations
4. **Send responses** - Reply to client messages

## Troubleshooting

### OAuth Token Expired

If you see "OAuth token expired" errors:

```bash
# Delete the token and re-authenticate
rm token.json

# Restart Claude Code - will trigger new OAuth flow
```

### Permission Denied

If you get "Permission denied" errors:

1. Check that Google Chat API is enabled in your project
2. Verify OAuth credentials have correct scopes
3. Ensure you've granted consent during OAuth flow

### API Errors

Common API error codes:

- **403 Forbidden** - Missing API access or permissions
- **404 Not Found** - Space or message doesn't exist
- **429 Rate Limit** - Too many requests (implements automatic retry)
- **500 Server Error** - Google API temporary issue

## API Reference

### Space Resource Name Format

Space names follow this pattern:
```
spaces/AAAAAAAAAAA
```

### Message Resource Name Format

Message names follow this pattern:
```
spaces/AAAAAAAAAAA/messages/BBBBBBB.CCCCCC
```

### Space Types

- `SPACE` - Regular chat space
- `GROUP_CHAT` - Group conversation
- `DIRECT_MESSAGE` - 1:1 conversation

## Dependencies

- `fastmcp>=0.8.0` - MCP server framework
- `google-auth>=2.25.0` - Google authentication
- `google-auth-oauthlib>=1.2.0` - OAuth flow handling
- `requests>=2.31.0` - HTTP client
- `python-dotenv>=1.0.0` - Environment configuration

## Security Notes

- **Never commit** `credentials.json` or `token.json` to git
- Token auto-refreshes and persists across sessions
- OAuth scopes request minimal necessary permissions
- Follows lazy loading pattern (no OAuth popup on startup)

## Related Documentation

- [Google Chat API Reference](https://developers.google.com/chat/api/reference/rest)
- [MCP Implementation Patterns](../MCP-IMPLEMENTATION-PATTERNS.md)
- [OAuth Setup Guide](../../../docs/OAUTH-SETUP.md)

## Version History

- **v0.1.0** (2025-12-16) - Initial implementation with core read/write tools
