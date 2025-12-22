---
name: collaber-chat-sync
description: Syncs messages from Collaber PPC Chat to !inbox/ for processing. Use when user says "sync Collaber Chat", "check Collaber Chat messages", or wants to import Google Chat messages from Collaber.
allowed-tools: mcp__google-chat__list_messages, mcp__google-chat__get_space, Read, Write
---

# Collaber Chat Sync Skill

**Purpose**: Fetch messages from Collaber PPC Chat space and save them to !inbox/ for processing by the AI inbox processor.

**Primary Client**: Tree2mydoor

---

## Configuration

**Space ID**: `spaces/AAAASSOCJ14`
**Space Name**: Collaber PPC Chat
**State File**: `!inbox/.collaber-chat-state.json`
**Output Directory**: `!inbox/`

---

## Workflow

1. **Load State** - Read `!inbox/.collaber-chat-state.json` to get last check time and processed message IDs
2. **Fetch Messages** - Use `mcp__google-chat__list_messages()` to get recent messages
3. **Filter New** - Skip messages already in `processed_message_ids`
4. **Format** - Convert each message to markdown format
5. **Save to Inbox** - Write to `!inbox/YYYYMMDD-HHMMSS-google-chat-{message_id}.md`
6. **Update State** - Add new message IDs to processed list
7. **Process Messages** - Automatically run AI inbox processor on new messages
8. **Route to Client** - Inbox processor routes to Tree2mydoor folder
9. **Report** - Show summary of messages processed and tasks created

---

## Message Format

Save messages as markdown in this format:

```markdown
# Google Chat Message (via MCP API)

**Space:** Collaber PPC Chat
**From:** {user_id}
**Time:** YYYY-MM-DD HH:MM
**Message ID:** {message_name}

---

{message text}

**Annotations:**
- Mentioned: {user}
- Link: {url}

**Attachments:**
- {filename} ({content_type})
  Drive ID: {drive_file_id}

**Thread:** {thread_name}

**Reactions:**
- {emoji} ({count})

---

**Source:** Google Chat API (MCP)
**Space:** Collaber PPC Chat
```

---

## State File Structure

```json
{
  "last_check_time": "2025-12-16T15:45:00",
  "processed_message_ids": [
    "spaces/AAAASSOCJ14/messages/ZZWbEoV7Ol8.NtbzhFb7y70",
    "spaces/AAAASSOCJ14/messages/ZZWbEoV7Ol8.ZZWbEoV7Ol8"
  ],
  "last_updated": "2025-12-16T15:45:05"
}
```

---

## Execution Steps

### 1. Load State

```python
import json
from pathlib import Path

state_file = Path('!inbox/.collaber-chat-state.json')

if state_file.exists():
    with open(state_file, 'r') as f:
        state = json.load(f)
        processed_ids = set(state.get('processed_message_ids', []))
        last_check = state.get('last_check_time')
else:
    processed_ids = set()
    last_check = None
```

### 2. Fetch Messages

```python
messages_response = mcp__google_chat__list_messages(
    space_name="spaces/AAAASSOCJ14",
    page_size=50,
    order_by="createTime desc"
)

all_messages = messages_response.get('messages', [])
```

### 3. Filter New Messages

```python
new_messages = [
    msg for msg in all_messages
    if msg.get('name') not in processed_ids
]
```

### 4. Format and Save Each Message

For each message:

```python
# Extract data
sender_name = msg.get('sender', {}).get('name', 'Unknown')
sender_id = sender_name.split('/')[-1]
create_time = msg.get('createTime', '')
text = msg.get('text', '')
message_name = msg.get('name', '')
message_id = message_name.split('/')[-1]

# Format timestamp for filename
from datetime import datetime
dt = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
date_str = dt.strftime('%Y%m%d-%H%M%S')

# Generate filename
safe_id = message_id.replace('.', '-').replace('_', '-')[:20]
filename = f"{date_str}-google-chat-{safe_id}.md"

# Build markdown content (see format above)
# Save to !inbox/{filename}
```

### 5. Update State

```python
# Add new message IDs to processed list
for msg in new_messages:
    processed_ids.add(msg.get('name'))

# Save updated state
state = {
    'last_check_time': datetime.now().isoformat(),
    'processed_message_ids': list(processed_ids),
    'last_updated': datetime.now().isoformat()
}

with open(state_file, 'w') as f:
    json.dump(state, f, indent=2)
```

### 6. Report Results

```
✅ Collaber Chat Sync Complete

📊 Summary:
- Fetched: {total_count} messages
- New: {new_count} messages
- Saved to: !inbox/
- State updated

Next Steps:
- Run ai-inbox-processor to process new messages
- Messages will be routed to Tree2mydoor client folder
```

---

## Integration with Inbox Processing

**After sync, messages flow through:**

1. **AI Inbox Processor** (`agents/ai-inbox-processor/`)
   - Detects client (Tree2mydoor)
   - Extracts actionable items
   - Checks for duplicates
   - Creates tasks if needed

2. **Inbox Processor** (`agents/inbox-processor/`)
   - Routes to `clients/tree2mydoor/collaber-updates/`
   - Archives processed messages

---

## Usage Examples

### Manual Sync

User says:
```
Sync Collaber Chat messages
```

Skill:
1. Fetches last 50 messages
2. Filters for new ones
3. Saves to !inbox/
4. Reports count

### Check Recent Messages

User says:
```
Check for new Collaber Chat messages
```

Skill:
1. Fetches messages since last check
2. Shows preview of new messages
3. Saves to inbox

### Sync Specific Date Range

User says:
```
Sync Collaber Chat messages from last week
```

Skill:
1. Fetches messages from date range
2. Filters for new ones
3. Saves and reports

---

## Product Update Detection

**Messages containing:**
- SKU numbers (e.g., "SKU 00813", "CAMWSA")
- Price changes (£XX.XX)
- Tree2mydoor links
- Stock updates ("back in stock", "new variant")

**Are automatically flagged by AI inbox processor for:**
- Task creation
- Client routing to Tree2mydoor
- Priority classification

---

## Error Handling

### No New Messages

```
✅ No new Collaber Chat messages
Last check: 2025-12-16 15:30:00
All caught up!
```

### OAuth Token Expired

```
❌ OAuth token expired
Running token refresh...
✅ Retry successful
```

### Space Not Accessible

```
❌ Cannot access Collaber PPC Chat space
Check:
- Space ID is correct
- You're a member of the space
- OAuth permissions include chat.messages.readonly
```

---

## Monitoring Pattern

**For automated monitoring:**

1. Create LaunchAgent to run this skill every 30 minutes
2. Or trigger manually when needed
3. Messages automatically flow through inbox processing
4. Tasks created for actionable items

---

## Related Files

- **Agent:** `agents/collaber-chat-monitor/collaber-chat-monitor.py`
- **MCP Server:** `infrastructure/mcp-servers/google-chat-mcp-server/`
- **Documentation:** `docs/GOOGLE-CHAT-INTEGRATION.md`
- **Client:** `clients/tree2mydoor/CONTEXT.md`
