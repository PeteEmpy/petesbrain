# Godshot - Supplemental Feed Implementation Guide

**Date:** 2025-11-17
**Purpose:** Add `shipping_label = coffee` to coffee products via supplemental feed
**Google Sheet:** [Godshot - Coffee Products Supplemental Feed](https://docs.google.com/spreadsheets/d/1ZokYgltwKkTbuq76rhVFkiQ_hJEMwhZvL07FNk3c5co/)

---

## What is a Supplemental Feed?

A supplemental feed allows you to **add or override attributes** for products in your main product feed without modifying the main feed itself. Perfect for adding `shipping_label` to specific products.

**Benefits:**
- ✅ No need to modify WooCommerce
- ✅ Quick to implement and update
- ✅ Easy to maintain
- ✅ Can be uploaded directly to Merchant Centre

---

## Step-by-Step Implementation

### Step 1: Complete the Product List ⏸️ IN PROGRESS

**Google Sheet:** https://docs.google.com/spreadsheets/d/1ZokYgltwKkTbuq76rhVFkiQ_hJEMwhZvL07FNk3c5co/

**Current Status:**
- ✅ 5 Dak coffee products verified with IDs
- ⏸️ ~5 more Dak products need IDs
- ⏸️ ~30 other coffee brands need to be added

**To Complete:**
1. Visit each missing coffee product page on https://mygodshot.com/product-category/coffee/
2. Extract Product ID from page source (look for `"productID":"XXXXX"`)
3. Add to spreadsheet with `shipping_label = coffee`

**Products Verified So Far:**

| Product Name | WooCommerce ID | SKU | Status |
|--------------|----------------|-----|--------|
| Dak - Milky Cake 250g | 55692 | - | ✅ Verified |
| Dak - Honeymoon 250g | 36586 | 18910 | ✅ Verified |
| Dak - Cream Donut 250g | 64218 | 22446 | ✅ Verified |
| Dak - Strawberry Kiss 250g | 38978 | - | ✅ Verified |
| Dak - Berry Blues 250g | 63722 | 22412 | ✅ Verified |

**Need to Add:**
- Dak - Purple Rain 250g
- Dak - Passion Twist 250g
- Dak - Orange Flirt 250g
- Dak - Yuzu Crew 125g
- Dak - Panettone 250g
- A Matter of Concrete Coffee
- Friedhats Coffee
- Bonanza Coffee
- ~30 more European roaster coffees

---

### Step 2: Verify ID Format 🔴 CRITICAL

**BEFORE uploading the supplemental feed, you MUST verify which ID format your main feed uses.**

#### Option A: Check in Merchant Centre (RECOMMENDED)

1. Go to: https://merchants.google.com/
2. Select Godshot account (5291405839)
3. Navigate to: **Products** → **All products**
4. Look at the **ID** column for a few coffee products
5. Check format:
   - If ID = `55692` → Use WooCommerce ID as-is
   - If ID = `gla_55692` → Add `gla_` prefix
   - If ID = SKU (e.g., `22446`) → Use SKU column instead

#### Option B: Check via Google Ads Product Report

Run this query in Google Ads to see product IDs:

```
SELECT
  segments.product_item_id,
  segments.product_title,
  metrics.clicks
FROM shopping_performance_view
WHERE segments.date DURING LAST_7_DAYS
  AND metrics.clicks > 0
ORDER BY metrics.clicks DESC
LIMIT 10
```

Look at the `product_item_id` format.

---

### Step 3: Format the Supplemental Feed

**Once you've verified the ID format:**

1. Open the Google Sheet
2. Update Column D ("ID for Feed") with the correct format:
   - If format is WooCommerce ID: Already done!
   - If format is `gla_` prefix: Add `gla_` before each ID (e.g., `gla_55692`)
   - If format is SKU: Use Column C values instead

3. Copy **ONLY columns D and E** (ID for Feed + shipping_label)
4. Create a new sheet/range with just those two columns
5. Ensure headers are exactly: `id` and `shipping_label`

**Final Format:**
```
id,shipping_label
55692,coffee
36586,coffee
64218,coffee
38978,coffee
63722,coffee
```

Or if using gla_ prefix:
```
id,shipping_label
gla_55692,coffee
gla_36586,coffee
gla_64218,coffee
gla_38978,coffee
gla_63722,coffee
```

---

### Step 4: Upload to Merchant Centre ⏸️ NOT YET DONE

**In Merchant Centre:**

1. Navigate to: **Products** → **Feeds**
2. Click **"Add supplemental feed"** (NOT "Add primary feed")
3. Configure:
   - **Feed name:** `Coffee Shipping Labels`
   - **Country:** United Kingdom
   - **Primary feed:** Select your main product feed
   - **Input method:** Google Sheets
4. Click **"Google Sheets"**
5. Paste the Google Sheets URL (or select from your Google Drive)
6. **Select the range** with just id and shipping_label columns
7. **Fetch now** to test
8. Review any errors
9. Click **"Create feed"**

**Expected Result:**
- Feed should show "X products processed"
- 0 errors (if IDs match correctly)
- Products now have `shipping_label: coffee` attribute

---

### Step 5: Create Shipping Service ⏸️ NOT YET DONE

**After supplemental feed is processed (wait 2-4 hours):**

1. Navigate to: **Growth** → **Manage programs** → **Shopping ads** → **Delivery**
2. Click **"Add shipping service"**
3. Configure:
   - **Service name:** `Coffee Shipping - £2.00`
   - **Country:** United Kingdom
   - **Delivery time:** 2-3 business days
   - **Rate type:** Flat rate
   - **Cost:** £2.00
4. **Apply to products:**
   - Select: **"Products with specific shipping labels"**
   - Enter label: `coffee`
5. **Save**

---

### Step 6: Verify ⏸️ 24-48 HOURS AFTER STEP 5

**Check Merchant Centre:**
1. Go to: Products → All products
2. Search for a coffee product (e.g., "Dak Milky Cake")
3. Click product to view details
4. Verify `shipping_label: coffee` appears in attributes

**Check Shopping Ads:**
1. Search Google Shopping for: "Dak coffee Godshot"
2. Check ad preview shows "£2.00 delivery"
3. Test multiple coffee products

**Check Google Ads Performance:**
1. Monitor "Coffee Generic" asset group (ID: 6491248230)
2. Check if clicks/conversions improve or maintain with correct shipping rate

---

## Troubleshooting

### Error: "Invalid product ID"
**Cause:** ID format in supplemental feed doesn't match main feed
**Solution:** Go back to Step 2, verify ID format, update Column D in sheet

### Error: "Duplicate product ID"
**Cause:** Product ID appears in both main feed and supplemental feed with conflicting data
**Solution:** Supplemental feeds should only ADD attributes, not replace. Check your main feed doesn't already have `shipping_label`

### Products not showing shipping_label
**Cause:** Feed hasn't refreshed yet
**Solution:** Wait 2-4 hours for supplemental feed to process. Check feed status in Merchant Centre.

### Shipping rate not showing in ads
**Cause:** Shipping service not configured, or changes haven't propagated
**Solution:**
1. Verify shipping service is created and active
2. Wait 24-48 hours for changes to appear in ads
3. Check Merchant Centre feed diagnostics for errors

---

## Alternative: If Supplemental Feed Doesn't Work

If you encounter issues with the supplemental feed approach:

**Fallback Option 1: Product Feed Override**
- Add `shipping` attribute directly to main feed
- Format: `shipping(country:price:service)`
- Example: `GB:2.00 GBP:Standard`

**Fallback Option 2: Category-Based Shipping**
- Ensure all coffee products are in "Food & Beverages > Coffee & Tea" category
- Create shipping service that applies to that category
- Downside: May apply to tea/matcha if in same category

**Fallback Option 3: WooCommerce Custom Field**
- See original implementation plan (shipping-implementation-plan-2025-11-17.md)
- Add `shipping_label` custom field to products in WooCommerce
- Requires main feed to include custom fields

---

## Success Criteria

✅ All ~40 coffee products have `shipping_label: coffee` in Merchant Centre
✅ Coffee Shipping service created and active
✅ Shopping ads show "£2.00 delivery" for coffee products
✅ Equipment/homeware products show different (correct) shipping rate
✅ No Merchant Centre feed errors

---

## Timeline

- **Step 1:** 2-3 hours (identify all 40 coffee products + IDs)
- **Step 2-3:** 30 minutes (verify ID format, format feed)
- **Step 4:** 15 minutes (upload to Merchant Centre)
- **Propagation wait:** 2-4 hours (supplemental feed processing)
- **Step 5:** 15 minutes (create shipping service)
- **Propagation wait:** 24-48 hours (appear in Shopping ads)
- **Step 6:** 30 minutes (verification)
- **Total:** ~3-4 hours active work + 1-2 days wait time

---

## Resources

- **Google Sheet:** https://docs.google.com/spreadsheets/d/1ZokYgltwKkTbuq76rhVFkiQ_hJEMwhZvL07FNk3c5co/
- **Merchant Centre:** https://merchants.google.com/ (Account: 5291405839)
- **Original Investigation:** `clients/godshot/documents/merchant-centre-coffee-shipping-investigation-2025-11-17.md`
- **Full Implementation Plan:** `clients/godshot/documents/shipping-implementation-plan-2025-11-17.md`

---

## Next Actions

**IMMEDIATE:**
- [ ] Complete product list with all ~40 coffee products
- [ ] Verify ID format in Merchant Centre
- [ ] Format supplemental feed correctly

**THEN:**
- [ ] Upload supplemental feed to Merchant Centre
- [ ] Wait 2-4 hours for processing
- [ ] Create Coffee Shipping service
- [ ] Wait 24-48 hours
- [ ] Verify changes in Shopping ads

---

**Status:** 🟡 In Progress - Product list 25% complete (5/40 products)
