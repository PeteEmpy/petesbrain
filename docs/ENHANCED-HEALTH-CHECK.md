# Enhanced Health Check System - Complete Documentation

**Status:** ✅ Fully Implemented  
**Last Updated:** 2025-11-09

## Overview

The Enhanced Health Check System provides comprehensive monitoring of all PetesBrain agents with immediate alerts, failure tracking, escalation, and system resource monitoring. You'll never miss a critical failure again.

## Key Features

### ✅ Immediate Email Alerts
- Sends email immediately when critical agents fail
- Configurable email addresses and throttling
- HTML email with detailed failure information

### ✅ Failure Tracking & Escalation
- Tracks failure history for each agent
- Escalates agents that fail 3+ times in 24 hours
- Maintains failure history for analysis

### ✅ Alert Throttling
- Prevents alert spam (configurable throttle period)
- Tracks last alert time per agent
- Only alerts on new failures if configured

### ✅ New Failure Detection
- Compares current state to previous state
- Only alerts on newly failed agents (optional)
- Tracks state between health checks

### ✅ Health Check Self-Monitoring
- Monitors if health check itself is running
- Alerts if health check hasn't run in configured time
- Ensures monitoring system is working

### ✅ System Resource Monitoring
- Disk space monitoring (alerts if < threshold)
- Memory usage monitoring (alerts if > threshold)
- Internet connectivity checks
- All configurable thresholds

### ✅ Multiple Notification Channels
- **Email**: Immediate HTML emails (Gmail SMTP)
- **Slack**: Webhook integration (optional)
- **SMS**: Twilio integration (optional, not yet implemented)

### ✅ Dependency Health Checks
- Gmail API token validation
- Google Ads API credentials check
- Internet connectivity verification

## Configuration

### Configuration File

Location: `agents/system/health-check-config.json`

```json
{
  "alerts": {
    "email": {
      "enabled": true,
      "to": null,
      "from": null,
      "critical_only": false,
      "throttle_hours": 1
    },
    "slack": {
      "enabled": false,
      "webhook_url": null
    },
    "sms": {
      "enabled": false,
      "provider": "twilio",
      "api_key": null,
      "api_secret": null,
      "from_number": null,
      "to_number": null
    }
  },
  "monitoring": {
    "check_disk_space": true,
    "disk_space_threshold_gb": 10,
    "check_memory": true,
    "memory_threshold_percent": 90,
    "check_internet": true,
    "check_apis": true
  },
  "failure_tracking": {
    "escalation_threshold": 3,
    "escalation_window_hours": 24,
    "alert_on_new_failures_only": true
  },
  "self_monitoring": {
    "enabled": true,
    "alert_if_not_run_hours": 1
  }
}
```

### Environment Variables

The system uses these environment variables (if config file values are null):

- `GMAIL_USER` - Email address for alerts
- `GMAIL_APP_PASSWORD` - Gmail app password for SMTP

## Usage

### Basic Health Check

```bash
python3 agents/system/health-check.py
```

### Verbose Output

```bash
python3 agents/system/health-check.py --verbose
```

### Auto-Restart Unhealthy Agents

```bash
python3 agents/system/health-check.py --restart-unhealthy
```

### Dry Run (Test Without Actions)

```bash
python3 agents/system/health-check.py --dry-run --restart-unhealthy
```

### Disable Alerts (Testing)

```bash
python3 agents/system/health-check.py --no-alerts
```

## Alert Types

### Critical Failures
- Agents marked as critical that are unhealthy
- Immediate email alert (if throttling allows)
- Logged to health check log

### Escalated Agents
- Agents that have failed 3+ times in 24 hours
- Highlighted in alert emails
- Requires immediate attention

### New Failures
- Agents that just became unhealthy (compared to previous check)
- Only alerted if `alert_on_new_failures_only` is true
- Helps distinguish new issues from ongoing ones

### System Issues
- Disk space below threshold
- Memory usage above threshold
- Internet connectivity issues
- API credential problems

### Restart Failures
- Agents that couldn't be automatically restarted
- Critical issue requiring manual intervention

## Alert Email Format

Alert emails include:

1. **Critical Failures Section** - Red highlighted
2. **Escalated Agents Section** - Red highlighted with failure count
3. **New Failures Section** - Yellow highlighted
4. **Restart Failed Section** - Red highlighted
5. **System Issues Section** - Yellow highlighted

Each section includes:
- Agent name and description
- Failure count (for escalated agents)
- Troubleshooting links

## Failure Tracking

### Failure History File

Location: `~/.petesbrain-failure-history.json`

Stores:
- Timestamp of each failure
- Whether failure was critical
- Last 100 failures per agent

### Escalation Logic

An agent is escalated if:
- It has failed `escalation_threshold` times (default: 3)
- Within `escalation_window_hours` (default: 24)

Escalated agents:
- Highlighted in alert emails
- Shown separately in summary
- Require immediate attention

## Alert Throttling

### How It Works

- Tracks last alert time per agent per alert type
- Only sends alert if `throttle_hours` have passed since last alert
- Prevents alert spam for persistent issues

### Alert Types Tracked

- `critical` - Critical failure alerts
- `new_failure` - New failure alerts
- `escalated` - Escalation alerts

### Throttle State File

Location: `~/.petesbrain-alert-state.json`

Stores last alert timestamp for each agent/type combination.

## System Resource Monitoring

### Disk Space

- Checks available disk space on root partition
- Alerts if below `disk_space_threshold_gb` (default: 10GB)
- Can be disabled in config

### Memory Usage

- Checks system memory usage
- Alerts if above `memory_threshold_percent` (default: 90%)
- Requires `psutil` package (optional, graceful fallback)
- Can be disabled in config

### Internet Connectivity

- Checks connectivity to Google DNS (8.8.8.8)
- Alerts if no internet connection
- Can be disabled in config

## Dependency Checks

### Gmail API

- Checks for token file existence
- Validates token age (alerts if > 7 days old)
- Can be disabled in config

### Google Ads API

- Checks for credentials file existence
- Can be disabled in config

## Health Check Self-Monitoring

### How It Works

- Checks health check log file timestamp
- Alerts if log hasn't been updated in `alert_if_not_run_hours`
- Ensures monitoring system itself is working

### Self-Monitoring Alert

If health check hasn't run:
- Sends immediate email alert
- Critical priority
- Helps catch if LaunchAgent is broken

## State Files

### Failure History
`~/.petesbrain-failure-history.json`
- Tracks all failures with timestamps
- Used for escalation detection

### Alert State
`~/.petesbrain-alert-state.json`
- Tracks last alert time per agent
- Used for throttling

### Health Check State
`~/.petesbrain-health-check-state.json`
- Stores last known unhealthy agents
- Used for new failure detection

## Notification Channels

### Email (Primary)

**Configuration:**
- Set `GMAIL_USER` and `GMAIL_APP_PASSWORD` environment variables
- Or configure in `health-check-config.json`

**Features:**
- HTML formatted emails
- Critical vs. non-critical distinction
- Detailed failure information
- Throttling support

### Slack (Optional)

**Configuration:**
1. Create Slack webhook URL
2. Set `webhook_url` in config
3. Set `enabled: true`

**Features:**
- Simple text alerts
- Quick notifications
- No throttling (Slack handles rate limiting)

### SMS (Future)

- Twilio integration planned
- Not yet implemented
- Will support critical-only alerts

## Exit Codes

- `0` - All systems healthy
- `1` - Some systems unhealthy (non-critical)
- `2` - Critical failure detected

## Integration with Daily Briefing

The Daily Briefing still includes agent status, but immediate alerts ensure you know about critical issues right away, not just in the morning briefing.

## Troubleshooting

### Alerts Not Sending

1. Check `GMAIL_USER` and `GMAIL_APP_PASSWORD` are set
2. Verify email config in `health-check-config.json`
3. Check alert throttling (may have already alerted)
4. Check health check log: `tail -f ~/.petesbrain-health-check.log`

### False Positives

1. Adjust thresholds in config file
2. Check log freshness calculations
3. Verify agent schedules are correct
4. Review activity checker logic

### Missing Dependencies

- `psutil` - Optional, for memory monitoring (graceful fallback)
- All other dependencies are standard library

## Best Practices

1. **Set Email Alerts** - Configure `GMAIL_USER` and `GMAIL_APP_PASSWORD`
2. **Review Thresholds** - Adjust disk/memory thresholds for your system
3. **Monitor Escalations** - Pay attention to escalated agents
4. **Check Logs Regularly** - Review `~/.petesbrain-health-check.log`
5. **Test Alerts** - Run with `--verbose` to see what would be alerted

## Example Alert Email

```
🚨 CRITICAL: 2 Agent(s) Failed

❌ Critical Failures (2)
• email-sync - Email sync workflow (Failed 3 times in last 24h)
• ai-inbox-processor - AI inbox processor (Failed 1 times in last 24h)

⚠️ Escalated Agents (1)
• email-sync - Email sync workflow (3 failures)

💻 System Issues (1)
• Disk space: Only 8.5GB free (threshold: 10GB)
```

## Related Documentation

- [System Health Monitoring](SYSTEM-HEALTH-MONITORING.md) - Original documentation
- [Agent Dashboard](agent-dashboard.md) - Interactive dashboard
- [Daily Briefing System](../reporting/DAILY-BRIEFING-SYSTEM.md) - Morning briefing

---

**Key Insight:** With immediate alerts, failure tracking, and escalation, you'll know about critical issues within minutes, not hours. The system ensures nothing fails silently.

