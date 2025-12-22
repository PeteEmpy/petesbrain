# Chart Generation Guide

Complete guide to automated chart generation for Google Ads reporting in PetesBrain.

**Professional chart automation principles for data-driven reporting.**

---

## Table of Contents

- [Overview](#overview)
- [Chart Types](#chart-types)
- [Quick Start](#quick-start)
- [Module Reference](#module-reference)
- [Integration Examples](#integration-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

### Why Charts Matter for Automation

When you automate reporting, charts transform raw data into **cognitive shortcuts**. The right chart lets you spot a trend in 0.5 seconds. The wrong chart forces you to read every number, defeating the entire purpose of automation.

**The Progression:**
- **Phase 1 (Manual)**: Collect data → Manually create charts → Send report
- **Phase 2 (Semi-Auto)**: Automate data collection → Manually create charts → Send report
- **Phase 3 (Fully Auto)**: Automate data collection → **Automate chart generation** → Automated delivery

**You're implementing Phase 3.**

### Architecture

```
Input (Google Ads API)
    ↓
Process (chart_generator.py)
    ↓
Output (PNG images + HTML emails)
```

**Modules:**
- `shared/chart_generator.py` - Core chart generation (matplotlib)
- `shared/google_sheets_charts.py` - Google Sheets integration
- `shared/email_template.py` - Email embedding
- `.claude/skills/google-ads-weekly-report/` - Weekly report automation

---

## Chart Types

### Line Charts (Trends Over Time)

**Use for:** Performance metrics over days, weeks, months

**Best for:**
- ROAS trend (last 30 days)
- Conversion volume (week-over-week)
- CPA trend (quarterly)

**Why it works:** Your brain recognizes slopes instantly. Upward = good. Downward = investigate.

**Example:**
```python
from shared.chart_generator import ChartGenerator

generator = ChartGenerator()
generator.line_chart(
    dates=['2025-12-01', '2025-12-02', '2025-12-03'],
    series={
        'Performance Max': [420, 435, 450],
        'Search': [380, 390, 385],
        'Shopping': [350, 360, 355]
    },
    title='ROAS Trend - Last 7 Days',
    y_label='ROAS (%)',
    output_path='clients/smythson/reports/roas-trend.png'
)
```

**Visual Example:**
```
450 |           ●━●
    |         ●╱
420 |     ●━●╱
    |   ●╱
390 | ●╱
    |________________________
      Mon Tue Wed Thu Fri
```

### Bar Charts (Category Comparisons)

**Use for:** Rankings, "which is best/worst?"

**Best for:**
- Top 10 campaigns by spend
- Ad groups ranked by conversion rate
- Products by revenue

**Why it works:** Bar length = visual magnitude. Brain instantly ranks without counting.

**Example:**
```python
generator.bar_chart(
    labels=['Campaign A', 'Campaign B', 'Campaign C'],
    values=[2450, 1850, 1200],
    title='Top Campaigns by Spend',
    x_label='Spend (£)',
    output_path='clients/smythson/reports/campaigns-spend.png',
    orientation='horizontal',  # Better for long campaign names
    limit=10  # Top 10 only
)
```

**Visual Example:**
```
Campaign A ████████████████ £2,450
Campaign B ████████████     £1,850
Campaign C ████████         £1,200
```

### Sparklines (Context in Cells)

**Use for:** Adding trend context to summary tables

**Best for:**
- Weekly budget tracking
- Conversion table trends
- Dashboard summaries

**Why it works:** NUMBER + DIRECTION in one glance. "£2,450 ╱╱─" tells a different story than "£2,450 ╲╲─"

**Example:**
```python
# ASCII sparklines (for markdown tables)
sparkline = generator.ascii_sparkline([100, 120, 115, 130, 125])
# Returns: '╱╱─╱─'

# Use in table:
# | Metric | Value  | Trend |
# | ROAS   | 420%   | ╱╱─╱─ |
# | Spend  | £2,450 | ─╱╱╱  |
```

**Google Sheets sparklines:**
```python
formula = generator.google_sheets_sparkline_formula('B2:B8')
# Returns: =SPARKLINE(B2:B8, {"charttype","line";"color","#10B981";"linewidth",2})
```

### What NOT to Do

**NEVER use pie charts.** They're universally terrible:
- Humans can't judge angles accurately
- Hard to compare slices
- Useless with >3 categories
- Always harder to read than a bar chart

**Bad:**
```
🥧 Campaign Spend Distribution
(You squint, try to figure out which slice is bigger, fail)
```

**Good:**
```
Bar Chart: Campaign Spend
Campaign A ████████████████ £2,450 (45%)
Campaign B ████████████     £1,850 (34%)
Campaign C ████████         £1,200 (21%)
```

---

## Quick Start

### 1. Basic Line Chart (5 minutes)

```python
from shared.chart_generator import quick_line_chart

quick_line_chart(
    dates=['2025-12-09', '2025-12-10', '2025-12-11'],
    values=[420, 435, 450],
    title='ROAS Trend',
    metric_name='ROAS (%)',
    output_path='/tmp/roas-test.png'
)
```

**Result:** PNG image saved to `/tmp/roas-test.png`

### 2. Basic Bar Chart (5 minutes)

```python
from shared.chart_generator import quick_bar_chart

quick_bar_chart(
    labels=['Campaign A', 'Campaign B', 'Campaign C'],
    values=[2450, 1850, 1200],
    title='Top Campaigns',
    output_path='/tmp/campaigns-test.png'
)
```

**Result:** PNG image with sorted bars (highest to lowest)

### 3. Add Sparklines to Table (5 minutes)

```python
from shared.chart_generator import ChartGenerator

generator = ChartGenerator()

# Generate sparkline
values = [100, 120, 115, 130, 125, 140, 135]
sparkline = generator.ascii_sparkline(values)

print(f"Values: {values}")
print(f"Trend: {sparkline}")
# Output:
# Values: [100, 120, 115, 130, 125, 140, 135]
# Trend: ╱╲╱╲╱╲
```

**Result:** ASCII sparkline ready for markdown tables

---

## Module Reference

### ChartGenerator Class

**Location:** `shared/chart_generator.py`

**Methods:**

#### `line_chart()`

```python
generator.line_chart(
    dates: List[str],           # ['2025-12-01', '2025-12-02', ...]
    series: Dict[str, List],    # {'Performance Max': [420, 435, ...]}
    title: str,                 # Chart title
    y_label: str,               # Y-axis label
    output_path: str,           # Where to save PNG
    x_label: str = 'Date',      # X-axis label (optional)
    figsize: Tuple = (12, 6),   # Figure size (optional)
    show_legend: bool = True,   # Show legend (optional)
    date_format: str = '%Y-%m-%d'  # Date parsing format (optional)
) -> Path
```

**Returns:** Path object of saved chart

**Example:**
```python
generator.line_chart(
    dates=['2025-12-09', '2025-12-10', '2025-12-11'],
    series={'ROAS': [420, 435, 450]},
    title='ROAS Trend',
    y_label='ROAS (%)',
    output_path='clients/smythson/reports/roas.png'
)
```

#### `bar_chart()`

```python
generator.bar_chart(
    labels: List[str],          # ['Campaign A', 'Campaign B', ...]
    values: List[float],        # [2450, 1850, 1200]
    title: str,                 # Chart title
    x_label: str,               # X-axis label
    output_path: str,           # Where to save PNG
    orientation: str = 'horizontal',  # 'horizontal' or 'vertical'
    sort_by_value: bool = True,       # Sort bars by value
    limit: int = None,                # Limit to top N
    figsize: Tuple = (10, 8),         # Figure size
    value_format: str = '£{:,.0f}',   # Value label format
    show_values: bool = True          # Show value labels
) -> Path
```

**Returns:** Path object of saved chart

**Example:**
```python
generator.bar_chart(
    labels=['Campaign A', 'Campaign B', 'Campaign C'],
    values=[2450, 1850, 1200],
    title='Top Campaigns',
    x_label='Spend (£)',
    output_path='clients/smythson/reports/campaigns.png',
    limit=10  # Top 10 only
)
```

#### `ascii_sparkline()`

```python
generator.ascii_sparkline(
    values: List[float],   # [100, 120, 115, 130]
    length: int = None     # Optional length (defaults to len(values) - 1)
) -> str
```

**Returns:** ASCII sparkline string (e.g., '╱╱─╱─')

**Example:**
```python
sparkline = generator.ascii_sparkline([100, 120, 115, 130, 125])
# Returns: '╱╱─╱─'
```

**Characters Used:**
- `╱` = Rising trend
- `╲` = Falling trend
- `─` = Flat (< 5% change)

#### `google_sheets_sparkline_formula()`

```python
generator.google_sheets_sparkline_formula(
    range_ref: str,           # 'B2:B8'
    chart_type: str = 'line', # 'line', 'bar', 'column', 'winloss'
    options: Dict = None      # Optional chart options
) -> str
```

**Returns:** Google Sheets formula string

**Example:**
```python
formula = generator.google_sheets_sparkline_formula('B2:B8')
# Returns: =SPARKLINE(B2:B8, {"charttype","line";"color","#10B981";"linewidth",2})
```

#### `create_google_ads_template_charts()`

```python
generator.create_google_ads_template_charts(
    client: str,           # 'Smythson'
    data: Dict,            # Report data
    date_range: str,       # '9-15 December 2025'
    output_dir: str        # 'clients/smythson/reports/weekly'
) -> Dict[str, Path]
```

**Returns:** Dict mapping chart_name → Path

**Example:**
```python
charts = generator.create_google_ads_template_charts(
    client='Smythson',
    data={
        'dates': ['2025-12-09', ...],
        'roas': {'Performance Max': [420, ...], 'Search': [380, ...]},
        'campaigns': {'Campaign A': 2450, 'Campaign B': 1850}
    },
    date_range='9-15 December 2025',
    output_dir='clients/smythson/reports/weekly'
)

# Returns:
# {
#     'roas_trend': Path('clients/smythson/reports/weekly/roas-trend.png'),
#     'campaigns_spend': Path('clients/smythson/reports/weekly/campaigns-spend.png')
# }
```

### Email Template Functions

**Location:** `shared/email_template.py`

#### `embed_chart()`

```python
from shared.email_template import embed_chart

chart_html = embed_chart(
    chart_path: str,           # 'roas-trend.png' (relative to email)
    alt_text: str,             # 'ROAS Trend'
    caption: str = None,       # Optional caption below chart
    max_width: str = "100%"    # Max width
) -> str
```

**Returns:** HTML string for chart embedding

**Example:**
```python
html = embed_chart(
    chart_path='2025-12-16-roas-trend.png',
    alt_text='ROAS Trend - Last 7 Days',
    caption='ROAS trending upward, driven by Performance Max'
)
```

#### `render_performance_email_with_charts()`

```python
from shared.email_template import render_performance_email_with_charts

email = render_performance_email_with_charts(
    recipient_name: str,       # 'Barry'
    client: str,               # 'Bright Minds'
    week_range: str,           # '9-15 December 2025'
    key_metrics: Dict,         # {'spend': '£2,450', 'roas': '420%', ...}
    charts: Dict[str, str],    # {'roas_trend': '2025-12-16-roas-trend.png', ...}
    insights: List[str],       # ['ROAS up 30pp', ...]
    recommendations: List = None,  # Optional recommendations
    sender_name: str = "Peter",
    sign_off: str = "Regards"
) -> str
```

**Returns:** Complete HTML email with embedded charts

**Example:**
```python
email = render_performance_email_with_charts(
    recipient_name="Barry",
    client="Bright Minds",
    week_range="9-15 December 2025",
    key_metrics={
        'spend': '£2,450',
        'roas': '420%',
        'conversions': '65',
        'spend_change': '+12%',
        'roas_change': '+30pp'
    },
    charts={
        'roas_trend': '2025-12-16-roas-trend.png',
        'campaigns_spend': '2025-12-16-campaigns-spend.png'
    },
    insights=[
        'ROAS improving steadily, up 30pp week-over-week',
        'Performance Max driving 60% of revenue'
    ],
    recommendations=[
        'Increase Performance Max budget by £200/week'
    ]
)
```

---

## Integration Examples

### Weekly Report Skill

The `google-ads-weekly-report` skill automatically generates charts:

**Workflow:**
1. Pull Google Ads data (via MCP)
2. **Generate charts** (NEW)
3. Create markdown report
4. Create HTML report with embedded charts
5. Save files and summary

**Usage:**
```
Skill(command='google-ads-weekly-report')
# User confirms client and date range
# Skill automatically generates charts and includes in report
```

**Output Files:**
```
clients/smythson/reports/weekly/
├── 2025-12-16-weekly-report.md
├── 2025-12-16-weekly-report.html
├── 2025-12-16-roas-trend.png
├── 2025-12-16-campaigns-spend.png
└── 2025-12-16-top-products.png
```

### Custom Report Script

```python
#!/usr/bin/env python3
"""
Custom weekly report with charts
"""

from shared.chart_generator import ChartGenerator
from shared.email_template import render_performance_email_with_charts, save_email_draft

# Assume you've fetched data from Google Ads API
dates = ['2025-12-09', '2025-12-10', '2025-12-11', '2025-12-12', '2025-12-13']
roas_values = [420, 435, 428, 450, 445]
campaigns = {'Performance Max': 2450, 'Search': 1850, 'Shopping': 1200}

# Generate charts
generator = ChartGenerator()

roas_chart = generator.line_chart(
    dates=dates,
    series={'ROAS': roas_values},
    title='ROAS Trend',
    y_label='ROAS (%)',
    output_path='clients/smythson/reports/roas-trend.png',
    show_legend=False
)

campaigns_chart = generator.bar_chart(
    labels=list(campaigns.keys()),
    values=list(campaigns.values()),
    title='Top Campaigns by Spend',
    x_label='Spend (£)',
    output_path='clients/smythson/reports/campaigns-spend.png'
)

# Create email with charts
email_html = render_performance_email_with_charts(
    recipient_name="Alex",
    client="Smythson",
    week_range="9-15 December 2025",
    key_metrics={
        'spend': '£5,500',
        'roas': '440%',
        'conversions': '142',
        'spend_change': '+8%',
        'roas_change': '+15pp'
    },
    charts={
        'roas_trend': 'roas-trend.png',
        'campaigns_spend': 'campaigns-spend.png'
    },
    insights=[
        'ROAS up 15pp driven by improved PMax performance',
        'Search efficiency improving (+12% conversion rate)',
        'Budget pacing on track for monthly target'
    ]
)

# Save and open
save_email_draft(
    email_html,
    'clients/smythson/documents/email-draft-weekly-update.html',
    open_in_browser=True
)

print("✅ Charts and email generated")
```

### Daily Briefing Enhancement

```python
# In your daily briefing script
from shared.chart_generator import ChartGenerator

generator = ChartGenerator()

# Add sparklines to metrics
daily_spend = [450, 480, 425, 510, 475, 490, 520]
spend_sparkline = generator.ascii_sparkline(daily_spend)

daily_roas = [420, 435, 428, 450, 445, 455, 460]
roas_sparkline = generator.ascii_sparkline(daily_roas)

# Include in briefing email
briefing = f"""
**Yesterday's Performance:**

| Metric | Value  | 7-Day Trend |
|--------|--------|-------------|
| Spend  | £520   | {spend_sparkline} |
| ROAS   | 460%   | {roas_sparkline} |

Performance trending positively across all metrics.
"""
```

---

## Best Practices

### Chart Design Principles

1. **Trend = Line Chart** (performance over time)
2. **Comparison = Bar Chart** (which is bigger/smaller?)
3. **Context = Sparklines** (trend + number in one cell)
4. **Never = Pie Chart** (always harder than bar chart)
5. **Sort by Value** (not alphabetically—magnitude matters)
6. **Limit Lines** (3-4 max on one chart—more = noise)
7. **Automation-First** (manual charting defeats the purpose)

### File Naming Convention

Use consistent, date-prefixed naming:

```
YYYY-MM-DD-{chart-type}.png

Examples:
- 2025-12-16-roas-trend.png
- 2025-12-16-campaigns-spend.png
- 2025-12-16-top-products.png
- 2025-12-16-conversions-trend.png
```

**Why:** Easy to:
- Sort chronologically
- Find latest charts
- Delete old charts
- Reference in emails

### Chart Storage

Store charts alongside reports:

```
clients/{client}/reports/weekly/
├── YYYY-MM-DD-weekly-report.md
├── YYYY-MM-DD-weekly-report.html
├── YYYY-MM-DD-roas-trend.png          ← Charts here
├── YYYY-MM-DD-campaigns-spend.png
└── YYYY-MM-DD-top-products.png
```

**Why:**
- Charts stay with reports
- Self-contained weekly folders
- Easy to archive
- Email HTML references relative paths

### Performance Optimisation

**Chart Generation is Fast:**
- Line chart: ~0.5 seconds
- Bar chart: ~0.3 seconds
- Sparkline: <0.01 seconds

**Total overhead for weekly report:** ~2 seconds (3 charts)

**If slow:**
- Use `figsize=(10, 6)` instead of `(16, 10)` (smaller = faster)
- Reduce DPI from 150 to 100 (lower quality but faster)
- Limit data points (e.g., last 30 days instead of 90)

### Accessibility

**Always include:**
- Alt text for images
- Captions for context
- Fallback text in emails (plain text version)

**Example:**
```python
embed_chart(
    chart_path='roas-trend.png',
    alt_text='ROAS Trend showing upward trajectory from 420% to 460% over 7 days',
    caption='ROAS increasing steadily, driven by Performance Max optimisations'
)
```

---

## Troubleshooting

### Charts Not Generating

**Symptom:** No PNG files created

**Check:**
1. Output directory exists?
   ```python
   from pathlib import Path
   output = Path('clients/smythson/reports/weekly')
   output.mkdir(parents=True, exist_ok=True)
   ```

2. Permissions correct?
   ```bash
   ls -la clients/smythson/reports/
   ```

3. Matplotlib installed?
   ```bash
   python3 -c "import matplotlib; print(matplotlib.__version__)"
   ```

**Fix:**
```bash
pip install matplotlib
```

### Charts Show But Look Wrong

**Symptom:** Chart displays but formatting is off

**Common Issues:**

1. **ROK colors not showing:**
   ```python
   # Check COLORS dict in chart_generator.py
   from shared.chart_generator import COLORS
   print(COLORS)  # Should show ROK greens
   ```

2. **Font too small:**
   ```python
   generator.line_chart(..., figsize=(16, 10))  # Bigger = easier to read
   ```

3. **Labels overlapping:**
   ```python
   # For bar charts, use horizontal orientation
   generator.bar_chart(..., orientation='horizontal')
   ```

### Sparklines Not Rendering

**Symptom:** Sparkline shows as '─────' (all flat)

**Cause:** All values identical

**Check:**
```python
values = [100, 100, 100, 100]  # All same = flat line
sparkline = generator.ascii_sparkline(values)
# Returns: '───'  (correct behaviour)
```

**Fix:** Ensure you're passing actual varying data

### Charts in Email Not Loading

**Symptom:** Email shows broken image icons

**Cause:** Incorrect relative paths

**Check:**
1. Email HTML location: `clients/smythson/documents/email-draft.html`
2. Chart location: `clients/smythson/reports/weekly/roas-trend.png`
3. Relative path from email to chart: `../reports/weekly/roas-trend.png`

**Fix:**
```python
# Use relative paths in email embedding
embed_chart(
    chart_path='../reports/weekly/2025-12-16-roas-trend.png',  # Relative to email location
    alt_text='ROAS Trend'
)
```

**Or use absolute paths (if email is in same directory as charts):**
```python
embed_chart(
    chart_path='2025-12-16-roas-trend.png',  # Same directory
    alt_text='ROAS Trend'
)
```

---

## Advanced Usage

### Custom Chart Styles

```python
generator = ChartGenerator(style='minimal')  # Clean, minimal style

# Or customise matplotlib params directly
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = False  # No grid
```

### Multi-Period Comparisons

```python
# Compare this week vs last week on same chart
generator.line_chart(
    dates=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    series={
        'This Week': [420, 435, 428, 450, 445, 455, 460],
        'Last Week': [380, 390, 385, 395, 390, 400, 410]
    },
    title='ROAS Week-over-Week Comparison',
    y_label='ROAS (%)',
    output_path='clients/smythson/reports/roas-wow.png'
)
```

### Annotated Charts

```python
# Add annotations for important events
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(dates, roas_values, marker='o', linewidth=2.5, color='#10B981')

# Annotate spike
ax.annotate(
    'Black Friday spike',
    xy=(dates[5], roas_values[5]),
    xytext=(dates[5], roas_values[5] + 50),
    arrowprops=dict(facecolor='black', shrink=0.05)
)

plt.savefig('clients/smythson/reports/roas-annotated.png', dpi=150)
```

---

## Connection to AI Automation Journey

This chart system fits into **Phase 1: Automated Reporting** of the Ads to AI Skill Map:

### Phase 1: Automated Reporting (Current)
- ✅ **Input:** Automated data collection (Google Ads API)
- ✅ **Process:** Automated chart generation (this system)
- ✅ **Output:** Automated delivery (email, dashboard)

**You've built systems that run themselves.** Charts are the OUTPUT layer—the interface between automation and human decision-making.

### Bridge to Phase 2: AI Analysis

Once you have automated charts:
1. **AI interprets charts** ("ROAS trending down, investigate PMax")
2. **AI annotates charts** ("Spike on Dec 12 = promo")
3. **AI recommends actions** ("Bar chart shows Campaign B overspending—reduce 15%")

**The progression:**
- Phase 1: Charts show WHAT happened (automated) ← **You are here**
- Phase 2: AI explains WHY it happened (AI analysis)
- Phase 3: System does this without asking (scheduled insights)
- Phase 6: AI executes within guidelines (autonomous agents)

---

## Reference

**Key Files:**
- `shared/chart_generator.py` - Core chart generation module
- `shared/google_sheets_charts.py` - Google Sheets integration
- `shared/email_template.py` - Email embedding functions
- `.claude/skills/google-ads-weekly-report/skill.md` - Weekly report automation

**External Resources:**
- Matplotlib documentation - matplotlib.org
- Google Sheets SPARKLINE docs - support.google.com

**Questions or Issues:**
See `docs/INCIDENTS.md` for historical troubleshooting examples

---

**Last Updated:** 2025-12-16
**Status:** Production-ready
**Version:** 1.0
