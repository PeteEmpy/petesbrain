# Product Impact Analyzer - Architecture Documentation

## Overview

The Product Impact Analyzer correlates product feed changes with Google Ads Shopping performance to identify what changes helped or hurt business metrics.

**Phase 1**: Claude-assisted (original implementation)
**Phase 2**: Standalone automation (deployed)
**Phase 3**: Merchant Center integration (deployed October 2025)

## New: Merchant Center Disapproval Tracking (Phase 3)

**Added**: October 30, 2025

The Product Impact Analyzer now tracks Google Merchant Center product approval status and disapproval reasons, providing complete visibility into why products disappear from your feeds.

**Key capabilities**:
- Real-time product status tracking across all clients
- Immediate alerts for newly disapproved products
- Detailed disapproval reasons and resolution guidance
- Integration with existing product monitoring system

**Documentation**: See **`MERCHANT-CENTER-TRACKING.md`** for complete details.

**Quick setup**:
```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
./setup_disapproval_monitoring.sh
```

## Architecture - Phase 1 (Claude-Assisted)

### Workflow

```
User asks: "Run the product impact analysis"
                    ↓
         Claude fetches data via MCP
                    ↓
    ┌──────────────┴───────────────┐
    │                              │
    ▼                              ▼
Google Sheets              Google Ads API
(Outliers Report)          (Shopping Performance)
    │                              │
    └──────────────┬───────────────┘
                   ↓
        Save to JSON files in data/
                   ↓
    Python analyzer.py processes data
                   ↓
        Calculate impact metrics
                   ↓
    ┌──────────────┴───────────────┐
    │                              │
    ▼                              ▼
JSON output/                Text summary
impact_analysis.json        (shown to user)
    │
    ▼
Claude writes to
Google Sheets
(Impact Analysis tab)
```

### Data Flow

**Input 1: Product Changes** (from Google Sheets)
```
Outliers Report → Read via MCP → Save to data/outliers_report.json
Format: [["Client", "Product ID", "Change Type", "Date", "Title", "Days", "Flag"], ...]
```

**Input 2: Performance Data** (from Google Ads)
```
For each enabled client:
  Google Ads API → GAQL query → Save to data/ads_{client_name}.json
  Query: Shopping performance by product, last 30 days
  Format: [{"segments": {}, "metrics": {}}, ...]
```

**Processing**:
```python
1. Parse product changes from Outliers Report
2. For each change:
   - Calculate before window: change_date - 7 days to change_date - 1
   - Calculate after window: change_date to change_date + 7 days
   - Aggregate Google Ads metrics for product in each window
   - Calculate impact: after vs before
3. Generate analysis with impact flags
```

**Output**:
```
JSON: output/impact_analysis.json (for Sheets upload)
Text: output/summary.txt (for user review)
```

## Key Components

### analyzer.py

**Core Classes**:
- `ProductChange`: Represents a single product change from Sheets
- `PerformanceMetrics`: Aggregated metrics (impressions, clicks, conversions, revenue, cost)
- `ImpactAnalysis`: Correlates change with before/after performance

**Core Functions**:
- `normalize_product_id()`: Handles ID format differences (287 vs 00287)
- `parse_product_changes()`: Extracts changes from Sheets data
- `aggregate_performance_by_product()`: Sums metrics by product/date range
- `analyze_impact()`: Main correlation engine
- `generate_text_summary()`: Creates human-readable report

### config.json

**Structure**:
```json
{
  "spreadsheet_id": "...",
  "outliers_sheet_name": "Outliers Report",
  "output_sheet_name": "Impact Analysis",

  "analysis_settings": {
    "comparison_window_days": 7,
    "min_clicks_threshold": 10,
    "significance_threshold_percent": 20
  },

  "clients": [
    {
      "name": "Tree2mydoor",
      "merchant_id": "107469209",
      "google_ads_customer_id": "4941701449",
      "enabled": true
    }
  ]
}
```

## Product ID Matching

**Challenge**: Different systems use different ID formats
- Google Sheets: `287`, `3539`, `FCB7007`
- Google Ads: `00287`, `03539`, `FCB7007`

**Solution**: `normalize_product_id()` strips leading zeros for comparison
```python
normalize_product_id("00287") → "287"
normalize_product_id("287") → "287"
normalize_product_id("FCB7007") → "FCB7007"
```

## Impact Calculation Logic

### Before/After Windows

For a change on `2025-10-26` with 7-day window:
```
Before: 2025-10-19 to 2025-10-25 (7 days)
After:  2025-10-26 to 2025-11-02 (7 days)
```

### Metrics Aggregated

For each window:
- **Impressions**: Total ad views
- **Clicks**: Total clicks
- **Conversions**: Total purchases
- **Revenue**: Total conversion value (£)
- **Cost**: Total ad spend (£)

Derived metrics:
- **CTR**: clicks / impressions * 100
- **CPC**: cost / clicks
- **Conversion Rate**: conversions / clicks * 100
- **ROAS**: revenue / cost

### Impact Flags

Based on revenue change:
- `📈` Strong positive: +£100 or more
- `🟢` Positive: +£0 to +£100
- `⚪` Minimal: -£10 to +£10
- `🟠` Negative: -£100 to £0
- `📉` Strong negative: -£100 or less

## Tuesday Reminder System

**Components**:
- `setup_reminder.sh`: One-time setup script
- `send_reminder.sh`: Email sending script
- `~/Library/LaunchAgents/com.roksystems.product-impact-analyzer.reminder.plist`: launchd scheduler

**Schedule**: Every Tuesday at 9:00 AM

**Email content**: Simple reminder to ask Claude: "Run the product impact analysis"

## Running the Analysis (Phase 1)

### User's Perspective

```
User: "Run the product impact analysis"
    ↓
Claude: [Fetches data, runs analyzer, shows summary]
    ↓
User: Reviews summary and detailed Sheets report
```

### Claude's Execution Steps

1. **Fetch Outliers Report**:
```python
mcp__google-sheets__read_cells(
    spreadsheet_id="...",
    range_name="Outliers Report!A1:G5000"
)
# Save to data/outliers_report.json
```

2. **Fetch Google Ads Data** (for each client):
```python
mcp__google-ads__run_gaql(
    customer_id="4941701449",
    query="SELECT segments.product_item_id, segments.date, metrics.* FROM shopping_performance_view WHERE segments.date >= '2025-10-01'"
)
# Save to data/ads_tree2mydoor.json
```

3. **Run Analyzer**:
```bash
cd tools/product-impact-analyzer
python3 analyzer.py
# Outputs to output/impact_analysis.json and output/summary.txt
```

4. **Show Summary** to user

5. **Write to Sheets** (optional):
```python
# Read output/impact_analysis.json
# Format for Sheets
mcp__google-sheets__write_cells(
    spreadsheet_id="...",
    range_name="Impact Analysis!A1",
    values=[...formatted data...]
)
```

## Error Handling

### Common Issues

**No ads data for client**:
- Check: Client enabled in config.json
- Check: google_ads_customer_id correct
- Check: Client has Shopping campaigns

**Product ID mismatch**:
- Normalized IDs handle leading zeros
- If still failing, check Merchant Center feed format

**No significant impacts**:
- Changes may be too old (>comparison window)
- Products may have low traffic (<10 clicks threshold)
- Changes may genuinely have minimal impact

### Debugging

**Check data files**:
```bash
cat data/outliers_report.json | python3 -m json.tool
cat data/ads_tree2mydoor.json | python3 -m json.tool
```

**Check output**:
```bash
cat output/summary.txt
cat output/impact_analysis.json | python3 -m json.tool
```

**Verbose run**:
```bash
python3 analyzer.py 2>&1 | tee debug.log
```

## Phase 2 Architecture (Future)

### Planned Enhancements

**Standalone Execution**:
- Direct Google Sheets API integration (no MCP dependency)
- Direct Google Ads API integration (no MCP dependency)
- Scheduled via cron or cloud function

**Automated Reporting**:
- Email HTML reports automatically
- Weekly trends analysis
- Month-over-month comparison

**Advanced Analytics**:
- Statistical significance testing
- Confidence intervals
- Seasonality adjustment
- ML-powered anomaly detection

**Alerts**:
- Slack/email notifications for critical changes
- Threshold-based triggering
- Client-specific alert rules

### Migration Path

Phase 1 → Phase 2:
1. Set up Google Cloud Project
2. Enable Sheets API and Ads API
3. Create service account credentials
4. Update analyzer.py to use google-api-python-client
5. Deploy to cloud (Cloud Run, Lambda, etc.)
6. Configure scheduling

## Testing

### Unit Tests (TODO)

```bash
python3 -m pytest tests/
```

### Integration Test (Current)

```bash
# With sample data in data/
python3 analyzer.py
```

Expected output:
- Successful parsing of changes
- Performance aggregation
- Impact calculation
- Report generation

## Performance Considerations

**Data Volume**:
- Outliers Report: ~10K rows (manageable)
- Google Ads data: ~100K rows per client per month (filter by date/clicks)

**API Limits**:
- Google Ads API: 10K requests/day (sufficient)
- Google Sheets API: 60 requests/minute (sufficient)

**Execution Time**:
- Fetch data: 30-60 seconds
- Process: 5-10 seconds
- Total: ~1-2 minutes per run

## Security

**Credentials**:
- Phase 1: MCP handles authentication (user's Google account)
- Phase 2: Service account JSON key (store securely)

**Data Privacy**:
- All data stays local (data/ and output/ directories)
- No external services (except Google APIs)
- Git ignore data/ and output/ directories

## Maintenance

**Weekly**:
- Run analysis on Tuesday
- Review output
- Share insights with clients

**Monthly**:
- Review config.json for new clients
- Check for product ID format changes
- Update thresholds if needed

**Quarterly**:
- Review Phase 2 migration readiness
- Update documentation
- Optimize query performance

## Files Overview

```
tools/product-impact-analyzer/
├── analyzer.py                           # Main analysis script
├── snapshot_product_feed.py              # Product feed snapshot system
├── run_snapshot_via_claude.py            # Claude helper for snapshots
├── monitor.py                            # Real-time monitoring & alerts
├── merchant_center_tracker.py            # Merchant Center API integration (Phase 3)
├── disapproval_monitor.py                # Disapproval detection & alerts (Phase 3)
├── run_automated_analysis.py             # Phase 2 automation entry point
├── trend_analyzer.py                     # Trend analysis over time
├── fetch_data.py                         # Data fetching helper
├── calculate_thresholds.py               # Per-client threshold calculator
├── config.json                           # Configuration
├── requirements.txt                      # Python dependencies
├── README.md                             # User-facing documentation
├── QUICKSTART.md                         # Getting started guide
├── TOOL_CLAUDE.md                        # This file - architecture notes
├── SNAPSHOT_SYSTEM.md                    # Product snapshot system docs
├── PHASE2.md                             # Phase 2 automation docs
├── MONITORING.md                         # Real-time monitoring docs
├── MERCHANT-CENTER-TRACKING.md           # Merchant Center integration docs (Phase 3)
├── PER-CLIENT-THRESHOLDS.md              # Per-client threshold documentation
├── ADDING-CLIENTS.md                     # How to add new clients
├── CLEAR-PROSPECTS-SETUP.md              # Multi-brand client setup example
├── setup_automation.sh                   # Phase 2 automation setup
├── setup_monitoring.sh                   # Real-time monitoring setup
├── setup_disapproval_monitoring.sh       # Merchant Center monitoring setup (Phase 3)
├── setup_daily_snapshot.sh               # Daily snapshot setup
├── setup_reminder.sh                     # Tuesday reminder setup
├── data/                                 # Input JSON files (gitignored)
│   ├── outliers_report.json
│   ├── ads_{client}.json
│   ├── snapshot_cache_{customer_id}.json
│   ├── snapshot_{client}_{date}.json
│   ├── previous_snapshot_{client}.json
│   ├── price_changes.json
│   └── merchant_center_snapshot.json     # Merchant Center data (Phase 3)
├── monitoring/                           # Monitoring snapshots (Phase 2/3)
│   ├── snapshot_{client}_{date}.json     # Product snapshots
│   ├── disapprovals_current.json         # Current disapproval status (Phase 3)
│   └── disapprovals_previous.json        # Previous disapproval status (Phase 3)
├── history/                              # Historical analyses
│   └── analysis_YYYY-MM-DD.json
└── output/                               # Analysis results (gitignored)
    ├── impact_analysis.json
    ├── summary.txt
    └── report_YYYY-MM-DD.html
```

## Contributing

When modifying the analyzer:
1. Test with sample data first
2. Verify product ID matching works
3. Check impact calculations are correct
4. Update this documentation
5. Commit with message: `[product-impact-analyzer]: description`

## Product Feed Snapshot System (NEW)

### Overview

**Added:** October 2025

The Product Feed Snapshot System tracks product-level changes (price, availability, title) over time and correlates them with Google Ads performance.

**Key enhancement:** Now you can see **WHY** a product's performance changed:
- Price drop → Click spike
- Product removed → Revenue drop
- New product → Learning phase impact

See **`SNAPSHOT_SYSTEM.md`** for complete documentation.

### Quick Reference

**Run snapshot via Claude Code:**
```
User: "Run the product feed snapshot"

Claude workflow:
1. Fetch product data via mcp__google-ads__run_gaql for each client
2. Cache results locally
3. Run: python3 snapshot_product_feed.py
4. Write results to Google Sheets
```

**New data files:**
- `snapshot_cache_{customer_id}.json` - Cached API results
- `snapshot_{client}_{date}.json` - Daily snapshot
- `previous_snapshot_{client}.json` - For comparison
- `price_changes.json` - Detected changes

**New Google Sheets tabs:**
- "Product Feed History" - Daily product snapshots
- "Price Change Log" - Detected changes
- "Outliers Report" (enhanced) - Now includes Old Price, New Price, Price Change %

**Key capabilities:**
- Detect product removals/additions
- Track price changes with percentage
- Correlate changes with performance impact
- Historical tracking for trend analysis

**Example insights:**
- "Product 01090 price dropped 16% → clicks increased 1,900%"
- "98 products removed Oct 26 → revenue -£500/week"
- "New product added → 50x click increase after learning phase"

**Automation:** Setup daily snapshots via LaunchAgent:
```bash
cd tools/product-impact-analyzer
./setup_daily_snapshot.sh
```
Runs daily at 6 AM (requires MCP integration for Phase 2)

## Support

Questions? Ask Claude:
- "How does the impact analyzer work?"
- "Why isn't product X showing up?"
- "Can you explain this metric?"
- "Run the product feed snapshot" (NEW)
- "Why did this product's performance change?" (NEW)
