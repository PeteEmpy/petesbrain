# AI Traffic Analysis

## Description

Analyses traffic from AI tools (ChatGPT, Claude, Perplexity, Gemini, Mistral, etc.) in Google Analytics 4 data. Shows which AI platforms are sending users, their engagement quality, and revenue contribution.

**Key Question**: "Are AI tools sending valuable traffic to my site?"

## Allowed Tools

- Read
- Write
- mcp__platform-ids__get_client_platform_ids
- mcp__google-analytics__run_report

## User Input

**Client name** (optional):
- If provided: Analyse single client
- If omitted: Analyse all clients with GA4 property IDs

**Date range** (optional):
- Default: Last 7 days vs previous 7 days
- Format: YYYY-MM-DD to YYYY-MM-DD

## Known AI Tool Sources

Track traffic from these sessionSource values:
- `chatgpt.com` - ChatGPT (OpenAI)
- `claude.ai` - Claude (Anthropic)
- `perplexity.ai` - Perplexity AI
- `gemini.google.com` - Gemini (Google)
- `bard.google.com` - Bard (Google, legacy)
- `chat.mistral.ai` - Mistral AI
- `you.com` - You.com AI search
- `poe.com` - Poe (multi-model aggregator)
- `character.ai` - Character.AI
- `huggingface.co/chat` - HuggingFace Chat
- `bing.com/chat` - Bing Chat (Copilot)
- `pi.ai` - Pi (Inflection AI)

## Analysis Logic

### Step 1: Get Client Platform IDs

If specific client provided:
```python
ids = mcp__platform-ids__get_client_platform_ids(client_slug)
ga4_property_id = ids['ga4_property_id']
```

If analysing all clients:
```python
# Search all CONTEXT.md files for GA4 Property IDs
# Pattern: **GA4 Property ID**: 123456789
clients_with_ga4 = []
for client_dir in glob("clients/*/CONTEXT.md"):
    # Extract client slug and GA4 ID
    clients_with_ga4.append({
        'client': client_slug,
        'ga4_property_id': property_id
    })
```

### Step 2: Query GA4 for AI Tool Traffic

**Date Calculation**:
- Current period: Last 7 complete days (today - 8 to today - 1)
- Previous period: Previous 7 days (today - 15 to today - 8)

**GAQL Query**:
```python
mcp__google-analytics__run_report(
    property_id=ga4_property_id,
    start_date=start_date,
    end_date=end_date,
    metrics=[
        'sessions',
        'totalUsers',
        'conversions',
        'totalRevenue',
        'engagementRate',
        'averageSessionDuration',
        'bounceRate'
    ],
    dimensions=['sessionSource', 'sessionMedium', 'date']
)
```

### Step 3: Filter AI Tool Traffic

From the raw data:
1. Filter rows where `sessionSource` matches known AI tools
2. Exclude `sessionMedium = 'organic'` (organic search results from AI tools, not AI chat referrals)
3. Keep `sessionMedium = 'referral'` (actual AI tool referrals)

### Step 4: Calculate Metrics

**Per AI Tool**:
- Total sessions
- Total users
- Total conversions
- Total revenue
- Average engagement rate
- Average session duration
- Conversion rate (conversions / sessions)
- Revenue per session

**Overall AI Tool Traffic**:
- Combined metrics for all AI tools
- % of total site traffic
- % of total site revenue

**Week-over-Week Comparison**:
- Change in sessions
- Change in revenue
- Change in conversion rate

### Step 5: Generate Report

**Output Format**: Markdown saved to:
- Single client: `clients/{client}/reports/ga4/YYYY-MM-DD-ai-traffic-analysis.md`
- All clients: `clients/_data/reports/YYYY-MM-DD-ai-traffic-analysis-all-clients.md`

**Report Structure**:

```markdown
# AI Traffic Analysis - {Client Name or "All Clients"}

**Report Period**: {start_date} - {end_date}
**Comparison Period**: {prev_start_date} - {prev_end_date}
**Generated**: {today}

---

## 🟢 **Executive Summary**

### Overall AI Tool Traffic

| Metric | Current Week | Previous Week | Change |
|--------|--------------|---------------|--------|
| **Total Sessions** | X | Y | +Z% |
| **Total Users** | X | Y | +Z% |
| **Total Revenue** | £X | £Y | +Z% |
| **Conversions** | X | Y | +Z% |
| **Share of Site Traffic** | X% | Y% | +Zpp |
| **Share of Site Revenue** | X% | Y% | +Zpp |

**Key Insight**: AI tools represent X% of sessions but Y% of revenue, indicating [higher/lower] value than average traffic.

---

## 📊 **AI Tool Breakdown**

### Current Week Performance

| AI Tool | Sessions | Revenue | Conv Rate | Engagement | Revenue/Session |
|---------|----------|---------|-----------|------------|-----------------|
| ChatGPT | X | £Y | Z% | W% | £V |
| Claude | X | £Y | Z% | W% | £V |
| Perplexity | X | £Y | Z% | W% | £V |
| Gemini | X | £Y | Z% | W% | £V |
| Other | X | £Y | Z% | W% | £V |

---

## 📈 **Trends**

### Week-over-Week Changes

| AI Tool | Sessions Change | Revenue Change | Status |
|---------|----------------|----------------|--------|
| ChatGPT | +X% | +Y% | 🔥/📈/📉 |
| Claude | +X% | +Y% | 🔥/📈/📉 |
| Perplexity | +X% | +Y% | 🔥/📈/📉 |

**Fastest Growing**: [Tool] (+X% sessions)
**Highest Value**: [Tool] (£X revenue per session)

---

## 🎯 **Insights & Recommendations**

{Generate based on patterns:}

1. If ChatGPT dominates: "ChatGPT represents X% of AI tool traffic - consider optimising for ChatGPT search/recommendations"

2. If conversion rate is high: "AI tool traffic converts at X%, significantly [higher/lower] than site average (Y%) - these are [qualified/exploratory] users"

3. If revenue per session is high: "AI tool users generate £X per session vs £Y site average - premium audience"

4. If growing week-over-week: "AI tool traffic growing X% WoW - emerging channel worth monitoring"

5. If engagement is low: "Engagement rate X% suggests users are fact-checking or price comparing - consider optimised landing pages"

---

**Data Source**: Google Analytics 4 Property ID {property_id}
**Analysis by**: Claude Code (via ai-traffic-analysis skill)
```

## Error Handling

**No GA4 Property ID**:
- If client has no GA4 property ID in CONTEXT.md, skip client and log warning
- Include summary at end: "Skipped 3 clients (no GA4 data): ClientA, ClientB, ClientC"

**No AI Tool Traffic**:
- If zero AI tool sessions found, report: "No AI tool traffic detected in this period"
- Still show comparison to site average for context

**API Errors**:
- Catch GA4 API errors gracefully
- Log error details
- Continue with next client if analysing all clients

## Example Usage

**Single Client Analysis**:
```
User: "Run ai-traffic-analysis for Smythson"
Assistant: Analyses Smythson's AI tool traffic for last 7 days
Output: clients/smythson/reports/ga4/2025-12-17-ai-traffic-analysis.md
```

**All Clients Analysis**:
```
User: "Run ai-traffic-analysis for all clients"
Assistant: Analyses AI tool traffic across all clients with GA4 data
Output: clients/_data/reports/2025-12-17-ai-traffic-analysis-all-clients.md
```

**Custom Date Range**:
```
User: "Run ai-traffic-analysis for Smythson from 2025-12-01 to 2025-12-14"
Assistant: Analyses Smythson's AI tool traffic for specified period
Output: clients/smythson/reports/ga4/2025-12-17-ai-traffic-analysis.md
```