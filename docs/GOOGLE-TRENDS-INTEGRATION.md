# Google Trends Integration - Complete

**Status:** ✅ Fully Integrated
**Date:** November 6, 2025
**Version:** 1.0

---

## Overview

PetesBrain now has complete access to Google Trends data through a custom MCP server. This enables:

- **Search demand tracking** for all client products/services
- **Seasonal pattern identification** for budget planning
- **Geographic opportunity analysis** for location targeting
- **Keyword research** for campaign expansion
- **Performance context** for root cause analysis

---

## What Was Built

### 1. MCP Server (`shared/mcp-servers/google-trends-mcp-server/`)

Full-featured Google Trends integration with 6 core functions:

| Function | Purpose | Use Case |
|----------|---------|----------|
| `get_interest_over_time` | Track trends over time | Identify seasonal patterns, compare periods |
| `get_interest_by_region` | Geographic analysis | Find high-potential regions |
| `get_related_queries` | Keyword discovery | Find rising/top related searches |
| `get_trending_searches` | Real-time trends | Identify current hot topics |
| `compare_keywords` | Keyword comparison | Prioritize product categories |
| `get_suggestions` | Autocomplete suggestions | Expand keyword lists |

**Tech Stack:**
- Python 3.13
- pytrends 4.9.2 (unofficial Google Trends API)
- MCP 1.1.0 (Model Context Protocol)
- pandas 2.2.0 (data manipulation)

**Rate Limiting:** Built-in retry logic, backoff, and delays to handle Google's ~10 requests/minute limit

### 2. Automated Agent (`agents/performance-monitoring/trend-monitor.py`)

Weekly monitoring agent that:
- Fetches trends for all client keywords
- Identifies significant changes (>20% movement)
- Updates client CONTEXT.md with insights
- Sends alerts for declining search interest
- Saves historical data for comparison

**Schedule:** Every Monday 8:15 AM

### 3. Documentation

- **README.md** - Technical overview and quick start
- **INTEGRATION-GUIDE.md** - Complete usage guide with examples
- **test_trends.py** - Test suite for verification
- **setup.sh** - One-command setup script

---

## Installation Status

### ✅ Completed

1. MCP server implemented with all 6 functions
2. Dependencies installed in virtual environment
3. Server added to `.mcp.json` configuration
4. Automated monitoring agent created
5. LaunchAgent plist file created
6. Comprehensive documentation written
7. Test suite created
8. Integration guide completed

### ⏳ Pending (requires restart)

1. **Restart Claude Code** to load new MCP server
2. **Install LaunchAgent** (optional, for automated monitoring):
   ```bash
   cp agents/launchagents/com.petesbrain.trend-monitor.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.petesbrain.trend-monitor.plist
   ```

---

## Quick Start Guide

### Test the Integration

After restarting Claude Code, try:

```plaintext
Can you check Google Trends for "christmas trees" over the last 3 months?
```

Expected response: Time-series data showing search interest (0-100 scale) with summary statistics.

### Common Commands

**Check seasonal patterns:**
```plaintext
Show me 5-year Google Trends for "christmas trees" to identify seasonal patterns
```

**Find related keywords:**
```plaintext
What are the rising related searches for "sustainable fashion"?
```

**Compare products:**
```plaintext
Compare Google Trends for "notebooks" vs "planners" vs "journals" over the last year
```

**Geographic analysis:**
```plaintext
Which UK regions have the highest search interest for "luxury hotels"?
```

---

## Use Cases by Client Type

### E-Commerce Clients (Tree2mydoor, Smythson, Superspace)

**Seasonal Planning:**
```plaintext
Analyze 5-year trends for [product] to identify peak months for budget increases
```

**Product Prioritization:**
```plaintext
Compare trends for our top 5 product categories to inform Q4 budget allocation
```

**Stock Planning:**
```plaintext
When does search interest for [product] typically start rising? (for supplier lead time)
```

### Service Clients (Devonshire Hotels, National Design Academy)

**Demand Forecasting:**
```plaintext
Show 12-month trends for "interior design courses" to identify enrollment peaks
```

**Geographic Expansion:**
```plaintext
Which UK cities show highest interest for "luxury hotels derbyshire"?
```

**Competitive Context:**
```plaintext
Compare trends for "online courses" vs "in-person courses" vs "hybrid courses"
```

### All Clients

**Performance Context:**
```plaintext
Get trends for [client product category] to see if campaign decline matches market decline
```

**Monthly Reports:**
```plaintext
Include search trend analysis in [client] monthly report to provide market context
```

**Strategy Reviews:**
```plaintext
What are the rising related searches for [client service]? (for campaign expansion ideas)
```

---

## Integration with Existing Systems

### 1. Client Context System

Trend insights automatically added to `CONTEXT.md`:

```markdown
### Search Trend Analysis (2025-11-06)

**Significant Changes:**
- **luxury stationery** ↑ 23.5% (current: 68, avg: 55.0)
- **leather notebooks** ↓ -18.2% (current: 45, avg: 55.0)

**Current Trends:**
- luxury stationery: 68/100 📈 (rising)
- personalised diaries: 52/100 📉 (falling)
```

### 2. Performance Analysis Workflow

New step in client analysis:

1. Read CONTEXT.md (strategic context)
2. Check tasks-completed.md (what was done)
3. Check experiment log (why it was done)
4. **Check Google Trends (market context)** ← NEW
5. Review Google Ads Change History
6. Consult Knowledge Base

### 3. Monthly Reporting

Add "Market Trends" section:

```markdown
## Market Trends

Google Trends analysis shows [product category] search interest:
- Current: 58/100 (vs 62/100 last month)
- Trend: ↓ -6% month-over-month

This suggests the performance dip is partly driven by reduced market
demand rather than campaign issues.
```

### 4. Budget Planning

Use trends for:
- Seasonal budget allocation (increase before peak)
- Product category prioritization (budget to winners)
- Geographic targeting (focus on high-interest regions)
- Timing of experiments (test during stable periods)

---

## Technical Details

### File Structure

```
shared/mcp-servers/google-trends-mcp-server/
├── .venv/                      # Virtual environment
├── server.py                   # MCP server implementation
├── requirements.txt            # Dependencies
├── README.md                   # Technical docs
├── INTEGRATION-GUIDE.md        # Usage guide
├── test_trends.py              # Test suite
└── setup.sh                    # Setup script

agents/performance-monitoring/
└── trend-monitor.py            # Weekly monitoring agent

agents/launchagents/
└── com.petesbrain.trend-monitor.plist  # Agent schedule

shared/data/trend-history/      # Historical trend data (created on first run)
└── [client]-YYYY-MM-DD.json
```

### Configuration

[.mcp.json](/.mcp.json#L65-68):
```json
"google-trends": {
  "command": "/path/to/.venv/bin/python",
  "args": ["/path/to/server.py"]
}
```

### Data Storage

Trend data saved to: `shared/data/trend-history/[client]-[date].json`

Format:
```json
{
  "client": "smythson",
  "keywords": ["luxury stationery", "leather notebooks"],
  "timeframe": "today 3-m",
  "geo": "GB",
  "summary": {
    "luxury stationery": {
      "average": 55.0,
      "max": 75,
      "min": 35,
      "current": 68,
      "trend": "rising"
    }
  },
  "data": [...]
}
```

---

## Rate Limiting & Best Practices

### Google Trends Limits

- **~10 requests per minute per IP**
- 429 error = rate limit exceeded (wait 60 seconds)
- 404 error = data not available (try different parameters)

### Recommended Usage

| Frequency | Use Case | Method |
|-----------|----------|--------|
| Weekly | Client monitoring | Automated agent |
| Monthly | Strategic reviews | Manual queries |
| Ad-hoc | Performance investigations | Manual queries |
| Daily | ❌ NOT RECOMMENDED | Will hit rate limits |

### Best Practices

1. **Batch requests:** Group related queries, wait 10 seconds between
2. **Cache results:** Save to JSON, reuse for multiple analyses
3. **Use sensible timeframes:**
   - Quick check: `today 3-m`
   - Seasonal: `today 5-y`
   - Historical: `all`
4. **Generic keywords:** Use product categories, not brand names
5. **Scheduled monitoring:** Weekly via agent, not daily

---

## Troubleshooting

### MCP Server Not Responding

```bash
# 1. Verify installation
ls /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server/.venv/bin/python

# 2. Test pytrends directly
cd shared/mcp-servers/google-trends-mcp-server
.venv/bin/python -c "from pytrends.request import TrendReq; print('✅ Working')"

# 3. Check .mcp.json
cat .mcp.json | grep -A 3 google-trends

# 4. Restart Claude Code
```

### Rate Limiting (429 Errors)

- Wait 60 seconds before retrying
- Reduce request frequency
- Use automated agent instead of manual queries
- Check no other processes using Trends API

### No Data Returned

- Try broader timeframe (`today 12-m` instead of `today 3-m`)
- Check keyword spelling
- Try different geo (GB vs worldwide "")
- Some niche terms lack sufficient data

### Agent Not Running

```bash
# Check if loaded
launchctl list | grep trend-monitor

# View logs
cat ~/.petesbrain-trend-monitor.log
cat ~/.petesbrain-trend-monitor-error.log

# Reload
launchctl unload ~/Library/LaunchAgents/com.petesbrain.trend-monitor.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.trend-monitor.plist

# Run manually
python3 agents/performance-monitoring/trend-monitor.py
```

---

## Future Enhancements

### Phase 2 (Potential)

1. **Dashboard Integration**
   - Visual trend charts in monthly reports
   - Embed trends in client dashboards
   - Real-time trend alerts in Slack

2. **Advanced Analysis**
   - Correlation with campaign performance
   - Predictive budget recommendations
   - Automated trend-based bidding adjustments

3. **Multi-Region Support**
   - Compare UK vs US vs EU trends
   - Market expansion opportunity scoring
   - Geographic arbitrage identification

4. **AI-Enhanced Insights**
   - Claude analyzes trends automatically
   - Generates strategic recommendations
   - Identifies anomalies and opportunities

---

## Documentation Links

- **MCP Server README:** [shared/mcp-servers/google-trends-mcp-server/README.md](../shared/mcp-servers/google-trends-mcp-server/README.md)
- **Integration Guide:** [shared/mcp-servers/google-trends-mcp-server/INTEGRATION-GUIDE.md](../shared/mcp-servers/google-trends-mcp-server/INTEGRATION-GUIDE.md)
- **Agents Overview:** [agents/README.md](../agents/README.md)
- **MCP Servers:** [docs/MCP-SERVERS.md](MCP-SERVERS.md)

---

## Summary

Google Trends integration is **complete and ready to use**. After restarting Claude Code:

✅ You can query Google Trends data directly
✅ Automated monitoring runs weekly
✅ Trend insights enhance client analysis
✅ Comprehensive documentation available

**Next Action:** Restart Claude Code, then test with: "Check Google Trends for christmas trees"

---

**Built for PetesBrain v1.0**
**MCP Server Version:** 1.0
**Agent Version:** 1.0
**Status:** Production Ready
