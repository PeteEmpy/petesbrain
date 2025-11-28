# Wispr Flow Integration

**Last Updated:** November 5, 2025

This document describes how to integrate Wispr Flow voice dictation notes with PetesBrain.

---

## Overview

Wispr Flow stores dictated notes in a SQLite database. This integration automatically extracts new notes and routes them to the PetesBrain inbox system for processing.

**Flow:**
```
Wispr Flow (Dictate) → SQLite Database → Importer Script → !inbox/ → Inbox Processor → Routed
```

---

## How It Works

### 1. You Dictate in Wispr Flow
- Use Wispr Flow normally to dictate notes
- Notes are saved to Wispr Flow's local database

### 2. Automatic Import (Every 30 Minutes)
- Importer script runs every 30 minutes via LaunchAgent
- Checks for new notes since last run
- Extracts notes from Wispr Flow database
- Saves each note as markdown in `!inbox/`

### 3. Inbox Processing (Daily at 8 AM)
- Inbox processor reads notes from `!inbox/`
- Routes based on keywords (client:, task:, knowledge:)
- Saves to appropriate locations
- Archives processed notes

---

## Installation

### 1. Script is Already Installed

Location: `agents/wispr-flow-importer/wispr-flow-importer.py`

### 2. Install LaunchAgent

```bash
# Copy LaunchAgent configuration
cp agents/launchagents/com.petesbrain.wispr-flow-importer.plist ~/Library/LaunchAgents/

# Load the agent
launchctl load ~/Library/LaunchAgents/com.petesbrain.wispr-flow-importer.plist

# Verify it's running
launchctl list | grep wispr-flow
```

### 3. Test the Import

```bash
# Run manually to test
python3 agents/wispr-flow-importer/wispr-flow-importer.py

# Check inbox for imported notes
ls -la !inbox/
```

---

## Usage

### Basic Workflow

1. **Dictate** your note in Wispr Flow
2. **Wait** up to 30 minutes (or run manually)
3. **Review** imported note in `!inbox/`
4. **Add routing keywords** if needed
5. **Let it process** (daily at 8 AM) or process manually

### Adding Routing Keywords

After notes are imported to `!inbox/`, you can add keywords to control routing:

**Client-related note:**
```markdown
client: Smythson

# Original Wispr Flow Note Title

[dictated content]
```

**Create a task:**
```markdown
task: Follow up with Devonshire Hotels

# Original Wispr Flow Note Title

[dictated content]
```

**Add to knowledge base:**
```markdown
knowledge: Google Ads

# Original Wispr Flow Note Title

[dictated content]
```

**Without keywords:**
Notes without keywords are saved to `!inbox/processed/` for manual review.

---

## Schedule

### Importer Script
- **Frequency:** Every 30 minutes (1800 seconds)
- **LaunchAgent:** `com.petesbrain.wispr-flow-importer`
- **Log:** `~/.petesbrain-wispr-flow.log`
- **Error Log:** `~/.petesbrain-wispr-flow-error.log`

### Inbox Processor
- **Frequency:** Daily at 8:00 AM
- **LaunchAgent:** `com.petesbrain.inbox-processor`
- **Log:** `~/.petesbrain-inbox.log`

---

## Manual Commands

### Run Importer Manually

```bash
# Import new notes now
python3 agents/wispr-flow-importer/wispr-flow-importer.py
```

### Process Inbox Manually

```bash
# Process all notes in inbox
python3 agents/system/inbox-processor.py
```

### Check Status

```bash
# Check if importer is running
launchctl list | grep wispr-flow

# View recent imports
cat ~/.petesbrain-wispr-flow.log | tail -30

# Check inbox contents
ls -la !inbox/
```

### Force Re-Import All Notes

```bash
# Delete state file to reset
rm shared/data/wispr-flow-state.json

# Run importer (will import last 7 days)
python3 agents/wispr-flow-importer/wispr-flow-importer.py
```

---

## State Management

The importer tracks the last processed timestamp to avoid duplicates.

**State File:** `shared/data/wispr-flow-state.json`

**Contents:**
```json
{
  "last_processed_timestamp": "2025-11-05 20:00:00.000 +00:00",
  "last_run": "2025-11-05T20:00:00"
}
```

**On First Run:**
- No state file exists
- Imports notes from last 7 days
- Creates state file with latest timestamp

**On Subsequent Runs:**
- Reads state file
- Imports only notes newer than last timestamp
- Updates state file

---

## Wispr Flow Database

**Location:** `~/Library/Application Support/Wispr Flow/backups/`

**Format:** SQLite database with backups

**Notes Table Schema:**
```sql
CREATE TABLE `Notes` (
    `id` VARCHAR(36) NOT NULL PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `contentPreview` TEXT NOT NULL,
    `content` TEXT NOT NULL,
    `createdAt` DATETIME NOT NULL,
    `modifiedAt` DATETIME NOT NULL,
    `synced` TINYINT(1) NOT NULL DEFAULT 1,
    `isDeleted` TINYINT(1) NOT NULL DEFAULT 0
);
```

**What We Extract:**
- `id` - Unique identifier
- `title` - Note title (if set)
- `content` - Full note content
- `createdAt` - When note was created
- `modifiedAt` - Last modification time
- `isDeleted` - Skip deleted notes

---

## Troubleshooting

### Importer Not Running

```bash
# Check LaunchAgent status
launchctl list | grep wispr-flow

# If not loaded, load it
launchctl load ~/Library/LaunchAgents/com.petesbrain.wispr-flow-importer.plist

# Check logs for errors
cat ~/.petesbrain-wispr-flow-error.log
```

### No Notes Being Imported

**Check if notes exist:**
```bash
sqlite3 "$HOME/Library/Application Support/Wispr Flow/backups/backup-*.sqlite" \
  "SELECT COUNT(*) FROM Notes WHERE isDeleted = 0"
```

**Check date range:**
- First run imports last 7 days only
- Subsequent runs import since last timestamp
- Delete state file to re-import last 7 days

**Run manually to see output:**
```bash
python3 agents/wispr-flow-importer/wispr-flow-importer.py
```

### Notes Not Being Routed

**Check inbox contents:**
```bash
ls -la !inbox/
```

**Add routing keywords:**
- Open note in `!inbox/`
- Add `client:`, `task:`, or `knowledge:` at top
- Run inbox processor manually

**Process manually:**
```bash
python3 agents/system/inbox-processor.py
```

### Database Not Found

**Check Wispr Flow is installed:**
```bash
ls -la "$HOME/Library/Application Support/Wispr Flow/backups/"
```

**Check backup files exist:**
```bash
ls -la "$HOME/Library/Application Support/Wispr Flow/backups/"/*.sqlite
```

---

## Examples

### Example 1: Client Meeting Note

**Dictate in Wispr Flow:**
> "Meeting with Smythson team. Discussed Q4 strategy. They want to increase budget by 30%. Need to prepare proposal."

**Imported to inbox as:**
`!inbox/20251105-143000-wispr-meeting-with-smythson-team-discussed.md`

**Add routing keyword:**
```markdown
client: Smythson

# Meeting with Smythson team

Discussed Q4 strategy. They want to increase budget by 30%. Need to prepare proposal.

---
*Source: Wispr Flow*
*Created: 2025-11-05 14:30:00.000 +00:00*
```

**After processing:**
Saved to `clients/smythson/documents/inbox-capture-20251105.md`

### Example 2: Quick Task

**Dictate in Wispr Flow:**
> "Review October performance for all clients"

**Imported to inbox as:**
`!inbox/20251105-150000-wispr-review-october-performance.md`

**Add routing keyword:**
```markdown
task: Review October performance for all clients

# Review October performance

Review October performance for all clients

---
*Source: Wispr Flow*
*Created: 2025-11-05 15:00:00.000 +00:00*
```

**After processing:**
Creates Google Task with note content

### Example 3: Knowledge Capture

**Dictate in Wispr Flow:**
> "Learned that Performance Max works best with stable budgets and at least 30 days of history"

**Imported to inbox as:**
`!inbox/20251105-160000-wispr-learned-that-performance-max-works.md`

**Add routing keyword:**
```markdown
knowledge: Performance Max

# PMax Best Practices

Learned that Performance Max works best with stable budgets and at least 30 days of history

---
*Source: Wispr Flow*
*Created: 2025-11-05 16:00:00.000 +00:00*
```

**After processing:**
Added to `roksys/knowledge-base/google-ads/performance-max/`

---

## Best Practices

### 1. Dictate Clearly
- Start with context (client name, topic)
- Use natural language
- Wispr Flow will transcribe accurately

### 2. Review Before Processing
- Check imported notes in `!inbox/` daily
- Add routing keywords for better organization
- Fix any transcription errors

### 3. Use Routing Keywords
- `client: [name]` for client-specific notes
- `task:` for action items
- `knowledge:` for learnings and insights
- No keyword = saved to processed/ for review

### 4. Process Regularly
- Automatic processing daily at 8 AM
- Or run manually when needed
- Keep inbox clean

---

## Advanced Usage

### Customize Import Frequency

Edit LaunchAgent to change from hourly to different schedule:

```bash
# Edit the plist file
nano ~/Library/LaunchAgents/com.petesbrain.wispr-flow-importer.plist

# Change StartInterval (in seconds):
# 1800 = 30 minutes
# 3600 = 1 hour (current)
# 7200 = 2 hours

# Reload after changes
launchctl unload ~/Library/LaunchAgents/com.petesbrain.wispr-flow-importer.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.wispr-flow-importer.plist
```

### Import Older Notes

By default, first run imports last 7 days. To import all notes:

Edit `agents/wispr-flow-importer/wispr-flow-importer.py`:

```python
# Change this line:
AND datetime(createdAt) > datetime('now', '-7 days')

# To import all notes:
# (Remove the date filter)
```

Then delete state and run:
```bash
rm shared/data/wispr-flow-state.json
python3 agents/wispr-flow-importer/wispr-flow-importer.py
```

---

## Future Enhancements

Possible improvements:
- Real-time import (watch for database changes)
- AI-powered routing (auto-detect client names)
- Smart keyword suggestion
- Integration with Wispr Flow's title feature
- Bulk edit imported notes
- Web interface for reviewing imports

---

## Related Documentation

- [Inbox System](INBOX-SYSTEM.md) - How the inbox processor works
- [Client Workflows](CLIENT-WORKFLOWS.md) - Adding context to client files
- [CLAUDE.md](../CLAUDE.md) - Overall architecture

---

**Status:** ✅ Installed and ready to use
**Schedule:** Every hour + daily processing at 8 AM
**Manual Run:** `python3 agents/wispr-flow-importer/wispr-flow-importer.py`
