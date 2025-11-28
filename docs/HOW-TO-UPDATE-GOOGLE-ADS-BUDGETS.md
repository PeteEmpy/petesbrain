# How to Update Google Ads Campaign Budgets

**TL;DR**: Use the simple shared script. One command. Done.

---

## Single Campaign Update

```bash
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/update-google-ads-budgets.py \
  --customer-id 8573235780 \
  --campaign "Brand Exact" \
  --budget 1500
```

**That's it.** The script:
1. Finds the campaign by name (partial match OK)
2. Shows current vs new budget
3. Updates it
4. Confirms success

---

## Multiple Campaigns (Batch Update)

### Step 1: Create simple JSON file

```json
[
  {"campaign": "Brand Exact", "new_daily_budget": 1500},
  {"campaign": "P Max H&S", "new_daily_budget": 600},
  {"campaign": "Shopping", "new_daily_budget": 700}
]
```

### Step 2: Run it

```bash
python3 /Users/administrator/Documents/PetesBrain/shared/scripts/update-google-ads-budgets.py \
  --customer-id 8573235780 \
  --file budgets.json
```

Done. All campaigns updated.

---

## Smythson Multi-Account Updates

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

---

## Account IDs (Common Clients)

| Client | Account ID | Notes |
|--------|------------|-------|
| **Smythson UK** | 8573235780 | Main UK market |
| **Smythson USA** | 7808690871 | US market |
| **Smythson EUR** | 7679616761 | European markets |
| **Smythson ROW** | 5556710725 | Rest of world |
| **Devonshire** | 5898250490 | Single account |
| **Superspace** | 7482100090 | Single account |

Find more: Check `clients/{client}/CONTEXT.md` under "Platform IDs"

---

## Campaign Name Matching

The script uses **partial matching**, so you don't need exact names:

- `"Brand Exact"` finds `"SMY | UK | Search | Brand Exact"`
- `"H&S Christmas"` finds `"SMY | UK | P Max | H&S Christmas Gifting"`
- `"Shopping"` finds any campaign with "Shopping" in the name

**Tip**: Use unique parts of the campaign name to avoid ambiguity.

---

## JSON Format (Simple)

Minimal required fields:

```json
[
  {
    "campaign": "partial campaign name",
    "new_daily_budget": 123.45
  }
]
```

You can also use `campaign_name` instead of `campaign` - both work.

---

## What Went Wrong Before

❌ **What I did** (complicated):
1. Tried to use non-existent MCP tools
2. Created 5+ different scripts with version conflicts
3. Manually queried for campaign IDs and budget IDs
4. Built complex JSON with campaign_id, budget_id, etc.
5. Spent 30+ minutes fighting API versions

✅ **What actually works** (simple):
1. One script that does everything
2. Just give it campaign name + new budget
3. Script finds IDs automatically
4. Uses proven HTTP API approach
5. Takes 30 seconds

---

## Future Improvements (Optional)

Could add:
- Interactive mode: "Which campaigns do you want to update?"
- Auto-detect account from campaign name
- Dry-run preview before applying
- Rollback functionality

But honestly, the current version is probably good enough. Simple is better.

---

## The Script Location

**Path**: `/Users/administrator/Documents/PetesBrain/shared/scripts/update-google-ads-budgets.py`

**What it needs**:
- MCP server OAuth (already set up)
- `~/google-ads.yaml` config (already exists)
- Manager account ID hardcoded: 2569949686 (Rok Systems MCC)

**No setup required** - it just works.

---

## Example: Full Smythson Phase 1 (Simplified)

Instead of what I did (30+ minutes, 5 scripts), here's how it SHOULD have been:

### 1. Create one JSON file per account (2 minutes)

`uk.json`:
```json
[
  {"campaign": "Brand Exact", "new_daily_budget": 1450},
  {"campaign": "H&S Christmas", "new_daily_budget": 650},
  {"campaign": "P Max | H&S", "new_daily_budget": 540},
  {"campaign": "Briefcases", "new_daily_budget": 420},
  {"campaign": "Shopping | H&S", "new_daily_budget": 650},
  {"campaign": "Semi Brand - Diaries", "new_daily_budget": 350}
]
```

### 2. Run 4 commands (2 minutes)

```bash
cd /Users/administrator/Documents/PetesBrain/clients/smythson/scripts

python3 ../../shared/scripts/update-google-ads-budgets.py --customer-id 8573235780 --file uk.json
python3 ../../shared/scripts/update-google-ads-budgets.py --customer-id 7808690871 --file usa.json
python3 ../../shared/scripts/update-google-ads-budgets.py --customer-id 7679616761 --file eur.json
python3 ../../shared/scripts/update-google-ads-budgets.py --customer-id 5556710725 --file row.json
```

**Total time: 4 minutes instead of 30+ minutes.**

---

**Bottom line**: Use the simple script. Don't overthink it.
