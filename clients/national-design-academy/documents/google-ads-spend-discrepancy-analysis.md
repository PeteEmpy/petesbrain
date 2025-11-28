# Google Ads Spend Discrepancy Analysis - NDA

**Date:** November 3, 2025
**Analysis Period:** August 1 - October 31, 2025 (Academic Year 2025-26 YTD)

---

## Summary of Discrepancy

| Source | Amount | Difference |
|--------|--------|------------|
| **Paul's Financial Data** | £130,729 | Baseline |
| **Google Ads API (NDA Account)** | £107,449 | -£23,280 (-17.8%) |

**Variance:** £23,280 (17.8% lower in API data)

---

## Possible Explanations

### 1. **Facebook Ads Included in Paul's Figure** ❌

Paul's screenshot shows separate lines:
- Facebook: £16,920
- Google: £130,729
- **Total Ad Spend: £147,649**

So the £130,729 figure **should be Google Ads only**, not including Facebook.

---

### 2. **Date Range Mismatch** ⚠️

Paul's data is labeled "YTD Total YE 2026" which likely means:
- **Academic Year 2025-26 Year-to-Date**
- Academic years typically run **September to August**

However, I queried:
- **August 1 - October 31, 2025** (3 months)

**Possible issue:**
- If Paul's "YTD" includes July 2025 (end of previous academic year)
- If Paul's YTD includes dates beyond Oct 31

**Need to clarify:** What exact date range does Paul's £130,729 represent?

---

### 3. **NMA (Motorsport) Spend Included** ❓

Paul's business runs:
- **NDA** (National Design Academy) - Account ID: 1994728449
- **NMA** (National Motorsport Academy) - Separate account ID: 5622468019

**Possibility:** Paul's financial system might combine NDA + NMA spend into one "Google Ads" line.

**Next step:** Query NMA account for same period to check.

---

### 4. **VAT or Currency Conversion** ❓

- API returns spend in account currency (likely GBP)
- Financial system might include VAT (20%) or currency conversion
- £107,449 × 1.20 (VAT) = £128,939 (close to £130,729!)

**Possible:** Paul's figure includes VAT, API figure doesn't.

---

### 5. **Management Fees or Agency Costs** ❓

Paul's £130,729 might include:
- Google Ads spend (£107,449)
- Roksys management fees (£23,280)
- Platform fees or other costs

**Need to clarify:** Is £130,729 pure media spend or total advertising cost?

---

### 6. **Timing of Data Pull** ⚠️

- Paul's data: "YTD Total YE 2026" - possibly pulled on a specific date
- API data: Pulled November 3, 2025 for Aug 1 - Oct 31
- Possible spend adjustments, refunds, or corrections between pulls

---

## What Google Ads API Shows

**Campaigns with spend (Aug 1 - Oct 31, 2025):** 39 campaigns

**Top spending campaigns:**
1. NDA | UK | Search | Interior Design Diploma: £18,695
2. NDA | UAE | Search | Interior Design Diploma: £7,185
3. NDA | Search | Interior Design Degree- UK: £6,974
4. NDA | P Max Reboot | ROTW: £7,205
5. NDA | P Max | Interior Design Diploma - UK: £6,085

**Total verified:** £107,449.27

---

## Recommendations

### Immediate Actions:

1. **Confirm Date Range with Paul:**
   - What exact dates does "YTD Total YE 2026" cover?
   - Is it Sep 1, 2025 - Oct 31, 2025?
   - Or Aug 1, 2025 - Oct 31, 2025?
   - Or includes July 2025?

2. **Clarify What's Included:**
   - Is £130,729 pure Google Ads media spend?
   - Or does it include VAT?
   - Or does it include NMA (motorsport academy)?
   - Or does it include management fees?

3. **Check NMA Account:**
   - Query NMA (5622468019) for same period
   - Check if NMA spend is being combined with NDA

4. **Reconcile with Invoice:**
   - Compare API data with Google Ads invoice
   - Google Ads invoices show exact charges

---

## Impact on ROAS Analysis

**Current analysis used:** £130,729 Google spend (from Paul)

**If correct spend is £107,449:**
- ROAS would be **739%** (not 538%)
- Cost per enrollment: £334 (not £459)
- More efficient than currently calculated

**This would completely change the narrative:**
- Instead of declining efficiency, NDA would show **improved efficiency**
- ROAS of 739% vs prior year 819% = only 10% decline (not 34%)

---

## Next Steps

**Critical:** We need to resolve this £23,280 discrepancy before finalising any ROAS analysis or recommendations.

**Action:** Draft email to Paul asking for clarification on:
1. Exact date range for £130,729 figure
2. What's included (VAT, NMA, fees, etc.)
3. Whether it matches Google Ads invoice total

**Once resolved:** Recalculate all ROAS and efficiency metrics with correct spend figure.
