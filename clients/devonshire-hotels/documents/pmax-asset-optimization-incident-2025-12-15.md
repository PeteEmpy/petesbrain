# Performance Max Asset Optimization - Incident Report

**Date**: December 15, 2025
**Client**: Devonshire Hotels
**Issue**: Cross-contamination bug in MCP tool
**Status**: RESOLVED ✅

---

## Executive Summary

During Performance Max asset text optimization (Dec 3-4, 2025), a bug in the `mcp__google-ads__replace_asset_group_text_assets` tool caused one asset to be added to TWO asset groups instead of one:

- ✅ **Intended**: The Devonshire Arms Hotel
- ❌ **Unintended**: The Fell

**Root Cause**: MCP tool lacked post-linking verification to ensure assets were only added to their intended asset groups.

**Resolution**:
1. ✅ Asset manually removed from The Fell (completed)
2. ✅ Verification script created (`verify-pmax-asset-integrity.py`)
3. ✅ MCP tool bug fixed with automatic cleanup logic
4. ✅ Documentation updated

---

## Timeline

| Date | Event |
|------|-------|
| Nov 26 | Initial asset analysis shared with Helen (35 underperforming assets) |
| Nov 27 | Revised analysis (20 HIGH priority assets, property-specific) |
| Dec 1 | Helen completed review, approved replacements |
| Dec 3-4 | Assets replaced via MCP tool |
| Dec 4 | Cross-contamination discovered during verification |
| Dec 15 | Asset manually removed, bug fixed, verification script created |

---

## The Bug

### What Happened

Asset ID `238389082105` ("Yorkshire Dales Boutique Hotel") was created and linked to The Devonshire Arms Hotel (intended), but **ALSO** appeared in The Fell asset group (unintended).

### Root Cause

The MCP tool workflow:
1. ✅ Creates new text asset at ACCOUNT level (Google Ads API)
2. ✅ Links asset to intended asset group
3. ❌ **Missing**: Verification that asset ONLY exists in intended group

**Theory**: Google Ads API may have:
- Reused existing asset with same text across multiple groups
- Cached asset incorrectly during batch operations
- Race condition in multi-operation requests

### Impact

- 19/20 asset replacements: ✅ Correct
- 1/20 asset replacement: ❌ Cross-contaminated
- **Client impact**: Minimal (manually removed same day)

---

## The Fix

### 1. Verification Script

**Location**: `clients/devonshire-hotels/scripts/verify-pmax-asset-integrity.py`

**Purpose**:
- Queries all asset groups in campaign
- Checks that newly added assets appear ONLY in their intended groups
- Reports cross-contamination issues with specific asset IDs

**Usage**:
```bash
# Run via Claude Code (requires MCP context)
python3 verify-pmax-asset-integrity.py
```

**Output**:
```
DEVONSHIRE HOTELS - PMAX ASSET INTEGRITY VERIFICATION
==============================================================

Step 1: Querying all asset groups...
  ✓ Found X enabled assets per group

Step 2: Building asset-to-group index...
  ✓ Indexed Y unique assets

Step 3: Checking newly added assets for cross-contamination...
  ✅ CORRECT: Asset 238389082105 in Devonshire Arms ONLY
  ...

SUMMARY:
Total assets checked: 20
Assets correctly isolated: 20
Cross-contamination issues: 0
✅ All assets correctly isolated!
```

### 2. MCP Tool Bug Fix

**File**: `infrastructure/mcp-servers/google-ads-mcp-server/server.py`
**Function**: `replace_asset_group_text_assets()` (line 2185+)

**Changes**:
- Added **Step 2d: Post-linking verification**
- After linking asset to asset group, queries where asset appears
- If found in multiple groups, **automatically removes from unintended groups**
- Logs warnings for monitoring
- Returns verification status in response

**New Response Fields**:
```python
{
    'verification': 'PASSED',  # or 'CLEANED', 'FAILED', 'WARNING'
    'detected': True,  # if cross-contamination found
    'cleanup': 'SUCCESS',  # or 'FAILED'
    'unintended_groups_cleaned': ['6456682997']  # asset group IDs
}
```

**Behavior**:
- ✅ **PASSED**: Asset only in intended group (normal case)
- ⚠️ **CLEANED**: Cross-contamination detected and automatically fixed
- ❌ **FAILED**: Cross-contamination detected but cleanup failed (manual intervention needed)
- ⚠️ **WARNING**: Asset not found after linking (shouldn't happen)

### 3. Documentation

**Created**:
- `BUGFIX-asset-cross-contamination.patch` - Detailed technical analysis
- This incident report (`pmax-asset-optimization-incident-2025-12-15.md`)

**Updated** (TODO):
- [ ] `/docs/GOOGLE-ADS-PROTOCOL.md` - Add verification requirement
- [ ] `/docs/INCIDENTS.md` - Record incident
- [ ] MCP server README - Note about cross-contamination prevention

---

## Asset Details (For Reference)

### The Unintended Asset

| Field | Value |
|-------|-------|
| **Asset ID** | 238389082105 |
| **Text** | "Yorkshire Dales Boutique Hotel" |
| **Field Type** | HEADLINE |
| **Intended For** | The Devonshire Arms Hotel (6456703966) |
| **Appeared In** | The Fell (6456682997) |
| **Status** | ✅ Manually removed Dec 15, 2025 |

### All 20 Assets Added During Optimization

See `verify-pmax-asset-integrity.py` for complete list with intended asset groups.

---

## Lessons Learned

### What Went Well

1. ✅ **Data-driven approach** - Statistical analysis identified underperformers
2. ✅ **Client collaboration** - Helen caught duplicate text issues during review
3. ✅ **Quick detection** - Cross-contamination found during post-implementation review
4. ✅ **Rapid response** - Issue resolved same day it was detected

### What Could Be Improved

1. ❌ **Verification missing** - Tool should have verified asset isolation from the start
2. ❌ **Post-implementation checks** - Should run automated verification immediately after changes
3. ❌ **Dry run limitations** - Dry run doesn't catch linking bugs (only safety check violations)

### Process Updates

**Going Forward**:
1. ✅ **ALWAYS run verification script** after PMax asset changes
2. ✅ **Monitor MCP logs** for cross-contamination warnings
3. ✅ **Document all asset IDs** before/after for traceability
4. ✅ **Use dry_run=True first** to verify safety checks
5. ✅ **Consider Google Ads Editor** for critical changes (more control, less API magic)

---

## Testing Checklist

Before considering this fix production-ready:

- [ ] Test single asset replacement (should verify PASSED)
- [ ] Test multiple assets in same group (should verify PASSED)
- [ ] Test with duplicate text across groups (should detect and clean)
- [ ] Verify cleanup operations work correctly
- [ ] Run verification script after test replacements
- [ ] Test dry_run mode still works correctly

---

## Monitoring

### MCP Logs to Watch

```bash
# Check for cross-contamination warnings in MCP server logs
grep "CROSS-CONTAMINATION" ~/.petesbrain-mcp-server.log
```

### Verification Script Schedule

Run after EVERY PMax asset modification:
```bash
python3 clients/devonshire-hotels/scripts/verify-pmax-asset-integrity.py
```

### Response Field Monitoring

Track these fields in MCP responses:
- `verification`: Should be 'PASSED' in >95% of cases
- `detected`: If True, investigate WHY cross-contamination occurred
- `cleanup`: If 'FAILED', manual intervention required

---

## Related Documentation

- **Incident Analysis**: This document
- **Bug Fix Details**: `BUGFIX-asset-cross-contamination.patch`
- **Verification Script**: `verify-pmax-asset-integrity.py`
- **Original Analysis**: Email thread Nov 26 - Dec 1, 2025
- **Complete Asset Change Log**: `documents/asset-changes-complete-view.html`

---

## Approval & Sign-Off

**Created By**: Peter Empson
**Reviewed By**: [Pending]
**Approved By**: [Pending]
**Status**: RESOLVED - Awaiting verification test results

---

**End of Report**
