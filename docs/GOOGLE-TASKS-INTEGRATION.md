# Google Tasks Integration

**Status:** ✅ Active  
**Last Updated:** 2025-11-05

## Overview

PetesBrain now integrates with Google Tasks! When you process inbox items with `task:` keywords, they automatically create tasks in Google Tasks that you can access on your phone, web, or any device.

## Features

- ✅ **Automatic Task Creation** - Tasks from inbox automatically appear in Google Tasks
- ✅ **Due Date Parsing** - Supports natural language ("Thursday this week", "tomorrow", "end of week")
- ✅ **Mobile Access** - View and complete tasks on any device
- ✅ **Local + Cloud** - Tasks stored both locally (markdown) and in Google Tasks
- ✅ **Task Linking** - Local todos include Google Task ID for reference
- ✅ **Existing Todo Migration** - Script to migrate historical todos

## How It Works

### 1. Create Inbox Item with Task Keyword

```markdown
# In !inbox/my-task.md

task: Review Q4 budgets

Need to check all client spending against targets.

Due: Friday
```

### 2. Process Inbox (Daily at 8 AM or Manual)

```bash
# Automatic: Runs daily at 8:00 AM
# Manual: Run anytime
python3 agents/system/inbox-processor.py
```

### 3. Task Created in Both Places

**Local Todo:** `todo/20251105-review-q4-budgets.md`
```markdown
# review q4 budgets

**Created:** 2025-11-05 10:30
**Source:** my-task.md
**Google Task ID:** abc123xyz

## Details
Need to check all client spending against targets.
Due: Friday

## Status
- [ ] Todo
```

**Google Tasks:** Task appears in "Peter's List"
- Title: "review q4 budgets"
- Notes: Full details
- Due date: Next Friday (automatically calculated)

## Due Date Formats

The system understands natural language:

| You Write | Interprets As |
|-----------|---------------|
| `Due: tomorrow` | Next day |
| `Due: Thursday` | Next Thursday |
| `Due: Thursday this week` | This week's Thursday |
| `Due: end of week` | This Friday |
| `Due: next week` | 7 days from now |
| `Due: 2025-11-07` | Exact date |

## Using Google Tasks

### On Mobile
1. Download **Google Tasks** app (iOS/Android)
2. Open app → Look for **"PetesBrain"** list
3. Your tasks are there!

### On Web
1. Go to https://tasks.google.com
2. Select **"PetesBrain"** list
3. View, complete, or edit tasks

### In Gmail
1. Open Gmail → Right sidebar
2. Click Tasks icon
3. Select **"PetesBrain"** list

## Migrating Existing Todos

If you have existing local todos, migrate them to Google Tasks:

```bash
cd /Users/administrator/Documents/PetesBrain
shared/mcp-servers/google-tasks-mcp-server/.venv/bin/python3 \
  shared/migrate-todos-to-google-tasks.py
```

This will:
- ✅ Create Google Tasks for all local todos
- ✅ Add Google Task IDs to local files
- ✅ Skip todos already migrated
- ✅ Preserve due dates and details

## Technical Details

### File Structure

```
PetesBrain/
├── shared/
│   ├── google_tasks_client.py          # Python client for Google Tasks API
│   ├── migrate-todos-to-google-tasks.py # Migration script
│   └── mcp-servers/
│       └── google-tasks-mcp-server/
│           ├── .venv/                   # Python virtual environment
│           ├── token.json               # OAuth token
│           └── credentials.json         # OAuth credentials
├── agents/
│   └── system/
│       └── inbox-processor.py          # Enhanced with Google Tasks
└── todo/
    └── *.md                             # Local todos with Google Task IDs
```

### Authentication

Uses OAuth 2.0 with Google Tasks API:
- **Token:** `shared/mcp-servers/google-tasks-mcp-server/token.json`
- **Scopes:** `https://www.googleapis.com/auth/tasks`
- **Auto-refresh:** Token refreshes automatically when expired

### API Requirements

**Due Date Format:**
- **MUST use RFC 3339 timestamp format:** `YYYY-MM-DDTHH:MM:SSZ`
- **Example:** `2025-11-06T00:00:00Z` (for November 6th, 2025)
- **Simple date format WILL FAIL:** `2025-11-06` returns "Request contains an invalid argument"
- **Time portion is discarded:** Only the date is used, but full timestamp required by API

### Python Environment

The integration uses a dedicated Python virtual environment with required packages:
- `google-api-python-client` - Google APIs
- `google-auth` - Authentication
- `google-auth-oauthlib` - OAuth flow
- `google-auth-httplib2` - HTTP library

**Python Path:** `shared/mcp-servers/google-tasks-mcp-server/.venv/bin/python3`

### LaunchAgent

The inbox processor LaunchAgent uses the venv Python:

```xml
<key>ProgramArguments</key>
<array>
    <string>/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-tasks-mcp-server/.venv/bin/python3</string>
    <string>/Users/administrator/Documents/PetesBrain/agents/system/inbox-processor.py</string>
</array>
```

## Future Enhancements

### Bi-Directional Sync ✅ IMPLEMENTED

**Status:** ✅ Complete - See [Bi-Directional Task Sync](BI-DIRECTIONAL-TASK-SYNC.md)

The system now supports:
- ✅ Mark complete in Google Tasks → Updates local todo
- ✅ Periodic sync agent (checks every 6 hours for Google → Local)
- ✅ Local → Google sync script (runs every hour)
- ✅ Status sync between systems
- ✅ Title, notes, and due date sync

**Implementation:** 
- `agents/system/tasks-monitor.py` - Syncs Google Tasks → Local files
- `agents/system/sync-todos-to-google-tasks.py` - Syncs Local files → Google Tasks

## Troubleshooting

### "Could not create Google Task" Error

**Issue:** Python can't find Google API libraries

**Solution:** Use the venv Python:
```bash
shared/mcp-servers/google-tasks-mcp-server/.venv/bin/python3 agents/system/inbox-processor.py
```

### "OAuth credentials not valid" Error

**Issue:** Token expired or missing

**Solution:** Re-authenticate:
```bash
cd shared/mcp-servers/google-tasks-mcp-server
.venv/bin/python3 setup_oauth.py
```

### Tasks Not Appearing in Google Tasks

**Check:**
1. Is the PetesBrain list created? (Should auto-create)
2. Check Google Tasks web: https://tasks.google.com
3. Refresh the app/page

### Duplicate Tasks

**Cause:** Running migration script multiple times

**Fix:** The script skips tasks with Google Task IDs, but if you manually delete the ID line, they'll re-migrate.

**Prevention:** Don't delete the `**Google Task ID:**` line from local todos.

## Examples

### Client Task with Due Date

```markdown
# In !inbox/smythson-review.md

task: Review Smythson Q4 performance

Analyze Shopping campaign results and prepare recommendations.

Due: Thursday this week
client: Smythson
```

**Result:**
- Local todo: `todo/20251105-review-smythson-q4-performance.md`
- Google Task: "review smythson q4 performance" (Due: 2025-11-07)

### Quick Task (No Due Date)

```markdown
# In !inbox/idea.md

task: Research new PMax features

Check Google Ads blog for recent Performance Max updates.
```

**Result:**
- Local todo: `todo/20251105-research-new-pmax-features.md`
- Google Task: "research new pmax features" (No due date)

### Multiple Tasks in One Day

```markdown
# File 1
task: Call Devonshire
Due: tomorrow

# File 2
task: Update Smythson budget
Due: tomorrow

# File 3
task: Review Superspace metrics
Due: tomorrow
```

**Result:** All three appear in Google Tasks with same due date, separately tracked.

## Benefits

### Mobile Access
- ✅ Check tasks on phone during meetings
- ✅ Complete tasks from anywhere
- ✅ Get reminders (if enabled in Google Tasks)

### Centralization
- ✅ One place for all tasks
- ✅ No more "where did I write that?"
- ✅ Searchable across devices

### Integration
- ✅ Works with Google ecosystem (Gmail, Calendar, etc.)
- ✅ Can use voice commands ("Hey Google, add task...")
- ✅ Integrates with third-party apps via Google Tasks API

### Local Backup
- ✅ Still have local markdown files
- ✅ Version controlled (Git)
- ✅ Searchable locally
- ✅ Never lose data even if API changes

## Statistics

**Integration Status:**
- ✅ Google Tasks API: Connected
- ✅ OAuth Authentication: Active
- ✅ Inbox Processor: Enhanced
- ✅ LaunchAgent: Updated
- ✅ Existing Todos: Migrated (4 todos)

**Task Lists:**
- **PetesBrain** (default) - All tasks created here
- Can create additional lists via Google Tasks web/app

---

**Related Documentation:**
- [Inbox Processing System](../docs/INBOX-SYSTEM.md)
- [Automation Overview](../docs/AUTOMATION.md)
- [Agents README](../agents/README.md)

