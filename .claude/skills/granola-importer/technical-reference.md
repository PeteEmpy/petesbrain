# Granola Importer - Technical Reference

## Architecture Overview

The Granola importer uses a **Google Docs → Zapier → Import** workflow:

```
Granola Meeting
    ↓
Zapier (External)
    ↓
Google Doc Created ("ROK | Granola - [date] [time]")
    ↓
Google Drive API Search
    ↓
Document Parsing & Client Detection
    ↓
Save to clients/[client]/meeting-notes/
    ↓
Extract Action Items → Google Tasks
```

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

### Document Naming Pattern
- **Pattern**: `ROK | Granola - [date] [time]`
- **Examples**:
  - `ROK | Granola - 2025-11-07 14:30`
  - `ROK | Granola - 2025-11-07T17:41:50+00:00`

## Client Detection Logic

### Priority Order

1. **Email Domain Matching** (Highest Priority)
   - Extracts email addresses from attendees
   - Matches domains to client folders
   - Uses `domain_mappings.yaml` for custom mappings
   - Example: `collaber.agency` → `tree2mydoor`

2. **Title-Based Detection**
   - Fuzzy string matching (Levenshtein distance)
   - Normalizes client names (lowercase, hyphens)
   - Example: "Bright Minds Q4 Review" → `bright-minds`

3. **Content-Based Detection**
   - Analyzes first 1000 characters of transcript
   - Counts client name mentions
   - Phrase matching for common patterns

### Domain Mappings

Edit `tools/granola-importer/domain_mappings.yaml`:
```yaml
"collaber.agency": "tree2mydoor"
"agency-name.com": "client-slug"
```

## Action Item Extraction

### Patterns Detected
- `### Action Items`
- `### Next Steps`
- `### Action Points`
- `### To-Do`
- `Action Items:`
- `Next Steps:`

### Filtering Logic
- Includes items with `Peter:` prefix
- Includes items with `Team:` prefix
- Includes unassigned items (no person prefix)
- Excludes items assigned to other people

### Google Tasks Format
- **Title**: `[client-name] Task description`
- **Notes**: 
  ```
  From: Meeting Title
  Date: 2025-11-07
  ```
- **List**: "Client Action Items" (auto-created)

## File Output Format

### Markdown Structure
```markdown
---
title: Meeting Title
date: 2025-11-07
time: 14:30
attendees:
  - Peter Smith
  - John Doe (john@client.com)
client: client-name
source: Google Docs (Zapier)
imported_at: 2025-11-07T14:35:00
---

# Meeting Title

**Date:** 2025-11-07 14:30

## Executive Summary
[AI-generated if available]

## Attendees
- Peter Smith
- John Doe

## Strategic Decisions
[AI-extracted if available]

## Key Learnings
[AI-extracted if available]

## Transcript
[Full transcript content]
```

### Filename Convention
- Format: `YYYY-MM-DD-meeting-title-slug-client-slug.md`
- Max title length: 50 characters
- Duplicates: Appends `-1`, `-2`, etc.

## API Integration

### Google Drive API
- **Endpoint**: Google Drive API v3
- **Authentication**: OAuth 2.0
- **Credentials**: `shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json`
- **Tokens**: `~/.config/google-drive-mcp/tokens.json`
- **Scope**: `https://www.googleapis.com/auth/drive.readonly`

### Google Docs API
- **Endpoint**: Google Docs API v1
- **Used for**: Fetching document content
- **Method**: `documents().get(documentId=doc_id)`

### Granola API (Optional)
- **Endpoint**: `https://api.granola.ai/v2`
- **Purpose**: Attendee enrichment
- **Credentials**: `~/Library/Application Support/Granola/supabase.json`
- **Method**: Matches meetings by timestamp (±2 hours)

### Google Tasks API
- **Purpose**: Create action items
- **List**: "Client Action Items"
- **Integration**: Via `shared/google_tasks_client.py`

## Error Scenarios

### 1. Google Drive Authentication Failed
**Symptoms**: "OAuth credentials not found"
**Solution**: 
- Verify `gcp-oauth.keys.json` exists
- Run: `npx @piotr-agier/google-drive-mcp auth --credentials ./gcp-oauth.keys.json`

### 2. Documents Not Found
**Symptoms**: "No documents found"
**Solution**:
- Verify document naming matches pattern
- Check document is in Shared Drive
- Verify document permissions

### 3. Client Detection Failed
**Symptoms**: Meeting saved to `_unassigned`
**Solution**:
- Add domain mapping to `domain_mappings.yaml`
- Check client folder names match expected format
- Manually move file and update history

### 4. Action Items Not Created
**Symptoms**: No tasks in Google Tasks
**Solution**:
- Verify Google Tasks MCP configured
- Check action item format in transcript
- Review logs for errors

## Dependencies

### Python Packages
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
pip install pyyaml requests python-dateutil thefuzz python-Levenshtein beautifulsoup4
```

### Optional
- `anthropic` - For AI analysis
- Google Tasks client - For action item creation

## History Tracking

### Import History
- **File**: `shared/data/granola-google-docs-history.json`
- **Format**:
```json
{
  "imported": {
    "doc_id": {
      "file_path": "clients/client/meeting-notes/file.md",
      "client": "client-slug",
      "imported_at": "2025-11-07T14:35:00"
    }
  },
  "last_check": "2025-11-07T14:35:00"
}
```

### Unmatched Meetings
- **File**: `shared/data/granola-unmatched-meetings.json`
- **Format**:
```json
[
  {
    "title": "Meeting Title",
    "date": "2025-11-07",
    "doc_id": "doc_id",
    "doc_name": "ROK | Granola - ...",
    "detected_at": "2025-11-07T14:35:00"
  }
]
```

## Automation

### LaunchAgent Setup
- **File**: `agents/launchagents/com.petesbrain.granola-google-docs-importer.plist`
- **Schedule**: Every hour
- **Command**: `python3 agents/granola-google-docs-importer/granola-google-docs-importer.py --days 7`
- **Logs**: `~/.petesbrain-granola-google-docs.log`

### Manual Execution
```bash
# Import last 7 days
python3 agents/granola-google-docs-importer/granola-google-docs-importer.py --days 7

# Import last 1 day
python3 agents/granola-google-docs-importer/granola-google-docs-importer.py --days 1

# Import specific document
python3 agents/granola-google-docs-importer/granola-google-docs-importer.py \
  --doc-id "DOCUMENT_ID" \
  --doc-name "ROK | Granola - 2025-11-07 14:30" \
  --doc-content "[content]"
```

## Migration from Old System

### Old System (Deprecated)
- **Location**: `tools/granola-importer/import_meeting.py`
- **Method**: Direct Granola API
- **Status**: Still works but replaced by Google Docs workflow

### New System (Current)
- **Location**: `agents/granola-google-docs-importer/granola-google-docs-importer.py`
- **Method**: Google Docs from Zapier
- **Status**: Active and recommended

### Migration Steps
1. Set up Zapier workflow (external)
2. Test import with new system
3. Disable old `sync_daemon.py` LaunchAgent
4. Enable new LaunchAgent
5. Monitor for a few days

## Troubleshooting Checklist

- [ ] Google Drive OAuth credentials exist
- [ ] Google Drive token file exists and is valid
- [ ] Document naming matches pattern `"ROK | Granola -"`
- [ ] Documents are in Shared Drive or "Shared with me"
- [ ] Python dependencies installed
- [ ] Client detector can access client folders
- [ ] Google Tasks MCP configured (for action items)
- [ ] Granola API credentials available (for enrichment)
- [ ] Import history file is writable

