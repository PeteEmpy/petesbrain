# Google Ads Scripts - Opportunities for Streamlining

**Analysis Date**: 2025-11-26
**Trigger**: Phase 1 budget deployment took 30+ minutes when it should have taken 4 minutes

---

## The Problem Pattern

Almost every client has **one-off budget update scripts** that:
1. Hardcode campaign IDs and budget IDs
2. Hardcode the exact budget amounts
3. Are single-use and then abandoned
4. Require manual GAQL queries to find IDs first
5. Have different implementations (some use Python client, some use HTTP API, some have version issues)

### Examples Found

```
/clients/devonshire-hotels/scripts/update-budgets-nov-18.py
/clients/devonshire-hotels/scripts/update-budgets-nov-20.py
/clients/devonshire-hotels/scripts/update-budgets-nov-24.py
/clients/devonshire-hotels/scripts/apply-budget-changes-nov-20.py
/clients/devonshire-hotels/scripts/apply-budgets-final.py
/clients/devonshire-hotels/scripts/apply-budgets-now.py
/clients/devonshire-hotels/scripts/apply-budgets-simple.py
```

**7 different budget scripts for one client!** Each one essentially does the same thing with different values.

---

## The Solution

**One universal script** that can handle ANY budget update:
- `/shared/scripts/update-google-ads-budgets.py`

### What It Does Better

| Old Approach | New Approach |
|--------------|--------------|
| Manually query for campaign IDs | Finds campaigns by name automatically |
| Manually query for budget IDs | Finds budget IDs automatically |
| Hardcode IDs in Python script | Simple JSON with just campaign name + budget |
| Create new script each time | Reuse same script forever |
| Fight with API versions | Uses proven HTTP API v22 |
| 30+ minutes setup | 4 minutes total |

---

## Scripts That Could Be Simplified

### 1. **Campaign Budget Updates** ✅ DONE

**Before**: 7+ different scripts per client
**After**: One shared script

**Candidates**:
- All `update-budgets-*.py` files
- All `apply-budgets-*.py` files
- All `budget-increase-*.py` files

**Benefit**: Eliminate 50+ redundant scripts

---

### 2. **Campaign Status Changes** (Pause/Enable)

**Current state**: Ad-hoc scripts like `/clients/devonshire-hotels/scripts/pause-keywords.py`

**Could create**: `/shared/scripts/update-google-ads-campaign-status.py`

```bash
# Pause campaigns
python3 update-google-ads-campaign-status.py \
  --customer-id 8573235780 \
  --campaign "Diaries" \
  --status PAUSED

# Enable campaigns
python3 update-google-ads-campaign-status.py \
  --customer-id 8573235780 \
  --file enable-campaigns.json
```

**JSON format**:
```json
[
  {"campaign": "P Max Diaries", "status": "ENABLED"},
  {"campaign": "Brand Exact", "status": "ENABLED"}
]
```

---

### 3. **Target ROAS Updates**

**Pattern seen**: Scattered scripts updating ROAS targets

**Could create**: `/shared/scripts/update-google-ads-target-roas.py`

```bash
python3 update-google-ads-target-roas.py \
  --customer-id 8573235780 \
  --campaign "P Max H&S" \
  --target-roas 3.0
```

**JSON format**:
```json
[
  {"campaign": "P Max H&S", "target_roas": 3.0},
  {"campaign": "Shopping", "target_roas": 2.5}
]
```

---

### 4. **Ad Copy/Asset Management**

**Current**: Complex asset export/import scripts

**Could simplify**: Asset CRUD operations with name-based lookup

---

### 5. **Performance Queries**

**Current state**: Every analysis script re-implements GAQL queries

**Could create**: `/shared/scripts/google-ads-performance-query.py`

```bash
# Get campaign performance
python3 google-ads-performance-query.py \
  --customer-id 8573235780 \
  --campaigns "Brand Exact,Shopping,P Max" \
  --start-date 2025-11-01 \
  --end-date 2025-11-26 \
  --metrics "cost,conversions,conversions_value" \
  --output csv
```

**Benefits**:
- Standard output format (CSV/JSON)
- Consistent metric calculations
- Reusable across all clients

---

## Implementation Priority

### High Priority (Do These)

1. ✅ **Campaign Budget Updates** - DONE
2. **Campaign Status Changes** (Pause/Enable) - NEXT
3. **Target ROAS Updates** - Common operation
4. **Performance Query Template** - Used constantly

### Medium Priority

5. **Geo Target Updates** - Less frequent but painful when needed
6. **Bid Strategy Changes** - Occasional but complex
7. **Negative Keyword Bulk Add** - Common for audits

### Low Priority

8. **Asset Management** - Complex, less frequent
9. **Ad Group Operations** - Rare manual changes
10. **Budget Pacing Calculations** - Analysis-focused

---

## Common Pattern to Follow

All shared scripts should:

1. **Accept campaign names (not IDs)**
   - Use partial matching
   - Find IDs automatically

2. **Support both CLI and JSON file input**
   ```bash
   # Single item CLI
   --campaign "Name" --value X

   # Batch JSON
   --file changes.json
   ```

3. **Use HTTP API v22 (most reliable)**
   - Via MCP server OAuth
   - Include manager account header

4. **Show before/after values**
   - Current value → New value
   - Clear confirmation of what changed

5. **Have simple JSON format**
   ```json
   [
     {"campaign": "partial name", "new_value": 123}
   ]
   ```

6. **Be in `/shared/scripts/`**
   - Not client-specific
   - Work for any account

---

## Scripts to Delete (After Migration)

Once new shared scripts are created and tested, these can be cleaned up:

```
/clients/*/scripts/update-budgets-*.py
/clients/*/scripts/apply-budgets-*.py
/clients/*/scripts/budget-increase-*.py
/clients/*/scripts/pause-*.py
/clients/*/scripts/enable-*.py
/clients/*/scripts/*-roas-*.py
```

**Estimated cleanup**: 60+ redundant scripts removed

---

## Testing Strategy

For each new shared script:

1. Test with Devonshire (simple single account)
2. Test with Smythson (multi-account scenario)
3. Test batch operations (JSON file with 5+ campaigns)
4. Document in `/docs/HOW-TO-*.md`

---

## Long-term Vision

**Ultimate goal**: No client should ever have a custom Google Ads mutation script.

All changes should be:
- Via shared scripts (for programmatic)
- Via Google Ads UI (for manual)
- Via MCP tools (if we build proper ones - currently don't exist)

**Exception**: Analysis/reporting scripts are fine to be client-specific (they're reading data, not mutating).

---

## Immediate Next Steps

1. ✅ Budget updates - DONE
2. Create `/shared/scripts/update-google-ads-campaign-status.py`
3. Create `/shared/scripts/update-google-ads-target-roas.py`
4. Update `/docs/HOW-TO-UPDATE-GOOGLE-ADS-BUDGETS.md` with new scripts
5. Test with next Smythson Phase 2 deployment (Friday)

---

**Bottom Line**: We've been reinventing the wheel 60+ times. Time to have ONE wheel that works perfectly.
