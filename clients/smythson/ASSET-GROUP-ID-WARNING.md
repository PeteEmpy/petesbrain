# ⚠️ CRITICAL: Asset Group ID Matching Issue
**Date Created**: 2025-11-27
**Priority**: HIGH
**Relates To**: Post-Black Friday asset reversion (Dec 2, 2025)

---

## Issue Summary

The Smythson asset reversion scripts (`apply-text-assets-from-sheet.py`) use **name-based matching** to find asset groups, which could cause wrong-group execution if duplicate names exist.

**Similar to**: Tree2mydoor bug fixed today (2025-11-27) where same asset text existed in multiple groups.

---

## The Risk

### Current Implementation

```python
# File: clients/smythson/scripts/apply-text-assets-from-sheet.py
# Lines: 166-199

def find_asset_group_id(headers, customer_id: str, campaign_name: str,
                         asset_group_name: str) -> Optional[str]:
    """Find asset group ID by campaign name and asset group name."""

    # Query ALL asset groups
    query = """
        SELECT asset_group.id, asset_group.name, campaign.id, campaign.name
        FROM asset_group
        WHERE campaign.status != 'REMOVED' AND asset_group.status != 'REMOVED'
    """

    # Search for matching names
    for result in results:
        camp_name = result.get('campaign', {}).get('name', '')
        ag_name = result.get('assetGroup', {}).get('name', '')

        if camp_name == campaign_name and ag_name == asset_group_name:
            return ag_id, camp_id  # Returns FIRST match found
```

### The Problem

**If duplicate asset group names exist**:
1. Function returns FIRST match found
2. Could target wrong account (UK vs US vs EUR vs ROW)
3. Could modify wrong campaign
4. No validation that the match is correct

**Example scenario**:
- UK account has asset group "Gifting | Leather Goods"
- US account also has "Gifting | Leather Goods"
- Spreadsheet says "update Gifting | Leather Goods"
- Script could modify either one (unpredictable)

---

## What Happened With Tree2mydoor Today

**Same issue, different trigger**:
- Asset text "Big Choice - Affordable Prices" existed in 2 groups
- Olive Tree Competitors (6519856317) ← User wanted this
- Lemon Trees (6512862214) ← Script matched this instead

**Result**: Wrong asset group modified

**Fix applied**: Use Asset Group ID from CSV instead of searching by text

---

## Smythson-Specific Risks

### Spreadsheet Structure

**Current spreadsheet** (https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit):

```
Column A: Campaign Name (e.g., "UK Gifting")
Column B: Asset Group Name (e.g., "Gifting | Leather Goods")
Columns C-AA: Text assets
```

**No Asset Group ID column!**

### Risk Level Assessment

**Low risk IF**:
- Asset group names are unique across ALL accounts
- Campaign names are unique across ALL accounts
- Combination (campaign + asset group) is definitely unique

**High risk IF**:
- Same asset group names used in multiple accounts
- Similar campaign structures across UK/US/EUR/ROW
- Copy-paste naming conventions

### Smythson Account Structure

**4 accounts**:
- UK (8573235780)
- US (7808690871)
- EUR (7679616761)
- ROW (5556710725)

**Question**: Do these accounts have identical campaign/asset group names?

If YES → **HIGH RISK** of wrong-account execution

---

## Recommended Fix

### Option 1: Add Asset Group IDs to Spreadsheet (Best)

**Changes needed**:

1. **Add column to spreadsheet**:
   ```
   Column A: Campaign ID
   Column B: Campaign Name
   Column C: Asset Group ID  ← NEW
   Column D: Asset Group Name
   Columns E-...: Text assets
   ```

2. **Update script to read Asset Group ID**:
   ```python
   def parse_text_assets_from_row(row: List[str]) -> Dict:
       campaign_id = row[0].strip()         # Column A
       campaign_name = row[1].strip()       # Column B
       asset_group_id = row[2].strip()      # Column C ← NEW
       asset_group_name = row[3].strip()    # Column D

       return {
           'campaign_id': campaign_id,
           'campaign_name': campaign_name,
           'asset_group_id': asset_group_id,  # ← Use this directly
           'asset_group_name': asset_group_name,
           ...
       }
   ```

3. **Remove `find_asset_group_id()` function**:
   ```python
   # OLD: asset_group_id, campaign_id = find_asset_group_id(...)
   # NEW: asset_group_id = text_data['asset_group_id']  # From spreadsheet
   ```

**Benefits**:
- Exact targeting (impossible to match wrong group)
- Faster (no API query needed)
- Safer (no name ambiguity)
- Same fix as Tree2mydoor

**Effort**: ~30 minutes (spreadsheet update + script changes)

---

### Option 2: Validate Match is Unique (Acceptable)

Keep current approach but add validation:

```python
def find_asset_group_id(headers, customer_id: str, campaign_name: str,
                         asset_group_name: str) -> Optional[str]:
    # ... existing code ...

    matches = []
    for result in results:
        camp_name = result.get('campaign', {}).get('name', '')
        ag_name = result.get('assetGroup', {}).get('name', '')

        if camp_name == campaign_name and ag_name == asset_group_name:
            ag_id = str(result.get('assetGroup', {}).get('id'))
            camp_id = str(result.get('campaign', {}).get('id'))
            matches.append((ag_id, camp_id, camp_name, ag_name))

    # VALIDATION: Ensure only ONE match
    if len(matches) == 0:
        raise ValueError(f"No asset group found: {campaign_name} / {asset_group_name}")
    elif len(matches) > 1:
        raise ValueError(
            f"AMBIGUOUS: Multiple asset groups match '{campaign_name} / {asset_group_name}':\n"
            + "\n".join([f"  - Campaign {m[1]}, Asset Group {m[0]}" for m in matches])
        )

    return matches[0][0], matches[0][1]
```

**Benefits**:
- Detects ambiguous matches
- Prevents wrong-group execution
- Minimal code changes

**Limitations**:
- Still requires unique names
- Slower (API query needed)
- Could fail if names aren't unique

**Effort**: ~15 minutes (add validation only)

---

### Option 3: Use Customer ID Filter (Minimum)

At minimum, filter the query to only search within the current customer account:

```python
def find_asset_group_id(headers, customer_id: str, campaign_name: str,
                         asset_group_name: str) -> Optional[str]:
    formatted_cid = format_customer_id(customer_id)

    query = f"""
        SELECT
            asset_group.id,
            asset_group.name,
            campaign.id,
            campaign.name
        FROM asset_group
        WHERE campaign.status != 'REMOVED'
        AND asset_group.status != 'REMOVED'
        AND campaign.customer.id = {formatted_cid}  ← ADD THIS FILTER
    """
```

**Benefits**:
- Prevents cross-account matching
- Minimal code changes

**Limitations**:
- Still risky if duplicate names within same account
- Doesn't fully solve the issue

**Effort**: ~5 minutes (add one line)

---

## Recommendation

**IMMEDIATE** (before Dec 2 execution):

1. ✅ **Option 3** (5 min) - Add customer ID filter to query
   - Prevents cross-account errors
   - Quick safety improvement

2. 🔶 **Option 2** (15 min) - Add ambiguity validation
   - Detects duplicate names
   - Fails safely if issue found

3. ⭐ **Option 1** (30 min) - Add Asset Group IDs to spreadsheet (BEST PRACTICE)
   - Eliminates risk entirely
   - Same safe approach as Tree2mydoor fix
   - Future-proof

**Suggested timeline**:
- **Now**: Implement Option 3 (customer ID filter)
- **Before execution**: Implement Option 2 (validation)
- **For future**: Implement Option 1 (Asset Group IDs in spreadsheet)

---

## Verification Steps

### Before Dec 2 Execution

**1. Check for duplicate names**:
```python
# Run this query for each account
query = """
    SELECT
        campaign.name,
        asset_group.name,
        COUNT(*) as count
    FROM asset_group
    WHERE campaign.status != 'REMOVED'
    GROUP BY campaign.name, asset_group.name
    HAVING COUNT(*) > 1
"""

# If count > 1 found → DUPLICATE NAMES EXIST → HIGH RISK
```

**2. Test with dry-run**:
```bash
python3 apply-text-assets-from-sheet.py --region uk --dry-run
```

**3. Verify asset group IDs**:
```
Check dry-run output shows correct asset groups
Compare against Google Ads UI
Confirm account ID matches (UK=8573235780, etc.)
```

**4. Test with 1 asset group first**:
```
Select single row in spreadsheet
Run live execution on one group
Verify in Google Ads UI
Then proceed with full execution
```

---

## Related Documentation

- **Tree2mydoor fix**: `/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/logs/investigation-report-2025-11-27.md`
- **Resolution summary**: `/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/logs/resolution-summary-2025-11-27.md`
- **Workflow guide**: `/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/WORKFLOW.md`

---

## Action Items

- [ ] Implement Option 3 (customer ID filter) - 5 minutes
- [ ] Implement Option 2 (ambiguity validation) - 15 minutes
- [ ] Check for duplicate asset group names across accounts
- [ ] Test dry-run before Dec 2
- [ ] Consider implementing Option 1 (Asset Group IDs) for future
- [ ] Update task notes with this warning

---

## Task Reference

**Related task**: `[Smythson] Revert Black Friday assets + create checklist for smooth execution`
- Due: 2025-12-02
- Spreadsheet: https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit
- Script: `/Users/administrator/Documents/PetesBrain/clients/smythson/scripts/apply-text-assets-from-sheet.py`

---

**Created**: 2025-11-27
**Priority**: HIGH
**Status**: WARNING - Action required before Dec 2 execution
**Author**: PetesBrain AI Assistant (based on Tree2mydoor lesson learned)
