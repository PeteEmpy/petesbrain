# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository Overview

PetesBrain is an AI-powered business management system for a Google Ads agency. It automates client work through 50 background agents, manages tasks across 30+ clients, and provides AI-powered tools for ad copy generation, reporting, and analysis.

**Key Technologies**: Python 3.13, Flask, MCP (Model Context Protocol), Google/Microsoft Ads APIs, macOS LaunchAgents

---

## Current System Architecture

**⚠️ IMPORTANT**: The system is currently in a pre-migration state. On December 10, 2025, a comprehensive architectural migration was attempted but was rolled back due to widespread agent failures. The documentation below describes the **current, working state** - not an aspirational future architecture.

**For full context on what happened**: See `docs/MIGRATION-POSTMORTEM.md`

### Current Architecture (As of December 11, 2025)

**Agents & Configuration**:
- Agents use LaunchAgent `.plist` files in `~/Library/LaunchAgents/`
- Agent configurations use hardcoded paths (352 locations throughout codebase)
- Some agents have credentials embedded in plist EnvironmentVariables (pre-migration state)
- Individual Python virtual environments per agent or agent group

**MCP Servers & Credentials** (successfully migrated):
- MCP servers configured in `.mcp.json`
- Global `env` section contains shared credentials (ANTHROPIC_API_KEY, GMAIL credentials)
- Individual `env` sections per MCP server for API-specific keys

**Task System** (dual system, does NOT sync):
- Internal `tasks.json` files in `clients/{client}/` for client work
- Google Tasks API for personal reminders and AI-generated suggestions
- These systems are intentionally separate - do NOT mix

**Agent Health** (as of Dec 11, 2025):
- 72 LaunchAgents configured
- 70/72 healthy after emergency fixes
- Core functionality restored (daily reports, email sync, budget monitoring, etc.)

---

## Business Context

Roksys operates as the "Self-Improving Agency" — an AI-powered solo PPC consultancy that scales through automation while maintaining owner expertise and personal service.

**Business context documentation** (helps Claude understand strategy, positioning, values):
- Location: `context/business/`
- Key files:
  - `README.md` - System overview
  - `business-overview.md` - Company, services, revenue model
  - `business-philosophy.md` - "Self-Improving Agency" concept, batch-driven operations, positioning
  - `personal-profile.md` - Peter's work style, preferences, constraints
  - `key-relationships.md` - Client segments, strategic partners
  - `market-position.md` - Competitive landscape, moats, positioning statement

**When to use business context:**
- Strategic decisions (e.g., "Should I use Slack?" → consult batch-driven philosophy)
- Pricing and service scope (e.g., "What should I charge?" → reference business model)
- Client decisions (e.g., "Should I hire?" → consult solo/automation philosophy)
- Market positioning (e.g., "How am I different?" → reference competitive moats)

**Key business facts:**
- Solo operation (Peter Empson, 22+ years PPC experience)
- 12 active clients, £12K-£18K/month MRR
- Goal: £30K/month (15-20 clients) in 6 months
- Batch-driven, asynchronous workflow (email primary, no Slack)
- Automated operations (50+ LaunchAgents, 1,983+ article knowledge base)

---

## Architecture Overview

### Per-Client Data Architecture

Each client has a self-contained folder at `clients/{client-slug}/` with standardised structure:

```
clients/{client-slug}/
├── CONTEXT.md              # Strategic context, platform IDs, voice aliases
├── tasks.json              # Active tasks (internal task system)
├── tasks-completed.md      # Completed task archive
├── emails/                 # Email correspondence
├── meeting-notes/          # Granola AI transcripts
├── reports/                # Weekly/monthly reports
├── documents/              # Strategy docs
└── spreadsheets/           # Data exports
```

**Platform IDs in CONTEXT.md**: Each client's CONTEXT.md contains their Google Ads Customer ID, Merchant Centre ID, GA4 Property ID, and Microsoft Ads Account ID. Use `mcp__google-ads__get_client_platform_ids('client-slug')` to retrieve them programmatically.

**Voice Transcription Aliases**: User inputs via voice dictation. Each CONTEXT.md includes "Voice Transcription Aliases" listing common mishearings (e.g., "Smythson" → "Smithson", "Tree2mydoor" → "tree to my door"). Always check aliases when client names don't match exactly.

### Dual Task System (CRITICAL)

**Two completely independent systems that DO NOT sync:**

| System | Location | Use For |
|--------|----------|---------|
| **Internal Client Tasks** | `clients/{client}/tasks.json` | ALL client work, recurring tasks, multi-step projects |
| **Google Tasks** | Google API ("Peter's List", "Client Work") | Personal reminders, AI-generated suggestions only |

**Decision Rule**:
- Client work? → Internal system (`clients/{client}/tasks.json`)
- Recurring tasks? → Internal system (REQUIRED - Google Tasks has no recurring support)
- Personal reminders? → Google Tasks ("Peter's List")

**Never mix these systems for the same task.** Full details: `docs/TASK-SYSTEM-DECISION-GUIDE.md` (498 lines)

### Parent/Child Task Hierarchy

Internal task system supports parent/child relationships:
- Parent tasks have `id` property
- Child tasks reference parent via `parent_id` property
- Only overdue children appear in daily briefing
- Use cases: meetings with action items, multi-week projects, related initiatives

Example: NMA 3-Week Improvement Plan = 1 parent task + 13 child tasks (Week 1-3 items)

### MCP Server Integration

11 active MCP servers provide direct API access. Configuration in `.mcp.json`:

**Google Services**: google-ads, google-analytics, google-sheets, google-tasks, google-trends, google-drive, google-photos
**Microsoft Services**: microsoft-ads
**Meta Services**: facebook-ads
**E-commerce**: woocommerce (multiple instances)

**Critical Pattern**: Platform IDs stored in `clients/{client}/CONTEXT.md`, extracted via `shared/platform_ids.py` helper. Single source of truth.

### Automated Agent System

50 background agents run via macOS LaunchAgents:
- Daily intel report (7 AM)
- Email sync (continuous)
- AI inbox processor
- Google/Facebook specs monitors
- Budget tracking
- Campaign audits
- Health check
- Tasks backup (daily)

Each agent has `.plist` config in `~/Library/LaunchAgents/`. Logs in `~/.petesbrain-{agent-name}.log`

### Claude Code Skills System

39 active skills in `.claude/skills/`. **Always check skills directory FIRST before searching for scripts.**

Key skills:
- `google-ads-weekly-report` - Comprehensive weekly analysis
- `csv-analyzer` - Analyse CSV exports (Google Ads reports use specialised analyser)
- `email-draft-generator` - Draft client emails (HTML format, British English)
- `task-manager` - Open task UI
- `granola-importer` - Import meeting transcripts
- `experiment-review` - Review A/B tests
- `google-ads-text-generator` - Launch ad copy generator web app

**Skills-First Protocol**: When user says "start", "launch", "run", or "use" ANY tool:
1. Check `.claude/skills/` FIRST
2. If matching skill exists, use Skill tool immediately
3. Only if no skill exists, search for scripts elsewhere

---

## Common Development Commands

### Task Management

**Create client task** (internal system):
```python
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()
service.create_task(
    title='[Client] Task description',
    client='client-slug',
    priority='P1',  # P0/P1/P2/P3
    recurring='weekly'  # or 'monthly', 'custom', None
)
```

**List client tasks**:
```python
service = ClientTasksService()
tasks = service.list_tasks(client='client-slug')
```

**Complete task** (automatically logs to tasks-completed.md):
```python
service.complete_task(client='client-slug', task_id='task-uuid')
```

**Google Tasks** (personal only):
```python
mcp__google_tasks__list_tasks(tasklist_id='...')
mcp__google_tasks__create_task(tasklist_id='...', title='...')
mcp__google_tasks__complete_task(task_id='...')
```

### Google Ads Queries

**CRITICAL: Always use customer-level queries for financial data**

```python
# CORRECT - Customer-level query for spend/revenue
mcp__google_ads__run_gaql(
    customer_id='8573235780',
    manager_id='2569949686',  # Always include for managed accounts
    query='''
        SELECT
            metrics.cost_micros,
            metrics.conversions_value,
            metrics.conversions
        FROM customer
        WHERE segments.date BETWEEN '2025-11-01' AND '2025-11-25'
    '''
)

# WRONG - Campaign-level queries can miss data
# DO NOT USE: FROM campaign (for financial totals)
```

**Get client platform IDs**:
```python
mcp__google_ads__get_client_platform_ids('smythson')
# Returns: {'google_ads_customer_id': '...', 'merchant_centre_id': '...', ...}
```

**Multi-account clients** (e.g., Smythson has UK/USA/EUR/ROW):
- Query all accounts separately
- Sum totals across accounts
- Convert currencies if needed (check CONTEXT.md for reporting currency)

### Running Skills

```python
# Launch skill by name
Skill(command='google-ads-weekly-report')
Skill(command='email-draft-generator')
Skill(command='task-manager')
```

### Email Formatting

**Standard**: HTML (not Markdown) with British English spelling

```html
<p style="margin: 6px 0; line-height: 1.4;">
    Hi [Name],<br><br>

    <strong>Key Point:</strong> Details here.<br><br>

    Let me know if you have questions.
</p>
```

**Delivery**: Save as `.html` file, auto-open in browser for copy/paste into Gmail

### Running Tools

**Google Ads Generator**:
```bash
cd /Users/administrator/Documents/PetesBrain/tools/google-ads-generator
./start.sh  # Opens web interface at http://localhost:5001
```

**Granola Importer**:
```bash
cd /Users/administrator/Documents/PetesBrain/tools/granola-importer
./start.sh  # Starts background daemon (checks every 5 minutes)
```

### Task Overview HTML Generation

```bash
cd /Users/administrator/Documents/PetesBrain
python3 generate-tasks-overview.py
```

Generates HTML dashboard of all tasks. Auto-opens in browser.

### Agent Management

**View agent status**:
```bash
launchctl list | grep petesbrain
```

**View agent logs**:
```bash
tail -f ~/.petesbrain-{agent-name}.log
tail -f ~/.petesbrain-{agent-name}-error.log
```

**Restart agent**:
```bash
launchctl unload ~/Library/LaunchAgents/co.roksys.petesbrain.{agent-name}.plist
launchctl load ~/Library/LaunchAgents/co.roksys.petesbrain.{agent-name}.plist
```

---

## Critical Patterns & Conventions

### British English Standard

**ALL output must use British English spelling**:
- analyse (not analyze)
- optimise (not optimize)
- organise (not organize)
- colour (not color)
- behaviour (not behavior)
- centre (not center)

Applies to: code comments, documentation, tasks, emails, reports, logs - everything.

### Protected Files (NEVER DELETE)

**These file patterns are CRITICAL DATA**:
- `*/tasks.json` - Active tasks (source of truth)
- `*/tasks-completed.md` - Permanent record of completed work
- `data/state/*.json` - System state files

**Rules**:
1. NEVER delete these files - only edit individual entries
2. NEVER overwrite with empty arrays `{"tasks": []}`
3. When completing a task, ONLY remove that specific task from the array
4. Before any bulk operation, verify the file has content
5. `ClientTasksService` has safety checks preventing accidental data loss

**If you're about to delete or clear a tasks.json file - STOP and ask the user first.**

### Task Completion & Archiving

**When completing tasks**:
1. Task marked as completed in `tasks.json`
2. Automatically logged to appropriate `tasks-completed.md`:
   - Client work: `clients/{client}/tasks-completed.md`
   - Personal/Roksys work: `roksys/tasks-completed.md`
3. Task remains in `tasks.json` (not deleted immediately)
4. Manual cleanup after 30 days

**When searching for historical tasks**: Check `*/tasks-completed.md` files, not Google Tasks

### Smart Task Creation from Reports

**Rule**: Only create tasks for P0 (Critical) recommendations that meet thresholds

**Thresholds**:
- ROAS drops >20% week-over-week
- Campaign with 0 conversions + >£50/week spend
- ROAS >15% below target
- Identified waste >£100/month

**Purpose**: Prevent task list flooding while catching genuine issues

### Google Ads Data Accuracy Protocols

**Critical Rules**:
1. Always use customer-level queries (`FROM customer`) for financial totals
2. Always include `manager_id` for managed accounts
3. Query spend AND revenue together (never assume revenue)
4. Query all regional accounts and sum totals (multi-account clients)
5. Present raw API data first before projections
6. Check CONTEXT.md for currency reporting standards

**Why**: Campaign-level queries can miss data. Customer-level queries are source of truth. Incorrect revenue data leads to incorrect strategic decisions.

### Email Sync & Client Organisation

**Incoming emails**: Auto-labelled by `email-auto-label` agent, synced to `clients/{client}/emails/` by `email-sync` agent

**Gmail labels**: Each client has label `Clients/{Client-Name}` and `Clients/{Client-Name}/Sent`

**Email storage**: Saved as markdown files with YAML frontmatter containing metadata (from, to, date, subject, thread_id)

### ROK Ad Copy Specifications

**Google Ads Text Generator** follows strict content structure:

**5 Content Sections**:
1. **Benefits** - Customer-focused value propositions
2. **Technical** - Specifications, features, differentiators
3. **Quirky** - Creative, attention-grabbing copy
4. **CTA** - Call-to-action focused
5. **Brand** - Brand positioning, heritage, trust

**Character Limits** (strictly enforced):
- Headlines: 30 characters max
- Long headlines: 90 characters max
- Descriptions: 90 characters max
- Sitelinks: 25 characters max
- Callouts: 25 characters max

**Export Format**: CSV or copy to clipboard (web interface)

### Client Name Recognition (Voice Input)

**User dictates via voice**. Client names may be transcribed incorrectly.

**Check CONTEXT.md Voice Transcription Aliases** when name doesn't match:
```
**Voice Transcription Aliases**: alias1, alias2, alias3
```

**Common patterns**:
- Words run together: "Superspace" → "Supabase"
- Homophones: "Tree2mydoor" → "tree to my door"
- Phonetic variants: "Smythson" → "Smithson"
- Acronyms: "NDA", "NMA", "JBB", "CCC"

**When creating new clients**: Always add Voice Transcription Aliases to CONTEXT.md

---

## Trigger Phrases & Special Actions

### "Process my task notes" / "Process task notes"

**DO NOT use wispr-flow-importer skill** - that's for voice notes.

**Protocol**:
1. Read `/Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json`
2. For each note, execute the `manual_note` instruction (e.g., "Done" = complete the task)
3. Log completed tasks to `roksys/tasks-completed.md`
4. Remove completed tasks from `roksys/tasks.json` (use Python for JSON editing)
5. Clear notes file: `echo '[]' > data/state/manual-task-notes.json`
6. Regenerate HTML: `python3 generate-tasks-overview.py`

**If file is empty `[]`**: Report "No task notes to process"

---

## Key Documentation Files

### System Architecture
- `docs/TASK-SYSTEM-DECISION-GUIDE.md` - Dual task system explained (498 lines)
- `docs/INTERNAL-TASK-SYSTEM.md` - Per-client architecture (543 lines)
- `docs/DAILY-BRIEFING-SYSTEM.md` - Morning briefing workflow
- `infrastructure/mcp-servers/MCP-IMPLEMENTATION-PATTERNS.md` - MCP patterns

### Operational Guides
- `docs/ADDING-A-NEW-CLIENT.md` - Complete client onboarding
- `docs/AGENT-MONITORING-GUIDE.md` - Agent health monitoring
- `docs/SYSTEM-HEALTH-MONITORING.md` - System monitoring
- `docs/BACKUP-SYSTEM.md` - Backup procedures

### Developer Guides
- `README.md` - Project overview
- `CONTEXT.md` - High-level context (201 lines)
- `.claude/skills/README.md` - Skills documentation
- Tool-specific `README.md` files in `tools/*/`

---

## Common Workflows

### Adding a New Client

1. Create folder structure:
   ```bash
   mkdir -p clients/{client-slug}/{emails,meeting-notes,reports,documents,spreadsheets,briefs,campaigns,knowledge-base,experiments}
   ```

2. Copy templates:
   ```bash
   cp clients/_template/README.md clients/{client-slug}/
   cp clients/_template/CONTEXT.md clients/{client-slug}/
   ```

3. Update CONTEXT.md with:
   - Client name and background
   - Platform IDs (Google Ads, GA4, Merchant Centre, Microsoft Ads)
   - Voice Transcription Aliases
   - Email formatting preferences
   - Manager account IDs

4. Add to inbox processors (`agents/inbox/ai-inbox-processor.py`)

5. Add to email sync (`shared/email-sync/`)

6. Create Gmail labels: `Clients/{Client-Name}`, `Clients/{Client-Name}/Sent`

Full guide: `docs/ADDING-A-NEW-CLIENT.md`

### Creating a New Skill

1. Create directory: `.claude/skills/{skill-name}/`

2. Create `skill.md` with:
   ```markdown
   # {Skill Name}

   ## Description
   [What this skill does]

   ## Allowed Tools
   - Read
   - Bash
   - mcp__google-ads__*

   ## Instructions
   [Detailed execution logic]

   ## Examples
   [Usage examples]
   ```

3. Test via Claude Code:
   ```python
   Skill(command='{skill-name}')
   ```

4. Document in `.claude/skills/README.md`

### Creating a New Agent

1. Create agent directory: `agents/{category}/{agent-name}/`

2. Create Python script with proper error handling and logging:
   ```python
   import logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(levelname)s - %(message)s'
   )
   ```

3. Create LaunchAgent plist in `~/Library/LaunchAgents/`:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>co.roksys.petesbrain.{agent-name}</string>
       <key>ProgramArguments</key>
       <array>
           <string>/path/to/venv/bin/python3</string>
           <string>/path/to/script.py</string>
       </array>
       <key>StartInterval</key>
       <integer>300</integer>
       <key>StandardOutPath</key>
       <string>/Users/administrator/.petesbrain-{agent-name}.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/administrator/.petesbrain-{agent-name}-error.log</string>
   </dict>
   </plist>
   ```

4. Load agent:
   ```bash
   launchctl load ~/Library/LaunchAgents/co.roksys.petesbrain.{agent-name}.plist
   ```

5. Monitor logs:
   ```bash
   tail -f ~/.petesbrain-{agent-name}.log
   ```

### Adding a New MCP Server

1. Create server directory: `infrastructure/mcp-servers/{server-name}/`

2. Implement server (Python or Node.js) following MCP specification

3. Add to `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "{server-name}": {
         "command": "/path/to/venv/bin/python",
         "args": ["/path/to/server.py"],
         "env": {
           "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
         }
       }
     }
   }
   ```

4. Test via MCP tool calls:
   ```python
   mcp__{server-name}__{function-name}(...)
   ```

5. Document in `infrastructure/mcp-servers/README.md`

---

## Environment & Dependencies

### Python Environment

**Version**: Python 3.13
**Virtual Environments**: Each tool/agent has own `venv/`
**Dependencies**: `requirements.txt` per component

### Setting up new tool/agent:
```bash
cd /path/to/component
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Credentials & Authentication

**OAuth Tokens**: `~/.google-ads/`, `~/.config/`
**Service Accounts**: `infrastructure/mcp-servers/*/credentials.json`
**API Keys**: Environment variables in `.env` files (gitignored)
**MCP Config**: `.mcp.json` (references credential paths)

### Required Environment Variables

**For Google Ads Generator**:
```bash
export ANTHROPIC_API_KEY='your-api-key'
```

**For MCP Servers**: Configured in `.mcp.json` env sections

---

## Troubleshooting

### MCP Server Not Loading

Check server location and re-add:
```bash
claude mcp add -s user {server-name} "/path/to/venv/bin/python" "/path/to/server.py"
```

Example (Microsoft Ads):
```bash
claude mcp add -s user microsoft-ads "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/microsoft-ads-mcp-server/.venv/bin/python" "/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/microsoft-ads-mcp-server/server.py"
```

### Agent Not Running

1. Check if loaded:
   ```bash
   launchctl list | grep petesbrain.{agent-name}
   ```

2. Check error logs:
   ```bash
   tail -50 ~/.petesbrain-{agent-name}-error.log
   ```

3. Common issues:
   - OAuth token expired (exit code 78)
   - Python path incorrect in plist
   - Missing environment variables
   - File permissions

### Empty Task Notes

If `manual-task-notes.json` is `[]` after processing, report "No task notes to process" - this is normal.

### Tasks Not Syncing

Tasks between internal system and Google Tasks DO NOT sync. This is by design. Check `docs/TASK-SYSTEM-DECISION-GUIDE.md` to verify correct system usage.

---

## Testing

### Manual Testing

**Task System**:
```python
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()

# Create test task
task = service.create_task(title='[Test] Sample task', client='smythson', priority='P2')

# List tasks
tasks = service.list_tasks(client='smythson')

# Complete task
service.complete_task(client='smythson', task_id=task['id'])

# Verify logged to tasks-completed.md
```

**MCP Servers**:
```python
# Test Google Ads
result = mcp__google_ads__get_client_platform_ids('smythson')
print(result)

# Test Google Tasks
lists = mcp__google_tasks__list_task_lists()
print(lists)
```

**Skills**:
```python
Skill(command='task-manager')  # Should open task UI
```

### Testing Guides

See `docs/TESTING_GUIDE.md` for comprehensive testing procedures

---

## Core Philosophy

**PetesBrain is built on these principles**:

1. **Maximum Automation** - Automate everything that can be automated (50 agents)
2. **Minimal Manual Work** - User focuses on strategy, system handles operations
3. **Comprehensive Context** - Every client has full context in CONTEXT.md
4. **Scalable Architecture** - Per-client folders scale to hundreds of clients
5. **Single Source of Truth** - Platform IDs in CONTEXT.md, tasks in tasks.json
6. **AI-First Design** - Claude AI powers tools, reporting, and analysis
7. **British English** - Consistent language across all output
8. **Data Safety** - Protected files, safety checks, daily backups

---

## Quick Reference

### File Paths

```
/Users/administrator/Documents/PetesBrain/          # Repository root
/Users/administrator/.claude/                       # Global Claude Code config
/Users/administrator/.petesbrain-*.log              # Agent logs
/Users/administrator/Library/LaunchAgents/          # Agent configs
```

### Key Services

| Service | Import Path |
|---------|-------------|
| ClientTasksService | `from shared.client_tasks_service import ClientTasksService` |
| GoogleTasksClient | `from shared.google_tasks_client import GoogleTasksClient` |
| PlatformIDs | `from shared.platform_ids import get_client_platform_ids` |
| DateUtils | `from shared.date_utils import *` |

### MCP Tool Patterns

```python
mcp__google_ads__run_gaql(customer_id, manager_id, query)
mcp__google_ads__get_client_platform_ids(client_name)
mcp__google_tasks__list_tasks(tasklist_id)
mcp__google_tasks__create_task(tasklist_id, title, due)
mcp__google_sheets__read_cells(spreadsheet_id, range)
mcp__microsoft_ads__get_campaigns(customer_id)
```

### Priority Levels

- **P0** - Critical/urgent (blocking issues, time-sensitive)
- **P1** - Important (client requests, optimisations)
- **P2** - Normal (improvements, non-urgent)
- **P3** - Low priority (nice-to-have, future work)

---

**For questions or issues, consult the comprehensive documentation in `docs/` (175+ markdown files).**
