# OTC (Online Tech Comms / Camera Manuals) - Context & Strategic Notes

> **Purpose**: Living document with important context for Google Ads analysis and reporting.
> **Last Updated**: 2025-10-30

---

## Account Overview

**Client Since**: [Pre-2024 - exact date TBD]
**Monthly Budget**: [TBD - analyze from Google Ads]
**Primary Contact**: Jeff Seymour - jeff@jeffseymour.co.uk - 07786 393088
**Account Manager**: Peter Empson

**Business Type**: E-commerce (Digital Products - PDF Camera Manuals)
**Industry**: Digital Publishing / Photography Equipment Documentation
**Geographic Focus**: UK and USA (dual currency operations - GBP and USD)

**Sister Business**: Print My PDF (mentioned as experiencing similar performance issues)

---

## Strategic Context

### Current Strategy
- **Campaign Structure**: Separate campaigns for UK and US markets
- **Campaign Types**: Both Performance Max and Search campaigns running
- **Key Campaigns**:
  - US | CMN (Camera Manuals) - PMax and Search
  - UK | CMN Search (top performer)
- **Bidding Strategy**: Target ROAS bidding (180-250% range historically)
- **Key Focus Areas**: Conversion rate recovery, US market stabilization, CPA reduction

### Why This Approach?
- Geographic split (UK/US) required due to dual currency operations (GBP/USD)
- Camera manual business has been established for 10+ years with consistent profitability
- Long-running campaigns mean Google has extensive learning data about target search terms
- Historical success with conversion-focused bidding strategies

### Current Crisis (October 2025)
**CRITICAL BUSINESS SITUATION**:
- Client facing potential account termination within 1 month if no improvement
- CPA has escalated to £12 when average sale is only £18
- Client stated: "I'm going to have to make some tough decisions in about a month if there's no sign of improvement" (Oct 22, 2025)
- New pricing launched Oct 21, 2025 for Print My PDF
- Stripe integration pending (expected within days as of Oct 22, 2025)

### Goals & KPIs
**Primary Goal**: Profitability restoration - reduce CPA to sustainable levels
**Historical Target CPA**: £5-6 (UK campaigns achieving this as of Sept 2024)
**Current CPA**: £12 (unsustainable - avg sale £18)
**US CPA Crisis**: £72.35 (Sept 2024) vs UK £5.75
**Target ROAS**: 180-250% (variable by campaign)
**Other KPIs**: Conversion rate recovery (currently 0.39% vs historical 3.61% for US)

---

## Historical Performance Patterns

### Seasonality
[TBD - needs historical analysis across multiple years]

### Year-Over-Year Trends
- Account has been profitable for 10+ years until recent crisis (as of Sept 2024)
- UK campaigns maintain strong performance historically
- US market showing long-term stability until mid-August 2024 collapse

### Known Anomalies

**MAJOR CRISIS PERIOD: July-October 2024**

**Timeline of Events**:

**July 4, 2024**: Conversion tracking changed in Tag Manager
- Enhanced conversions implementation by client's Bangladesh developer
- Initial changes included currency and order value tracking

**July 4-17, 2024**: Double Counting Issue
- Conversion tracking error causing inflated metrics
- Made Google's bidding algorithms think performance was better than reality
- Impressions and cost increased dramatically

**Mid-August 2024 (around Aug 19)**: Performance Cliff
- US campaigns: Conversion rate dropped 70% in 14 days (Sept 6 baseline)
- Overall conversion rate dropped 36% across all campaigns
- US campaigns particularly affected - dropped "off the radar" for impression share
- UK campaigns: 20% conversion rate drop but recovered
- Jeff described: "less money coming in than going out, which hasn't happened for 15 years"

**Late August 2024**: Impression Recovery Period
- Impressions started recovering from double-counting distortion
- However, conversions continued falling

**September 2024**: Critical Failure Period
- US conversion rate: 0.39% (down from 3.61%)
- US CPA: £72.35 vs UK £5.75
- 85% drop in US conversion rate vs UK
- Top US products from August had ZERO sales in September
- Competitor activity increased significantly during this period

**October 1-7, 2024**: Troubleshooting Period
- Oct 1: Currency tracking removed from Tag Manager per Peter's recommendation
- Oct 6: Still no improvement - "Still nothing for the US but the UK is performing really well"
- Oct 7: Bidding strategy "slowing up because it is getting no conversion data"
- US actual sales: 60 GBP + 30 USD per week (vs expected 140)

**October 22, 2025**: Client Ultimatum Email
- New pricing went live Oct 21, 2025
- Stripe integration pending
- CPA now £12, average sale £18
- Client warns of "tough decisions in about a month" if no improvement
- Performance described as "continuing to get worse this month"

---

## Client Preferences & Communication

### Communication Style
- **Preferred Update Frequency**: Regular email updates during crisis periods
- **Preferred Format**: Email with detailed analysis and data/charts
- **Detail Level**: Appreciates thorough technical analysis with visual evidence
- **Response Time**: Responds quickly during crisis situations (same day)

### Decision-Making
- **Who Makes Final Decisions**: Jeff Seymour (owner/sole decision maker)
- **Technical Resources**: Has developer in Bangladesh (handles Tag Manager, Cookiebot, technical implementations)
- **Risk Tolerance**: Normally conservative, but desperate for solutions during crisis period
- **Approval Process**: Direct communication with Peter, willing to try suggested changes

### Red Flags / Sensitive Topics

**CRITICAL SENSITIVITIES**:
- **Financial Pressure**: Client explicitly stated cash flow negative for first time in 15 years
- **Developer Changes**: Very sensitive about Bangladesh developer making Google Ads changes (told him to "keep his hands off Google Ads")
- **Time Pressure**: Has given 1-month ultimatum (as of Oct 22, 2025) before making "tough decisions"
- **US Market Failure**: Extremely frustrated by US campaigns failing while UK performs well
- **CPA Sensitivity**: Cannot sustain CPA above ~£11-12 given £18 average sale value

**Communication Notes**:
- Jeff becomes increasingly urgent/stressed in communication during poor performance
- Appreciates Peter's thorough diagnostic approach
- Wants evidence-based explanations, not guesses
- Responds well to actionable recommendations with clear rationale

---

## Business Context

### Product/Service Details

**Main Product**: PDF Camera Manuals (downloadable instruction manuals for cameras)

**Top Performing Products (pre-crisis)**: Camera manufacturer manuals (various models)

**Business Model**:
- Digital product delivery (instant download PDFs)
- Low operational costs (no physical inventory)
- Established for 10+ years
- Operates in both UK and US markets

**Pricing Strategy**:
- Average sale value: £18
- Pricing changed June 4, 2024, adjusted June 25, 2024
- Main change: Very largest manuals (400+ pages) now cost more
- New pricing for Print My PDF launched Oct 21, 2025

**Sister Business**: Print My PDF (experiencing similar performance challenges)

### Website & Technical

**Website Platform**: [TBD - appears to be custom or standard CMS with WooCommerce/similar]

**Known Technical Issues**:

1. **Conversion Tracking Crisis (July-Oct 2024)**:
   - Enhanced conversions implementation by Bangladesh developer
   - Initial implementation included currency/order value tracking (removed Oct 1, 2024)
   - Double counting issue from July 4-17, 2024
   - US dollar conversion tracking failure (conversions not registering)
   - Suspect issue related to multi-currency handling (GBP vs USD)

2. **Cookie Consent Implementation**:
   - Cookiebot implemented with geographic variants
   - Strict banner: EU and UK
   - Less strict: USA, Canada, Australia
   - No banner: Rest of world
   - Tested with NordVPN and working as intended
   - Initially may have deterred US visitors but was adjusted

3. **Geo-Redirect/Currency Detection**:
   - System detects customer location and charges appropriate currency
   - Mechanism for GBP vs USD detection unknown
   - May be related to conversion tracking issues

**Conversion Tracking**:
- **Setup**: Google Ads conversion tracking via Tag Manager
- **Known Issues**:
  - US dollar orders not being tracked properly (Sept-Oct 2024)
  - Enhanced conversions implementation problematic
  - Fixed conversion value setup in Google Ads (Jeff's dev wanted to change, but told not to)
- **Last Audit**: Ongoing troubleshooting through Sept-Oct 2024
- **Current Status**: Peter tested links from Merchant Centre multiple times - all working OK
- **Bid Strategy Impact**: Bid strategy exclusion period created for July 17-Aug 27 to exclude corrupted data

### Competitive Landscape

**Main Competitors** (US Market - identified Sept 2024):
- **eBay**: Sells some manuals, but limited selection
- **Amazon**: Don't sell manuals, sell cameras (mismatch targeting)
- **Adorama**: Don't sell manuals, sell cameras (mismatch targeting)
- **B&H Photo**: Don't sell manuals, sell cameras (mismatch targeting)
- **Walmart**: Don't sell manuals, sell cameras (mismatch targeting)

**Competitive Context**:
- Jeff frustrated by Google showing ads against camera retailers who don't sell manuals
- These competitors are taking impression share but aren't directly competitive
- Significant increase in competitor activity during August-September 2024
- OTC lost impression share dramatically during crisis period ("dropped off the radar")

**Competitive Advantages**:
- Specialized niche (camera manuals only)
- 10+ years established business
- Extensive manual catalog
- Instant digital delivery

**Competitive Disadvantages**:
- Competing against major retailers (eBay, Amazon) despite product mismatch
- Limited average sale value (£18) restricts advertising budget flexibility
- US market more competitive than UK

---

## Known Issues & Challenges

### Current Issues (October 2025)

1. **CRITICAL: Business Survival Issue** - ACTIVE
   - **Description**: Unsustainable CPA (£12) vs average sale (£18)
   - **Impact**: Client has given 1-month warning before "tough decisions"
   - **Status**: New pricing (Oct 21) and Stripe integration pending
   - **Next Review**: Approximately Nov 22, 2025

2. **US Market Conversion Tracking Failure** - PARTIALLY RESOLVED?
   - **Description**: US campaigns lost 85% of conversion rate vs UK
   - **Impact**: US CPA £72.35 vs UK £5.75 (September 2024)
   - **Status**: Currency tracking removed from Tag Manager (Oct 1, 2024), but still showing poor performance as of Oct 22, 2025
   - **Root Cause**: Suspected multi-currency handling issue in Tag Manager Enhanced Conversions

3. **Bidding Strategy Data Starvation** - ACTIVE
   - **Description**: Bidding strategy "slowing up because it is getting no conversion data"
   - **Impact**: Inability to optimize bids, leading to wasted spend
   - **Status**: Ongoing as of Oct 7, 2024

### Recurring Challenges

1. **Multi-Currency Complexity**:
   - UK (GBP) and US (USD) operations require separate tracking
   - Conversion tracking implementations must handle both currencies correctly
   - Historical issues with Enhanced Conversions and currency handling

2. **Low Average Order Value**:
   - £18 average sale leaves little margin for advertising costs
   - CPA must stay below ~£11-12 to be profitable
   - Small margin for error or efficiency losses

3. **Developer Coordination**:
   - Bangladesh-based developer makes technical changes that can affect tracking
   - Need tight coordination between Peter (Google Ads) and Jeff's developer (Tag Manager/site)
   - Previous developer changes caused major tracking disruptions

4. **Conversion Rate Volatility**:
   - Historical pattern of sudden, dramatic drops in conversion rate
   - Difficult to identify root causes (tracking vs site vs market factors)
   - UK and US markets behave very differently

### External Factors to Monitor

1. **Competitor Activity**:
   - Increased significantly Aug-Sept 2024
   - May continue to squeeze market share
   - Mismatched competitors (camera retailers vs manual sellers) affect auction dynamics

2. **Google Algorithm/Bidding Changes**:
   - Smart Bidding requires consistent conversion data
   - Data disruptions from July-August 2024 may have long-lasting effects on algorithm learning

3. **Cookie Consent Regulations**:
   - Stricter requirements in EU/UK vs other markets
   - May affect conversion tracking accuracy
   - Could reduce reported conversions vs actual sales

4. **Print My PDF Performance**:
   - Sister business experiencing similar issues
   - May indicate broader market or technical factors beyond just Camera Manuals

---

## Key Learnings & Insights

### What Works Well

1. **UK Campaigns Performance**:
   - UK | CMN Search campaign doubled sales and increased conversion rate 51% (Sept 2024)
   - UK campaigns maintaining CPA of £5.58-£5.75 even during crisis period
   - UK campaigns recovered from double-counting issue more effectively than US

2. **Established Search Terms**:
   - Account has 10+ years of data
   - Google knows exactly what terms to target for camera manuals
   - Top phrases are consistently camera manual-related

3. **Campaign Structure**:
   - Geographic split (UK/US) appropriate for dual currency business
   - Mix of PMax and Search campaigns provides coverage and control

### What Doesn't Work

1. **Enhanced Conversions Implementation**:
   - July 2024 implementation by Bangladesh developer caused major issues
   - Currency and order value tracking in Tag Manager created problems
   - DO NOT let developer make changes to Google Ads conversion settings

2. **Multi-Currency Enhanced Conversions**:
   - Standard Tag Manager enhanced conversion setup failed with GBP/USD orders
   - Customer-only data (no currency/value) approach may be safer

3. **US Market Recovery**:
   - Unlike UK, US campaigns did not recover after double-counting fix
   - Conversion rate remained at 0.39% vs historical 3.61%
   - Root cause still unclear as of October 2024

### Successful Tests & Experiments

| Date | Test Description | Result | Action Taken |
|------|-----------------|--------|--------------|
| Oct 1, 2024 | Removed currency tracking from Tag Manager Enhanced Conversions | Minimal impact - US still underperforming | Continue monitoring |
| Sept 2024 | Bid strategy date exclusion (July 17-Aug 27) to exclude corrupted data | Unknown impact | Implemented to prevent bad data affecting Smart Bidding |
| [Prior] | Target ROAS reduction to 180% per Google recommendation | [TBD - outcome not in emails] | Attempted to stimulate sales volume |

### Failed Tests (Learn From)

| Date | Test Description | Why It Failed | Lesson Learned |
|------|-----------------|---------------|----------------|
| July 4, 2024 | Enhanced Conversions with currency/order value tracking in Tag Manager | Caused double counting and US conversion tracking failure | Keep Tag Manager Enhanced Conversions simple - customer data only, no currency/value |
| June 4, 2024 | Price increases (adjusted June 25) | Timing coincides with performance issues, though causation unclear | Major pricing changes should be monitored closely and may interact with algorithm learning periods |

---

## Campaign-Specific Notes

### Campaign: US | CMN (Camera Manuals) - Performance Max
- **Purpose**: Automated campaign for US market camera manual sales
- **Structure**: Performance Max with product feed from Merchant Centre
- **Pre-Crisis Performance**: Strong performer, consistent conversion rate ~3.61%
- **Crisis Performance**: Conversion rate dropped to 0.39% (Aug-Sept 2024)
- **Current Status**: Still struggling as of Oct 2024
- **Special Considerations**:
  - Relies on accurate conversion data for optimization
  - Lost impression share dramatically vs competitors during crisis
  - Top products from August had zero sales in September

### Campaign: US | CMN - Search
- **Purpose**: Search campaign for US market
- **Structure**: [TBD - keyword details not in emails]
- **Performance Notes**: Also affected by same crisis as PMax
- **Special Considerations**: Both Search and PMax failing indicates site/tracking issue, not campaign type issue

### Campaign: UK | CMN Search
- **Purpose**: Search campaign for UK market
- **Structure**: [TBD - keyword details not in emails]
- **Performance Notes**: STAR PERFORMER during crisis - doubled sales, +51% conversion rate (Sept 2024)
- **Current Status**: CPA £5.58-£5.75 consistently
- **Special Considerations**:
  - Proves the account fundamentals work when tracking is correct
  - Should be used as benchmark for what "healthy" performance looks like
  - Recovery from double-counting issues was quick and complete

### Campaign: UK | CMN - Performance Max
- **Purpose**: PMax for UK market
- **Performance Notes**: Also recovered well post-crisis, maintaining strong CPA
- **Special Considerations**: Similar strong recovery to UK Search campaign

---

## Action Items & Reminders

### Ongoing Tasks
- [ ] Monitor new pricing impact (launched Oct 21, 2025)
- [ ] Monitor Stripe integration performance (pending as of Oct 22, 2025)
- [ ] Weekly CPA monitoring - CRITICAL for business survival
- [ ] US conversion tracking verification - ensure US orders registering correctly
- [ ] Monthly review with Jeff - next critical checkpoint ~Nov 22, 2025

### Future Plans
- [ ] Full conversion tracking audit if issues persist
- [ ] Consider US campaign restructure if tracking can't be resolved
- [ ] Explore reducing US spend until tracking stabilizes
- [ ] Document baseline metrics post-pricing change and Stripe integration

### Important Dates
- **Oct 21, 2025**: New pricing launched
- **Oct 22, 2025**: Client ultimatum email - 1 month to show improvement
- **Nov 22, 2025 (approx)**: Decision deadline for client
- **July 4, 2024**: Conversion tracking change (historical reference)
- **Aug 19, 2024**: Performance cliff began (historical reference)

---

## Quick Reference

### Emergency Contacts
- **Client Primary**: Jeff Seymour - 07786 393088 - jeff@jeffseymour.co.uk
- **Account Manager**: Peter Empson - 07932 454652 - petere@roksys.co.uk

### Important Links
- **Google Ads Account**: [Account ID TBD]
- **Google Analytics**: [Property ID TBD]
- **Website**: [URL TBD - appears to be camera manual site]
- **Sister Business**: Print My PDF (printmypdf.com assumed)

### Login Credentials
[DO NOT store passwords - reference location if needed]
- **Location**: [e.g., "Stored in 1Password vault under OTC/Camera Manuals"]

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
| 2025-10-30 | Comprehensive population from 15 most recent emails and experiment log analysis | Claude |

---

## Ad Hoc Notes

### Recent Observations (Oct 2025)

**Positive Signals**:
- UK campaigns continue to perform exceptionally well (£5-6 CPA)
- Client has implemented llms.txt for AI discoverability
- New pricing and Stripe integration show client is actively improving business
- Site fundamentals appear sound (Peter tested multiple times, no issues found)

**Concerning Signals**:
- Client explicitly warned of "tough decisions in about a month" (Oct 22)
- CPA at £12 is unsustainable vs £18 average sale
- Performance described as "continuing to get worse this month"
- Pattern of worsening rather than improving post-crisis

**Questions to Investigate**:
1. Why did UK recover from double-counting crisis but US did not?
2. Is there a geo-redirect or payment gateway issue specific to US customers?
3. Are US conversions actually happening but not being tracked?
4. Has competitor activity stabilized or is it still increasing?
5. What is the true current conversion rate for US campaigns?

**Next Steps for Analysis**:
1. Pull actual Google Ads data for October 2025 to quantify current state
2. Compare US vs UK campaign settings side-by-side for discrepancies
3. Review Tag Manager implementation for any remaining currency-related code
4. Check Google Analytics to verify US traffic vs conversions vs Google Ads data
5. Consider A/B test: temporarily pause Enhanced Conversions to see if tracking improves
