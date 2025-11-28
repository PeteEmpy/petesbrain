# Smythson Black Friday Phase 1 - Deployment Summary

**Date**: 2025-11-26 08:30 GMT
**Status**: ✅ SUCCESSFULLY DEPLOYED
**Duration**: Tue 26th Nov - Thu 28th Nov (3 days)

---

## Overview

Phase 1 Black Friday budget increases successfully deployed across all 4 Smythson regional accounts. Total of **15 campaigns** updated with new daily budgets.

**Total Daily Budget Increase**: £9,680/day
**3-Day Phase 1 Total**: £29,040

---

## UK Account (8573235780)

**Target**: £5,000/day total
**Campaigns Updated**: 6

| Campaign | Old Budget | New Budget | Increase |
|----------|------------|------------|----------|
| SMY \| UK \| Search \| Brand Exact | £1,200/day | £1,450/day | +£250 |
| SMY \| UK \| P Max \| H&S Christmas Gifting | £510/day | £650/day | +£140 |
| SMY \| UK \| P Max \| H&S | £400/day | £540/day | +£140 |
| SMY \| UK \| P Max \| H&S - Men's Briefcases | £300/day | £420/day | +£120 |
| SMY \| UK \| Shopping \| H&S | £450/day | £650/day | +£200 |
| SMY \| UK \| Search \| Semi Brand - Diaries | £250/day | £350/day | +£100 |

**UK Total Increase**: +£950/day

---

## USA Account (7808690871)

**Target**: £3,000/day total
**Campaigns Updated**: 4

| Campaign | Old Budget | New Budget | Increase |
|----------|------------|------------|----------|
| SMY \| US \| Search \| Brand Exact | £910/day | £1,285/day | +£375 |
| SMY \| USA \| Search \| Brand \| Stationery | £80/day | £135/day | +£55 |
| SMY \| US \| P Max \| H&S Christmas Gifting | £510/day | £680/day | +£170 |
| SMY \| US \| P Max \| H&S | £620/day | £780/day | +£160 |

**USA Total Increase**: +£760/day

---

## EUR Account (7679616761)

**Target**: £1,300/day total
**Campaigns Updated**: 4

| Campaign | Old Budget | New Budget | Increase |
|----------|------------|------------|----------|
| SMY \| EUR \| IT \| Search Brand Ai | £80/day | £100/day | +£20 |
| SMY \| EUR \| ROEuro \| Search \| Brand Ai | £390/day | £480/day | +£90 |
| SMY \| EUR \| DE \| Search \| Brand Ai | £210/day | £270/day | +£60 |
| SMY \| EUR \| FR \| P Max \| Christmas Gifting | £53/day | £70/day | +£17 |

**EUR Total Increase**: +£187/day

---

## ROW Account (5556710725)

**Target**: £380/day total
**Campaigns Updated**: 1

| Campaign | Old Budget | New Budget | Change |
|----------|------------|------------|--------|
| SMY \| ROW \| Search \| Brand Ai | £470/day | £380/day | **-£90** |

**ROW Total Decrease**: -£90/day

*Note: ROW reduced to align with realistic demand expectations while maintaining other ROW campaigns at existing levels.*

---

## Implementation Details

**Method**: Google Ads API v22 (HTTP REST)
**Authentication**: OAuth via MCP server
**Manager Account**: 2569949686
**Deployment Scripts**:
- `phase1-create-budget-jsons.py` - Campaign ID lookup and JSON generation
- `deploy-phase1-budgets.py` - Budget mutation execution

**Deployment Time**: ~2 minutes total across all 4 accounts
**Success Rate**: 100% (15/15 campaigns)

---

## ROAS Baselines (7-day average for monitoring)

- **UK**: 515%
- **USA**: 441%
- **EUR**: 774%
- **ROW**: 340%

**Monitoring Schedule**:
- Hourly checks: 9am, 10am, 11am, 12pm (Tue 26th)
- Daily evening check: 6pm (Tue, Wed, Thu)
- Phase 2 planning: Thu 28th evening based on Tue-Thu performance

---

## Expected Hourly Pacing (£9,680 daily target)

- 9am: ~£807 (8%)
- 10am: ~£1,613 (17%)
- 11am: ~£2,420 (25%)
- 12pm: ~£3,227 (33%)
- 6pm: Target £9,680 (100%)

---

## Next Steps

1. **Monitor hourly pacing** (Tue 9am-12pm) - Task ID: smythson-2025-11-26-bf-004
2. **Evening check Tue 26th** (6pm) - Task ID: smythson-2025-11-26-bf-005
3. **Daily checks Wed/Thu** - Track which campaigns hit budget limits
4. **Phase 2 planning Thu 28th evening** - Determine Friday-Saturday allocation based on Phase 1 performance

**Phase 2 Available Budget**: £28,694 (£14,347/day Fri-Sat)

---

## Files Created

- `/clients/smythson/scripts/phase1-budgets-uk.json`
- `/clients/smythson/scripts/phase1-budgets-usa.json`
- `/clients/smythson/scripts/phase1-budgets-eur.json`
- `/clients/smythson/scripts/phase1-budgets-row.json`
- `/clients/smythson/scripts/phase1-create-budget-jsons.py`
- `/clients/smythson/scripts/deploy-phase1-budgets.py`

---

**Deployment Completed**: 2025-11-26 08:30 GMT
**Next Action**: Hourly monitoring begins 9am
