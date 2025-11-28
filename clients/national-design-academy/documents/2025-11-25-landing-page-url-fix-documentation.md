# NDA Landing Page URL Fix - 25 November 2025

## Issue Discovered

While reviewing the top 5 landing pages spreadsheet for NDA, discovered that the degree URL appeared twice:
- `/study/courses/degrees-interior-design` (appeared in rows 3 and 4)

Investigation revealed the root cause: **Three Diploma campaign asset groups were accidentally sending traffic to the Degree page instead of the Diploma page.**

---

## The Problem

**Affected Asset Groups (all ENABLED and live):**

| Asset Group | Campaign | Issue |
|-------------|----------|-------|
| Remarketing UAE | NDA \| P Max Reboot \| Interior Design Diploma - UAE 175 no target 28/5 | Sending diploma remarketing traffic to degree page |
| Remarketing UAE | NDA \| P Max \| Interior Design Diploma - UAE 175 | Sending diploma remarketing traffic to degree page |
| Interior Design Diploma | NDA \| P Max \| Interior Design - Australia/New Zealand | Sending diploma traffic to degree page |

**Wrong URL (what they were using):**
```
https://www.nda.ac.uk/study/courses/degrees-interior-design/
```

**Correct URL (what they should use):**
```
https://www.nda.ac.uk/study/courses/diploma-interior-design/
```

---

## Impact

**User Experience:**
- Users interested in **Diplomas** were landing on the **Degree** course page
- Confusing messaging and incorrect course information
- Likely causing lower conversion rates on these campaigns

**Performance Data:**
From last 30 days landing page data:
- `/courses/degrees-interior-design`: 2,398 clicks (includes wrong diploma traffic)
- `/interior-design-degrees/`: 11,834 clicks (legitimate degree traffic)

The diploma traffic was incorrectly inflating the degree page stats and splitting traffic between two different degree URLs.

---

## The Fix

**Method:** Update `finalUrls` field in 3 asset groups via Google Ads API

**Asset Groups Updated:**

1. **Asset Group ID: 6574590886**
   - Campaign: NDA | P Max Reboot | Interior Design Diploma - UAE 175 no target 28/5
   - Asset Group: Remarketing UAE
   - Description: UAE Diploma remarketing (newer campaign)

2. **Asset Group ID: 6553188869**
   - Campaign: NDA | P Max | Interior Design Diploma - UAE 175
   - Asset Group: Remarketing UAE
   - Description: UAE Diploma remarketing (older campaign)

3. **Asset Group ID: 6518747041**
   - Campaign: NDA | P Max | Interior Design - Australia/New Zealand
   - Asset Group: Interior Design Diploma
   - Description: Australia/NZ Diploma main asset group

**API Operation Used:**
```json
{
    "operations": [{
        "update": {
            "resourceName": "customers/1994728449/assetGroups/{asset_group_id}",
            "finalUrls": ["https://www.nda.ac.uk/study/courses/diploma-interior-design/"]
        },
        "updateMask": "finalUrls"
    }]
}
```

---

## Implementation

**Script Created:**
`/clients/national-design-academy/scripts/fix-asset-group-urls.py`

**To run the fix:**
```bash
cd /Users/administrator/Documents/PetesBrain/clients/national-design-academy/scripts
python3 fix-asset-group-urls.py
```

**Script features:**
- Shows review of all changes before proceeding
- Requires explicit "yes" confirmation
- Updates all 3 asset groups via Google Ads API
- Provides detailed success/failure reporting
- Safe to run multiple times (idempotent)

---

## Verification Steps

**After running the fix:**

1. **Check asset group URLs via API:**
```python
mcp__google-ads__run_gaql(
    customer_id="1994728449",
    query="""
        SELECT
          asset_group.id,
          asset_group.name,
          asset_group.final_urls
        FROM asset_group
        WHERE asset_group.id IN (6574590886, 6553188869, 6518747041)
    """
)
```

2. **Monitor landing page performance:**
   - Check that diploma traffic goes to `/courses/diploma-interior-design/`
   - Verify degree traffic consolidates to `/interior-design-degrees/`
   - Watch conversion rates on the 3 fixed campaigns

3. **Re-run top 5 landing pages report:**
   - Degree URL should only appear once
   - Diploma URL should appear separately with correct traffic

---

## Expected Results

**Before Fix:**
- Diploma campaigns → Degree page (wrong)
- Degree URL appears twice in top 5 landing pages
- Confused user journey

**After Fix:**
- Diploma campaigns → Diploma page (correct)
- Degree URL appears once in top 5 landing pages
- Clear, correct user journey
- Expected: Higher conversion rates on fixed campaigns

---

## Root Cause Analysis

**Why did this happen?**

The asset groups were likely set up by copying from degree campaigns and the URLs weren't updated when creating the diploma variants. Common setup error when duplicating Performance Max campaigns.

**Prevention:**
- Always verify final URLs match campaign intent (diploma vs degree)
- Use descriptive asset group names that clearly indicate target course
- Regular audits of landing page usage by campaign type

---

## Timeline

- **25 November 2025, 14:30**: Issue discovered during landing page analysis
- **25 November 2025, 15:00**: Root cause identified (3 asset groups with wrong URLs)
- **25 November 2025, 15:30**: Fix script created and tested
- **25 November 2025, 16:00**: Awaiting client approval to implement

---

## Files Created/Modified

**New Files:**
- `/clients/national-design-academy/scripts/fix-asset-group-urls.py` - Fix script
- `/clients/national-design-academy/documents/2025-11-25-landing-page-url-fix-documentation.md` - This document
- `/clients/national-design-academy/documents/text-draft-2025-11-25-landing-page-url-issue.html` - Teams message to Paul

**Analysis Files:**
- Google Ads landing page data (last 30 days)
- Asset group configuration export

---

## Contact

**Client:** Paul Riley (pk@nda.ac.uk)
**Account Manager:** Peter Empson (petere@roksys.co.uk)
**Date:** 25 November 2025

---

## Notes

- All 3 asset groups are currently ENABLED and actively sending traffic
- Fix is low-risk (simple URL update, no changes to ads or targeting)
- No campaign performance history will be lost
- Change takes effect immediately upon API update
- Consider similar audit for NMA (National Motorsports Academy) campaigns
