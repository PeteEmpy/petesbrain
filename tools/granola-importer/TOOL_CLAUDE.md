# Granola Meeting Importer - Technical Documentation

This document provides detailed technical information about the Granola Meeting Importer tool for Claude Code.

## Architecture Overview

The Granola Meeting Importer is a modular Python tool that automatically imports meeting transcripts and AI-generated notes from Granola AI into the Pete's Brain client management system.

### Core Components

```
tools/granola-importer/
├── granola_api.py              # API client for Granola
├── prosemirror_converter.py    # ProseMirror JSON → Markdown converter
├── client_detector.py          # Intelligent client detection
├── import_meeting.py           # Main import script (CLI)
├── sync_daemon.py              # Background sync daemon
├── install_service.sh          # macOS LaunchAgent installer
├── uninstall_service.sh        # Service uninstaller
├── requirements.txt            # Python dependencies
├── .import_history.json        # Tracks imported meetings (auto-generated)
├── README.md                   # User documentation
└── TOOL_CLAUDE.md             # This file
```

## Component Details

### 1. `granola_api.py` - Granola API Client

**Purpose**: Handles authentication and communication with Granola's API.

**Key Features**:
- Reads credentials from `~/Library/Application Support/Granola/supabase.json`
- Fetches meeting documents via `https://api.granola.ai/v2/get-documents`
- Supports pagination and filtering by date range
- Includes retry logic and error handling

**Main Classes**:
- `GranolaAPI`: Primary API client
  - `get_documents(limit, offset)`: Fetch meetings
  - `get_document_by_id(document_id)`: Fetch specific meeting
  - `get_recent_documents(days)`: Fetch meetings from last N days

**Dependencies**: `requests`

**Error Handling**:
- `FileNotFoundError`: Credentials not found (Granola not installed/logged in)
- `PermissionError`: API authentication failed
- `requests.exceptions.HTTPError`: API request failures

### 2. `prosemirror_converter.py` - Document Converter

**Purpose**: Converts Granola's ProseMirror JSON format to clean Markdown.

**Key Features**:
- Recursive node processing
- Handles all standard Markdown elements (headings, lists, blockquotes, code blocks)
- Preserves inline formatting (bold, italic, links, code)
- Extracts full transcripts if available

**Main Classes**:
- `ProseMirrorConverter`: Document converter
  - `convert(prosemirror_doc)`: Convert ProseMirror JSON → Markdown
  - `_process_node(node)`: Recursively process document nodes
  - `_extract_text(node)`: Extract and format text content

**Main Functions**:
- `extract_transcript(document)`: Extract full transcript from various document structures

**ProseMirror Structure**:
```json
{
  "type": "doc",
  "content": [
    {
      "type": "heading",
      "attrs": {"level": 1},
      "content": [{"type": "text", "text": "Meeting Title"}]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Regular text"},
        {"type": "text", "text": "bold text", "marks": [{"type": "bold"}]}
      ]
    }
  ]
}
```

### 3. `client_detector.py` - Intelligent Client Detection

**Purpose**: Automatically determines which client folder a meeting belongs to using fuzzy matching.

**Two-Stage Detection**:

#### Stage 1: Title-Based Detection (Primary)
- Fuzzy string matching against meeting title
- Generates client name variations:
  - `bright-minds` → ["bright-minds", "bright minds", "brightminds", "Bright Minds", "BrightMinds", "Bright", "Minds"]
- Uses multiple fuzzy algorithms:
  - `fuzz.partial_ratio()`: Substring matching
  - `fuzz.token_sort_ratio()`: Word order independent
  - `fuzz.token_set_ratio()`: Set-based matching
- Threshold: 60% confidence

#### Stage 2: Content-Based Detection (Fallback)
- Analyzes first 1000 chars of meeting content
- Counts direct mentions of client name variations
- Performs phrase-level fuzzy matching
- Calculates confidence: `min(100, (mention_count * 20) + (fuzzy_score_sum / client_count))`
- Higher threshold: 70% confidence (more conservative)

**Main Classes**:
- `ClientDetector`: Detection engine
  - `detect_client(title, content)`: Detect with boolean result
  - `detect_with_confidence(title, content)`: Returns (client, confidence, method)
  - `_match_text(text, threshold)`: Title-based matching
  - `_match_content(content, threshold)`: Content-based matching

**Dependencies**: `thefuzz`, `python-Levenshtein`

**Detection Method Results**:
- `"title"`: Matched via meeting title
- `"content"`: Matched via content analysis
- `"none"`: No match found

### 4. `import_meeting.py` - Main Import Script

**Purpose**: CLI tool for importing Granola meetings into client folders.

**Key Features**:
- Import by document ID, date range, or all new meetings
- Duplicate detection via `.import_history.json`
- Generates standardized filenames: `YYYY-MM-DD-meeting-title-[client].md`
- Creates Markdown files with YAML frontmatter + AI notes + transcript

**Main Classes**:
- `MeetingImporter`: Core import logic
  - `import_document(document)`: Import single meeting
  - `import_by_id(document_id)`: Import specific meeting
  - `import_recent(days, limit)`: Import recent meetings
  - `import_all_new(limit)`: Import all unimported meetings
  - `_create_markdown_file(document, client, output_dir)`: Generate Markdown file

**Output Format**:
```markdown
---
granola_id: abc123
date: 2025-10-28
time: 14:30
duration: 45 minutes
participants: ["John Smith", "Jane Doe"]
client: bright-minds
imported_at: 2025-10-28T15:45:00Z
---

# Meeting Title

## AI-Enhanced Notes

[Granola's formatted notes]

---

## Full Transcript

**[14:30:00] John Smith:**
Let's start...

**[14:31:15] Jane Doe:**
Great idea...
```

**CLI Usage**:
```bash
# Import specific meeting
python3 import_meeting.py --meeting-id "abc123"

# Import last 7 days
python3 import_meeting.py --days 7

# Import all new meetings
python3 import_meeting.py --all

# Import with limit
python3 import_meeting.py --days 30 --limit 10
```

### 5. `sync_daemon.py` - Background Sync Daemon

**Purpose**: Runs continuously in the background to automatically import new meetings.

**Key Features**:
- Checks for new meetings every 5 minutes (configurable)
- Graceful shutdown handling (SIGINT, SIGTERM)
- Logs to `~/.petesbrain-granola-importer.log`
- Retry logic for API failures
- Can run as macOS LaunchAgent for auto-start on login

**Main Classes**:
- `SyncDaemon`: Background service
  - `start()`: Start daemon loop
  - `_sync_meetings()`: Perform single sync
  - `_initialize_importer()`: Setup with retry logic
  - `_signal_handler()`: Handle shutdown signals

**CLI Usage**:
```bash
# Start daemon (runs continuously)
python3 sync_daemon.py

# Run once and exit
python3 sync_daemon.py --once

# Custom check interval (seconds)
python3 sync_daemon.py --interval 600  # 10 minutes
```

**Service Installation**:
```bash
# Install as macOS LaunchAgent
./install_service.sh

# Uninstall service
./uninstall_service.sh
```

## Data Flow

```
┌─────────────────┐
│  Granola API    │
│  (Cloud)        │
└────────┬────────┘
         │ HTTP GET /v2/get-documents
         ↓
┌─────────────────────────┐
│  granola_api.py         │
│  - Fetch documents      │
│  - Authenticate         │
└──────────┬──────────────┘
           │ ProseMirror JSON
           ↓
┌─────────────────────────┐
│  prosemirror_converter  │
│  - Convert to Markdown  │
│  - Extract transcript   │
└──────────┬──────────────┘
           │ Markdown text
           ↓
┌─────────────────────────┐
│  client_detector.py     │
│  - Analyze title        │
│  - Analyze content      │
│  - Match to client      │
└──────────┬──────────────┘
           │ client_slug
           ↓
┌─────────────────────────┐
│  import_meeting.py      │
│  - Generate filename    │
│  - Add YAML frontmatter │
│  - Save to disk         │
└──────────┬──────────────┘
           │ Write file
           ↓
┌─────────────────────────────┐
│  clients/[client]/          │
│    meeting-notes/           │
│      YYYY-MM-DD-title.md    │
└─────────────────────────────┘
```

## Import History Tracking

**File**: `.import_history.json`

**Purpose**: Tracks which meetings have been imported to prevent duplicates.

**Structure**:
```json
{
  "imported": {
    "granola-doc-id-1": {
      "file_path": "/path/to/clients/bright-minds/meeting-notes/2025-10-28-meeting.md",
      "client": "bright-minds",
      "imported_at": "2025-10-28T15:45:00Z"
    },
    "granola-doc-id-2": {
      "file_path": "/path/to/clients/_unassigned/meeting-notes/2025-10-27-call.md",
      "client": null,
      "imported_at": "2025-10-27T14:30:00Z"
    }
  }
}
```

## File Naming Convention

**Format**: `YYYY-MM-DD-meeting-title-slug-[client-slug].md`

**Process**:
1. Extract date from meeting metadata
2. Slugify meeting title:
   - Convert to lowercase
   - Remove special characters
   - Replace spaces with hyphens
   - Truncate to 50 characters
3. Append client slug if detected
4. Add `.md` extension

**Examples**:
- `2025-10-28-q4-strategy-review-bright-minds.md`
- `2025-10-27-uno-lighting-product-launch-uno-lighting.md`
- `2025-10-26-weekly-standup.md` (no client detected)

## Client Folder Assignment

**Priority Order**:
1. If title-based detection succeeds → `clients/[client-slug]/meeting-notes/`
2. If content-based detection succeeds → `clients/[client-slug]/meeting-notes/`
3. If no detection succeeds → `clients/_unassigned/meeting-notes/`

**Client Folder Structure**:
```
clients/
├── bright-minds/
│   ├── meeting-notes/
│   │   ├── 2025-10-28-q4-review-bright-minds.md
│   │   └── 2025-10-15-kickoff-bright-minds.md
│   └── ...
├── uno-lighting/
│   ├── meeting-notes/
│   └── ...
└── _unassigned/
    └── meeting-notes/
        └── 2025-10-26-internal-planning.md
```

## Dependencies

```
requests>=2.31.0       # HTTP client for Granola API
python-dateutil>=2.8.2 # Date/time parsing
thefuzz>=0.20.0        # Fuzzy string matching
python-Levenshtein>=0.21.0  # Fast fuzzy matching (optional but recommended)
pyyaml>=6.0            # YAML frontmatter generation
```

## Configuration

**Environment Variables**: None required (uses Granola's existing credentials)

**Configurable Parameters**:
- `CHECK_INTERVAL` in `sync_daemon.py`: Sync frequency (default: 300 seconds)
- `LOG_FILE`: Daemon log location (default: `~/.petesbrain-granola-importer.log`)
- Title detection threshold: 60% (in `client_detector.py`)
- Content detection threshold: 70% (in `client_detector.py`)

## Error Handling

### Common Errors

1. **Credentials Not Found**
   - Cause: Granola not installed or user not logged in
   - Fix: Install Granola app and log in
   - Location: `~/Library/Application Support/Granola/supabase.json`

2. **API Authentication Failed**
   - Cause: Expired or invalid credentials
   - Fix: Log out and back into Granola app

3. **No Client Match**
   - Cause: Meeting title and content don't match any client
   - Result: Saved to `clients/_unassigned/meeting-notes/`
   - Fix: Manually move to correct client folder

4. **Import History Corrupt**
   - Cause: Malformed JSON in `.import_history.json`
   - Fix: Delete file (will be regenerated)

## Performance Considerations

- **API Rate Limiting**: Granola API has unknown rate limits; daemon uses 5-minute intervals by default
- **Content Analysis**: Only analyzes first 1000 characters to avoid processing huge transcripts
- **Fuzzy Matching**: Uses `python-Levenshtein` for fast C-based fuzzy matching
- **Caching**: Import history prevents re-processing of already imported meetings

## Testing

### Test Individual Components

```bash
# Test API connection
python3 granola_api.py

# Test ProseMirror conversion
python3 prosemirror_converter.py

# Test client detection
python3 client_detector.py
```

### Test Import Workflow

```bash
# Dry run: Import recent meetings (check logs, no side effects if already imported)
python3 import_meeting.py --days 1

# Test daemon once
python3 sync_daemon.py --once
```

## Future Enhancements

Potential improvements:
1. **Interactive Client Selection**: Prompt user when confidence is low (50-70%)
2. **Webhook Support**: Real-time import via Granola webhooks (if they add this)
3. **Email Notifications**: Alert when new meetings are imported
4. **Web Dashboard**: View import history and reassign meetings via browser
5. **Multi-Client Detection**: Handle meetings with multiple clients
6. **Custom Detection Rules**: User-defined keywords → client mappings

## Troubleshooting

### Daemon Not Starting
```bash
# Check credentials exist
ls -la ~/Library/Application\ Support/Granola/

# Check Python dependencies
pip3 list | grep -E "requests|thefuzz|pyyaml"

# View logs
tail -f ~/.petesbrain-granola-importer.log
```

### Meetings Not Auto-Detected
```bash
# Test detection manually
python3 client_detector.py

# Check client folders exist
ls clients/

# Review unassigned meetings
ls clients/_unassigned/meeting-notes/
```

### Service Not Running
```bash
# Check LaunchAgent status
launchctl list | grep granola

# Reload service
launchctl unload ~/Library/LaunchAgents/com.petesbrain.granola-importer.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.granola-importer.plist
```

## Integration with Pete's Brain

This tool follows Pete's Brain's modular architecture:
- Self-contained under `tools/granola-importer/`
- Independent virtual environment
- Detailed `TOOL_CLAUDE.md` documentation
- User-facing `README.md`
- Integrates with existing `clients/` structure

See `CLAUDE.md` in project root for overall architecture guidelines.
