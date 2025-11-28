# Claude Code Sub-Agents

**Location:** `.claude/agents/`
**Last Updated:** 2025-11-23
**Status:** 4 agents operational

---

## Overview

Sub-agents are specialized Claude Code assistants that can be invoked via the **Task tool** to perform focused, autonomous work. Unlike skills (which auto-trigger during conversations), sub-agents are explicitly launched for specific tasks.

**Key Characteristics:**
- Run in isolated context (don't pollute main conversation)
- Can work in parallel with other tasks
- Specialized for specific workflows
- Return structured reports

---

## Available Agents

### 1. Client Researcher
**File:** `client-researcher.md`
**Model:** Haiku (fast, cost-effective)
**Purpose:** Gather comprehensive client context before starting work

**When to Use:**
- Before working on any client task
- When asked "what's the context for [client]"
- Preparing for client meetings or reports

**What It Does:**
- Reads client CONTEXT.md
- Checks recent emails (last 14 days)
- Reviews meeting notes (last 30 days)
- Lists active tasks from tasks.json
- Filters experiment log for client
- Summarises completed work patterns

**Example Prompts:**
```
"Research Smythson before I work on their Q4 dashboard"
"What's the context for Tree2mydoor?"
"Gather background on Devonshire Hotels"
```

**Output:** Structured markdown with business overview, targets, recent activity, active tasks, and key context points.

---

### 2. Google Ads Analyst
**File:** `google-ads-analyst.md`
**Model:** Sonnet (for API calls and complex analysis)
**Purpose:** Query Google Ads accounts and provide performance analysis

**When to Use:**
- Checking account performance
- Investigating ROAS/conversion changes
- Campaign-level analysis
- Budget utilisation reviews

**What It Does:**
- Runs GAQL queries via Google Ads MCP
- Calculates ROAS, CPA, CTR, conversion rates
- Compares performance periods
- Identifies issues and opportunities
- Provides data-driven recommendations

**Example Prompts:**
```
"Analyse Superspace's Google Ads performance this week"
"Why did Smythson's ROAS drop?"
"Check budget utilisation for Tree2mydoor"
"Which products are wasting spend for Clear Prospects?"
```

**Output:** Structured analysis with summary, key metrics table, campaign breakdown, issues identified, and recommendations.

**Note:** Formats ROAS as percentage (420%, not £4.20) per ROK standards.

---

### 3. Product Investigator
**File:** `product-investigator.md`
**Model:** Haiku (read-only research)
**Purpose:** Investigate why a specific product's performance changed

**When to Use:**
- Product revenue dropped unexpectedly
- Click spikes or drops on specific products
- Tracking product changes over time
- Correlating feed changes with performance

**What It Does:**
- Searches Product Impact Analyzer data sources:
  - Performance snapshots (clicks, revenue, impressions)
  - Price history and price change logs
  - Disapproval status snapshots
  - Label changes (Hero/Sidekick/Villain/Zombie)
- Builds chronological timeline
- Identifies root cause
- Provides recommendations

**Example Prompts:**
```
"Why did product 287 drop for Tree2mydoor?"
"What happened to the Olive Tree product?"
"Investigate product 01090 performance spike"
"Track product FCB7007 history for Smythson"
```

**Output:** Investigation report with timeline, performance summary, current status, root cause analysis, and recommendations.

**Data Sources:**
```
tools/product-impact-analyzer/monitoring/
├── snapshot_{client}_YYYY-MM-DD.json      # Performance
├── prices/prices_{client}_YYYY-MM-DD.json  # Pricing
├── prices/price_changes_YYYY-MM.json       # Price changes
├── disapprovals/disapprovals_{client}_*.json
└── labels/labels_{client}_YYYY-MM-DD.json  # Hero/Sidekick/etc
```

---

### 4. Task Triager
**File:** `task-triager.md`
**Model:** Haiku (categorisation task)
**Purpose:** Process inbox items and route to appropriate clients

**When to Use:**
- Processing manual task notes from task_manager UI
- Triaging inbox items
- Assigning unassigned meeting notes to clients

**What It Does:**
- Reads manual-task-notes.json
- Checks !inbox/ folder
- Reviews unassigned meeting notes
- Detects client using:
  - Email domain matching
  - Keyword detection
  - Contact name matching
- Categorises items (urgent-action, client-request, optimization, etc.)
- Assigns priority (P0-P3)
- Recommends routing and actions

**Example Prompts:**
```
"Process my task notes"
"Triage inbox items"
"Which client does this meeting belong to?"
"Categorise these incoming items"
```

**Output:** Triage results with routing recommendations, confidence levels, and suggested next steps.

**Primary Sources:**
```
data/state/manual-task-notes.json    # From task_manager UI
!inbox/                               # Unprocessed notes
clients/_unassigned/meeting-notes/    # Unassigned meetings
```

---

## How to Invoke Sub-Agents

Sub-agents are invoked via the **Task tool** in Claude Code. The system automatically maps your request to the appropriate agent based on intent.

### Direct Invocation Pattern
```
User: "Research [client] before I start work"
→ Claude uses Task tool with client-researcher prompt

User: "Why did product X drop?"
→ Claude uses Task tool with product-investigator prompt

User: "Analyse [client]'s Google Ads"
→ Claude uses Task tool with google-ads-analyst prompt

User: "Process my task notes"
→ Claude uses Task tool with task-triager prompt
```

### Agent Selection Matrix

| User Intent | Agent | Sub-agent Type |
|-------------|-------|----------------|
| Client context/background | client-researcher | Explore |
| Google Ads performance | google-ads-analyst | general-purpose |
| Product investigation | product-investigator | Explore |
| Inbox/task triage | task-triager | Explore |

---

## Agent Design Principles

### 1. Read-Only by Default
Most agents (3 of 4) are read-only - they gather and report but don't modify files. This prevents unintended changes during autonomous work.

### 2. Structured Output
All agents return structured markdown reports with consistent sections, making outputs predictable and easy to parse.

### 3. Model Selection
- **Haiku** for read-only research (faster, cheaper)
- **Sonnet** for API calls and complex reasoning

### 4. Isolated Context
Agents run in separate context windows, keeping the main conversation clean and focused.

### 5. Source Documentation
Each agent documents which files/APIs it accesses, making behaviour transparent.

---

## Creating New Agents

To create a new sub-agent:

1. **Create agent file** in `.claude/agents/[name].md`

2. **Use this frontmatter:**
```yaml
---
name: agent-name
description: One-line description for intent matching
tools: Read, Glob, Grep (or MCP tools if needed)
model: haiku (or sonnet for complex work)
---
```

3. **Document in the file:**
- Purpose and when to use
- Data sources accessed
- Output format with example
- Rules and constraints

4. **Update this README** with the new agent

5. **Test** using the Task tool

---

## Troubleshooting

### Agent not being invoked
- Check if user intent matches agent description
- Try more explicit prompt ("Use the product-investigator to...")

### Wrong data returned
- Verify client slug mapping in agent file
- Check data source paths exist
- Ensure date ranges cover relevant period

### Slow performance
- Consider if Haiku model is sufficient (vs Sonnet)
- Reduce data sources checked if not all needed

---

## Related Documentation

- `.claude/skills/README.md` - Skills (auto-triggered capabilities)
- `docs/CLAUDE.md` - Main architecture documentation
- `tools/product-impact-analyzer/TOOL_CLAUDE.md` - Product Impact Analyzer details
- `docs/MCP-SERVERS.md` - MCP tool reference

---

**Maintained by:** PetesBrain System
**Review Frequency:** As agents are added/modified
