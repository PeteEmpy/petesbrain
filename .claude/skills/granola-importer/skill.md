---
name: granola-importer
description: Imports Granola meeting notes from Google Docs into client folders with automatic client detection, action item extraction, and Google Tasks creation. Use when user says "import Granola meetings", "sync meeting notes", "process meetings", or needs to import meeting transcripts.
allowed-tools: Bash, Read, Write, mcp__google-tasks__create_task
---

# Granola Meeting Importer Skill

## Instructions

When this skill is triggered:

1. **Determine the import scope**:
   - Recent meetings (default: last 7 days)
   - Specific meeting by document ID
   - All new meetings since last import

2. **Execute the import** using the Google Docs importer:
   ```bash
   python3 agents/granola-google-docs-importer/granola-google-docs-importer.py --days [N]
   ```

3. **Handle the import process**:
   - The importer searches Google Drive for documents matching `"ROK | Granola -"`
   - Parses meeting title, attendees, and transcript
   - Detects client using intelligent matching (email domains, keywords, fuzzy matching)
   - Saves to `clients/[client-name]/meeting-notes/` or `clients/_unassigned/meeting-notes/`
   - Extracts action items and creates Google Tasks
   - Enriches with Granola API attendee data (if available)

4. **Report results**:
   - Number of meetings imported
   - Client assignments
   - Action items created
   - Unmatched meetings (if any)

5. **Handle errors gracefully**:
   - Missing Google Drive credentials
   - API authentication issues
   - Document parsing errors
   - Client detection failures

## Import Workflow

### Step 1: Find Google Docs
- Searches Google Drive for documents matching pattern: `"ROK | Granola -"`
- Filters by modification date (last N days)
- Uses Google Drive API with OAuth credentials

### Step 2: Parse Documents
- Extracts meeting title (from document name or first line)
- Parses attendees list
- Extracts full transcript
- Extracts date/time from document name

### Step 3: Client Detection
Uses 3-tier intelligent detection:
1. **Email Domain Matching** (Primary - Most Accurate)
   - Matches attendee email domains to clients
   - Uses `domain_mappings.yaml` for custom mappings
   - Example: `alex@smythson.com` → `smythson`

2. **Title-Based Detection** (Secondary)
   - Fuzzy string matching against meeting titles
   - Example: "Bright Minds Q4 Review" → `bright-minds`

3. **Content-Based Detection** (Fallback)
   - Analyzes transcript for client mentions
   - Keyword and phrase matching

### Step 4: Enrichment (Optional)
- Matches meeting timestamp with Granola API data
- Enriches attendee information from Granola
- Adds email addresses for better client detection

### Step 5: Create Meeting Files
- Saves to appropriate client folder
- Includes YAML frontmatter with metadata
- Formats with AI-generated summary (if available)
- Includes full transcript

### Step 6: Extract Action Items
- Looks for "Action Items", "Next Steps", "Action Points" sections
- Filters for items assigned to "Peter:" or "Team:"
- Creates Google Tasks in "Client Action Items" list
- Includes meeting context in task notes

### Step 7: Create Review Tasks
- Creates task for reviewing meeting and updating CONTEXT.md
- Includes AI-suggested context updates
- Sets due date 2 days from now

## Usage Examples

### Import Recent Meetings
```
User: "Import Granola meetings from the last week"

Claude (using skill):
- Runs: python3 agents/granola-google-docs-importer/granola-google-docs-importer.py --days 7
- Reports: "Imported 5 meetings: 3 to smythson, 1 to bright-minds, 1 unassigned"
- Lists action items created
```

### Check for New Meetings
```
User: "Any new Granola meetings?"

Claude (using skill):
- Runs import for last 1 day
- Reports: "Found 2 new meetings: [list]"
- Shows client assignments
```

### Import Specific Meeting
```
User: "Import the Granola meeting from yesterday"

Claude (using skill):
- Runs import for last 1 day
- Identifies specific meeting
- Shows import details and action items
```

## Integration Points

### Google Drive API
- Uses OAuth credentials from `shared/mcp-servers/google-drive-mcp-server/`
- Searches Shared Drive for Granola documents
- Fetches document content via Google Docs API

### Granola API (Optional)
- Used for attendee enrichment
- Reads credentials from `~/Library/Application Support/Granola/supabase.json`
- Matches meetings by timestamp
- Extracts attendee email addresses

### Client Detector
- Uses existing client detection logic from `tools/granola-importer/client_detector.py`
- Supports email domain mappings in `tools/granola-importer/domain_mappings.yaml`
- Fuzzy matching for client names

### Google Tasks
- Creates action items in "Client Action Items" task list
- Includes meeting context (title, date, file path)
- Formats as: `[client-name] Task description`

### AI Analysis (Optional)
- Uses Anthropic Claude API for meeting analysis
- Extracts executive summary, strategic decisions, key learnings
- Suggests CONTEXT.md updates
- Requires `ANTHROPIC_API_KEY` environment variable

## File Locations

### Import Script
- Main importer: `agents/granola-google-docs-importer/granola-google-docs-importer.py`
- Client detector: `tools/granola-importer/client_detector.py`
- Granola API: `tools/granola-importer/granola_api.py`

### Output Locations
- Meeting files: `clients/[client-name]/meeting-notes/YYYY-MM-DD-meeting-title-client.md`
- Unassigned: `clients/_unassigned/meeting-notes/`
- History: `shared/data/granola-google-docs-history.json`
- Unmatched: `shared/data/granola-unmatched-meetings.json`

### Configuration
- Domain mappings: `tools/granola-importer/domain_mappings.yaml`
- Google Drive OAuth: `shared/mcp-servers/google-drive-mcp-server/gcp-oauth.keys.json`
- Google Drive tokens: `~/.config/google-drive-mcp/tokens.json`

## Error Handling

### Missing Credentials
- **Google Drive**: Check OAuth setup in `shared/mcp-servers/google-drive-mcp-server/`
- **Granola API**: Verify Granola desktop app is installed and logged in
- **Google Tasks**: Check Google Tasks MCP server configuration

### Document Not Found
- Verify document naming matches: `"ROK | Granola -"`
- Check document is in Shared Drive or "Shared with me"
- Verify document permissions

### Client Detection Failure
- Check `domain_mappings.yaml` for custom mappings
- Review meeting title/transcript for client keywords
- Manually move to correct client folder if needed

### Import Errors
- Check logs: `~/.petesbrain-granola-google-docs.log`
- Verify Python dependencies installed
- Check Google API libraries: `pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`

## Resources

- [Import Documentation](../../../docs/GRANOLA-GOOGLE-DOCS-IMPORTER.md) - Complete setup and usage guide
- [Client Detector](../../../tools/granola-importer/client_detector.py) - Client detection logic
- [Google Drive Setup](../../../shared/mcp-servers/google-drive-mcp-server/README.md) - OAuth configuration

## Notes

- **Primary Source**: Google Docs created by Zapier (not direct Granola API)
- **Document Pattern**: Must match `"ROK | Granola -"` in name
- **Automatic Processing**: Can be scheduled via LaunchAgent
- **De-duplication**: Tracks imported documents in history file
- **Unmatched Meetings**: Saved to `_unassigned` and tracked for reporting
- **Action Items**: Automatically extracted and created as Google Tasks
- **AI Analysis**: Optional feature requiring Anthropic API key

## Related Skills

- Can work with other content sync skills
- Integrates with client management workflows
- Supports task management via Google Tasks

