# Automated Workflows - Detailed Reference

Pete's Brain includes several automated workflows that run in the background to keep data synchronized, send summary emails, and track tasks.

## Weekly Meeting Review Email System

**Location**: `shared/scripts/weekly-meeting-review.py`
**Purpose**: Automatically review past week's meetings and completed tasks, send summary email
**Status**: Active, production-ready

### What It Does

1. Scans `clients/*/meeting-notes/` for meetings in past 7 days
2. Scans `shared/data/tasks-completed.json` for completed tasks in past 7 days
3. Reads each meeting's notes and transcript
4. Uses Claude API to analyze meetings for:
   - Key decisions and action items
   - Strategic insights
   - Client concerns or requests
   - Performance discussions
   - Budget or timeline changes
5. Generates structured weekly summary email including:
   - List of meetings with previews
   - Completed tasks grouped by client (Roksys Internal vs Client-specific)
6. Sends email via Gmail API

### Running Manually

```bash
cd /Users/administrator/Documents/PetesBrain
GOOGLE_APPLICATION_CREDENTIALS=shared/email-sync/credentials.json \
  shared/email-sync/.venv/bin/python3 shared/scripts/weekly-meeting-review.py
```

### Automated Schedule

- **When**: Every Monday at 9 AM
- **LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.weekly-review.plist`
- **Log**: Check `~/.petesbrain-weekly-review.log` (if configured)

### Configuration

- **Email template**: Embedded in script
- **Email subject**: "📅 Weekly Review: Meetings & Tasks - {date}"
- **Recipient**: Configured in script (petere@roksys.co.uk)
- **Date range**: Last 7 days (configurable in script)
- **Tasks source**: `shared/data/tasks-completed.json`

---

## Knowledge Base Weekly Summary Email

**Location**: `shared/scripts/knowledge-base-weekly-summary.py`
**Purpose**: Automatically review and summarize knowledge base activity, including automated news monitoring
**Status**: Active, production-ready

### What It Does

1. **Automated Industry News Monitoring Results**:
   - Gathers Google Ads industry articles imported by `industry-news-monitor.py`
   - Gathers AI news articles imported by `ai-news-monitor.py`
   - Shows top-scoring articles (relevance scores 6-10)
   - Highlights most active sources and emerging themes
2. Scans AI newsletters and emails from inbox
3. Gathers new knowledge base documents from all categories
4. Uses Claude API to analyze and create comprehensive summary with sections:
   - 🤖 Automated Industry Monitoring (Google Ads + AI news)
   - AI News Highlights (organized by topic)
   - Knowledge Base Additions (by category)
   - Key Insights for ROK (actionable takeaways)
   - This Week in Numbers (key statistics)
5. Sends formatted HTML email via Gmail API

### Running Manually

```bash
cd /Users/administrator/Documents/PetesBrain
ANTHROPIC_API_KEY="your-key" shared/email-sync/.venv/bin/python3 shared/scripts/knowledge-base-weekly-summary.py
```

### Automated Schedule

- **When**: Every Monday at 9 AM
- **LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.kb-summary.plist`

### Configuration

- **Email subject**: "📚 Knowledge Base Weekly Summary - {date range}"
- **Recipient**: Configured in script (petere@roksys.co.uk)
- **Date range**: Last 7 days
- **Integrates with**: `industry-news-monitor.py`, `ai-news-monitor.py`, `knowledge-base-processor.py`

### Benefits

- See what industry news was automatically monitored and imported
- Stay current with AI developments relevant to marketing
- Track knowledge base growth and curation
- Get AI-powered insights and strategic takeaways
- Zero manual effort required

---

## Industry News Monitoring

**Location**: `shared/scripts/industry-news-monitor.py`
**Purpose**: Automatically monitor RSS feeds from top Google Ads industry websites
**Status**: Active, production-ready

### What It Does

1. Monitors RSS feeds from 9 respected industry sources every 6 hours
2. Uses Claude API to score each article for relevance (0-10 scale)
3. Imports articles scoring 6+ to knowledge base inbox
4. Articles automatically processed and categorized by existing inbox system

### Sources Monitored

- Search Engine Land (Google Ads & PPC)
- Search Engine Journal (PPC)
- Google Ads Blog (Official)
- Think with Google
- WordStream Blog
- PPC Hero
- Neil Patel Blog
- Unbounce Blog

### Running Manually

```bash
ANTHROPIC_API_KEY="your-key" shared/email-sync/.venv/bin/python3 shared/scripts/industry-news-monitor.py
```

### Automated Schedule

- **When**: Every 6 hours
- **LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.industry-news.plist`
- **Log file**: `~/.petesbrain-industry-news.log`

### Configuration

- **Relevance threshold**: 6/10 minimum (configurable in script)
- **State tracking**: `shared/data/industry-news-state.json`
- **Initial run**: Processes articles from last 7 days on first run

### Documentation

See `roksys/knowledge-base/INDUSTRY-NEWS-MONITORING.md` for complete details.

---

## AI News Monitoring

**Location**: `shared/scripts/ai-news-monitor.py`
**Purpose**: Automatically monitor RSS feeds from top AI and machine learning news websites
**Status**: Active, production-ready

### What It Does

1. Monitors RSS feeds from 12 respected AI news sources every 6 hours
2. Uses Claude API to score each article for relevance to AI in marketing/advertising (0-10 scale)
3. Imports articles scoring 6+ to knowledge base inbox
4. Articles automatically processed and categorized by existing inbox system

### Sources Monitored

**Marketing AI**:
- Marketing AI Institute
- MarTech
- Adweek

**Major AI Companies**:
- OpenAI Blog
- Google AI Blog
- Microsoft AI Blog
- Anthropic News

**AI News & Analysis**:
- MIT Technology Review
- VentureBeat
- AI News

**Practical AI/ML**:
- Machine Learning Mastery
- Towards Data Science

### Running Manually

```bash
ANTHROPIC_API_KEY="your-key" shared/email-sync/.venv/bin/python3 shared/scripts/ai-news-monitor.py
```

### Automated Schedule

- **When**: Every 6 hours
- **LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.ai-news.plist`
- **Log file**: `~/.petesbrain-ai-news.log`

### Configuration

- **Relevance threshold**: 6/10 minimum (configurable in script)
- **State tracking**: `shared/data/ai-news-state.json`
- **Initial run**: Processes articles from last 7 days on first run

### Scoring Criteria

- **HIGH (8-10)**: AI tools for marketing, generative AI, marketing automation, AI strategy
- **MEDIUM (5-7)**: General AI trends, AI product launches, ML fundamentals
- **LOW (0-4)**: Pure academic research, non-marketing AI applications

---

## Knowledge Base Processor

**Location**: `shared/scripts/knowledge-base-processor.py`
**Purpose**: Automatically process and categorize files dropped into knowledge base inbox
**Status**: Active, production-ready

### What It Does

1. User drops files into `roksys/knowledge-base/_inbox/` (emails, PDFs, video transcripts, articles)
2. Processor runs every 6 hours (automated via LaunchAgent)
3. Content analyzed with Claude API to determine topic and category
4. Files formatted as markdown and moved to appropriate category folder
5. Knowledge base index updated automatically

### Running Manually

```bash
python3 shared/scripts/knowledge-base-processor.py
```

### Automated Schedule

- **When**: Every 6 hours
- **LaunchAgent**: Configured in `roksys/knowledge-base/setup-automation.sh`
- **Logs**: `~/.petesbrain-knowledge-base.log` and `shared/data/kb-processing.log`

### Documentation

See `roksys/knowledge-base/QUICKSTART.md` and `EMAIL-INTEGRATION.md` for complete details.

---

## Google Tasks Tracking & CONTEXT.md Integration

**Location**: `shared/scripts/tasks-monitor.py`
**Purpose**: Automatically track Google Tasks lifecycle and sync to CONTEXT.md and tasks-completed.md
**Status**: Active, production-ready

### What It Does

1. Polls Google Tasks API every 6 hours
2. Detects whether tasks are for specific clients or Roksys internal work
3. **NEW TASK CREATION** - When task created with substantial notes (>50 characters):
   - Adds task to `clients/[client-name]/CONTEXT.md` under "Planned Work" section
   - Includes full task notes, status (📋 In Progress), and hidden task ID for tracking
4. **TASK COMPLETION** - When task marked complete:
   - Moves task from "Planned Work" → "Completed Work" in CONTEXT.md
   - Updates status to ✅ Completed with date
   - Also logs to `tasks-completed.md` for historical record
5. Integrates with weekly review email to show completed tasks grouped by client

### Running Manually

```bash
cd /Users/administrator/Documents/PetesBrain
GOOGLE_APPLICATION_CREDENTIALS=shared/mcp-servers/google-tasks-mcp-server/credentials.json \
  shared/mcp-servers/google-tasks-mcp-server/.venv/bin/python3 shared/scripts/tasks-monitor.py
```

### Automated Schedule

- **When**: Every 6 hours (21600 seconds)
- **LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.tasks-monitor.plist`
- **Log file**: `~/.petesbrain-tasks-monitor.log`

### Client Detection Logic

- Checks task list name, task title, and notes for client mentions
- Matches against all client folder names in `clients/` directory
- Special handling for abbreviations (e.g., "T2MD" → tree2mydoor, "OTC" → otc)
- If no client detected → categorized as "Roksys Internal"

### File Outputs

- `clients/[client-name]/CONTEXT.md` - "Planned Work" and "Completed Work" sections
- `clients/[client-name]/tasks-completed.md` - Historical log of completed tasks
- `roksys/CONTEXT.md` - Roksys internal tasks
- `roksys/tasks-completed.md` - Historical log of internal tasks
- `shared/data/tasks-completed.json` - Central JSON log for weekly email

### Task Notes Are Critical

Task notes often contain important status information:
- "Completed but waiting for customer response"
- "Analysis done but client needs to approve changes"
- "Fixed temporarily, may need further investigation"

Always read task notes carefully when analyzing client work and reference them when discussing what's been done.

### Weekly Email Integration

Weekly review email includes completed tasks grouped by:
- **🏢 Roksys Internal** (purple styling)
- **👤 Client Name** (green styling, grouped by client)

Shows task title, completion date, task list, and full notes to help track what work has been done across all clients.

### User Workflow (Zero Manual Steps)

1. Create task in Google Tasks with detailed notes (>50 chars)
2. System auto-adds to CONTEXT.md "Planned Work" (within 6 hours)
3. Work on the task
4. Mark complete in Google Tasks
5. System auto-moves to "Completed Work" (within 6 hours)

### Configuration

- **Minimum note length for CONTEXT.md tracking**: 50 characters
- **Clients list**: Auto-loaded from `clients/` directory
- **Task state file**: `shared/data/tasks-state.json`
- **Completions log**: `shared/data/tasks-completed.json`

---

## Email Sync System

**Location**: `shared/email-sync/`
**Purpose**: Sync Gmail emails to client folders as markdown
**Status**: Active, production-ready

### What It Does

1. Monitors Gmail for client communications
2. Identifies client from email metadata (labels, subject, sender)
3. Exports email as markdown with YAML frontmatter
4. Saves to `clients/[client-name]/emails/YYYY-MM-DD_*.md`

### Configuration

- **Service account credentials**: `shared/email-sync/credentials.json`
- **Client mapping**: Configured in script

---

## Granola Meeting Import System

**Location**: `tools/granola-importer/`
**Purpose**: Automatically import meeting transcripts from Granola AI
**Status**: Active, production-ready

### What It Does

1. Polls Granola API every 5 minutes for new meetings
2. Two-stage client detection:
   - Stage 1: Analyzes meeting title for client names
   - Stage 2: If unclear, analyzes meeting content
3. Saves both AI notes and full transcript as markdown
4. Exports to `clients/[client-name]/meeting-notes/` or `roksys/meeting-notes/`

### Client Assignment Validation

- Auto-assignment may be incorrect for internal/company meetings
- User should periodically run `./shared/scripts/review-meeting-client.sh` to validate
- Mis-assigned meetings can be moved to correct location

### Running

```bash
cd tools/granola-importer
./start.sh  # Starts background daemon
```

### Documentation

See `tools/granola-importer/README.md` for complete details.

---

## Google Sheets Automated Exports

**Location**: `shared/mcp-servers/google-sheets-mcp-server/export_experiments_sheet.py`
**Purpose**: Export ROK Experiments Google Sheet to CSV
**Status**: Active, production-ready

### What It Does

Exports the ROK Experiments Google Sheet to CSV files every 6 hours.

### Automated Schedule

- **When**: Every 6 hours
- **LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.googlesheets.export.plist`

### Output Files

- `roksys/spreadsheets/rok-experiments-client-notes.csv` - Timestamped experiment log
- `roksys/spreadsheets/rok-experiments-client-list.csv` - Simple list of all ROK clients

### Data Freshness

CSV files are auto-updated every 6 hours from the [ROK | Experiments Google Sheet](https://docs.google.com/spreadsheets/d/18K5FkeC_E__jj2BZO8UPrEH_EWh4K36WC-CGtI6aQUE/)

---

## LaunchAgent Best Practices & Requirements

### Suppress Background Activity Notifications

**CRITICAL**: All PetesBrain LaunchAgents must include `ProcessType: Background` to suppress macOS notifications.

**System-wide setting** (already applied):
```bash
defaults write com.apple.backgroundtaskmanagementagent.faceless BAHelperShowsUserNotification -bool false
```

**Per-agent requirement** (must be in ALL .plist files):
```xml
<key>ProcessType</key>
<string>Background</string>
```

**Location**: Add before the final `</dict>` tag in the plist file.

**Why this matters**:
- Prevents "Python 3 is running in the background" notifications
- Improves user experience (no notification spam)
- Required for all 50+ PetesBrain agents

**For new agents**: Use the script to add ProcessType automatically:
```bash
python3 shared/scripts/add-process-type-to-plists.py
```

**For manual creation**: Include ProcessType in your plist template:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.agent-name</string>

    <key>ProgramArguments</key>
    <array>
        <string>/path/to/python3</string>
        <string>/path/to/agent.py</string>
    </array>

    <!-- Other configuration here -->

    <key>ProcessType</key>
    <string>Background</string>
</dict>
</plist>
```

**Verification**: Check all plists have ProcessType:
```bash
grep -L "ProcessType" ~/Library/LaunchAgents/com.petesbrain.*.plist
# Should return nothing - all should have it
```

**Last Updated**: November 18, 2025 - All 91 plists updated with ProcessType
