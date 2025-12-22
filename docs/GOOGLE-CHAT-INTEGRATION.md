# Google Chat API Integration

**Date Created:** 2025-12-16
**Status:** ✅ Active
**Primary Use Case:** Monitor Collaber PPC Chat for Tree2mydoor client updates

---

## Overview

Direct API integration with Google Chat to monitor the **Collaber PPC Chat** space for client communications, product updates, and actionable items.

**Key Capabilities:**
- Read messages from Collaber PPC Chat space
- Extract product updates (SKUs, prices, stock changes)
- Monitor for Tree2mydoor mentions
- Create tasks from actionable items
- Save important updates to client folders

---

## Setup (Completed 2025-12-16)

### 1. Google Cloud Console Configuration

**Project:** PetesBrain (`gen-lang-client-0000536395`)

**Steps Completed:**
1. ✅ Enabled Google Chat API
2. ✅ Created OAuth 2.0 Desktop credentials
3. ✅ Configured OAuth consent screen (External)
4. ✅ Added required scopes:
   - `https://www.googleapis.com/auth/chat.spaces.readonly`
   - `https://www.googleapis.com/auth/chat.messages.readonly`
   - `https://www.googleapis.com/auth/chat.messages`
5. ✅ Configured Chat app (minimal config for API access)

### 2. MCP Server Configuration

**Location:** `infrastructure/mcp-servers/google-chat-mcp-server/`

**Credentials:**
- OAuth credentials: `credentials.json` (downloaded from Google Cloud Console)
- OAuth token: `token.json` (auto-generated on first use)

**MCP Config:** Already configured in `.mcp.json`

```json
{
  "mcpServers": {
    "google-chat": {
      "command": "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-chat-mcp-server/.venv/bin/python",
      "args": [
        "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-chat-mcp-server/server.py"
      ],
      "env": {
        "GOOGLE_CHAT_OAUTH_CONFIG_PATH": "/Users/administrator/Documents/PetesBrain.nosync/infrastructure/mcp-servers/google-chat-mcp-server/credentials.json"
      }
    }
  }
}
```

### 3. OAuth Authorization

**First Run:** OAuth flow triggered automatically when first MCP tool called
**Token Storage:** `infrastructure/mcp-servers/google-chat-mcp-server/token.json`
**Token Refresh:** Automatic (handled by MCP server)

---

## Available MCP Tools

### List Spaces

```python
mcp__google_chat__list_spaces(page_size=10)
```

**Returns:** All accessible Google Chat spaces

### List Messages

```python
mcp__google_chat__list_messages(
    space_name="spaces/AAAASSOCJ14",  # Collaber PPC Chat
    page_size=50,
    order_by="createTime desc"
)
```

**Returns:** Messages from specified space

### Get Specific Message

```python
mcp__google_chat__get_message(
    message_name="spaces/AAAASSOCJ14/messages/ZZWbEoV7Ol8.NtbzhFb7y70"
)
```

### Search Spaces

```python
mcp__google_chat__search_spaces(query="Collaber")
```

### Send Message (Optional)

```python
mcp__google_chat__create_message(
    space_name="spaces/AAAASSOCJ14",
    text="Message content"
)
```

---

## Collaber PPC Chat Space

**Space Name:** `spaces/AAAASSOCJ14`
**Display Name:** Collaber PPC Chat
**Type:** ROOM
**Created:** 2024-10-30
**Members:** 4 direct human users

**Primary Client:** Tree2mydoor

**Web URL:** https://chat.google.com/room/AAAASSOCJ14?cls=11

---

## Common Use Cases

### 1. Check Recent Messages

```python
messages = mcp__google_chat__list_messages(
    space_name="spaces/AAAASSOCJ14",
    page_size=20,
    order_by="createTime desc"
)
```

### 2. Extract Product Updates

Look for messages containing:
- SKU numbers (e.g., "SKU 00813", "CAMWSA")
- Price changes
- Stock updates ("back in stock", "out of stock")
- Product names
- Tree2mydoor links

### 3. Identify Mentions

Filter messages with user mentions:
```python
# Messages contain 'annotations' field with USER_MENTION type
# Check for @Peter Empson mentions
```

### 4. Extract Links and Attachments

Messages may contain:
- `richLinkMetadata` - Google Drive files, URLs
- `attachment` - Spreadsheets, documents
- Inline links in `formattedText`

---

## Message Structure

**Key Fields:**
- `name` - Message resource name (ID)
- `sender.name` - User ID of sender
- `createTime` - ISO 8601 timestamp
- `text` - Plain text content
- `formattedText` - Formatted text (with links, mentions)
- `annotations` - Mentions, rich links
- `thread.name` - Thread ID
- `attachment` - File attachments
- `emojiReactionSummaries` - Reactions (👍, etc.)

**Example Message:**
```json
{
  "name": "spaces/AAAASSOCJ14/messages/ZZWbEoV7Ol8.NtbzhFb7y70",
  "sender": {"name": "users/107700440653669458242", "type": "HUMAN"},
  "createTime": "2025-12-16T15:30:10.865199Z",
  "text": "Hi @Peter Empson. The new 5L variant is set up...",
  "thread": {"name": "spaces/AAAASSOCJ14/threads/ZZWbEoV7Ol8"},
  "annotations": [
    {
      "type": "USER_MENTION",
      "startIndex": 3,
      "length": 13,
      "userMention": {"user": {"name": "users/113360725466140923732"}}
    }
  ]
}
```

---

## Automated Agents

### Collaber Chat Monitor Agent

**Location:** `agents/collaber-chat-monitor/`
**Schedule:** Every 30 minutes
**Purpose:** Check for new messages and extract client updates

**Workflow:**
1. Fetch messages since last check
2. Filter for Tree2mydoor mentions
3. Extract product/SKU updates
4. Save to `clients/tree2mydoor/collaber-updates/`
5. Create tasks for actionable items

### Message Extraction Tool

**Location:** `tools/collaber-message-extractor/`
**Purpose:** Manual extraction of messages to client folder

---

## Integration with Existing Systems

### Inbox Processing Pipeline

**Collaber Chat messages flow through the standard inbox processing pipeline:**

1. **Collaber Chat Monitor** (`agents/collaber-chat-monitor/`) or **Sync Skill** (`.claude/skills/collaber-chat-sync/`)
   - Fetches messages via MCP API
   - Saves to `!inbox/YYYYMMDD-HHMMSS-google-chat-{message_id}.md`
   - Tracks processed messages in `!inbox/.collaber-chat-state.json`

2. **AI Inbox Processor** (`agents/ai-inbox-processor/`)
   - Detects client from message content (Tree2mydoor)
   - Extracts actionable items and creates tasks
   - Checks for duplicates
   - AI enhancement with Claude

3. **Inbox Processor** (`agents/inbox-processor/`)
   - Routes to final destination: `clients/tree2mydoor/collaber-updates/`
   - Archives processed messages

**Benefits of inbox integration:**
- Consistent processing across all message sources (email, Chat, WhatsApp)
- Automatic client detection and routing
- Duplicate detection and task creation
- AI-powered enhancement and categorisation
- Single source of truth for inbox state

### Email Sync Agent

Replaces the previous Gmail notification-based approach with direct API access for:
- Real-time access to full message history
- Thread context and conversation flow
- Structured message data (no email parsing)
- Emoji reactions and attachments
- No dependency on Gmail notification timing

### Tree2mydoor Client Folder

**Final message destinations:**
- `clients/tree2mydoor/collaber-updates/` - Processed Chat messages
- `clients/tree2mydoor/meeting-notes/` - Important discussions
- `clients/tree2mydoor/documents/` - Strategic documents
- `clients/tree2mydoor/tasks.json` - Auto-created tasks from Chat mentions

---

## Troubleshooting

### OAuth Token Expired

**Symptom:** "OAuth token expired" errors

**Solution:**
```bash
cd infrastructure/mcp-servers/google-chat-mcp-server
rm token.json
# Restart Claude Code - will trigger new OAuth flow
```

### 404 Not Found Errors

**Symptom:** "Google Chat app not found"

**Solution:** Verify Google Chat API is enabled and Chat app is configured in Google Cloud Console

### Permission Denied

**Symptom:** "Permission denied" when accessing space

**Solution:**
- Check you're a member of the Collaber PPC Chat space
- Verify OAuth scopes are correctly configured
- Re-authorize with correct scopes

---

## Message Patterns to Monitor

### Product Updates

**Keywords:**
- "SKU", "product", "variant", "item"
- "back in stock", "out of stock"
- "price", "£", "revised to"
- Tree2mydoor domain links

**Example:**
> "SKU 00813 - The Christmas Holly Tree Gift - back in stock and revised to £56.99"

### Urgent Actions

**Keywords:**
- "@Peter Empson" (direct mentions)
- "urgent", "asap", "today"
- "needs", "requires", "can you"

### Google Ads Related

**Keywords:**
- "Google Ads", "PPC", "adwords"
- "headlines", "descriptions", "text assets"
- "campaign", "ad group"
- "ROAS", "spend", "budget"

---

## Rate Limits

**Google Chat API Quotas:**
- 1,500 requests per minute (per project)
- No documented per-day limits

**Monitoring Agent:**
- Runs every 30 minutes = 48 requests/day
- Well within quota limits

---

## Security Notes

- OAuth credentials stored in `credentials.json` (gitignored)
- OAuth token auto-refreshes (no manual intervention)
- Read-only access by default (messages.readonly scope)
- Send message capability available but unused

---

## Future Enhancements

**Potential Additions:**
1. Sentiment analysis on client messages
2. Automatic Google Ads campaign updates from SKU changes
3. Integration with product feed monitoring
4. Slack/email notifications for urgent mentions
5. AI-powered message summarisation

---

## Related Documentation

- `infrastructure/mcp-servers/google-chat-mcp-server/README.md` - MCP server details
- `.claude/skills/messaging-processor/skill.md` - Message processing skill
- `agents/google-chat-processor/agent.md` - Original Gmail-based processor (legacy)
- `clients/tree2mydoor/CONTEXT.md` - Tree2mydoor client context

---

## Version History

- **v1.0.0** (2025-12-16) - Initial setup and documentation
  - Google Chat API enabled
  - OAuth configured
  - MCP server tested
  - Collaber PPC Chat access confirmed
