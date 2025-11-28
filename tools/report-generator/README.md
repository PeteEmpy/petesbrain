# Report Generator

Professional, data-driven reports from your Google Ads and Analytics data with interactive visualizations and multiple export formats.

![Report Generator](https://img.shields.io/badge/status-active-success)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

## Features

✨ **Interactive Web Interface** - Beautiful, intuitive UI for creating reports
📊 **Dynamic Charts** - Interactive Chart.js visualizations with toggle controls
📈 **Multiple Report Types** - Q4 strategy, weekly performance, monthly summaries, campaign analysis
🎨 **Professional Design** - Print-ready layouts with client-specific branding
💾 **Multiple Export Formats** - HTML, JSON, and PDF (coming soon)
🔄 **Real-Time Data** - Integrates with Google Ads, Analytics, and Sheets via MCP
📁 **Report Library** - Save and browse previously generated reports
🎯 **Client-Focused** - Automatically discovers clients from Pete's Brain structure

## Quick Start

### 1. Installation

```bash
cd tools/report-generator
./start.sh
```

The script will:
- Create a virtual environment
- Install dependencies
- Start the Flask web server

### 2. Access the Web Interface

Open your browser to:
```
http://localhost:5002
```

### 3. Generate Your First Report

1. **Select Report Type** - Choose from Q4 Strategy, Weekly Performance, Monthly Summary, or Campaign Analysis
2. **Choose Client** - Select from automatically discovered clients
3. **Set Date Range** - Pick a preset or custom date range
4. **Generate** - Click generate and view your interactive report!

## Report Types

### 📈 Q4 Strategy Report

Comprehensive quarterly strategy with:
- Budget allocation across regions
- ROAS targets and current performance
- Revenue projections
- Implementation timeline
- Strategic recommendations

**Best for**: Quarterly planning, budget reviews, stakeholder presentations

### 📊 Weekly Performance Report

Week-over-week performance analysis:
- Key metrics dashboard
- Campaign breakdown
- Trend analysis
- Performance alerts

**Best for**: Regular check-ins, quick status updates, identifying issues

### 📅 Monthly Summary Report

End-of-month overview:
- Monthly highlights
- Top performing campaigns
- Key insights and learnings
- Action items for next month

**Best for**: Monthly reviews, client updates, progress tracking

### 🔍 Campaign Analysis Report

Deep dive into campaign performance:
- Campaign-level metrics
- Optimization recommendations
- A/B test results
- Bidding strategy analysis

**Best for**: Campaign optimization, troubleshooting, strategic adjustments

## Interactive Features

### Dynamic Charts

Reports include interactive Chart.js visualizations:
- **Toggle between views** - Budget → ROAS → Revenue with button controls
- **Hover tooltips** - Detailed data on hover
- **Responsive design** - Adapts to screen size
- **Color-coded regions** - Consistent visual identity

### Export Options

**HTML Export**
- Standalone file (can be opened anywhere)
- Preserves all styling and charts
- Share via email or cloud storage

**JSON Export**
- Raw data structure
- Can be re-imported later
- Machine-readable format

**PDF Export** *(Coming Soon)*
- Professional print layout
- Embedded charts
- Multi-page support

## Examples

### Smythson Q4 2025 Strategy Report

Generated report shows:
- **Executive Summary**: £367K budget, £781K revenue target, 2.13x ROAS goal
- **Regional Breakdown**: UK (44%), USA (37%), EUR (14%), ROW (6%)
- **Current Performance**: All regions exceeding targets (UK: 4.15 ROAS vs 3.0 target)
- **Timeline**: Oct 29 launch → Nov 25 Thanksgiving boost → Dec 31 review
- **Recommendations**: 6 strategic insights based on current performance

[View Example Report](../../clients/smythson/q4-2025-strategy-report.html)

## File Structure

```
tools/report-generator/
├── app.py                   # Flask web application
├── report_generator.py      # Core report engine
├── start.sh                 # Startup script
├── requirements.txt         # Dependencies
├── templates/               # HTML templates
│   ├── base.html
│   ├── index.html
│   └── reports/
│       ├── q4_strategy.html
│       ├── weekly_performance.html
│       ├── monthly_summary.html
│       ├── campaign_analysis.html
│       └── list.html
├── static/                  # CSS and JavaScript
│   ├── css/style.css
│   └── js/main.js
└── reports/                 # Generated reports
    └── exports/             # Exported files
```

## Configuration

### Adding a New Client

Clients are automatically discovered from `clients/` directory. To add a new client:

1. Create client folder: `clients/new-client/`
2. Add Google Ads account mapping in `report_generator.py`:

```python
account_mapping = {
    'new-client': {
        'accounts': [
            {'id': '1234567890', 'name': 'Client Account', 'region': 'UK'}
        ],
        'manager_id': '9876543210'
    }
}
```

### Changing the Port

Edit `app.py` (bottom of file):
```python
app.run(debug=True, port=5002, host='127.0.0.1')
```

Default is **5002** to avoid conflicts with Google Ads Generator (5001).

## Data Integration

### Google Ads MCP

Reports can fetch data from Google Ads via MCP integration:

```python
# Example: Fetch performance data
data = mcp__google-ads__run_gaql(
    customer_id='1234567890',
    manager_id='9876543210',
    query="""
        SELECT
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM customer
        WHERE segments.date BETWEEN '2025-10-01' AND '2025-10-29'
    """
)
```

### Google Analytics MCP

Pull website metrics to complement ad data:

```python
# Example: Get page views
data = mcp__google-analytics__get_page_views(
    property_id='123456789',
    start_date='2025-10-01',
    end_date='2025-10-29'
)
```

### Google Sheets MCP

Read experiment logs and client notes:

```python
# Example: Read experiment data
data = mcp__google-sheets__read_cells(
    spreadsheet_id='abc123',
    range_name='Client Notes!A1:D100'
)
```

## Saved Reports

Reports are automatically saved to two locations:

1. **Tool directory**: `tools/report-generator/reports/`
2. **Client folder**: `clients/{client}/reports/` (if option enabled)

### Viewing Saved Reports

Click "Saved Reports" in the navigation to browse all previously generated reports.

Reports are sorted by generation date (newest first).

## Tips & Best Practices

### For Best Results

1. **Use specific date ranges** - Custom ranges give more precise insights
2. **Save to client folder** - Keep reports with client data for easy access
3. **Export regularly** - Create HTML exports for sharing
4. **Review recommendations** - Reports include AI-generated insights

### Performance Tips

- Reports load instantly with cached data
- Charts render on the client side (no server lag)
- Export large reports as JSON for faster loading

### Sharing Reports

**Internal Team**:
- Export as HTML and share via Google Drive/Dropbox
- Or share the client folder link

**Clients**:
- Export as HTML (standalone, opens in any browser)
- PDF export (coming soon) for professional presentations
- Screenshots of key sections

## Troubleshooting

### Port 5002 already in use

```bash
# Kill existing process
lsof -ti:5002 | xargs kill -9

# Restart
./start.sh
```

### Charts not showing

1. Check internet connection (Chart.js loads from CDN)
2. Open browser console (F12) for JavaScript errors
3. Try a different browser

### Report not generating

1. Check terminal for Flask error messages
2. Verify client folder exists in `clients/`
3. Ensure date range is valid

### Template not found

```bash
# Verify templates directory structure
ls -R templates/
```

Should show `base.html`, `index.html`, and `reports/` subdirectory.

## Development

### Running in Debug Mode

```bash
source .venv/bin/activate
export FLASK_ENV=development
python3 app.py
```

Debug mode enables:
- Auto-reload on file changes
- Detailed error messages
- Interactive debugger

### Adding a New Report Template

1. Create HTML template in `templates/reports/new_report.html`
2. Add data fetcher function in `app.py`
3. Add generation method in `report_generator.py`
4. Update form in `templates/index.html`

See [TOOL_CLAUDE.md](TOOL_CLAUDE.md) for detailed instructions.

### Testing Changes

1. Make changes to code
2. Reload browser (Flask auto-reloads)
3. Test report generation
4. Check exports work correctly

## Requirements

- **Python**: 3.8+
- **Browser**: Modern browser with JavaScript enabled
- **Internet**: For Chart.js CDN (charts only)

Full dependencies in `requirements.txt`:
- Flask 3.0.0
- Jinja2 3.1.2
- Chart.js 4.4.0 (CDN)
- Google Ads/Analytics/Sheets APIs

## Version History

### v1.0.0 (2025-10-29)
- Initial release
- Q4 Strategy report template
- Interactive chart controls
- HTML/JSON export
- Client auto-discovery
- Saved reports library

### Coming Soon
- PDF export functionality
- Weekly/monthly report templates
- Campaign analysis deep dives
- Scheduled automated reports
- Email delivery integration
- More chart types and filters

## Support

For help with the Report Generator:

1. **Documentation**: Read [TOOL_CLAUDE.md](TOOL_CLAUDE.md) for technical details
2. **Claude Code**: Ask Claude for assistance with specific issues
3. **Issues**: Check terminal output for error messages

## License

Part of Pete's Brain project. For internal use only.

## Credits

Built with:
- Flask (web framework)
- Chart.js (charts)
- Jinja2 (templates)
- Claude Code (development assistant)

---

**Generated with**: Claude Code
**Last Updated**: 2025-10-29
**Version**: 1.0.0
