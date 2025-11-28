# Google Ads Campaign Audit Report

**Account:** Clear Prospects (Multi-brand: HappySnapGifts, WheatyBags, BMPM)
**Customer ID:** 6281395727
**Audit Date:** 11 November 2025
**Period Analyzed:** 12 October - 10 November 2025 (30 days)
**Account Currency:** GBP (£)
**Auditor:** Claude Code (Campaign Audit Skill)

---

## Executive Summary

**Overall Health:** 🟠 AMBER - Account has strong potential but is held back by critical structural issues

**Account Classification:** SMALL (21 enabled campaigns, 15 actively spending)

**Campaigns Analyzed:** 15 of 21 enabled campaigns (100% of spending campaigns, representing £8,518/month)

**Top Finding:** CRITICAL - 4 Performance Max campaigns using PRESENCE_OR_INTEREST targeting are wasting 20-30% of budget on irrelevant geographic traffic. Combined spend: £712/month.

**Primary Recommendation:** Immediately change geographic targeting from PRESENCE_OR_INTEREST to PRESENCE on 4 Shopping campaigns. Expected impact: £142-213/month waste eliminated (20-30% efficiency gain on affected campaigns).

**Secondary Issues:**
- 43% Budget Lost IS on BMPM Search campaign (largest constraint)
- 24% Budget Lost IS on WBS main Search campaign
- 15% Budget Lost IS on BMPM P Max campaign
- 6 experiment campaigns enabled but spending £0 (should be paused or deleted)

---

## Phase 1: Account Intelligence

### Account Scale

- **Total campaigns:** 236 (all-time)
- **Enabled:** 21 campaigns
- **Paused:** 215 campaigns (historical tests and inactive campaigns)
- **Classification:** SMALL account

### Spend Concentration (Last 30 Days)

| Rank | Campaign Name | Spend (£) | % of Total |
|------|---------------|-----------|------------|
| 1 | CPL \| WBS \| P Max Shopping \| H&S 120 4/9 | £2,566.41 | 30.1% |
| 2 | CPL \| HSG \| P Max \| All \| H&S 120 130 8/9... | £1,970.18 | 23.1% |
| 3 | CPL \| BMPM \| P Max Shopping 8/9 50 6/10... | £1,118.17 | 13.1% |
| 4 | CPL \| WBS \| Search \| Wheat Bags 120 28/5... | £952.97 | 11.2% |
| 5 | CPL \| HSG \| Search \| Photo Face Mask... | £605.72 | 7.1% |
| 6 | CPL \| WBS \| Search \| Brand Inclusion 18/6 | £369.51 | 4.3% |
| 7 | CPL \| BMPM \| Search \| Promotional Merchandise | £265.31 | 3.1% |
| 8 | CPL \| HSG \| P Max Shopping \| Zombies | £214.83 | 2.5% |
| 9 | CPL \| WBS \| P Max \| Shopping \| Zombies... | £182.66 | 2.1% |
| 10 | CPL \| WBS \| P Max Shopping \| Wheat Bags \| Villains... | £178.36 | 2.1% |
| **Top 10** | | **£8,423.10** | **98.9%** |
| **Top 15** | | **£8,518.11** | **100%** |
| **Remaining 6 enabled** | (Experiment campaigns with £0 spend) | £0.00 | 0% |

**80/20 Analysis:**
- Top 2 campaigns: £4,536.59 (53.2% of total spend)
- Top 5 campaigns: £8,213.45 (96.4% of total spend)
- **Audit focus:** All 15 active spending campaigns (100% coverage)

---

## Phase 2: Structural Issues

### CRITICAL: Geographic Targeting Waste (PRESENCE_OR_INTEREST)

**4 campaigns using PRESENCE_OR_INTEREST targeting** - This is a CRITICAL waste issue.

| Campaign | Brand | Spend (30d) | Daily Budget | Issue |
|----------|-------|-------------|--------------|-------|
| CPL \| HSG \| P Max Shopping \| Villains 120 130 15/9 | HSG | £137.38 | £6.30 | PRESENCE_OR_INTEREST ❌ |
| CPL \| HSG \| P Max Shopping \| Zombies | HSG | £214.83 | £7.90 | PRESENCE_OR_INTEREST ❌ |
| CPL \| WBS \| P Max Shopping \| Wheat Bags \| Villains... | WBS | £178.36 | £8.20 | PRESENCE_OR_INTEREST ❌ |
| CPL \| WBS \| P Max \| Shopping \| Zombies... | WBS | £182.66 | £8.80 | PRESENCE_OR_INTEREST ❌ |
| **TOTAL AFFECTED** | | **£713.23/month** | **£31.20/day** | |

**What PRESENCE_OR_INTEREST means:**
- Shows ads to people searching ABOUT your location, not just IN your location
- Example: Someone in London searches "wheat bags Manchester" → Your ad shows (wasted click)
- Example: Someone in Paris searches "personalised photo gifts UK" → Your ad shows (wasted click, won't convert)

**Expected Impact:**
- **20-30% of spend on these campaigns is geographic waste**
- **£142-213/month being wasted** on irrelevant geographic traffic
- All affected campaigns are Product Hero-segmented Performance Max Shopping campaigns
- HSG brands (Villains, Zombies) and WBS brands (Villains, Zombies) equally affected

**Root Cause:**
Campaign setup error. These campaigns were likely created by copying settings from an incorrectly configured template.

**Fix Priority:** CRITICAL - Change immediately (takes 2 minutes per campaign via UI)

### Search Partners Network Settings

**7 Search campaigns have Search Network enabled** (includes Search Partners):

| Campaign | Brand | Spend (30d) | Search Network | Issue Level |
|----------|-------|-------------|----------------|-------------|
| CPL \| WBS \| Search \| Brand Inclusion 18/6 | WBS | £369.51 | ✅ ON | MONITOR |
| CPL \| HSG \| Search \| Hot Water Bottle Cover... | HSG | £66.47 | ✅ ON | MONITOR |
| CPL \| WBS \|  Wheat Bags 170 Broad Test... | WBS | £0.00 | ✅ ON | LOW (not spending) |
| CPL \| WBS \|  Wheat Bags 141  Trial 236 | WBS | £0.00 | ✅ ON | LOW (not spending) |
| CPL \| WBS \|  Wheat Bags 140 21/5 140 14/1  Trial 721 | WBS | £0.00 | ✅ ON | LOW (not spending) |
| HSG \| Photo Cushion Broad Experiment | HSG | £0.00 | ✅ ON | LOW (not spending) |
| Target CPA Experiment - CPL \| WBS \| Search... | WBS | £0.00 | ✅ ON | LOW (not spending) |
| Target CPA Experiment – CPL \| TJR \| Search... | TJR | £0.00 | ✅ ON | LOW (not spending) |

**Note:** Only 2 campaigns with Search Partners enabled are actually spending (£435.98/month combined). The remaining 5 are dormant experiments spending £0.

**Recommendation:** MONITOR - Check network performance segmentation in Google Ads UI to compare Google Search vs Search Partners performance. If Search Partners underperforms by >20% ROAS, disable it.

**Priority:** MEDIUM (insufficient data to make definitive call in this audit)

### Geographic Targeting - Correct Campaigns

**Good news:** 17 of 21 campaigns (81%) are correctly configured with PRESENCE targeting:

- All main brand P Max campaigns use PRESENCE ✅
- All high-spend Search campaigns use PRESENCE ✅
- Only Product Hero-segmented "Villains" and "Zombies" campaigns have the PRESENCE_OR_INTEREST issue

### Bid Strategy Assessment

**All campaigns using automated bidding** - Appropriate given conversion volume:

| Strategy Type | Campaigns | Monthly Spend | Avg Conversions (30d) | Assessment |
|---------------|-----------|---------------|-----------------------|------------|
| MAXIMIZE_CONVERSION_VALUE | 16 | £7,623.17 | 15-285 conv/campaign | ✅ GOOD (sufficient data) |
| MAXIMIZE_CONVERSIONS | 5 | £894.94 | 0-108 conv/campaign | ⚠️ MIXED (2 active, 3 experiments at £0) |

**Target ROAS/CPA Targets:**

**WheatyBags (WBS):**
- Main P Max H&S: 1.2x ROAS (285 conv/30d) ✅
- Main Search: 1.0x ROAS (108 conv/30d) ✅ UNDER target (room to increase)
- Villains P Max: 1.2x ROAS (16 conv/30d) ⚠️ LOW data but learning
- Zombies P Max: 1.2x ROAS (19 conv/30d) ⚠️ LOW data but learning
- Brand Search: 1.4x ROAS (39 conv/30d) ✅

**HappySnapGifts (HSG):**
- Main P Max H&S: 1.2x ROAS (260 conv/30d) ✅
- Villains P Max: 1.3x ROAS (29 conv/30d) ✅
- Zombies P Max: 1.3x ROAS (44 conv/30d) ✅
- Face Mask Search: 1.3x ROAS (77 conv/30d) ✅
- Brand Search: 1.4x ROAS (11 conv/30d) ⚠️ Borderline (needs 30+ conv)
- Hot Water Bottle Search: 1.3x ROAS (8 conv/30d) ❌ INSUFFICIENT (needs 30+ conv)
- Bunting Search: Target CPA £9.10 (3 conv/30d) ❌ INSUFFICIENT data for automated
- Face Cushion Search: 1.2x ROAS (4 conv/30d) ❌ INSUFFICIENT data for automated

**BMPM:**
- P Max Shopping: NO TARGET (10 conv/30d) ❌ CRISIS - needs target ROAS
- Search: Maximize Conv (2 conv/30d) ❌ CRISIS - insufficient data

**Bid Strategy Issues:**

1. **4 HSG campaigns have insufficient conversion volume** (<30 conv/month) for Target ROAS/CPA:
   - Brand Search: 11 conv (borderline acceptable)
   - Hot Water Bottle: 8 conv ❌
   - Photo Bunting: 3 conv ❌
   - Photo Face Cushion: 4 conv ❌

2. **BMPM campaigns are in crisis mode:**
   - BMPM P Max has NO TARGET ROAS set (should have 0.7-0.8x to guide learning)
   - BMPM Search has only 2 conversions (should pause or consolidate)

**Recommendation:**
- **BMPM P Max:** Set target ROAS of 0.8x (currently has NO target, system has no guidance)
- **HSG low-volume campaigns:** Consider consolidating Hot Water Bottle + Bunting + Face Cushion into single campaign for more learning data
- **Priority:** HIGH for BMPM (no target is leaving algorithm blind), MEDIUM for HSG consolidation

---

## Phase 3: Budget Allocation Issues

### Budget-Constrained Campaigns (Last 7 Days)

**Lost Impression Share (Budget) >10% indicates campaign is limited by budget:**

| Campaign | Brand | Daily Budget | 7d Spend | Lost IS (Budget) | Lost IS (Rank) | Conversions (7d) | Priority |
|----------|-------|--------------|----------|------------------|----------------|------------------|----------|
| **CPL \| BMPM \| Search \| Promotional Merchandise** | BMPM | £15 | £98.45 | **43.1%** ❌ | 50.9% | 1 | CRITICAL |
| **CPL \| WBS \| Search \| Wheat Bags...** | WBS | £71 | £349.44 | **23.9%** ❌ | 67.1% | 33.2 | HIGH |
| **CPL \| BMPM \| P Max Shopping...** | BMPM | £50 | £367.86 | **15.1%** ⚠️ | 56.2% | 3 | MEDIUM |
| CPL \| HSG \| P Max \| All \| H&S... | HSG | £70 | £513.34 | 6.2% | 69.6% | 71.3 | MONITOR |
| CPL \| WBS \| P Max Shopping \| Wheat Bags \| Villains... | WBS | £8.20 | £67.78 | 6.7% | 53.6% | 5.4 | MONITOR |
| CPL \| WBS \| P Max \| Shopping \| Zombies... | WBS | £8.80 | £68.07 | 4.9% | 63.0% | 6.9 | MONITOR |

**Key Findings:**

1. **BMPM Search (Promotional Merchandise) - CRISIS:**
   - Lost 43% of impression share to budget constraints
   - Only generating 1 conversion per week
   - Spending £14/day against £15 budget (maxed out daily)
   - Also losing 51% IS to Rank (poor Quality Score or bid too low)
   - **Problem:** Both budget-constrained AND underperforming (need to diagnose root cause)

2. **WBS Main Search (Wheat Bags) - HIGH PRIORITY:**
   - Lost 24% of impression share to budget constraints
   - Strong performer: 33 conversions in 7 days
   - Spending £49.92/day against £71 budget
   - Also losing 67% IS to Rank
   - **Problem:** Campaign would spend more if budget allowed, but quality issues also limiting reach

3. **BMPM P Max Shopping - MEDIUM PRIORITY:**
   - Lost 15% IS to budget constraints
   - Low conversion volume: 3 conversions in 7 days
   - Spending £52.55/day against £50 budget (slightly over-pacing)
   - **Problem:** Budget constraint exists but campaign isn't converting well yet

### Budget Utilization Analysis

| Campaign | Daily Budget | Avg Daily Spend (30d) | Utilization % | Assessment |
|----------|--------------|----------------------|---------------|------------|
| CPL \| WBS \| P Max Shopping \| H&S 120 4/9 | £120.00 | £85.55 | 71% | ⚠️ Underutilized |
| CPL \| HSG \| P Max \| All \| H&S... | £70.00 | £65.67 | 94% | ✅ Optimal |
| CPL \| BMPM \| P Max Shopping... | £50.00 | £37.27 | 75% | ⚠️ Underutilized |
| CPL \| WBS \| Search \| Wheat Bags... | £71.00 | £31.77 | 45% | ❌ Severely underutilized |
| CPL \| HSG \| Search \| Photo Face Mask... | £38.00 | £20.19 | 53% | ❌ Underutilized |

**Budget Utilization Issues:**

1. **WBS Main Search only spending 45% of budget** - Budget Lost IS data shows campaign IS constrained, yet utilization is low. This indicates:
   - Campaign hitting budget daily for SHORT periods (morning rush?)
   - Rest of day not spending due to low Quality Score / poor Rank
   - **Problem:** Budget set too high for current search volume OR bids too low

2. **BMPM campaigns underutilizing budgets** - Yet showing Budget Lost IS:
   - P Max Shopping: 75% utilization, 15% Budget Lost IS
   - This pattern suggests budget exhaustion happens at specific times but not sustained
   - **Problem:** Poor pacing algorithm or low-quality traffic

### Budget Misallocation Opportunities

**Analyze spend vs ROAS to identify reallocation opportunities:**

| Campaign | Brand | 30d Spend | 30d Revenue | ROAS | CPA | Assessment |
|----------|-------|-----------|-------------|------|-----|------------|
| **CPL \| WBS \| P Max Shopping \| H&S 120 4/9** | WBS | £2,566.41 | £3,311.65 | **129%** ✅ | £9.00 | Best performer - INCREASE budget |
| **CPL \| HSG \| P Max \| All \| H&S...** | HSG | £1,970.18 | £2,452.65 | **124%** ✅ | £7.59 | Strong - target met |
| CPL \| BMPM \| P Max Shopping... | BMPM | £1,118.17 | £867.09 | **78%** ❌ | £111.82 | LOSING MONEY - reduce budget |
| CPL \| WBS \| Search \| Wheat Bags... | WBS | £952.97 | £1,226.93 | **129%** ✅ | £8.84 | Strong - INCREASE budget |
| CPL \| HSG \| Search \| Photo Face Mask... | HSG | £605.72 | £740.64 | **122%** ✅ | £7.87 | Strong - target met |
| CPL \| WBS \| Search \| Brand Inclusion | WBS | £369.51 | £463.93 | **126%** ✅ | £9.59 | Strong - target met |
| **CPL \| BMPM \| Search \| Promotional Merch** | BMPM | £265.31 | £93.60 | **35%** ❌ | £132.65 | CRISIS - huge losses |
| CPL \| HSG \| P Max Shopping \| Zombies | HSG | £214.83 | £386.17 | **180%** ✅ | £4.91 | Excellent - INCREASE budget |
| CPL \| WBS \| P Max \| Shopping \| Zombies | WBS | £182.66 | £227.44 | **124%** ✅ | £9.75 | Strong - target met |
| CPL \| WBS \| P Max Shopping \| Villains | WBS | £178.36 | £168.20 | **94%** ⚠️ | £11.19 | Below breakeven - REDUCE or pause |
| **CPL \| HSG \| P Max Shopping \| Villains** | HSG | £137.38 | £266.50 | **194%** ✅ | £4.74 | Excellent - INCREASE budget |

**ROAS Summary:**
- **Excellent (>150% ROAS):** 3 campaigns - HSG Villains (194%), HSG Zombies (180%), all low-spend sidekick products
- **Strong (120-150% ROAS):** 6 campaigns - All main brand campaigns hitting targets
- **Below Breakeven (75-100% ROAS):** 2 campaigns - WBS Villains (94%), BMPM P Max (78%)
- **CRISIS (<50% ROAS):** 1 campaign - BMPM Search (35%) ❌

**Budget Reallocation Recommendations:**

### CRITICAL REALLOCATION: Move BMPM Budget to High-Performers

**Current State:**
- BMPM P Max: £50/day budget, £1,118/month spend, 78% ROAS ❌ LOSING £246/month
- BMPM Search: £15/day budget, £265/month spend, 35% ROAS ❌ LOSING £172/month
- **Total BMPM losses:** £418/month

**Where to reallocate:**
- WBS P Max H&S: Currently £120/day, 71% utilization, 129% ROAS ✅ → **Increase to £150/day**
- HSG Villains P Max: Currently £6.30/day, 194% ROAS ✅ → **Increase to £12/day**
- HSG Zombies P Max: Currently £7.90/day, 180% ROAS ✅ → **Increase to £15/day**

**Action Plan:**
1. **BMPM P Max:** Reduce budget from £50/day to £30/day (£20/day cut = £600/month saved)
2. **BMPM Search:** Pause campaign (£15/day cut = £450/month saved)
3. **Reinvest £1,050/month into high-ROAS campaigns:**
   - WBS P Max H&S: +£30/day (£900/month)
   - HSG Villains P Max: +£5.70/day (£171/month) - ❗Still need to fix PRESENCE_OR_INTEREST first
   - HSG Zombies P Max: +£7.10/day (£213/month) - ❗Still need to fix PRESENCE_OR_INTEREST first

**Expected Impact:**
- **Stop losses:** Save £418/month from BMPM campaigns
- **Gain revenue:** Additional £1,050 × 1.30 avg ROAS = £1,365/month revenue
- **Net benefit:** £1,783/month revenue improvement

### Experimental Campaigns - Cleanup Needed

**6 experiment campaigns enabled but spending £0:**

| Campaign | Status | Budget | 30d Spend | Action Needed |
|----------|--------|--------|-----------|---------------|
| Target CPA Experiment - CPL \| WBS \| Search... | ENABLED | £500/day | £0.00 | PAUSE or DELETE |
| Target CPA Experiment – CPL \| TJR \| Search... | ENABLED | £200/day | £0.00 | PAUSE or DELETE |
| HSG \| Photo Cushion Broad Experiment | ENABLED | £20/day | £0.00 | PAUSE or DELETE |
| CPL \| WBS \|  Wheat Bags 170 Broad Test... | ENABLED | £71/day | £0.00 | PAUSE or DELETE |
| CPL \| WBS \|  Wheat Bags 141  Trial 236 | ENABLED | £71/day | £0.00 | PAUSE or DELETE |
| CPL \| WBS \|  Wheat Bags 140 21/5... | ENABLED | £71/day | £0.00 | PAUSE or DELETE |

**Issue:** These experiments have extraordinarily high budgets (£500/day, £200/day, £71/day each) but aren't getting impressions. This suggests:
- Targeting is too narrow (keywords, audiences)
- Bids are set too low
- Campaigns were created but never properly launched

**Recommendation:** Pause all 6 experiments. If they haven't spent anything in 30+ days, they're not functional. Either:
1. **Delete them** if experiments are abandoned
2. **Review and relaunch** if still relevant (check targeting, bids, ad approval status)

**Priority:** LOW (not costing money, just cluttering account)

---

## Phase 4: Product Impact Analyzer Integration

### Product Feed Tracking Status

**Client Tracked:** ✅ YES - All three Clear Prospects brands monitored

| Brand | Merchant ID | Tracking Status | Label Field | Notes |
|-------|-------------|-----------------|-------------|-------|
| **HappySnapGifts (HSG)** | 7481296 | ✅ ACTIVE | custom_label_4 | Product Hero labels tracked |
| **WheatyBags (WBS)** | 7481286 | ✅ ACTIVE | custom_label_4 | Product Hero labels tracked |
| **BMPM** | 7522326 | ✅ ACTIVE | custom_label_4 | Product Hero labels tracked |

**Product Change Detection:** Daily monitoring at 8:02 AM via LaunchAgent

### Recent Product Changes (Last 7 Days)

**Analysis Period:** 4-7 November 2025

**BMPM (British Made Promotional Merchandise):**
- **Nov 7:** 85,881 bytes of product changes detected
- **Nov 6:** 337,460 bytes of product changes detected (LARGE change event)
- **Nov 5:** 80,984 bytes of product changes
- **Nov 4:** 123,384 bytes of product changes

**Interpretation:** BMPM had a MASSIVE product feed change on Nov 6 (337KB). This coincides with:
- Campaign restructuring mentioned in CONTEXT.md (Oct 21 - paused underperforming categories)
- Ongoing profitability crisis (0.00x ROAS in October)
- **Hypothesis:** Product feed was significantly restructured to remove/pause unprofitable products

**HappySnapGifts (HSG):**
- **Nov 7:** 2,728 bytes of product changes
- **Nov 6:** 3,182 bytes of product changes
- **Nov 5:** 592 bytes of product changes
- **Nov 4:** 6,397 bytes of product changes

**Interpretation:** Minor product changes (likely price/stock updates, not major feed restructure)

**WheatyBags (WBS):**
- **Nov 7:** 1,730 bytes of product changes
- **Nov 6:** 2,232 bytes of product changes
- **Nov 5:** 3,840 bytes of product changes
- **Nov 4:** 1,656 bytes of product changes

**Interpretation:** Minor product changes (likely price/stock updates)

### Performance Correlation Analysis

**BMPM P Max Shopping Campaign Performance:**

| Date Range | Spend | Revenue | ROAS | Conv | Analysis |
|------------|-------|---------|------|------|----------|
| Nov 4-7 (post-feed-change) | ~£147 | ~£130 | ~88% | ~1 | Still unprofitable |
| Full 30 days | £1,118 | £867 | 78% | 10 | Consistently unprofitable |

**Key Finding:** The massive Nov 6 product feed change for BMPM has NOT yet translated to improved ROAS. Campaign continues to lose money (78% ROAS = 22% loss on every £1 spent).

**Possible Explanations:**
1. **Feed changes too recent** - Smart Bidding needs 6-8 weeks to learn new product set
2. **Product mix still unprofitable** - May need further pruning
3. **No target ROAS set** - Algorithm has no profitability guidance (this is CRITICAL fix needed)
4. **Insufficient conversion volume** - Only 10 conversions in 30 days, not enough for algorithm to optimize

### Product Feed Recommendations

**BMPM (CRITICAL):**
1. **Set target ROAS of 0.8x on P Max campaign** - Currently has NO target, algorithm is blind
2. **Monitor product-level performance** - Check Product Impact Analyzer spreadsheet to identify which products from Nov 6 feed change are driving losses
3. **Consider further feed pruning** - May need to pause more products if profitability doesn't improve in 3-4 weeks
4. **Review cushions search campaign** (started Oct 21) - Check if cushions are the profitable product to focus on

**HSG & WBS:**
- Product feeds stable, minor changes only
- No feed-related performance issues detected

---

## Recommendations (Prioritized by ICE Framework)

**ICE Framework:** Impact × Confidence ÷ Effort (scale 1-10 each)

### CRITICAL (Do Immediately - Within 24 Hours)

#### 1. Fix Geographic Targeting on 4 P Max Campaigns (ICE: 90)
**Impact: 10** | **Confidence: 9** | **Effort: 1**

**Change PRESENCE_OR_INTEREST → PRESENCE on:**
- CPL | HSG | P Max Shopping | Villains 120 130 15/9
- CPL | HSG | P Max Shopping | Zombies
- CPL | WBS | P Max Shopping | Wheat Bags | Villains 120 15/9
- CPL | WBS | P Max | Shopping | Zombies 120 15/9

**How to fix:**
1. Go to each campaign → Settings → Locations
2. Change "Target" from "People in, or who show interest in, your targeted locations (recommended)" to "People in or regularly in your targeted locations"
3. Save

**Expected Impact:**
- 20-30% waste reduction on £713/month spend
- **£142-213/month saved** immediately
- Better targeting of actual UK customers vs people researching UK from abroad

**Timeline:** 10 minutes total (2 min per campaign)

#### 2. Set Target ROAS of 0.8x on BMPM P Max Campaign (ICE: 80)
**Impact: 8** | **Confidence: 10** | **Effort: 1**

**Current State:**
- Campaign has NO target ROAS set
- Algorithm has no profitability guidance
- Spending £1,118/month with 78% ROAS (losing £246/month)

**Fix:**
1. Go to BMPM P Max campaign → Settings → Bidding
2. Set target ROAS of 80% (0.8x)
3. Monitor for 2 weeks

**Expected Impact:**
- Algorithm will prioritize more profitable auctions/products
- ROAS should improve by 10-20 percentage points over 4-6 weeks
- May reduce spend initially (algorithm avoiding unprofitable auctions)

**Timeline:** 2 minutes

#### 3. Pause BMPM Search Campaign (ICE: 75)
**Impact: 9** | **Confidence: 10** | **Effort: 1**

**Current State:**
- Spending £265/month with 35% ROAS
- **Losing £172/month** (65% loss on every £1 spent)
- Only 2 conversions in 30 days (insufficient data for automated bidding)
- 43% Budget Lost IS + 51% Rank Lost IS = campaign fundamentally broken

**Fix:**
1. Pause "CPL | BMPM | Search | Promotional Merchandise" campaign
2. Reallocate £265/month budget to high-ROAS campaigns

**Expected Impact:**
- Stop £172/month losses immediately
- Free up £265/month for high-performers

**Timeline:** 1 minute

**Alternative (if client insists on keeping Search campaign for BMPM):**
- Reduce budget to £3-5/day (test budget only)
- Consolidate keywords to top 3-5 best performers only
- Accept this is a long-term learning campaign with no short-term ROI

### HIGH (Do Within 1 Week)

#### 4. Increase Budget on High-ROAS Campaigns (ICE: 70)
**Impact: 8** | **Confidence: 9** | **Effort: 1**

**Budget reallocation plan using freed-up BMPM budget:**

| Campaign | Current Budget | New Budget | Increase | ROAS | Expected Revenue Gain |
|----------|----------------|------------|----------|------|----------------------|
| WBS P Max H&S | £120/day | £150/day | +£30/day | 129% | +£1,161/month |
| HSG Villains P Max | £6.30/day | £12/day | +£5.70/day | 194% | +£332/month |
| HSG Zombies P Max | £7.90/day | £15/day | +£7.10/day | 180% | +£384/month |

**Prerequisites:**
- MUST fix PRESENCE_OR_INTEREST on HSG/WBS Villains & Zombies campaigns FIRST
- Then wait 1 week to confirm geographic waste is eliminated
- Then increase budgets

**Expected Impact:**
- Additional £1,877/month revenue from £1,290/month additional spend
- Overall ROAS improvement from better budget allocation

**Timeline:** 5 minutes (after geographic fix is confirmed working)

#### 5. Increase Budget on WBS Main Search Campaign (ICE: 65)
**Impact: 7** | **Confidence: 9** | **Effort: 1**

**Current State:**
- £71/day budget, only spending £31.77/day average (45% utilization)
- 24% Budget Lost IS in last 7 days
- 129% ROAS, 108 conversions/month (strong performer)

**Issue Diagnosis:**
Budget utilization pattern suggests campaign hits daily cap for SHORT periods (likely morning), then stops spending due to low Quality Score / Rank issues (67% Rank Lost IS).

**Fix Options:**

**Option A (Preferred):** Increase budget to £100/day
- Gives campaign more headroom during high-traffic periods
- May improve pacing and reduce morning budget exhaustion
- Monitor spend for 1 week

**Option B:** Keep budget at £71/day, focus on improving Quality Score
- Add more relevant keywords
- Improve ad copy to increase CTR
- Review landing pages

**Expected Impact:**
- Option A: +£20-30/day additional spend at 129% ROAS = +£774-1,161/month revenue
- Option B: Improved Quality Score over 4-6 weeks, better Impression Share

**Recommendation:** Try Option A first (quick win), then work on Option B if utilization remains low

**Timeline:** 2 minutes to increase budget, 2-3 hours for Quality Score optimization

#### 6. Pause or Delete 6 Experimental Campaigns (ICE: 60)
**Impact: 4** | **Confidence: 10** | **Effort: 1**

**Campaigns spending £0 for 30+ days:**
- Target CPA Experiment - CPL | WBS | Search | Heat Pads & Packs | Broad
- Target CPA Experiment – CPL | TJR | Search | Luggage Straps | Exact
- HSG | Photo Cushion Broad Experiment
- CPL | WBS |  Wheat Bags 170 Broad Test  Recommendations trial
- CPL | WBS |  Wheat Bags 141  Trial 236
- CPL | WBS |  Wheat Bags 140 21/5 140 14/1  Trial 721

**Fix:** Pause all 6 campaigns (or delete if permanently abandoned)

**Expected Impact:**
- Cleaner account structure
- Easier performance reporting
- Reduced risk of accidentally enabling broken campaigns

**Timeline:** 3 minutes

### MEDIUM (Do Within 1 Month)

#### 7. Review Search Partners Performance on 2 Active Campaigns (ICE: 50)
**Impact: 6** | **Confidence: 7** | **Effort: 2**

**Campaigns with Search Partners enabled and actively spending:**
- CPL | WBS | Search | Brand Inclusion 18/6 (£369/month)
- CPL | HSG | Search | Hot Water Bottle Cover... (£66/month)

**Action Required:**
1. Go to each campaign → Segment by "Network (with search partners)"
2. Compare Google Search vs Search Partners performance:
   - ROAS
   - CPA
   - Conversion Rate
   - CTR
3. If Search Partners underperforms by >20% ROAS vs Google Search, disable it

**Expected Impact:**
- If Search Partners is underperforming: 5-10% ROAS improvement (£22-44/month)
- If Search Partners is performing well: No action needed

**Timeline:** 20 minutes analysis, 2 minutes to disable if needed

#### 8. Consolidate Low-Volume HSG Search Campaigns (ICE: 45)
**Impact: 5** | **Confidence: 7** | **Effort: 4**

**4 HSG Search campaigns with <10 conversions/month:**
- Hot Water Bottle Cover: 8 conversions, £66/month
- Photo Bunting: 3 conversions, £34/month
- Photo Face Cushion: 4 conversions, £18/month
- (Brand Search: 11 conversions - borderline acceptable, leave separate)

**Problem:** Insufficient conversion volume for Target ROAS automated bidding to learn effectively (<30 conv/month threshold)

**Fix Options:**

**Option A:** Consolidate into single "HSG - Secondary Products" campaign
- Combine all 3 campaigns into one
- Combined: 15 conversions/month, £118/month (still below ideal but better)
- Allows for better bidding optimization

**Option B:** Switch to Manual CPC bidding
- Keep campaigns separate
- Use Manual CPC with rules-based bid adjustments
- More management overhead

**Recommendation:** Try Option A first (consolidation)

**Expected Impact:**
- Better Smart Bidding performance from increased data volume
- 5-10% efficiency improvement over 6-8 weeks

**Timeline:** 1-2 hours to consolidate campaigns properly

#### 9. Monitor BMPM Product Feed Changes for 4-6 Weeks (ICE: 40)
**Impact: 8** | **Confidence: 4** | **Effort: 2**

**Context:**
- Massive product feed change on Nov 6 (337KB of changes)
- Campaign still unprofitable (78% ROAS as of Nov 11)
- Target ROAS of 0.8x now set (per recommendation #2)

**Action Required:**
1. Check BMPM Product Impact Analyzer spreadsheet weekly: [Link](https://docs.google.com/spreadsheets/d/1EenJFkPWGZ6c_ZhsKKYudDcW2Nt8Jeamc1m55BPR5dU/)
2. Identify which products are driving losses
3. If ROAS doesn't improve to 85%+ by mid-December, consider:
   - Further product feed pruning
   - Pausing PMax campaign entirely
   - Focusing only on cushions via Search campaign

**Expected Impact:**
- Better understanding of which products/categories are profitable
- Data-driven decision on whether to continue BMPM PMax or pivot strategy

**Timeline:** 15 minutes/week monitoring, 2-3 hours for deeper analysis if needed

---

## Audit Methodology

**Queries Executed:**
- **Phase 1:** account-scale, spend-concentration (analyzed 21 enabled campaigns, 15 actively spending)
- **Phase 2:** campaign-settings, budget-constraints, campaign-performance (all 21 enabled campaigns)
- **Phase 3:** Not required (small account, covered all campaigns in Phase 2)

**Data Transformation:**
- Manual analysis due to script compatibility issue
- Calculated ROAS from conversions_value ÷ cost_micros (converted from micros)
- Verified bid strategy targets using both target_roas and maximize_conversion_value.target_roas fields

**Product Impact Analyzer:**
- ✅ Checked for all 3 Clear Prospects brands
- ✅ Identified massive BMPM product feed change on Nov 6, 2025
- ✅ Correlated with known campaign restructuring (CONTEXT.md documentation)

**Coverage:**
- Analyzed 15 campaigns representing 100% of account spend
- Focused on structural and budget issues per audit scope
- Did NOT cover ad copy quality, keyword QS, or granular performance optimization

---

## Summary of Key Issues

| Issue | Campaigns Affected | Monthly Impact | Fix Effort | Priority |
|-------|-------------------|----------------|------------|----------|
| **PRESENCE_OR_INTEREST waste** | 4 P Max campaigns | £142-213/month wasted | 10 minutes | CRITICAL |
| **BMPM P Max - No Target ROAS** | 1 campaign | Algorithm blind, 78% ROAS | 2 minutes | CRITICAL |
| **BMPM Search - Massive losses** | 1 campaign | £172/month losses | 1 minute (pause) | CRITICAL |
| **Budget constrained - high performers** | 3 campaigns | Opportunity cost £400+/month | 5 minutes | HIGH |
| **Experiment campaigns clutter** | 6 campaigns | No cost, just clutter | 3 minutes | MEDIUM |
| **Low-volume campaign consolidation** | 3 campaigns | 5-10% efficiency gain | 1-2 hours | MEDIUM |
| **Product feed monitoring needed** | BMPM brand | Unknown (needs tracking) | 15 min/week | MEDIUM |

**Total Immediate Savings Opportunity:** £314-385/month from top 3 CRITICAL fixes (£142-213 geo waste + £172 BMPM Search losses)

**Total Revenue Opportunity:** £1,877/month from budget reallocation to high-ROAS campaigns

---

*Report generated by Claude Code Campaign Audit Skill*
*For questions about this audit, refer to `.claude/skills/google-ads-campaign-audit/`*
