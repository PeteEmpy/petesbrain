# TOOL_CLAUDE.md - Devonshire Hotels Monthly Report Generator

## Architecture Overview

This tool generates comprehensive monthly performance reports for Devonshire Hotels by:
1. Querying Google Ads API for campaign performance data
2. Generating 11 individual slide HTML files with data visualization
3. Creating detailed commentary with root cause analysis
4. Compiling everything into a single navigable HTML report

## Critical Technical Pattern: Chart.js Variable Uniqueness

**IMPORTANT**: When combining multiple HTML files with Chart.js visualizations, variable conflicts will break chart rendering. The solution implemented:

### Problem
Multiple slides with charts create conflicting JavaScript variables:
```javascript
// Slide 1
const ctx = document.getElementById('chart1').getContext('2d');
new Chart(ctx, {...});

// Slide 2 (CONFLICTS!)
const ctx = document.getElementById('chart2').getContext('2d');
new Chart(ctx, {...});
```

### Solution Pattern
The build script (`build_complete_report.py`) makes variables unique per slide:

```python
# For each slide (slide_counter = 0, 1, 2, ...)
script = script.replace('const ctx = ', f'const ctx_{slide_counter} = ')
script = script.replace('const chart = ', f'const chart_{slide_counter} = ')

# But PRESERVE helper functions with ctx parameter
if 'function createPctChart(ctx,' in script:
    # Don't touch ctx inside these functions
    pass
else:
    # Safe to replace Chart constructor calls
    script = script.replace('new Chart(ctx,', f'new Chart(ctx_{slide_counter},')
```

### Result
- **Slide 16**: No charts (just KPI boxes)
- **Slide 17**: Uses helper functions → `new Chart(ctx, ...)` PRESERVED inside functions
- **Slide 20**: Direct chart → `new Chart(ctx_4, ...)`
- **Slide 25**: Direct chart → `new Chart(ctx_9, ...)`

### Key Insight
**Slides with helper functions** (like Slide 17's `createPctChart` and `createAbsChart`) receive context as a parameter and should use that parameter unchanged. The build script detects this pattern and skips replacement inside functions.

## File Structure

```
tools/devonshire-monthly-report/
├── README.md                    # User-facing documentation
├── TOOL_CLAUDE.md              # This file (architecture details)
├── requirements.txt            # Python dependencies
├── start.sh                    # Entry point
├── app.py                      # Flask UI (future)
├── templates/                  # Slide HTML templates
│   ├── slide-16-overview.html
│   ├── slide-17-yoy.html
│   ├── slide-18-hotels.html
│   ├── slide-19-search-pmax.html
│   ├── slide-20-profitability.html
│   ├── slide-21-locations.html
│   ├── slide-22-self-catering.html
│   ├── slide-23-the-hide.html
│   ├── slide-24-weddings.html
│   ├── slide-25-hide-trend.html
│   ├── slide-26-venues.html
│   └── commentary-template.html
├── scripts/
│   ├── build_complete_report.py  # Master compile script (CANONICAL)
│   ├── query_google_ads.py       # Data fetching
│   └── generate_commentary.py    # AI-powered commentary generation
└── .venv/                      # Virtual environment
```

## Canonical Build Script Location

**MASTER TEMPLATE**: `/Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/scripts/build_complete_report.py`

This is the **authoritative version** that correctly handles:
- Chart ID uniqueness
- Context variable conflicts
- Helper function preservation
- Navigation generation
- Style consolidation

**When creating monthly reports**: Copy this script's pattern exactly. The logic at lines 473-511 is critical for Chart.js multi-slide compatibility.

## Data Flow

```
┌─────────────────────┐
│ Google Ads API      │
│ (MCP Server)        │
└──────┬──────────────┘
       │
       │ Query via mcp__google-ads__run_gaql
       │
       ▼
┌─────────────────────────────────────────┐
│ query_google_ads.py                     │
│ - Fetches campaign data                 │
│ - Calculates YoY comparisons            │
│ - Aggregates by hotel/campaign type     │
└──────┬──────────────────────────────────┘
       │
       │ JSON data
       │
       ▼
┌─────────────────────────────────────────┐
│ Individual Slide Generators             │
│ - slide_16_generator.py (KPI boxes)     │
│ - slide_17_generator.py (YoY charts)    │
│ - slide_18_generator.py (Hotels table)  │
│ - ... (9 more)                          │
└──────┬──────────────────────────────────┘
       │
       │ 11 HTML files
       │
       ▼
┌─────────────────────────────────────────┐
│ generate_commentary.py                  │
│ - Analyzes performance changes          │
│ - Identifies root causes                │
│ - Writes strategic insights             │
│ - Uses Claude API for generation        │
└──────┬──────────────────────────────────┘
       │
       │ commentary.html
       │
       ▼
┌─────────────────────────────────────────┐
│ build_complete_report.py                │
│ - Combines 11 slides + commentary       │
│ - Adds navigation and styling           │
│ - Makes chart variables unique          │
│ - Preserves helper functions            │
└──────┬──────────────────────────────────┘
       │
       │ complete-report.html
       │
       ▼
┌─────────────────────────────────────────┐
│ Browser Display                         │
│ - Navigable single-page report          │
│ - All charts render correctly           │
│ - Smooth scroll between sections        │
└─────────────────────────────────────────┘
```

## Key Technical Decisions

### 1. Single HTML Output vs. Multiple Files
**Choice**: Single HTML file with internal navigation
**Rationale**:
- Easier to share with client (one file vs. folder)
- Better for email attachment
- Maintains context when reviewing multiple sections
- No broken links if files moved

### 2. Chart.js CDN vs. Local
**Choice**: CDN (chart.js@4.4.0 + annotation plugin@3.0.1)
**Rationale**:
- No local dependencies to manage
- Always latest stable version
- Reduces file size
- Works offline once cached

### 3. Static HTML vs. Interactive Dashboard
**Choice**: Static HTML with Chart.js visualizations
**Rationale**:
- Client can open in any browser
- No server/hosting required
- Easy to archive and version control
- Printable/PDF-exportable
- Still interactive (chart tooltips, navigation)

### 4. Python Build Script vs. Template Engine
**Choice**: Python with regex and string manipulation
**Rationale**:
- Full control over HTML structure
- No additional dependencies (no Jinja2, etc.)
- Easier to debug
- Matches existing codebase patterns

### 5. Commentary: Manual vs. AI-Generated
**Current**: Manual with structured sections
**Future**: Hybrid (AI-generated with human review)
**Rationale**:
- Critical insights need human judgment
- AI good for pattern detection and drafting
- Final strategic recommendations need Pete's input

## Google Ads API Query Patterns

### Campaign Structure
```python
# Main Properties (excludes Hide, Castles, Weddings)
MAIN_PROPERTIES_QUERY = """
SELECT
  campaign.name,
  segments.date,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions_by_conversion_date,
  metrics.conversions_value_by_conversion_date
FROM campaign
WHERE
  campaign.name LIKE 'DEV | Properties%'
  AND segments.date BETWEEN '{start_date}' AND '{end_date}'
  AND campaign.status = 'ENABLED'
"""

# Year-over-Year (10 months: Jan-Oct)
YOY_QUERY = """
SELECT
  segments.month,
  segments.year,
  metrics.ctr,
  metrics.conversions,
  metrics.conversions_value_by_conversion_date,
  metrics.cost_micros
FROM campaign
WHERE
  campaign.name LIKE 'DEV | Properties%'
  AND segments.year IN ({current_year}, {previous_year})
  AND campaign.status = 'ENABLED'
GROUP BY segments.month, segments.year
"""
```

### Critical Metric Notes
- **ALWAYS use "by conversion time"** metrics: `conversions_by_conversion_date`, `conversions_value_by_conversion_date`
- **Cost**: Stored in micros (divide by 1,000,000)
- **ROAS**: Express as percentage (576%, not 5.76x)
- **CTR**: Already percentage in API response

## Brand Styling Constants

```python
COLORS = {
    'estate_blue': '#00333D',     # Primary brand color
    'stone': '#E5E3DB',           # Backgrounds
    'success_green': '#2E7D32',   # Positive metrics
    'alert_red': '#C62828',       # Negative metrics
    'chart_gradient': [           # For profitability chart
        '#00333D',  # Darkest
        '#006677',
        '#008094',
        '#0099B1',
        '#33B3CE',
        '#66CCEB'   # Lightest
    ]
}

FONTS = {
    'family': 'Arial, Helvetica, sans-serif',
    'h1_size': '42px',
    'h2_size': '28px',
    'body_size': '15-18px'
}
```

## Commentary Generation Pattern

### Structure
1. **Section per slide** (H2 heading)
2. **Slide reference** (gray italic text)
3. **Performance summary** (commentary box with key metrics)
4. **Root cause analysis** (bullet points with evidence)
5. **Action items** (highlight box for critical issues)

### Root Cause Categories
- ✅ **Your Actions** (budget changes, bid adjustments)
- 🌍 **External Factors** (seasonality, competitors)
- 🏢 **Client Business** (stock issues, pricing)
- ⚙️ **Technical Issues** (tracking, platform bugs)
- 📦 **Product-Level** (out of stock, feed issues)
- 🔧 **Platform Updates** (Google algorithm changes)

### AI Prompt Pattern (Future)
```python
commentary_prompt = f"""
Generate monthly report commentary for Devonshire Hotels.

**Data Summary:**
- Revenue: £{current_revenue:,.2f} (vs £{previous_revenue:,.2f} previous month)
- ROAS: {current_roas}% (vs {previous_roas}% previous month)
- Spend: £{current_spend:,.2f} (vs £{previous_spend:,.2f} previous month)
- Bookings: {current_bookings} (vs {previous_bookings} previous month)

**Known Context:**
{context_from_tasks_completed}
{context_from_experiment_log}
{context_from_knowledge_base}

**Style Requirements:**
- Concise, data-driven language
- Use positive/negative spans for metrics
- Cite specific evidence for all claims
- Categorize root causes clearly
- Include actionable recommendations

Generate commentary following the structure in the template.
"""
```

## Testing Checklist

When generating a new month's report:
- [ ] All 11 slides have unique canvas IDs
- [ ] Year-over-Year charts (Slide 17) render correctly (12 charts total)
- [ ] Hotel Profitability chart (Slide 20) displays with gradient colors
- [ ] The Hide trend chart (Slide 25) shows annotation line
- [ ] Navigation links scroll smoothly to each section
- [ ] Active nav link highlights correctly on scroll
- [ ] All tables display proper formatting (zebra striping, borders)
- [ ] KPI boxes show correct arrows (↑/↓) and colors (green/red)
- [ ] Commentary sections match slide order
- [ ] Footer metadata is accurate (dates, campaign names, generated date)
- [ ] File size < 100KB (should be ~88-90KB)
- [ ] Browser console shows no JavaScript errors

## Deployment

### Manual Process (Current)
1. Update data in individual slide HTML files
2. Run `python3 scripts/build_complete_report.py`
3. Open `reports/{month}-2025-complete-report.html` in browser
4. Review for accuracy
5. Share with client

### Future Automation
1. **Flask UI**: Select month → auto-generate
2. **Scheduled**: First week of month, auto-run via LaunchAgent
3. **Email delivery**: Auto-send to client via Gmail API
4. **Archive**: Auto-commit to git with month tag

## Dependencies

```
Flask==3.0.0
google-ads==23.1.0
anthropic==0.5.0
python-dotenv==1.0.0
```

## Environment Variables

```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-api03-...
GOOGLE_ADS_CUSTOMER_ID=7816697284
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

## Integration with Pete's Brain

### Links to Other Systems
- **CONTEXT.md**: Strategic context and historical notes
- **tasks-completed.md**: What was done (with caveats in notes)
- **rok-experiments-client-notes.csv**: Why changes were made
- **Knowledge Base**: Platform updates (2-4 week delayed impact)

### Workflow Integration
1. **Beginning of month**: Run monthly report generator
2. **Report generation**: Tool creates complete HTML report
3. **Review**: Pete reviews and adds strategic commentary
4. **Delivery**: Share with client via email
5. **Archive**: Save to `reports/` folder and commit to git
6. **Update CONTEXT.md**: Add key learnings and insights

---

**Last Updated**: 2025-11-07
**Technical Contact**: Pete (Pete's Brain project owner)
