# Smythson Q4 Dashboard - Update Required (Dec 17)

**Analysis Date**: 2025-12-17
**Issue**: Dashboard using outdated pre-P9 crisis targets from Nov 3, 2025

---

## 🚨 Critical Finding: Dashboard Out of Sync with Current Strategy

### Current Dashboard Targets (Nov 3, 2025 - OUTDATED)

| Metric | Dashboard Value | Status |
|--------|-----------------|--------|
| **Total Q4 Budget** | £367,014 | ❌ **WRONG** |
| **Revenue Target** | £780,691 | ❌ **WRONG** |
| **Target ROAS** | 2.13 blended | ❌ **WRONG** |
| **Regional Targets** | UK: 3.0, USA: 1.5, EUR: 1.5, ROW: 1.0 | ❌ **OUTDATED** |
| **Q4 Period** | Oct 29 - Dec 31 (9 weeks) | ❌ **OUTDATED** |

### Current P9 Strategy Targets (Dec 1-31, 2025 - CORRECT)

| Metric | Actual P9 Value | Status |
|--------|-----------------|--------|
| **P9 Budget** | £171,128 | ✅ HARD CONSTRAINT |
| **Revenue Target** | £810k-£992k range | ✅ REALISTIC |
| **Budget Already Spent (Dec 1-16)** | £109,020 | ⚠️ 64% used |
| **Budget Remaining** | £61,980 | ⚠️ 36% for 14 days |
| **P9 Period** | Dec 1-31 (31 days) | ✅ CURRENT |

### Discrepancy Summary

| Metric | Dashboard | Reality | Difference |
|--------|-----------|---------|------------|
| **Budget** | £367,014 | £171,128 | **-53%** (£196k overestimated) |
| **Revenue Target** | £780,691 | £810k-£992k | Different range entirely |
| **Time Period** | Q4 (Oct 29-Dec 31) | P9 (Dec 1-31) | Only tracking December |
| **ROAS Targets** | UK: 3.0, USA: 1.5 | Post-cuts: UK ~5.0+, USA ~4.0+ | Significantly higher actual |

---

## Why Dashboard is Outdated

### Timeline of Events

1. **Nov 3, 2025**: Dashboard created with original Q4 strategy
   - Full Q4 period (Oct 29 - Dec 31)
   - Budget: £367k
   - Conservative ROAS targets

2. **Dec 1, 2025**: P9 Budget Crisis
   - Hard budget constraint discovered: £171k for December only
   - 48% budget cuts implemented Dec 4
   - Strategy completely revised
   - New revenue targets calculated

3. **Dec 4-17, 2025**: Multiple P9 strategy documents created
   - P9-REVENUE-STRATEGY-FINAL.html
   - P9-IMPLEMENTATION-PLAN-FINAL.html
   - P9-BUDGET-ALIGNMENT-VISUAL.html
   - Budget lag analysis completed
   - Daily monitoring implemented

4. **Dec 17, 2025**: Dashboard still using Nov 3 targets
   - No update to reflect P9 reality
   - Traffic lights showing incorrect status
   - Budget pacing calculations wrong

---

## Impact of Outdated Dashboard

### ❌ **False Status Indicators**

**Budget Pacing**:
- Dashboard thinks: "We have £367k to spend over 9 weeks"
- Reality: "We have £171k to spend over 31 days (£109k already used)"
- Result: Budget pacing showing GREEN when should show RED

**Revenue Targets**:
- Dashboard thinks: "Target is £780k"
- Reality: "Target is £810k-£992k"
- Result: Revenue status may be incorrect

**ROAS Expectations**:
- Dashboard thinks: "UK should be 3.0x ROAS"
- Reality: "UK is achieving 5.0-8.0x ROAS post-budget cuts"
- Result: Missing the full picture of profitability improvement

### ❌ **Misleading Weekly Reports**

- Email integration sends dashboard snapshot to Alex weekly
- Alex receiving outdated metrics
- Decision-making based on incorrect targets

### ❌ **No P9 Phase Tracking**

- Dashboard shows Q4 phases (1-5) from Nov 3 strategy
- Doesn't show P9 phases (Cyber Week, Pre-Christmas, etc.)
- Missing current strategic initiatives

---

## What Dashboard Needs

### ✅ **Required Updates**

1. **Budget Section**
   - Change from £367k to £171k
   - Show December-only period (Dec 1-31)
   - Add "Budget Used" tracker (£109k / £171k = 64%)
   - Add "Days Remaining" (14 days)
   - Add "Required Daily Avg" (£4,427/day)

2. **Revenue Section**
   - Update target range to £810k-£992k
   - Add "Realistic" vs "Optimistic" scenarios
   - Show actual ROAS achieved (not just targets)

3. **Regional Breakdown**
   - Update to 4 accounts (UK, USA, EUR, ROW) with correct IDs:
     - UK: 8573235780
     - USA: 7808690871
     - EUR: 7679616761
     - ROW: 5556710725
   - Show actual ROAS vs revised targets
   - Add spend per account (not just total)

4. **Phase Tracking**
   - Replace Q4 phases with P9 phases:
     - Phase 1: Cyber Week (Dec 2-7)
     - Phase 2a: Last Order Dates (Dec 8-16)
     - Phase 2b: Post-Last Orders (Dec 17-23)
     - Phase 3: Christmas Day (Dec 24-26)
     - Phase 4: Sale Launch (Dec 27-31)

5. **Status Indicators**
   - Recalculate all traffic lights based on P9 targets
   - Add "Budget Risk" indicator (overspend projection)
   - Add "Phase Status" (which P9 phase we're in)

6. **Automation Script**
   - Update `update-q4-dashboard.py` to pull correct metrics
   - Use P9 targets, not Q4 targets
   - Calculate budget pacing correctly

---

## Immediate Actions Required

### 1. **Stop Automated Updates** (Until Fixed)

```bash
# Temporarily disable dashboard automation
launchctl unload ~/Library/LaunchAgents/com.petesbrain.smythson-dashboard.plist
```

**Why?**: Preventing incorrect data from being sent to Alex in weekly emails

### 2. **Update Dashboard Manually**

**Option A**: Create NEW P9 dashboard from scratch
- Copy existing dashboard structure
- Replace all targets with P9 numbers
- Update automation script to match
- Test thoroughly before re-enabling automation

**Option B**: Update existing dashboard in-place
- Change header from "Q4 Strategy" to "P9 Strategy (December)"
- Update all target cells with P9 numbers
- Verify automation script pulls correct data
- Re-test and re-enable

**Recommendation**: Option A (clean slate prevents confusion)

### 3. **Document Dashboard Update**

Create: `clients/smythson/documents/dashboard-p9-migration-checklist.md`

Track:
- Old values vs new values
- What was changed
- What was tested
- When re-enabled

### 4. **Notify Alex**

If Alex has been receiving weekly dashboard emails with outdated targets:
- Inform him dashboard was using Nov 3 pre-crisis numbers
- Explain P9 budget constraint wasn't reflected
- Clarify that actual performance is being tracked correctly (just dashboard display was wrong)

---

## Recommended Next Steps

1. ✅ **Acknowledge dashboard is outdated** (this document)
2. ⏸️ **Pause automation** until fixed
3. 📝 **Create P9 dashboard spec** (list all fields and values)
4. 🔨 **Build/update dashboard** (manual or automated)
5. ✅ **Test with real data** (verify traffic lights correct)
6. 🚀 **Re-enable automation**
7. 📧 **Send corrected update** to Alex

---

## Technical Notes

**Dashboard Spreadsheet**: https://docs.google.com/spreadsheets/d/10vRzZJuUQMX0l86plKcuZfdoiidoexI1LPYnhr6gJlU/edit

**Automation Script**: `clients/smythson/scripts/update-q4-dashboard.py`

**LaunchAgent**: `~/Library/LaunchAgents/com.petesbrain.smythson-dashboard.plist`

**Current Status**:
- Last updated: Nov 10, 2025 (automation fix)
- Using targets from: Nov 3, 2025
- Current date: Dec 17, 2025
- **Lag**: 44 days outdated

---

## Conclusion

The Q4 Strategy Dashboard is using targets from **before the P9 budget crisis** and is **completely out of sync** with current December strategy.

**Critical Action**: Dashboard must be updated or rebuilt to reflect:
- £171k budget constraint (not £367k)
- P9 phases (not Q4 phases)
- Current ROAS targets
- Budget risk indicators

**Priority**: HIGH - Alex is receiving incorrect metrics in weekly emails.

**Estimated Time to Fix**: 2-3 hours (rebuild dashboard + test automation)

---

**Document Status**: Dashboard audit complete
**Action Required**: Update dashboard to P9 strategy before next weekly email
