# Enable Merchant API (Current)

The product feed tracker uses the **Merchant API** - the current recommended API for accessing Google Merchant Center data.

**Note**: The old Content API for Shopping is deprecated. This system has been updated to use the Merchant API.

## Quick Enable (2 minutes)

Visit this URL (takes you directly to enable the API):

https://console.developers.google.com/apis/api/merchantapi.googleapis.com/overview?project=257130067085

Then click the blue **"ENABLE"** button.

## Manual Steps

1. Go to https://console.cloud.google.com/
2. Select project: **petesbrain-emailsync** (ID: 257130067085)
3. Go to **APIs & Services** > **Library**
4. Search for "Merchant API"
5. Click on it
6. Click **"Enable"**
7. Wait 2-3 minutes for it to propagate

## After Enabling

Once enabled, run the product feed tracker:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-sheets-mcp-server/credentials.json \
  .venv/bin/python3 product_feed_tracker.py
```

You should see:
```
Fetching products for Tree2mydoor...
  ✓ Fetched 211 products for Tree2mydoor
```

## Why This API is Needed

The Merchant API allows us to:
- Fetch product feed data (price, title, description, availability)
- Track product changes over time
- Detect when products are added/removed
- Monitor product attributes and custom labels

This is separate from the Google Ads API (which we're already using).

## Migration from Content API

The system was updated from the deprecated Content API for Shopping to the current Merchant API:

**Key differences**:
- API endpoint: `merchantapi` (was `content`)
- Version: `products_v1beta` (was `v2.1`)
- Response format: `products` array with nested `attributes` object
- Price format: Uses `amountMicros` + `currencyCode` (divide by 1M for standard units)
- Documentation: https://developers.google.com/merchant/api

**No changes needed**: The product_feed_tracker.py has been updated to use the new API automatically.

## Alternative: Command Line

If you prefer the command line:

```bash
gcloud services enable merchantapi.googleapis.com --project=257130067085
```

---

**Once enabled**, the entire Product Impact Analyzer system will work automatically via LaunchAgents.
