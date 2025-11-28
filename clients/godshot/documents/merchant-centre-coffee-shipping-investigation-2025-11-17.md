# Godshot - Merchant Centre Coffee Shipping Investigation

**Date:** 2025-11-17
**Issue:** Coffee products showing incorrect delivery charge in Shopping ads
**Correct Rate:** £2.00 for coffee products
**Merchant Centre ID:** 5291405839

---

## Problem Statement

Client (Godshot) reports that when coffee products are advertised in Shopping ads, the delivery charge shown is incorrect. Coffee products should show £2.00 delivery, but they're currently showing a different rate (likely default shipping rate for all products).

---

## Current Status: Investigation Phase

Need to access Merchant Centre to check current shipping configuration.

---

## Where to Check Shipping Settings

**Merchant Centre Location:**
1. Go to: https://merchants.google.com/
2. Select Godshot account (5291405839)
3. Navigate to: **Growth** → **Manage programs** → **Shopping ads** → **Delivery**
4. Or: **Tools** → **Shipping and returns** → **Shipping**

---

## Likely Root Causes

### Scenario 1: Single Default Rate
- All products using same shipping rate (e.g., £3.95 or free delivery threshold)
- Coffee needs separate £2 rate but not configured

### Scenario 2: Weight-Based Shipping
- Shipping calculated by weight
- Coffee (250g bags) might be in wrong weight bracket

### Scenario 3: No Product-Specific Rules
- Generic shipping applies to everything
- Coffee needs its own shipping rule/service

---

## Solution Options

### ✅ Option 1: Use Shipping Labels (RECOMMENDED)

**Step 1: Add shipping label to coffee products**
- In WooCommerce or product feed, add custom attribute: `shipping_label = "coffee"`
- Apply to all coffee products (beans, ground coffee, matcha, tea)
- Products affected: Dak Coffee, A Matter of Concrete, Friedhats, Bonanza, etc.

**Step 2: Create shipping service in Merchant Centre**
- Go to Shipping settings
- Create new shipping service: "Coffee Shipping - £2"
- Set flat rate: £2.00
- Under "What products does this apply to?" → **"Products with specific shipping labels"**
- Enter shipping label: `coffee`

**Pros:**
- Most flexible and accurate
- Easy to maintain (just tag products)
- Scales well if product range changes

**Cons:**
- Requires feed update with shipping_label attribute
- 24-48 hour delay for feed refresh

---

### Option 2: Use Product Categories

**If coffee products are in specific category:**
- Create shipping service in Merchant Centre
- Set £2 flat rate
- Apply to: **"Products in specific categories"**
- Select: "Food & Beverages > Beverages > Coffee & Tea"

**Pros:**
- No feed changes needed if categories already correct
- Quick to implement

**Cons:**
- Less granular control
- May catch non-coffee products in same category

---

### Option 3: Use Product Types

**If coffee products have consistent product_type in feed:**
- Create shipping service
- Apply to specific product types
- Set £2 rate

---

## Recommended Configuration for Godshot

Based on product range (coffee + homeware + lifestyle):

```
Shipping Services:
├── Coffee Shipping (£2.00)
│   └── Products with shipping_label = "coffee"
│
├── Small Items (£3.95)
│   └── Cups, accessories, stationery, etc.
│
├── Large Items (£5.95)
│   └── Grinders, kettles, furniture, lighting
│
└── Free Delivery (£0.00)
    └── Orders over £50
```

---

## Implementation Steps

### Step 1: Audit Current Setup
- [ ] Access Merchant Centre (5291405839)
- [ ] Review existing shipping services
- [ ] Identify which shipping rate coffee currently shows
- [ ] Check product feed structure (categories, product_type, custom attributes)

### Step 2: Choose Implementation Method
- [ ] Decide: Shipping labels vs Categories vs Product types
- [ ] Document decision rationale

### Step 3: Update Product Feed (if using shipping labels)
- [ ] Add `shipping_label` attribute to coffee products in WooCommerce
- [ ] Verify feed includes shipping_label field
- [ ] Wait for feed refresh (24-48 hours)

### Step 4: Configure Merchant Centre
- [ ] Create "Coffee Shipping" service
- [ ] Set £2.00 flat rate
- [ ] Apply to coffee products (via chosen method)
- [ ] Save and activate

### Step 5: Verify
- [ ] Wait 24-48 hours for changes to propagate
- [ ] Search for Godshot coffee on Google Shopping
- [ ] Check "Delivery" shown in ad preview
- [ ] Confirm shows "£2.00 delivery"
- [ ] Test with multiple coffee products

---

## Next Steps

### Immediate Actions:
1. **Access Merchant Centre** - Log in and review current shipping configuration
2. **Document current setup** - Screenshot existing shipping services
3. **Identify coffee products** - List all SKUs that need £2 shipping
4. **Check feed structure** - Determine if shipping labels already exist or need adding

### Decision Required:
- Which implementation method to use (shipping labels recommended)
- Whether to update other product shipping rates at same time
- Timeline for implementation (immediate vs. coordinated with other changes)

---

## Alternative: Check via WooCommerce MCP

We have WooCommerce MCP access for Godshot. Could use to:
- View current product structure
- Check if products have shipping classes
- Identify coffee product IDs
- See current shipping settings in WooCommerce

---

## Questions for Client

1. Are there other products besides coffee beans that should have £2 shipping? (e.g., tea, matcha?)
2. What's the current default shipping rate being shown?
3. Is this urgent (affecting sales) or can we plan implementation?
4. Do they want to review full shipping structure or just fix coffee?

---

## Technical Notes

**Coffee Products in Godshot Catalog:**
- Dak Coffee (Milky Cake, Cream Donut, Yuzu Crew, etc.)
- A Matter of Concrete coffee
- Friedhats coffee
- Bonanza coffee
- Various European roasters (Three Marks, Manhattan, Prolog, etc.)
- Estimated: 30-50 SKUs

**Current Feed Configuration:**
- Platform: WooCommerce with Savoy theme
- Product feed likely generated by WooCommerce Google Listings & Ads plugin
- Feed ID structure: Custom IDs (e.g., 21857) separate from WooCommerce IDs

---

## Related Issues

**Known Godshot Technical Issues:**
1. Product ID mismatch between feed and WooCommerce (80% attribution mismatch)
2. Conversion tracking plugin recently updated (Nov 10, 2025)
3. Policy violations on 10 products (title issues)

This shipping issue is separate but could be part of broader Merchant Centre audit.

---

## Status: PAUSED - Awaiting Claude Code Reboot

**Resume by:**
1. Read this document
2. Access Merchant Centre to check current configuration
3. Document findings
4. Implement chosen solution
5. Verify results

**Key Context:**
- Client: Godshot (Sam)
- Merchant Centre: 5291405839
- Issue: Coffee products need £2 shipping shown in ads
- Current charge: Unknown (need to check)
- Recommended fix: Shipping labels method
