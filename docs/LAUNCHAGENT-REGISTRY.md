# LaunchAgent Registry

**Purpose**: Central registry of all PetesBrain LaunchAgents with ownership, resources, and dependencies.

**Last Updated**: 2025-12-23
**Total Active Agents**: 72

---

## Quick Reference

### Task System Agents (CRITICAL)

| Agent | Ports | Purpose | Depends On |
|-------|-------|---------|------------|
| `com.petesbrain.task-manager` | 8767, 5002 | Unified HTML + API server | None |
| `com.petesbrain.task-manager-hourly-regenerate` | - | Regenerates task HTML views hourly | task-manager |
| `com.petesbrain.task-manager-monitor` | - | Monitors server health, restarts if crashed | task-manager |
| `com.petesbrain.tasks-backup` | - | Daily backup of all tasks.json files | None |
| `com.petesbrain.tasks-monitor` | - | Monitors task system for anomalies | None |

**⚠️ CRITICAL**: These agents manage the core task system. If `com.petesbrain.task-manager` fails, the Task Manager UI will be unavailable.

---

## Core System Agents

### Communication & Inbox

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.email-auto-label` | Every 2 min | Auto-labels Gmail with client names | Gmail API |
| `com.petesbrain.email-sync` | Every 5 min | Syncs emails to client folders | Gmail API, Disk I/O |
| `com.petesbrain.ai-inbox-processor` | Every 15 min | Processes !inbox/ messages | Anthropic API |
| `com.petesbrain.inbox-processor` | Every 30 min | Legacy inbox processor | Anthropic API |
| `com.petesbrain.ai-google-chat-processor` | Every 15 min | Processes Google Chat messages | Google Chat API |
| `com.petesbrain.booking-processor` | Every 30 min | Processes meeting bookings | Gmail API |

### Daily Operations

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.daily-intel-report` | 7:00 AM daily | Morning briefing email | Multiple APIs |
| `com.petesbrain.daily-anomaly-alerts` | 8:00 AM daily | Performance anomaly detection | Google Ads API |
| `com.petesbrain.health-check` | Every 15 min | System health monitoring | Process, Disk, Network |
| `com.petesbrain.diagnostics-monitor` | Every 30 min | Agent diagnostics | LaunchAgent status |

### Backup & Safety

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.tasks-backup` | 6:00 AM daily | Backup all tasks.json | Google Drive API |
| `com.petesbrain.daily-backup` | 11:00 PM daily | Full system backup | Google Drive API |
| `com.petesbrain.critical-tasks-backup` | Every 2 hours | P0 task snapshots | Google Drive API |
| `com.petesbrain.safe-backup` | Every 4 hours | Incremental backups | Google Drive API |
| `com.petesbrain.weekly-backup-audit` | Sunday 9:00 AM | Verify backup integrity | Google Drive API |

---

## Google Ads Monitoring

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.budget-monitor` | Every 30 min | Budget pacing alerts | Google Ads API |
| `com.petesbrain.devonshire-budget` | Every 15 min | Devonshire budget tracking | Google Ads API |
| `com.petesbrain.disapproval-monitor` | Every 2 hours | Ad disapproval alerts | Google Ads API |
| `com.petesbrain.google-ads-auditor` | Every 6 hours | Campaign structure audits | Google Ads API |
| `com.petesbrain.google-specs-monitor` | Every 4 hours | Policy/specs updates | Google RSS |
| `com.petesbrain.google-specs-processor` | Every 6 hours | Process spec changes | Knowledge Base |

---

## E-commerce & Product Monitoring

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.merchant-center` | Every 30 min | Merchant Centre monitoring | Merchant Centre API |
| `com.petesbrain.product-impact-analyzer` | Tuesday 9:00 AM | Weekly product impact analysis with email reports | Google Ads API, Merchant Centre API, Google Sheets API |
| `com.petesbrain.product-tracking` | Daily 7:45 AM | Daily product feed tracking and change detection | Merchant Centre API, Google Sheets API |
| `com.petesbrain.product-monitor` | Every 2 hours | Product performance monitoring with alerts (12x daily) | Google Ads API, Merchant Centre API |
| `com.petesbrain.product-data-fetcher` | Daily 7:00 AM | Fetch Google Ads performance data for all clients | Google Ads API |
| `com.petesbrain.product-sheets-sync` | Daily 8:00 AM | Sync product analysis results to Google Sheets | Google Sheets API |
| `com.petesbrain.price-monitor` | Every 6 hours | Price change detection | WooCommerce API |
| `com.petesbrain.label-tracker` | Every 4 hours | Product label changes | Merchant Centre API |
| `com.petesbrain.label-snapshots` | Daily 6:00 AM | Daily label state snapshots | Merchant Centre API |
| `com.petesbrain.baseline-calculator` | Sunday 8:00 AM | Calculate performance baselines | Google Ads API |
| `com.petesbrain.order-processor` | Every 15 min | Process e-commerce orders | WooCommerce API |
| `com.petesbrain.woocommerce-daily-cache` | 5:00 AM daily | Cache WooCommerce data | WooCommerce API |

---

## Knowledge Base & Content

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.knowledge-base` | Every hour | Update KB from RSS feeds | RSS, Disk I/O |
| `com.petesbrain.kb-indexer` | Every 2 hours | Index KB for search | Disk I/O |
| `com.petesbrain.kb-external-sources` | Every 6 hours | Import external sources | Web scraping |
| `com.petesbrain.kb-weekly-summary` | Sunday 10:00 AM | Weekly KB digest | KB Index |
| `com.petesbrain.sunday-kb-update` | Sunday 9:00 AM | Manual KB update trigger | KB system |

### News Monitoring

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.ai-news` | Every 4 hours | AI industry news | RSS |
| `com.petesbrain.industry-news` | Every 6 hours | PPC industry news | RSS |
| `com.petesbrain.facebook-news-monitor` | Every 4 hours | Facebook Ads news | RSS |
| `com.petesbrain.shopify-news` | Every 6 hours | Shopify platform news | RSS |
| `com.petesbrain.weekly-news-digest` | Monday 8:00 AM | Weekly news summary | Knowledge Base |

### Blog & Content Generation

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.weekly-blog-generator` | Monday 9:00 AM | Generate blog articles | Anthropic API |
| `com.petesbrain.draft-cleanup` | Friday 6:00 PM | Archive old drafts | Disk I/O |

---

## Client-Specific Agents

| Agent | Schedule | Purpose | Client |
|-------|----------|---------|--------|
| `com.petesbrain.smythson-dashboard` | Every 6 hours | Q4 strategy dashboard | Smythson |
| `com.petesbrain.tree2mydoor-search-trends` | Weekly | Search trends analysis | Tree2mydoor |
| `com.petesbrain.tree2mydoor-context-upload` | Monthly | Update context docs | Tree2mydoor |
| `com.petesbrain.nda-enrolments` | Weekly | NDA enrolment tracking | National Design Academy |

---

## Meeting & Documentation

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.granola-google-docs-importer` | Every 5 min | Import Granola transcripts | Google Docs API |
| `com.petesbrain.granola-weekly-summary` | Monday 9:00 AM | Weekly meeting summary | Granola data |
| `com.petesbrain.document-archival` | Monthly 1st | Archive old documents | Disk I/O |

---

## Reporting & Analytics

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.fetch-client-performance` | 6:00 AM daily | Fetch performance data | Google Ads API |
| `com.petesbrain.weekly-impact-report` | Monday 8:00 AM | Weekly product impact report | Product data |
| `com.petesbrain.weekly-label-reports` | Monday 9:00 AM | Weekly label change reports | Label tracker data |
| `com.petesbrain.tier2-tracker-weekly` | Monday 10:00 AM | Tier 2 client tracking | Multiple sources |

---

## Experiments & Testing

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.experiment-review` | Friday 3:00 PM | Review A/B tests | Google Ads API |

---

## Data Sync & Utilities

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.populate-spreadsheets` | Every 6 hours | Update tracking sheets | Google Sheets API |
| `com.petesbrain.product-sheets-sync` | Daily 8:00 AM | Sync product analysis results to Google Sheets | Google Sheets API |
| `com.petesbrain.product-data-fetcher` | Daily 7:00 AM | Fetch Google Ads performance data for all clients | Google Ads API |
| `com.petesbrain.business-context-sync` | Every 12 hours | Sync business context | Disk I/O |
| `com.petesbrain.shared-drives` | Every 6 hours | Sync shared drives | Google Drive API |
| `com.petesbrain.auto-snapshot` | Every 30 min | Auto-snapshot critical data | Disk I/O |

---

## Task Management Utilities

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.task-priority-updater` | Every 2 hours | Update task priorities | tasks.json files |
| `com.petesbrain.cleanup-completed-tasks` | Daily 11:00 PM | Archive completed tasks | tasks.json files |

---

## Platform Spec Monitoring

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.facebook-specs-monitor` | Every 4 hours | Facebook specs updates | RSS |
| `com.petesbrain.facebook-specs-processor` | Every 6 hours | Process Facebook specs | Knowledge Base |
| `com.petesbrain.google-ads-feature-email-processor` | Every 15 min | Process Google Ads emails | Gmail API |

---

## Supporting Services

| Agent | Schedule | Purpose | Resources |
|-------|----------|---------|-----------|
| `com.petesbrain.agent-loader` | On-demand | Load/unload agents | LaunchAgent system |
| `co.roksys.petesbrain.reminder-api` | Continuous | Reminder API server | Port 5050 |
| `co.roksys.petesbrain.backup-task-monitor` | Every 30 min | Monitor backup tasks | Task system |
| `co.roksys.petesbrain.youtube-monitor` | Every 6 hours | Monitor YouTube content | YouTube API |

---

## Port Allocations

| Port | Service | Agent |
|------|---------|-------|
| 8767 | Task Manager HTML | com.petesbrain.task-manager |
| 5002 | Task Manager API | com.petesbrain.task-manager |
| 5050 | Reminder API | co.roksys.petesbrain.reminder-api |
| 5001 | Google Ads Generator | (manual tool) |

**⚠️ CRITICAL**: If any agent crashes with "Address already in use", check for duplicate agents holding these ports:

```bash
lsof -i :8767
lsof -i :5002
lsof -i :5050
```

---

## Deprecated Agents (DO NOT LOAD)

**Location**: `~/Library/LaunchAgents/_DEPRECATED/`

| Agent | Deprecated | Reason |
|-------|------------|--------|
| `com.petesbrain.task-manager-server` | Dec 22, 2025 | Replaced by unified server |
| `com.petesbrain.task-notes-server` | Dec 22, 2025 | Replaced by unified server |
| `com.petesbrain.file-organizer` | Dec 23, 2025 | Infinite loop (97% CPU) |

**See**: `~/Library/LaunchAgents/_DEPRECATED/README.md` for full details.

---

## Agent Management Commands

### List All Agents

```bash
launchctl list | grep petesbrain
```

### Check Agent Status

```bash
launchctl list | grep {agent-name}
```

### View Agent Logs

```bash
tail -f ~/.petesbrain-{agent-name}.log
tail -f ~/.petesbrain-{agent-name}-error.log
```

### Restart Agent

```bash
launchctl unload ~/Library/LaunchAgents/{agent-name}.plist
launchctl load ~/Library/LaunchAgents/{agent-name}.plist
```

Or use kickstart (preferred):

```bash
launchctl kickstart -k gui/502/{agent-label}
```

### Check Agent Health

```bash
python3 shared/scripts/validate-task-system-health.py
```

---

## Adding a New Agent

1. **Create plist** in `~/Library/LaunchAgents/`:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.petesbrain.{agent-name}</string>
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

2. **Update this registry** - Add to appropriate section

3. **Load agent**:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.petesbrain.{agent-name}.plist
   ```

4. **Verify running**:
   ```bash
   launchctl list | grep {agent-name}
   tail -f ~/.petesbrain-{agent-name}.log
   ```

---

## Troubleshooting

### Agent Not Running

1. Check if loaded:
   ```bash
   launchctl list | grep {agent-name}
   ```

2. Check error logs:
   ```bash
   tail -50 ~/.petesbrain-{agent-name}-error.log
   ```

3. Common exit codes:
   - **0**: Success
   - **1**: General error
   - **78**: OAuth token expired (run oauth-refresh skill)
   - **-15**: Killed (SIGTERM)

### Agent Crashes Immediately

1. Check Python path is correct in plist
2. Check virtual environment exists
3. Check file permissions (script must be readable)
4. Check for syntax errors: `python3 /path/to/script.py`

### Port Conflicts

```bash
# Find what's using a port
lsof -i :{port}

# Kill process holding port
kill {pid}

# Or restart agent
launchctl kickstart -k gui/502/com.petesbrain.{agent-name}
```

---

## Related Documentation

- `docs/TASK-MANAGER-INCIDENT-DEC22-23-2025.md` - December 2025 incident report
- `shared/scripts/validate-task-system-health.py` - Health check script
- `~/Library/LaunchAgents/_DEPRECATED/README.md` - Deprecated agents
- `docs/AGENT-MONITORING-GUIDE.md` - Agent monitoring procedures

---

**Last Registry Update**: 2025-12-23 08:55 GMT
**Active Agents**: 72
**Deprecated Agents**: 3
