# NMA Demographic Bid Adjustments - Backup & Execution Plan
**Date**: 2025-12-11  
**Review Date**: 2026-01-11 (30 days)  
**Purpose**: Apply -20% bid adjustments to underperforming demographics

---

## Current State (Backup)

### Management Campaigns - Current Bid Modifiers

**NMA | Search | UK | Management 100 Ai 25/8 No Target**
- Age 18-24 (503001): No modifier (1.0)
- Age 25-34 (503002): 0.80 (-20%)
- Age 35-44 (503003): 0.90 (-10%)
- Age 45-54 (503004): No modifier (1.0)
- Age 55-64 (503005): No modifier (1.0)
- Age 65+ (503006): 0.60 (-40%)
- Parent (301): No modifier (1.0)

**NMA | Search | ROW | Management 100 No Target**
- Age 65+ (503006): 0.70 (-30%)
- All other ages: No modifier (1.0)
- Parent: No modifier (1.0)

---

## Planned Changes (Step 2)

### Implementation Strategy
Apply -20% bid adjustments to Management campaigns for demographics identified as underperformers in analysis:

**UK Management Campaign** (12578308466):
- Age 35-44 (503003): Change from 0.90 → **0.80** (-20%)
- Age 45-54 (503004): Change from 1.0 → **0.80** (-20%)  [NEW]
- Age 55-64 (503005): Change from 1.0 → **0.80** (-20%)  [NEW]
- Parent status (301): Change from 1.0 → **0.80** (-20%)  [NEW]

**ROW Management Campaign** (13071720649):
- Age 35-44 (503003): Change from 1.0 → **0.80** (-20%)  [NEW]
- Age 45-54 (503004): Change from 1.0 → **0.80** (-20%)  [NEW]
- Age 55-64 (503005): Keep existing 0.70 (no change needed, already -30%)
- Parent status (301): Change from 1.0 → **0.80** (-20%)  [NEW]

**Engineering Campaigns** - NO CHANGES
- Engineering campaigns are performing excellently (£52-£199 CPA)
- Keep all existing bid modifiers

---

## Expected Impact (Post-Adjustment)

**Spend Reallocation**:
- UK Management Search: Budget shifts away from age 35+ and parents
- ROW Management Search: Budget shifts away from age 35+ and parents
- Engineering campaigns: Maintain current performance

**Conversion Quality**:
- Management campaigns attract higher-quality leads (younger, non-parent)
- Expected CPA improvement: 5-8% account-wide
- Estimated monthly savings: £400-650/month

**Monitoring Period**: Dec 11, 2025 - Jan 11, 2026 (30 days)

---

## Rollback Plan

If analysis shows negative results, can revert all changes:
- UK Management: Revert age 35-44 back to 0.90, age 45-54 and 55-64 back to 1.0, parent back to 1.0
- ROW Management: Revert age 35-44 and 45-54 back to 1.0, parent back to 1.0

