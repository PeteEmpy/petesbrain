# Weekly Client Performance System

## Overview
Automated weekly performance tracking for all ROK clients with trend analysis, outlier detection, and integration into the weekly summary email.

**Status**: ✅ Active, Production-ready (deployed Nov 3, 2025)

## System Architecture

### Two-Stage Process

**Stage 1: Data Fetching (Monday 8:00 AM)**
- Script: `shared/scripts/fetch-weekly-client-performance.py`
- Fetches last 7 days vs previous 7 days for all 12 clients
- Calculates week-over-week changes
- Detects statistical outliers (>1.5 standard deviations)
- Generates one-sentence summaries per client
- Outputs: `shared/data/weekly-client-performance.json`

**Stage 2: Weekly Summary Integration (Monday 8:30 AM)**
- Script: `shared/scripts/knowledge-base-weekly-summary.py`
- Reads performance JSON
- Includes in email as 2nd section (after Week Ahead)
- Groups clients by trend (Up/Stable/Down)
- Highlights outlier days

## What It Tracks

### Metrics Per Client
- **Revenue**: Total conversions value
- **Cost**: Total spend
- **ROAS**: Return on ad spend (expressed as percentage: 400%, not £4.00)
- **Conversions**: Total conversion count
- **Clicks**: Total clicks
- **Impressions**: Total impressions

### Analysis
- **Week-over-week comparison**: Current 7 days vs previous 7 days
- **Trend classification**: Up (>5% revenue increase), Down (>5% decrease), Stable
- **Outlier detection**: Days with revenue >1.5 standard deviations from weekly mean
- **Summary generation**: One-sentence performance summary per client

## Files

### Scripts
- **`shared/scripts/fetch-weekly-client-performance.py`** - Data fetching (237 lines)
  - Uses Google Ads Python library directly (no MCP dependency)
  - Processes all 12 clients in sequence
  - Statistical analysis for outliers
  - JSON output generation

- **`shared/scripts/knowledge-base-weekly-summary.py`** - Email generation
  - Function `get_client_performance()` reads JSON
  - Formats performance data for Claude prompt
  - Includes in email as prominent 2nd section

### Data
- **`shared/data/weekly-client-performance.json`** - Weekly output
  - Generated at timestamp
  - Period dates (current/previous weeks)
  - All 12 clients sorted by revenue (highest first)
  - Per-client: metrics, changes, outliers, summary

### Configuration
- **`~/Library/LaunchAgents/com.petesbrain.fetch-client-performance.plist`**
  - Runs Mondays 8:00 AM
  - Logs to `~/.petesbrain-fetch-performance.log`

- **`~/Library/LaunchAgents/com.petesbrain.kb-weekly-summary.plist`**
  - Runs Mondays 8:30 AM (30 min after data fetch)
  - Logs to `~/.petesbrain-kb-weekly-summary.log`

## Active Clients

All 12 ROK clients (same list as daily anomaly detection):
1. Bright Minds - 1404868570
2. Tree2mydoor - 4941701449
3. National Design Academy - 1994728449
4. Accessories for the Home - 7972994730
5. Devonshire Hotels - 5898250490
6. Go Glean - 8492163737
7. Godshot - 9922220205
8. Grain Guard - 4391940141
9. Just Bin Bags - 9697059148
10. Smythson UK - 8573235780
11. Superspace - 7482100090
12. Uno Lighting - 6413338364

## Weekly Email Format

**Subject**: `📅 Weekly Summary & Week Ahead - [Date Range]`

**Performance Section** (2nd after Week Ahead):
```
📊 Client Performance - Last Week

Week of Oct 27 - Nov 2 vs previous week

Strong Performers (↑):
• Bright Minds: Revenue up 63% (£3,733 vs £2,285). ROAS improved to 302%.
• Superspace: Revenue up 20% (£207,202 vs £171,618). ROAS improved to 877%.
• Uno Lighting: Revenue up 21% (£12,019 vs £9,890). ROAS improved to 201%.

Stable Performers (→):
• Accessories for the Home: Stable performance (£13,600 revenue, 203% ROAS).
  Notable: Oct 31 performance spike.
• Godshot: Stable performance (£5,148 revenue, 1116% ROAS).
• Go Glean: Stable performance (£1,321 revenue, 271% ROAS).

Needs Attention (↓):
• Smythson UK: Revenue down 41% (£25,465 vs £43,483). ROAS declined to 366%.
  Notable: Nov 2 performance spike.
• National Design Academy: Revenue down 65% (£969 vs £2,820). ROAS declined to 12%.
  Notable: Oct 27 performance spike.
• Devonshire Hotels: Revenue down 34% (£8,956 vs £13,717). ROAS declined to 239%.
```

## JSON Output Structure

```json
{
  "generated_at": "2025-11-03T10:11:23.559530",
  "period": {
    "current_week": {"start": "2025-10-27", "end": "2025-11-02"},
    "previous_week": {"start": "2025-10-20", "end": "2025-10-26"}
  },
  "clients": [
    {
      "name": "Superspace",
      "current_week": {
        "revenue": 207202.69,
        "cost": 23609.14,
        "roas": 878.0,
        "conversions": 626.1
      },
      "previous_week": {
        "revenue": 171618.84,
        "cost": 25432.69,
        "roas": 675.0,
        "conversions": 530.7
      },
      "changes": {
        "revenue_pct": 20.7,
        "roas_pct": 30.1,
        "trend": "up"
      },
      "outliers": [
        {
          "date": "2025-10-27",
          "metric": "revenue",
          "value": 22246.71,
          "deviation": "-24%",
          "note": "Below week average of £29600"
        }
      ],
      "summary": "↑ Revenue up 20% week-over-week (£207202 vs £171618). ROAS improved to 877%."
    }
  ]
}
```

## Running Manually

**Fetch Performance Data:**
```bash
GOOGLE_ADS_CONFIGURATION_FILE_PATH=/Users/administrator/google-ads.yaml \
/Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3 \
/Users/administrator/Documents/PetesBrain/shared/scripts/fetch-weekly-client-performance.py
```

**Generate Weekly Summary:**
```bash
ANTHROPIC_API_KEY="[your-key]" \
/Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3 \
/Users/administrator/Documents/PetesBrain/shared/scripts/knowledge-base-weekly-summary.py
```

**Run Both in Sequence:**
```bash
# Step 1: Fetch data
GOOGLE_ADS_CONFIGURATION_FILE_PATH=/Users/administrator/google-ads.yaml \
shared/email-sync/.venv/bin/python3 shared/scripts/fetch-weekly-client-performance.py

# Step 2: Generate summary (includes performance data)
ANTHROPIC_API_KEY="[your-key]" \
shared/email-sync/.venv/bin/python3 shared/scripts/knowledge-base-weekly-summary.py
```

## Monitoring

**Check LaunchAgents:**
```bash
launchctl list | grep -E "(fetch-client-performance|kb-weekly-summary)"
```

**View Logs:**
```bash
# Performance fetching
tail -50 ~/.petesbrain-fetch-performance.log

# Weekly summary
tail -50 ~/.petesbrain-kb-weekly-summary.log
```

**Check Output:**
```bash
cat shared/data/weekly-client-performance.json | jq '.clients[] | {name, trend: .changes.trend, revenue_change: .changes.revenue_pct}'
```

## Outlier Detection Logic

Uses statistical analysis to identify unusual performance days:

```python
# Calculate mean and standard deviation for the week
revenues = [day1, day2, day3, day4, day5, day6, day7]
avg_revenue = mean(revenues)
std_revenue = stdev(revenues)

# Flag days >1.5 standard deviations from mean
for day in revenues:
    z_score = (day - avg_revenue) / std_revenue
    if abs(z_score) > 1.5:
        # This is an outlier
```

**Example**:
- Week average: £3,637/day
- Nov 2: £1,076 (-70% deviation)
- Z-score: -2.8 (outlier)

## Integration Points

### Knowledge Base Weekly Summary
- Performance data loaded in `main()` function
- Function: `get_client_performance()` reads JSON
- Added to Claude prompt for summarization
- Formatted as 2nd email section (after Week Ahead)

### Daily Anomaly Detection
- Complements weekly trends with daily monitoring
- Uses same Google Ads API credentials
- Same client list for consistency
- Daily focuses on immediate issues, weekly on trends

### Client CONTEXT.md Files
- Weekly performance insights should be manually added to client CONTEXT.md as needed
- Update "Strategic Context" or "Campaign Notes" sections with significant changes
- Document cause of major shifts (experiments, external factors, etc.)

## Troubleshooting

### No Performance Data in Email
1. Check if JSON exists: `ls -lh shared/data/weekly-client-performance.json`
2. Verify timing: Fetch at 8:00 AM, summary at 8:30 AM
3. Check fetch logs for errors
4. Run fetch script manually

### Incorrect Trends
- Review baseline calculation (7 days vs 7 days)
- Check for data gaps in Google Ads API response
- Verify date ranges in JSON output

### Missing Clients
- Verify client in `ACTIVE_CLIENTS` dict
- Check Google Ads API access
- Review fetch logs for specific errors

## Implementation History

**Nov 3, 2025**: Initial deployment
- Google Ads Python library integration
- 12 active clients configured
- Week-over-week analysis with trends
- Statistical outlier detection
- Integration with weekly summary email
- Automated Monday morning schedule

**Test Results** (Nov 3, 2025):
- All 12 clients processed successfully
- Performance data included in weekly email
- Detected multiple outliers (Smythson -70%, NDA -65%, etc.)
- Email formatting working correctly
- Complete workflow tested end-to-end

## Future Enhancements

Potential improvements discussed:
- Client-specific thresholds for outlier detection
- Multi-week trend analysis (4-week rolling average)
- Seasonality adjustments (compare to same week last year)
- Budget pacing alerts (spend vs monthly budget)
- Per-campaign breakdowns for large accounts
