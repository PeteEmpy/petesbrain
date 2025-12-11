# Devonshire Budget Optimizer

## Description

Analyzes Devonshire Hotels campaign performance and generates budget optimization recommendations. Identifies high-performing campaigns that are budget-constrained and underperforming campaigns to free up budget for reallocation within the £9,000 monthly Properties budget.

**Key Features**:
- Analyzes last 7 days of campaign performance
- Identifies ROAS and Lost Impression Share for each campaign
- Suggests specific budget increases/decreases
- Generates detailed HTML report with expected impact
- Sends email report to petere@roksys.co.uk

**Thresholds**:
- ROAS > 550% (5.5x) with Lost IS > 10% = Increase candidates
- ROAS < 550% or zero conversions = Decrease candidates
- Budget maintained at £9,000/month (budget-neutral reallocations)

## When to Run

Run this skill:
- **Weekly** before strategy review meetings
- **Quarterly** as part of performance optimization cycle
- **Ad-hoc** when you want to review campaign budgets
- **Before** making manual budget adjustments to validate current recommendations

## Allowed Tools
- Bash
- Read
- GoogleAdsAPI (via Python subprocess)
- Gmail (via Python subprocess)

## Instructions

### Step 1: Execute the Analysis

Run the budget optimizer script:

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/agents/devonshire-weekly-budget-optimizer
ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" python3 devonshire-weekly-budget-optimizer.py
```

### Step 2: Monitor Execution

The script will:
1. Authenticate with Google Ads API
2. Fetch last 7 days of campaign performance for "DEV | Properties" campaigns
3. Calculate ROAS and Lost IS Budget for each campaign
4. Categorize campaigns (increase, decrease, maintain)
5. Calculate budget reallocations
6. Generate detailed HTML email report
7. Send email to petere@roksys.co.uk

### Step 3: Review Email Report

Once sent, check your email for:
- **Budget Increases** - Campaigns with ROAS > 550% that are budget-constrained
- **Budget Reductions** - Campaigns with ROAS < 550% or zero conversions
- **Maintain** - Well-optimized campaigns with no changes
- **Expected Impact** - Estimated weekly revenue increase from reallocations
- **Implementation Steps** - How to apply changes in Google Ads

### Step 4: Implement (Optional)

If recommendations are actionable:
1. Open Google Ads → Devonshire account
2. Update campaign daily budgets as recommended
3. Monitor performance over next 7 days
4. Run optimizer again next week to validate impact

## Output

The script outputs:
- **Console logs** - Real-time execution details
- **HTML email** - Formatted report sent to petere@roksys.co.uk
- **Log file** - `~/.petesbrain-devonshire-optimizer.log` (if run via launchctl)

### Example Log Output

```
[2025-12-11 14:30:00] ================================================================================
[2025-12-11 14:30:00] 📊 Devonshire Weekly Budget Optimizer
[2025-12-11 14:30:00] ================================================================================
[2025-12-11 14:30:00] 📅 Date: Wednesday, December 11, 2025
[2025-12-11 14:30:00] Fetching campaign performance (last 7 days)...
[2025-12-11 14:30:01] ✓ Fetched 12 Properties campaigns (excluding The Hide)
[2025-12-11 14:30:01] Analyzing campaigns for optimization opportunities...
[2025-12-11 14:30:01] 📊 Campaign Analysis:
[2025-12-11 14:30:01]    Increase candidates: 3 campaigns
[2025-12-11 14:30:01]    Decrease candidates: 2 campaigns
[2025-12-11 14:30:01]    Maintain: 7 campaigns
[2025-12-11 14:30:02] 📧 Generating email report...
[2025-12-11 14:30:02] 💡 Actionable recommendations found
[2025-12-11 14:30:02] 🔐 Authenticating with Gmail...
[2025-12-11 14:30:03] 📧 Sending weekly report to petere@roksys.co.uk...
[2025-12-11 14:30:03] ✅ Report sent successfully! Message ID: 17d1234567890abcdef
[2025-12-11 14:30:03] 💡 Recommendations Summary:
[2025-12-11 14:30:03]    Increase: 3 campaigns
[2025-12-11 14:30:03]    Decrease: 2 campaigns
[2025-12-11 14:30:03]    Maintain: 7 campaigns
```

## What Changed

Previously this ran **automatically** every Thursday at 9:00 AM via LaunchAgent. Now it's a **manual skill** so you can:
- Run it on-demand whenever you want
- Control when budget recommendations are generated
- Schedule it manually around your workflow instead of automatic emails
- Still get the same detailed analysis and recommendations

## Troubleshooting

### Script fails to authenticate

**Error**: "No valid Gmail credentials"

**Solution**:
```bash
# Check token exists
ls -la /Users/administrator/Documents/PetesBrain.nosync/shared/email-sync/token.json

# If missing, run email-sync to re-authenticate
/usr/local/bin/python3 /Users/administrator/Documents/PetesBrain.nosync/shared/email-sync/sync-emails.py
```

### No campaign data returned

**Error**: "No campaign data available"

**Cause**: Filter looking for campaigns matching `'%DEV | Properties%'`

**Check**: Verify campaign names in Google Ads match this pattern exactly

### Gmail API errors

**Solution**: Re-authenticate:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/shared/email-sync
python3 -c "from google_auth_oauthlib.flow import InstalledAppFlow; flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/gmail.send']); creds = flow.run_local_server(); import json; print(json.dumps({'token': creds.token, 'refresh_token': creds.refresh_token}))"
```

## Related

- **Devonshire Hotels context**: `clients/devonshire-hotels/CONTEXT.md`
- **Budget tracking**: `clients/devonshire-hotels/scripts/update_budget_tracker.py`
- **Manual application**: Google Ads UI → Campaigns → Budget settings
- **Weekly strategy**: Schedule this as part of your Thursday optimization routine
