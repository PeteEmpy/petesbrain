# Devonshire Slides Corrections - November 2025

## Google Slides to Update

**Presentation:** https://docs.google.com/presentation/d/1ZOqydusG-wBNIAV_RWXHdoVOiRcs2i4W80zcSVaJTCk/edit

---

## Figures That Need Correcting

### NOVEMBER 2024 VS NOVEMBER 2025 (Month-on-month comparison)

**CORRECT figures (from HTML report):**

| Metric | Nov 2024 (Cleaned) | Nov 2025 | Change |
|--------|-------------------|----------|--------|
| **Conversions** | 62.33 | 168.00 | **+169%** |
| **Revenue** | £33,113 | £84,796 | **+156%** |
| **ROAS** | 3.82x | 7.33x | **+92%** |
| **Spend** | £6,705 | £9,359 | +40% |

**Key message:** November showed exceptional growth - nearly 3x more conversions and 2.5x more revenue year-over-year.

---

### JAN-NOV 2024 VS JAN-NOV 2025 (Cumulative year-to-date)

**CORRECT figures (from HTML report):**

| Metric | Jan-Nov 2024 (Cleaned) | Jan-Nov 2025 | Change |
|--------|----------------------|--------------|--------|
| **Conversions** | 822 | 1,269 | **+54%** |
| **Revenue** | £558,000 | £654,000 | **+17%** |
| **ROAS** | 7.44x | 6.91x | -7% |

**Key message:** Strong cumulative growth with 54% more conversions, though revenue per booking declined as volume strategy prioritised accessibility.

---

## Data Quality Note

**CRITICAL:** All 2024 figures use **cleaned data only** - Cavendish Hotel Booking conversion action (ID: 960167161).

**Highwayman contamination excluded:**
- October 2024: 21.55 phantom conversions (£0 value)
- November 2024: 111.05 phantom conversions (£0 value)
- **Total contamination:** 132.6 conversions with £0 value

Using "by conversion time" metrics eliminates October contamination but November 2024 still had 111 contaminated conversions in the raw data. The **cleaned figures above exclude this contamination**.

---

## What Slides Need Updating?

Based on Helen's email, she mentioned:
- **Slide 23** - Shows conversions UP (likely correct)
- **Slide 24** - Shows "8% fewer conversions" (WRONG - needs updating)

**Action:** Go through slides and ensure ALL year-over-year conversion comparisons use the cleaned figures above.

---

## Reference

All correct data is in: `clients/devonshire-hotels/reports/devonshire-november-2025-corrected.html`

Lines 1940-1965 contain the JavaScript data arrays with all cleaned monthly figures.
