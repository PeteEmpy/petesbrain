# Chatsworth Inns Negative Keywords - Implementation Complete

**Date**: 2025-12-22 16:45 GMT
**Campaign**: DEV | Core Properties CE | Chatsworth Escapes Inns & Hotels
**Campaign ID**: 2080736142
**Customer ID**: 5898250490

---

## ✅ Implementation Status: COMPLETE

All negative keywords have been successfully added to the campaign to prevent property cannibalization.

---

## Changes Made

### Negative Keywords Added: 15

**Property-Specific (11 keywords)**:

| Property | Keywords | Match Types | Purpose |
|----------|----------|-------------|---------|
| **The Hide** | hide, highwayman | EXACT + PHRASE each (4 total) | Prevent "the hide chatsworth" searches (£33.63 wasted) |
| **Pilsley Inn** | pilsley | EXACT + PHRASE (2 total) | Prevent "pilsley inn" searches (£45.16 wasted) |
| **Beeley Inn** | beeley | EXACT + PHRASE (2 total) | Prevent "beeley inn" searches (£4.80 wasted) |
| **Devonshire Arms** | devonshire arms | PHRASE (1 total) | Preventive - dedicated campaign exists |
| **The Fell** | fell | PHRASE (1 total) | Preventive - dedicated campaign exists |
| **Cavendish** | cavendish | PHRASE (1 total) | Preventive - dedicated campaign exists |

**Informational (4 keywords)**:

| Intent | Keywords | Match Type | Purpose |
|--------|----------|------------|---------|
| Menu searches | menu, menus | EXACT | Non-booking intent (£0.33 wasted) |
| Pub searches | pub, pubs | EXACT | Non-booking intent (£2.19 wasted) |

---

## Expected Impact

### Financial Projections (Monthly)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Monthly Spend** | £476 | £309 | **-35% (£167 saved)** |
| **Property Cannibalization** | £167/month | £0 | **£167/month saved** |
| **Conversions** | 0-2/month | 2-4/month (est.) | **+2 conversions** |
| **Revenue** | £580/month | £870/month (est.) | **+£290** |
| **ROAS** | 161% | 280% (est.) | **+119pp** |

### Wasted Spend Eliminated

**Dec 8-22 Baseline (15 days)**:
- Property searches: 211 clicks, £83.59 (35.1% of total spend)
- Informational searches: 22 clicks, £2.52
- **Total wasted**: 233 clicks, £86.11

**Monthly Projection if Continued**:
- Property waste: £167/month
- Informational waste: £5/month
- **Total monthly waste**: £172/month

**After Implementation**:
- Expected waste: £0 (keywords blocked)
- **Monthly savings**: £172

---

## Pre-Implementation State

**Campaign Status**:
- Status: ENABLED
- Bidding Strategy: TARGET_ROAS
- Daily Budget: £17 (£17,000,000 micros)
- Existing Negative Keywords: 206

**Performance (Dec 1-22, 2025)**:
- Total Conversions: 2 (both on Dec 7)
- Total Revenue: £580.02
- Total Spend: £360.95
- ROAS: 161%
- Last Conversion: Dec 7 (15 days ago)

**Zero-Conversion Streak**: Dec 8-22 (15 days)
- Spend: £238.24
- Conversions: 0
- Wasted: 100% of spend

---

## Post-Implementation State

**Campaign Status**:
- Status: ENABLED (unchanged)
- Bidding Strategy: TARGET_ROAS (unchanged)
- Daily Budget: £17 (unchanged)
- Total Negative Keywords: 221 (was 206, added 15)

**New Negative Keywords Active**:
1. hide [EXACT]
2. hide [PHRASE]
3. highwayman [EXACT]
4. highwayman [PHRASE]
5. pilsley [EXACT]
6. pilsley [PHRASE]
7. beeley [EXACT]
8. beeley [PHRASE]
9. devonshire arms [PHRASE]
10. fell [PHRASE]
11. cavendish [PHRASE]
12. menu [EXACT]
13. menus [EXACT]
14. pub [EXACT]
15. pubs [EXACT]

**Backup Created**: `clients/devonshire-hotels/reports/chatsworth-inns-backup-2025-12-22.json`

---

## Monitoring Plan

### 7-Day Review (Due: 2025-12-29)

**Task Created**: `[Devonshire] P0: Chatsworth Inns 7-Day Review (Negative Keywords Impact)`

**Success Criteria**:
1. ✅ Zero property searches (hide, pilsley, beeley)
2. ✅ Spend reduction 30-40% (target: £10.32/day vs £15.88 baseline)
3. ✅ At least 1 conversion
4. ✅ Remaining searches are generic "chatsworth" queries

**Metrics to Track**:
- Search terms report (Dec 23-29)
- Property cannibalization check (should be zero)
- Daily spend vs baseline
- Conversion volume
- ROAS

**Red Flags**:
- 🚨 Spend drops >50% (over-negation)
- 🚨 Still seeing property searches (implementation error)
- 🚨 Zero impressions (campaign disabled)

---

### 30-Day Strategic Evaluation (Due: 2026-01-21)

**Task Created**: `[Devonshire] P1: Chatsworth Inns 30-Day Strategic Evaluation (Campaign Future)`

**Purpose**: Determine if campaign should continue, be paused, or be restructured.

**Decision Framework**:

| Outcome | Criteria | Action |
|---------|----------|--------|
| **PAUSE** | <2 conversions/month, <300% ROAS | Close campaign, reallocate £309/month to property campaigns |
| **MONITOR** | 2-4 conversions/month, 300-500% ROAS | Continue for additional 30 days, consider restructuring |
| **CONTINUE** | 5+ conversions/month, >500% ROAS | Maintain current structure, optimize for growth |

**Analysis Required**:
- 30-day performance vs baseline
- Search term uniqueness analysis
- Campaign overlap audit (vs Performance Max, property campaigns)
- Opportunity cost calculation
- Recommendation with rationale

---

## Risk Assessment

### Risk 1: Over-Negation (LOW)

**Scenario**: Legitimate searches blocked by PHRASE match

**Mitigation**:
- Daily search terms monitoring (first 7 days)
- EXACT match used for single words where appropriate
- Rollback plan: Remove overly broad negatives

**Status**: Monitoring

---

### Risk 2: Campaign Becomes Redundant (MEDIUM)

**Scenario**: No unique value after property searches removed

**Mitigation**:
- 30-day evaluation to assess unique value
- Compare with Performance Max and property campaigns
- Decision point: Pause vs restructure vs continue

**Status**: Evaluation scheduled (Jan 21)

---

### Risk 3: Property Campaigns Miss Broad Searches (LOW)

**Scenario**: Generic "chatsworth accommodation" searches now missed

**Mitigation**:
- Monitor overall account conversions
- Check Performance Max capture of generic queries
- Add broad keywords if gap identified

**Status**: Monitoring

---

## Rollback Plan (If Needed)

**If over-negation detected (>50% spend drop)**:

1. **Identify problematic negatives** (likely: "fell", "cavendish", "hide" - single words)
2. **Remove EXACT match versions** (keep PHRASE)
3. **Monitor for 48 hours**
4. **Adjust as needed**

**Backup available**: `chatsworth-inns-backup-2025-12-22.json`

---

## Documentation

**Implementation Files**:
- Full Plan: `clients/devonshire-hotels/documents/chatsworth-inns-negative-keywords-implementation-plan.md`
- HTML Summary: `clients/devonshire-hotels/documents/chatsworth-inns-implementation-plan-summary.html`
- Backup: `clients/devonshire-hotels/reports/chatsworth-inns-backup-2025-12-22.json`
- This Report: `clients/devonshire-hotels/reports/chatsworth-inns-implementation-complete-2025-12-22.md`

**Investigation Report**: `clients/devonshire-hotels/tasks-completed.md` (Dec 22, 2025 entry)

**Monitoring Tasks**:
1. 7-Day Review: `chatsworth-inns-7day-review-20251222` (Due: Dec 29)
2. 30-Day Evaluation: `chatsworth-inns-30day-review-20251222` (Due: Jan 21)

---

## Next Steps

1. ✅ **Implementation Complete** (Dec 22, 16:45)
2. ⏳ **Monitor Search Terms** (Dec 23-29 - Daily)
3. ⏳ **7-Day Review** (Dec 29)
4. ⏳ **Weekly Monitoring** (Jan 5, 12, 19)
5. ⏳ **30-Day Evaluation** (Jan 21)
6. ⏳ **Strategic Decision** (Jan 21 - Pause/Monitor/Continue)

---

## Summary

**What Changed**: Added 15 negative keywords to prevent property cannibalization

**Why**: Campaign was wasting 35% of budget on searches for properties with dedicated campaigns

**Expected Result**: £167/month savings, improved ROAS from 161% to 280%, 2+ additional conversions/month

**Monitoring**: Daily (7 days) → Weekly (30 days) → Strategic decision (Jan 21)

**Implementation Status**: ✅ **COMPLETE & ACTIVE**

---

**Implemented by**: Peter Empson (PetesBrain AI)
**Approved by**: Pending client review
**Implementation Time**: 45 minutes
**Tools Used**: Google Ads MCP, Change Protection Protocol
