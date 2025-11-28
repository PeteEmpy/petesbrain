# Label Tracking Rollout - Completion Guide

**Status:** Partially Complete (1 of 8 clients fully rolled out)
**Time Required:** ~30-45 minutes
**Recommended Schedule:** Next week (early in week for testing)

---

## Current Status

### ✅ Completed
- **Tree2mydoor:** 208 products tracked, October 2025 baseline created
- **Label Validation Reports:** Integrated into weekly reporting system
- **Automation Framework:** Hybrid manual/automated approach documented and ready

### ⏸️ In Progress
- **Accessories for the Home (AFH):** 500 products fetched (have labels)
- **Clear Prospects (BMPM):** 500 products fetched (awaiting Product Hero labeling)

### ⏭️ Pending
- **Uno Lights:** MCP query ready, needs execution
- **Grain Guard:** MCP query ready, needs execution (requires manager_id)
- **Crowd Control:** MCP query ready, needs execution
- **HappySnapGifts:** Shares customer_id with BMPM
- **WheatyBags:** Shares customer_id with BMPM

---

## Completion Steps

### Step 1: Execute Remaining MCP Queries (15 minutes)

**Prompt to Claude Code:**
```
Complete the label tracking rollout for all remaining clients. Execute the MCP queries from pending_label_queries.json for:
- Uno Lights
- Grain Guard (with manager_id)
- Crowd Control

Process all responses and create current-labels.json files for all 8 enabled clients.
```

**What Claude Code will do:**
1. Read `pending_label_queries.json`
2. Execute 3-4 remaining MCP queries:
   - Uno Lights: `customer_id=6413338364, custom_label_1, LIMIT 500`
   - Grain Guard: `customer_id=4391940141, manager_id=2569949686, custom_label_0, LIMIT 10000`
   - Crowd Control: `customer_id=9385103842, custom_label_0, LIMIT 10000`
3. Process all MCP responses (including already-fetched AFH and Clear Prospects)
4. Create `current-labels.json` for each client

**Expected Output:**
- 7-8 new `history/label-transitions/{client}/current-labels.json` files
- Summary showing product counts and label distributions per client

---

### Step 2: Generate October Baselines (5 minutes)

**Prompt to Claude Code:**
```
Generate October 2025 baselines for all clients with label tracking enabled.
```

**What Claude Code will do:**
1. Run `python3 create_october_baseline.py`
2. Create `history/label-transitions/{client}/2025-10.json` for each client
3. Display summary stats (product counts, label distributions)

**Expected Output:**
- 7-8 new `history/label-transitions/{client}/2025-10.json` files
- Baseline complete for all enabled clients

---

### Step 3: Test Weekly Report Generation (10 minutes)

**Prompt to Claude Code:**
```
Test the weekly report generation with label validation for one client (Tree2mydoor).
```

**What Claude Code will do:**
1. Run `label_validation_report.py` for Tree2mydoor
2. Generate HTML report showing:
   - Current label distribution
   - Recent transitions (if any from ongoing tracking)
   - Recommendations
3. Save test report to file

**Expected Output:**
- Test HTML report showing label tracking data
- Confirmation that weekly reports will include Product Hero label sections

---

### Step 4: Verify Complete Rollout (5 minutes)

**Prompt to Claude Code:**
```
Verify the complete label tracking rollout. Check that all 8 enabled clients have:
1. current-labels.json
2. 2025-10.json (October baseline)
3. Proper directory structure

Generate a summary report.
```

**What Claude Code will do:**
1. Check `history/label-transitions/` for all 8 clients
2. Verify files exist and have valid data
3. Generate summary table showing:
   - Client name
   - Products tracked
   - Label distribution
   - October baseline status
   - Notes (e.g., "partial coverage" for large accounts)

**Expected Output:**
- Comprehensive rollout status table
- Confirmation that all systems are ready for daily tracking

---

## Post-Completion Actions

### Immediate (Same Day)
1. **Run first daily tracking:** Ask Claude Code to run daily label tracking for all clients
2. **Verify no errors:** Check that all 8 clients process successfully
3. **Review output:** Confirm product counts and distributions look reasonable

### Within 7 Days
1. **Monitor for transitions:** Check if any products change labels
2. **Test weekly reports:** Wait for Monday's automated weekly report to include label data
3. **Validate alerts:** Ensure significant transitions appear in reports

### Ongoing
1. **Daily tracking:** Ask Claude Code to run tracking daily (2-3 minutes)
2. **Weekly review:** Check label validation sections in Monday reports
3. **Monthly review:** Compare label distributions month-over-month

---

## Important Notes

### Label Field Mapping (Reference)
- **Tree2mydoor:** custom_label_3
- **Accessories for the Home:** custom_label_0
- **Uno Lights:** custom_label_1
- **HappySnapGifts:** custom_label_4
- **WheatyBags:** custom_label_4
- **BMPM:** custom_label_4
- **Grain Guard:** custom_label_0 (requires manager_id: 2569949686)
- **Crowd Control:** custom_label_0

### Token Limits & Coverage
- **Large accounts (AFH, Uno Lights):** LIMIT 500 = partial coverage
- **All others:** LIMIT 10000 = full coverage
- This is expected and documented in config.json

### Clear Prospects Multi-Brand
- **Customer ID 6281395727** serves 3 brands:
  - HappySnapGifts
  - WheatyBags
  - BMPM
- Products distinguished by product_id prefix (e.g., "bmpm" for BMPM products)
- **Note:** As of Oct 31, 2025, BMPM products don't have Product Hero labels assigned yet
  - This is normal - Product Hero may not have labeled them yet
  - Labels will appear once Product Hero processes the products
  - Tracking will start capturing labels once they're assigned

### Troubleshooting

**If MCP query fails with token limit:**
- Reduce LIMIT to 500 for that client
- Update config.json with note about partial coverage
- Re-run query

**If no labels appear (all products unlabeled):**
- Check label_field is correct in config.json
- Verify Product Hero has actually assigned labels to products
- For new clients, labels may not exist yet (system will track once assigned)

**If manager_id error (Grain Guard):**
- Ensure manager_id is included in MCP query
- Customer 4391940141 requires manager 2569949686 for API access

---

## Files Reference

### Scripts
- `/tools/product-impact-analyzer/fetch_all_labels.py` - Generate MCP queries
- `/tools/product-impact-analyzer/label_tracking_executor.py` - Process MCP responses
- `/tools/product-impact-analyzer/create_october_baseline.py` - Generate baselines
- `/tools/product-impact-analyzer/label_validation_report.py` - Weekly report integration

### Configuration
- `/tools/product-impact-analyzer/config.json` - Client settings (label fields, limits)
- `/tools/product-impact-analyzer/pending_label_queries.json` - MCP query queue

### Documentation
- `/tools/product-impact-analyzer/AUTOMATION-SOLUTION.md` - Automation approach
- `/tools/product-impact-analyzer/OCTOBER-BASELINE-SUMMARY.md` - Baseline documentation
- `/tools/product-impact-analyzer/ROLLOUT-COMPLETION-GUIDE.md` - This file

### Data Files (Generated)
- `/tools/product-impact-analyzer/history/label-transitions/{client}/current-labels.json`
- `/tools/product-impact-analyzer/history/label-transitions/{client}/2025-10.json`
- `/tools/product-impact-analyzer/history/label-transitions/{client}/YYYY-MM-DD_*.json` (daily snapshots)

---

## Success Criteria

Rollout is complete when:
- ✅ All 8 enabled clients have `current-labels.json`
- ✅ All 8 enabled clients have `2025-10.json` (October baseline)
- ✅ Test weekly report generates successfully with label validation section
- ✅ First daily tracking run completes without errors
- ✅ All product counts and distributions are reasonable (no empty datasets)

**Estimated Total Time:** 30-45 minutes (broken into 4 steps above)

---

**Created:** October 31, 2025
**Last Updated:** October 31, 2025
**Next Review:** After completion (next week)
