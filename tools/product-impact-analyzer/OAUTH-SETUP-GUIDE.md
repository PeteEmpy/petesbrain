# OAuth Setup for Merchant Center Access

This guide walks you through setting up OAuth authentication to access Merchant Center data (including disapprovals).

## Why OAuth?

- ✅ Full Merchant Center access (all product data + disapprov

als)
- ✅ One-time manual login
- ✅ Refresh token works automatically forever (until revoked)
- ✅ Use manager account to access all 15 clients at once

## Step 1: Create OAuth Credentials (5 minutes)

1. **Go to Google Cloud Console**:
   https://console.cloud.google.com/apis/credentials?project=257130067085

2. **Click "+ CREATE CREDENTIALS"** → **"OAuth client ID"**

3. **Application type**: Select **"Desktop app"**

4. **Name**: Enter **"Product Impact Analyzer"**

5. **Click "CREATE"**

6. **Download JSON**:
   - Click the **download icon** (⬇️) next to your new OAuth client
   - Save the file as `client_secrets.json`
   - Move it to: `/Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/client_secrets.json`

## Step 2: Run OAuth Setup (2 minutes)

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

.venv/bin/python3 setup_oauth.py
```

**What happens**:
1. Browser window opens
2. You log in with your Google account (**use your Google Ads MANAGER account**)
3. Grant permission to "Content API for Shopping"
4. Browser shows "Authentication successful"
5. Refresh token saved to `oauth_credentials.json`

**IMPORTANT**: Log in with your **Google Ads manager account** email to get access to all 15 client accounts automatically.

## Step 3: Test (30 seconds)

```bash
.venv/bin/python3 product_feed_tracker.py
```

You should see:
```
[2025-11-03 10:30:00] Using OAuth credentials (user authentication)
[2025-11-03 10:30:00] Fetching products for Tree2mydoor (merchant: 107469209)...
[2025-11-03 10:30:01]   ✓ Fetched 211 products for Tree2mydoor
[2025-11-03 10:30:01]   ✓ Saved snapshot to data/product_feed_history/Tree2mydoor/2025-11-03.json
```

## What You Get

Once OAuth is set up:
- ✅ **All product attributes** (price, title, description, availability, etc.)
- ✅ **Disapproval data** (approved/disapproved/pending status)
- ✅ **Disapproval reasons** (policy violations, data quality issues)
- ✅ **Products with zero impressions** (before they get any traffic)
- ✅ **Complete Merchant Center catalog**
- ✅ **Automatic refresh** (no more logins needed)

## Troubleshooting

**"client_secrets.json not found"**:
- Make sure you downloaded the OAuth client JSON from Google Cloud Console
- Rename it to `client_secrets.json` (not `client_secret_123456.json`)
- Move it to the product-impact-analyzer directory

**"The caller does not have access to the accounts"**:
- You logged in with the wrong Google account
- Delete `oauth_credentials.json` and run `setup_oauth.py` again
- Log in with your Google Ads **manager account**

**"Error opening browser"**:
- The script will print a URL - copy and paste it into your browser manually

## Re-authenticating

To re-authenticate (e.g., if you want to use a different account):

```bash
rm oauth_credentials.json
.venv/bin/python3 setup_oauth.py
```

## Security

- `oauth_credentials.json` contains a refresh token (treat like a password)
- File is stored locally only (not committed to git)
- Token can be revoked at: https://myaccount.google.com/permissions

---

**Estimated time**: 7-10 minutes total (most of it is Google Cloud Console setup)

**Result**: Automated Merchant Center access with full disapproval data forever
