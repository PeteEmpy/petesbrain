# Add Service Account to Merchant Center Accounts

To enable the Product Impact Analyzer to access Merchant Center data, you need to add the service account as a user to each Merchant Center account.

## Service Account Email

```
petesbrain-emailsync@petesbrain-emailsync.iam.gserviceaccount.com
```

**Copy this email - you'll need it for each account.**

## Steps Per Account

For each of the 15 Merchant Center accounts below:

1. **Log into Merchant Center** at https://merchants.google.com/
2. Select the correct account from the account selector
3. Click **Settings** (⚙️ gear icon) in the left menu
4. Click **Users** in the settings menu
5. Click **➕ Add User** (or **Invite User**)
6. Enter email: `petesbrain-emailsync@petesbrain-emailsync.iam.gserviceaccount.com`
7. Set access level: **Standard** (or **Admin** if Standard is not available)
8. Click **Save** or **Send Invite**

**Note**: Service accounts don't need to accept invites - access is granted immediately.

## Accounts to Set Up (15 Total)

### ✅ Checklist

Copy this checklist and mark off as you complete each one:

- [ ] **Tree2mydoor** (Merchant ID: 107469209)
- [ ] **Smythson UK** (Merchant ID: 102535465)
- [ ] **BrightMinds** (Merchant ID: 5291988198)
- [ ] **Accessories for the Home** (Merchant ID: 117443871)
- [ ] **Go Glean UK** (Merchant ID: 5320484948)
- [ ] **Superspace UK** (Merchant ID: 645236311)
- [ ] **Uno Lights** (Merchant ID: 513812383)
- [ ] **Godshot** (Merchant ID: 5291405839)
- [ ] **HappySnapGifts** (Merchant ID: 7481296)
- [ ] **WheatyBags** (Merchant ID: 7481286)
- [ ] **BMPM** (Merchant ID: 7522326)
- [ ] **Grain Guard** (Merchant ID: 5354444061)
- [ ] **Crowd Control** (Merchant ID: 563545573)
- [ ] **Just Bin Bags** (Merchant ID: 181788523)
- [ ] **Just Bin Bags JHD** (Merchant ID: 5085550522)

## After Setup

Once you've added the service account to all accounts, test it:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

export GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json

.venv/bin/python3 product_feed_tracker.py
```

You should see:
```
[2025-11-03 10:30:00] Fetching products for Tree2mydoor (merchant: 107469209)...
[2025-11-03 10:30:01]   ✓ Fetched 211 products for Tree2mydoor
[2025-11-03 10:30:01]   ✓ Saved snapshot to data/product_feed_history/Tree2mydoor/2025-11-03.json
```

## Tips

- **Fast method**: Open all 15 Merchant Center accounts in separate browser tabs
- **Copy-paste**: Keep the service account email in your clipboard
- **Verify**: After adding, you should see the service account email in the Users list
- **Access level**: "Standard" is sufficient (read-only access to products)

## What This Enables

Once setup is complete, the Product Impact Analyzer will have access to:

- ✅ All product attributes (price, title, description, etc.)
- ✅ Product availability status
- ✅ **Disapproval data** (approved/disapproved/pending)
- ✅ **Disapproval reasons** (policy violations, data issues)
- ✅ Products with zero impressions
- ✅ New products before they get impressions
- ✅ Complete Merchant Center product catalog

## Troubleshooting

**"User already exists"**: Skip that account - it's already set up

**"Invalid email"**: Double-check you copied the full service account email:
```
petesbrain-emailsync@petesbrain-emailsync.iam.gserviceaccount.com
```

**401 errors after adding**: Wait 2-3 minutes for permissions to propagate, then test again

---

**Estimated time**: 5-10 minutes for all 15 accounts
