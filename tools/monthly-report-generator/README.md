# Monthly Report Generator - Devonshire Hotels

Automated Google Slides presentation generator for monthly Paid Search reports.

## Status: ✅ PRODUCTION READY (OAuth Version)

**OAuth Authentication**: Simple one-time browser login, no complex permissions needed
**Phase 2 Complete**: Fully automated Google Slides generation with branded formatting
**Enhanced**: Professional tables with Estate Blue and Stone brand colors

## What It Does

Generates a complete, standalone Google Slides presentation for Devonshire Hotels Paid Search monthly reporting. The presentation matches the format used in September 2025 and includes:

- Executive Summary with budget and performance metrics
- Individual hotel property performance tables
- Top performers and attention-needed properties
- Campaign type breakdown (Performance Max, Search, Self-Catering)
- Self-catering detailed analysis
- The Hide separate budget tracking
- Placeholder slides for Weddings and Lismore/Hall
- Key insights (highlights and areas for improvement)
- Actionable recommendations for next month

## October 2025 Report - COMPLETED

**✅ Presentation Created**: [Devonshire Paid Search - October 2025](https://docs.google.com/presentation/d/1uobWS1AxZwjZ7bpMh0jVeNCJgf0xP4oYiKBuQQBC3f8)

**Presentation ID**: `1uobWS1AxZwjZ7bpMh0jVeNCJgf0xP4oYiKBuQQBC3f8`

**Contains**:
- 14 slides covering all Paid Search sections
- Complete October 2025 performance data
- Budget tracking (£10,775.93 spend vs £11,730 budget)
- Property-level performance analysis
- Strategic recommendations for November

## How It Works

### Current Method (Python Script with Full API)

**Enhanced Version** (Recommended):
1. Run: `python3 generate_devonshire_slides.py --month 2025-10`
2. Script queries Google Ads API for data
3. Creates presentation with branded, formatted tables
4. Tables use Estate Blue (#00333D) headers and Stone (#E5E3DB) backgrounds
5. Receive presentation link ready to share

**Basic Version** (Claude Code MCP):
1. Read the markdown report from `/clients/devonshire-hotels/reports/[month]-paid-search-report.md`
2. Use Claude Code to convert data to Google Slides format
3. Call `mcp__google-drive__createGoogleSlides` with structured slide data
4. Receive presentation link ready to share (basic text format)

### Data Sources

- Google Ads API (via MCP) - Campaign performance metrics
- Budget Tracker (Google Sheets) - Budget and pacing data
- Experiment Notes (CSV) - Strategic context
- Email Communications - Client feedback and issues

## Slide Structure

The presentation follows this format (matching September 2025 deck):

1. **Title Slide** - "Paid Search - [Month]"
2. **Executive Summary** - Budget and overall performance
3. **Hotels - Top Performers** - By ROAS ranking
4. **Hotels - Attention Needed** - Underperforming properties
5. **Campaign Type Breakdown** - PMax, Search, Self-Catering splits
6. **Self Catering Campaigns** - Detailed SC performance
7. **The Hide** - Separate £2,000 budget tracking
8. **Weddings** - Placeholder (data when available)
9. **Lismore and The Hall** - Placeholder (data when available)
10. **Key Insights - Highlights** - Performance wins
11. **Key Insights - Areas for Improvement** - Issues and recommendations
12. **Recommendations for Next Month** - Part 1
13. **Recommendations for Next Month** - Part 2 (continuation)

Total: **13-14 slides**

## Monthly Workflow

### End of Month (e.g., Oct 31)
1. Wait 2-3 days into next month for Google Ads data to finalize
2. Review client emails for context on performance
3. Check experiment notes for strategic changes during the month

### Generate Report (e.g., Nov 2-3)
1. Ask Claude Code: "Generate the [Month] Paid Search report for Devonshire"
2. Claude Code will:
   - Query Google Ads data for the completed month
   - Compile performance tables and metrics
   - Generate insights and recommendations
   - Create Google Slides presentation
3. Receive presentation link
4. Review and customize as needed

### Deliver to Client
1. Open the generated presentation
2. Review data accuracy and formatting
3. Make any final adjustments (styling, additional commentary)
4. Copy slides into the shared deck (which includes SEO and other sections)
5. Send to Gary at A Cunning Plan for review
6. Gary forwards to Devonshire Hotels

## Time Savings

**Before Automation**:
- Data queries: 30-45 minutes
- Table creation: 30-45 minutes
- Performance analysis: 30-60 minutes
- Commentary writing: 20-30 minutes
- Slide formatting: 20-30 minutes
**Total: 2-3 hours per month**

**After Automation**:
- Request generation from Claude Code: 2 minutes
- Review and customize: 15-20 minutes
**Total: ~20 minutes per month**

**Monthly Time Saved**: ~2.5 hours

## Brand Colors (Estate Escapes)

The enhanced version uses the official Estate Escapes brand colors:

- **Estate Blue**: `#00333D` - Deep blue for table headers
  - Used for: Header backgrounds, titles, emphasis
  - Text on Estate Blue: White (#FFFFFF) for maximum contrast

- **Stone**: `#E5E3DB` - Light neutral for backgrounds
  - Used for: Data cell backgrounds, subtle backgrounds
  - Text on Stone: Dark gray (#333333) for readability

- **Supporting Colors**:
  - White (#FFFFFF) - Header text, clean backgrounds
  - Dark Gray (#333333) - Data text, readable on light backgrounds

**Why these colors?**
- Helen Hargreave (Marketing Manager, Estate Escapes) provided these official brand colors
- Estate Blue represents Chatsworth properties
- Stone provides elegant, readable contrast
- Professional appearance matching hotel group branding

## Key Features

### Automatic Data Collection
- Queries Google Ads API for all campaign groups
- Calculates metrics (ROAS, CTR, CPA, etc.)
- Sorts properties by performance
- Identifies attention-needed campaigns

### Intelligent Analysis
- Highlights top performers (by ROAS)
- Flags underperforming campaigns
- Calculates budget pacing and variance
- Generates month-over-month comparisons (when previous data available)

### Professional Formatting
- Tables with proper currency and percentage formatting
- Clear visual hierarchy (emojis for status indicators)
- Consistent slide structure matching client expectations
- Ready to copy into shared deck

## Campaign Groupings

### Main Properties (£9,000-£11,730 budget)
- **Hotels**: Devonshire Arms, Cavendish, Beeley Inn, Pilsley Inn, The Fell, Chatsworth Inns
- **Performance Max**: All properties combined (Campaign ID: 18899261254)
- **Locations**: Chatsworth (19654308682), Bolton Abbey (22720114456)
- **Self-Catering**: Chatsworth SC (19534201089), Bolton Abbey SC (22536922700)

### The Hide (£2,000 budget)
- **The Hide**: Current campaign (23069490466) - launched Oct 10, 2025
- **Highwayman Arms**: Paused campaign (21815704991) - pre-rename

### Weddings (separate tracking)
- Campaign IDs to be added when available

### Lismore and The Hall (separate tracking)
- Campaign IDs to be added when available

## Important Notes

### Data Exclusions
- Main properties figures **exclude** The Hide, Castles, and Weddings campaigns
- These are tracked separately with their own budgets
- Paused campaigns with historical spend (like Highwayman Arms) **are included** in totals

### The Hide Timeline
- Launched: October 10, 2025
- Formerly: "The Highwayman"
- October report includes both The Hide (£1,431.28) and Highwayman Arms (£491.81)
- November onwards: The Hide only

### Conversion Tracking
- Conversions include both **direct bookings** and **qualified leads**
- Some properties may have conversion tracking issues (e.g., Bolton Abbey SC in October)
- Always validate zero-conversion campaigns

## Technical Details

### Required Access
- Google Ads API access (Customer ID: 5898250490)
- Google Drive API access (MCP integration)
- Devonshire Hotels account permissions

### MCP Tools Used
- `mcp__google-ads__run_gaql` - Query campaign data
- `mcp__google-drive__createGoogleSlides` - Generate presentation

### File Locations
- **Scripts**: `/tools/monthly-report-generator/`
- **Reports**: `/clients/devonshire-hotels/reports/`
- **CONTEXT.md**: `/clients/devonshire-hotels/CONTEXT.md`
- **Budget Tracker**: Google Sheets (ID: 1hfshBOXryp0LYuU40kE9HKHQocoinfpXZH8TL6Me7Yc)

## Future Enhancements

Potential additions for future versions:

1. **Automated Charts**
   - ROAS trend line by property
   - Spend distribution pie chart
   - Month-over-month comparison graphs

2. **Previous Month Comparison**
   - Automatic MoM delta calculations
   - Performance trend indicators
   - Budget variance analysis

3. **Client Branding**
   - Apply Devonshire Hotels brand colors
   - Add logo to title slide
   - Custom slide layouts

4. **Email Integration**
   - Automatic email to Gary at A Cunning Plan
   - Include presentation link and summary
   - CC Peter Empson

5. **Scheduling**
   - Run automatically on 3rd of each month
   - Auto-generate report when data is finalized
   - Send notification when ready for review

## Troubleshooting

### Presentation Not Created
- Check Google Drive MCP server is configured
- Verify OAuth credentials are valid
- Ensure Claude Code has Drive API access

### Missing Data
- Wait until 2-3 days after month ends for complete data
- Check that campaign IDs are correct in CAMPAIGN_GROUPS
- Verify Google Ads API access for Customer ID 5898250490

### Incorrect Metrics
- Validate date range matches intended month
- Check for paused campaigns that should be included
- Review campaign filter excludes Castles and Weddings

## Questions or Issues?

- **Owner**: Peter Empson (petere@roksys.co.uk)
- **Client Contact**: Gary Lee, A Cunning Plan (garry@acunningplan.co.uk)
- **End Client**: Devonshire Hotels

See also:
- `QUICKSTART.md` - Quick reference guide
- `generate_slides.py` - Python script structure (for reference)
- `/clients/devonshire-hotels/CONTEXT.md` - Client strategic context

---

**Last Updated**: 2025-11-02
**Version**: 2.0 (Phase 2 - Automated Slides)
**Status**: Production Ready ✅
