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

Extract account ID using `mcp__platform-ids__get_client_platform_ids`

### 2. Calculate Comparison Periods & Pull Google Ads Data

**CRITICAL: Use the time_comparisons module for proper same-day alignment.**

**CRITICAL: Use the data_cleaning module for universal campaign name standardisation.**

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/shared')))
from time_comparisons import get_comparison_periods, parse_performance_data, calculate_changes, format_comparison_report
from data_cleaning import clean_campaign_name

# Get properly aligned date ranges (Monday-to-Monday, not date-to-date)
periods = get_comparison_periods('WoW')

# Example output:
# {
#   'current': {'start': '2025-12-09', 'end': '2025-12-15'},
#   'previous': {'start': '2025-12-02', 'end': '2025-12-08'}
# }

# Check for holiday flags that may affect comparisons
from time_comparisons import get_holiday_flags
holiday_flags = get_holiday_flags(periods['current']['start'], periods['current']['end'])
if holiday_flags:
    print(f"⚠️ Holiday period detected: {', '.join(holiday_flags)}")
```

Use `mcp__google-ads__run_gaql` to extract these metrics for **both current and previous periods**:

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

**IMPORTANT: Clean campaign names when processing results:**

```python
# When processing campaign data from API response:
campaigns = []
for result in api_response['results']:
    campaign = {
        'name_raw': result['campaign']['name'],  # Keep original for reference
        'name': clean_campaign_name(result['campaign']['name']),  # Use cleaned for display/grouping
        'id': result['campaign']['id'],
        'spend': result['metrics']['costMicros'] / 1_000_000,
        'conversions': result['metrics']['conversions'],
        'revenue': result['metrics']['conversionsValue']
    }
    campaigns.append(campaign)

# When grouping campaigns for analysis, use cleaned names:
campaign_groups = {}
for campaign in campaigns:
    clean_name = campaign['name']  # Already cleaned
    if clean_name not in campaign_groups:
        campaign_groups[clean_name] = {
            'spend': 0,
            'revenue': 0,
            'conversions': 0,
            'raw_names': []  # Track which raw names were combined
        }
    campaign_groups[clean_name]['spend'] += campaign['spend']
    campaign_groups[clean_name]['revenue'] += campaign['revenue']
    campaign_groups[clean_name]['conversions'] += campaign['conversions']
    campaign_groups[clean_name]['raw_names'].append(campaign['name_raw'])

# This ensures campaigns with different naming formats (underscores vs hyphens) are grouped correctly
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

### 3. Calculate Key Metrics & Time Comparisons

**Query both periods and parse results:**

```python
# Query current period
current_query = f"""
    SELECT
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value
    FROM customer
    WHERE
        segments.date >= '{periods['current']['start']}'
        AND segments.date <= '{periods['current']['end']}'
"""

current_result = mcp__google_ads__run_gaql(
    customer_id=customer_id,
    manager_id=manager_id,
    query=current_query
)

# Parse current period data
current_metrics = parse_performance_data(current_result)
# Returns: {'spend': 520.00, 'conversions': 12, 'revenue': 2080.00, 'roas': 4.0, 'cpa': 43.33}

# Query previous period (same structure)
previous_query = current_query.replace(
    periods['current']['start'], periods['previous']['start']
).replace(
    periods['current']['end'], periods['previous']['end']
)

previous_result = mcp__google_ads__run_gaql(
    customer_id=customer_id,
    manager_id=manager_id,
    query=previous_query
)

# Parse previous period data
previous_metrics = parse_performance_data(previous_result)

# Calculate changes with safeguards
changes = calculate_changes(current_metrics, previous_metrics)
# Returns: Changes for all metrics with flags for low volume, large changes, etc.

# Generate formatted comparison report section
comparison_report = format_comparison_report(
    client_name=client_name,
    periods=periods,
    changes=changes,
    comparison_type='WoW'
)
# This creates a complete markdown section ready to insert into the report
```

**Key Metrics Calculated Automatically:**
- **ROAS** = Conversion Value / Spend (as multiplier, e.g., 4.0x)
- **CPA** = Spend / Conversions
- **Absolute Change** = Current - Previous
- **Percentage Change** = ((Current - Previous) / Previous) × 100
- **Safeguard Flags** = LOW_VOLUME, LARGE_SPEND_CHANGE, LARGE_ROAS_CHANGE, etc.

### 4. Generate Insights (Data → Information → Insight)

**CRITICAL: This is where we move from information to insight.**

Use the InsightEngine to systematically analyse performance changes:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/shared')))
from insight_rules import InsightEngine

# Initialize insight engine
engine = InsightEngine()

# Generate account-level insights
account_insights = engine.generate_insights(
    current_metrics={
        'spend': current_spend,
        'revenue': current_revenue,
        'roas': current_roas,
        'conversions': current_conversions,
        'cpc': current_cpc,
        'cvr': current_cvr,
        'aov': current_aov
    },
    previous_metrics={
        'spend': previous_spend,
        'revenue': previous_revenue,
        'roas': previous_roas,
        'conversions': previous_conversions,
        'cpc': previous_cpc,
        'cvr': previous_cvr,
        'aov': previous_aov
    },
    target_roas=target_roas  # From CONTEXT.md if available
)

# Generate campaign-level insights for significant changes
campaign_insights = []
for campaign in campaigns:
    if campaign['roas_change_pct'] > 15 or campaign['roas_change_pct'] < -15:
        insights = engine.generate_insights(
            current_metrics=campaign['current'],
            previous_metrics=campaign['previous']
        )
        campaign_insights.extend(insights)
```

**What This Does:**

1. **Detects patterns** - Identifies ROAS drops, spikes, zero conversions, spend changes
2. **Diagnoses WHY** - "External competitive pressure" vs "Landing page issue" vs "Product mix"
3. **Recommends direction** - Specific actions based on diagnosis
4. **Sets priority** - P0 (critical) vs P1 (important) vs P2 (monitor)

**Example Output:**

```python
{
    'type': 'roas_drop',
    'title': 'ROAS dropped 14% WoW',
    'what_changed': 'ROAS decreased from 420% to 360% (-14%)',
    'why_it_happened': 'CPC increased 22% while conversion rate remained stable at 4.2%. This indicates auction competition increased, not a performance issue.',
    'diagnosis': 'External competitive pressure',
    'recommended_direction': [
        'Test improved ad copy to increase Quality Score and reduce CPC',
        'Add exact match keywords to reduce waste from broad match',
        'Check Auction Insights for new competitors'
    ],
    'priority': 'P1'
}
```

### 5. Generate Markdown Report

Create report with these sections:

```markdown
# Google Ads Weekly Report: [Client Name]
**Period:** [Start Date] - [End Date]
**Generated:** [Today's Date]

---

## Week over Week Performance Comparison

{comparison_report}

<!-- This section is automatically generated by format_comparison_report() -->
<!-- It includes:
     - Current vs Previous period dates
     - Safeguard flags (LOW_VOLUME, LARGE_ROAS_CHANGE, etc.)
     - Metrics table with absolute + percentage changes
     - Quick insights based on significant changes
-->

---

## Executive Summary

### Account Performance (LEVEL 2: Information)

| Metric | This Week | Last Week | Change | Trend |
|--------|-----------|-----------|--------|-------|
| Spend | £X,XXX | £X,XXX | +X% | [sparkline] |
| Conversions | XXX | XXX | +X% | [sparkline] |
| Conv Value | £XX,XXX | £XX,XXX | +X% | [sparkline] |
| ROAS | XXX% | XXX% | +Xpp | [sparkline] |
| CPA | £XXX | £XXX | -X% | [sparkline] |
| CTR | X.X% | X.X% | +X% | [sparkline] |
| Avg CPC | £X.XX | £X.XX | +X% | [sparkline] |

**This tells you WHAT changed, but not WHY or what to do about it.**

---

## Performance Analysis (LEVEL 3: Insight)

**This section explains WHY metrics changed and suggests direction.**

{for each insight generated by InsightEngine}

### {insight['title']} {priority_badge}

**What Changed:**
{insight['what_changed']}

**Why It Happened:**
{insight['why_it_happened']}

**Diagnosis:** {insight['diagnosis']}

**Recommended Direction:**
{for each recommendation in insight['recommended_direction']}
- {recommendation}
{end for}

**Supporting Data:**
- Current ROAS: {insight['metrics']['current_roas']:.0f}%
- Previous ROAS: {insight['metrics']['previous_roas']:.0f}%
- CPC Change: {insight['metrics']['cpc_change_pct']:+.0f}%
- CVR Change: {insight['metrics']['cvr_change_pct']:+.0f}%

---

{end for}

**If no significant insights:** "Performance stable - no major changes detected this week."

---

## Campaign Breakdown

**IMPORTANT: Use cleaned campaign names in all tables. If multiple raw names were combined, note this.**

### Top Performing Campaigns
| Campaign | Spend | Conv | ROAS | WoW Change |
|----------|-------|------|------|------------|
| SMY \| UK \| P Max \| Diaries | £2,450 | 24 | 420% | +15% |
| DEV \| Search \| Brand \| The Fell | £1,100 | 18 | 380% | +8% |
| ... | ... | ... | ... | ... |

**If campaigns were grouped (multiple raw names combined):**
```markdown
| Campaign | Spend | Conv | ROAS | WoW Change | Notes |
|----------|-------|------|------|------------|-------|
| UK \| Brand \| Core Max | £2,000 | 28 | 408% | +12% | *Combined: 2 campaigns* |
```

### Campaigns Requiring Attention
[List campaigns with >15% negative change or poor performance using cleaned names]

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

## Framework Diagnostic Check

**ONLY INCLUDE THIS SECTION IF STRUCTURAL ISSUES DETECTED**

**Conditions that trigger framework diagnostic:**
- ≥3 campaigns with Lost IS Budget >10% (suggests budget allocation issue → Framework 5.5)
- ≥2 campaigns with 0 conversions spending >£50/week (suggests structural issue → Framework 4.4)
- Campaign ROAS variance >3x (best ROAS / worst ROAS >3) (suggests account structure issue → Framework 5.2)
- Search Partners spending >10% of budget AND ROAS <50% of Google Search (→ Framework 5.14)
- ≥4 consecutive weeks of declining performance (>5% decline each week) (suggests deeper audit needed)

**If any condition met, add brief diagnostic section:**

```
---

## 🔍 Structural Issue Detected

This week's data suggests a potential structural issue that may require a comprehensive audit:

**Issue Pattern**: [Brief description - e.g., "Budget constraints limiting 3 high-ROAS campaigns"]
**Framework Section**: [Section reference - e.g., "Framework 5.5 - Budget Allocation"]
**Recommended Action**: [e.g., "Schedule comprehensive campaign audit to review budget allocation strategy"]

*This is not urgent for this week's optimisation, but should be addressed in next monthly review.*
```

**If NO structural issues detected, skip this section entirely** (don't add noise to report)

---

## Appendix: Data Notes

- ROAS calculated as: Conversion Value / Spend × 100
- "Week-over-week" compares [dates] vs [dates]
- Product data limited to top 100 by conversion value
- Placement data aggregated across all campaigns

---

**Next Review:** [Next week's date]
```

### 6. Generate Charts

**CRITICAL: Always generate visual charts to make data instantly scannable.**

Use the chart_generator module to create PNG charts for the report:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync/shared')))
from chart_generator import ChartGenerator

generator = ChartGenerator()
charts_dir = Path(f"clients/{client_slug}/reports/weekly")
charts_dir.mkdir(parents=True, exist_ok=True)

# Prepare data for charts
# (Extract from API response data collected in steps 2-4)

# 1. ROAS Trend Line Chart (REQUIRED - shows performance direction)
roas_chart_data = {
    'dates': daily_dates,  # List of dates from current week
    'series': {
        'Performance Max': pmax_daily_roas,    # Daily ROAS values
        'Search': search_daily_roas,
        'Shopping': shopping_daily_roas
    }
}

roas_chart_path = generator.line_chart(
    dates=roas_chart_data['dates'],
    series=roas_chart_data['series'],
    title=f'{client_name} - ROAS Trend ({date_range})',
    y_label='ROAS (%)',
    output_path=str(charts_dir / f'{report_date}-roas-trend.png')
)

# 2. Campaign Spend Bar Chart (REQUIRED - shows budget allocation)
campaign_labels = [c['name'] for c in top_campaigns]  # Campaign names
campaign_spend = [c['spend'] for c in top_campaigns]  # Spend values

spend_chart_path = generator.bar_chart(
    labels=campaign_labels,
    values=campaign_spend,
    title=f'{client_name} - Top Campaigns by Spend ({date_range})',
    x_label='Spend (£)',
    output_path=str(charts_dir / f'{report_date}-campaigns-spend.png'),
    limit=10  # Top 10 only
)

# 3. Conversion Trend Line Chart (OPTIONAL - for high-volume accounts)
if total_weekly_conversions > 50:  # Only if meaningful volume
    conv_chart_path = generator.line_chart(
        dates=daily_dates,
        series={'Conversions': daily_conversions},
        title=f'{client_name} - Conversion Trend ({date_range})',
        y_label='Conversions',
        output_path=str(charts_dir / f'{report_date}-conversions-trend.png'),
        show_legend=False  # Single series
    )

# 4. Top Products Bar Chart (FOR E-COMMERCE ONLY)
if top_products:  # If shopping/PMax data available
    product_labels = [p['title'][:40] for p in top_products[:10]]  # Truncate long names
    product_revenue = [p['revenue'] for p in top_products[:10]]

    products_chart_path = generator.bar_chart(
        labels=product_labels,
        values=product_revenue,
        title=f'{client_name} - Top Products by Revenue ({date_range})',
        x_label='Revenue (£)',
        output_path=str(charts_dir / f'{report_date}-top-products.png'),
        limit=10
    )

# 5. Generate ASCII Sparklines for Summary Table
# Add sparklines to account metrics table for inline trends
account_sparklines = {
    'spend': generator.ascii_sparkline(daily_spend),
    'conversions': generator.ascii_sparkline(daily_conversions),
    'roas': generator.ascii_sparkline(daily_roas)
}

# Use sparklines in markdown table:
# | Metric | This Week | Last Week | Change | Trend |
# | Spend  | £2,450    | £2,100    | +16.7% | ╱╱─╱  |
# | ROAS   | 420%      | 390%      | +30pp  | ─╱╱╱  |
```

**Chart File Naming Convention:**
- `YYYY-MM-DD-roas-trend.png` - ROAS line chart
- `YYYY-MM-DD-campaigns-spend.png` - Campaign spend bar chart
- `YYYY-MM-DD-conversions-trend.png` - Conversions line chart
- `YYYY-MM-DD-top-products.png` - Products bar chart

**Chart Requirements:**
- ✅ ROAS trend line chart (ALWAYS)
- ✅ Campaign spend bar chart (ALWAYS)
- ✅ ASCII sparklines in summary table (ALWAYS)
- ✅ Products bar chart (E-COMMERCE ONLY)
- ⚠️ Conversions trend (OPTIONAL - only if >50 conversions/week)

### 7. Save Report

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
            <!-- CHARTS SECTION -->
            <div class="charts-section" style="margin-bottom: 30px;">
                <h2 style="color: #059669; border-bottom: 2px solid #10B981; padding-bottom: 10px;">Performance Charts</h2>

                <!-- ROAS Trend Chart -->
                <div class="chart-container" style="margin: 20px 0;">
                    <img src="{report_date}-roas-trend.png"
                         alt="ROAS Trend"
                         style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px;">
                </div>

                <!-- Campaign Spend Chart -->
                <div class="chart-container" style="margin: 20px 0;">
                    <img src="{report_date}-campaigns-spend.png"
                         alt="Top Campaigns by Spend"
                         style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px;">
                </div>

                <!-- Optional: Products Chart (if e-commerce) -->
                <!-- Uncomment if products chart generated -->
                <!--
                <div class="chart-container" style="margin: 20px 0;">
                    <img src="{report_date}-top-products.png"
                         alt="Top Products"
                         style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px;">
                </div>
                -->
            </div>

            <!-- REPORT BODY -->
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

### 7. Create Tasks from Insights (LEVEL 4: Action)

**CRITICAL: Tasks are created from INSIGHTS, not arbitrary thresholds.**

Create tasks from insights that meet criteria:

1. **Priority P0 or P1** (from InsightEngine diagnosis)
2. **Clear action required** (not just "monitor")
3. **Measurable impact** (revenue opportunity or waste reduction)

```python
from shared.client_tasks_service import ClientTasksService
from datetime import datetime, timedelta

service = ClientTasksService()

# For each insight from InsightEngine:
for insight in account_insights + campaign_insights:
    priority = insight['priority']  # P0, P1, P2, P3 (set by engine)

    # Only create tasks for P0 (critical) and P1 (important)
    if priority not in ['P0', 'P1']:
        continue

    # For P1 tasks, only create if actionable (not just "monitor")
    if priority == 'P1':
        # Check if recommended_direction contains actionable items
        actionable_keywords = ['test', 'add', 'check', 'review', 'consider', 'increase', 'reduce', 'pause']
        has_action = any(
            any(keyword in rec.lower() for keyword in actionable_keywords)
            for rec in insight['recommended_direction']
        )
        if not has_action:
            continue  # Skip "monitor only" insights

    # Calculate due date based on priority
    if priority == 'P0':
        due_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')  # Urgent - 2 days
    else:
        due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')  # This week

    # Convert recommended directions to task notes
    action_items = '\n'.join([f'- {rec}' for rec in insight['recommended_direction']])

    # Create task with insight context
    service.create_task(
        title=f"[{client_name}] {insight['title']}",
        client=client_slug,
        priority=priority,
        due_date=due_date,
        time_estimate_mins=60,  # Default 1 hour
        notes=f"""**From Weekly Report - {report_date}**

**What Changed:**
{insight['what_changed']}

**Why It Happened:**
{insight['why_it_happened']}

**Diagnosis:** {insight['diagnosis']}

**Recommended Actions:**
{action_items}

**Supporting Metrics:**
{json.dumps(insight['metrics'], indent=2)}

Full report: clients/{client_slug}/reports/weekly/{report_date}-weekly-report.md
""",
        source=f"Weekly Report - {report_date}",
        tags=["weekly-report", "insight-driven", insight['type']],
        task_type="standalone",
        context={
            'insight_type': insight['type'],
            'diagnosis': insight['diagnosis'],
            'metrics': insight['metrics']
        }
    )

    print(f"✅ Created task: [{client_name}] {insight['title']} ({priority})")
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
**Files:**
- Markdown: clients/[client]/reports/weekly/YYYY-MM-DD-weekly-report.md
- HTML: clients/[client]/reports/weekly/YYYY-MM-DD-weekly-report.html

**Charts Generated:**
- ✓ ROAS trend line chart
- ✓ Campaign spend bar chart
- ✓ ASCII sparklines in summary table
[- ✓ Top products bar chart (e-commerce)]

**Key Metrics:**
- Spend: £X,XXX (+X% WoW) [sparkline: ╱╱─╱]
- ROAS: XXX% (+Xpp WoW) [sparkline: ─╱╱╱]
- Conversions: XXX (+X% WoW) [sparkline: ╱─╱─]

**Top 3 Insights:**
1. [Insight]
2. [Insight]
3. [Insight]

**Action Required:**
[Most important recommendation]

Full report with charts saved for client review.
Open HTML file in browser to view formatted report with embedded charts.
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
- **Campaign name cleaning**: Universal cleaning function standardises campaign names across all clients (2025-12-17)
  - Preserves good formats (campaigns already using " | " separator)
  - Cleans old formats (underscores, hyphens → standard " | " format)
  - Groups campaign variations correctly (e.g., "UK_Brand_Core" and "UK-brand-core" → "UK | Brand | Core")
  - Zero risk - only cleans at reporting level, never touches Google Ads

---

**Last Updated:** 2025-12-17
**Status:** Phase 1A Complete - Smart task creation + Universal campaign name cleaning integrated
