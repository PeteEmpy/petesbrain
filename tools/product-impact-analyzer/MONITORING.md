# Product Impact Analyzer - Real-Time Monitoring

**Status**: ✅ Ready for deployment
**Last Updated**: October 30, 2025

## Overview

Real-time monitoring detects critical product changes **as they happen** and sends immediate alerts, allowing you to respond quickly to revenue drops, investigate spikes, and catch feed issues before they impact performance.

## Key Features

### 🚨 Immediate Alerts
- **Critical revenue drops** - Alert when revenue drops >£500 in 24 hours
- **Revenue spikes** - Investigate unexpected gains (opportunities!)
- **Click drops** - Alert when clicks drop >50% in 24 hours
- **Missing products** - Detect when 5+ products disappear from feed

### ⏰ Smart Alerting
- Only alerts during **business hours** (9 AM - 6 PM, weekdays)
- No spam on weekends or at night
- Customizable thresholds for your needs

### 📧 Multi-Channel Delivery
- **Email** - Immediate alerts to petere@roksys.co.uk
- **Slack** - Optional webhook integration
- **Future**: SMS via Twilio

### 📊 Daily Snapshots
- Takes snapshots every day at 10 AM
- Compares to previous day
- Builds historical baseline automatically

---

## Installation

### Quick Setup

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
./setup_monitoring.sh
```

This will:
1. ✅ Create monitoring LaunchAgent
2. ✅ Configure environment variables
3. ✅ Set up daily 10 AM checks
4. ✅ Optionally run test check

### Prerequisites

- Phase 2 automation already set up (`./setup_automation.sh` completed)
- Environment variables configured (ANTHROPIC_API_KEY, GMAIL_APP_PASSWORD)

---

## How It Works

### Daily Workflow

```
Every day at 10 AM:
    ↓
1. Fetch latest Google Ads data (last 24 hours)
    ↓
2. Aggregate metrics by product
    ↓
3. Compare to yesterday's snapshot
    ↓
4. Detect critical changes:
   - Revenue drops > £500
   - Revenue spikes > £500
   - Click drops > 50%
   - Missing products (5+)
    ↓
5. If alerts found AND business hours:
   → Send email alert
   → Send Slack message (if configured)
    ↓
6. Save today's snapshot for tomorrow
```

### Alert Types

| Alert Type | Severity | Trigger | Example |
|------------|----------|---------|---------|
| **Revenue Drop** | 🔥 Critical | Revenue -£500+ in 24h | "Product 287 revenue dropped £680 - investigate!" |
| **Click Drop** | ⚠️ Warning | Clicks -50%+ in 24h | "Product 593 clicks dropped 75% - check availability" |
| **Products Missing** | ⚠️ Warning | 5+ products disappeared | "15 products missing from feed - sync issue?" |
| **Revenue Spike** | 💡 Info | Revenue +£500+ in 24h | "Product 287 spiked +£850 - what changed?" |

---

## Configuration

### Alert Thresholds

Edit `config.json` to customize:

```json
{
  "monitoring": {
    "enabled": true,
    "check_frequency": "daily",

    "alert_revenue_drop_threshold": 500,     // £500 revenue drop triggers alert
    "alert_revenue_spike_threshold": 500,    // £500 revenue spike triggers alert
    "alert_click_drop_threshold_percent": 50, // 50% click drop triggers alert
    "alert_product_missing_count": 5,         // 5+ missing products triggers alert

    "alert_hours_start": 9,  // Start alerting at 9 AM
    "alert_hours_end": 18,   // Stop alerting at 6 PM

    "slack_webhook": null  // Add webhook URL to enable Slack
  }
}
```

### Example Configurations

**Conservative** (fewer alerts):
```json
{
  "alert_revenue_drop_threshold": 1000,  // Only alert for >£1000 drops
  "alert_click_drop_threshold_percent": 75,  // Only alert for >75% drops
  "alert_product_missing_count": 10   // Only alert for 10+ missing products
}
```

**Aggressive** (more sensitive):
```json
{
  "alert_revenue_drop_threshold": 200,  // Alert for >£200 drops
  "alert_click_drop_threshold_percent": 30,  // Alert for >30% drops
  "alert_product_missing_count": 3   // Alert for 3+ missing products
}
```

---

## Email Alerts

### What You'll Receive

Subject: **🚨 Product Impact Alert - 3 Critical Changes**

```
┌──────────────────────────────────────┐
│ 🚨 Product Impact Alert              │
│ Alert Time: October 30, 2025 10:15 AM│
│ Total: 3 alerts (2 critical, 1 info) │
└──────────────────────────────────────┘

🔥 Critical Alerts
──────────────────
🔥 Tree2mydoor - 287: Olive Tree Large
   Revenue dropped £680 in last 24 hours
   Change: -£680.00 | Threshold: -£500.00

🔥 Tree2mydoor - 593: Lemon Tree Medium
   Revenue dropped £520 in last 24 hours
   Change: -£520.00 | Threshold: -£500.00

💡 Opportunities
──────────────────
💡 Smythson - FCB7007: Card Holder Black
   Revenue spiked +£850 in last 24 hours
```

---

## Slack Integration (Optional)

### Setup

1. **Create Slack Incoming Webhook**:
   - Go to https://api.slack.com/apps
   - Create new app → Incoming Webhooks
   - Activate Incoming Webhooks
   - Add New Webhook to Workspace
   - Select channel (e.g., #ppc-alerts)
   - Copy webhook URL

2. **Add to config.json**:
   ```json
   {
     "monitoring": {
       "slack_webhook": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
     }
   }
   ```

3. **Reload LaunchAgent**:
   ```bash
   cd tools/product-impact-analyzer
   launchctl unload ~/Library/LaunchAgents/com.petesbrain.product-monitor.plist
   launchctl load ~/Library/LaunchAgents/com.petesbrain.product-monitor.plist
   ```

### Slack Message Format

```
🚨 *Product Impact Alert*

Total: 3 alerts (2 critical, 1 warnings)

🔥 *Tree2mydoor* - 287
   Revenue dropped £680 in last 24 hours

🔥 *Tree2mydoor* - 593
   Revenue dropped £520 in last 24 hours

💡 *Smythson* - FCB7007
   Revenue spiked +£850 in last 24 hours - investigate!
```

---

## Usage

### Automated (Default)

Once set up, monitoring runs automatically every day at 10 AM. **No action required!**

### Manual Runs

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Full check (respects business hours)
.venv/bin/python3 monitor.py

# Test mode (ignore business hours, always alert)
.venv/bin/python3 monitor.py --test

# Check specific client only
.venv/bin/python3 monitor.py --client "Tree2mydoor" --test
```

---

## Logs & Monitoring

### Log Files

| File | Purpose |
|------|---------|
| `~/.petesbrain-product-monitor.log` | Standard output |
| `~/.petesbrain-product-monitor-error.log` | Error output |

### View Logs

```bash
# Tail standard log
tail -f ~/.petesbrain-product-monitor.log

# View last run
tail -20 ~/.petesbrain-product-monitor.log

# Check for errors
cat ~/.petesbrain-product-monitor-error.log
```

### Check Status

```bash
# Is LaunchAgent running?
launchctl list | grep product-monitor

# View LaunchAgent details
launchctl print user/$(id -u)/com.petesbrain.product-monitor

# Reload LaunchAgent (after config changes)
launchctl unload ~/Library/LaunchAgents/com.petesbrain.product-monitor.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.product-monitor.plist
```

---

## Troubleshooting

### No Alerts Received

1. **Check if monitoring is enabled**:
   ```bash
   cat config.json | grep '"enabled"'
   ```

2. **Check business hours**:
   - Alerts only sent 9 AM - 6 PM, weekdays
   - Test mode bypasses this: `monitor.py --test`

3. **Check email configuration**:
   - Verify GMAIL_APP_PASSWORD is set
   - Check error log for SMTP errors

4. **Check thresholds**:
   - Changes may not exceed alert thresholds
   - Lower thresholds to be more sensitive

### LaunchAgent Not Running

```bash
# Check if loaded
launchctl list | grep product-monitor

# If not loaded, load it
launchctl load ~/Library/LaunchAgents/com.petesbrain.product-monitor.plist

# Check for errors
cat ~/.petesbrain-product-monitor-error.log
```

### No Data for Comparison

First run won't generate alerts (needs baseline). Run twice:

```bash
# First run - establishes baseline
.venv/bin/python3 monitor.py --test

# Wait or manually change data

# Second run - compares to baseline
.venv/bin/python3 monitor.py --test
```

---

## Advanced Features

### Custom Alert Logic

Edit `monitor.py` to add custom alert types:

```python
# Example: Alert on conversion rate drops
if prev_metrics['conversions'] > 0:
    conv_rate_old = prev_metrics['conversions'] / prev_metrics['clicks']
    conv_rate_new = current_metrics['conversions'] / current_metrics['clicks']

    if conv_rate_new < conv_rate_old * 0.5:  # 50% drop in conversion rate
        alerts.append(Alert(
            severity="warning",
            alert_type="conversion_rate_drop",
            message=f"Conversion rate dropped 50%"
        ))
```

### Multiple Daily Checks

Change LaunchAgent schedule for more frequent checks:

Edit `~/Library/LaunchAgents/com.petesbrain.product-monitor.plist`:

```xml
<!-- Every 6 hours -->
<key>StartCalendarInterval</key>
<array>
    <dict><key>Hour</key><integer>6</integer></dict>
    <dict><key>Hour</key><integer>12</integer></dict>
    <dict><key>Hour</key><integer>18</integer></dict>
</array>
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.product-monitor.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.product-monitor.plist
```

---

## Integration with Weekly Reports

### How They Work Together

**Daily Monitoring** (10 AM):
- Quick checks for immediate issues
- Alerts for critical changes
- Takes snapshots for comparison

**Weekly Analysis** (Tuesday 9 AM):
- Comprehensive impact analysis
- Trend analysis over time
- Anomaly detection
- Professional report generation

**They complement each other**:
- Monitoring catches problems early
- Weekly report provides deep insights
- Both use same data sources

---

## FAQ

**Q: Will I get alerts every day?**
A: Only if critical changes are detected. Most days = no alerts (which is good!).

**Q: Can I disable monitoring temporarily?**
A: Yes, set `"enabled": false` in config.json monitoring section.

**Q: What if I'm on vacation?**
A: Alerts will pause outside business hours. Or temporarily disable monitoring.

**Q: Can I add more recipients?**
A: Currently single recipient. Would need to modify `monitor.py` to support multiple.

**Q: How much data does it use?**
A: Minimal - only fetches last 24 hours of data per client.

**Q: Does it replace weekly reports?**
A: No! They work together. Monitoring = immediate alerts. Weekly = comprehensive analysis.

---

## Future Enhancements

Potential improvements:

1. **SMS Alerts** - Via Twilio for critical issues
2. **Mobile App** - Push notifications
3. **Alert Routing** - Different thresholds per client
4. **Machine Learning** - Smart anomaly detection
5. **Auto-Responses** - Automatic actions for certain alerts

---

## Support

Questions or issues?

- **Logs**: Check `~/.petesbrain-product-monitor.log` first
- **Test run**: `python3 monitor.py --test`
- **Ask Claude**: "Why didn't I get a monitoring alert?"
- **Documentation**: This file + `PHASE2.md`

---

**Built with**: Python 3, Gmail SMTP, Slack API (optional), macOS LaunchAgent
**Version**: 1.0.0
**Release Date**: October 30, 2025
