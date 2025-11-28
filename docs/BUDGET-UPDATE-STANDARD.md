# Budget Update Standard - Google Ads API

**Created:** 2025-11-20
**Status:** ✅ Active Standard
**Pattern Source:** `pause-keywords.py` methodology

---

## Overview

Standardized approach for updating Google Ads campaign budgets via API. Replaces manual CSV imports with automated, logged API updates.

## The Standard Tool

**Location:** `shared/scripts/update-campaign-budgets.py`

**Features:**
- ✅ Google Ads API v18 with MCP oauth authentication
- ✅ Dry-run mode for safe previewing
- ✅ JSON-based configuration (reusable, version-controllable)
- ✅ Detailed logging and error handling
- ✅ Confirmation prompts for safety
- ✅ Batch updates (multiple campaigns at once)

---

## Quick Start

### 1. Create Changes JSON

```json
[
  {
    "campaign_id": "12345",
    "budget_id": "67890",
    "new_daily_budget": 100.00,
    "campaign_name": "Campaign Name",
    "reason": "Reason for change"
  }
]
```

### 2. Preview Changes (Dry Run)

```bash
python3 shared/scripts/update-campaign-budgets.py \
  --customer-id CUSTOMER_ID \
  --changes changes.json \
  --dry-run
```

### 3. Apply Changes

```bash
python3 shared/scripts/update-campaign-budgets.py \
  --customer-id CUSTOMER_ID \
  --changes changes.json
```

---

## When to Use This Approach

**Use the standardized script when:**
- ✅ Making budget changes for ANY client
- ✅ Need audit trail (JSON files are version-controllable)
- ✅ Multiple campaigns being updated at once
- ✅ Want to preview changes before applying (dry-run)
- ✅ Need to document reason for changes

**Alternative approaches:**
- ❌ Manual Google Ads UI: Slow, no audit trail, error-prone
- ❌ Google Ads Editor CSV: Extra step, no automation, manual import
- ⚠️ MCP direct tool calls: Good for one-off, but harder to document/replay

---

## Pattern Consistency

This tool follows the **same pattern** as other Google Ads utilities:

| Tool | Purpose | Pattern |
|------|---------|---------|
| `pause-keywords.py` | Pause keywords | MCP oauth + API + JSON config |
| `update-campaign-budgets.py` | Update budgets | **Same pattern** ✅ |
| Future tools... | Other operations | **Same pattern** ✅ |

**Benefits:**
- Consistent authentication approach
- Same error handling patterns
- Familiar usage for all Google Ads operations
- Easy to maintain and extend

---

## Real-World Examples

### Devonshire Hotels - Nov 20, 2025

**Scenario:** Restore client-approved budgets, deploy remaining budget to top performers

**Changes File:** `clients/devonshire-hotels/scripts/devonshire-budget-changes-nov-20.json`

```json
[
  {
    "campaign_id": "19577006833",
    "budget_id": "12288076740",
    "new_daily_budget": 100.00,
    "campaign_name": "Dev Arms Hotel",
    "reason": "Restore £52 approved + deploy £48 additional (850% ROAS)"
  },
  {
    "campaign_id": "22666031909",
    "budget_id": "14649374763",
    "new_daily_budget": 26.00,
    "campaign_name": "The Fell",
    "reason": "Restore to client-approved budget (Nov 13)"
  }
]
```

**Execute:**
```bash
python3 shared/scripts/update-campaign-budgets.py \
  --customer-id 5898250490 \
  --changes clients/devonshire-hotels/scripts/devonshire-budget-changes-nov-20.json
```

### Superspace - Nov 20, 2025

**Scenario:** Deploy underspent budget to high-ROAS campaigns

**Changes File:** `clients/superspace/scripts/superspace-budget-changes-nov-20.json`

```json
[
  {
    "campaign_id": "19675367886",
    "budget_id": "12349631912",
    "new_daily_budget": 150.00,
    "campaign_name": "UK Search Generics",
    "reason": "1,079% ROAS, 77% budget-constrained"
  },
  {
    "campaign_id": "21830614241",
    "budget_id": "14021956507",
    "new_daily_budget": 200.00,
    "campaign_name": "UK Shopping All",
    "reason": "2,081% ROAS, 61% budget-constrained"
  }
]
```

---

## Complete Workflow

### Step 1: Analysis

Analyse current budgets and identify opportunities:
```bash
# Query current budgets
mcp__google-ads__run_gaql(
    customer_id="CUSTOMER_ID",
    query="""
        SELECT campaign.id, campaign.name, campaign_budget.id,
               campaign_budget.amount_micros, metrics.cost_micros,
               metrics.conversions_value, metrics.search_budget_lost_impression_share
        FROM campaign
        WHERE segments.date DURING THIS_MONTH
    """
)
```

### Step 2: Create Changes JSON

Document planned changes with budget IDs and rationale.

### Step 3: Dry Run

Preview changes to verify correctness:
```bash
python3 shared/scripts/update-campaign-budgets.py \
  --customer-id CUSTOMER_ID \
  --changes changes.json \
  --dry-run
```

### Step 4: Apply Changes

Execute with confirmation prompt:
```bash
python3 shared/scripts/update-campaign-budgets.py \
  --customer-id CUSTOMER_ID \
  --changes changes.json
```

### Step 5: Document

Log to experiment tracker and tasks-completed.md:

**Experiment Tracker:**
```bash
echo "$(date +%d/%m/%Y %H:%M),Client Name,\"Budget changes: [summary]. Reason: [rationale]. Expected impact: [projections].\"" >> roksys/spreadsheets/rok-experiments-client-notes.csv
```

**Tasks Completed:**
```markdown
## Budget Optimization - [Date]
**Completed:** YYYY-MM-DD HH:MM
**Source:** Manual completion (API budget update)

[Detailed notes about changes and expected impact]

---
```

### Step 6: Monitor

Track impact over next 3-7 days to verify expected results.

---

## Best Practices

### 1. Always Version Control Changes JSON

```bash
# Save changes file in client scripts directory
clients/[client-name]/scripts/budget-changes-YYYY-MM-DD.json

# Commit to git for audit trail
git add clients/[client-name]/scripts/budget-changes-YYYY-MM-DD.json
git commit -m "[client-name]: Document budget changes YYYY-MM-DD"
```

### 2. Include Comprehensive Reasons

**Good:**
```json
{
  "reason": "850% ROAS, 44% budget-constrained, top performer. Restore £52 approved (Nov 13) + deploy £48 additional from underspend."
}
```

**Bad:**
```json
{
  "reason": "Increase budget"
}
```

### 3. Dry Run First, Always

```bash
# ALWAYS preview before applying
--dry-run

# Only remove flag after verifying output
```

### 4. Document Expected Impact

In changes JSON or accompanying analysis document:
- Expected revenue increase/decrease
- ROAS projections
- Budget utilization targets
- Review date

### 5. Log to Multiple Places

1. **Changes JSON** (version controlled)
2. **Experiment tracker** (rok-experiments-client-notes.csv)
3. **Tasks completed** (clients/[client]/tasks-completed.md)
4. **CONTEXT.md** (if significant strategic change)

---

## Authentication

Uses **MCP server oauth** module:
- **No separate setup required**
- **Auto-refreshes tokens**
- **Same credentials** as other MCP tools
- **Location:** `infrastructure/mcp-servers/google-ads-mcp-server/oauth/`

---

## Troubleshooting

### Error: "Resource not found"
**Cause:** Invalid budget_id
**Fix:** Re-query campaign_budget.id via GAQL

### Error: "Permission denied"
**Cause:** Wrong customer ID or credentials issue
**Fix:** Verify customer_id, check MCP credentials

### Error: "Invalid JSON"
**Cause:** Malformed changes.json
**Fix:** Validate with `jq` or online JSON validator

### Script hangs on confirmation
**Cause:** Waiting for user input
**Fix:** Type "yes" or "y" to confirm, or Ctrl+C to cancel

---

## Future Enhancements

Potential additions to standardized approach:

1. **Rollback functionality**
   - Save pre-change budgets
   - Quick rollback command if issues

2. **Schedule changes**
   - Apply budget changes at specific time
   - Useful for time-zone specific optimizations

3. **Budget ramping**
   - Gradual budget increases over days
   - Safer for large changes

4. **Impact tracking**
   - Auto-generate comparison reports
   - Before/after performance analysis

---

## Summary

**Before (Nov 2025):**
- ❌ Manual Google Ads Editor CSV imports
- ❌ No consistent audit trail
- ❌ Difficult to replay or rollback
- ❌ Error-prone manual entry

**After (Nov 2025):**
- ✅ Standardized API-based approach
- ✅ Version-controlled JSON configs
- ✅ Dry-run for safety
- ✅ Comprehensive logging
- ✅ Consistent with other Google Ads tools
- ✅ Easy to replay and document

---

**Documentation:**
- **Tool:** `shared/scripts/update-campaign-budgets.py`
- **README:** `shared/scripts/UPDATE-CAMPAIGN-BUDGETS-README.md`
- **Example:** `shared/scripts/update-campaign-budgets-example.json`

**Created:** 2025-11-20
**Author:** Peter Empson
**Pattern:** Based on `pause-keywords.py` methodology
