# Go Glean - Completed Tasks

This file tracks all completed tasks for Go Glean (Customer ID: 8492163737).

---

## Scale Villains Campaign Budget
**Completed:** 2025-12-11
**Task ID:** f6d044f0-5f82-4e95-a574-b62a1d956f38
**Priority:** P0
**Source:** Weekly Report - 2025-11-18

**Issue Identified:** Best-performing campaign (640% ROAS) only getting 8% of budget allocation.

**Expected Impact:** +£400-600/month revenue if ROAS maintains at 500%+

**Scaling Strategy:**
1. Increase budget from £5/day to £20-25/day (incremental approach)
2. Monitor ROAS daily for first week
3. If ROAS stays >400%, continue increasing by £5/day every 3 days
4. Cap at £50/day or when ROAS drops below 300%

**Supporting Data:**
- Campaign: "GOG | P Max Shopping | Villains 280 2/9 249 8/9 260 11/9 230 15/9 260 23/9"
- Current ROAS: 640% (best in account)
- Current spend: £35.92/week (~£5/day)
- Revenue: £229.91
- CPA: £5.13 (excellent efficiency)

**Context:** Go Glean is a **Product Hero Client** using performance-based campaign segmentation. The Villains campaign, despite its name, is significantly outperforming other campaigns due to strong product-level performance indicators. This is a scaling opportunity for high-performing products within the account.

**Status:** Completed - Strategy documented and ready for implementation.

---

## Campaign Audit Recommendations - Phase 1 Implementation
**Completed:** 2025-11-14
**Source:** Manual completion (reported in Claude Code) + Google Ads Campaign Audit (20251114-campaign-audit.md)

**Context:**
Following comprehensive campaign audit identifying budget misallocation and geographic targeting waste, implemented first phase of recommended optimizations.

**Changes Made:**

1. **Shopping Catch All Campaign ROAS Adjustment**
   - Campaign: GOG | Shopping | Catch All 310 280 8/9 230 15/9 260 23/9
   - Previous target: 260% (2.6x)
   - New target: 240% (2.4x)
   - Reason: Campaign performing above target (286% actual vs 260% target), reduced to align with account-wide 240% standard and allow more volume
   - Campaign name updated to reflect change: "...260 23/9 240 14/11"

2. **Villains PMax Geographic Targeting Fix**
   - Campaign: GOG | P Max Shopping | Villains 280 2/9 249 8/9 260 11/9 230 15/9 260 23/9
   - Previous: PRESENCE_OR_INTEREST (geographic waste)
   - New: PRESENCE (correct targeting)
   - Impact: Eliminates 5-10% budget waste (~£7.50-£15/month) on irrelevant traffic
   - Performance: Campaign achieving 422% ROAS (vs 260% target), strong performer

**Expected Outcomes:**
- Shopping Catch All: Increased volume while maintaining profitability above 240% target
- Villains: Reduced wasted spend on non-present users, improved efficiency on small budget
- Overall: Aligned ROAS targets across campaigns (240-260% range)

**Review Date:** November 21, 2025 (7 days post-implementation)
- Monitor Shopping Catch All volume increase and ROAS performance
- Verify Villains targeting change reduced waste
- Assess readiness for Phase 2 (budget reallocation recommendation)

**Audit Reference:** /Users/administrator/Documents/PetesBrain/clients/go-glean/audits/20251114-campaign-audit.md

**Notes:**
- Villains ROAS target remains at 260% (no change needed - performing 62% above target)
- Primary audit recommendation (budget reallocation) deferred pending Phase 1 results
- All campaigns now using PRESENCE targeting (best practice)
- Search Partners remain disabled across all campaigns (best practice)

---

---

## [Go Glean] Pause Search Campaign - Zero Conversions
**Completed:** 2025-11-28
**Task ID:** 1518316f-9bb6-4bc9-b883-9e282673e779
**Priority:** P0
**Source:** Weekly Report - 2025-11-18

**Issue:** Search campaign "GOG | Search | Products" spent £50.40 with ZERO conversions in 7 days. 6.43% CTR suggested broken targeting.

**Action Taken:** Campaign has been paused in Google Ads.

**Expected Impact:** Stop bleeding £200/month in wasted spend.

**Supporting Data:**
- Spend: £50.40 (11% of weekly budget)
- Conversions: 0
- Clicks: 65 at £0.78 CPC
- CTR: 6.43% (unusually high - suggested broad match issues)

**Manual Note:** This has been paused. Task completed per manual task notes (2025-11-28).


---

## [Go Glean] Audit Primary PMax Asset Groups
**Completed:** 2025-11-20
**Task ID:** f0a95d3c-0569-4e76-aa05-f5072f165410
**Priority:** P0
**Source:** Weekly Report - 2025-11-18

**Audit Completed:** 2025-11-20

**Summary:** 
Comprehensive audit of Primary PMax asset groups for Non Grout H&S&Z campaign completed. 

**Key Findings:**
- Hero/Sidekick classification confirmed based on 30-day ROAS (not 7-day)
- Black Stone products validated as Heroes with strong 30-day performance
- Identified potential Zombie products for promotion based on sustained performance
- Full audit report: clients/go-glean/reports/ad-hoc/2025-11-20-pmax-asset-group-audit-CORRECTED.html

**Critical Learning:** 
Product Hero Strategy uses 30-day performance metrics. Short-term 7-day variance is expected and acceptable.

**Manual Note (2025-11-28):** Audit already completed per task notes. Task marked complete.
## [Go Glean] Audit Primary PMax Asset Groups
**Completed:** 2025-12-12 15:23
**Source:** Weekly Report - 2025-11-18

**From Weekly Report - 2025-11-18**
**AUDIT COMPLETED: 2025-11-20** ✅
**STRATEGY CLARIFICATION: 2025-11-20** 📋

**CRITICAL LEARNING: Product Hero Strategy = 30-Day Performance**

Hero/Sidekick classification is based on **30-day ROAS**, not 7-day. Short-term variance is expected and acceptable - that's what the segmentation handles.

**Black Stone Products (30-Day Performance):**
- Black Stone Sealer 500ml: **265% ROAS** → Hero status JUSTIFIED ✓
- Black Stone Restorer: **338% ROAS** → Hero status JUSTIFIED ✓

**7-Day Performance (Nov 12-18):**
- Black Stone Restorer - Heroes: 0% ROAS, £19.09 spent
- This is normal variance for Heroes - let them ride it out

**ACTION: NO PAUSING REQUIRED** - Heroes should stay active through short-term fluctuations.

---

**REVISED FOCUS: Identify True Zombies That Need Promoting**

Based on 7-day data showing strong performers, check if these need **30-day performance review** for potential promotion:

1. ⭐ Grout Reviver Pens: 881% ROAS (7d) - Check 30d performance
2. ⭐ Salt Stain Remover 5L: 1,380% ROAS (7d) - Check 30d performance  
3. ⭐ Composite Sink Restorer: Strong conversions (7d) - Check 30d performance
4. Glass & Mirror Cleaner: 231% ROAS (7d) - Check 30d performance

**Next Step:** Pull 30-day product-level ROAS to see if any Zombies qualify for Hero/Sidekick promotion based on sustained 30-day performance.

**Supporting Data:**
- Campaign: "GOG | P Max | Non Grout H&S&Z 240 11/10"
- Current ROAS: 122% (vs 240% target)
- Budget share: 60% (£275.68/week)
- Date range: Nov 12-18 (complete data, 2-day lag buffer)
- Full audit report: clients/go-glean/reports/ad-hoc/2025-11-20-pmax-asset-group-audit-CORRECTED.html


---

## [Go Glean] Pause Search Campaign - Zero Conversions
**Completed:** 2025-12-12 16:55
**Source:** Weekly Report - 2025-11-18

**Campaign Status:** PAUSED ✅

**Campaign Details:**
- Name: GOG | Search | Products 350 16/6 AI Max 26/6 300 1/8 230 15/9 260 23/9 240 3/10
- ID: 22422709676
- Current Status: PAUSED

**Performance Nov 1 - Dec 12:**
- Total Spend: £169.59
- Conversions: 5.58
- CPA: £30.44
- Clicks: 193
- Impressions: 3,211

**Resolution:**
The campaign identified in the Nov 18 weekly report (£50.40 spend, 0 conversions) has been paused. After the initial zero-conversion period, it generated 5.58 conversions before being paused, but the CPA of £30.44 is likely too high for Go Glean's profitability model.

**Action Taken:** Campaign already paused - no further action needed. Waste elimination successful.
