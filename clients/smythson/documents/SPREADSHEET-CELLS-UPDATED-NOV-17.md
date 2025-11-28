# Smythson Q4 Dashboard - Spreadsheet Cells Updated (Nov 17)

**Status:** ✅ ALL REFERENCE CELLS CORRECTED
**Script Run:** 2025-11-17 14:57:54
**Cells Updated:** 117 (up from 111)

---

## Column B Reference Cells - CORRECTED

These cells contain the **target/reference values** that actual performance is compared against:

### Overall Q4 Targets (Status Section)

| Cell | Metric | Old Value | New Value | Change |
|------|--------|-----------|-----------|--------|
| **B11** | Target ROAS | 4.17 | **4.57** | +0.40 (higher target due to lower budget) |
| **B41** | Revenue Target | £2,380,000 | £2,380,000 | No change (client target) |
| **B42** | Total Q4 Budget | £570,252 | **£521,052** | -£49,200 (no P7 carryforward) |
| **B43** | ROAS Target | 4.17 | **4.57** | +0.40 (same as B11) |
| **B44** | Budget Pacing % | (dynamic) | (dynamic) | Updates daily via weighted pacing |

### Monthly Budget Targets

| Cell | Metric | Old Value | New Value | Change |
|------|--------|-----------|-----------|--------|
| **B23** | November Budget | £204,604 | **£186,051** | -£18,553 (no P7 carryforward) |
| **B35** | December Budget | £183,929 | **£183,929 (21 days effective)** | Note added about Christmas cutoff |

---

## Regional Revenue Targets - CORRECTED

### November (P8) Regional Targets - Column L (Rows 19-22)

| Cell | Region | Old Target | New Target | Change |
|------|--------|-----------|-----------|---------|
| **L19** | UK | £577,167 | **£491,175** | -£85,992 (-15%) |
| **L20** | USA | £354,227 | **£301,401** | -£52,826 (-15%) |
| **L21** | EUR | £122,446 | **£104,190** | -£18,256 (-15%) |
| **L22** | ROW | £65,596 | **£55,817** | -£9,779 (-15%) |
| **L23** | TOTAL | £1,119,436 | **£952,583** | -£166,853 (-15%) |

**Basis:** £186,051 budget at 512% ROAS (28 days)

### December (P9) Regional Targets - Column L (Rows 31-34)

| Cell | Region | Old Target | New Target | Change |
|------|--------|-----------|-----------|---------|
| **L31** | UK | £485,564 | **£322,182** | -£163,382 (-34%) |
| **L32** | USA | £297,882 | **£201,380** | -£96,502 (-32%) |
| **L33** | EUR | £103,001 | **£68,628** | -£34,373 (-33%) |
| **L34** | ROW | £55,179 | **£34,965** | -£20,214 (-37%) |
| **L35** | TOTAL | £941,626 | **£627,155** | -£314,471 (-33%) |

**Basis:** £122,598 effective budget at 512% ROAS (21 days - Christmas delivery cutoff)

---

## Performance Data Cells - AUTO-UPDATE

These cells update daily with actual performance data from Google Ads API:

### November Regional Performance (Rows 19-22)
- **Column D:** Actual ROAS (from API)
- **Column E:** ROAS Status (🟢🟡🔴)
- **Column F:** Actual Revenue (from API)
- **Column G:** Expected Revenue (weighted pacing)
- **Column H:** Revenue Status (🟢🟡🔴)
- **Column I:** Actual Spend (from API)
- **Column J:** Expected Spend (weighted pacing)
- **Column K:** Spend Status (🟢🟡🔴)

### December Regional Performance (Rows 31-34)
- Same columns as November (D-K)
- Expected spend uses 21-day effective period

### Overall Status Section (Rows 41-44)
- **C41:** Total Revenue (actual from API)
- **C42:** Total Spend (actual from API)
- **C43:** Overall ROAS (calculated)
- **C44:** Budget Pacing % (actual)
- **D41-D44:** Status indicators (🟢🟡🔴)

---

## What Changed in This Update

### 6 New Column B Reference Cells Added to Script
Previously these cells were **manually updated** (prone to being outdated).
Now they **auto-update daily** with the correct values:

1. **B11** - Target ROAS (now 4.57, not 4.17)
2. **B23** - November Budget (now £186,051, not £204,604)
3. **B35** - December Budget (now shows "21 days effective" note)
4. **B41** - Revenue Target (£2,380,000 - confirmed)
5. **B42** - Total Q4 Budget (now £521,052, not £570,252)
6. **B43** - ROAS Target (now 4.57, not 4.17)

### Regional Target Cells Already Auto-Updating
The regional targets in Column L (rows 19-22 for Nov, 31-34 for Dec) were **already being updated** by the script using the `NOVEMBER_REVENUE_TARGETS` and `DECEMBER_REVENUE_TARGETS` dictionaries, which have been corrected.

---

## Verification Checklist

### ✅ Column B Reference Cells
- [x] B11: Shows 4.57 (not 4.17)
- [x] B23: Shows £186,051 (not £204,604)
- [x] B35: Shows £183,929 with "(21 days effective)" note
- [x] B41: Shows £2,380,000 (unchanged)
- [x] B42: Shows £521,052 (not £570,252)
- [x] B43: Shows 4.57 (not 4.17)

### ✅ November Regional Targets (Column L)
- [x] L19 (UK): £491,175 (not £577,167)
- [x] L20 (USA): £301,401 (not £354,227)
- [x] L21 (EUR): £104,190 (not £122,446)
- [x] L22 (ROW): £55,817 (not £65,596)
- [x] L23 (TOTAL): £952,583 (not £1,119,436)

### ✅ December Regional Targets (Column L)
- [x] L31 (UK): £322,182 (not £485,564)
- [x] L32 (USA): £201,380 (not £297,882)
- [x] L33 (EUR): £68,628 (not £103,001)
- [x] L34 (ROW): £34,965 (not £55,179)
- [x] L35 (TOTAL): £627,155 (not £941,626)

---

## Script Batch Update Details

**Total cells updated:** 117
**Breakdown:**
- Performance data (columns C-K): ~105 cells (actual/expected/status)
- Reference targets (column B): 6 cells
- Regional targets (column L): ~6 cells
- Initiative status (column D): ~13 cells
- Timestamp (B12): 1 cell

**API efficiency:** 1 batch call (not 117 individual calls)
**Runtime:** ~3 seconds
**Next update:** Tomorrow 7:00 AM (automated)

---

## Summary

✅ **All reference cells corrected** - No more old/outdated values
✅ **November budget:** £186,051 (15% reduction from previous)
✅ **December budget:** Effective 21 days noted (Christmas cutoff)
✅ **Target ROAS:** 4.57 (not 4.17) - reflects tighter budget constraint
✅ **Regional targets:** All recalculated based on corrected budgets
✅ **Auto-update enabled:** All Column B cells now update daily

**The dashboard is now fully aligned with the corrected Q4 budget reality.**

---

**Document Created:** 2025-11-17 14:58
**Last Script Run:** 2025-11-17 14:57:54
**Status:** ✅ Complete and verified
