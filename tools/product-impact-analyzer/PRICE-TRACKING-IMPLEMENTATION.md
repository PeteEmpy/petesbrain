# Price Tracking Implementation Plan

**Date**: November 12, 2025
**Status**: Ready to implement
**Priority**: HIGH - Price changes have massive impact on product performance

---

## Current State

### What We Have ✅
- Merchant Center API access configured and working
- Service account has access to all client Merchant Center accounts
- Daily product performance snapshots (clicks, impressions, revenue, cost)
- Disapproval tracking working (automated every 6 hours)

### What's Missing ❌
- **Price data is NOT being captured** in daily snapshots
- No price comparison between snapshots
- No price change alerts
- No correlation between price changes and performance changes

---

## What the API Provides

The Merchant Center `products().list()` API returns **complete price data** for each product:

```json
{
  "offerId": "HSG848901V379425",
  "title": "Fabric Face Bunting - 5 Metres...",
  "price": {
    "value": "24.99",
    "currency": "GBP"
  },
  "salePrice": {
    "value": "19.99",
    "currency": "GBP"
  },
  "availability": "in stock"
}
```

**Fields available:**
- `price.value` - Regular price (string, e.g., "24.99")
- `price.currency` - Currency code (e.g., "GBP")
- `salePrice.value` - Sale price (if on sale)
- `salePrice.currency` - Sale price currency
- `availability` - Stock status ("in stock", "out of stock", "preorder")

---

## Implementation Plan

### Phase 1: Add Price Data to Snapshots

**File**: `tools/product-impact-analyzer/snapshot_product_feed.py`

**Current snapshot structure**:
```json
{
  "product_id": "HSG848901V379425",
  "product_title": "Fabric Face Bunting...",
  "clicks": 5,
  "impressions": 120,
  "revenue": 99.99,
  "cost": 12.50
}
```

**New snapshot structure** (add price fields):
```json
{
  "product_id": "HSG848901V379425",
  "product_title": "Fabric Face Bunting...",
  "price": 24.99,
  "sale_price": 19.99,
  "currency": "GBP",
  "availability": "in stock",
  "clicks": 5,
  "impressions": 120,
  "revenue": 99.99,
  "cost": 12.50
}
```

**Changes needed**:
1. Fetch Merchant Center product data alongside Google Ads performance data
2. Join on `product_id` to merge price with performance
3. Store price fields in daily snapshots
4. Handle missing price data gracefully (some products may not be in Merchant Center)

**Code location**: `snapshot_product_feed.py` lines ~36-96 (fetch_product_data_via_mcp function)

### Phase 2: Detect Price Changes

**File**: `tools/product-impact-analyzer/monitor.py` (or new `price_change_detector.py`)

**Logic**:
1. Load today's snapshot (with prices)
2. Load yesterday's snapshot (with prices)
3. Compare prices for each product:
   - Price increased: `today.price > yesterday.price`
   - Price decreased: `today.price < yesterday.price`
   - Sale started: `today.sale_price` exists but `yesterday.sale_price` didn't
   - Sale ended: `yesterday.sale_price` existed but `today.sale_price` doesn't
4. Calculate percentage change: `(new_price - old_price) / old_price * 100`
5. Flag significant changes (e.g., >5% price change, any sale price change)

**Price change types to track**:
- **Price increase** (e.g., £19.99 → £24.99, +25%)
- **Price decrease** (e.g., £24.99 → £19.99, -20%)
- **Sale started** (regular price → sale price, e.g., £24.99 → £19.99 sale)
- **Sale ended** (sale price → regular price, e.g., £19.99 sale → £24.99)
- **Both changed** (e.g., regular price and sale price both updated)

### Phase 3: Correlate Price Changes with Performance Changes

**File**: `tools/product-impact-analyzer/impact_correlator.py` (or extend existing)

**Analysis**:
1. Identify products with price changes in last 7-30 days
2. Compare performance before/after price change:
   - Clicks: Did clicks increase/decrease after price change?
   - CTR: Did click-through rate change?
   - Conversion rate: Did conversions change?
   - Revenue: Did revenue increase/decrease (separate from price effect)?
   - ROAS: Did efficiency improve/decline?
3. Calculate impact metrics:
   - **Revenue impact** = (New revenue/day - Old revenue/day) * days_since_change
   - **Volume impact** = (New clicks/day - Old clicks/day)
   - **Efficiency impact** = (New ROAS - Old ROAS)

**Example scenarios**:
- **Price reduced 20% → Clicks +40%, Revenue +12%** = Good move (volume compensated for lower price)
- **Price increased 15% → Clicks -5%, Revenue +9%** = Good move (maintained volume, increased margin)
- **Sale ended → Clicks -60%, Revenue -45%** = Expected, quantify impact
- **Price reduced 10% → Clicks flat, Revenue -10%** = Bad move (gave away margin for no gain)

### Phase 4: Automated Alerts and Reports

**Integration points**:

1. **Daily anomaly alerts** (monitor.py)
   - Alert when product with recent price change shows unexpected performance
   - Example: "Product X price reduced 20% on Nov 10, but clicks down 15% (expected: up)"

2. **Weekly impact reports** (weekly_impact_report.py)
   - Section: "Price Changes This Week"
   - List all price changes with performance impact
   - Highlight winners (price change → better performance)
   - Flag losers (price change → worse performance)

3. **Product Impact Analyzer Google Sheets**
   - Add "Price Change Log" sheet
   - Columns: Date, Client, Product ID, Product Title, Old Price, New Price, Change %, Type (increase/decrease/sale), Days Since Change, Performance Impact

---

## Data Storage

### New Snapshot Fields

**File**: `monitoring/snapshot_{client}_YYYY-MM-DD.json`

Add to each product:
```json
{
  "product_id": "...",
  "product_title": "...",
  "price": 24.99,              // NEW: Regular price
  "sale_price": 19.99,         // NEW: Sale price (null if no sale)
  "currency": "GBP",           // NEW: Currency
  "availability": "in stock",  // NEW: Stock status
  "price_last_changed": "2025-11-10",  // NEW: Date price last changed (track in comparison)
  "clicks": ...,
  "impressions": ...,
  "revenue": ...,
  "cost": ...
}
```

### Price Change History

**New file**: `monitoring/price_changes_{client}_YYYY-MM.json`

```json
{
  "client": "HappySnapGifts",
  "month": "2025-11",
  "changes": [
    {
      "date": "2025-11-10",
      "product_id": "HSG848901V379425",
      "product_title": "Fabric Face Bunting...",
      "change_type": "price_decrease",
      "old_price": 24.99,
      "new_price": 19.99,
      "change_percent": -20.0,
      "currency": "GBP",
      "performance_before_7d": {
        "clicks_per_day": 5.0,
        "revenue_per_day": 124.95,
        "roas": 4.2
      },
      "performance_after_7d": {
        "clicks_per_day": 7.0,
        "revenue_per_day": 139.93,
        "roas": 4.5
      },
      "impact_analysis": {
        "revenue_change_pct": 12.0,
        "clicks_change_pct": 40.0,
        "volume_compensated_for_price": true,
        "net_impact": "positive"
      }
    }
  ]
}
```

---

## Implementation Steps

### Step 1: Extend Snapshot Collection (1-2 hours)
1. Modify `snapshot_product_feed.py` to fetch Merchant Center product data
2. Join Merchant Center data with Google Ads performance data
3. Add price fields to snapshot JSON
4. Test on one client (HappySnapGifts)
5. Verify snapshots contain price data

### Step 2: Implement Price Change Detection (1-2 hours)
1. Create `price_change_detector.py` or extend `monitor.py`
2. Load yesterday and today snapshots
3. Compare prices and identify changes
4. Store price changes in history file
5. Test detection logic

### Step 3: Add Alerts (1 hour)
1. Integrate price change detection into daily monitoring
2. Send email/Slack alerts for significant price changes (>10% change, or any sale change)
3. Format alerts with before/after prices and expected impact
4. Test alert delivery

### Step 4: Correlation Analysis (2-3 hours)
1. Create price impact analyzer
2. For each price change, fetch before/after performance (7-day windows)
3. Calculate impact metrics
4. Store in price change history
5. Generate insights ("Price cut worked: +40% clicks, +12% revenue")

### Step 5: Weekly Reports (1 hour)
1. Add "Price Changes" section to weekly impact report
2. List all price changes with impact analysis
3. Highlight top winners and losers
4. Email to stakeholders

### Step 6: Documentation (30 mins)
1. Update TOOL_CLAUDE.md with price tracking capabilities
2. Update README with examples
3. Add to client onboarding guide

**Total estimated time**: 6-10 hours

---

## Example Use Cases

### Scenario 1: Black Friday Sale
**Situation**: Client runs Black Friday sale, reduces prices 25% across top 50 products

**What price tracking would show**:
- Day 1: 50 price changes detected (25% reduction avg)
- Day 2-7: Performance tracking shows:
  - Clicks: +120% (expected)
  - Revenue: +40% (volume compensated for price cut)
  - ROAS: -15% (expected efficiency drop from lower prices)
- Week 2: Sale ends, prices return to normal
  - Clicks: -60% (expected)
  - Revenue: -25% (back to baseline)

**Insight**: "Black Friday sale generated £2,500 incremental revenue despite 25% price cut. Volume spike more than compensated."

### Scenario 2: Competitor Price War
**Situation**: Competitor drops prices, client reduces prices to stay competitive

**What price tracking would show**:
- Products with price cuts: Which ones maintained volume? Which lost share?
- Margin erosion: Quantify revenue loss from price cuts
- Volume response: Did lower prices drive enough volume to compensate?

**Insight**: "Price cuts on 10 hero products cost £500/week in margin but prevented 30% volume loss. Worthwhile defensive move."

### Scenario 3: Price Optimization
**Situation**: Testing optimal price points for new products

**What price tracking would show**:
- Price increase: "Product X increased from £19.99 to £24.99 (+25%). Clicks -10%, Revenue +12%. Net positive."
- Price sweet spot: Track multiple price changes to find optimal price/volume balance

**Insight**: "£24.99 is optimal price point: maintains 90% of volume at 25% higher margin."

---

## Why This Matters

**Impact on analysis**:
- Currently when revenue drops, we can see it but not WHY
- With price tracking: "Revenue dropped 15% because price was reduced 20% on Nov 10. Volume increased 5%, net effect expected."

**Client communication**:
- Currently: "Your revenue is down 15% this week"
- With price tracking: "Your revenue is down 15% due to the Black Friday sale (prices down 20%). Volume is actually up 5%, which is strong performance for a 20% price cut."

**Strategic decisions**:
- Quantify ROI of price changes
- Identify products where price cuts worked (volume surge) vs. didn't (volume flat)
- Optimize pricing strategy with data

---

## Next Actions

1. **Immediate** (do now):
   - Implement Step 1: Add price data to snapshots
   - Test on Clear Prospects brands

2. **This week**:
   - Implement Steps 2-3: Price change detection and alerts
   - Run for 7 days to collect baseline data

3. **Next week**:
   - Implement Steps 4-5: Correlation analysis and reporting
   - Backfill price history from existing Merchant Center data (if possible)

4. **Ongoing**:
   - Monitor price changes daily
   - Include in weekly client reports
   - Refine impact analysis based on patterns

---

## Technical Notes

### Merchant Center API Quotas
- **Products.list**: 15,000 calls/day per project
- Each client query = 1 call (paginated if >250 products)
- 15 clients * 4 times/day = 60 calls/day (well within quota)

### Performance Considerations
- Fetching Merchant Center data adds ~2-3 seconds per client
- Run alongside Google Ads queries (parallel when possible)
- Cache Merchant Center data for 1 hour to reduce API calls

### Data Quality
- Some products may not have price data (new products, removed from feed)
- Handle missing prices gracefully (log warning, use last known price)
- Track price history to detect temporary vs. permanent changes

---

## Questions to Answer

1. **Threshold for alerts**: What % price change triggers alert? (Suggest: 10%+ or any sale price change)
2. **Analysis window**: How many days before/after to measure impact? (Suggest: 7 days, or until next price change)
3. **Report frequency**: Daily alerts + weekly summary? Or weekly only?
4. **Integration**: Add to existing weekly reports or separate price change report?

---

**Status**: Ready to implement when prioritized. All infrastructure in place, just needs price fields added to snapshot collection and comparison logic.
