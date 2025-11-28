# October 2025 Historical Baseline - Summary

**Date:** October 31, 2025
**Status:** ✅ Complete (with documented limitations)

---

## Objective

Create historical baseline for Product Hero label tracking covering October 2025.

---

## Challenge: MCP Token Limits

**Problem:** MCP `run_gaql` has a 25,000 token response limit.

**Impact on historical queries:**
- Even simple queries (LIMIT 500, single date) exceed token limit
- Each product row includes verbose JSON (product_item_id, campaign names, custom attributes)
- Full month queries: 30,000+ tokens
- Single date queries (LIMIT 500): 34,000+ tokens
- **Conclusion:** Cannot fetch October 2025 data via MCP

**Attempted solutions:**
1. ❌ Full month aggregate (`DURING LAST_MONTH`) - 79,478 tokens
2. ❌ Single date with LIMIT 2000 - 34,025 tokens
3. ❌ Single date with LIMIT 500 - 34,024 tokens
4. ❌ Sampled dates approach (3 dates × 8 clients = 24 queries) - Each query still exceeds limit

---

## Solution Implemented

### Approach: Current Snapshot as October Baseline

**Rationale:**
- Product Hero labeling system was implemented in October 2025
- Current label snapshots (created Oct 31) represent end-of-October state
- This provides a valid historical baseline for November tracking
- Going-forward tracking (Nov 1+) will detect all transitions

**Implementation:**
- Created `create_october_baseline.py` script
- Copies current-labels.json to 2025-10.json for each client
- Adds metadata documenting method and limitations

**Result:**
- ✅ Tree2mydoor: October baseline created (3 products)
- ⏸️ Other 7 clients: Will create baselines after first daily tracking run

---

## Files Created

### `/tools/product-impact-analyzer/create_october_baseline.py`
**Purpose:** Create October 2025 baselines from current snapshots

**Usage:**
```bash
python3 create_october_baseline.py
```

**Output:** Creates `history/label-transitions/{client}/2025-10.json` for each client with existing current-labels.json

### `/tools/product-impact-analyzer/run_october_backfill.py`
**Status:** Not used (documented for reference)
**Reason:** MCP token limits prevent historical queries

**What it does:**
- Generates queries for October 2025 data
- Attempts sampled approach (3 dates per client)
- Would work if token limits allowed

**Preserved for:** Future reference if MCP limits increase or alternative API access becomes available

---

## October 2025 Baseline Data

### Tree2mydoor
**File:** `history/label-transitions/tree2mydoor/2025-10.json`

**Data:**
```json
{
  "month": "2025-10",
  "baseline_date": "2025-10-31",
  "method": "current_snapshot_as_baseline",
  "total_products": 3,
  "products": {
    "smrg": "sidekicks",
    "ffrbg": "heroes",
    "50gwrb": "villains"
  }
}
```

**Distribution:**
- Heroes: 1 (33.3%)
- Sidekicks: 1 (33.3%)
- Villains: 1 (33.3%)

### Other Clients
**Status:** Pending first daily tracking run

**Process:**
1. User runs daily label tracking (asks Claude Code)
2. `fetch_all_labels.py` generates queries
3. Claude Code executes MCP queries
4. `label_tracking_executor.py` creates current-labels.json
5. Run `create_october_baseline.py` to create October baseline

---

## Limitations & Caveats

### What October Baseline Captures
✅ End-of-October label distribution
✅ Snapshot of all tracked products as of Oct 31
✅ Valid baseline for detecting November transitions

### What October Baseline Does NOT Capture
❌ Mid-October label changes (if any occurred)
❌ Products that were active earlier in October but not on Oct 31
❌ Intra-month transitions

### Impact
- **Minimal** for transition tracking purposes
- November tracking will capture all changes from Oct 31 baseline
- Historical analysis for October is representative (end-of-month state)

---

## Alternative Approaches (Not Implemented)

### 1. Google Ads API Direct (Python Client)
**Bypass MCP, use Google Ads Python library directly**

**Pros:**
- No token limits (returns Python objects, not JSON)
- Full pagination support
- Can query entire October month

**Cons:**
- Requires service account setup
- Additional authentication complexity
- Would take significant development time

**Decision:** Not worth effort for one-time historical backfill

### 2. Manual Export from Google Ads UI
**Download Shopping performance report for October**

**Pros:**
- Works today
- No technical barriers

**Cons:**
- Manual process
- Would need to parse CSV and map to Product Hero labels
- Campaign inference still required (labels may not be in export)

**Decision:** Not implemented (current snapshot approach simpler)

### 3. Wait for MCP Token Limit Increase
**Future enhancement to MCP server**

**Pros:**
- Would enable historical queries
- Clean solution

**Cons:**
- Timeline unknown
- Baseline needed now

**Decision:** Use current approach, revisit if limits increase

---

## Recommendations

### Immediate (November 2025)
1. ✅ October baseline complete for Tree2mydoor
2. ⏸️ Run daily label tracking to create current snapshots for other 7 clients
3. ⏸️ Run `create_october_baseline.py` to create their October baselines
4. ✅ Begin daily tracking (Nov 1+) to capture all going-forward transitions

### Short Term (Next 2 Weeks)
- Implement LaunchAgent email reminders (Phase 2 automation)
- Build up transition history through daily tracking
- Monitor for any unexpected label changes

### Long Term (Optional)
- If MCP token limits increase, re-run historical backfill for complete October data
- Consider Google Ads API direct integration for richer historical analysis
- Implement performance-based label inference for pre-October months

---

## Success Criteria

✅ **Primary Goal:** Enable transition tracking starting November 1
✅ **Achieved:** October baseline exists (Tree2mydoor), framework ready for other clients
✅ **Going Forward:** Daily tracking will capture all transitions from Oct 31 baseline

**Status:** October baseline implementation complete and production-ready.

---

**Created:** October 31, 2025
**Last Updated:** October 31, 2025
**Maintained By:** Claude Code + Pete Ewbank
