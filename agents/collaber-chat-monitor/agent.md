---
name: collaber-chat-monitor
status: active
created: 2025-12-16
---

# Collaber Chat Monitor Agent

## Purpose

Monitors the Collaber PPC Chat Google Chat space for new messages related to Tree2mydoor client work and saves them to `!inbox/` for processing.

**Key Functions:**
- Fetch messages via Google Chat MCP API (direct access, not Gmail notifications)
- Save new messages to `!inbox/` directory
- Messages automatically processed by AI inbox processor
- Client detection, task creation, and routing handled by inbox pipeline
- Replaces Gmail notification-based approach with real-time API access

---

## Schedule

**Frequency:** Every 30 minutes
**Method:** macOS LaunchAgent

---

## Configuration

**Script:** `collaber-chat-monitor.py`
**LaunchAgent:** `config.plist` (to be created)
**Log:** `~/.petesbrain-collaber-chat-monitor.log`

**State File:** `!inbox/.collaber-chat-state.json`
**Output:** `!inbox/` (then processed to `clients/tree2mydoor/collaber-updates/`)

---

## What It Monitors

### Message Types

1. **Product Updates**
   - SKU additions/changes
   - Price updates
   - Stock status changes
   - Product variant additions

2. **Client Communications**
   - Direct mentions (@Peter Empson)
   - Questions requiring response
   - Urgent requests

3. **Strategic Discussions**
   - Google Ads text asset updates
   - Campaign strategy changes
   - Performance feedback

---

## Output Files

### Daily Message Logs

**Location:** `clients/tree2mydoor/collaber-updates/collaber-YYYY-MM-DD.md`

**Format:**
```markdown
# Collaber PPC Chat - 2025-12-16

## 15:30 - Product Update

**From:** Gareth Mitchell

The new 5L variant is set up for the At Peace Rose Bush...

**SKUs:** AT-PEACE-5L
**Products:** At Peace Rose Bush
**Links:** https://tree2mydoor.com/products/at-peace-rose-bush

---
```

### Product Change Summary

**Location:** `clients/tree2mydoor/collaber-updates/product-changes-YYYY-MM-DD.json`

**Format:**
```json
{
  "date": "2025-12-16",
  "changes": [
    {
      "type": "new_variant",
      "sku": "AT-PEACE-5L",
      "product": "At Peace Rose Bush",
      "details": "5L pot instead of 3L pot",
      "timestamp": "2025-12-16T15:30:10Z"
    }
  ]
}
```

---

## Task Creation Rules

### Auto-Create Task When:

1. **Peter is mentioned** directly in message
2. **Action keywords** detected: "can you", "please", "need", "urgent"
3. **Product changes** require Google Ads updates
4. **Price changes** detected (may need bid adjustments)

### Task Format:

```json
{
  "title": "[Tree2mydoor] Update Google Ads for new 5L At Peace Rose Bush variant",
  "client": "tree2mydoor",
  "priority": "P1",
  "source": "Collaber Chat",
  "context": "Gareth mentioned new 5L pot variant - need to add to PMAX text assets"
}
```

---

## Integration Points

### 1. Google Chat MCP Server

Uses `mcp__google-chat__list_messages()` to fetch messages

### 2. Client Tasks Service

Creates tasks via `ClientTasksService.create_task()`

### 3. Product Feed Monitor

Cross-references SKUs with product feed data

### 4. Email Sync

Supplements Gmail notification-based Chat tracking

---

## Message Patterns

### Product Update Pattern

**Triggers:**
- Contains "SKU" or "product"
- Contains price (£XX.XX)
- Contains Tree2mydoor link
- Contains "back in stock", "out of stock", "new variant"

**Example:**
> "SKU 00813 - The Christmas Holly Tree Gift - back in stock and revised to £56.99"

### Action Required Pattern

**Triggers:**
- Direct mention (@Peter Empson)
- Question mark with action keyword
- Words: "can you", "could you", "please update"

**Example:**
> "Hi @Peter Empson can you update the Google Ads text for the new Camellia variants?"

### Urgent Pattern

**Triggers:**
- Words: "urgent", "asap", "today", "now"
- Multiple exclamation marks
- Price increase >10%

**Example:**
> "URGENT: Mini Christmas Tree prices dropped to clear stock - update ads ASAP!!"

---

## Monitoring Workflow

1. **Fetch Messages** - Get messages since last check (30 min window)
2. **Filter Relevant** - Keep only Tree2mydoor/product-related messages
3. **Extract Data** - Pull SKUs, prices, links, mentions
4. **Classify** - Determine if actionable/urgent
5. **Save** - Write to daily log file
6. **Create Tasks** - Auto-create tasks for action items
7. **Update State** - Record last check timestamp

---

## Error Handling

### OAuth Token Expired

**Symptom:** 401 Unauthorized errors

**Solution:** Token auto-refreshes via MCP server

### Space Not Found

**Symptom:** 404 Not Found for space

**Solution:** Verify space ID hasn't changed, check access

### No Messages

**Normal:** Some 30-minute windows may have no messages

**Action:** Log status, update state, continue

---

## Logs

### Success Log

```
2025-12-16 15:45:00 - INFO - Collaber Chat Monitor
2025-12-16 15:45:01 - INFO - Last check: 2025-12-16 15:15:00
2025-12-16 15:45:02 - INFO - Fetched 3 new messages
2025-12-16 15:45:03 - INFO - Found 2 product updates
2025-12-16 15:45:04 - INFO - Created 1 task
2025-12-16 15:45:05 - INFO - ✅ Monitor check complete
```

### Error Log

```
2025-12-16 15:45:00 - ERROR - Failed to fetch messages: OAuth token expired
2025-12-16 15:45:01 - INFO - Retrying with token refresh...
2025-12-16 15:45:05 - INFO - ✅ Retry successful
```

---

## Future Enhancements

1. **Sentiment Analysis** - Detect client satisfaction/frustration
2. **Automatic Google Ads Updates** - Push SKU changes to campaigns
3. **Slack/Email Notifications** - Alert on urgent mentions
4. **Message Summarization** - AI-powered daily digest
5. **Link Preview** - Fetch and display tree2mydoor product details

---

## Related Files

- **MCP Server:** `infrastructure/mcp-servers/google-chat-mcp-server/`
- **Extraction Tool:** `tools/collaber-message-extractor/`
- **Documentation:** `docs/GOOGLE-CHAT-INTEGRATION.md`
- **Client Context:** `clients/tree2mydoor/CONTEXT.md`

---

## Manual Testing

```bash
cd agents/collaber-chat-monitor
python3 collaber-chat-monitor.py
```

**Note:** Requires Claude Code environment with Google Chat MCP server configured.
