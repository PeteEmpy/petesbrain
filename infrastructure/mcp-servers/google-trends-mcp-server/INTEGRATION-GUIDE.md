# Google Trends Integration Guide

Complete guide for using Google Trends data in PetesBrain.

## Quick Start

### 1. Verify Installation

```bash
cd /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server

# Check server is configured in .mcp.json
cat /Users/administrator/Documents/PetesBrain/.mcp.json | grep google-trends

# Test the connection (wait 5 seconds between tests to avoid rate limiting)
.venv/bin/python test_trends.py
```

### 2. Restart Claude Code

After adding the server to `.mcp.json`, restart Claude Code to load the new MCP server.

### 3. Test in Claude Code

```plaintext
Can you check Google Trends for "christmas trees" over the last 3 months?
```

## Common Use Cases

### 1. Seasonal Planning

**Use Case:** Identify when to increase budgets for seasonal products

```python
# Via Claude Code MCP integration
mcp__google_trends__get_interest_over_time(
    keywords=["christmas trees", "artificial christmas trees"],
    timeframe="today 5-y",  # 5 years to see seasonal patterns
    geo="GB"
)
```

**Analysis:**
- Look for annual peaks (typically November/December for Christmas)
- Identify week-by-week growth patterns
- Compare current year vs previous years
- Plan budget increases 4-6 weeks before peak

**Integration with PetesBrain:**
- Add seasonal trend patterns to client CONTEXT.md
- Use in Q4 planning discussions
- Reference in budget increase proposals

### 2. Keyword Research for Campaign Expansion

**Use Case:** Find new keywords based on rising searches

```python
mcp__google_trends__get_related_queries(
    keyword="sustainable fashion",
    timeframe="today 12-m",
    geo="GB"
)
```

**Analysis:**
- "Rising" queries = fastest growing (ideal for early adoption)
- "Top" queries = established high volume (competitive)
- Use rising queries for discovery campaigns
- Use top queries for branded campaigns

**Integration with PetesBrain:**
- Export related queries to experiment log
- Add to client keyword strategy section
- Test in low-budget campaigns first

### 3. Geographic Targeting

**Use Case:** Identify which regions to prioritize

```python
mcp__google_trends__get_interest_by_region(
    keywords=["luxury hotels"],
    resolution="REGION",  # COUNTRY, REGION, CITY, or DMA
    geo="GB",
    timeframe="today 12-m"
)
```

**Analysis:**
- Top regions = highest search interest
- Use for location bid adjustments
- Identify expansion opportunities
- Correlate with conversion data

**Integration with PetesBrain:**
- Compare trends vs actual performance by region
- Update location targeting strategy
- Document in CONTEXT.md under "Geographic Insights"

### 4. Product/Category Prioritization

**Use Case:** Decide which product categories deserve more budget

```python
mcp__google_trends__compare_keywords(
    keywords=["stationery", "notebooks", "pens", "planners"],
    timeframe="today 12-m",
    geo="GB"
)
```

**Analysis:**
- Winner = highest average search volume
- Rising trend = growing demand (invest more)
- Falling trend = declining demand (reduce or optimize)
- Use to inform budget allocation

**Integration with PetesBrain:**
- Document in budget strategy discussions
- Reference in monthly reports
- Update product performance section

### 5. Performance Context Analysis

**Use Case:** Understand if campaign decline matches market decline

```python
# Check client's product search interest
mcp__google_trends__get_interest_over_time(
    keywords=["client-product-category"],
    timeframe="today 3-m",
    geo="GB"
)
```

**Analysis:**
- Campaign declining + search interest stable = campaign issue
- Campaign declining + search interest declining = market trend
- Use for root cause analysis
- Inform strategic recommendations

**Integration with PetesBrain:**
- Add to performance analysis workflow
- Document in client CONTEXT.md
- Reference in weekly performance reviews

## Rate Limiting & Best Practices

### Google Trends Rate Limits

- **Public API:** ~10 requests per minute per IP
- **429 Error:** Rate limit exceeded, wait 60 seconds
- **404 Error:** Data not available (try different parameters)

### Best Practices

1. **Batch Requests:** Group related queries together
2. **Add Delays:** Wait 5-10 seconds between requests
3. **Use Sensible Timeframes:**
   - Quick checks: `today 3-m`
   - Seasonal analysis: `today 5-y`
   - Broad trends: `all` (2004-present)

4. **Cache Results:** Save to JSON for repeated analysis
5. **Scheduled Monitoring:** Use automated agent weekly, not daily

### Example: Rate-Limited Batch Processing

```python
import time

clients = ["smythson", "tree2mydoor", "national-design-academy"]

for client in clients:
    keywords = get_client_keywords(client)
    trends = mcp__google_trends__get_interest_over_time(
        keywords=keywords,
        timeframe="today 3-m"
    )

    # Save results
    save_trends(client, trends)

    # Wait 10 seconds before next request
    time.sleep(10)
```

## Automated Monitoring

### Weekly Trend Monitor Agent

**Location:** `agents/performance-monitoring/trend-monitor.py`

**Schedule:** Every Monday 8:15 AM

**What It Does:**
1. Fetches trends for all client keywords
2. Compares vs previous week
3. Identifies >20% changes
4. Updates client CONTEXT.md
5. Sends alerts for significant changes

**Install Agent:**
```bash
cp agents/launchagents/com.petesbrain.trend-monitor.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.petesbrain.trend-monitor.plist
```

**Check Status:**
```bash
launchctl list | grep trend-monitor
cat ~/.petesbrain-trend-monitor.log
```

**Run Manually:**
```bash
python3 agents/performance-monitoring/trend-monitor.py
```

## Data Interpretation

### Understanding the 0-100 Scale

Google Trends data is **relative**, not absolute:
- **100** = Peak popularity in the dataset
- **50** = Half as popular as peak
- **0** = Less than 1% of peak

**Important:** You cannot compare absolute volumes between different searches!

### Trend Indicators

- **Rising** = Current > 3-month average (growing demand)
- **Falling** = Current < 3-month average (declining demand)
- **Breakout** = >5000% increase (massive growth)

### Seasonal Patterns

Look for:
- **Annual cycles:** Same time every year (Christmas, Back to School)
- **Monthly patterns:** End of month spikes (payday)
- **Day of week:** Weekday vs weekend differences

## Integration with Client Analysis

### Update CONTEXT.md Template

Add to client CONTEXT.md:

```markdown
## Search Trend Analysis

**Last Updated:** 2025-11-06

### Current Trends (3-month average)
- [Product A]: 65/100 📈 (rising)
- [Product B]: 42/100 📉 (falling)
- [Product C]: 78/100 📈 (rising)

### Key Insights
- [Product A] showing 15% growth vs last quarter - consider budget increase
- [Product B] declining correlates with campaign performance drop - likely market trend
- [Product C] peak season approaching - plan for Nov/Dec budget ramp

### Geographic Opportunities
- London: Highest interest (100/100)
- Manchester: Growing market (67/100, +12% vs last quarter)
- Birmingham: Underperforming (45/100)

### Related Queries (Rising)
1. "[related query 1]" - Breakout
2. "[related query 2]" - +450%
3. "[related query 3]" - +280%
```

### Monthly Report Integration

In monthly reports, add section:

```markdown
## Market Trends

We monitor Google search trends to provide context for campaign performance:

**[Product Category] Search Interest:**
- Current: 58/100 (vs 62/100 last month)
- Trend: ↓ -6% month-over-month
- Analysis: Declining search interest correlates with campaign performance

This suggests the performance dip is partly driven by reduced market demand
rather than campaign issues. We recommend [action based on trend].
```

## Troubleshooting

### Server Not Responding

```bash
# Check .mcp.json configuration
cat .mcp.json | grep -A 3 google-trends

# Verify Python environment
ls /Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server/.venv/bin/python

# Test pytrends directly
cd shared/mcp-servers/google-trends-mcp-server
.venv/bin/python -c "from pytrends.request import TrendReq; print('✅ pytrends working')"
```

### Rate Limiting Issues

If you get 429 errors:
1. Wait 60 seconds before retrying
2. Reduce request frequency
3. Use agent for scheduled monitoring instead of manual queries
4. Check you're not running multiple instances

### No Data Returned

If you get empty results:
- Try broader timeframe (`today 12-m` instead of `today 3-m`)
- Check spelling of keywords
- Try different geo (GB vs worldwide "")
- Some niche terms may have insufficient data

### Wrong Results

Common issues:
- Using brand names (use generic product categories instead)
- Too specific keywords (use broader terms)
- Multiple word order matters ("christmas trees" ≠ "trees christmas")

## Advanced Usage

### Custom Date Ranges

```python
# Specific period
mcp__google_trends__get_interest_over_time(
    keywords=["luxury hotels"],
    timeframe="2024-09-01 2024-11-01",  # Sept-Oct 2024
    geo="GB"
)
```

### Category Filtering

```python
# Shopping category only
mcp__google_trends__get_interest_over_time(
    keywords=["notebooks"],
    category=18,  # Shopping category
    timeframe="today 12-m"
)
```

Common categories:
- 0: All categories (default)
- 18: Shopping
- 67: Computers & Electronics
- 71: Arts & Entertainment
- 174: Travel

### Multi-Region Comparison

```python
# Compare UK vs US
uk_trends = mcp__google_trends__get_interest_over_time(
    keywords=["luxury stationery"],
    geo="GB"
)

us_trends = mcp__google_trends__get_interest_over_time(
    keywords=["luxury stationery"],
    geo="US"
)
```

## FAQ

**Q: Can I get exact search volumes?**
A: No, Trends provides relative data (0-100 scale). Use Google Ads Keyword Planner for volume estimates.

**Q: How often should I check trends?**
A: Weekly via automated agent is sufficient. Daily checks hit rate limits.

**Q: Can I compare different time periods?**
A: Yes, run separate queries and compare the relative patterns.

**Q: Why do I get different results on Google Trends website?**
A: API may have slight delays (1-2 days) vs real-time website data.

**Q: Can I get historical data?**
A: Yes, use `timeframe="all"` for data back to 2004.

**Q: Are mobile and desktop searches combined?**
A: Yes, by default. Use `gprop="youtube"` or `gprop="images"` for specific properties.

## Support

- **MCP Server:** [shared/mcp-servers/google-trends-mcp-server/README.md](README.md)
- **pytrends Docs:** https://pypi.org/project/pytrends/
- **Agent Monitoring:** [agents/README.md](../../../agents/README.md)

---

**Remember:** Google Trends is for **context**, not decisions. Always combine trend data with:
- Actual campaign performance
- Conversion data
- Client business context
- Competitive landscape
- Economic factors
