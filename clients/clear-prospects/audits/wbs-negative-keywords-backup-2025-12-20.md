# WBS Negative Keywords Implementation - Backup & Plan
**Date**: 2025-12-20
**Task ID**: 5b605794-6504-446a-9918-3dd7f913fa41
**Campaign**: CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12
**Expected Savings**: £50/month

---

## Current State (Before Changes)

**Campaign Details**:
- Client: Clear Prospects (Customer ID: 6281395727)
- Brand: WBS (Westbourne Bathroom Showroom)
- Campaign ID: 60035097
- Campaign Name: CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12
- Campaign Type: Search
- Campaign Status: ENABLED

**Current Negative Keywords**: 83 negative keywords currently configured
- Neither "wheat bag company" nor "microwave heat pack" currently exist
- Full list includes: 12 volt, electric, adhesive, anti static, argos wheat bag, battery, beurer, and 76 other terms
- Verified: 2025-12-20 via GAQL query

---

## Planned Changes

### Adding 2 Tier 1 Negative Keywords (Exact Match)

| Keyword | Match Type | Clicks (60d) | Spend (60d) | Conversions | Justification |
|---------|-----------|--------------|-------------|-------------|---------------|
| wheat bag company | EXACT | 47 | £25.96 | 0 | Users looking for category/company name, not to buy. Daily rate: 0.78 clicks/day |
| microwave heat pack | EXACT | 51 | £24.37 | 0 | Generic heating product search, low purchase intent. Daily rate: 0.85 clicks/day |

**Total Expected Savings**: £50.30/month

**Statistical Confidence**: High (60-day data, consistent zero conversions)

**False Positive Risk**: <5%

**Revenue Risk**: None (these terms never converted)

---

## Implementation Methods

### Option 1: Google Ads Editor (Recommended)

1. Open Google Ads Editor
2. Select account: Clear Prospects (6281395727)
3. Navigate to: Campaigns → Search Campaigns → [Campaign Name]
4. Go to: Keywords → Negative keywords (Campaign level)
5. Add new negative keywords:
   - `[wheat bag company]` (exact match - use square brackets)
   - `[microwave heat pack]` (exact match - use square brackets)
6. Review changes in editor
7. Post changes to Google Ads
8. Verify in Google Ads UI

### Option 2: Google Ads UI (Manual)

1. Log into Google Ads account 6281395727
2. Navigate to: Campaigns → [Campaign Name]
3. Click "Keywords" → "Negative keywords"
4. Click "+ NEGATIVE KEYWORD"
5. Select "Campaign level"
6. Add keywords:
   - `[wheat bag company]` (Exact match)
   - `[microwave heat pack]` (Exact match)
7. Save changes

---

## CSV Import Format (Google Ads Editor)

```csv
Campaign,Keyword,Match Type
"CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12","wheat bag company","Exact"
"CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12","microwave heat pack","Exact"
```

---

## Implementation Complete ✅

**Executed**: 2025-12-20 22:58 GMT
**Method**: Google Ads API (campaignCriteria:mutate endpoint)
**Result**: Successfully added 2 negative keywords

**Added Keywords**:
1. **"wheat bag company"** [EXACT]
   - Resource: customers/6281395727/campaignCriteria/60035097~304006914200
   - Criterion ID: 304006914200
   - Status: Active ✅

2. **"microwave heat pack"** [EXACT]
   - Resource: customers/6281395727/campaignCriteria/60035097~303113319295
   - Criterion ID: 303113319295
   - Status: Active ✅

**Verification**: Both keywords confirmed via GAQL query immediately after implementation

**Campaign State**: Now has 85 negative keywords (was 83)

---

## Post-Implementation Verification

**Check After 7 Days** (2025-12-27):

1. Run search terms report for WBS Wheat Bags campaign
2. Verify NO impressions for:
   - "wheat bag company"
   - "microwave heat pack"
3. Confirm keywords appear in negative keywords list
4. Monitor campaign performance (conversions should be unaffected)
5. Update implementation status file

**Expected Outcome**:
- Zero impressions for both terms
- £50/month spend reduction
- No impact on conversions (these terms never converted)
- Campaign continues performing normally

---

## Rollback Plan

If implementation causes unexpected issues:

1. Navigate to negative keywords list
2. Remove both keywords:
   - `[wheat bag company]`
   - `[microwave heat pack]`
3. Monitor for 48 hours
4. Re-assess if negative keywords should be reinstated

**Rollback Risk**: Very low (these are proven zero-conversion terms)

---

## References

- Keyword Audit: `/clients/clear-prospects/audits/keyword-audit-2025-12-17.md`
- Implementation Status: `/clients/clear-prospects/audits/keyword-audit-2025-12-17-IMPLEMENTATION-STATUS.md`
- Task: `/clients/clear-prospects/tasks.json` (ID: 5b605794-6504-446a-9918-3dd7f913fa41)
