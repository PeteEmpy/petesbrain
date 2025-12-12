# Smythson P9: Budget Reallocation Execution Plan
## Dec 12-17 Reallocation Window

---

## Overview

**Objective:** Shift £212/day from underperforming UK campaigns to high-ROAS EUR campaigns

**Timeline:** 6-day window (Dec 12-17), reversible Dec 18
**Status:** Ready for execution upon confirmation

---

## Phase 1: Pre-Execution (Dec 11)

### Step 1: Backup Current State ✅
Query current campaign budgets from Google Ads and document as backup.
- All 12 campaigns (5 UK cuts, 7 EUR increases)
- Save budget amounts and conversion data
- Create verification file for post-execution comparison

### Step 2: User Confirmation (PENDING)
Present backup and plan to user for final approval before proceeding.

---

## Phase 2: Execution (Dec 12, Morning)

### UK Account (Customer ID: 8573235780)

**Campaign Budget Changes:**

| Campaign ID | Campaign Name | Current Budget | New Budget | Change |
|---|---|---|---|---|
| 22845468179 | P Max H&S | £450/day | £250/day | -£200 |
| 13813053110 | Search Brand Stationery | £91/day | £32/day | -£59 |
| 13813052579 | Search Brand Plus | £100/day | £50/day | -£50 |
| 14944953037 | P Max H&S Men's Briefcases | £179/day | £143/day | -£36 |
| 15115980463 | P Max H&S Christmas Gifting | £243/day | £231/day | -£12 |

**Total UK Reduction:** -£357/day

---

### EUR Account (Customer ID: 7679616761)

**Campaign Budget Changes:**

| Campaign ID | Campaign Name | Current Budget | New Budget | Change |
|---|---|---|---|---|
| 23257761115 | DE P Max Diaries | £15/day | £40/day | +£25 |
| 691020848 | DE Search Brand | £44/day | £79/day | +£35 |
| 23248988334 | FR P Max Christmas Gifting | £30/day | £66/day | +£36 |
| 1599767262 | IT Search Brand | £60/day | £110/day | +£50 |
| 23253394509 | P Max Christmas Gifting | £60/day | £90/day | +£30 |
| 22440993281 | ROEuro Search Brand | £130/day | £153/day | +£23 |
| 23257901431 | IT P Max Diaries | £25/day | £50/day | +£25 |

**Total EUR Increase:** +£224/day

---

### Execution Order
1. Update UK campaigns (5 budget changes)
2. Update EUR campaigns (7 budget changes)
3. Each change via `update_campaign_budget` MCP call with new daily amount
4. No campaign pauses—only budget ceiling adjustments

---

## Phase 3: Monitoring (Dec 12-17)

**Daily Checklist:**
- [ ] EUR ROAS tracking (target: 800%+ to validate shift is working)
- [ ] UK ROAS monitoring (expect slight downward pressure from budget reduction)
- [ ] Watch for any anomalies (campaigns hitting new budget ceilings, etc.)

**Decision Point: Dec 15 (Midpoint)**
- If EUR ROAS drops below 700%: Consider early reversal
- If EUR ROAS maintains 800%+: Proceed as planned

---

## Phase 4: Reversal (Dec 18, Morning)

### UK Account: Restore Original Budgets

| Campaign | Restored Budget |
|---|---|
| P Max H&S | £450/day |
| Search Brand Stationery | £91/day |
| Search Brand Plus | £100/day |
| P Max H&S Men's Briefcases | £179/day |
| P Max H&S Christmas Gifting | £243/day |

### EUR Account: Restore Original Budgets

| Campaign | Restored Budget |
|---|---|
| DE P Max Diaries | £15/day |
| DE Search Brand | £44/day |
| FR P Max Christmas Gifting | £30/day |
| IT Search Brand | £60/day |
| P Max Christmas Gifting | £60/day |
| ROEuro Search Brand | £130/day |
| IT P Max Diaries | £25/day |

**Timing:** Dec 18 before 9 AM to allow EUR to wind down while UK prepares for Last Order Week surge

---

## Phase 5: Post-Execution (Dec 19-20)

### Analysis & Documentation
- [ ] Capture final P9 revenue numbers
- [ ] Calculate actual EUR uplift vs projected
- [ ] Document what worked, what didn't
- [ ] Create playbook for Dec 2026

---

## Risk Mitigation

**If EUR ROAS drops significantly:**
- Revert immediately (same-day reversal possible)
- No harm done—all changes are proportional and reversible

**If UK ROAS collapses:**
- Diaries campaigns are protected (minimal cuts)
- Low-ROAS campaigns were over-funded anyway
- UK still has solid Brand Exact funding

**Contingency:**
- Dec 15 decision point allows mid-stream correction
- Full reversal takes 10 minutes max

---

## Success Criteria

✅ All 12 budget changes applied successfully
✅ EUR campaigns receive increased budget allocation by Dec 12, 9 AM
✅ EUR maintains 800%+ ROAS throughout Dec 12-17
✅ All changes reversed Dec 18 morning
✅ P9 finishes above adjusted £1,045k revenue target

---

**Next Step:** Backup current budgets and await user confirmation to proceed.
