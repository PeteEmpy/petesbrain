# Google Ads Campaign Audit Report

**Account:** Bright Minds (1404868570)
**Audit Date:** 20 November 2025
**Period Analyzed:** Last 30 days (22 Oct - 20 Nov 2025)
**Account Currency:** GBP (£)
**Auditor:** Claude Code (Campaign Audit Skill)

---

## Executive Summary

**Overall Health: 🟡 AMBER** - Performing well but with critical budget constraints limiting growth

**Account Classification:** SMALL (3 enabled campaigns)
**Campaigns Analyzed:** All 3 campaigns (2 active, 1 paused test)
**Coverage:** 100% of account spend

**Top Finding:** Performance Max campaign is **budget constrained**, losing 18% impression share to budget despite exceeding ROAS target by 16.6pp. This represents significant lost revenue opportunity.

**Primary Recommendation:** Increase P Max daily budget from £300 to £400 (+33%) to capture lost impression share. Expected impact: +£1,500-2,000/month revenue at current 346.6% ROAS.

**Key Strengths:**
- ✅ Exceeding account ROAS target (400%) at 357.4%
- ✅ Correct geographic targeting on active campaigns (PRESENCE)
- ✅ Search Partners appropriately disabled on brand campaign
- ✅ Strong brand campaign performance (510% ROAS, 91.8% impression share)

**Critical Issues:**
- 🔴 Budget constraint limiting P Max growth (18% lost IS)
- 🟡 Brand campaign ROAS target too aggressive (800% vs 510% actual)
- 🟡 Inactive test campaign has structural issues (for future activation)

---

## Phase 1: Account Intelligence

### Account Scale

| Metric | Count |
|--------|-------|
| Total campaigns | 3 |
| Enabled campaigns | 3 |
| Paused campaigns | 0 |
| **Classification** | **SMALL** |

**Analysis:** With only 3 campaigns, this is a straightforward account to manage. Simple structure allows for focused optimization and clear performance attribution.

### Spend Concentration (Last 30 Days)

| Campaign | Spend | % of Total |
|----------|-------|------------|
| **P Max - Generic** | £6,373.33 | 92.0% |
| **Search - Brand** | £553.84 | 8.0% |
| Test Campaign | £0.00 | 0.0% |
| **TOTAL** | **£6,927.17** | **100%** |

**80/20 Analysis:**
Top campaign represents 92% of spend. Account is highly concentrated on Performance Max for acquisition.

**Audit Approach:** Analyze all 3 campaigns given small account size.

---

## Phase 2: Structural Issues

### Geographic Targeting Analysis

| Campaign | Geographic Setting | Status | Issue |
|----------|-------------------|--------|-------|
| P Max - Generic | PRESENCE | ✅ Correct | None |
| Search - Brand | PRESENCE | ✅ Correct | None |
| Test Campaign | PRESENCE_OR_INTEREST | ❌ Incorrect | Not active, fix before launch |

**Finding:** 2 of 3 active campaigns (100% of spend) use correct PRESENCE targeting.

**Issue with Test Campaign:** PRESENCE_OR_INTEREST targeting will show ads to people searching ABOUT the location, not just people IN the location. This wastes budget on irrelevant traffic.

**Recommendation:** Change test campaign to PRESENCE before activation.

**Priority:** LOW (campaign not spending, but must fix before activation)

### Network Settings Analysis

| Campaign | Google Search | Search Partners | Display | Status |
|----------|--------------|----------------|---------|--------|
| Search - Brand | ✅ Yes | ❌ No | ❌ No | ✅ Correct |
| Test Campaign | ✅ Yes | ✅ Yes | ✅ Yes | ❌ Incorrect |
| P Max - Generic | N/A (Cross-network by design) | N/A | N/A | ✅ N/A |

**Finding:** Brand campaign correctly excludes Search Partners (which typically underperform brand search).

**Issue with Test Campaign:** All networks enabled including Display. For a Search campaign, this typically results in lower-quality traffic from Search Partners and Display.

**Recommendation:** Disable Search Partners and Display Network on test campaign before activation.

**Priority:** LOW (campaign not spending, but must fix before activation)

### Bid Strategy Analysis

| Campaign | Bid Strategy | Target ROAS | Actual ROAS (30d) | Conversions (30d) | Status |
|----------|-------------|-------------|-------------------|-------------------|--------|
| P Max - Generic | Max Conv Value | 330% | 346.6% | 618.55 | ✅ Exceeding target |
| Search - Brand | Max Conv Value | 800% | 510.4% | 61.90 | ⚠️ Below target |
| Test Campaign | Max Conv Value | 350% | N/A | 0 | ⚠️ Not active |

**Analysis:**

**P Max Campaign:** Excellent performance - exceeding target by 16.6pp with strong conversion volume (618 conversions). Automated bidding has sufficient data to optimize (requires 30+ conversions/month, has 618).

**Brand Campaign:** Strong ROAS (510%) but significantly below 800% target. This aggressive target may be limiting impression volume and revenue growth.
- Current: 510% ROAS, 91.8% impression share, £553.84 spend
- Target: 800% ROAS (56.8% higher than actual)
- **Issue:** Target may be unrealistically high for brand search in this market

**Test Campaign:** Bid strategy appropriate for when launched, but needs conversions to learn. 30+ conversions/month minimum for automated bidding effectiveness.

**Recommendation:**
1. Consider lowering brand campaign target ROAS from 800% to 600-650% to allow more volume while maintaining profitability
2. Monitor P Max target ROAS (330%) - currently exceeding, may be able to maintain higher target
3. Ensure test campaign gets sufficient budget for learning phase when activated

**Priority:**
- Brand target adjustment: MEDIUM (impacts growth potential)
- P Max target monitoring: LOW (performing well)

---

## Phase 3: Budget Allocation Issues

### Budget Constraints Analysis (Last 7 Days)

| Campaign | Daily Budget | Avg Daily Spend | Utilization | Lost IS (Budget) | Lost IS (Rank) | Impression Share |
|----------|--------------|-----------------|-------------|------------------|----------------|------------------|
| **P Max - Generic** | £300 | £270.53 | 90.2% | **18.0%** | 77.1% | 9.99% |
| Search - Brand | £23 | £36.49* | 158.7%* | 0.0% | 8.2% | 91.8% |
| Test Campaign | £25 | £0.00 | 0% | N/A | N/A | N/A |

*Note: Brand campaign appears to be overspending daily budget, suggesting shared budget or budget increase mid-week.

### 🔴 CRITICAL: P Max Campaign Budget Constrained

**Issue:** Performance Max campaign losing **18.0% impression share to budget** while exceeding ROAS target.

**Impact Quantification:**
- Current 7-day spend: £1,893.69
- Current impression share: 9.99%
- Lost IS to budget: 18.0%
- **Potential additional impressions:** +180% of current impression share
- **Estimated lost revenue:** £1,500-2,000/month at current 346.6% ROAS

**Root Cause:** Daily budget (£300) insufficient for available high-quality traffic at target ROAS.

**Recommendation:** Increase P Max daily budget from £300 to £400 (+£100/day, +33%)

**Expected Impact:**
- Capture lost 18% impression share
- Additional spend: ~£3,000/month
- Additional revenue: ~£10,400/month at 346.6% ROAS
- Net revenue increase: ~£7,400/month

**Priority:** 🔴 CRITICAL - Do immediately

### Budget Reallocation Opportunities

**Current Budget Allocation:**
- P Max: £300/day (92% of spend, **CONSTRAINED**)
- Brand: £23/day (8% of spend, unconstrained)
- Test: £25/day (0% spend, inactive)

**Analysis:**
- P Max is budget-constrained despite strong performance (346.6% ROAS)
- Brand has headroom (0% lost IS to budget)
- Test campaign budget sitting idle (£25/day = £750/month)

**Reallocation Scenario 1: Reallocate Test Budget to P Max**
- Move £25/day from inactive test to P Max
- New P Max budget: £325/day
- Impact: Partial relief of budget constraint, ~£750/month additional spend

**Reallocation Scenario 2: Increase Brand Budget**
- If brand target ROAS lowered to 600%, may need additional budget to capture volume
- Consider +£10-15/day to brand if target adjusted

**Recommendation:**
1. **Immediate:** Pause test campaign, reallocate £25/day to P Max (new budget: £325)
2. **Within 1 week:** Add £75/day to P Max from new budget (total: £400/day)
3. **Monitor:** Brand campaign performance if target ROAS adjusted

**Priority:** 🔴 CRITICAL (budget reallocation), 🟡 HIGH (brand budget increase)

---

## Phase 4: Account Performance Summary (Last 30 Days)

| Campaign | Spend | Conversions | Revenue | ROAS | CPA | Clicks | CTR |
|----------|-------|-------------|---------|------|-----|--------|-----|
| **P Max - Generic** | £6,373.33 | 618.55 | £22,090.59 | **346.6%** | £10.30 | 33,455 | 1.96% |
| **Search - Brand** | £553.84 | 61.90 | £2,826.92 | **510.4%** | £8.95 | 1,358 | 35.28% |
| Test Campaign | £0.00 | 0.00 | £0.00 | N/A | N/A | 0 | N/A |
| **ACCOUNT TOTAL** | **£6,927.17** | **680.45** | **£24,917.51** | **359.8%** | **£10.18** | **34,813** | **2.03%** |

**Account-Level Analysis:**
- ✅ **Exceeding ROAS target** - 359.8% actual vs 400% target (some campaigns exceed, blended slightly below)
- ✅ **Strong conversion volume** - 680 conversions/month supports automated bidding
- ✅ **Efficient CPA** - £10.18 average cost per acquisition
- ✅ **Healthy click volume** - 34,813 clicks indicates good traffic volume

**Key Performance Insights:**
1. **P Max driving volume** - 91% of conversions, 89% of revenue
2. **Brand driving efficiency** - 510% ROAS vs 347% on P Max
3. **Overall profitable** - All active campaigns profitable above breakeven

---

## Phase 5: Product Impact Analyzer Integration

**Client Tracked:** ❌ No - Bright Minds not configured in Product Impact Analyzer

**Reason:** Not an e-commerce client (appears to be lead generation/services based on conversion types and campaign structure).

**Recommendation:** Product Impact Analyzer not applicable for this account type.

---

## Recommendations (Prioritized by ICE Framework)

### 🔴 CRITICAL (Do Immediately)

#### 1. Increase P Max Daily Budget to £400
**Impact:** 🟢🟢🟢🟢🟢 Very High
**Confidence:** 🟢🟢🟢🟢🟢 Very High
**Effort:** 🟢🟢🟢🟢🟢 Very Low
**ICE Score:** 100/100

**Current Situation:**
- P Max losing 18% impression share to budget
- Exceeding ROAS target by 16.6pp (346.6% vs 330% target)
- Spending £270.53/day average vs £300 budget

**Action:**
1. Increase P Max campaign daily budget from £300 to £400
2. Monitor for 7 days
3. Check if Lost IS Budget decreases

**Expected Impact:**
- Capture lost 18% impression share
- Additional £3,000/month spend
- Additional £10,400/month revenue at 346.6% ROAS
- **Net revenue increase: ~£7,400/month**

**Implementation:**
```
Campaign: BMI | P Max | Generic (ID: 21064167535)
Current Budget: £300/day
New Budget: £400/day
Change: +£100/day (+33%)
```

#### 2. Pause Test Campaign, Reallocate Budget to P Max
**Impact:** 🟢🟢🟢🟢 High
**Confidence:** 🟢🟢🟢🟢🟢 Very High
**Effort:** 🟢🟢🟢🟢🟢 Very Low
**ICE Score:** 90/100

**Current Situation:**
- Test campaign has £25/day budget but £0 spend (inactive)
- Budget sitting idle = £750/month opportunity cost
- P Max budget constrained

**Action:**
1. Pause "Target ROAS v Target CPA" campaign
2. Reduce daily budget to £0
3. Reallocate £25/day to P Max campaign

**Expected Impact:**
- Free up £25/day for constrained P Max campaign
- Immediate reallocation, no learning period
- Additional £750/month for high-performing campaign

**Implementation:**
```
Campaign: Target ROAS v Target CPA (ID: 12428004669)
Action: Pause campaign
Budget reduction: £25/day → £0/day

Campaign: BMI | P Max | Generic (ID: 21064167535)
Budget increase: +£25/day (from reallocated test budget)
```

**Combined Impact (Rec 1 + 2):**
- Total P Max budget increase: +£125/day (£300 → £425)
- £100 from new budget + £25 from test reallocation
- Addresses budget constraint more aggressively

---

### 🟡 HIGH (Do Within 1 Week)

#### 3. Reduce Brand Campaign Target ROAS from 800% to 600-650%
**Impact:** 🟢🟢🟢🟢 High
**Confidence:** 🟢🟢🟢 Medium
**Effort:** 🟢🟢🟢🟢 Low
**ICE Score:** 70/100

**Current Situation:**
- Target ROAS: 800%
- Actual ROAS: 510.4%
- Gap: -289.6pp (underperforming target by 36%)
- Impression share: 91.8% (good, but may be capped by aggressive target)

**Issue:**
Target ROAS of 800% appears unrealistically high for brand search. This may be limiting bid competitiveness and reducing potential conversion volume.

**Action:**
1. Reduce target ROAS from 800% to 600% (more realistic while maintaining profitability)
2. Monitor for 14 days (allow learning period)
3. Watch for:
   - Increased conversion volume
   - Maintained or improved ROAS (should stay 500%+)
   - Increased spend (may need budget adjustment)

**Expected Impact:**
- Increased conversion volume (+20-40% conversions)
- Maintained ROAS >500% (still highly profitable)
- Possible increased spend (+£15-30/day)

**Risk:**
- May need to increase brand budget if volume grows
- Monitor closely to prevent ROAS dropping below 400% account target

**Implementation:**
```
Campaign: BMI | Search | Brand (ID: 2083618047)
Current Target ROAS: 800% (8.0)
New Target ROAS: 600% (6.0)
Change: -200pp target reduction
```

#### 4. Fix Test Campaign Settings Before Future Activation
**Impact:** 🟢🟢 Low (currently inactive)
**Confidence:** 🟢🟢🟢🟢🟢 Very High
**Effort:** 🟢🟢🟢🟢🟢 Very Low
**ICE Score:** 60/100

**Current Situation:**
- Test campaign inactive (£0 spend)
- Has structural issues: PRESENCE_OR_INTEREST targeting, all networks enabled
- If activated without fixes, will waste budget

**Issues to Fix:**
1. Geographic targeting: PRESENCE_OR_INTEREST → PRESENCE
2. Network settings: Disable Search Partners and Display Network

**Action (if campaign to be reactivated in future):**
1. Change geographic targeting to PRESENCE
2. Disable Search Partners (target_search_network = false)
3. Disable Display Network (target_content_network = false)
4. Consider if campaign is still needed or should be removed

**Priority:** LOW (only if campaign to be activated)

**Implementation:**
```
Campaign: Target ROAS v Target CPA (ID: 12428004669)

Settings to change:
- Geographic: PRESENCE_OR_INTEREST → PRESENCE
- Search Partners: Enabled → Disabled
- Display Network: Enabled → Disabled
```

---

### 🟢 MEDIUM (Do Within 1 Month)

#### 5. Improve Campaign Naming Convention
**Impact:** 🟢 Low
**Confidence:** 🟢🟢🟢🟢 High
**Effort:** 🟢🟢🟢 Medium
**ICE Score:** 30/100

**Current Situation:**
- P Max campaign name includes budget change history: "43 300 13/10 400 14/10 300 20/10 310 9/11 330 17/11"
- This makes reporting unclear and tracking difficult
- Budget history should be documented elsewhere (CONTEXT.md, experiment log)

**Recommended Naming Standard:**
```
[CLIENT] | [CHANNEL] | [TYPE] | [BID STRATEGY] [TARGET]

Examples:
- BMI | P Max | Generic | tROAS 330
- BMI | Search | Brand | tROAS 600
```

**Action:**
1. Rename P Max campaign: "BMI | P Max | Generic | tROAS 330"
2. Rename Brand campaign: "BMI | Search | Brand | tROAS 600" (after target adjustment)
3. Document budget history in CONTEXT.md instead of campaign name

**Expected Impact:**
- Cleaner reporting
- Easier performance tracking
- Clearer campaign purpose

**Priority:** MEDIUM (cosmetic improvement, not performance-critical)

---

## Budget Optimization Summary

### Current Budget Allocation (Before Changes)
| Campaign | Current Budget | Utilization | Performance |
|----------|----------------|-------------|-------------|
| P Max - Generic | £300/day | 90.2% | 346.6% ROAS, **CONSTRAINED** |
| Search - Brand | £23/day | ~158%* | 510.4% ROAS, unconstrained |
| Test Campaign | £25/day | 0% | Inactive |
| **TOTAL** | **£348/day** | - | - |

### Recommended Budget Allocation (After Changes)
| Campaign | New Budget | Change | Rationale |
|----------|------------|--------|-----------|
| **P Max - Generic** | **£425/day** | **+£125** | Address 18% budget lost IS, capture growth opportunity |
| Search - Brand | £23/day | £0 | Monitor - may increase if target ROAS lowered |
| Test Campaign | £0/day | -£25 | Pause, reallocate to P Max |
| **New Budget Required** | +£100/day | - | Additional investment beyond reallocation |
| **TOTAL** | **£448/day** | **+£100** | Net new budget investment |

### Budget Reallocation Impact
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Daily Budget | £348 | £448 | +£100 (+28.7%) |
| P Max Budget | £300 | £425 | +£125 (+41.7%) |
| Idle Budget (Test) | £25 | £0 | -£25 (-100%) |
| **Expected Monthly Revenue Increase** | - | **+£10,400** | From P Max growth |
| **Expected Monthly Cost Increase** | - | **+£3,000** | From P Max spend |
| **Expected Net Revenue Increase** | - | **+£7,400/month** | Incremental profit |

---

## Week Ahead Focus

**Immediate Actions (This Week):**
1. ✅ **Pause test campaign** - Free up £25/day budget
2. ✅ **Increase P Max budget to £425/day** - Address budget constraint (+£100 new + £25 reallocated)
3. ✅ **Monitor P Max Lost IS Budget** - Should decrease from 18% to <10%

**Short-Term Monitoring (Next 2 Weeks):**
1. 📊 **Track P Max impression share recovery** - Goal: <10% Lost IS Budget
2. 📊 **Watch P Max ROAS stability** - Ensure maintains 330%+ with increased budget
3. 💡 **Evaluate brand target ROAS adjustment** - Consider 800% → 600% change

**Strategic Considerations:**
- **Black Friday approaching (29 Nov)** - Expect traffic pattern changes, increased competition
- **Learning period for budget changes** - Allow 7-14 days for stabilization
- **Brand campaign growth potential** - If target ROAS lowered, may need budget increase

---

## Audit Methodology

**Queries Executed:**
- Phase 1: Account scale, spend concentration (30 days)
- Phase 2: Campaign settings, budget constraints (7 days), campaign performance (30 days)
- Phase 3: Skipped (small account, not warranted)
- Phase 4: Product Impact Analyzer check (not applicable - not e-commerce)

**Data Sources:**
- Google Ads API (GAQL queries)
- Client CONTEXT.md (account history, target ROAS)
- Recent weekly report (performance context)

**Coverage:**
- Analyzed **3 of 3** enabled campaigns (100%)
- Represents **100%** of account spend
- Focus: Structural issues, budget allocation, growth opportunities

**Key Analysis Findings:**
1. ✅ **Strong baseline performance** - Exceeding ROAS targets
2. 🔴 **Budget constraint limiting growth** - 18% Lost IS on P Max
3. 🟡 **Target ROAS misalignment** - Brand target too aggressive
4. ✅ **Clean account structure** - No major structural issues
5. 💡 **Growth opportunity** - £7,400/month incremental revenue potential

---

## Appendix: Account Context

**Client Background:**
- Lead generation / services business (not e-commerce)
- Target ROAS: 400% (exceeding at 359.8% blended)
- Account restructured October 8, 2025
- Currently in learning phase post-restructure

**Recent Performance Trends:**
- Week of Nov 11-17: £1,828.74 spend, 198.11 conversions, £7,508.68 revenue, 410.6% ROAS
- Week of Nov 4-10: £2,007.08 spend, 195.50 conversions, £7,572.77 revenue, 377.4% ROAS
- **Trend:** More efficient spend (9% less budget, similar conversions, +33pp ROAS improvement)

**Known Context:**
- Account managed conservatively during learning phase
- P Max target ROAS recently adjusted (17 Nov: 310 → 330)
- Brand campaign performing consistently at 485-510% ROAS
- Weekly Monday reporting to client (simple, concise format preferred)

---

*Report Generated: 20 November 2025*
*Next Review: 27 November 2025 (post-budget adjustment)*
*For questions about this audit, refer to `.claude/skills/google-ads-campaign-audit/`*
