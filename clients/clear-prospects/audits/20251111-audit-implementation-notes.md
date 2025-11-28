# Clear Prospects Campaign Audit - Implementation Notes

**Date Implemented:** 11 November 2025
**Implemented By:** Peter Empson
**Audit Report:** [20251111-campaign-audit.md](20251111-campaign-audit.md)

---

## Actions Completed ✅

### 1. Geographic Targeting Fix (CRITICAL)

**Changed 4 campaigns from PRESENCE_OR_INTEREST to PRESENCE:**

| Campaign | Brand | Previous Setting | New Setting | Expected Savings |
|----------|-------|------------------|-------------|------------------|
| CPL \| HSG \| P Max Shopping \| Villains 120 130 15/9 | HSG | PRESENCE_OR_INTEREST ❌ | PRESENCE ✅ | £27-41/month |
| CPL \| HSG \| P Max Shopping \| Zombies | HSG | PRESENCE_OR_INTEREST ❌ | PRESENCE ✅ | £43-64/month |
| CPL \| WBS \| P Max Shopping \| Wheat Bags \| Villains 120 15/9 | WBS | PRESENCE_OR_INTEREST ❌ | PRESENCE ✅ | £36-53/month |
| CPL \| WBS \| P Max \| Shopping \| Zombies 120 15/9 | WBS | PRESENCE_OR_INTEREST ❌ | PRESENCE ✅ | £37-55/month |

**Total Expected Impact:** £142-213/month waste eliminated (20-30% of £713/month combined spend)

**Review Date:** 9 December 2025 (4 weeks post-change)

---

### 2. BMPM PMax Target ROAS Set (CRITICAL)

**Campaign:** CPL | BMPM | P Max Shopping 8/9 50 6/10 70 No target 21/10

**Change:**
- **Previous:** No target ROAS (algorithm had no profitability guidance)
- **New:** 70% target ROAS (0.7x)
- **Current Actual ROAS:** 78% (losing 22% on every £1 spent)

**Rationale:**
- Algorithm was spending without any profitability constraint
- 70% target gives algorithm guidance to prioritize more profitable auctions/products
- May initially reduce spend as algorithm avoids unprofitable auctions (this is GOOD)

**Expected Impact:**
- ROAS improvement of 10-20 percentage points over 4-6 weeks
- Initial spend reduction possible (algorithm learning which auctions/products are profitable)
- Monitor product-level performance in [BMPM Product Performance Spreadsheet](https://docs.google.com/spreadsheets/d/1EenJFkPWGZ6c_ZhsKKYudDcW2Nt8Jeamc1m55BPR5dU/)

**Review Date:** 9 December 2025 (4 weeks) and mid-December (6 weeks)

**Decision Point:** If ROAS doesn't improve to 85%+ by mid-December, consider:
- Pausing PMax campaign entirely
- Focusing only on cushions Search campaign (started Oct 21)
- Further product feed pruning

---

### 3. WBS PMax H&S Budget Increase

**Campaign:** CPL | WBS | P Max Shopping | H&S 120 4/9

**Change:**
- **Previous:** £120/day budget (71% utilization = £85.55 avg daily spend)
- **New:** £150/day budget
- **Performance:** 129% ROAS (strong performer), 285 conversions/30 days

**Rationale:**
- High-ROAS campaign was underutilizing budget (only 71%)
- Geographic targeting fixes on Villains/Zombies campaigns freed up recommendation to increase this one
- Campaign has strong conversion volume for Smart Bidding to optimize effectively

**Expected Impact:**
- Better budget utilization (expecting 80-90% of £150/day)
- Additional £20-30/day spend at 129% ROAS
- **Revenue gain:** £774-1,161/month additional revenue

**Review Date:** 18 November 2025 (1 week) - check utilization %, then 9 December (4 weeks) - full performance review

---

### 4. HSG Search Campaign Consolidation

**Consolidated 3 low-volume campaigns into 1:**

| Old Campaign | 30d Conv | 30d Spend | Status |
|--------------|----------|-----------|--------|
| CPL \| HSG \| Search \| Hot Water Bottle Cover 120 28/5 130 16/9 | 8 | £66.47 | ❌ PAUSED |
| CPL \| HSG \| Search \| Photo Bunting 120 18/10 tCPA 9/10 8/7 Ai MAx 14/10 | 3 | £33.73 | ❌ PAUSED |
| CPL \| HSG \| Search \| Photo Face Cushion 130 18/6 120 24/6 Ai Max 14/10 | 4 | £17.67 | ❌ PAUSED |

**New Campaign:** CPL | HSG | Search | Products 130 16/9
- **Combined Budget:** £40/day (sum of previous campaigns)
- **Combined Conversions:** 15/month (still below ideal 30+ but better than 3-8 individually)
- **Target ROAS:** 1.3x (130%)
- **Bidding:** Maximize Conversion Value with target ROAS

**Rationale:**
- Individual campaigns had insufficient conversion volume (<10 conv/month) for Target ROAS automated bidding
- Consolidation provides better data volume for Smart Bidding algorithm to learn
- Reduces campaign management overhead

**Expected Impact:**
- 5-10% efficiency improvement over 6-8 weeks as Smart Bidding learns from larger data set
- Better performance than 3 separate campaigns struggling with low data

**Review Date:** 9 December 2025 (4 weeks post-consolidation)

---

## Actions NOT Completed ⚠️

### 5. Pause BMPM Search Campaign (CRITICAL - AUDIT RECOMMENDATION)

**Status:** NOT IMPLEMENTED (client decision pending)

**Campaign:** CPL | BMPM | Search | Promotional Merchandise
- **Current Status:** ENABLED and spending
- **Performance:** 35% ROAS (losing £172/month)
- **Conversions:** Only 2 in 30 days (insufficient for automated bidding)
- **Budget Lost IS:** 43% (severely constrained)

**Audit Recommendation:** PAUSE campaign immediately to stop losses

**Actual Decision:** Left enabled for now (client may want to keep Search presence)

**Alternative Implemented:** Monitor closely for December review

**Risk:** Continues to lose £172/month (65% loss on every £1 spent)

---

### 6. Delete/Pause 6 Experiment Campaigns

**Status:** CANNOT DELETE (Google Ads restriction)

**Campaigns Affected:**
- Target CPA Experiment - CPL | WBS | Search | Heat Pads & Packs | Broad
- Target CPA Experiment – CPL | TJR | Search | Luggage Straps | Exact
- HSG | Photo Cushion Broad Experiment
- CPL | WBS |  Wheat Bags 170 Broad Test  Recommendations trial
- CPL | WBS |  Wheat Bags 141  Trial 236
- CPL | WBS |  Wheat Bags 140 21/5 140 14/1  Trial 721

**Issue:** Google Ads does not allow deletion of experiment campaigns (API/UI restriction)

**Current Status:** Left ENABLED but spending £0 (no active traffic, no cost)

**Impact:** None (no cost, just clutter in account view)

**Workaround:** Accepted as limitation - campaigns not actively managed

---

## Investigation Notes 🔍

### BMPM Nov 6 Product Feed Change - NOT CONFIRMED

**Audit Finding:** Product Impact Analyzer detected 337KB of product changes on Nov 6, 2025 for BMPM brand

**Investigation Result:** **NO CHANGE VISIBLE in Google Merchant Centre**

**Possible Explanations:**
1. **False positive** - Product Impact Analyzer may have logged data sync issue as "change"
2. **Temporary change reverted** - Change was made and quickly reverted same day
3. **Merchant Centre vs API data lag** - Change visible in API but not reflected in UI
4. **Label changes only** - Product Hero labels changed (custom_label_4) but not visible in Merchant Centre product view

**Action Required:**
- Check Product Impact Analyzer source data: `tools/product-impact-analyzer/data/product_changes/BMPM/2025-11-06.json`
- Compare with Merchant Centre API feed data for Nov 6
- May need to review Product Impact Analyzer change detection logic

**Impact on Audit:**
- Does NOT affect other audit findings (geographic targeting, bid strategy, budget issues all confirmed)
- BMPM product feed hypothesis cannot be confirmed or used for performance correlation
- Continue monitoring BMPM performance regardless of feed changes

---

## Monitoring Schedule 📅

### Week 1 Review (18 Nov 2025)
- Check WBS PMax H&S budget utilization (£150/day vs previous £120/day)
- Quick check: Are 4 geographic targeting fixes showing reduced spend?

### Week 4 Review (9 Dec 2025) - FULL REVIEW
- **Geographic Targeting:** Confirm 20-30% waste reduction on 4 campaigns
- **BMPM PMax 70% Target:** Check if ROAS improving from 78% toward target
- **WBS PMax H&S Budget:** Analyze revenue gain from £120→£150 increase
- **HSG Products Consolidated Campaign:** Review conversion volume and performance vs old campaigns
- **Decision Point:** BMPM Search campaign - continue or pause?

### Week 6 Review (23 Dec 2025 / Early Jan 2026)
- **BMPM Strategy Decision:** If ROAS <85%, consider pausing PMax and focusing on cushions Search only

---

## Expected Outcomes Summary

| Action | Expected Savings/Gain | Timeline | Status |
|--------|----------------------|----------|---------|
| Geographic targeting fix (4 campaigns) | £142-213/month saved | 4 weeks | ✅ IMPLEMENTED |
| BMPM PMax 70% target set | ROAS improvement 78%→85%+ | 4-6 weeks | ✅ IMPLEMENTED |
| WBS PMax H&S budget increase | £774-1,161/month revenue | 1-4 weeks | ✅ IMPLEMENTED |
| HSG campaign consolidation | 5-10% efficiency gain | 6-8 weeks | ✅ IMPLEMENTED |
| BMPM Search pause (NOT DONE) | £172/month losses avoided | Immediate | ⚠️ NOT IMPLEMENTED |

**Total Implemented Savings/Gains:** £916-1,374/month (conservative estimate)

**Total Audit Potential:** £1,088-1,546/month if BMPM Search also paused

---

## Notes for Future Reference

1. **Geographic Targeting Best Practice:** Always use PRESENCE for UK-only campaigns. PRESENCE_OR_INTEREST only appropriate for international brand awareness campaigns where showing ads to people researching from abroad is valuable.

2. **Automated Bidding Data Requirements:** Target ROAS/CPA strategies need 30+ conversions/month per campaign minimum. Below this, consider:
   - Campaign consolidation (done for HSG)
   - Manual CPC bidding
   - Maximize Conversions without target (accepts all conversions regardless of CPA)

3. **BMPM Crisis Management:** Two-track approach:
   - Track A: Set profitability guardrails (70% target ROAS) and monitor
   - Track B: Test focused approach (cushions-only Search campaign started Oct 21)
   - Decision in 4-6 weeks which track is working

4. **Experiment Campaign Limitation:** Google Ads does not allow deletion of draft/experiment campaigns through UI or API. Can only pause. Keep this in mind for future experiment setup - use clear naming so they're identifiable as inactive.

5. **Product Impact Analyzer Data Quality:** Need to validate Nov 6 BMPM feed change detection. May require review of change detection algorithm or API data source validation.

---

*Implementation notes compiled by Peter Empson*
*Next review: 9 December 2025*
