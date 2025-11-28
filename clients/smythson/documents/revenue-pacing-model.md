# Revenue Pacing Model - Smythson Q4 Dashboard

**Created**: 2025-11-04
**Status**: ✅ Implemented in update-q4-dashboard.py

## Overview

The dashboard now uses a **weighted pacing model** instead of simple linear day-counting to calculate expected revenue progress. This accounts for the non-linear nature of Q4 e-commerce performance.

## Why Weighted Pacing?

Simple linear pacing assumes every day contributes equally to monthly revenue:
```
Simple pacing = days_elapsed / total_days
```

This is inaccurate for Q4 because:
- **Black Friday/Cyber Monday** generate disproportionate revenue
- **Pre-Christmas rush** (Dec 15-23) has elevated conversion rates
- **Post-Christmas** (Dec 26-31) typically sees lower performance
- **Christmas Eve/Day** have reduced shopping activity

## Weighted Pacing Formula

Instead, we calculate:
```
weighted_pacing = weighted_days_elapsed / weighted_total_days
```

Where each day gets a **weight multiplier** based on expected performance.

## Weight Multipliers

### 1. Seasonal CVR Lift (Q4 Holiday Shopping Behavior)

**Critical context**: These are **established campaigns** (ran through P7: Oct 3 - Nov 2) with proven performance:
- P7 results: £114k spend → £467k revenue → 410% ROAS
- Not "new" campaigns requiring learning period
- Historical conversion rate data exists

**Expected Q4 CVR behavior**:

The model assumes CVR **increases** through Q4 due to:
- **Gift-buying intent**: Luxury leather goods, notebooks perfect for Christmas gifts
- **Holiday shopping urgency**: Deadline pressure (Christmas delivery cutoff)
- **Deal-seeking behavior**: Black Friday/Cyber Monday heightened purchase intent

**CVR expectations by period**:

**November 1-14** (Early November): **1.0x baseline**
- Similar CVR to P7 performance
- Budget scaling from £131k → £219k (P8)
- Volume increases, CVR stable

**November 15-24** (Mid November): **1.05x lift**
- Gift-buying intent building
- CVR improves 5% above baseline
- Pre-Black Friday momentum

**November 25-30** (Black Friday week): **1.5x peak**
- Deal-seeking behavior peaks
- Urgency + discounts drive conversions
- Combined with traffic volume spike

**December 1-14** (Early December): **1.1x elevated**
- Gift urgency increases (Christmas approaching)
- CVR 10% above November baseline
- "Last chance for Christmas delivery" messaging

**December 15-23** (Pre-Christmas peak): **1.3x maximum**
- Maximum urgency ("order by X for Christmas")
- CVR at seasonal peak
- Final gift purchasing window

**December 24-31** (Post-Christmas): **1.0x baseline**
- Returns to normal shopping behavior
- Some Boxing Day/New Year gifting
- Post-holiday normalization

### 2. Peak Shopping Periods

**November**:
- **Nov 3-24**: Base performance (with learning curve applied)
- **Nov 25-30** (Black Friday week): **1.5x**
  - Includes Cyber Monday (Nov 29)
  - Accounts for 15-25% of monthly revenue in just 6 days

**December**:
- **Dec 1-14**: Base performance (1.0x)
- **Dec 15-23** (Pre-Christmas peak): **1.3x**
  - High conversion rates, last-minute shopping
  - Strong demand for gift delivery before Dec 25
- **Dec 24-25** (Christmas Eve/Day): **0.8x / 0.6x**
  - Reduced shopping activity on holidays
  - Cut-off for Christmas delivery passed
- **Dec 26-31** (Post-Christmas): **0.9x**
  - Returns, Boxing Day, lower activity
  - Some late gifting and New Year shopping

### 3. Phase Transitions (Strategy Changes)

**When budget or ROAS targets change**, expect temporary performance dips:

- **Nov 15**: UK ROAS reduction (4.3→3.8), ROW launch
  - Days 15-17: **0.85x multiplier** (re-learning period)
- **Nov 25**: USA budget increase (+15%)
  - Days 25-27: **0.85x multiplier** (bidding adjustment)
- **Dec 1**: All regions ROAS reductions
  - Days 1-3: **0.85x multiplier** (Smart Bidding recalibration)

## Example Calculation

### Scenario 1: November 4th (Day 2 - Early Learning Period)

**Simple linear pacing**:
```
2 / 28 = 7.1%
Expected revenue: £489,540 × 0.071 = £34,758
```

**Weighted pacing (with CVR ramp-up)**:
```
Days 1-2: 2 days × 0.3 (CVR ramp) = 0.6 weighted days
Days 3-5: 3 days × 0.5 (CVR building) = 1.5
Days 6-7: 2 days × 0.6 (CVR ~60%) = 1.2
Days 8-10: 3 days × 0.7 (CVR ~70%) = 2.1
Days 11-14: 4 days × 0.85 (CVR ~85%) = 3.4
Days 15-24: 10 days × 1.0 (steady CVR) = 10.0
Days 25-28: 4 days × 1.0 × 1.5 (Black Friday boost) = 6.0

Weighted elapsed: 0.6
Weighted total: 0.6 + 1.5 + 1.2 + 2.1 + 3.4 + 10.0 + 6.0 = 24.8

Weighted pacing: 0.6 / 24.8 = 2.4%
Expected revenue: £489,540 × 0.024 = £11,749
```

**Result**:
- Simple pacing expects £34,758 (assumes full CVR from day 1!)
- Weighted pacing expects £11,749 (realistic CVR for day 2)
- Actual £7,064 = 60% of weighted expectation

**Why this makes sense**:
- Day 2 CVR might be 0.8% (vs 2.5% steady state)
- Expected to reach only 30% of steady-state conversion rate
- Revenue = Clicks × CVR × AOV
- Lower CVR = proportionally lower revenue

### Scenario 2: November 20th (Day 18 - Fully Optimized)

**Weighted pacing**:
```
Days 1-3: 3 days × 0.4 = 1.2 weighted days
Days 4-7: 4 days × 0.6 = 2.4
Days 8-10: 3 days × 0.8 = 2.4
Days 11-17: 7 days × 1.0 = 7.0
Days 15-17: 3 days × 0.85 (phase transition) = reduces by 15%
  Effective: 7.0 - (3 × 0.15) = 6.55

Weighted elapsed: 1.2 + 2.4 + 2.4 + 6.55 = 12.55
Weighted total: 26.0 (from above)

Weighted pacing: 12.55 / 26.0 = 48.3%
Expected revenue: £489,540 × 0.483 = £236,448
```

**Result**: By Nov 20, campaigns are fully optimized. Expected revenue is 48.3% (not 71% from simple pacing) because:
1. Learning period reduced early days (Days 1-10)
2. Phase transition on Nov 15 caused temporary dip
3. Black Friday (Days 25-28) still ahead, representing major revenue spike

## Traffic Light Thresholds

Revenue status uses more lenient thresholds than ROAS:
- 🟢 **Green**: Actual ≥ 85% of weighted expected
- 🟡 **Amber**: Actual ≥ 70% of weighted expected
- 🔴 **Red**: Actual < 70% of weighted expected

**Why more lenient?**
- Early month revenue is naturally lower (cold starts, learning periods)
- Peak periods can dramatically shift performance
- Avoid panic reactions before key shopping dates

## Dashboard Implementation

**Columns**:
- **F**: Actual Revenue (from Google Ads API)
- **G**: Expected Revenue (what we should have by now, based on weighted pacing)
- **H**: Rev Status (traffic light comparing actual vs expected)
- **I**: Spend
- **J**: Target Revenue (full monthly target from strategy)

**Update frequency**: Daily at 7:00 AM (automated via LaunchAgent)

**Logic** (in `update-q4-dashboard.py`):
```python
# Calculate weighted pacing
november_pacing = calculate_weighted_pacing(NOVEMBER_START, NOVEMBER_END, today)

# Expected revenue at this point
expected_revenue = NOVEMBER_REVENUE_TARGETS[region] * november_pacing

# Traffic light status
if actual_revenue >= expected_revenue * 0.85:
    status = "🟢"
elif actual_revenue >= expected_revenue * 0.70:
    status = "🟡"
else:
    status = "🔴"
```

## Benefits

1. **Accurate expectations**: Accounts for seasonal patterns in Q4
2. **Prevents false alarms**: Won't show red before Black Friday just because early November is slow
3. **Strategic insight**: Can see if actual performance matches expected peak period lift
4. **Proactive alerts**: Will flag if Black Friday/pre-Christmas performance is below expectations

## Monitoring Strategy

- **Before Nov 25**: Expect slower progress (weighted pacing < 50%)
- **Nov 25-30**: Should see major revenue acceleration (6 days = ~25% of monthly target)
- **Dec 1-14**: Return to baseline pacing
- **Dec 15-23**: Should see sustained elevation (9 days = ~20% of monthly target)
- **Dec 24-31**: Lower expectations, focus on hitting overall monthly target

## Future Enhancements

Potential improvements if needed:
- Add day-of-week weighting (weekends vs weekdays)
- Phase-specific multipliers (budget increases affect expected revenue)
- Region-specific patterns (UK vs USA shopping behaviors)
- Historical data calibration (adjust multipliers based on actual past performance)
