# Google Ads Simple Scripts

**TL;DR**: Seven universal scripts for common Google Ads operations. Simple, fast, reliable.

---

## The Seven Scripts

All located in `/shared/scripts/`:

1. **update-google-ads-budgets.py** - Update campaign budgets
2. **update-google-ads-campaign-status.py** - Pause/enable campaigns
3. **update-google-ads-target-roas.py** - Update target ROAS bidding
4. **query-google-ads-performance.py** - Query performance data
5. **add-google-ads-negative-keywords.py** - Add negative keywords to campaigns
6. **update-google-ads-keyword-status.py** - Pause/enable individual keywords
7. **export-google-ads-search-terms.py** - Export search term reports with metrics

**Why These Scripts Exist**: Instead of 60+ redundant client-specific scripts, we have 7 universal scripts that work for all clients.

---

## 1. Budget Updates

### Single Campaign

```bash
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/update-google-ads-budgets.py \
  --customer-id 8573235780 \
  --campaign "Brand Exact" \
  --budget 1500
```

### Multiple Campaigns (Batch)

Create JSON file:
```json
[
  {"campaign": "Brand Exact", "new_daily_budget": 1500},
  {"campaign": "P Max H&S", "new_daily_budget": 600},
  {"campaign": "Shopping", "new_daily_budget": 700}
]
```

Run:
```bash
python3 update-google-ads-budgets.py --customer-id 8573235780 --file budgets.json
```

**Output**:
```
Brand Exact                                   £1,200.00 → £1,500.00... ✅
P Max H&S                                     £  500.00 → £  600.00... ✅
Shopping                                      £  650.00 → £  700.00... ✅

✅ 3/3 successful
```

---

## 2. Campaign Status (Pause/Enable)

### Single Campaign

```bash
python3 update-google-ads-campaign-status.py \
  --customer-id 8573235780 \
  --campaign "Brand Exact" \
  --status PAUSED
```

### Multiple Campaigns (Batch)

Create JSON file:
```json
[
  {"campaign": "Brand Exact", "status": "PAUSED"},
  {"campaign": "Shopping", "status": "ENABLED"}
]
```

Run:
```bash
python3 update-google-ads-campaign-status.py --customer-id 8573235780 --file updates.json
```

**Valid Statuses**: `ENABLED`, `PAUSED`, `REMOVED`

---

## 3. Target ROAS Updates

### Single Campaign

```bash
python3 update-google-ads-target-roas.py \
  --customer-id 8573235780 \
  --campaign "P Max H&S" \
  --target-roas 4.0
```

**Target ROAS Format**: Decimal (e.g., `4.0` = 400%, `2.5` = 250%)

**Warning System**: If campaign bidding strategy is not `TARGET_ROAS`, script shows warning and asks for confirmation.

### Multiple Campaigns (Batch)

Create JSON file:
```json
[
  {"campaign": "P Max H&S", "target_roas": 4.0},
  {"campaign": "Shopping", "target_roas": 3.5}
]
```

Run:
```bash
python3 update-google-ads-target-roas.py --customer-id 8573235780 --file updates.json
```

---

## 4. Performance Queries

### Account-Level Summary

```bash
python3 query-google-ads-performance.py \
  --customer-id 8573235780 \
  --start-date 2025-11-01 \
  --end-date 2025-11-25 \
  --output summary
```

**Output**:
```
====================================================================================================
PERFORMANCE SUMMARY
====================================================================================================

Campaign                                                Spend      Revenue     ROAS   Conv
----------------------------------------------------------------------------------------------------
SMY | UK | Search | Brand Exact                    £ 14846.33 £  119478.44     805%  701.5
SMY | UK | P Max | H&S                             £  7389.56 £   30919.39     418%  223.3
SMY | UK | P Max | Diaries                         £  6335.36 £   21144.28     334%  165.3
----------------------------------------------------------------------------------------------------
TOTAL                                              £ 61594.81 £  340250.70     552% 1997.4

Clicks: 25,478 | Impressions: 1,234,567 | CTR: 2.06% | Avg CPC: £2.42
====================================================================================================
```

### Export to CSV

```bash
python3 query-google-ads-performance.py \
  --customer-id 8573235780 \
  --start-date 2025-11-01 \
  --end-date 2025-11-25 \
  --output csv \
  --file performance.csv
```

### Export to JSON

```bash
python3 query-google-ads-performance.py \
  --customer-id 8573235780 \
  --start-date 2025-11-01 \
  --end-date 2025-11-25 \
  --output json \
  --file performance.json
```

### Filter by Campaigns

```bash
python3 query-google-ads-performance.py \
  --customer-id 8573235780 \
  --start-date 2025-11-01 \
  --end-date 2025-11-25 \
  --campaigns "Brand,Shopping,P Max" \
  --output summary
```

**Campaign Matching**: Partial match supported (e.g., "Brand" finds all brand campaigns)

---

## 5. Add Negative Keywords

### Single Campaign

```bash
python3 add-google-ads-negative-keywords.py \
  --customer-id 8573235780 \
  --campaign "Brand Exact" \
  --keywords "cheap,free,discount"
```

**Output**:
```
Adding 3 negative keywords (EXACT match)

Adding [cheap]... ✅
Adding [free]... ✅
Adding [discount]... ✅

✅ 3/3 keywords added successfully
```

### With Match Type

```bash
python3 add-google-ads-negative-keywords.py \
  --customer-id 8573235780 \
  --campaign "Shopping" \
  --keywords "wholesale,bulk" \
  --match-type PHRASE
```

**Match Types**: `EXACT`, `PHRASE`, `BROAD` (default: EXACT)

### Multiple Campaigns (Batch)

Create JSON file:
```json
[
  {
    "campaign": "Brand Exact",
    "keywords": ["cheap", "free", "discount"],
    "match_type": "EXACT"
  },
  {
    "campaign": "Shopping",
    "keywords": ["wholesale", "bulk"],
    "match_type": "PHRASE"
  }
]
```

Run:
```bash
python3 add-google-ads-negative-keywords.py --customer-id 8573235780 --file keywords.json
```

---

## 6. Keyword Status (Pause/Enable)

### Single Keyword

```bash
python3 update-google-ads-keyword-status.py \
  --customer-id 8573235780 \
  --campaign "Brand Exact" \
  --keyword "smythson" \
  --status PAUSED
```

**Output**:
```
Finding keyword in campaign: Brand Exact
Keyword: smythson

Found:
  Campaign: SMY | UK | Search | Brand Exact
  Ad Group: UK - Brand
  Keyword: smythson [BROAD]
  Current status: ENABLED
  New status: PAUSED

Updating... ✅ SUCCESS
```

**Valid Statuses**: `ENABLED`, `PAUSED`, `REMOVED`

### Multiple Keywords (Batch)

Create JSON file:
```json
[
  {
    "campaign": "Brand Exact",
    "keyword": "smythson",
    "status": "PAUSED"
  },
  {
    "campaign": "Shopping",
    "keyword": "luxury notebooks",
    "status": "ENABLED"
  }
]
```

Run:
```bash
python3 update-google-ads-keyword-status.py --customer-id 8573235780 --file keywords.json
```

**Note**: Keyword matching is partial - script finds keywords containing the text you provide.

---

## 7. Export Search Terms

### Summary View (Default)

```bash
python3 export-google-ads-search-terms.py \
  --customer-id 8573235780 \
  --start-date 2025-11-01 \
  --end-date 2025-11-25 \
  --output summary
```

**Output**:
```
SEARCH TERM REPORT SUMMARY
Total Search Terms: 98
Total Spend: £19,060.79
Total Revenue: £154,085.74
Overall ROAS: 808%

⚠️  WASTAGE CANDIDATES (£10+ spend, 0 conversions): 49 terms
   Total wastage: £1,892.08 (9.9% of spend)

Search Term                                             Spend   Clicks   Match Type
smythson wallet                                    £   104.40      101        EXACT
smythson watch box                                 £    91.28       40        EXACT
...

✅ EXPANSION OPPORTUNITIES (ROAS >400%, 2+ conversions): 31 terms

Search Term                                            ROAS      Revenue   Match Type
smythson                                               770% £   86021.80        EXACT
smythson diary                                        1856% £    9262.14        EXACT
...
```

### Export to CSV

```bash
python3 export-google-ads-search-terms.py \
  --customer-id 8573235780 \
  --start-date 2025-11-01 \
  --end-date 2025-11-25 \
  --output csv \
  --file search-terms.csv
```

### Find Wastage (High Clicks, No Conversions)

```bash
python3 export-google-ads-search-terms.py \
  --customer-id 8573235780 \
  --start-date 2025-10-01 \
  --end-date 2025-11-25 \
  --min-clicks 10 \
  --output summary
```

**Use Case**: Identifies terms with ≥10 clicks but 0 conversions (wastage candidates)

### High-Spend Terms Only

```bash
python3 export-google-ads-search-terms.py \
  --customer-id 8573235780 \
  --start-date 2025-10-01 \
  --end-date 2025-11-25 \
  --min-cost 50 \
  --output csv \
  --file high-spend.csv
```

**Use Case**: Focus on terms that spent ≥£50 (or $50, depending on currency)

### Filter by Campaign

```bash
python3 export-google-ads-search-terms.py \
  --customer-id 8573235780 \
  --start-date 2025-11-01 \
  --end-date 2025-11-25 \
  --campaign "Brand" \
  --output summary
```

**Note**: Campaign matching is partial (e.g., "Brand" finds all brand campaigns)

### Common Use Cases

**Monthly Search Term Audit**:
```bash
python3 export-google-ads-search-terms.py \
  --customer-id 8573235780 \
  --start-date 2025-10-01 \
  --end-date 2025-10-31 \
  --output csv \
  --file october-search-terms.csv
```
Then review in Excel/Google Sheets for:
- Wastage terms → Add as negatives
- Expansion terms → Add as exact match keywords
- Irrelevant terms → Add as broad negatives

**Quick Wastage Check**:
```bash
python3 export-google-ads-search-terms.py \
  --customer-id 8573235780 \
  --start-date 2025-11-01 \
  --end-date 2025-11-25 \
  --min-clicks 5 \
  --output summary
```
Shows terms with ≥5 clicks instantly - wastage candidates highlighted.

---

## Common Account IDs

| Client | Account ID | Notes |
|--------|------------|-------|
| **Smythson UK** | 8573235780 | Main UK market |
| **Smythson USA** | 7808690871 | US market |
| **Smythson EUR** | 7679616761 | European markets |
| **Smythson ROW** | 5556710725 | Rest of world |
| **Devonshire** | 5898250490 | Single account |
| **Superspace** | 7482100090 | Single account |

**Find More**: Check `clients/{client}/CONTEXT.md` under "Platform IDs"

**Or Use MCP Tool**:
```python
mcp__google_ads__get_client_platform_ids('smythson')
# Returns: {'google_ads_customer_id': '8573235780', ...}
```

---

## Campaign Name Matching

All scripts use **partial matching** - you don't need exact names:

| You Type | Script Finds |
|----------|-------------|
| `"Brand Exact"` | `"SMY \| UK \| Search \| Brand Exact"` |
| `"H&S Christmas"` | `"SMY \| UK \| P Max \| H&S Christmas Gifting"` |
| `"Shopping"` | Any campaign with "Shopping" in the name |

**Tip**: Use unique parts of the campaign name to avoid ambiguity. If multiple campaigns match, script uses the first one found.

---

## JSON Format Standards

All batch operations use the same simple JSON structure:

**Budgets**:
```json
[
  {
    "campaign": "partial campaign name",
    "new_daily_budget": 123.45
  }
]
```

**Campaign Status**:
```json
[
  {
    "campaign": "partial campaign name",
    "status": "PAUSED"
  }
]
```

**Target ROAS**:
```json
[
  {
    "campaign": "partial campaign name",
    "target_roas": 3.5
  }
]
```

**Flexible Field Names**: `campaign` or `campaign_name` both work.

---

## Multi-Account Operations (e.g., Smythson)

Smythson has 4 accounts. Run the script 4 times:

```bash
# UK
python3 update-google-ads-budgets.py --customer-id 8573235780 --file uk-budgets.json

# USA
python3 update-google-ads-budgets.py --customer-id 7808690871 --file usa-budgets.json

# EUR
python3 update-google-ads-budgets.py --customer-id 7679616761 --file eur-budgets.json

# ROW
python3 update-google-ads-budgets.py --customer-id 5556710725 --file row-budgets.json
```

**Alternative**: Create a simple wrapper script if you do this often.

---

## How These Scripts Work

**Key Pattern** (same across all four scripts):

1. **Campaign Name Lookup**: Find campaign by partial name match
   ```python
   query = f'''
       SELECT campaign.id, campaign.name, ...
       FROM campaign
       WHERE campaign.name LIKE "%{campaign_name_pattern}%"
   '''
   ```

2. **HTTP API v22**: Update via REST endpoint (most reliable method)
   ```python
   headers = get_headers_with_auto_token()
   headers['login-customer-id'] = MANAGER_ID  # Critical for managed accounts

   url = f"https://googleads.googleapis.com/v22/customers/{customer_id}/campaigns:mutate"
   payload = {
       'operations': [{
           'updateMask': 'field_name',
           'update': {
               'resourceName': resource_name,
               'fieldName': new_value
           }
       }]
   }
   ```

3. **Simple Success/Failure**: Returns `True` or error message

**What Makes Them Simple**:
- No manual ID lookups required
- No complex JSON structures
- No API version conflicts
- No client-specific configurations
- Just campaign name + new value

---

## Technical Requirements

**Python Environment**:
```bash
/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-ads-mcp-server/.venv/bin/python3
```

**Dependencies**:
- MCP server OAuth (already set up)
- `~/google-ads.yaml` config (already exists)
- Manager account ID hardcoded: 2569949686 (Rok Systems MCC)

**No Setup Required** - scripts just work.

---

## Error Handling

**Campaign Not Found**:
```
❌ Campaign not found matching 'Brand Exact'
```
Fix: Check campaign name spelling or use more specific partial match

**Permission Denied (403)**:
```
❌ FAILED
403: User does not have access
```
Fix: Verify customer ID and manager account ID

**API Rate Limits**:
Scripts include automatic retry logic. Large batch operations (50+ campaigns) may take a few minutes.

---

## When NOT to Use These Scripts

**Don't use for**:
- Creating new campaigns (use Google Ads UI or MCP tools)
- Complex bulk operations (use Google Ads Editor)
- Automated scheduled changes (create dedicated agent)
- Ad copy updates (use Google Ads Text Generator skill)

**Use for**:
- Quick manual updates
- Black Friday/Sales event prep
- Budget adjustments based on performance
- Emergency pauses
- Strategy shifts (e.g., changing ROAS targets)

---

## Future Enhancements (Optional)

Could add:
- Interactive mode: "Which campaigns do you want to update?"
- Auto-detect account from campaign name
- Dry-run preview before applying
- Rollback functionality
- Scheduled changes (combine with cron/LaunchAgents)

But the current versions are probably good enough. **Simple is better.**

---

## Comparison: Old vs New

### Before (Complicated)

❌ **What we had**:
- 60+ client-specific scripts across different folders
- Each script hardcoded to one client
- Copy/paste modifications for each new operation
- Version conflicts (v17, v18, v22)
- Manual ID lookups required
- Spent 30+ minutes per task

### After (Simple)

✅ **What we have now**:
- 4 universal scripts for all clients
- Campaign name lookup (no manual IDs)
- Simple JSON format
- HTTP API v22 (proven reliable)
- Takes 30 seconds per task

**Time Saved**: Phase 1 Smythson deployment took 4 minutes instead of 30+ minutes

---

## Examples

### Example 1: Black Friday Budget Increases

**Task**: Increase budgets across 15 Smythson campaigns (4 accounts)

**Time**: 4 minutes total

**Steps**:
1. Create 4 JSON files (1 per account) - 2 minutes
2. Run script 4 times - 2 minutes
3. Verify in Google Ads UI - 30 seconds

### Example 2: Pause Underperforming Campaigns

**Task**: Pause 5 campaigns with poor ROAS

**Time**: 1 minute

**Steps**:
1. Create JSON with campaign names + `"status": "PAUSED"`
2. Run status updater
3. Done

### Example 3: ROAS Target Adjustment

**Task**: Lower ROAS targets for Q4 sales period

**Time**: 2 minutes

**Steps**:
1. Create JSON with new ROAS targets (e.g., 3.0 → 2.5)
2. Run ROAS updater
3. Monitor performance

### Example 4: Weekly Performance Export

**Task**: Export last week's performance to CSV for client report

**Time**: 30 seconds

**Steps**:
1. Run performance query with date range and `--output csv`
2. Import CSV to Google Sheets
3. Add to client report

### Example 5: Add Wastage Negatives

**Task**: Add negative keywords identified in search term audit

**Time**: 30 seconds

**Steps**:
1. Run: `python3 add-google-ads-negative-keywords.py --customer-id 8573235780 --campaign "Shopping" --keywords "cheap,free,wholesale,bulk"`
2. Done - all negatives added at campaign level

### Example 6: Pause Low-Performing Keywords

**Task**: Pause 10 keywords with poor ROAS after keyword audit

**Time**: 2 minutes

**Steps**:
1. Create JSON with campaign + keyword + status
2. Run keyword status updater
3. Monitor performance impact

---

## Related Documentation

- **HOW-TO-UPDATE-GOOGLE-ADS-BUDGETS.md** - Detailed budget update guide
- **GOOGLE-ADS-SCRIPT-IMPROVEMENTS.md** - Original improvement roadmap
- **ADDING-A-NEW-CLIENT.md** - Client onboarding (includes platform IDs)
- **CLAUDE.md** - Core development patterns

---

**Bottom line**: Use these simple scripts. Don't overthink it. They work reliably and save massive amounts of time.
