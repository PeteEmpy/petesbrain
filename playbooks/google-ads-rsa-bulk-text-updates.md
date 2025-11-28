# Google Ads RSA Bulk Text Updates via Editor CSV Import

**Purpose**: Update RSA headlines/descriptions across multiple ads while preserving performance history

**When to use**:
- Seasonal promotions (Black Friday, Christmas, etc.)
- Countdown timer additions
- Brand messaging updates
- Any bulk text changes across 10+ RSAs

**Why CSV import instead of API**: Google Ads API doesn't allow updating RSA text (immutable fields). CSV import with #Original columns is the only workaround.

---

## Key Concepts

### The #Original Column Method
Google Ads Editor can match and update existing ads using **#Original columns**:

- **#Original columns** = Current state (for matching)
- **Regular columns** = New state (what you want to change to)
- If `#Original` is blank but new value exists → **ADDS** new headline/description
- If `#Original` has text but new value differs → **REPLACES** existing text
- If `#Original` matches new value → **NO CHANGE**

### Account Column Format
For multi-account imports, the Account column must be the **customer ID with dashes**:
- Format: `XXX-XXX-XXXX`
- Example: `7808690871` → `780-869-0871`
- Find in Google Ads Editor account list or from customer_id in CONTEXT.md

---

## Workflow

### Step 1: Fetch Current State from Google Ads

**Why**: You need the current headlines/descriptions to populate #Original columns

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/path/to/google-ads-mcp-server')
from oauth.google_auth import execute_gaql
import json

# Account config
CUSTOMER_ID = '7808690871'
MANAGER_ID = '2569949686'

# Get ad IDs from spreadsheet or list
AD_IDS = ["784198246551", "784523200052", ...]

query = f"""
SELECT
    campaign.name,
    ad_group.name,
    ad_group_ad.ad.id,
    ad_group_ad.status,
    ad_group_ad.ad.responsive_search_ad.headlines,
    ad_group_ad.ad.responsive_search_ad.descriptions,
    ad_group_ad.ad.final_urls
FROM ad_group_ad
WHERE
    ad_group_ad.ad.id IN ({",".join(AD_IDS)})
    AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
"""

result = execute_gaql(CUSTOMER_ID, query, MANAGER_ID)
# Save to JSON for next step
```

### Step 2: Build Update JSON

**Decision point**: Are you replacing existing text or adding new headlines?

**Option A: Adding new headlines** (e.g., adding countdown as next available headline):
```python
for ad in current_state:
    new_headlines = ad['current_headlines'].copy()
    new_headlines.append("Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}")
    # Store both current and new
```

**Option B: Replacing existing headlines** (e.g., swapping H8):
```python
for ad in current_state:
    new_headlines = ad['current_headlines'].copy()
    new_headlines[7] = "New H8 text here"  # Replace H8 (index 7)
    # Store both current and new
```

**Option C: Compare with spreadsheet** (desired state in Google Sheet):
```python
# Fetch spreadsheet data
# Compare current vs desired
# Build updates JSON with differences
```

### Step 3: Generate CSV

**Required columns** (in order):
1. `Account` (optional for single-account, required for multi-account)
2. `Action` (always "Edit")
3. `Campaign`
4. `Ad group`
5. `Ad ID`
6. `Ad type` (always "Responsive search ad")
7. `Ad status` (e.g., "Enabled")
8. `Headline 1#Original` through `Headline 15#Original`
9. `Headline 1` through `Headline 15`
10. `Description 1#Original` through `Description 4#Original`
11. `Description 1` through `Description 4`
12. `Final URL`

**Critical rules**:
- #Original columns must match EXACTLY what's currently in Google Ads
- New columns contain the updated text
- Empty strings for headlines/descriptions that don't exist
- NO Account column if importing to single account already loaded in Editor
- Include Account column (with dashes) for multi-account imports

### Step 4: Import to Google Ads Editor

**Single account**:
1. Open Google Ads Editor
2. Load the target account
3. Account > Import > From file...
4. Select CSV
5. Review changes (should show "Edit" not "Add")
6. Process > Review > Post

**Multiple accounts**:
1. Open Google Ads Editor
2. Load ALL target accounts
3. Account > Import > From file...
4. Select CSV with Account column
5. Editor will route each row to correct account based on Account column
6. Review changes across all accounts
7. Process > Review > Post

---

## Common Scenarios

### Scenario 1: Adding Countdown Timer to All RSAs

**Challenge**: Different RSAs have different numbers of headlines (11-14). Where to add countdown?

**Solution**: Add as NEXT available headline for each ad
- Ad with 11 headlines → add as H12
- Ad with 13 headlines → add as H14
- Etc.

**Script**: `smart_rsa_updates.py` (adds countdown intelligently)

### Scenario 2: Multi-Region Update (Different Accounts)

**Challenge**: Update USA, EUR, ROW accounts in one go

**Solution**:
1. Fetch current state for each account separately
2. Build update JSONs for each region
3. Combine all into single CSV with Account column
4. Import once to all accounts

**Script**: `combine_all_regions_csv.py`

### Scenario 3: Spreadsheet-Based Updates

**Challenge**: Client has updated RSAs in Google Sheet, need to sync to Google Ads

**Solution**:
1. Fetch current state from Google Ads
2. Read desired state from Google Sheet
3. Compare field-by-field
4. Generate CSV with only changed ads
5. Import

**Script**: `build_region_rsa_updates.py` (with spreadsheet comparison)

---

## Scripts Reference

### Location
- **Universal scripts**: `/shared/scripts/`
- **Client-specific scripts**: `/clients/{client}/scripts/`
- **Data files**: `/clients/{client}/data/`

### Key Scripts

**`generate-rsa-update-csv.py`** (universal)
- Converts update JSON to Google Ads Editor CSV
- Handles #Original column generation
- Used by all RSA update workflows

**`smart_rsa_updates.py`** (example)
- Adds countdown as next available headline
- Detects existing countdowns
- Handles varying headline counts

**`combine_all_regions_csv.py`** (example)
- Merges multiple region JSONs
- Adds Account column with dashed IDs
- Single CSV for multi-account import

**`process_all_regions.py`** (example)
- Fetches current state from multiple accounts
- Parallel processing
- Saves region-specific JSONs

---

## Troubleshooting

### Error: "A required account column is missing"
**Cause**: Multi-account export but no Account column
**Fix**: Add Account column with dashed customer ID

### Error: "Invalid account specified"
**Cause**: Account name/ID doesn't match loaded accounts
**Fix**:
- Check Account column format (should be `XXX-XXX-XXXX`)
- OR remove Account column entirely if single account

### Import shows "Add" instead of "Edit"
**Cause**: #Original columns don't match current ad state
**Fix**: Re-fetch current state from Google Ads to ensure exact match

### Only some ads importing (e.g., 10 of 27)
**Cause**: Google Ads Editor has filters applied
**Fix**: Check top-right filter icon, clear all filters

### Headlines not in right position
**Cause**: Google Ads Editor re-arranges headlines alphabetically in some views
**Fix**: This is just display - actual positions are preserved

---

## Best Practices

1. **Always fetch fresh current state** - don't rely on old exports
2. **Test on 1-2 ads first** - verify CSV format before bulk import
3. **Save all intermediate JSONs** - current_state, updates, etc. for debugging
4. **Keep original CSVs** - in case you need to rollback
5. **Verify in Google Ads UI** - after posting, spot-check ads in web UI
6. **Document what changed** - save summary of old vs new text

---

## Limitations

**Cannot do via CSV import**:
- Add more than 15 headlines (Google Ads max)
- Add more than 4 descriptions (Google Ads max)
- Change ad type (e.g., RSA to something else)
- Delete ads (use Google Ads Editor UI or API)
- Add headlines/descriptions out of sequence (must fill H1-H11 before adding H12)

**Must use UI/API for**:
- Creating new RSAs
- Removing RSAs
- Changing final URLs to different domains (must match account domain)
- Bulk pausing/enabling (easier via Editor UI)

---

## Related Playbooks

- `google-ads-pmax-text-asset-updates.md` - For PMAX asset text (uses API, not CSV)
- `google-ads-editor-bulk-operations.md` - Other bulk operations via Editor
- `google-ads-seasonal-promotions.md` - Seasonal campaign updates

---

## Example: Smythson Black Friday 2025

**Context**: Add countdown timer to 59 RSAs across USA/EUR/ROW accounts

**Steps taken**:
1. Fetched current state from all 3 accounts (41 USA, 14 EUR, 4 ROW)
2. Built update JSONs adding countdown as next headline
3. Combined into single CSV with Account column
4. Imported to all accounts at once

**Files**:
- `/clients/smythson/scripts/smart_rsa_updates.py`
- `/clients/smythson/scripts/combine_all_regions_csv.py`
- `/clients/smythson/data/all_regions_rsa_updates.csv`

**Result**: 59 RSAs updated in ~5 minutes vs hours of manual editing
