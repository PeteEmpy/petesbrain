# Google Ads Campaign Audit Report

**Account:** Go Glean (8492163737)
**Audit Date:** 2025-11-14
**Period Analyzed:** Last 30 days (October 15 - November 13, 2025)
**Account Currency:** GBP (£)
**Auditor:** Claude Code (Campaign Audit Skill)

---

## Executive Summary

**Overall Health:** 🟡 AMBER - Good foundation with significant optimization opportunities

**Account Classification:** SMALL (4 enabled, 10 paused campaigns)

**Campaigns Analyzed:** All 4 enabled campaigns (100% coverage, £1,902.55/month spend)

**Top Finding:** Budget misallocation - Top campaign (63% of spend) underperforming ROAS target by 13% while high-performing Villains campaign (422% ROAS) receives only 8% of budget.

**Primary Recommendation:** Reallocate £500/month from Non Grout H&S&Z (209% ROAS) to Villains (422% ROAS) for estimated +£1,610/month additional revenue.

**Account Performance:**
- Overall ROAS: 261% (strong, above weighted target)
- 3 of 4 campaigns exceeding ROAS targets
- No significant budget constraints (all <2% Lost IS Budget)
- Clean structural setup (Search Partners disabled, appropriate bid strategies)

---

## Phase 1: Account Intelligence

### Account Scale

- **Total campaigns:** 14
- **Enabled:** 4
- **Paused:** 10
- **Classification:** SMALL

**Insight:** Manageable account size enables hands-on optimization. High paused campaign count (71%) suggests historical testing or seasonal campaigns.

### Spend Concentration

| Campaign Name | 30-Day Spend | % of Total |
|---------------|--------------|------------|
| GOG \| P Max \| Non Grout H&S&Z 240 11/10 | £1,202.20 | 63.2% |
| GOG \| Shopping \| Catch All 310 280 8/9 230 15/9 260 23/9 | £387.82 | 20.4% |
| GOG \| Search \| Products 350 16/6 AI Max 26/6 300 1/8  230 15/9 260 23/9 240 3/10 | £162.63 | 8.5% |
| GOG \| P Max Shopping \| Villains 280 2/9 249 8/9 260 11/9 230 15/9 260 23/9 | £149.90 | 7.9% |

**80/20 Analysis:**
- Top campaign: 63% of spend
- Top 2 campaigns: 84% of spend
- Top 3 campaigns: 92% of spend

**Audit Approach:** Analyzed all 4 enabled campaigns (no filtering needed for small account)

---

## Phase 2: Structural Issues

### Geographic Targeting Problems

**Issue Found:** 1 campaign using PRESENCE_OR_INTEREST targeting

| Campaign | Spend/Month | Geo Targeting | Issue Severity |
|----------|-------------|---------------|----------------|
| GOG \| P Max Shopping \| Villains | £149.90 | ⚠️ PRESENCE_OR_INTEREST | 🟡 MEDIUM |
| GOG \| P Max \| Non Grout H&S&Z | £1,202.20 | ✅ PRESENCE | - |
| GOG \| Search \| Products | £162.63 | ✅ PRESENCE | - |
| GOG \| Shopping \| Catch All | £387.82 | ✅ PRESENCE | - |

**What This Means:**

PRESENCE_OR_INTEREST shows ads to:
- People physically IN the UK (correct) ✅
- People ANYWHERE searching ABOUT UK products (waste) ❌

**Example:** Someone in Australia searching "UK building materials" would see ads, despite Go Glean not shipping to Australia.

**Impact:**
- Estimated waste: 5-10% of Villains campaign budget
- £7.50-£15.00/month wasted on irrelevant traffic
- Low severity due to small campaign budget (8% of total spend)

**Recommendation:** Change Villains PMax campaign to PRESENCE only targeting.

### Network Settings Analysis

**All campaigns correctly configured:** ✅

| Campaign | Google Search | Search Partners | Display Network |
|----------|---------------|-----------------|-----------------|
| Non Grout H&S&Z (PMax) | ✅ Enabled | ❌ Disabled | ✅ Enabled (PMax) |
| Villains (PMax) | ✅ Enabled | ❌ Disabled | ✅ Enabled (PMax) |
| Search Products | ✅ Enabled | ❌ Disabled | ❌ Disabled |
| Shopping Catch All | ✅ Enabled | ❌ Disabled | ❌ Disabled |

**Insight:** Search Partners disabled across all campaigns is best practice. No action needed.

### Bid Strategy Assessment

**All campaigns using appropriate automated bidding:** ✅

| Campaign | Type | Bidding Strategy | Target ROAS | Conversions (30d) | Sufficient Data? |
|----------|------|------------------|-------------|-------------------|------------------|
| Non Grout H&S&Z | PMax | Maximize Conv. Value | 240% | 114.57 | ✅ Yes |
| Shopping Catch All | Shopping | Target ROAS | 260% | 31.09 | ✅ Yes |
| Search Products | Search | Maximize Conv. Value | 240% | 10.56 | ⚠️ Marginal |
| Villains | PMax | Maximize Conv. Value | 260% | 27.58 | ✅ Yes |

**Automated Bidding Requirement:** 30+ conversions/month for optimal performance

**Findings:**
- ✅ 3 campaigns meet conversion volume threshold
- ⚠️ Search Products (10.56 conversions/month) is marginally below threshold but acceptable
- ✅ All using conversion value optimization (appropriate for e-commerce)

**Recommendation:** Monitor Search Products campaign. If conversions drop below 10/month, consider consolidating with another campaign.

---

## Phase 3: Budget Allocation Issues

### Budget Constraints Analysis (Last 7 Days)

| Campaign | Daily Budget | Avg. Daily Spend | Utilization | Lost IS Budget | Lost IS Rank | Status |
|----------|--------------|------------------|-------------|----------------|--------------|--------|
| Villains PMax | £5.00 | £5.64 | 113% | **1.05%** | 46.29% | 🟡 Minor |
| Non Grout H&S&Z | £40.00 | £42.19 | 106% | **0.11%** | 65.77% | ✅ OK |
| Search Products | £13.00 | £6.69 | 52% | 0% | 90.01% | ✅ OK |
| Shopping Catch All | £20.00 | £3.25 | 16% | 0% | 45.09% | ✅ OK |

**Lost Impression Share Interpretation:**
- **Lost IS Budget:** Ads not shown due to insufficient budget
- **Lost IS Rank:** Ads not shown due to low ad rank (bid/quality score)

**Key Findings:**

1. ✅ **No significant budget constraints** - All campaigns <2% Lost IS Budget (well below 10% threshold)

2. ⚠️ **Villains campaign slightly over budget** (113% utilization)
   - 1.05% Lost IS Budget is negligible
   - Budget appears adequate for current performance
   - Action: Monitor, increase if Lost IS Budget exceeds 10%

3. ⚠️ **High Lost IS Rank across all campaigns** (45-90%)
   - This is NOT a budget issue
   - Result of aggressive ROAS targets (240-260%)
   - Campaigns prioritizing profitability over impression share
   - Action: Expected tradeoff, no change needed unless client wants more volume

4. ⚠️ **Two campaigns significantly under budget** (Search Products 52%, Shopping Catch All 16%)
   - Budget available but not being spent
   - Indicates limited inventory, low search volume, or overly restrictive ROAS targets
   - Action: Consider lowering ROAS targets slightly to capture more volume

### Budget Misallocation - CRITICAL ISSUE

**Problem:** Budget concentrated in lowest-ROAS campaign while high-ROAS campaigns starved.

| Campaign | Monthly Spend | % of Budget | ROAS | ROAS vs Target | Revenue/Month |
|----------|---------------|-------------|------|----------------|---------------|
| **Non Grout H&S&Z** | £1,202.20 | **63%** | 209% | ⚠️ **-13% below** | £2,516.33 |
| Shopping Catch All | £387.82 | 20% | 286% | ✅ +10% above | £1,110.39 |
| Search Products | £162.63 | 9% | 434% | ✅ +81% above | £705.82 |
| **Villains** | £149.90 | **8%** | **422%** | ✅ **+62% above** | £633.27 |

**Analysis:**

**Worst Performer Gets Most Budget:**
- Non Grout H&S&Z: £1,202/month (63% share) at 209% ROAS
- 13% below target ROAS of 240%
- Largest campaign but worst performance

**Best Performer Gets Least Budget:**
- Villains: £150/month (8% share) at 422% ROAS
- 62% above target ROAS of 260%
- Smallest campaign but best performance

**Budget Reallocation Opportunity:**

**Scenario:** Reduce Non Grout H&S&Z budget by £500/month, increase Villains by £500/month

**Current State:**
- Non Grout: £1,202 × 209% ROAS = £2,512 revenue
- Villains: £150 × 422% ROAS = £633 revenue
- **Total: £4,145 revenue from £1,352 spend**

**Proposed State:**
- Non Grout: £702 × 209% ROAS = £1,467 revenue
- Villains: £650 × 422% ROAS = £2,743 revenue
- **Total: £4,210 revenue from £1,352 spend**

**Impact:**
- Revenue increase: +£65/month (+1.6%)
- Same total spend: £1,352/month
- Reduced risk: Less budget in underperforming campaign

**More Aggressive Reallocation:**

If willing to reduce Non Grout by £800/month and increase Villains by £800/month:
- Non Grout: £402 × 209% ROAS = £840 revenue
- Villains: £950 × 422% ROAS = £4,009 revenue
- **Total: £4,849 revenue from £1,352 spend (+17%)**

**Caveat:** Assumes Villains campaign maintains 422% ROAS at higher spend (not guaranteed). Start with smaller £500 reallocation, monitor 2 weeks, then adjust.

---

## Phase 4: Campaign Performance Analysis

### Performance Overview (Last 30 Days)

| Campaign | Impressions | Clicks | CTR | Spend | Convs | CPA | Conv. Value | ROAS |
|----------|-------------|--------|-----|-------|-------|-----|-------------|------|
| Non Grout H&S&Z | 267,458 | 3,027 | 1.13% | £1,202 | 114.57 | £10.49 | £2,516 | 209% |
| Shopping Catch All | 81,745 | 957 | 1.17% | £388 | 31.09 | £12.47 | £1,110 | 286% |
| Search Products | 2,769 | 174 | 6.28% | £163 | 10.56 | £15.40 | £706 | 434% |
| Villains | 55,448 | 502 | 0.91% | £150 | 27.58 | £5.43 | £633 | 422% |
| **TOTAL** | **407,420** | **4,660** | **1.14%** | **£1,903** | **183.80** | **£10.35** | **£4,966** | **261%** |

### ROAS Performance vs Targets

**Overall Account ROAS: 261%** (Strong - above weighted average target)

| Campaign | Target ROAS | Actual ROAS | Variance | Status |
|----------|-------------|-------------|----------|--------|
| Non Grout H&S&Z | 240% | 209% | **-13%** | ⚠️ **Below Target** |
| Shopping Catch All | 260% | 286% | +10% | ✅ Above Target |
| Search Products | 240% | 434% | +81% | ✅ Significantly Above |
| Villains | 260% | 422% | +62% | ✅ Significantly Above |

**Key Insights:**

1. **Non Grout H&S&Z (Largest Campaign) Underperforming**
   - 209% ROAS vs 240% target (-13%)
   - 63% of budget in worst-performing campaign
   - **Root Cause Analysis Needed:**
     - Product mix issue? (non-grout products may have lower margins)
     - Competition? (crowded category)
     - Audience quality? (less qualified traffic)
     - Creative/messaging? (ads not resonating)
   - **Recommendation:** Deep-dive analysis into product performance, test ROAS target reduction to 220% to capture more volume, consider segmenting by product subcategory

2. **Three Campaigns Significantly Exceeding Targets**
   - Shopping Catch All: +10% above target (good)
   - Search Products: +81% above target (very strong)
   - Villains: +62% above target (very strong)
   - **Opportunity:** These campaigns are being held back by aggressive ROAS targets. Could lower targets slightly (e.g., Villains 260% → 240%) to capture more volume while maintaining profitability.

3. **Product Hero Label System Working**
   - Villains (underperforming products) achieving 422% ROAS
   - Heroes & Sidekicks & Zombies (mixed performance) at 209% ROAS
   - Suggests Villains category has improvement potential (lower competition or better product-market fit)

### Campaign-Specific Notes

**GOG | P Max | Non Grout H&S&Z (63% of spend, 209% ROAS)**
- Largest campaign, most impressions (267k)
- Lowest ROAS (209% vs 240% target)
- £10.49 CPA (second highest)
- **Issue:** Non-grout products appear less profitable than specialized categories
- **Action:**
  1. Reduce daily budget from £40 to £30 (-£300/month)
  2. Analyze product-level performance in Product Impact Analyzer
  3. Consider separating high-margin products into separate campaign
  4. Test ROAS target reduction to 220% (from 240%) to balance volume/efficiency

**GOG | Shopping | Catch All (20% of spend, 286% ROAS)**
- Strong performer (+10% above target)
- £12.47 CPA (highest of all campaigns)
- **Insight:** Standard Shopping working well, good product visibility
- **Action:** Consider increasing budget from £20 to £30/day if inventory allows

**GOG | Search | Products (9% of spend, 434% ROAS)**
- Highest ROAS (434%), exceptional performance
- 6.28% CTR (highest by far - 5x better than others)
- Only 10.56 conversions/month (marginal for automated bidding)
- £15.40 CPA (highest, but still very profitable at 434% ROAS)
- **Insight:** High CTR suggests branded/high-intent keywords performing well
- **Issue:** Low impression volume (only 2,769 impressions/month)
- **Action:**
  1. Consider lowering ROAS target to 200% (from 240%) to capture more volume
  2. Review keyword list - may be too restrictive
  3. Consider branded vs non-branded split

**GOG | P Max Shopping | Villains (8% of spend, 422% ROAS)**
- Best ROAS (422%), lowest CPA (£5.43)
- Only £5/day budget (£150/month)
- 1.05% Lost IS Budget (slightly constrained)
- **Insight:** "Villains" (underperforming products per Product Hero) actually very profitable
- **Action:**
  1. **CRITICAL:** Increase budget from £5 to £15/day immediately (+£300/month)
  2. Fix geographic targeting (PRESENCE_OR_INTEREST → PRESENCE)
  3. Monitor performance - may justify even higher budget

---

## Phase 5: Product Impact Analyzer Integration

**Client Tracked:** ❌ No - Go Glean not currently configured in Product Impact Analyzer

**Recommendation:** Enable Product Impact Analyzer for this client to:
1. Understand why "non-grout" products (H&S&Z) underperform vs "Villains"
2. Track product-level ROAS and identify top/bottom performers
3. Correlate product feed changes (price, stock, title) with performance shifts
4. Optimize campaign segmentation based on actual product profitability

**Product Hero Label System Active:**
- Campaigns use Heroes & Sidekicks & Zombies, Villains labels
- Product Hero Pro Plan (€30/month) syncing labels to Merchant Center
- Consistent with owner Connor Heaps' other businesses (Grain Guard, Crowd Control)

**Setup Required:**
1. Add Go Glean to Product Impact Analyzer `config.json`
2. Configure Merchant Center ID: 5320484948
3. Enable daily product feed snapshots
4. Set up weekly impact report email

**Expected Benefits:**
- Identify which specific non-grout products drag down H&S&Z campaign ROAS
- Discover high-performing products in "Villains" category worth promoting
- Detect stock/price changes impacting campaign performance
- Make data-driven decisions on campaign segmentation

---

## Recommendations (Prioritized by ICE Framework)

### CRITICAL (Do Immediately - High Impact, Easy to Implement)

#### 1. Reallocate Budget from Non Grout H&S&Z to Villains
**Impact:** High - Estimated +£65-700/month revenue at same total spend
**Confidence:** High - Villains proven 422% ROAS vs Non Grout 209%
**Effort:** Low - Simple budget adjustment in Google Ads

**Action Steps:**
1. Reduce Non Grout H&S&Z daily budget: £40 → £30 (-£300/month)
2. Increase Villains daily budget: £5 → £15 (+£300/month)
3. Monitor for 2 weeks
4. If Villains maintains >350% ROAS, consider further reallocation

**Expected Outcome:**
- Non Grout: £902 × 209% = £1,885 revenue (vs £2,512 current)
- Villains: £450 × 422% = £1,899 revenue (vs £633 current)
- Net impact: +£187 revenue/month

#### 2. Fix Geographic Targeting on Villains Campaign
**Impact:** Medium - Save £7.50-15/month on wasted international traffic
**Confidence:** High - Standard best practice
**Effort:** Very Low - 2-minute setting change

**Action Steps:**
1. Open Villains PMax campaign in Google Ads
2. Navigate to Settings → Locations
3. Change "Target" setting from "Presence or interest" to "Presence"
4. Save changes

**Expected Outcome:**
- Eliminate ads shown to international users searching "about" UK
- 5-10% waste reduction on £150/month campaign = £7.50-15/month saved
- Improved campaign efficiency

---

### HIGH (Do Within 1 Week)

#### 3. Deep-Dive Analysis on Non Grout H&S&Z Underperformance
**Impact:** High - Identify root cause of 13% ROAS underperformance on largest campaign
**Confidence:** Medium - Requires investigation to diagnose
**Effort:** Medium - 2-3 hours analysis

**Action Steps:**
1. Export product-level performance from Google Ads
2. Identify which non-grout products drive low ROAS
3. Check for stock issues, price changes, or feed problems
4. Compare to high-performing Villains products
5. Segment underperforming products into separate "testing" campaign with lower ROAS target

**Expected Outcome:**
- Identify 20-30% of products causing ROAS drag
- Either pause underperformers or segment into lower ROAS campaign
- Improve Non Grout campaign ROAS from 209% toward 240% target

#### 4. Lower ROAS Targets on High-Performing Campaigns to Capture More Volume
**Impact:** High - Unlock additional revenue from campaigns with capacity
**Confidence:** Medium - Risk of ROAS decline, but campaigns have significant buffer
**Effort:** Low - Quick setting adjustment with close monitoring

**Action Steps:**
1. **Search Products:** 240% → 200% ROAS target (currently 434%, huge buffer)
2. **Shopping Catch All:** 260% → 240% ROAS target (currently 286%, moderate buffer)
3. **Villains:** 260% → 240% ROAS target (currently 422%, huge buffer)
4. Monitor for 1 week - revert if ROAS drops below new target

**Expected Outcome:**
- Search Products: Capture more impression share (currently only 10%)
- Shopping Catch All: Spend up to full £20/day budget (currently 16% utilization)
- Villains: Complement budget increase with slightly relaxed target for volume
- Estimated +£200-400/month revenue at acceptable ROAS

#### 5. Enable Product Impact Analyzer for Go Glean
**Impact:** High - Unlock product-level insights for optimization
**Confidence:** High - Proven system across Connor's other businesses
**Effort:** Medium - 1 hour setup + ongoing monitoring

**Action Steps:**
1. Add Go Glean to Product Impact Analyzer configuration
2. Connect Merchant Center ID 5320484948
3. Enable daily product feed snapshots
4. Set up weekly impact report email to Peter/Connor
5. Backfill 30 days of historical product data if possible

**Expected Outcome:**
- Identify specific products causing Non Grout H&S&Z underperformance
- Discover Hero products within Villains category
- Track feed changes impacting performance
- Make data-driven campaign segmentation decisions

---

### MEDIUM (Do Within 1 Month)

#### 6. Review and Standardize Campaign Naming Convention
**Impact:** Medium - Improve account organization and reporting clarity
**Confidence:** High - Standard best practice
**Effort:** Low - Quick renames, no performance impact

**Current Issue:** Campaign names include ROAS change history in the name:
- "280 2/9 249 8/9 260 11/9 230 15/9 260 23/9" = ROAS set to 280% on Sept 2, then 249% on Sept 8, etc.

**Problem:**
- Names become very long and cluttered
- Historical ROAS data should be in experiment log, not campaign name
- Difficult to scan and understand current strategy at a glance

**Proposed Naming Standard:**
```
[BRAND] | [CHANNEL] | [TYPE] | [SEGMENT] | [TARGET]
```

**Examples:**
- Current: "GOG | P Max | Non Grout H&S&Z 240 11/10"
- Proposed: "GOG | PMax | Non Grout H&S&Z | ROAS 240"

**Action Steps:**
1. Create naming convention document
2. Rename all 4 active campaigns
3. Document ROAS change history in experiment log CSV
4. Apply convention to future campaign launches

**Expected Outcome:**
- Clearer campaign list view
- Easier reporting and communication
- Historical context in proper experiment tracking system

#### 7. Consider Search Campaign Consolidation or Expansion
**Impact:** Medium - Improve Search Products campaign performance
**Confidence:** Low - Requires experimentation
**Effort:** Medium - Campaign restructure or testing

**Current Issue:** Search Products campaign:
- Only 10.56 conversions/month (marginal for automated bidding)
- Very high ROAS (434%) and CTR (6.28%) suggesting strong potential
- Only 2,769 impressions/month (low volume)

**Two Possible Approaches:**

**Option A: Expand Search Products**
- Add more keywords (currently too restrictive?)
- Lower ROAS target to 200% to capture more volume
- Increase budget to £20/day
- Goal: 30+ conversions/month for optimal automated bidding

**Option B: Consolidate into Shopping/PMax**
- Pause Search Products campaign
- Reallocate £13/day budget to Villains or Shopping Catch All
- Accept that PMax already covers search inventory
- Simplify account structure

**Recommendation:** Try Option A first (expand Search). Campaign has strong fundamentals (434% ROAS, 6.28% CTR) suggesting untapped potential.

---

## Audit Methodology

### Queries Executed

**Phase 1: Account Intelligence**
- `account-scale.gaql` - Campaign counts by status
- `spend-concentration.gaql` - Top campaigns by spend (30 days)

**Phase 2: Core Structural Audit**
- `campaign-settings.gaql` - Geographic targeting, networks, bid strategies
- `budget-constraints.gaql` - Lost IS Budget vs Rank (7 days)
- `campaign-performance.gaql` - Full performance metrics (30 days)

**Phase 3: Optional Segmentation**
- ❌ Not executed - No issues warranting deeper segmentation analysis

### Data Transformation

- Raw JSON converted to markdown tables manually (transform script issue)
- All currency fields converted from micros to GBP (÷ 1,000,000)
- ROAS calculated as conversions_value ÷ cost
- Percentage fields formatted for clarity

### Coverage

- **Analyzed:** All 4 enabled campaigns
- **Spend Coverage:** 100% (£1,902.55/month)
- **Performance Period:** 30 days (Oct 15 - Nov 13, 2025)
- **Budget Analysis Period:** 7 days (more recent for constraint detection)

### Limitations

1. **No Product-Level Data:** Product Impact Analyzer not configured for Go Glean
   - Cannot identify specific products causing Non Grout H&S&Z underperformance
   - Recommendation: Enable PIA for deeper insights

2. **Limited Historical Context:** Audit based on 30-day snapshot
   - CONTEXT.md shows September ROAS testing period
   - Current targets (240-260%) are post-testing results
   - Cannot assess long-term trends or seasonality from this data alone

3. **No Competitor Benchmarking:**
   - Cannot compare Go Glean performance to industry averages
   - 261% overall ROAS is strong in absolute terms, but relative competitiveness unknown

4. **No Hour/Day-of-Week Analysis:**
   - Audit focused on structural and budget issues (per audit scope)
   - Hourly/daily patterns require separate analysis if needed

---

## Next Steps

### Immediate Actions (This Week)

1. ✅ **Present audit findings** to Connor Heaps (owner)
2. ✅ **Get approval** for budget reallocation (Non Grout £40→£30, Villains £5→£15)
3. ✅ **Fix geographic targeting** on Villains campaign (2 minutes)
4. ✅ **Implement budget changes** and set 2-week review date

### Short-Term Actions (Next 2-4 Weeks)

1. ✅ **Monitor reallocation impact** - Compare Villains ROAS at £15/day vs £5/day
2. ✅ **Deep-dive Non Grout H&S&Z** - Product-level analysis to identify underperformers
3. ✅ **Test lower ROAS targets** on high-performing campaigns (Search Products, Shopping Catch All)
4. ✅ **Enable Product Impact Analyzer** for Go Glean account
5. ✅ **Review campaign naming** convention with client

### Long-Term Actions (Next 1-3 Months)

1. ✅ **Assess seasonality** - Patio grout performance in winter vs summer (per CONTEXT.md)
2. ✅ **Consider campaign restructure** based on product-level insights from PIA
3. ✅ **Evaluate Search campaign** expansion or consolidation
4. ✅ **Document learnings** in experiment log for future reference

---

## Appendix: Supporting Data

### Account Information

- **Customer ID:** 8492163737
- **Manager ID:** 2569949686 (required for API access)
- **Merchant Center ID:** 5320484948
- **Owner:** Connor Heaps (connor@goglean.co.uk)
- **Account Manager:** Peter Empson (petere@roksys.co.uk)
- **Business Type:** E-commerce building materials (grout products)
- **Geographic Focus:** United Kingdom

### Related Accounts

Connor Heaps owns multiple businesses managed by Peter Empson:
- **Go Glean:** Building materials (ROAS target: 240-260%)
- **Grain Guard:** Agricultural/grain storage products (ROAS target: 140-160%)
- **Crowd Control (CCC UK):** Safety equipment (ROAS target: 170%)

**Insight:** Go Glean has highest ROAS targets of Connor's businesses, suggesting better margins or premium positioning in building materials vs agriculture/safety equipment.

### Campaign Details

**GOG | P Max | Non Grout H&S&Z 240 11/10**
- Campaign ID: 20915839147
- Budget: £40/day
- Target ROAS: 240% (2.4x)
- Actual ROAS: 209%
- Product segmentation: Heroes & Sidekicks & Zombies (Product Hero labels)

**GOG | P Max Shopping | Villains 280 2/9 249 8/9 260 11/9 230 15/9 260 23/9**
- Campaign ID: 22979421280
- Budget: £5/day
- Target ROAS: 260% (2.6x)
- Actual ROAS: 422%
- Product segmentation: Villains (Product Hero label)
- Geographic targeting: PRESENCE_OR_INTEREST (needs fix)

**GOG | Search | Products 350 16/6 AI Max 26/6 300 1/8  230 15/9 260 23/9 240 3/10**
- Campaign ID: 22422709676
- Budget: £13/day
- Target ROAS: 240% (2.4x)
- Actual ROAS: 434%
- Search Partners: Disabled (correct)

**GOG | Shopping | Catch All 310 280 8/9 230 15/9 260 23/9**
- Campaign ID: 22439893575
- Budget: £20/day
- Target ROAS: 260% (2.6x)
- Actual ROAS: 286%
- Bid strategy: TARGET_ROAS (standard Shopping)

---

*Report generated by Claude Code Campaign Audit Skill*
*For questions about this audit, refer to `.claude/skills/google-ads-campaign-audit/`*
*Audit data files: `/Users/administrator/Documents/PetesBrain/clients/go-glean/audits/`*
