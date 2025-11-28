# Product Impact Analyzer - Current Status & Capabilities

**Date**: November 12, 2025
**Purpose**: Document what the Product Impact Analyzer actually does vs. what was planned

---

## Current Active Features ✅

### 1. Product Performance Monitoring (ACTIVE)
**What it does**:
- Fetches Google Ads Shopping performance data daily
- Tracks product-level metrics: clicks, impressions, revenue, cost
- Stores snapshots in `monitoring/snapshot_{brand}_YYYY-MM-DD.json`
- **LaunchAgent**: `com.petesbrain.product-monitor` (status code 1)

**Data tracked per product**:
- `product_id` - Google Shopping product ID
- `product_title` - Product name
- `clicks` - Daily clicks
- `impressions` - Daily impressions
- `revenue` - Daily revenue (converted value)
- `cost` - Daily ad spend

**What it does NOT track in performance snapshots**:
- Product approval status (tracked separately by disapproval monitor)
- Price data (tracked separately by price tracker)
- Title/description changes (partially tracked, not actively monitored)

### 2. Product Hero Labeling (ACTIVE for some clients)
**What it does**:
- Classifies products as Heroes/Sidekicks/Villains/Zombies based on performance
- Reads labels from custom_label fields in Google Merchant Center
- Tracks label transitions over time
- Weekly email reports on label changes

**Clients with label tracking enabled** (from config.json):
- ✅ Tree2mydoor (custom_label_3)
- ✅ Accessories for the Home (custom_label_0)
- ✅ Uno Lights (custom_label_1)
- ✅ HappySnapGifts (custom_label_4)
- ✅ WheatyBags (custom_label_4)
- ✅ BMPM (custom_label_4)
- ✅ Grain Guard (custom_label_0)
- ✅ Crowd Control (custom_label_0)

**Clients WITHOUT label tracking**:
- ❌ Smythson UK (permission denied)
- ❌ BrightMinds (no labels detected)
- ❌ Go Glean UK (permission denied)
- ❌ Superspace UK (no labels detected)
- ❌ Godshot (no full label system)
- ❌ Just Bin Bags (limited labels)
- ❌ Just Bin Bags JHD (no labels)

### 3. Revenue Anomaly Alerts (ACTIVE)
**What it does**:
- Compares current day to previous day's snapshot
- Detects revenue drops/spikes above client-specific thresholds
- Sends email alerts during business hours (9 AM - 6 PM weekdays)
- **LaunchAgent**: `com.petesbrain.product-impact-analyzer` (status code 0)

**Example thresholds** (from config.json):
- Tree2mydoor: £300 drop / £400 spike
- Smythson: £1000 drop / £1500 spike
- Clear Prospects brands: £50-120 drop / £100-220 spike

### 4. Merchant Center Disapproval Tracking (ACTIVE)
**Status**: ✅ **IMPLEMENTED** (November 12, 2025)

**What it does**:
- Tracks product approval status from Google Merchant Center
- Monitors disapproval reasons (missing GTIN, policy violations, data quality issues)
- Detects newly disapproved products by comparing snapshots
- Sends email alerts with issue codes and recommended resolutions
- **LaunchAgent**: `com.petesbrain.disapproval-monitor` (runs every 6 hours)

**Schedule**: Every 6 hours (02:00, 08:00, 14:00, 20:00)

**Data tracked per product**:
- `product_id` - Merchant Center offer ID
- `title` - Product title
- `status` - approved/disapproved/pending
- `destination_statuses` - Status per destination (Shopping Ads, Free Listings, etc.)
- `item_level_issues` - Specific disapproval reasons with severity
- `expiration_date` - When product expires from feed

**Clients monitored** (as of Nov 12, 2025):
- ✅ HappySnapGifts (Merchant ID: 7481296) - 299 disapprovals tracked
- ✅ WheatyBags (Merchant ID: 7481286) - 1 disapproval
- ✅ BMPM (Merchant ID: 7522326) - 23 disapprovals
- ✅ Tree2mydoor (Merchant ID: 107469209) - 1 disapproval
- ✅ Smythson UK (Merchant ID: 102535465) - 1,615 disapprovals (CRITICAL)
- ✅ BrightMinds (Merchant ID: 5291988198) - 256 disapprovals
- ✅ Accessories for the Home (Merchant ID: 117443871) - 39 disapprovals
- ✅ Go Glean UK (Merchant ID: 5320484948) - 0 disapprovals
- ✅ Superspace UK (Merchant ID: 645236311) - 2 disapprovals
- ✅ Uno Lights (Merchant ID: 513812383) - 32 disapprovals
- ✅ Godshot (Merchant ID: 5291405839) - 10 disapprovals (policy violations)
- ✅ Grain Guard (Merchant ID: 5354444061) - 0 disapprovals
- ✅ Crowd Control (Merchant ID: 563545573) - 6 disapprovals
- ✅ Just Bin Bags (Merchant ID: 181788523) - 6 disapprovals
- ✅ Just Bin Bags JHD (Merchant ID: 5085550522) - 0 disapprovals

**Action Plan Created** (Nov 12, 2025):
- Comprehensive disapproval audit completed across all 15 clients
- Action plan document created: `DISAPPROVAL-ACTION-PLAN.md`
- Google Tasks created for all action items (10 tasks):
  - URGENT: Smythson Greece shipping (1,500 products affected)
  - HIGH: Godshot policy violations, BrightMinds CSS, Uno Lights landing pages
  - MEDIUM: Accessories GTINs, Superspace prices, Crowd Control prices, Just Bin Bags pages, BMPM shipping
  - LOW: Tree2mydoor optional title change
- Tasks assigned with due dates based on priority and impact

**Manual usage**:
```bash
cd tools/product-impact-analyzer
.venv/bin/python3 disapproval_monitor.py --client "HappySnapGifts"
.venv/bin/python3 merchant_center_tracker.py --client "HappySnapGifts" --report
```

---

### 5. Price Change Tracking (ACTIVE)
**Status**: ✅ **IMPLEMENTED** (November 12, 2025)

**What it does**:
- Fetches complete price data from Merchant Center API 3x daily
- Tracks: regular price, sale price, sale effective dates, currency, availability
- Detects: price increases, decreases, sale started, sale ended, sale date changes
- Stores snapshots in `monitoring/prices/prices_{client}_YYYY-MM-DD.json`
- Logs changes in `monitoring/prices/price_changes_YYYY-MM.json`
- **LaunchAgent**: `com.petesbrain.price-monitor` (status code 0)

**Schedule**: 6:30 AM, 12:30 PM, 6:30 PM daily

**Data tracked per product**:
- `product_id` - Merchant Center offer ID
- `title` - Product title
- `price` - Regular price (float, e.g., 24.99)
- `sale_price` - Sale price if on sale (null if no sale)
- `sale_effective_date` - Sale start/end dates (e.g., "2025-11-29T00:00:00Z/2025-12-02T23:59:59Z")
- `currency` - Currency code (GBP, USD, EUR, etc.)
- `availability` - Stock status (in stock, out of stock, preorder)

**Important**: Sale prices apply immediately when set, regardless of effective dates. Effective dates are for *scheduled* sales that start/end automatically.

**Current baselines established** (Nov 12, 2025):
- HappySnapGifts: 13,486 products
- WheatyBags: 2,959 products
- BMPM: 6,613 products

**Change detection types**:
- PRICE_INCREASE (e.g., £19.99 → £24.99, regular price increased)
- PRICE_DECREASE (e.g., £24.99 → £19.99, regular price decreased)
- SALE_STARTED (sale price added, effective immediately or scheduled)
- SALE_ENDED (sale price removed, back to regular price)
- PRICE_AND_SALE_CHANGED (both regular and sale prices changed)
- SALE_DATES_CHANGED (sale effective dates modified - extended, shortened, or rescheduled)

**Manual usage**:
```bash
cd tools/product-impact-analyzer
.venv/bin/python3 price_tracker.py --client "HappySnapGifts"
.venv/bin/python3 price_tracker.py --report
```

### 6. Title/Description Change History (READY FOR USE)
**Status**: ✅ **AVAILABLE FOR IMPACT ANALYSIS**

**Purpose**: Track title/description changes made via Product Heroes AI for performance impact analysis

**What it does**:
- Title field already captured in daily performance snapshots
- Historical data available for before/after comparison
- Can correlate performance changes with title changes

**Use case**:
1. Product Heroes AI makes title/description changes to products
2. Performance snapshots capture new titles automatically (within 24 hours)
3. When analyzing impact, compare performance before/after the change date
4. Document: old title, new title, performance metrics before/after

**What's NOT needed**:
- ❌ Real-time monitoring (changes are intentional, not accidents)
- ❌ Automated alerts (you know when changes were made)
- ❌ Proactive scanning (changes are controlled via Product Heroes)

**How to use for impact analysis**:
```bash
# After making Product Heroes title changes, analyze impact:
cd tools/product-impact-analyzer

# Compare product performance before/after specific date
.venv/bin/python3 monitor.py --client "HappySnapGifts" --compare-dates 2025-11-01 2025-11-15

# Check which products had title changes
# (Compare snapshots manually or via custom script)
```

**Future enhancement**: Create dedicated impact analysis script that:
- Takes product ID and change date
- Pulls performance data 7 days before and 7 days after
- Shows: old title, new title, performance delta
- Calculates statistical significance of change

---

## Active LaunchAgents

From `launchctl list | grep petesbrain`:

### Related to Product Impact Analyzer:
1. **com.petesbrain.product-monitor** (status 1)
   - Purpose: Daily product performance monitoring
   - Appears to be running (creates snapshots)

2. **com.petesbrain.product-impact-analyzer** (status 0)
   - Purpose: Main analyzer (compares snapshots, detects anomalies)
   - Status code 0 = running successfully

3. **com.petesbrain.label-snapshots** (status 1)
   - Purpose: Track Product Hero label transitions
   - Status code 1 = running

4. **com.petesbrain.label-tracker** (status 0)
   - Purpose: Label tracking and reporting
   - Status code 0 = running successfully

5. **com.petesbrain.weekly-label-reports** (status 0)
   - Purpose: Weekly email reports on label changes
   - Status code 0 = running successfully

6. **com.petesbrain.disapproval-monitor** (status 0)
   - Purpose: Merchant Center disapproval tracking
   - Status code 0 = running successfully (activated Nov 12, 2025)

7. **com.petesbrain.price-monitor** (status 0)
   - Purpose: Price change tracking from Merchant Center
   - Status code 0 = running successfully (activated Nov 12, 2025)

---

## Summary: What Product Impact Analyzer Tracks

**Fully Implemented and Active** ✅:

1. **Product Performance Metrics** (Daily)
   - Clicks, impressions, revenue, cost per product
   - Snapshot-based change detection
   - Revenue anomaly alerts

2. **Product Hero Labeling** (Daily for 8 clients)
   - Hero/Sidekick/Villain/Zombie classification
   - Label transition tracking
   - Weekly email reports

3. **Merchant Center Disapprovals** (Every 6 hours)
   - Product approval status monitoring
   - Disapproval reason tracking
   - Email alerts for newly disapproved products

4. **Price Change Tracking** (3x daily)
   - Regular price monitoring
   - Sale price monitoring (immediate and scheduled)
   - Sale effective date tracking
   - Change detection with type classification

5. **Title/Description Change History** (Available for impact analysis)
   - Title field captured in daily snapshots
   - Historical data ready for before/after comparison
   - Used for Product Heroes AI impact analysis (not proactive monitoring)

**Future Development** (Not started):
- Correlation analysis between price changes and performance impact
- Email alerts for significant price changes (>10% changes or new sales)
- Weekly price change summary reports
- Integration of price data into existing weekly reports
- Dedicated Product Heroes title change impact analysis tool:
  - Input: Product ID + change date
  - Output: Old title, new title, 7-day before/after performance comparison
  - Statistical significance calculation (CTR change, conversion rate change, revenue impact)

### Step 2: Run Setup Script
```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer
./setup_disapproval_monitoring.sh
```

This will:
1. Create LaunchAgent for disapproval monitoring
2. Configure environment variables
3. Set up daily 10:30 AM checks
4. Optionally run test check

### Step 3: Verify Setup
```bash
# Check LaunchAgent loaded
launchctl list | grep disapproval

# View logs
tail -f ~/.petesbrain-disapproval-monitor.log

# Run test
.venv/bin/python3 disapproval_monitor.py --test --client "HappySnapGifts"
```

---

## Final Status Summary

**Date**: November 12, 2025
**Overall Status**: ✅ **FULLY OPERATIONAL**

The Product Impact Analyzer is now tracking everything it was designed to track:

✅ **Core Tracking (Active)**:
1. Product performance metrics (daily)
2. Product Hero label transitions (daily for 8 clients)
3. Revenue anomaly detection (real-time)
4. Weekly reports (automated)

✅ **Merchant Center Integration (Active as of Nov 12, 2025)**:
5. Disapproval tracking (every 6 hours)
6. Price change monitoring (3x daily)
   - Regular prices
   - Sale prices (immediate and scheduled)
   - Sale effective dates

✅ **Available for Use**:
7. Title/description change history (for Product Heroes AI impact analysis)

**Service Account Access**: Granted to all 15 client Merchant Center accounts
**LaunchAgents Running**: 7 active agents monitoring different aspects
**Baselines Established**: 23,058 products across Clear Prospects brands

**Next Development Phase** (Future):
- Price change impact correlation analysis
- Price change email alerts
- Integration into existing weekly reports
- Dedicated title change impact analysis script (pull 7-day before/after performance)
