# NDA Geographic Budget Reallocation Project - Status Update

**Date:** November 10, 2025
**Project:** Geographic Campaign Consolidation & Budget Optimization
**Status:** Discovery Phase - Awaiting Client Input

---

## Project Objective

Consolidate NDA's 39 active Google Ads campaigns into a tier-based geographic structure that focuses budget on countries driving actual enrollments, while maintaining separate visibility for:
1. **Geography:** UK / UAE / Rest of World (tiered)
2. **Course Type:** Diploma vs Degree

---

## Key Findings from Investigation

### 1. Conversion Tracking Analysis

**Enhanced Conversions For Leads (Offline):**
- Implemented: April 16, 2025 (7 months active)
- Total conversions Apr-Nov 10: ~69 conversions
- Click attribution window: 90 days
- Status: Primary for goal (drives Smart Bidding)
- Volume: ~10-15 conversions/month (still low)

**Supporting Conversion Actions:**
- `application_approved` (GA4): ~204 conversions Aug-Nov
- `application_completed` (GA4): ~111 conversions Aug-Nov
- Total all actions: ~418 conversions vs 167 actual enrollments
- Issue: Tracking applications, not enrollments

**Conversion Lag Analysis:**
- 38% convert within 2 days
- 71% convert within 11 days
- 87% convert within 21 days
- 11% take 21-90 days (long consideration period)

### 2. Geographic Conversion Data Quality Issues

**Spain:**
- Enhanced Conversions: 3 tracked
- Actual enrollments: 4
- Match rate: 75% ✅ Good

**Germany:**
- Enhanced Conversions: 0 tracked
- Actual enrollments: 7
- Match rate: 0% ❌ Critical gap

**Root Causes:**
1. Enhanced Conversions only started April 2025 (limited history)
2. Email matching failures in offline conversion uploads
3. GCLID not captured on all enrollment confirmations
4. Cross-device journeys causing attribution loss

**Implication:** Cannot rely solely on Google Ads conversion data for geographic optimization decisions. Must use enrollment spreadsheet correlation.

### 3. Current Campaign Structure

**UK Market (£31,587 spend Aug-Nov):**
- 84.8% Search, 15.2% PMax
- Diploma campaigns: £28,047 (68%)
- Degree campaigns: £13,495 (32%)
- Status: Keep separate, do not merge

**UAE Market (£16,938 spend Aug-Nov):**
- 78.9% Search, 21.1% PMax
- Diploma campaigns: £11,693 (69%)
- Degree campaigns: £5,234 (31%)
- Status: Keep separate, do not merge

**Rest of World (£60,594 spend Aug-Nov):**
- ~40% PMax, ~60% Search
- 20+ fragmented campaigns
- Many countries <£500 spend
- **Problem:** Cannot easily shift budget to high-enrollment countries

### 4. Pricing & Course Performance (DATA GAP)

**What We Know:**
- Revenue per enrollment 2025-26: £2,467 (average)
- Revenue per enrollment 2024-25: £7,217 (much higher)
- 65.8% drop suggests course mix shift

**What We DON'T Know:**
- Diploma vs Degree pricing differences
- Geographic course preferences (which markets prefer which course)
- Application → Enrollment conversion rates by course type
- Strategic positioning by market

**Action Required:** Client question sent Nov 10, 2025 to Paul Riley

---

## Proposed Campaign Structure (Pending Client Input)

### Tier-Based Framework

**UK Market (Unchanged):**
- UK | Search | Diploma
- UK | PMax | Diploma
- UK | Search | Degree
- UK | PMax | Degree

**UAE Market (Unchanged):**
- UAE | Search | Diploma
- UAE | PMax | Diploma
- UAE | Search | Degree
- UAE | PMax | Degree

**Tier A Markets (High Enrollment Performance):**
- Tier A | PMax | Diploma (GCC, Spain, proven performers)
- Tier A | Search | Diploma
- Tier A | PMax | Degree (Europe, GCC proven performers)
- Tier A | Search | Degree

**Tier B Markets (Testing/Emerging):**
- Tier B | PMax | Diploma (India, emerging markets)
- Tier B | Search | Diploma
- Tier B | PMax | Degree (India, emerging markets)
- Tier B | Search | Degree

**Tier C Markets (Zero Enrollment - Exclude):**
- Geo-exclude entirely: Malaysia, Japan, China, Denmark, Uruguay

**Total Campaign Count:** 16 campaigns (down from 39)

---

## Outstanding Questions for Client

### Email Sent: Nov 10, 2025
**File:** `email-draft-2025-11-10-geographic-consolidation-course-preferences.html`

**Key Questions:**
1. Diploma vs Degree pricing structure
2. Geographic course preferences by market (UAE, Europe, India, USA/Canada, UK)
3. Application → Enrollment conversion rates by course type
4. Strategic positioning requirements (markets requiring both courses vs single focus)

---

## Data Quality Issues Identified

### Issue 1: Enrollment Spreadsheet Missing Course Type
- **Problem:** Standardized enrollment JSON doesn't include Diploma vs Degree
- **Impact:** Cannot segment markets by course preference without client input
- **Resolution:** Awaiting client response + need to update data extraction

### Issue 2: Enhanced Conversions Attribution Gaps
- **Problem:** Only 23% of enrollments tracked in Google Ads (39 vs 167)
- **Impact:** Cannot optimize campaigns based on Google Ads conversion data alone
- **Resolution:** Build enrollment correlation report (manual process required)

### Issue 3: Conversion Lag Complexity
- **Problem:** 90-day attribution windows mean August spend affects Aug-Nov enrollments
- **Impact:** Cannot evaluate campaign performance until 90 days post-spend
- **Resolution:** Use trailing 90-day analysis windows in reporting

---

## Next Steps (Pending Client Response)

### 1. Immediate Actions (Once Client Responds):
- [ ] Update ROAS calculations with actual Diploma vs Degree pricing
- [ ] Segment countries by course preference (client-provided data)
- [ ] Finalize Tier A/B/C country assignments

### 2. Build Enrollment Correlation Report:
**Purpose:** Weekly/monthly process to match actual enrollments to Google Ads spend by country

**Process:**
1. Pull enrollment spreadsheet data by country
2. Pull Google Ads spend + application conversions by country (same period + 90-day lag)
3. Calculate:
   - Application → Enrollment conversion rate by country
   - True CPA by country (Spend ÷ Actual Enrollments)
   - True ROAS by country ((Enrollments × Course Fee) ÷ Spend)
4. Identify optimization opportunities:
   - High app volume, low enrollment rate → investigate quality issues or geo-exclude
   - Low app volume, high enrollment rate → scale opportunity
   - High spend, zero enrollments → immediate geo-exclude

### 3. Campaign Restructuring:
- [ ] Create new campaign structure in Google Ads Editor
- [ ] Migrate budgets to tier-based model
- [ ] Set up proper geo-targeting for each tier
- [ ] Maintain UK/UAE separation throughout

### 4. Ongoing Monitoring:
- [ ] Weekly enrollment correlation report
- [ ] Monthly Enhanced Conversions upload validation
- [ ] Quarterly tier reassignment (promote/demote countries based on performance)

---

## Key Decisions Required

1. **Course Pricing Confirmation:** Actual Diploma vs Degree fees (affects all ROAS calculations)
2. **Geographic Tiering:** Which countries belong in Tier A vs Tier B (client input + data)
3. **Diploma/Degree Split:** Which markets get both courses vs single focus (strategic decision)
4. **Budget Allocation:** PMax vs Search split by tier (data-driven + client preference)

---

## Expected Impact

### Current State:
- 39 campaigns with fragmented budgets
- Cannot easily shift spend to high-performing countries
- ~£616/month wasted on zero-enrollment countries
- Limited visibility into actual enrollment performance by market

### Future State (Post-Consolidation):
- 16 campaigns with clear tier-based structure
- Easy budget reallocation to proven enrollment markets
- Zero spend on non-performing geographies
- Monthly enrollment correlation reports for data-driven optimization
- Proper course-level segmentation (Diploma vs Degree)

---

## Files Created

1. `email-draft-2025-11-10-geographic-consolidation-course-preferences.html` - Client question email
2. `geographic-budget-reallocation-project-status-2025-11-10.md` - This status document

## Related Analysis Files

1. `documents/COUNTRY-CORRELATION-EXECUTIVE-SUMMARY.md` - Nov 3 country analysis
2. `documents/financial-enrollment-correlation-analysis-2025-11-03.md` - Revenue analysis
3. `spreadsheets/country-correlation-analysis.csv` - Country performance data
4. `product-feeds/NDA-International-Enrolments-STANDARDIZED.json` - Enrollment data

---

## Notes

- Enhanced Conversions implementation still maturing (only 7 months old)
- Need to fix email matching in Enhanced Conversions uploads (Germany gap)
- Consider adding GCLID tracking to enrollment confirmation pages
- Weekly-client-strategy.json updated: "Geographic Expansion Budget Optimization" marked as "data_quality_issue"
