# Granola Google Docs Importer

**New workflow for importing Granola meeting notes via Zapier → Google Docs**

## Overview

This replaces the previous Granola API-based import system. Instead of pulling directly from the Granola API, meetings are now:

1. **Created by Zapier** → Google Doc in Shared Drive
2. **Document naming**: `ROK | Granola - [date] [time]`
3. **Content includes**: Meeting title, attendees, full transcript
4. **Automatically processed** → Client detection → Meeting notes → Action items → Google Tasks

---

## How It Works

### 1. Zapier Setup (External)

Zapier creates Google Docs in your Shared Drive with:
- **Name pattern**: `ROK | Granola - 2025-11-07 14:30`
- **Content structure**:
  ```
  Meeting Title
  
  Attendees:
  - Name 1
  - Name 2
  
  Transcript:
  [Full conversation transcript]
  ```

### 2. Import Process

The importer (`granola-google-docs-importer.py`):
1. **Searches Google Drive** for documents matching `"ROK | Granola -"`
2. **Parses document** to extract:
   - Meeting title
   - Date/time (from filename or content)
   - Attendees list
   - Full transcript
3. **Detects client** using existing client detection logic:
   - Email domain matching (from attendees)
   - Keyword matching (title + transcript)
   - Fuzzy string matching
4. **Saves to**:
   - `clients/[client-name]/meeting-notes/` (if client detected)
   - `clients/_unassigned/meeting-notes/` (if no client detected)
5. **Extracts action items** and creates Google Tasks
6. **Tracks unmatched meetings** for reporting

### 3. Action Items

Action items are extracted using the same logic as the original Granola importer:
- Looks for sections: "Action Items", "Next Steps", "Action Points", "To-Do"
- Filters for items assigned to "Peter" or "Team" (or unassigned)
- Creates Google Tasks in "Client Action Items" task list
- Format: `[client-name] Task description`

### 4. Unmatched Meetings

Meetings that can't be matched to a client are:
- Saved to `clients/_unassigned/meeting-notes/`
- Tracked in `shared/data/granola-unmatched-meetings.json`
- **Included in daily/weekly summary reports** for manual review

---

## Setup

### Prerequisites

1. **Google Drive API** configured and authenticated
   - OAuth credentials: `shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json`
   - Token file: `~/.config/google-drive-mcp/tokens.json` (created via MCP auth)
   - See: `shared/mcp-servers/google-drive-mcp-server/README.md`
   - Must have access to Shared Drive

2. **Python Google API libraries** installed:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

3. **Client Detector** available
   - Located in: `tools/granola-importer/client_detector.py`
   - Uses existing client detection logic

4. **Google Tasks** integration
   - Located in: `shared/google_tasks_client.py`
   - For creating action item tasks

### Installation

1. **Make scripts executable**:
   ```bash
   chmod +x agents/granola-google-docs-importer/granola-google-docs-importer.py
   chmod +x agents/content-sync/fetch-granola-docs.py
   ```

2. **Test import** (manual):
   ```bash
   cd /Users/administrator/Documents/PetesBrain
   python3 agents/granola-google-docs-importer/granola-google-docs-importer.py --days 7
   ```

3. **Set up automated processing** (see LaunchAgent section below)

---

## Usage

### Manual Import

**Import recent documents**:
```bash
python3 agents/granola-google-docs-importer/granola-google-docs-importer.py --days 7
```

**Import specific document** (when called from Claude Code with MCP):
```bash
python3 agents/granola-google-docs-importer/granola-google-docs-importer.py \
  --doc-id "DOCUMENT_ID" \
  --doc-name "ROK | Granola - 2025-11-07 14:30" \
  --doc-content "[document content]"
```

### Automated Import

Set up a LaunchAgent to run automatically (see below).

---

## Integration with Inbox System

**Recommendation**: Process through inbox first for review, then auto-process.

**Option 1: Direct Processing** (Current Implementation)
- Documents are processed immediately
- Client detection happens automatically
- Unmatched meetings flagged for review

**Option 2: Inbox First** (Recommended Enhancement)
- Documents saved to `!inbox/` first
- Inbox processor routes to clients
- Allows for manual review before processing

**To enable inbox routing**, modify the importer to:
1. Save documents to `!inbox/` instead of directly to client folders
2. Let `inbox-processor.py` handle routing
3. Add Granola-specific detection logic to inbox processor

---

## File Structure

```
clients/
  [client-name]/
    meeting-notes/
      2025-11-07-meeting-title-client-name.md
  _unassigned/
    meeting-notes/
      2025-11-07-meeting-title.md

shared/
  data/
    granola-google-docs-history.json      # Import history
    granola-unmatched-meetings.json       # Unmatched meetings list
```

---

## Document Format

### Expected Google Doc Structure

```
Meeting Title Here

Attendees:
- Peter Smith
- John Doe (john@client.com)

Transcript:
[Full conversation transcript here...]

Action Items:
- Peter: Follow up on budget
- Team: Review performance metrics
```

### Parsed Metadata

Each imported meeting includes YAML frontmatter:
```yaml
---
title: Meeting Title
date: 2025-11-07
time: 14:30
attendees:
  - Peter Smith
  - John Doe
client: client-name
source: Google Docs (Zapier)
imported_at: 2025-11-07T14:35:00
---
```

---

## Action Items → Google Tasks

Action items are automatically extracted and created as Google Tasks:

**Task Format**:
- **Title**: `[client-name] Task description`
- **Notes**: 
  ```
  From: Meeting Title
  Date: 2025-11-07
  ```

**Task List**: "Client Action Items" (created automatically if needed)

**Filtering**:
- Only includes items assigned to "Peter", "Team", or unassigned
- Skips items assigned to other people

---

## Unmatched Meetings Reporting

Unmatched meetings are tracked and reported in:

1. **Daily Briefing** (`agents/reporting/daily-briefing.py`)
   - Lists unmatched meetings from last 24 hours
   - Prompts for manual assignment

2. **Weekly Summary** (`agents/reporting/kb-weekly-summary.py`)
   - Includes section: "Unmatched Meetings"
   - Lists all unmatched meetings from last 7 days
   - Provides links to files for review

**To manually assign**:
1. Review meeting in `clients/_unassigned/meeting-notes/`
2. Move file to correct client folder
3. Update `granola-unmatched-meetings.json` (or re-run importer)

---

## Troubleshooting

### Documents Not Found

**Issue**: Importer can't find Google Docs

**Solutions**:
1. Verify OAuth credentials exist: `shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json`
2. Verify token file exists: `~/.config/google-drive-mcp/tokens.json`
   - If missing, run: `npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json`
3. Check document naming matches pattern: `ROK | Granola -`
4. Verify documents are in Shared Drive or "Shared with me"
5. Check document permissions (must be accessible)
6. Verify Google API libraries installed: `pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`

### Client Detection Failing

**Issue**: Meetings going to `_unassigned` incorrectly

**Solutions**:
1. Check `tools/granola-importer/domain_mappings.yaml` for email domain mappings
2. Verify client names in `clients/` directory match expected format
3. Review meeting title/transcript for client keywords
4. Manually move file and update history

### Action Items Not Created

**Issue**: Action items not appearing in Google Tasks

**Solutions**:
1. Verify Google Tasks integration is configured
2. Check task list "Client Action Items" exists
3. Review action item format in transcript
4. Check logs for errors

---

## Migration from Old System

**Old System**: `tools/granola-importer/import_meeting.py`
- Pulled directly from Granola API
- Used `sync_daemon.py` for continuous sync

**New System**: `agents/granola-google-docs-importer/granola-google-docs-importer.py`
- Pulls from Google Docs (created by Zapier)
- Uses Google Drive MCP for access
- Same client detection and action item logic

**Migration Steps**:
1. Set up Zapier workflow (external)
2. Test import with new system
3. Disable old `sync_daemon.py` LaunchAgent
4. Enable new LaunchAgent (see below)
5. Monitor for a few days to ensure all meetings are captured

---

## LaunchAgent Setup

Create LaunchAgent for automated processing:

**File**: `agents/launchagents/com.petesbrain.granola-google-docs-importer.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.granola-google-docs-importer</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/administrator/Documents/PetesBrain/agents/granola-google-docs-importer/granola-google-docs-importer.py</string>
        <string>--days</string>
        <string>7</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/administrator/.petesbrain-granola-google-docs.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/administrator/.petesbrain-granola-google-docs.error.log</string>
</dict>
</plist>
```

**Install**:
```bash
ln -s /Users/administrator/Documents/PetesBrain/agents/launchagents/com.petesbrain.granola-google-docs-importer.plist \
      ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.petesbrain.granola-google-docs-importer.plist
```

**Runs**: Every hour, checks last 7 days

---

## Next Steps

1. ✅ **Create importer script** - Done
2. ✅ **Integrate with Google Drive API** - Complete (uses direct API calls)
3. ⏳ **Test with sample documents** - Ready to test
4. ⏳ **Set up LaunchAgent** - Ready to install
5. ✅ **Update weekly summary** - Complete (includes unmatched meetings)
6. ⏳ **Consider inbox routing** - Optional enhancement

## Status: ✅ Ready for Testing

The importer is fully integrated with Google Drive API and ready to use. To test:

1. Ensure OAuth is set up (see Prerequisites above)
2. Create a test Google Doc named: `ROK | Granola - 2025-11-07 14:30`
3. Run: `python3 agents/granola-google-docs-importer/granola-google-docs-importer.py --days 7`
4. Check output for imported meetings

---

## Questions?

- **Client detection issues**: Check `tools/granola-importer/client_detector.py`
- **Action item extraction**: See `tools/granola-importer/generate_daily_tasks.py`
- **Google Drive access**: See `shared/mcp-servers/google-drive-mcp-server/README.md`

