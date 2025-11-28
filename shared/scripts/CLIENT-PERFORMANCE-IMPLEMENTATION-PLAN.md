# Client Performance Weekly Summary - Implementation Plan

## Overview
Add automated client performance insights to the weekly summary email with:
- One-sentence performance summary per client
- Week-over-week comparison
- Outlier detection (unusual spikes/drops on specific days)

## Phase 2 Architecture

### 1. Data Collection Script
**File**: `shared/scripts/fetch-weekly-performance-data.py`

**What it does**:
- Runs every Monday at 8:00 AM (30 min before weekly summary)
- Fetches Google Ads data for all active clients via MCP
- Queries last 7 days + previous 7 days for comparison
- Calculates:
  * Total revenue, cost, ROAS per client
  * Week-over-week % change
  * Day-by-day performance to identify outliers
  * Statistical outliers (days >2 standard deviations from mean)

**Output**: `shared/data/weekly-client-performance.json`

```json
{
  "generated_at": "2025-11-03T08:00:00Z",
  "period": {
    "current_week": {"start": "2025-10-27", "end": "2025-11-02"},
    "previous_week": {"start": "2025-10-20", "end": "2025-10-26"}
  },
  "clients": [
    {
      "name": "Bright Minds",
      "account_id": "1404868570",
      "current_week": {
        "revenue": 3732.33,
        "cost": 1235.03,
        "roas": 302,
        "conversions": 95
      },
      "previous_week": {
        "revenue": 3100.50,
        "cost": 1180.20,
        "roas": 263,
        "conversions": 82
      },
      "changes": {
        "revenue_pct": 20.4,
        "roas_pct": 14.8,
        "trend": "up"
      },
      "outliers": [
        {
          "date": "2025-11-01",
          "metric": "revenue",
          "value": 838.19,
          "deviation": "+156%",
          "note": "Significantly above week average of £326"
        },
        {
          "date": "2025-11-02",
          "metric": "revenue",
          "value": 939.86,
          "deviation": "+188%",
          "note": "Highest day of the week"
        }
      ],
      "summary": "↑ Revenue up 20% week-over-week (£3,732 vs £3,101). ROAS improved to 302%. Strong weekend performance (Nov 1-2) with revenue spike."
    }
  ]
}
```

### 2. Weekly Summary Integration
**File**: `shared/scripts/knowledge-base-weekly-summary.py`

**Changes needed**:
1. Add function to read `weekly-client-performance.json`
2. Add "Client Performance" section to Claude prompt
3. Include in email template with proper formatting

**New section in email** (after Week Ahead, before Industry News):
```html
<h2>📊 Client Performance - Last Week</h2>
<p>Week of Oct 27 - Nov 2 vs previous week</p>

<div class="client-performance">
  <div class="client-card positive">
    <h3>Bright Minds ↑</h3>
    <p class="summary">Revenue up 20% week-over-week (£3,732 vs £3,101). ROAS improved to 302%.</p>
    <div class="metrics">
      <span class="metric">Revenue: £3,732 (+20%)</span>
      <span class="metric">ROAS: 302% (+15%)</span>
    </div>
    <div class="outliers">
      <span class="outlier">⚡ Nov 1-2: Strong weekend with £838 and £940 revenue (2x week average)</span>
    </div>
  </div>

  <!-- More clients... -->
</div>
```

### 3. LaunchAgent Setup
**File**: `~/Library/LaunchAgents/com.petesbrain.fetch-client-performance.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.petesbrain.fetch-client-performance</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/administrator/Documents/PetesBrain/shared/scripts/fetch-weekly-performance-data.py</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/Users/administrator/.petesbrain-fetch-performance.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/administrator/.petesbrain-fetch-performance.log</string>

    <key>WorkingDirectory</key>
    <string>/Users/administrator/Documents/PetesBrain</string>
</dict>
</plist>
```

## Implementation Steps

1. **Create data fetching script** with MCP integration
2. **Test script manually** to verify data collection
3. **Update weekly summary** to read and include performance data
4. **Create LaunchAgent** to run script before weekly summary
5. **Test full workflow** end-to-end

## MCP Integration Challenge

**Problem**: Python scripts can't directly call MCP tools (those are only available to Claude Code)

**Solutions**:
1. **Option A**: Create a wrapper that uses `claude` CLI if available
2. **Option B**: Use Google Ads API directly in Python (requires google-ads library)
3. **Option C**: Pre-generate performance data manually via Claude Code each week
4. **Option D**: Build MCP client in Python (complex)

**Recommended**: **Option B** - Use google-ads library directly in Python
- Most reliable and maintainable
- No dependency on Claude Code being available
- Can run in LaunchAgent without issues
- Credentials already available in MCP server directory

## Next Steps

Would you like me to:
1. Implement Option B (Google Ads API in Python) now?
2. Or create a simpler Phase 1.5 that just references the Product Impact Analyzer for now?
