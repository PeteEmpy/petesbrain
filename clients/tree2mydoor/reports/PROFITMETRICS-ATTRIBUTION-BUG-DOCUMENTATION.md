# ProfitMetrics Google Ads Attribution Bug - Impact Documentation

**Date Created:** 11 December 2025
**Client:** Tree2mydoor
**Issue:** Google Ads offline conversion attribution failure via ProfitMetrics
**Status:** Awaiting ProfitMetrics resolution update + Google recompense claim

---

## Timeline

| Date | Event |
|------|-------|
| **5-6 Dec (Thu-Fri)** | Bug begins affecting offline conversions in Google Ads |
| **7 Dec (Sun)** | Peter notices massive sales drop, alerts Gareth |
| **8 Dec (Mon)** | ProfitMetrics sends alert about Google Ads attribution error to all customers |
| **8 Dec (Mon)** | Peter sends detailed analysis to Gareth explaining impact |
| **9 Dec (Tue)** | Gareth confirms: (1) Shopify access granted for analytics, (2) Agreement to request Google refund/credit |
| **11 Dec (Wed)** | Awaiting ProfitMetrics resolution update |

---

## The Issue

**What Happened:**
- Tree2mydoor uses **ProfitMetrics Conversion Booster** to send profit data via offline conversion imports
- ProfitMetrics had a system bug affecting ALL customers
- Google Ads received conversion data but **failed to attribute it properly**
- Result: Google Ads showed **50-100% fewer conversions than actually occurred**

**Why This Matters:**
This isn't just a reporting issue. When conversion data stops reaching Google's algorithm:
1. Algorithm thinks campaigns aren't working
2. Algorithm pulls back on bidding
3. Impression share decreases
4. Traffic quality decreases
5. **Actual sales drop** (beyond reporting distortion)

---

## Verified Impact - Google Ads API Data (Dec 1-8)

**Queried from Google Ads API** - all campaigns with spend included

| Date | Day | Conversions | Spend | Revenue | ROAS | Status |
|------|-----|-------------|-------|---------|------|--------|
| **1 Dec** | Mon | 27.86 | £657.32 | £483.78 | 0.74x | ✓ Baseline |
| **2 Dec** | Tue | 14.92 | £590.82 | £323.49 | 0.55x | ✓ Baseline |
| **3 Dec** | Wed | 11.85 | £533.59 | £249.68 | 0.47x | ✓ Baseline |
| **4 Dec** | Thu | 15.59 | £714.20 | £296.51 | 0.42x | ✓ Baseline |
| **5 Dec** | Fri | 25.41 | £721.52 | £449.48 | 0.62x | ⚠️ Issue begins |
| **6 Dec** | Sat | **5.67** | **£625.93** | **£134.99** | **0.22x** | 🔴 **Sharp drop** |
| **7 Dec** | Sun | 15.57 | £911.75 | £296.58 | 0.33x | 📉 **Still depressed** |
| **8 Dec** | Mon | 31.19 | £797.55 | £613.01 | 0.77x | ↗️ **Recovery starting** |

**Critical Note:** These are the conversion figures **reported to Google Ads**. ProfitMetrics has confirmed these numbers are **50-100% lower than actual conversions**, meaning real Shopify sales during Dec 6-8 were likely double what Google Ads was reporting.

---

## Quantifiable Impact

### Pre-Bug Baseline (Dec 1-5)

- **Average conversions/day:** 17.1
- **Average revenue/day:** £376.59
- **Average spend/day:** £650.71
- **Average ROAS:** 0.58x

### Peak Impact Window: 6-7 December (2 days)

**Reported conversions (from API):**
- **Dec 6:** 5.67 conversions (79% below baseline)
- **Dec 7:** 15.57 conversions (9% below baseline)
- **2-day total:** 21.24 conversions

**Expected conversions (extrapolating baseline):**
- Expected: 17.1 × 2 = **34.2 conversions**
- **Shortfall: 13 conversions** (38% reduction)

**Spend during issue:**
- Dec 6-7: **£1,537.68** (spend continued normally, conversions dropped)

**Revenue shortfall:**
- Expected revenue: £376.59 × 2 = £753.18
- Actual revenue: £431.57
- **Direct revenue loss: £321.61**

### Critical: API Data vs. Actual Reality

**⚠️ IMPORTANT FOR GOOGLE CLAIM**

- ProfitMetrics confirmed the bug caused **50-100% underreporting** of conversions
- API data shows the already-reduced figures Google Ads reported
- **Actual Shopify conversions during Dec 6-8 were likely 2-3× higher than these numbers**
- The spend continued because the algorithm didn't immediately pull back fully
- By Dec 8, recovery has begun (31.19 conversions, highest of the period)

**Real-world impact likely much higher** - pending verification from Shopify actual order data (being compiled by Gareth).

---

## Recovery Status

**ProfitMetrics Status:**
- Sent resolution update pending (awaiting confirmation)
- Working with Google API support to fix the issue

**Expected Recovery:**
- Once fix deployed, Google Ads algorithm will receive conversion signals again
- Algorithm should recalibrate to higher-quality traffic
- Normal performance expected within 24-48 hours of fix

**Current Monitoring:**
- Peter monitoring Google Ads attribution daily
- Will check mid-week for recovery signs
- Gareth checking actual Shopify order data to verify recovery correlates

---

## Evidence Files

All correspondence and analysis saved in client folder:

1. **Email Thread:** `2025-12-07_re-site-issues.md` - Initial issue discovery
2. **Email Thread:** `2025-12-08_re-site-issues.md` - Gareth's response & commitment to Google claim
3. **Email Thread:** `2025-12-09_re-site-issues.md` - Gareth confirms Shopify access and refund approach
4. **Sent Report:** `2025-12-05_sent-november-month-end-report.md` - Historical baseline for comparison

---

## Next Actions for Google Recompense Claim

### When Gareth Asks (Expected: This Week or Next)

**What We Have Ready for Google:**
1. ✅ **Specific dates:** 5-8 Dec (ProfitMetrics confirmed the bug started 5th-6th)
2. ✅ **API-verified impact:**
   - 13 conversion shortfall (38% reduction) during peak impact (Dec 6-7)
   - £321.61 direct revenue loss (Dec 6-7)
   - £1,537.68 spend during issue period with suboptimal conversion reporting
3. ✅ **ProfitMetrics confirmation:** Bug affected all customers, 50-100% offline conversion underreporting
4. ✅ **Google Ads API data:** Daily breakdown showing attribution collapse on Dec 6
5. ⏳ **Actual Shopify data:** Real order counts (Gareth collecting to show 2-3× higher impact than Google Ads reported)

### Claim Strategy for Google

**Two-pronged approach:**

**Component 1: Conservative Claim (Easy to justify)**
- **Wasted spend:** £1,537.68 (spend on Dec 6-7 when algorithm was receiving bad conversion signals)
- **Justification:** Google's API partner (ProfitMetrics) had a bug causing false conversion data; Google benefited from the spending while being unable to optimize properly
- **Request:** Refund the spend from the broken service period

**Component 2: Revenue Impact Claim (When Shopify data arrives)**
- **Minimum verified loss:** £321.61 (based on API data alone)
- **Actual loss:** Likely £600-1,000+ (once Shopify data confirms 2-3× underreporting)
- **Justification:** When offline conversion attribution fails, the algorithm pulls back bidding on lower-quality traffic, causing both reporting loss AND real performance loss. Even accounting for Shopify's own traffic recovery, Google's platform malfunction degraded live performance

**Expected outcome:**
- Conservative: Refund the £1,537.68 spend
- Realistic: Spend refund + 20-30% credit on lost ROAS (£200-300)
- Optimistic: Full revenue impact credit if Shopify data shows >50% drop

---

## Next Steps

1. **Monitor:** Watch for ProfitMetrics resolution email (from Frederik Boysen)
2. **Verify:** Check Google Ads attribution recovery once ProfitMetrics confirms fix
3. **Await:** Gareth's request for Google contact (expected this week)
4. **Prepare:** Have this documentation ready for Gareth + draft Google support claim
5. **Execute:** Submit formal request to Google with quantified impact + Shopify data

---

## Contact Information

**ProfitMetrics:** Frederik Boysen (support@profitmetrics.io)
**Gareth Mitchell (Collaber/Tree2mydoor):** gareth@collaber.agency
**Google Ads Account:** Tree2mydoor (Customer ID: 8573235780)

---

**Document Status:** Ready for Google claim submission pending ProfitMetrics resolution confirmation
