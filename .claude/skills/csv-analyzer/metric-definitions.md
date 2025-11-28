# Google Ads Metric Definitions

## Core Metrics

### Impressions
Number of times ads were shown.
- **Good**: Indicates reach and visibility
- **Watch for**: Very high impressions with low clicks (relevance issue)

### Clicks
Number of times ads were clicked.
- **Good**: Shows ad engagement
- **Watch for**: Clicks without conversions (landing page or offer issues)

### Cost (Spend)
Total amount spent on ads.
- **In reports**: Usually in dollars
- **In API**: Often in micros (divide by 1,000,000)

### Conversions
Number of conversion actions completed.
- **Note**: Can include multiple conversion types
- **Watch for**: Conversion tracking issues (very low or zero)

### Conversion Value
Total value of conversions in currency.
- **Shopping**: Usually order value
- **Lead gen**: Assigned values
- **Watch for**: Inconsistent or missing values

## Calculated Metrics

### CTR (Click-Through Rate)
```
CTR = (Clicks / Impressions) × 100%
```
- **Excellent**: >5% (Search), >3% (Shopping)
- **Good**: 2-5% (Search), 1-3% (Shopping)
- **Poor**: <1% (Search), <0.5% (Shopping)

### CPC (Cost Per Click)
```
CPC = Cost / Clicks
```
- **Industry varies widely**
- **Benchmark**: $0.50 - $2.00 (Shopping), $1.00 - $4.00 (Search)
- **Watch for**: Sudden CPC increases (competition or quality issues)

### CVR (Conversion Rate)
```
CVR = (Conversions / Clicks) × 100%
```
- **Excellent**: >5%
- **Good**: 2-5%
- **Poor**: <1%
- **Industry dependent**

### CPA (Cost Per Acquisition)
```
CPA = Cost / Conversions
```
- **Business specific**: Compare to customer LTV
- **Watch for**: CPA creep over time
- **Target**: Below breakeven point

### ROAS (Return on Ad Spend)
```
ROAS = Conversion Value / Cost
```
- **Excellent**: >4.0 (400%)
- **Good**: 2.0-4.0 (200-400%)
- **Break-even**: ~1.5 (depends on margins)
- **Poor**: <1.5

## Shopping-Specific Metrics

### Benchmark IS (Impression Share)
```
Impression Share = Actual Impressions / Eligible Impressions × 100%
```
- **Excellent**: >80%
- **Good**: 60-80%
- **Opportunity**: <60% (room to grow)

### Budget Lost IS
```
Percentage of impressions lost due to budget constraints
```
- **Action needed**: >20% (increase budget)
- **Watch**: 10-20% (monitor)
- **OK**: <10%

### Rank Lost IS
```
Percentage of impressions lost due to ad rank
```
- **Action needed**: >20% (improve quality or bids)
- **Watch**: 10-20%
- **OK**: <10%

## Performance Flags

### 🔴 Critical Issues
- ROAS < 1.0 with significant spend
- CTR < 0.3% (Shopping) or < 0.5% (Search)
- Conversions = 0 with high spend (>$100)
- CPA above breakeven point

### 🟡 Warning Signs
- ROAS 1.0-1.5 (marginal)
- CTR 0.5-1% (Shopping) or 1-2% (Search)
- Week-over-week metric drop >15%
- Budget Lost IS > 20%

### 🟢 Strong Performance
- ROAS > 4.0
- CTR > 3% (Shopping) or > 5% (Search)
- CVR > 4%
- Stable or improving trends

## Time-Based Analysis

### Week-over-Week (WoW)
```
% Change = ((This Week - Last Week) / Last Week) × 100%
```
- **Significant**: ±15%
- **Critical**: ±30%
- **Seasonal**: Expected fluctuations (holidays, sales)

### Month-over-Month (MoM)
Similar to WoW but smooths out weekly volatility.

### Year-over-Year (YoY)
Accounts for seasonal patterns.

## Data Quality Checks

### Expected Relationships
- ✅ Clicks ≤ Impressions
- ✅ Conversions ≤ Clicks
- ✅ Cost = CPC × Clicks (approximately)
- ✅ ROAS = Conversion Value / Cost

### Red Flags
- ❌ Clicks > Impressions (data issue)
- ❌ Cost = $0 but clicks > 0 (tracking issue)
- ❌ Conversions > Clicks (attribution window issue or data error)
- ❌ Conversion Value = $0 with conversions > 0 (value tracking issue)

## Benchmarks by Campaign Type

### Shopping Campaigns
- CTR: 0.5-2%
- CVR: 1-3%
- ROAS: 2-5× (varies by margin)

### Search Campaigns
- CTR: 2-8%
- CVR: 2-5%
- CPA: Varies by industry

### Performance Max
- Similar to Shopping for e-commerce
- Less granular data available
- Focus on asset group performance

### Display Campaigns
- CTR: 0.1-0.5% (much lower is normal)
- Focus on brand awareness metrics
- ROAS: Often lower than search/shopping

## Industry Benchmarks

### E-commerce (Product-focused)
- Average ROAS: 3-5×
- Average CVR: 1-3%
- Average AOV: Varies by product category

### Lead Generation
- Average CVR: 2-5%
- Focus on cost per lead vs LTV
- Longer conversion cycles

### B2B
- Lower CVR but higher value
- Longer attribution windows
- Multiple touchpoints

## Usage in Analysis

When analyzing CSVs:
1. **Calculate missing metrics** using formulas above
2. **Flag outliers** using thresholds
3. **Compare to benchmarks** by campaign type
4. **Identify trends** using time-based comparisons
5. **Prioritize actions** based on impact × ease

