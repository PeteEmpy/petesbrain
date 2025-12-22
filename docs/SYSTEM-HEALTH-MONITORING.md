# System Health Monitoring (Enhanced)

**Status:** ✅ Active (Enhanced with Comprehensive Monitoring)  
**Last Updated:** 2025-11-09

## Overview

Automated health check system that **automatically discovers** all PetesBrain LaunchAgents and monitors their health with **immediate alerts, failure tracking, escalation, and system resource monitoring**. No manual configuration needed - discovers agents from plist files and intelligently monitors them.

**🚨 NEW: Enhanced with immediate email alerts, failure tracking, escalation, and comprehensive monitoring!**

See [Enhanced Health Check Documentation](ENHANCED-HEALTH-CHECK.md) for complete details on all new features.

## Key Features

✅ **Auto-Discovery** - Automatically finds all `com.petesbrain.*` LaunchAgents  
✅ **Intelligent Monitoring** - Determines schedule type and criticality automatically  
✅ **Activity Verification** - Checks if agents are actually doing their job  
✅ **Auto-Recovery** - Can automatically restart unhealthy agents  
✅ **Daily Briefing Integration** - Agent status appears in morning briefing  
✅ **Dashboard** - Interactive command-line dashboard for quick status checks  
✅ **🚨 Immediate Email Alerts** - Get notified instantly when critical agents fail  
✅ **📊 Failure Tracking** - Track failure history and escalation  
✅ **⏱️ Alert Throttling** - Prevents alert spam  
✅ **🆕 New Failure Detection** - Only alert on newly failed agents  
✅ **💻 System Resource Monitoring** - Disk space, memory, internet checks  
✅ **🔗 Dependency Checks** - API credentials and connectivity validation  
✅ **🔔 Multiple Notification Channels** - Email, Slack, SMS support  

## Components

### 1. LaunchAgent Discovery (`shared/scripts/launchagent_discovery.py`)

Automatically scans `~/Library/LaunchAgents/` for all PetesBrain agents:
- Parses plist files to extract configuration
- Determines schedule type (interval/daily/weekly/daemon)
- Identifies log file paths
- Detects critical vs non-critical agents
- Gets current status (loaded/not loaded)

**Usage:**
```bash
python3 shared/scripts/launchagent_discovery.py
```

### 2. Enhanced Health Check (`agents/system/health-check.py`)

Uses auto-discovery to monitor all agents with comprehensive features:
- Checks if LaunchAgent is loaded
- Verifies log freshness (based on schedule)
- Checks workflow-specific activity
- Can auto-restart unhealthy agents
- **🚨 Sends immediate email alerts for critical failures**
- **📊 Tracks failure history and escalates repeat failures**
- **💻 Monitors system resources (disk, memory, internet)**
- **🔗 Validates API credentials and dependencies**

**Usage:**
```bash
# Basic check
python3 agents/system/health-check.py

# Verbose output
python3 agents/system/health-check.py --verbose

# Auto-restart unhealthy agents
python3 agents/system/health-check.py --restart-unhealthy

# Dry run (show what would be restarted)
python3 agents/system/health-check.py --dry-run --restart-unhealthy

# Disable alerts (testing)
python3 agents/system/health-check.py --no-alerts
```

**Configuration:**
- Edit `agents/system/health-check-config.json` for alert settings
- Set `GMAIL_USER` and `GMAIL_APP_PASSWORD` environment variables for email alerts

### 3. Agent Dashboard (`agents/system/agent-dashboard.py`)

Interactive dashboard showing all agents and their status:

**Usage:**
```bash
# Show full dashboard
python3 agents/system/agent-dashboard.py

# Show specific agent details
python3 agents/system/agent-dashboard.py --status ai-inbox-processor

# View agent logs
python3 agents/system/agent-dashboard.py --logs ai-inbox-processor 100

# Restart an agent
python3 agents/system/agent-dashboard.py --restart ai-inbox-processor
```

### 4. Daily Briefing Integration

Agent status automatically appears in Daily Briefing:
- Shows healthy/unhealthy counts
- Highlights critical agents needing attention
- Lists non-critical issues
- Appears every morning at 7 AM

## What Gets Monitored

The system automatically discovers and monitors **all** PetesBrain LaunchAgents, including:

**Critical Agents** (auto-detected):
- `ai-inbox-processor` - AI inbox processor (every 10 min)
- `email-sync` - Email sync workflow (every 6 hours)
- `inbox-processor` - Inbox processor (daily 8 AM)
- `granola-google-docs-importer` - Meeting importer (every 5 min)
- `tasks-monitor` - Google Tasks sync (every 6 hours)
- `knowledge-base` - KB processor (every 6 hours)
- `industry-news` - Industry news monitor (every 6 hours)
- `ai-news` - AI news monitor (every 6 hours)
- `daily-anomaly-alerts` - Anomaly detector (daily 9 AM)
- And more...

**Non-Critical Agents**:
- Weekly summaries
- Product tracking
- Client-specific automation
- Reporting agents

## Health Checks Performed

For each agent, the system checks:

1. **Process Running**: Is the LaunchAgent loaded?
   - Uses `launchctl list` to verify

2. **Log Freshness**: Has the log been updated recently?
   - Interval agents: Within interval + 1 hour grace
   - Daily agents: Within 25 hours
   - Weekly agents: Within 7 days (or 25 hours on expected day)
   - Daemons: Within 15 minutes

3. **Activity Verification**: Is the agent actually working?
   - Granola: Checking for meeting fetches (not stuck at 0)
   - Inbox: Checking for processing activity
   - Email Sync: Checking for sync activity
   - Tasks: Checking for sync activity
   - KB: Checking for processing activity

## Criticality Detection

Agents are automatically classified as critical if they:
- Run frequently (interval < 1 hour)
- Match critical name patterns (email-sync, inbox-processor, etc.)
- Are daemons (continuous processes)

## Automatic Recovery

When health check detects unhealthy agents:

1. **Logs the issue** to `~/.petesbrain-health-check.log`
2. **Can auto-restart** if `--restart-unhealthy` flag is used
3. **Reports in Daily Briefing** for visibility

**Critical vs Non-Critical**:
- **Critical** failures generate alerts and immediate attention
- **Non-critical** failures are logged but less urgent

## Schedule

- **Health Check**: Runs every 30 minutes via LaunchAgent
- **Daily Briefing**: Includes agent status (daily 7 AM)
- **Dashboard**: Run manually anytime

## Manual Usage

### Check All Agents
```bash
python3 agents/system/agent-dashboard.py
```

### Check Specific Agent
```bash
python3 agents/system/agent-dashboard.py --status ai-inbox-processor
```

### View Agent Logs
```bash
python3 agents/system/agent-dashboard.py --logs ai-inbox-processor
```

### Restart Unhealthy Agents
```bash
python3 agents/system/health-check.py --restart-unhealthy
```

### View Health Check Logs
```bash
tail -f ~/.petesbrain-health-check.log
```

## Daily Briefing Integration

Agent status appears in Daily Briefing as:

```markdown
## 🤖 Agent Status

**26/35 agents healthy**

⚠️ **2 critical agent(s) need attention:**

- 🔴 **email-auto-label**: Email auto-labeling (deprecated - use email-sync)
- 🔴 **granola-weekly-summary**: Meeting weekly review (Mon 9 AM)

⚪ **7 non-critical agent(s) with issues:**

- ⚪ **label-snapshots**: Product label snapshots (daily)
- ⚪ **product-data-fetcher**: Product data fetcher (daily 6 AM)
...
```

## Troubleshooting

### Agent Not Discovered

If an agent isn't being discovered:
1. Check plist file exists: `ls ~/Library/LaunchAgents/com.petesbrain.*.plist`
2. Verify plist is valid: `plutil -lint ~/Library/LaunchAgents/com.petesbrain.AGENT.plist`
3. Check label matches pattern: Must start with `com.petesbrain.`

### False Positives

If health check reports false positives:
- Check log file path is correct in plist
- Verify schedule type is detected correctly
- Adjust activity checker thresholds if needed

### Agent Keeps Failing

If an agent repeatedly fails:
1. Check logs: `tail -f ~/.petesbrain-AGENT.log`
2. Check error log: `tail -f ~/.petesbrain-AGENT-error.log`
3. Run manually: `python3 agents/CATEGORY/script.py`
4. Check LaunchAgent: `launchctl list com.petesbrain.AGENT`

## Benefits

✅ **No Manual Configuration** - Discovers agents automatically  
✅ **Comprehensive Coverage** - Monitors all agents, not just a subset  
✅ **Intelligent Detection** - Understands schedules and criticality  
✅ **Visibility** - See status in Daily Briefing every morning  
✅ **Quick Actions** - Dashboard for fast status checks  
✅ **Auto-Recovery** - Can automatically restart failed agents  

## Related Documentation

- **[Enhanced Health Check](ENHANCED-HEALTH-CHECK.md)** - Complete documentation of all enhanced features
- [Agent Dashboard](agent-dashboard.md) - Interactive dashboard guide
- [Daily Briefing System](DAILY-BRIEFING-SYSTEM.md) - Morning briefing
- [Agents Overview](../agents/README.md) - All automation agents

---

**Key Insight:** With immediate alerts, failure tracking, and escalation, you'll know about critical issues within minutes, not hours. The system ensures nothing fails silently.
