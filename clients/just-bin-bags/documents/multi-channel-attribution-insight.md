# Just Bin Bags - Multi-Channel Attribution Insight

**Date:** 18 December 2025
**Status:** ✅ Critical Context for All Future Campaign Decisions

---

## Executive Summary

**Key Finding:** Google Ads ROAS (reported by Google) does NOT equal true product profitability for Just Bin Bags/Just Health Disposables.

**Why this matters:** Products that appear unprofitable in Google Ads reports are actually profitable when viewing total revenue across all channels (Google Ads + Direct/Phone + Organic + Referral).

---

## The Numbers

### JHD PMax Campaign Example

| Metric | Google Ads-Only View | Multi-Channel Reality | Difference |
|--------|---------------------|---------------------|------------|
| **Revenue** | £147.77 (Google Ads attributed) | **£308.23** (total product revenue) | +108% |
| **Cost** | £190.87 (Google Ads spend) | £190.87 (Google Ads spend) | - |
| **ROAS** | **0.77x** (appears unprofitable) | **1.61x** (actually profitable) | +109% |

**Missing revenue breakdown:**
- Google Ads: £220.39 (71.5%)
- Direct/Phone: £28.83 (9.4%)
- Organic Search: £32.31 (10.5%)
- Referral: £26.69 (8.7%)

---

## Why This Happens (B2B/B2C Attribution Gap)

### Customer Journey Examples

**Journey 1 - Research Online, Buy by Phone:**
1. Customer sees Google Ad for "blue vinyl gloves"
2. Visits website, checks specs
3. Calls office to place bulk order (B2B buyer preference)
4. WooCommerce attributes order to "Direct" (phone order)
5. **Google Ads gets no credit, but it drove the awareness**

**Journey 2 - Brand Awareness → Organic Search:**
1. Customer sees Google Ad for Just Health Disposables
2. Doesn't click immediately
3. Later searches "just health disposables gloves" on Google
4. Clicks organic result, purchases
5. WooCommerce attributes to "Organic Search"
6. **Google Ads built the brand awareness, but gets no credit**

**Journey 3 - Referral After Ad Exposure:**
1. Customer sees Google Ad
2. Finds review/link on external site
3. Purchases via referral link
4. WooCommerce attributes to "Referral"
5. **Google Ads initiated the interest, but gets no credit**

---

## Strategic Implications

### ✅ DO

1. **Always check WooCommerce total product revenue** before making campaign budget decisions
2. **Consider multi-channel ROAS** when evaluating campaign performance
3. **Recognize Google Ads' role in brand awareness** that drives non-Google conversions
4. **Monitor direct/phone orders as a leading indicator** of Google Ads effectiveness

### ❌ DON'T

1. **Don't kill campaigns based solely on Google Ads ROAS** without checking total product revenue
2. **Don't assume all product revenue should be Google Ads attributed** in a B2B/B2C business
3. **Don't ignore the brand awareness effect** of paid advertising on other channels

---

## Campaign Decision Framework

**When evaluating any Google Ads campaign:**

```
Step 1: Check Google Ads ROAS (from Google Ads API)
Step 2: Pull WooCommerce product revenue for same products (all channels)
Step 3: Calculate: Total Product Revenue ÷ Google Ads Cost = True ROAS
Step 4: Make decision based on TRUE ROAS, not just Google Ads ROAS
```

**Example Decision Matrix:**

| Google Ads ROAS | True Multi-Channel ROAS | Decision |
|----------------|------------------------|----------|
| 0.77x | 1.61x | ✅ Keep active, optimize |
| 0.50x | 1.20x | ✅ Keep active, reduce budget |
| 0.30x | 0.60x | ⚠️ Investigate, likely pause |
| 2.50x | 4.00x | ✅ Scale aggressively |

---

## Real-World Example: JHD Products

### Blue Disposable Nitrile Gloves (Product 398)

**Google Ads attributes:** £54.99 (48.2% of total)
**But total product revenue:** £114.03

**Missing revenue sources:**
- Direct/Phone orders: £26.69 (23.4%)
- Organic search: £5.66 (5.0%)
- Referral: £26.69 (23.4%)

**Insight:** Google Ads generates less than half the direct revenue, but likely influences the other 52% through brand awareness.

### Clear Medical Grade Vinyl Gloves (Product 84)

**Google Ads attributes:** £0.00
**But total product revenue:** £28.79

**Revenue sources:**
- Organic search: £26.65 (92.6%)
- Direct: £2.14 (7.4%)

**Insight:** Product appears to have "no Google Ads value" but generates meaningful revenue through organic (likely brand searches influenced by previous Google Ads exposure).

---

## Attribution by Product Category

### JBB Main Brand (30-day period: 18 Nov - 17 Dec 2025)

- **Total Revenue:** £10,899.16
- **Google Ads Share:** 63.3% (£6,826.37)
- **Direct Share:** 25.6% (£2,786.56)
- **Organic Share:** 11.8% (£1,286.23)

**Highest direct revenue products:**
1. 160 Gauge Bin Bags - AQUARIUS: 61% direct (£231.88)
2. Clear Bin Bags Heavy Duty | Diamond: 100% direct (£229.04)
3. 120-240L Clear Wheelie Bin Liners: 71% direct (£182.76)

### JHD Sub-brand (30-day period: 18 Nov - 17 Dec 2025)

- **Total Revenue:** £308.23
- **Google Ads Share:** 71.5% (£220.39)
- **Direct Share:** 9.4% (£28.83)
- **Organic Share:** 10.5% (£32.31)
- **Referral Share:** 8.7% (£26.69)

---

## Monitoring Protocol

**Monthly Review Checklist:**

1. ✅ Pull Google Ads performance data (via API)
2. ✅ Pull WooCommerce product revenue for same products (all channels)
3. ✅ Calculate multi-channel ROAS
4. ✅ Compare month-over-month trends
5. ✅ Look for changes in direct/organic share (indicates brand awareness impact)
6. ✅ Make budget decisions based on TRUE ROAS, not just Google Ads ROAS

**Red Flags to Watch:**

- Direct/organic revenue declining while Google Ads ROAS steady → brand awareness weakening
- Google Ads ROAS increasing but total product revenue flat → cannibalizing other channels
- Large gap between Google Ads ROAS and true ROAS narrowing → attribution improving OR brand effect weakening

---

## Tools & Data Sources

**Google Ads API:** Campaign-level ROAS, product impressions/clicks/conversions
**WooCommerce REST API:** Order data with attribution metadata (`_wc_order_attribution_*`)
**Product Impact Analyzer:** Daily product-level Google Ads performance
**Analysis Scripts:** Located in `clients/just-bin-bags/audits/`

---

## Revised Campaign Recommendations (Post-Attribution Analysis)

### JHD PMax Campaign

**Original recommendation (Google Ads-only view):**
- Reduce budget £10/day → £3-5/day (campaign losing money at 0.81x ROAS)

**Revised recommendation (multi-channel view):**
- ✅ Keep campaign active (products profitable at 1.61x true ROAS)
- ⚠️ Moderate budget reduction: £10/day → £7-8/day (optimize, not kill)
- 🎯 Fix geographic targeting: PRESENCE_OR_INTEREST → PRESENCE
- 📊 Monitor multi-channel performance monthly
- 🔍 Audit product feed to improve direct Google Ads ROAS from 0.77x toward 1.5x

### JBB Main PMax Campaign

**Status:** Performing well at 1.99x Google Ads ROAS
**Multi-channel boost:** Likely ~2.5-3.0x true ROAS (based on 63% Google Ads share)
**Recommendation:** Scale budget, high Lost IS Budget indicates room for growth

### Brand Search Campaign

**Status:** Exceptional 12.49x Google Ads ROAS, 10% budget utilization
**Multi-channel consideration:** Organic search strong (£1,286 revenue), brand awareness healthy
**Recommendation:** Increase budget aggressively, capturing brand demand

---

## Key Takeaway for All Future Analysis

**"Google Ads ROAS is NOT product profitability for Just Bin Bags."**

Always analyze:
1. Google Ads ROAS (campaign effectiveness)
2. Multi-channel product revenue (true profitability)
3. Attribution mix (brand awareness impact)

This insight applies to ALL campaign decisions, budget allocations, and performance reviews.

---

**Document Owner:** Roksys (Peter Empson)
**Last Updated:** 18 December 2025
**Review Frequency:** Reference before every budget/campaign decision
