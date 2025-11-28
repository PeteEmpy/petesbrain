# Black Friday Merchant Centre Promotions - Week 1 Performance Analysis

**Date Created:** 2025-11-26
**Analysis Period:** Nov 19-25 (with promotions) vs Nov 12-18 (baseline)
**Status:** PRELIMINARY - Full analysis deferred to January 2025

---

## Promotion Feed Summary

**Feed Status:**
- ✅ **757 products** successfully matched with promotions (55% success rate)
- ❌ **627 products** failed to match (45% failure rate)
- **Total intended products:** 1,384 (GB market only)

**Promotion Details:**
- **BF2025_LEATHER_30**: 30% off leather products
- **BF2025_BOOKS_20**: 20% off books/stationery
- **Live dates:** 17 November - 1 December 2025
- **Channel:** Online, Shopping ads
- **Type:** NO_CODE (automatic discount)

**Initial Setup Issues (Resolved Nov 18):**
- Original feed (Nov 13): 368 products
- Nov 18: All 598 products failed - used EU/DE/FR country codes instead of GB
- Nov 18: Corrected feed uploaded with GB products only
- Nov 19: 757 products successfully matched, 627 failed (reason unknown)

---

## Week 1 Performance Analysis (UK Shopping Campaigns)

### Shopping Campaign Performance - WITH Promotions (Nov 19-25)

| Campaign | Spend | Revenue | ROAS | Conversions | Clicks | Impressions |
|----------|-------|---------|------|-------------|--------|-------------|
| **H&S** | £2,018 | £9,138 | **453%** | 64.3 | 1,498 | 165,962 |
| **Zombies** | £1,129 | £1,930 | **171%** | 11.1 | 255 | 24,137 |
| **Villains** | £473 | £406 | **86%** | 3.7 | 160 | 9,418 |
| **TOTAL** | **£3,620** | **£11,474** | **317%** | **79.1** | **1,913** | **199,517** |

---

### Shopping Campaign Performance - BEFORE Promotions (Nov 12-18)

| Campaign | Spend | Revenue | ROAS | Conversions | Clicks | Impressions |
|----------|-------|---------|------|-------------|--------|-------------|
| **H&S** | £1,334 | £8,607 | **645%** | 52.1 | 907 | 128,176 |
| **Zombies** | £925 | £6,272 | **678%** | 14.5 | 262 | 25,910 |
| **Villains** | £426 | £1,920 | **451%** | 12.4 | 153 | 11,271 |
| **TOTAL** | **£2,685** | **£16,799** | **626%** | **79.0** | **1,322** | **165,357** |

---

### Week-on-Week Comparison

| Metric | Before Promos | With Promos | Change | % Change |
|--------|---------------|-------------|--------|----------|
| **Spend** | £2,685 | £3,620 | +£935 | **+35%** ✅ |
| **Revenue** | £16,799 | £11,474 | -£5,325 | **-32%** 🔴 |
| **ROAS** | 626% | 317% | -309pp | **-49%** 🔴 |
| **Conversions** | 79.0 | 79.1 | +0.1 | **0%** ⚠️ |
| **Clicks** | 1,322 | 1,913 | +591 | **+45%** ✅ |
| **Impressions** | 165,357 | 199,517 | +34,160 | **+21%** ✅ |
| **CPC** | £2.03 | £1.89 | -£0.14 | **-7%** ✅ |
| **CTR** | 0.80% | 0.96% | +0.16pp | **+20%** ✅ |
| **CVR** | 5.98% | 4.14% | -1.84pp | **-31%** 🔴 |

---

## Preliminary Findings

### What Improved:
- ✅ **Impressions up 21%** - More visibility in Shopping results
- ✅ **Clicks up 45%** - Promotion badges attracting more clicks
- ✅ **CTR up 20%** - Better click-through rate
- ✅ **CPC down 7%** - Cheaper clicks (possibly Google rewarding promoted products)

### What Deteriorated:
- 🔴 **Revenue down 32%** - Despite more clicks, less revenue generated
- 🔴 **ROAS dropped 49%** (626% → 317%) - Efficiency collapsed
- 🔴 **Conversion rate down 31%** (5.98% → 4.14%) - Lower quality traffic

### What Stayed Flat:
- ⚠️ **Conversions unchanged** (79.0 → 79.1) - Same number of sales despite increased traffic

---

## Campaign-Specific Performance

### H&S Campaign - Best Performer
- ROAS: 453% (down from 645% - 30% decline)
- Revenue: £9,138 (down 6%)
- Spend: +51%
- **Assessment:** Handling promotions reasonably well, revenue held up

### Zombies Campaign - Worst Hit
- ROAS: 171% (down from 678% - 75% decline)
- Revenue: £1,930 (down 69%)
- Spend: +22%
- **Assessment:** Promotions appear ineffective for this product category

### Villains Campaign - Loss-Making
- ROAS: 86% (down from 451% - 81% decline)
- Revenue: £406 (down 79%)
- Spend: +11%
- **Assessment:** Campaign losing money with promotions active

---

## Initial Hypothesis

**The Promotion Paradox:**

The 757 promoted products ARE receiving preferential treatment from Google:
- More impressions (visibility boost)
- More clicks (badge attraction)
- Lower CPCs (algorithmic reward)

**BUT this has NOT translated into business value:**
- Same number of conversions (no incremental sales)
- Lower revenue per conversion (discount effect)
- Collapsed ROAS (efficiency loss)

**Possible Explanation:**
The promotions are attracting bargain hunters who would have purchased anyway, but now at lower margins. The 30% and 20% discounts are reducing basket value without driving incremental demand.

**Alternative Explanation:**
The week of Nov 19-25 may have had other factors affecting performance (budget changes, campaign pauses, seasonal patterns, competitive intensity) that confound the promotion effect.

---

## Outstanding Questions for January Analysis

1. **Incremental Sales:** Did the promotions drive NEW customers, or just discount existing demand?
2. **Product Mix:** Which specific products performed better/worse with promotions?
3. **Customer Behaviour:** Did promoted products have higher/lower return rates?
4. **Competitive Context:** How did Black Friday week (Nov 26-Dec 1) perform vs early promotion week?
5. **Full Funnel:** What was the impact on Performance Max campaigns (which also use Shopping feed)?
6. **Failed Products:** What happened to the 627 products that failed to match? Could they have performed better?
7. **Badge Visibility:** Were promotion badges actually showing in ads consistently?

---

## Data Sources for Future Analysis

**Available Data:**
- `/clients/smythson/spreadsheets/smythson-bf2025-promotions-feed-CORRECTED.csv` (1,384 products)
- `/clients/smythson/documents/BlackFridayPromotions2025.f406579615.gb.en.u1763467357616000.feeduploadreport.csv` (598 errors from initial upload)
- Google Ads API - Shopping campaign performance (Nov 12-Dec 1)
- Google Ads API - Product-level performance (shopping_performance_view)
- Merchant Centre - Promotion approval status

**Analysis Tools:**
- `/clients/smythson/scripts/check-bf-promotions-products.py` (product verification script)

---

## Recommended January Deep Dive

**Scope:**
- Full Black Friday period (Nov 17 - Dec 1)
- All UK campaigns (Shopping + Performance Max)
- Product-level analysis (promoted vs non-promoted)
- Customer-level analysis (new vs returning)
- Competitive benchmarking (category averages)

**Goal:**
Determine whether Merchant Centre promotions are a worthwhile tactic for future seasonal events, or if alternative approaches (site-wide sales, coupon codes, Performance Max creative emphasis) deliver better ROI.

**Timeline:**
January 2025 (after Q4 reporting complete, before 2025 planning)

---

## Files Created

- `/clients/smythson/documents/bf-promotions-week1-performance-analysis.md` (this document)
- `/clients/smythson/documents/bf-promotions-verification-2025-11-18.md` (product verification report)
- `/clients/smythson/documents/smythson-bf2025-merchant-centre-promotions-setup.md` (setup guide)

---

**Status:** Analysis paused until January 2025
**Next Action:** Full retrospective analysis post-Black Friday
**Owner:** Peter Empson
