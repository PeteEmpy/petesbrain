# Devonshire Hotels Monthly Report Generator

**Purpose**: Generate complete monthly performance reports for Devonshire Hotels with consistent formatting, navigation, and commentary structure.

## Features

- **11 standardized slide templates** covering all performance areas
- **Automatic report compilation** with navigation and styling
- **Chart.js integration** for year-over-year comparisons and profitability visualizations
- **Consistent brand styling** using Estate Blue (#00333D) and Stone (#E5E3DB)
- **Comprehensive commentary** with root cause analysis and strategic insights

## Usage

### Quick Start
```bash
cd /Users/administrator/Documents/PetesBrain/tools/devonshire-monthly-report
./start.sh
```

Then open http://localhost:5000 in your browser.

### Generate Report
1. Select reporting month (e.g., "October 2025")
2. Script will:
   - Query Google Ads API for performance data
   - Generate 11 individual slide HTML files
   - Create commentary document
   - Compile everything into single navigable report
3. Output: `clients/devonshire-hotels/reports/{month}-complete-report.html`

## Report Structure

### Slides (11 total)
1. **Slide 16**: Overview - KPI boxes (revenue, ROAS, spend, bookings, impressions, CTR)
2. **Slide 17**: Year-over-Year - 12 charts (6 % change + 6 absolute values)
3. **Slide 18**: Individual Hotel Performance - Ranked table
4. **Slide 19**: Search vs PMax - Separate tables
5. **Slide 20**: Hotel Profitability - Bar chart with gradient shading
6. **Slide 21**: Locations Performance - Table
7. **Slide 22**: Self-Catering - Ad group breakdown table
8. **Slide 23**: The Hide - Separate budget property
9. **Slide 24**: Weddings - Ad group table
10. **Slide 25**: Hide Trend - Line chart with annotation
11. **Slide 26**: Exclusive Venues - Castle properties

### Commentary
- Hotels KPI Overview (vs previous month)
- Year-over-Year Trends (current year vs previous year)
- Individual Hotel Performance (top/mid-tier analysis)
- Search vs PMax Analysis
- Hotel Profitability (ROAS ranking)
- Locations Performance
- Self-Catering Campaigns
- The Hide (separate budget tracking)
- November Priorities
- What Worked Well

## File Locations

```
clients/devonshire-hotels/
├── Monthly Report Slides/
│   ├── Slide 16 {Month} 25.html
│   ├── Slide 17 {Month} 25 UPDATED.html
│   ├── Slide 18 {Month} 25.html
│   ├── Slide 19 {Month} 25.html
│   ├── Slide 20 {Month} 25.html
│   ├── Slide 21 {Month} 25.html
│   ├── Slide 22 {Month} 25.html
│   ├── Slide 23 {Month} 25.html
│   ├── Slide 24 {Month} 25.html
│   ├── Slide 25 {Month} 25.html
│   └── Slide 26 {Month} 25.html
├── documents/
│   └── {month}-2025-slide-commentary.html
├── reports/
│   └── {month}-2025-complete-report.html
└── scripts/
    └── build_complete_report.py  ← Master template
```

## Brand Guidelines

### Colors
- **Estate Blue**: #00333D (primary)
- **Stone**: #E5E3DB (backgrounds)
- **Success Green**: #2E7D32 (positive metrics)
- **Alert Red**: #C62828 (negative metrics)

### Typography
- **Font**: Arial, Helvetica, sans-serif
- **H1**: 42px bold (Estate Blue)
- **H2**: 28px bold
- **Body**: 15-18px

### Formatting
- **ROAS**: Express as percentage (576%, not 5.76x)
- **Currency**: British pounds (£)
- **Dates**: "October 1-31, 2025" format
- **Changes**: "percentage points" not "pts"

## Technical Notes

### Chart.js Integration
- **Version**: 4.4.0 (CDN loaded)
- **Annotation Plugin**: 3.0.1 (for vertical line markers)
- **Canvas IDs**: Made unique per slide (`chartId_1`, `chartId_4`, `chartId_9`)
- **Context Variables**: Unique per slide to avoid conflicts

### Build Script Challenges Solved
1. **Variable conflicts**: Each slide uses unique `ctx_{slide_counter}` variables
2. **Function preservation**: Helper functions with `ctx` parameter preserved
3. **Chart constructor calls**: Only replaced outside of helper functions
4. **Navigation**: Smooth scroll with active state tracking

## Data Sources

### Google Ads API
- **Customer ID**: 7816697284
- **Metrics**: "By conversion time" (conversions_by_conversion_date, conversions_value_by_conversion_date)
- **Campaign Structure**:
  - DEV | Properties (main hotels)
  - DEV | Locations (Chatsworth, Bolton Abbey)
  - DEV | Self-Catering (Chatsworth, Bolton Abbey)
  - DEV | Castles (Lismore, The Hall)
  - DEV | Weddings
  - The Hide (formerly Highwayman)

### Historical Data
- **YoY Comparisons**: January-October 2024 vs 2025
- **Monthly Trends**: 10-month progression (Jan-Oct)

## Maintenance

### Monthly Workflow
1. **First week of new month**: Generate previous month's report
2. **Query Google Ads**: Pull performance data via MCP
3. **Generate slides**: Update data in 11 HTML templates
4. **Write commentary**: Add context and root cause analysis
5. **Build report**: Run `build_complete_report.py`
6. **Review**: Open in browser, verify all charts render
7. **Archive**: Save to reports folder

### Updating Templates
- Individual slide templates in `Monthly Report Slides/`
- Build script at `scripts/build_complete_report.py`
- Commentary template structure documented in `MONTHLY-REPORT-STATUS-{MONTH}-2025.md`

## Future Enhancements

### Potential Additions
- [ ] Flask UI for month selection and data input
- [ ] Automated Google Ads API query based on date range
- [ ] PDF export functionality
- [ ] Email delivery to client
- [ ] Comparative analysis (current month vs same month previous year)
- [ ] Automated commentary generation using Claude API
- [ ] Historical report archive browser

### Data Integrations
- [ ] Google Analytics 4 (website traffic correlation)
- [ ] Booking system data (direct API integration)
- [ ] Weather data (impact analysis)
- [ ] Competitor spend estimates

## Related Documentation

- **Workflow Guide**: `clients/devonshire-hotels/MONTHLY-REPORT-WORKFLOW.md`
- **Status Tracking**: `clients/devonshire-hotels/MONTHLY-REPORT-STATUS-OCTOBER-2025.md`
- **Context**: `clients/devonshire-hotels/CONTEXT.md`

---

**Last Updated**: 2025-11-07
**Report Format Version**: 1.0 (October 2025 baseline)
