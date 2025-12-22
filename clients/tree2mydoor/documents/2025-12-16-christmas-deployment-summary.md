# Tree2mydoor Christmas Deployment Summary

**Date:** 16th December 2025
**Meeting:** Ryan (Collaber) + Peter

---

## ✅ Tasks Completed

### 1. 5L vs 3L Rose Bush Experiment - BASELINE DOCUMENTED

**Status:** ✓ Complete
**File:** `clients/tree2mydoor/experiments/2025-12-16-at-peace-rose-bush-5l-vs-3l-pot-test.md`
**5L Product ID:** **APRBG5W** ✓ Confirmed

**What's Done:**
- Launch date marker created (16 Dec 2025)
- Baseline performance captured (last 30 days)
- Analysis methodology documented
- Review dates scheduled (30-day, 90-day)
- 5L SKU confirmed: APRBG5W

**Next Steps:**
- 5L variant (APRBG5W) live in product feed
- First review: 15 Jan 2026 (30 days)
- Full analysis: 16 Mar 2026 (90 days)

---

### 2. Christmas Budget Deployment - APPROVED & READY

**Status:** ✓ Approved, ready to execute Monday 22 Dec at 9am
**CSV:** `clients/tree2mydoor/spreadsheets/christmas-shutdown-budget-dec22-jan5-NO-PAUSE.csv`
**Backup:** `clients/tree2mydoor/reports/budget-deployment-backup-2025-12-16_172958.json`

**Budget Summary:**

| Metric | Value |
|--------|-------|
| Current daily budget | £660/day |
| Shutdown budget | £112/day |
| Reduction | £548/day (83%) |
| Last year's actual | £89.67/day |
| Headroom vs last year | +25% |

**Key Decisions:**
- ✅ **NO campaigns paused** (all 9 campaigns remain active)
- ✅ **Data-driven budgets** (based on last year's Christmas shutdown performance)
- ✅ **"Unprofitable" campaign kept active** - had 181% ROAS last year during shutdown
- ✅ **Room for Boxing Day** - last year hit 200%+ ROAS on several days

**Campaign Budgets:**

| Campaign | Current | Shutdown | Change |
|----------|---------|----------|--------|
| PMax HP&P | £175 | £40 | -£135 |
| Shopping Catch All | £200 | £20 | -£180 |
| Search Trees | £69 | £10 | -£59 |
| Search Roses | £63 | £10 | -£53 |
| DSA | £68 | £5 | -£63 |
| **PMax Shopping Unprofitable** | £15 | **£10** | -£5 |
| **Shopping Low Traffic** | £10 | **£5** | -£5 |
| Brand Inclusion | £50 | £10 | -£40 |
| Memorial Gift | £10 | £2 | -£8 |

---

## 📊 Last Year's Christmas Performance (22 Dec 2024 - 5 Jan 2025)

**Total Period:**
- Spend: £2,040.04
- Revenue: £4,514.02
- ROAS: 221%
- Conversions: 183.3

**Christmas Shutdown (24-31 Dec 2024):**
- Daily spend: £89.67/day average
- ROAS: 156% average
- Best days: 27-29 Dec (200%+ ROAS)
- Worst day: 25 Dec (48% ROAS)

**New Year Recovery (1-5 Jan 2025):**
- Daily spend: £229.33/day average
- ROAS: 232% average
- Strong restart performance

---

## 🚀 Deployment Instructions

### Monday 22nd December 2025 at 9am

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/budget-deployer

python3 deploy.py \
  --client tree2mydoor \
  --csv ../../clients/tree2mydoor/spreadsheets/christmas-shutdown-budget-dec22-jan5-NO-PAUSE.csv \
  --execute
```

**Why 9am Monday:**
- Last order date: Monday 22nd Dec at 11am
- Budget changes take effect Tuesday 23rd morning
- Minimises spend during dead period (23 Dec - 4 Jan)

### Monday 5th January 2026

**Restore budgets to normal levels:**
- Team returns Monday 5th January
- Review last year's January performance (task created)
- Wind budgets back up gradually

---

## 📝 Related Tasks

| Task | Priority | Due Date | Status |
|------|----------|----------|--------|
| Drop Christmas campaign budgets | P0 | 22 Dec 2025 | Ready to deploy |
| 5L vs 3L rose bush experiment | P1 | 23 Dec 2025 | Baseline documented |
| Follow up meeting with Ryan | P1 | 23 Dec 2025 | Pending |
| Review Jan restart timing | P2 | 5 Jan 2026 | Pending |

---

## 🎯 Success Criteria

**Budget Deployment:**
- ✅ Budgets deployed before last order cutoff (11am Monday)
- ✅ Spend reduced by ~80% during shutdown
- ✅ ROAS remains positive (>100%)
- ✅ No campaigns accidentally paused

**5L Rose Bush Experiment:**
- TBC - Define success metrics once SKU confirmed
- TBC - Revenue split target between 3L and 5L
- TBC - Minimum ROAS threshold for 5L variant

---

**Created:** 16th December 2025
**Last Updated:** 16th December 2025
**Next Action:** Deploy budgets Monday 22 Dec at 9am
