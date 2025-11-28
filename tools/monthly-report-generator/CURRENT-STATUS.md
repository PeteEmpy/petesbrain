# Monthly Report Generator - Current Status

**Last Updated:** 2025-11-04

## Overview

The Monthly Report Generator for Devonshire Hotels is now producing 11 complete slides for the October 2025 report, ready for insertion into Google Slides.

## Completed Slides

All slide images are generated in: `clients/devonshire-hotels/reports/october-2025-images/`

### Slide 1: Core Hotel Properties - Metric Boxes
- **File:** `01-metric-boxes.png`
- **Format:** 4 metric boxes (Spend, Revenue, ROAS, Conversions)
- **Content:** October vs September comparison with percentage changes
- **Footnote:** Explains data includes core hotel properties only, excludes self-catering/weddings/specialty properties
- **Status:** ✅ Complete

### Slide 2: Hotels - Individual Property Performance
- **File:** `02-hotels-breakdown.png`
- **Format:** Table with 6 hotel properties ranked by revenue
- **Columns:** Rank, Property, Revenue, Spend, ROAS, Conversions
- **Status:** ✅ Complete

### Slide 3: Performance Max Campaign Results
- **File:** `03-pmax-results.png`
- **Format:** Table showing PMax campaign performance
- **Status:** ✅ Complete

### Slide 4: Search Campaign Results
- **File:** `04-search-results.png`
- **Format:** Table showing Search campaign performance
- **Status:** ✅ Complete

### Slide 5: Hotels - Overall Profitability
- **File:** `05-profitability-chart.png`
- **Format:** Horizontal bar chart showing ROAS by property
- **Status:** ✅ Complete

### Slide 6: Location Based Search Campaigns
- **File:** `06-locations-table.png`
- **Format:** Table with 2 location-based campaigns
- **Columns:** Rank, Campaign, Revenue, Spend, ROAS, Conversions
- **Status:** ✅ Complete

### Slide 7: Self Catering Campaign Performance
- **File:** `07-self-catering-table.png`
- **Format:** Table with 7 ad groups (including Russian Cottage)
- **Ad Groups:**
  - Chatsworth Estate Cottages
  - Chatsworth Self Catering
  - Peak District Cottages
  - Shepherds Huts
  - Hunting Tower
  - Russian Cottage (low activity, may be paused in future)
  - Yorkshire Cottages
- **Columns:** Ad Group, Impressions, Clicks, CTR, Spend, Revenue, ROAS
- **Status:** ✅ Complete - Shows all 7 ad groups with accurate October data

### Slide 8: The Hide / Highwayman
- **File:** `08-the-hide-table.png`
- **Format:** Table with 2 campaigns
- **Campaigns:**
  - The Hide (launched 10th October)
  - Highwayman Arms
- **Columns:** Campaign, Impressions, Clicks, CTR, Spend, Revenue, ROAS, Conversions
- **Note:** Includes yellow note box explaining tracking investigation for The Hide
- **Status:** ✅ Complete - Factual tracking note added (non-accusatory)

### Slide 8a: Hide & Highwayman Trends (NEW)
- **File:** `08a-hide-highwayman-trends.png`
- **Format:** 6 line charts arranged in 2 rows of 3
- **Top Row:**
  - Clicks
  - CTR
  - ROAS
- **Bottom Row:**
  - Conversions
  - Conversion Rate
  - Spend
- **Timeline:** January 2025 - October 2025 (10 months)
- **Special Feature:** Red vertical dashed line at October marking The Hide launch
- **Data Source:** `query_hide_highwayman_history.py` - consolidated Hide + Highwayman performance
- **Status:** ✅ Complete - All 6 charts showing monthly trends with Hide launch marker

### Slide 9: Weddings
- **File:** `09-weddings-table.png`
- **Format:** Table with 8 wedding ad groups
- **Columns:** Ad Group, Impressions, Clicks, CTR, Spend, Revenue, ROAS, Conversions
- **Status:** ✅ Complete - No tracking commentary per user feedback

### Slide 10: Lismore and The Hall
- **File:** `10-lismore-hall-table.png`
- **Format:** Table with 3 ad groups across 2 campaigns
- **Columns:** Campaign, Ad Group, Impressions, Clicks, CTR, Spend, Revenue, ROAS, Conversions
- **Status:** ✅ Complete - No tracking commentary per user feedback

## Viewer Tool

### HTML Slide Viewer
- **File:** `clients/devonshire-hotels/reports/october-2025-images/view-all-slides.html`
- **Features:**
  - Sticky navigation bar with quick links to all 11 slides
  - Scrollable single-page view
  - Devonshire brand styling (Estate Blue #00333D)
  - Opens directly in browser for easy review
- **Status:** ✅ Complete and functional

## Key Scripts

### Main Generator
- **File:** `generate_slide_images.py`
- **Purpose:** Generates all 11 slide images from October data
- **Brand Colors:**
  - Estate Blue: #00333D
  - Stone: #E5E3DB
  - Dark Gray: #4A4A4A
  - White: #FFFFFF
- **Dependencies:** matplotlib, pandas
- **Usage:** `python3 generate_slide_images.py`

### Data Query Scripts

#### `query_hide_highwayman_history.py`
- **Purpose:** Query monthly consolidated performance for Hide + Highwayman (Jan-Oct 2025)
- **Customer ID:** 5898250490 (Devonshire Group)
- **Metrics:** Clicks, impressions, CTR, cost, revenue, conversions
- **Note:** Uses two separate GAQL queries to avoid OR syntax errors

#### `query_the_hide.py`
- **Purpose:** Query October data for Hide and Highwayman campaigns separately
- **Used for:** Populating Slide 8 table data

#### `query_ad_groups.py`
- **Purpose:** Query all ad groups with October activity
- **Used for:** Validating self-catering, weddings, and other ad group data

## Important Notes

### The Hide Campaign
- **Launch Date:** 10th October 2025
- **Tracking Issue:** Only 3 conversions tracked despite £1,460 spend
- **Context:** Email from Oct 27 mentions only 1 booking tracked from £2,000 budget
- **Slide Note:** "The Hide launched 10th October. Conversion tracking setup is being investigated. Tracked performance may not reflect actual bookings."
- **User Guidance:** Factual, non-accusatory tone per user request

### Russian Cottage Ad Group
- **Current Status:** Active in October with minimal activity (104 impressions, 26 clicks)
- **User Note:** May be paused in future but must be included in October report
- **Action:** Included in self-catering table as requested

### GAQL Syntax Learning
- **Issue:** OR conditions with parentheses cause syntax errors in GAQL
- **Solution:** Split into separate queries and consolidate results in Python
- **Example:** Query Hide and Highwayman separately, then merge monthly data

## Data Quality

All slide data reflects actual October 2025 performance from Google Ads API:
- ✅ Self-catering: 7 ad groups verified
- ✅ The Hide tracking note: Factual and non-accusatory
- ✅ Weddings/Lismore/Hall: Clean tables without tracking commentary
- ✅ Hide/Highwayman trends: 10 months of consolidated historical data
- ✅ Customer ID: 5898250490 (correct Devonshire Group ID)
- ✅ Footnotes: All 11 slides now include small, unobtrusive footnotes explaining data sources, date ranges, and criteria used

## Next Steps (When Needed)

1. **Copy slide images** to Google Slides presentation
2. **Replace September slides** with October equivalents
3. **Verify formatting** matches brand guidelines
4. **Add any commentary slides** between data slides if needed
5. **Final review** with client

## File Locations

```
/Users/administrator/Documents/PetesBrain/
├── clients/devonshire-hotels/
│   ├── reports/october-2025-images/
│   │   ├── 01-metric-boxes.png
│   │   ├── 02-hotels-breakdown.png
│   │   ├── 03-pmax-results.png
│   │   ├── 04-search-results.png
│   │   ├── 05-profitability-chart.png
│   │   ├── 06-locations-table.png
│   │   ├── 07-self-catering-table.png
│   │   ├── 08-the-hide-table.png
│   │   ├── 08a-hide-highwayman-trends.png (NEW)
│   │   ├── 09-weddings-table.png
│   │   ├── 10-lismore-hall-table.png
│   │   └── view-all-slides.html
│   └── emails/
│       ├── 2025-10-10_sent-re-the-hide-urls.md
│       └── 2025-10-30_sent-re-ppc-landing-page.md
└── tools/monthly-report-generator/
    ├── generate_slide_images.py
    ├── query_hide_highwayman_history.py
    ├── query_the_hide.py
    ├── query_ad_groups.py
    └── CURRENT-STATUS.md (this file)
```

## Technical Details

### Python Environment
- **Virtual Environment:** `.venv` in tools/monthly-report-generator/
- **Key Dependencies:**
  - matplotlib (chart generation)
  - google-ads-googleads (API access)
  - pandas (data manipulation)

### Google Ads API
- **Config File:** `~/google-ads.yaml`
- **Customer ID:** 5898250490
- **Authentication:** OAuth via google-ads-googleads library
- **Query Language:** GAQL (Google Ads Query Language)

### Image Generation
- **Format:** PNG
- **Resolution:** 300 DPI
- **Size:** 14" x 8" (1400px x 800px at 100 DPI)
- **Fonts:** System defaults (matplotlib)
- **Color Space:** RGB

## Recent Changes (Nov 4, 2025)

1. ✅ Added Slide 8a (Hide/Highwayman trends) with 6 line charts
2. ✅ Updated HTML viewer to include new slide between 8 and 9
3. ✅ Added spend chart as 6th metric in trends slide
4. ✅ Verified all historical data (Jan-Oct 2025) for trends
5. ✅ Added Hide launch marker (red vertical line) at October
6. ✅ Adjusted metric boxes "vs September" text positioning (moved up from border)
7. ✅ Added footnotes to ALL slides explaining data sources and criteria
8. ✅ All 11 slides generated successfully with accurate October data and footnotes

## Known Issues

None currently. All slides generating successfully and viewer functioning as expected.

## Usage

### Generate All Slides
```bash
cd /Users/administrator/Documents/PetesBrain/tools/monthly-report-generator
source .venv/bin/activate
python3 generate_slide_images.py
```

### View All Slides in Browser
```bash
open /Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/reports/october-2025-images/view-all-slides.html
```

### Query Individual Data
```bash
# Hide/Highwayman October data
python3 query_the_hide.py

# Hide/Highwayman historical trends (Jan-Oct)
python3 query_hide_highwayman_history.py

# All ad groups for October
python3 query_ad_groups.py
```
