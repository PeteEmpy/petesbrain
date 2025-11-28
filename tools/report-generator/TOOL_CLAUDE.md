# Report Generator - Architecture & Implementation

This document provides comprehensive technical details about the Report Generator tool for Claude Code.

## Overview

**Report Generator** is an interactive web-based tool for creating professional, data-driven reports from Google Ads, Google Analytics, and client data. It features a Flask web interface, dynamic chart generation, and multiple export formats.

## Architecture

### Core Components

```
tools/report-generator/
├── app.py                      # Flask web application
├── report_generator.py         # Core report generation engine
├── requirements.txt            # Python dependencies
├── start.sh                    # Startup script
├── templates/                  # Jinja2 HTML templates
│   ├── base.html              # Base layout
│   ├── index.html             # Home page with form
│   └── reports/
│       ├── q4_strategy.html   # Q4 strategy report template
│       ├── weekly_performance.html
│       ├── monthly_summary.html
│       ├── campaign_analysis.html
│       └── list.html          # Saved reports list
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│       └── main.js            # JavaScript utilities
├── reports/                    # Generated reports storage
│   └── exports/               # Exported files
└── data/                       # Temporary data cache
```

### Data Flow

```
User Input (Form)
    ↓
Flask Route Handler
    ↓
Data Fetching (MCP Integration)
    ↓
ReportGenerator.generate_report()
    ↓
Template Rendering
    ↓
Interactive Display (Chart.js)
    ↓
Export Options (HTML/PDF/JSON)
```

## Key Classes

### ReportGenerator

**Location**: `report_generator.py`

**Purpose**: Core engine for report generation, data management, and export.

**Key Methods**:

- `list_clients()` - Discover all clients from Pete's Brain directory structure
- `get_client_accounts(client_name)` - Retrieve Google Ads account mappings for a client
- `calculate_date_range(range_type, custom_start, custom_end)` - Calculate date ranges from presets or custom dates
- `generate_report(report_type, client_name, date_range, data, options)` - Main report generation method
- `save_report(report_data, save_to_client_folder)` - Persist reports to disk
- `list_saved_reports(client_name)` - Retrieve list of previously generated reports

**Report Types**:

1. **Q4 Strategy** - Multi-regional quarterly strategy with budget allocation, ROAS targets, timeline
2. **Weekly Performance** - Week-over-week trends, campaign breakdown, alerts
3. **Monthly Summary** - Month-end overview, top campaigns, insights
4. **Campaign Analysis** - Deep dive into specific campaigns with optimization recommendations

## Flask Application Structure

### Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page with report generation form |
| `/generate` | POST | Generate new report (AJAX) |
| `/view` | GET | View latest generated report |
| `/reports` | GET | List all saved reports |
| `/reports/<filename>` | GET | Load specific saved report |
| `/export/<format>` | GET | Export current report (html/pdf/json) |
| `/api/clients` | GET | API: Get client list |
| `/api/client/<name>/accounts` | GET | API: Get client account info |

### Global State Pattern

**IMPORTANT**: The Flask app uses a **global variable pattern** (not sessions) for single-user desktop deployment:

```python
latest_report = None  # Global variable

@app.route('/generate', methods=['POST'])
def generate_report():
    global latest_report
    # ... generate report ...
    latest_report = report  # Store in global
    return jsonify({'redirect': '/view'})

@app.route('/view')
def view_report():
    if latest_report is None:
        return redirect('/')
    return render_template('reports/...', report=latest_report)
```

This means:
- App is **single-user only**
- Data persists only in memory during runtime
- No database required
- Restart clears latest report (but saved reports persist on disk)

## Data Integration

### MCP Server Integration

The tool is designed to integrate with Model Context Protocol (MCP) servers for data fetching:

**Google Ads MCP** (`mcp__google-ads__*`):
- `mcp__google-ads__list_accounts` - List accessible accounts
- `mcp__google-ads__run_gaql` - Execute GAQL queries for performance data

**Google Analytics MCP** (`mcp__google-analytics__*`):
- `mcp__google-analytics__get_page_views` - Page view metrics
- `mcp__google-analytics__get_traffic_sources` - Traffic analysis
- `mcp__google-analytics__run_report` - Custom GA4 reports

**Google Sheets MCP** (`mcp__google-sheets__*`):
- `mcp__google-sheets__read_cells` - Read experiment data
- `mcp__google-sheets__list_sheets` - List available sheets

### Data Fetching Functions

**Location**: `app.py` (bottom of file)

```python
def fetch_q4_strategy_data(client_name: str, start_date: str, end_date: str) -> dict:
    """Fetch data for Q4 strategy report

    This function calls MCP tools to get real Google Ads data.
    Currently has hardcoded Smythson data for demonstration.
    """
    # TODO: Replace with real MCP calls
    # Example:
    # data = mcp__google-ads__run_gaql(
    #     customer_id=account_id,
    #     manager_id=manager_id,
    #     query="SELECT ... FROM customer WHERE ..."
    # )

    return structured_data_dict
```

**Note**: MCP tools are NOT directly callable from Flask. Data must be fetched and passed to `generate_report()`.

To add real data integration:
1. Create a separate data fetching module that uses MCP
2. Call MCP tools from outside Flask (e.g., command-line script)
3. Pass fetched data to Flask via API or file system
4. OR: Integrate Claude Code's MCP client library directly

## Report Templates

### Template Structure

All report templates extend `base.html` and follow this pattern:

```html
{% extends "base.html" %}

{% block title %}Report Title{% endblock %}

{% block extra_head %}
<!-- Report-specific CSS and scripts -->
{% endblock %}

{% block content %}
<!-- Report content with data binding -->
<div class="report-header">...</div>
<div class="section">
    <h2>{{ report.section_title }}</h2>
    <div class="chart-container">
        <canvas id="chartId"></canvas>
    </div>
</div>

<script>
// JavaScript for dynamic charts
const reportData = {{ report|tojson }};
// Chart.js initialization
</script>
{% endblock %}
```

### Interactive Charts

Reports use **Chart.js 4.4.0** for visualizations:

- **Doughnut Charts** - Budget allocation, percentage breakdowns
- **Bar Charts** - ROAS comparison, revenue targets vs actual
- **Line Charts** - Time series trends (weekly/monthly)
- **Mixed Charts** - Combined metrics

**Chart Controls**:
- Toggle between different chart views (Budget → ROAS → Revenue)
- Interactive tooltips with formatted values
- Responsive design (adapts to screen size)
- Print-friendly rendering

### Data Binding

Templates use Jinja2 template syntax:

```html
<!-- Simple variables -->
{{ report.client_display }}

<!-- Number formatting -->
£{{ "{:,}".format(report.total_budget) }}

<!-- Calculations -->
{% set vs_target = ((region.current_roas / region.roas_target - 1) * 100)|round|int %}

<!-- Loops -->
{% for region in report.regions %}
    <div class="region-card">{{ region.name }}</div>
{% endfor %}

<!-- Conditionals -->
{% if report.recommendations %}
    <ul>
    {% for rec in report.recommendations %}
        <li>{{ rec }}</li>
    {% endfor %}
    </ul>
{% endif %}
```

## Styling System

### CSS Architecture

**Main Stylesheet**: `static/css/style.css`

**Design System**:
- CSS Variables for theming (`--primary-color`, `--success-color`, etc.)
- Responsive grid layouts (CSS Grid + Flexbox)
- Mobile-first approach with media queries
- Print-specific styles for export

**Key Components**:

1. **Navigation** - Sticky navbar with brand and links
2. **Forms** - Radio card selection, dropdowns, checkboxes
3. **Cards** - Summary cards, region cards, timeline items
4. **Buttons** - Primary, secondary, outline variants with hover effects
5. **Charts** - Responsive containers with controls
6. **Status Badges** - Color-coded performance indicators

**Color Palette**:
- Primary: `#667eea` (purple-blue gradient)
- Success: `#4CAF50` (green)
- Warning: `#FF9800` (orange)
- Danger: `#f44336` (red)
- Text: `#333` / `#666`
- Background: `#f5f7fa`

### Regional Color Coding

Reports use consistent colors for regions:

- **UK** 🇬🇧: Green (`#4CAF50`)
- **USA** 🇺🇸: Blue (`#2196F3`)
- **EUR** 🇪🇺: Orange (`#FF9800`)
- **ROW** 🌍: Purple (`#9C27B0`)

## Export Functionality

### HTML Export

**Route**: `/export/html`

Renders report template to standalone HTML file:
- Includes all CSS inline
- Embeds Chart.js from CDN
- Self-contained (no external dependencies except CDN)
- Can be opened in any browser

**Implementation**:
```python
def export_html():
    html_content = render_template(
        template,
        report=report_data,
        standalone=True  # Flag for standalone mode
    )
    # Save to exports/ directory
    return send_file(export_path, as_attachment=True)
```

### JSON Export

**Route**: `/export/json`

Exports raw report data as JSON:
- Full report data structure
- Can be re-imported
- Useful for API integration
- Machine-readable format

### PDF Export (Future)

**Status**: Not yet implemented

**Planned Implementation**:
- Use WeasyPrint library (already in requirements.txt)
- Render HTML template to PDF
- Preserve styling and charts (as images)
- Professional print layout

**Code Stub**:
```python
def export_pdf():
    # TODO: Implement using weasyprint
    from weasyprint import HTML
    html_content = render_template(...)
    pdf = HTML(string=html_content).write_pdf()
    return send_file(pdf, as_attachment=True)
```

## Report Storage

### File System Structure

```
tools/report-generator/
├── reports/                    # Main reports directory
│   ├── smythson_q4_strategy_20251029_143022.json
│   ├── tree2mydoor_weekly_performance_20251029_150000.json
│   └── exports/               # Exported HTML/PDF files
│       ├── smythson_q4_strategy_20251029_143022.html
│       └── smythson_q4_strategy_20251029_143022.pdf
└── clients/
    └── smythson/
        └── reports/            # Client-specific copies (optional)
            └── smythson_q4_strategy_20251029_143022.json
```

### Report Filename Format

`{client}_{report_type}_{timestamp}.{ext}`

- `client`: Client name (e.g., "smythson")
- `report_type`: Report type (e.g., "q4_strategy")
- `timestamp`: `YYYYMMDD_HHMMSS` format
- `ext`: File extension (json, html, pdf)

**Example**: `smythson_q4_strategy_20251029_143022.json`

### Report Data Structure

JSON format:
```json
{
  "type": "q4_strategy",
  "client": "smythson",
  "generated_at": "2025-10-29T14:30:22",
  "data": {
    "client_name": "smythson",
    "client_display": "Smythson",
    "generated_date": "2025-10-29",
    "date_range": ["2025-10-01", "2025-12-31"],
    "total_budget": 367014,
    "total_revenue_target": 780691,
    "overall_roas_target": 2.13,
    "regions": [
      {
        "name": "UK",
        "code": "GB",
        "account_id": "8573235780",
        "budget": 160752,
        "revenue_target": 300000,
        "roas_target": 3.0,
        "current_spend": 37752,
        "current_revenue": 156639,
        "current_roas": 4.15,
        "conversions": 1086
      },
      // ... more regions
    ],
    "timeline": [...],
    "recommendations": [...]
  }
}
```

## Development & Debugging

### Running Locally

```bash
cd tools/report-generator
./start.sh
```

**Manual Start**:
```bash
source .venv/bin/activate
python3 app.py
```

**Access**: `http://localhost:5002`

### Debug Mode

Flask runs with `debug=True` in `app.py`:
- Auto-reload on file changes
- Detailed error messages
- Interactive debugger in browser

### Common Issues

**Port 5002 already in use**:
```bash
lsof -ti:5002 | xargs kill -9
```

**Virtual environment issues**:
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Template not found**:
- Check template path matches route
- Ensure templates/ directory structure is correct
- Verify template extends base.html

**Charts not rendering**:
- Check browser console for JavaScript errors
- Ensure Chart.js CDN is accessible
- Verify reportData is properly passed to template

## Future Enhancements

### Priority Additions

1. **Real MCP Integration**
   - Replace mock data with live Google Ads queries
   - Add Google Analytics integration
   - Pull from Google Sheets experiment log

2. **PDF Export**
   - Implement WeasyPrint export
   - Chart rendering as images
   - Professional PDF layouts

3. **More Report Types**
   - A/B test results
   - Budget pacing report
   - Competitive analysis
   - ROI attribution report

4. **Scheduled Reports**
   - Automated weekly/monthly generation
   - Email delivery via Gmail API
   - Configurable schedules per client

5. **Report Comparison**
   - Week-over-week comparisons
   - Year-over-year analysis
   - Goal tracking over time

6. **Interactive Filters**
   - Date range sliders in reports
   - Campaign-level drill-down
   - Real-time chart updates

7. **Report Templates**
   - Custom branding per client
   - White-label options
   - Template editor

### Technical Improvements

- Add database (SQLite) for report metadata
- Implement proper user sessions
- Add report sharing/collaboration
- API endpoints for programmatic access
- Caching layer for data fetching
- Background job processing (Celery)

## Integration with Pete's Brain

### Client Discovery

Tool automatically discovers clients from:
`/Users/administrator/Documents/PetesBrain/clients/*/`

Excludes:
- Folders starting with `_` (e.g., `_templates`, `_unassigned`)
- Non-directory files

### Account Mappings

Hardcoded in `report_generator.py` → `get_client_accounts()`:

```python
account_mapping = {
    'smythson': {
        'accounts': [
            {'id': '8573235780', 'name': 'Smythson UK', 'region': 'UK'},
            {'id': '7808690871', 'name': 'Smythson USA', 'region': 'USA'},
            {'id': '7679616761', 'name': 'Smythson EUR', 'region': 'EUR'},
            {'id': '5556710725', 'name': 'Smythson ROW', 'region': 'ROW'}
        ],
        'manager_id': '2569949686'
    }
}
```

**To add new clients**:
1. Add entry to `account_mapping` dictionary
2. Ensure client folder exists in `clients/`
3. Add Google Ads account IDs and manager ID

### Saving to Client Folders

When `save_to_client_folder` option is enabled:
- Report JSON saved to `clients/{client}/reports/`
- Creates directory if it doesn't exist
- Maintains copy in tool's `reports/` directory

## Testing

### Manual Testing Checklist

1. **Home Page**
   - [ ] All report types display correctly
   - [ ] Clients load from directory
   - [ ] Date range selector works
   - [ ] Custom date range shows/hides properly

2. **Client Selection**
   - [ ] Account information loads via API
   - [ ] Multiple accounts display correctly

3. **Report Generation**
   - [ ] Form submits successfully
   - [ ] Loading state displays
   - [ ] Redirects to report view
   - [ ] Report renders correctly

4. **Report View**
   - [ ] All sections display
   - [ ] Charts render properly
   - [ ] Chart toggle buttons work
   - [ ] Data formatting correct

5. **Export**
   - [ ] HTML export downloads
   - [ ] JSON export downloads
   - [ ] Files saved to correct location

6. **Saved Reports**
   - [ ] List page shows all reports
   - [ ] Can load previous reports
   - [ ] Correct sorting (newest first)

### Example Test Data

**Smythson Q4 Strategy** - Hardcoded in `fetch_q4_strategy_data()`:
- 4 regions (UK, USA, EUR, ROW)
- October 2025 performance data
- Q4 targets and projections
- Timeline milestones

To test other report types, add mock data to respective `fetch_*_data()` functions.

## Dependencies

See `requirements.txt` for full list:

**Core**:
- Flask 3.0.0 - Web framework
- Jinja2 3.1.2 - Template engine

**Data & APIs**:
- google-ads 24.1.0 - Google Ads API
- google-api-python-client 2.111.0 - Google APIs
- pandas 2.1.4 - Data manipulation

**Export**:
- weasyprint 60.1 - PDF generation (not yet used)

**Utilities**:
- python-dateutil 2.8.2 - Date handling
- pytz 2023.3 - Timezone support

## Performance Considerations

- Reports load in < 2 seconds with mock data
- Chart rendering is instant (client-side)
- No database queries (file system only)
- Single-user means no concurrency issues

**Future optimizations**:
- Cache fetched data (15 min TTL)
- Lazy-load charts on scroll
- Compress export files
- Background data fetching

## Security Notes

**Current**:
- Single-user desktop app (localhost only)
- No authentication
- No external access
- File system access limited to tool directory

**If deploying publicly** (not recommended without changes):
- [ ] Add authentication (Flask-Login)
- [ ] Implement CSRF protection
- [ ] Use secure session keys
- [ ] Restrict file system access
- [ ] Add rate limiting
- [ ] Enable HTTPS

## Maintenance

### Adding a New Report Type

1. **Create template**: `templates/reports/new_report_type.html`
2. **Add data fetcher**: `def fetch_new_report_data()` in `app.py`
3. **Add generator method**: `_generate_new_report()` in `report_generator.py`
4. **Update generate_report()**: Add elif branch for new type
5. **Add form option**: Update `index.html` with new report type card
6. **Test**: Generate report and verify all sections render

### Updating Client Accounts

Edit `report_generator.py` → `get_client_accounts()`:
```python
account_mapping['client_name'] = {
    'accounts': [...],
    'manager_id': '...'
}
```

### Changing Port

Edit `app.py` (bottom):
```python
app.run(debug=True, port=5002, host='127.0.0.1')
```

## Support & Troubleshooting

**Flask errors**: Check terminal output for detailed tracebacks
**Chart issues**: Open browser console (F12) for JavaScript errors
**Template errors**: Check Jinja2 syntax and variable names
**Data issues**: Verify data structure matches template expectations

For Claude Code assistance:
```
Ask: "How do I [task] in the Report Generator tool?"
Provide: Error message and relevant code snippet
```

---

**Last Updated**: 2025-10-29
**Version**: 1.0.0
**Maintainer**: Claude Code
