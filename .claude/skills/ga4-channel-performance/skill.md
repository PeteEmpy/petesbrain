# GA4 Channel Performance Analysis

Generate comprehensive weekly traffic source performance analysis combining GA4 attribution data with Google Ads spend to provide complete channel ROI view.

## When to Use

- Weekly client check-ins ("Which channels are working?")
- Budget allocation decisions
- Attribution analysis (GA4 vs Google Ads conversion counting)
- Understanding organic vs paid performance
- Identifying undervalued channels with strong assisted conversions

## Allowed Tools

- Read
- mcp__google-analytics__get_client_platform_ids
- mcp__google-analytics__run_report
- mcp__google-ads__get_client_platform_ids
- mcp__google-ads__run_gaql

## Input Required

- **Client name** (for CONTEXT.md and account lookup)
- **Date range** (defaults to last 7 days)
- **Comparison period** (defaults to previous 7 days for week-over-week)

## Output

Markdown report saved to `clients/{client}/reports/ga4/YYYY-MM-DD-channel-performance.md` with:

### 1. Executive Summary
- Total sessions, users, conversions, revenue across all channels
- Week-over-week changes
- Key findings (one-liner)

### 2. Channel Overview Table
```markdown
| Channel             | Sessions | Revenue  | Google Ads Spend | Blended ROAS | Conv Rate | vs Previous |
|---------------------|----------|----------|------------------|--------------|-----------|-------------|
| Paid Search         | 40,729   | £85,400  | £18,200          | 469%         | 3.2%      | -5%         |
| Organic Search      | 23,550   | £42,100  | £0               | N/A          | 2.8%      | +12%        |
| Direct              | 54,198   | £98,200  | £0               | N/A          | 3.5%      | +3%         |
| Paid Social         | 9,232    | £15,600  | £4,100           | 380%         | 2.1%      | +18%        |
| Organic Social      | 1,290    | £1,800   | £0               | N/A          | 1.9%      | -8%         |
| Email               | 11,409   | £28,400  | £0               | N/A          | 4.1%      | +6%         |
| Referral            | 3,200    | £5,100   | £0               | N/A          | 2.3%      | +2%         |
| Affiliates          | 9,998    | £18,900  | £0               | N/A          | 2.9%      | +15%        |
```

### 3. Attribution Comparison (If Available)
- **Google Ads reported conversions**: X
- **GA4 attributed conversions to Paid Search**: Y
- **Discrepancy**: Z (+/-% difference)
- **Why this matters**: Explanation of attribution window differences

### 4. Channel Deep Dive

For each major channel (>5% of sessions):

**Paid Search:**
- Sessions: 40,729 (+2,100 vs previous week)
- Revenue: £85,400 (+£4,200 vs previous week)
- Google Ads Spend: £18,200 (+£800 vs previous week)
- **Blended ROAS**: 469% (GA4 revenue ÷ Google Ads spend)
- **Google Ads Reported ROAS**: 420% (from Google Ads conversion tracking)
- **Attribution Gap**: +49pp (GA4 sees more revenue - likely includes view-through conversions)
- Conversion Rate: 3.2% (-0.1pp vs previous week)

**Key Insights:**
- Performance improved week-over-week despite slight conversion rate decline
- Attribution gap suggests Google Ads undervaluing its impact
- Strong channel for continued investment

### 5. Recommendations

**P0 - Critical:**
1. **Fix Organic Social conversion drop** (-8% sessions, -£400 revenue)
   - Instagram traffic down 15% week-over-week
   - Action: Review recent content performance, increase posting frequency
   - Impact: +£200/week potential recovery

**P1 - Important:**
2. **Scale Paid Social** (380% ROAS, only 6% of total sessions)
   - Currently £4,100/week spend
   - Recommendation: Increase to £6,000/week (+£2,000)
   - Projected Impact: +£7,600/week revenue at current 380% ROAS

3. **Investigate Paid Search attribution discrepancy** (+49pp vs Google Ads)
   - GA4 sees £85k revenue, Google Ads reports £76k
   - £9k gap = possible view-through conversions not credited in Google Ads
   - Action: Review attribution model settings in GA4 and Google Ads

**P2 - Nice-to-Have:**
4. **Improve Email conversion rate** (4.1% is good but could be better)
   - Test personalised product recommendations
   - Segment by purchase history

## Implementation Notes

### Data Collection Process

1. **Get Platform IDs**
```python
ga4_ids = mcp__google-analytics__get_client_platform_ids(client_name)
ga4_property_id = ga4_ids['ga4_property_id']

google_ads_ids = mcp__google-ads__get_client_platform_ids(client_name)
customer_id = google_ads_ids['google_ads_customer_id']
manager_id = google_ads_ids['google_ads_manager_id']
```

2. **Query GA4 Channel Performance**
```python
# Current period (last 7 days)
current_report = mcp__google-analytics__run_report(
    property_id=ga4_property_id,
    start_date='2025-12-10',
    end_date='2025-12-16',
    metrics=['sessions', 'totalUsers', 'conversions', 'totalRevenue', 'engagementRate'],
    dimensions=['sessionDefaultChannelGroup'],
    limit=20
)

# Previous period (7 days before that)
previous_report = mcp__google-analytics__run_report(
    property_id=ga4_property_id,
    start_date='2025-12-03',
    end_date='2025-12-09',
    metrics=['sessions', 'totalUsers', 'conversions', 'totalRevenue', 'engagementRate'],
    dimensions=['sessionDefaultChannelGroup'],
    limit=20
)
```

3. **Query Google Ads Spend (for ROAS calculation)**
```python
# Get spend by advertising channel
google_ads_spend = mcp__google-ads__run_gaql(
    customer_id=customer_id,
    manager_id=manager_id,
    query="""
        SELECT
            advertising_channel_type,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE
            segments.date BETWEEN '2025-12-10' AND '2025-12-16'
            AND campaign.status IN ('ENABLED', 'PAUSED')
        ORDER BY metrics.cost_micros DESC
    """
)
```

4. **Calculate Blended ROAS**
```
Blended ROAS = (GA4 Revenue for Paid Search) / (Google Ads Total Spend) × 100
```

### Key Calculations

**Week-over-Week Change:**
```python
change_pct = ((current_value - previous_value) / previous_value) * 100
```

**Blended ROAS (GA4 Revenue vs Google Ads Spend):**
```python
blended_roas = (ga4_paid_search_revenue / google_ads_spend) * 100
```

**Attribution Discrepancy:**
```python
# Compare Google Ads reported conversions vs GA4 Paid Search conversions
discrepancy = ga4_conversions - google_ads_conversions
discrepancy_pct = (discrepancy / google_ads_conversions) * 100
```

### Channel Mapping (GA4 to Google Ads)

GA4 uses `sessionDefaultChannelGroup` which includes:
- **Paid Search** = Google Ads Search campaigns
- **Paid Shopping** = Google Ads Shopping campaigns
- **Paid Social** = Facebook/Instagram/LinkedIn Ads
- **Display** = Google Display Network
- **Paid Video** = YouTube Ads

Map these to Google Ads `advertising_channel_type`:
- SEARCH → Paid Search
- SHOPPING → Paid Shopping (often grouped with Paid Search)
- DISPLAY → Display
- VIDEO → Paid Video
- PERFORMANCE_MAX → Could appear in multiple GA4 channels

### British English Standards

- ✅ "analyse" not "analyze"
- ✅ "optimise" not "optimize"
- ✅ ROAS as "420%" not "£4.20"
- ✅ Currency: £ (British pounds)

## Common Client Questions This Answers

1. **"Which channels are working?"**
   → Channel Overview Table shows revenue and ROAS by channel

2. **"Should we increase Google Ads budget?"**
   → Blended ROAS calculation shows true ROI including view-through conversions

3. **"Why do Google Ads and GA4 show different conversion numbers?"**
   → Attribution Comparison section explains the discrepancy

4. **"Is organic search growing?"**
   → Week-over-week comparison shows trend

5. **"Are we getting value from email marketing?"**
   → Email channel performance with conversion rate benchmarking

## Success Criteria

- ✅ Generate report in <5 minutes
- ✅ Accurately calculate blended ROAS for paid channels
- ✅ Flag >15% performance changes week-over-week
- ✅ Surface attribution discrepancies between Google Ads and GA4
- ✅ Provide 3-5 actionable recommendations prioritised by impact

## Test Clients

1. **Smythson** - Complex multi-channel strategy, needs attribution clarity
2. **Superspace** - Understanding organic vs paid performance
3. **Tree2MyDoor** - Seasonal traffic pattern analysis

## Time Estimate

5 hours implementation:
- 2 hours: GAQL queries + GA4 API calls
- 2 hours: Blended ROAS calculation logic
- 1 hour: Report generation + testing

## Related Skills

- `google-ads-weekly-report` - Google Ads performance analysis (Phase 1A)
- Future: `meta-ads-weekly-report` - Meta Ads performance (Phase 6)

## Example Usage

```
User: "Generate GA4 channel performance report for Smythson"

Assistant loads this skill and:
1. Reads clients/smythson/CONTEXT.md for platform IDs
2. Queries GA4 for current and previous week channel data
3. Queries Google Ads for spend data
4. Calculates blended ROAS
5. Identifies week-over-week changes >15%
6. Generates recommendations
7. Saves to clients/smythson/reports/ga4/2025-12-17-channel-performance.md
8. Presents summary to user
```

---

**Status**: Phase 1C implementation
**Priority**: P1 (High Value, Low Effort)
**Dependencies**: Google Analytics MCP, Google Ads MCP
**ROI**: ⭐⭐⭐⭐⭐ (Answers #1 client question: "Which channels are working?")
