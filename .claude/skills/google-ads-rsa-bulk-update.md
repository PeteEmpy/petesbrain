# Google Ads RSA Bulk Update Skill

**Triggers**: "RSA bulk update", "update RSAs", "RSA text update", "bulk RSA changes"

**Purpose**: Guide user through bulk RSA headline/description updates using Google Ads Editor CSV import method

**When to use**:
- Seasonal promotions (Black Friday, Christmas, etc.)
- Countdown timer additions
- Brand messaging updates
- Any bulk text changes across multiple RSAs

---

## Context

**Why CSV import?**: Google Ads API doesn't allow updating RSA text (immutable fields). CSV import with #Original columns is the only workaround that preserves performance history.

**Key playbook**: `/playbooks/google-ads-rsa-bulk-text-updates.md`

---

## Workflow Steps

### Step 1: Gather Requirements

Ask the user:
1. **Which client?** (need customer ID and manager ID from CONTEXT.md)
2. **Which accounts?** (Single account or multi-region: USA/EUR/ROW/etc.)
3. **What's the change?**
   - Adding new headlines? (e.g., countdown timer)
   - Replacing existing headlines? (e.g., swapping H8)
   - Both?
4. **Which RSAs?** (provide ad IDs, or filter criteria like campaign name pattern)

### Step 2: Fetch Current State

Use GAQL to fetch current RSA state:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server')
from oauth.google_auth import execute_gaql
import json

CUSTOMER_ID = '[from CONTEXT.md]'
MANAGER_ID = '[from CONTEXT.md]'
AD_IDS = ['id1', 'id2', ...]  # OR use campaign filter

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
# Save to JSON: clients/{client}/data/{region}_rsa_current_state.json
```

**Output**: Save current state JSON for each account/region

### Step 3: Build Update JSON

**Decision point**: Are you replacing existing text or adding new headlines?

**Option A: Adding new headlines** (e.g., countdown as next available):
```python
for ad in current_state:
    new_headlines = ad['current_headlines'].copy()

    # Smart placement: add as next available headline
    if len(new_headlines) < 15:
        new_headlines.append("Black Friday Ends in {COUNTDOWN(2025-12-01 23:59:59,5)}")

    updates.append({
        'campaign_name': ad['campaign_name'],
        'ad_group_name': ad['ad_group_name'],
        'ad_id': ad['ad_id'],
        'status': ad['status'],
        'current_headlines': ad['current_headlines'],
        'new_headlines': new_headlines,
        'current_descriptions': ad['current_descriptions'],
        'new_descriptions': ad['current_descriptions'],  # No change
        'final_url': ad['final_url']
    })
```

**Option B: Replacing existing headlines** (e.g., swapping H8):
```python
for ad in current_state:
    new_headlines = ad['current_headlines'].copy()
    new_headlines[7] = "New H8 text here"  # Replace H8 (index 7)
    # ... build update object
```

**Option C: Compare with spreadsheet** (desired state in Google Sheet):
- Fetch spreadsheet data via MCP
- Compare current vs desired field-by-field
- Build updates JSON with only differences

**Output**: Save update JSON: `clients/{client}/data/{region}_rsa_updates_full.json`

### Step 4: Generate CSV

**Single account**:
```bash
cd /Users/administrator/Documents/PetesBrain/shared/scripts
python3 generate-rsa-update-csv.py \
    --input /path/to/updates.json \
    --output /path/to/updates.csv
```

**Multiple accounts**:
Use the universal combiner script (see Step 5)

**CSV Requirements**:
- Action column = "Edit"
- #Original columns must match EXACTLY what's in Google Ads
- New columns contain updated text
- Empty strings for non-existent headlines/descriptions
- NO Account column for single account
- INCLUDE Account column (XXX-XXX-XXXX format) for multi-account

### Step 5: Combine Multi-Account CSVs (if applicable)

If updating multiple accounts (USA/EUR/ROW):

```bash
cd /Users/administrator/Documents/PetesBrain/shared/scripts
python3 combine-multi-account-rsa-csv.py \
    --config /path/to/account_config.json \
    --inputs usa_updates.json eur_updates.json row_updates.json \
    --output all_regions_rsa_updates.csv
```

**Account config format**:
```json
{
    "USA": {"customer_id": "7808690871", "account_id": "780-869-0871"},
    "EUR": {"customer_id": "7679616761", "account_id": "767-961-6761"},
    "ROW": {"customer_id": "5556710725", "account_id": "555-671-0725"}
}
```

### Step 6: Import Instructions

Provide user with:

```
================================================================================
Import Instructions
================================================================================
1. Open Google Ads Editor
2. Load [SINGLE ACCOUNT / ALL ACCOUNTS: USA, EUR, ROW]
3. Account > Import > From file...
4. Select: [CSV path]
5. Review (should show X ads to be EDITED)
6. Process > Review > Post

⚠️  For multi-account: Account column will route each ad to correct account
⚠️  #Original columns ensure ads are UPDATED, not duplicated
⚠️  Test on 1-2 ads first to verify format
```

---

## Common Scenarios

### Scenario 1: Adding Countdown Timer

**User says**: "Add countdown timer to all Smythson RSAs for Black Friday"

**Steps**:
1. Fetch current state for all regions (USA/EUR/ROW)
2. Build updates adding countdown as next available headline
3. Combine into single CSV with Account column
4. Provide import instructions

**Smart placement**: Add as H12, H13, H14, or H15 depending on current count

### Scenario 2: Seasonal Messaging Update

**User says**: "Replace H8 with Christmas messaging across all RSAs"

**Steps**:
1. Fetch current state
2. Build updates replacing headline at index 7
3. Generate CSV
4. Provide import instructions

### Scenario 3: Spreadsheet-Based Updates

**User says**: "I've updated RSAs in the spreadsheet, sync to Google Ads"

**Steps**:
1. Fetch current state from Google Ads
2. Read desired state from Google Sheet (via MCP)
3. Compare field-by-field
4. Generate CSV with only changed ads
5. Provide import instructions

---

## Universal Scripts Reference

| Script | Location | Purpose |
|--------|----------|---------|
| `generate-rsa-update-csv.py` | `/shared/scripts/` | Converts JSON to Google Ads Editor CSV |
| `combine-multi-account-rsa-csv.py` | `/shared/scripts/` | Merges multiple region JSONs with Account column |
| `format_customer_id.py` | `/shared/utils/google-ads-formatters.py` | Formats customer ID with dashes |

---

## Troubleshooting

### Error: "A required account column is missing"
**Cause**: Multi-account export but no Account column
**Fix**: Use `combine-multi-account-rsa-csv.py` to add Account column

### Error: "Invalid account specified"
**Cause**: Account column format doesn't match loaded accounts
**Fix**: Ensure Account column uses dashed format (XXX-XXX-XXXX)

### Import shows "Add" instead of "Edit"
**Cause**: #Original columns don't match current ad state
**Fix**: Re-fetch current state from Google Ads to ensure exact match

### Only some ads importing
**Cause**: Google Ads Editor has filters applied
**Fix**: Check top-right filter icon, clear all filters

---

## Best Practices

1. **Always fetch fresh current state** - don't rely on old exports
2. **Test on 1-2 ads first** - verify CSV format before bulk import
3. **Save all intermediate JSONs** - for debugging if needed
4. **Keep original CSVs** - in case rollback needed
5. **Verify in Google Ads UI** - spot-check ads after posting
6. **Document what changed** - save summary of old vs new text

---

## Related Playbooks

- `/playbooks/google-ads-rsa-bulk-text-updates.md` - Comprehensive workflow guide
- `/playbooks/google-ads-pmax-text-asset-updates.md` - For PMAX assets (uses API)
- `/playbooks/google-ads-seasonal-promotions.md` - Seasonal campaign updates
