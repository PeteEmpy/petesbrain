# Merchant Center Tracking - Quick Start

**Ready to deploy** - Follow these steps to enable automated Merchant Center disapproval tracking.

---

## What You're Setting Up

✅ Automated checking of Merchant Center product approval status every 6 hours
✅ Email alerts when products are disapproved
✅ Historical tracking of approval/disapproval changes
✅ Integration with Product Impact Analyzer

---

## Step 1: Grant Merchant Center Access (USER ACTION REQUIRED)

The service account needs "Standard" access to read product status.

**Service account email:**
```
mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com
```

### For Clear Prospects (Priority - Do First)

1. Go to [Google Merchant Center](https://merchants.google.com/)
2. For **each** of these three accounts:
   - HappySnapGifts (7481296)
   - WheatyBags (7481286)
   - BMPM (7522326)
3. Click Settings ⚙️ → **Users**
4. Click **Add user** (+)
5. Enter: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
6. Select access level: **Standard**
7. Click **Save**

### For Other Clients (Can Do Later)

Repeat the same process for other merchant accounts listed in `MERCHANT-CENTER-SETUP.md`

---

## Step 2: Test Access

After granting access to at least HappySnapGifts, test it:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 merchant_center_tracker.py --client "HappySnapGifts" --report
```

**Expected output:**
```
Checking HappySnapGifts (Merchant ID: 7481296)...
  ✓ 127 products: 125 approved, 2 pending, 0 disapproved

✅ No disapproved products found!
```

**If you see "The caller does not have access":**
- Wait 5 minutes for permissions to propagate
- Verify you added the correct email address
- Try again

---

## Step 3: Set Up Automated Monitoring

Once access is confirmed, run the setup script:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

./setup_merchant_center_monitoring.sh
```

This creates a LaunchAgent that runs every 6 hours.

---

## Step 4: Test the Automation

Trigger a manual run:

```bash
launchctl start com.petesbrain.merchant-center
```

View the log:

```bash
tail -f ~/.petesbrain-merchant-center.log
```

---

## Step 5: Update Email Draft

Once working, the email to Michael is accurate. The claim:

> "Merchant Centre disapprovals - the system monitors your product feed every 6 hours and alerts me immediately when products get disapproved"

...will be TRUE after completing these steps.

---

## Quick Commands

### Check all clients
```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 merchant_center_tracker.py --report --save
```

### Check monitoring status
```bash
launchctl list | grep merchant-center
```

### View logs
```bash
tail -f ~/.petesbrain-merchant-center.log
```

### Stop monitoring
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.merchant-center.plist
```

### Restart monitoring
```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.merchant-center.plist
```

---

## Estimated Time

- **Step 1 (Merchant Center access):** 5-10 minutes for 3 Clear Prospects accounts
- **Step 2 (Testing):** 2 minutes
- **Step 3 (LaunchAgent setup):** 1 minute
- **Total:** ~15 minutes to have it running for Clear Prospects

---

## What Happens Next

Once deployed:

1. **6 AM, 12 PM, 6 PM, 12 AM** - System checks all Merchant Center accounts
2. **Disapprovals detected** - Generates report and saves snapshot
3. **No disapprovals** - Logs "✅ No disapproved products found"
4. **Historical tracking** - Snapshots saved to `data/merchant_center_snapshot.json`

---

## For the Email to Michael

After completing Step 3, the Merchant Centre monitoring claim in the email draft is **accurate and can be sent**.

Current draft location:
```
clients/clear-prospects/email-draft-2025-11-04-october-response.txt
```

---

## Troubleshooting

**"The caller does not have access"**
→ Grant Merchant Center access (Step 1), wait 5 mins, try again

**"No module named 'google'"**
→ Use `.venv/bin/python3` not `python3`

**LaunchAgent not running**
→ Check: `launchctl list | grep merchant-center`
→ View log: `cat ~/.petesbrain-merchant-center.log`

---

## Related Documentation

- Full setup guide: `MERCHANT-CENTER-SETUP.md`
- Client tracking status: `CLIENT-TRACKING-STATUS.md`
- Email status: `clients/clear-prospects/EMAIL-STATUS-MICHAEL-OCT-2025.md`
