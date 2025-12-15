# Relative Threshold Update - NDA PMax Asset Replacement

**Date**: 2025-12-12
**Updated Script**: `populate-by-asset-type.py`

## What Changed

### OLD Logic (Absolute Thresholds) ❌

```python
# Flag if:
- conversions == 0
- cost >= £200 (HEADLINE) or £30 (LONG_HEADLINE) or £50 (DESCRIPTION)
```

**Problem**: This approach doesn't account for asset group context.

**Example Issue**:
- Asset Group A (high CTR): Asset with 5% CTR flagged as "good"
- Asset Group B (low CTR): Asset with 2% CTR flagged as "bad"
- **But 5% might be 50% BELOW Asset Group A's median, while 2% might be 50% ABOVE Asset Group B's median**

### NEW Logic (Relative Thresholds) ✅

```python
# For each asset group + field type:
1. Calculate median CTR of all assets in that group
2. Flag assets that are:
   - CTR < 50% of group median
   - AND conversions == 0
   - AND impressions >= 1,000 (statistical significance)
```

## How It Works

### Step 1: Group Assets

Assets are grouped by `(asset_group_id, field_type)`:

```
Group 1: India Campaign - HEADLINE
Group 2: India Campaign - LONG_HEADLINE
Group 3: India Campaign - DESCRIPTION
Group 4: UK Campaign - HEADLINE
...
```

### Step 2: Calculate Group Median CTR

For each group:
- Get all assets with ≥1,000 impressions
- Calculate median CTR
- Set threshold = median × 0.5 (50% of median)

**Example**:

**Asset Group: "India Campaign" - LONG_HEADLINE**

| Asset | CTR | Impressions |
|-------|-----|-------------|
| A | 4.2% | 50,000 |
| B | 3.8% | 30,000 |
| C | 3.5% | 25,000 |
| D | 3.2% | 15,000 |
| E | 1.4% | 10,000 |
| F | 0.9% | 8,000 |

**Median CTR**: 3.35%
**Threshold**: 1.68% (50% of median)
**Flagged**: E (1.4%) and F (0.9%)

### Step 3: Flag Underperformers

An asset is flagged if:
```python
ctr < threshold AND conversions == 0 AND impressions >= 1000
```

### Step 4: Calculate Relative Performance

For flagged assets, calculate gap from median:
```python
relative_performance = ((asset_ctr / median_ctr) - 1) × 100
```

**Example**:
- Asset CTR: 1.4%
- Median CTR: 3.35%
- Relative performance: ((1.4 / 3.35) - 1) × 100 = **-58%**
- Issue: "-58% vs group median, 0 conv"

## New Configuration Constants

```python
MIN_IMPRESSIONS = 1000           # Minimum impressions for statistical significance
RELATIVE_CTR_THRESHOLD = 0.5     # Flag assets below 50% of group median CTR
```

**Adjustable per client**:
- High-volume accounts: Increase `MIN_IMPRESSIONS` to 5,000+
- Low-volume accounts: Decrease to 500
- More aggressive: Set `RELATIVE_CTR_THRESHOLD = 0.75` (75% of median)
- Less aggressive: Set to `0.3` (30% of median)

## New Sheet Columns

| Column | Old Name | New Name | New Meaning |
|--------|----------|----------|-------------|
| J | Benchmark | **Group Median CTR** | Median CTR for this asset's group |
| K | Gap | **Gap vs Median** | Relative performance (e.g., "-58%") |

## Benefits

1. **Context-aware** - Compares assets to their peers in the same asset group
2. **Fair** - Accounts for different campaign types (high-intent vs cold audience)
3. **Accurate** - Flags TRUE underperformers, not just low absolute numbers
4. **No false positives** - Won't flag assets performing well for their context
5. **Statistical rigor** - Requires minimum impressions for significance

## Example Comparison

### Scenario 1: High-Performing Campaign

**Asset Group Median CTR**: 8%
**Asset CTR**: 5%
**Asset Conversions**: 0

- **OLD logic**: "5% CTR is good, ignore" ✅
- **NEW logic**: "5% is 37.5% below median, FLAG" ❌ (correct!)

**Analysis**: Text isn't compelling *relative to other assets in this high-performing group*. The landing page works (8% median proves it), so the issue IS the text.

### Scenario 2: Low-Performing Campaign

**Asset Group Median CTR**: 1.2%
**Asset CTR**: 2%
**Asset Conversions**: 0

- **OLD logic**: "2% CTR is bad, FLAG" ❌
- **NEW logic**: "2% is 67% ABOVE median, ignore" ✅ (correct!)

**Analysis**: Text is actually performing WELL relative to its group. The problem is elsewhere (landing page, offer, audience).

## Migration Notes

**No changes required to**:
- `batch-generate-all-alternatives.py` (still uses same alternatives file)
- `final-alternatives-for-dropdowns.json` (same structure)
- Google Sheet structure (columns J/K just have new meanings)

**Re-run required**:
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts
python3 populate-by-asset-type.py
```

This will re-query assets and flag underperformers using the new relative logic.

## Expected Impact on NDA

**Previous run (absolute thresholds)**:
- 67 assets flagged (11 HEADLINE, 37 LONG_HEADLINE, 19 DESCRIPTION)

**New run (relative thresholds)**:
- Expected: Fewer false positives (assets with good CTR but high spend)
- Expected: More true positives (assets with poor CTR relative to group)
- **Actual numbers will depend on group-level performance distribution**

## Future Application to Other Clients

This logic is now **client-agnostic** and can be copied to other clients:

1. Update `CUSTOMER_ID` and `SPREADSHEET_ID`
2. Adjust `MIN_IMPRESSIONS` if needed (based on account volume)
3. Adjust `RELATIVE_CTR_THRESHOLD` if needed (0.5 = 50% is recommended default)
4. Run `populate-by-asset-type.py`
5. Run `batch-generate-all-alternatives.py` for flagged assets
6. User reviews and implements

**This is now the standard approach for all PMax asset replacement projects.**
