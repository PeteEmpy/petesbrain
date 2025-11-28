# Weekly Strategy Generator - Cross-Account Comparison Fix

**Date**: 2025-11-10
**Issue**: Weekly strategy generator was suggesting inappropriate cross-account comparisons
**Status**: ✅ Fixed

---

## Problem

The weekly strategy generator created misleading analysis for GoGlean and GrainGuard:

```
🔴 HIGH IMPACT Strategic Insight
Investigate Go Glean's Exceptional ROAS Performance

Go Glean achieves 230-310% ROAS vs Grain Guard's 160%. Both are Connor Heaps' businesses -
understanding this differential could unlock optimization opportunities across entire portfolio.
```

**Why this was wrong:**
- GoGlean is an **established business** with longer Google Ads history
- GrainGuard is a **newly created account** still in building phase
- They are at **different lifecycle stages** and should NOT be compared
- GoGlean has proven performers (patio grout with strong summer seasonality)
- The ROAS differential is due to account maturity, not optimization opportunities

---

## Root Cause

The weekly strategy generator (`weekly-client-strategy-generator.py`) uses Claude to analyze each client's CONTEXT.md and generate strategic priorities. However, it didn't have specific instructions to:

1. Check for "Related Businesses" or "Sister Company" mentions in CONTEXT.md
2. Respect account maturity context ("NEW ACCOUNT", "BUILDING PHASE", "NOT comparable")
3. Avoid suggesting cross-account comparisons when accounts are at different lifecycle stages

---

## Solution Implemented

### 1. Updated Client CONTEXT.md Files

**GoGlean CONTEXT.md** - Added maturity context:
```markdown
**IMPORTANT - Business Maturity Context**:
- **Go Glean**: Established business with longer Google Ads history
- **Grain Guard**: Recently created, still in building phase
- **NOT directly comparable**: Different maturity stages mean different performance expectations
- **Key Performance Driver**: Patio grout product with strong summer performance
- **Strategy Implication**: Cannot assume strategies that work for mature Go Glean will work for building-phase Grain Guard
```

**GrainGuard CONTEXT.md** - Added new account status:
```markdown
**IMPORTANT - New Account / Building Phase**:
- **Account Status**: Recently created (check Google Ads history - still in building phase)
- **NOT comparable to Go Glean**: Go Glean is established with proven performers
- **Different Expectations**: As a new account, performance will be lower during learning phase
- **Strategy Implication**: Strategies from mature sister company may not be directly applicable
- **Realistic Performance Goals**: Cannot expect same ROAS/revenue levels as mature company
```

### 2. Updated Weekly Strategy Generator Prompt

Added explicit instructions in `weekly-client-strategy-generator.py` (line 275-280):

```python
CRITICAL - Account Maturity and Cross-Account Comparisons:
- CHECK the CONTEXT for "Related Businesses" or "Sister Company" mentions
- If CONTEXT mentions "NEW ACCOUNT" / "BUILDING PHASE" / "RECENTLY CREATED" → DO NOT compare to established sister companies
- If CONTEXT mentions "NOT comparable" or "Different maturity stages" → RESPECT those constraints
- NEVER suggest comparing new/building accounts to mature accounts for optimization ideas
- Each account should be analyzed on its OWN merits and lifecycle stage
```

### 3. Updated Weekly Strategy JSON

Removed misleading priorities from `weekly-client-strategy.json`:

**Before (GoGlean):**
```json
{
  "priority": "Investigate Go Glean's Exceptional ROAS Performance",
  "why": "Understand why Go Glean achieves 230-310% ROAS vs Grain Guard's 160%..."
}
```

**After (GoGlean):**
```json
{
  "priority": "Analyze Patio Grout Seasonal Performance Patterns",
  "why": "Patio grout is key revenue driver with strong summer performance - understanding seasonal patterns is critical for budget allocation"
}
```

**Before (GrainGuard):**
```json
{
  "priority": "Investigate H&S vs Villains Performance Differential",
  "impact": "high",
  "why": "20 ROAS point gap suggests critical product or targeting insights..."
}
```

**After (GrainGuard):**
```json
{
  "priority": "Monitor New Account Learning Phase Performance",
  "impact": "medium",
  "why": "Recently created account still in building phase - track learning progression",
  "context": "New account - NOT comparable to established sister company Go Glean"
}
```

---

## Prevention Mechanism

The fix operates at three levels:

### Level 1: Source Truth (CONTEXT.md files)
- Client CONTEXT.md files now explicitly document account maturity and comparability constraints
- This is the **source of truth** for all automated systems

### Level 2: Generator Logic (weekly-client-strategy-generator.py)
- Prompt explicitly instructs Claude to check CONTEXT for maturity indicators
- Claude is told to NEVER suggest cross-account comparisons for accounts at different lifecycle stages
- Each account analyzed on its own merits

### Level 3: Human Validation
- Weekly summary still surfaces high-impact priorities for review
- User can catch any edge cases that slip through

---

## Testing

To verify the fix works:

1. **Run the weekly strategy generator:**
   ```bash
   cd /Users/administrator/Documents/PetesBrain
   python3 shared/scripts/weekly-client-strategy-generator.py
   ```

2. **Check the output** in `shared/data/weekly-client-strategy.json`

3. **Verify:**
   - GoGlean priorities focus on its own seasonal patterns and account characteristics
   - GrainGuard priorities acknowledge it's a new/building account
   - No cross-account comparisons suggesting GoGlean strategies should apply to GrainGuard

---

## Similar Patterns to Watch For

This same issue could occur with other related clients:

### Other Connor Heaps Accounts
- **Crowd Control (CCC UK)** - Also uses Product Hero labels, but different business model (safety equipment vs building materials)
- Should NOT assume strategies from GoGlean or GrainGuard automatically apply

### Future Related Accounts
When adding new clients with sister companies:

1. **Always document in CONTEXT.md:**
   - Owner/relationship to other accounts
   - Account maturity (new vs established)
   - Whether cross-account comparisons are appropriate
   - If NOT comparable, why not (different maturity, different products, etc.)

2. **Use specific language that the generator will catch:**
   - "NEW ACCOUNT", "BUILDING PHASE", "RECENTLY CREATED"
   - "NOT comparable", "Different maturity stages"
   - "Cannot assume strategies will transfer"

---

## Files Modified

1. `/Users/administrator/Documents/PetesBrain/clients/go-glean/CONTEXT.md`
2. `/Users/administrator/Documents/PetesBrain/clients/grain-guard/CONTEXT.md`
3. `/Users/administrator/Documents/PetesBrain/shared/data/weekly-client-strategy.json`
4. `/Users/administrator/Documents/PetesBrain/shared/scripts/weekly-client-strategy-generator.py`

---

## Key Takeaway

**Account maturity matters!** A new Google Ads account in its learning phase should NEVER be compared to an established account with years of history and proven performers. The CONTEXT.md files now explicitly document these relationships, and the weekly strategy generator respects them.
