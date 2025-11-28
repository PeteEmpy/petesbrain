# Godshot - Coffee Bean Supplemental Feed Guide

**Date:** 2025-11-17
**Merchant Centre ID:** 5291405839
**Sheet URL:** https://docs.google.com/spreadsheets/d/1XVyXywJvLraLys6oDP4aBlEAN_mOWoyf8LxjRLc2lxM/

---

## ✅ Ready to Upload - Clean Supplemental Feed

I've created a **clean two-column supplemental feed** with the actual Merchant Centre product IDs for all coffee beans.

### What's Included

**17 Coffee Bean Products:**
- Dak - Milky Cake 250g (15164)
- Dak - Honeymoon 250g (18910)
- Dak - Berry Blues 250g (22412)
- Dak - The Alchemist 250g (20867)
- Dak - Panettone 250g [Christmas] (22899, 23035)
- Dak - Yuzu Crew 125g (21142)
- Dak - Lush Buds 250g (22557)
- Dak - Mirabelle 250g (22553)
- Dak - Cream Donut 250g (22446)
- Dak - Orange Flirt 250g (18535)
- Dak - Golden Hour 250g (22511)
- Dak - Jazz Fruits 250g (19599)
- Dak - White Lotus 250g (22078)
- Dak - Lady in Red 125g (20830)
- Dak - Cherry Slide 250g (22417)

**Shipping Label:** `coffee_bean` (all products)

---

## How to Upload to Merchant Centre

### Step 1: Open the Sheet
https://docs.google.com/spreadsheets/d/1XVyXywJvLraLys6oDP4aBlEAN_mOWoyf8LxjRLc2lxM/

### Step 2: Log into Merchant Centre
1. Go to: https://merchants.google.com/
2. Select account: **5291405839** (Godshot)

### Step 3: Create Supplemental Feed
1. Navigate to: **Products** → **Feeds**
2. Click **"Add supplemental feed"** (blue button)
3. **Feed configuration:**
   - Feed name: `Coffee Bean Shipping Labels`
   - Country: **United Kingdom**
   - Primary feed: Select your main product feed
   - Input method: **Google Sheets**

4. Click **"Google Sheets"**
5. **Paste this URL:** https://docs.google.com/spreadsheets/d/1XVyXywJvLraLys6oDP4aBlEAN_mOWoyf8LxjRLc2lxM/
6. **Select range:** Sheet1!A1:B18 (or just A:B for all data)
7. Click **"Fetch now"** to test the connection
8. Review the preview - should show 17 products
9. Click **"Create feed"**

### Step 4: Wait for Processing
- Supplemental feed processing: **2-4 hours**
- Check feed status in Merchant Centre
- Should show "17 items processed" with 0 errors

### Step 5: Verify Products Updated
1. Go to: **Products** → **All products**
2. Search for: "Dak Milky Cake"
3. Click product to view details
4. Check that `shipping_label: coffee_bean` appears in attributes
5. Repeat for 2-3 other products to confirm

---

## Step 6: Create Shipping Service

**After supplemental feed is processed (2-4 hours later):**

1. Navigate to: **Growth** → **Manage programs** → **Shopping ads** → **Delivery**
   - OR: **Tools & Settings** (gear icon) → **Shipping and returns**

2. Click **"Add shipping service"** or **"Create shipping service"**

3. **Configure the service:**
   - **Service name:** `Coffee Bean Shipping - £2.00`
   - **Country:** United Kingdom
   - **Delivery time:** 2-3 business days (adjust as needed)
   - **Currency:** GBP (£)

4. **Set shipping rate:**
   - **Rate type:** Flat rate
   - **Cost:** £2.00

5. **Apply to products:**
   - **Product selection:** "Products with specific shipping labels"
   - **Shipping label value:** `coffee_bean` (exact match, case-sensitive)

6. **Save and activate**

---

## Step 7: Verify in Shopping Ads (24-48 hours later)

**Check Shopping Ad Preview:**
1. Search Google Shopping: "Dak coffee Godshot"
2. Look for Godshot products in results
3. **Verify:** Ad shows "£2.00 delivery" or "+£2.00 delivery"
4. Test multiple coffee products

**Monitor Performance:**
1. Google Ads → Performance Max campaign
2. Asset group: "Coffee Generic" (ID: 6491248230)
3. Check if performance improves with accurate shipping rate

---

## Product IDs - Full Reference

| Merchant Centre ID | Product Name | Impressions (Nov) |
|-------------------|--------------|-------------------|
| 15164 | Dak - Milky Cake 250g | 10,879 (highest) |
| 18910 | Dak - Honeymoon 250g | 2,235 |
| 22412 | Dak - Berry Blues 250g | 1,887 |
| 20867 | Dak - The Alchemist 250g | 1,835 |
| 19907 | Dak - Milky Cake (variant) | 1,331 |
| 22899 | Dak - Panettone 250g | 1,277 |
| 21142 | Dak - Yuzu Crew 125g | 1,204 |
| 22557 | Dak - Lush Buds 250g | 1,153 |
| 22553 | Dak - Mirabelle 250g | 1,133 |
| 22446 | Dak - Cream Donut 250g | 910 |
| 18535 | Dak - Orange Flirt 250g | 876 |
| 22511 | Dak - Golden Hour 250g | 831 |
| 19599 | Dak - Jazz Fruits 250g | 816 |
| 23035 | Dak - Panettone (variant) | 777 |
| 22078 | Dak - White Lotus 250g | 701 |
| 20830 | Dak - Lady in Red 125g | 620 |
| 22417 | Dak - Cherry Slide 250g | 580 |

**Total:** 17 coffee bean products

---

## Important Notes

### ✅ What's Included
- **Only Dak coffee beans** (250g and 125g bags)
- All products currently active with impressions in November 2025
- Uses actual Merchant Centre product IDs (verified via Google Ads)

### ❌ What's NOT Included
- Coffee equipment (grinders, kettles, French presses)
- Other coffee brands (if any exist in catalog)
- Matcha/tea products
- Hot chocolate
- Non-coffee products

### 🔍 If You Have Other Coffee Brands
If you stock coffee from other roasters (Friedhats, Bonanza, A Matter of Concrete, etc.), you'll need to:
1. Find their product pages on mygodshot.com
2. Get their Merchant Centre IDs from the Shopping Performance report
3. Add them to the supplemental feed sheet
4. Re-upload the feed

---

## Troubleshooting

### "Invalid product ID" error
- **Cause:** Product ID doesn't exist in main feed
- **Solution:** Double-check IDs match Shopping Performance View data

### "Duplicate attribute" error
- **Cause:** Main feed already has `shipping_label` for these products
- **Solution:** Supplemental feed should override. If issue persists, remove from main feed first.

### Products not showing `shipping_label`
- **Cause:** Feed hasn't processed yet
- **Solution:** Wait 2-4 hours, refresh Merchant Centre

### Shipping rate not showing in ads
- **Cause:** Changes haven't propagated, or service not configured correctly
- **Solution:**
  1. Verify shipping service created and active
  2. Verify service applies to `shipping_label = coffee_bean`
  3. Wait 24-48 hours for Shopping ads to update
  4. Check Merchant Centre diagnostics for errors

---

## Timeline

- ⏱️ **Step 3 (Upload):** 10 minutes
- ⏱️ **Step 4 (Processing):** 2-4 hours
- ⏱️ **Step 5 (Verify):** 10 minutes
- ⏱️ **Step 6 (Shipping service):** 15 minutes
- ⏱️ **Propagation:** 24-48 hours
- ⏱️ **Step 7 (Verify ads):** 15 minutes

**Total active work:** ~50 minutes
**Total wait time:** 1-2 days

---

## Success Criteria

✅ Supplemental feed uploaded successfully (0 errors)
✅ 17 products show `shipping_label: coffee_bean` in Merchant Centre
✅ Shipping service created and active for `coffee_bean` label
✅ Shopping ads show "£2.00 delivery" for coffee products
✅ Equipment/other products show different (correct) shipping rates

---

## Files Created

1. **Supplemental Feed Sheet:** https://docs.google.com/spreadsheets/d/1XVyXywJvLraLys6oDP4aBlEAN_mOWoyf8LxjRLc2lxM/
2. **This Guide:** `clients/godshot/documents/coffee-bean-supplemental-feed-guide.md`
3. **Original Investigation:** `clients/godshot/documents/merchant-centre-coffee-shipping-investigation-2025-11-17.md`

---

**Status:** ✅ Ready to upload - All product IDs verified from actual Merchant Centre data
