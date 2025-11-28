# NMA (National Motorsport Academy) Performance Audit - November 2025

**Account ID**: 5622468019
**Audit Date**: November 10, 2025
**Period Analyzed**: Last 30 days
**Status**: ⚠️ **UNDERPERFORMING - Multiple Issues Identified**

---

## Executive Summary

The NMA account is significantly underperforming with several critical issues:

1. **Extremely High CPCs**: £947 average CPC on Engineering Search (should be £50-200 for education)
2. **Performance Max Failure**: Management PMax campaign has £67 CPC but only 1 conversion from 13,718 clicks
3. **Poor Quality Scores**: Multiple keywords with QS 3-5 (should be 7+)
4. **Budget Inefficiency**: Spending £8,100 for just 47.8 conversions (£169 cost per conversion)
5. **ROW Campaigns Zero Performance**: Rest of World campaigns spending £950 with 10 conversions total

---

## Campaign Performance (Last 30 Days)

### Overall Account Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| **Total Spend** | £8,145.95 | High |
| **Total Conversions** | 47.8 | **Very Low** ❌ |
| **Cost Per Conversion** | £170.42 | **Very High** ❌ |
| **Total Clicks** | 24,186 | High |
| **Total Impressions** | 1,299,197 | Reasonable |
| **Overall CTR** | 1.86% | Low |

**Comparison to NDA**: NDA achieves £191 CPA after budget cuts. NMA at £170 seems comparable BUT:
- NMA has far fewer conversions (47.8 vs NMA should be achieving 100+)
- NMA campaigns show structural problems NDA doesn't have

---

## Campaign-by-Campaign Analysis

### 1. NMA | Search | UK | Engineering 55 Ai 25/8
**Budget**: £100/day | **Spend**: £2,906 | **Conv**: 19 | **CPA**: £152.95

✅ **Positives**:
- Best performing campaign (19 conversions)
- Decent CTR (9.08%)
- AI Max enabled

❌ **Critical Issues**:
- **CPC £947** - **CATASTROPHICALLY HIGH** ❌❌❌
  - Should be £1-3 for education keywords
  - Suggests severe bidding strategy problem
- Many keywords with QS 5 or below
- "race car mechanic school" - 310 clicks, 0 conversions, £284 spent

**Root Cause**: Likely Target CPA or Max Conversions bidding set way too high, or portfolio bid strategy misconfigured

---

### 2. NMA | P Max | UK | Engineering Max Conv 46 100 19/11
**Budget**: £70/day | **Spend**: £2,135 | **Conv**: 17 | **CPA**: £125.63

✅ **Positives**:
- Good conversion volume (17)
- Best CPA in account (£125)
- Reasonable CPC (£379)

⚠️ **Issues**:
- CTR only 0.78% (very low for PMax)
- Still room for optimization
- Asset groups may need review

**Status**: Best performing campaign - **KEEP AND OPTIMIZE**

---

### 3. NMA | Search | UK | Management 100 Ai 25/8
**Budget**: £40/day | **Spend**: £1,186 | **Conv**: 0.83 | **CPA**: £1,437

❌ **Critical Issues**:
- **CPC £1,386** - **EVEN WORSE THAN ENGINEERING** ❌❌❌
- Only 0.83 conversions from £1,186 spend
- £1,437 cost per conversion is **UNACCEPTABLE**
- Quality scores 3-7 range

**Recommendation**: **PAUSE IMMEDIATELY** - Fix bidding strategy before reactivating

---

### 4. NMA | P Max | UK | Management 100
**Budget**: £30/day | **Spend**: £917 | **Conv**: 1 | **CPA**: £917

❌ **DISASTER CAMPAIGN**:
- **13,718 clicks for only 1 conversion** ❌❌❌
- **CPC £67** (reasonable for PMax)
- **CTR 2.64%** (decent)
- **0.0073% conversion rate** (catastrophic)

**Root Causes**:
- Asset groups likely targeting wrong audience
- Landing pages not relevant
- May be targeting "motorsport management" too broadly (attracting job seekers, not students)
- Possible tracking issue (only 1 conv from 13k clicks is statistically improbable)

**Recommendation**: **PAUSE AND REBUILD** from scratch

---

### 5. NMA | Search | ROW | Management 100
**Budget**: £21.96/day | **Spend**: £651 | **Conv**: 0 | **CPA**: N/A

❌ **Zero Conversions**:
- 563 clicks, no conversions
- CPC £1,157 (very high)
- Targeting international markets with UK-specific offer may not resonate

**Recommendation**: **PAUSE** - No evidence this works

---

### 6. NMA | Search | ROW | Engineering 100
**Budget**: £10/day | **Spend**: £298 | **Conv**: 10 | **CPA**: £29.86

✅ **STANDOUT PERFORMER**:
- **£29.86 CPA** - **BEST IN ACCOUNT** ✅✅✅
- 10 conversions from £298 spend
- CPC £843 (high but converting)
- ROW markets responding well to engineering

**Recommendation**: **INCREASE BUDGET** - This is a hidden gem

---

## Keyword Quality Score Analysis

### Critical Quality Score Issues

**Quality Score 3 (Needs Urgent Attention)**:
- "mechanical engineering degree" - 1,137 impressions
- "automotive engineering universities uk" - 110 impressions
- "international business management" - 134 impressions
- "how to become an f1 engineer" - 112 impressions

**Quality Score 4-5 (Below Average)**:
- "car engineering courses" - 4,808 impressions (QS 5)
- "online engineering degree" - 3,561 impressions (QS 5)
- "motor engineering course" - 3,505 impressions (QS 5)
- "motorsport engineering degree" - 5,369 impressions (QS 5)

**Quality Score 7-10 (Good to Excellent)**:
- "motorsport academy" - 863 impressions (QS 10) ✅
- "motorsport courses" - 1,817 impressions (QS 8) ✅
- "motorsport engineering courses" - 2,303 impressions (QS 8) ✅

---

## Conversion Tracking Assessment

### Conversion Actions Setup

| Conversion Action | Type | Conversions | Value | Status |
|-------------------|------|-------------|-------|--------|
| **NMA Enhanced Conversions For Leads** | Purchase | 0.83 | £8,875.81 | ✅ Working |
| **application_complete** (GA4) | Default | 42 | £42 | ✅ Working |
| **application_approved** (GA4) | Default | 5 | £5 | ✅ Working |

**Total**: 47.8 conversions

⚠️ **Issues**:
1. **Three different conversion actions** creates attribution confusion
2. Enhanced Conversions shows £8,875.81 value for 0.83 conversions = £10,750 per conversion (seems misconfigured)
3. GA4 conversions have £1 values (need proper value assignment)
4. Management PMax showing only 1 conversion suggests possible tracking issues

**Recommendation**: Audit conversion tracking setup - values appear incorrect

---

## Top Issues Ranked by Priority

### 🔴 CRITICAL (Fix Immediately)

1. **Search CPC Crisis**: £947-£1,386 CPCs are 10-20x too high for education
   - **Cause**: Portfolio bid strategy likely misconfigured or Target CPA set at £1,000+
   - **Fix**: Check bid strategy settings, reduce Target CPA to £50-100, or switch to Manual CPC temporarily
   - **Impact**: Fixing this alone would 10x account performance

2. **Management PMax Disaster**: 13,718 clicks, 1 conversion
   - **Cause**: Wrong audience targeting or landing page mismatch
   - **Fix**: Pause campaign, review asset groups, check search terms
   - **Impact**: Save £900/month immediately

3. **Conversion Value Misconfiguration**: £10,750 per conversion in Enhanced Conversions
   - **Cause**: Likely passing incorrect value from backend
   - **Fix**: Audit Enhanced Conversions implementation
   - **Impact**: Bidding strategies using wrong values = waste

### 🟡 HIGH PRIORITY (Fix This Week)

4. **Quality Score Issues**: 15+ keywords with QS 3-5
   - **Cause**: Ad copy/landing page relevance issues
   - **Fix**: Rewrite ads to match keyword intent, improve landing pages
   - **Impact**: 30-50% CPC reduction possible

5. **Management Search Campaign**: £1,437 CPA unacceptable
   - **Cause**: Same CPC issues as Engineering + poor conversion rate
   - **Fix**: Pause until Search CPC crisis resolved
   - **Impact**: Save £1,186/month

6. **ROW Management Zero Conversions**: £651 wasted
   - **Cause**: UK-specific course may not resonate internationally
   - **Fix**: Pause or restructure with international-specific messaging
   - **Impact**: Save £650/month

### 🟢 MEDIUM PRIORITY (Optimize Soon)

7. **Engineering PMax Underperforming CTR**: 0.78% CTR
   - **Cause**: Asset groups need fresh creative
   - **Fix**: Add more assets, test different messaging
   - **Impact**: 20-30% improvement possible

8. **Budget Reallocation Needed**: ROW Engineering performing at £29 CPA vs UK Engineering at £152
   - **Cause**: Budget not aligned with performance
   - **Fix**: Shift budget from UK Engineering to ROW Engineering
   - **Impact**: 5x more conversions from same spend

---

## Immediate Action Plan

### Week 1 (Nov 11-17): Emergency Fixes

**Day 1-2** (Critical):
1. ✅ **Audit bid strategies** - Check if portfolio bid strategy exists, verify Target CPA settings
2. ✅ **Pause worst performers**:
   - Management PMax (£917 for 1 conversion)
   - Management UK Search (£1,437 CPA)
   - Management ROW Search (0 conversions)
3. ✅ **Fix Search CPC crisis**:
   - If portfolio bid strategy: Check Target CPA (likely set at £1,000+, should be £80-150)
   - If campaign-level: Switch Engineering Search to Manual CPC at £2-5 temporarily
   - Monitor for 24-48 hours

**Day 3-5** (Stabilize):
4. ✅ **Audit conversion tracking**:
   - Check Enhanced Conversions implementation
   - Verify GA4 conversion values are correct
   - Test Management PMax tracking (1 conv from 13k clicks seems wrong)
5. ✅ **Quality Score fixes**:
   - Pause QS 3 keywords
   - Rewrite ads for QS 4-5 keywords to improve relevance
6. ✅ **Budget reallocation**:
   - Increase ROW Engineering from £10/day to £30/day (£29 CPA is excellent)
   - Reduce UK Engineering from £100/day to £55/day (until CPC fixed)

**Day 6-7** (Optimize):
7. ✅ **Review search terms** - Add negatives for irrelevant terms
8. ✅ **Asset group audit** - Review Engineering PMax for CTR improvement opportunities
9. ✅ **Create weekly monitoring dashboard** - Track CPC, CPA, Quality Scores

---

### Week 2-4 (Nov 18 - Dec 8): Optimization & Testing

**Engineering PMax** (currently best performer):
- Add new headline/description assets
- Test different audience signals
- Upload fresh imagery/videos
- Target: Improve 0.78% CTR to 1.5%+

**Search Campaigns** (after CPC fixed):
- Expand keyword lists for high-performing terms
- Test AI Max on ROW campaigns (currently manual)
- Implement RSAs with dynamic keyword insertion
- Target: Reduce average CPA from £152 to £80-100

**Management Campaigns** (rebuild):
- Create new PMax asset groups with student-focused messaging (not job seekers)
- Test dedicated landing pages for Management vs Engineering
- Consider separate campaigns for "MBA motorsport" vs "motorsport management degree"
- Target: Achieve £100-150 CPA (currently £917-£1,437)

---

## Comparison to NDA Account

| Metric | NDA | NMA | Assessment |
|--------|-----|-----|------------|
| **Daily Spend** | £765 | £271 | NMA smaller scale |
| **Cost Per Conversion** | £191 | £170 | NMA slightly better CPA ✅ |
| **Conversion Volume** | 4/day | 1.6/day | **NMA very low** ❌ |
| **CPC Range** | £50-200 | £67-£1,386 | **NMA has extreme outliers** ❌ |
| **Quality Scores** | 6-8 average | 3-7 average | **NMA worse** ❌ |
| **PMax Performance** | Mixed | Disaster on Management | **NMA worse** ❌ |

**Key Difference**: NDA has consistent performance across campaigns. NMA has huge variance - some campaigns excellent (ROW Engineering £29 CPA), others catastrophic (Management Search £1,437 CPA).

---

## Strategic Recommendations

### Short-term (November)
1. **Fix bid strategy crisis** - This is the #1 issue. £947 CPCs will bankrupt the account.
2. **Pause underperformers** - Stop bleeding £2,500/month on broken campaigns
3. **Scale winners** - ROW Engineering at £29 CPA is a goldmine, give it more budget
4. **Conversion tracking audit** - Values appear misconfigured, affecting all bidding

### Medium-term (December)
1. **Rebuild Management campaigns** - Current setup not working, needs fresh approach
2. **Landing page optimization** - 13k clicks for 1 conversion suggests landing page issues
3. **Quality Score improvement** - Rewrite ads, improve relevance, reduce CPCs by 30-50%
4. **Budget alignment** - Shift from UK to ROW if ROW continues outperforming

### Long-term (Q1 2026)
1. **Conversion value optimization** - Assign proper values to application stages
2. **Expand high performers** - Once CPC fixed, scale Engineering campaigns
3. **Geographic expansion** - If ROW Engineering works, test other international markets
4. **Cross-academy learning** - Apply NDA optimizations that worked to NMA

---

## Budget Impact Projections

### Current State (November)
- **Spend**: £8,100/month
- **Conversions**: 47.8
- **CPA**: £170

### If Immediate Fixes Applied (Estimated December)
- **Pause underperformers**: Save £2,500/month
- **Fix Search CPC (10x improvement)**: 10x more conversions from Search
- **Reallocate to ROW Engineering**: 3x conversions from shifted budget

**Projected December**:
- **Spend**: £5,600/month (paused £2,500 of waste)
- **Conversions**: 120+ (vs 47.8)
- **CPA**: £47 (vs £170)

**ROI Impact**: 2.5x more conversions at 1/4 the cost = **10x improvement in efficiency**

---

## Next Steps

1. **Run this audit by client** (Paul Riley) - Get buy-in for pausing campaigns
2. **Access bid strategy settings** - Identify the root cause of CPC crisis
3. **Implement Week 1 actions** - Emergency fixes first
4. **Monitor daily** - Watch for CPC normalization
5. **Weekly progress report** - Update client on improvements

---

## Appendix: Technical Details

### Portfolio Bid Strategy Check Needed
```
If account uses portfolio bid strategy:
- Check target CPA setting (likely £800-1,000, should be £80-150)
- Check if multiple campaigns sharing strategy
- Consider campaign-level strategies instead for better control
```

### Conversion Tracking Audit Required
```
Enhanced Conversions For Leads showing:
- 0.825657 conversions = £8,875.81 value
- = £10,750 per conversion
- This suggests backend is passing £10,750 as course value
- Bidding strategies will optimize to this value
- May be correct (if courses are £10k) or misconfigured
```

### Quality Score Improvement Process
```
For each QS 3-5 keyword:
1. Review ad copy - Does it mention the exact keyword?
2. Check landing page - Does headline match keyword?
3. Review CTR - Is it above 5% for Search?
4. Add exact match version if using broad
5. Test new ad copy with keyword in headline
```

---

**Audit Completed By**: Claude Code
**Next Review**: November 18, 2025 (after Week 1 fixes)
**Client Contact**: Paul Riley (pk@nda.ac.uk)
