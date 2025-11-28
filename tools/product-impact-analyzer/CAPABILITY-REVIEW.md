# Product Impact Analyzer - Capability Review

**Date**: November 3, 2025
**Status**: Post-Migration Review

## Your Requirements Summary

1. **Product Change Impact Analysis** - Track changes to products and their performance impact:
   - Price changes
   - In/out of stock status
   - Title/description changes
   - Product type changes
   - Ability to go back and analyze if changes were positive or negative

2. **Product Hero Label Tracking** - Monitor label classifications over time:
   - Track hero/sidekick/villain/zombie labels
   - Detect label transitions
   - Understand long-term stability

3. **Merchant Center Disapproval Monitoring** - Get alerted when products are disapproved:
   - Immediate alerts when products disapproved
   - Identify disapproval reasons
   - Alert as soon as possible

4. **Performance Anomaly Detection** - Alert on unusual performance changes:
   - Per-product performance monitoring
   - Per-client percentage-based thresholds
   - Detect dips and peaks
   - Account for different client norms

## Current System Capabilities

### ✅ IMPLEMENTED - Working Features

#### 1. Daily Product Performance Tracking
**File**: `sheets_writer.py` + daily monitoring
**What it does**:
- Captures daily snapshots for every product
- Metrics: impressions, clicks, conversions, revenue, cost, CTR, conv rate, ROAS
- Historical data stored in per-client spreadsheets
- Data dating back to October 2, 2025

**Status**: ✅ Fully operational after migration

---

#### 2. Product Hero Label Tracking
**Files**: `label_tracker.py`, `label_tracking_executor.py`
**What it does**:
- Daily snapshots of Product Hero labels per product
- Tracks label field per client (configured in `config.json`)
- Detects label transitions (hero→sidekick, villain→zombie, etc.)
- Assessment window configurable per client (30-60 days)

**Enabled for**:
- Tree2mydoor (custom_label_3)
- Accessories for the Home (custom_label_0)
- Uno Lights (custom_label_1)
- HappySnapGifts (custom_label_4)
- WheatyBags (custom_label_4)
- BMPM (custom_label_4)
- Grain Guard (custom_label_0, requires manager ID)
- Crowd Control (custom_label_0)

**Disabled for** (no labels detected):
- Smythson UK
- BrightMinds
- Go Glean UK
- Superspace UK
- Godshot
- Just Bin Bags (limited labels)

**Status**: ✅ Operational, runs as part of daily monitoring

---

#### 3. Merchant Center Disapproval Monitoring
**Files**: `disapproval_monitor.py`, `merchant_center_tracker.py`
**What it does**:
- Checks Google Merchant Center daily for product disapprovals
- Uses Google Content API for Shopping
- Detects new disapprovals since last check
- Tracks disapproval reasons and affected countries
- Sends email alerts immediately (business hours only)
- Compares current snapshot to previous to identify changes

**Alert Features**:
- Severity levels: critical, warning, info
- Business hours only (9 AM - 6 PM weekdays)
- Email alerts via SMTP
- Includes product ID, title, issue code, resolution steps

**Status**: ✅ Implemented, configured for daily runs

---

#### 4. Performance Anomaly Detection
**File**: `monitor.py`
**What it does**:
- Daily monitoring of account-level performance
- Per-client thresholds (configured in `config.json`):
  - Revenue drop alerts (e.g., Tree2mydoor: £300, Smythson: £1000)
  - Revenue spike alerts (investigate unexpected gains)
  - Click drop percentage (40-50% depending on client)
- Compares today vs yesterday or 7-day rolling average
- Sends email alerts for anomalies

**Alert Types**:
- Revenue drop (critical)
- Revenue spike (warning)
- Product missing (critical if 5+ products disappear)
- Click drop (warning)

**Status**: ✅ Operational, but **ACCOUNT-LEVEL** not per-product

---

### ⚠️ PARTIALLY IMPLEMENTED - Needs Enhancement

#### Product Change Detection
**Current State**: INDIRECT tracking only

**What exists**:
- Daily product snapshots capture current state
- Can compare snapshots to detect changes retrospectively
- Historical data allows manual analysis

**What's missing**:
- ❌ No automated price change detection
- ❌ No in/out of stock tracking
- ❌ No title/description change detection
- ❌ No product type change tracking
- ❌ No automated "what changed" analysis
- ❌ No impact correlation (e.g., "price increased 10% → revenue dropped 15%")

**Gap**: The system doesn't actively track Merchant Center product data changes - only Google Ads performance data.

---

#### Per-Product Performance Monitoring
**Current State**: Account-level monitoring only

**What exists**:
- `monitor.py` detects account-level revenue/click changes
- Per-client thresholds configured
- Email alerts for critical changes

**What's missing**:
- ❌ No per-product performance anomaly detection
- ❌ Can't alert "Product 287 revenue dropped 50% today"
- ❌ No product-specific thresholds (e.g., "alert if hero product drops 20%")
- ❌ No historical baseline per product (e.g., "this product normally does £100/day")

**Gap**: Need product-level anomaly detection with product-specific baselines and thresholds.

---

### ❌ NOT IMPLEMENTED - Missing Features

#### Product Change Impact Analysis Engine
**What's needed**:
1. **Change Detection**:
   - Track Merchant Center product feed changes (price, stock, title, description, type)
   - Detect when changes occur
   - Log changes with before/after values

2. **Impact Correlation**:
   - Compare performance before/after change
   - Calculate statistical significance
   - Determine if change was positive/negative
   - Account for external factors (seasonality, competitors)

3. **Historical Analysis Interface**:
   - Query: "Show me all price changes for this product and their impact"
   - Query: "Show me all out-of-stock periods and revenue lost"
   - Query: "Did the title change on Oct 15 improve CTR?"

**Why it matters**: This is the core requirement you mentioned - being able to go back and analyze if changes were positive or not.

---

## Architecture Analysis

### Data Sources (Current)

1. **Google Ads API** (via MCP `google-ads` server)
   - Shopping campaign performance data
   - Product-level impressions, clicks, conversions, revenue
   - GAQL queries for historical data

2. **Google Merchant Center API** (Content API for Shopping)
   - Product status (approved/disapproved)
   - Disapproval reasons
   - Used by `merchant_center_tracker.py`

3. **Product Hero Labels** (via Google Ads custom labels)
   - Stored in custom label fields (0-4)
   - Read via Google Ads API

### Data Sources (Missing)

1. **Merchant Center Product Feed Data** (NOT currently tracked)
   - Product attributes: price, title, description, availability, product_type
   - Need to snapshot these daily to detect changes
   - Available via Content API `products.list()` endpoint

### Data Storage

**Current**:
- Per-client Google Spreadsheets (daily performance snapshots)
- JSON files for monitoring state (`disapprovals_previous.json`, etc.)
- Label tracking data (separate JSON files)

**Optimal**:
- ✅ Daily performance: Google Spreadsheets (good for visualization, client sharing)
- ❓ Product changes: JSON files or database (for fast queries and analysis)
- ❓ Impact analysis: Could be computed on-demand or pre-computed weekly

---

## Recommendations

### Priority 1: Product Change Detection (HIGH VALUE)

**Implement Merchant Center Product Feed Tracker**:
- Daily snapshot of all product attributes (price, title, description, availability, type)
- Compare to previous snapshot to detect changes
- Log changes with before/after values, timestamp
- Store in JSON or lightweight database

**Files to create**:
- `product_feed_tracker.py` - Fetch and snapshot product data daily
- `product_change_detector.py` - Compare snapshots, identify changes
- `data/product_feed_history/` - Store daily snapshots per client

**Benefits**:
- Answer: "Did the price change cause the revenue drop?"
- Answer: "How long was this product out of stock?"
- Correlate changes with performance automatically

---

### Priority 2: Per-Product Performance Monitoring (MEDIUM VALUE)

**Enhance `monitor.py` for product-level anomalies**:
- Calculate per-product baselines (7-day, 30-day averages)
- Detect when individual products deviate significantly
- Alert: "Product 287 (Olive Tree Large) revenue dropped 60% (£680/week → £272/week)"
- Configurable per-product thresholds (heroes more sensitive than zombies)

**Changes needed**:
- Read last 30 days of product data from spreadsheets
- Calculate rolling averages per product
- Compare today's performance to baseline
- Generate product-specific alerts

**Benefits**:
- Early warning for top-performing products
- Identify which specific products are driving account changes
- More actionable alerts (fix specific product vs investigate whole account)

---

### Priority 3: Impact Analysis Engine (HIGH VALUE, LONGER TERM)

**Build retrospective analysis capability**:
- Query interface: "Analyze price changes for Product 287"
- Statistical significance testing (did change cause impact?)
- Before/after comparison with control periods
- Account for external factors (seasonality, day of week)

**Implementation**:
- `impact_analyzer.py` - Analyze historical changes and performance
- Report generator - Create PDF/HTML reports per client
- Weekly/monthly summary: "5 products changed this month, 3 positive, 2 negative"

**Benefits**:
- Learn what works (which changes drive revenue)
- Optimize product feed continuously
- Justify feed management decisions to clients

---

## Migration Impact on Capabilities

### What the Per-Client Spreadsheet Migration Improved

✅ **Performance**: Faster data loading for product-level queries
✅ **Client Sharing**: Can now share product data with specific clients
✅ **Scalability**: Per-client growth isolated
✅ **Organization**: Client data in dedicated spreadsheets

### What the Migration Didn't Change

- ⚠️ Still no automated product change detection (gap existed before migration)
- ⚠️ Still account-level monitoring only (not per-product anomaly detection)
- ⚠️ Still no impact correlation engine

### What the Migration Made Easier

✅ Simpler to implement per-client product baselines (data already isolated)
✅ Easier to share product-level insights with clients (dedicated spreadsheets)
✅ Faster to query product history for impact analysis (smaller datasets)

---

## Summary: What You Have vs What You Need

| Requirement | Status | Notes |
|-------------|--------|-------|
| Daily product performance tracking | ✅ Complete | Per-client spreadsheets, historical data |
| Product Hero label tracking | ✅ Complete | Daily snapshots, transition detection |
| Disapproval monitoring | ✅ Complete | Email alerts, business hours only |
| Account-level anomaly detection | ✅ Complete | Per-client thresholds, email alerts |
| **Product change detection** | ❌ Missing | Price, stock, title, type changes not tracked |
| **Per-product performance monitoring** | ❌ Missing | Only account-level, need product baselines |
| **Impact analysis engine** | ❌ Missing | Can't correlate changes with performance |

## Next Steps

If you want to implement the missing capabilities (product change detection, per-product monitoring, impact analysis), I can help you build them. These would be valuable additions that fulfill your original vision for the Product Impact Analyzer.

Would you like me to start with Priority 1 (Product Change Detection)?
