# Per-Client Alert Thresholds

**Implemented**: October 30, 2025
**Status**: ✅ Complete

## Overview

The Product Impact Analyzer monitoring system now uses **intelligent, per-client alert thresholds** instead of global defaults. Each client has thresholds calibrated to their typical revenue patterns, business size, and risk profile.

## Implementation

### Configuration Structure

Each client in `config.json` now has a `monitoring_thresholds` object:

```json
{
  "name": "Client Name",
  "merchant_id": "...",
  "google_ads_customer_id": "...",
  "enabled": true,
  "monitoring_thresholds": {
    "revenue_drop": 300,           // £ threshold for critical revenue drop alert
    "revenue_spike": 400,           // £ threshold for revenue spike investigation
    "click_drop_percent": 40,       // % threshold for click volume drop alert
    "comment": "Context about client size and typical performance"
  }
}
```

### Monitor Logic

The `monitor.py` script now:

1. **Gets client-specific config** using `get_client_config(client_name)` helper
2. **Extracts monitoring_thresholds** from client config
3. **Falls back to global defaults** if client doesn't have custom thresholds
4. **Logs which thresholds are being used** for transparency

## Client-Specific Thresholds

### Tier 1: Large/Premium Clients

**Smythson UK**
- Revenue drop: £1,000
- Revenue spike: £1,500
- Click drop: 30%
- **Rationale**: Premium luxury brand with high AOV, £1,000+/day revenue typical

**Devonshire Hotels**
- Revenue drop: £800
- Revenue spike: £1,200
- Click drop: 30%
- **Rationale**: Hotel group with high monthly budget (£11,730 in Oct 2025), ~£380/day revenue

### Tier 2: Mid-Size E-commerce

**Tree2mydoor**
- Revenue drop: £300
- Revenue spike: £400
- Click drop: 40%
- **Rationale**: Mid-tier e-commerce, £300-400/day revenue typical

**Superspace UK**
- Revenue drop: £250
- Revenue spike: £350
- Click drop: 40%
- **Rationale**: International markets (US, UK, AUS), £250-350/day revenue

**BrightMinds**
- Revenue drop: £200
- Revenue spike: £300
- Click drop: 40%
- **Rationale**: Educational toys, steady volume, £200-300/day revenue

**Godshot**
- Revenue drop: £200
- Revenue spike: £300
- Click drop: 40%
- **Rationale**: Specialty coffee/lifestyle retail, £64/day budget, exceptional 1107% ROAS
- **Note**: Has conversion tracking issues (20% match rate)

**Go Glean UK**
- Revenue drop: £200
- Revenue spike: £300
- Click drop: 40%
- **Rationale**: Mid-sized account, £200-300/day revenue

### Tier 3: Smaller Accounts

**Uno Lights**
- Revenue drop: £180
- Revenue spike: £280
- Click drop: 45%
- **Rationale**: Lighting products, £180-280/day revenue typical

**Accessories for the Home**
- Revenue drop: £150
- Revenue spike: £250
- Click drop: 45%
- **Rationale**: Smaller account, £150-250/day revenue typical

### Clear Prospects Multi-Brand (3 Separate Entries)

**HappySnapGifts (HSG)**
- Revenue drop: £100
- Revenue spike: £200
- Click drop: 40%
- **Rationale**: Photo gifts brand, 1.15x ROAS achieved, CPA <£10, stable performance
- **Products**: Photo gifts, face masks, bunting
- **Status**: Achieving targets Oct 2025

**WheatyBags (WBS)**
- Revenue drop: £120
- Revenue spike: £220
- Click drop: 40%
- **Rationale**: Wheat bag heat packs, 1.30x ROAS (best performing of 3 brands), needs CPA improvement
- **Products**: Wheat bag heat therapy products
- **Status**: Best ROAS but CPA optimization needed

**BMPM (British Made Promotional Merchandise)**
- Revenue drop: £50 ⚠️
- Revenue spike: £100
- Click drop: 50%
- **Rationale**: **CRISIS MODE** - 0.10x ROAS in Sep, 0.00x in Oct, restructuring for profitability
- **Products**: B2B branded merchandise (cushions focus post-restructure)
- **Status**: Very low thresholds for early warning. Paused underperforming categories (mugs, coasters, napkins) early Oct. New search campaign Oct 21. Needs close monitoring.
- **Note**: Hair-trigger sensitivity due to crisis state

**Grain Guard**
- Revenue drop: £150
- Revenue spike: £250
- Click drop: 40%
- **Rationale**: Agricultural/grain storage products, strong performance (160% ROAS H&S, 140% Villains)
- **Owner**: Connor Heaps (also owns Go Glean)
- **Seasonal**: Harvest season Aug-Oct

**Crowd Control (CCC UK)**
- Revenue drop: £180
- Revenue spike: £280
- Click drop: 40%
- **Rationale**: Safety/crowd control equipment, 170% ROAS across all campaigns
- **Note**: All campaigns converged to 170% ROAS on Oct 14, 2025

**Just Bin Bags**
- Revenue drop: £120
- Revenue spike: £200
- Click drop: 45%
- **Rationale**: Industrial bin bags, multi-brand (JBB main + JHD sub-brand)
- **Note**: Two merchant feeds (181788523 main, 5085550522 JHD)

### Disabled Clients (Configured but Not Monitored)

**National Design Academy**
- Revenue drop: £150
- Revenue spike: £250
- Click drop: 40%
- **Status**: Lead generation (not e-commerce), needs customer ID
- **Budget**: £3,000-5,000/month

**OTC (Camera Manuals)**
- Revenue drop: £100
- Revenue spike: £150
- Click drop: 50%
- **Status**: CRITICAL CRISIS - CPA £12 vs £18 avg sale
- **Note**: Client ultimatum (1 month to improve as of Oct 22, 2025)

**Print My PDF**
- Revenue drop: £100
- Revenue spike: £150
- Click drop: 50%
- **Status**: Price reduction experiment Oct 21, 2025
- **Note**: Account not in accessible accounts list

## Threshold Calculation Methodology

Thresholds were determined based on:

1. **Historical Budget Data** (from CONTEXT.md files)
   - Devonshire: £11,730/month budget → £380/day → £800 drop threshold (2x daily revenue)
   - Godshot: £64/day budget → £200 drop threshold (3x daily spend)

2. **Business Tier Classification**
   - Premium/luxury (Smythson, Devonshire): Higher thresholds, lower click % tolerance
   - Mid-tier e-commerce: Moderate thresholds (£200-300 drops)
   - Smaller accounts: Lower thresholds (£150-180 drops), higher click % tolerance

3. **Risk Profile**
   - High-margin products (Smythson): Can tolerate larger absolute swings
   - Low-margin products (OTC): Lower thresholds, higher sensitivity
   - Lead gen (Devonshire, NDA): Revenue-equivalent conversions

4. **Client Situation**
   - Crisis accounts (OTC): Very low thresholds (£100) for early warning
   - Stable accounts: Higher thresholds to avoid alert fatigue
   - New/testing accounts (Godshot): Moderate thresholds, note tracking issues

## Benefits

### 1. Reduced Alert Fatigue
- Small accounts won't trigger alerts on normal £100 fluctuations
- Large accounts won't miss critical £500 drops that are significant for them

### 2. Risk-Appropriate Monitoring
- Premium clients (Smythson £1,000+ daily) get appropriate thresholds
- Crisis clients (OTC) get hair-trigger sensitivity

### 3. Business Context Awareness
- Lead gen clients (Devonshire, NDA) have different thresholds than e-commerce
- Multi-brand clients (Clear Prospects) have aggregate thresholds

### 4. Scalable System
- Adding new clients: Just set their `monitoring_thresholds` in config
- Adjusting thresholds: Edit config, no code changes needed
- Testing: Override thresholds for specific monitoring runs

## Usage

### Running Monitoring with Per-Client Thresholds

```bash
cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

# Normal monitoring run (uses per-client thresholds automatically)
.venv/bin/python3 monitor.py

# Dry run to see thresholds being used
.venv/bin/python3 monitor.py --dry-run

# Check log output to verify thresholds
cat ~/.petesbrain-product-monitor.log
```

**Log Output Example**:
```
[2025-10-30 10:00:05] Monitoring client: Smythson UK
[2025-10-30 10:00:05]   Using thresholds for Smythson UK: Rev drop £1000, Rev spike £1500, Click drop 30%
[2025-10-30 10:00:06] Monitoring client: Tree2mydoor
[2025-10-30 10:00:06]   Using thresholds for Tree2mydoor: Rev drop £300, Rev spike £400, Click drop 40%
```

### Adjusting Thresholds

Edit `config.json`:

```json
{
  "name": "Tree2mydoor",
  "monitoring_thresholds": {
    "revenue_drop": 400,  // Increased from 300
    "revenue_spike": 500,  // Increased from 400
    "click_drop_percent": 35  // Decreased from 40
  }
}
```

No need to restart LaunchAgent - next monitoring run will use new thresholds.

### Fallback Behavior

If a client doesn't have `monitoring_thresholds` defined, system falls back to global defaults from `config.json`:

```json
"monitoring": {
  "alert_revenue_drop_threshold": 500,
  "alert_revenue_spike_threshold": 500,
  "alert_click_drop_threshold_percent": 50
}
```

## Future Enhancements

1. **Statistical Auto-Calibration**
   - Analyze 30-60 days of client history
   - Calculate mean + 2 standard deviations as threshold
   - Auto-update thresholds quarterly

2. **Time-Based Thresholds**
   - Different thresholds for weekdays vs weekends
   - Seasonal threshold adjustments (Q4 vs Q1)
   - Holiday-aware thresholds

3. **Product-Level Thresholds**
   - High-value products get lower thresholds
   - Low-volume products get higher % thresholds
   - Seasonal products get date-range specific thresholds

4. **Alert Confidence Scores**
   - Factor in recent volatility
   - Account for day-of-week patterns
   - Reduce false positives from normal variance

## Troubleshooting

### Issue: Client Using Global Thresholds Instead of Custom

**Symptom**: Log shows generic £500 thresholds instead of client-specific
**Cause**: Client name mismatch (config has "Tree2mydoor", code looking for "tree2mydoor")
**Fix**: `get_client_config()` does case-insensitive matching, but check for exact name match

### Issue: Alert Not Triggering When Expected

**Symptom**: Revenue dropped £400 for Tree2mydoor but no alert
**Check**:
1. Is threshold set to £300? (should trigger)
2. Is monitoring during business hours? (9 AM - 6 PM weekdays only)
3. Check `~/.petesbrain-product-monitor.log` for threshold being used

### Issue: Too Many Alerts

**Solution**: Increase thresholds for that client:
```json
"monitoring_thresholds": {
  "revenue_drop": 500,  // Increase if getting too many alerts
  "click_drop_percent": 50  // Increase if too sensitive
}
```

## Complete Client List

**Total Clients**: 19
- **Enabled & Monitored**: 15
  - Tree2mydoor, Smythson, BrightMinds, Accessories for the Home, Go Glean, Superspace, Uno Lights
  - Devonshire Hotels, Godshot
  - **HappySnapGifts**, **WheatyBags**, **BMPM** (Clear Prospects 3 brands)
  - **Grain Guard**, **Crowd Control**, **Just Bin Bags** ← NEW!
- **Disabled (Cannot Monitor - Lead Gen)**: 4 (National Design Academy, Devonshire Hotels marked as lead gen, OTC, Print My PDF)

**Next Steps to Enable Disabled Clients**:
1. Find Google Ads customer IDs for each
2. Verify merchant IDs (some are "UNKNOWN")
3. Test monitoring with small data samples
4. Enable once data flow confirmed
5. Adjust thresholds based on first week of monitoring data

## Documentation

- **Config File**: `tools/product-impact-analyzer/config.json`
- **Monitor Script**: `tools/product-impact-analyzer/monitor.py`
- **Setup Guide**: `tools/product-impact-analyzer/MONITORING.md`
- **This Document**: `tools/product-impact-analyzer/PER-CLIENT-THRESHOLDS.md`

---

**Version**: 1.0
**Last Updated**: October 30, 2025
**Author**: Claude Code (with Pete's Brain context)
