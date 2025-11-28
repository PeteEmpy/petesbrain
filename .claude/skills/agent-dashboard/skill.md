---
name: agent-dashboard
description: Checks status of all PetesBrain LaunchAgents, views health status, restarts unhealthy agents, and views agent logs. Use when user asks "check agent status", "agent dashboard", "are agents working", "restart agent", "view agent logs", or wants to monitor automated workflows.
allowed-tools: Bash, Read
---

# Agent Dashboard Skill

## Instructions

When this skill is triggered, use the agent dashboard commands below to check status, diagnose issues, and manage agents.

---

## Manual Commands

### Quick Status Check

```bash
# Show full agent dashboard
python3 agents/agent-dashboard/agent-dashboard.py
```

### Check Specific Agent

```bash
# Detailed status for one agent
python3 agents/agent-dashboard/agent-dashboard.py --status AGENT-NAME

# Examples:
python3 agents/agent-dashboard/agent-dashboard.py --status ai-inbox-processor
python3 agents/agent-dashboard/agent-dashboard.py --status email-sync
python3 agents/agent-dashboard/agent-dashboard.py --status wispr-flow-importer
```

### View Agent Logs

```bash
# View recent logs (last 50 lines)
python3 agents/agent-dashboard/agent-dashboard.py --logs AGENT-NAME

# View more lines
python3 agents/agent-dashboard/agent-dashboard.py --logs AGENT-NAME 100
```

### Restart Unhealthy Agent

```bash
# Restart a specific agent
python3 agents/agent-dashboard/agent-dashboard.py --restart AGENT-NAME
```

### Health Check

```bash
# Quick health check
python3 agents/health-check/health-check.py

# Verbose output (shows all agents)
python3 agents/health-check/health-check.py --verbose

# Auto-restart unhealthy agents
python3 agents/health-check/health-check.py --restart-unhealthy
```

---

## What You'll See

### Dashboard Output

The dashboard shows:
- **Total agents**: How many agents are discovered
- **Healthy agents**: Count of working agents
- **Critical issues**: Critical agents needing attention
- **Non-critical issues**: Less urgent problems
- **Agent list**: All agents grouped by status

### Example Output

```
================================================================================
PetesBrain Agent Dashboard
Time: 2025-11-08 19:47:24
================================================================================

🔍 Checking agent health...

✅ HEALTHY AGENTS
================================================================================
31 agent(s) running correctly

🔴 Critical (12):
   ✅ ai-inbox-processor
   ✅ email-sync
   ✅ wispr-flow-importer
   ...

⚪ NON-CRITICAL AGENTS WITH ISSUES
================================================================================
❌ label-snapshots: Product label snapshots (daily)
   Issues: stale log
```

---

## Common Agent Names

**Critical Agents:**
- `ai-inbox-processor` - AI inbox processor (every 10 min)
- `email-sync` - Email sync workflow (every 6 hours)
- `wispr-flow-importer` - Wispr Flow notes (every 30 min)
- `inbox-processor` - Inbox processor (daily 8 AM)
- `granola-google-docs-importer` - Meeting importer (every 5 min)
- `tasks-monitor` - Google Tasks sync (every 6 hours)
- `knowledge-base` - KB processor (every 6 hours)
- `industry-news` - Industry news monitor (every 6 hours)
- `ai-news` - AI news monitor (every 6 hours)
- `daily-anomaly-alerts` - Anomaly detector (daily 9 AM)

**Non-Critical Agents:**
- `label-snapshots` - Product label snapshots (daily)
- `product-data-fetcher` - Product data fetcher (daily 6 AM)
- `kb-indexer` - Knowledge base indexer
- `kb-weekly-summary` - KB weekly summary (Mon 8:30 AM)
- `granola-weekly-summary` - Meeting weekly review (Mon 9 AM)
- `product-impact-analyzer` - Product impact analyzer
- `smythson-dashboard` - Smythson Q4 dashboard (daily)
- `product-monitor` - Product Monitor agent

---

## Troubleshooting

### Agent Not Running

```bash
# Check if LaunchAgent is loaded
launchctl list | grep petesbrain

# Check specific agent
launchctl list com.petesbrain.AGENT-NAME

# View logs
tail -50 ~/.petesbrain-AGENT-NAME.log
tail -50 ~/.petesbrain-AGENT-NAME-error.log
```

### Restart Agent

```bash
# Via dashboard
python3 agents/agent-dashboard/agent-dashboard.py --restart AGENT-NAME

# Via launchctl
launchctl stop com.petesbrain.AGENT-NAME
launchctl start com.petesbrain.AGENT-NAME
```

### View Health Check Logs

```bash
# Health check results
tail -50 ~/.petesbrain-health-check.log

# Health check errors
tail -50 ~/.petesbrain-health-check-error.log
```

---

## Integration with Daily Briefing

Agent status is automatically included in the Daily Briefing email every morning at 7 AM. The briefing shows:
- Total healthy/unhealthy counts
- Critical agents needing attention
- Non-critical issues

Check `clients/_system/daily-briefings/YYYY-MM-DD.md` for the full briefing.

---

## Auto-Discovery

The system automatically discovers all `com.petesbrain.*` LaunchAgents, so:
- ✅ No manual configuration needed
- ✅ New agents are automatically monitored
- ✅ Schedule type is detected automatically
- ✅ Criticality is determined automatically

---

## Related Commands

**Check all agents:**
```bash
launchctl list | grep petesbrain
```

**View agent logs directly:**
```bash
tail -f ~/.petesbrain-AGENT-NAME.log
```

**Run health check:**
```bash
python3 agents/health-check/health-check.py --verbose
```

---

## Notes

- The dashboard uses auto-discovery - all agents are found automatically
- Health check runs automatically every 30 minutes
- Daily Briefing includes agent status every morning
- Critical agents are auto-detected based on schedule and name patterns

