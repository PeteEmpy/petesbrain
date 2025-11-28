# Positive Bakes - Context & Strategic Notes

> **Purpose**: Living document with important context for Google Ads analysis and reporting.
> **Last Updated**: 2025-11-24

**Voice Transcription Aliases**: PositiveBakes, Positive Bake, positive baiks, positive bakes cookies

---

## Account Overview

**Client Since**: [Date to be added]
**Monthly Budget**: [To be determined]
**Primary Contact**: Aatin Anadkat (Owner) - [Email to be added]
**Account Manager**: [Your name]

**Business Type**: E-commerce (Shopify)
**Industry**: Food & Beverage / Baked Goods
**Geographic Focus**: [To be determined]

**Platform IDs**:
- **Google Ads Customer ID**: 2401439541
- **Google Merchant Centre ID**: [TBD]
- **Google Analytics 4 (GA4) Property ID**: [TBD]
- **Microsoft Ads Account ID**: [TBD]
- **Facebook Ads Account ID**: [TBD]

---

## Strategic Context

### Current Strategy
- **Campaign Structure**: [To be established]
- **Bidding Strategy**: [To be determined]
- **Key Focus Areas**: [To be established]

### Why This Approach?
[To be documented as strategy develops]

### Goals & KPIs
**Primary Goal**: [To be determined - likely Revenue/ROAS]
**Target ROAS**: [To be determined]
**Target CPA**: [To be determined]
**Other KPIs**: [To be determined]

---

## Historical Performance Patterns

### Seasonality
- **Peak Seasons**: [To be documented]
- **Slow Seasons**: [To be documented]
- **Expected Patterns**: [To be documented]

### Year-Over-Year Trends
- [To be documented as data becomes available]

### Known Anomalies
[To be documented as they occur]

---

## Client Preferences & Communication

### Communication Style
- **Preferred Update Frequency**: [To be established]
- **Preferred Format**: [To be established]
- **Detail Level**: [To be established]

### Email Formatting Standards
**Default format for all client emails** (established Nov 2025):
- **Format**: HTML (not markdown) with proper `<strong>` tags for bold
- **Spelling**: British English for UK clients (analyse not analyze, customisation not customization, emphasise not emphasize)
- **Spacing**: Tight spacing for readability
  - `line-height: 1.4` (not 1.6+)
  - Paragraph margins: `6px` (not 10px+)
  - List margins: `6px` (not 10px+)
- **Font**: System fonts (`-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif`)
- **Delivery**: Save as `.html` file in client folder, auto-open in browser for copy/paste into Apple Mail
- **Purpose**: Ensures clean formatting when copying from browser to email client, avoids color scheme issues

### Decision-Making
- **Who Makes Final Decisions**: Aatin Anadkat (Owner)
- **Approval Process**: [To be established]
- **Risk Tolerance**: [To be established]

### Red Flags / Sensitive Topics
[To be documented as relationship develops]

---

## Business Context

### Product/Service Details

**Top Performers**: [To be documented]
- [Product categories/items that drive most revenue]

**Problem Products**: [To be documented]
- [Products that don't convert well]

**Pricing Strategy**: [To be documented]
**Average Order Value**: [To be determined]
**Typical Margins**: [To be determined]

### Website & Technical

**Website Platform**: Shopify (migrated from BigCommerce in 2025)
**Feed Management**: Channable
**Known Technical Issues**:
- **Product ID Discontinuity** (Nov 2025): Product IDs changed during BigCommerce → Shopify migration
  - See "Current Issues" section for full details and solutions

**Conversion Tracking**:
- **Setup**: [To be verified]
- **Known Issues**: [To be documented]
- **Last Audit**: [To be scheduled]

### Competitive Landscape

**Main Competitors**: [To be identified]
- [Competitor analysis to be documented]

**Competitive Advantages**: [To be documented]
**Competitive Disadvantages**: [To be documented]

---

## Known Issues & Challenges

### Current Issues

**✅ RESOLVED: Platform Migration Product ID Issue** (Discovered 2025-11-07, Resolved 2025-11-11)
- **Problem**: Migrated from BigCommerce to Shopify without maintaining original product IDs
- **Impact**:
  - All products now appear as "new" in Google Merchant Center
  - Lost all historical product performance data
  - Performance Max campaigns lost product-level optimization learning
  - Shopping campaign product groups may be broken
  - Channable rules based on old IDs no longer work
- **Root Cause**: BigCommerce and Shopify use different product ID formats
  - BigCommerce: Simple numeric IDs (e.g., "12345")
  - Shopify: Platform-specific format (e.g., "shopify_GB_67890_45678")
- **✅ Solution Implemented**: Merchant Centre now using main new SKUs
- **Status**: ✅ COMPLETED (Nov 11, 2025)
  - No issues with Merchant Centre regarding ID migration
  - Some products initially came over with old IDs, but migration now fully completed
  - Account is up and running successfully

### Recent Updates & Progress

**✅ Merchant Center & Stock Level Issues - RESOLVED** (Nov 11, 2025)
- ✅ **ID Migration Complete**: Merchant Centre using main new SKUs, migration fully completed
- ✅ **Stock Levels**: No current stock level issues with Supabase
- ✅ **Account Settings**: Current settings accommodating stock levels properly
- 📊 **Previous Update** (Nov 10, 2025): Friday performance looking very positive
- 💬 **Client Response**: Aatin pleased with resolution progress
- 🛠️ **Client Actions in Progress**:
  - Implementing new cart flows in Klaviyo
  - Merchandising Christmas collections to improve shopability
  - Working on conversion optimization

### Recurring Challenges
[To be documented as patterns emerge]

### External Factors to Monitor
- Christmas/holiday season performance (Q4 2025)
- Klaviyo cart flow implementation impact on conversion rates

---

## Key Learnings & Insights

### What Works Well
- [To be documented as campaigns develop]

### What Doesn't Work
- [To be documented as tests are run]

### Successful Tests & Experiments
| Date | Test Description | Result | Action Taken |
|------|-----------------|--------|--------------|
| [To be documented] | | | |

### Failed Tests (Learn From)
| Date | Test Description | Why It Failed | Lesson Learned |
|------|-----------------|---------------|----------------|
| [To be documented] | | | |

---

## Campaign-Specific Notes

### Performance Max Campaign
- **Purpose**: Main acquisition campaign for e-commerce conversions
- **Current Bid Strategy**: Target ROAS 120% (changed from Max Conversions on 2025-11-20)
- **Performance Notes**:
  - Converting but with poor order values (pre-Nov 20)
  - Bid strategy changed to optimize for higher-value orders
  - Review scheduled: Nov 27, 2025
- **Special Considerations**:
  - Change made just before Black Friday (Nov 29)
  - Results will be mixed with holiday shopping patterns
  - Need to separate baseline performance from seasonal effects

[Additional campaigns to be documented as they're created]

---

## Action Items & Reminders

### Ongoing Tasks
- [ ] Set up Google Ads account structure
- [ ] Verify conversion tracking setup
- [ ] Establish baseline performance metrics
- [ ] Create initial campaign strategy
- [ ] Get Google Ads customer ID and add to all config files
- [ ] Find Merchant Center ID (if Shopping/PMax campaigns exist)
- [ ] Create Product Performance Spreadsheet (if e-commerce with product feeds)
- [ ] Share spreadsheet with service account: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`

### Future Plans
- [ ] [Planned test/experiment]
- [ ] [Strategic initiative to implement]

### Important Dates
- [Date]: [Event/deadline]

---

## Quick Reference

### Emergency Contacts
- **Client Primary**: Aatin Anadkat - [Phone] - [Email]
- **Client Technical**: [To be added]
- **Agency Contact**: [To be added]

### Important Links
- **Google Ads Account**: [Account ID to be added]
- **Google Analytics**: [Property ID to be added]
- **Client Dashboard**: [URL if applicable]
- **Website**: [Shopify store URL to be added]
- **Admin Access**: [URL if needed]

### Login Credentials
- **Location**: [e.g., "Stored in 1Password vault under Positive Bakes"]

---

## Document History

| Date | Change Made | Updated By |
|------|-------------|------------|
| 2025-11-10 | Added Recent Updates section documenting positive Merchant Center resolution progress, Friday performance improvements, and Aatin's Klaviyo cart flow/Christmas merchandising initiatives. Updated External Factors to monitor holiday season and Klaviyo impact. | Claude Code |
| 2025-01-27 | Initial creation | System |


## Planned Work

### [Positive Bakes] Schedule initial campaign strategy meeting with Aatin Anadkat
<!-- task_id: UTZvelhCQnNwcW5sQW03RA -->
**Status:** 📋 In Progress  
| 2025-11-13 | **TASK DEDUPLICATION**: Removed 14 duplicate AI-generated task entries. Preserved all manual tasks and first occurrence of each AI task pattern. Cleanup based on provenance analysis showing 'Source: AI Generated' metadata. | Claude Code |

---
**Source:** AI Generated (2025-11-11 09:30)
**Client:** positive-bakes
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Establish key performance goals, budget, and initial campaign approach for new Google Ads account
**AI Task ID:** cd90a733-1e2e-42d7-976f-5494dbe0a3ee
---

Establish key performance goals, budget, and initial campaign approach for new Google Ads account



### [Positive Bakes] Review Channable feed settings and product ID mapping
<!-- task_id: Nk9aTmpyaHhQM25NQzhYZA -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 09:29)
**Client:** positive-bakes
**Priority:** P1
**Time Estimate:** 30 mins
**Reason:** Cross-check feed configuration to resolve potential product listing issues from BigCommerce to Shopify transition
**AI Task ID:** cdc5fb65-6c86-4714-a28e-aab331ea0678
---

Cross-check feed configuration to resolve potential product listing issues from BigCommerce to Shopify transition



### [Positive Bakes] Verify Merchant Centre product feed configuration after Shopify migration
<!-- task_id: SzZLLW81X215ZDFNeERUXw -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 09:29)
**Client:** positive-bakes
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Ensure product listings are correctly mapped and available for free listings following recent platform migration
**AI Task ID:** 5852fafb-5b75-4e48-be9d-a0072078201e
---

Ensure product listings are correctly mapped and available for free listings following recent platform migration



### [Positive Bakes] Verify Merchant Centre product feed configuration
<!-- task_id: Z3pNZ2cyQ3VlWE5HSkxLMQ -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 10:29)
**Client:** positive-bakes
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Ensure product listings are correctly mapped and available for free listings following recent platform migration
**AI Task ID:** a82ee2a6-3aee-4a8b-b68c-1d369c4e5d69
---

Ensure product listings are correctly mapped and available for free listings following recent platform migration



### [Positive Bakes] Verify Merchant Centre product feed configuration
<!-- task_id: TXNZbGJKTEZtcDVZeWk4Rg -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 10:26)
**Client:** positive-bakes
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Ensure product listings are correctly mapped and available for free listings following recent platform migration
**AI Task ID:** 6021c497-03e4-4252-a063-f55112bce4ed
---

Ensure product listings are correctly mapped and available for free listings following recent platform migration



---

**Cleanup Note (2025-11-13):**
Removed 14 duplicate task entries:
- 6x: Schedule initial campaign strategy meeting with Aatin Anadka
- 5x: Review Channable feed settings and product ID mapping
- 3x: Verify Merchant Centre product feed configuration after Shop

All manual tasks preserved. AI-generated tasks deduplicated to first occurrence only.

### Investigate Merchant Centre Product Listing Availability
<!-- task_id: Y0RFb0xxWkJYczJWbDVnRA -->
**Status:** 📋 In Progress  

Client: positive-bakes

Troubleshoot why products are not available for free listings in Google Merchant Centre:
1. Review Product Impact Analyser for specific flagging reasons
2. Cross-reference with recent BigCommerce to Shopify migration
3. Check product ID mapping and feed configuration
4. Verify Channable feed settings
5. Document findings and potential resolution steps


### [Positive Bakes] Verify Merchant Centre product feed configuration
<!-- task_id: Z3pNZ2cyQ3VlWE5HSkxLMQ -->
**Status:** 📋 In Progress  

---
**Source:** AI Generated (2025-11-11 10:29)
**Client:** positive-bakes
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Ensure product listings are correctly mapped and available for free listings following recent platform migration
**AI Task ID:** a82ee2a6-3aee-4a8b-b68c-1d369c4e5d69
---

Ensure product listings are correctly mapped and available for free listings following recent platform migration

