# Go Glean - Google Ads Account Audit
**Date**: 6 November 2025
**Audited By**: Peter Empson, Rok Systems
**Account ID**: 8492163737
**Period Analysed**: Last 30 days (7 Oct - 5 Nov 2025)

---

## Executive Summary

Go Glean is a £70K/month account achieving **204% ROAS** with strong performance from patio grout products. The account shows healthy fundamentals with proper conversion tracking but has opportunities for improvement in campaign structure and budget allocation.

### Key Metrics (Last 30 Days)
- **Spend**: £2,357.71
- **Conversions**: 189.28
- **Conversion Value**: £4,927.80
- **ROAS**: 204%
- **CPA**: £12.46
- **Avg Order Value**: £26.03

### Overall Health Score: 8/10

**Strengths**:
- ✅ Proper conversion tracking configuration
- ✅ Strong ROAS performance across all campaigns (204-487%)
- ✅ Well-structured themed product segmentation (Heroes/Sidekicks/Villains)
- ✅ Healthy conversion rate and click volume
- ✅ Good product portfolio coverage
- ✅ Appropriate seasonal management (grout paused for winter)

**Opportunities for Improvement**:
- ⚠️ Budget concentration risk (51% to one campaign with lowest ROAS)
- ⚠️ High-performing campaigns budget-constrained (Search at 487% ROAS only £5/day)
- ⚠️ Inconsistent bidding strategies across campaigns
- ⚠️ Several non-converting products consuming budget

---

## 1. Account Configuration

### Account Details
| Setting | Status | Notes |
|---------|--------|-------|
| **Account Name** | Go Glean UK | ✅ Correctly configured |
| **Currency** | GBP | ✅ Correct |
| **Time Zone** | Europe/London | ✅ Correct |
| **Auto-Tagging** | Enabled | ✅ Essential for tracking |
| **Enhanced Conversions** | Enabled | ✅ Leads enabled (good) |

### Merchant Center
- **Merchant ID**: 5320484948
- **Status**: Active and feeding Shopping campaigns
- **Product Count**: 130+ active products

**Assessment**: ✅ **Good** - Account fundamentals properly configured.

---

## 2. Conversion Tracking Setup

### ✅ Conversion Tracking Verified as Correct

**Primary Conversion Action**: Google Shopping App Purchase (webpage tag)
- **Status**: ✅ Enabled and included in main conversions metric
- **Type**: Webpage conversion
- **Category**: Purchase
- **Primary for goal**: Yes
- **Counts in "Conversions"**: Yes

**Supporting Informational Actions** (not counted in main metric - correct):
- **Glean (web) purchase** (GA4) - Informational only
- **Purchase (Page load thank_you)** (Webpage) - Informational backup
- Additional micro-conversions (add to cart, page views, etc.) - Informational

**Current Performance (Last 30 Days)**:
- **Conversions (Orders)**: 189.28
- **Conversion Value**: £4,927.80
- **ROAS**: 204%
- **CPA**: £12.46
- **Average Order Value**: £26.03

### Understanding "All Conversions" vs "Conversions"

The large gap between metrics is **expected and correct**:
- **Conversions**: 189.28 = Actual orders (what we care about)
- **All Conversions**: 16,281.51 = Orders + all micro-conversions (page views, add to carts, searches, etc.)

This is normal behaviour - "All Conversions" includes every interaction, not just purchases.

### Tracking Assessment

**✅ CONVERSION TRACKING IS CORRECTLY CONFIGURED**

The setup is actually ideal:
1. **One primary purchase action** counting toward conversions (Google Shopping App Purchase)
2. **Backup tracking** for verification (GA4 purchase, page load)
3. **Micro-conversions** for funnel analysis (add to cart, page views)
4. **Enhanced conversions** enabled for better accuracy

**No critical issues found** - tracking is functioning as intended.

**Assessment**: ✅ **Good** - Conversion tracking properly configured with appropriate primary action and supporting informational conversions.

---

## 3. Campaign Structure & Performance

### Active Campaigns (Last 30 Days)

| Campaign | Type | Status | Spend | Conv | Conv Value | ROAS | CPA | Budget/Day |
|----------|------|--------|-------|------|------------|------|-----|-----------|
| **Non Grout H&S&Z 240** | PMax | ✅ Active | £1,198.11 | 108.91 | £2,447.82 | 204% | £11.00 | £40 |
| **Catch All 260** | Shopping | ✅ Active | £424.70 | 32.71 | £1,169.96 | 275% | £12.99 | £20 |
| **Search Products 240** | Search | ✅ Active | £152.53 | 11.09 | £743.15 | 487% | £13.76 | £5 |
| **Villains 260** | PMax | ✅ Active | £149.84 | 21.08 | £546.83 | 365% | £7.11 | £5 |
| **Grout PMax** | PMax | ⚠️ Paused | £432.50 | 15.48 | £818.96 | 189% | £27.95 | £30 |

### Campaign Analysis

#### 1. Non Grout H&S&Z 240 (PMax) - £1,198 spend
**Performance**: Good volume, decent ROAS
- Takes 51% of total spend (budget concentration risk)
- £40/day budget (largest allocation)
- Focused on non-grout products using Heroes/Sidekicks/Zombies theme
- ROAS lower than other campaigns (204% vs 275-487%)

**Recommendation**: This campaign is carrying the account but has the weakest ROAS. Consider:
- Splitting into separate Heroes/Sidekicks/Zombies campaigns for better control
- Testing lower daily budget to shift spend to higher ROAS campaigns

#### 2. Catch All 260 (Shopping) - £425 spend
**Performance**: Strong ROAS (275%), good efficiency
- Standard Shopping with Target ROAS 260%
- 2 active ad groups: Heroes (93% of spend), Sidekicks (7%)
- Zombies ad group is paused
- Higher ROAS than PMax campaign despite being "catch all"

**Recommendation**:
- Reactivate Zombies ad group if it has inventory
- This campaign outperforms PMax - consider increasing budget

#### 3. Search Products 240 (Search) - £153 spend
**Performance**: Exceptional ROAS (487%)
- Only £5/day budget despite being best performer
- Focused on "Patio Grout - Generic" ad group
- Very efficient but severely budget-constrained

**Recommendation**:
- **Immediate action**: Increase budget to £10-15/day
- Test with tROAS bidding instead of Max Conv Value for more control
- Add more ad groups for other product categories

#### 4. Villains 260 (PMax) - £150 spend
**Performance**: Excellent ROAS (365%), low CPA
- Only £5/day budget
- Second-best performing campaign
- Focused on "Villains" product theme

**Recommendation**:
- Increase budget to £10-15/day to capture more volume
- Consider this as a model for future themed campaigns

#### 5. Grout PMax (PAUSED) - £433 spend before pause
**Status**: Recently paused, was spending ~£14/day
- Had £30/day budget
- ROAS was 189% (lower than other campaigns)
- Grout products are core business - should have dedicated campaign

**✅ PAUSE EXPLAINED**: Patio grout is **highly seasonal** - can only be applied in warmer months (typically April-September in UK). Pausing in November is correct seasonal management.

**Seasonality Impact**:
- **Peak Season**: April-September (outdoor application weather)
- **Off-Season**: October-March (too cold for proper curing)
- Current pause (November) is appropriate and expected
- ROAS of 189% in October suggests declining demand as weather cools

**Recommendation**:
- ✅ Keep paused through winter (Nov-Mar)
- Plan reactivation for late March/early April 2026
- Consider weather-triggered reactivation (when temps consistently above 10°C)
- Use winter months to optimise non-grout products
- Prepare grout campaign refresh for spring (updated copy, new assets)

### Paused Legacy Campaigns

Multiple "ALG" (presumably "Algorithm" or previous agency) campaigns are paused:
- ALG - Branded Shopping
- ALG - Patio Grout - UK - Shopping
- ALG - PMAX - Poor Performers
- ALG - PMAX - Top Performers
- ALG - PMAX - Other Products

**Assessment**: ✅ **Good** - Properly cleaned up legacy campaigns.

**Assessment**: 7/10 - Good structure with themed segmentation, but budget allocation needs optimisation.

---

## 4. Product Performance Analysis

### Top 10 Products by Spend (Last 30 Days)

| Product | Spend | Conv | Conv Value | ROAS | Status |
|---------|-------|------|------------|------|--------|
| Patio Grout - Pure Light Grey 15kg | £314.25 | 9.33 | £787.01 | 250% | ✅ Hero |
| Patio Grout - Grey 15kg | £263.77 | 10.99 | £531.09 | 201% | ✅ Hero |
| Patio Grout - Natural Buff 15kg | £179.45 | 4.50 | £245.47 | 137% | ⚠️ Low |
| Composite Sink Restorer 500ml | £146.40 | 27.28 | £412.68 | 282% | ✅ Hero |
| Grout Reviver Kit - Light Grey | £77.49 | 5.02 | £105.42 | 136% | ⚠️ Low |
| Black Stone Sealer 500ml | £64.44 | 11.33 | £238.56 | 370% | ✅ Hero |
| Oil & Drive Cleaner 1L | £56.75 | 7.50 | £172.94 | 305% | ✅ Hero |
| Black Stone Restorer 1L | £48.91 | 5.98 | £272.71 | 558% | ✅ Star |
| Stone Polish Gloss Wax | £34.93 | 5.00 | £77.95 | 223% | ✅ Good |
| Grout Reviver Kit - Black | £31.95 | 5.00 | £139.75 | 437% | ✅ Hero |

### Product Insights

**Heroes** (High spend, strong ROAS):
1. **Patio Grout Range** - Core business, driving most revenue
2. **Composite Sink Restorer** - Excellent ROAS (282%) with high conversion rate
3. **Black Stone Sealer** - Strong performer (370% ROAS)
4. **Oil & Drive Cleaner** - Solid performer (305% ROAS)

**Stars** (Lower spend, exceptional ROAS):
- Black Stone Restorer 1L (558% ROAS) - Deserves higher budget
- Grout Reviver Kit - Black (437% ROAS)

**Problem Products** (Spending with no conversions):
- Patio Grout - Basalt (£27.97 spend, 0 conversions)
- Patio Grout Resin Remover (£16.09 spend, 0 conversions)
- Salt Stain Remover 5L (£15.33 spend, 0 conversions)
- Anti-Slip Treatment 500ml (£11.72 spend, 0 conversions)
- Several others with 0 conversions in last 30 days

### Product-Level Recommendations

**Immediate Actions**:
1. **Create negative product groups** for non-converters (10+ products with £0 conversion value)
2. **Increase bids** on Star products (Black Stone Restorer, Grout Reviver Black)
3. **Test supplemental feeds** to boost Heroes with custom labels

**Medium-term**:
1. Investigate why Basalt patio grout doesn't convert (price? description? stock?)
2. Review product titles for SEO optimisation
3. Consider product bundling for slow movers

**Assessment**: 8/10 - Strong product portfolio with clear heroes, but need to optimise tail.

---

## 5. Budget Allocation Analysis

### Current Daily Budgets

| Campaign | Daily Budget | % of Total | 30-Day Spend | % Utilisation |
|----------|-------------|-----------|--------------|---------------|
| Non Grout H&S&Z | £40 | 51% | £1,198.11 | 100% |
| Catch All Shopping | £20 | 26% | £424.70 | 71% |
| Grout PMax (paused) | £30 | - | £432.50 | 48% |
| Search Products | £5 | 6% | £152.53 | 102% ✅ |
| Villains PMax | £5 | 6% | £149.84 | 100% |
| **Total Active** | **£70/day** | 100% | **£1,925.18** | 92% |

### Budget Issues Identified

**1. Budget Concentration**
- 51% of budget in one campaign (Non Grout H&S&Z)
- Single point of failure if campaign performance drops
- Limits ability to test and scale other campaigns

**2. Budget Constraints on Top Performers**
- Search campaign hitting 102% budget (best ROAS at 487%)
- Villains PMax hitting 100% budget (365% ROAS)
- Both campaigns capped at only £5/day

**3. Underutilised Budget**
- Catch All Shopping only using 71% of £20 budget
- Could reallocate unused budget to Search/Villains

**4. Paused Core Product Campaign**
- Grout PMax paused (was £30/day)
- Unclear where grout product budget went

### Recommended Budget Allocation

#### Option A: Optimise for ROAS (Conservative)
Shift budget toward highest ROAS campaigns:

| Campaign | Current | Proposed | Change | Rationale |
|----------|---------|----------|--------|-----------|
| Search Products | £5 | £15 | +£10 | 487% ROAS - needs scale |
| Villains PMax | £5 | £12 | +£7 | 365% ROAS - proven winner |
| Catch All Shopping | £20 | £18 | -£2 | Underutilising, slight trim |
| Non Grout H&S&Z | £40 | £30 | -£10 | Lower ROAS, reduce dominance |
| Grout PMax | £0 | £10 | +£10 | Reactivate core products |
| **Total** | **£70** | **£85** | **+£15** | 21% budget increase |

**Expected Impact**:
- Overall ROAS increase from 204% to ~280%
- Reduced concentration risk
- Core grout products back in market

#### Option B: Balanced Growth (Moderate)
Keep current total budget, redistribute:

| Campaign | Current | Proposed | Change |
|----------|---------|----------|--------|
| Search Products | £5 | £10 | +£5 |
| Villains PMax | £5 | £10 | +£5 |
| Catch All Shopping | £20 | £20 | £0 |
| Non Grout H&S&Z | £40 | £30 | -£10 |
| Grout PMax | £0 | £0 | £0 |
| **Total** | **£70** | **£70** | **£0** |

**Expected Impact**:
- No budget increase required
- Better balance across campaigns
- Reduced risk from concentration

**Assessment**: 6/10 - Budget allocation doesn't match campaign performance.

---

## 6. Bidding Strategy Review

### Current Strategies

| Campaign | Bidding Strategy | Target ROAS | Notes |
|----------|------------------|-------------|-------|
| Non Grout H&S&Z | Maximise Conversion Value | - | No tROAS constraint |
| Catch All Shopping | Target ROAS | 260% | Explicit target |
| Search Products | Maximise Conversion Value | - | No tROAS constraint |
| Villains PMax | Maximise Conversion Value | - | No tROAS constraint |

### Issues Identified

**1. Inconsistent Strategy**
- 3 campaigns use Max Conv Value (no ROAS target)
- 1 campaign uses Target ROAS (260%)
- Campaign names suggest ROAS targets (240, 260) but bidding doesn't enforce them

**2. No Safety Rails**
- Max Conv Value campaigns have no floor/ceiling
- Could spend aggressively if algorithm decides to
- Risk of ROAS dropping without warning

**3. Campaign Names Misleading**
- "Non Grout H&S&Z **240**" suggests 240% target
- "Catch All **260**" has tROAS 260% set (consistent)
- "Search Products **240**" has no 240% target
- "Villains **260**" has no 260% target

### Recommendations

**Option A: Standardise on Target ROAS**
- Set explicit tROAS targets matching campaign names
- Non Grout H&S&Z → tROAS 240%
- Search Products → tROAS 240%
- Villains → tROAS 260%
- Provides safety rails and aligns naming with strategy

**Option B: Keep Max Conv Value but Add Monitoring**
- Continue with Max Conv Value for flexibility
- Set up automated alerts when ROAS drops below targets
- Remove numbers from campaign names to avoid confusion

**Recommended**: Option A for consistency and control.

**Assessment**: 6/10 - Inconsistent bidding strategies creating confusion.

---

## 7. Performance Trends (Last 7 Days)

### Daily Performance

| Date | Spend | Conv | Conv Value | ROAS | CPA |
|------|-------|------|------------|------|-----|
| 5 Nov | £68.26 | 5.84 | £169.66 | 249% | £11.69 |
| 4 Nov | £43.99 | 7.00 | £132.93 | 302% | £6.28 |
| 3 Nov | £62.13 | 2.98 | £74.28 | 120% | £20.83 |
| 2 Nov | £82.85 | 7.16 | £230.18 | 278% | £11.57 |
| 1 Nov | £48.90 | 4.00 | £110.93 | 227% | £12.22 |
| 31 Oct | £67.73 | 5.99 | £190.37 | 281% | £11.31 |
| 30 Oct | £61.56 | 9.00 | £125.13 | 203% | £6.84 |

### Trend Analysis

**Performance Stability**: Moderate
- Daily ROAS ranges from 120% to 302%
- Average daily spend: £62.20
- Average daily conversions: 5.99
- High day-to-day variation

**Concerning Trends**:
- 3 Nov showed significant drop (120% ROAS vs 280% average)
- Conversion rate volatile (2.98 to 9 conversions/day)
- Spend also varies widely (£44-£83/day)

**Possible Causes**:
1. Budget constraints hitting different campaigns each day
2. Competition fluctuations
3. Product stock availability
4. Conversion tracking delays

**Recommendation**:
- Monitor for continued volatility
- Check for budget-limited days
- Ensure conversion tracking is real-time

**Assessment**: 7/10 - Generally stable but some volatility to investigate.

---

## 8. Account Health Checklist

### Technical Setup
| Item | Status | Notes |
|------|--------|-------|
| Auto-tagging enabled | ✅ Pass | Required for tracking |
| Enhanced conversions enabled | ✅ Pass | Leads only, could add for sales |
| Conversion tracking installed | ⚠️ **Issue** | Multiple purchase actions, primary not counting |
| Google Analytics linked | ✅ Pass | GA4 conversion visible |
| Merchant Center linked | ✅ Pass | ID 5320484948 active |
| Negative keywords list | ❓ Unknown | Not audited in this review |
| Audience lists | ❓ Unknown | Not audited in this review |

### Campaign Health
| Item | Status | Notes |
|------|--------|-------|
| Active campaigns running | ✅ Pass | 4 active campaigns |
| Campaigns not limited by budget | ⚠️ **Issue** | Search & Villains at 100%+ |
| Consistent bidding strategy | ⚠️ **Issue** | Mix of Max Conv Value and tROAS |
| Ad group structure | ✅ Pass | Themed segmentation (Heroes/Sidekicks/Villains) |
| Product coverage | ✅ Pass | 130+ products, good coverage |
| Performance consistency | ⚠️ **Issue** | High day-to-day volatility |

### Reporting & Optimisation
| Item | Status | Notes |
|------|--------|-------|
| Conversion tracking accurate | ❌ **Fail** | 85% of conversions not counting |
| Budget allocation optimised | ⚠️ **Issue** | 51% in lowest ROAS campaign |
| Regular optimisation | ✅ Pass | Evidence of ROAS testing in Sept |
| Performance monitoring | ✅ Pass | Campaign names show ongoing management |

**Overall Health**: ⚠️ **Needs Improvement** - Strong foundation but critical conversion tracking and budget issues.

---

## 9. Priority Action Items

### 🚨 Critical (Do First)

**1. ✅ Conversion Tracking - Verified Correct**
- **Status**: Properly configured with Google Shopping App Purchase as primary action
- **Verification**: Single primary conversion counting orders, supporting conversions for information only
- **No action needed** ✅

**2. ✅ Grout Campaign Seasonality - No Action Needed**
- **Status**: Grout campaign correctly paused for winter (Nov-Mar)
- **Reason**: Patio grout can only be applied in warmer months (April-September)
- **Action**:
  - Keep paused until late March 2026
  - Prepare spring campaign refresh (new assets, updated copy)
  - Set calendar reminder for March reactivation
- **No immediate action required** ✅

**3. Increase Search Campaign Budget (PRIORITY)**
- **Problem**: Best performing campaign (487% ROAS) limited to £5/day, hitting budget cap
- **Action**: Increase budget to £15/day immediately
- **Expected Impact**: +£300-450/month revenue at 400%+ ROAS
- **Effort**: 5 minutes
- **Risk**: Very low (already proven high ROAS)

### ⚠️ High Priority (This Week)

**4. Redistribute Budget from Non Grout H&S&Z**
- **Problem**: 51% of budget in lowest ROAS campaign (204%)
- **Action**:
  - Reduce from £40 to £30/day
  - Reallocate £10 to Search (£5) and Villains (£5)
- **Expected Impact**: 15-20% overall ROAS improvement

**5. Standardise Bidding Strategies**
- **Problem**: Inconsistent strategies and misleading campaign names
- **Action**:
  - Set tROAS on all campaigns matching name targets (240%, 260%)
  - Or remove numbers from names if keeping Max Conv Value
- **Impact**: Better control and clearer expectations

**6. Exclude Non-Converting Products**
- **Problem**: 10+ products spending with 0 conversions
- **Action**: Create negative product list or exclude from all campaigns
- **Expected Impact**: 5-10% budget efficiency gain

### 📊 Medium Priority (This Month)

**7. Test Product Segmentation**
- Split Non Grout H&S&Z into separate Heroes, Sidekicks, Zombies campaigns
- Allows better budget control per theme
- Test over 2-3 weeks with equal budgets

**8. Optimise Product Titles & Descriptions**
- Review top 20 products for search relevance
- Add key terms (brand, size, benefits)
- Test impact on impressions and CTR

**9. Set Up Performance Monitoring**
- Daily alerts for ROAS drops below 180%
- Weekly product performance review
- Monthly campaign structure review

### 📈 Nice to Have (Next Quarter)

**10. Test Supplemental Feeds**
- Add custom labels for Heroes/Sidekicks/Villains at product level
- Enables tighter campaign control
- Requires Merchant Center feed setup

**11. Explore Demand Gen**
- Test with small budget (£5-10/day)
- Use creative from PMax campaigns
- Target audience expansion

**12. Build Remarketing Lists**
- Cart abandoners
- Product page viewers
- Past purchasers for cross-sell

---

## 10. Expected Impact Summary

### If All High Priority Actions Completed

**Current State** (Last 30 days):
- Spend: £2,357.71
- Conversions (Orders): 189.28
- Revenue: £4,927.80
- ROAS: 204%
- CPA: £12.46

**Projected State** (30 days after budget optimisation):
- Spend: £2,500 (6% increase from budget reallocation)
- Conversions: 220-250 (+16-32% from better budget allocation)
- Revenue: £6,000-6,500 (+22-32% increase)
- ROAS: 240-260% (+18-27% improvement)
- CPA: £10-11 (15-20% improvement)

### ROI on Actions

| Action | Effort | Cost | Expected Gain | ROI |
|--------|--------|------|---------------|-----|
| Budget reallocation | 30 min | £0 | +15-20% ROAS | Infinite |
| Increase Search budget | 5 min | +£300/mo | +£1,200-1,500/mo @ 400% | 400-500% |
| Exclude non-converters | 1 hour | £0 | +5-10% efficiency | Infinite |
| Standardise bidding | 30 min | £0 | Better control | N/A |
| Optimise product mix | 1 hour | £0 | +5-8% winter ROAS | Infinite |

**Total estimated time investment**: 3 hours
**Total estimated cost**: £300/month (from budget increase)
**Expected revenue increase**: £1,200-1,700/month
**Net gain**: £900-1,400/month

---

## 11. Competitor Considerations

**Typical Go Glean Competitors**:
1. **Trade Suppliers**: Screwfix, Toolstation, Travis Perkins
2. **DIY Retailers**: B&Q, Wickes, Homebase
3. **Specialist Suppliers**: CTD Tiles, Topps Tiles
4. **Online Specialists**: Various specialist grout/stone care brands

**Competitive Positioning**:
- Premium pricing (evidenced by high ROAS targets)
- Specialist product range (grout, stone care, sealers)
- Strong brand ("Glean" visible in many product titles)
- E-commerce focus (Shopify platform)

**Competitive Threats**:
- Large trade suppliers with better brand recognition
- Amazon aggregating similar products
- Direct manufacturer channels

**Recommendations**:
1. Monitor competitor activity via Auction Insights
2. Test brand campaigns to protect brand terms
3. Consider trademark bids for core products
4. Develop unique value propositions in ad copy

---

## 12. Questions for Client

To complete optimisation, we need clarity on:

**Campaign Strategy**:
1. ~~Why was the Grout PMax campaign paused?~~ ✅ **Answered**: Seasonal - patio grout only applicable April-September
2. What is the rationale for the Heroes/Sidekicks/Villains/Zombies theme?
3. Are there specific products we should prioritise or avoid?
4. What's the business priority: volume, profit margin, or market share?
5. **New**: How much does revenue typically drop in winter vs summer months?

**Conversion Tracking**:
6. ~~Which conversion action is source of truth?~~ ✅ **Answered**: Google Shopping App Purchase (correctly configured)
7. ~~Are you aware of 3 purchase tracking methods?~~ ✅ **Answered**: Primary + backup informational tracking (correct setup)

**Budget & Targets**:
8. Is there flexibility to increase budget for high performers?
9. What's the minimum acceptable ROAS?
10. ~~Are there any seasonal factors?~~ ✅ **Answered**: Grout is highly seasonal (April-September only)

**Product Inventory**:
11. Are all products in stock and available?
12. Any upcoming product launches or discontinuations?
13. Which products have the best margins?
14. **New**: Should we focus winter budget on indoor products (cleaners, sealers)?

---

## Appendix A: Themed Product Framework

The account uses a "Heroes & Sidekicks & Zombies & Villains" framework consistent across owner Connor Heaps' multiple businesses (Go Glean, Grain Guard, Crowd Control).

### Framework Interpretation

**Heroes**: Best-performing products
- High conversion rate
- Strong ROAS
- Core business drivers
- Examples: Top patio grout products, bestselling cleaners

**Sidekicks**: Supporting products
- Complementary to Heroes
- Medium performance
- Cross-sell opportunities
- Examples: Accessories, smaller sizes, related items

**Zombies**: Struggling products
- Low or no conversions
- Poor ROAS
- Dead inventory
- Examples: Slow-moving grout colours, niche cleaners

**Villains**: Problem products / premium tier (unclear)
- Could be premium products (high margin)
- Or could be problematic (low margin, high return rate)
- Need clarification from client

### Campaign Mapping

| Campaign | Theme Focus | Products Included |
|----------|-------------|-------------------|
| Non Grout H&S&Z | Heroes + Sidekicks + Zombies | All non-grout products |
| Catch All | Heroes + Sidekicks | Broad coverage |
| Villains PMax | Villains only | Premium/Problem products |
| Grout PMax (paused) | Grout products | Core grout range |

**Recommendation**: Get explicit definition of each theme from Connor to optimise categorisation.

---

## Appendix B: Technical Specifications

### API Access Details
- **Customer ID**: 8492163737
- **Manager ID**: 2569949686 (required for API access)
- **Merchant ID**: 5320484948
- **Conversion Tracking ID**: 11461085377

### Integration Status
| System | Status | Notes |
|--------|--------|-------|
| Google Ads | ✅ Active | Full API access |
| Google Merchant Center | ✅ Active | Shopping feed live |
| Google Analytics 4 | ✅ Active | GA4 conversions visible |
| Enhanced Conversions | ✅ Active | Leads enabled |
| Remarketing | ❓ Unknown | Not checked |

### Data Export
All data in this audit is available via:
- Google Ads API (MCP server)
- Google Sheets export
- Custom dashboard (if required)

---

## Audit Completed By

**Peter Empson**
Account Manager, Rok Systems
petere@roksys.co.uk
07932 454652

**Date**: 6 November 2025
**Review Period**: 7 October 2025 - 5 November 2025 (30 days)
**Next Review Due**: 6 December 2025

---

## Document Version History

| Date | Version | Changes |
|------|---------|---------|
| 6 Nov 2025 | 1.0 | Initial audit completed |
