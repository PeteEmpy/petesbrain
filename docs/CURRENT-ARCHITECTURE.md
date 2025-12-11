# Current Architecture (December 11, 2025)

## Status: Pre-Migration State

**Important**: This document describes the PetesBrain system as it currently exists, following a failed architectural migration on December 10, 2025. The system has been rolled back to its pre-migration state, with only partial migration improvements retained.

For the full story of what happened, see `docs/MIGRATION-POSTMORTEM.md`.

---

## System Overview

PetesBrain is an AI-powered business automation system for a Google Ads agency, consisting of:
- **72 LaunchAgent-based background workers** (70/72 currently healthy)
- **30+ client management folders** with tasks, emails, reports, and documents
- **11 MCP servers** providing API access to Google, Microsoft, Meta, and WooCommerce platforms
- **Task management system** (dual system: internal JSON + Google Tasks)
- **Automation tools** for reporting, analysis, and optimization

---

## Architecture Components

### 1. LaunchAgent-Based Agents

**Configuration**:
- Agents defined via `.plist` XML files in `~/Library/LaunchAgents/`
- Each plist specifies:
  - Python executable path
  - Script file location
  - Schedule (StartCalendarInterval for periodic tasks, StartInterval for daemons)
  - Environment variables
  - Log file paths
  - KeepAlive status

**Execution Model**:
- **Periodic agents**: Run on specified schedule (daily at 7am, twice daily, etc.)
- **Daemon agents**: Keep running with automatic restart (KeepAlive=true)
- **One-time agents**: Run once and exit

**Current Issues (Pre-Migration)**:
- 352 hardcoded absolute paths throughout codebase
- Some agents have plaintext API keys in plist EnvironmentVariables:
  - 12 agents: `ANTHROPIC_API_KEY` embedded
  - 4 agents: `GMAIL_APP_PASSWORD` and `GMAIL_USER` embedded
- Individual virtual environments per agent (1.8GB total disk usage)
- No centralized path configuration

**Critical Agents (Core Functionality)**:
- **daily-intel-report** - Generates morning briefing (7:00 AM daily)
- **ai-inbox-processor** - Processes Google Chat and messages
- **email-sync** - Auto-labels and syncs emails to client folders
- **budget-monitor** - Tracks campaign spend vs targets
- **disapproval-monitor** - Alerts on product feed disapprovals

**Status**: 70 of 72 agents healthy. 2 agents may have issues (status uncertain).

**Health Check**:
```bash
launchctl list | grep petesbrain | grep "^-[^0]"  # Shows unhealthy agents
```

---

### 2. MCP Servers (Model Context Protocol)

**Purpose**: Provide Claude with direct API access to external services

**Successfully Migrated** (credentials in `.mcp.json`):
- `google-ads-mcp-server` - Google Ads API
- `google-analytics-mcp-server` - GA4 API
- `google-sheets-mcp-server` - Google Sheets API
- `google-tasks-mcp-server` - Google Tasks API
- `google-photos-mcp-server` - Google Photos API
- `google-trends-mcp-server` - Google Trends API
- `microsoft-ads-mcp-server` - Microsoft Ads API
- `facebook-ads-mcp-server` - Meta Ads API
- `woocommerce-mcp-server` - WooCommerce API (multi-instance)
- `prestashop-mcp-server` - PrestaShop API
- `google-drive-mcp-server` - Google Drive API

**Configuration** (in `.mcp.json`):
```json
{
  "mcpServers": {
    "google-ads": {
      "command": "/path/to/venv/bin/python",
      "args": ["server.py"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  },
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-...",
    "GMAIL_USER": "...",
    "GMAIL_APP_PASSWORD": "..."
  }
}
```

**Credential Management**:
- Global `env` section contains shared credentials (successfully centralized)
- Per-server `env` sections for API-specific keys
- All MCP servers work correctly with this configuration

---

### 3. Client Management Structure

**Directory Layout**:
```
clients/{client-slug}/
├── CONTEXT.md              # Strategic context, platform IDs, voice aliases
├── tasks.json              # Active tasks (internal task system)
├── tasks-completed.md      # Completed task archive
├── emails/                 # Email correspondence
├── meeting-notes/          # Granola AI transcripts
├── reports/                # Weekly/monthly reports
├── documents/              # Strategy documents
└── spreadsheets/           # Data exports
```

**Platform IDs** (stored in each client's CONTEXT.md):
- Google Ads Customer ID(s)
- Google Merchant Centre ID(s)
- GA4 Property ID
- Microsoft Ads Account ID

**30+ Supported Clients**:
- Smythson
- Superspace
- Devonshire Hotels
- Tree2mydoor
- Uno Lighting
- Wheatybags
- Clear Prospects (multi-brand)
- And 23+ others

---

### 4. Task Management System (Dual System)

**Two Independent Systems** (intentionally separate, do NOT sync):

#### Internal Client Tasks (`clients/{client}/tasks.json`)
- **Purpose**: Track all client-related work
- **Format**: JSON array with task objects
- **Recurring**: Supports weekly, monthly, custom recurring tasks
- **Parent/Child**: Tasks can have parent-child relationships (meetings with action items, etc.)
- **Completed**: Archive to `tasks-completed.md`
- **Usage**: All client work, multi-step projects, recurring maintenance
- **Tool**: `ClientTasksService` Python class

#### Google Tasks (via Google Tasks API)
- **Purpose**: Personal reminders and AI-generated suggestions
- **Format**: Google Tasks lists ("Peter's List", "Client Work")
- **Recurring**: NOT supported (API limitation)
- **Completed**: Can mark as done, but not archived
- **Usage**: Personal reminders, AI brainstorm results, quick notes
- **Decision Rule**: If it's recurring or client work, use internal system

**Example Correct Usage**:
```python
# Client work → Internal system
service.create_task(
    title='[Smythson] Review Q4 performance',
    client='smythson',
    recurring='monthly'
)

# Personal reminder → Google Tasks
mcp__google_tasks__create_task(
    tasklist_id='tasks/@default',
    title='Call Peter about project status'
)
```

**Critical Rule**: Never create the same task in both systems

---

### 5. Path Configuration

**Current State**: Hardcoded absolute paths (352 locations)

**Example Paths**:
```
/Users/administrator/Documents/PetesBrain.nosync/
├── clients/{client}/tasks.json
├── agents/daily-intel-report/daily-intel-report.py
├── infrastructure/mcp-servers/google-ads-mcp-server/
├── shared/scripts/email-sync.py
├── tools/google-ads-generator/
└── [etc.]
```

**Hardcoding Issue**:
- Not portable (assumes specific macOS user account)
- Hard to refactor or move directories
- Difficult to test on different machines
- **Dec 10 Migration Planned**: Introduce `shared/paths.py` with environment variable-based discovery (FAILED, rolled back)

**Current Workaround**: All agents expect this exact directory structure

---

### 6. Credential Management

**Current State** (Pre-Migration):

**In `.mcp.json` (Global)** ✅:
```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-...",
    "GMAIL_USER": "petere@roksys.co.uk",
    "GMAIL_APP_PASSWORD": "...",
    "WORDPRESS_USER": "...",
    "WORDPRESS_PASSWORD": "..."
  }
}
```

**In LaunchAgent Plist Files** ❌ (Not secure):
- 12 agents have `ANTHROPIC_API_KEY`
- 4 agents have `GMAIL_APP_PASSWORD` and `GMAIL_USER`
- Example agents: ai-inbox-processor, daily-intel-report, email-sync

**Dec 10 Migration Planned** (FAILED):
- Move all credentials to macOS Keychain
- Use `shared/secrets.py` for Keychain access
- Remove plaintext credentials from plist files
- **Status**: Rolled back due to import errors

**Security Assessment**:
- ⚠️ Risk: Plaintext credentials in plist XML files
- ✅ Improvement: MCP credentials in `.mcp.json` (Dec 10 migration success)
- ⚠️ Still needed: Keychain-based secrets for agents

---

### 7. Virtual Environments

**Current State** (Pre-Migration):

**Individual VEnvs per Agent**:
- Most agents have their own Python virtual environment
- Located in agent directories: `agents/{agent-name}/.venv/`
- Each has separate `requirements.txt`
- Total disk usage: ~1.8GB

**System Python**:
- Some agents use `/usr/local/bin/python3` directly
- System Python at `/usr/bin/python3` (macOS built-in)

**Dec 10 Migration Planned** (FAILED):
- Consolidate into 3 shared venvs:
  - `venv-google` - Google services (Ads, Analytics, Sheets, etc.)
  - `venv-ads` - Ad platform APIs (Microsoft, Facebook, etc.)
  - `venv-tools` - Shared tools and utilities
- Expected size: 680MB (62% reduction)
- Status: Rolled back due to import errors and missing dependencies

**Current Workaround**: Individual venvs per agent/group, ~1.8GB usage

---

### 8. Logging

**Current State**:
- Agents write to `~/.petesbrain-{agent-name}.log`
- Format: Text/shell-formatted output (print statements)
- Location: User home directory logs

**Dec 10 Migration Planned** (FAILED):
- Introduce `shared/structured_logging.py`
- All agents output JSON-formatted logs
- Machine-readable for monitoring and analysis
- Status: Rolled back, not implemented

**Current Limitations**:
- Hard to parse programmatically
- Mixed formats (print statements, custom formats)
- Difficult to aggregate and analyze

---

## System Health Status

### Agent Status Summary (Dec 11, 2025)

**Total**: 72 agents configured
**Healthy**: 70 agents (97.2%)
**Unhealthy**: 2 agents (2.8%)

**Critical Agents** (all healthy ✅):
- daily-intel-report: Exit code 0
- ai-inbox-processor: Exit code 0
- email-sync: Exit code 0
- budget-monitor: Exit code 0
- disapproval-monitor: Exit code 0

**Other Healthy Agents**: 65 additional agents at exit code 0

**Current Issues** (2 agents):
- Status unclear for 2 agents (likely task-notes-server edge case or similar)

### Verification Command

```bash
# List all agents and their exit codes
launchctl list | grep "petesbrain\|roksys.petesbrain"

# Count healthy agents
launchctl list | grep "petesbrain" | grep "0\s" | wc -l  # Should be 70

# Find unhealthy agents
launchctl list | grep "petesbrain" | grep -v "0\s"
```

---

## Known Limitations

### 1. Hardcoded Paths (352 locations)
- **Impact**: Not portable, hard to refactor
- **Workaround**: Use exact directory structure
- **Future**: Introduce `shared/paths.py` in Phase 2 of incremental migration

### 2. Plaintext Credentials in Plist Files (16 agents)
- **Impact**: Security risk, visible in XML files
- **Workaround**: Ensure plist files are only readable by owner
- **Future**: Move to Keychain in Phase 2 of incremental migration

### 3. Individual Virtual Environments (1.8GB)
- **Impact**: Disk space, slow to rebuild
- **Workaround**: Consolidate as needed
- **Future**: Introduce consolidated venvs in Phase 2 of incremental migration

### 4. No Structured Logging
- **Impact**: Hard to monitor, parse, or analyze logs
- **Workaround**: Manual log inspection
- **Future**: Introduce structured logging in Phase 3 of incremental migration

### 5. No Automated Rebuild Tools
- **Impact**: Manual setup, error-prone
- **Workaround**: Use existing setup scripts
- **Future**: Introduce `master-rebuild.py` in Phase 3 of incremental migration

---

## Roadmap: Incremental Migration (Phase 2+)

### Week 2: Keychain Secrets (5 Critical Agents)
- Create `shared/secrets.py` with Keychain access
- Migrate 5 critical agents to use Keychain
- Keep plist credentials as fallback
- Test extensively

### Week 3: Path Standardization (5 Critical Agents)
- Create `shared/paths.py` with centralized path discovery
- Update 5 critical agents to use `PROJECT_ROOT`
- Set `PETESBRAIN_ROOT` in plist EnvironmentVariables
- Verify file access

### Week 4: Verify and Expand
- Verify 5 migrated agents work for 7 days
- If stable, migrate next 5 agents
- If unstable, fix before expanding

### Weeks 5-8: Continue Migration
- 5 agents per week
- Create incremental architecture docs
- Can rollback individual agents if needed

### Weeks 9+: Infrastructure Tools
- Introduce `system-verifier.py` (health checks)
- Introduce `validate-agent.py` (compliance)
- Introduce `create-new-agent.py` (scaffolding)
- Only add when migration proves stable

---

## How to Work With This System

### Adding a New Agent

1. Create `.plist` file in `~/Library/LaunchAgents/`
2. Write Python script with proper error handling
3. Use absolute paths (e.g., `/Users/administrator/Documents/PetesBrain.nosync/...`)
4. If credentials needed, add to plist EnvironmentVariables
5. Load agent: `launchctl load ~/Library/LaunchAgents/com.petesbrain.{agent-name}.plist`
6. Test: `launchctl list | grep {agent-name}`
7. Monitor: `tail -f ~/.petesbrain-{agent-name}.log`

**Note**: During Phase 2 migration, follow migration pattern (Keychain + paths.py) instead.

### Adding a New Client

1. Create folder: `clients/{client-slug}/`
2. Create CONTEXT.md with platform IDs and strategy
3. Create empty `tasks.json`: `{"tasks": []}`
4. Create empty `tasks-completed.md`
5. Create subdirectories: emails/, meeting-notes/, reports/, documents/
6. Add client to relevant agents (email-sync, reporting, etc.)

### Running a One-Time Report

Use MCP servers via Python:

```python
from mcp import google_ads_run_gaql

result = google_ads_run_gaql(
    customer_id='8573235780',
    query='SELECT metrics.cost_micros FROM customer WHERE ...'
)
```

Or use Claude Code skills:
```
/weekly smythson  # Generate weekly report for Smythson client
```

---

## Important Files

### Agent Configuration
```
~/Library/LaunchAgents/com.petesbrain.*.plist  # All agent plist files
~/.petesbrain-*.log                             # Agent logs
~/.petesbrain-*-error.log                       # Agent error logs
```

### Core Configuration
```
/Users/administrator/Documents/PetesBrain.nosync/.mcp.json  # MCP servers + credentials
/Users/administrator/Documents/PetesBrain.nosync/.claude/CLAUDE.md  # Claude Code guidance
/Users/administrator/Documents/PetesBrain.nosync/README.md  # Project overview
```

### Client Data
```
/Users/administrator/Documents/PetesBrain.nosync/clients/{client}/  # Per-client folders
```

### Documentation
```
/Users/administrator/Documents/PetesBrain.nosync/docs/  # System documentation
/Users/administrator/Documents/PetesBrain.nosync/.claude/skills/  # Claude Code skills
```

---

## Questions or Issues?

Refer to:
- `docs/MIGRATION-POSTMORTEM.md` - What happened Dec 10 and why
- `docs/TASK-SYSTEM-DECISION-GUIDE.md` - When to use internal tasks vs Google Tasks
- `.claude/CLAUDE.md` - Claude Code guidance for this project
- Agent logs (`~/.petesbrain-*.log`) - For debugging specific agents

This is the working architecture as of December 11, 2025. It has known limitations but is stable and functional for current operations.
