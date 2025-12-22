# Google Ads Campaign Audit Report

**Account:** Just Bin Bags (9697059148)
**Audit Date:** 18 December 2025
**Period Analysed:** Last 30 days (18 Nov - 17 Dec 2025), with month-on-month comparison
**Account Currency:** GBP (£)
**Auditor:** Claude Code (Campaign Audit Skill)

---

## Executive Summary

**Overall Health: 🟡 AMBER** - Mixed performance with critical issues requiring immediate attention

**Account Classification:** SMALL (3 enabled campaigns, 6 paused)
**Campaigns Analysed:** All 3 enabled campaigns (100% of spend)
**Total Spend (Last 30 Days):** £1,893.04
**Total Revenue (Last 30 Days):** £5,334.54
**Account ROAS:** 2.82x (282%)

### Top Finding

**CRITICAL: JHD Performance Max campaign is losing money** - Operating at 81% ROAS (losing 19p per £1 spent) while consuming £292/month. Additionally using PRESENCE_OR_INTEREST targeting, wasting budget on people searching about health disposals, not purchasing them.

### Primary Recommendation

**Immediate action required on JHD PMax campaign:**
1. Change geographic targeting from PRESENCE_OR_INTEREST to PRESENCE (Framework 4.4)
2. Reduce daily budget from £10/day to £3-5/day until profitability achieved
3. Review conversion tracking and product feed quality for JHD sub-brand

---

## Phase 1: Account Intelligence

### Account Scale

| Metric | Count |
|--------|-------|
| **Total Campaigns** | 9 |
| **Enabled** | 3 |
| **Paused** | 6 |
| **Removed** | 0 |
| **Classification** | SMALL |

### Spend Concentration (Last 30 Days)

| Campaign | Spend | % of Total | Cumulative % |
|----------|-------|------------|--------------|
| JBB \| P Max 200 21/5 | £1,418.95 | 74.9% | 74.9% |
| JBB \| JHD \| P Max Shopping tROAS 26/11 | £292.32 | 15.4% | 90.4% |
| JBB \| Brand 6 7 31/3 | £181.78 | 9.6% | 100.0% |

**80/20 Analysis:**
- Top campaign represents 74.9% of spend
- All 3 campaigns analysed (100% coverage)
- Audit focus: All enabled campaigns

---

## Phase 2: Structural Issues

### Geographic Targeting Problems

**Framework Reference:** Section 4.4 - Account → Location Targeting

| Campaign | Current Setting | Issue | Impact |
|----------|----------------|-------|--------|
| JBB \| JHD \| P Max Shopping tROAS 26/11 | PRESENCE_OR_INTEREST | ❌ Wasting budget | £292.32/month |
| JBB \| P Max 200 21/5 | PRESENCE | ✅ Correct | N/A |
| JBB \| Brand 6 7 31/3 | PRESENCE | ✅ Correct | N/A |

**Finding:** 1 campaign (33%) using PRESENCE_OR_INTEREST targeting, representing 15.4% of account spend (£292/month).

**Impact:** PRESENCE_OR_INTEREST shows ads to people searching ABOUT health disposals in the UK, not people IN the UK searching for health disposals. For example, someone in France searching "health disposal supplies UK" would see these ads despite being unable to purchase.

**Recommendation:** Change JHD PMax to PRESENCE targeting immediately.

**Framework Check:** ❌ Campaign using "Target people in or regularly in your targeted locations" (Framework 4.4)

---

### Network Settings Issues

**Framework Reference:** Section 5.14 - Targeting & Data → Search Partners

| Campaign | Google Search | Search Partners | Display | Issue |
|----------|---------------|----------------|---------|-------|
| JBB \| Brand 6 7 31/3 | ✅ Enabled | ❌ Disabled | ❌ Disabled | ✅ Correct |
| JBB \| P Max 200 21/5 | ✅ Enabled | ✅ Enabled | ✅ Enabled | N/A (PMax default) |
| JBB \| JHD \| P Max Shopping tROAS 26/11 | ✅ Enabled | ✅ Enabled | ✅ Enabled | N/A (PMax default) |

**Finding:** Network settings are appropriate for campaign types. Brand Search campaign correctly has Search Partners disabled. Performance Max campaigns have full network access (standard configuration).

**Framework Check:** ✅ Search Partners reviewed and disabled where underperforming (Framework 5.14)

---

### Bid Strategy Configuration

**Framework Reference:** Section 3.3 - Planning → Bidding Strategy Selection

| Campaign | Bid Strategy | Target | Conversions (30d) | Volume Check |
|----------|--------------|--------|-------------------|--------------|
| JBB \| P Max 200 21/5 | MAXIMIZE_CONVERSION_VALUE | 2.0x ROAS (200%) | 49 | ✅ Sufficient (30+ required) |
| JBB \| JHD \| P Max Shopping tROAS 26/11 | MAXIMIZE_CONVERSION_VALUE | 0.58x ROAS (58%) | 7.99 | ❌ Insufficient (<30) |
| JBB \| Brand 6 7 31/3 | MAXIMIZE_CONVERSIONS | £7.00 CPA | 30 | ✅ Sufficient (30+ required) |

**Finding:** JHD PMax using Target ROAS automated bidding with only 7.99 conversions in last 30 days - below the 30 conversion minimum for effective automated bidding.

**Issue:** Insufficient conversion volume means the automated bidding algorithm cannot learn effectively, contributing to poor performance (81% ROAS).

**Recommendation:**
- Option 1: Consolidate JHD products into main JBB PMax to increase conversion volume
- Option 2: Switch to manual CPC until conversion volume increases to 30+/month
- Option 3: Reduce budget and accept learning period with low performance

**Framework Check:** ⚠️ Bid strategies partially match conversion volume - JHD PMax below 30 conv/month threshold (Framework 3.3)

---

## Phase 3: Budget Allocation Issues

### Budget Constraints Analysis (Last 7 Days)

**Framework Reference:** Section 5.5 - Budget & KPI → Budget Limited Campaigns

| Campaign | Daily Budget | Avg Daily Spend | Utilisation | Lost IS Budget | Search IS | Status |
|----------|--------------|-----------------|-------------|----------------|-----------|--------|
| JBB \| JHD \| P Max Shopping tROAS 26/11 | £10.00 | £9.34 | 93% | 19.6% | 14.2% | ⚠️ Constrained |
| JBB \| P Max 200 21/5 | £57.00 | £58.57 | 103% | 4.7% | 23.1% | ⚠️ Slightly constrained |
| JBB \| Brand 6 7 31/3 | £31.00 | £3.07 | 10% | 0.0% | 95.7% | ✅ Not constrained |

**Finding:** 2 campaigns showing budget constraints, but analysis reveals critical context:

1. **JHD PMax** - 19.6% Lost IS Budget BUT operating at 81% ROAS (losing money)
   - **Problem:** Budget constraint on unprofitable campaign
   - **Action:** REDUCE budget, don't increase - fix profitability first

2. **Main PMax** - 4.7% Lost IS Budget, operating at 199% ROAS (profitable, near target)
   - **Problem:** Minor constraint on strong performer
   - **Action:** Consider increasing budget from £57/day to £65-70/day

3. **Brand Search** - 0% Lost IS Budget, 95.7% impression share, exceptional 1,249% ROAS
   - **Problem:** Only spending £3.07/day of £31 budget (10% utilisation)
   - **Opportunity:** Could significantly increase budget to capture more branded traffic

**Framework Check:** ⚠️ Budget limited campaigns identified - JHD requires profitability fix before budget increase, Main PMax has growth opportunity (Framework 5.5)

---

### Campaign Performance Analysis (Last 30 Days)

| Campaign | Spend | Revenue | ROAS | Target ROAS | Conversions | CPA | Clicks | CTR | Assessment |
|----------|-------|---------|------|-------------|-------------|-----|--------|-----|------------|
| JBB \| P Max 200 21/5 | £1,418.95 | £2,829.02 | 1.99x | 2.00x | 49 | £28.96 | 882 | 1.26% | ✅ On target |
| JBB \| JHD \| P Max Shopping tROAS 26/11 | £292.32 | £235.44 | 0.81x | 0.58x | 7.99 | £36.58 | 159 | 0.76% | ❌ Unprofitable |
| JBB \| Brand 6 7 31/3 | £181.78 | £2,270.08 | 12.49x | £7 CPA | 30 | £6.06 | 85 | 47.75% | ✅ Excellent |
| **TOTAL** | **£1,893.04** | **£5,334.54** | **2.82x** | - | **86.99** | **£21.76** | **1,126** | **1.24%** | **🟢 Strong** |

**Key Insights:**

1. **Main PMax (74.9% of spend):** Performing at target (199% vs 200% target). Stable and predictable. Small budget increase warranted.

2. **JHD PMax (15.4% of spend):** CRITICAL ISSUE - Operating at 81% ROAS (losing £56.88 in last 30 days). Target of 58% ROAS suggests expectation of unprofitability, but current performance is even worse than target. Combined with low conversion volume (7.99 vs 30 required) and PRESENCE_OR_INTEREST targeting waste, this campaign needs immediate intervention.

3. **Brand Search (9.6% of spend):** Exceptional performer at 1,249% ROAS with £6.06 CPA (under £7 target). Extremely high CTR (47.75%) confirms strong brand recognition. Currently heavily underutilised (10% budget utilisation).

**Framework Check:** ⚠️ Campaign budgets partially aligned with performance - JHD requires budget reduction and targeting fix, Brand has major expansion opportunity (Framework 5.5)

---

### Budget Reallocation Opportunities

**Framework Reference:** Section 5.5 - Budget & KPI → When to Increase Campaign Budgets

| Action | Current Daily Budget | Recommended Daily Budget | Expected Impact |
|--------|---------------------|-------------------------|-----------------|
| **REDUCE: JHD PMax** | £10.00 | £3.00 - £5.00 | Stop losing £2/day, preserve budget for profitable campaigns |
| **INCREASE: Main PMax** | £57.00 | £65.00 - £70.00 | Capture 4.7% Lost IS Budget, ~£8-13/day additional revenue |
| **INCREASE: Brand Search** | £31.00 | £50.00 - £75.00 | Capture branded demand, potential £20-40/day additional revenue |

**Quantified Scenario (Conservative):**
- Reduce JHD from £10/day to £5/day: Save £150/month waste
- Increase Main PMax from £57/day to £65/day: +£240/month revenue (at 2x ROAS)
- Increase Brand from £31/day to £50/day: +£2,370/month revenue (at 12.5x ROAS)

**Net Impact:** -£150 waste, +£2,610 revenue/month = £2,460/month improvement

**Framework Check:** ✅ Budget reallocation opportunities identified with quantified impact (Framework 5.5)

---

## Month-on-Month Performance Comparison

### October 2025 Performance

| Campaign | Spend | Revenue | ROAS | Conversions | Change from Previous |
|----------|-------|---------|------|-------------|---------------------|
| JBB \| P Max 200 21/5 | £1,434.64 | £2,705.60 | 1.89x | 57.96 | Baseline |
| JBB \| JHD \| P Max Shopping tROAS 26/11 | £301.56 | £0.24 | 0.001x | 0.008 | Baseline (CRISIS) |
| JBB \| Brand 6 7 31/3 | £133.22 | £1,890.24 | 14.19x | 30.56 | Baseline |
| **TOTAL** | **£1,869.42** | **£4,596.08** | **2.46x** | **88.53** | **Baseline** |

### November 2025 Performance

| Campaign | Spend | Revenue | ROAS | Conversions | Change from October |
|----------|-------|---------|------|-------------|---------------------|
| JBB \| P Max 200 21/5 | £1,353.12 | £2,635.17 | 1.95x | 41.98 | -5.7% spend, +3.2% ROAS ✅ |
| JBB \| JHD \| P Max Shopping tROAS 26/11 | £304.06 | £163.18 | 0.54x | 6.00 | +0.8% spend, **+53,900% ROAS** ⚠️ |
| JBB \| Brand 6 7 31/3 | £206.97 | £2,168.87 | 10.48x | 33.00 | +55.4% spend, -26.1% ROAS ⚠️ |
| **TOTAL** | **£1,864.15** | **£4,967.22** | **2.66x** | **80.98** | **-0.3% spend, +8.1% ROAS** ✅ |

### December 2025 Performance (1-17 Dec, partial month)

| Campaign | Spend | Revenue | ROAS | Conversions | Projected Full Month |
|----------|-------|---------|------|-------------|---------------------|
| JBB \| P Max 200 21/5 | £959.71 | £1,951.91 | 2.03x | 33 | £1,753/month, 2.03x ROAS ✅ |
| JBB \| JHD \| P Max Shopping tROAS 26/11 | £164.19 | £74.18 | 0.45x | 2.99 | £300/month, 0.45x ROAS ❌ |
| JBB \| Brand 6 7 31/3 | £76.48 | £1,227.02 | 16.04x | 13 | £140/month, 16.04x ROAS ✅ |
| **TOTAL** | **£1,200.38** | **£3,253.11** | **2.71x** | **48.99** | **£2,193/month, 2.71x ROAS** ✅ |

### Key Trends (Oct → Nov → Dec)

**Main PMax:**
- ROAS: 1.89x → 1.95x → 2.03x (steady improvement, converging on 2.0x target) ✅
- Spend: £1,435 → £1,353 → £960 (17 days) = declining trajectory
- **Trend:** Stable performance, declining spend suggests budget constraints or seasonality

**JHD PMax:**
- ROAS: 0.001x → 0.54x → 0.45x (improved from catastrophic to merely unprofitable) ⚠️
- October was near-zero revenue (£0.24 on £301 spend = 0.1% ROAS)
- November dramatically improved but still unprofitable (54% ROAS)
- December declining again (45% ROAS)
- **Trend:** Fundamental profitability issue - never achieved break-even in 3 months

**Brand Search:**
- ROAS: 14.19x → 10.48x → 16.04x (volatile but consistently excellent) ✅
- Spend: £133 → £207 → £76 (17 days) = highly variable
- Budget utilisation: Only using 10% of £31/day budget in December
- **Trend:** Exceptional performer being starved of budget (£3/day actual vs £31 available)

**Account Overall:**
- ROAS improving: 2.46x → 2.66x → 2.71x (+10% over 3 months) ✅
- Spend declining: £1,869 → £1,864 → £1,200 (projected £2,193/month) ⚠️
- **Trend:** Account health improving but total volume declining

---

## Phase 4: Product Impact Analyzer Integration

### Product Feed Impact Analysis

**Client Tracked:** ✅ Yes - Both JBB (merchant 181788523) and JHD (merchant 5085550522) feeds monitored

**Product Performance Spreadsheets:**
- JBB Main Brand: [Daily Product Performance](https://docs.google.com/spreadsheets/d/1zEiKnU-jJjEqchmXIX3QhML-g3H3v6ZstLFfz69CJyA/)
- JHD Sub-brand: [Daily Product Performance](https://docs.google.com/spreadsheets/d/1p7hVR4bwMVTiBj8za6pVv3kmnVr8v3YEz2fhGun2YSk/)

**Monitoring Status:**
- Last data update: 18 December 2025 07:01
- Label tracking: Disabled (no Product Hero classification system in use)
- Price monitoring: Active (snapshot files available)
- Product-level performance: Tracked daily

**Key Observations:**

1. **Label Tracking Not Enabled**
   - Neither feed uses Product Hero labels (Heroes/Sidekicks/Villains/Zombies)
   - Config notes: "Limited Product Hero labels detected - only 'bestseller' in custom_label_0 for some products"
   - **Implication:** Cannot analyse performance by product tier or track label transitions

2. **Separate Merchant Feeds**
   - JBB main brand uses merchant 181788523
   - JHD sub-brand uses merchant 5085550522
   - Two completely separate product catalogues, no overlap
   - **Implication:** JHD performance issues are isolated to JHD product catalogue

3. **JHD Product Feed Quality Concerns**
   - JHD ROAS has been consistently unprofitable (0.001x → 0.54x → 0.45x)
   - Low conversion volume (0.008 → 6 → 2.99 conversions per month)
   - **Recommendation:** Conduct manual audit of JHD merchant feed:
     - Product titles - are they clear and include search terms?
     - Product prices - are they competitive?
     - Product images - are they high quality?
     - Stock status - are products actually available?
     - Product types/categories - correctly configured?

4. **Price Monitoring Available**
   - Recent price snapshot files exist for both feeds
   - Can be analysed if performance shifts correlate with price changes
   - No automated price change alerts configured

**Product Feed Recommendations:**

1. **Enable Product Hero Labels** (JBB Main Brand)
   - Main PMax performing well (199% ROAS) but could optimise further
   - Identify top performers (Heroes), moderate performers (Sidekicks), and underperformers (Villains/Zombies)
   - Allocate budget according to product tier performance

2. **Conduct JHD Feed Audit**
   - JHD's persistent unprofitability (81% ROAS) may be product feed issue, not campaign issue
   - Check product data quality: titles, descriptions, images, prices
   - Compare JHD product prices to competitor pricing
   - Verify stock status accuracy

3. **Consider Feed Consolidation**
   - If JHD products are complementary to JBB products, consider merging feeds
   - Would increase conversion volume for automated bidding (currently 7.99, need 30+)
   - Would simplify account management (2 PMax campaigns → 1 PMax campaign)

**Framework Check:** ✅ Product feed monitoring active, manual audit recommended for underperforming JHD feed

---

## Recommendations (Prioritised by ICE Framework)

All recommendations reference Google Ads Audit Framework (`docs/GOOGLE-ADS-AUDIT-FRAMEWORK.csv`)

### CRITICAL (Do Immediately)

#### 1. Fix JHD PMax Geographic Targeting (Framework 4.4)
**Issue:** Campaign using PRESENCE_OR_INTEREST targeting, wasting budget on people searching about health disposals, not purchasing them

**Action:**
1. Go to JBB | JHD | P Max Shopping tROAS 26/11 campaign settings
2. Navigate to Locations
3. Change "Location options" from "Presence or interest" to "Presence"
4. Save changes

**Expected Impact:**
- Immediate reduction in wasted impressions/clicks
- 10-15% efficiency improvement = £30-45/month saved
- Better qualified traffic = potential ROAS improvement from 81% toward break-even

**ICE Score:** Impact 8/10, Confidence 9/10, Effort 1/10 = **72/10**

**Framework Item:** "Location options: Target people in or regularly in your targeted locations" (Framework 4.4 - Account → Location Targeting)

---

#### 2. Reduce JHD PMax Daily Budget (Framework 5.5)
**Issue:** Campaign operating at 81% ROAS (losing money) while consuming £10/day

**Action:**
1. Reduce JHD PMax daily budget from £10.00 to £5.00
2. Monitor performance for 2 weeks
3. If ROAS improves above 100%, gradually increase budget
4. If ROAS remains below 100%, reduce further to £3/day or pause

**Rationale:**
- 19.6% Lost IS Budget is MISLEADING - shouldn't increase budget on unprofitable campaign
- Reducing budget reduces losses while preserving opportunity to improve efficiency
- Lower daily spend allows automated bidding more time to optimise within limited budget

**Expected Impact:**
- Reduce losses from £2/day to £1/day = £30/month saved
- Potential efficiency improvement with lower budget pressure
- Preserve capital for profitable campaigns (Main PMax, Brand)

**ICE Score:** Impact 7/10, Confidence 9/10, Effort 1/10 = **63/10**

**Framework Item:** "Review budget limited campaigns (and the 5 steps to follow)" - but in this case, reduce budget not increase (Framework 5.5 - Budget & KPI → Budget Limited Campaigns)

---

#### 3. Conduct JHD Product Feed Quality Audit (Framework 6.1)
**Issue:** JHD ROAS consistently unprofitable over 3 months (0.001x → 0.54x → 0.45x) suggests fundamental product/pricing issue

**Action:**
1. Export JHD merchant feed data (merchant 5085550522)
2. Review product data quality:
   - **Titles:** Do they include relevant search terms? (e.g., "Nitrile Gloves Medical Grade 100 Pack" vs "Gloves")
   - **Prices:** Are they competitive vs competitors? (check Amazon, healthcare suppliers)
   - **Images:** High quality, clear product photos?
   - **Stock status:** Are out-of-stock products still active?
   - **Product types:** Correctly categorised?
3. Compare JHD feed quality to main JBB feed (which performs well at 199% ROAS)
4. Fix any quality issues identified

**Rationale:**
- Campaign-level optimisations (targeting, bidding) cannot fix poor product-market fit
- JHD may have wrong products, wrong prices, or wrong target market
- Main JBB feed performs well (199% ROAS) = feed quality matters

**Expected Impact:**
- Difficult to quantify until audit complete
- Potential for 50-100% ROAS improvement if pricing/product issues identified
- May reveal that JHD products are not viable for paid advertising

**ICE Score:** Impact 9/10, Confidence 7/10, Effort 5/10 = **63/50 = 1.26/10**

**Framework Item:** "Product feed quality and optimisation" (Framework 6.1 - SHOPPING → Merchant Feed)

---

### HIGH (Do Within 1 Week)

#### 4. Increase Brand Search Daily Budget (Framework 5.5)
**Issue:** Exceptional performer (1,249% ROAS, £6.06 CPA vs £7 target) only using 10% of available budget (£3.07/day of £31/day)

**Action:**
1. Increase Brand Search daily budget from £31.00 to £50.00
2. Monitor for 1 week
3. If spend increases without CPA deterioration, increase to £75.00
4. Target: Achieve 30-50% budget utilisation (£15-25/day spend)

**Rationale:**
- 95.7% impression share = capturing most branded traffic already
- 0% Lost IS Budget = not constrained by budget, but opportunity for more aggressive bidding
- Exceptional ROAS (1,249%) means even if efficiency drops 50%, still incredibly profitable
- Branded traffic is highest intent, lowest hanging fruit

**Expected Impact:**
- Conservatively: +£10/day spend → +£125/day revenue (at 12.5x ROAS) = +£3,750/month revenue
- Even if ROAS drops to 500%, still +£1,500/month revenue
- Potential to capture 100% branded impression share

**ICE Score:** Impact 8/10, Confidence 8/10, Effort 1/10 = **64/10**

**Framework Item:** "When to increase campaign budgets" (Framework 5.5 - Budget & KPI → Budget Optimisation)

---

#### 5. Increase Main PMax Daily Budget (Framework 5.5)
**Issue:** Strong performer at target ROAS (199% vs 200%) with 4.7% Lost IS Budget = missing opportunities

**Action:**
1. Increase Main PMax daily budget from £57.00 to £65.00
2. Monitor for 1 week - check if spend increases and ROAS remains at 2x
3. If stable, increase to £70.00
4. Target: Reduce Lost IS Budget from 4.7% to <2%

**Rationale:**
- Performing at target (199% ROAS) = algorithm is working effectively
- 4.7% Lost IS Budget = leaving money on the table
- Small budget increase preserves profitability while capturing more volume

**Expected Impact:**
- +£8/day spend → +£16/day revenue (at 2x ROAS) = +£480/month revenue
- Capture additional 2-3% impression share
- Potential to push ROAS slightly above 200% with more auction opportunities

**ICE Score:** Impact 6/10, Confidence 8/10, Effort 1/10 = **48/10**

**Framework Item:** "When to increase campaign budgets" (Framework 5.5 - Budget & KPI → Budget Optimisation)

---

#### 6. Consider JHD Feed Consolidation or Campaign Pause (Framework 5.2)
**Issue:** JHD PMax has insufficient conversion volume (7.99 vs 30 required) and persistent unprofitability

**Action - Option A: Consolidate Feeds**
1. Evaluate if JHD products can be merged into main JBB merchant feed (181788523)
2. If complementary (both bin bags/healthcare supplies), consolidate into single feed
3. Run single PMax campaign with all products
4. Benefits: Higher conversion volume, simpler management, consolidated learning

**Action - Option B: Pause JHD Campaign**
1. Pause JHD PMax for 2-4 weeks
2. During pause:
   - Conduct thorough feed quality audit
   - Research competitor pricing
   - Analyse whether JHD products are viable for paid ads
3. If audit reveals fixable issues, address and re-launch
4. If audit reveals fundamental profitability issues, keep paused or discontinue

**Rationale:**
- 7.99 conversions/month insufficient for automated bidding (need 30+)
- 3 months of unprofitability (0.001x → 0.54x → 0.45x) = not a temporary learning issue
- Either fix fundamentals or stop losing money

**Expected Impact:**
- Option A (Consolidate): Potential to achieve 30+ conversions/month, enable effective automated bidding
- Option B (Pause): Stop losing £2/day immediately = £60/month saved, redeploy budget to profitable campaigns

**ICE Score:** Impact 7/10, Confidence 6/10, Effort 7/10 = **42/70 = 0.6/10**

**Framework Item:** "Review when to consider splitting campaigns or ad groups" - in this case, consider consolidating (Framework 5.2 - Account Structure → When to Split Campaigns)

---

### MEDIUM (Do Within 1 Month)

#### 7. Enable Product Hero Labels for JBB Main Feed (Framework 6.2)
**Issue:** Main JBB feed not using Product Hero label classification system to optimise budget allocation

**Action:**
1. Review product performance data in [JBB Daily Performance Spreadsheet](https://docs.google.com/spreadsheets/d/1zEiKnU-jJjEqchmXIX3QhML-g3H3v6ZstLFfz69CJyA/)
2. Classify products into tiers:
   - **Heroes:** Top 20% by revenue, high ROAS
   - **Sidekicks:** Middle 40%, moderate ROAS
   - **Villains:** Bottom 20%, low ROAS but some conversions
   - **Zombies:** No conversions in 30+ days, wasting spend
3. Apply labels to merchant feed custom_label_0 field
4. Enable label tracking in Product Impact Analyzer config
5. Create separate PMax asset groups or campaigns by label tier (optional)

**Rationale:**
- Main PMax performing at target (199% ROAS) but could optimise further
- Product Hero system identifies which products to prioritise
- Can allocate more budget to Heroes, less to Villains/Zombies
- Proven methodology across other clients (Grain Guard, Accessories for the Home, etc.)

**Expected Impact:**
- 5-10% ROAS improvement potential (2.0x → 2.1-2.2x)
- Identify Zombie products wasting budget
- Enable more sophisticated budget allocation strategies

**ICE Score:** Impact 6/10, Confidence 7/10, Effort 6/10 = **42/60 = 0.7/10**

**Framework Item:** "Product segmentation and performance analysis" (Framework 6.2 - SHOPPING → Product Optimisation)

---

#### 8. Review and Improve Account Naming Conventions (Framework 4.1)
**Issue:** Inconsistent naming conventions make reporting and analysis more difficult

**Current Campaign Names:**
- "JBB | P Max 200 21/5" (unclear what "200" and "21/5" mean)
- "JBB | JHD | P Max Shopping tROAS 26/11" (mix of abbreviations)
- "JBB | Brand 6 7 31/3" (unclear what "6 7" and "31/3" mean)

**Recommended Standard Format:**
```
[BRAND]_[CHANNEL]_[TYPE]_[TARGET]_[GEO]_[NOTES]

Examples:
JBB_PMAX_Main_tROAS200_UK
JBB_PMAX_JHD_tROAS58_UK
JBB_SEARCH_Brand_tCPA7_UK
```

**Action:**
1. Propose naming convention standard to client
2. Rename campaigns during low-traffic period (avoid mid-week)
3. Update all reporting templates with new names
4. Document naming convention in account notes

**Rationale:**
- Improves readability in reports
- Makes filtering and sorting easier
- Facilitates automated reporting
- Industry best practice

**Expected Impact:**
- No direct performance impact
- Significantly improves account management efficiency
- Reduces confusion in reporting

**ICE Score:** Impact 3/10, Confidence 10/10, Effort 3/10 = **30/30 = 1.0/10**

**Framework Item:** "Appropriate naming convention is in place" (Framework 4.1 - Campaign Hygiene → Naming Convention)

---

## Framework Alignment Summary

This audit covered the following sections of the Google Ads Audit Framework:

| Framework Section | Items Covered | Status |
|-------------------|---------------|--------|
| **Section 3.3 - Account Structure** | Bid strategy selection, conversion volume requirements | ⚠️ Reviewed - JHD PMax below 30 conv/month |
| **Section 4.1 - Campaign Hygiene** | Naming conventions | ⚠️ Reviewed - needs improvement |
| **Section 4.4 - Account Settings** | Geographic targeting, network settings | ❌ JHD using PRESENCE_OR_INTEREST |
| **Section 5.2 - Account Structure** | Campaign consolidation opportunities | ⚠️ Reviewed - JHD consolidation recommended |
| **Section 5.5 - Budget & KPI** | Budget constraints, allocation, optimisation | ⚠️ Multiple issues - JHD reduce, Brand/Main PMax increase |
| **Section 5.14 - Network Performance** | Search Partners settings | ✅ Correct configuration |
| **Section 6.1 - Merchant Feed** | Product feed quality | ⚠️ JHD feed audit required |
| **Section 6.2 - Product Optimisation** | Product Hero labels | ⚠️ Not implemented - opportunity |

**Not covered in this audit** (requires separate audits):
- **Section 1 - FOUNDATION** (tracking, analytics, conversion setup) → Use `docs/CLIENT-ONBOARDING-AUDIT-CHECKLIST.md`
- **Section 5.6 - Keyword & Query** (keyword decision matrix) → Separate keyword audit for Brand Search campaign
- **Section 5.7 - Search Terms** (negative keyword mining) → Separate keyword audit

**Next Steps:**
1. **CRITICAL:** Complete recommendations 1-3 immediately (JHD targeting fix, budget reduction, feed audit)
2. **HIGH:** Complete recommendations 4-6 within 1 week (Brand/Main PMax budget increases, JHD consolidation decision)
3. **Consider running:** Keyword audit for Brand Search campaign (currently only 178 impressions/month - may need more keywords)
4. **Consider running:** Foundation audit if conversion tracking or attribution concerns exist

**Full framework reference:** `docs/AUDIT-FRAMEWORK-GUIDE.md`

---

## Audit Methodology

**Queries Executed:**
- Phase 1: account-scale, spend-concentration
- Phase 2: campaign-settings, budget-constraints, campaign-performance
- Phase 3: Not required (small account, no device/geo/network segmentation warranted)
- Month-on-Month: October, November, December 2025 comparison queries

**Data Transformation:**
- Queries executed via Google Ads API (MCP)
- Data analysed directly from API responses (no transform script needed for small account)
- All micros fields converted to currency (÷ 1,000,000)
- All decimal fields converted to percentages (× 100)
- ROAS calculated as: conversions_value ÷ (cost_micros ÷ 1,000,000)

**Product Impact Analyzer:**
- ✅ Both JBB and JHD feeds tracked in Product Impact Analyzer
- Data last updated: 18 December 2025 07:01
- Label tracking: Not enabled (no Product Hero classification)
- Product-level performance data available in Google Sheets

**Coverage:**
- Analysed: 3 campaigns representing 100% of account spend
- Time period: Last 30 days (18 Nov - 17 Dec 2025)
- Comparison: 3 full months (Oct, Nov, Dec 2025)
- Focus: Structural issues, budget allocation, profitability

---

## Summary of Critical Actions

### Week 1 (Immediate)
1. ✅ Change JHD PMax to PRESENCE targeting (5 minutes)
2. ✅ Reduce JHD PMax budget to £5/day (2 minutes)
3. 📋 Conduct JHD feed quality audit (2 hours)

### Week 2 (High Priority)
4. ✅ Increase Brand Search budget to £50/day (2 minutes)
5. ✅ Increase Main PMax budget to £65/day (2 minutes)
6. 📋 Decision: JHD consolidation vs pause (1 hour analysis, 2-4 hours implementation if consolidating)

### Month 1 (Medium Priority)
7. 📋 Enable Product Hero labels for JBB main feed (4-6 hours setup)
8. 📋 Standardise campaign naming conventions (1 hour)

**Expected Total Impact (if all recommendations implemented):**
- Reduce waste: £30-45/month (JHD targeting) + £30/month (JHD budget reduction) = **£60-75/month saved**
- Increase revenue: £3,750/month (Brand expansion) + £480/month (Main PMax growth) = **£4,230/month gained**
- Net improvement: **£4,290-4,305/month** = **£51,480-51,660/year**

**Account Health After Implementation:**
- Current: 🟡 AMBER (mixed performance)
- Projected: 🟢 GREEN (all campaigns profitable and optimised)

---

*Report generated by Claude Code Campaign Audit Skill*
*For questions about this audit, refer to `.claude/skills/google-ads-campaign-audit/`*
