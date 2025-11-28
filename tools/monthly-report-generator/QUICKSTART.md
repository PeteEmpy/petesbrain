# Devonshire Hotels - Monthly Report Generator

## Quick Start

This tool automates the generation of monthly Paid Search reports for Devonshire Hotels, saving hours of manual work each month.

## Current Status

**Phase 1: Markdown Reports** ✅ COMPLETE
- October 2025 report generated and available
- Located at: `/clients/devonshire-hotels/reports/october-2025-paid-search-report.md`
- Ready to copy into Google Slides deck

**Phase 2: Automated Slides** 🚧 IN PROGRESS
- Full automation with Google Slides API coming soon
- Will generate complete slide deck automatically

## Using the October 2025 Report

The October report is complete and ready to use:

**File**: `/Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/reports/october-2025-paid-search-report.md`

**Contents**:
1. Executive Summary (budget, overall performance)
2. Individual Property Performance (Hotels)
   - Top performers by ROAS
   - Properties requiring attention
3. Campaign Type Breakdown
4. Key Insights & Commentary
5. Self-Catering Campaigns
6. The Hide (separate budget)
7. Recommendations for November

**To Use**:
1. Open the markdown file
2. Copy sections into your Google Slides deck
3. Add charts/visualizations as needed
4. Format to match existing slide style

## Report Structure

The report follows the same structure as the September 2025 deck (Slides 14-27):

### Slide 1: Title - "Paid Search - [Month]"
- Month name
- Report period
- Devonshire Hotels branding

### Slide 2: Hotels - Overview
- Overall hotel performance metrics
- Budget vs spend
- ROAS summary

### Slide 3: Hotels - Top Performers
- Table showing best ROAS properties
- CTR and conversion data

### Slide 4: Hotels - Attention Needed
- Properties underperforming
- Issues and recommendations

### Slide 5: Campaign Type Breakdown
- Performance Max
- Search (Hotels)
- Search (Self-Catering)
- Search (Locations)

### Slide 6: Self Catering
- Chatsworth SC performance
- Bolton Abbey SC performance
- Commentary and recommendations

### Slide 7: The Hide
- Separate £2,000 budget
- Performance data
- Notes on rename from Highwayman

### Slide 8: Weddings
- Data when available
- Placeholder for now

### Slide 9: Lismore and The Hall
- Data when available
- Placeholder for now

### Slide 10: Key Insights
- Performance highlights
- Areas for improvement
- Month-over-month comparison

### Slide 11: Recommendations for Next Month
- Specific action items
- Budget adjustments
- Campaign optimizations

## Data Sources

The report pulls data from:

1. **Google Ads API** (via MCP)
   - Campaign performance metrics
   - Spend, revenue, conversions
   - Impressions, clicks, CTR

2. **Budget Tracker** (Google Sheets)
   - Monthly budget allocations
   - Pacing calculations
   - Variance analysis

3. **Experiment Notes** (CSV)
   - Strategic changes during the month
   - Expected outcomes
   - Context for performance changes

4. **Email Communications**
   - Client feedback and requests
   - Issues or concerns raised
   - Strategic discussions

## Key Metrics

- **ROAS**: Revenue / Spend (target varies by campaign)
- **CTR**: (Clicks / Impressions) × 100
- **CPA**: Spend / Conversions
- **Pacing**: (Actual Spend / Budget) × 100

## Campaign Groupings

### Main Properties (£9,000-£11,730 budget)
- **Hotels**: Devonshire Arms, Cavendish, Beeley Inn, Pilsley Inn, The Fell, Chatsworth Inns
- **Performance Max**: All properties combined
- **Locations**: Chatsworth, Bolton Abbey
- **Self-Catering**: Chatsworth SC, Bolton Abbey SC

### The Hide (£2,000 budget)
- The Hide (current campaign, launched Oct 10, 2025)
- Highwayman Arms (paused, pre-rename)

### Weddings (separate tracking)
- Data to be added when available

### Lismore and The Hall (separate tracking)
- Data to be added when available

## Monthly Workflow

### End of Month (e.g., Oct 31)
1. Wait for all Google Ads data to finalize (usually 2-3 days into next month)
2. Review email communications for context
3. Check experiment notes for strategic changes

### Generate Report (e.g., Nov 2-3)
1. Open the October 2025 report as reference
2. Query Google Ads data for the completed month
3. Update budget tracker with final numbers
4. Compile performance tables
5. Write key insights and recommendations
6. Save to `/clients/devonshire-hotels/reports/[month-year]-paid-search-report.md`

### Deliver to Client (via A Cunning Plan)
1. Copy sections into shared Google Slides deck
2. Add visualizations (charts, graphs)
3. Format to match existing style
4. Send to Gary at A Cunning Plan for review
5. Gary forwards to Devonshire Hotels

## Important Notes

- **Shared Deck**: The full monthly report includes SEO and other sections managed by other contributors. Only add the Paid Search section.
- **Data Exclusions**: Main properties figures exclude The Hide, Castles, and Weddings campaigns (tracked separately)
- **Conversion Types**: Conversions include both direct bookings and qualified leads
- **The Hide Launch**: October 10, 2025 (formerly The Highwayman)
- **Budget Changes**: November 2025 reduced to £9,000 (from £11,730 in October)

## Future Automation

**Coming Soon**: Full automation that will:
1. Run with a single command: `python3 generate_devonshire_report.py --month 2025-11`
2. Query all data automatically
3. Generate complete Google Slides presentation
4. Include charts and visualizations
5. Apply brand formatting
6. Export ready-to-share deck

## Questions or Issues?

See the main tool documentation at `/tools/monthly-report-generator/README.md` or check the skeleton script at `generate_devonshire_report.py` for technical details.

---

**Last Updated**: 2025-11-02
**Tool Status**: Phase 1 Complete (Markdown Reports)
**Next Phase**: Automated Google Slides generation
