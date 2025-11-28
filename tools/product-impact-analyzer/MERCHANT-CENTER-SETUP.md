# Merchant Center Disapproval Tracking Setup

**Status:** Ready for deployment
**Last Updated:** 2025-11-04

---

## Overview

Automated tracking of Google Merchant Center product approval status to alert on disapprovals before they impact revenue.

**What it does:**
- Checks all products in Merchant Center every 6 hours
- Identifies disapproved products and disapproval reasons
- Saves snapshots for historical tracking
- Generates email alerts for new disapprovals
- Integrates with existing Product Impact Analyzer

---

## Current Status

✅ **Script ready:** `merchant_center_tracker.py` fully functional
✅ **Config ready:** All merchant IDs configured in `config.json`
✅ **API dependencies:** Google Content API libraries installed
❌ **Service account access:** Needs Merchant Center permissions
❌ **LaunchAgent:** Not yet scheduled
❌ **Email alerts:** Not yet configured

---

## Prerequisites

### Service Account Email
`mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`

This service account needs "Standard" or "Admin" access to each Merchant Center account to read product status.

---

## Setup Steps

### Step 1: Grant Merchant Center Access

For EACH client Merchant Center account, grant access to the service account:

1. Go to [Merchant Center](https://merchants.google.com/)
2. Select the merchant account (e.g., HappySnapGifts - 7481296)
3. Click **Settings** (⚙️) → **Users**
4. Click **Add user** (+)
5. Enter email: `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`
6. Select access level: **Standard** (read-only) or **Admin**
7. Click **Save**

**Repeat for all merchant accounts:**

| Client | Merchant ID | Status |
|--------|-------------|--------|
| **Clear Prospects (Priority 1)** |||
| HappySnapGifts | 7481296 | ⏳ Pending |
| WheatyBags | 7481286 | ⏳ Pending |
| BMPM | 7522326 | ⏳ Pending |
| **Other E-commerce Clients** |||
| Tree2mydoor | 107469209 | ⏳ Pending |
| Smythson UK | 102535465 | ⏳ Pending |
| BrightMinds | 5291988198 | ⏳ Pending |
| Accessories for the Home | 117443871 | ⏳ Pending |
| Go Glean UK | 5320484948 | ⏳ Pending |
| Superspace UK | 645236311 | ⏳ Pending |
| Uno Lights | 513812383 | ⏳ Pending |
| Godshot | 5291405839 | ⏳ Pending |
| Grain Guard | 5354444061 | ⏳ Pending |
| Crowd Control | 563545573 | ⏳ Pending |
| Just Bin Bags | 181788523 | ⏳ Pending |
| Just Bin Bags JHD | 5085550522 | ⏳ Pending |
| OTC (Camera Manuals) | 7253170 | ⏳ Pending |

---

### Step 2: Test Access

After granting access, test with a single client:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Test HappySnapGifts
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 merchant_center_tracker.py --client "HappySnapGifts" --report

# Should show:
# ✓ X products: Y approved, Z pending, W disapproved
```

---

### Step 3: Run Full Test

Once access is confirmed for all clients:

```bash
# Check all clients
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 merchant_center_tracker.py --report --save

# This will:
# - Check all enabled clients
# - Generate disapproval report
# - Save snapshot to data/merchant_center_snapshot.json
```

---

### Step 4: Set Up Automated Monitoring

Create LaunchAgent to run every 6 hours (6 AM, 12 PM, 6 PM, 12 AM):

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Run setup script
./setup_merchant_center_monitoring.sh
```

This will create `~/Library/LaunchAgents/com.petesbrain.merchant-center.plist`

**Verify it's running:**
```bash
# Check status
launchctl list | grep merchant-center

# View log
tail -f ~/.petesbrain-merchant-center.log
```

---

### Step 5: Configure Email Alerts

Edit `config.json` to enable email alerts:

```json
"alert_settings": {
  "email_enabled": true,
  "email_to": "petere@roksys.co.uk",
  "email_from": "petere@roksys.co.uk"
}
```

Configure Gmail app password in `config.json`:
```json
"email": {
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "petere@roksys.co.uk",
  "sender_password": "YOUR_GMAIL_APP_PASSWORD"
}
```

---

## Testing Commands

### Test Single Client
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 merchant_center_tracker.py --client "HappySnapGifts" --report
```

### Test All Clients
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 merchant_center_tracker.py --report
```

### Save Snapshot
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 merchant_center_tracker.py --save
```

---

## Output Examples

### Success (No Disapprovals)
```
Checking HappySnapGifts (Merchant ID: 7481296)...
  ✓ 127 products: 125 approved, 2 pending, 0 disapproved
Checking WheatyBags (Merchant ID: 7481286)...
  ✓ 89 products: 89 approved, 0 pending, 0 disapproved

✅ No disapproved products found!
```

### Disapprovals Found
```
Checking HappySnapGifts (Merchant ID: 7481296)...
  ✓ 127 products: 120 approved, 2 pending, 5 disapproved

════════════════════════════════════════════════════════════════
HappySnapGifts: 5 Disapproved Products
════════════════════════════════════════════════════════════════

🚫 Product 287: Personalised Face Mask with Photo
   Destination: Shopping (Disapproved in: GB)
   Issue: desktop_crawl_errors (unserviceable)
      Google cannot crawl your desktop site
      Resolution: Make sure your site is accessible to Googlebot

🚫 Product 412: Custom Photo Cushion
   Destination: Shopping (Disapproved in: GB)
   Issue: desktop_crawl_errors (unserviceable)
      Google cannot crawl your desktop site
```

---

## Integration with Product Impact Analyzer

### Snapshot Location
Snapshots saved to: `data/merchant_center_snapshot.json`

### Snapshot Format
```json
{
  "timestamp": "2025-11-04T10:00:00",
  "clients": {
    "HappySnapGifts": [
      {
        "product_id": "online:en:GB:287",
        "title": "Personalised Face Mask",
        "status": "disapproved",
        "item_level_issues": [
          {
            "code": "desktop_crawl_errors",
            "servability": "unserviceable",
            "description": "Google cannot crawl your desktop site"
          }
        ]
      }
    ]
  }
}
```

---

## Monitoring Schedule

Once LaunchAgent is configured:

- **6:00 AM** - Check all Merchant Center accounts
- **12:00 PM** - Check all Merchant Center accounts
- **6:00 PM** - Check all Merchant Center accounts
- **12:00 AM** - Check all Merchant Center accounts

**Log file:** `~/.petesbrain-merchant-center.log`

---

## Troubleshooting

### Error: "The caller does not have access"
**Solution:** Grant service account access in Merchant Center (see Step 1)

### Error: "No module named 'google'"
**Solution:** Use `.venv/bin/python3` not `python3`

### No output from LaunchAgent
**Solution:** Check log file: `cat ~/.petesbrain-merchant-center.log`

### Service account email needed
**Email:** `mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com`

---

## Next Steps

1. **User action required:** Grant Merchant Center access to service account (Step 1)
2. **Test:** Run test commands to verify access (Step 2)
3. **Deploy:** Create LaunchAgent for automated monitoring (Step 4)
4. **Alert:** Configure email alerts (Step 5)
5. **Update CONTEXT.md:** Document actual implementation status

---

## Related Files

- **Script:** `tools/product-impact-analyzer/merchant_center_tracker.py`
- **Config:** `tools/product-impact-analyzer/config.json`
- **Snapshots:** `tools/product-impact-analyzer/data/merchant_center_snapshot.json`
- **LaunchAgent:** `~/Library/LaunchAgents/com.petesbrain.merchant-center.plist` (to be created)
- **Log:** `~/.petesbrain-merchant-center.log` (to be created)
