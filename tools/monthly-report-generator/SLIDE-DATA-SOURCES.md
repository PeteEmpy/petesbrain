# Devonshire Hotels - Paid Search Slides Data Source Analysis

**Purpose**: Map each slide in the September 2025 deck to its data source
**Goal**: Identify what data we have vs. what we need to create

---

## Slide Structure from September 2025

### Slide 14: Title Slide
**Content**: "Paid Search - September 2025"
**Data Source**: Static text (month name)
**Status**: ✅ Easy to generate

---

### Slide 15: Overall Performance Summary (Image)
**Content**: Single large metrics table/image
**Data Source**: **NEEDS INVESTIGATION**
**Questions**:
- What metrics are shown?
- Is this the Executive Summary table?
- Where does this image come from?

**Action**: Need to look at the actual image content

---

### Slide 16: Hotels Overview
**Content**: Title "Hotels" + Images
**Data Source**: **NEEDS INVESTIGATION**
**Images in slide**:
- Image ID: g384de62e0b8_0_5
- Image ID: g384de62e0b8_0_6

**Action**: Need to see what these images contain

---

### Slide 17: Hotels - Multiple Images
**Content**: Title "Hotels" + 6 images
**Data Source**: **NEEDS INVESTIGATION**
**Images**: 6 separate image elements (IDs: 0_65, 0_66, 0_67, 0_68, 0_69, 0_70)

**Likely Content**:
- Individual hotel property tables?
- Performance charts?

**Action**: Need to view actual images

---

### Slide 18: Hotels - Single Image
**Content**: Title "Hotels" + 1 image
**Data Source**: **NEEDS INVESTIGATION**
**Image ID**: g384de62e0b8_0_87

**Action**: Need to see what this image contains

---

### Slide 19: Hotels - Breakdown with Commentary
**Content**:
- Title: "Hotels"
- Text: "This is a breakdown of the performance of the individual hotels. The Chatsworth Estate Hotels campaign targets this page..."
- Image: Table showing individual hotel performance

**Data Source**:
- ✅ Google Ads API - Campaign performance by property
- Query: Individual hotel campaigns (Campaign IDs in CAMPAIGN_GROUPS['hotels'])

**Metrics Needed**:
- Spend, Revenue, Conversions, ROAS, Clicks, CTR by property

**Current Status**:
- ✅ We have this data in October markdown report (Hotels - Top Performers table)
- ✅ HTML report includes this table
- 🔄 Need to format as image for slides

---

### Slide 20: Hotels - Campaign Type Breakdown
**Content**:
- Title: "Hotels"
- Text: "The breakdown of the campaign types was as follow"
- Image: Table showing campaign type split

**Data Source**:
- ✅ Google Ads API - Performance by campaign type
- Breakdown: Performance Max vs. Search campaigns

**Metrics Needed**:
- Spend, Revenue, Conversions, ROAS by channel type

**Current Status**:
- ✅ We have this in October markdown report (Campaign Type Breakdown)
- ✅ HTML report includes this table
- 🔄 Need to format as image for slides

---

### Slide 21: Hotels - Profitability
**Content**:
- Title: "Hotels"
- Text: "Their overall profitability"
- Image: Profitability table

**Data Source**: **UNCLEAR**
**Questions**:
- What metrics define "profitability"?
- Is this just ROAS ranking?
- Or profit margin calculation (Revenue - Spend)?

**Action**: Need to see the actual table to understand metrics

---

### Slide 22: Hotels - Location Campaigns
**Content**:
- Title: "Hotels"
- Text: "This is the performance of the location based search campaigns."
- Image: Location campaign performance table

**Data Source**:
- ✅ Google Ads API - Location campaigns
- Campaigns: "Locations (Chatsworth)" and "Locations (Bolton Abbey)"

**Metrics Needed**:
- Spend, Revenue, Conversions, ROAS for location campaigns

**Current Status**:
- ✅ We have this data in October markdown report (included in top performers)
- 🔄 Need separate table just for location campaigns
- 🔄 Need to format as image for slides

---

### Slide 23: Hotels - Budget Performance & Commentary
**Content**:
- Title: "Hotels"
- Long commentary text about September performance:
  - "Spend for September came in at £370 below budget..."
  - "Devonshire's core hotel property portfolio achieved exceptional efficiency optimization..."
  - ROAS improvements, spend optimization, etc.

**Data Source**:
- ✅ Google Ads API - Overall spend and revenue
- ✅ Budget Tracker - Budget vs. actual comparison
- ✅ Month-over-month comparison (August vs. September)

**Metrics Needed**:
- Budget vs. Actual Spend
- Variance
- MoM ROAS comparison
- MoM spend comparison
- MoM CTR comparison

**Current Status**:
- ✅ We have budget/actual in October markdown report
- ❌ We don't have MoM comparisons yet
- 🔄 Need to add MoM calculations

**Action**: Add month-over-month comparison logic

---

### Slide 24: Self Catering
**Content**:
- Title: "Self Catering"
- Text: "The self-catering campaigns are now going to be reported individually. In September, the ads were amended to land on a bookmark section..."
- Image: Self-catering performance table

**Data Source**:
- ✅ Google Ads API - Self-catering campaigns
- Campaigns: "Chatsworth Self Catering" and "Bolton Abbey Self Catering"

**Metrics Needed**:
- Spend, Revenue, Conversions, ROAS, Clicks, CTR per campaign

**Current Status**:
- ✅ We have this in October markdown report (Self-Catering Campaigns table)
- ✅ HTML report includes this table
- 🔄 Need to add commentary text box
- 🔄 Need to format as image for slides

---

### Slide 25: Highwayman (The Hide)
**Content**:
- Title: "Highwayman"
- Image: The Hide performance table

**Data Source**:
- ✅ Google Ads API - The Hide campaigns
- Campaigns: "The Hide" (23069490466) and "Highwayman Arms" (21815704991)
- Note: Separate £2,000 budget

**Metrics Needed**:
- Spend, Revenue, Conversions, ROAS for The Hide campaigns

**Current Status**:
- ✅ We have this in October markdown report (The Hide section)
- ✅ HTML report includes this table
- 🔄 Need to format as image for slides

---

### Slide 26: Weddings
**Content**:
- Title: "Weddings"
- Text: "Only two conversions were tracked for the weddings campaign in September. There is some issue which I have been unable to get to the bottom of yet..."
- Image: Weddings performance table

**Data Source**:
- ✅ Google Ads API - Weddings campaign
- Campaign: "DEV | Weddings - UK 40 37 11/6  30 3/10 No Target 13/6 Ai 75 6/8 No Target 26/8" (ID: 8357761197)

**Metrics Available**:
- Spend: £912.11
- Revenue: £12.00 (CRITICAL ISSUE)
- Conversions: 12.00
- ROAS: 0.01x
- Clicks: 701
- CTR: 7.84%
- Impressions: 8,947

**Current Status**:
- ✅ Campaign ID identified
- ✅ October data retrieved
- ✅ Added to HTML report
- ⚠️ **CRITICAL ISSUE**: Only £12 in tracked revenue from 12 conversions despite £912 spend suggests conversion value tracking misconfiguration

**Action**: Investigate conversion value tracking setup for weddings campaign

---

### Slide 27: Lismore and The Hall
**Content**:
- Title: "Lismore and The Hall"
- Text: "The activation of Ai Max on both campaigns has increased the impressions for both campaigns with no increase in cost..."
- Image: Lismore/Hall performance table

**Data Source**:
- ✅ Google Ads API - Castle campaigns
- Campaigns:
  - "DEV | Castles | Lismore" (ID: 20117845164)
  - "DEV | Castles | The Hall" (ID: 17002402214)

**Metrics Available**:
| Campaign | Spend | Revenue | Conv | ROAS | Clicks | CTR |
|----------|-------|---------|------|------|--------|-----|
| Lismore | £247.55 | £0.00 | 0.00 | 0.00x | 198 | 8.33% |
| The Hall | £241.34 | £0.00 | 0.00 | 0.00x | 165 | 4.58% |
| **Total** | **£488.89** | **£0.00** | **0.00** | **0.00x** | **363** | **6.46%** |

**Current Status**:
- ✅ Campaign IDs identified
- ✅ October data retrieved
- ✅ Added to HTML report
- ⚠️ **CRITICAL ISSUE**: Zero conversions and zero revenue from both castle campaigns despite £488.89 combined spend

**Action**: Immediate conversion tracking audit and landing page review required

---

## Summary: What We Have vs. What We Need

### ✅ Data We Have (October 2025)

1. **Executive Summary** - Budget, spend, revenue, ROAS, conversions, impressions, clicks, CTR
2. **Hotels - Top Performers** - All 8 properties with full metrics
3. **Properties Requiring Attention** - Underperformers with issues
4. **Campaign Type Breakdown** - PMax, Search Hotels, Search SC, Search Locations
5. **Self-Catering Detailed** - Chatsworth SC and Bolton Abbey SC
6. **The Hide** - Separate budget tracking with breakdowns
7. **Weddings** - Campaign performance data (⚠️ with critical conversion value tracking issue)
8. **Lismore and The Hall** - Campaign performance data (⚠️ zero conversions issue)

### 🔄 Data We Need to Add

1. **Location Campaigns Table** - Separate table just for Chatsworth and Bolton Abbey location campaigns
2. **Profitability Table** - Need to clarify what this shows (likely just ROAS ranking)
3. **Month-over-Month Comparisons** - September vs. October
   - MoM ROAS change
   - MoM Spend change
   - MoM CTR change
   - MoM Revenue change

### ⚠️ Critical Issues Identified

1. **Weddings Campaign** - Only £12 in tracked revenue from 12 conversions (£912 spend)
   - Suggests conversion value tracking misconfiguration
   - Requires immediate investigation

2. **Lismore and The Hall** - Zero conversions, zero revenue (£488.89 combined spend)
   - Lismore has decent CTR (8.33%) indicating ad relevance
   - The Hall has low CTR (4.58%)
   - Requires conversion tracking audit and landing page review

### 🔍 Data Sources to Investigate

1. **Slide 15** - Overall performance summary image (what does it contain?)
2. **Slides 16-18** - Multiple hotel images (what are these showing?)
3. **Slide 21** - Profitability table (what metrics define this?)

---

## Next Steps

1. **Identify Missing Campaign IDs**:
   - Query Google Ads to find Wedding campaign IDs
   - Query Google Ads to find Lismore and Hall campaign IDs
   - Add to CAMPAIGN_GROUPS in generate_devonshire_slides.py

2. **Add Month-over-Month Comparison Logic**:
   - Query previous month's data
   - Calculate deltas (MoM change %)
   - Add to markdown and HTML reports

3. **Clarify Unknown Slides**:
   - Look at actual September deck images to see what Slides 15-18, 21 contain
   - Determine if we need additional tables or if existing data covers it

4. **Create Location Campaigns Table**:
   - Extract just the location campaigns from top performers
   - Create separate table for slide

5. **Add Commentary Text Boxes**:
   - Generate performance commentary based on data
   - Add to HTML report for easy copy-paste

---

**Last Updated**: 2025-11-02
**Status**: Analysis in progress
