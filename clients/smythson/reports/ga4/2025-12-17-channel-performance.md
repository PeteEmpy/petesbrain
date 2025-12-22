# Smythson - GA4 Channel Performance Analysis

**Report Period:** 10 December - 16 December 2025
**Comparison Period:** 3 December - 9 December 2025
**Generated:** 17 December 2025

---

## 🟢 **Executive Summary**

### Overall Performance

| Metric | Current Week | Previous Week | Change | Status |
|--------|--------------|---------------|--------|--------|
| **Total Sessions** | 176,004 | 128,493 | +37.0% | ⬆️ Strong |
| **Total Users** | 123,547 | 82,700 | +49.4% | ⬆️ Strong |
| **Total Conversions** | 938,084 | 1,007,875 | -6.9% | ⬇️ Declining |
| **Total Revenue** | **£644,351.76** | **£591,601.43** | **+8.9%** | ✅ Excellent |
| **Avg Engagement Rate** | 64.1% | 82.8% | -18.7pp | ⚠️ Concerning |

### Google Ads Performance (All Regions Combined)

| Metric | Current Week | Previous Week | Change |
|--------|--------------|---------------|--------|
| **Spend** | £38,800.17 | £38,012.39 | +2.1% |
| **Revenue** | £285,244.61 | £331,980.19 | **-14.1%** |
| **Conversions** | 1,493.52 | 1,720.94 | -13.2% |
| **ROAS** | **735%** | **873%** | **-138pp** |

**Key Takeaway:** Revenue and sessions are up, but conversion efficiency has declined week-over-week. Google Ads ROAS dropped 15.8% despite stable spend. Direct traffic surged +53.5%, suggesting strong brand momentum or possible attribution shifts.

---

## 📊 **Channel Overview**

### Current Week Performance (10-16 Dec)

| Channel | Sessions | Revenue | Conv Rate | vs Previous | Share of Revenue |
|---------|----------|---------|-----------|-------------|------------------|
| **Direct** | 40,037 | £134,032.22 | 0.41% | +53.5% 🔥 | 20.8% |
| **Unassigned** | 38,723 | £73,664.01 | 0.39% | +424.1% ⚠️ | 11.4% |
| **Organic Search** | 30,874 | £107,744.21 | 0.63% | -1.2% | 16.7% |
| **Paid Search** | 18,773 | **£150,927.08** | **0.97%** | +1.6% | **23.4%** |
| **Cross-network (PMax)** | 20,637 | £88,004.12 | 0.55% | +28.0% | 13.7% |
| **Email** | 10,605 | £70,066.75 | 0.66% | -13.4% | 10.9% |
| **Paid Other** | 8,874 | £10,907.64 | 0.23% | -13.0% | 1.7% |
| **Organic Social** | 2,615 | £1,195.92 | 0.37% | +13.4% | 0.2% |
| **Paid Shopping** | 617 | £1,153.996 | 1.21% | -76.7% ⚠️ | 0.2% |
| **Referral** | 1,483 | £4,286.25 | 1.31% | +7.3% | 0.7% |
| **SMS** | 247 | £590.32 | 0.43% | +18.8% | 0.1% |
| **Paid Social** | 14 | £0 | 0.11% | +40.0% | 0.0% |

---

## 🔍 **Attribution Comparison: Google Ads vs GA4**

### The Discrepancy

**Google Ads Reported Revenue:** £285,244.61
**GA4 Attributed to Paid Channels:** £250,992.84
**Discrepancy:** **-£34,251.77 (-12.0%)**

⚠️ **Unusual Finding:** Google Ads reports 12% MORE revenue than GA4 attributes to paid channels.

Typically, GA4 sees more revenue due to view-through conversions and multi-touch attribution. This reverse discrepancy suggests:

1. **Store Visits / Phone Calls:** Google Ads may be tracking offline conversions (store visits, phone calls) that GA4 doesn't capture
2. **Attribution Model Differences:** Some Google Ads-driven conversions are being attributed to "Direct" or "Organic" in GA4's last-click model
3. **Cross-Device Tracking:** Google Ads tracks cross-device conversions better than GA4's cookie-based tracking
4. **Data Collection Issues:** GA4 may be missing some conversion events or revenue data

### Paid Channels GA4 Revenue Breakdown

| Channel | GA4 Revenue | Share of Paid |
|---------|-------------|---------------|
| Paid Search | £150,927.08 | 60.1% |
| Cross-network (PMax) | £88,004.12 | 35.1% |
| Paid Other | £10,907.64 | 4.3% |
| Paid Shopping | £1,153.996 | 0.5% |
| Paid Social | £0 | 0.0% |
| **Total Paid** | **£250,992.84** | **100%** |

---

## 📈 **Channel Deep Dive**

### 1. Direct Traffic 🔥 **Surging**

**Performance:**
- Sessions: 40,037 (+13,949 vs previous week, **+53.5%**)
- Revenue: £134,032.22 (+£8,606, +6.9%)
- Conversions: 163,578 (-31,190, -16.0%)
- Engagement Rate: 82.6% (-17.0pp)

**Week-over-Week Change:** +53.5% sessions (massive increase)

**Analysis:**
Direct traffic surged dramatically this week (+53.5%) while maintaining strong revenue growth (+6.9%). However, conversion count dropped 16%, suggesting traffic quality may have shifted.

**Possible Causes:**
1. **Christmas Shopping Season:** Returning customers going straight to site (no search)
2. **Email Marketing:** Campaigns driving "direct" traffic (email links may not be properly tagged)
3. **Attribution Shift:** Google Ads conversions being misattributed to Direct due to tracking issues
4. **Brand Awareness:** Offline marketing or PR driving direct site visits

**Recommendation:** Investigate if email campaigns are properly tagged with UTM parameters. If Direct surge continues, review attribution model settings.

---

### 2. Paid Search ⭐ **Top Revenue Driver**

**Performance:**
- Sessions: 18,773 (+290 vs previous week, +1.6%)
- Revenue: £150,927.08 (+£18,287, **+13.8%**)
- Conversions: 182,766 (+6,140, +3.5%)
- Engagement Rate: 96.8% (-3.0pp)

**Google Ads Data (All Regions):**
- Spend: £38,800.17
- Google Ads Revenue: £285,244.61
- Google Ads Conversions: 1,493.52
- Google Ads ROAS: 735%

**Blended ROAS (GA4 Paid Revenue ÷ Google Ads Spend):**
- **647%** (£250,992.84 / £38,800.17)

**Attribution Gap:** Google Ads reports £34k MORE revenue than GA4 attributes to paid channels. This suggests Google Ads is capturing offline conversions or GA4 is attributing some paid conversions to other channels (Direct/Organic).

**Week-over-Week:**
- GA4 Paid Search revenue UP 13.8%
- Sessions relatively flat (+1.6%)
- Conversion rate improving

**Analysis:** Paid Search remains the strongest revenue driver despite sessions staying flat. Revenue per session increased significantly (+12%), indicating improved traffic quality or higher AOV.

**Regional Performance (Google Ads):**
1. **UK:** £17,474 spend → £133,138 revenue (762% ROAS)
2. **USA:** £12,901 spend → £103,191 revenue (800% ROAS)
3. **EUR:** £6,112 spend → £37,658 revenue (616% ROAS) ⚠️
4. **ROW:** £2,313 spend → £11,258 revenue (487% ROAS) ⚠️

**Recommendation:** UK and USA performing well. EUR and ROW underperforming relative to account average - review campaign settings and bid strategies for these regions.

---

### 3. Organic Search 🌱 **Strong but Declining**

**Performance:**
- Sessions: 30,874 (-367 vs previous week, -1.2%)
- Revenue: £107,744.21 (-£13,093, **-10.8%**)
- Conversions: 195,539 (-29,890, -13.3%)
- Engagement Rate: 97.0% (-2.7pp)

**Week-over-Week Change:** -10.8% revenue (concerning decline)

**Analysis:** Organic Search remains a major traffic source (2nd by sessions, 3rd by revenue) but declined 10.8% week-over-week. This could be:
1. Seasonal shift (users switching to Direct during Christmas shopping)
2. Google algorithm changes or SERP feature changes
3. Increased competition from paid ads
4. Technical SEO issues

**Recommendation:** Monitor Google Search Console for ranking changes or technical errors. If decline continues, investigate keyword rankings and organic visibility.

---

### 4. Cross-network (Performance Max) 📈 **Growing**

**Performance:**
- Sessions: 20,637 (+4,520 vs previous week, **+28.0%**)
- Revenue: £88,004.12 (+£7,432, +9.2%)
- Conversions: 113,823 (+4,592, +4.2%)
- Engagement Rate: 95.7% (-4.1pp)

**Week-over-Week Change:** +28.0% sessions, +9.2% revenue

**Analysis:** Performance Max campaigns are scaling well (+28% sessions, +9.2% revenue). Session growth outpacing revenue growth suggests diminishing returns at higher volumes, which is expected with increased impression share.

**Recommendation:** Monitor efficiency metrics. If ROAS continues to hold above target, PMax has room for further budget increases.

---

### 5. Email 📧 **High Engagement, Declining Volume**

**Performance:**
- Sessions: 10,605 (-1,644 vs previous week, -13.4%)
- Revenue: £70,066.75 (+£447, +0.6%)
- Conversions: 70,054 (-19,878, -22.1%)
- Engagement Rate: **98.2%** (+4.9pp) ⭐

**Week-over-Week Change:** -13.4% sessions but revenue stable (+0.6%)

**Analysis:** Email sessions down 13.4% but revenue only down marginally (+0.6%), indicating higher-quality traffic or better targeting. Engagement rate is excellent (98.2%), meaning email subscribers are highly engaged.

**Recommendation:** Maintain current email strategy - quality over quantity. Consider increasing email frequency during Christmas season to recapture lost volume.

---

### 6. Unassigned ⚠️ **Tracking Issue**

**Performance:**
- Sessions: 38,723 (+31,336 vs previous week, **+424.1%**)
- Revenue: £73,664.01 (+£36,072, +96.0%)
- Conversions: 149,602 (+47,416, +46.4%)
- Engagement Rate: **3.2%** (-7.9pp) ⚠️

**Week-over-Week Change:** +424.1% sessions (massive increase)

**CRITICAL ISSUE:** "Unassigned" channel surged 424% and now represents 22% of all sessions. Engagement rate is only 3.2%, suggesting these are mostly bot traffic or tracking failures.

**Possible Causes:**
1. **UTM Parameter Errors:** Campaigns not properly tagged
2. **Cookie Consent Issues:** Users blocking tracking cookies
3. **Bot Traffic:** Automated scrapers or bots
4. **Dark Social:** Social media apps stripping referrer data
5. **Google Tag Manager Issues:** GA4 configuration errors

**Recommendation:** **P0 Priority** - Investigate GA4 configuration and UTM tagging. If this is legitimate traffic, £73k revenue is being misattributed. Review GTM container and consent mode settings.

---

### 7. Paid Shopping ⚠️ **Collapsed**

**Performance:**
- Sessions: 617 (-2,033 vs previous week, **-76.7%**)
- Revenue: £1,153.996 (-£11,203, -90.7%)
- Conversions: 7,483 (-14,438, -65.9%)
- Engagement Rate: 98.9% (-1.0pp)

**Week-over-Week Change:** -76.7% sessions (collapsed)

**CRITICAL ISSUE:** Paid Shopping traffic collapsed by 77% week-over-week. Revenue down 90.7%.

**Possible Causes:**
1. **Campaign Paused:** Shopping campaign(s) paused or budget depleted
2. **Feed Issues:** Merchant Centre feed disapprovals
3. **Budget Shifted:** Budget reallocated to Performance Max (which may be cannibalising Shopping traffic)
4. **Seasonal Competition:** Increased competition during Christmas shopping

**Recommendation:** **P0 Priority** - Check Google Merchant Centre for feed errors or disapprovals. Verify Shopping campaigns are active and funded. This represents a significant revenue loss (-£11k/week).

---

## 🎯 **Recommendations**

### P0 - Critical (Action This Week)

**1. Investigate "Unassigned" Channel Surge** (£73k revenue misattributed)
- **Issue:** "Unassigned" traffic surged 424% with only 3.2% engagement rate
- **Action:** Review GA4 configuration, GTM setup, and UTM tagging
- **Owner:** Beth (technical/tracking)
- **Timeline:** This week
- **Impact:** Proper attribution could reveal £73k/week revenue source

**2. Fix Paid Shopping Campaign Collapse** (-£11k revenue)
- **Issue:** Paid Shopping sessions down 77%, revenue down 91%
- **Action:** Check Merchant Centre for feed errors, verify campaigns active
- **Timeline:** Today
- **Impact:** Recover £11k/week revenue

**3. Investigate Google Ads Attribution Discrepancy** (£34k gap)
- **Issue:** Google Ads reports £34k MORE revenue than GA4 attributes to paid channels
- **Action:** Review conversion tracking setup, attribution models, offline conversion imports
- **Owner:** Beth (technical/tracking)
- **Timeline:** This week
- **Impact:** Understanding true attribution improves budget allocation decisions

---

### P1 - Important (Action Next Week)

**4. Monitor EUR and ROW Regional Performance** (Below-average ROAS)
- **Issue:** EUR (616% ROAS) and ROW (487% ROAS) underperforming vs UK (762%) and USA (800%)
- **Action:** Review campaign settings, bid strategies, and budget allocation for EUR/ROW
- **Timeline:** Next week
- **Impact:** Potential +10-15% ROAS improvement in underperforming regions

**5. Investigate Organic Search Decline** (-10.8% revenue)
- **Issue:** Organic Search revenue down 10.8% week-over-week
- **Action:** Review Google Search Console for ranking changes or technical errors
- **Timeline:** Next week
- **Impact:** Organic is 16.7% of total revenue - maintain search visibility

**6. Confirm Direct Traffic Source** (+53.5% sessions)
- **Issue:** Direct traffic surged 53.5% - may be misattributed email or Google Ads traffic
- **Action:** Verify email campaigns have proper UTM tags, review attribution model
- **Timeline:** Next week
- **Impact:** Accurate attribution improves channel ROI understanding

---

### P2 - Nice-to-Have (Ongoing)

**7. Scale Performance Max Campaigns** (+28% sessions, +9% revenue)
- **Observation:** PMax growing efficiently - sessions +28%, revenue +9%
- **Action:** Monitor ROAS - if holding above target, consider budget increase
- **Timeline:** Ongoing
- **Impact:** Additional £5-10k/week revenue potential

**8. Increase Email Frequency During Christmas** (-13% sessions but strong engagement)
- **Observation:** Email engagement excellent (98.2%) but volume down 13%
- **Action:** Test increased email frequency (2-3x/week) during peak shopping period
- **Timeline:** Ongoing through Christmas
- **Impact:** Potential +5-10% email revenue

---

## 📋 **Data Verification**

✅ **Data Sources Verified:**
- GA4 Property ID: 342726123
- Google Ads Accounts: UK (8573235780), USA (7808690871), EUR (7679616761), ROW (5556710725)
- Manager Account ID: 2569949686
- All queries use customer-level aggregation (not campaign-level)
- Currency: All figures in GBP (£)

✅ **Calculation Methods:**
- Week-over-week: (Current - Previous) / Previous × 100
- Blended ROAS: (GA4 Paid Revenue / Google Ads Spend) × 100
- Google Ads ROAS: (Google Ads Revenue / Google Ads Spend) × 100

---

## 🗓️ **Next Review**

**Weekly Cadence:** Generate this report every Monday for previous week (Mon-Sun)
**Next Report:** 24 December 2025 (covering 17-23 December)
**Key Metrics to Watch:**
- "Unassigned" channel attribution (should decrease if fixed)
- Paid Shopping recovery
- Google Ads ROAS trend
- Organic Search revenue trend

---

**Report Generated:** 17 December 2025
**Analysis by:** Claude Code (via ga4-channel-performance skill)
**Data Period:** 10-16 December 2025
