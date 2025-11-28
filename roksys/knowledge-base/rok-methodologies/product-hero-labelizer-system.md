# Product Hero Labelizer System - Core ROK Methodology

**Created:** 2025-10-31
**Status:** FOUNDATIONAL STRATEGY - Implemented across all e-commerce clients
**Platform:** [Product Hero](https://www.producthero.com/labelizer)

---

## Overview

The **Product Hero Labelizer** is the **foundational product segmentation methodology** used across all ROK e-commerce clients. It automatically classifies every product in a shopping feed into four performance-based categories (Heroes, Sidekicks, Villains, Zombies), enabling strategic budget allocation and campaign structure optimization.

**Core Purpose:** Regain control over Performance Max campaigns by guiding Google's algorithm toward high-performing products and away from budget-draining underperformers.

---

## The Four Product Classifications

### 1. Heroes ⭐
**Definition:** Top revenue generators - "Less than 10% of your products generate 80% or more of your revenue"

**Characteristics:**
- High conversion rates
- Strong revenue contribution
- Proven market demand
- Best-performing products in the catalog

**Strategic Treatment:**
- Maximum budget allocation
- Highest visibility in campaigns
- Dedicated asset groups or standalone campaigns
- Aggressive bidding to capture all available demand
- Premium ad placements

**Google Ads Implementation:**
- Separate PMax campaigns or asset groups
- Higher ROAS targets (can afford to be more selective)
- Best creative assets
- Priority in budget distribution

---

### 2. Sidekicks 🎯
**Definition:** Strong converters with insufficient visibility - "10% of your products convert well but are not getting enough impressions/clicks"

**Characteristics:**
- Good conversion rates when they get traffic
- Under-exposed in current campaign structure
- Revenue potential not being realized
- Often hidden behind Heroes in algorithm prioritization

**Strategic Treatment:**
- Increased budget allocation to boost visibility
- Promotional support to drive traffic
- Goal: Elevate to Hero status
- Test standalone campaigns or dedicated asset groups

**Google Ads Implementation:**
- Dedicated asset groups with increased budgets
- Lower ROAS targets initially (to increase volume)
- Strategic bid adjustments to increase impressions
- Monitor for promotion to Hero status

---

### 3. Villains 👎
**Definition:** Budget drainers with poor conversion - "50% of your budget goes to products that don't convert"

**Characteristics:**
- High click/impression volume
- Low or zero conversions
- Draining budget from better performers
- Often attractive in search but don't convert (wrong intent, pricing issues, etc.)

**Strategic Treatment:**
- Reduce or eliminate advertising spend
- Exclude from high-budget campaigns
- Investigate WHY they don't convert (pricing, product-market fit, listing quality)
- Consider pausing or removing from catalog

**Google Ads Implementation:**
- Separate low-budget "Villain" campaigns with very low ROAS targets
- Or exclude entirely from PMax campaigns
- Redirect budget to Heroes and Sidekicks
- Use as negative examples in optimization

---

### 4. Zombies 🧟
**Definition:** Dormant products with minimal visibility - "Over 60% of your products hardly get any impressions or clicks"

**Characteristics:**
- Little to no traffic
- Unknown conversion potential
- Hidden from algorithm
- May include seasonal products, new additions, or niche items

**Strategic Treatment:**
- Strategic reactivation with controlled budget
- Test market demand
- May reveal hidden gems (potential Sidekicks/Heroes)
- Seasonal Zombies may need periodic reactivation

**Google Ads Implementation:**
- Dedicated "Zombie activation" campaigns with modest budgets
- Test in small batches
- Monitor for performance signals
- Products that show promise → move to Sidekicks
- Products that continue to underperform → keep dormant or remove

---

## How Classification Works

### Daily Automated Analysis

The Product Hero platform performs **daily analysis** of product performance based on:

1. **Volume Metrics:**
   - Clicks
   - Impressions
   - Traffic patterns

2. **Performance Metrics:**
   - Conversions
   - Revenue contribution
   - Target ROAS achievement

3. **Relative Performance:**
   - Comparison to account averages
   - Historical performance trends
   - Category benchmarks

### Dynamic Labeling

**Products move between categories dynamically:**
- Zombie → Sidekick (when activation campaign reveals conversion potential)
- Sidekick → Hero (when visibility increase drives significant revenue)
- Hero → Sidekick (seasonal decline or market changes)
- Any → Villain (if conversion rate drops while maintaining clicks)

**No manual updates required** - the system automatically reassigns labels based on daily performance data.

---

## Integration with Google Ads

### Supplemental Feed Connection

Product Hero labels integrate with Google Merchant Center via **Supplemental Sources:**

1. **Product Hero generates labels** daily based on performance
2. **Labels sync to Google Merchant Center** as custom attributes
3. **Custom attribute used in campaigns** to segment products
4. **Google's algorithm adjusts bidding** based on segmentation signals

**Custom Attribute Field:**
- Attribute name: `custom_label_0` (or similar field)
- Values: `heroes`, `sidekicks`, `villains`, `zombies`

### Campaign Structure Options

**Option 1: Separate Campaigns by Label**
- Campaign 1: Heroes (high budget, high ROAS target)
- Campaign 2: Sidekicks (medium budget, lower ROAS to increase volume)
- Campaign 3: Villains (minimal budget or paused)
- Campaign 4: Zombies (test budget, activation strategy)

**Option 2: Asset Groups by Label** (within same PMax campaign)
- Asset Group: Heroes & Sidekicks
- Asset Group: Zombies (activation)
- Villains excluded from campaign

**Option 3: Hybrid Approach** (ROK Standard)
- Main PMax: Heroes & Sidekicks (combined or separate asset groups)
- Zombie Activation: Dedicated low-budget campaign
- Villains: Excluded entirely

---

## Implementation at ROK

### Standard Client Setup

**For all e-commerce clients:**

1. **Product Feed Analysis**
   - Connect client's Google Merchant Center feed to Product Hero
   - Historical performance analysis to establish baseline
   - Initial product classification

2. **Supplemental Feed Setup**
   - Product Hero creates supplemental feed with labels
   - Link supplemental feed to Google Merchant Center
   - Verify labels appear in product data

3. **Campaign Structure**
   - Restructure campaigns to align with labels
   - Typical structure:
     * Heroes & Sidekicks: Primary PMax campaign(s)
     * Furniture/Categories: Segmented by product type AND label
     * Zombies: Activation campaigns (seasonal or ongoing)
     * Villains: Excluded or minimal budget catch-all

4. **Ongoing Optimization**
   - Daily: Product Hero updates labels automatically
   - Weekly: Review classification changes
   - Monthly: Analyze transitions (which products moved categories)
   - Quarterly: Strategic review of overall catalog performance

---

## Case Study: Accessories for the Home

### Campaign Structure (Current)

**Campaign:** AFH | P Max | H&S Zombies Furniture
**Asset Groups:**
- Furniture - Heroes
- Furniture - Sidekicks
- Furniture - Zombies
- Competitors - All H&S
- H & S Wealthy
- Armchairs Sidekicks & Zombies
- Bar Stools - H & S
- Remarketing - Furniture Heroes & Sidekicks
- Remarketing H&S and Zombies Nkuku

**Issue Identified (Oct 2025):**
- "Furniture - Sidekicks" asset group experienced massive traffic spike (Oct 22-23)
- 9,555 clicks over 2 days vs normal ~50-100 clicks/day
- 0 conversions from spike traffic
- Root cause: Products labeled as "heroes" and "villains" incorrectly appearing in "sidekicks" asset group
- **This demonstrates why proper label filtering is critical**

**Correct Implementation:**
- Asset groups must have product filters matching custom_label_0 values
- Furniture - Heroes → filter: custom_label_0 = "heroes"
- Furniture - Sidekicks → filter: custom_label_0 = "sidekicks"
- Furniture - Zombies → filter: custom_label_0 = "zombies"

**Without proper filtering:** Google's algorithm can serve wrong products, leading to wasted spend and poor performance.

---

## Key Metrics & Expected Results

### Product Hero Platform Promises

**Average Performance Improvements:**
- 10-30% ROAS increase
- Cost reductions on underperformers
- Volume growth from activated Zombie products
- 25% average increase in ad performance (documented case studies)

### ROK Client Results

**[To be added as we compile client-specific results]**

**Monitoring Framework:**
- Compare pre-Labelizer vs post-Labelizer performance
- Track product transitions between categories
- Measure ROAS by label category
- Identify which Zombies successfully activated to Sidekicks/Heroes

---

## Critical Implementation Rules

### 1. **Asset Group Filtering is Mandatory**

**Always use product filters in asset groups:**
```
Asset Group: "Furniture - Heroes"
Product Filter: custom_label_0 = "heroes"
```

**Never rely on naming convention alone** - Google needs explicit filtering to prevent cross-contamination.

### 2. **Villain Handling**

**DO NOT mix Villains with Heroes/Sidekicks:**
- Villains drain budget from high performers
- Create separate low-budget campaign OR exclude entirely
- Investigate WHY products are Villains (pricing, quality, market fit)

### 3. **Zombie Activation Strategy**

**Controlled reactivation:**
- Dedicated budget (don't steal from Heroes)
- Test in batches (not all at once)
- Monitor for 14-30 days
- Products showing promise → move to Sidekicks
- Continued underperformers → pause or remove

### 4. **Label Trust**

**Product Hero's classifications are data-driven:**
- Don't override labels based on gut feeling
- Labels update daily based on actual performance
- If a "premium product" is labeled Villain, it means it's not converting - investigate why
- Trust the data, not assumptions

---

## Monthly Review Process

### 1st of Each Month - Labelizer Review

**What to Check:**

1. **Product Transitions**
   - Which products moved from Zombie → Sidekick?
   - Any Heroes that dropped to Sidekick?
   - New Villains to investigate?

2. **Category Distribution**
   - % of products in each label
   - % of budget spent by label
   - % of revenue by label

3. **Zombie Activation Results**
   - Which Zombies got traffic?
   - Any conversions from Zombie products?
   - Candidates for promotion to Sidekicks?

4. **Villain Analysis**
   - Why are Villains not converting?
   - Pricing issues? (check Price Benchmark tool)
   - Product listing quality issues?
   - Market demand mismatch?

5. **Campaign Structure Optimization**
   - Do asset group filters match labels correctly?
   - Budget allocation aligned with performance?
   - Any cross-contamination issues?

---

## Integration with Other ROK Tools

### Product Hero Platform Tools

**1. Labelizer** (Core - described in this document)

**2. Google CSS (Comparison Shopping Service)**
- 20% lower CPC compared to standard Google Shopping
- Alternative to Google's own CSS
- Works alongside Labelizer for cost reduction

**3. Products AI**
- Feed optimization with AI
- Bulk title optimization
- Improves product visibility

**4. Title Optimizer**
- Product title optimization for search
- Increases CTR and relevance

**5. Price Benchmark**
- Competitive pricing insights
- Identify Villains caused by pricing issues

**6. PMax Insights**
- Advanced Performance Max analytics
- Campaign performance analysis beyond Google Ads UI

### Integration with ROK Strategy Experiment System

**Complementary Systems:**

**Product Hero Labelizer:**
- Focus: Product-level performance classification
- Automated daily updates
- Guides campaign structure decisions

**ROK Strategy Experiments:**
- Focus: Strategic campaign-level changes
- Manual logging of tests and hypotheses
- Evaluates impact of structural changes

**Together:**
- Labelizer provides product segmentation framework
- Strategy Experiments test how to best leverage that framework
- Example: Test "Should Sidekicks be in same campaign as Heroes or separate?" → Log experiment, review results, document in Playbook

---

## Troubleshooting Common Issues

### Issue 1: Products in Wrong Asset Groups

**Symptoms:**
- Traffic spikes in unexpected asset groups
- Poor conversion rates from specific asset groups
- Budget waste

**Diagnosis:**
- Check asset group product filters
- Verify custom_label_0 values in Merchant Center
- Review Product Hero label assignments

**Fix:**
- Add explicit product filters: `custom_label_0 = "[label name]"`
- Verify supplemental feed is syncing correctly
- Check for Google Merchant Center processing delays

---

### Issue 2: Hero Products Not Getting Budget

**Symptoms:**
- Known best-sellers showing low impressions
- Budget going to lower-performing products
- ROAS declining

**Diagnosis:**
- Check if Heroes are in right campaign/asset group
- Verify budget allocation by campaign
- Review bid strategy settings

**Fix:**
- Ensure Heroes have dedicated high-budget campaign or asset group
- Increase campaign budget cap
- Consider standalone campaign for top Heroes

---

### Issue 3: Zombies Never Activate

**Symptoms:**
- Zombie products get no impressions even in activation campaign
- Budget not being spent

**Diagnosis:**
- Check product approval status in Merchant Center
- Verify products are in stock and active
- Review price competitiveness (Price Benchmark tool)
- Check search demand for products

**Fix:**
- Fix Merchant Center disapprovals
- Improve product titles (Title Optimizer tool)
- Adjust pricing if too high vs competitors
- Some Zombies may simply have no market demand → remove from catalog

---

### Issue 4: Too Many Villains

**Symptoms:**
- 40%+ of products labeled as Villains
- High click volume but low conversions across account

**Diagnosis:**
- Pricing issues (use Price Benchmark)
- Product listing quality (images, descriptions)
- Product-market fit (wrong products for your audience)
- Conversion tracking issues

**Fix:**
- Audit Villain products for common patterns
- Price adjustments where needed
- Improve product data quality
- Consider removing products with no conversion potential
- **Verify conversion tracking is working correctly first!**

---

## References & Resources

### Product Hero Platform
- **Main Site:** https://www.producthero.com
- **Labelizer Page:** https://www.producthero.com/labelizer
- **Help Center:** (linked from platform)
- **Video Tutorial:** "Producthero Labelizer in action" (on Labelizer page)

### Related ROK Documents
- [ROK Strategy Playbook](strategy-playbook.md) - Proven campaign structures using Labelizer
- [Experiment Logging Guide](experiment-logging-guide.md) - How to test Labelizer strategies
- [Impact Analysis Workflow](impact-analysis-workflow.md) - Evaluating Labelizer-based tests

### Client CONTEXT.md Files
Each client's CONTEXT.md includes:
- Current Labelizer implementation details
- Product distribution across labels
- Campaign structure aligned with labels
- Historical performance by label

---

## Action Items for Claude Code

**When analyzing client performance:**

1. **Always check product labels** in analysis
   - Query shopping_performance_view with segments.product_custom_attribute0
   - Group performance by label (Heroes, Sidekicks, Villains, Zombies)

2. **Verify asset group filtering**
   - When traffic spikes or anomalies occur, check if products match intended labels
   - Cross-reference product custom_label_0 with asset group names

3. **Reference this methodology in explanations**
   - "This product is labeled as a Villain, meaning it gets clicks but doesn't convert"
   - "The Furniture - Sidekicks asset group should only contain products with custom_label_0 = 'sidekicks'"

4. **Update client CONTEXT.md**
   - Document label distribution changes
   - Note products that transition between labels
   - Track which labels drive performance

5. **Flag labeling issues**
   - Alert user if products appear in wrong asset groups
   - Identify when Villains are in high-budget campaigns
   - Suggest structural improvements based on labels

---

## Conclusion

The Product Hero Labelizer is not just a tool - it's the **foundational strategic framework** for all ROK e-commerce campaign management. Proper implementation and ongoing optimization of this system is critical to client success.

**Key Principles:**
- Trust the data (labels update daily based on real performance)
- Segment campaigns by labels (never mix Villains with Heroes)
- Use proper filtering (explicit product filters, not naming convention)
- Review monthly (track transitions, optimize structure)
- Integrate with experiments (test how to best leverage labels)

**Expected Outcome:**
10-30% ROAS improvement through systematic budget allocation to high-performing products and elimination of waste on non-converters.

---

**Last Updated:** 2025-10-31
**Maintained By:** Peter Empson, ROK Systems
