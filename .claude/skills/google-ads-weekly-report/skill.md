---
name: google-ads-weekly-report
description: Generates comprehensive weekly Google Ads performance analysis for e-commerce clients with prioritised recommendations and smart task creation. Use when user says "weekly report for [client]", "Google Ads weekly analysis", or needs a client performance report.
allowed-tools: mcp__google-ads__run_gaql, mcp__google-ads__list_accounts, Read, Write, Bash
---

# Google Ads Weekly E-commerce Report

---

## Instructions

When this skill is invoked:

### 1. Identify Client and Get Context

Ask user to confirm:
- **Client name** (e.g., "Godshot", "Superspace", "Bright Minds")
- **Date range** (defaults to last 7 days if not specified)

Then read:
```bash
Read: clients/[client-name]/CONTEXT.md
```

Extract account ID using `mcp__google-ads__get_client_platform_ids`

### 2. Pull Google Ads Data

Use `mcp__google-ads__run_gaql` to extract these metrics for the specified period and previous period:

**Account-Level Metrics:**
```sql
SELECT
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.clicks,
  metrics.impressions,
  metrics.ctr,
  metrics.average_cpc
FROM customer
WHERE segments.date DURING [DATE_RANGE]
```

**Campaign-Level Performance:**
```sql
SELECT
  campaign.name,
  campaign.id,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.clicks,
  metrics.impressions,
  metrics.ctr,
  metrics.average_cpc,
  metrics.search_impression_share
FROM campaign
WHERE segments.date DURING [DATE_RANGE]
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

**Product-Level Performance (Shopping/PMax):**
```sql
SELECT
  segments.product_item_id,
  segments.product_title,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.clicks,
  metrics.impressions
FROM shopping_performance_view
WHERE segments.date DURING [DATE_RANGE]
ORDER BY metrics.conversions_value DESC
LIMIT 100
```

**Placement Performance:**
```sql
SELECT
  segments.ad_network_type,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.clicks,
  metrics.impressions
FROM customer
WHERE segments.date DURING [DATE_RANGE]
GROUP BY segments.ad_network_type
```

### 3. Calculate Key Metrics

For both current period and previous period:

- **ROAS** = Conversion Value / Spend × 100
- **Cost per Conversion** = Spend / Conversions
- **Conversion Rate** = Conversions / Clicks × 100
- **Week-over-week % change** = ((Current - Previous) / Previous) × 100

### 4. Flag Performance Changes

Identify and highlight:
- Campaigns with >±15% change in ROAS
- Campaigns with >±15% change in conversions
- Products with >±15% change in conversion value
- New top 10 products not in previous top 10

### 5. Generate Markdown Report

Create report with these sections:

```markdown
# Google Ads Weekly Report: [Client Name]
**Period:** [Start Date] - [End Date]
**Generated:** [Today's Date]

---

## Executive Summary

### Account Performance
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Spend | £X,XXX | £X,XXX | +X% |
| Conversions | XXX | XXX | +X% |
| Conv Value | £XX,XXX | £XX,XXX | +X% |
| ROAS | XXX% | XXX% | +Xpp |
| CPA | £XXX | £XXX | -X% |
| CTR | X.X% | X.X% | +X% |
| Avg CPC | £X.XX | £X.XX | +X% |

**Key Takeaway:** [One-line summary of overall performance]

---

## Campaign Breakdown

### Top Performing Campaigns
| Campaign | Spend | Conv | ROAS | WoW Change |
|----------|-------|------|------|------------|
| ... | ... | ... | ... | ... |

### Campaigns Requiring Attention
[List campaigns with >15% negative change or poor performance]

---

## Product Performance (E-commerce)

### Top 10 Products by Revenue
| Product | Conv Value | Conv | ROAS | WoW Change |
|---------|------------|------|------|------------|
| ... | ... | ... | ... | ... |

### Bottom 10 Products (High Spend, Low ROAS)
| Product | Spend | ROAS | Issue |
|---------|-------|------|-------|
| ... | ... | ... | ... |

### Notable Changes
[Products with >15% change in performance]

---

## Placement Analysis

| Placement | Spend | Conv Value | ROAS | Share of Spend |
|-----------|-------|------------|------|----------------|
| Shopping | £X,XXX | £XX,XXX | XXX% | XX% |
| YouTube | £XXX | £X,XXX | XXX% | XX% |
| Display | £XXX | £X,XXX | XXX% | XX% |
| Discover | £XX | £XXX | XXX% | X% |

**Insight:** [Which placements are driving best ROAS vs wasting spend]

---

## Week-over-Week Trends

[Chart or table showing daily performance over both weeks]

**Trend Analysis:**
- [Observation about performance patterns]
- [Notable days - spikes or drops]
- [Correlation with any known events]

---

## Prioritised Recommendations

### 1. [Highest Priority Action]
**Issue:** [What's wrong]
**Impact:** [Revenue/efficiency opportunity]
**Action:** [Specific recommendation]

### 2. [Second Priority Action]
**Issue:** [What's wrong]
**Impact:** [Revenue/efficiency opportunity]
**Action:** [Specific recommendation]

### 3. [Third Priority Action]
...

---

## Appendix: Data Notes

- ROAS calculated as: Conversion Value / Spend × 100
- "Week-over-week" compares [dates] vs [dates]
- Product data limited to top 100 by conversion value
- Placement data aggregated across all campaigns

---

**Next Review:** [Next week's date]
```

### 6. Save Report

**Save both Markdown and HTML versions:**

```python
# Save Markdown version
md_path = f"clients/{client_slug}/reports/weekly/{report_date}-weekly-report.md"
with open(md_path, 'w') as f:
    f.write(markdown_content)

# Generate HTML version with ROK branding
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Ads Weekly Report: {client_name}</title>
    <style>
        /* ROK branding styles - see shared/assets/branding/roksys-report-styles.css */
        body {{
            font-family: Verdana, sans-serif;
            font-size: 13px;
            line-height: 1.6;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #2d5016 0%, #1a3009 100%);
            color: white;
            padding: 30px;
            position: relative;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 28px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        .header .meta {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .logo {{
            position: absolute;
            top: 20px;
            right: 30px;
            background: white;
            padding: 5px;
            border-radius: 4px;
        }}
        .logo img {{
            width: 120px;
            height: auto;
            display: block;
        }}
        .content {{
            padding: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        .positive {{ color: #28a745; }}
        .negative {{ color: #dc3545; }}
        .priority-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
        }}
        .p0 {{ background: #dc3545; color: white; }}
        .p1 {{ background: #fd7e14; color: white; }}
        .p2 {{ background: #ffc107; color: black; }}
        .alert {{
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #dc3545;
            background-color: #f8d7da;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <img src="file:///Users/administrator/Documents/PetesBrain/shared/assets/branding/roksys-logo-200x50.png" alt="ROK Systems">
            </div>
            <h1>Google Ads Weekly Report: {client_name}</h1>
            <div class="meta">Period: {period_dates} | Generated: {report_date}</div>
        </div>
        <div class="content">
            {html_body}
        </div>
    </div>
</body>
</html>"""

# Save HTML version
html_path = f"clients/{client_slug}/reports/weekly/{report_date}-weekly-report.html"
with open(html_path, 'w') as f:
    f.write(html_content)

# Track report generation in state file
state_file = Path("data/state/weekly-reports-generated.json")
state_file.parent.mkdir(parents=True, exist_ok=True)

if state_file.exists():
    with open(state_file, 'r') as f:
        state = json.load(f)
else:
    state = {"reports": []}

state["reports"].append({
    "client": client_name,
    "client_slug": client_slug,
    "date": report_date,
    "period": period_dates,
    "md_path": md_path,
    "html_path": html_path,
    "tasks_created": tasks_created_count,
    "generated_at": datetime.now().isoformat()
})

# Keep only last 30 days of reports in state
cutoff_date = (datetime.now() - timedelta(days=30)).isoformat()
state["reports"] = [r for r in state["reports"] if r["generated_at"] > cutoff_date]

with open(state_file, 'w') as f:
    json.dump(state, f, indent=2)
```

**File paths created:**
- Markdown: `clients/{client}/reports/weekly/YYYY-MM-DD-weekly-report.md`
- HTML: `clients/{client}/reports/weekly/YYYY-MM-DD-weekly-report.html`
- State: `data/state/weekly-reports-generated.json` (tracks all reports for summary email)

### 7. Create Tasks from Recommendations

**Smart Task Creation (Only for Critical Issues)**

Create tasks ONLY when:
1. Priority is **P0 (Critical/Urgent)**
   AND
2. Meets at least one threshold:
   - ✅ ROAS drops >20% WoW
   - ✅ Campaign with 0 conversions spending >£50/week
   - ✅ ROAS >15% below target
   - ✅ Identified waste >£100/month

This prevents task list flooding while catching genuine fires.

```python
from shared.client_tasks_service import ClientTasksService
from datetime import datetime, timedelta

service = ClientTasksService()

# For each P0 recommendation in the report:
for recommendation in prioritised_recommendations:
    priority = recommendation['priority']  # P0, P1, P2, P3

    # Only consider P0 (Critical/Urgent)
    if priority != 'P0':
        continue

    # Check if recommendation meets threshold criteria
    meets_threshold = False

    # Threshold 1: ROAS drop >20% WoW
    if recommendation.get('roas_wow_change_pp', 0) < -20:
        meets_threshold = True

    # Threshold 2: Zero conversion campaign with >£50/week spend
    if (recommendation.get('conversions', 1) == 0 and
        recommendation.get('weekly_spend', 0) > 50):
        meets_threshold = True

    # Threshold 3: ROAS >15% below target
    if (recommendation.get('roas_vs_target_pct', 0) < -15):
        meets_threshold = True

    # Threshold 4: Identified waste >£100/month
    if recommendation.get('monthly_waste', 0) > 100:
        meets_threshold = True

    # Only create task if threshold met
    if not meets_threshold:
        continue

    # Calculate due date based on timeline
    timeline = recommendation['timeline']  # TODAY, THIS WEEK, NEXT WEEK, etc.
    if timeline == 'TODAY' or timeline == 'URGENT':
        due_date = datetime.now().strftime('%Y-%m-%d')
    elif timeline == 'THIS WEEK':
        due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    elif timeline == 'NEXT WEEK':
        due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    else:
        due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    # Extract time estimate from recommendation (if specified)
    time_estimate = recommendation.get('time_estimate_mins', 60)  # Default 1 hour

    # Create task
    service.create_task(
        title=f"[{client_name}] {recommendation['title']}",
        client=client_slug,
        priority=priority,
        due_date=due_date,
        time_estimate_mins=time_estimate,
        notes=f"""**From Weekly Report - {report_date}**

**Issue:** {recommendation['issue']}

**Expected Impact:** {recommendation['impact']}

**Action:** {recommendation['action']}

**Supporting Data:** {recommendation.get('data', 'See weekly report for details')}
""",
        source=f"Weekly Report - {report_date}",
        tags=["weekly-report", "optimization", recommendation.get('category', 'general')],
        task_type="standalone"
    )
```

**Task Creation Rules:**
- ✅ Only create tasks for **P0 (Critical/Urgent)** recommendations
- ✅ P0 recommendation MUST meet threshold criteria (see above)
- ❌ Don't create tasks for P1/P2/P3 (informational only - stay in report)
- 📅 Timeline mapping:
  - "TODAY" or "URGENT" → Due today
  - "THIS WEEK" → Due in 7 days
  - "NEXT WEEK" → Due in 14 days
  - Default → Due in 7 days
- ⏱️ Time estimate defaults to 60 minutes if not specified in recommendation
- 🏷️ Tags: Always include ["weekly-report", "optimization"] + category + threshold type

**Threshold Examples:**

✅ **Creates task**: Go Glean Search campaign (0 conversions, £50 spend, £200/mo waste)
✅ **Creates task**: Godshot ROAS 534% vs 700% target (-24% below target)
✅ **Creates task**: Account ROAS drops 219% → 156% (-29% WoW)
❌ **No task**: Bright Minds performing well (390% ROAS, +7% WoW)
❌ **No task**: Minor optimization opportunity (+£100-200/mo)

**Confirmation Messages:**

If tasks created:
```
✅ Created {count} tasks from critical issues:
- {task1_title} (P0 - Due: {date}) [ROAS -63pp WoW]
- {task2_title} (P0 - Due: {date}) [£200/mo waste]

All tasks saved to clients/{client}/tasks.json
```

If no tasks created (performance stable):
```
ℹ️ No critical issues detected - all recommendations are informational.

Report contains {count} optimization opportunities (P1/P2) but none meet
threshold for automatic task creation. Review report for details.
```

### 8. Create Summary for User

Provide concise summary:

```
✅ Weekly Google Ads Report Generated

**Client:** [Name]
**Period:** [Dates]
**File:** clients/[client]/reports/weekly/YYYY-MM-DD-weekly-report.md

**Key Metrics:**
- Spend: £X,XXX (+X% WoW)
- ROAS: XXX% (+Xpp WoW)
- Conversions: XXX (+X% WoW)

**Top 3 Insights:**
1. [Insight]
2. [Insight]
3. [Insight]

**Action Required:**
[Most important recommendation]

Full report saved for client review.
```

---

## Special Handling

### For Shopping/PMax Campaigns:
- Include product-level analysis
- Flag products with declining performance
- Identify inventory or feed issues if products disappear from top performers

### For Search Campaigns:
- Include top search query performance
- Identify wasted spend on zero-conversion queries
- Highlight keyword opportunities

### For Lead Gen Clients (NDA, NMA):
- Replace "ROAS" with "Cost per Lead"
- Focus on lead volume and quality metrics
- Include conversion rate analysis

### For Multi-Market Clients (Superspace):
- Break down performance by market (UK vs US)
- Compare market-level ROAS
- Identify market-specific opportunities

---

## Error Handling

**If account ID not found:**
- Check CONTEXT.md exists
- Try mcp__google-ads__list_accounts to find account
- Ask user to provide account ID manually

**If no data returned:**
- Verify date range is valid
- Check if account has been active during period
- Try shorter date range (3 days instead of 7)

**If product data missing:**
- Note in report that product-level data unavailable
- Focus on campaign and placement analysis
- Recommend checking Merchant Centre feed status

---

## Testing Checklist

When testing this skill:

✅ Report generates in <5 minutes
✅ All calculations are accurate (manually verify ROAS for one campaign)
✅ Week-over-week changes correctly calculated
✅ At least 1 actionable insight identified
✅ Report is clear and client-friendly (no technical jargon)
✅ Markdown formatting renders correctly
✅ Recommendations are specific and prioritized

---

## Task Creation - What Gets Automated vs Not

### Examples from Phase 1A Testing

**This Week's Reports (Nov 18):**

| Client | Result | Reason |
|--------|--------|--------|
| **Go Glean** | ✅ 2 tasks created | Search campaign: 0 conv + £50 spend (Threshold 2) + £200/mo waste (Threshold 4)<br>PMax: ROAS 122% likely unprofitable (borderline, created due to 60% budget share) |
| **Godshot** | ✅ 1 task created | ROAS -24% vs target (meets Threshold 3: >15% below target)<br>Conversion tracking verification |
| **Bright Minds** | ❌ 0 tasks | Performing well (390% ROAS, +7% WoW improvement)<br>All recommendations are P2/P3 optimizations |

**Total**: 3 tasks from 3 clients (1 task per client average, 2 clients with issues, 1 clean)

**Weekly Automation Estimate:**
- With 16 clients running weekly reports
- Expect 3-5 tasks per week total (only critical issues)
- ~20% of clients will have P0 issues in any given week
- 80% of clients will have clean reports (optimizations documented but no tasks created)

---

## Notes

- This is adapted from GoMarble's comprehensive prompt
- Focus on **business impact** not technical metrics
- Use British English throughout (analyse, optimise)
- ROAS always expressed as percentage (420% not £4.20)
- Keep tone collaborative ("our" not "your")
- Prioritize recommendations by revenue impact
- **Task automation**: Only P0 + threshold criteria (prevents flooding)

---

**Last Updated:** 2025-11-19
**Status:** Phase 1A Complete - Smart task creation implemented
