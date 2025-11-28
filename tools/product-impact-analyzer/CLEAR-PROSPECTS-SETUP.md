# Clear Prospects Multi-Brand Configuration

**Setup Date**: October 30, 2025
**Approach**: Separate monitoring entries for each brand

## Overview

Clear Prospects operates **3 distinct e-commerce brands** under one Google Ads account (Customer ID: `6281395727`). Each brand has:
- Its own Google Merchant Center feed (different merchant IDs)
- Different product catalogs and target audiences
- Significantly different performance profiles
- Separate optimization needs

**Decision**: Monitor each brand separately with brand-specific alert thresholds.

---

## The Three Brands

### 1. HappySnapGifts (HSG)
**Website**: https://happysnapgifts.co.uk/
**Merchant ID**: `7481296`

**Products**: Photo gifts, face masks, bunting

**Performance Profile** (Oct 2025):
- ROAS: ~1.15x ✅ (achieved target)
- CPA: <£10 ✅ (achieved target)
- Status: **Stable, achieving targets**

**Alert Thresholds**:
- Revenue drop: **£100** (moderate sensitivity)
- Revenue spike: **£200** (investigate opportunities)
- Click drop: **40%**

**Rationale**: Stable performer hitting targets. Moderate thresholds appropriate for consistent business. Any £100+ drop warrants investigation but not panic.

---

### 2. WheatyBags (WBS)
**Website**: https://wheatybags.co.uk/
**Merchant ID**: `7481286`

**Products**: Wheat bag heat therapy products, heat packs

**Performance Profile** (Oct 2025):
- ROAS: ~1.30x ✅✅ (BEST of the 3 brands)
- CPA: Needs improvement ⚠️
- Status: **Strong ROAS, needs CPA optimization**

**Alert Thresholds**:
- Revenue drop: **£120** (slightly higher - best performer)
- Revenue spike: **£220**
- Click drop: **40%**

**Rationale**: Best performing brand (1.30x ROAS) can tolerate slightly higher revenue fluctuations. Still needs close monitoring for CPA optimization. Higher threshold reflects stronger performance baseline.

---

### 3. BMPM (British Made Promotional Merchandise)
**Website**: https://bmpm.trade/
**Merchant ID**: `7522326`

**Products**: B2B branded promotional merchandise
**Current Focus**: Cushions (post-restructure)

**Performance Profile** (Sep-Oct 2025):
- ROAS: 0.10x (Sep) → 0.00x (Oct) ❌❌ **CRISIS**
- Status: **Restructuring for profitability**

**Recent Actions** (Early Oct 2025):
- Paused underperforming categories: branded mugs, coasters, napkins
- Launched new search campaign (Oct 21): Cushions ad group, broad match + AI Max
- Reduced PMax budget to £50/day
- Removed ROAS target

**Alert Thresholds**:
- Revenue drop: **£50** ⚠️⚠️ (HAIR-TRIGGER)
- Revenue spike: **£100** (any positive movement important)
- Click drop: **50%** (very sensitive)

**Rationale**: **Crisis mode** requires extremely low thresholds for early warning. Any £50 drop needs immediate attention. Even small revenue spikes (£100+) are important to investigate as potential recovery signals. Brand is being restructured - close monitoring critical.

---

## Why Separate Monitoring?

### Performance Variance
- WheatyBags: 1.30x ROAS (healthy)
- HappySnapGifts: 1.15x ROAS (healthy)
- BMPM: 0.00x ROAS (crisis)

**Issue with combined monitoring**: A £150 drop threshold for "Clear Prospects overall" would:
- ❌ Miss critical £100 drops in BMPM (already struggling)
- ❌ Create false alarms for WheatyBags (naturally more volatile at higher volume)
- ❌ Obscure which specific brand is having issues

### Business Context
- **HSG & WBS**: Consumer B2C, stable demand, lower AOV, higher volume
- **BMPM**: B2B, project-based, higher AOV, lower volume, currently restructuring

Different business models require different alert sensitivity.

### Optimization Independence
Each brand has:
- Separate campaigns in Google Ads
- Different target audiences
- Independent budgets
- Brand-specific product issues

**Example**: HSG has critical GMC disapproval issues (89 products) that don't affect WBS or BMPM.

---

## Configuration Details

### config.json Entries

```json
{
  "name": "HappySnapGifts",
  "merchant_id": "7481296",
  "google_ads_customer_id": "6281395727",
  "enabled": true,
  "monitoring_thresholds": {
    "revenue_drop": 100,
    "revenue_spike": 200,
    "click_drop_percent": 40,
    "comment": "Photo gifts brand under Clear Prospects. 1.15x ROAS, CPA <£10, stable"
  }
}
```

```json
{
  "name": "WheatyBags",
  "merchant_id": "7481286",
  "google_ads_customer_id": "6281395727",
  "enabled": true,
  "monitoring_thresholds": {
    "revenue_drop": 120,
    "revenue_spike": 220,
    "click_drop_percent": 40,
    "comment": "Wheat bags under Clear Prospects. 1.30x ROAS (best), needs CPA improvement"
  }
}
```

```json
{
  "name": "BMPM",
  "merchant_id": "7522326",
  "google_ads_customer_id": "6281395727",
  "enabled": true,
  "monitoring_thresholds": {
    "revenue_drop": 50,
    "revenue_spike": 100,
    "click_drop_percent": 50,
    "comment": "B2B merchandise under Clear Prospects. CRISIS: 0.00x ROAS, restructuring"
  }
}
```

### Key Implementation Notes

**Shared Google Ads Customer ID**: All 3 brands use `6281395727`
- They're in the same Google Ads account
- Different campaigns with brand prefixes (CPL | HSG, CPL | WBS, CPL | BMPM)
- Data fetching uses same customer ID, filtered by merchant ID

**Separate Merchant IDs**: Each brand has its own product feed
- Product Impact Analyzer will analyze each merchant feed independently
- Product-level changes tracked separately per brand
- Different products, different catalog issues

---

## Expected Weekly Report Output

With this setup, the weekly email report will show:

```
Product Impact Analysis Report
Period: [Date Range]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HappySnapGifts (Clear Prospects)
--------------------------------
Products with significant changes: 3

✅ Positive Changes:
• Photo Cushion Face 30cm - Revenue +£45.20 (+15%)

⚠️ Negative Changes:
• Halloween Face Mask - Revenue -£32.10 (-22%)
• Christmas Bunting 10m - Clicks -18 (-35%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WheatyBags (Clear Prospects)
--------------------------------
Products with significant changes: 2

✅ Positive Changes:
• Lavender Wheat Bag Large - Revenue +£78.50 (+12%)

⚠️ Negative Changes:
• Neck Wrap Heat Pad - Revenue -£42.00 (-18%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BMPM (Clear Prospects) ⚠️ CRISIS MODE
--------------------------------
Products with significant changes: 1

✅ Positive Changes:
• Branded Cushions 40cm - Revenue +£22.00 (+180%) 🎉 RECOVERY SIGNAL!

⚠️ Negative Changes:
None this week

Note: BMPM restructuring showing early positive signs. Continue monitoring.
```

**Benefits**:
- Clear which brand is performing/struggling
- Different thresholds mean appropriate alerts per brand
- Client can see brand-specific product trends
- BMPM flagged as "CRISIS MODE" with context

---

## Daily Monitoring Behavior

Each brand monitored independently at 10 AM weekdays:

**Scenario 1: HSG drops £120, WBS stable, BMPM stable**
- ✅ Alert sent for HappySnapGifts (exceeds £100 threshold)
- ⏸️ No alert for WheatyBags (stable)
- ⏸️ No alert for BMPM (stable)

**Scenario 2: BMPM drops £60**
- ✅ **CRITICAL ALERT** sent for BMPM (exceeds £50 threshold)
- ⏸️ No alert for HSG or WBS (their drops below thresholds)
- Email subject: "🚨 CRITICAL: BMPM Revenue Drop -£60"

**Scenario 3: All 3 brands have issues**
- ✅ Separate alerts for each brand with context
- Client sees full picture across all brands
- Can prioritize response based on severity

---

## Alternative Approach Considered (Not Used)

### "Clear Prospects Consolidated" Approach

**What it would be**:
```json
{
  "name": "Clear Prospects",
  "merchant_id": "7481296",  // Use one primary merchant ID
  "google_ads_customer_id": "6281395727",
  "monitoring_thresholds": {
    "revenue_drop": 150,  // Combined threshold
    ...
  }
}
```

**Why we didn't use it**:
- ❌ Can't set brand-specific thresholds
- ❌ BMPM's crisis would be hidden in aggregate
- ❌ WheatyBags' strong performance masks HSG issues
- ❌ Only monitors one merchant feed (misses other 2 brands)
- ❌ Weekly report wouldn't separate brand performance
- ❌ Can't track brand-specific product issues (HSG's GMC problems)

**When consolidated might work**:
- All brands have similar performance
- All brands share one merchant feed
- Client wants high-level overview only
- Brands not independently managed

**Clear Prospects reality**: Brands have wildly different performance (0.00x to 1.30x ROAS), so separate monitoring is essential.

---

## Maintenance & Adjustments

### When to Adjust Thresholds

**HappySnapGifts**:
- If consistently achieving >1.30x ROAS → Increase thresholds to £120 drop, £250 spike
- If drops below 1.0x ROAS → Reduce thresholds to £80 drop for earlier warning

**WheatyBags**:
- If CPA improvements achieved → Can increase thresholds slightly (£150 drop)
- If ROAS drops below 1.2x → Reduce to £100 drop

**BMPM**:
- **When ROAS reaches 0.5x+** → Increase to £100 drop (still cautious)
- **When ROAS reaches 1.0x+** → Increase to £150 drop (normalized)
- **If remains at 0.00x for 2+ months** → Consider disabling monitoring (not viable business)

### Quarterly Review

Every quarter, review:
1. Each brand's ROAS trend
2. Alert frequency (too many? too few?)
3. Threshold appropriateness
4. Whether brands should remain separate or consolidate

---

## Client Communication

When discussing Product Impact Analyzer with Clear Prospects client:

**Email Template**:
```
Hi Michael,

We've set up automated product-level monitoring for all 3 of your brands:

• HappySnapGifts - Monitoring for £100+ revenue changes
• WheatyBags - Monitoring for £120+ revenue changes
• BMPM - Monitoring for £50+ changes (close watch during restructuring)

You'll receive:
1. Weekly email reports every Tuesday with product-level insights for each brand
2. Daily alerts (business hours only) if any brand sees significant drops

BMPM has the most sensitive thresholds given its current state - any £50 drop will alert us immediately so we can investigate.

Let me know if you'd like to adjust any of these thresholds.

Best,
Peter
```

---

## Technical Notes

### Data Fetching
Each brand's data is fetched separately:
- Query 1: Shopping data for merchant `7481296` (HSG)
- Query 2: Shopping data for merchant `7481286` (WBS)
- Query 3: Shopping data for merchant `7522326` (BMPM)

Saved as:
- `data/shopping_happysnapgifts.json`
- `data/shopping_wheatybags.json`
- `data/shopping_bmpm.json`

### Monitoring Snapshots
Daily monitoring creates separate snapshots:
- `monitoring/snapshot_happysnapgifts_2025-10-30.json`
- `monitoring/snapshot_wheatybags_2025-10-30.json`
- `monitoring/snapshot_bmpm_2025-10-30.json`

### Weekly Analysis
Analyzer processes each brand independently:
```python
for client in enabled_clients:
    # client.name = "HappySnapGifts", "WheatyBags", or "BMPM"
    # client.merchant_id = brand-specific merchant ID
    # Analysis runs separately for each
```

---

## Success Metrics

**After 1 Month** (Dec 1, 2025):
- [ ] All 3 brands have baseline snapshots
- [ ] Weekly reports showing each brand separately
- [ ] BMPM alerts triggering appropriately (not too many false positives)
- [ ] Client finds brand-level insights valuable

**After 3 Months** (Jan 1, 2026):
- [ ] BMPM shows ROAS improvement (target: >0.5x)
- [ ] Threshold adjustments made based on actual performance
- [ ] Client using insights to make brand-specific decisions
- [ ] Alert frequency appropriate (not overwhelming, not missing issues)

---

**Version**: 1.0
**Last Updated**: October 30, 2025
**Contact**: See clients/clear-prospects/CONTEXT.md for client details
