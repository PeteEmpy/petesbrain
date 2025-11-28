# Product Hero - Knowledge Base

Product Hero is a Shopify app that provides automated product performance classification and campaign segmentation for Google Shopping and Performance Max campaigns.

**Official Website:** https://www.producthero.com/
**Help Center:** https://helpcenter.producthero.com/

---

## Overview

Product Hero automatically classifies products into performance tiers (Heroes, Sidekicks, Villains, Zombies) based on revenue, conversion rate, and other metrics. These labels sync to Google Merchant Center custom labels, enabling performance-based campaign segmentation.

### ROK Clients Using Product Hero

**PRO Plan (€30/month):**
- **Go Glean** (Customer ID: 8492163737)
  - Labels: Heroes & Sidekicks & Zombies, Villains
  - Industry: Building materials (grout products)
  - Strategy: Performance-based segmentation with grout vs non-grout split

- **Grain Guard** (Customer ID: 4391940141)
  - Labels: Heroes & Sidekicks, Villains
  - Industry: Wood care products
  - Strategy: Performance-based segmentation for new account

- **Crowd Control** (Customer ID: 9385103842)
  - Labels: Heroes & Sidekicks, Villains, Zombies
  - Industry: Safety/security equipment (crowd control barriers)
  - Strategy: Full 3-tier segmentation with all label types

**Common Owner:** Connor Heaps owns Go Glean and Grain Guard (managed by Peter Empson)

---

## Core Features

### 1. Labelizer (Automatic Performance Labels)

**How it works:**
- Analyzes product performance data (revenue, conversions, CTR, ROAS)
- Automatically classifies products into performance tiers
- Syncs labels to Google Merchant Center custom labels
- Updates labels dynamically as performance changes

**Label Tiers:**
- **Heroes**: Top revenue generators (typically top 20% of products)
- **Sidekicks**: Good converters needing more visibility
- **Villains**: Underperformers with optimization potential
- **Zombies**: Very poor performers (no conversions, low impressions)

**Campaign Application:**
- Separate campaigns per label tier
- Higher budgets and ROAS targets for Heroes
- Lower targets or optimization focus for Villains
- Pause or exclude Zombies

### 2. Manual Tagging (PRO Plan)

**How it works:**
- Create custom, static product tags for any segmentation strategy
- Apply tags in bulk via filters, checkboxes, or individual products
- Sync tags to Google Merchant Center custom labels
- Use tags for seasonal, clearance, or custom campaign segmentation

**See full documentation:** [manual-tagging-feature.md](manual-tagging-feature.md)

---

## Available Documentation

### Features & Functionality
- [Manual Tagging Feature](manual-tagging-feature.md) - Static custom tags for seasonal and custom campaigns (PRO Plan)

### Coming Soon
- Labelizer Configuration Guide
- Product Hero + Google Merchant Center Integration
- Campaign Structure Best Practices
- Performance Monitoring & Label Transitions
- Multi-dimensional Segmentation Strategies

---

## Quick Reference

### Plan Levels
- **Free**: Basic product classification
- **Basic**: Enhanced features (€X/month)
- **PRO**: Full features including manual tagging (€30/month)

### Custom Label Usage (Typical ROK Setup)
- `custom_label_0`: Labelizer label (Heroes, Sidekicks, Villains, Zombies) - **Dynamic**
- `custom_label_1`: Available for additional segmentation
- `custom_label_2`: Available for additional segmentation
- `custom_label_3`: Available for additional segmentation
- `custom_label_4`: Manual tags (seasonal, clearance, etc.) - **Static**

### Integration Points
- **Shopify**: App installed in Shopify store
- **Google Merchant Center**: Labels sync via supplemental feed
- **Google Ads**: Labels used in Shopping/PMax product group filters

---

## Related Knowledge Base Articles

### Google Ads Campaign Structure
- See `roksys/knowledge-base/google-ads/shopping/` for Shopping campaign best practices
- See `roksys/knowledge-base/google-ads/performance-max/` for PMax optimization guides

### Google Merchant Center
- See `roksys/knowledge-base/shopify/product-feeds/` for feed management
- See `roksys/knowledge-base/analytics/` for custom label tracking

### Client Context
- See `clients/go-glean/CONTEXT.md` for Product Hero usage in building materials
- See `clients/grain-guard/CONTEXT.md` for wood care product segmentation
- See `clients/crowd-control/CONTEXT.md` for safety equipment campaigns

---

## Document History

| Date | Change Made | Updated By |
|------|-------------|------------|
| 2025-11-14 | Initial creation with Manual Tagging Feature documentation | Claude Code |

---

## Contributing

When adding new Product Hero documentation:

1. Create markdown file in this directory
2. Use consistent frontmatter (title, source, date_added, tags)
3. Update this README with link to new article
4. Cross-reference with relevant client CONTEXT.md files
5. Include practical ROK strategy applications and examples

**Contact:** Peter Empson - petere@roksys.co.uk
