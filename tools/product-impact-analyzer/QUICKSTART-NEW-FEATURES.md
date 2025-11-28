# Product Impact Analyzer - Quick Start Guide (New Features)

**Date**: November 3, 2025

## What's New?

Three major features have been added to the Product Impact Analyzer:

1. **Product Change Detection** - Track price, stock, title, and description changes
2. **Per-Product Performance Monitoring** - Alert on product-level anomalies
3. **Impact Analysis Engine** - Analyze if changes were positive or negative

---

## Quick Start

### 1. First-Time Setup

The system requires Google Content API for Shopping credentials (already configured if disapproval monitoring works).

Test the product feed tracker:
```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 product_feed_tracker.py
```

Expected output:
```
[2025-11-03 08:00:00] ================================================================================
[2025-11-03 08:00:00] PRODUCT FEED TRACKER
[2025-11-03 08:00:00] ================================================================================
[2025-11-03 08:00:00]
[2025-11-03 08:00:00] Fetching products for Tree2mydoor (merchant: 107469209)...
[2025-11-03 08:00:05]   ✓ Fetched 248 products for Tree2mydoor
[2025-11-03 08:00:05]   ✓ Saved snapshot to data/product_feed_history/Tree2mydoor/2025-11-03.json
```

### 2. Run Change Detector

After running the tracker for 2+ days, run the change detector:
```bash
.venv/bin/python3 product_change_detector.py
```

Expected output:
```
[2025-11-03 08:05:00] Detecting changes for Tree2mydoor...
[2025-11-03 08:05:00]   Changed products: 12
[2025-11-03 08:05:00]     Price changes: 5
[2025-11-03 08:05:00]     Availability changes: 3
[2025-11-03 08:05:00]   New products: 2
[2025-11-03 08:05:00]   Removed products: 1
[2025-11-03 08:05:00]   ✓ Saved changes to data/product_changes/Tree2mydoor/2025-11-03.json
```

### 3. Calculate Baselines

After 7+ days of daily performance data exists:
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 product_baseline_calculator.py
```

Expected output:
```
[2025-11-03 07:00:00] ================================================================================
[2025-11-03 07:00:00] PRODUCT BASELINE CALCULATOR
[2025-11-03 07:00:00] ================================================================================
[2025-11-03 07:00:00]
[2025-11-03 07:00:00] Using 30 days of historical data
[2025-11-03 07:00:00]
[2025-11-03 07:00:00] Loading 30 days of data for Tree2mydoor...
[2025-11-03 07:00:02]   ✓ Loaded 4,587 rows from last 30 days
[2025-11-03 07:00:03] Calculating baselines for Tree2mydoor...
[2025-11-03 07:00:03]   ✓ Calculated baselines for 248 products
[2025-11-03 07:00:03]   ✓ Saved baselines to data/product_baselines/Tree2mydoor.json
```

### 4. Test Product Anomaly Detection

(This would be integrated into monitor.py, but you can test the module):
```bash
.venv/bin/python3 product_anomaly_detector.py
```

### 5. Analyze a Specific Product

Analyze impact of changes for a specific product:
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 impact_correlator.py --client "Tree2mydoor" --product-id "287"
```

Expected output:
```
[2025-11-03 10:00:00] ================================================================================
[2025-11-03 10:00:00] IMPACT ANALYSIS: Tree2mydoor - Product 287
[2025-11-03 10:00:00] ================================================================================
[2025-11-03 10:00:00]
[2025-11-03 10:00:00] Finding changes for product 287 in last 90 days...
[2025-11-03 10:00:01]   ✓ Found 2 change events
[2025-11-03 10:00:01] Analyzing impact of change on 2025-10-15...
[2025-11-03 10:00:02]   ✓ Impact: positive (revenue 9.5%)
[2025-11-03 10:00:02]
[2025-11-03 10:00:02] ================================================================================
[2025-11-03 10:00:02] ANALYSIS COMPLETE
[2025-11-03 10:00:02] ================================================================================
[2025-11-03 10:00:02]
[2025-11-03 10:00:02] Changes analyzed: 2
[2025-11-03 10:00:02]   Positive impact: 1
[2025-11-03 10:00:02]   Negative impact: 1
[2025-11-03 10:00:02]   Neutral impact: 0
```

### 6. Generate Weekly Report

Generate a summary of all changes this week:
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 weekly_impact_report.py
```

Output will be saved to `reports/Tree2mydoor_2025-10-28_to_2025-11-03.txt`

---

## Automated Scheduling

### Daily Tasks (8:00 AM)

Create `~/Library/LaunchAgents/com.petesbrain.product-tracking.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.product-tracking</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>
        cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer &amp;&amp;
        GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json .venv/bin/python3 product_feed_tracker.py &amp;&amp;
        sleep 60 &amp;&amp;
        .venv/bin/python3 product_change_detector.py
        </string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/administrator/.petesbrain-product-tracking.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/administrator/.petesbrain-product-tracking.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.product-tracking.plist
```

Check status:
```bash
launchctl list | grep petesbrain.product-tracking
```

View logs:
```bash
tail -f ~/.petesbrain-product-tracking.log
```

### Weekly Tasks (Monday 7:00 AM)

Create `~/Library/LaunchAgents/com.petesbrain.baseline-calculator.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.baseline-calculator</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>
        cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer &amp;&amp;
        GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json .venv/bin/python3 product_baseline_calculator.py
        </string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/administrator/.petesbrain-baseline-calculator.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/administrator/.petesbrain-baseline-calculator.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.baseline-calculator.plist
```

### Weekly Report (Monday 9:00 AM)

Create `~/Library/LaunchAgents/com.petesbrain.weekly-impact-report.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.weekly-impact-report</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>
        cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer &amp;&amp;
        GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json .venv/bin/python3 weekly_impact_report.py
        </string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/administrator/.petesbrain-weekly-impact-report.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/administrator/.petesbrain-weekly-impact-report.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.weekly-impact-report.plist
```

---

## Email Configuration

To enable product anomaly email alerts, update `config.json`:

```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password"
  }
}
```

**Gmail App Password Setup**:
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Enter "PetesBrain Product Monitor"
4. Copy the generated password
5. Paste into config.json

---

## Troubleshooting

### Product feed tracker fails

**Error**: `403 Forbidden` or `The caller does not have permission`

**Fix**: Ensure service account has Content API for Shopping access:
1. Go to Google Cloud Console
2. Navigate to APIs & Services > Enabled APIs
3. Ensure "Content API for Shopping" is enabled
4. Check service account has proper permissions in Merchant Center

### Change detector shows no changes

**Cause**: Need at least 2 days of snapshots

**Fix**: Run product feed tracker for 2+ consecutive days before running change detector

### Baseline calculator shows no data

**Cause**: Need at least 7 days of daily performance data in per-client spreadsheets

**Fix**: Ensure daily monitoring has been running for 7+ days

### Impact correlator shows "insufficient data"

**Cause**: Need sufficient data before AND after change date

**Fix**:
- Changes must be at least 7 days old (need data after change)
- Changes must have 7+ days of data before them
- Wait longer, then re-run analysis

---

## What to Expect

### After 1 Day
- Product feed snapshots being created
- Ready for change detection on day 2

### After 2 Days
- Change detection working
- Seeing price/availability/title changes

### After 7 Days
- Baseline calculation possible
- Product anomaly detection can start

### After 14 Days
- Impact analysis becomes meaningful
- Can analyze recent changes

### After 30 Days
- Full system operational
- High-confidence baselines
- Comprehensive impact analysis available

---

## Next Steps

1. **Test with 1-2 clients first** - Run manually for a week
2. **Set up automation** - LaunchAgents for daily/weekly runs
3. **Configure email alerts** - Add SMTP credentials to config.json
4. **Roll out to all clients** - Once testing validates the system
5. **Analyze first month** - Review insights and tune thresholds

---

## Getting Help

**Documentation**:
- Complete system docs: [COMPLETE-SYSTEM.md](COMPLETE-SYSTEM.md)
- Implementation status: [IMPLEMENTATION-STATUS.md](IMPLEMENTATION-STATUS.md)
- Capability review: [CAPABILITY-REVIEW.md](CAPABILITY-REVIEW.md)

**Logs**:
```bash
# Daily tracking
tail -f ~/.petesbrain-product-tracking.log

# Weekly baseline
tail -f ~/.petesbrain-baseline-calculator.log

# Weekly report
tail -f ~/.petesbrain-weekly-impact-report.log
```

**Manual runs** (for debugging):
```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Test tracker
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 product_feed_tracker.py

# Test change detector
.venv/bin/python3 product_change_detector.py

# Test baseline calculator
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 product_baseline_calculator.py
```
