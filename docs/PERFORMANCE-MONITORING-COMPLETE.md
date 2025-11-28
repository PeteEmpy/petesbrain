# Performance Monitoring System - Complete Implementation

**Deployed**: November 3, 2025
**Status**: ✅ Production-ready and active

## Overview

Complete automated performance monitoring system with daily anomaly detection and weekly trend analysis for all 12 ROK clients.

## Two Systems Working Together

### 1. Daily Anomaly Detection (9:00 AM Every Day)
**Purpose**: Catch immediate issues requiring attention
- Compares yesterday vs 7-day baseline
- Detects critical drops (>50% revenue, >40% ROAS, zero revenue days)
- Detects warnings (30-50% changes)
- Only sends email when anomalies found
- **File**: `shared/scripts/daily-performance-anomaly-detector.py`
- **LaunchAgent**: `com.petesbrain.daily-anomaly-alerts.plist`
- **Output**: `shared/data/daily-performance-anomalies.json`
- **Documentation**: `docs/DAILY-PERFORMANCE-ALERTS.md`

### 2. Weekly Performance Summary (Monday 8:00 AM + 8:30 AM)
**Purpose**: Strategic overview of trends and patterns
- **8:00 AM**: Fetch performance data for all clients
- **8:30 AM**: Generate summary email with performance section
- Week-over-week comparison (7 days vs previous 7)
- Trend classification (Up/Stable/Down)
- Statistical outlier detection
- **Files**:
  - `shared/scripts/fetch-weekly-client-performance.py`
  - `shared/scripts/knowledge-base-weekly-summary.py` (updated)
- **LaunchAgents**:
  - `com.petesbrain.fetch-client-performance.plist`
  - `com.petesbrain.kb-weekly-summary.plist`
- **Output**: `shared/data/weekly-client-performance.json`
- **Documentation**: `docs/WEEKLY-CLIENT-PERFORMANCE.md`

## What Gets Monitored

### All 12 Active Clients
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

### Metrics Tracked
- Revenue (conversions value)
- Cost (spend)
- ROAS (return on ad spend, expressed as percentage)
- Conversions
- Clicks
- Impressions

## Email Schedule

**Daily - 9:00 AM** (only if anomalies detected):
```
Subject: 🚨 Performance Alerts - [Date]
Content: Critical issues and warnings requiring attention
```

**Weekly - Monday 8:30 AM** (always):
```
Subject: 📅 Weekly Summary & Week Ahead - [Date Range]
Content:
1. Week Ahead (upcoming tasks)
2. Client Performance - Last Week (trends and outliers)
3. Automated Industry Monitoring
4. AI News Highlights
5. Knowledge Base Additions
6. Key Insights for ROK
7. This Week in Numbers
```

## Evidence-Based Thresholds

### Daily Anomaly Detection
Based on historical data analysis (Oct 27 - Nov 2, 2025):

**Critical (🚨)**:
- Revenue drop >50%
- Zero revenue (when baseline >£50/day)
- ROAS drop >40%
- Spend spike >50%
- Conversion drop >60%

**Warning (⚠️)**:
- Revenue change 30-50%
- ROAS change 25-40%
- Spend spike 30-50%
- Conversion drop 40-60%

### Weekly Outlier Detection
Statistical analysis using standard deviation:
- Days >1.5 standard deviations from weekly mean
- Example: Smythson Nov 2 (-70%), NDA Oct 27 (+587%)

## Test Results (Nov 3, 2025)

### Daily Anomaly Detection Test
- **Clients analyzed**: 12
- **Anomalies detected**: 24 (9 clients affected)
- **Critical issues**: 14
- **Warnings**: 10
- **Email sent**: ✅ Success (Message ID: 19a495c43ba9e501)

**Notable detections**:
- Tree2mydoor: Revenue -85%, ROAS -83%, Conversions -90%
- National Design Academy: Revenue -99%, ROAS -99%
- Smythson UK: Multiple critical drops
- Bright Minds: Revenue spike +96% (warning)

### Weekly Performance Test
- **Clients processed**: 12
- **Data range**: Oct 27 - Nov 2 vs Oct 20-26
- **Outliers detected**: Multiple (Smythson -70%, NDA -65%, etc.)
- **Email sent**: ✅ Success (Message ID: 19a49344223c0c24)
- **Performance section**: Properly formatted with Up/Stable/Down groupings

## File Locations

### Scripts
```
shared/scripts/
├── daily-performance-anomaly-detector.py    # Daily alerts
├── fetch-weekly-client-performance.py       # Weekly data fetch
└── knowledge-base-weekly-summary.py         # Weekly email (updated)
```

### Data Output
```
shared/data/
├── daily-performance-anomalies.json         # Daily anomaly results
└── weekly-client-performance.json           # Weekly performance data
```

### LaunchAgents
```
~/Library/LaunchAgents/
├── com.petesbrain.daily-anomaly-alerts.plist           # Daily 9:00 AM
├── com.petesbrain.fetch-client-performance.plist       # Mon 8:00 AM
└── com.petesbrain.kb-weekly-summary.plist              # Mon 8:30 AM
```

### Documentation
```
docs/
├── DAILY-PERFORMANCE-ALERTS.md              # Daily system details
├── WEEKLY-CLIENT-PERFORMANCE.md             # Weekly system details
├── PERFORMANCE-MONITORING-COMPLETE.md       # This file
└── AUTOMATION.md                            # Updated with new workflows
```

### Logs
```
~/.petesbrain-daily-anomaly.log              # Daily alerts log
~/.petesbrain-fetch-performance.log          # Weekly fetch log
~/.petesbrain-kb-weekly-summary.log          # Weekly summary log
```

## Dependencies

### Google Ads API
- **Library**: `google-ads` Python package
- **Config**: `/Users/administrator/google-ads.yaml`
- **Credentials**: Service account with Google Ads API access
- **All 12 client accounts**: Read access required

### Gmail API
- **Credentials**: `shared/email-sync/credentials.json`
- **Token**: `shared/email-sync/token-weekly-summary.json`
- **Scopes**: `gmail.send`

### Anthropic Claude API
- **API Key**: Set in LaunchAgent environment variables
- **Model**: claude-sonnet-4-5-20250929
- **Usage**: Weekly summary content generation only

## Monitoring Commands

### Check All Performance Workflows
```bash
launchctl list | grep -E "(daily-anomaly|fetch-client-performance|kb-weekly-summary)"
```

### View Recent Logs
```bash
# Daily alerts
tail -50 ~/.petesbrain-daily-anomaly.log

# Weekly fetch
tail -50 ~/.petesbrain-fetch-performance.log

# Weekly summary
tail -50 ~/.petesbrain-kb-weekly-summary.log
```

### Check Latest Data
```bash
# Daily anomalies
cat shared/data/daily-performance-anomalies.json | jq '.summary'

# Weekly performance
cat shared/data/weekly-client-performance.json | jq '.clients[] | {name, trend: .changes.trend}'
```

### Manual Testing
```bash
# Test daily anomaly detection
GOOGLE_ADS_CONFIGURATION_FILE_PATH=/Users/administrator/google-ads.yaml \
shared/email-sync/.venv/bin/python3 shared/scripts/daily-performance-anomaly-detector.py

# Test weekly performance fetch + summary
GOOGLE_ADS_CONFIGURATION_FILE_PATH=/Users/administrator/google-ads.yaml \
shared/email-sync/.venv/bin/python3 shared/scripts/fetch-weekly-client-performance.py

ANTHROPIC_API_KEY="your-key" \
shared/email-sync/.venv/bin/python3 shared/scripts/knowledge-base-weekly-summary.py
```

## Future Enhancements

### Threshold Refinement
- Client-specific thresholds (large vs small accounts)
- Day-of-week adjustments (weekends vs weekdays)
- Seasonal patterns (holiday periods)
- Dynamic thresholds based on historical volatility

### Additional Detection
- Click-through rate anomalies
- Impression drop detection
- Quality score changes
- Campaign-level anomalies (not just account)

### Multi-Week Analysis
- 4-week rolling averages
- Month-over-month comparisons
- Year-over-year seasonality
- Budget pacing alerts

### Integration
- Slack notifications for critical issues
- SMS alerts for emergency situations
- Dashboard visualization
- Historical trend charts

## Troubleshooting

See detailed troubleshooting sections in:
- `docs/DAILY-PERFORMANCE-ALERTS.md`
- `docs/WEEKLY-CLIENT-PERFORMANCE.md`

Common issues:
1. **No emails received**: Check logs, verify LaunchAgent loaded
2. **Missing client data**: Verify Google Ads API access
3. **Incorrect thresholds**: Adjust in script configuration
4. **Timing issues**: Ensure fetch runs before summary

## Success Criteria Met

✅ **Daily anomaly detection**: Working, tested, sending emails
✅ **Weekly performance tracking**: Working, tested, integrated
✅ **All 12 clients monitored**: Confirmed in test runs
✅ **Evidence-based thresholds**: Derived from historical data
✅ **Automated scheduling**: LaunchAgents loaded and active
✅ **Email delivery**: Gmail API integration working
✅ **Documentation**: Complete reference docs created
✅ **Test results**: Both systems tested successfully Nov 3, 2025

## Implementation Complete

Both the daily and weekly performance monitoring systems are now fully operational and will run automatically on their schedules. All documentation has been saved and the systems are production-ready.
