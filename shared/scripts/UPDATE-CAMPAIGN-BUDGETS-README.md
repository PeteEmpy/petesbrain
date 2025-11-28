# Update Campaign Budgets - Standard Utility

**Location:** `shared/scripts/update-campaign-budgets.py`

## Purpose

Standardized tool for updating Google Ads campaign budgets via API. Uses the same authentication pattern as other Google Ads utilities (pause-keywords, etc.).

## Usage

### Basic Usage

```bash
python3 shared/scripts/update-campaign-budgets.py \
  --customer-id CUSTOMER_ID \
  --changes changes.json
```

### Dry Run (Preview Changes)

```bash
python3 shared/scripts/update-campaign-budgets.py \
  --customer-id CUSTOMER_ID \
  --changes changes.json \
  --dry-run
```

### Verbose Output

```bash
python3 shared/scripts/update-campaign-budgets.py \
  --customer-id CUSTOMER_ID \
  --changes changes.json \
  --verbose
```

---

## Changes JSON Format

```json
[
  {
    "campaign_id": "12345",
    "budget_id": "67890",
    "new_daily_budget": 100.00,
    "campaign_name": "Optional: Campaign Name",
    "reason": "Optional: Reason for change"
  }
]
```

**Required Fields:**
- `campaign_id`: Google Ads campaign ID
- `budget_id`: Campaign budget ID (get via GAQL query)
- `new_daily_budget`: New daily budget in pounds (e.g., 100.00)

**Optional Fields:**
- `campaign_name`: Campaign name for logging/display
- `reason`: Reason for budget change (for documentation)

---

## How to Get Budget IDs

Use GAQL query to fetch campaign and budget IDs:

```sql
SELECT
  campaign.id,
  campaign.name,
  campaign_budget.id,
  campaign_budget.amount_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
```

Via MCP tool:
```python
mcp__google-ads__run_gaql(
    customer_id="CUSTOMER_ID",
    query="SELECT campaign.id, campaign.name, campaign_budget.id FROM campaign"
)
```

---

## Example Workflow

### 1. Query Current Budgets

```bash
# Get current budgets and IDs
python3 -c "
from mcp__google_ads import run_gaql
result = run_gaql(
    customer_id='5898250490',
    query='''
        SELECT campaign.id, campaign.name, campaign_budget.id,
               campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.status = \"ENABLED\"
    '''
)
print(result)
"
```

### 2. Create Changes JSON

Create `budget-changes.json`:
```json
[
  {
    "campaign_id": "18899261254",
    "budget_id": "11945680219",
    "new_daily_budget": 50.00,
    "campaign_name": "Performance Max All",
    "reason": "Increase for peak season"
  }
]
```

### 3. Preview Changes (Dry Run)

```bash
python3 shared/scripts/update-campaign-budgets.py \
  --customer-id 5898250490 \
  --changes budget-changes.json \
  --dry-run
```

### 4. Apply Changes

```bash
python3 shared/scripts/update-campaign-budgets.py \
  --customer-id 5898250490 \
  --changes budget-changes.json
```

Script will ask for confirmation before applying.

---

## Real-World Example: Devonshire Hotels Nov 20

**Scenario:** Restore client-approved budgets and deploy remaining budget

**File:** `clients/devonshire-hotels/scripts/devonshire-budget-changes-nov-20.json`

```json
[
  {
    "campaign_id": "19577006833",
    "budget_id": "12288076740",
    "new_daily_budget": 100.00,
    "campaign_name": "Dev Arms Hotel",
    "reason": "Restore £52 approved + deploy £48 additional (850% ROAS top performer)"
  },
  {
    "campaign_id": "22666031909",
    "budget_id": "14649374763",
    "new_daily_budget": 26.00,
    "campaign_name": "The Fell",
    "reason": "Restore to client-approved budget (Nov 13 approval)"
  },
  {
    "campaign_id": "21839323410",
    "budget_id": "14032878235",
    "new_daily_budget": 48.00,
    "campaign_name": "Cavendish",
    "reason": "Restore to client-approved budget"
  }
]
```

**Execute:**
```bash
cd /Users/administrator/Documents/PetesBrain

python3 shared/scripts/update-campaign-budgets.py \
  --customer-id 5898250490 \
  --changes clients/devonshire-hotels/scripts/devonshire-budget-changes-nov-20.json
```

---

## Authentication

Uses MCP server's oauth module for authentication:
- **Location:** `infrastructure/mcp-servers/google-ads-mcp-server/oauth/google_auth.py`
- **Method:** `get_headers_with_auto_token()` - auto-refreshes tokens
- **Pattern:** Same as `pause-keywords.py` and other Google Ads utilities

No separate authentication setup required - uses existing MCP credentials.

---

## Error Handling

**Common Errors:**

1. **Invalid Budget ID**
   - Error: "Resource not found"
   - Fix: Re-query campaign_budget.id via GAQL

2. **Permission Denied**
   - Error: "User doesn't have permission to access customer"
   - Fix: Check customer ID and MCP credentials

3. **Invalid Budget Amount**
   - Error: "Budget amount must be positive"
   - Fix: Ensure new_daily_budget > 0

4. **JSON Format Error**
   - Error: "Invalid JSON"
   - Fix: Validate JSON syntax (use `jq` or online validator)

---

## Best Practices

1. **Always dry-run first**
   ```bash
   --dry-run  # Preview changes before applying
   ```

2. **Document reasons**
   - Include `reason` field in JSON for audit trail
   - Helps with month-end reporting

3. **Backup current budgets**
   - Query and save current state before changes
   - Allows rollback if needed

4. **Batch related changes**
   - Group all budget changes for one client in single JSON file
   - One execution, consistent timestamp

5. **Log to experiment tracker**
   - After budget changes, log to `rok-experiments-client-notes.csv`
   - Enables impact analysis

---

## Integration with Workflows

### Log to Experiment Tracker

After applying budget changes:

```bash
# Add to rok-experiments-client-notes.csv
echo "$(date +%d/%m/%Y %H:%M),Devonshire Hotels,\"Budget changes applied: Dev Arms £36→£100/day (+£64), The Fell £22→£26/day (+£4), Cavendish £50→£48/day (-£2). Reason: Restore approved budgets + deploy remaining £660 to top performer (850% ROAS).\"" >> roksys/spreadsheets/rok-experiments-client-notes.csv
```

### Log to tasks-completed.md

```markdown
## Budget Optimization - November 2025
**Completed:** 2025-11-20 10:30
**Source:** Manual completion (API budget update)

Updated campaign budgets for November based on performance analysis:
- Dev Arms Hotel: £36 → £100/day (+£64) - 850% ROAS, 44% budget-constrained
- The Fell: £22 → £26/day (+£4) - Restore client-approved budget (Nov 13)
- Cavendish: £50 → £48/day (-£2) - Restore client-approved budget
- P Max All: £48 → £36/day (-£12) - Reduce underperformer (397% ROAS)
- Chatsworth Inns: £22 → £15/day (-£7) - Reduce critical underperformer (140% ROAS)

Expected Impact: +£7,117 additional revenue over remaining 10 days

Implementation: Google Ads API via shared/scripts/update-campaign-budgets.py

---
```

---

## See Also

- **Pause Keywords:** `clients/*/scripts/pause-keywords.py` - Similar pattern for keyword operations
- **MCP OAuth:** `infrastructure/mcp-servers/google-ads-mcp-server/oauth/google_auth.py`
- **GAQL Reference:** https://developers.google.com/google-ads/api/fields/v18/campaign

---

**Created:** 2025-11-20
**Author:** Peter Empson
**Pattern Source:** `pause-keywords.py` methodology
