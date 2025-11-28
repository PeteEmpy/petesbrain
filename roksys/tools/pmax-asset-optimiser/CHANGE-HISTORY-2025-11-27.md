# Google Ads Change History - 2025-11-27
**Customer:** Tree2mydoor (4941701449)
**Campaign:** T2MD | P Max | HP&P 150 5/9 140 23/10 (15820346778)
**Asset Group:** Olive Tree Competitors (6519856317)

---

## Summary of Changes

**Total Changes Today:** 4
- 3 × Asset CREATE operations
- 1 × Campaign Budget UPDATE operation

**All changes made by:** petere@roksys.co.uk

---

## Asset Changes in Asset Group 6519856317 (Olive Tree Competitors)

### Change 1: Long Headline Added
**Timestamp:** 2025-11-27 10:05:45
**Operation:** CREATE
**Asset ID:** 312332933791
**Field Type:** LONG_HEADLINE
**Text:** "Premium Olive Trees - Perfect For Patios - Gift Wrapped With Next Day Delivery"

**Context:** Created during morning test execution

---

### Change 2: Description Added
**Timestamp:** 2025-11-27 10:05:46
**Operation:** CREATE
**Asset ID:** 312332899219
**Field Type:** DESCRIPTION
**Text:** "Authentic olive trees delivered next day - perfect for Mediterranean garden vibes"

**Context:** Created during morning test execution (1 second after previous)

---

### Change 3: Long Headline Added
**Timestamp:** 2025-11-27 12:24:32
**Operation:** CREATE
**Asset ID:** 312353453677
**Field Type:** LONG_HEADLINE
**Text:** "Authentic Mediterranean Olive Trees For Patios - Gift Wrapped With Personal Cards"

**Context:** Created during afternoon dry-run test (that actually executed)

---

## Other Changes

### Campaign Budget Update
**Timestamp:** 2025-11-27 11:33:09
**Operation:** UPDATE
**Resource:** customers/4941701449/campaignBudgets/10174280533
**User:** petere@roksys.co.uk

**Context:** Budget adjustment made between test runs

---

## Current Asset Group State

**Asset Group:** 6519856317 (Olive Tree Competitors)
**Campaign:** T2MD | P Max | HP&P 150 5/9 140 23/10

### Current Long Headlines (5/5 - at maximum)
1. "Our Unique Living Gifts Make A Perfect Present For Any Occasion - Take A Look" (41583396096)
2. "Sustainable & Ethical, Olive Trees Make The Perfect Present - Come And Look" (60317720054)
3. "All Our Olive Trees Are Packed With Love & Care and Presented In A Jute Bag or Gift Wrap" (60317720060)
4. **"Premium Olive Trees - Perfect For Patios - Gift Wrapped With Next Day Delivery"** (312332933791) ← **NEW**
5. **"Authentic Mediterranean Olive Trees For Patios - Gift Wrapped With Personal Cards"** (312353453677) ← **NEW**

### Current Descriptions (5/5 - at maximum)
1. (Existing descriptions - 4 original)
2. **"Authentic olive trees delivered next day - perfect for Mediterranean garden vibes"** (312332899219) ← **NEW**

---

## Execution Timeline

**10:05 AM** - Morning test execution
- Created 2 new assets (1 long headline, 1 description)
- Part of initial testing after bug fix

**11:33 AM** - Budget update
- Manual budget adjustment

**12:24 PM** - Afternoon test execution
- Created 1 new long headline
- This was during a "dry-run" that actually executed

---

## Verification in Google Ads UI

To view these changes in Google Ads:

1. Go to Google Ads UI → Tools (wrench icon)
2. Click "Change history" under Setup
3. Filter by:
   - **Date:** 2025-11-27
   - **Campaign:** T2MD | P Max | HP&P 150 5/9 140 23/10
   - **Change type:** Asset groups

You will see entries showing:
- Asset created (with Asset ID)
- Asset linked to asset group
- User email (petere@roksys.co.uk)
- Exact timestamps

---

## Testing Context

These changes were made during end-to-end testing of the PMAX Asset Optimizer system after fixing a critical bug where the execution engine was targeting wrong asset groups.

**Bug Fixed:** System now uses Asset_Group_ID from CSV instead of searching by text
**Result:** All 3 assets correctly added to Asset Group 6519856317 (Olive Tree Competitors)

**Execution Logs Available:**
- `logs/execution-report-dry-run-2025-11-27_10-05-48.json`
- `logs/execution-report-live-2025-11-27_10-17-14.json` (wrong group - reverted)
- `logs/execution-report-dry-run-2025-11-27_10-38-34.json`
- `logs/execution-report-dry-run-2025-11-27_12-24-33.json`
- `logs/execution-report-live-2025-11-27_12-25-35.json`

---

## API Query Used

```sql
SELECT
    change_event.change_date_time,
    change_event.resource_change_operation,
    change_event.user_email,
    change_event.change_resource_name
FROM change_event
WHERE change_event.change_date_time >= '2025-11-27 00:00:00'
AND change_event.change_date_time <= '2025-11-27 23:59:59'
ORDER BY change_event.change_date_time DESC
LIMIT 200
```

---

## Scripts for Future Change Queries

**Universal change history script:** `query_google_ads_changes.py`

**Usage examples:**
```bash
# All changes today
python3 query_google_ads_changes.py --customer-id 4941701449

# Asset changes in last 7 days
python3 query_google_ads_changes.py --customer-id 4941701449 --days 7 --resource-type asset

# Only CREATE operations
python3 query_google_ads_changes.py --customer-id 4941701449 --operation CREATE
```

---

**Document Created:** 2025-11-27
**Created By:** PetesBrain AI Assistant
**Purpose:** Complete audit trail of today's Google Ads changes during PMAX Asset Optimizer testing
