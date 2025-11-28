# Product Disapproval Action Plan

**Date Created**: November 12, 2025
**Purpose**: Address existing critical disapprovals across all clients before implementing automated daily monitoring

---

## Executive Summary

**Total Clients Checked**: 15
**Clients with Critical Issues**: 4 (Smythson, Godshot, BrightMinds, Uno Lights)
**Clients with Minor Issues**: 5 (Accessories for the Home, Superspace, Crowd Control, Just Bin Bags, Tree2mydoor)
**Clients with No Issues**: 3 (Go Glean, Grain Guard, Just Bin Bags JHD)
**Clients with Expected Issues**: 3 (HappySnapGifts, WheatyBags, BMPM - adult/sensitive content)

---

## URGENT Priority - Action Required Immediately

### 1. Smythson UK - 1,615 Products Disapproved

**Impact**: ~1,500 products blocked from showing in Greece market

**Primary Issue**: Mismatched shipping currency for Greece
- **Issue Code**: `missing_shipping_mismatch_of_shipping_method_and_offer_currency`
- **Products Affected**: ~1,500 greeting cards and stationery items
- **Root Cause**: Shipping configuration for Greece requires GBP currency settings

**Action Items**:
1. Access Smythson Merchant Center (ID: 102535465)
2. Navigate to: Tools → Shipping and Returns
3. Check Greece shipping configuration:
   - Ensure shipping rates are configured in GBP (not EUR)
   - OR exclude Greece if not shipping there
4. **Expected Result**: ~1,500 products restored to Shopping ads for Greece

**Additional Issues Found**:
- Missing prices on greeting cards (~100 products)
  - **Action**: Check product feed for blank price fields
  - **Issue Code**: `missing_price_in_feed`
- Landing page errors on some products
  - **Action**: Review products with `landing_page_error` and fix URLs

**Estimated Impact**: HIGH - Restoring 1,500 products could significantly improve reach

---

## HIGH Priority - Action Required This Week

### 2. Godshot - 10 Products Disapproved (Policy Violations)

**Impact**: 10 premium products blocked due to policy violations

**Issue**: Product titles/descriptions triggering automated policy filters

**Products Affected**:

#### A. "19-69 Miami Blue EDP" (4 variants)
- **Current Title**: "19-69 Miami Blue EDP"
- **Policy Trigger**: "Miami Blue" flagged as illegal drugs reference
- **Issue Code**: `policy_violation_drugs`
- **Suggested Fix**: "19-69 Blue Fragrance EDP 30ml" (remove "Miami Blue")
- **Product IDs**: Check report for specific offer IDs

#### B. "A Matter of Concrete" Coffee
- **Current Title**: Contains "Concrete"
- **Policy Trigger**: "Concrete" flagged as guns/weapons (potentially "concealed" misread)
- **Issue Code**: `policy_violation_weapons`
- **Suggested Fix**: "A Matter of Coffee - Laurina3 Varietal"
- **Product IDs**: 1 product

#### C. "Haeckels Marine Facial Cleanser"
- **Current Title**: Contains "Facial Cleanser"
- **Policy Trigger**: Flagged as prescription drug
- **Issue Code**: `policy_violation_prescription_drug`
- **Suggested Fix**: Add "Skincare" qualifier: "Haeckels Marine Skincare Face Wash"
- **Product IDs**: 1 product

**Action Items**:
1. Review product feed and identify exact titles
2. Update product titles in WooCommerce/Shopify/feed system
3. Resubmit feed to Merchant Center
4. Request manual review if needed (Merchant Center → Needs Attention → Request Review)

**Note**: These are false positives - legitimate beauty/coffee products triggering automated filters. Title changes should resolve.

**Estimated Impact**: MEDIUM - 10 high-value products (fragrances/specialty coffee)

---

### 3. BrightMinds - 256 Products Disapproved

**Impact**: Products not showing in Free Listings (Shopping tab), only Paid Ads

**Primary Issue**: CSS (Comparison Shopping Service) not selected for Free Listings
- **Issue Code**: `css_not_selected_for_free_listings`
- **Products Affected**: Majority of disapprovals
- **Root Cause**: Free Listings destination requires CSS selection

**Action Items**:
1. Access BrightMinds Merchant Center (ID: 5291988198)
2. Navigate to: Growth → Manage Programs → Shopping Ads (Free Listings)
3. Select CSS provider (likely Google Shopping CSS)
4. Enable Free Listings destination for products

**Additional Issues**:
- Custom label formatting (`custom_label_2_does_not_have_valid_format`)
  - **Action**: Review custom_label_2 field format requirements
  - Check if using unsupported characters or format
- Landing page errors
  - **Action**: Identify products with 404/500 errors and fix URLs

**Estimated Impact**: MEDIUM-HIGH - Unlock free organic traffic via Shopping tab

---

### 4. Uno Lights - 32 Products Disapproved

**Impact**: LED lighting products blocked due to landing page errors

**Issue**: Landing page not working (404 errors or broken URLs)
- **Issue Code**: `landing_page_error`
- **Products Affected**: 32 LED products
- **Root Cause**: Product URLs returning errors when Google crawls

**Action Items**:
1. Access Uno Lights Merchant Center (ID: 513812383)
2. Export list of 32 disapproved products
3. Test each product URL:
   ```bash
   # Example
   curl -I [product-url]
   # Check for 200 OK vs 404 Not Found
   ```
4. Common fixes:
   - Update URLs in product feed if products moved
   - Fix broken website links/redirects
   - Restore product pages if accidentally deleted
   - Check for URL encoding issues

**Estimated Impact**: MEDIUM - 32 products blocked from showing

---

## MEDIUM Priority - Address Within 2 Weeks

### 5. Accessories for the Home - 39 Products Disapproved

**Issues**:

#### A. Invalid GTINs (15 products)
- **Issue Code**: `invalid_gtin`
- **Action**:
  - Check if GTINs are correct in product feed
  - If products don't have GTINs (handmade/custom), remove GTIN field entirely
  - Only include GTINs for products with manufacturer barcodes

#### B. Sexual Content Flags (24 products - "Body Vases")
- **Issue Code**: `policy_violation_adult_content`
- **Products**: Body-shaped vases flagged as sexual
- **Action**:
  - Review product images (ensure not explicit)
  - Update titles to emphasize "home decor" or "art vase"
  - Example: "Female Form Ceramic Vase" → "Abstract Art Ceramic Vase - Home Decor"
  - Request manual review if clearly not adult content

**Estimated Impact**: LOW-MEDIUM - Niche products, lower traffic

---

### 6. Superspace UK - 2 Products Disapproved

**Issue**: Price issues
- **Issue Code**: Likely `price_mismatch` or `missing_price`
- **Action**: Check 2 products in feed, ensure prices are:
  - Present and non-zero
  - Match landing page price
  - In correct currency (GBP)

**Estimated Impact**: LOW - Only 2 products

---

### 7. Crowd Control - 6 Products Disapproved

**Issue**: Price mismatches between feed and landing page
- **Issue Code**: `price_mismatch`
- **Action**:
  - Identify 6 products
  - Compare feed price to landing page price
  - Update feed to match current website price
  - OR update website if feed price is correct

**Estimated Impact**: LOW - Only 6 products

---

### 8. Just Bin Bags - 6 Products Disapproved

**Issue**: Landing page errors
- **Issue Code**: `landing_page_error`
- **Action**: Same as Uno Lights - test URLs and fix broken links

**Estimated Impact**: LOW - Only 6 products

---

## LOW Priority - Monitor but No Immediate Action

### 9. Tree2mydoor - 1 Product Disapproved

**Issue**: Tree named "Shirazz" flagged as alcohol
- **Issue Code**: `policy_violation_alcohol`
- **Product**: Ornamental tree variety named after wine grape
- **Action**:
  - Optional: Rename to "Ornamental Tree - Shirazz Variety"
  - OR: Leave as-is, acceptable loss (1 product out of thousands)

**Estimated Impact**: NEGLIGIBLE - False positive, 1 product

---

## ACCEPTABLE - No Action Required

These clients have disapprovals that are expected/acceptable based on their product catalog:

### 10. HappySnapGifts - 299 Products Disapproved

**Issue**: Adult content (novelty/rude gifts)
- **Reason**: Expected for this client's product line
- **Action**: None - these products are intentionally adult-themed

### 11. WheatyBags - 1 Product Disapproved

**Issue**: Sensitive content flag
- **Reason**: Minor flag, likely false positive
- **Action**: Monitor - no immediate action needed

### 12. BMPM - 23 Products Disapproved

**Issues**:
- Condom products (policy violation - expected)
- Missing shipping (technical issue)
- Sensitive content (expected for some products)

**Action**: Review missing shipping issues only, ignore policy flags on condoms

---

## CLEAN - No Issues

### 13. Go Glean UK - 0 Disapprovals ✅
### 14. Grain Guard - 0 Disapprovals ✅
### 15. Just Bin Bags JHD - 0 Disapprovals ✅

---

## Summary Action Checklist

### Immediate (This Week)
- [ ] **Smythson**: Fix Greece shipping configuration (1,500 products)
- [ ] **Godshot**: Rewrite 10 product titles to avoid policy triggers
- [ ] **BrightMinds**: Enable CSS for Free Listings (256 products)
- [ ] **Uno Lights**: Fix 32 landing page errors

### Short-term (Next 2 Weeks)
- [ ] **Accessories for the Home**: Fix 15 invalid GTINs, review 24 body vase titles
- [ ] **Superspace**: Fix 2 price issues
- [ ] **Crowd Control**: Fix 6 price mismatches
- [ ] **Just Bin Bags**: Fix 6 landing page errors
- [ ] **BMPM**: Review missing shipping on non-condom products

### Monitor Only
- [ ] **Tree2mydoor**: Consider renaming "Shirazz" tree (optional)
- [ ] **HappySnapGifts**: Track adult content disapprovals (no action)
- [ ] **WheatyBags**: Monitor sensitive content flag (no action)

---

## Next Steps

1. **Review this document** with client priority in mind
2. **Start with Smythson** (highest impact - 1,500 products)
3. **Address Godshot, BrightMinds, Uno Lights** (high-value products/traffic)
4. **Schedule medium-priority fixes** for following week
5. **After current issues resolved**: Implement automated daily monitoring to catch new disapprovals early

---

## Technical Details for Daily Monitoring Setup

Once current issues are addressed, implement daily monitoring with:

**Baseline Approach**:
- Take snapshot of current approval status for all products
- Store in `monitoring/disapprovals/baseline_{client}_YYYY-MM-DD.json`
- Daily comparison to detect approved → disapproved transitions

**Filtering Logic**:
- Only alert on `disapproved` status (not `unaffected` warnings)
- Only alert on Shopping Ads destination (ignore DisplayAds-only issues)
- Client-specific ignore rules:
  - HappySnapGifts: Ignore `policy_violation_adult_content`
  - BMPM: Ignore condom-related policy violations
  - All clients: Ignore `pending_initial_policy_review` (expected for new products)

**Integration**:
- Add to daily intel report as separate section: "Product Disapproval Alerts"
- Show NEW disapprovals only (approved yesterday → disapproved today)
- Include: Product ID, title, issue code, recommended action

---

**Document Status**: Active - Update as issues are resolved
**Owner**: Pete's Brain Product Impact Analyzer
**Last Updated**: November 12, 2025
