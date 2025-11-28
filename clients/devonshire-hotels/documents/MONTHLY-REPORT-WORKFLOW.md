# Devonshire Hotels - Monthly Report Generation Workflow

**Purpose**: Complete step-by-step process to replicate monthly performance reports
**Template Based On**: October 2025 report structure
**Estimated Time**: 2-3 hours per report

---

## Pre-Flight Checklist

Before starting, verify you have:
- [ ] Google Ads API access configured (customer ID: 7816697284)
- [ ] Access to all slide templates from previous month
- [ ] Previous month's commentary file for reference
- [ ] CONTEXT.md updated with any strategic changes
- [ ] tasks-completed.md reviewed for October activity

---

## Phase 1: Data Collection (30-45 minutes)

### Step 1.1: Main Property Campaigns Data

Query Google Ads API for main hotel properties (DEV | Properties campaigns, excluding Hide/Highwayman):

```sql
-- Main hotels campaign-level performance
SELECT
  campaign.name,
  metrics.conversions_value_by_conversion_date,
  metrics.cost_micros,
  metrics.conversions_by_conversion_date,
  metrics.clicks,
  metrics.ctr,
  segments.month
FROM campaign
WHERE
  campaign.name LIKE 'DEV | Properties%'
  AND campaign.name NOT LIKE '%Hide%'
  AND campaign.name NOT LIKE '%Highwayman%'
  AND segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
ORDER BY metrics.conversions_value_by_conversion_date DESC
```

**Expected Output**: 6-8 hotel campaigns with revenue, spend, ROAS, bookings, CTR

**Save to**: `data/october-hotels-performance.json` or spreadsheet

### Step 1.2: Search vs PMax Breakdown

```sql
-- Search campaigns
SELECT
  campaign.name,
  metrics.conversions_value_by_conversion_date,
  metrics.cost_micros,
  metrics.conversions_by_conversion_date
FROM campaign
WHERE
  campaign.advertising_channel_type = 'SEARCH'
  AND segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
  AND campaign.name LIKE 'DEV | Properties%'
ORDER BY campaign.name

-- Performance Max campaigns
SELECT
  campaign.name,
  metrics.conversions_value_by_conversion_date,
  metrics.cost_micros,
  metrics.conversions_by_conversion_date
FROM campaign
WHERE
  campaign.advertising_channel_type = 'PERFORMANCE_MAX'
  AND segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
  AND campaign.name LIKE 'DEV | Properties%'
ORDER BY campaign.name
```

**Expected Output**: Individual hotel spend/revenue split by Search and PMax

### Step 1.3: Year-over-Year Data

Query monthly data for current year and previous year (Jan-Oct or Jan-Nov):

```sql
-- Current year monthly (e.g., 2025)
SELECT
  segments.month,
  SUM(metrics.ctr) as ctr,
  SUM(metrics.average_cpc) as avg_cpc,
  SUM(metrics.conversions_by_conversion_date) as conversions,
  SUM(metrics.conversions_value_by_conversion_date) as conv_value,
  SUM(metrics.cost_micros) as cost
FROM campaign
WHERE
  segments.year = 2025
  AND segments.month IN (1,2,3,4,5,6,7,8,9,10,11)
  AND campaign.name LIKE 'DEV | Properties%'
  AND campaign.name NOT LIKE '%Hide%'
  AND campaign.name NOT LIKE '%Highwayman%'
GROUP BY segments.month
ORDER BY segments.month

-- Previous year monthly (e.g., 2024)
[Same query with segments.year = 2024]
```

**Expected Output**: 10-11 months of data for both years

**Calculate**: Percentage changes for each metric by month

### Step 1.4: Location Data

```sql
-- Geographic performance
SELECT
  geographic_view.country_criterion_id,
  metrics.conversions_value_by_conversion_date,
  metrics.cost_micros,
  metrics.conversions_by_conversion_date,
  metrics.clicks,
  metrics.impressions
FROM geographic_view
WHERE
  segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
  AND campaign.name LIKE 'DEV | Properties%'
ORDER BY metrics.conversions_value_by_conversion_date DESC
LIMIT 10
```

**Expected Output**: Top 10 countries/regions by revenue

### Step 1.5: Self-Catering Campaigns

```sql
-- Campaign totals
SELECT
  campaign.name,
  metrics.conversions_value_by_conversion_date,
  metrics.cost_micros,
  metrics.conversions_by_conversion_date,
  metrics.clicks,
  metrics.ctr
FROM campaign
WHERE
  segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
  AND campaign.name LIKE '%Self-Catering%'
ORDER BY campaign.name

-- Ad group breakdown
SELECT
  ad_group.name,
  campaign.name,
  metrics.conversions_value_by_conversion_date,
  metrics.cost_micros,
  metrics.conversions_by_conversion_date,
  metrics.clicks,
  metrics.ctr
FROM ad_group
WHERE
  segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
  AND campaign.name LIKE '%Self-Catering%'
ORDER BY campaign.name, metrics.conversions_value_by_conversion_date DESC
```

**Expected Output**:
- Chatsworth Escapes Self-Catering (campaign + 2-3 ad groups)
- Bolton Abbey Self-Catering (campaign + ad groups)

### Step 1.6: Weddings Campaign

```sql
-- Weddings ad groups
SELECT
  ad_group.name,
  metrics.clicks,
  metrics.ctr,
  metrics.conversions_by_conversion_date as enquiries,
  (metrics.conversions_by_conversion_date / metrics.clicks) * 100 as enquiry_rate
FROM ad_group
WHERE
  segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
  AND campaign.name = 'DEV | Weddings'
ORDER BY metrics.clicks DESC
```

**Expected Output**: 7 ad groups ranked by clicks

### Step 1.7: Exclusive Venues

```sql
-- Castles campaigns
SELECT
  campaign.name,
  metrics.cost_micros,
  metrics.ctr,
  metrics.conversions_by_conversion_date as enquiries
FROM campaign
WHERE
  segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
  AND campaign.name LIKE 'DEV | Castles%'
ORDER BY metrics.cost_micros DESC
```

**Expected Output**: Lismore Castle, The Hall

---

## Phase 2: Slide Generation (60-90 minutes)

### Slide 16: Account Overview

**Template**: `Monthly Report Slides/Slide 16 October 25.html`

**Data to Update**:
1. Change title to current month: "Account Overview - [Month] 2025"
2. Update table rows with top 6-8 hotels:
   ```html
   <tr>
       <td>1</td>
       <td>[Hotel Name]</td>
       <td>£[revenue]</td>
       <td>£[spend]</td>
       <td>[roas]%</td>
       <td>[bookings]</td>
   </tr>
   ```
3. Update footer date range: "[Month] 1-31, 2025"

**Validation**:
- [ ] Hotels ranked by revenue (highest first)
- [ ] ROAS calculated correctly: (revenue / spend) * 100
- [ ] All currency formatted with £ symbol
- [ ] Footer shows correct month

### Slide 17: Year-over-Year Comparison

**Template**: `Monthly Report Slides/Slide 17 October 25 UPDATED.html`

**Data to Update**:
1. Update JavaScript data arrays (lines 151-176):
   ```javascript
   const metrics2024 = {
       ctr: [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov],
       convRate: [...],
       conversions: [...],
       convValue: [...],
       cost: [...],
       roas: [...]
   };

   const metrics2025 = {
       // Same structure with 2025 data
   };
   ```

2. Calculate percentage changes:
   ```javascript
   const percentageChanges = {
       ctr: [(2025_Jan - 2024_Jan) / 2024_Jan * 100, ...],
       // Repeat for all metrics
   };
   ```

3. Update month labels if November data:
   ```javascript
   const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"];
   ```

4. Update footer: "Data: January-[Month] 2024 vs January-[Month] 2025"

**Validation**:
- [ ] All 12 charts render correctly
- [ ] Percentage changes show green (positive) or red (negative) bars
- [ ] Absolute value charts show both 2024 (gray) and 2025 (blue) bars
- [ ] Footer reflects correct date range

### Slide 18: Monthly Performance Trend

**Template**: `Monthly Report Slides/Slide 18 October 25.html`

**Data to Update**:
1. Update JavaScript monthly data (lines 148-159):
   ```javascript
   const monthlyData = {
       months: ['Jan', 'Feb', ..., 'Oct', 'Nov'],
       revenue: [value1, value2, ...],
       spend: [...],
       roas: [...],
       bookings: [...],
       ctr: [...]
   };
   ```

2. Update footer date range

**Validation**:
- [ ] All line charts show upward/downward trends
- [ ] Revenue and spend charts use currency formatting
- [ ] ROAS chart uses 'x' suffix
- [ ] CTR chart uses '%' suffix

### Slide 19: Search vs PMax Breakdown

**Template**: `Monthly Report Slides/Slide 19 October 25.html`

**Data to Update**:
1. Update Search table rows (lines 167-230):
   ```html
   <tr>
       <td>1</td>
       <td>[Hotel Name]</td>
       <td>£[revenue]</td>
       <td>£[spend]</td>
       <td>[roas]%</td>
       <td>[bookings]</td>
   </tr>
   ```

2. Update PMax table rows (lines 244-307)

3. Update totals (lines 231-241, 308-318)

4. Update footer date range

**Validation**:
- [ ] Search table totals match sum of individual rows
- [ ] PMax table totals match sum of individual rows
- [ ] Combined totals = Search + PMax

### Slide 20: Profitability Analysis

**Template**: `Monthly Report Slides/Slide 20 October 25.html`

**Data to Update**:
1. Update JavaScript hotel data (lines 110-124):
   ```javascript
   const hotelData = [
       {name: "Hotel Name", roas: 653, revenue: 8851, bookings: 21},
       // Continue for all hotels
   ];
   ```

2. Sort by ROAS descending

3. Chart will automatically color bars:
   - Green: ROAS ≥ 400%
   - Red: ROAS < 400%

4. Update footer date range

**Validation**:
- [ ] Hotels sorted by ROAS (highest to lowest)
- [ ] Threshold line at 400% is visible
- [ ] Colors reflect profitability (green above, red below)

### Slide 21: Locations Performance

**Template**: `Monthly Report Slides/Slide 21 October 25.html`

**Data to Update**:
1. Update table rows with top 10 locations (lines 117-176):
   ```html
   <tr>
       <td>1</td>
       <td>[Location Name]</td>
       <td>£[revenue]</td>
       <td>£[spend]</td>
       <td>[roas]%</td>
       <td>[bookings]</td>
       <td>[clicks]</td>
       <td>[impressions]</td>
   </tr>
   ```

2. Update total row (lines 177-187)

3. Update footer date range

**Validation**:
- [ ] Locations ranked by revenue
- [ ] Totals match sum of individual rows
- [ ] All metrics formatted correctly

### Slide 22: Self-Catering Ad Groups

**Template**: `Monthly Report Slides/Slide 22 October 25.html`

**Data to Update**:

1. **Chatsworth Escapes Self-Catering ad groups** (lines 167-196):
   ```html
   <tr>
       <td>1</td>
       <td>Chatsworth Self-Catering (General)</td>
       <td>£[revenue]</td>
       <td>£[spend]</td>
       <td>[roas]%</td>
       <td>[bookings]</td>
       <td>[clicks]</td>
       <td>[ctr]%</td>
   </tr>
   ```

2. Check if any ad groups are paused:
   - Query daily impression data to find pause dates
   - Mark paused ad groups with class="paused"
   - Update ad group name to include pause date

3. **Chatsworth Total** row (lines 197-206):
   - Sum of all Chatsworth ad groups

4. **Bolton Abbey Self-Catering** (lines 212-221):
   - Usually single ad group "Bolton Abbey Self-Catering (All)"

5. **Bolton Abbey Total** row (lines 222-231)

6. **Combined Total** row (lines 234-243):
   - Sum of both campaign totals

7. Update footer (lines 248-252):
   - Note any paused ad groups with dates
   - Mention low spend context

**Validation**:
- [ ] Chatsworth subtotal = sum of ad groups
- [ ] Bolton Abbey subtotal = individual ad group
- [ ] Combined total = Chatsworth + Bolton Abbey
- [ ] Paused ad groups styled in gray italic
- [ ] Footer notes any structural changes

### Slide 24: Weddings

**Template**: `Monthly Report Slides/Slide 24 October 25.html`

**Data to Update**:
1. Update ad group rows (lines 118-173):
   ```html
   <tr>
       <td>1</td>
       <td>[Ad Group Name]</td>
       <td>[clicks]</td>
       <td>[ctr]%</td>
       <td>[enquiries]</td>
       <td>[enquiry_rate]%</td>
   </tr>
   ```

2. Rank by clicks (highest first)

3. Calculate enquiry rate: (enquiries / clicks) * 100

4. Update footer date range

**Validation**:
- [ ] Ad groups ranked by clicks
- [ ] Enquiry rates calculated correctly
- [ ] All 7 ad groups included

### Slide 26: Exclusive Venues

**Template**: `Monthly Report Slides/Slide 26 October 25.html`

**Data to Update**:
1. Update Lismore Castle row (lines 132-138):
   ```html
   <tr>
       <td>1</td>
       <td>Lismore Castle (Ireland)</td>
       <td>£[spend]</td>
       <td>[ctr]%</td>
       <td class="alert">[enquiries]</td>
   </tr>
   ```

2. Update The Hall row (lines 139-145)

3. Update footer date range

**Validation**:
- [ ] Both venues included
- [ ] Zero enquiries marked with class="alert" (red)
- [ ] Context boxes explain business model

---

## Phase 3: Commentary Generation (45-60 minutes)

### Step 3.1: Create Commentary File

**Template**: `documents/october-2025-slide-commentary.html`

**Save As**: `documents/[month]-2025-slide-commentary.html`

### Step 3.2: Update Sections

#### KPI Overview

**Key Metrics to Extract**:
- Total revenue, spend, ROAS, bookings for the month
- Month-over-month comparison (vs previous month)
- Year-over-year comparison (vs same month last year)

**Template Structure**:
```html
<div class="commentary-box">
    <h3>Key Takeaway</h3>
    <p><strong>[Context about performance]</strong></p>
    <ul>
        <li><strong>Revenue:</strong> £[amount] ([+/-]X% vs [previous month])</li>
        <li><strong>ROAS:</strong> [value]% ([+/-]X pts vs [previous month])</li>
        <li><strong>Bookings:</strong> [count] ([+/-]X% vs [previous month])</li>
    </ul>
</div>
```

**Critical**:
- Check CONTEXT.md for any known factors (promotions, stock issues, strategic changes)
- Check tasks-completed.md for campaign changes made during the month
- Check knowledge-base for platform updates (2-4 week delayed impact)

#### Individual Hotel Performance

**For Each Hotel**:
1. Identify standout performers (highest ROAS, highest revenue)
2. Identify underperformers (below 400% ROAS threshold)
3. Note significant month-over-month changes (±20% revenue or ROAS)

**Template**:
```html
<li><strong>[Hotel Name] (Rank [X]):</strong> £[revenue] revenue, [roas]% ROAS, [bookings] bookings. [Brief insight about performance]</li>
```

#### Year-over-Year Trends

**Extract from Slide 17 data**:
- Current month vs same month last year
- Highlight significant improvements or declines
- Provide context for changes

**Template**:
```html
<div class="commentary-box">
    <h3>[Month] 2025 vs [Month] 2024 - [Strong Growth / Comparable Performance]</h3>
    <p><strong>[Month] 2025 [outperformed/matched] [Month] 2024:</strong></p>
    <ul>
        <li><strong>CTR:</strong> [2025_value]% vs [2024_value]% = [+/-]X% change</li>
        <li><strong>Conversions:</strong> [2025] vs [2024] = [+/-]X% change</li>
        <li><strong>Revenue:</strong> £[2025] vs £[2024] = [+/-]X% change</li>
        <li><strong>ROAS:</strong> [2025_value]x vs [2024_value]x = [+/-]X% change</li>
    </ul>
</div>
```

#### Search vs Performance Max

**Compare Performance**:
- Which channel drove more revenue?
- Which channel had better ROAS?
- Note any significant shifts in spend allocation

#### Self-Catering Campaigns

**Key Points to Cover**:
1. Total spend across both campaigns
2. Note if spend is low (under £1,500 typically)
3. Individual property performance breakdown
4. Any structural changes (paused ad groups, new properties)

**Template**:
```html
<div class="commentary-box">
    <h3>Campaign Overview - [Low Spend Context]</h3>
    <p><strong>Combined monthly spend:</strong> £[total] across two campaigns ([Campaign1] £[amount], [Campaign2] £[amount]). [Context about spend levels and statistical significance]</p>
    <p><strong>Portfolio changes:</strong> [Note any pauses or launches]</p>
</div>

<div class="commentary-box">
    <h3>Chatsworth Escapes Self-Catering</h3>
    <ul>
        <li><strong>Chatsworth Self-Catering (General):</strong> £[revenue] revenue, [roas]% ROAS, [bookings] bookings from £[spend] spend.</li>
        <li><strong>Hunting Tower:</strong> [Details or note if paused]</li>
        <li><strong>Russian Cottage:</strong> [Details or note if paused]</li>
    </ul>
    <p><strong>Combined:</strong> £[total_revenue] revenue, [combined_roas]% ROAS, [total_bookings] bookings from £[total_spend] spend.</p>
</div>
```

#### Weddings and Exclusive Venues

**Brief Summary**:
- Total enquiries generated
- Spend levels
- Note that these are lead generation campaigns (not direct bookings)

### Step 3.3: Root Cause Analysis

For any significant performance changes (±20% revenue or ROAS), analyze root causes:

**Framework**:

✅ **Your Actions** (controllable):
- Budget changes → Check tasks-completed.md
- Bid strategy adjustments → Check Google Ads Change History
- Campaign launches/pauses → Check tasks-completed.md
- Ad copy changes → Check Google Ads Change History

🌍 **External Factors** (uncontrollable):
- Seasonality → Compare to previous year same month
- Market trends → Check client emails for mentions
- Competitor activity → Limited visibility, note if suspected

🏢 **Client Business** (client-driven):
- Stock issues → Check emails, WebFetch client website
- Pricing changes → Check emails, compare to previous month
- Website updates → WebFetch client site, check emails

⚙️ **Technical Issues**:
- Tracking problems → Check error emails, conversion rate drops
- Pixel issues → Check Analytics vs Ads conversion discrepancies
- Platform bugs → Check knowledge-base for reported issues

📦 **Product-Level Changes** (e-commerce):
- N/A for Devonshire (hotel bookings, not e-commerce)

🔧 **Platform Updates** (Google):
- Algorithm changes → Check knowledge-base/google-ads/platform-updates/
- New features → Check Google Ads UI notifications
- Policy updates → Check client alerts
- **Note**: 2-4 week delayed impact typical

**Critical**: Only cite causes with evidence. No speculation without data.

### Step 3.4: November Priorities

**Standard Items**:
- Continue monitoring [metric] trends
- Review [underperforming campaign] performance
- Consider [strategic opportunity]

**Specific to Current Month**:
- Address any urgent issues identified (e.g., zero conversion campaigns)
- Follow up on tests launched during the month
- Plan for next month seasonality

---

## Phase 4: Quality Assurance (20-30 minutes)

### Data Validation Checklist

- [ ] All slide totals match API query totals
- [ ] ROAS calculations correct: (revenue / spend) * 100
- [ ] Conversion rates correct: (conversions / clicks) * 100
- [ ] Percentage changes calculated correctly: ((new - old) / old) * 100
- [ ] All currency values formatted with £ symbol
- [ ] All percentage values formatted with % symbol
- [ ] All dates show correct month and year

### Slide Validation Checklist

- [ ] Slide 16: Hotels ranked by revenue, totals correct
- [ ] Slide 17: All 12 charts render, data arrays populated
- [ ] Slide 18: Line charts show trends, legend displays
- [ ] Slide 19: Search + PMax totals = combined total
- [ ] Slide 20: ROAS threshold line visible at 400%
- [ ] Slide 21: Locations ranked, totals match
- [ ] Slide 22: Ad group subtotals match campaign totals
- [ ] Slide 24: Weddings enquiry rates calculated
- [ ] Slide 26: Exclusive venues context boxes accurate

### Commentary Validation Checklist

- [ ] Key metrics match slide data
- [ ] All comparisons (MoM, YoY) are accurate
- [ ] Root cause analysis backed by evidence
- [ ] No speculation without data
- [ ] Terminology consistent ("percentage points" not "pts")
- [ ] British spelling throughout
- [ ] HTML structure valid (no unclosed tags)
- [ ] All sections completed

### Brand Compliance Checklist

- [ ] Estate Blue (#00333D) and Stone (#E5E3DB) colors used
- [ ] Arial/Helvetica font throughout
- [ ] ROAS expressed as percentage (576%, not 5.76x)
- [ ] Professional tone maintained
- [ ] No marketing hyperbole

---

## Phase 5: Finalization (10-15 minutes)

### Step 5.1: Update CONTEXT.md

Add new insights to `clients/devonshire-hotels/CONTEXT.md`:

**Performance Patterns Section**:
```markdown
### [Month] 2025 Performance
- **Revenue**: £[amount] ([+/-]X% vs [previous month])
- **ROAS**: [value]% ([+/-]X pts vs [previous month])
- **Key Insight**: [1-2 sentence summary of standout finding]
- **Action Taken**: [Any changes made in response]
```

### Step 5.2: Create Status Document

Save current status for future reference:

**File**: `MONTHLY-REPORT-STATUS-[MONTH]-2025.md`

**Contents**:
- Completion checklist for all slides
- Outstanding tasks (if any)
- Data sources used
- Query history
- Review notes

### Step 5.3: Archive Previous Month

Move previous month's slides to archive if needed:

```bash
mkdir -p "Monthly Report Slides/Archive/October 2025"
# Keep current month in main folder
```

---

## Troubleshooting

### Issue: API Authentication Failures

**Symptoms**: 401 Unauthorized or CUSTOMER_NOT_FOUND errors

**Solutions**:
1. Verify customer ID is correct: 7816697284
2. Check MCP server configuration in `.mcp.json`
3. Verify Google Ads API credentials are valid
4. Check if account access permissions changed

**Workaround**: Export data from Google Ads UI manually

### Issue: Missing Data for Ad Groups

**Symptoms**: Some ad groups show no data or TBC placeholders

**Solutions**:
1. Check if ad groups were paused during the month
2. Query daily impression data to find activity dates
3. Verify campaign name filters in queries are correct

**Query to Check Pauses**:
```sql
SELECT
  segments.date,
  ad_group.name,
  ad_group.status,
  metrics.impressions
FROM ad_group
WHERE
  segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
  AND campaign.name LIKE '%Self-Catering%'
ORDER BY ad_group.name, segments.date
```

### Issue: Chart Not Rendering

**Symptoms**: Blank space where chart should appear

**Solutions**:
1. Open browser console (F12) to check for JavaScript errors
2. Verify Chart.js library loaded: `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>`
3. Check data array syntax is valid JavaScript
4. Verify canvas element has correct ID

### Issue: Totals Don't Match

**Symptoms**: Slide totals ≠ API query totals

**Solutions**:
1. Check date range consistency across all queries
2. Verify campaign name filters match exactly
3. Check for duplicate entries (same campaign counted twice)
4. Verify "by conversion time" vs "by click time" metrics used consistently

**Validation Query**:
```sql
-- Get account-level totals to verify
SELECT
  SUM(metrics.conversions_value_by_conversion_date) as total_revenue,
  SUM(metrics.cost_micros) as total_spend,
  SUM(metrics.conversions_by_conversion_date) as total_conversions
FROM campaign
WHERE
  segments.date BETWEEN 'YYYY-MM-01' AND 'YYYY-MM-31'
  AND campaign.name LIKE 'DEV | Properties%'
```

---

## Time-Saving Tips

1. **Create a Data Collection Spreadsheet**: Build a template spreadsheet with all query outputs. Fill in once, reference for all slides.

2. **Use Find & Replace for Dates**: After duplicating previous month's files, use find/replace to update all date references at once.

3. **Automate ROAS Calculations**: Use spreadsheet formulas to calculate ROAS from revenue/spend, then copy values to HTML.

4. **Save Query Templates**: Keep SQL queries in a text file, update dates only each month.

5. **Version Control**: Use git commits for each major update phase ("Data collection complete", "Slides updated", "Commentary finalized").

6. **Parallel Processing**: While waiting for API queries, work on commentary structure and previous month review.

---

## Monthly Variations

### November (Current Month)
- Include Halloween/Bonfire Night impact in external factors
- Note Q4 seasonal patterns starting
- Christmas booking window opening

### December
- Christmas/New Year booking behavior
- Reduced budget expectations (holiday period)
- Year-end summary context

### January
- New Year comparison artifacts (low December baseline)
- Post-Christmas recovery patterns
- Account restructure opportunities

### February-March
- Valentine's Day (February)
- Mother's Day planning (March)
- Spring booking season beginning

### April-June
- Easter impact (April)
- Wedding season peak (May-June)
- Summer booking window

### July-August
- Peak summer performance
- Last-minute booking behavior
- Self-catering demand high

### September-October
- Back-to-school quieter period
- Autumn breaks
- Award publicity effects (check for industry news)

---

## Files Required for Next Month

Keep these as templates:

### Slide Templates
```
Monthly Report Slides/
├── Slide 16 October 25.html
├── Slide 17 October 25 UPDATED.html
├── Slide 18 October 25.html
├── Slide 19 October 25.html
├── Slide 20 October 25.html
├── Slide 21 October 25.html
├── Slide 22 October 25.html
├── Slide 24 October 25.html
└── Slide 26 October 25.html
```

### Commentary Template
```
documents/october-2025-slide-commentary.html
```

### Reference Documents
```
CONTEXT.md
tasks-completed.md
MONTHLY-REPORT-STATUS-OCTOBER-2025.md
MONTHLY-REPORT-WORKFLOW.md (this file)
```

### SQL Query Library
```
queries/
├── 01-main-hotels-performance.sql
├── 02-search-vs-pmax.sql
├── 03-year-over-year.sql
├── 04-locations.sql
├── 05-self-catering.sql
├── 06-weddings.sql
└── 07-exclusive-venues.sql
```

---

## Quick Reference: Key Numbers

### Customer ID
- **Google Ads**: 7816697284

### Campaign Names
- **Main Hotels**: `DEV | Properties%` (exclude Hide, Highwayman)
- **Self-Catering**: `%Self-Catering%`
- **Weddings**: `DEV | Weddings`
- **Exclusive Venues**: `DEV | Castles%`

### Important Metrics
- **By Conversion Time**: `conversions_by_conversion_date`, `conversions_value_by_conversion_date`
- **ROAS Calculation**: (revenue / spend) * 100
- **Profitability Threshold**: 400% ROAS

### Brand Colors
- **Estate Blue**: #00333D
- **Stone**: #E5E3DB
- **Positive Green**: #2E7D32
- **Negative Red**: #C62828

---

## Success Criteria

Report is complete when:
- [ ] All 9 slides generated with current month data
- [ ] Commentary document complete with all sections
- [ ] All totals validated and accurate
- [ ] CONTEXT.md updated with new insights
- [ ] Status document created for future reference
- [ ] Previous month archived (if applicable)
- [ ] Client review scheduled
- [ ] Any urgent issues flagged in commentary

---

**Next Update**: After November 2025 report generation, update this workflow with any improvements or lessons learned.

**Maintained By**: Pete's Brain (Claude Code)
**Version**: 1.0
**Last Updated**: 2025-11-06
