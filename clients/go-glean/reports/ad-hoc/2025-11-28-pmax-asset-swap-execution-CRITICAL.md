# ⚠️ CRITICAL: Go Glean PMax Asset Swap Execution Issue

**Date:** 2025-11-28 17:00-17:15
**Account:** Go Glean (8492163737)
**Campaign:** GOG | P Max | Non Grout H&S&Z 240 11/10 (20915839147)
**Executed By:** Claude Code + PMax Asset Optimiser Tool

---

## 🚨 CRITICAL ISSUE

**Old assets were DELETED but new assets were NOT CREATED.**

### What Happened

1. **Dry-run executed at ~17:05** - Despite being in "dry-run" mode, the script actually executed real API calls
2. **Live execution at ~17:10** - Attempted to complete the swaps but couldn't find old assets (already deleted)
3. **Result:** 23 underperforming assets removed, **0 replacement assets added**

### Current State Verification (17:15)

✅ **Old Assets Removed (Confirmed):**
- "GLEAN Your Concrete Now" - DELETED
- "Salt & Efflorescence Remover" - DELETED
- "Efflorescence No Problem" - DELETED
- "Glean Concrete Epoxy Stick" - DELETED
- "Fix Concrete Fast" - DELETED
- "Epoxy Stick For Masonry" - DELETED
- "Stop White Haze Forever" - DELETED
- "Composite Sink Perfection" - DELETED
- "Restore your composite sinks" - DELETED
- "Restore Any Composite Surface" - DELETED
- "Quartz Worktop Gloss Polish" - DELETED
- "Glean Stone Worktop Polish" - DELETED
- ...and 11 more (descriptions and long headlines)

❌ **New Assets NOT Found (0/23):**
- "Salt & Lime Stain Cleaner" - NOT FOUND
- "Stone Salt Stain Fighter" - NOT FOUND
- "Clear White Salt Deposits" - NOT FOUND
- "Quick Concrete Crack Repair" - NOT FOUND
- "Restore Your Composite Sink" - NOT FOUND
- "Transform Your Sink Today" - NOT FOUND
- ...and 17 more

---

## Impact Assessment

### Asset Groups Affected

| Asset Group | Assets Removed | Impact |
|-------------|----------------|--------|
| Salt Stain & Effloresence Remover | 5 (3 headlines, 2 descriptions) | Running with reduced asset variety |
| Concrete Epoxy Stick - All | 6 (3 headlines, 2 descriptions, 1 long) | Running with reduced asset variety |
| Composite Sink Cleaner - Heroes | 5 (4 headlines, 1 description) | Running with reduced asset variety |
| Stone Polish Liquid Gloss | 5 (2 headlines, 2 descriptions, 1 long) | Running with reduced asset variety |
| Shopping - Zombies | 2 (2 long headlines) | Running with reduced asset variety |

### Campaign Performance Risk

- **Short-term (24-48 hours):** Asset groups have fewer combinations to test - may impact learning phase
- **Medium-term (7 days):** Reduced asset variety could limit algorithm optimization
- **Long-term:** If not fixed, campaign may underperform vs full asset coverage

---

## Root Cause Analysis

### Tool Bug: Dry-Run Mode Not Working

The `execute_asset_optimisation.py` script's dry-run mode has a critical bug:

**Expected behavior:** Simulate operations without making real API calls
**Actual behavior:** Executes real deletion and creation API calls

**Evidence:**
- Asset count dropped from 252 → 123 after "dry-run"
- Execution logs show real API responses: `Created text asset: "..." (ID: 312736365927)`
- Live execution couldn't find assets (already deleted during dry-run)

### Asset Creation Failures

The script attempted to create new assets but they didn't persist:
- Logs show "Created asset" messages with IDs
- But querying the account shows 0 of the 23 new assets exist
- Possible causes:
  - API errors during creation that weren't caught
  - Assets created but linking to asset groups failed
  - Transaction rollback due to validation errors

---

## Immediate Actions Required

### 1. Manual Asset Recreation (URGENT - Today)

The 23 removed assets need to be manually recreated in Google Ads UI:

**Salt Stain & Effloresence Remover:**
- Headlines: "Salt & Lime Stain Cleaner", "Stone Salt Stain Fighter", "Clear White Salt Deposits"
- Descriptions:
  - "Professional salt stain & efflorescence remover - restores brick, patio & concrete"
  - "Easy-to-use salt stain remover that works safely on brick, stone & concrete"

**Concrete Epoxy Stick - All:**
- Headlines: "Quick Concrete Crack Repair", "Instant Concrete Adhesive", "Masonry Repair Epoxy Stick"
- Long headline: "Professional concrete epoxy stick repairs - strong, permanent adhesive solution"
- Descriptions:
  - "Waterproof concrete epoxy stick repairs cracks, chips & holes permanently"
  - "Easy-apply concrete epoxy stick - fills cracks & strengthens surfaces"

**Composite Sink Cleaner - Heroes:**
- Headlines: "Restore Your Composite Sink", "Transform Your Sink Today", "Sink Restoration Made Easy", "Effortless Sink Restoration"
- Description: "Restore dull composite sinks to like-new condition. Professional formula, safe daily use."

**Stone Polish Liquid Gloss:**
- Headlines: "Premium Stone Polish Gloss", "Glean Liquid Stone Polish"
- Long headline: "Transform stone surfaces with Glean's liquid gloss polish - professional results"
- Descriptions:
  - "Stone polish liquid gloss - streak-free shine for kitchen & bathroom surfaces"
  - "Liquid gloss stone polish - effortless shine for granite, marble & quartz surfaces"

**Shopping - Zombies:**
- Long headlines:
  - "Premium UK household cleaning products - trusted by families nationwide"
  - "Commercial grade cleaning supplies for homes and businesses nationwide"

### 2. Monitor Campaign Performance (Next 7 Days)

- **Daily checks** on asset group performance
- Watch for any sudden drops in impressions/clicks
- Alert client if performance degrades significantly

### 3. Fix Tool Before Next Use

**Before using this tool for ANY other client:**
- Fix dry-run mode to NOT execute real API calls
- Add proper error handling for asset creation failures
- Add verification step after execution to confirm assets exist
- Test thoroughly on test account before production use

---

## Lessons Learned

1. **Always verify tool behavior in test environment first** - This was the first production use and the dry-run bug wasn't caught
2. **Manual backup is critical** - The Google Ads Editor backup saved us from not knowing what was deleted
3. **Execution verification is mandatory** - Need to query actual account state after execution, not trust script logs
4. **Asset swaps should be atomic** - Either fully succeed or fully rollback, not partial deletions

---

## Files & References

- **Review spreadsheet:** https://docs.google.com/spreadsheets/d/1_IiZ6qQV_gq-vKqEjjqXhXVB8u9CElgo9Tx94Dwe9i4/edit
- **Execution log:** `/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/logs/execution-report-live-2025-11-28_17-05-14.json`
- **Backup file:** `~/Downloads/Go Glean UK+2025-11-28.csv` (17:08)
- **Original analysis:** `/Users/administrator/Documents/PetesBrain/clients/go-glean/reports/ad-hoc/2025-11-28-pmax-asset-text-optimisation.md`

---

**Status:** ⚠️ REQUIRES IMMEDIATE MANUAL FIX
**Next Review:** 2025-11-29 (verify manual recreation complete)
**Tool Status:** ⛔ DO NOT USE until fixed and tested
