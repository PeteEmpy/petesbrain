# Weekly Email Attachment Integration Guide

**Purpose:** Add CSV attachment capability to the weekly meeting review email
**Use Case:** Automatically attach Devonshire November 2025 budget CSV when related task is present

---

## What Was Created

1. **CSV File:** `/clients/devonshire-hotels/spreadsheets/devonshire-november-2025-budgets.csv`
   - Ready to import into Google Ads Editor
   - Contains all 12 campaigns with new November budgets

2. **Helper Module:** `/shared/scripts/email_attachment_helper.py`
   - `create_message_with_attachment()` - Enhanced email creation with attachments
   - `should_attach_devonshire_budget_csv()` - Checks if Devonshire budget task exists
   - `get_devonshire_budget_csv_path()` - Returns path to CSV file

3. **Google Task:** Created with due date Nov 1, 2025

---

## How to Integrate (Option 1: Automatic)

### Step 1: Modify `weekly-meeting-review.py`

**Add import at the top (around line 15):**
```python
from email_attachment_helper import (
    create_message_with_attachment,
    should_attach_devonshire_budget_csv,
    get_devonshire_budget_csv_path
)
```

**Replace the `create_message()` call (around line 530):**

Find this section:
```python
def main():
    # ... existing code ...

    # Create and send email
    message_body = create_message(
        to='petere@roksys.co.uk',
        subject=subject,
        html_content=html
    )
```

**Replace with:**
```python
def main():
    # ... existing code ...

    # Check if we should attach Devonshire budget CSV
    attachments = []
    if should_attach_devonshire_budget_csv(completed_tasks + [task for task in tasks if not task.get('completed')]):
        csv_path = get_devonshire_budget_csv_path()
        if csv_path:
            attachments.append(str(csv_path))
            print(f"📎 Will attach: {csv_path.name}")

    # Create and send email
    message_body = create_message_with_attachment(
        to='petere@roksys.co.uk',
        subject=subject,
        html_content=html,
        attachments=attachments if attachments else None
    )
```

---

## How to Integrate (Option 2: Manual - Simpler)

If you prefer a simpler approach without modifying the script:

### Just Attach Manually

The CSV is ready at:
```
/Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/spreadsheets/devonshire-november-2025-budgets.csv
```

**When you receive the Monday email:**
1. Forward it to yourself with the CSV attached
2. Or download the CSV separately and use it on Nov 1st

---

## How to Use the CSV in Google Ads Editor

### Step 1: Open Google Ads Editor
- Launch Google Ads Editor
- Select Devonshire Hotels account

### Step 2: Import the CSV
1. Go to **Account** → **Import** → **From file**
2. Browse and select: `devonshire-november-2025-budgets.csv`
3. Click **Import**

### Step 3: Review Changes
- Google Ads Editor will show all 12 budget changes
- Review each campaign to ensure correct amounts
- Column format:
  - Campaign name (exact match)
  - New budget amount (daily)
  - Action: "Set" (replaces existing budget)

### Step 4: Apply Changes
1. Click **Review changes** button
2. Verify all 12 campaigns are listed
3. Click **Post** to send to Google Ads
4. Wait for confirmation

### Alternative: Manual Import Process

If automatic import doesn't work:

1. **In Google Ads Editor:**
   - Go to **Campaigns** tab
   - Filter: Show only enabled campaigns
   - Filter: Campaign name contains "DEV | Properties"

2. **Update budgets manually:**
   - Select each campaign
   - Edit budget field
   - Use the values from the CSV

---

## CSV File Format Explained

```csv
Campaign,Budget,Action
DEV | Properties BE | Devonshire Arms Hotel...,48,Set
...
```

**Columns:**
- **Campaign:** Exact campaign name from Google Ads
- **Budget:** New daily budget in GBP (no currency symbol)
- **Action:** "Set" (overwrites existing budget)

**Important:**
- Campaign names must match EXACTLY (including spaces, pipes, numbers)
- Budget is daily amount, not monthly
- Currency is GBP (Google Ads Editor should auto-detect from account)

---

## Testing the Integration

### Test the Helper Functions

```bash
cd /Users/administrator/Documents/PetesBrain/shared/scripts
python3 -c "
from email_attachment_helper import *

# Test CSV path detection
csv_path = get_devonshire_budget_csv_path()
print(f'CSV found: {csv_path}')

# Test task detection
test_tasks = [
    {'title': 'Implement November 2025 Budget Changes - Devonshire Hotels'}
]
should_attach = should_attach_devonshire_budget_csv(test_tasks)
print(f'Should attach: {should_attach}')
"
```

Expected output:
```
CSV found: /Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/spreadsheets/devonshire-november-2025-budgets.csv
Should attach: True
```

### Test the Weekly Email Script

```bash
# Dry run (add --dry-run flag if available)
GOOGLE_APPLICATION_CREDENTIALS=shared/email-sync/credentials.json \
  shared/email-sync/.venv/bin/python3 shared/scripts/weekly-meeting-review.py
```

Check the output for:
```
📎 Will attach: devonshire-november-2025-budgets.csv
Attached: devonshire-november-2025-budgets.csv
Email sent successfully
```

---

## Benefits of CSV Import

✅ **Faster:** 12 budget changes in ~2 minutes vs 15 minutes manual
✅ **Accurate:** No typos or wrong values
✅ **Reviewable:** See all changes in Editor before posting
✅ **Auditable:** CSV file serves as record of what was changed
✅ **Repeatable:** Can re-import if needed

---

## Troubleshooting

### "Campaign not found" in Google Ads Editor

**Cause:** Campaign name doesn't match exactly

**Fix:**
1. In Google Ads Editor, copy the exact campaign name
2. Update the CSV file with the correct name
3. Re-import

### CSV Won't Import

**Cause:** Format issue or wrong file type

**Fix:**
1. Ensure file is saved as `.csv` (not `.xlsx` or `.txt`)
2. Open in text editor to verify format
3. Should show comma-separated values, no quotes around campaign names

### Email Attachment Doesn't Appear

**Cause:** Integration not completed or CSV path wrong

**Fix:**
1. Check if `email_attachment_helper.py` is in correct location
2. Verify CSV path exists
3. Check script output for error messages

---

## Alternative Approach: Google Sheets Import

If CSV import to Google Ads Editor doesn't work well, you can also:

1. **Upload CSV to Google Sheets**
2. **Open in Google Sheets** (auto-converts to spreadsheet)
3. **Copy values** from Sheet
4. **Paste into Google Ads Editor** bulk edit window

---

## Maintenance

### For Future Budget Changes

1. **Create new CSV** with updated values
2. **Update task title** to include the month/year
3. **Update helper function** `should_attach_devonshire_budget_csv()` if needed
4. **CSV filename pattern:** `devonshire-{month}-{year}-budgets.csv`

### Remove Old CSVs

After November 1st, you can archive or delete:
```
devonshire-november-2025-budgets.csv
```

---

## Summary

**Created:**
- ✅ CSV file with 12 budget changes
- ✅ Helper module for email attachments
- ✅ Google Task with due date Nov 1
- ✅ Integration guide (this document)

**Next Steps:**
1. Choose integration approach (automatic or manual)
2. If automatic: Modify `weekly-meeting-review.py` as shown above
3. If manual: Just use the CSV file directly on Nov 1
4. Test the CSV import in Google Ads Editor beforehand

**Recommended:** Try the CSV import in Google Ads Editor NOW (before Nov 1) with a test campaign to ensure the format works!

---

**Created:** 2025-10-30
**For:** Weekly meeting review email enhancement
**Contact:** Peter Empson - petere@roksys.co.uk
