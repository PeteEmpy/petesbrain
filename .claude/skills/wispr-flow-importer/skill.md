---
name: wispr-flow-importer
description: Imports Wispr Flow voice dictation notes from SQLite database into PetesBrain inbox system with automatic routing based on keywords. Use when user says "import Wispr notes", "sync voice notes", "process Wispr Flow", or wants to fetch recent dictation notes.
allowed-tools: Bash, Read
---

# Wispr Flow Importer Skill

## Instructions

When this skill is triggered, run the Wispr Flow importer using the manual commands below.

---

## Manual Commands

### Run Importer Manually

```bash
# Import new notes now
python3 agents/content-sync/wispr-flow-importer.py
```

### Process Inbox Manually

```bash
# Process all notes in inbox (routes based on keywords)
python3 agents/system/inbox-processor.py
```

### Check Status

```bash
# Check if importer is running
launchctl list | grep wispr-flow

# View recent imports
tail -30 ~/.petesbrain-wispr-flow.log

# Check for errors
tail -30 ~/.petesbrain-wispr-flow-error.log

# Check inbox contents
ls -la !inbox/
```

### Force Re-Import All Notes

```bash
# Delete state file to reset
rm shared/data/wispr-flow-state.json

# Run importer (will import last 7 days)
python3 agents/content-sync/wispr-flow-importer.py
```

---

## What Happens

When you run the Wispr Flow importer:

1. **Extracts Notes from Database**
   - Reads from Wispr Flow SQLite database: `~/Library/Application Support/Wispr Flow/flow.sqlite`
   - Finds notes newer than last processed timestamp
   - Skips deleted notes (`isDeleted = 0`)

2. **Saves to Inbox**
   - Creates markdown files in `!inbox/`
   - Filename format: `YYYYMMDD-HHMMSS-wispr-[note-title-slug].md`
   - Includes note content, creation date, and source metadata

3. **Routing (via Inbox Processor)**
   - Notes with `client:` keyword → `clients/[client-name]/documents/inbox-capture-YYYYMMDD.md`
   - Notes with `task:` keyword → Creates Google Task
   - Notes with `knowledge:` keyword → Routes to knowledge base
   - Notes without keywords → `!inbox/processed/` for manual review

## File Locations

### Main Scripts
- **Importer**: `agents/content-sync/wispr-flow-importer.py`
- **Inbox Processor**: `agents/system/inbox-processor.py`

### Database
- **Wispr Flow Database**: `~/Library/Application Support/Wispr Flow/flow.sqlite`
- **State File**: `shared/data/wispr-flow-state.json` (tracks last processed timestamp)

### Logs
- **Import Log**: `~/.petesbrain-wispr-flow.log`
- **Error Log**: `~/.petesbrain-wispr-flow-error.log`

### Output Locations
- **Inbox**: `!inbox/YYYYMMDD-HHMMSS-wispr-[title].md`
- **Processed**: `!inbox/processed/` (notes without routing keywords)
- **Client Notes**: `clients/[client-name]/documents/inbox-capture-YYYYMMDD.md`

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

### Manual Run
The importer can be run manually anytime using the commands above.

## Routing Keywords

After notes are imported to `!inbox/`, add keywords at the top to control routing:

### Client Notes
```markdown
client: Smythson

# Your note title
[content]
```
**Routes to:** `clients/smythson/documents/inbox-capture-YYYYMMDD.md`

### Tasks
```markdown
task: Follow up with Devonshire Hotels

# Your note title
[content]
```
**Routes to:** Google Tasks

### Knowledge Base
```markdown
knowledge: Google Ads

# Your note title
[content]
```
**Routes to:** `roksys/knowledge-base/google-ads/`

### No Keyword
Notes without keywords are saved to `!inbox/processed/` for manual review.

## State Management

The importer tracks processed notes to avoid duplicates.

**State File:** `shared/data/wispr-flow-state.json`

**Contents:**
```json
{
  "last_processed_timestamp": "2025-11-08 12:48:31.700 +00:00",
  "last_run": "2025-11-08T12:48:31"
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

## Troubleshooting

### Importer Not Running

```bash
# Check LaunchAgent status
launchctl list | grep wispr-flow

# If not loaded, load it
launchctl load ~/Library/LaunchAgents/com.petesbrain.wispr-flow-importer.plist

# Check logs for errors
tail -50 ~/.petesbrain-wispr-flow-error.log
```

### No Notes Being Imported

**Check if notes exist:**
```bash
sqlite3 "$HOME/Library/Application Support/Wispr Flow/flow.sqlite" \
  "SELECT COUNT(*) FROM Notes WHERE isDeleted = 0"
```

**Check date range:**
- First run imports last 7 days only
- Subsequent runs import since last timestamp
- Delete state file to re-import last 7 days

**Run manually to see output:**
```bash
python3 agents/content-sync/wispr-flow-importer.py
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
ls -la "$HOME/Library/Application Support/Wispr Flow/flow.sqlite"
```

**Verify database exists:**
- Wispr Flow must be installed and running
- Database is created automatically when Wispr Flow is first used
- Check Wispr Flow app is working properly

## Related Skills

- **Granola Importer** - For importing Granola meeting notes
- **Email Sync** - For syncing client emails
- **Inbox Processor** - Processes notes from inbox

## Notes

- **Automatic**: Runs every 30 minutes via LaunchAgent
- **Deduplication**: Tracks processed notes to avoid duplicates
- **Routing**: Notes require keywords for automatic routing
- **Manual Processing**: Inbox processor runs daily or can be run manually
- **State Tracking**: Uses timestamp-based state management

---

**Quick Command**:
```bash
python3 agents/content-sync/wispr-flow-importer.py
```

