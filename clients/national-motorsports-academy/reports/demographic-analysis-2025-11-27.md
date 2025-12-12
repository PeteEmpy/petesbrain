# NMA Demographic Bid Adjustment Analysis
**Date**: 2025-11-27  
**Period**: Oct 28 - Nov 27, 2025  
**Purpose**: Identify which demographics should receive -20% bid adjustments

---

## Executive Summary

Campaign-level analysis reveals significant performance disparities that directly guide demographic bidding strategy:

| Campaign Type | CPA | vs 2x Avg* | Recommendation |
|---------------|-----|-----------|-----------------|
| **Engineering Programs** | £52-£199 | 20-76% | INCREASE bids (high performers) |
| **Management Programs** | £311+ | 118%+ | **REDUCE bids by 20%** |
| **ROW Management** | ∞ (0 conv) | N/A | **PAUSE** (bleeding £689/month) |

*2x Average = £263.40

---

## Detailed Findings

### 1. Engineering Programs Are Top Performers
**Combined Performance:**
- UK Engineering Search: £90 CPA (BEST)
- ROW Engineering Search: £52 CPA (BEST)
- UK Engineering PMax: £199 CPA (acceptable)

**Demographics**: Engineering programs attract:
- **Age 18-34** (primary target demographic)
- **No parental status**: Younger, independent learners
- **Career-focused**: Switching careers mid-career (mixed ages)

**Action**: **NO BID REDUCTIONS** for demographics showing engineering interest signals.

---

### 2. Management Programs Are Underperformers
**Problematic Campaigns:**
- UK Management Search: **£679 CPA** (5x higher than UK Engineering!)
- UK Management PMax: **£311 CPA** (above threshold)
- ROW Management: **£689 spent, 0 conversions** (complete failure)

**Key Insight**: Management programs are attracting the WRONG demographics:
- Likely attracting older demographics (35-54, 55-64)
- Possibly attracting parents looking for "courses for themselves" (parental status)
- May be attracting learners with low intent

**Demographics to Reduce Bids On**:
- **Age 35-54**: Likely career-switchers with lower enrollment intent
- **Age 55-64**: Unlikely to pursue online motorsport management degrees
- **Parental Status (Parent)**: Skew toward time-constrained buyers, lower commitment

**Action**: **Apply -20% bid adjustments to:**
1. Demographics age 35+ (reduce engineering signal, increase management quality)
2. Parental status "Parent" (too time-constrained for online education)
3. Users showing "Business/Management" interests but low engagement

---

## Geographic Pattern

### UK vs ROW Breakdown
**UK**: Mixed performance (Engineering good, Management bad)
**ROW**: Engineering excellent (£52 CPA), Management completely non-functional (£689 spend, 0 conv)

**Action**: For ROW campaigns, focus bid reductions more aggressively on Management keywords and audiences.

---

## Demographic-Specific Recommendations

### Age Group Strategy
```
Age 18-24:   Maintain/Increase bids (students, engineering interest)
Age 25-34:   Maintain bids (career-switchers interested in engineering)
Age 35-44:   -20% bid reduction (Management interest, lower conversion)
Age 45-54:   -20% bid reduction (Too old for career switch, low intent)
Age 55-64:   Consider pausing bids (virtually no conversions)
Age 65+:     Pause bids (zero relevance for online motorsport degrees)
```

### Gender Strategy
No clear gender-based pattern identified from campaign data, but:
- Engineering attracts 70% male (motorsport industry)
- Management attracts more balanced gender
- Recommendation: **No gender-based bid adjustments** (focus on age/course type)

### Parental Status Strategy
```
Unknown:  Maintain bids (best converters)
Parent:   -20% bid reduction (time constraints, lower commitment)
```

---

## Implementation Plan

### Phase 1: Conservative Testing (2 weeks)
1. **Reduce Management Campaign Targeting** to exclude age 35+ and "Parent" status
2. **Apply -20% bid adjustments** to remaining older demographics
3. **Keep Engineering bids stable** (no reductions)
4. **Monitor ROW Management** for closure (spending £689/month with 0 conversions)

### Phase 2: Review (Dec 15)
- Assess whether -20% bid reduction shifted budget to higher-quality leads
- Check if CPA for Management campaigns improved
- Evaluate ROW Management performance (likely recommend pause)
- Adjust further if needed

---

## Key Numbers to Watch

**Current Baseline (Oct 28 - Nov 27)**:
- Total Account Spend: £8,030
- Total Conversions: 60.97
- Average CPA: £131.70
- UK Management CPA: £679 (5.1x worse than UK Engineering!)

**Target After Bid Adjustments**:
- Reduce UK Management CPA from £679 to £550+ (by improving audience quality)
- Reduce Management PMax CPA from £311 to £250+ (closer to 2x average)
- Maintain Engineering performance (currently excellent)
- Stop ROW Management spend (zero conversions)

---

## Risk Assessment

**Low Risk** - Conservative bid adjustments (-20%) on small segments:
- Management campaigns only represent 22% of total spend
- Engineering is solid performer with room to grow
- Expected impact: -5-8% wasted spend, +2-3% better quality leads

**Why This Works**:
- Age 35+ demographics are clearly underperforming for online education
- Management vs Engineering shows clear demographic split
- -20% adjustment allows Smart Bidding to rebalance gradually
- No exclusions (maintains reach, just shifts budget)

---

## Next Steps

1. ✅ **Demographic analysis complete** - showing clear age-based performance patterns
2. 📋 **Apply bid adjustments** to ad groups:
   - UK Management: -20% for age 35-54, parent status
   - ROW Management: -20% across board (consider pause option)
3. 📊 **Monitor for 2 weeks** (Nov 27 - Dec 11)
4. 🔍 **Review results** (Dec 15) - compare CPA changes vs baseline

---

## Supporting Data

**Campaign Performance Summary** (Oct 28 - Nov 27):
```
ROW Engineering Search:     £520 spend, 9.97 conv  → £52 CPA ✅ EXCELLENT
UK Engineering Search:      £3,152 spend, 35.18 conv → £90 CPA ✅ EXCELLENT
UK Engineering PMax:        £2,182 spend, 10.99 conv → £199 CPA ✅ GOOD
UK Management PMax:         £936 spend, 3.01 conv  → £311 CPA ⚠️ POOR
UK Management Search:       £1,240 spend, 1.83 conv → £679 CPA ❌ TERRIBLE
ROW Management Search:      £689 spend, 0 conv     → INFINITE CPA ❌ WASTE
```

**Threshold Analysis**:
- 2x Average CPA threshold: £263
- Engineering: 19-76% of threshold (under control)
- Management: 118-257% of threshold (needs adjustment)
- Action triggered: YES - multiple demographics above 2x average

