---
title: Shopify Plus Features and Capabilities (2025)
source: Shopify Plus Documentation + Industry Analysis
date_added: 2025-11-12
tags: [shopify-plus, enterprise, advanced-features, automation, wholesale]
---

## Summary

- Shopify Plus is enterprise-tier plan starting at $2,000/month (volume-based pricing)
- Key benefits: advanced automation, custom checkout, wholesale channel, priority support
- Designed for high-volume merchants (£1M+ annual revenue) or complex operations
- Access to Plus-exclusive features unavailable on standard Shopify
- Dedicated account management and technical support
- Justification threshold: typically £750k-1M+ annual revenue

## What is Shopify Plus?

**Shopify Plus** is Shopify's enterprise ecommerce platform designed for high-growth and high-volume merchants who require advanced features, customization, and scalability beyond standard Shopify plans.

**Pricing**: Starts at $2,000/month (flat rate) or 0.25% of sales (whichever is higher)
- Volume-based tiers unlock at higher revenue levels
- Negotiable for very large merchants (£10M+ annual revenue)
- Additional costs: Shopify Payments fees (same as regular), apps, development

**Target Customers**:
- High-volume merchants (1,000+ orders/month)
- Multi-store/multi-brand operations
- Wholesale + DTC businesses
- International expansion (multi-currency, multi-language)
- Complex workflows requiring automation

## Plus-Exclusive Features

### 1. Shopify Flow (Automation Platform)

**What it is**: Visual workflow automation builder (no code required)

**Use Cases**:
- **Inventory management**: Auto-tag low-stock products, notify buyers
- **Customer segmentation**: Auto-tag VIP customers based on spend
- **Fraud detection**: Flag suspicious orders for manual review
- **Order management**: Auto-fulfill specific products, split orders by location
- **Product management**: Auto-publish products when inventory arrives

**Example Workflows**:
```
When: Customer lifetime value > £5,000
Then: Add tag "VIP", send Slack notification to account manager

When: Product inventory < 10 units
Then: Add tag "Low Stock", hide from Google Shopping feed

When: Order value > £1,000 AND first-time customer
Then: Flag for fraud review, delay fulfillment 24 hours
```

**Advantages**:
- Saves hours of manual work weekly
- Reduces human error
- Scales operations without hiring
- Connects to 100+ apps via integrations

### 2. Launchpad (Campaign Automation)

**What it is**: Automate product launches, sales, and flash events

**Key Features**:
- **Scheduled events**: Product releases, sales start/end, theme changes
- **Price changes**: Bulk price updates on schedule
- **Inventory releases**: Gradually release stock (artificial scarcity)
- **Theme switching**: Switch between sale and regular themes automatically
- **Scripts**: Activate Shopify Scripts on schedule

**Use Cases**:
- Black Friday/Cyber Monday sales (auto-start at midnight)
- Limited edition product drops (auto-publish at launch time)
- Flash sales (24-hour sale auto-starts and auto-ends)
- Seasonal catalog updates (summer collection replaces spring)

**Example**:
```
Black Friday Event (scheduled):
- 12:00 AM Nov 29: Activate "Black Friday" theme
- 12:00 AM Nov 29: Apply 20% discount via script to all products
- 12:00 AM Nov 29: Publish "Black Friday Deals" collection
- 11:59 PM Nov 29: Revert to standard theme
- 11:59 PM Nov 29: Remove discounts
```

### 3. Custom Checkout Customization

**What you can customize**:
- Add custom fields (gift messages, delivery instructions)
- Modify checkout layout and design (limited to Shopify's structure)
- Add upsells and cross-sells at checkout
- Custom discount logic via Shopify Scripts
- Checkout extensibility (apps can modify checkout)

**Use Cases**:
- Gift message collection
- Delivery date selection
- Subscription product additions
- "Add gift wrapping for £5" upsell
- Corporate purchase order field (B2B)

**Limitations**:
- Can't completely rebuild checkout (security/compliance reasons)
- Must follow Shopify's checkout structure
- PCI compliance requirements limit some modifications

### 4. Shopify Scripts (Checkout Customization Logic)

**What they are**: Ruby-based scripts that run at checkout to modify cart behavior

**Script Types**:
- **Line item scripts**: Modify products in cart (bundling, discounts)
- **Shipping scripts**: Custom shipping rate logic
- **Payment scripts**: Hide/show payment methods conditionally

**Use Cases**:
- **Volume discounts**: "Buy 3, get 10% off"
- **Bundling discounts**: "Buy product A + B, save £10"
- **Shipping logic**: "Free shipping for orders >£50 to UK only"
- **Payment rules**: "Hide COD for orders >£500"
- **Tiered pricing**: Different prices for wholesale customers

**Example Script** (Volume Discount):
```ruby
# Buy 3+ of same product, get 10% off
Input.cart.line_items.each do |line_item|
  if line_item.quantity >= 3
    discount = line_item.line_price * 0.10
    line_item.change_line_price(line_item.line_price - discount, message: "10% volume discount")
  end
end

Output.cart = Input.cart
```

### 5. Wholesale Channel (B2B)

**What it is**: Separate storefront for wholesale/B2B customers with custom pricing

**Key Features**:
- Separate wholesale catalog (hidden from retail site)
- Custom pricing per customer or customer tag
- Minimum order quantities
- Payment terms (Net 30, Net 60)
- Volume/tiered pricing
- Draft order creation tools

**Use Cases**:
- Manufacturers selling to retailers + direct to consumers
- Distributors with trade customers
- Brands with retail partners
- B2B + B2C hybrid businesses

**Workflow**:
1. Create wholesale customer accounts
2. Set wholesale prices (per product or via price lists)
3. Customers log in to see wholesale prices
4. Place orders at wholesale rates
5. Fulfill as normal orders

**Advantages vs. Separate Store**:
- Single inventory pool
- Unified order management
- One platform to manage
- Simplified accounting and reporting

### 6. Unlimited Staff Accounts

**Standard Shopify**: Limited staff accounts (5 on Advanced, 15 on Shopify)
**Shopify Plus**: Unlimited staff accounts

**Use Cases**:
- Large teams (customer service, fulfillment, marketing, development)
- Multiple departments need access
- Agency partners need access (developers, marketers)
- Seasonal staff (don't need to remove and re-add)

**Permissions**:
- Granular permissions control (Orders, Products, Customers, Reports, etc.)
- Custom staff roles
- Location-specific access (multi-warehouse operations)

### 7. Expanded API Limits

**Standard Shopify**: 2 requests/second API rate limit
**Shopify Plus**: 4 requests/second (2x higher)

**Why it matters**:
- Custom integrations run faster
- ERP/WMS systems sync more efficiently
- Headless commerce builds perform better
- Real-time inventory sync with multiple channels

### 8. Plus Partner Support

**Dedicated Support**:
- Named Merchant Success Manager (account manager)
- Priority technical support (faster response times)
- Access to Plus Community (peer network)
- Quarterly business reviews
- Launch management for big events

**Plus Partner Network**:
- Access to certified Shopify Plus agencies
- Vetted developers and strategists
- Migration specialists
- Custom development partners

### 9. Multi-Store Management (Shopify Organizations)

**What it is**: Manage multiple Shopify stores under one organization

**Features**:
- Shared staff accounts across stores
- Centralized billing
- Unified reporting (cross-store analytics)
- Transfer products/data between stores
- Manage multiple brands from one dashboard

**Use Cases**:
- Multi-brand businesses (different brands, separate stores)
- Multi-region stores (UK store, US store, EU store)
- DTC + wholesale (separate storefronts)
- Testing/staging environments

### 10. Advanced Reporting

**Custom Reports**:
- Build custom reports with any data combination
- Export to CSV for external analysis
- Schedule automated reports (email delivery)
- Cross-store reporting (Organizations feature)

**Enhanced Data Access**:
- Longer data retention (compared to standard Shopify)
- More granular metrics
- Custom segmentation
- Real-time reporting

## When to Upgrade to Shopify Plus

### Financial Justification

**Break-even analysis**:
- Shopify Plus: $2,000/month = $24,000/year
- Need to justify $24k in additional value vs. Advanced Shopify ($399/month)
- Difference: $19,200/year

**Ways to justify**:
- **Increased conversion**: 1% conversion lift = £19,200+ additional revenue (on £2M annual)
- **Time savings**: Automation saves 20 hours/month = £9,600/year (at £40/hour)
- **Wholesale channel**: B2B sales justify the expense
- **Multi-store efficiency**: Managing 2+ stores without Plus is painful
- **Development needs**: Custom checkout, scripts unlock growth opportunities

### Indicators You Need Plus

**Volume Indicators**:
- 1,000+ orders per month
- £1M+ annual revenue
- £750k+ revenue if growing fast (50%+ YoY)
- 10,000+ products
- Multiple sales channels (DTC + wholesale + marketplaces)

**Operational Indicators**:
- Need for automation (manual processes don't scale)
- Custom checkout requirements (gift messages, custom fields)
- Wholesale business alongside DTC
- International expansion (multi-currency, multi-language)
- High-stakes product launches (need Launchpad)
- Complex discount logic (Scripts required)

**Team Indicators**:
- Need for 15+ staff accounts
- Multiple agencies/contractors need access
- Separate fulfillment team needs permissions
- Customer service team growing beyond standard limits

## Shopify Plus vs. Standard Shopify Comparison

| Feature | Shopify Advanced | Shopify Plus |
|---------|-----------------|--------------|
| **Pricing** | £299/month | $2,000+/month |
| **Transaction fees** (non-Shopify Payments) | 0.5% | 0.15% |
| **Staff accounts** | 15 | Unlimited |
| **Locations** | 1,000 | 1,000 |
| **API rate limit** | 2 req/sec | 4 req/sec |
| **Shopify Flow** | ❌ | ✅ |
| **Launchpad** | ❌ | ✅ |
| **Custom checkout** | Limited | Advanced |
| **Shopify Scripts** | ❌ | ✅ |
| **Wholesale channel** | ❌ | ✅ |
| **Multi-store orgs** | ❌ | ✅ |
| **Dedicated support** | Standard | Priority + Account Manager |
| **Custom reports** | Basic | Advanced |

## Migration from Standard to Plus

**Migration Process**:
1. **Consultation**: Meet with Shopify Plus team
2. **Onboarding**: Account manager assigned
3. **Technical setup**: Plus features enabled
4. **Data migration**: Automatic (no downtime)
5. **Launch**: Store remains live throughout

**Timeline**: 2-4 weeks from signup to full onboarding

**No downtime**: Store continues operating during migration

**Data preserved**: All products, customers, orders transfer automatically

## Cost-Benefit Analysis Example

**Scenario**: £2M annual revenue Shopify merchant considering Plus

**Current costs (Advanced Shopify)**:
- Plan: £299/month × 12 = £3,588/year
- Apps: £200/month × 12 = £2,400/year
- Manual work: 40 hours/month × £40/hour × 12 = £19,200/year
- **Total**: £25,188/year

**Plus costs**:
- Plan: $2,000/month × 12 = $24,000/year (£18,720 at 1.28 exchange)
- Apps: £200/month × 12 = £2,400/year (same apps)
- Automation savings: 30 hours/month automated = -£14,400/year saved
- **Net cost**: £6,720/year

**Plus benefits**:
- Automation saves 30 hours/month = £14,400/year
- Wholesale channel adds £200k revenue = £40k profit (20% margin)
- Checkout optimization improves conversion 0.5% = £10k additional profit
- **Total benefit**: £64,400/year

**Net benefit**: £64,400 - £6,720 net cost = £57,680/year positive ROI

## Key Insights

1. **Plus is for growth-stage businesses**: Below £750k revenue, standard Shopify usually sufficient
2. **Automation is the killer feature**: Shopify Flow alone can justify the investment
3. **Wholesale changes economics**: B2B + DTC hybrid businesses benefit immediately
4. **Custom checkout enables optimization**: Scripts and checkout customization unlock conversion gains
5. **Multi-store management is game-changing**: Managing 2+ stores without Plus is operationally painful
6. **Support quality matters at scale**: Dedicated account manager valuable when revenue at stake
7. **API limits matter for integrations**: Custom builds and ERP systems need higher limits

## Common Questions

**Q: Can I negotiate Plus pricing?**
A: Yes, at higher revenue levels ($10M+) pricing is negotiable.

**Q: Can I downgrade from Plus?**
A: Yes, but you lose Plus-exclusive features (Flows will stop, Scripts disabled, etc.).

**Q: Do I need a developer for Plus?**
A: Not required, but recommended for Scripts and advanced customizations.

**Q: Is Plus worth it for small businesses?**
A: Rarely. Unless you have specific needs (wholesale, complex automation), wait until £1M+ revenue.

**Q: Can I trial Plus before committing?**
A: Shopify offers consultations and demos, but no free trial of Plus features.

## Resources

- [Shopify Plus Official Page](https://www.shopify.com/plus)
- [Shopify Plus Pricing](https://www.shopify.com/plus/pricing)
- [Shopify Flow Documentation](https://help.shopify.com/en/manual/apps/flow)
- [Shopify Scripts Documentation](https://help.shopify.com/en/manual/checkout-settings/script-editor)
- [Plus Partner Directory](https://www.shopify.com/plus/partners)
