# Godshot - Coffee Shipping Implementation Plan

**Date:** 2025-11-17
**Issue:** Coffee beans showing incorrect delivery charge in Shopping ads
**Required Rate:** £2.00 for coffee beans (250g bags)
**Merchant Centre ID:** 5291405839
**Status:** Ready for Implementation

---

## Coffee Products Requiring £2 Shipping

### Coffee Beans (250g bags) - £2.00 Shipping
- Dak – Milky Cake 250g (£17.00)
- Dak – Honeymoon 250g (£17.00)
- Dak – Strawberry Kiss 250g (£16.50)
- Dak – Cream Donut 250g (£18.00)
- Dak – Orange Flirt 250g (£14.00)
- Dak – Berry Blues 250g (£19.00)
- Dak – Panettone 250g (£22.00)

### Small Format Coffee - £2.00 Shipping
- Dak – Yuzu Crew 125g (£15.00)

**Total Products:** ~8 core coffee products (likely more in full catalog)

**Note:** Coffee equipment (grinders, kettles, French presses) should use standard/higher shipping rates.

---

## Implementation Method: Shipping Labels (RECOMMENDED)

### Why This Method?
✅ Most flexible for adding new coffee products
✅ Clear separation between coffee and equipment
✅ Easy to maintain long-term
✅ Standard Google Merchant Centre feature

---

## Step-by-Step Implementation Guide

### Phase 1: Access Merchant Centre ⏸️ NOT YET DONE

**Action Required:** Manual login to Google Merchant Centre

1. **Navigate to:** https://merchants.google.com/
2. **Log in** with Google account that has access to Godshot
3. **Select Merchant Centre account:** 5291405839 (Godshot)
4. **Navigate to Shipping Settings:**
   - Click **"Growth"** in left sidebar
   - Click **"Manage programs"**
   - Select **"Shopping ads"**
   - Click **"Delivery"** OR
   - Click **"Tools & Settings"** (gear icon)
   - Select **"Shipping and returns"**

**Document Current Setup:**
- [ ] Screenshot existing shipping services
- [ ] Note what default shipping rate is currently shown
- [ ] Check if any product-specific rules already exist
- [ ] Verify delivery country settings (should be UK)

---

### Phase 2: Add Shipping Label to Coffee Products ⏸️ NOT YET DONE

**Two Options:**

#### Option A: Via WooCommerce Product Feed Plugin (PREFERRED)

1. **Install/Configure Product Feed Plugin:**
   - Plugin: WooCommerce Product Feed Manager or Google Listings & Ads
   - Navigate to: WooCommerce → Settings → Products

2. **Add Custom Attribute:**
   - For each coffee product (beans/ground coffee):
   - Add custom field: `shipping_label`
   - Value: `coffee`

3. **Bulk Edit (Recommended):**
   - Navigate to: Products → All Products
   - Filter: Category = "Coffee" (if available)
   - Select all coffee bean products
   - Bulk Actions → Edit
   - Add custom field: `shipping_label = coffee`

#### Option B: Via Product Feed CSV (Alternative)

1. **Export current product feed**
2. **Add column:** `shipping_label`
3. **Set value:** `coffee` for all coffee products
4. **Re-import feed** to Merchant Centre

**Verification:**
- [ ] Check feed diagnostics in Merchant Centre
- [ ] Confirm `shipping_label` field appears in product data
- [ ] Verify ~8 products show `shipping_label: coffee`

---

### Phase 3: Create Coffee Shipping Service in Merchant Centre ⏸️ NOT YET DONE

**Steps in Merchant Centre:**

1. **Navigate to Shipping Settings** (see Phase 1)

2. **Click "Add Shipping Service"** or "Create new service"

3. **Configure Service:**
   - **Service name:** `Coffee Shipping - £2.00`
   - **Country:** United Kingdom
   - **Currency:** GBP (£)
   - **Delivery time:** 2-3 business days (adjust as needed)

4. **Set Shipping Rate:**
   - **Rate type:** Flat rate
   - **Cost:** £2.00

5. **Apply to Products:**
   - **Product selection:** "Products with specific shipping labels"
   - **Shipping label:** `coffee`
   - This will apply to all products with `shipping_label = coffee`

6. **Additional Settings:**
   - **Minimum order value:** (leave blank for no minimum)
   - **Maximum order value:** (leave blank for no maximum)
   - **Order cutoff time:** (e.g., 3:00 PM for same-day processing)

7. **Save Service**

---

### Phase 4: Verify Other Products Have Correct Shipping

**Check Default Shipping Service:**
- What rate applies to equipment (grinders, kettles)?
- Is there a free shipping threshold?
- Are large items (furniture, lighting) configured separately?

**Recommended Structure:**
```
Shipping Services:
├── Coffee Shipping (£2.00)
│   └── Products with shipping_label = "coffee"
│
├── Small Items (£3.95 or actual rate)
│   └── Cups, accessories, stationery, etc.
│
├── Large Items (£5.95 or actual rate)
│   └── Grinders, kettles, furniture, lighting
│
└── Free Delivery (£0.00)
    └── Orders over £50 (if applicable)
```

---

### Phase 5: Test & Verify ⏸️ 24-48 HOURS AFTER IMPLEMENTATION

**Wait for Propagation:**
- Changes take **24-48 hours** to appear in Shopping ads
- Feed must refresh and be re-processed

**Verification Steps:**

1. **Check Merchant Centre Feed:**
   - Go to: Products → All products
   - Filter for coffee products
   - Verify `shipping_label: coffee` appears in product data

2. **Test Shopping Ads:**
   - Search Google Shopping for: "Dak coffee Godshot"
   - Check ad preview - should show "£2.00 delivery"
   - Test multiple coffee products

3. **Verify Asset Group Performance:**
   - Check Google Ads Performance Max campaign
   - Asset group: "Coffee Generic" (ID: 6491248230)
   - Monitor clicks/conversions after implementation

4. **Document Results:**
   - Screenshot before/after shipping rates
   - Note any products still showing incorrect rate
   - Check for Merchant Centre errors/warnings

---

## Alternative Implementation (If Shipping Labels Don't Work)

### Fallback Option: Product Category-Based Shipping

If shipping labels aren't supported or cause issues:

1. **Ensure coffee products are in correct category:**
   - Google product category: `Food, Beverages & Tobacco > Food Items > Coffee & Tea`

2. **Create shipping service:**
   - Apply to: "Products in specific categories"
   - Select: Food & Beverages → Coffee & Tea
   - Set £2.00 rate

**Downside:** May apply to tea/matcha if in same category

---

## Troubleshooting

### Issue: Shipping label doesn't appear in feed
**Solution:**
- Check product feed plugin settings
- Verify custom attributes are included in feed export
- May need to map `shipping_label` in feed configuration

### Issue: Shipping service not applying to products
**Solution:**
- Verify exact shipping label value matches (case-sensitive)
- Check country settings match (UK)
- Allow 24-48 hours for propagation

### Issue: Wrong products getting £2 shipping
**Solution:**
- Review which products have `shipping_label = coffee`
- Remove label from equipment/non-coffee items
- Create more specific labels if needed

---

## Questions for Client (BEFORE IMPLEMENTATION)

1. **Confirm scope:** Should tea/matcha also have £2 shipping, or only coffee beans?
2. **Equipment shipping:** What's the correct rate for coffee grinders, kettles, etc.?
3. **Free shipping threshold:** Is there a minimum order value for free delivery?
4. **Urgency:** Is this affecting sales significantly, or can we plan implementation carefully?
5. **Other products:** Any other product categories with incorrect shipping rates?

---

## Related Godshot Issues

**Context:** This shipping issue is separate from, but related to:

1. **Product ID mismatch** (80% attribution issue) - Product feed IDs don't match WooCommerce IDs
2. **Conversion tracking** - Plugin recently updated (Nov 10, 2025)
3. **Policy violations** - 10 products with disapproved titles

**Opportunity:** While accessing Merchant Centre for shipping, could also:
- Audit product feed structure and IDs
- Review disapproved products (if not already fixed)
- Check for other feed quality issues

---

## Success Criteria

✅ Coffee products show "£2.00 delivery" in Shopping ads
✅ Equipment products show correct (higher) shipping rate
✅ No Merchant Centre feed errors or warnings
✅ Coffee Generic asset group maintains/improves performance
✅ Client confirms shipping rates are now accurate

---

## Timeline

- **Phase 1-2:** 1-2 hours (Merchant Centre audit + WooCommerce setup)
- **Phase 3-4:** 30 minutes (Create shipping service)
- **Propagation wait:** 24-48 hours
- **Phase 5:** 30 minutes (Verification)
- **Total:** ~2-3 hours active work + 1-2 days wait time

---

## Next Actions

**IMMEDIATE (Today):**
- [ ] Get client confirmation on questions above
- [ ] Schedule implementation session (1-2 hours)
- [ ] Ensure access to Merchant Centre login

**IMPLEMENTATION SESSION:**
- [ ] Phase 1: Document current Merchant Centre setup
- [ ] Phase 2: Add `shipping_label = coffee` to products
- [ ] Phase 3: Create Coffee Shipping service in Merchant Centre
- [ ] Phase 4: Review other shipping services

**FOLLOW-UP (48 hours later):**
- [ ] Phase 5: Verify changes in Shopping ads
- [ ] Report results to client
- [ ] Update Godshot CONTEXT.md with final configuration

---

## Document History

| Date | Action | Status |
|------|--------|--------|
| 2025-11-17 | Investigation started - identified issue | ✅ Complete |
| 2025-11-17 | Coffee products identified (~8 SKUs) | ✅ Complete |
| 2025-11-17 | Implementation plan created | ✅ Complete |
| TBD | Phase 1-3 implementation | ⏸️ Pending |
| TBD | Phase 5 verification | ⏸️ Pending |

---

**Status:** ✅ Ready for implementation - awaiting Merchant Centre access and client confirmation
