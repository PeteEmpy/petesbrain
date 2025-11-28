# Campaign Audit System - Mike Rhodes Integration Complete

**Date:** November 9, 2025  
**Status:** ✅ Complete - Ready for Use

---

## What Was Built

### 1. Updated Skill (Auto-Execution)
**Location:** `.claude/skills/google-ads-campaign-audit/skill.md`

- **Auto-executes** MCP queries when triggered
- **Hierarchical 3-phase approach:**
  - Phase 1: Account Intelligence (2 queries)
  - Phase 2: Core Structural Audit (3 queries)
  - Phase 3: Optional Deep-Dive (conditional queries)
- **Focus:** Structural inefficiencies + budget misallocations (not performance optimization)
- **Uses:** `mcp__google-ads__run_gaql` tool directly

### 2. Data Transformation Script
**Location:** `.claude/skills/google-ads-campaign-audit/transform_data.py`

- Converts raw Google Ads JSON to markdown tables
- Eliminates calculation errors (ROAS, currency, percentages)
- Auto-detects field types (`*_micros` → currency, `ctr` → percentage)
- Handles `conversions_value` correctly (already in currency, NOT micros)

### 3. GAQL Query Templates
**Location:** `.claude/skills/google-ads-campaign-audit/queries/`

**Core Queries (Always Run):**
- `account-scale.gaql` - Campaign counts by status
- `spend-concentration.gaql` - Top campaigns by spend
- `campaign-settings.gaql` - Configuration audit
- `budget-constraints.gaql` - Budget utilization and Lost IS
- `campaign-performance.gaql` - Full performance metrics

**Optional Queries (Phase 3):**
- `device-performance.gaql` - Device segmentation
- `geographic-performance.gaql` - Geographic analysis
- `network-performance.gaql` - Search vs Search Partners

### 4. Python Agent Script
**Location:** `agents/reporting/campaign-audit-agent.py`

- Executes Phase 1 & Phase 2 queries automatically
- Saves results to JSON files
- Runs data transformation
- Creates audit data directory: `clients/[client]/audits/YYYYMMDD-campaign-audit-data/`

**Usage:**
```bash
# Single client
python3 agents/reporting/campaign-audit-agent.py --client smythson

# All active clients
python3 agents/reporting/campaign-audit-agent.py --all
```

### 5. LaunchAgent (Scheduled Execution)
**Location:** `agents/launchagents/com.petesbrain.campaign-audit-agent.plist`

- Runs every Monday at 10:00 AM
- Executes audits for all active clients
- Logs to: `~/.petesbrain-campaign-audit-agent.log`

**To activate:**
```bash
cp agents/launchagents/com.petesbrain.campaign-audit-agent.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.petesbrain.campaign-audit-agent.plist
```

---

## How It Works

### Skill Usage (Interactive)

When you say "Run an audit for [client]" or "Audit the [client] account":

1. **Skill auto-triggers** and loads client config
2. **Phase 1:** Executes account-scale and spend-concentration queries
3. **Phase 2:** Executes campaign-settings, budget-constraints, campaign-performance queries
4. **Transforms data:** Runs `transform_data.py` to create markdown tables
5. **Analyzes:** Reviews transformed data for structural issues
6. **Generates report:** Writes complete audit to `clients/[client]/audits/YYYYMMDD-campaign-audit.md`

### Agent Usage (Automated)

Every Monday at 10 AM:

1. **Agent runs** for all active clients
2. **Executes queries** and saves JSON files
3. **Transforms data** to markdown tables
4. **Creates audit data directory** with all files
5. **Ready for analysis** - Use Claude Code skill to generate full report

---

## Key Differences from Previous System

### Before (Template-Based)
- ❌ Generated templates only
- ❌ Required manual MCP execution
- ❌ No data transformation
- ❌ Focused on performance optimization

### After (Mike Rhodes Approach)
- ✅ Auto-executes MCP queries
- ✅ Hierarchical query execution
- ✅ Data transformation eliminates errors
- ✅ Focuses on structure + budget (foundation first)

---

## Workflow

### For Interactive Audits (Skill)

1. Say: "Run an audit for Just Bin Bags"
2. Skill executes Phase 1 & Phase 2 queries
3. Data is transformed automatically
4. Skill analyzes and generates complete report
5. Report saved to `clients/just-bin-bags/audits/YYYYMMDD-campaign-audit.md`

### For Automated Audits (Agent)

1. Agent runs Monday 10 AM
2. Creates audit data directories for all clients
3. Data is ready for analysis
4. Use skill to generate reports: "Analyze the audit data for [client]"

---

## Files Created

```
.claude/skills/google-ads-campaign-audit/
├── skill.md                          ✅ Updated (auto-execution)
├── transform_data.py                 ✅ New (data transformation)
└── queries/
    ├── account-scale.gaql            ✅ New
    ├── spend-concentration.gaql      ✅ New
    ├── campaign-settings.gaql        ✅ New
    ├── budget-constraints.gaql       ✅ New
    ├── campaign-performance.gaql     ✅ New
    ├── device-performance.gaql       ✅ New (optional)
    ├── geographic-performance.gaql   ✅ New (optional)
    └── network-performance.gaql       ✅ New (optional)

agents/reporting/
└── campaign-audit-agent.py           ✅ New (automated execution)

agents/launchagents/
└── com.petesbrain.campaign-audit-agent.plist  ✅ New (scheduled)
```

---

## Next Steps

1. **Test the skill:** Say "Run an audit for Just Bin Bags" to test auto-execution
2. **Activate the agent:** Load the LaunchAgent for weekly automated audits
3. **Review reports:** Check `clients/[client]/audits/` for generated reports

---

## Notes

- **Currency detection:** Automatically detects £, $, or A$ from client CONTEXT.md
- **Manager accounts:** Supports MCC-managed accounts via manager_id
- **Large accounts:** Automatically limits queries for accounts with 100+ campaigns
- **Error handling:** Gracefully handles missing MCP configuration

---

**Status:** ✅ Complete and Ready for Production Use

