# Enable Content API for Shopping

The product feed tracker needs the **Content API for Shopping** enabled in your Google Cloud project.

## Quick Fix

Visit this URL (it will take you directly to enable the API):

https://console.developers.google.com/apis/api/shoppingcontent.googleapis.com/overview?project=257130067085

Then click "Enable" button.

## Manual Steps

1. Go to https://console.cloud.google.com/
2. Select project: **petesbrain-emailsync** (ID: 257130067085)
3. Go to **APIs & Services** > **Library**
4. Search for "Content API for Shopping"
5. Click on it
6. Click **"Enable"**
7. Wait 2-3 minutes for it to propagate

## After Enabling

Once enabled, run the product feed tracker again:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 product_feed_tracker.py
```

It should start fetching product data for all 15 clients.

## Why This is Needed

The Content API for Shopping allows us to:
- Fetch product feed data (price, title, description, availability)
- Track product changes over time
- Detect when products are added/removed
- Monitor product disapprovals

This is separate from the Google Ads API (which we're already using).
