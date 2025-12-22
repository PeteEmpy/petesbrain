# Collaber Chat Message Extractor

Extracts messages from the Collaber PPC Chat Google Chat space and saves them to the Tree2mydoor client folder.

---

## Quick Start (via Claude Code)

**Extract recent messages:**
```
Extract the last 7 days of Collaber Chat messages
```

**Extract product updates:**
```
Get product updates from Collaber Chat this month
```

**Extract since specific date:**
```
Extract Collaber Chat messages since December 1st
```

---

## Output Location

Messages saved to: `clients/tree2mydoor/collaber-updates/`

**File naming:**
- `collaber-messages-YYYY-MM-DD.md` - Markdown format
- `collaber-messages-YYYY-MM-DD.json` - JSON format

---

## What Gets Extracted

### Message Data

- Timestamp
- Sender
- Text content
- User mentions (@Peter Empson, etc.)
- Links and attachments
- Thread context
- Emoji reactions

### Product Updates

Automatically highlights messages containing:
- SKU numbers
- Price changes
- Stock updates
- Tree2mydoor links
- Product names

---

## Usage Examples

### Extract Last 7 Days

```python
# Via Claude Code MCP tools
messages = mcp__google_chat__list_messages(
    space_name="spaces/AAAASSOCJ14",
    page_size=100,
    order_by="createTime desc"
)

# Save to Tree2mydoor folder
save_messages_markdown(messages, "clients/tree2mydoor/collaber-updates/collaber-messages-2025-12-16.md")
```

### Filter for Product Updates

```python
# Extract only messages with product keywords
product_messages = [
    msg for msg in messages
    if any(keyword in msg.get('text', '').lower()
           for keyword in ['sku', 'price', 'stock', 'product'])
]
```

### Extract Mentions

```python
# Get messages where Peter was mentioned
mentions = [
    msg for msg in messages
    if any(ann.get('type') == 'USER_MENTION'
           for ann in msg.get('annotations', []))
]
```

---

## Output Formats

### Markdown Format

```markdown
# Collaber PPC Chat Messages

**Extracted:** 2025-12-16 15:45:00

---

## Message - 2025-12-16 15:30

**From:** users/107700440653669458242

Hi @Peter Empson. The new 5L variant is set up for the At Peace Rose Bush...

**Mentions/Links:**
- Mentioned: users/113360725466140923732

---
```

### JSON Format

```json
{
  "extracted_at": "2025-12-16T15:45:00",
  "space": "spaces/AAAASSOCJ14",
  "message_count": 10,
  "messages": [
    {
      "name": "spaces/AAAASSOCJ14/messages/...",
      "sender": {"name": "users/...", "type": "HUMAN"},
      "createTime": "2025-12-16T15:30:10.865199Z",
      "text": "Message content...",
      "annotations": [],
      "thread": {"name": "spaces/.../threads/..."}
    }
  ]
}
```

---

## Integration with Monitoring Agent

The `collaber-chat-monitor` agent uses this tool automatically:

- Runs every 30 minutes
- Extracts new messages since last check
- Saves to `clients/tree2mydoor/collaber-updates/`
- Creates tasks for actionable items

---

## Manual Extraction (Advanced)

For standalone Python usage (requires Google Chat API credentials):

```bash
cd tools/collaber-message-extractor
python3 extract_messages.py --days 7 --format markdown
```

**Note:** Manual extraction requires setting up Google Chat API credentials separately from the MCP server.

---

## Message Filtering

### By Keywords

Filter messages containing specific terms:

```python
keywords = ['SKU', 'price', 'Tree2mydoor', 'stock']
filtered = [
    msg for msg in messages
    if any(k.lower() in msg.get('text', '').lower() for k in keywords)
]
```

### By Date Range

```python
from datetime import datetime, timedelta

start_date = datetime.now() - timedelta(days=7)
recent_messages = [
    msg for msg in messages
    if datetime.fromisoformat(msg['createTime'].replace('Z', '+00:00')) > start_date
]
```

### By Sender

```python
# Filter by specific user
gareth_messages = [
    msg for msg in messages
    if msg.get('sender', {}).get('name') == 'users/118380887499517434029'
]
```

---

## Common Patterns

### Extract SKU Updates

```python
import re

sku_pattern = r'SKU[:\s-]*([A-Z0-9-]+)'

for msg in messages:
    text = msg.get('text', '')
    skus = re.findall(sku_pattern, text, re.IGNORECASE)
    if skus:
        print(f"SKUs found: {', '.join(skus)}")
        print(f"Message: {text[:100]}...")
        print()
```

### Extract Price Changes

```python
price_pattern = r'£\s*(\d+(?:\.\d{2})?)'

for msg in messages:
    text = msg.get('text', '')
    if 'price' in text.lower() or '£' in text:
        prices = re.findall(price_pattern, text)
        if prices:
            print(f"Prices: £{', £'.join(prices)}")
            print(f"Context: {text}")
            print()
```

### Extract Tree2mydoor Links

```python
for msg in messages:
    formatted_text = msg.get('formattedText', '')
    if 'tree2mydoor.com' in formatted_text:
        print(f"Tree2mydoor link found in message from {msg.get('createTime')}")
        print(formatted_text)
        print()
```

---

## Troubleshooting

### No Messages Extracted

**Check:**
1. Space ID is correct (`spaces/AAAASSOCJ14`)
2. You have access to the Collaber PPC Chat space
3. OAuth token is valid
4. Date range includes actual messages

### Missing Attachments

Attachments are referenced but not downloaded. To download:

```python
drive_file_id = msg['attachment'][0]['driveDataRef']['driveFileId']
# Use Google Drive API to download
```

### Formatting Issues

If markdown output looks wrong:
- Check for special characters in message text
- Verify markdown escaping
- Use JSON format as alternative

---

## Related Tools

- **Monitoring Agent:** `agents/collaber-chat-monitor/`
- **Messaging Processor:** `.claude/skills/messaging-processor/`
- **Google Chat MCP Server:** `infrastructure/mcp-servers/google-chat-mcp-server/`

---

## Future Enhancements

- Automatic SKU extraction and validation
- Price change detection and alerting
- Link preview generation
- Sentiment analysis on client messages
- Integration with product feed monitoring
