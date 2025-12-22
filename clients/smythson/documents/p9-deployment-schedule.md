# P9 Deployment Schedule - Balanced Strategy
**Total P9 Budget Remaining: £53,239 (Dec 22-28)**

## Deployment Timeline & Commands

### 🗓️ December 22 (Sunday) - Minimal Start
**Time**: 00:01 GMT
**Budget**: £2,000 total
**File**: `p9-dec-22-minimal.csv`
**Command**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer
python3 deploy_budgets.py \
  --csv-file ../../clients/smythson/universal-budget-deployer/p9-dec-22-minimal.csv \
  --mode apply \
  --verify
```

---

### 🗓️ December 23 (Monday) - Maintain Minimal
**Time**: 00:01 GMT
**Budget**: £2,000 total
**File**: `p9-dec-23-minimal.csv`
**Command**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer
python3 deploy_budgets.py \
  --csv-file ../../clients/smythson/universal-budget-deployer/p9-dec-23-minimal.csv \
  --mode apply \
  --verify
```

---

### 🎄 December 24 (Tuesday) - SALE LAUNCH
**Time**: 17:45 GMT (15 minutes before sale at 18:00)
**Budget**: £3,500 total
**File**: `p9-dec-24-6pm-sale-launch.csv`
**Critical**: Must deploy BEFORE 18:00 when sale goes live!
**Command**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer
python3 deploy_budgets.py \
  --csv-file ../../clients/smythson/universal-budget-deployer/p9-dec-24-6pm-sale-launch.csv \
  --mode apply \
  --verify
```

**Post-deployment monitoring**:
```bash
# Check performance at 19:00, 20:00, 21:00, 22:00
python3 verify_budgets.py --check-performance
```

---

### 🎅 December 25 (Wednesday) - Christmas Day Scale
**Time**: 00:01 GMT
**Budget**: £6,000 total
**File**: `p9-dec-25-christmas.csv`
**Command**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer
python3 deploy_budgets.py \
  --csv-file ../../clients/smythson/universal-budget-deployer/p9-dec-25-christmas.csv \
  --mode apply \
  --verify
```

---

### 🎁 December 26 (Thursday) - BOXING DAY MAXIMUM
**Time**: 00:01 GMT
**Budget**: £12,000 total (peak day)
**File**: `p9-dec-26-boxing-day.csv`
**Critical**: Largest budget day - monitor closely!
**Command**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer
python3 deploy_budgets.py \
  --csv-file ../../clients/smythson/universal-budget-deployer/p9-dec-26-boxing-day.csv \
  --mode apply \
  --verify
```

**Hourly monitoring required**:
```bash
# Run every hour from 01:00 to 23:00
python3 verify_budgets.py --check-performance --alert-if-issues
```

---

### 📈 December 27 (Friday) - Sustained High
**Time**: 00:01 GMT
**Budget**: £10,000 total
**File**: `p9-dec-27-sustained.csv`
**Command**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer
python3 deploy_budgets.py \
  --csv-file ../../clients/smythson/universal-budget-deployer/p9-dec-27-sustained.csv \
  --mode apply \
  --verify
```

---

### 🏁 December 28 (Saturday) - Final P9 Day
**Time**: 00:01 GMT
**Budget**: £8,000 total
**File**: `p9-dec-28-final.csv`
**Command**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer
python3 deploy_budgets.py \
  --csv-file ../../clients/smythson/universal-budget-deployer/p9-dec-28-final.csv \
  --mode apply \
  --verify
```

---

## Pre-deployment Checklist

### Before EACH deployment:
1. ✅ Verify current budgets match expected "current_budget_gbp" in CSV
2. ✅ Check account access is working
3. ✅ Ensure no other budget changes are pending
4. ✅ Have rollback CSV ready (current state)

### Critical Dec 24 Checklist (17:30 GMT):
1. ✅ Test API connection to all 4 accounts
2. ✅ Verify sale is scheduled for 18:00
3. ✅ Have monitoring dashboard open
4. ✅ Prepare hourly check schedule
5. ✅ Alert Alex that deployment is starting

---

## Monitoring & Alerts

### Key Metrics to Track:
- **Spend Rate**: Actual vs expected hourly spend
- **ROAS**: By campaign and account
- **Budget Utilization**: % of daily budget used
- **Top Performers**: Campaigns hitting budget limits

### Alert Thresholds:
- 🔴 **Critical**: Any campaign >150% of expected spend rate
- 🟡 **Warning**: ROAS drops >30% from baseline
- 🟢 **Success**: Within 10% of expected spend with ROAS >400%

### Performance Tracking Commands:
```bash
# Quick performance check
python3 /Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer/check_performance.py \
  --date 2025-12-26 \
  --accounts 8573235780,7808690871,7679616761,5556710725

# Detailed ROAS analysis
python3 analyze_roas.py --date-range 2025-12-24:2025-12-28
```

---

## Rollback Procedures

If issues arise, use these rollback files:

### Emergency Rollback to Minimal (£2,000):
```bash
python3 deploy_budgets.py \
  --csv-file rollback/p9-emergency-minimal.csv \
  --mode apply \
  --force
```

### Rollback Specific Account:
```bash
# UK only
python3 deploy_budgets.py \
  --csv-file rollback/p9-uk-previous-state.csv \
  --mode apply \
  --customer-id 8573235780
```

---

## Files Summary

| Date | Time | Budget | Campaigns | File |
|------|------|--------|-----------|------|
| Dec 22 | 00:01 | £2,000 | 44 | p9-dec-22-minimal.csv |
| Dec 23 | 00:01 | £2,000 | 44 | p9-dec-23-minimal.csv |
| **Dec 24** | **17:45** | **£3,500** | **49** | **p9-dec-24-6pm-sale-launch.csv** |
| Dec 25 | 00:01 | £6,000 | 51 | p9-dec-25-christmas.csv |
| **Dec 26** | **00:01** | **£12,000** | **59** | **p9-dec-26-boxing-day.csv** |
| Dec 27 | 00:01 | £10,000 | 58 | p9-dec-27-sustained.csv |
| Dec 28 | 00:01 | £8,000 | 58 | p9-dec-28-final.csv |

**Total P9 Sale Period Spend**: £53,500 (includes £261 contingency)

---

## Contact & Escalation

**Primary**: Peter (you)
**Backup**: Alex (if urgent decisions needed)
**Google Support**: [Include ticket number if opened]

**Dashboard URL**: `/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports/p9-performance-tracker.html`