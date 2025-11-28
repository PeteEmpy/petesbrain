# Setup Merchant Center Tracking - Action Plan

**Date**: November 12, 2025
**Status**: Service account exists, needs Merchant Center access

---

## Problem Identified

The Product Impact Analyzer's Merchant Center disapproval tracking was **documented but never activated**. Testing confirmed:

✅ Scripts exist and are functional
✅ Service account exists: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
❌ Service account does NOT have access to Merchant Center accounts

**Error**: `The caller does not have access to the accounts: [7481296]`

---

## What Needs to Be Done

### Step 1: Grant Service Account Access to Merchant Center

You need to add the service account to each Merchant Center account as a user.

**Service Account Email**: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`

**Merchant Center accounts that need access** (from config.json):

| Client | Merchant ID | URL |
|--------|-------------|-----|
| HappySnapGifts | 7481296 | https://merchants.google.com/mc/accounts/7481296/users |
| WheatyBags | 7481286 | https://merchants.google.com/mc/accounts/7481286/users |
| BMPM | 7522326 | https://merchants.google.com/mc/accounts/7522326/users |
| Tree2mydoor | 107469209 | https://merchants.google.com/mc/accounts/107469209/users |
| Smythson UK | 102535465 | https://merchants.google.com/mc/accounts/102535465/users |
| BrightMinds | 5291988198 | https://merchants.google.com/mc/accounts/5291988198/users |
| Accessories for the Home | 117443871 | https://merchants.google.com/mc/accounts/117443871/users |
| Go Glean UK | 5320484948 | https://merchants.google.com/mc/accounts/5320484948/users |
| Superspace UK | 645236311 | https://merchants.google.com/mc/accounts/645236311/users |
| Uno Lights | 513812383 | https://merchants.google.com/mc/accounts/513812383/users |
| Godshot | 5291405839 | https://merchants.google.com/mc/accounts/5291405839/users |
| Just Bin Bags | 181788523 | https://merchants.google.com/mc/accounts/181788523/users |
| Just Bin Bags JHD | 5085550522 | https://merchants.google.com/mc/accounts/5085550522/users |
| Grain Guard | 5354444061 | https://merchants.google.com/mc/accounts/5354444061/users |
| Crowd Control | 563545573 | https://merchants.google.com/mc/accounts/563545573/users |

**For each Merchant Center account**:
1. Go to the URL above (or navigate to Merchant Center → Settings → Users)
2. Click "Add User" or "Invite User"
3. Enter email: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
4. Select access level: **"Standard"** (read access to products and reports)
5. Save

**Important**: Permissions can take 5-10 minutes to propagate. Wait after adding before testing.

---

### Step 2: Test Merchant Center Access

After granting access, test each account:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
source .venv/bin/activate

# Test Clear Prospects brands (priority)
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  python3 merchant_center_tracker.py --client "HappySnapGifts" --report

GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  python3 merchant_center_tracker.py --client "WheatyBags" --report

GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  python3 merchant_center_tracker.py --client "BMPM" --report
```

**Expected output** (success):
```
Checking HappySnapGifts (Merchant ID: 7481296)...

Product Status Summary:
- Total Products: 234
- Approved: 230
- Disapproved: 4
- Pending: 0

Disapproved Products:
1. Product ID: online:en:GB:12345
   Title: Photo Cushion Large
   Issue: missing_gtin
   Description: Product is missing required GTIN
   Resolution: Add valid GTIN to product feed
```

**If you see 401 error**, wait 5-10 more minutes and try again.

---

### Step 3: Enable Automated Disapproval Monitoring

Once access is confirmed, run the setup script:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
./setup_disapproval_monitoring.sh
```

This will:
1. Create LaunchAgent for daily disapproval checks (10:30 AM weekdays)
2. Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable
3. Optionally run a test check

**Select "Yes" when prompted** to run the test check and verify everything works.

---

### Step 4: Verify Automated Monitoring

Check that the LaunchAgent is running:

```bash
# Check if loaded
launchctl list | grep disapproval

# View logs
tail -f ~/.petesbrain-disapproval-monitor.log

# Manually trigger a check (test mode, ignore business hours)
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
source .venv/bin/activate
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  python3 disapproval_monitor.py --test
```

**Expected output**: Email alert if any products are disapproved.

---

### Step 5: Check Clear Prospects for Disapprovals NOW

Once access is granted and tested, immediately check all three Clear Prospects brands:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
source .venv/bin/activate

# Check all three brands
for brand in "HappySnapGifts" "WheatyBags" "BMPM"; do
  echo "=== Checking $brand ==="
  GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
    python3 merchant_center_tracker.py --client "$brand" --report
  echo ""
done
```

This will show current disapproval status for all Clear Prospects products.

---

## Timeline

**Immediate** (today):
1. Grant service account access to all Merchant Center accounts (15-20 minutes)
2. Wait 10 minutes for permissions to propagate
3. Test access for Clear Prospects brands
4. Check for current disapprovals

**Once access confirmed** (today):
5. Run setup script to enable automated monitoring
6. Verify LaunchAgent is running

**Ongoing** (automated):
- Daily checks at 10:30 AM (weekdays)
- Email alerts for new disapprovals during business hours
- Snapshots stored in `monitoring/disapprovals_*.json`

---

## What This Will Enable

Once set up, the Product Impact Analyzer will automatically:

✅ **Track product approval status** from Google Merchant Center
✅ **Detect newly disapproved products** (compare today vs. yesterday)
✅ **Classify disapproval severity**:
   - CRITICAL: Policy violations (counterfeit, prohibited content)
   - WARNING: Data quality (missing GTIN, invalid price)
✅ **Send email alerts** with:
   - Product ID and title
   - Disapproval reason (issue code)
   - Human-readable description
   - Resolution guidance
   - Affected countries
✅ **Store historical data** to track disapproval patterns

---

## Priority: Clear Prospects

For your immediate question about Clear Prospects disapprovals:

**Current limitation**: Cannot check disapprovals until service account has Merchant Center access.

**After granting access** (Step 1 above), you'll be able to:
1. See ALL current disapprovals across HappySnapGifts, WheatyBags, BMPM
2. Understand WHY products disappeared (if due to disapprovals)
3. Get specific issue codes and resolution steps
4. Monitor for NEW disapprovals going forward (automated daily)

---

## Quick Start (Minimum Steps)

If you just want to check Clear Prospects disapprovals RIGHT NOW:

1. **Grant access** (5 minutes):
   - Go to https://merchants.google.com/mc/accounts/7481296/users
   - Add user: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
   - Access level: Standard
   - Repeat for merchant IDs: 7481286, 7522326

2. **Wait 10 minutes** for permissions to propagate

3. **Check disapprovals** (2 minutes):
   ```bash
   cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
   source .venv/bin/activate

   GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
     python3 merchant_center_tracker.py --client "HappySnapGifts" --report
   ```

This will immediately show if there are any disapprovals on HappySnapGifts.

---

## Support

Questions or issues?

- **Logs**: Check `~/.petesbrain-disapproval-monitor.log` after setup
- **Test manually**: `python3 disapproval_monitor.py --test --client "HappySnapGifts"`
- **Verify permissions**: Wait 10 minutes after granting Merchant Center access
- **Documentation**: See `MERCHANT-CENTER-TRACKING.md` for complete guide

---

**Next Action**: Grant service account access to Merchant Center accounts (see Step 1 above).
