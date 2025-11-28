# Devonshire Hotels - Monthly Report Slides

This folder contains HTML slides for the monthly Paid Search report presented to A Cunning Plan.

## Workflow

1. **Generate HTML slides** using scripts or manual creation
2. **Open in browser** and take screenshots
3. **Insert into Google Slides** presentation
4. **Send to Gary** at A Cunning Plan

## Slide Structure (October 2025)

### Slide 16: KPI Comparison
- **File**: `Slide 16 October 25.html`
- **Content**: 6 KPI boxes comparing October vs September
  - Conversion Value by Time
  - ROAS Over Time
  - Total Spend
  - Total Bookings
  - Daily Impressions
  - Overall CTR
- **Layout**: 3x2 grid, Estate Blue KPI values, up/down arrows with percentages
- **Campaigns**: DEV | Properties (excluding Hide, Highwayman, Castles, Weddings)
- **⚠️ CRITICAL**: Always use "by conversion time" metrics

### Slide 17: Year-over-Year Performance
- **File**: `Slide 17 October 25.html`
- **Content**: 12 charts comparing 2024 vs 2025 month-by-month
  - 6 Percentage Change Charts: CTR, Conv. Rate, Conversions, Conv. Value, Cost, ROAS
  - 6 Absolute Value Charts: Same metrics with side-by-side bars
- **Layout**: Two sections with 3x2 grids, Chart.js interactive visualizations
- **Data Source**: Google Ads API via MCP (direct queries, no Excel needed)
- **Campaigns**: DEV | Properties (excluding Hide, Highwayman, Castles, Weddings)
- **⚠️ CRITICAL**: Always use "by conversion time" metrics
- **Note**: Replaces old Devonshire Dashboard.app workflow

### Slide 18: Individual Hotel Performance
- **File**: `Slide 18 October 25.html`
- **Content**: Table ranking hotels by total booking revenue
- **Data**: Consolidated Search + PMax asset groups per hotel
- **Columns**: Rank, Hotel Name, Total Booking Revenue, Total Spend, ROAS, Number of Bookings
- **Layout**: Single table with Estate Blue header, alternating Stone row backgrounds
- **⚠️ CRITICAL**: Always use "by conversion time" metrics

### Slide 19: Search vs Performance Max Comparison
- **File**: `Slide 19 October 25.html`
- **Content**: Two tables comparing Search campaigns vs PMax asset groups
- **Data**: Separate breakdowns for Search and PMax performance by hotel
- **Layout**: Two identical table structures (Search first, then PMax)
- **Note**: PMax uses standard conversion metrics (API limitation at asset_group level)

### Slide 20: Hotel Profitability Chart
- **File**: `Slide 20 October 25.html`
- **Content**: Vertical bar chart showing ROAS by hotel
- **Data**: Combined Search + PMax ROAS, sorted descending
- **Layout**: Chart.js bar chart with 8 shades of Estate Blue (darkest = highest ROAS)
- **Visual**: Bars descend left to right, hotel names rotated 45°

## Creating Future Monthly Slides

When creating slides for November, December, etc.:

1. **Copy the template** from previous month
2. **Update the data** with new month's metrics
3. **Update comparisons** to compare against previous month
4. **Save as**: `Slide [number] [Month] [Year].html`
5. **Document any new slides** in this README

## Data Requirements

### Always Use "By Conversion Time" Metrics
- `metrics.conversions_by_conversion_date`
- `metrics.conversions_value_by_conversion_date`
- This matches what client sees in Google Ads interface

### Campaign Filter
```
WHERE campaign.name LIKE 'DEV | Properties%'
  AND campaign.name NOT LIKE '%Hide%'
  AND campaign.name NOT LIKE '%Highwayman%'
  AND campaign.status IN ('ENABLED', 'PAUSED')
```

## Styling Standards

- **Colors**: Estate Blue (#00333D), Stone (#E5E3DB)
- **Font**: Arial, 14px minimum
- **No Emojis**: Clean professional design
- **Brand Consistency**: Match Devonshire brand guidelines

## Notes

- Each slide is self-contained HTML that can be opened in any browser
- Screenshots should be high quality (retina if possible)
- File naming: `Slide [number] [Month] [YY].html` (e.g., "Slide 16 October 25.html")

---

**Last Updated**: 2025-11-03
**Next Report Due**: Early December 2025 (for November data)
