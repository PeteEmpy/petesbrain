# Product Impact Analyzer - Current Status

**Date**: November 2, 2025
**Status**: 🚨 AT CAPACITY LIMIT - Action Required

## Current Situation

### Spreadsheet Capacity: 100% (CRITICAL)

- **Total cells**: 9,996,090 / 10,000,000 (99.96%)
- **Daily Performance**: 323,807 rows × 26 columns = 8,418,982 cells (84.2%)
- **Days until full**: 0 (at limit NOW)

### What Data is Currently Available

**Successfully Backfilled (Partial 90-day)**:
1. ✅ Tree2mydoor - 90 days (Aug 3 - Nov 1)
2. ✅ Smythson UK - 90 days (Aug 3 - Nov 1)
3. ✅ BrightMinds - 90 days (Aug 3 - Nov 1)
4. ✅ Accessories for the Home - 90 days (Aug 3 - Nov 1) ⭐
5. ✅ Go Glean UK - 90 days (Aug 3 - Nov 1)
6. ✅ Superspace UK - 90 days (Aug 3 - Nov 1)

**Not Backfilled (Hit Capacity Limit)**:
7. ❌ Uno Lights - Only partial data (stopped at batch 10/12)
8. ❌ Devonshire Hotels - No shopping data available
9. ❌ Godshot - Only 17 days available
10. ❌ HappySnapGifts - Not backfilled
11. ❌ WheatyBags - Not backfilled
12. ❌ BMPM - Not backfilled
13. ❌ Grain Guard - Not backfilled
14. ❌ Crowd Control - Not backfilled
15. ❌ Just Bin Bags - Not backfilled

**GOOD NEWS**: Your primary question about **Accessories for the Home October volatility** CAN be analyzed - you have 90 days of AFH data! ✅

## Immediate Action Required

### Option 1: Run Archive Script NOW (Recommended)

This will move old data to a separate archive spreadsheet and free up 80%+ capacity:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \\
  .venv/bin/python3 archive_old_data.py --yes --keep-days 30
```

**What this does**:
- Keeps last 30 days in main sheet (~4M cells)
- Moves older data (60 days) to "Product Impact Analyzer - Archive 2025"
- Frees ~4M cells (40% capacity)
- Allows daily accumulation to continue

**After archiving**: You can then backfill the remaining 9 clients

### Option 2: Accept Current State

- You have 6 clients with 90 days of historical data
- AFH (your primary concern) is included ✅
- Daily accumulation will continue from tomorrow
- Archive in 2 weeks when capacity fills again

## Automated Monitoring

### Capacity Check Script

**Created**: [check_capacity.py](tools/product-impact-analyzer/check_capacity.py)

**What it does**:
- Checks spreadsheet capacity daily
- Sends email alerts at 70%, 85%, and 95% capacity
- Tells you exactly when to run archival
- Runs automatically via LaunchAgent (setup below)

**Manual check**:
```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \\
  .venv/bin/python3 check_capacity.py
```

### Alert Thresholds

| Capacity | Alert Level | Action Required | Timeline |
|----------|-------------|-----------------|----------|
| 70-84% | ℹ️  INFO | Plan archival | 2-4 weeks |
| 85-94% | ⚠️  WARNING | Schedule archival | 1 week |
| 95-100% | 🚨 CRITICAL | Archive NOW | Immediate |

**Current**: 🚨 CRITICAL (100%)

## Setup Automated Monitoring

Create LaunchAgent to check capacity daily:

```bash
cat > ~/Library/LaunchAgents/com.petesbrain.capacity-check.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.capacity-check</string>

    <key>ProgramArguments</key>
    <array>
        <string>/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/.venv/bin/python3</string>
        <string>/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/check_capacity.py</string>
    </array>

    <key>EnvironmentVariables</key>
    <dict>
        <key>GOOGLE_APPLICATION_CREDENTIALS</key>
        <string>/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json</string>
        <key>GMAIL_USER</key>
        <string>your-email@gmail.com</string>
        <key>GMAIL_APP_PASSWORD</key>
        <string>your-app-password</string>
        <key>ALERT_EMAIL</key>
        <string>your-email@gmail.com</string>
    </dict>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/Users/administrator/.petesbrain-capacity-check.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/administrator/.petesbrain-capacity-check.log</string>
</dict>
</plist>
EOF

# Load the LaunchAgent
launchctl load ~/Library/LaunchAgents/com.petesbrain.capacity-check.plist

# Check status
launchctl list | grep capacity-check

# View logs
tail -f ~/.petesbrain-capacity-check.log
```

## Completing the Backfill for Other Clients

Once you've archived old data and freed up capacity:

```bash
# Clear progress file
rm -f tools/product-impact-analyzer/data/backfill_progress.json

# Run backfill for 30 days (fits in freed space)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \\
  .venv/bin/python3 backfill_historical_data.py --yes --days 30
```

**This will backfill**:
- All 15 clients
- Last 30 days of data
- ~4M cells total (fits easily after archival)

## Long-Term Maintenance Schedule

### Daily (Automated)
- 9:00 AM: Capacity check (alerts if needed)
- 9:30 AM: Fetch data from Google Ads API
- 10:00 AM: Monitor runs, appends yesterday to Daily Performance

### Every 2 Weeks (Manual, When Alerted)
- Run archival script when capacity check sends WARNING alert (85%+)
- Keep last 30-60 days in main sheet
- Move older data to archives

### Quarterly (Manual)
- Review archive spreadsheets
- Verify data quality and accessibility
- Consider BigQuery migration if archives become unwieldy

## Analyzing AFH October Volatility

You can NOW analyze AFH's October sales fluctuations with the backfilled data!

### Query the Data

**Via Google Sheets**:
1. Open spreadsheet: https://docs.google.com/spreadsheets/d/1Hovs50_nU3Ruo37F1vJsUmqCXmKxbHboPC2XWQOzw3Q/edit
2. Filter Daily Performance sheet:
   - Client = "Accessories for the Home"
   - Date >= "2025-10-01" AND Date <= "2025-10-31"
3. Create pivot table:
   - Rows: Date
   - Values: SUM(Clicks), SUM(Revenue), SUM(Cost)
   - Calculate: Clicks per £100 Revenue

**Via Python**:
```python
import pandas as pd

# Export Daily Performance sheet to CSV
df = pd.read_csv("daily_performance_export.csv")

# Filter for AFH in October
afh_oct = df[
    (df['Client'] == 'Accessories for the Home') &
    (df['Date'] >= '2025-10-01') &
    (df['Date'] <= '2025-10-31')
]

# Daily aggregates
daily = afh_oct.groupby('Date').agg({
    'Clicks': 'sum',
    'Revenue (£)': 'sum',
    'Cost (£)': 'sum'
}).reset_index()

daily['Clicks per £100 Revenue'] = daily['Clicks'] / daily['Revenue (£)'] * 100

print(daily)

# Identify best and worst days
best_day = daily.loc[daily['Clicks per £100 Revenue'].idxmin()]
worst_day = daily['Clicks per £100 Revenue'].idxmax()]

print(f"\nBest traffic efficiency: {best_day['Date']} ({best_day['Clicks per £100 Revenue']:.1f} clicks/£100)")
print(f"Worst traffic efficiency: {worst_day['Date']} ({worst_day['Clicks per £100 Revenue']:.1f} clicks/£100)")
```

## Documentation

- **[CAPACITY-MANAGEMENT.md](CAPACITY-MANAGEMENT.md)** - Complete capacity guide
- **[BACKFILL-GUIDE.md](BACKFILL-GUIDE.md)** - How to run backfill
- **[CONSOLIDATION-COMPLETE.md](CONSOLIDATION-COMPLETE.md)** - System architecture

## Summary

### What You Have Now

✅ **Historical data for 6 clients** (including AFH) - 90 days each
✅ **Automated daily accumulation** starting Nov 3
✅ **Capacity monitoring script** ready to deploy
✅ **Archive script** ready to free up space
✅ **Complete documentation** for maintenance

### What You Need to Do

🚨 **IMMEDIATE** (Today): Run archive script to free up 40% capacity
📅 **NEXT** (After archiving): Backfill remaining 9 clients (30 days)
🔄 **ONGOING** (Every 2 weeks): Run archival when alerted

### Your Question Answered

**"How can we ensure that in the future this won't hit the limit again?"**

**Answer**: Run the automated capacity checker daily (via LaunchAgent). It will alert you at 85% capacity (about 2 weeks before limit). When alerted, run the archive script to move old data to separate spreadsheets. This gives you unlimited capacity by maintaining a rolling window.

---

**Generated**: November 2, 2025
**Status**: At capacity limit, archival required to continue
**Primary Goal Achieved**: AFH October data available for analysis ✅
