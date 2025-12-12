# Smythson - Context & Strategic Notes

> **Purpose**: Living document with important context for Google Ads analysis and reporting.
> **Last Updated**: 2025-11-24

**Voice Transcription Aliases**: Smithson, Smith son, Smyth son, Smithsons, Smythsons

---

## 🚨 ACTIVE: P9 BUDGET REALLOCATION (Dec 12-17, 2025)

**STATUS:** Campaign budgets reallocated as of Dec 11, 2025, 13:40 UTC

**REVERSAL REQUIRED:** Dec 18, 2025 before 09:00 AM (MANDATORY)

**What Changed:**
- 5 UK campaigns: Budget reduced by total -£357/day (proportional to ROAS weakness)
- 7 EUR campaigns: Budget increased by total +£224/day (proportional to ROAS strength)
- All 12 campaigns remain ENABLED (no pauses)

**Reversal Document:** `/clients/smythson/reports/REVERSAL-CHECKLIST-DEC-18-2025.md` (CRITICAL)

**Why:** EUR performing at 892% ROAS vs UK at 389%. 6-day window before EUR delivery cutoff to capture efficiency gain. Reversible on Dec 18 when UK needs full budget for Last Order Week.

**Contact:** Responsible party TBD for Dec 18 reversal execution

---

## ⚠️ CRITICAL: DATA ACCURACY PROTOCOLS

**Google Ads API Query Standards:**

When querying financial data (spend, revenue, conversions) for reporting or P8/P9 tracking:

1. **ALWAYS use customer-level queries**, not campaign-level:
   ```sql
   SELECT metrics.cost_micros, metrics.conversions_value
   FROM customer
   WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
   ```

2. **ALWAYS query BOTH spend AND revenue** together - never make assumptions about revenue figures

3. **ALWAYS include manager_id** in API calls:
   - Manager Account ID: `2569949686`
   - Required for all 4 regional accounts (UK, USA, EUR, ROW)

4. **ALWAYS query all 4 accounts** and sum totals for account-level reporting:
   - UK: 8573235780
   - USA: 7808690871
   - EUR: 7679616761
   - ROW: 5556710725

5. **ALWAYS present raw API data** before building projections or strategies

6. **NEVER use placeholder values** for revenue - if you don't have actual data, query it first

7. **ALL currency figures reported in GBP (£)** - no conversions, all accounts use GBP

**Why this matters:** Campaign-level queries can miss spend/revenue. Customer-level queries are the source of truth for account totals. Incorrect revenue data leads to incorrect strategic decisions.

---

## Account Overview

**Client Since**: [TBD]
**Monthly Budget**: Variable by quarter (Q4 2025: see budget revision below)
**Primary Contacts**:
- Lauryn Sobers (day-to-day account management, PPC expert - deeply understands Google Ads)
- Alex Clarke (senior oversight, PPC literate)
- Ciana (marketing copy approval)
- Beth (technical/tracking)
**Account Manager**: Peter Empson

**Business Type**: Luxury leather goods retailer
**Industry**: Luxury retail - British heritage brand
**Geographic Focus**: Multi-regional (UK primary, USA, EUR, ROW)
**Website**: https://www.smythson.com/

**REPORTING STANDARD - CURRENCY**:
⚠️ **ALL financial reporting for Smythson must be in British Pounds (£) ONLY**
- This applies to ALL regions: UK, USA, EUR, ROW
- Even though Google Ads accounts use local currencies (USD, EUR), convert everything to GBP for reporting
- Budgets, spend, revenue, and all financial metrics = GBP only
- No exceptions - client expects single-currency reporting

**Google Ads Account Structure**:
Smythson operates across **four separate Google Ads accounts**, each representing a distinct geographical region:

1. **Smythson UK** - Account ID: 8573235780
   - **Geographic Coverage**: United Kingdom only (100% of impressions)
   - Primary market with highest budget allocation (43.8% of Q4 spend)
   - Strongest performance expectations (ROAS target: 3.0 / 300%)

2. **Smythson USA** - Account ID: 7808690871
   - **Geographic Coverage**: United States only (100% of impressions)
   - Second-largest market (36.5% of Q4 spend)
   - Growth market with moderate ROAS target (1.5 / 150%)

3. **Smythson EUR** - Account ID: 7679616761
   - **Geographic Coverage**: 40 European countries
     - **Germany** (78% of EUR impressions) - dominant market
     - **France** (9.5%) - secondary market
     - **Italy** (8.9%) - secondary market
     - **Other 37 countries** (3.6%) - Spain, Switzerland, Sweden, Netherlands, Greece, Ireland, Austria, Belgium, Denmark, Norway, Poland, Portugal, and more
   - European markets (14.0% of Q4 spend)
   - Moderate ROAS target (1.5 / 150%)
   - **Known Issue**: Using GA4 conversion tracking (needs fixing - Oct 2025)

4. **Smythson ROW** (Rest of World) - Account ID: 5556710725
   - **Geographic Coverage**: 134+ countries across Asia-Pacific, Middle East, Africa, Americas
     - **Singapore** (53% of ROW impressions) - dominant market
     - **Australia** (21%) - secondary market
     - **Canada** (5%) - tertiary market
     - **Top regions**: Asia-Pacific (66%), Oceania (22%), Middle East (4%), Africa (2%), Latin America (1%)
     - **Notable markets**: Hong Kong, Israel, India, Japan, Mexico, New Zealand, South Africa, Malaysia, Thailand
   - Exploratory markets (5.7% of Q4 spend)
   - Conservative ROAS target (1.0 / 100%)
   - **Known Issue**: Using GA4 conversion tracking (needs fixing - Oct 2025)

**Platform IDs**:
- **Google Ads Manager Account**: 2569949686
- **Google Merchant Centre IDs**:
  - UK: 102535465
  - USA: 102535465 (same feed as UK)
  - EUR: [TBD]
  - ROW: [TBD]
- **Google Analytics 4 (GA4)**:
  - Property ID: 342726123 (New Site - GA4)
  - Additional Properties: 401381930 (Dev), 403524324 (GBP backup)
  - Note: EUR and ROW accounts currently using GA4 conversion tracking (needs migration to Google Ads native tracking)
- **Microsoft Ads Account ID**: [TBD]
- **Facebook Ads Account ID**: [TBD]

All four accounts are managed under the Rok Systems MCC (Manager Account ID: 2569949686)

**Geographic Analysis**: See [documents/geographic-targeting-analysis.md](documents/geographic-targeting-analysis.md) for complete breakdown (based on Aug-Nov 2025 actual ad delivery data)

**Data Available**:
- 112 emails on file
- 2 meeting notes
- 4 experiment log entries

---

## Strategic Context

### Q4 2025 Budget Approval Process (October 25, 2025)
**Added**: 2025-10-29
**Updated**: 2025-11-03 (clarified approval process)
**Source**: Teams chat (Alex Clarke announcement)
**Impact**: Budget proposal partially approved

**Budget Proposal vs Approval**:
- **Proposed additional paid media budget**: £415k
- **Actual client approval**: £215k (52% of proposal approved)
- **Proposed Additional Paid Search spend**: £270k
- **Actual approval**: £130k

**Context**: The £415k was a proposal that was never fully approved by the client. The actual approved Q4 budget was £215k from the outset. This was a budget clarification, not a mid-quarter cut.

**Approved Period Budgets**:
- **P7** (Sep 29 - Nov 2): £151,072 (complete: £151,072 spent, 318% ROAS, NO underspend)
- **P8** (Nov 3-30, 28 days): **£186,051** (corrected Nov 2025 - no P7 carryforward)
- **P9** (Dec 1-28, 28 days): £183,929 (21 days effective due to Dec 22 Christmas cutoff)
- **Total Q4 Approved**: £521,052

**CRITICAL:** P8 budget is £186,051, NOT £218,653. See `documents/SMYTHSON-Q4-AUTHORITATIVE-FIGURES.md` for all definitive Q4 figures.

**Cost Split by Region** (July-October 2025 average):
- **UK**: 44.2%
- **USA**: 36.2%
- **EUR**: 14.0%
- **ROW**: 5.6%

**Strategic Response**:
- Peter created Q4 strategy based on approved £215k budget
- Recommendation: Drop target ROAS 15-20% in November/December to maximize volume
- Consolidated strategy document created for all 4 accounts
- Focus on profitable scaling within approved budget constraints

**P7 Performance (Sep 29 - Nov 2, 2025)**:
- **Total Spend**: £113,970 across all regions (UK: £45,956, USA: £43,933, EUR: £16,640, ROW: £7,441)
- **Total Revenue**: £467,094
- **Overall ROAS**: 410% (4.10)
- **Budget Pacing**: 86.0% of £132,519 budget ✅
- **Assessment**: Strong foundation established, all regions performing at or above Q4 ROAS targets

---

### Q4 2025 Multi-Regional Christmas Strategy
**Added**: 2025-10-29
**Source**: Comprehensive strategy report (assets-organizer-cdn.gomarble.ai)

**Total Q4 Budget**: £367,014 distributed across:
- **UK**: £160,752 (43.8%) - Largest market investment
- **USA**: £133,960 (36.5%)
- **EUR**: £51,382 (14.0%)
- **ROW**: £20,920 (5.7%)

**Daily Spend Targets**:
- November: £6,202/day
- December: £5,838/day

**ROAS Targets by Region** (phased approach):
- **UK**: 4.3 (Oct 29) → 3.8 (Nov 15) → 3.5 (Dec 1)
- **USA**: 2.5 (Oct 29) → 2.2 (Nov 15) → 2.0 (Dec 1)
- **EUR**: 1.5 (Oct 29) → 1.3 (Nov 15) → 1.2 (Dec 1)
- **ROW**: 1.0 (Oct 29) → 0.9 (Dec 1)

**Q4 2025 Revenue Target**: £2,720,970 combined across all regions
- P7 (actual): £479,840
- P8 (target): £1,119,436
- P9 (target): £1,121,694

**Implementation Timeline**:
- **Oct 29**: UK & EUR launches
- **Nov 1**: USA launch
- **Nov 15**: ROW launch + first performance review
- **Nov 25**: USA Thanksgiving budget boost (+15%)
- **Dec 1**: Peak season adjustments
- **Dec 15**: Mid-December assessment
- **Dec 31**: End-of-quarter review

**Q4 2024 Baseline Performance** (for comparison):
- UK: 10.15% peak conversion rate (Nov), 915% avg ROAS, £1.5M revenue
- USA: 4.35% conversion rate (Dec), 514% ROAS, $890K revenue
- EUR: 425% ROAS, €174K revenue
- ROW: 152% ROAS

**Monitoring Framework**:
- Weekly performance reviews against CR and ROAS thresholds
- Escalation protocols for underperformance (budget reductions/reallocation)
- Regional performance dashboards with specific KPIs per market

### Current Strategy
[To be filled from analysis of 112 emails and 2 meeting notes]

### Why This Approach?
Multi-regional approach recognizes different market maturity levels and performance potential. UK as primary market receives largest investment with highest ROAS expectations. USA and EUR positioned for growth with moderate targets. ROW as exploratory market with conservative expectations.

### Goals & KPIs
**Primary Goal**: £780,691 Q4 2025 revenue across all regions
**Target ROAS by Region**:
- UK: 3.0
- USA: 1.5
- EUR: 1.5
- ROW: 1.0
**Target CPA**: [TBD]
**Other KPIs**: Weekly conversion rate and ROAS monitoring per region

---

## Budget Guidelines

**Maximum Daily Budget**: £5,000/day total across all campaigns (can exceed during major events with approval)

**Budget Allocation Priority**:
1. **Brand campaigns first** (historically 650%+ ROAS efficiency)
2. **UK campaigns** (strongest performance, ROAS 3.0+ target)
3. **USA/EUR campaigns** (ROAS 1.5+ target)
4. **ROW campaigns** (ROAS 1.0+ target)

**Seasonal Budget Adjustments**:
- **Q4 (Oct-Dec)**: Increased budgets for gifting season
- **Black Friday/Cyber Monday**: Phased deployment approach
  - Phase 1: Brand campaigns + proven performers
  - Phase 2: Expand to all profitable campaigns
  - Phase 3: Maximum deployment with daily monitoring
- **January**: Reduced budgets post-Christmas
- **Valentine's/Mother's Day**: Moderate increases for gifting peaks

**Budget Change Thresholds**:
- Daily adjustments <£500: Execute directly
- Daily adjustments £500-£1,500: Note in weekly report
- Daily adjustments >£1,500: Document reasoning in client folder
- Major event deployment (e.g., Black Friday): Document full strategy in `/documents/`

**Performance-Based Budget Rules**:
- **Scale UP**: If campaign ROAS >150% of target for 3+ days
- **Scale DOWN**: If campaign ROAS <80% of target for 3+ days
- **Pause**: If campaign ROAS <50% of target or zero conversions for 7+ days
- **Emergency pause**: If daily spend exceeds £1,000 with zero conversions

**Budget Monitoring Cadence**:
- **Daily**: During major events (Black Friday, Cyber Monday)
- **3x weekly**: During seasonal peaks (Q4)
- **Weekly**: Standard monitoring (Q1-Q3)

---

## Historical Performance Patterns

### Seasonality
[TBD - analyze historical data]

### Year-Over-Year Trends

**UK November Performance (Nov 1-24, 2024 vs 2025):**

**2024 Baseline:**
- Total Revenue: £283,888
- Total Cost: £42,699
- Overall ROAS: 6.65x (665%)
- Clicks: 29,961
- CPC: £1.43
- **Brand**: £189,561 (66.8% of revenue) | 11.35x ROAS | £1.11 CPC
- **Non-Brand**: £94,326 (33.2% of revenue) | 3.63x ROAS | £1.75 CPC

**2025 Performance:**
- Total Revenue: £321,018
- Total Cost: £56,506
- Overall ROAS: 5.68x (568%)
- Clicks: 36,623
- CPC: £1.54
- **Brand**: £180,340 (56.2% of revenue) | 7.27x ROAS | £1.78 CPC
- **Non-Brand**: £140,677 (43.8% of revenue) | 4.44x ROAS | £1.40 CPC

**Year-over-Year Changes:**
- Total Revenue: +£37,130 (+13.1%) ✅
- Total Cost: +£13,807 (+32.3%)
- Overall ROAS: -0.97x (-14.6%)
- Brand Revenue: -£9,221 (-4.9%)
- Brand ROAS: -4.08x (-36.0%)
- Brand CPC: +£0.67 (+60.4%) ⚠️
- Non-Brand Revenue: +£46,351 (+49.1%) 🚀
- Non-Brand ROAS: +0.81x (+22.3%)
- Non-Brand CPC: -£0.35 (-20.0%)

**Strategic Implications (Nov 2025):**
- ✅ **Successfully diversified from brand dependency**: Brand mix reduced from 66.8% → 56.2%
- ✅ **Non-brand scaling efficiently**: +49% revenue with improving ROAS (3.63x → 4.44x)
- ⚠️ **Brand CPC inflation**: 60% increase suggests competitive pressure on branded terms
- 💡 **New customer acquisition**: Non-brand growth suggests improved new customer acquisition
- ⚠️ **Double counting issue**: Historical data affected by conversion tracking problem (worse in UK than US)

### Known Anomalies
[TBD]

---

## Client Preferences & Communication

### Communication Style

**Primary Contacts:**
- **Alex Clarke** (Senior oversight, PPC literate)
  - **Decision-making style**: Quick approvals when strategy is clear and "easy to digest"
  - **Communication preference**: Appreciative, collaborative, values gratitude
  - **Data requirements**: Needs YoY context before reporting to senior management
  - **Timing**: Responds promptly to urgent requests (e.g., "need approval by 8am tomorrow")
  - **Quote**: "That's a really easy to digest strategy by the way, thank you!"

- **Lauryn Sobers** (Day-to-day account management, PPC expert)
  - Deeply understands Google Ads mechanics
  - Technical liaison for implementation

**Communication Standards:**
- **Teams Chat**: "Paid Search Catch Up" - regular performance updates
- **Strategy docs**: Must be "easy to digest" - clear, concise, actionable
- **Urgent approvals**: Flag tight deadlines clearly (implementation time-sensitive)
- **Performance reporting**: Always include YoY comparison data
- **Appreciation**: Client values being appreciated and acknowledges good work

**Collaboration approach:**
- Regular Teams chat updates
- Frequent strategy calls and planning meetings
- Open to data-driven recommendations and experimentation
- "I am grateful!" - client explicitly values the work

### Decision-Making
**Marketing Approval Process**:
- **Ciana** (marketing team) must approve all ad copy changes
- **Identified bottleneck**: Marketing approval process slows down implementation
- **Goal**: Remove/streamline approval bottleneck for faster execution
- Peter can share ad copy in Google Docs for Ciana's review

**Ad Copy Preferences**:
- Client feedback: Existing client-provided copy is "awful" - too generic and copy-paste
- Need more compelling, targeted ad copy (not just brand-compliant)
- Should bring tone of voice from website into ads
- Headlines need to be more compelling than descriptions
- Generic copy doesn't compel new customers to click

**Approval Workflow**:
1. Peter creates ad copy in Google Sheet/Doc
2. Shares with Lauryn
3. Lauryn invites Ciana to review
4. Ciana provides approval/feedback
5. Implementation (currently slow due to step 3-4 delay)

**Promotional Strategy Preferences (December 2025):**
- **Approach**: "Sprinkle promo into existing mix" - add promotional headlines to existing Christmas campaigns
- **No new asset groups or campaigns** - integrate promotions into BAU structure
- **Merchant Centre promotions crucial** - shown against shopping ads (primary visibility)
- **Target audiences**: Christmas campaigns benefit most (audience targeting gift seekers)
- **Implementation speed**: Can pivot quickly (Dec promo changes announced "hot off the press in last 15 minutes")

**December 2025 Promotion Changes:**
- ❌ **Cancelled**: Gold Stamping promotion (6-7th Dec) - originally planned
- ❌ **Cancelled**: 20% off Notebooks promotion - originally planned
- ✅ **New**: 20% off selected Gifts (8-14th Dec)
  - One creative asset
  - Headlines woven into existing Christmas campaigns
  - Product line list to follow end of week
- 📅 **Dec 2nd**: Back to "Christmas Gifting" BAU campaigns

### Red Flags / Sensitive Topics
- Marketing approval delays - sensitive topic but acknowledged as an issue
- Budget cuts mid-quarter (Q4 2025 reduction was significant)

---

## Business Context

### Product/Service Details

**Smythson** is a luxury British leather goods and stationery brand with heritage dating back to 1887, holding Royal Warrants and operating from Bond Street, London.

**Business Model**: Multi-regional luxury e-commerce retailer (UK, US, and other markets) offering premium leather goods, stationery, diaries, and accessories with strong gifting positioning.

**Brand Positioning**: 
- **"Thoughtfully made, meaningfully given"** - Core brand philosophy emphasizing craftsmanship and gifting
- **Heritage luxury** - 138+ years of British craftsmanship, Royal Warrants holder
- **Bond Street prestige** - Flagship location on prestigious Bond Street, London
- **Multi-regional** - UK, US, and international markets with regional websites (/uk/, /us/, etc.)

**USP**:
- **Royal Warrants** - Official supplier to the Royal Family (prestigious credential displayed prominently)
- **Heritage craftsmanship** - 138+ years of British leather goods expertise
- **Luxury positioning** - Premium pricing justified by quality, heritage, and brand prestige
- **Strong gifting angle** - "Thoughtfully made, meaningfully given" positioning across all categories
- **Complimentary delivery** - Free standard delivery on orders over £300, plus complimentary UK returns
- **Multi-category luxury** - From stationery to travel accessories to tech accessories (broadens appeal)
- **Brand recognition** - High search volume for branded terms like "luxury notebooks", "Smythson diaries"
- **Christmas gifting focus** - 380+ products curated for Christmas with National Literacy Trust charity partnership

**Core Products**:
- **Notebooks**: Core product line with 93+ untitled and 56+ titled notebooks - "Smythson's core product"
- **Panama Collection**: Signature collection with 139+ products - strong brand recognition
- **Travel Accessories**: 25 travel wallets, 30 passport covers, luggage tags
- **Card Holders & Small Leather Goods**: 57+ card holders (high-volume, lower price entry point)
- **Stationery & Writing Paper**: Heritage product line, correspondence cards, greeting cards - strong for corporate gifting
- **Jewellery Storage**: 18 jewellery boxes, 24 trinket cases, 12 trinket trays
- **Wallets & Purses**: 17 wallets, 14 small purses, 6 large purses
- **Desk Accessories**: A4/A5 writing folders, pen holders, desk mats (professional/corporate segment)
- **Tech Accessories**: Phone cases, laptop cases, tech pouches (younger luxury consumers)

**Product Hero Label Segmentation** (Performance-Based Categories - Used in Google Ads campaigns):
- **Plan Level**: Pro Plan (€30/month per account - UK and USA accounts)
- **Heroes & Sidekicks (H&S)** - Top-performing products (Heroes = top revenue generators, Sidekicks = good converters needing more visibility)
- Products classified by Product Hero based on performance data
- Campaigns structured around these labels to optimize budget allocation and bidding strategy
- **Note**: Product Hero is used ONLY for UK and USA accounts. EUR and ROW accounts do not use Product Hero labels.

**Note**: Campaign names referencing "H&S" (Heroes & Sidekicks) refer to Product Hero performance labels, not actual product categories. Product Hero automatically classifies products based on performance data and syncs these labels to Google Merchant Center for campaign segmentation. This system is only implemented for UK and USA accounts.

**Seasonal Products**:
- **Christmas Gifts Collection**: 380+ products specifically curated for Christmas gifting
- National Literacy Trust charity partnership adds emotional appeal
- Christmas gifts page exists but "doesn't look very Christmassy" (expecting launch updates)

**Product Characteristics**:
- Luxury positioning with premium pricing
- Strong gifting angle across most categories
- Heritage British brand with "Bond Street" prestige
- High search volume for branded terms like "luxury notebooks"

**Target Market**: 
- **Primary**: Affluent UK and US consumers seeking luxury gifts, premium stationery, and heritage British brands
- **Secondary**: Corporate gifting market, luxury travellers, professionals seeking quality accessories
- **Demographics**: High-income, brand-conscious consumers valuing heritage, craftsmanship, and British luxury

### Google Merchant Center - Supplemental Feeds
**Added**: 2025-11-04

**Custom Label 0 Feeds** (created Nov 4, 2025):
- **Purpose**: Product categorization for custom bidding and reporting
- **Products**: 117 products across 3 categories:
  - Travel Bags (24 products)
  - Card Holders (44 products)
  - Jewellery Boxes (49 products)
- **Format**: CSV with columns: id, custom_label_0

**Google Sheets (for Merchant Center upload)**:
- **UK & USA Feed** (single feed for both regions): [Smythson - Custom Label 0 - UK & USA Feed](https://docs.google.com/spreadsheets/d/1nqKuSEDoKIHC0aNrVXicuGxCaHGiYvMhKM7KHtfRzac)
- **USA Feed** (obsolete - not in use): [Smythson - Custom Label 0 - USA Feed](https://docs.google.com/spreadsheets/d/1XkAcRlS9vLN1JoDWLEseDs9Mdznx784vw4RUT_piW00)

**Important Notes**:
- Both UK and USA accounts use **identical feed data** from the single UK & USA feed
- The UK feed CSV is used as source for both regions
- Separate USA feed Google Sheet exists but is **not being used** (obsolete)
- Single feed uploaded to both Merchant Center accounts (UK: 8573235780, USA: 7808690871)

**Local Files**:
- Source CSV: `product-feeds/Smythson_Custom_Label_0_UK.csv`
- USA CSV (obsolete): `product-feeds/Smythson_Custom_Label_0_USA.csv`
- Original Q4 file: `product-feeds/Smythson_Custom_Label_0_Q4_2025.csv`

**Contact**: Lauryn Sobers (managing supplemental feed setup)

### Website & Technical
**Website Platform**: [TBD]
**Website URL**: https://www.smythson.com/ (multi-regional: /uk/, /us/, etc.)
**Known Technical Issues**: [TBD]

**Conversion Tracking**:
- **Setup**: Google Ads conversion tracking primary
- **Known Issues**:
  - **EUR and ROW accounts using GA4 conversion tracking** (needs fixing - October 2025)
  - Working with Beth and Google tech team to resolve
  - Expected resolution time: ~1 week
  - Issue discovered during October 2025 strategy review
- **Last Audit**: October 2025 (EUR/ROW issue identified)

**CRITICAL - Historical Data Warning (UK & USA Accounts)**:
- **Issue**: UK and USA accounts had **double counting on the purchase conversion action** throughout 2024
- **Fixed**: April 2025
- **Impact on Historical Analysis**:
  - All 2024 conversion data for UK and USA using "All Conversions" is **inflated/inaccurate**
  - When comparing 2024 vs 2025 performance, you **MUST use the specific "Purchase (Google Ads)" conversion action**
  - UK conversion action: "Purchase ( Google Ads)" - ID: 503366585
  - USA conversion action: "Purchase US ( Google Ads)" - ID: 6810743457
- **Correct Approach for YoY Analysis**:
  - Filter by `segments.conversion_action_name` in GAQL queries
  - Do NOT use `metrics.conversions` without filtering - this includes the double-counted data
  - EUR and ROW accounts were NOT affected by this issue
- **Source**: Confirmed in 2025-11-10 Paid Search catch-up meeting notes

### Competitive Landscape
[TBD]

---

## Known Issues & Challenges

### Current Issues (October 2025)

**1. EUR & ROW Conversion Tracking Issue**
- **Problem**: EUR and ROW accounts using GA4 conversion tracking instead of Google Ads native tracking
- **Impact**: Potential tracking discrepancies and optimization issues
- **Status**: In progress - working with Beth and Google tech team
- **Timeline**: ~1 week expected for resolution
- **Discovered**: October 2025 during strategy review

**2. Marketing Approval Bottleneck**
- **Problem**: Ciana (marketing) must approve all ad copy, creating delays
- **Impact**: Slows down implementation of new ads and campaign launches
- **Status**: Acknowledged issue, looking to streamline process
- **Workaround**: Peter shares Google Docs for async review

**3. Customer List Segmentation Issues**
- **Problem**: Customer lists not properly defined for new/returning/lapsed segments
- **Impact**: Bidding strategies based on customer status were ineffective
- **Resolution**: October 2025 - Removed all new/returning customer campaign splits
- **Action Taken**: Now bidding equally for all customers across all campaigns
- **Note**: Lapsed customer bidding settings also switched off

**4. Brand Stationery Campaign Restructure**
- **Problem**: Brand stationery products mixed into general campaigns
- **Resolution**: October 2025 - Moved to dedicated campaign
- **Status**: Ongoing - new ads being created for better relevance

### Recurring Challenges
- Ad copy approval delays (see issue #2 above)
- Client-provided copy tends to be too generic and not compelling
- Need balance between brand compliance and performance-driven copy

### External Factors to Monitor
- Mid-quarter budget cuts (Q4 2025 experienced 48% reduction in additional budget)
- Christmas seasonality and gifting search volume spikes (October-December)
- Competitive bidding on Smythson brand terms

---

## Key Learnings & Insights

### Brand vs Non-Brand Performance Analysis (November 2025)
**Added**: 2025-11-13
**Analysis Period**: Oct 14 - Nov 12 (2024 vs 2025)
**Source**: Google Ads API search term analysis
**Status**: CRITICAL - Immediate action required

**EXECUTIVE SUMMARY - SEVERE EFFICIENCY DECLINE**:
Year-over-year analysis of UK Search campaigns reveals a critical performance collapse:
- **Brand CPC increased 71%** (£0.86 → £1.46) - competitive pressure confirmed
- **Brand spend increased 65%** (£11.3k → £18.6k)
- **Brand revenue DECLINED 22%** (£159.6k → £124.6k) ⚠️ **SPENDING MORE, EARNING LESS**
- **Brand ROAS collapsed 53%** (1411% → 669%) - efficiency more than halved
- **Result**: £7,306 additional spend generated £35,015 LESS revenue (negative returns)

**BRAND TERMS DETAILED METRICS (2024 vs 2025)**:
- CPC: +70.7% (£0.86 → £1.46)
- Clicks: -3.6% (13,224 → 12,748)
- Conversions: -18.4% (1,024 → 835)
- Conversion Rate: -15.4% (7.7% → 6.6%)
- CPA: +101.8% (£11.04 → £22.27) - **DOUBLED**
- Revenue per click: -19.0% (£12.07 → £9.77)
- Total Revenue: -21.9% (£159.6k → £124.6k)
- ROAS: -52.6% (1411% → 669%)

**NON-BRAND TERMS METRICS (2024 vs 2025)**:
- CPC: -43.8% (£3.18 → £1.79) - opposite trend to brand
- Clicks: +140.6% (180 → 433)
- Conversions: -79.8% (13 → 2)
- Conversion Rate: -91.6% (7.7% → 0.7%) ⚠️ **COLLAPSED**
- Revenue: -26.6% (£2.2k → £1.6k)
- ROAS: -45.7% (380% → 206%)

**CRITICAL INSIGHTS**:

1. **Triple Penalty Effect**: Higher CPCs (+71%) + Lower conversion rates (-15%) + Lower revenue per click (-19%) = ROAS collapse from 1411% to 669%

2. **Competitive Pressure Confirmed**: CPC inflation of 71% is NOT normal market inflation - indicates aggressive competitive bidding specifically on Smythson brand terms

3. **Negative Returns on Incremental Spend**: The additional £7,306 spent in 2025 generated NEGATIVE returns compared to 2024 efficiency levels. If 2024 ROAS (1411%) had continued, £18.6k spend should have generated £262k revenue. Actual: £124.6k. **Gap: Missing £138k in potential revenue.**

4. **Non-Brand Quality Collapse**: Non-brand conversion rate at 0.7% (down from 7.7%) suggests severe traffic quality issues despite lower CPCs

5. **Compounding Decline**: This is not just inefficiency - it's a structural performance collapse requiring urgent intervention

**ROOT CAUSE HYPOTHESES** (Require Investigation):

Priority 1 - Website/Technical Issues:
- Check GA4 conversion funnel metrics (2024 vs 2025)
- Audit site speed and Core Web Vitals
- Review checkout process for friction points
- Check mobile vs desktop conversion rate split

Priority 2 - Product/Inventory Issues:
- Compare active products now vs Oct-Nov 2024
- Check bestselling 2024 products still in stock
- Review pricing changes year-over-year
- Check out-of-stock rates for key products

Priority 3 - Competitive Landscape:
- Run Auction Insights for brand terms
- Identify new competitors entering in 2025
- Review competitor ad copy and positioning
- Analyze impression share trends

Priority 4 - Market/Demand Changes:
- Economic conditions affecting luxury spend
- Consumer confidence in UK market
- Brand perception or reputation issues
- Search intent shifts (research vs purchase)

**IMMEDIATE ACTIONS REQUIRED** (Next 48 Hours):

1. **Reduce brand bids by 20-30%** - Stop overpaying for clicks at current CPCs
2. **Audit website conversion funnel** - Could be quick fix if technical issue
3. **Check product availability** - Compare inventory vs 2024
4. **Run Auction Insights** - Identify who's bidding on brand terms

**STRATEGIC IMPLICATIONS**:

- At 669% ROAS, brand is still profitable but trajectory is alarming
- If decline continues at current rate: Will hit unprofitable levels in Q1 2026
- Decision point: Is this temporary (fixable) or structural market change (new normal)?
- Risk: Current strategy of defending brand at all costs may no longer be sustainable

**FILES**:
- Full analysis: `documents/brand-yoy-comparison-2025-11-13-CORRECTED.txt`
- Current period (30 days): `documents/brand-vs-nonbrand-analysis-2025-11-13.txt`
- Scripts: `scripts/brand-yoy-comparison-v2.py`, `scripts/run-brand-analysis.py`

**DATA NOTES**:
- 2024: "Purchase ( Google Ads)" conversion action only (£161.8k total)
- 2025: All conversion actions from search_term_view
- Brand/non-brand split for 2024 conversions estimated from click proportions
- Analysis uses search term level data for precise brand/non-brand categorization

### What Works Well
[TBD - populate from email analysis and experiment results]

### What Doesn't Work
[TBD]

### Successful Tests & Experiments

| Date | Test Description | Result | Action Taken |
|------|-----------------|--------|--------------|
| [TBD] | [From experiment log] | [TBD] | [TBD] |
| [TBD] | [From experiment log] | [TBD] | [TBD] |
| [TBD] | [From experiment log] | [TBD] | [TBD] |

### Recent Experiments (from log):
- 23/10/2025 11:30,Smythson,"New ads set live for the UK search brand stationery campaign. These have higher relevance, so hopefully will improve CTR"
- 23/10/2025 14:05,Smythson,"For the UK account, search Brand Exact all customers and new customers consolidated into one campaign. The campaign it was consolidated into is the all customers version of it. The target RAS was dropped from 660 to 450, no change to the budget because it doesn't appear to be spent on a daily basis"
- 23/10/2025 16:37,Smythson,Paused the PMax H&S new customers campaign and increased the budget on the PMax H&S returning customers campaign to £300 per day
- 24/10/2025 11:55,Smythson,AI max for the UK generics campaign

---

## Campaign-Specific Notes

### Recent Campaign Structure Changes (October 2025)

**UK Search - Brand Exact Campaign**:
- **Action**: Consolidated all customers and new customers campaigns into single campaign (October 23, 2025)
- **Change**: Paused "new customers" version, kept "all customers" version
- **Target ROAS**: Reduced from 660 to 450
- **Budget**: No change (wasn't being fully spent)
- **Rationale**: Simplify structure, improve efficiency

**Performance Max - Heroes & Sidekicks (H&S)**:
- **Note**: "H&S" refers to Product Hero performance labels (Heroes & Sidekicks), not a product collection name
- **Product Hero Label System**: Products are automatically classified by Product Hero based on performance data
- **Heroes & Sidekicks**: Top-performing products (Heroes = top revenue generators, Sidekicks = good converters needing more visibility)
- Campaigns structured around these labels to optimize budget allocation and bidding strategy
- **Account Scope**: Product Hero is used ONLY for UK and USA accounts. EUR and ROW accounts do not use Product Hero labels.
- **Action**: October 23, 2025 changes:
  - Paused "New Customers" P Max campaign
  - Increased budget on "Returning Customers" P Max to £300/day
- **Action**: October 24, 2025:
  - Restarted Shopping H&S campaign for brand searches
  - P Max has brand exclusion, so Shopping will capture brand search traffic
  - **Rationale**: Low-hanging fruit for Q4, prevent competitor bidding on brand terms

**Performance Max H&S - Channel Distribution Analysis (October 2025)**:
- **Added**: 2025-10-30
- **Report**: `pmax-hs-actual-channel-distribution-oct-2025.html`
- **Key Finding**: Search absolutely dominates this campaign
  - **Search**: 93.9% of impressions (703,740), 98.9% of spend (£5,666.51)
  - **YouTube**: 5.0% impressions, 0.4% spend
  - **All other channels**: <1% impressions each (Maps, Display, Discover, Gmail)
- **Strategic Implication**: Square product images (1:1) for Shopping ads are BY FAR the most critical asset
  - 94% of impressions are Google Search Shopping carousel placements
  - Landscape/portrait images for YouTube, Display, Discover represent <6% of total reach
  - Asset prioritization should heavily favor square product photography quality
- **vs. Industry Benchmarks**: Campaign is significantly more Search-focused than typical PMax (40-60% benchmark)
  - Likely due to strong product feed optimization and Shopping/Search conversion signals
  - Non-Search channels severely underutilized compared to industry norms

**UK Generics Campaign**:
- **Action**: AI Max switched ON (October 24, 2025)
- **Status**: Active and monitoring performance

**US Brand Exact Campaign**:
- **Status**: Brand AI has been ON since mid-August 2025
- **Verification**: Confirmed via search query report analysis

**Customer Acquisition Settings - Global Change**:
- **Action**: October 25, 2025 - Removed all new/returning customer splits
- **Changes made**:
  - Switched OFF higher bidding for new customers (now bid equally)
  - Switched OFF higher bidding for lapsed customers
  - Paused dedicated new/returning customer campaigns across all accounts
- **Rationale**: Customer lists not properly defined, causing ineffective segmentation
- **New approach**: Bid equally for all customers on all campaigns

**Brand Stationery Campaign**:
- **Action**: Brand stationery products moved to dedicated campaign
- **Status**: New ads being created with higher relevance and better CTR focus
- **Ad copy**: Shared with Lauryn and Ciana for marketing approval

### Christmas Gifting Campaigns (Q4 2025)

**Christmas Gifts Search Campaigns**:
- **Status**: Planned for November/December launch
- **Ad Copy**: Ciana provided ad copy for Search and P Max
  - Descriptions and long headlines approved
  - Headlines need to be more compelling (identified as weak)
- **Products**: 380+ products in Christmas Gifts collection
- **Angle**: National Literacy Trust charity partnership adds emotional appeal
- **Landing Page**: Christmas gifts page exists but needs updates ("doesn't look very Christmassy")
- **Expected**: Updates to main navigation for Christmas section

### Performance Max - Q4 2025 Asset Group Strategy

**Added**: 2025-10-28
**Updated**: 2025-10-29 (Christmas Gifts moved to #1 priority)
**Context**: Prioritized asset groups for UK Performance Max campaign expansion

**Status**: Ad copy being developed for P Max product groups (expected late October 2025)

#### 1. Christmas Gifts Collection
- **URL**: https://www.smythson.com/uk/christmas-gifts
- **Rationale**: 380+ products specifically curated for Christmas gifting. Massive seasonal traffic spike from October-December. Includes everything from luxury games to jewellery boxes. Supporting National Literacy Trust charity angle adds emotional appeal.
- **Priority**: HIGHEST - Seasonal urgency for Q4 2025

#### 2. Notebooks - General Collection
- **URL**: https://www.smythson.com/uk/diaries-and-books/notebooks/all-notebooks
- **Rationale**: Core product with 93+ untitled and 56+ titled notebooks. High search volume for "luxury notebooks" and strong gifting potential.
- **Priority**: High

#### 3. Travel Accessories Collection
- **URL**: https://www.smythson.com/uk/all-accessories/travel
- **Rationale**: 25 travel wallets, 30 passport covers, luggage tags - strong category with high-value customers and seasonal peaks.
- **Priority**: High

#### 4. Card Holders & Small Leather Goods
- **URL**: https://www.smythson.com/uk/all-accessories/card-holders
- **Rationale**: 57 card holders represent high-volume, lower price point entry product with year-round demand.
- **Priority**: High

#### 5. Stationery & Writing Paper
- **URL**: https://www.smythson.com/uk/stationery
- **Rationale**: Heritage product line including correspondence cards, writing paper, and greeting cards - strong for corporate gifting.
- **Priority**: Medium-High

#### 6. Jewellery Storage & Home Accessories
- **URL**: https://www.smythson.com/uk/home/accessories
- **Rationale**: 18 jewellery boxes, 24 trinket cases, 12 trinket trays - high-value gifting items with strong seasonal peaks.
- **Priority**: Medium-High

#### 7. Wallets & Purses Collection
- **URL**: https://www.smythson.com/uk/all-accessories/wallets-and-purses
- **Rationale**: 17 wallets, 14 small purses, 6 large purses - essential accessories with strong repeat purchase potential.
- **Priority**: Medium

#### 8. Desk Accessories & Organisation
- **URL**: https://www.smythson.com/uk/home/desk-accessories
- **Rationale**: A4/A5 writing folders, pen holders, desk mats - targets professional/corporate segment.
- **Priority**: Medium

#### 9. Tech Accessories
- **URL**: https://www.smythson.com/uk/all-accessories/tech
- **Rationale**: Phone cases, laptop cases, tech pouches - modern essentials appealing to younger luxury consumers.
- **Priority**: Medium-Low

#### 10. Panama Collection
- **URL**: https://www.smythson.com/uk/collections/panama
- **Rationale**: Signature collection with 139+ products, strong brand recognition but more niche appeal.
- **Priority**: Low-Medium

**Implementation Notes**:
- **URGENT**: Asset Group #1 (Christmas Gifts) - Highest priority for immediate Q4 launch (seasonal)
- Asset groups 2-4 (Notebooks, Travel, Card Holders) for immediate Q4 launch
- Asset groups 5-7 (Stationery, Jewellery, Wallets) for mid-Q4 expansion
- Asset groups 8-10 (Desk, Tech, Panama) for Q1 2026 or as budget allows
- Monitor performance by asset group and adjust priority based on ROAS
- Ad copy development in progress (expected late October 2025)

---

## Action Items & Reminders

### Ongoing Tasks
- [ ] [TBD]

### Future Plans
- [ ] [TBD]

### Important Dates

**Q4 2025 Implementation Timeline** (Tasks created in Google Tasks):
- **Oct 29, 2025**: UK & EUR campaign launches
- **Nov 1, 2025**: USA campaign launch
- **Nov 15, 2025**: ROW campaign launch + UK ROAS reduction (4.3→3.8) + Mid-quarter performance review
- **Nov 25, 2025**: USA Thanksgiving budget boost (+15% to $2,604/day)
- **Dec 1, 2025**: Peak season ROAS adjustments across all regions (UK: 3.8→3.5, USA: 2.2→2.0, EUR budget decrease, ROW budget decrease)
- **Dec 15, 2025**: Revenue target validation review
- **Dec 31, 2025**: Final Q4 performance assessment

**Q4 Strategy Tracker**: `documents/q4-2025-strategy-tracker.md`
- Milestone-by-milestone performance tracking
- Expected vs actual results for each phase
- Weekly cumulative performance updates
- Red flags and course correction triggers

**Post-Christmas Sales Dates 2026** (Budget Planning):

**UK/US/ROW**:
- Wednesday 24th December: Launch - Up to 50% Off Selected Styles
- Wednesday 7th January: Further up to 60% off Selected Styles
- Thursday 15th January: Extra 10% off using code [x]
- Tuesday 20th January: Sale Ends

**EU**:
- Tuesday 6th January: Launch
- Thursday 15th January: Extra 10% off using code [x] (TBC)
- Tuesday 20th January: Sale Ends

---

## Q4 2025 Authoritative Figures

**⚠️ CRITICAL: For all Q4 budget, revenue, and ROAS figures, ALWAYS reference:**

**[SMYTHSON-Q4-AUTHORITATIVE-FIGURES.md](SMYTHSON-Q4-AUTHORITATIVE-FIGURES.md)** ← Single source of truth

This document contains:
- ✅ Approved budgets (P7/P8/P9)
- ✅ Revenue targets (total & regional)
- ✅ Target ROAS by phase
- ✅ Current performance baselines
- ✅ Dashboard reference values
- ✅ Daily budgets by phase

**Do NOT use budget/revenue figures from sections below - they may be outdated. Use AUTHORITATIVE FIGURES document.**

---

## Budget Tracking

**MICE Budget Spreadsheet**: https://docs.google.com/spreadsheets/d/1BB2V2e13PbRLhTvGqYITRhcpa5U92HLQV4_Bm9zxbVI/

**Structure**: Period-based budget tracking (P1-P12)
**Current Period** (as of Oct 31, 2025): P7
- Start: 29/09/2025
- End: 03/11/2025
- Budget: £130,911.79
- Actual Spend: £107,503.61
- Budget Pacing: 88.91%
- Days Elapsed: 32, Days Left: 4
- Required Spend/Day: £5,852.04

**Historical Periods**:
- P1 (31/03-04/05): £52,980 budget, £52,214.39 spent (£765.61 under)
- P2 (05/05-01/06): £57,000 budget, £52,914.98 spent (£4,085.02 under) - additional budget agreed 13/05
- P3 (02/06-29/06): £70,000 budget, £66,448.62 spent (£3,551.38 under)
- P4 (30/06-03/08): £74,462 budget, £71,253.59 spent (£3,208.41 under) - Plus £1,500 for UAE
- P5 (04/08-31/08): £63,247 budget, £62,125.94 spent (£1,121.06 under) - Underspend from P4 added (£3,204.01)
- P6 (01/09-28/09): £68,692.89 budget, £68,364.80 spent (£328.09 under) - Underspend from P5 added (£1,120.89)

**Monitoring**:
- Budget status automatically included in weekly summary emails
- Tracks: period budget, actual spend, pacing %, days remaining, required daily spend
- Alerts if pacing falls below 85% or exceeds 115%

---

## Quick Reference

### Emergency Contacts
- **Client Primary**: Lauryn Sobers (day-to-day management) - [Email TBD]
- **Client Senior**: Alex Clarke (senior oversight) - [Email TBD]
- **Marketing Approval**: Ciana (copy approval) - [Email TBD]
- **Technical Contact**: Beth (tracking/technical) - [Email TBD]
- **Account Manager**: Peter Empson - petere@roksys.co.uk - 07932 454652

### Important Links
- **Google Ads Account**: Multi-regional (UK, USA, EUR, ROW) - [Account IDs TBD]
- **Google Analytics**: [Property ID TBD]
- **Website**: https://www.smythson.com/ (with regional versions: /uk/, /us/, etc.)
- **Product Impact Analyzer**: https://docs.google.com/spreadsheets/d/1DtK0MX5qwISwO8blvbBT9rEQWqn-uVFp5hS3xBR-glo/
- **Strategy Documents**:
  - **FINAL AGREED Q4 2025 Strategy**: https://assets-organizer-cdn.gomarble.ai/mcp-agent/generated-reports/4f1715ac-5b98-4865-9694-42dc772abb1b-v1761732545570-smythson-all-accounts-strategy-for-q4-2025-1761732548802.html
  - Local copy: `q4-2025-strategy-report-final.html` (saved Oct 29, 2025)
  - Previous version: `q4-2025-strategy-report.html`
- **Performance Max Analysis**:
  - PMax H&S Channel Distribution Report: `pmax-hs-actual-channel-distribution-oct-2025.html` (Oct 2025 data)
  - PMax Placement Examples: `pmax-placement-examples.html`
  - PMax Asset Usage Guide: `pmax-asset-usage-guide-smythson.html`
- **Ad Copy Review**: Google Sheets/Docs shared with Ciana for approval

---

## Shared Drive Resources

**Last Scanned:** 2025-10-31

### Key Shared Documents

_Automatic monitoring via "Shared with Me" in Google Drive_
_Updated documents will appear here when detected by daily scans_

**Note**: This section tracks important resources shared by the client via Google Drive, including:
- Monthly reports and presentations
- Campaign briefs and strategy documents
- Product data and assets
- Client-maintained documentation

---

## Document History

| Date | Change Made | Updated By |
|------|-------------|------------|
| 2025-10-28 | Initial skeleton creation | Claude (automated) |
| 2025-10-28 | Added Q4 2025 Performance Max asset group strategy (10 prioritized groups) | User (via chat) |
| 2025-10-29 | Added Q4 2025 Multi-Regional Christmas Strategy (budget allocation, ROAS targets, timeline, Q4 2024 baseline) | Claude (from strategy report) |
| 2025-10-29 | **MAJOR UPDATE** from Teams chat: Added budget revision (£415k→£215k cut), client contacts (Lauryn, Alex, Ciana, Beth), product details (380+ Christmas gifts, notebooks, Panama collection), marketing approval bottleneck, conversion tracking issues (EUR/ROW GA4), customer segmentation removal, campaign structure changes (brand exact consolidation, H&S shopping restart, AI Max activation, customer acquisition settings), Christmas campaign planning, ad copy preferences. Moved Christmas Gifts to #1 priority asset group. | Claude (from Teams chat) |
| 2025-10-29 | Added final Q4 strategy report link (`q4-2025-strategy-report-final.html`), populated Important Dates section with complete Q4 implementation timeline, created 13 dated Google Tasks for budget/ROAS changes and performance reviews (Oct 29-Dec 31) | Claude (automated) |
| 2025-10-30 | Added Performance Max H&S channel distribution analysis (October 2025 actual data from Google Ads). Key finding: Search dominates with 93.9% impressions, 98.9% spend - significantly above industry benchmarks. Created visual report `pmax-hs-actual-channel-distribution-oct-2025.html` for client presentation. Strategic implication: Square product images (1:1) for Shopping ads are most critical asset type. | Claude (from Google Sheets channel report) |
| 2025-10-31 | Added **Strategy Experiments Log** section with 2 active tests (Diaries standalone campaign, category asset groups) and 1 failed test (blanket ROAS reduction). Includes complete experiment tracking: what changed, why, hypothesis, success criteria, rollout candidates. Review date Nov 11 for both active tests. | Claude (experiment tracking system) |
| 2025-10-31 | Added **Budget Tracking** section with MICE spreadsheet link, current P7 period details (£130,911.79 budget, 88.91% pacing), and historical periods P1-P6. Budget status now automatically included in weekly summary emails. | Claude (budget monitoring integration) |
| 2025-11-03 | **Q4 Strategy Progress Update**: Clarified budget approval process (£415k was proposal, £215k actually approved - not a cut). Added P7 final performance results (£151,072 spend, £479,840 revenue, 318% ROAS). All regions performing at or above Q4 ROAS targets. P8 (Nov 3-30) begins with £186,051 budget - the real Q4 scaling period. | Claude (via user clarification) |
| 2025-11-27 | **P8 Budget Correction**: Updated P8 budget from incorrect £218,653 to correct £186,051 (no P7 carryforward). P7 actual: £151,072 spent. Total Q4: £521,052. Reference: SMYTHSON-Q4-AUTHORITATIVE-FIGURES.md | Claude (correction from authoritative figures) |
| 2025-11-03 | Added **Google Ads Account Structure** section in Account Overview with four separate Smythson accounts (UK: 8573235780, USA: 7808690871, EUR: 7679616761, ROW: 5556710725), including budget allocations, ROAS targets, and known conversion tracking issues for EUR/ROW. | Claude (via user request) |
| 2025-11-03 | **MAJOR GEOGRAPHIC ANALYSIS**: Analyzed 3 months of actual ad delivery data (Aug-Nov 2025) via Google Ads API to determine which countries each account serves. UK=UK only, USA=US only, EUR=40 countries (78% Germany, 9.5% France, 8.9% Italy), ROW=134+ countries (53% Singapore, 21% Australia, 5% Canada). Created comprehensive geographic analysis document `documents/geographic-targeting-analysis.md` with detailed country breakdowns, regional insights, and strategic recommendations. Updated Account Structure section with geographic coverage details. | Claude (via GAQL analysis) |
| 2025-11-04 | Added **Google Merchant Center - Supplemental Feeds** section in Business Context. Documented Custom Label 0 supplemental feeds setup (117 products across Travel Bags, Card Holders, Jewellery Boxes). Both UK and USA accounts use identical feed data from UK source CSV. Created Google Sheets for Merchant Center upload. Noted USA CSV file is obsolete since same data used for both regions. Contact: Lauryn Sobers. | Claude (supplemental feed setup) |
| 2025-11-13 | **TASK DEDUPLICATION**: Removed 17 duplicate AI-generated task entries. Preserved all manual tasks and first occurrence of each AI task pattern. Cleanup based on provenance analysis showing 'Source: AI Generated' metadata. | Claude Code |
| 2025-11-13 | **CRITICAL: Brand vs Non-Brand YoY Analysis** - Added comprehensive year-over-year performance analysis (Oct 14-Nov 12, 2024 vs 2025) to Key Learnings section. **URGENT FINDINGS**: Brand ROAS collapsed 53% (1411% → 669%), revenue declined 22% despite 65% more spend, CPC increased 71%. Negative returns on incremental spend (£7,306 more spend → £35,015 less revenue). Non-brand conversion rate collapsed 91.6% (7.7% → 0.7%). **STATUS: Critical - immediate action required**. Files: `brand-yoy-comparison-2025-11-13-CORRECTED.txt`, `brand-vs-nonbrand-analysis-2025-11-13.txt`. Scripts created for ongoing monitoring. | Claude Code (via user request) |

---

## Notes for Population

This CONTEXT.md was created automatically from available data. Priority areas to populate:
1. **Account Overview** - Get client details, budget info, business type
2. **Strategic Context** - Review recent emails for strategy and goals
3. **Client Preferences** - Analyze communication patterns from emails
4. **Business Context** - Research website and products
5. **Known Issues** - Extract from recent emails (3 most recent available)
6. **Campaign Notes** - After reviewing Google Ads account structure

**Data sources to process**:
- 112 emails in /emails folder (focus on most recent 10-20)
- 2 meeting notes in /meeting-notes folder
- Experiment log entries (see above)

---

## Strategy Experiments Log

> **Purpose:** Track strategic changes and tests with complete information for future analysis and rollout decisions.

### Active Tests (Currently Monitoring)

#### Test #1: Diaries Standalone PMax Campaign
**Started:** Oct 28, 2025
**Review Date:** Nov 11, 2025
**Status:** 🟡 MONITORING

**What Changed:**
- Created "SMY | UK | P Max | Diaries" campaign (ID: 23194794411)
- Moved "Diaries AW25 - All" asset group from main H&S campaign
- Set dedicated budget for seasonal control

**Why (Strategic Reasoning):**
- Diaries have distinct AW25 seasonality (peak Sept-Dec)
- Product line represents significant revenue percentage
- Different ROAS profile than blended account average
- Need dedicated budget control during peak season

**Hypothesis (Expected Outcome):**
- +10% diary revenue vs blended performance in original campaign
- ROAS maintains or improves from 3.8 baseline
- Clearer performance signals (not blended with other products)
- Easier budget allocation during seasonal peak

**Success Criteria:**
- Diary revenue increase 8-12%
- ROAS 4.0+ (vs 3.8 blended)
- Budget management easier (qualitative)
- If successful, roll out to USA and EUR

**Early Signals:** [To be updated weekly]

**Rollout Candidates if Successful:**
- Smythson USA (high priority)
- Smythson EUR (high priority)
- Other clients with seasonal product lines (Tree2mydoor Christmas trees)

**ROK Experiments Sheet:** Row [TBD]

---

#### Test #2: Category-Based Asset Group Segmentation
**Started:** Oct 2025
**Review Date:** Nov 11, 2025
**Status:** 🟡 MONITORING

**What Changed:**
- Created 5 category-specific asset groups in "SMY | UK | P Max | H&S" campaign
- Categories: Travel Bags, Card Holders, Notebooks, Stationery, Jewellery Boxes

**Asset Groups Created:**
1. Jewellery Boxes and Rolls (ID: 6625631890) - ENABLED
2. Stationery (ID: 6625607553) - ENABLED
3. Card Holders (ID: 6625594993) - ENABLED
4. Travel Bags (ID: 6625003098) - ENABLED
5. Notebooks (ID: 6624708659) - ENABLED

**Why (Strategic Reasoning):**
- Different product categories have different margins and AOV
- Category-specific creative and messaging improves relevance
- Better performance visibility by category
- Google's algorithm can optimize for category-specific signals

**Hypothesis (Expected Outcome):**
- Higher-margin categories (Travel Bags, Card Holders) will show stronger ROAS
- Category-specific assets improve CTR and conversion rate
- Better insight into which categories drive performance
- Individual asset groups will outperform blended 3.8 ROAS baseline

**Success Criteria:**
- At least 3 of 5 asset groups show ROAS 4.0+
- Overall campaign ROAS maintains or improves
- Clear performance visibility by category enables optimization
- If successful, roll out to other Smythson regions and multi-category clients

**Early Signals:** [To be updated weekly]

**Rollout Candidates if Successful:**
- Smythson USA/EUR/ROW (adapt categories)
- Tree2mydoor (segment by tree type/size)
- Superspace (segment by furniture category)
- Any multi-category e-commerce client

**ROK Experiments Sheet:** Row [TBD]

---

### Completed Tests

#### ❌ FAILED: Blanket 15% ROAS Reduction
**Proposed:** Oct 28, 2025
**Status:** NOT IMPLEMENTED (superseded by better strategy)

**Original Plan:**
- Reduce ROAS targets by 15% across ALL Smythson campaigns
- Goal: Increase volume heading into Q4

**Why It Would Have Failed:**
- Ignores regional performance differences (UK ROAS 4.3 vs USA 2.5)
- Blanket approach doesn't account for market maturity
- Risk of unprofitable volume in lower-performing regions
- No strategic differentiation

**Better Alternative (What We Did Instead):**
- Regional ROAS targets based on market performance
- UK: Higher ROAS target (mature market, strong performance)
- USA: Lower ROAS target (growth market, building volume)
- EUR/ROW: Baseline targets for newer markets

**Learning:**
- One-size-fits-all approaches ignore account complexity
- Regional/product-level strategies beat blanket changes
- Always segment by performance before adjusting targets

**Added to Strategy Playbook:** Yes (Failed Tests section)

---

### Proven Winners (Rolled from Other Accounts)

[None yet - this section will contain successful strategies tested elsewhere and rolled out to Smythson]

---

## Planned Work

### [Smythson] Update dashboard with actual ROAS and revenue vs strategy targets
<!-- task_id: NG4ydWp5QzhydkYxTVVycA -->
**Status:** 📋 In Progress  

From meeting: 2025-11-10 Paid Search catch up 2
File: clients/smythson/meeting-notes/2025-11-10-paid-search-catch-up-2.md



### [Smythson] Simplify budget projection document for easier tracking
<!-- task_id: THlwWkljcVhMSEViVnJRTg -->
**Status:** 📋 In Progress  

From meeting: 2025-11-10 Paid Search catch up
File: clients/smythson/meeting-notes/2025-11-10-paid-search-catch-up.md



### [Smythson] Move diary asset group to new standalone PMAX campaign
<!-- task_id: V0Vuam84c0x0QVpoWHl0Rw -->
**Status:** 📋 In Progress  

253 products, 50 conversions in 30 days justifies separation
From meeting: 2025-11-10 Paid Search catch up
File: clients/smythson/meeting-notes/2025-11-10-paid-search-catch-up.md



### [Smythson] Create PMAX asset groups with Christmas and product page images, pause initially for review
<!-- task_id: Q2VWSk1rVGpPM2MwVmRYVw -->
**Status:** 📋 In Progress  

From meeting: 2025-11-10 Paid Search catch up
File: clients/smythson/meeting-notes/2025-11-10-paid-search-catch-up.md



### [Smythson] Move diary asset group to new standalone PMAX campaign
<!-- task_id: VzZPbjNBLTNiTHI1ZVk4cw -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 09:30)
**Client:** smythson
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Identified in recent meeting as justified by 253 products and 50 conversions in 30 days, supports campaign optimization
**AI Task ID:** 3e61e095-21c4-4510-b392-8ca695145e5b
---

Identified in recent meeting as justified by 253 products and 50 conversions in 30 days, supports campaign optimization



### [Smythson] Review and prepare PMAX Christmas campaign 1-week performance update
<!-- task_id: V0JrU0IwU25rWDFtYlhkVg -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 09:29)
**Client:** smythson
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Critical performance update promised to client for recent PMAX structure changes, need to monitor campaign scaling and key metrics
**AI Task ID:** bd68d3ff-41ae-4fc2-9eec-0dd86b40f005
---

Critical performance update promised to client for recent PMAX structure changes, need to monitor campaign scaling and key metrics



### [Smythson] Update Smythson dashboard with actual ROAS and revenue vs strategy targets
<!-- task_id: RmZIWXJjRGVZQUVtVllJcQ -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 09:29)
**Client:** smythson
**Priority:** P1
**Time Estimate:** 30 mins
**Reason:** Directly requested in recent meeting to provide daily budget visibility and track performance against Q4 strategy
**AI Task ID:** 5920c6d5-8626-4d12-9018-67dc854055d8
---

Directly requested in recent meeting to provide daily budget visibility and track performance against Q4 strategy



### [P1] Create merchant promotions for Smythson
<!-- task_id: U2l0a1E5TUh3UnhYbXlQQQ -->
**Status:** 📋 In Progress  

Priority 1: Set up merchant-level promotions in Google Merchant Centre for Smythson's campaigns.

Related to Black Friday/holiday season preparations.



### [URGENT] Smythson - Fix Greece Shipping Configuration (1,500 products affected)
<!-- task_id: VXZkVnczYWlSU0tSYTJOWA -->
**Status:** 📋 In Progress  

**Priority**: URGENT
**Products Affected**: ~1,500 greeting cards blocked from Greece market

**Issue**: Mismatched shipping currency for Greece
- Issue Code: missing_shipping_mismatch_of_shipping_method_and_offer_currency

**Action Items**:
1. Access Smythson Merchant Center (ID: 102535465)
2. Navigate to: Tools → Shipping and Returns
3. Check Greece shipping configuration:
   - Ensure shipping rates are configured in GBP (not EUR)
   - OR exclude Greece if not shipping there
4. Verify fix by re-checking Merchant Center status

**Additional Issues to Address**:
- Missing prices on ~100 greeting cards (check feed for blank price fields)
- Landing page errors on some products (review and fix URLs)

**Expected Impact**: Restore ~1,500 products to Shopping ads

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md



---

**Cleanup Note (2025-11-13):**
Removed 17 duplicate task entries:
- 7x: Move diary asset group to new standalone PMAX campaign
- 5x: Review and prepare PMAX Christmas campaign 1-week performanc
- 5x: Update Smythson dashboard with actual ROAS and revenue vs st

All manual tasks preserved. AI-generated tasks deduplicated to first occurrence only.

### [Smythson] Update dashboard with actual ROAS and revenue vs strategy targets
<!-- task_id: NG4ydWp5QzhydkYxTVVycA -->
**Status:** 📋 In Progress  

From meeting: 2025-11-10 Paid Search catch up 2
File: clients/smythson/meeting-notes/2025-11-10-paid-search-catch-up-2.md


### [Smythson] Simplify budget projection document for easier tracking
<!-- task_id: THlwWkljcVhMSEViVnJRTg -->
**Status:** 📋 In Progress  

From meeting: 2025-11-10 Paid Search catch up
File: clients/smythson/meeting-notes/2025-11-10-paid-search-catch-up.md


### [Smythson] Move diary asset group to new standalone PMAX campaign
<!-- task_id: V0Vuam84c0x0QVpoWHl0Rw -->
**Status:** 📋 In Progress  

253 products, 50 conversions in 30 days justifies separation
From meeting: 2025-11-10 Paid Search catch up
File: clients/smythson/meeting-notes/2025-11-10-paid-search-catch-up.md


### [Smythson] Create PMAX asset groups with Christmas and product page images, pause initially for review
<!-- task_id: Q2VWSk1rVGpPM2MwVmRYVw -->
**Status:** 📋 In Progress  

From meeting: 2025-11-10 Paid Search catch up
File: clients/smythson/meeting-notes/2025-11-10-paid-search-catch-up.md


### Smythson: Send PMAX Christmas Campaign 1-week performance update
<!-- task_id: YkEweXRfZVVOSG83YkcwVA -->
**Status:** 📋 In Progress  

CRITICAL: Performance update promised to client for PMAX structure changes made 2025-11-10. Monitor Christmas campaign scaling, ROAS maintenance, budget pacing, combined gifting revenue, and impression share.


### [Smythson] Follow up on Greece shipping configuration (Merchant Centre housekeeping)
<!-- task_id: WGFGU1FyWWg2V255LUJkZQ -->
**Status:** 📋 In Progress  

---
**Source:** Email sent (2025-11-14)
**Client:** smythson
**Priority:** P2 (Low priority - housekeeping)
**Time Estimate:** 15 mins
**Reason:** Follow up on email sent to Lauren and Alex about Greece shipping configuration issue in Merchant Centre
---

**Context:**
Sent email on Nov 14 flagging minor Merchant Centre housekeeping items:
- Greece shipping currency mismatch (~1,500 greeting cards affected)
- ~100 greeting cards with missing prices
- A few broken product links

**Follow-up Actions:**
1. Check if they've updated the Greece shipping settings in Merchant Centre
2. Verify products are no longer flagged as disapproved
3. If not done, send gentle reminder or offer to help

**Important:** This is low priority - Greece isn't a huge market for them. Just good to keep things tidy. No urgency needed in follow-up.


### [Smythson] Move diary asset group to new standalone PMAX campaign
<!-- task_id: dFpNUG54Z0RKRXNxRlY4NA -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 10:10)
**Client:** smythson
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Justified by 253 products and 50 conversions in 30 days, supports campaign optimization
**AI Task ID:** 13eb8d50-93de-48ce-b4dd-d3bf740ed08c
---

Justified by 253 products and 50 conversions in 30 days, supports campaign optimization


### Smythson: Remove Black Friday messaging from PMax assets
<!-- task_id: Y0JDT3ZRaEdOSHpjS3ZSRw -->
**Status:** 📋 In Progress  

Post-Black Friday asset revert. Plan: documents/2025-12-02-asset-revert-plan.md


### Smythson: Revenue Target Validation - Mid-December Check
<!-- task_id: OHFwc1ZsVEhLXzZhRXlfTQ -->
**Status:** 📋 In Progress  

📊 **Q4 STRATEGY MILESTONE REVIEW**

**What this is:**
- **CRITICAL CHECKPOINT** - Will we hit £780,691 revenue target?
- 6.5 weeks of Q4 complete (Oct 29 - Dec 15)
- 2.5 weeks remaining to year-end
- Projection and final course correction opportunity

**Context:**
- Total Q4 Budget: £367,014
- Target Revenue: £780,691
- Overall Target ROAS: Variable by region
- Time elapsed: ~72% of Q4
- Expected revenue to date: ~£560K (72% of £780K)

---

**CONVERSATION TO HAVE WITH CLAUDE:**

**Step 1 - Pull complete Q4 performance to date:**
```
"Run Smythson Q4 revenue validation - Oct 29 to Dec 15"
```

**Claude will show you:**
- Total Q4 revenue to date (all regions combined)
- Total Q4 spend to date
- Overall ROAS to date
- % of £780K target achieved
- % of £367K budget used

**Step 2 - Get projection to year-end:**
```
"Based on current pace, will we hit the £780,691 target by Dec 31?"
```

**Claude will:**
- Calculate daily/weekly revenue run rate
- Project final Q4 revenue (based on current pace)
- Show gap to target (positive or negative)
- Calculate probability of hitting target

**Step 3 - Regional performance breakdown:**
```
"Which regions are overperforming and underperforming vs expectations?"
```

**Claude will:**
- UK: Revenue, ROAS, vs target contribution
- USA: Revenue, ROAS, vs target contribution
- EUR: Revenue, ROAS, vs target contribution
- ROW: Revenue, ROAS, vs target contribution
- Identify winners and laggards

**Step 4 - Get final 2-week recommendations:**
```
"What changes should I make in the final 2 weeks to maximize Q4 revenue?"
```

**Claude will provide:**
- If AHEAD of target: Maintain course or optimize profitability?
- If ON TARGET: Stay the course, no changes
- If BEHIND target: Emergency optimizations:
  * Increase budgets in best-performing regions
  * Pause/reduce underperforming regions
  * Final ROAS adjustments
  * Push harder on winners

**Step 5 - Update tracker:**
```
"Update Q4 tracker with Dec 15 validation and final 2-week plan"
```

**Claude will:**
- Fill in Milestone 5.1 (Revenue Target Validation)
- Update cumulative performance table
- Document final 2-week strategy
- Set expectations for Dec 31 final assessment

---

**WHY THIS MATTERS:**
- **Last chance to course-correct** before Q4 ends
- Determine if £780K target is achievable
- Identify if emergency optimizations needed
- Prepare for final 2-week push or controlled finish

**POSSIBLE SCENARIOS:**

**Scenario 1: AHEAD of Target** (>78% to target by Dec 15)
- ✅ On track to exceed £780K
- Options: Maintain course, optimize for profitability, or push even harder
- Focus: Protect gains, don't overspend budget

**Scenario 2: ON Target** (72-78% to target)
- ✅ Pacing well, likely to hit target
- Options: Stay the course, minor tweaks only
- Focus: Steady execution through year-end

**Scenario 3: SLIGHTLY Behind** (65-72% to target)
- ⚠️ Behind pace but catchable
- Options: Moderate budget increases, optimize mix
- Focus: 2-week push to close gap

**Scenario 4: SIGNIFICANTLY Behind** (<65% to target)
- ❌ Unlikely to hit target without major changes
- Options: Emergency budget increases, pause laggards, all-in on winners
- Decision: Go all-in for target or accept shortfall and optimize ROAS?

---

**KEY QUESTIONS TO ANSWER:**

1. **Will we hit £780,691?** (Yes / Likely / Maybe / Unlikely)
2. **Revenue gap to target?** (£X,XXX over/under)
3. **Budget remaining?** (£X,XXX of £367K left)
4. **Best performing region?** (Reallocate budget here?)
5. **Worst performing region?** (Pause or reduce?)
6. **Final 2-week strategy?** (Aggressive push / Maintain / Optimize profitability)

---

**NEXT MILESTONE:** Dec 31 (Final Q4 Assessment - how did we do?)

**TIME REQUIRED:** 45-60 minutes (comprehensive analysis and decision-making)

---

**DOCUMENTS:**
- Q4 Strategy Tracker: clients/smythson/documents/q4-2025-strategy-tracker.md
- Monitoring Workflow: clients/smythson/documents/q4-strategy-monitoring-workflow.md
- Q4 Strategy Report: clients/smythson/documents/q4-2025-strategy-report-final.html


### Smythson: Review All December Changes (Pre-Implementation)
<!-- task_id: dDJ2c0dxbkhJQkM2ZEF1NQ -->
**Status:** 📋 In Progress  

📊 **Q4 STRATEGY MILESTONE REVIEW**

**What this is:**
- BEFORE implementing Dec 1 changes, review all November performance
- Go/no-go decision for December ROAS reductions and budget adjustments
- Assess whether to proceed as planned or modify the strategy

**November changes to review:**
- Nov 15: UK ROAS reduction (4.3 → 3.8)
- Nov 15: ROW campaign launch (£354/day)
- Nov 25: USA Thanksgiving boost ($2,604/day, ROAS reduction)

**December changes proposed:**
- UK: ROAS 3.8 → 3.5, budget maintain/adjust
- USA: ROAS 2.2 → 2.0, budget $2,131/day
- EUR: Budget €868 → €817/day, ROAS 1.5 → 1.2
- ROW: Budget £354 → £333/day, ROAS 1.0 → 0.9

---

**CONVERSATION TO HAVE WITH CLAUDE:**

**Step 1 - Review complete November performance:**
```
"Run Smythson November performance review - all regions"
```

**Claude will show you:**
- UK: Oct 29 - Nov 30 performance (full 5 weeks)
- USA: Nov 1 - Nov 30 performance (4 weeks)
- EUR: Oct 29 - Nov 30 performance (5 weeks)
- ROW: Nov 15 - Nov 30 performance (2 weeks)
- Overall Q4 progress vs £780K target

**Step 2 - Assess each November change:**
```
"Did November changes (UK ROAS drop, ROW launch, USA Thanksgiving) work as expected?"
```

**Claude will:**
- UK ROAS reduction: Success/failure vs hypothesis
- ROW launch: Break-even or profitable?
- USA Thanksgiving: Worth the budget increase?
- Overall November assessment

**Step 3 - Get December recommendations:**
```
"Based on November results, should I proceed with all planned December changes?"
```

**Claude will provide:**
- UK: Proceed with 3.8→3.5 or hold? (depends on Nov 15 results)
- USA: Proceed with 2.2→2.0 or adjust? (depends on Thanksgiving)
- EUR: Safe to reduce budget €868→€817? (depends on performance)
- ROW: Continue or pause? (depends on Nov 15-30 results)

**Step 4 - Update tracker and make decisions:**
```
"Update Q4 tracker with complete November results and December go/no-go decisions"
```

**Claude will:**
- Fill in all November milestones with actual results
- Update cumulative performance table (budget pacing, revenue progress)
- Document your decisions for December changes
- Highlight any course corrections needed

---

**WHY THIS MATTERS:**
- **Critical decision point** - Don't blindly implement December changes
- November results determine December strategy
- If November underperformed, December ROAS cuts might be too aggressive
- If November exceeded expectations, might push even harder
- Budget reallocation based on regional performance

**DECISION FRAMEWORK:**

**Proceed with December changes IF:**
- ✅ November changes met expectations
- ✅ On track for £780K Q4 target (or close)
- ✅ No major red flags in any region
- ✅ Budget pacing healthy (not overspending)

**Adjust December changes IF:**
- ⚠️ November mixed results (some worked, some didn't)
- ⚠️ Behind on revenue target but still achievable
- ⚠️ One region underperforming (reallocate budget)

**Pause/revert IF:**
- ❌ November changes failed to meet expectations
- ❌ Significantly behind revenue target
- ❌ Budget overspend concerns
- ❌ ROAS drops too severe

---

**NEXT MILESTONE:** Dec 15 (Revenue target validation - are we on track for £780K?)

**TIME REQUIRED:** 30-45 minutes (comprehensive review)

---

**DOCUMENTS:**
- Q4 Strategy Tracker: clients/smythson/documents/q4-2025-strategy-tracker.md
- Monitoring Workflow: clients/smythson/documents/q4-strategy-monitoring-workflow.md
- Q4 Strategy Report: clients/smythson/documents/q4-2025-strategy-report-final.html


### Smythson: Review USA Thanksgiving Boost Performance
<!-- task_id: b19WWnhHTjk1dTZ6blowMQ -->
**Status:** 📋 In Progress  

📊 **Q4 STRATEGY MILESTONE REVIEW**

**What happened:**
- Nov 25: USA budget increased $2,264 → $2,604/day (+15%)
- Nov 25: USA ROAS reduced (likely 2.5 → 2.2 based on strategy)
- This is 1-week review of Thanksgiving/Black Friday performance

**Expected outcomes (from strategy report):**
- Revenue increase: +20-30% during Thanksgiving week
- ROAS: Maintain ≥2.0
- Capture peak Black Friday/Cyber Monday demand

**Success criteria:**
- ✅ Thanksgiving week revenue ≥20% above normal
- ✅ ROAS maintains ≥2.0
- ✅ Profitable holiday sales capture

---

**CONVERSATION TO HAVE WITH CLAUDE:**

**Step 1 - Pull Thanksgiving week results:**
```
"Review USA Thanksgiving boost performance - Nov 25 to Dec 1"
```

**Claude will show you:**
- Baseline period (Nov 18-24): Revenue, ROAS, conversions
- Thanksgiving week (Nov 25-Dec 1): Revenue, ROAS, conversions
- Change: Actual vs expected (+20-30% revenue target)
- Peak day analysis (Black Friday Nov 29, Cyber Monday Dec 2)

**Step 2 - Get detailed analysis:**
```
"Did the USA Thanksgiving boost meet our expectations?"
```

**Claude will:**
- Compare actual results to hypothesis (+20-30% revenue, ROAS 2.0+)
- Show day-by-day performance (identify peak days)
- Assess whether budget increase was justified
- Calculate incremental revenue from the boost

**Step 3 - Update tracker:**
```
"Update Q4 tracker with USA Thanksgiving boost results"
```

**Claude will:**
- Fill in "Actual Results" for Milestone 3.1
- Add "Impact Assessment"
- Update cumulative performance table

**Step 4 - Get recommendation for December:**
```
"Based on Thanksgiving results, how should I adjust USA budget for December?"
```

**Claude will:**
- Recommend whether to maintain higher budget into December
- Suggest whether to proceed with planned Dec 1 ROAS reduction
- Identify if USA market warrants more aggressive spend

---

**WHY THIS MATTERS:**
- Validates whether holiday demand spikes justify budget increases
- Informs USA December strategy (proceed with changes or adjust?)
- Tests hypothesis: "USA Thanksgiving = major revenue opportunity"
- Shows whether higher budgets during peak periods are profitable

**NEXT MILESTONE:** Dec 1 (USA ROAS 2.2→2.0 + all regions December adjustments)

**TIME REQUIRED:** 15-20 minutes

---

**DOCUMENTS:**
- Q4 Strategy Tracker: clients/smythson/documents/q4-2025-strategy-tracker.md
- Monitoring Workflow: clients/smythson/documents/q4-strategy-monitoring-workflow.md


### Smythson: Review UK ROAS Reduction Impact (Nov 15 Change)
<!-- task_id: OVJPamlsdjFKZ0Q1bVhPeg -->
**Status:** 📋 In Progress  

📊 **Q4 STRATEGY MILESTONE REVIEW**

**What happened:**
- Nov 15: UK ROAS reduced from 4.3 → 3.8 (-11.6%)
- Budget: £2,716/day (unchanged)
- This is 14-day review of the change impact

**Expected outcomes (from strategy report):**
- Volume increase: +15-20%
- Revenue increase: +10-15% vs baseline
- ROAS: 3.8-4.0 range (acceptable for volume growth)

**Success criteria:**
- ✅ Revenue increase ≥10%
- ✅ ROAS maintains ≥3.8
- ✅ Profitable volume growth

---

**CONVERSATION TO HAVE WITH CLAUDE:**

**Step 1 - Pull the results:**
```
"Review UK ROAS reduction results - Nov 15 to Nov 28 vs baseline"
```

**Claude will show you:**
- Baseline period (Oct 29 - Nov 14): Revenue, ROAS, conversions
- Test period (Nov 15 - Nov 28): Revenue, ROAS, conversions
- Change: Actual vs expected
- Verdict: Success / Mixed / Failed

**Step 2 - Get detailed analysis:**
```
"Did the UK ROAS reduction meet our expectations?"
```

**Claude will:**
- Compare actual results to hypothesis (+10-15% revenue, ROAS 3.8+)
- Explain what worked / what didn't
- Show whether success criteria were met
- Calculate statistical significance

**Step 3 - Update tracker:**
```
"Update Q4 tracker with UK ROAS reduction results"
```

**Claude will:**
- Fill in "Actual Results" section in tracker (Milestone 2.1)
- Add "Impact Assessment"
- Update cumulative performance table

**Step 4 - Get recommendation:**
```
"Should I proceed with Dec 1 UK ROAS reduction to 3.5?"
```

**Claude will:**
- Based on Nov 15 results, recommend whether to continue scaling
- If Nov 15 reduction worked well → Recommend proceeding
- If mixed/failed → Recommend holding or reverting

---

**WHY THIS MATTERS:**
- Validates whether ROAS reductions drive volume as expected
- Informs decision on Dec 1 changes (all regions)
- Tests key hypothesis: "Lower ROAS = higher profitable volume in Q4"

**NEXT MILESTONE:** Dec 1 (UK ROAS 3.8→3.5, USA/EUR/ROW adjustments)

**TIME REQUIRED:** 15-20 minutes

---

**DOCUMENTS:**
- Q4 Strategy Tracker: clients/smythson/documents/q4-2025-strategy-tracker.md
- Monitoring Workflow: clients/smythson/documents/q4-strategy-monitoring-workflow.md


### Smythson: Review Week 1 Q4 Performance (UK/EUR/USA Launches)
<!-- task_id: LTNkRkliczloakhIQWZROA -->
**Status:** 📋 In Progress  

📊 **Q4 STRATEGY MILESTONE REVIEW**

**What happened:**
- Oct 29: UK & EUR campaigns launched
- Nov 1: USA campaign launched
- This is the first formal review of Q4 strategy performance

**Expected outcomes (from strategy report):**
- UK: Establish baseline, ROAS 4.3+
- EUR: Establish baseline, ROAS 1.5+
- USA: Establish baseline, ROAS 2.5+

---

**CONVERSATION TO HAVE WITH CLAUDE:**

**Step 1 - Pull the data:**
```
"Review Smythson Week 1 Q4 performance - Oct 29 to Nov 10"
```

**Claude will show you:**
- UK: Spend, revenue, ROAS, conversions (12 days of data)
- EUR: Spend, revenue, ROAS, conversions (12 days)
- USA: Spend, revenue, ROAS, conversions (9 days)
- Comparison to expected baselines
- Any red flags or issues

**Step 2 - Update the tracker:**
```
"Update Q4 strategy tracker with Week 1 and 2 results"
```

**Claude will:**
- Fill in actual results for UK/EUR/USA launches in tracker
- Update cumulative performance table
- Mark milestones 1.1, 1.2, 1.3 as complete with results

**Step 3 - Get recommendation:**
```
"Based on Week 1-2 results, should I proceed with Nov 15 changes?"
```

**Claude will:**
- Assess if baselines are healthy
- Confirm readiness for UK ROAS reduction + ROW launch
- Recommend: proceed / delay / adjust

---

**WHY THIS MATTERS:**
- First check that Q4 strategy is working
- Validates baseline performance before making changes
- Go/no-go decision for Nov 15 milestone

**NEXT MILESTONE:** Nov 15 (UK ROAS reduction + ROW launch)

**TIME REQUIRED:** 10-15 minutes

---

**DOCUMENTS:**
- Q4 Strategy Tracker: clients/smythson/documents/q4-2025-strategy-tracker.md
- Q4 Strategy Report: clients/smythson/documents/q4-2025-strategy-report-final.html


### Smythson: Dec 1 - ROW Budget & ROAS Change
<!-- task_id: V1lHeEVPVDNGdGtRMFNacA -->
**Status:** 📋 In Progress  

Budget £354→£333/day; ROAS reduction to 0.9
Region: ROW


### Smythson: Dec 1 - USA ROAS Reduction
<!-- task_id: SXFmSFh5VWg3cjl3ai0xNA -->
**Status:** 📋 In Progress  

REDUCE: ROAS from 2.2→2.0 (-9.1%) budget to $2,131/day
Region: USA


### Smythson: USA Thanksgiving Budget Boost
<!-- task_id: bEhBYWR6U3phUk51cGxHWA -->
**Status:** 📋 In Progress  

INCREASE: Budget $2,264→$2,604/day (+15% Thanksgiving) and ROAS reduction
Region: USA


### Smythson: Q4 Performance Review (Mid-Nov)
<!-- task_id: ZzB2N0pWRzVQYW90b0pJZQ -->
**Status:** 📋 In Progress  

Performance Assessment vs targets
Scope: All Regions


### Smythson: Reduce UK ROAS Target
<!-- task_id: cXlYd1VGcnFsRFFqM3Y0Zw -->
**Status:** 📋 In Progress  

REDUCE: ROAS from 4.3→3.8 (-11.6%) budget unchanged
Region: UK


### Smythson: Launch ROW Q4 Campaign
<!-- task_id: SzZ4MUVEN3AxRFl4S0E1eg -->
**Status:** 📋 In Progress  

SET: Budget £354/day + Target ROAS 1.0 (baseline)
Region: ROW (Rest of World)


### Smythson: Copy Teams meeting chats to CONTEXT.md
<!-- task_id: OHFpZHZtM1puaXRDdWFfVA -->
**Status:** 📋 In Progress  

Recurring reminder every 2 weeks:

1. Open Teams chat with Smythson team
2. Copy recent conversations from last 2 weeks
3. Paste into Claude Code
4. Ask Claude to update CONTEXT.md

File: clients/smythson/CONTEXT.md


### [smythson] Provide performance summary report for leadership presentation
<!-- task_id: MDQ1QXRod1pBVXNJeFJ4TQ -->
**Status:** 📋 In Progress  

From: Smythson
Date: 2025-12-10
AI Generated (2025-12-10 10:32)


### [smythson] Review meeting: Smythson
<!-- task_id: ODV4dm1VOThLdlpBWjBKRg -->
**Status:** 📋 In Progress  

Meeting: Smythson
Date: 2025-12-10
File: /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/meeting-notes/2025-12-10-smythson-smythson.md

Review meeting notes and update CONTEXT.md with key insights.


## Completed Work

### Smythson: Analyze competitor bidding strategies
<!-- task_id: ZE1NZXphWGtUR2tYamVKVw -->
**Status:** ✅ Completed (2025-10-29)  

Research and document competitor bidding patterns for Smythson's product categories. Focus on luxury stationery segment. Deliverable: Competitive analysis report with recommendations for bid adjustments and new keyword opportunities.


### Smythson: Begin 15% ROAS reduction across all campaigns
<!-- task_id: YXBYajduMGFlTXBiclRnRQ -->
**Status:** ✅ Completed (2025-10-29)  

From Smythson meeting on 2025-10-28. Reduce ROAS targets by 15% across all Smythson campaigns to increase volume and scale spend heading into Q4 peak season. START DATE: 2025-10-29. Monitor performance closely after implementation.
This wasn't carried out; it was superseded by the new strategy that was produced. 



### Smythson: Launch UK Q4 Campaign
<!-- task_id: Q192QXpPM1NaUjZGRHRyWQ -->
**Status:** ✅ Completed (2025-11-03)  

SET: Budget £2,716/day + Target ROAS 4.3 (baseline)
Region: UK


### Smythson: Launch EUR Q4 Campaign
<!-- task_id: UExDQWFCN3p6X1dvamlZQw -->
**Status:** ✅ Completed (2025-11-03)  

SET: Budget €868/day + Target ROAS 1.5 (baseline)
Region: EUR


### Smythson: Launch USA Q4 Campaign
<!-- task_id: Z0oxbzFRbzNPcHBsVnhhQw -->
**Status:** ✅ Completed (2025-11-03)  

SET: Budget $2,264/day + Target ROAS 2.5 (baseline)
Region: USA


### [Smythson] Send UK & USA Custom Label 0 supplemental feeds to Lauryn
<!-- task_id: bWtlM3YtNXMxR2Z6M3JHMQ -->
**Status:** ✅ Completed (2025-11-04)  

Custom label 0 supplemental feeds prepared for UK and USA markets.

Files created:
- clients/smythson/product-feeds/Smythson_Custom_Label_0_UK.csv (117 products)
- clients/smythson/product-feeds/Smythson_Custom_Label_0_USA.csv (117 products - identical to UK)

Email draft ready:
- clients/smythson/email-draft-2025-11-04-supplemental-feeds.txt

Products breakdown:
- Travel Bags: 24 products
- Card Holders: 44 products
- Jewellery Boxes: 49 products

Action: Send email to Lauryn Sobers with both CSV files attached.



### Smythson: Copy Teams meeting chats to CONTEXT.md
<!-- task_id: N2JyV0M5LUlEY20zRUR5Vw -->
**Status:** ✅ Completed (2025-11-09)  

Recurring reminder every 2 weeks:

1. Open Teams chat with Smythson team
2. Copy recent conversations from last 2 weeks
3. Paste into Claude Code
4. Ask Claude to update CONTEXT.md

File: clients/smythson/CONTEXT.md

After completing, recreate this task with due date 2 weeks out.



---

## Post-Black Friday Asset Swap Workflow

**Added**: 2025-11-25
**Purpose**: Automated replacement of Black Friday promotional copy with post-BF Christmas/New Collection messaging
**Execution Date**: Tuesday, December 3rd, 2025
**Tool Location**: `/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/`

### Overview

Smythson runs Black Friday promotional campaigns from November 17 - December 1, 2025. Immediately after (December 2nd onwards), all promotional copy must be swapped back to Christmas Phase 2 messaging. This is a large-scale asset swap across all four regional accounts.

**Scale:**
- 4 Google Ads accounts (UK, USA, EUR, ROW)
- ~30 Performance Max campaigns
- ~60 asset groups
- ~1,500 individual text assets (headlines, long headlines, descriptions)

### Asset Source

**Google Spreadsheet**: https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit

**Shared with**: mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com

**Sheet Structure:**
- **UK ad copy** tab: Assets for Smythson UK (8573235780)
- **US ad copy** tab: Assets for Smythson USA (7808690871)
- **EUR ad copy** tab: Assets for Smythson EUR (7679616761)
- **ROW ad copy** tab: Assets for Smythson ROW (5556710725)
- **Christmas phase 2** tab: Secondary Christmas messaging (if needed)

**Column Format:**
| Campaign | Asset Group | Headline 1-15 | Long headline 1-5 | Description 1-4 |
|----------|-------------|---------------|-------------------|-----------------|

### Workflow Steps

#### 1. Pre-Execution Verification (December 2nd)

```bash
# Verify access to spreadsheet
python3 -c "from mcp_google_sheets import list_sheets; print(list_sheets('1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g'))"

# Should show: ["Christmas phase 2", "US ad copy", "UK ad copy", "EUR ad copy", "ROW ad copy"]
```

#### 2. Generate Swap CSVs (one per region)

Run for each region to create swap instructions:

```python
# Pseudo-code - to be implemented as generate_smythson_swaps.py

for region in ['UK', 'USA', 'EUR', 'ROW']:
    # Read regional sheet from Google Spreadsheet
    sheet_data = read_google_sheet(
        spreadsheet_id='1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g',
        sheet_name=f'{region} ad copy'
    )
    
    # For each row (campaign + asset group):
    for row in sheet_data:
        campaign_name = row['Campaign']
        asset_group_name = row['Asset Group']
        
        # Find asset group in Google Ads
        asset_group_id = find_asset_group(campaign_name, asset_group_name)
        
        # Get current assets
        current_assets = get_current_assets(asset_group_id)
        
        # Generate swap instructions
        swaps = []
        for i in range(1, 16):  # Headlines 1-15
            if row[f'Headline {i}']:
                swaps.append({
                    'Original_Text': current_assets['headlines'][i-1],
                    'Asset_Type': 'Headline',
                    'Replacement_Text': row[f'Headline {i}'],
                    'Action': 'SWAP'
                })
        
        # Repeat for Long Headlines (1-5) and Descriptions (1-4)
    
    # Export to CSV
    export_to_csv(swaps, f'output/smythson-{region}-post-bf-swaps.csv')
```

**Output files:**
- `output/smythson-UK-post-bf-swaps.csv`
- `output/smythson-USA-post-bf-swaps.csv`
- `output/smythson-EUR-post-bf-swaps.csv`
- `output/smythson-ROW-post-bf-swaps.csv`

#### 3. Review CSV Files

Manual check:
1. Open each CSV in Excel/Google Sheets
2. Verify `Original_Text` matches current Black Friday copy
3. Verify `Replacement_Text` is correct Christmas/New Collection copy
4. Check character limits (Headlines ≤30, Long Headlines/Descriptions ≤90)
5. Confirm `Action=SWAP` for all rows

**Generate HTML visualizations for client review:**

```bash
python3 generate_html_preview.py --csv output/smythson-UK-post-bf-swaps.csv
# Opens browser with formatted table showing old → new
```

#### 4. Dry-Run Execution (Dec 2nd evening)

Test on one small asset group first:

```bash
python3 execute_asset_optimisation.py \
  --customer-id 8573235780 \
  --campaign-id [test-campaign-id] \
  --csv output/smythson-UK-post-bf-swaps.csv \
  --dry-run
```

**Check:**
- All assets found successfully
- No character limit errors
- Batching strategy appropriate
- Execution log clean

#### 5. Live Execution (December 3rd - Tuesday morning)

Execute sequentially by region:

```bash
# UK first (largest market, highest priority)
python3 execute_asset_optimisation.py \
  --customer-id 8573235780 \
  --csv output/smythson-UK-post-bf-swaps.csv \
  --live

# USA second
python3 execute_asset_optimisation.py \
  --customer-id 7808690871 \
  --csv output/smythson-USA-post-bf-swaps.csv \
  --live

# EUR third
python3 execute_asset_optimisation.py \
  --customer-id 7679616761 \
  --csv output/smythson-EUR-post-bf-swaps.csv \
  --live

# ROW last
python3 execute_asset_optimisation.py \
  --customer-id 5556710725 \
  --csv output/smythson-ROW-post-bf-swaps.csv \
  --live
```

**Monitor:**
- Success rate (target: 100%)
- Execution logs for errors
- Time taken per region (~5-15 minutes each)

#### 6. Post-Execution Validation

Verify in Google Ads UI:
1. Spot-check 3-5 asset groups per region
2. Confirm Black Friday copy is gone
3. Confirm Christmas/New Collection copy is live
4. Check no asset groups below minimums (3 headlines, 1 long headline, 2 descriptions)

**Send confirmation to Lauryn:**
- "Post-Black Friday asset swap completed across all regions"
- Include success rates and any issues encountered
- Attach execution logs if requested

### Important Notes

**Asset Order Will Change:**
After swapping, assets will appear in a different order in Google Ads UI (usually alphabetical or by creation date). This is normal API behaviour and doesn't affect performance. Explain to client if they notice.

**Character Limit Compliance:**
All text in spreadsheet MUST meet character limits or swaps will fail. The spreadsheet should be validated before execution.

**Spreadsheet Must Be Final:**
The Google Spreadsheet should be locked/finalized by December 2nd. Any late changes after CSVs are generated will not be reflected in the swap.

**Cannot Rollback Easily:**
Once swapped, rolling back requires creating a new CSV with reverse swaps. Keep backups of original Black Friday copy if needed.

**Regional Differences:**
Each region has different messaging - ensure you're using the correct sheet tab for each account. UK ≠ USA ≠ EUR ≠ ROW.

### Troubleshooting

**"Asset not found in campaign"**
- **Cause:** Campaign/Asset Group name in spreadsheet doesn't match Google Ads exactly
- **Fix:** Compare spreadsheet names to Google Ads UI, update spreadsheet to match exactly

**"Character limit exceeded"**
- **Cause:** Replacement text too long (>30 chars for headlines, >90 for long headlines/descriptions)
- **Fix:** Edit spreadsheet to shorten text, regenerate CSV

**"Resource limit exceeded"**
- **Cause:** This shouldn't happen with smart ordering (v1.1+)
- **Fix:** Check execution logs, verify asset counts, report as bug

**Spreadsheet access denied**
- **Cause:** Service account permissions issue
- **Fix:** Verify mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com has View access

### Future Improvements

**Automation Opportunities:**
1. Auto-generate CSVs from spreadsheet (eliminate manual step)
2. Scheduled execution on December 3rd (cron job)
3. Auto-validation of character limits in spreadsheet
4. Post-execution report sent to client automatically

**Spreadsheet Enhancements:**
1. Add character count formulas to validate limits
2. Colour-code cells that exceed limits
3. Include preview of current Black Friday copy for comparison
4. Add checkbox column for "reviewed" status

### Related Documentation

- **Asset Swap Tool**: `/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/ASSET-SWAP-TOOL.md`
- **General Optimisation Flow**: `/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/ASSET-OPTIMISATION-FLOW.md`
- **Meeting Notes**: `clients/smythson/meeting-notes/2025-11-24--enhanced-notes--smythson.md` (discussion of this workflow)

### Execution History

| Date | Region | Assets Swapped | Success Rate | Notes |
|------|--------|----------------|--------------|-------|
| 2025-12-03 | UK | TBD | TBD% | Post-Black Friday swap |
| 2025-12-03 | USA | TBD | TBD% | Post-Black Friday swap |
| 2025-12-03 | EUR | TBD | TBD% | Post-Black Friday swap |
| 2025-12-03 | ROW | TBD | TBD% | Post-Black Friday swap |

(Update this table after execution with actual results)

---
