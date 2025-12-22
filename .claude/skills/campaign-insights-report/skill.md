# Campaign Insights Report

Generate comprehensive campaign analysis with product-level insights and actionable recommendations. Automatically opens in browser with beautiful HTML formatting.

## Description

This skill generates detailed campaign performance reports with:
- Campaign performance metrics (spend, revenue, ROAS, conversions)
- Product-level analysis (top products, ROAS by product)
- Priority-ranked recommendations (P0/P1/P2)
- Knowledge base article suggestions
- Actionable next steps

Reports are generated in both JSON (for historical reference) and HTML (for viewing/sharing).

## When to Use

- Weekly client reviews
- Monthly performance analysis
- Campaign optimization planning
- Client reporting
- Product performance analysis

## Triggers

- User says: "campaign insights for [client]", "weekly report for [client]", "analyse [client] campaigns"
- User requests: "campaign report", "performance analysis", "product insights"

## Allowed Tools

- Read
- Write
- Edit
- Bash
- mcp__google-ads__run_gaql
- mcp__google-ads__get_client_platform_ids

## Instructions

### Step 1: Get Client Information

Ask the user which client they want to analyse:
- If user provides client name in request, use it
- Otherwise, ask: "Which client would you like to generate a campaign insights report for?"

### Step 2: Determine Date Range

**CRITICAL: Conversion Lag Protection**

Google Ads conversion data takes 24-48 hours to settle. Always end reports 3 days before today to ensure accurate conversion data.

Ask for date range (or use default):
- **Default: Last 7 days ending 3 days ago** (e.g., on Dec 16th, report Dec 6-12)
- User can specify: "last 14 days", "last 30 days", "this month", "last month"
- Or specific dates: "2025-12-01 to 2025-12-15"

**Why 3-day lag:**
- Conversions can be attributed days after clicks (typical window: 30 days)
- Google Ads data isn't final for 24-48 hours minimum
- E-commerce clients (Tree2mydoor) have longer research/buying cycles
- Prevents underreporting conversions and ROAS

**When to override:**
- User explicitly requests dates including recent days
- Real-time monitoring (acknowledge data is incomplete)
- Specific date range analysis (historical periods)

### Step 3: Fetch Real Data via MCP

1. Get client platform IDs:
   ```python
   mcp__google-ads__get_client_platform_ids(client_name)
   ```

2. Fetch campaign data:
   ```sql
   SELECT
       campaign.id,
       campaign.name,
       campaign.status,
       campaign.advertising_channel_type,
       metrics.cost_micros,
       metrics.conversions_value,
       metrics.conversions,
       metrics.clicks,
       metrics.impressions,
       metrics.search_impression_share,
       metrics.search_budget_lost_impression_share
   FROM campaign
   WHERE
       segments.date >= 'START_DATE'
       AND segments.date <= 'END_DATE'
       AND metrics.cost_micros > 0
   ORDER BY metrics.cost_micros DESC
   ```

3. Fetch product data (for e-commerce clients with Shopping/Performance Max):
   ```sql
   SELECT
       segments.product_item_id,
       segments.product_title,
       segments.date,
       metrics.clicks,
       metrics.impressions,
       metrics.conversions,
       metrics.conversions_value,
       metrics.cost_micros
   FROM shopping_performance_view
   WHERE
       segments.date >= 'START_DATE'
       AND segments.date <= 'END_DATE'
       AND metrics.cost_micros > 0
   ORDER BY metrics.cost_micros DESC
   LIMIT 100
   ```

### Step 4: Generate Report

Use the report generator in `/Users/administrator/Documents/PetesBrain.nosync/tools/report-generator`:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/report-generator
python3 generate_campaign_insights.py <client-slug> --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

The script will:
1. Transform MCP data to analyzer format
2. Run campaign + product analysis
3. Generate prioritised recommendations
4. Save JSON report (for historical reference)
5. Generate HTML report
6. Automatically open HTML report in browser

### Step 5: Summary

Provide user with:
- Key metrics summary (spend, revenue, ROAS, conversions)
- Top 3 recommendations with priority
- Path to saved reports (JSON and HTML)

## Example Usage

**User**: "Campaign insights for Tree2mydoor"

**Assistant**:
1. Fetches Tree2mydoor platform IDs
2. Gets campaign data for last 7 days
3. Gets product data (e-commerce client)
4. Generates comprehensive analysis
5. Opens HTML report in browser
6. Provides summary:
   ```
   ✓ Tree2mydoor Campaign Insights (Dec 9-15, 2025)

   Performance:
   - Total Spend: £2,474
   - Total Revenue: £3,383
   - Blended ROAS: 1.37x
   - Conversions: 161

   Top 3 Recommendations:
   1. [P1] Low ROAS Performance - 16 campaigns below target (£1,410 spend)
   2. [P1] High Spend, Low Performance - "Roses" campaign losing money (£115 spend, 0.56x ROAS)
   3. [P1] Budget Constraints - "Low Traffic Shopping" limited by budget (57% Lost IS)

   Reports saved:
   - HTML: tree2mydoor_insights_20251216_112958.html (opened in browser)
   - JSON: tree2mydoor_insights_20251216_112958.json
   ```

## Output Format

### Browser (HTML):
- Professional formatted report with green branding
- Health score at top
- Metrics grid (spend, revenue, ROAS, conversions, issues)
- Product performance table (top 5 by spend)
- Priority-ranked recommendations with:
  - Impact metrics
  - Detailed analysis
  - Next steps checklist
  - Related KB articles

### JSON (Saved):
- Complete analysis data
- Campaign breakdowns
- Product metrics
- Recommendations with full context
- KB article references

## Files Created

- `reports/[client]_insights_[timestamp].html` - Browser-viewable report
- `reports/[client]_insights_[timestamp].json` - Complete analysis data

## Notes

- Always fetch REAL data via MCP (never use mock data)
- Product analysis only runs for e-commerce clients (Shopping/Performance Max campaigns)
- Reports automatically open in browser for immediate viewing
- JSON files stored for historical reference and future analysis
- KB articles automatically matched to recommendations

## Error Handling

- If MCP token limit exceeded: Reduce LIMIT on product query
- If no Shopping campaigns: Skip product analysis
- If client not found: Check voice transcription aliases in CONTEXT.md
- If no data for date range: Inform user and suggest different dates
