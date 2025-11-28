# PetesBrain Agents

**Last Updated:** $(date +%Y-%m-%d)
**Total Agents:** $(ls -1 agents/ | grep -v README | grep -v launchagents | grep -v "^_" | wc -l | tr -d ' ')

---

## Overview

This directory contains all automated background agents (LaunchAgents) that power PetesBrain's self-improving agency infrastructure. Each agent runs on a schedule to monitor, analyze, sync, and report without manual intervention.

**Structure:** Each agent is self-contained in its own folder:
```
agents/
├── agent-name/
│   ├── agent.md              # Metadata (schedule, status, dependencies)
│   ├── agent-name.py         # Implementation
│   ├── config.plist          # LaunchAgent configuration
│   └── README.md             # Documentation (optional)
```

---

## Quick Reference

### List All Agents
```bash
ls -1 agents/ | grep -v README | grep -v launchagents
```

### Search Agent Purposes
```bash
grep -h "## Purpose" agents/*/agent.md
```

### List by Status
```bash
grep -h "status:" agents/*/agent.md | sort | uniq -c
```

### Check Running Agents
```bash
launchctl list | grep petesbrain
```

### View Agent Logs
```bash
cat ~/.petesbrain-AGENT-NAME.log
```

---

## Agent Categories

### Content Sync
Sync meetings, emails, knowledge base, and news content

- **ai-news-monitor** - Monitor AI industry RSS feeds
- **industry-news-monitor** - Monitor Google Ads industry RSS feeds
- **knowledge-base-processor** - Process and organize knowledge base content
- **granola-google-docs-importer** - Import meeting transcripts from Granola
- **weekly-blog-generator** - Generate weekly blog articles
- **facebook-news-monitor** - Monitor Facebook Ads news
- **facebook-specs-monitor** - Monitor Facebook platform specs
- **google-specs-monitor** - Monitor Google Ads platform specs
- **google-ads-feature-email-processor** - Process Google feature announcement emails

### Reporting
Generate and send automated reports and summaries

- **daily-intel-report** - Daily intelligence briefing with pre-verified tasks
- **kb-weekly-summary** - Knowledge base weekly summary email
- **weekly-meeting-review** - Weekly meeting summary email
- **campaign-audit-agent** - Weekly campaign audits (Mike Rhodes approach)
- **google-ads-auditor** - Google Ads audit templates

### System
System maintenance, inbox processing, task tracking

- **ai-inbox-processor** - AI-enhance Wispr Flow notes before routing
- **inbox-processor** - Process and route inbox captures
- **tasks-monitor** - Sync Google Tasks to CONTEXT.md
- **sync-todos-to-google-tasks** - Sync local todos to Google Tasks
- **health-check** - Monitor system health and agent status
- **agent-dashboard** - View status of all agents

### Performance Monitoring
Monitor client performance, detect anomalies

- **daily-anomaly-detector** - Detect critical performance drops
- **fetch-weekly-performance** - Fetch performance data for all clients
- **baseline-calculator** - Calculate performance baselines
- **nda-enrolments-tracker** - Track National Design Academy enrolments
- **trend-monitor** - Track Google Trends for all clients

### Budget Tracking
Monitor budgets and spending

- **daily-budget-monitor** - Monitor daily budget pacing
- **devonshire-budget-tracker** - Specialized Devonshire budget tracking

### Product Feeds
Monitor product feeds and merchant center

- **product-monitor** - Monitor product feed health
- **merchant-center-monitor** - Check Merchant Center status
- **label-tracker** - Track product label changes
- **snapshot-product-feed** - Daily product feed snapshots
- **product-data-fetcher** - Fetch product data from Google Ads

---

## Managing Agents

### Start an Agent
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.AGENT-NAME.plist
```

### Stop an Agent
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.AGENT-NAME.plist
```

### Run Agent Manually (Once)
```bash
launchctl start com.petesbrain.AGENT-NAME
# or
python3 agents/AGENT-NAME/AGENT-NAME.py
```

### Reload All Agents
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.*.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.*.plist
```

---

## Adding a New Agent

1. **Create agent folder:**
   ```bash
   mkdir agents/new-agent-name
   ```

2. **Create the script:**
   ```bash
   touch agents/new-agent-name/new-agent-name.py
   chmod +x agents/new-agent-name/new-agent-name.py
   ```

3. **Create agent.md metadata:**
   ```markdown
   ---
   name: new-agent-name
   category: content-sync|reporting|system|monitoring|tracking
   schedule: "Every 6 hours"
   status: active
   dependencies:
     - package1
     - package2
   ---

   # Agent Name

   ## Purpose
   Brief description

   ## Configuration
   - LaunchAgent: config.plist
   - Log: ~/.petesbrain-agent-name.log
   ```

4. **Create LaunchAgent plist:**
   ```bash
   # Copy template from another agent
   cp agents/ai-news-monitor/config.plist agents/new-agent-name/config.plist
   # Edit paths and schedule
   ```

5. **Install and test:**
   ```bash
   cp agents/new-agent-name/config.plist ~/Library/LaunchAgents/com.petesbrain.new-agent-name.plist
   launchctl load ~/Library/LaunchAgents/com.petesbrain.new-agent-name.plist
   launchctl start com.petesbrain.new-agent-name
   tail -f ~/.petesbrain-new-agent-name.log
   ```

6. **Update this README** with new agent in appropriate category

---

## Troubleshooting

### Agent Not Running
```bash
# Check if loaded
launchctl list | grep AGENT-NAME

# Check logs
cat ~/.petesbrain-AGENT-NAME.log
cat ~/.petesbrain-AGENT-NAME-error.log

# Reload
launchctl unload ~/Library/LaunchAgents/com.petesbrain.AGENT-NAME.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.AGENT-NAME.plist
```

### Script Errors
```bash
# Run directly to see errors
cd /Users/administrator/Documents/PetesBrain
python3 agents/AGENT-NAME/AGENT-NAME.py
```

### Permission Issues
```bash
# Make executable
chmod +x agents/AGENT-NAME/AGENT-NAME.py

# Check plist
plutil -lint ~/Library/LaunchAgents/com.petesbrain.AGENT-NAME.plist
```

---

## Migration Notes

**Restructured:** 2025-11-13

Previous structure had agents organized in category folders (content-sync/, reporting/, etc.).
New structure has each agent in its own self-contained folder for better organization and portability.

**Benefits:**
- Each agent is complete and portable
- Easy to add/remove agents
- Clear ownership of all files
- Better scalability (35+ agents, growing)

---

## Related Documentation

- [CLAUDE.md](../CLAUDE.md) - Main project documentation
- [Automation Overview](../docs/AUTOMATION.md) - All automated workflows
- [Troubleshooting](../docs/TROUBLESHOOTING.md) - Common issues and fixes
- [Migration Plan](../RESTRUCTURE-MIGRATION-PLAN.md) - Details of 2025-11-13 restructuring

---

