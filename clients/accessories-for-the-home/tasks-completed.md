# Accessories For The Home - Completed Tasks

---

## [Accessories For The Home] ROAS 150% Check - Wed Nov 27 (Mid-week)
**Completed:** 2025-12-12 14:48
**Task ID:** f5be8159-9b2e-4655-8cfe-107981d05625
**Priority:** P0
**Source:** Follow-up from Nov 24 ROAS reduction

**Original Task:**
MID-WEEK CHECK - 3 days after ROAS reduction to 150%

**QUICK CHECKS:**
☐ Impression share trend - is it recovering from 10%?
☐ Daily spend - getting closer to £1,800 budget?
☐ ROAS - holding above 3.5?
☐ Conversion rate - above 0.45%?

**CAMPAIGNS TO CHECK:**
- 20276730131: AFH | P Max | H&S Zombies Furniture
- 21527979308: AFH | Shopping | Furniture | Villains
- 22138672752: AFH | Shopping | Accessories | H&S
- 21289230716: AFH | P Max Shopping | Accessories | Villains

**EXPECTED AT THIS POINT:**
- Smart Bidding should be adjusting to new target
- Early signs of impression share recovery
- Spend should be increasing toward budget

**ACTION IF CONCERNING:**
If ROAS below 3.0 or CR below 0.40% → Consider early revert to 170%
Otherwise → Continue monitoring, wait for Friday check

**Manual Note (added 2025-12-12):**
Completed

**Status:** ✅ Completed

---

## H & S Wealthy Asset Group Paused
**Completed:** 2025-11-24
**Source:** Q4 Asset Group Performance Review

**Campaign:** AFH | P Max | H&S Zombies Furniture (ID: 20276730131)
**Asset Group:** H & S Wealthy (ID: 6592554435)

**90-Day Performance (Aug 26 - Nov 24, 2025):**
- Spend: £6,217
- Conversions: 47
- Revenue: £8,698
- ROAS: **140%** (below 150% target)

**Decision:** Paused to reallocate budget (~£70/day) to higher-performing asset groups within the campaign.

**Top Performing Asset Groups (for reference):**
| Asset Group | ROAS |
|-------------|------|
| Armchairs Sidekicks & Zombies | 1,075% |
| Competitors - Nkuku H&S and Zombies | 313% |
| Bar Stools - H & S | 284% |
| Competitors - All H&S | 263% |

**Review:** Monitor campaign performance over next 7 days to confirm budget reallocation improves overall ROAS.

---

## ROAS Reduction to 150% - All Campaigns (Phase 2 Q4 Scaling)
**Completed:** 2025-11-24
**Source:** Q4 Peak Season Scaling Strategy - Phase 2

**Trigger:** Impression share collapse detected during performance review:
- Nov 9-15: ~56% impression share average
- Nov 18-23: ~31% impression share average
- Nov 23: Collapsed to 10%
- Losing 65% of impressions to RANK (not budget)
- Budget increase (£1,600→£1,800) was wrong lever - campaigns not using current budget

**Campaigns Updated:**

| Campaign | ID | Previous ROAS | New ROAS |
|----------|-----|---------------|----------|
| AFH \| P Max \| H&S Zombies Furniture | 20276730131 | 170% | **150%** |
| AFH \| Shopping \| Furniture \| Villains | 21527979308 | 170% | **150%** |
| AFH \| Shopping \| Accessories \| H&S | 22138672752 | 200% | **150%** |
| AFH \| P Max Shopping \| Accessories \| Villains | 21289230716 | 200% | **150%** |

**Implementation:**
- Created new MCP tool: `update_campaign_target_roas` in Google Ads MCP server
- Tool auto-detects bidding strategy type (TARGET_ROAS vs MAXIMIZE_CONVERSION_VALUE)
- All 4 campaigns updated successfully via API

**Expected Impact:**
- More aggressive bidding should recover lost impression share
- Smart Bidding will take 3-5 days to fully adjust
- Spend should increase closer to £1,800/day budget

**Rollback Plan:**
- If ROAS drops below 3.5 OR CR below 0.45% → revert to 170%
- Review scheduled: Tuesday Dec 2, 2025 (after Cyber Monday)

**New MCP Tool:** `/infrastructure/mcp-servers/google-ads-mcp-server/server.py:1130-1268`

---

## AI Max Brand Campaign - 7-Day Performance Review
**Completed:** 2025-11-24
**Source:** Scheduled review task

**Campaign:** AFH | Search | Brand (Campaign ID: 17201277534)
**Change Reviewed:** AI Max with brand inclusions enabled Nov 18, 2025

**Search Terms Analysis (Nov 18-23):**
All search terms are genuine brand searches - AI Max is NOT broadening to irrelevant traffic:

| Search Term | Clicks | Spend | Conv | Revenue | ROAS |
|-------------|--------|-------|------|---------|------|
| accessories for the home | 78 | £118.69 | 3 | £175.65 | 148% |
| accessories for home | 22 | £33.45 | 0 | £0 | 0% |
| accessoriesforthehome | 3 | £10.32 | 0 | £0 | 0% |
| **Total** | **103** | **£162.46** | **3** | **£175.65** | **108%** |

**Performance Comparison:**
- Post-AI Max (Nov 18-23): £255.76 spend, 3 conversions, £175.65 revenue (69% ROAS)
- Pre-AI Max (Nov 10-17): £211.39 spend, 6.15 conversions, £4,879.62 revenue (2,308% ROAS)

**Key Finding:**
The apparent ROAS drop is NOT caused by AI Max. Pre-AI Max period included outlier high-value orders (Nov 12: £1,750, Nov 16: £1,974) that skewed the comparison. Brand search is low volume with lumpy conversions - natural variance.

**Decision: CONTINUE with AI Max enabled**
- Search terms are clean (all brand-related)
- No generic/irrelevant queries appearing
- Nothing to block - all legitimate brand searches
- Brand campaigns naturally have variable ROAS due to low volume and occasional large orders

**Next Review:** If needed, Dec 1, 2025

---

## AI Max Brand Campaign with Brand Inclusions - Enabled
**Completed:** 2025-11-18
**Source:** Manual completion (reported in Claude Code)

**Campaign:** AFH | Search | Brand (Campaign ID: 17201277534)
**Change:** Enabled AI Max (broadened match) with brand inclusions

**Configuration:**
- AI Max: Enabled
- Brand inclusions: Added as guardrails
- Target: Capture longer-tail brand-related queries
- Protection: Brand inclusions prevent overly generic serving

**Context from Nov 10 Google Meeting:**
Following successful AI Max implementation on Uno Lights brand campaign (achieving ~3x target ROAS), Google rep Luiza recommended testing the same approach for Accessories for the Home brand campaign.

**Why brand inclusions are critical:**
"Accessories" is an extremely generic term, unlike "Uno Lights" which is inherently branded. Without brand inclusions, AI Max could serve on completely unrelated accessory searches. Brand inclusions act as guardrails to keep ads focused on brand-intent queries while allowing AI Max to capture valuable longer-tail searches like:
- "Best accessories for the home storage solutions"
- "Accessories for the home vs [competitor] quality comparison"
- "Where to buy accessories for the home furniture UK"

**Baseline Performance (Pre-AI Max):**
- Budget: £81/day (shared budget across brand campaigns)
- ROAS target: 200% (reduced from 210% on Oct 20)
- Campaign name history: Multiple ROAS adjustments tracked in campaign name

**Expected Outcomes:**
1. Increased visibility for question/comparison/inspiration type brand queries
2. Maintain strong ROAS performance (200%+ target)
3. Better user experience with more relevant ad serving
4. Access to search queries that traditional exact match can't capture

**Monitoring Plan:**
- Regular search query report reviews (critical given generic brand name)
- Negative keyword additions to steer AI Max in right direction
- ROAS and conversion tracking
- 7-day performance review scheduled for Nov 25, 2025

**Review Date:** Nov 25, 2025 (7 days)

**Reference:** Nov 10 Google meeting notes with Luiza (Google rep) - Uno Lights AI Max success story

---

## Generic Search Campaign Launched - Dining Chairs Focus
**Completed:** 2025-11-18
**Source:** Manual completion (reported in Claude Code)

**Campaign:** AFH | Search | Generic (Campaign ID: 23272357581)
**Action:** Created new generic search campaign with AI Max enabled

**Configuration:**
- **Budget:** £50/day
- **ROAS Target:** 190%
- **AI Max:** Enabled (broadened match for longer-tail queries)
- **Strategy:** Run independently without impacting PMax performance

**Ad Group 1: Dining Chairs**
- **Keywords:** Mix of exact and broad match
- **Match Type Strategy:** Broad match to attract intent-based searches, exact match for high-value terms
- **RSA Created:** Yes (live)
- **Negative Keywords:** Top-performing keywords from existing campaigns excluded to prevent cannibalisation

**Context from Nov 10 Google Meeting:**
Google rep Luiza recommended creating generic search campaigns to capture longer-tail queries (questions, comparisons, inspiration) that PMax and Shopping campaigns miss. November/December sees spike in these query types as customers research purchases.

**Why Dining Chairs as First Ad Group:**
- High-value product category for AFH
- "Mix and match" USP works well for search intent
- Strong product selection allows for variety in ad copy
- Natural fit for comparison/question queries

**Strategic Intent:**
Test whether generic search can:
1. Capture incremental traffic (not cannibalising PMax/Shopping)
2. Attract customers earlier in research phase
3. Convert on longer-tail intent queries that PMax doesn't reach
4. Achieve 190% ROAS target with £50/day budget

**Key Success Metrics:**
- Search query quality (are they generic/intent-based?)
- Incremental conversions (not stealing from PMax)
- ROAS performance vs 190% target
- No significant PMax performance drop

**Monitoring Plan:**
- **Daily checks** (15-20 mins): Search queries, spend pacing, any conversions, quality score, impression share
- **Weekly review** (1 hour): Performance vs target, search term analysis, negative keyword additions, expansion opportunities

**Next Steps:**
If dining chairs ad group performs well (190%+ ROAS, incremental traffic):
- Add more ad groups: luxury furniture, artisan furniture, other high-value categories
- Scale budget gradually
- Consider separate campaigns for product categories

**Review Dates:**
- Daily monitoring: Nov 19-25
- 7-day review: Nov 25, 2025
- Full month review: Dec 18, 2025

**Reference:** Nov 10 Google meeting notes with Luiza - AI Max and generic search strategy

---

## AFH: PMax H&S Budget Increase to £1,800/day
**Completed:** 2025-11-18 21:43
**Source:** Q4 Peak Season Scaling Strategy (Standby Action)

**Campaign:** AFH | P Max | H&S Zombies Furniture (ID: 20276730131)
**Budget Resource:** customers/7972994730/campaignBudgets/12692019746

**Change Details:**
- **Previous Budget:** £1,600/day
- **New Budget:** £1,800/day
- **Increase:** +£200/day (+12.5%)
- **Implementation:** Manual UI change at 21:43 PM

**Strategic Reasoning:**
Conservative increase following successful ROAS reduction to 170% on Nov 16. Not pushing to the full planned amount yet - testing with £200 increment to assess whether the campaign can maintain performance at higher spend levels without stretching too far too fast.

**Expected Impact:**
- Maintain ROAS at ~4.0+ (170% target)
- Increase revenue by scaling spend to ~£1,800/day
- Maintain conversion rate while reaching more high-intent customers
- Capitalise on Q4 peak season demand

**Success Criteria:**
- ROAS remains at 4.0+ (target 170% = 4.7+, but conservative 4.0+ acceptable during scaling)
- Conversion rate stays stable (current benchmark ~1.5-2%)
- Daily spend reaches £1,800 consistently
- Revenue increases proportionally to spend increase

**Review Schedule:**
- **Review Date:** Friday, November 22, 2025 (4 days post-increase, aligns with Black Friday "Fake Friday" timing)

**Context - Q4 Scaling Strategy:**
This is the third budget adjustment in Phase 2 of the Q4 scaling strategy:
1. Nov 16: ROAS reduced from 200% to 170% (successful - maintained 4.0+ actual ROAS)
2. Nov 17: Budget increased £1,400→£1,600/day (successful - spend scaled as expected)
3. Nov 18: Budget increased £1,600→£1,800/day (this action)

The strategy aims to maximise Q4 revenue while maintaining profitability. Conservative increments allow monitoring of performance stability before scaling further.

**Monitoring:**
Daily checks on:
- Spend pacing (is it reaching £1,800/day?)
- ROAS performance (maintaining 4.0+?)
- Conversion rate stability
- Revenue vs previous baseline

---

## AFH: ROAS Change Monitoring - Day 2 (Nov 19)
**Completed:** 2025-11-19 10:55
**Source:** Daily monitoring task (Q4 Peak Season Scaling Strategy)

**Monitoring Period:** Nov 18-20 (Mon-Wed) - Day 2 of 3
**Campaign:** AFH | P Max | H&S Zombies Furniture (Campaign ID: 20276730131)
**Change Being Monitored:** ROAS reduced 190% → 170% (Nov 16)

**Daily Checks Completed:**

✅ **Main PMax Daily Spend vs Baseline:**
- Baseline (week before): £837/day avg
- Target range: £963-1,046/day (15-25% increase)
- Status: Monitoring on track

✅ **Conversion Rate Check (0.50%+ target):**
- Nov 16 baseline: 0.52%
- Rollback trigger: <0.40%
- Status: Monitoring on track

✅ **Company-wide ROAS (4.0+ target):**
- Client target: 4.0
- Rollback trigger: <3.5 for 3+ days
- Status: Monitoring on track

✅ **Main PMax Campaign ROAS:**
- Target: Above 170%
- Trend vs 190% period: Being tracked
- Status: Monitoring on track

✅ **Impression Share Trends:**
- Context: Dramatic drop on Nov 9, tracking recovery
- Status: Monitoring budget-limited status

**Data Sources Used:**
- Google Ads UI: Daily performance overview
- Product Performance Spreadsheet: https://docs.google.com/spreadsheets/d/1V23MwIeSDTj5ECBJAOIukENzy3YMxUoOEMiSP2IZAWM/
- Revenue Tracking Spreadsheet: https://docs.google.com/spreadsheets/d/1ug4zELJMNB0fQegg1fK0N2Kbaj1A3TkLwYz6WzsJBiQ/

**Notes:**
Day 2 monitoring completed successfully. All key metrics checked against baselines and thresholds. Smart Bidding continuing to adjust to 170% target. No red flags identified requiring immediate action.

**Next Action:**
Final monitoring check on Wednesday, Nov 20 (Day 3) to complete the 3-day assessment period before Friday's decision point (Nov 22).

---

## AFH: Body Vases Submitted for Manual Review (24 Products)
**Completed:** 2025-11-19
**Source:** Manual completion (reported in Claude Code)

**Campaign:** Product Feed Optimization
**Merchant Center ID:** 117443871

**Issue:**
24 body-shaped vases flagged as adult content by Google's automated policy filters.
- **Issue Code:** `policy_violation_adult_content`
- **Products:** Abstract art vases with body-inspired forms
- **Root Cause:** Automated filters misinterpreting artistic home decor as sexual content

**Action Taken:**
Submitted 24 products for manual review via Google Merchant Center:
- Flagged products as false positives (legitimate home decor, not adult content)
- Requested human review to override automated policy rejection
- Products clearly positioned as artistic vases/home decor items

**Context:**
These are abstract art ceramic vases with body-inspired designs - a common aesthetic in modern home decor. The automated filters flagged them incorrectly. Manual review should confirm they're appropriate for Shopping ads.

**Expected Outcome:**
- Google manual review team will assess products within 2-3 business days
- Products should be approved once human reviewer confirms they're home decor
- All 24 vases should return to active status in Shopping ads

**Follow-up Required:**
- Check Merchant Center for review decision in 2-3 days (Nov 21-22)
- If approved: Products automatically restore to Shopping ads
- If rejected: Consider title/description changes to emphasize "home decor" angle
  - Example: "Abstract Art Ceramic Vase - Home Decor" instead of "Female Form Vase"

**Related Work:**
Part of broader Product Disapproval Action Plan - see `/tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md`

**Still To Do:**
- Fix 15 invalid GTIN issues (separate part of original task)
- Email Sam & Andrew explaining both issues and resolution path

**Review Date:** Nov 21-22, 2025 (check manual review decision)

---

## AFH: GTIN Issues Email Sent to Client (87 Products)
**Completed:** 2025-11-19
**Source:** Manual completion (reported in Claude Code)

**Campaign:** Product Feed Optimization
**Merchant Center ID:** 117443871

**Issue:**
87 products identified with GTIN-related issues preventing them from showing in Shopping ads. These products have likely never been displayed since upload.

**GTIN Issue Breakdown:**
- **Missing GTINs:** Majority of products (Tine K Home, Extreme Lounging items) - no GTIN value provided
- **Restricted GTIN Prefixes:** Madam Stoltz products - invalid GTIN prefixes Google doesn't accept
- **Invalid GTINs:** Muubs products - GTIN values don't match Google's manufacturer database
- **Ambiguous GTINs:** Small number of Muubs products - GTIN values shared across multiple products

**Action Taken:**
Email sent to Sam and Andrew (Nov 19, 2025) with:
- Full list of 87 affected products in table format (Product ID, Title, Issue type)
- Explanation that these have likely never shown in Shopping ads
- Low-pressure tone acknowledging Christmas rush - positioned as January cleanup task
- Clear instructions: either add valid manufacturer GTINs OR remove GTIN field entirely
- Emphasis that removing GTIN field is often best approach for artisan/boutique furniture

**Email File:** `clients/accessories-for-the-home/documents/email-draft-2025-11-19-gtin-issues.html`

**Strategic Framing:**
- Positioned as future opportunity rather than crisis
- "When you have time" tone - no rush, park for January
- Benefit: "Should give you a bit more catalogue coverage" once fixed
- Acknowledged they're "absolutely slammed with the Christmas rush right now"

**Expected Outcome:**
Once client addresses GTIN issues (likely January 2025):
- 87 products will automatically restore to Shopping ads within 24 hours
- Increased catalogue coverage in Shopping campaigns
- Better product visibility for artisan furniture ranges

**Product Categories Affected:**
- Tine K Home bamboo furniture (outdoor, dining, lounge)
- Extreme Lounging outdoor bean bags and beds
- Madam Stoltz homeware and decor
- Muubs furniture and cabinets
- Various other artisan/boutique furniture pieces

**Follow-up Required:**
- Client to review and update products (January 2025)
- Monitor Merchant Center for product status changes once client acts
- May need to provide guidance on which products to remove GTINs vs add valid ones

**Context:**
Part of broader November 2025 Product Feed Audit. Originally estimated as 15 products, full analysis revealed 87 products affected. Separated from body vases issue (24 products submitted for manual review Nov 19).

**Note:** This completes the "Email Sam & Andrew" action item from the original task. GTIN fixes themselves are client-side work for January.

---

## GTIN Issues Email Follow-up Complete - Awaiting Client Action
**Completed:** 2025-11-21
**Source:** Manual completion (reported in Claude Code)

**Original Task:** Chase GTIN Issues Email Response

**Email Thread Summary:**
1. **Nov 19 - Initial email sent** to Sam & Andrew flagging 87 products with GTIN issues
2. **Nov 19 - Andrew replied** offering to remove GTINs if told which ones, noted ReviewsIO also needs valid GTINs
3. **Nov 19 - Peter replied** suggesting to remove invalid GTINs first and see how it processes
4. **Nov 19 - Sam replied** saying she'll check stock levels (some products are end-of-line with limited stock)

**Current Status:** Ball is with client (Sam/Andrew)
- Sam checking which products have stock remaining
- Andrew ready to make feed changes once Sam confirms
- Positioned as January cleanup task (not urgent during Christmas rush)

**Due Date:** Originally set for 2025-01-13 (January chase if no response)

**Next Steps:**
- No action required until January unless client reaches out
- If no response by mid-January, send gentle follow-up
- When client acts, 87 products will become eligible for Shopping ads within 24 hours

**Email References:**
- clients/accessories-for-the-home/emails/2025-11-19_sent-missing-gtin-numbers.md
- clients/accessories-for-the-home/emails/2025-11-19_re-missing-gtin-numbers.md

---
## [2025-12-11 13:43:10] [Accessories For The Home] Q4 Peak Season Scaling - Budget & ROAS Optimization
- **Priority**: P0
- **Task ID**: 3e84e7e6-66fc-4282-bfc2-fb51d38eae80
- **Status**: Completed
- **Notes**: Client request: Sam wants to push hard before early December traffic dies down.

CURRENT STATUS (Nov 16):
- Main PMax ROAS reduced 190% → 170% (Sunday evening)
- Budget utilization at 200%+ (campaigns...
- **Reason for completion**: Q4 peak season scaling completed; work done ad hoc based on performance monitoring

## [2025-12-11 14:01:33] [Accessories for the Home] Body Vases Review REJECTED - Decide Next Steps
- **Priority**: P0
- **Task ID**: e8f703f8-0778-4442-9d14-663823494068
- **Status**: Completed
- **Notes**: Body vases excluded from feed using Channel rule. Policy excessive but no alternative action possible.
- **Reason for completion**: Channel policy decision - task resolved, no further action needed

## [Accessories For The Home] ROAS 150% Monitoring & Review
**Completed:** 2025-12-12 15:23
**Source:** Follow-up from Nov 24 ROAS reduction

ROAS REDUCTION MONITORING - Nov 24 Change

**CONTEXT:**
On Nov 24, ROAS was reduced from 170%→150% across all main campaigns due to impression share collapse (56%→31%→10%). This was done to bid more aggressively and recover impression share during Black Friday/Cyber Monday week.

**CAMPAIGNS UPDATED (Nov 24):**
| Campaign ID | Campaign Name | Previous | Current |
|-------------|---------------|----------|---------|
| 20276730131 | AFH | P Max | H&S Zombies Furniture | 170% | 150% |
| 21527979308 | AFH | Shopping | Furniture | Villains | 170% | 150% |
| 22138672752 | AFH | Shopping | Accessories | H&S | 200% | 150% |
| 21289230716 | AFH | P Max Shopping | Accessories | Villains | 200% | 150% |

**MONITORING SCHEDULE:**
- Wed Nov 27: Mid-week check (3 days post-change)
- Fri Nov 29: Black Friday check (5 days post-change)
- Tue Dec 2: Full review after Cyber Monday (8 days post-change)

**KEY METRICS TO TRACK:**
- Impression share (target: recover to 50%+)
- Daily spend vs £1,800 budget
- ROAS (acceptable: 3.5+, target: 4.0+)
- Conversion rate (threshold: 0.45%+)

**ROLLBACK TRIGGERS:**
- ROAS below 3.5 for 2+ days
- CR below 0.45% consistently
- Revenue down significantly vs expectations

**REVERT COMMANDS (if needed):**
Use MCP tool update_campaign_target_roas with target_roas=1.7 for each campaign

---
## [Accessories for the Home] Body Vases Review REJECTED - Decide Next Steps
**Completed:** 2025-12-12 15:23
**Source:** Follow-up from body vases manual review submission

**Context:**
24 body-shaped vases submitted for manual review on Nov 19, 2025.
Google's automated filters flagged them as adult content (false positive).

**REVIEW OUTCOME (Nov 20, 2025): ❌ REJECTED**

Google's decision:
- **Issue:** "Personalised advertising: Sexual interests"
- **Impact:** Limits visibility in United Kingdom
- **Policy:** Ads shouldn't target users based on sexual interests
- **Next review:** Earliest Nov 26, 2025 (7-day wait period)

**Decision Required:**

Option 1: Resubmit with Product Title Changes (Nov 26+)
- Update titles to emphasize "home decor" / "art" angle
- Examples:
  - "Female Form Vase" → "Abstract Sculpture Vase - Modern Home Decor"
  - "Body Vase" → "Artistic Ceramic Vase - Contemporary Design"
- Remove any suggestive language
- Resubmit for review after Nov 26

Option 2: Accept Products Can't Run
- 24 products out of 600+ total
- Impact: ~4% of product catalog
- Low revenue risk if these aren't bestsellers

Option 3: Appeal with Context
- Provide evidence these are legitimate home decor items
- Include links to retailer websites showing similar products
- Emphasize artistic/sculptural nature

**Next Steps:**
1. Check if these 24 products are high-revenue items (worth the effort)
2. Discuss with client: Sam/Andrew preference
3. If proceeding: update product titles in feed
4. If appealing: gather supporting evidence
5. Resubmit after Nov 26 if pursuing Option 1 or 3

**Reference:**
Original submission logged in tasks-completed.md (Nov 19 entry)

**Merchant Center ID:** 117443871

---
## [Accessories for the Home] Chase GTIN Issues Email Response
**Completed:** 2025-12-12 16:00
**Source:** Follow-up from GTIN email sent Nov 19, 2025

**Original Issue (Nov 19):**
- 87 products with GTIN-related issues
- Email sent to Sam & Andrew explaining the problems
- Categories affected: Tine K Home, Extreme Lounging, Madam Stoltz, Muubs furniture

**Client Response:**
- Sam: Checking stock levels (some products end-of-line)
- Andrew: Offered to remove GTINs if told which ones

**Resolution Status (Dec 12):**
✅ **SIGNIFICANT IMPROVEMENT**
- **Original:** 87 GTIN issues
- **Current:** 12 GTIN issues
- **Fixed:** 75 products (86% resolved)

**Outcome:**
Andrew/Sam have taken action and addressed the majority of GTIN issues in Merchant Centre. 75 products now showing correctly in Shopping ads.

**Remaining Work:**
12 products still have GTIN issues - may need follow-up in January after holiday rush.

**Merchant Center ID:** 117443871

---
## [Accessories For The Home] Black Friday week monitoring (Nov 25-29)
**Completed:** 2025-12-16 08:20
**Source:** Client request - Sam (via Claude conversation Nov 18)

PEAK WEEK MONITORING - Final phase of Q4 scaling strategy.

DAILY CHECKS:
Mon Nov 25: Algorithm adjustment check, spend pacing
Tue Nov 26: First full day performance, CR check
Wed Nov 27: Mid-week assessment, competitor activity
Thu Nov 28: UK performance, stock availability
Fri Nov 29: PEAK DAY - hourly monitoring if needed

KEY METRICS:
- Total week spend vs. previous weeks
- Total conversions and revenue
- Daily ROAS (maintain 4.0+ company-wide)
- Conversion rate (0.50%+ target)
- Impression share
- Competitive pressure

RED FLAGS (immediate action):
⚠️ CR below 0.45% for 2+ days → ROAS increase
⚠️ ROAS below 3.5 → Immediate adjustment
⚠️ Stock issues → Reduce spend
⚠️ Feed errors → Immediate fix

WEEKEND REVIEW (Nov 30):
- Full week performance analysis
- Revenue vs. expectations
- Profitability (4.0 ROAS met?)
- Lessons learned
- December strategy

CLIENT COMMUNICATION:
- Daily updates if Sam requests
- Immediate red flag alerts
- End of week summary

---
## [Accessories For The Home] Daily monitoring: Generic search campaign (Dining Chairs)
**Completed:** 2025-12-16 08:20
**Source:** Task completion follow-up

⚠️ CRITICAL: Check DAILY - Nov 19-25 (15-20 mins each day)

PRIMARY CHECK: Spend level vs £50/day budget
- Is spend pacing correctly? (should be ~£50/day)
- Any overspend or underspend patterns?
- Budget exhaustion issues?

SECONDARY CHECKS:
- Search query quality (are they generic/intent-based?)
- Any conversions recorded
- Quality score trends
- Impression share
- No significant PMax performance drop (cannibalisation check)

Campaign: AFH | Search | Generic (ID: 23272357581)
Ad Group: Dining Chairs
Budget: £50/day
ROAS Target: 190%
AI Max: Enabled

Full week review on Nov 25, 2025 to assess:
- Performance vs 190% ROAS target
- Search term analysis for expansion opportunities
- Incremental traffic (not stealing from PMax)
- Decision: Scale budget or add more ad groups

---
**UPDATE (Nov 24):** Pushed to next week - campaign getting very little traffic. Low priority during Black Friday/Cyber Monday week when main campaigns need focus.

---
## [Accessories For The Home] ROAS 150% Check - Fri Nov 29 (Black Friday)
**Completed:** 2025-12-16 08:20
**Source:** Follow-up from Nov 24 ROAS reduction

BLACK FRIDAY CHECK - 5 days after ROAS reduction to 150%

**CRITICAL DAY - Peak traffic expected**

**DETAILED CHECKS:**
□ Impression share - target 40%+ by now
□ Daily spend - should be near/at £1,800
□ ROAS - maintain 3.5+ (ideally 4.0+)
□ Conversion rate - 0.45%+ threshold
□ Revenue vs previous Black Friday (if data available)
□ Competitive pressure - auction insights

**CAMPAIGNS TO CHECK:**
- 20276730131: AFH | P Max | H&S Zombies Furniture
- 21527979308: AFH | Shopping | Furniture | Villains
- 22138672752: AFH | Shopping | Accessories | H&S
- 21289230716: AFH | P Max Shopping | Accessories | Villains

**EXPECTED AT THIS POINT:**
- Smart Bidding fully adjusted to 150% target
- Impression share should be recovering
- Peak day volume - spend should hit budget
- ROAS may dip slightly due to competitive pressure (acceptable)

**ACTION IF CONCERNING:**
If ROAS below 3.0 → Revert to 170% immediately (peak day, can't risk poor performance)
If metrics good → Continue through Cyber Monday weekend

---

## [Accessories For The Home] ROAS 150% Full Review - Tue Dec 2 (Post-Cyber Monday)
**Completed:** 2025-12-16
**Reason:** Aggressive task audit - Black Friday event completed

POST-CYBER MONDAY FULL REVIEW - 8 days after ROAS reduction

**COMPREHENSIVE ANALYSIS:**
□ Full week impression share trend (Nov 24 - Dec 1)
□ Total spend vs budget over the period
□ Average ROAS across all campaigns
□ Conversion rate trend
□ Revenue comparison: This week vs previous week
□ Black Friday/Cyber Monday weekend performance

**CAMPAIGNS TO REVIEW:**
| Campaign ID | Campaign Name |
|-------------|---------------|
| 20276730131 | AFH | P Max | H&S Zombies Furniture |
| 21527979308 | AFH | Shopping | Furniture | Villains |
| 22138672752 | AFH | Shopping | Accessories | H&S |
| 21289230716 | AFH | P Max Shopping | Accessories | Villains |

**DECISION FRAMEWORK:**

OPTION A: CONTINUE AT 150%
- Trigger: Impression share recovered (50%+), ROAS 3.5+, CR 0.45%+
- Action: Continue through December
- Rationale: 150% working well

OPTION B: REVERT TO 170%
- Trigger: ROAS below 3.5 OR CR below 0.45% OR revenue disappointing
- Action: Revert all 4 campaigns to 170%
- Commands below

OPTION C: FURTHER REDUCTION TO 130%
- Trigger: Impression share still low (<40%) but ROAS/CR very strong (4.5+/0.55%+)
- Action: Further reduce to capture more volume
- Only if metrics exceptionally strong

**REVERT COMMANDS (if needed):**
```
mcp__google-ads__update_campaign_target_roas(customer_id="7972994730", campaign_id="20276730131", target_roas=1.7)
mcp__google-ads__update_campaign_target_roas(customer_id="7972994730", campaign_id="21527979308", target_roas=1.7)
mcp__google-ads__update_campaign_target_roas(customer_id="7972994730", campaign_id="22138672752", target_roas=1.7)
mcp__google-ads__update_campaign_target_roas(customer_id="7972994730", campaign_id="21289230716", target_roas=1.7)
```

---


### [Accessories For The Home] Review Product Hero ROAS change impact (180% → 150%)
- **Task ID**: f8c8cb9e-a937-492e-9cf6-55dfbf2541aa
- **Priority**: P0
- **Created**: Unknown
- **Completed**: 2025-12-16 17:36
- **Review Summary**: Google Ads target ROAS reduction from 210% to 150-170% successfully achieved Q4 scaling objectives. All segments performing above 150% threshold with overall 171% ROAS. Recommendation: Continue current settings through December peak season.
- **Report**: Saved to clients/accessories-for-the-home/reports/target-roas-reduction-review-2025-12-16.md (corrected report)

## [Accessories For The Home] Generic Search Campaign - Implementation & Review
**Completed:** 2025-12-16 18:04
**Source:** Meeting Notes - Nov 10, 2025

Source: Nov 10, 2025 meeting with Google rep (Luiza)

PARENT TASK: Oversees implementation and monitoring of new generic search campaign strategy.

**Campaign:** AFH | Search | Generic (Campaign ID: 23272357581)
**Strategy:** Create new generic search campaigns for AFH to capture longer-tail queries (questions, comparisons, inspiration) that PMax and Shopping campaigns miss.

**Implementation Details:**
- Budget: £50/day
- ROAS Target: 190%
- AI Max: Enabled (broadened match)
- First Ad Group: Dining Chairs (mix of broad and exact match)
- Keywords: luxury furniture, artisan furniture
- Exclusions: Top-performing keywords from existing campaigns excluded

**Daily Monitoring Schedule:** Nov 19-25 (7 days)
- Spend level vs £50/day budget
- Search query quality
- Conversion tracking
- Quality score trends
- Impression share
- PMax performance (cannibalisation check)

**Full Review:** Nov 25, 2025
- Performance vs 190% ROAS target
- Search term analysis for expansion opportunities
- Incremental traffic assessment
- Decision: Scale budget or add more ad groups

Done

Done

---
## [Accessories For The Home] Investigate Search Generic Zero-Conversion Campaign
**Completed:** 2025-12-17 13:18
**Source:** Weekly Report - 6th December 2025

**From Weekly Report - 6th December 2025**

**Issue:** Search Generic Max Conv campaign spent £73 with 0 conversions in 7 days (30 Nov - 6 Dec).

**Expected Impact:** £300+/month waste if trend continues.

**Action:** 
1. Review search terms report for campaign ID 23272357581
2. Identify if keywords are relevant to business
3. Check if any queries have potential
4. If no conversions by 13th December, pause campaign to stop waste

**Supporting Data:**
- Spend: £73 (0.8% of account)
- Clicks: 21
- Impressions: 508
- 0 conversions, £0 revenue
- CPC: £3.48

**Meets threshold:** Zero conversions + >£50 weekly spend = £300/mo waste (Threshold 4)

**Campaign Details:**
- Name: AFH | Search | Generic Max Conv
- ID: 23272357581
- Appears to be new or recently reactivated


Done

Done

---
