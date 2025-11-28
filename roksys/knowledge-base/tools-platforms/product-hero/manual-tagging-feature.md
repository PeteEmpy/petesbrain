---
title: Product Hero Manual Tagging Feature
source: https://helpcenter.producthero.com/en/articles/12783004-manual-tagging
date_added: 2025-11-14
category: tools-platforms
tags: [product-hero, product-segmentation, google-merchant-center, campaign-optimization, pro-plan]
plan_level: PRO Plan Only
---

## Summary

Product Hero's Manual Tagging feature allows merchants to create **static, custom product tags** for campaign segmentation beyond the automated Labelizer system (Heroes, Sidekicks, Villains, Zombies). This PRO plan feature enables bulk tagging for seasonal promotions, stock clearance, bestseller highlighting, and custom product groupings that sync to Google Merchant Center custom labels.

**Key Distinction:** Manual tags are **static** (require manual updates) vs. Labelizer labels which are **dynamic** (automatically update based on performance).

---

## Feature Overview

### What It Does
- Create custom product tags for any segmentation strategy
- Apply tags in bulk across multiple products
- Sync tags to Google Merchant Center via custom labels
- Use tags for campaign segmentation in Google Ads Shopping and Performance Max

### Common Use Cases
1. **Seasonal Campaigns**: Tag products for Black Friday, Christmas, Valentine's Day, etc.
2. **Stock Clearance**: Identify products for end-of-season sales or inventory reduction
3. **Bestseller Promotion**: Highlight top-performing products for special campaigns
4. **New Product Launches**: Group new arrivals for dedicated promotion
5. **Custom Segmentation**: Create any business-specific groupings (e.g., "gift items", "trade products", "eco-friendly")
6. **Complementary to Labelizer**: Use alongside Heroes/Villains labels for multi-dimensional segmentation

---

## Technical Specifications

### Plan Requirements
- **PRO Plan Only** (€30/month)
- Not available in Free or Basic plans

### Tag Limitations
- **One tag per product** (mutually exclusive)
- Tags are **static values** (do not auto-update)
- Manual intervention required to change or remove tags
- Cannot have multiple tags on the same product simultaneously

### Integration Requirements
1. Tags must be assigned to an **empty custom label** in Google Merchant Center
2. **Do NOT overwrite** existing Labelizer labels (custom_label_0 through custom_label_4)
3. Use a supplemental feed to populate the custom label
4. Expect delays: Product Hero → GMC → Google Ads (can take hours)

---

## Three Methods to Apply Tags

### 1. Manual Selection (Checkbox Method)
**Best for:** Small, specific product groups

**How it works:**
- Navigate to Product Hero product overview
- Select products using checkboxes
- Options:
  - Select individual products
  - Select all products on current page (up to 15)
  - Select all available products (bulk operation)
- Apply tag to selected products

**Use case example:** Manually tag 5 specific bestselling products for a "Featured Collection" campaign

### 2. Filter-Based Tagging (Bulk Automation)
**Best for:** Large product groups matching specific criteria

**Available filters:**
- Product groups
- Labelizer labels (Heroes, Sidekicks, Villains, Zombies)
- Brands
- Categories
- Product types
- Previously edited products
- Existing tags

**How it works:**
1. Apply filters to identify target products
2. Select all filtered products
3. Apply tag in bulk

**Use case examples:**
- Tag all "Villains" products as "Clearance" for end-of-season sale
- Tag all products in "Winter Collection" category as "Seasonal"
- Tag all products from "Brand X" for brand-specific campaign

**ROK Strategy Application:**
- Combine Labelizer labels with manual tags for multi-dimensional segmentation
- Example: Tag "Villains" products as "Clearance" while keeping Labelizer label for performance tracking

### 3. Product-Level Entry (Individual Tagging)
**Best for:** One-off tagging or spreadsheet-style editing

**How it works:**
- Navigate to product details
- Enter tag value directly into the tag column
- Save changes

**Use case example:** Quickly tag a single new product as "New Arrival"

---

## Google Merchant Center Integration

### Setup Workflow

1. **Create Tags in Product Hero**
   - Choose one of three methods above
   - Apply tags to products

2. **Assign to Empty Custom Label**
   - Select an unused custom label (e.g., custom_label_4)
   - **Critical:** Do NOT overwrite Labelizer labels (typically custom_label_0 to custom_label_3)
   - Assign Product Hero manual tags to the empty label

3. **Configure Supplemental Feed**
   - Product Hero generates supplemental feed
   - Feed populates the chosen custom label with tag values
   - Feed syncs to Google Merchant Center

4. **Wait for Propagation**
   - **Product Hero → GMC**: Can take several hours
   - **GMC → Google Ads**: Additional delay (hours to 24+ hours)
   - Check GMC "Products" tab to verify tag values appear

5. **Verify in Google Ads**
   - Navigate to campaign > Products > Product Groups
   - Check that custom label values appear in listing group filters
   - Values should match tags created in Product Hero

### Custom Label Best Practices

**Typical ROK Setup:**
- `custom_label_0`: Labelizer label (Heroes, Sidekicks, Villains, Zombies)
- `custom_label_1`: Unused or other segmentation
- `custom_label_2`: Unused or other segmentation
- `custom_label_3`: Unused or other segmentation
- `custom_label_4`: **Manual tags** (seasonal, clearance, etc.)

**Why this matters:**
- Labelizer labels auto-update (dynamic)
- Manual tags are static (require updates)
- Mixing them in the same label would cause conflicts

---

## Google Ads Campaign Implementation

### Campaign Segmentation Strategy

**Use tags in listing group filters** to segment products within Shopping and Performance Max campaigns:

1. **Create Product Groups by Tag**
   - In campaign settings, navigate to product groups
   - Add subdivision by custom_label_4 (or whichever label holds tags)
   - Create groups for each tag value (e.g., "Seasonal", "Clearance", "Bestsellers")

2. **Set Distinct Strategies per Tag**
   - **Budget allocation**: Allocate more budget to high-priority tags
   - **Bid adjustments**: Increase bids for "Bestsellers", decrease for "Clearance"
   - **ROAS targets**: Set aggressive targets for profitable tags, lower for clearance

3. **Exclusion Logic (Critical)**
   - Ensure products don't compete across multiple campaigns
   - Example: If "Seasonal" products are in dedicated campaign, exclude them from "Catch All" campaign
   - Use negative product groups or campaign priorities to prevent overlap

### Example Campaign Structure

**Scenario:** E-commerce store with seasonal Christmas products

**Product Hero Setup:**
- Tag 150 Christmas products as "Christmas"
- Assign to custom_label_4
- Sync to Google Merchant Center

**Google Ads Setup:**
1. **Campaign 1: Christmas PMax**
   - Product group filter: custom_label_4 = "Christmas"
   - Budget: £100/day
   - Target ROAS: 200%
   - Focus: Maximize seasonal sales

2. **Campaign 2: Catch All PMax**
   - Product group filter: custom_label_4 ≠ "Christmas" (exclude Christmas products)
   - Budget: £50/day
   - Target ROAS: 250%
   - Focus: Maintain baseline performance

**Result:** Christmas products get dedicated budget and strategy without competing with general inventory

---

## Manual Tags vs. Labelizer Labels

### When to Use Manual Tags

**Best for:**
- **Temporary campaigns**: Seasonal promotions, limited-time sales
- **Business-defined segments**: Custom groupings that don't align with performance
- **Stock management**: Clearance, overstock, pre-order
- **Marketing initiatives**: New arrivals, featured collections, gift guides

### When to Use Labelizer Labels (Heroes, Villains, etc.)

**Best for:**
- **Performance-based segmentation**: Automatically group by revenue, ROAS, conversion rate
- **Ongoing optimization**: Labels update automatically as performance changes
- **Budget allocation**: Invest more in Heroes, optimize Villains, pause Zombies
- **Permanent campaign structure**: Base campaigns on proven performance tiers

### Combining Both Systems (ROK Strategy)

**Multi-dimensional segmentation** for advanced campaign structures:

**Example 1: Seasonal + Performance**
- Labelizer: Heroes, Sidekicks, Villains, Zombies (custom_label_0)
- Manual tag: "Christmas" (custom_label_4)
- Campaign: "Christmas Heroes" (filter by BOTH labels)
- Strategy: Promote top-performing Christmas products with maximum budget

**Example 2: Clearance + Performance**
- Labelizer: Villains (underperformers)
- Manual tag: "Clearance"
- Campaign: "Clearance Villains"
- Strategy: Liquidate underperforming stock with low ROAS target

**Example 3: New Products + Performance Monitoring**
- Manual tag: "New Arrival" (initial 30 days)
- Labelizer: Automatically classifies as Hero/Villain based on performance
- Transition: Products move from "New Arrival" campaign to performance-based campaigns as data accumulates

---

## ROK Methodologies: Manual Tagging in Practice

### Connor Heaps Portfolio Strategy

**Current Setup (Go Glean, Grain Guard, Crowd Control):**
- Primary segmentation: Labelizer labels (Heroes & Sidekicks, Villains, Zombies)
- Secondary segmentation opportunity: Manual tags for seasonal/clearance

**Potential Applications:**

**Go Glean (Building Materials):**
- Manual tag: "Summer Patio" for seasonal grout products
- Labelizer: Heroes & Sidekicks & Zombies
- Campaign: "Summer Patio Heroes" (capitalize on strong summer performance noted in CONTEXT.md)

**Grain Guard (Wood Care):**
- Manual tag: "Spring Outdoor" for seasonal wood treatments
- Labelizer: Heroes & Sidekicks, Villains
- Campaign: Target spring DIY season with top performers

**Crowd Control (Safety Equipment):**
- Manual tag: "Event Season" for peak event products
- Labelizer: Heroes & Sidekicks, Villains, Zombies
- Campaign: Seasonal event campaign during festival/concert season

### Implementation Checklist

When implementing manual tagging for a client:

- [ ] Verify PRO plan active (€30/month)
- [ ] Identify empty custom label in GMC (typically custom_label_4)
- [ ] Define tagging strategy (seasonal, clearance, etc.)
- [ ] Apply tags using appropriate method (manual/filter/individual)
- [ ] Configure supplemental feed in Product Hero
- [ ] Verify tags appear in GMC (wait 2-24 hours)
- [ ] Verify tags appear in Google Ads product groups
- [ ] Create campaign structure using tag filters
- [ ] Set exclusion logic to prevent campaign overlap
- [ ] Document tag usage in client CONTEXT.md
- [ ] Plan tag refresh cadence (monthly, quarterly, seasonal)

---

## Limitations and Considerations

### Tag Management
- **Manual updates required**: Tags don't auto-update like Labelizer labels
- **One tag per product**: Cannot apply multiple tags simultaneously
- **No tag versioning**: Changing a tag requires manual re-tagging

### Propagation Delays
- **Product Hero → GMC**: Several hours typical
- **GMC → Google Ads**: Additional hours to 24+ hours
- **Plan ahead**: Apply tags at least 24-48 hours before campaign launch

### Custom Label Conflicts
- **Risk**: Overwriting Labelizer labels breaks performance-based segmentation
- **Solution**: Always use an empty custom label for manual tags
- **Verify**: Check GMC product data to confirm correct label assignment

### Maintenance Burden
- **Seasonal tags**: Require regular updates (e.g., remove "Christmas" tag in January)
- **Dynamic needs**: For changing segments, consider if Labelizer automation is better
- **Documentation**: Essential to track tag meanings and usage across campaigns

---

## Troubleshooting

### Tags Not Appearing in GMC

**Possible causes:**
1. Tag assigned to custom label already used by Labelizer
2. Supplemental feed not configured correctly
3. Propagation delay (wait 24 hours)
4. GMC account not linked to Product Hero

**Solutions:**
- Check Product Hero supplemental feed settings
- Verify empty custom label selected
- Wait 24-48 hours for propagation
- Re-sync feed manually in Product Hero

### Tags Not Appearing in Google Ads

**Possible causes:**
1. GMC hasn't synced to Google Ads yet (additional delay)
2. Products not approved in GMC (check product status)
3. Campaign not pulling from correct GMC feed

**Solutions:**
- Check GMC product status (approved/pending/disapproved)
- Verify campaign linked to correct GMC account
- Wait additional 24 hours after GMC verification
- Check campaign settings > Merchant Center feed

### Products in Wrong Campaigns

**Possible causes:**
1. Exclusion logic not configured
2. Multiple campaigns targeting same products without priorities
3. Tag values not mutually exclusive

**Solutions:**
- Add negative product groups to exclude tagged products from "Catch All"
- Set campaign priorities (High/Medium/Low) to control serving
- Review tag application to ensure clean segmentation

---

## Additional Resources

- **Product Hero Help Center**: https://helpcenter.producthero.com/en/articles/12783004-manual-tagging
- **Google Merchant Center Custom Labels**: https://support.google.com/merchants/answer/6324473
- **ROK Product Hero Clients**: Go Glean, Grain Guard, Crowd Control (all PRO plan)
- **Related Feature**: Labelizer (automatic performance-based labels)

---

## Document Metadata

**Created:** 2025-11-14
**Author:** Claude Code (ROK Systems)
**Version:** 1.0
**Status:** Active
**Next Review:** 2025-12-14 (1 month)

**Tags for Knowledge Base Search:**
- product-hero
- manual-tagging
- product-segmentation
- google-merchant-center
- campaign-structure
- seasonal-campaigns
- custom-labels
- shopping-campaigns
- performance-max
- pro-plan-features
