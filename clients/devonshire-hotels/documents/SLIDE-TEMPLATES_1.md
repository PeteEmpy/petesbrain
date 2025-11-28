# Monthly Report Slide Templates

This document tracks all slide templates created for the Devonshire monthly report.

## Slide 16: KPI Comparison

**Purpose**: Show month-over-month performance at a glance

**Template Location**: Reference `Slide 16 October 25.html` as template

**Data Required**:
- Current month: Conversions by time, Conversion value by time, Spend, Impressions, Clicks
- Previous month: Same metrics for comparison
- Calculations: ROAS (by time), CTR, Daily impressions average, % changes

**KPIs Displayed**:
1. Conversion Value by Time (£)
2. ROAS Over Time (%)
3. Total Spend (£)
4. Total Bookings (count)
5. Daily Impressions (average)
6. Overall CTR (%)

**GAQL Query Pattern**:
```sql
SELECT
  metrics.cost_micros,
  metrics.conversions_by_conversion_date,
  metrics.conversions_value_by_conversion_date,
  metrics.impressions,
  metrics.clicks
FROM campaign
WHERE segments.date BETWEEN '[YYYY-MM-01]' AND '[YYYY-MM-31]'
  AND campaign.name LIKE 'DEV | Properties%'
  AND campaign.name NOT LIKE '%Hide%'
  AND campaign.name NOT LIKE '%Highwayman%'
  AND campaign.status IN ('ENABLED', 'PAUSED')
```

**Layout**:
- 3x2 grid of KPI boxes
- Estate Blue (#00333D) for values and headers
- Stone (#E5E3DB) for box backgrounds
- Up arrows (green) for positive changes
- Down arrows (red) for negative changes
- 3-4 word description under each change percentage

**Future Replication**:
1. Copy `Slide 16 October 25.html`
2. Run GAQL query for new month and previous month
3. Calculate totals and percentages
4. Update HTML with new values
5. Save as `Slide 16 [Month] [YY].html`

---

---

## Slide 17: Year-over-Year Performance

**Purpose**: Compare 2024 vs 2025 performance month-by-month across key metrics

**Template Location**: Reference `Slide 17 October 25.html` as template

**Data Source**: Google Ads API (via MCP) - pulls data directly, no Excel import needed

**Data Required**:
- Monthly aggregated data for each year (Jan-Oct)
- Metrics: Cost, Conversions by time, Conversion value by time, Impressions, Clicks
- Derived calculations: CTR, Conversion rate, ROAS

**GAQL Query Pattern** (for each month):
```sql
SELECT
  metrics.cost_micros,
  metrics.conversions_by_conversion_date,
  metrics.conversions_value_by_conversion_date,
  metrics.impressions,
  metrics.clicks
FROM campaign
WHERE segments.date BETWEEN '[YYYY-MM-01]' AND '[YYYY-MM-31]'
  AND campaign.name LIKE 'DEV | Properties%'
  AND campaign.name NOT LIKE '%Hide%'
  AND campaign.name NOT LIKE '%Highwayman%'
  AND campaign.status IN ('ENABLED', 'PAUSED')
```

**Charts Displayed** (12 total):

**Percentage Change Charts (6)**:
1. CTR % Change (2024 vs 2025)
2. Conversion Rate % Change
3. Conversions % Change
4. Conversion Value % Change
5. Cost % Change
6. ROAS % Change

**Absolute Value Charts (6)**:
1. CTR (2024 vs 2025 side-by-side bars)
2. Conversion Rate
3. Conversions
4. Conversion Value
5. Cost
6. ROAS

**Layout**:
- 3x2 grid for each section (percentage change, then absolute values)
- Estate Blue (#00333D) for 2025 bars
- Light Gray (#C0C0C0) for 2024 bars
- Green bars for positive % changes, Red for negative
- Stone (#E5E3DB) for chart backgrounds

**Technology**:
- Chart.js for interactive visualizations
- Self-contained HTML file (no external dependencies except CDN)
- All data embedded in JavaScript

**Future Replication**:
1. Copy `Slide 17 October 25.html`
2. Query Google Ads MCP for each month of both years (Jan-current month)
3. Aggregate campaign-level data to monthly totals
4. Update the `data` object in JavaScript with new values
5. Charts automatically regenerate from the updated data
6. Save as `Slide 17 [Month] [YY].html`

**Note**: This slide replaces the old Excel-based workflow. No longer need to:
- Download Excel files from Google Ads UI
- Run Devonshire Dashboard.app
- Take screenshots of generated PNGs

**Old Workflow (Deprecated)**:
- Devonshire Dashboard.app (in Applications folder)
- Required Excel file: `Account performance by month DEV [Month] 2025.xlsx`
- Generated PNG files on Desktop
- Source code: `~/Downloads/DevonshireYOYApp/main.py`

---

## Slide 18: Individual Hotel Performance

**Purpose**: Rank hotels by total booking revenue with consolidated Search + PMax data

**Template Location**: Reference `Slide 18 October 25.html` as template

**Data Required**:
- Search campaign data by hotel (by conversion time)
- PMax asset group data by hotel (standard conversions)
- Consolidate by matching hotel names in campaigns/asset groups

**GAQL Query Patterns**:

Search campaigns:
```sql
SELECT
  campaign.name,
  metrics.cost_micros,
  metrics.conversions_by_conversion_date,
  metrics.conversions_value_by_conversion_date
FROM campaign
WHERE segments.date BETWEEN '[YYYY-MM-01]' AND '[YYYY-MM-31]'
  AND campaign.name LIKE 'DEV | Properties%'
  AND campaign.name NOT LIKE '%Hide%'
  AND campaign.name NOT LIKE '%Highwayman%'
  AND campaign.name NOT LIKE '%Castles%'
  AND campaign.name NOT LIKE '%Weddings%'
  AND campaign.name NOT LIKE '%Self-Catering%'
```

PMax asset groups:
```sql
SELECT
  campaign.name,
  asset_group.name,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM asset_group
WHERE segments.date BETWEEN '[YYYY-MM-01]' AND '[YYYY-MM-31]'
  AND campaign.name LIKE 'DEV | Properties%'
  [same exclusions as above]
```

**Columns**:
1. Rank (sorted by Total Booking Revenue descending)
2. Hotel Name
3. Total Booking Revenue (Search + PMax conversion value)
4. Total Spend (Search + PMax cost)
5. ROAS (calculated: revenue / spend * 100)
6. Number of Bookings (Search + PMax conversions)

**Layout**:
- Single table with Estate Blue header
- Alternating Stone (#E5E3DB) backgrounds on rows
- 17px numbers, 18px hotel names, 20px rank

**Typography** (STANDARD for all slides):
- Hotel names: 18px, font-weight 600, Estate Blue
- Numbers: 17px, font-weight 500, right-aligned
- Rank: 20px, bold, centered, Estate Blue

**Future Replication**:
1. Query Search campaigns for new month
2. Query PMax asset groups for new month
3. Consolidate by hotel (match campaign/asset group names to hotels)
4. Calculate totals and ROAS
5. Sort by revenue descending
6. Update HTML table rows
7. Save as `Slide 18 [Month] [YY].html`

---

## Slide 19: Search vs Performance Max Comparison

**Purpose**: Show separate breakdowns of Search and PMax performance by hotel

**Template Location**: Reference `Slide 19 October 25.html` as template

**Data Required**:
- Same queries as Slide 18, but keep Search and PMax separate (don't consolidate)

**Layout**:
- Two identical tables: "Search Campaigns" then "Performance Max Asset Groups"
- Same column structure as Slide 18
- Each ranked independently by revenue

**Note**:
- Search uses "by conversion time" metrics
- PMax uses standard conversion metrics (API limitation at asset_group resource level)
- Footer clarifies this difference

**Future Replication**:
1. Use same queries as Slide 18
2. Keep Search and PMax data separate
3. Create two tables with identical structure
4. Rank each independently
5. Save as `Slide 19 [Month] [YY].html`

---

## Slide 20: Hotel Profitability Chart

**Purpose**: Visual representation of hotel profitability (ROAS) using bar chart

**Template Location**: Reference `Slide 20 October 25.html` as template

**Data Required**:
- Consolidated hotel ROAS data from Slide 18
- Sort by ROAS descending

**Technology**:
- Chart.js for bar chart visualization
- 8 shades of Estate Blue (darkest to lightest)

**Chart Configuration**:
```javascript
const hotelData = [
    { name: "Hotel Name", roas: 857 },
    // ... sorted by ROAS descending
];

const estateBlueShades = [
    '#00333D', // Darkest
    '#004D5A',
    '#006677',
    '#008094',
    '#0099B1',
    '#33B3CE',
    '#66CCEB',
    '#99E6FF'  // Lightest
];
```

**Layout**:
- Vertical bar chart
- Y-axis: ROAS percentage (begins at 0)
- X-axis: Hotel names (rotated 45° for readability)
- Bars descend left to right (highest ROAS on left)
- Stone background for chart container

**Future Replication**:
1. Copy `Slide 20 October 25.html`
2. Extract ROAS data from Slide 18
3. Update `hotelData` array in JavaScript
4. Ensure sorted by ROAS descending
5. Charts regenerate automatically
6. Save as `Slide 20 [Month] [YY].html`

---

## Future Slides

Add new slide templates here as they're created...

---

**Last Updated**: 2025-11-03
