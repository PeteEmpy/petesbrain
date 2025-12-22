# Clear Prospects - Last Order Date Decision Tree

**Date**: December 16, 2025 (Tuesday)
**Status**: AWAITING RESPONSE from Michael
**Critical**: This determines Phase 2/3 budget deployment

---

## Email Sent: Christmas Delivery Messaging Questions

**Questions asked**:
1. What's the last order date for guaranteed pre-Christmas delivery?
2. Will website prominently display this date (urgency messaging)?
3. After that date, will messaging switch to post-Christmas delivery warning?

---

## Decision Tree: Response Scenarios

### SCENARIO A: Last Order Date = Monday Dec 15 (ALREADY PASSED) 🚨

**Implications**:
- Currently spending £820/day (Phase 2) on post-Christmas delivery only
- Gift products (HSG/WBS) have 60-80% lower value
- Potential losses: £246-£410/day

**Decision Path**:

#### A1: Website HAS clear post-Christmas messaging
**Action**: Monitor today's ROAS, decide tomorrow (Dec 17)
- If ROAS >120%: Continue Phase 2 (customers self-selecting)
- If ROAS 100-120%: Deploy Phase 2B (£300/day reduced budget)
- If ROAS <100%: Deploy Phase 3 immediately (£50/day shutdown)

**Commands ready**:
```bash
# If ROAS <100% - Deploy Phase 3
cd /Users/administrator/Documents/PetesBrain.nosync/tools/budget-deployer
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase3-shutdown-keep-warm-dec20.csv

# If ROAS 100-120% - Need to create Phase 2B first
# (See "Phase 2B Creation" section below)
```

#### A2: Website LACKS clear messaging
**Action**: Deploy Phase 3 IMMEDIATELY
- Reason: High risk of wasted spend without customer awareness
- Reduce to £50/day shutdown budget now
- Wait for Boxing Day recovery (Phase 4, Dec 26)

**Command**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/budget-deployer
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase3-shutdown-keep-warm-dec20.csv
```

---

### SCENARIO B: Last Order Date = Today (Tuesday Dec 16) or Tomorrow (Wed Dec 17)

**Implications**:
- Currently in last-hours window for Christmas delivery
- Phase 2 budgets (£820/day) are appropriate for remainder of today/tomorrow
- Need to transition to Phase 3 immediately after last order date passes

**Decision Path**:

#### B1: Last order date = Today at 12 noon (6 hours ago)
**Action**: Same as Scenario A (already passed)

#### B2: Last order date = Tomorrow (Wed Dec 17) at 12 noon
**Action**: Continue Phase 2 through tomorrow, deploy Phase 3 on Thursday Dec 18

**Commands**:
```bash
# On Thursday Dec 18 morning:
cd /Users/administrator/Documents/PetesBrain.nosync/tools/budget-deployer
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase3-shutdown-keep-warm-dec20.csv
```

---

### SCENARIO C: Last Order Date = Thursday Dec 18 or Later

**Implications**:
- Phase 2 budgets (£820/day) appropriate through last order date
- Original five-phase strategy timing is correct
- No immediate changes needed

**Decision Path**:

#### C1: Last order date = Thu Dec 18 or Fri Dec 19
**Action**: Continue Phase 2 as planned, deploy Phase 3 on Dec 20

**Timeline**:
- Phase 2: Dec 16-19 (£820/day) ✅ CONTINUE
- Phase 3: Dec 20-25 (£50/day) - Deploy Saturday morning
- Phase 4: Dec 26-Jan 5 (£150/day)
- Phase 5: Jan 6+ (£439/day)

**Command** (Saturday Dec 20):
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/budget-deployer
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase3-shutdown-keep-warm-dec20.csv
```

#### C2: Last order date = Saturday Dec 20 or later
**Action**: REVISE STRATEGY - Phase 3 timing needs adjustment

**Issue**: If last order date is Dec 20, we shouldn't deploy £50/day shutdown on Dec 20 - that's still within Christmas window

**Revised timeline**:
- Phase 2: Dec 16-20 (£820/day) - Extend through last order date
- Phase 3: Dec 21-25 (£50/day) - Start day after last order date
- Phase 4: Dec 26-Jan 5 (£150/day)
- Phase 5: Jan 6+ (£439/day)

**Action required**: Update phase3 CSV start date in deployment plan

---

### SCENARIO D: Website Urgency Messaging Status

#### D1: Website WILL display urgency messaging (e.g., "Order by [date] for Christmas")
**Implications**:
- ✅ Supports maintaining Phase 2 budgets through last order date
- ✅ Urgency drives conversions, justifies £820/day spend
- ✅ Customer expectations managed pre-last-order-date

**Action**: Proceed with current strategy timing based on last order date

#### D2: Website WILL NOT display urgency messaging
**Implications**:
- ⚠️ Missed opportunity for conversion uplift
- ⚠️ Customers may not realise urgency
- ⚠️ Potentially lower ROAS in run-up to last order date

**Action**:
- Suggest Michael adds urgency banner (quick win)
- Monitor ROAS more closely in final days before last order date
- Be prepared to reduce budgets early if ROAS drops

---

## Phase 2B Creation (If Needed)

**When needed**: Scenario A1 with ROAS 100-120% (post-last-order-date, partial value)

**Budget allocation** (£300/day total):
- HSG: £162/day (30% of £540 baseline, proportionally scaled)
- WBS: £138/day (30% of £460 baseline, proportionally scaled)
- BMPM: £0/day (stays paused)

**Creation script**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/budget-deployer

# Create phase2b-post-last-order-dec16.csv
# Copy create_five_phase_deployment.py and modify Phase 3 to create Phase 2B at £300/day
# Then deploy:
python3 deploy-budget-changes.py ../clients/clear-prospects/spreadsheets/phase2b-post-last-order-dec16.csv
```

---

## Monitoring Requirements

### Daily ROAS Checks (While Awaiting Response)

**Check end of day Tuesday Dec 16**:
```bash
# Query today's performance
# Compare to Phase 1 (Dec 15) ROAS to see if post-last-order-date drop is visible
```

**Threshold decisions**:
- ROAS >130%: Phase 2 working well, continue
- ROAS 100-130%: Borderline, monitor closely
- ROAS <100%: Losing money, deploy Phase 3 or Phase 2B

---

## Summary: Response-to-Action Mapping

| Michael's Response | Last Order Date | Website Messaging | Immediate Action |
|-------------------|-----------------|-------------------|------------------|
| **Mon Dec 15** | PASSED | Clear messaging | Monitor today, decide tomorrow |
| **Mon Dec 15** | PASSED | No messaging | Deploy Phase 3 NOW (£50/day) |
| **Wed Dec 17** | 24 hours away | Any | Continue Phase 2, deploy Phase 3 Thu Dec 18 |
| **Thu-Fri Dec 18-19** | 2-3 days away | Any | Continue Phase 2, deploy Phase 3 Sat Dec 20 |
| **Sat Dec 20+** | 4+ days away | Any | REVISE Phase 3 timing, extend Phase 2 |

---

## CSV Files Ready for Deployment

**Currently available**:
- ✅ `phase3-shutdown-keep-warm-dec20.csv` (£50/day) - Ready
- ✅ `phase4-boxing-day-recovery-dec26.csv` (£150/day) - Ready
- ✅ `phase5-january-seasonal-jan6.csv` (£439/day) - Ready

**May need to create**:
- ❓ `phase2b-post-last-order-dec16.csv` (£300/day) - If partial value scenario

---

## Next Steps

1. ✅ Email sent to Michael
2. ⏳ **AWAITING RESPONSE**
3. Based on response, execute decision tree path above
4. Deploy appropriate budget changes
5. Update five-phase summary document with actual timeline

---

**Status**: WAITING FOR MICHAEL'S RESPONSE - Decision tree ready for all scenarios
