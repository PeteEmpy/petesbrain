# Daily Performance Anomaly Detection System

## Overview
Automated daily email alerts for unusual client performance patterns.
Detects anomalies in revenue, ROAS, spend, and conversions by comparing yesterday's data to a 7-day baseline.

**Status**: ✅ Active, Production-ready (deployed Nov 3, 2025)

## What It Does

### Daily Monitoring
- Runs every morning at **9:00 AM**
- Analyzes yesterday's performance for all 12 active clients
- Compares to 7-day baseline (excluding yesterday)
- Only sends email when anomalies are detected (no noise on normal days)

### Detection Types

**CRITICAL (🚨) Thresholds:**
- Revenue drop >50% from 7-day average
- Zero revenue days (when baseline >£50/day)
- ROAS drop >40% from baseline
- Spend spike >50% above average
- Conversion drop >60% from average

**WARNING (⚠️) Thresholds:**
- Revenue change 30-50% from average
- ROAS change 25-40% from baseline
- Spend spike 30-50% above average
- Conversion drop 40-60% from average

### Evidence-Based Thresholds
Thresholds established from historical data analysis (Oct 27 - Nov 2, 2025):
- Smythson: -70% revenue outlier detected
- National Design Academy: -99% revenue drop
- Tree2mydoor: Zero revenue day (£0)
- Multiple clients showing 30-50% daily variations

These can be refined over time based on what proves most useful.

## Files

### Scripts
- **`shared/scripts/daily-performance-anomaly-detector.py`** - Main detection script
  - Fetches yesterday's data via Google Ads API
  - Calculates 7-day baseline
  - Detects anomalies across multiple metrics
  - Generates and sends HTML email alerts
  - Saves results to JSON

### Data
- **`shared/data/daily-performance-anomalies.json`** - Daily output
  - Target date and baseline period
  - All detected anomalies with severity levels
  - Summary statistics (total clients checked, anomaly counts)

### Configuration
- **`~/Library/LaunchAgents/com.petesbrain.daily-anomaly-alerts.plist`** - Scheduler
  - Runs daily at 9:00 AM
  - Logs to `~/.petesbrain-daily-anomaly.log`

## Active Clients Monitored

All 12 ROK clients:
1. Bright Minds (1404868570)
2. Tree2mydoor (4941701449)
3. National Design Academy (1994728449)
4. Accessories for the Home (7972994730)
5. Devonshire Hotels (5898250490)
6. Go Glean (8492163737)
7. Godshot (9922220205)
8. Grain Guard (4391940141)
9. Just Bin Bags (9697059148)
10. Smythson UK (8573235780)
11. Superspace (7482100090)
12. Uno Lighting (6413338364)

## Email Format

**Subject**: `🚨 Performance Alerts - [Date]`

**Sections**:
1. **Critical Issues** - Clients with severe anomalies requiring immediate attention
2. **Warnings** - Clients with moderate changes worth monitoring
3. **Footer** - Threshold explanations and baseline info

**Example**:
```
🚨 Daily Performance Alerts - November 3, 2025

CRITICAL ISSUES (3 clients):
• Tree2mydoor: Revenue £26 (84% below baseline £176)
  - ROAS 14% (83% below baseline 88%)
  - Conversions 1.0 (90% below baseline 10.5)

• National Design Academy: Revenue £3 (99% below baseline £401)
  - ROAS 0% (99% below baseline 33%)

WARNINGS (2 clients):
• Bright Minds: Revenue £939 (96% above baseline £478)
  - ROAS 453% (61% above baseline 281%)
```

## Running Manually

```bash
# Test with current data
GOOGLE_ADS_CONFIGURATION_FILE_PATH=/Users/administrator/google-ads.yaml \
/Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3 \
/Users/administrator/Documents/PetesBrain/shared/scripts/daily-performance-anomaly-detector.py

# View output
cat /Users/administrator/Documents/PetesBrain/shared/data/daily-performance-anomalies.json
```

## Monitoring

**Check LaunchAgent Status:**
```bash
launchctl list | grep daily-anomaly
```

**View Logs:**
```bash
tail -50 ~/.petesbrain-daily-anomaly.log
```

**Reload After Changes:**
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.daily-anomaly-alerts.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.daily-anomaly-alerts.plist
```

## Threshold Refinement

### Current Settings
These are starting thresholds based on Oct 2025 data analysis and can be adjusted in the script.

### How to Adjust
Edit `daily-performance-anomaly-detector.py`:

```python
THRESHOLDS = {
    'critical': {
        'revenue_drop_pct': 50,      # Increase = less sensitive
        'roas_drop_pct': 40,
        'spend_spike_pct': 50,
        'conversion_drop_pct': 60,
        'zero_revenue_min': 50
    },
    'warning': {
        'revenue_change_pct': 30,
        'roas_change_pct': 25,
        'spend_spike_pct': 30,
        'conversion_drop_pct': 40
    }
}
```

### Potential Refinements
- **Client-specific thresholds** (large vs small accounts)
- **Day-of-week adjustments** (weekends vs weekdays)
- **Seasonal patterns** (holiday periods)
- **Add new detection types** (click-through rate, impression drops, etc.)

## Integration with Weekly Summary

The daily alerts complement the weekly summary system:
- **Daily (9:00 AM)**: Anomaly detection for immediate issues
- **Weekly (Monday 8:30 AM)**: Comprehensive performance review with trends

Both systems share the same Google Ads API credentials and client list for consistency.

## Troubleshooting

### No Email Received
1. Check if anomalies were detected: `cat shared/data/daily-performance-anomalies.json`
2. View logs: `cat ~/.petesbrain-daily-anomaly.log`
3. Test manually (see "Running Manually" above)

### Too Many Alerts
- Increase threshold percentages in `THRESHOLDS` dict
- Add client-specific exclusions
- Adjust baseline window (currently 7 days)

### Missing Clients
- Verify client is in `ACTIVE_CLIENTS` dict
- Check Google Ads API access for that account
- Review logs for specific error messages

## Implementation History

**Nov 3, 2025**: Initial deployment
- Evidence-based thresholds from historical data
- 12 active clients monitored
- Severity-based alerting (Critical vs Warning)
- HTML email with clear formatting
- Automated daily at 9:00 AM

**Test Results** (Nov 3, 2025):
- 24 anomalies detected across 9 clients
- 14 critical, 10 warnings
- Email sent successfully
- System performing as expected
