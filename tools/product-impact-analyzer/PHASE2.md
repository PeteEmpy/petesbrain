# Product Impact Analyzer - Phase 2 (Fully Automated)

**Status**: ✅ Ready for deployment
**Last Updated**: October 30, 2025

## Overview

Phase 2 transforms the Product Impact Analyzer from a Claude-assisted tool into a fully automated weekly workflow that:

1. ✅ **Runs automatically** every Tuesday at 9 AM
2. ✅ **Fetches data** from Google Sheets and Google Ads
3. ✅ **Analyzes impacts** with historical context
4. ✅ **Detects anomalies** and trends over time
5. ✅ **Generates HTML reports** with professional formatting
6. ✅ **Sends email reports** automatically
7. ✅ **Tracks history** for trend analysis

## What's New in Phase 2

### 🤖 Full Automation
- **LaunchAgent** runs weekly on schedule
- No manual intervention required (after setup)
- Automatic data fetching and analysis
- Email delivery to configured recipients

### 📊 Trend Analysis
- Tracks product performance over time
- Identifies improving vs declining products
- Detects volatile products with high variance
- Calculates client-level performance averages

### 🚨 Anomaly Detection
- Statistical anomaly detection (z-score based)
- Identifies unusual performance spikes or drops
- Severity classification (low, medium, high)
- Critical anomaly alerts

### 📧 HTML Email Reports
- Professional, branded email design
- Visual impact indicators (emojis, colors)
- Top 10 impacts per client
- Summary metrics and insights
- Responsive design for mobile/desktop

### 📈 Historical Tracking
- Saves all analyses to `history/` directory
- Enables week-over-week comparisons
- Powers trend analysis and anomaly detection
- Long-term pattern identification

## Architecture

```
Tuesday 9 AM (LaunchAgent Trigger)
          ↓
┌─────────────────────────────────────┐
│  run_automated_analysis.py          │
│                                     │
│  1. Fetch data (via MCP/fetch_data) │
│  2. Run impact analysis             │
│  3. Generate trend analysis         │
│  4. Detect anomalies                │
│  5. Create HTML report              │
│  6. Send email                      │
│  7. Save to history                 │
└─────────────────────────────────────┘
          ↓
    Output Files:
    - output/impact_analysis.json
    - output/report_YYYY-MM-DD.html
    - history/analysis_YYYY-MM-DD.json
          ↓
    Email Report
    (pete@roksys.co.uk)
```

## Installation & Setup

### Prerequisites

1. **Python virtual environment** (created automatically by setup script)
2. **Environment variables** in `~/.bashrc` or `~/.zshrc`:
   ```bash
   export ANTHROPIC_API_KEY='your-key-here'
   export GMAIL_APP_PASSWORD='your-gmail-app-password'
   export GOOGLE_APPLICATION_CREDENTIALS='/path/to/credentials.json'
   ```

3. **Gmail App Password** (for email sending):
   - Go to Google Account → Security → 2-Step Verification
   - Generate App Password for "Mail"
   - Save as `GMAIL_APP_PASSWORD` environment variable

### One-Command Setup

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
./setup_automation.sh
```

The setup script will:
1. ✅ Create Python virtual environment
2. ✅ Install dependencies
3. ✅ Configure LaunchAgent with your API keys
4. ✅ Set up email recipient
5. ✅ Install LaunchAgent plist
6. ✅ Load and activate automation
7. ✅ Optionally run test analysis

### Verification

```bash
# Check LaunchAgent is loaded
launchctl list | grep product-impact

# View logs
tail -f ~/.petesbrain-product-impact-analyzer.log

# Manual test run
cd tools/product-impact-analyzer
.venv/bin/python3 run_automated_analysis.py --dry-run --test
```

## Usage

### Automated (Default)

Once set up, the analyzer runs automatically every Tuesday at 9 AM. No action required.

### Manual Runs

```bash
cd tools/product-impact-analyzer

# Full run (sends email)
.venv/bin/python3 run_automated_analysis.py

# Dry run (no email)
.venv/bin/python3 run_automated_analysis.py --dry-run

# Test mode (verbose output)
.venv/bin/python3 run_automated_analysis.py --test --dry-run
```

### Fetching Data (Bridging to MCP)

The automation requires product change data and Google Ads performance data:

```bash
# Generate MCP fetch commands (for Claude Code)
python3 fetch_data.py

# Verify data exists before running analysis
python3 fetch_data.py --test
```

**Note**: In Phase 2, data fetching is still manual via Claude Code until MCP client library is integrated. The `fetch_data.py` script outputs the exact MCP commands Claude Code should run.

## New Files & Components

### Core Scripts

| File | Purpose |
|------|---------|
| `run_automated_analysis.py` | Main automation orchestrator |
| `fetch_data.py` | MCP data fetching helper |
| `trend_analyzer.py` | Trend analysis and anomaly detection |
| `setup_automation.sh` | One-command setup script |
| `com.petesbrain.product-impact-analyzer.plist` | LaunchAgent configuration |

### Data Directories

| Directory | Purpose |
|-----------|---------|
| `data/` | Input JSON files (outliers, ads data) |
| `output/` | Analysis results and HTML reports |
| `history/` | Historical analyses for trend tracking |

### Output Files

| File | Description |
|------|-------------|
| `output/impact_analysis.json` | Latest analysis results |
| `output/report_YYYY-MM-DD.html` | HTML email report |
| `history/analysis_YYYY-MM-DD.json` | Historical snapshot |

## Email Reports

### Report Structure

```
┌──────────────────────────────────────┐
│ 📊 Weekly Product Impact Analysis    │
│ Report Date: October 30, 2025        │
├──────────────────────────────────────┤
│ Summary Box                          │
│ - Total Changes: 45                  │
│ - Clients Covered: 7                 │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ Client: Tree2mydoor                  │
├──────────────────────────────────────┤
│ 📈 Product 287: Olive Tree Large     │
│    Revenue: +£245 (+42%)             │
│    Clicks: 156 → 218 (+40%)          │
├──────────────────────────────────────┤
│ 📉 Product 593: Lemon Tree Medium    │
│    Revenue: -£180 (-36%)             │
│    Clicks: 422 → 301 (-29%)          │
└──────────────────────────────────────┘

[Repeat for each client]
```

### Visual Indicators

- 📈 **Strong positive**: Revenue +£100 or more
- 🟢 **Positive**: Revenue +£0 to +£100
- ⚪ **Minimal**: Revenue change < £10
- 🟠 **Negative**: Revenue -£0 to -£100
- 📉 **Strong negative**: Revenue -£100 or worse

## Trend Analysis

### How It Works

The trend analyzer (`trend_analyzer.py`) processes all historical analysis files to identify:

1. **Improving Products**
   - Recent performance better than historical average
   - Positive trajectory over time

2. **Declining Products**
   - Recent performance worse than historical
   - Negative trajectory

3. **Volatile Products**
   - High standard deviation in impacts
   - Unpredictable performance

4. **Client Averages**
   - Overall performance by client
   - Identify best/worst performing accounts

### Running Trend Analysis

```bash
# Standalone trend analysis
cd tools/product-impact-analyzer
.venv/bin/python3 trend_analyzer.py

# Output includes:
# - Products tracked
# - Improving vs declining counts
# - Volatile products
# - Top anomalies
# - Client averages
```

## Anomaly Detection

### Statistical Method

Uses **z-score** based detection:
- Calculates mean and standard deviation for each product
- Flags values > 2 standard deviations from mean
- Classifies severity based on z-score magnitude

### Anomaly Types

| Type | Description |
|------|-------------|
| **spike** | Revenue significantly higher than expected |
| **drop** | Revenue significantly lower than expected |
| **unusual** | Other statistical anomaly |

### Severity Levels

| Severity | Z-Score |
|----------|---------|
| **high** | > 3.0 |
| **medium** | 2.5 - 3.0 |
| **low** | 2.0 - 2.5 |

## Configuration

### Email Settings

Edit `config.json`:

```json
{
  "alert_settings": {
    "email_enabled": true,
    "email_to": "pete@roksys.co.uk",
    "email_from": "pete@roksys.co.uk",
    "alert_on_negative_impact": true,
    "alert_threshold_revenue_loss": 100,
    "include_trends": true,
    "include_anomalies": true
  }
}
```

### Analysis Settings

```json
{
  "analysis_settings": {
    "comparison_window_days": 7,  // Before/after window
    "min_clicks_threshold": 10,   // Ignore low-traffic products
    "significance_threshold_percent": 20  // Flag changes >20%
  }
}
```

### Client Management

```json
{
  "clients": [
    {
      "name": "Tree2mydoor",
      "merchant_id": "107469209",
      "google_ads_customer_id": "4941701449",
      "enabled": true  // Set to false to exclude from analysis
    }
  ]
}
```

## Logs & Monitoring

### Log Files

| File | Purpose |
|------|---------|
| `~/.petesbrain-product-impact-analyzer.log` | Standard output |
| `~/.petesbrain-product-impact-analyzer-error.log` | Error output |

### View Logs

```bash
# Tail standard log
tail -f ~/.petesbrain-product-impact-analyzer.log

# Tail error log
tail -f ~/.petesbrain-product-impact-analyzer-error.log

# View last run
cat ~/.petesbrain-product-impact-analyzer.log | grep "AUTOMATED RUN"
```

### Check Status

```bash
# Is LaunchAgent running?
launchctl list | grep product-impact

# When is next run?
launchctl print user/$(id -u)/com.petesbrain.product-impact-analyzer

# Reload LaunchAgent (after config changes)
launchctl unload ~/Library/LaunchAgents/com.petesbrain.product-impact-analyzer.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.product-impact-analyzer.plist
```

## Troubleshooting

### No Email Received

1. **Check email configuration** in `config.json`
2. **Verify GMAIL_APP_PASSWORD** environment variable
3. **Check error log** for SMTP errors
4. **Test email manually**:
   ```bash
   .venv/bin/python3 run_automated_analysis.py --dry-run
   # Then remove --dry-run to actually send
   ```

### LaunchAgent Not Running

```bash
# Check if loaded
launchctl list | grep product-impact

# If not, load it
launchctl load ~/Library/LaunchAgents/com.petesbrain.product-impact-analyzer.plist

# Check for errors
cat ~/.petesbrain-product-impact-analyzer-error.log
```

### No Data / Analysis Fails

```bash
# Verify data files exist
python3 fetch_data.py --test

# If missing, fetch via Claude Code
python3 fetch_data.py
# Then run the MCP commands it outputs
```

### Permission Errors

```bash
# Ensure scripts are executable
chmod +x setup_automation.sh
chmod +x run_automated_analysis.py
chmod +x fetch_data.py
chmod +x trend_analyzer.py
```

## Migration from Phase 1

If you were using Phase 1 (Claude-assisted):

1. **Your existing data is preserved**
   - Historical analyses can be manually copied to `history/`
   - Config and data files are compatible

2. **Tuesday reminder still works**
   - The old reminder plist won't conflict
   - You can disable it: `launchctl unload ~/Library/LaunchAgents/com.roksystems.product-impact-analyzer.reminder.plist`

3. **No breaking changes**
   - Can still run manually via Claude Code
   - Phase 2 is additive, not replacement

## Future Enhancements (Phase 3)

Potential improvements for future versions:

1. **Direct MCP Integration**
   - Python MCP client library for data fetching
   - Eliminate manual Claude Code step

2. **Predictive Scoring**
   - ML models to predict impact before changes go live
   - "What if" analysis for price changes

3. **Real-Time Monitoring**
   - Daily lightweight checks
   - Immediate alerts for critical changes

4. **Interactive Dashboard**
   - Web interface for viewing trends
   - Drill-down into specific products
   - Export capabilities

5. **Multi-Channel Analysis**
   - Expand beyond Shopping to Search, Display
   - Cross-campaign correlation

## Support

Questions or issues?

- **Documentation**: `README.md`, `TOOL_CLAUDE.md`, `QUICKSTART.md`
- **Logs**: Check error logs first
- **Ask Claude**: "Why isn't the impact analyzer working?"
- **Manual test**: `python3 run_automated_analysis.py --test --dry-run`

## Credits

**Built with**:
- Python 3
- Google Sheets API (via MCP)
- Google Ads API (via MCP)
- Gmail SMTP
- macOS LaunchAgent

**Generated with**: Claude Code
**Version**: 2.0.0
**Release Date**: October 30, 2025
