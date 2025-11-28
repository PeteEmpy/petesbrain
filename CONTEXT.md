# PetesBrain - Project Context

**Last Updated:** 2025-11-24

PetesBrain is an AI-powered business management system for a Google Ads agency. It automates client work, task management, reporting, and communications.

---

## Directory Structure

```
PetesBrain/
├── agents/                    # Automated background agents (LaunchAgents)
│   ├── client-work/          # Client-specific automation
│   ├── inbox/                # Email/message processing
│   ├── reporting/            # Automated reports
│   └── system/               # System maintenance agents
├── clients/                   # Per-client data and context
│   └── {client-slug}/
│       ├── CONTEXT.md        # Client background, IDs, strategy
│       ├── tasks.json        # Client's active tasks (internal system)
│       ├── tasks-completed.md # Completed task log
│       └── emails/           # Client email archive
├── data/
│   ├── state/                # System state files (protected)
│   └── knowledge-base/       # Reference documents
├── docs/                      # 164+ documentation files
├── infrastructure/
│   └── mcp-servers/          # MCP server implementations
├── shared/                    # Shared Python modules
│   ├── client_tasks_service.py  # Internal task system
│   ├── google_tasks_client.py   # Google Tasks API client
│   └── ...
└── .claude/
    └── skills/               # Claude Code skills (check here first)
```

---

## Two Task Systems (DO NOT CONFUSE)

**These are completely independent and do NOT sync.**

| System | Location | Purpose |
|--------|----------|---------|
| **Internal Client Tasks** | `clients/{client}/tasks.json` | ALL client work |
| **Google Tasks** | Google API | Personal tasks only |

**Decision:**
- Client work? → Internal system
- Recurring? → Internal system (required)
- Personal? → Google Tasks

**Full guide:** `docs/TASK-SYSTEM-DECISION-GUIDE.md`

---

## Key Services

| Service | Location | Purpose |
|---------|----------|---------|
| `ClientTasksService` | `shared/client_tasks_service.py` | Internal task CRUD |
| `GoogleTasksClient` | `shared/google_tasks_client.py` | Google Tasks API |
| `EmailSyncService` | `shared/email-sync/` | Gmail integration |

---

## MCP Servers

| Server | Purpose | Tools |
|--------|---------|-------|
| `google-ads` | Google Ads API | `run_gaql`, `get_client_platform_ids` |
| `google-analytics` | GA4 API | `run_report`, `get_page_views` |
| `google-tasks` | Tasks API | `list_tasks`, `create_task` |
| `google-trends` | Trends data | `get_interest_over_time` |
| `microsoft-ads` | Bing Ads API | `get_campaigns`, `run_gaql` |

---

## Client Platform IDs

Each client's `CONTEXT.md` contains their platform IDs:
- Google Ads Customer ID
- Merchant Centre ID
- GA4 Property ID
- Microsoft Ads Account ID

Use `mcp__google-ads__get_client_platform_ids('client-slug')` to retrieve.

---

## Skills (Check First)

Before searching for scripts, check `.claude/skills/`:

```bash
ls .claude/skills/
```

Common skills:
- `google-ads-weekly-report` - Weekly performance analysis
- `csv-analyzer` - Analyse CSV exports
- `email-draft-generator` - Draft client emails
- `task-manager` - Open task UI

---

## Conventions

1. **British English** - analyse, optimise, colour
2. **Client prefixes** - `[Client]` in task titles
3. **Protected files** - Never delete `tasks.json`, `tasks-completed.md`
4. **Voice input** - User dictates; check client aliases for mishearings

---

## Key Documentation

| Topic | File |
|-------|------|
| Task system decision guide | `docs/TASK-SYSTEM-DECISION-GUIDE.md` |
| Adding new clients | `docs/ADDING-A-NEW-CLIENT.md` |
| Agent monitoring | `docs/AGENT-MONITORING-GUIDE.md` |
| Internal task system | `docs/INTERNAL-TASK-SYSTEM.md` |

---

## Common Operations

**Get client IDs:**
```python
mcp__google-ads__get_client_platform_ids('smythson')
```

**Run Google Ads query:**
```python
mcp__google-ads__run_gaql(customer_id='123', query='SELECT ...')
```

**Create client task:**
```python
from shared.client_tasks_service import ClientTasksService
service = ClientTasksService()
service.create_task(title='[Client] Task', client='client-slug', priority='P1')
```

**List Google Tasks:**
```python
mcp__google-tasks__list_tasks(tasklist_id='...')
```
