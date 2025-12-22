# P9 Bulletproof Implementation Guide - Google Ads Rules

**Created:** December 19, 2025
**Purpose:** Failsafe implementation of P9 budget changes using Google Ads automated rules

---

## 🎯 MOST BULLETPROOF METHOD: Google Ads Automated Rules

### Why This Is The Best Approach:
✅ Runs automatically even if you're not logged in
✅ Can be set up and tested days in advance
✅ Native to Google Ads (no external dependencies)
✅ Has built-in logging of all changes
✅ Can be paused/edited if plans change
✅ Works at account level (changes all campaigns)

---

## Step-by-Step Setup Guide

### STEP 1: Create Account-Level Budget Rules (Dec 20-21)

**For EACH account (UK, USA, EUR, ROW):**

1. **Navigate to:** Tools & Settings → Bulk Actions → Rules
2. **Click:** + New Rule → Campaign rules
3. **Select:** "Change budgets"

### STEP 2: Create Rules for Each Date

You'll need **7 rules per account** (28 total). Here's the template:

#### Rule 1: December 22 Reduction
```
Name: P9 - Dec 22 - Set to £650 (UK)
Frequency: Once
Date: Dec 22, 2025 at 00:01
Action: Set budget to £650
Apply to: All enabled campaigns
```

#### Rule 2: December 23 Increase
```
Name: P9 - Dec 23 - Set to £860 (UK)
Frequency: Once
Date: Dec 23, 2025 at 00:01
Action: Set budget to £860
Apply to: All enabled campaigns
```

#### Rule 3: December 24 Sale Launch (CRITICAL)
```
Name: P9 - Dec 24 - SALE LAUNCH - Set to £1,505 (UK)
Frequency: Once
Date: Dec 24, 2025 at 17:45 (5:45 PM)
Action: Set budget to £1,505
Apply to: All enabled campaigns
Email notification: YES ✅
```

#### Rule 4-7: Continue pattern for Dec 25-28

---

## Complete Rules Table by Account

### UK Account (8573235780)

| Rule # | Name | Date & Time | Action | Amount |
|--------|------|-------------|--------|--------|
| 1 | P9-Dec22-UK | Dec 22 00:01 | Set budget | £650 |
| 2 | P9-Dec23-UK | Dec 23 00:01 | Set budget | £860 |
| 3 | P9-Dec24-SALE-UK | Dec 24 17:45 | Set budget | £1,505 |
| 4 | P9-Dec25-UK | Dec 25 00:01 | Set budget | £2,900 |
| 5 | P9-Dec26-BOXING-UK | Dec 26 00:01 | Set budget | £5,000 |
| 6 | P9-Dec27-UK | Dec 27 00:01 | Set budget | £5,880 |
| 7 | P9-Dec28-UK | Dec 28 00:01 | Set budget | £5,670 |

### USA Account (7808690871)

| Rule # | Name | Date & Time | Action | Amount |
|--------|------|-------------|--------|--------|
| 1 | P9-Dec22-USA | Dec 22 00:01 | Set budget | £465 |
| 2 | P9-Dec23-USA | Dec 23 00:01 | Set budget | £620 |
| 3 | P9-Dec24-SALE-USA | Dec 24 17:45 | Set budget | £1,085 |
| 4 | P9-Dec25-USA | Dec 25 00:01 | Set budget | £2,089 |
| 5 | P9-Dec26-BOXING-USA | Dec 26 00:01 | Set budget | £3,800 |
| 6 | P9-Dec27-USA | Dec 27 00:01 | Set budget | £4,480 |
| 7 | P9-Dec28-USA | Dec 28 00:01 | Set budget | £4,320 |

### EUR Account (7679616761)

| Rule # | Name | Date & Time | Action | Amount |
|--------|------|-------------|--------|--------|
| 1 | P9-Dec22-EUR | Dec 22 00:01 | Set budget | £270 |
| 2 | P9-Dec23-EUR | Dec 23 00:01 | Set budget | £360 |
| 3 | P9-Dec24-SALE-EUR | Dec 24 17:45 | Set budget | £630 |
| 4 | P9-Dec25-EUR | Dec 25 00:01 | Set budget | £1,213 |
| 5 | P9-Dec26-BOXING-EUR | Dec 26 00:01 | Set budget | £2,500 |
| 6 | P9-Dec27-EUR | Dec 27 00:01 | Set budget | £2,940 |
| 7 | P9-Dec28-EUR | Dec 28 00:01 | Set budget | £2,835 |

### ROW Account (5556710725)

| Rule # | Name | Date & Time | Action | Amount |
|--------|------|-------------|--------|--------|
| 1 | P9-Dec22-ROW | Dec 22 00:01 | Set budget | £115 |
| 2 | P9-Dec23-ROW | Dec 23 00:01 | Set budget | £160 |
| 3 | P9-Dec24-SALE-ROW | Dec 24 17:45 | Set budget | £280 |
| 4 | P9-Dec25-ROW | Dec 25 00:01 | Set budget | £537 |
| 5 | P9-Dec26-BOXING-ROW | Dec 26 00:01 | Set budget | £700 |
| 6 | P9-Dec27-ROW | Dec 27 00:01 | Set budget | £700 |
| 7 | P9-Dec28-ROW | Dec 28 00:01 | Set budget | £675 |

---

## Alternative Method: Campaign-Level Rules

If accounts have different budgets per campaign:

### Option A: Percentage-Based Rules
Instead of "Set budget to £X", use:
- "Increase budget by 75%" (for Dec 24 sale launch)
- "Increase budget by 93%" (for Dec 25)
- "Increase budget by 78%" (for Dec 26)

### Option B: Google Ads Editor + Scripts
1. **Google Ads Editor:** Prepare all changes offline
2. **Google Ads Scripts:** Schedule the uploads

```javascript
// Example Google Ads Script for Dec 24
function main() {
  var currentHour = new Date().getHours();

  if (currentHour >= 18) { // 6pm or later
    // UK Account
    var ukCampaigns = AdsApp.campaigns()
      .withCondition("Status = ENABLED")
      .get();

    while (ukCampaigns.hasNext()) {
      var campaign = ukCampaigns.next();
      var currentBudget = campaign.getBudget().getAmount();
      campaign.getBudget().setAmount(currentBudget * 1.75);
    }
  }
}
```

---

## Testing Protocol (CRITICAL)

### Dec 20: Create Test Rule
1. Create a test rule for Dec 20 at 3pm
2. Set a tiny budget change (£1 difference)
3. Verify it executes correctly
4. Check email notification works
5. Delete test rule

### Dec 21: Final Setup
1. Create all 28 rules (7 per account)
2. Double-check amounts
3. Enable email notifications for critical ones:
   - Dec 24 sale launch rules
   - Dec 26 Boxing Day rules
4. Screenshot all rules for backup

### Dec 22: First Live Test
1. Check at 00:15 that Dec 22 rules executed
2. Verify budgets changed correctly
3. Confirm next rules are scheduled

---

## Backup Plans

### Plan B: Manual Implementation Sheet
Print this and keep handy:

| Time | Action |
|------|--------|
| Dec 24, 5:30pm | Log into Google Ads |
| Dec 24, 5:45pm | Open all 4 accounts |
| Dec 24, 6:00pm | Execute changes: UK→£1,505, USA→£1,085, EUR→£630, ROW→£280 |
| Dec 24, 6:30pm | Verify all changed |

### Plan C: API/MCP Automation
```python
# If comfortable with MCP tools
from datetime import datetime
import time

def update_budgets_at_time(target_hour=18):
    while True:
        now = datetime.now()
        if now.day == 24 and now.month == 12 and now.hour >= target_hour:
            # Execute budget updates via MCP
            mcp__google_ads__update_campaign_budget(
                customer_id="8573235780",
                campaign_id="[campaign_id]",
                daily_budget_micros=1505000000  # £1,505
            )
            break
        time.sleep(300)  # Check every 5 minutes
```

---

## Why Automated Rules Are Most Bulletproof

### Advantages:
1. **Set and forget** - Configure once, runs automatically
2. **Platform native** - No external dependencies
3. **Audit trail** - Google Ads logs all rule executions
4. **Email confirmation** - Get notified when rules run
5. **Bulk capable** - Can change all campaigns at once
6. **Time zone aware** - Uses account time zone
7. **Rollback easy** - Can pause/delete rules instantly

### Only Disadvantage:
- Must be set up in advance (can't create retroactive rules)

---

## Common Pitfalls to Avoid

❌ **DON'T** set rules to "Increase by X%" repeatedly (compounds incorrectly)
❌ **DON'T** forget to use account time zone
❌ **DON'T** apply to paused campaigns
❌ **DON'T** set conflicting rules for same time
✅ **DO** use "Set budget to £X" for precision
✅ **DO** enable email notifications
✅ **DO** test with a harmless rule first
✅ **DO** screenshot your rules as backup

---

## Final Checklist

### By December 21:
- [ ] All 28 rules created (7 per account)
- [ ] Email notifications enabled for critical rules
- [ ] Test rule executed successfully
- [ ] Screenshots taken of all rules
- [ ] Backup manual plan printed
- [ ] Calendar reminders set for verification

### Daily Verification:
- [ ] Dec 22, 00:15 - Check first rules executed
- [ ] Dec 23, 00:15 - Verify day 2 changes
- [ ] Dec 24, 18:30 - **CRITICAL** - Verify sale launch changes
- [ ] Dec 25, 00:15 - Check Christmas Day budgets
- [ ] Dec 26, 00:15 - **CRITICAL** - Verify Boxing Day maximum
- [ ] Dec 27, 00:15 - Check peak day budgets
- [ ] Dec 28, 00:15 - Verify final day settings

---

## Summary

**Most Bulletproof Approach:**
1. Use Google Ads automated rules
2. Set up all 28 rules by Dec 21
3. Test with harmless rule on Dec 20
4. Enable email notifications
5. Have manual backup plan ready

This method requires 2-3 hours of setup but then runs completely automatically, even if you're not at your computer. The platform handles everything, logs all changes, and sends confirmations.

**Remember:** The Dec 24 at 17:45 (5:45pm) rules are the most critical - these trigger the sale launch budget increases!