---
name: process-collaber-chat
description: Complete workflow - sync Collaber Chat messages, process through AI inbox, route to Tree2mydoor, create tasks. Use when user says "process Collaber Chat", "sync and process Collaber", or wants full end-to-end Chat processing.
allowed-tools: mcp__google-chat__list_messages, Read, Write, Bash
---

# Process Collaber Chat (Complete Workflow)

**Purpose**: End-to-end workflow that syncs Collaber PPC Chat messages and immediately processes them through the inbox pipeline.

**No manual steps required** - everything flows automatically from Chat → Inbox → AI Processing → Client Folder → Tasks

---

## Complete Workflow

### Step 1: Sync Messages from Chat
1. Load state from `!inbox/.collaber-chat-state.json`
2. Fetch messages via `mcp__google-chat__list_messages()`
3. Filter for new messages (not in processed list)
4. Save each to `!inbox/YYYYMMDD-HHMMSS-google-chat-{id}.md`
5. Update state with new message IDs

### Step 2: Process Through AI Inbox
1. Immediately run `agents/ai-inbox-processor/ai-inbox-processor.py`
2. AI detects client (Tree2mydoor)
3. Extracts SKUs, prices, product info
4. Creates tasks for mentions and action items
5. Checks for duplicates

### Step 3: Route to Client Folder
1. Run `agents/inbox-processor/inbox-processor.py`
2. Routes to `clients/tree2mydoor/collaber-updates/`
3. Moves processed files to archive

### Step 4: Report Results
- Messages synced
- Tasks created
- Files routed
- Summary of product updates

---

## Execution Pattern

```python
# 1. Sync messages (save to !inbox/)
messages = sync_collaber_chat_messages()

# 2. Process through AI inbox
run_bash("cd agents/ai-inbox-processor && python3 ai-inbox-processor.py")

# 3. Route to client folders
run_bash("cd agents/inbox-processor && python3 inbox-processor.py")

# 4. Report
print(f"✅ Processed {len(messages)} messages")
print(f"✅ Routed to Tree2mydoor folder")
print(f"✅ {tasks_created} tasks created")
```

---

## What Gets Auto-Created

### Tasks Created For:
- **Direct mentions** (@Peter Empson)
- **Product updates** requiring Google Ads changes
- **Price changes** needing bid adjustments
- **Urgent requests** (ASAP, urgent, today)

### Files Created:
- `clients/tree2mydoor/collaber-updates/collaber-YYYY-MM-DD.md` - Daily message log
- `clients/tree2mydoor/tasks.json` - Auto-added tasks
- `!inbox/.collaber-chat-state.json` - Updated state

---

## Message Processing Logic

**AI Inbox Processor detects:**
1. **Client**: Tree2mydoor (from space name, message content)
2. **SKUs**: Extracted via regex patterns
3. **Prices**: Extracted from £XX.XX format
4. **Mentions**: Annotations with USER_MENTION type
5. **Links**: Tree2mydoor.com URLs

**Inbox Processor routes based on:**
- Client detection → `clients/tree2mydoor/`
- Message type → `collaber-updates/` subdirectory
- Creates tasks in `tasks.json` if actionable

---

## State Management

**Tracks processed messages to prevent duplicates:**

```json
{
  "last_check_time": "2025-12-16T16:00:00",
  "processed_message_ids": [
    "spaces/AAAASSOCJ14/messages/..."
  ],
  "last_updated": "2025-12-16T16:00:00"
}
```

---

## Example Output

```
🟢 Collaber Chat Processing Complete

📊 Sync Summary:
- Fetched: 10 messages from Collaber PPC Chat
- New: 4 messages
- Saved to: !inbox/

🤖 AI Processing:
- Client detected: Tree2mydoor
- SKUs extracted: 00813, CTG17125, CAMP01
- Prices found: £56.99
- Mentions: 2 (@Peter Empson)

✅ Routing Complete:
- Destination: clients/tree2mydoor/collaber-updates/
- Tasks created: 2
  - [Tree2mydoor] Update Google Ads for Christmas Holly Tree (£56.99)
  - [Tree2mydoor] Review new 5L Rose Bush variant pricing

📋 Product Updates:
- SKU 00813: Christmas Holly Tree - back in stock @ £56.99
- New variant: 5L At Peace Rose Bush (waiting on price)
- Christmas Tree SKUs: CTG17125, 04588, CTG13467
- Camellia SKUs: CAMWSA, CAMP01, CAMR01

Next Steps:
- Check clients/tree2mydoor/tasks.json for new tasks
- Review clients/tree2mydoor/collaber-updates/ for message details
```

---

## Error Handling

### No New Messages
```
✅ No new messages in Collaber Chat
Last check: 2025-12-16 16:00
All caught up!
```

### Processing Errors
```
⚠️  AI inbox processor encountered errors
Check logs: ~/.petesbrain-ai-inbox-processor-error.log
Messages saved but not yet processed
Run manually: cd agents/ai-inbox-processor && python3 ai-inbox-processor.py
```

### OAuth Issues
```
❌ Cannot access Collaber Chat - OAuth token expired
Refreshing token...
✅ Retry successful
```

---

## Monitoring & Automation

### Manual Trigger (On-Demand)
User says:
```
Process Collaber Chat
```

### Automated Schedule (via LaunchAgent)
- Run every 30 minutes
- Checks for new messages
- Processes automatically
- Logs to `~/.petesbrain-collaber-chat-processor.log`

---

## Integration Benefits

**Single workflow replaces:**
1. ~~Manual Chat sync~~
2. ~~Separate AI processing step~~
3. ~~Manual routing to client folder~~
4. ~~Manual task creation~~

**Now:**
- One command → Complete processing
- Messages flow automatically
- Tasks created on-the-fly
- No manual intervention needed

---

## Related Files

- **State:** `!inbox/.collaber-chat-state.json`
- **Output:** `clients/tree2mydoor/collaber-updates/`
- **Tasks:** `clients/tree2mydoor/tasks.json`
- **AI Processor:** `agents/ai-inbox-processor/ai-inbox-processor.py`
- **Inbox Processor:** `agents/inbox-processor/inbox-processor.py`
