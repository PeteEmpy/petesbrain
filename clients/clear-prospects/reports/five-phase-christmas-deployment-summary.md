# Clear Prospects - Five-Phase Christmas Deployment 2024

**Data-Driven Strategy Based on Christmas 2023 Performance**

---

## 📊 Christmas 2023 Analysis Summary

### Key Performance Periods (Dec 20, 2023 - Jan 10, 2024)

| Period | Daily Spend | ROAS | Status |
|--------|------------|------|---------|
| **Dec 20** (Pre-shutdown) | £577 | 105% | ✅ Profitable |
| **Dec 21** (Budget cut) | £47 | 135% | ✅ Profitable (92% reduction) |
| **Dec 22-23** | £0 | N/A | ⏸️ No data (likely paused) |
| **Dec 24-25** (Christmas) | £85 avg | 37% | ❌ **LOSING MONEY (-£111)** |
| **Dec 26-31** (Boxing Day) | £159 avg | 201% | ✅ **Recovered - profitable** |
| **Jan 1-10** (New Year) | £296 avg | 147% | ✅ Strong performance |

### Critical Insights

1. **Dec 21-23**: Budget cut by 92% (£577 → £47/day) successfully kept campaigns warm while remaining profitable (135% ROAS)
2. **Dec 24-25**: Christmas shutdown period **LOST MONEY** (37% ROAS) - spent £170, earned £59 = -£111 loss
3. **Dec 26+**: Boxing Day recovery was immediate and profitable (201% ROAS)
4. **Jan 1-10**: New Year period continued strong performance (147% ROAS)

---

## 🎯 Five-Phase Deployment Strategy

### Phase 1: Run-up to Christmas ✓ DEPLOYED
**Dates**: December 15, 2024  
**Status**: Already deployed

**Budget Changes**:
- HSG H&S PMax: £70 → £510/day (+629%)
- WBS H&S PMax: £150 → £310/day (+107%)
- **Total: £845/day**

**Performance**: HSG 151% ROAS, WBS 139% ROAS

---

### Phase 2: Christmas Peak ⏳ READY
**Dates**: December 16-19, 2024  
**CSV**: `phase2-christmas-peak-dec16.csv`

**Strategy**: Pause BMPM (stop losses), maintain HSG/WBS at peak levels

**Changes**:
- BMPM P Max Shopping: PAUSE
- BMPM Search | Promotional Merchandise: PAUSE
- All other campaigns: Maintained

**Total**: ~£820/day (down from £845/day)

**Deployment Command**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/budget-deployer
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase2-christmas-peak-dec16.csv
```

---

### Phase 3: Christmas Shutdown (Keep Warm) ⏳ READY
**Dates**: December 20-25, 2024  
**CSV**: `phase3-shutdown-keep-warm-dec20.csv`

**Strategy**: Keep campaigns warm during staff backlog and Christmas shutdown

**Based on 2023 data**:
- Dec 21-23: £47/day (135% ROAS - profitable)
- Dec 24-25: £85/day (37% ROAS - **LOST MONEY**)

**2024 Target**: **£50/day total** (94% reduction from peak)

**Budget Allocation**:
- BMPM: £1.00/day total
  - P Max: £0.60
  - Search: £0.40
- HSG: £27.19/day total
  - H&S PMax: £20.46
  - Other campaigns: £6.73
- WBS: £21.80/day total
  - H&S PMax: £12.44
  - Other campaigns: £9.36

**Deployment Command**:
```bash
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase3-shutdown-keep-warm-dec20.csv
```

---

### Phase 4: Boxing Day Recovery ⏳ READY
**Dates**: December 26, 2024 - January 5, 2025  
**CSV**: `phase4-boxing-day-recovery-dec26.csv`

**Strategy**: Resume moderate spending for Boxing Day sales and New Year recovery

**Based on 2023 data**:
- Dec 26-31: £159/day average (201% ROAS - profitable)
- Jan 1-5: £296/day average (147% ROAS - strong)

**2024 Target**: **£150/day total** (moderate reduction, keep campaigns warm for January)

**Budget Allocation**:
- BMPM: £3.01/day total
  - P Max: £1.81
  - Search: £1.20
- HSG: £81.61/day total
  - H&S PMax: £61.39
  - Other campaigns: £20.22
- WBS: £65.38/day total
  - H&S PMax: £37.31
  - Other campaigns: £28.07

**Deployment Command**:
```bash
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase4-boxing-day-recovery-dec26.csv
```

---

### Phase 5: January Seasonal Budgets ⏳ READY
**Dates**: January 6, 2025 onwards  
**CSV**: `phase5-january-seasonal-jan6.csv`

**Strategy**: Full seasonal budgets based on year-on-year analysis (Jan 2024 vs Dec 2024)

**Seasonal Factors** (Jan 2024 as % of Dec 2024):
- **BMPM**: 91.7% (minimal seasonality - B2B trade)
- **HSG**: 26.0% (massive drop - gift business)
- **WBS**: 44.2% (significant drop - also gift-focused)

**2025 Budget Allocation**:
- **BMPM**: £22.93/day (RESTORED - not paused)
  - P Max: £13.76
  - Search: £9.17
- **HSG**: £176.28/day (26% of Dec peak)
  - H&S PMax: £132.60
  - Other campaigns: £43.68
- **WBS**: £240.09/day (44% of Dec peak)
  - H&S PMax: £137.02
  - Other campaigns: £103.07

**Total**: **£439.30/day**

**Deployment Command**:
```bash
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase5-january-seasonal-jan6.csv
```

---

## 📅 Deployment Timeline

```
Dec 15  ━━━━━━━┓
            Phase 1: Christmas Peak (£845/day) ✓ DEPLOYED
Dec 16  ━━━━━━━┓
            Phase 2: BMPM Pause (£820/day)
Dec 20  ━━━━━━━┓
            Phase 3: Shutdown Keep Warm (£50/day)
Dec 26  ━━━━━━━┓
            Phase 4: Boxing Day Recovery (£150/day)
Jan 6   ━━━━━━━┓
            Phase 5: January Seasonal (£439/day)
```

---

## ⚠️ Key Warnings

1. **Dec 24-25 (Christmas)**: Phase 3 includes Christmas Day and Boxing Day morning. Last year this period LOST MONEY (37% ROAS). Budgets are kept minimal (£50/day) to reduce losses while keeping campaigns warm.

2. **Staff Availability**: Michael finishes Dec 19, staff finish Dec 23. During shutdown, fulfillment is slower/delayed. Website messaging should warn customers of delivery delays.

3. **BMPM in January**: Do NOT keep BMPM paused into January. January 2024 showed 91.7% spend levels vs December with profitable performance. Phase 5 restores BMPM to seasonal levels.

---

## 📈 Expected Performance

| Phase | Daily Spend | Expected ROAS (based on 2023) | Rationale |
|-------|------------|-------------------------------|-----------|
| Phase 1 (Dec 15) | £845 | 140-150% | Christmas peak demand |
| Phase 2 (Dec 16-19) | £820 | 140-150% | Maintain peak, cut losses |
| Phase 3 (Dec 20-25) | £50 | 80-135% | Keep warm, accept lower ROAS |
| Phase 4 (Dec 26-Jan 5) | £150 | 150-200% | Boxing Day recovery |
| Phase 5 (Jan 6+) | £439 | 130-180% | Normal January performance |

---

## ✅ Active Campaigns Included

**Total: 13 campaigns** (excludes 6 past experiment campaigns)

- **BMPM**: 2 campaigns
- **HSG**: 6 campaigns
- **WBS**: 5 campaigns
- **TJR**: 0 campaigns (experiment ended 2018)

---

## 📊 Total Spend Projection

| Phase | Duration | Daily Spend | Total Spend |
|-------|----------|-------------|-------------|
| Phase 1 | 1 day (Dec 15) | £845 | £845 |
| Phase 2 | 4 days (Dec 16-19) | £820 | £3,280 |
| Phase 3 | 6 days (Dec 20-25) | £50 | £300 |
| Phase 4 | 11 days (Dec 26-Jan 5) | £150 | £1,650 |
| Phase 5 | 25 days (Jan 6-31) | £439 | £10,975 |
| **TOTAL** | **47 days** | - | **£17,050** |

**Average daily spend Dec 15 - Jan 31**: £363/day

---

**Generated**: December 16, 2024  
**Based on**: Christmas 2023 actual performance data + Jan 2024 vs Dec 2024 YoY analysis
