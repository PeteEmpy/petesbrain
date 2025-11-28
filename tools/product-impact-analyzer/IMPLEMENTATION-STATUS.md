# Product Impact Analyzer - Implementation Status

**Date**: November 3, 2025
**Status**: Ready to Implement Missing Features

## Completed Work

### ✅ Per-Client Spreadsheet Migration (COMPLETE)
- **Status**: Successfully completed November 3, 2025
- **Details**: See [PER-CLIENT-MIGRATION-COMPLETE.md](PER-CLIENT-MIGRATION-COMPLETE.md)
- 15 separate Google Spreadsheets created (one per client)
- 277,791 historical rows migrated
- `sheets_writer.py` updated to write to per-client spreadsheets
- 6 client CONTEXT.md files updated with spreadsheet links
- All automated systems (monitor.py, backfill scripts) working with new architecture

### ✅ Capability Review (COMPLETE)
- **Status**: Completed November 3, 2025
- **Details**: See [CAPABILITY-REVIEW.md](CAPABILITY-REVIEW.md)
- Documented all working features
- Identified gaps in original requirements
- Prioritized three missing capabilities

## Implementation Plan - Three Priority Features

### Priority 1: Product Change Detection (HIGH VALUE)
**Goal**: Track changes to products from Merchant Center feed and detect when they occur

**What to Build**:
1. **Product Feed Tracker** (`product_feed_tracker.py`)
   - Daily snapshot of all product attributes via Content API for Shopping
   - Attributes: price, title, description, availability, product_type, link, image_link
   - Store in `data/product_feed_history/[client_name]/[YYYY-MM-DD].json`
   - One snapshot per day per client

2. **Product Change Detector** (`product_change_detector.py`)
   - Compare today's snapshot to yesterday's snapshot
   - Identify changes: price, stock status, title, description, type
   - Log changes with before/after values
   - Store in `data/product_changes/[client_name]/[YYYY-MM-DD].json`

3. **Integration with Sheets Writer**
   - Add "Changes Detected" column to daily performance data
   - Flag products that changed on that date
   - Optionally: Separate "Product Changes" sheet in each client's spreadsheet

**API Requirements**:
- Google Content API for Shopping (already used for disapproval monitoring)
- Endpoint: `products.list()` for each merchant ID
- Authentication: Service account (already configured)

**Estimated Scope**: 2-3 files, ~500 lines of code

---

### Priority 2: Per-Product Performance Monitoring (MEDIUM VALUE)
**Goal**: Detect when individual products deviate significantly from their baselines

**What to Build**:
1. **Product Baseline Calculator** (`product_baseline_calculator.py`)
   - Read last 30 days of product data from per-client spreadsheets
   - Calculate per-product rolling averages: revenue, clicks, conversions, impressions
   - Store baselines in `data/product_baselines/[client_name].json`
   - Update weekly or on-demand

2. **Product Anomaly Detector** (enhance existing `monitor.py`)
   - Add `detect_product_anomalies()` method
   - Compare today's performance to product baselines
   - Configurable thresholds per client (e.g., "alert if product revenue drops >50%")
   - Separate hero product sensitivity (e.g., heroes: 30%, villains: 60%)

3. **Alert System**
   - Email alerts for significant product deviations
   - Format: "Product 287 (Olive Tree Large) revenue dropped 60% (£680/week → £272/week)"
   - Include product label (hero/sidekick/villain/zombie) for context

**Integration**:
- Extend existing `monitor.py` to add product-level checks
- Reuse existing email alert system
- Add product-specific thresholds to `config.json`

**Estimated Scope**: Enhance 1 file, add 1 new file, ~400 lines of code

---

### Priority 3: Impact Analysis Engine (HIGH VALUE, LONGER TERM)
**Goal**: Correlate product changes with performance outcomes to answer "was this change positive or negative?"

**What to Build**:
1. **Impact Correlator** (`impact_correlator.py`)
   - Query interface: "Analyze price changes for Product 287"
   - Statistical comparison: performance before/after change
   - Control period: Compare to same day-of-week in previous weeks
   - Account for external factors (seasonality, day of week effects)

2. **Change Impact Report Generator**
   - Weekly summary: "5 products changed this month, 3 positive, 2 negative"
   - Per-product analysis: Show change timeline and performance impact
   - Statistical significance: Determine if change caused the impact

3. **Analysis Methodology**:
   - Before period: 7-30 days before change
   - After period: 7-30 days after change
   - Metrics: Revenue, ROAS, CTR, conversion rate
   - Significance test: Compare means with confidence intervals

**Output**:
- HTML/PDF reports per client
- JSON data for programmatic access
- Integration with weekly email reports

**Estimated Scope**: 2-3 files, ~600 lines of code, reporting templates

---

## Implementation Order

### Phase 1: Product Change Detection (Week 1)
1. Build product feed tracker
2. Build change detector
3. Integrate with daily monitoring
4. Test with 2-3 clients
5. Roll out to all 15 clients

### Phase 2: Per-Product Monitoring (Week 2)
1. Build baseline calculator
2. Enhance monitor.py with product anomaly detection
3. Add product-specific thresholds to config
4. Test alerts with real data
5. Deploy to production

### Phase 3: Impact Analysis Engine (Week 3-4)
1. Build impact correlator
2. Create analysis methodology
3. Build report generator
4. Create report templates
5. Integrate with weekly email system

---

## Technical Requirements

### New Dependencies
```
google-api-python-client>=2.0.0  # Already installed
scipy>=1.0.0  # For statistical significance testing
jinja2>=3.0.0  # For HTML report templates
```

### New Configuration (config.json)
```json
{
  "product_monitoring": {
    "baseline_days": 30,
    "hero_threshold_pct": 30,
    "sidekick_threshold_pct": 40,
    "villain_threshold_pct": 60,
    "zombie_threshold_pct": 70
  },
  "impact_analysis": {
    "before_days": 30,
    "after_days": 30,
    "min_significance_level": 0.95
  }
}
```

### New Data Directories
```
data/product_feed_history/[client_name]/
data/product_changes/[client_name]/
data/product_baselines/
```

---

## Benefits Upon Completion

### For Account Management
- **Proactive alerts**: Know immediately when top products underperform
- **Root cause analysis**: Link performance changes to specific product changes
- **Data-driven decisions**: Know which feed optimizations work

### For Clients
- **Transparency**: See exactly what changed and when
- **Optimization insights**: Learn which changes drive revenue
- **Feed management**: Justify and optimize product data continuously

### For Pete's Brain System
- **Complete original vision**: All four requirements fully implemented
- **Differentiated capability**: Few agencies have this level of product-level intelligence
- **Automated intelligence**: No manual analysis required

---

## Next Steps

**Ready to implement all three priorities in order:**
1. Priority 1: Product Change Detection
2. Priority 2: Per-Product Performance Monitoring
3. Priority 3: Impact Analysis Engine

Each priority builds on the previous, creating a comprehensive product intelligence system.

---

**Status**: Implementation ready to begin
**Estimated Timeline**: 3-4 weeks for complete implementation
**Risk**: Low - building on proven architecture with existing data pipelines
