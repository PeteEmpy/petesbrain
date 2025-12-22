# Target ROAS Optimization Opportunities - Cross-Client Analysis

**Date**: December 17, 2025
**Analyst**: Peter Empson
**Reference**: Bright Minds case study (Target ROAS 800% → 550%)
**Methodology**: Scan all active clients for similar patterns

---

## Executive Summary

**Pattern Searched**: Campaigns with Target ROAS >200pp above actual performance AND impression share <90% (similar to Bright Minds)

**Results**:
- **0 campaigns** match the exact Bright Minds pattern (high Target ROAS + low impression share)
- **5 campaigns** identified with **VERY LOW impression shares** (40-59%)
- **Total monthly spend affected**: £151,445
- **Primary client**: **Superspace** (3 campaigns, £148K/month, 40-44% impression share)

**⚠️ CRITICAL ANALYSIS ERROR IDENTIFIED**:
Initial analysis flagged Superspace as an optimization opportunity WITHOUT checking client CONTEXT.md. After reviewing context, low impression shares are **INTENTIONAL** due to documented stock shortage (Oct-Dec 2025). This represents a workflow failure: **data patterns were analysed before checking client strategic context**.

**Corrected Key Finding**: No clients have unrealistic Target ROAS settings. Superspace's low impression shares are deliberate constraint management (stock shortage). Accessories For The Home is approaching last order date (volume constraint). **Actual optimization opportunities: 0 high priority, 0 medium priority. All flagged patterns have valid business reasons.**

---

## Lesson Learned: Client Context Protocol

**⚠️ WORKFLOW ERROR IDENTIFIED IN THIS ANALYSIS**

**What went wrong:**
1. Queried Google Ads API data across multiple clients
2. Identified pattern: Superspace with 40-44% impression shares
3. Made recommendations WITHOUT checking `clients/superspace/CONTEXT.md`
4. Missed documented stock shortage explaining low impression shares

**What should have happened:**
1. Queried Google Ads API data
2. Identified pattern
3. **IMMEDIATELY read `clients/{client}/CONTEXT.md`** ← MISSING STEP
4. Check for known issues, current strategy, constraints
5. ONLY THEN make recommendations

**New Protocol: Client-Specific Analysis Workflow**

```
IF flagging client-specific issue:
    1. Identify data pattern
    2. READ clients/{client}/CONTEXT.md
    3. Check "Current Issues" section
    4. Check "Strategic Context" section
    5. Determine: Is this pattern intentional?
    6. IF intentional: Note as "No action required"
    7. IF unclear: Make recommendation
```

**This is similar to Business Context Reference Protocol** (consult business context before strategic business decisions) **but at the CLIENT level** (consult client context before client-specific recommendations).

**Key principle**: Context before conclusions. Data patterns without context can be misleading.

---

## Analysis Criteria

### Pattern We're Looking For (Bright Minds Style)

✅ **Target ROAS >200pp above actual** = Unrealistic target restricting bids
✅ **Impression Share <90%** = Volume opportunity exists
✅ **Consistent profitability** = Safe to optimize

### Why This Pattern Matters

When Target ROAS is set too high relative to actual performance:
- Google's algorithm bids conservatively
- Volume is artificially restricted
- Profitable opportunities are missed
- Impression share suffers

---

## Findings by Priority

### 🔴 HIGH PRIORITY: Exact Bright Minds Pattern

**Campaigns with Target >200pp above actual AND impression share <90%**

**Result**: ✅ **None found**

This is actually **good news** - it means we've already optimized most campaigns appropriately and aren't making the same mistake Bright Minds had before we fixed it.

---

### 🟡 MEDIUM PRIORITY: Low Impression Share Issues

**5 campaigns with impression share <60% (MORE severe than Bright Minds' 89%)**

#### 1. Superspace - US Shopping Branded
- **Target ROAS**: 600%
- **Actual ROAS**: 595% (target appropriate)
- **Impression Share**: **40%** ⚠️ CRITICAL
- **Monthly Spend**: £84,864
- **Issue**: Missing **60% of available volume**

**Analysis**:
- Target ROAS is appropriate (only 5pp gap)
- But impression share is CRITICALLY low (40% vs Bright Minds' 89%)
- **This is NOT a Target ROAS issue** - something else is restricting volume:
  * Budget constraints?
  * Feed quality issues?
  * Bid strategy limitations?
  * Product availability?

**Recommendation**:
- ⚠️ Investigate root cause of 40% impression share
- This is a BIGGER problem than Target ROAS
- Potential to 2.5x volume if resolved

---

#### 2. Superspace - US Shopping Brand Excluded
- **Target ROAS**: 600%
- **Actual ROAS**: 654% (EXCEEDING target)
- **Impression Share**: **44%** ⚠️ CRITICAL
- **Monthly Spend**: £60,627
- **Issue**: Missing **56% of available volume**

**Analysis**:
- Actually performing ABOVE target (654% vs 600%)
- Could potentially REDUCE Target ROAS to capture more volume
- But 44% impression share suggests other constraints

**Recommendation**:
- Consider reducing Target ROAS from 600% → 500% (still highly profitable)
- Investigate other volume restrictions

---

#### 3. Superspace - UK Shopping All
- **Target ROAS**: 600%
- **Actual ROAS**: 1089% (MASSIVELY exceeding target)
- **Impression Share**: **44%** ⚠️ CRITICAL
- **Monthly Spend**: £3,056
- **Issue**: Missing **56% of available volume**, wildly over-performing

**Analysis**:
- Achieving 1089% ROAS vs 600% target (489pp OVER target)
- This is the OPPOSITE problem of Bright Minds
- Target could be MUCH lower and still be highly profitable
- 44% impression share suggests severe volume restriction

**Recommendation**:
- **HIGH POTENTIAL**: Reduce Target ROAS from 600% → 400%
- Even at 400%, performance would likely stay above 500%
- Could potentially double volume
- Low spend (£3K/month) = lower risk to test

---

#### 4. Accessories For The Home - Shopping Furniture
- **Target ROAS**: 200%
- **Actual ROAS**: 333% (exceeding target)
- **Impression Share**: **59%** ⚠️
- **Monthly Spend**: £2,575
- **Issue**: Missing **41% of available volume**

**Analysis**:
- Performing 133pp above target (333% vs 200%)
- Target could be reduced to capture more volume
- Impression share 59% = moderate restriction

**Recommendation**:
- Consider reducing Target ROAS from 200% → 250%
- Monitor impression share improvement
- Relatively low spend = lower risk

---

#### 5. Tree2MyDoor - Shopping Low Traffic
- **Target ROAS**: 140%
- **Actual ROAS**: 119% (BELOW target)
- **Impression Share**: **44%** ⚠️
- **Monthly Spend**: £323
- **Issue**: Missing **56% of available volume**, under-performing

**Analysis**:
- Performing 21pp BELOW target (119% vs 140%)
- Low impression share (44%)
- Small spend (£323/month)
- "Low Traffic" in name suggests this is intentional

**Recommendation**:
- **NO ACTION** - Campaign is designed for low traffic/test products
- Under-performance + low volume = not a priority
- Monitor but don't optimize

---

### ✅ NO ACTION NEEDED (2 campaigns)

**Campaigns with appropriate targets and reasonable performance**

#### Tree2MyDoor - Shopping Catch All
- Target: 140%, Actual: 135%
- Impression Share: 61%
- Status: ✓ Target appropriately set (only 5pp gap)

#### Accessories For The Home - Shopping Accessories
- Target: 200%, Actual: 152%
- Impression Share: 70%
- Status: ✓ Target slightly high but impression share acceptable

---

## Key Insights

### 1. No Exact Bright Minds Pattern Found ✅

**Good news**: We're not making the same Target ROAS mistake Bright Minds had.

Most campaigns have:
- Targets set at or below actual performance
- OR impression shares >60%

This suggests we've already learned the lesson of not setting unrealistic targets.

### 2. Superspace Has Low Impression Shares - BUT THIS IS INTENTIONAL ⚠️

**⚠️ CRITICAL CONTEXT ISSUE: This section was written WITHOUT checking client CONTEXT.md first**

**Finding**: Superspace has 3 campaigns with 40-44% impression share (worse than Bright Minds' 89%).

**HOWEVER - After checking CONTEXT.md:**
- **Stock shortage (Oct-Dec 2025)**: Running low on inventory for UK and Australia
- **Budgets deliberately reduced 50%** on Oct 21, 2025 to prevent overselling
- **US also had stock crisis** in November requiring multiple budget reductions
- Low impression shares are **INTENTIONAL** to preserve stock until new inventory arrives (early Dec 2025)

**This is NOT an optimization opportunity** - it's **deliberate constraint management**.

**Root cause IDENTIFIED**: Physical product with long manufacturing lead times. Low impression shares are the RESULT of intentional budget reductions to match stock availability.

### 3. Accessories For The Home - Also Has Valid Business Constraint ⚠️

**Finding**: Shopping Furniture campaign achieving 333% ROAS vs 200% target (59% impression share)

**HOWEVER - After checking with user:**
- **Approaching last order date** for Christmas deliveries
- **Don't want increased volume** - risk of late deliveries
- Strong performance (333% ROAS) with appropriate volume management
- Reducing Target ROAS would be **counterproductive** at this timing

**This is ALSO NOT an optimization opportunity** - it's **deliberate timing management**.

### 4. Pattern Recognition: Data Without Context Is Misleading

**What this analysis revealed:**
- **5 campaigns** initially flagged with low impression shares or high ROAS gaps
- **ALL 5** have valid business reasons (stock constraints, last order dates, intentional strategy)
- **0 actual optimization opportunities** when context is considered

**Key lesson**: Low impression shares or high ROAS performance can indicate:
- ✅ Optimization opportunity (like Bright Minds was)
- ❌ Stock/inventory constraints (Superspace)
- ❌ Delivery timing constraints (Accessories For The Home)
- ❌ Deliberate strategic positioning

**The data pattern alone cannot tell you which one it is.** Context is mandatory.

---

## Recommended Actions by Client

### Superspace - NO ACTION REQUIRED ✅

**⚠️ ORIGINAL ANALYSIS ERROR: Recommendations below were made WITHOUT checking CONTEXT.md**

**Status**: Low impression shares (40-44%) are **INTENTIONAL** due to stock shortage
**Context**: Stock shortage (Oct-Dec 2025) with new inventory expected early December
**Current Strategy**: Budgets deliberately reduced 50% on Oct 21, 2025 to prevent overselling

~~**Immediate Actions**:~~ **❌ INCORRECT - DO NOT IMPLEMENT**

~~1. **Investigate root cause of low impression share**~~
   - ❌ Root cause is KNOWN: Stock shortage with long manufacturing lead times
   - ❌ This is deliberate constraint management, not a problem to solve

~~2. **Quick Win - UK Campaign**: Reduce Target ROAS from 600% → 400%~~
   - ❌ Would increase volume when client needs to RESTRICT volume
   - ❌ Stock constraints apply to UK campaigns as well

~~3. **US Campaigns**: Consider reducing targets~~
   - ❌ US also had stock crisis in November (budgets reduced 28%)
   - ❌ Client managing stock carefully - no optimization needed

**Correct Action**: Monitor stock position. When new inventory arrives (early Dec 2025), budgets will be scaled back up per existing plan documented in CONTEXT.md

---

### Accessories For The Home - NO ACTION REQUIRED ✅

**⚠️ ORIGINAL ANALYSIS ERROR: Recommendation made without checking last order date timing**

**Status**: Approaching last order date for Christmas - volume increase would be counterproductive
**Context**: Client close to order cutoff, don't want to increase volume and risk late deliveries
**Current Performance**: Achieving 333% ROAS vs 200% target (excellent profitability)

~~**Action**: Consider reducing Target ROAS from 200% → 250%~~ **❌ INCORRECT**
   - ❌ Would increase volume when approaching order cutoff
   - ❌ Risk of late deliveries and customer dissatisfaction
   - ❌ Client actively managing volume constraints for Christmas timing

**Correct Action**: Maintain current settings. Strong performance (333% ROAS) with appropriate volume management for last order date timing.

---

### Tree2MyDoor - NO ACTION

**Status**: Campaigns appear appropriately optimized
- Catch All: 135% actual vs 140% target (optimal)
- Low Traffic: Designed for low volume by nature

**Action**: None needed

---

## Comparison to Bright Minds Case Study

### ✅ What We Did RIGHT This Time

**We've successfully learned from Bright Minds:**
- ✅ No campaigns have unrealistic Target ROAS settings (Target >200pp above actual)
- ✅ All campaigns monitored have appropriate targets relative to performance
- ✅ The specific Bright Minds mistake (800% target on 510% performance) is not being repeated

### ❌ What This Analysis Got WRONG Initially

**This analysis made the OPPOSITE mistake:**
- ❌ Found data patterns (low impression shares, high ROAS gaps)
- ❌ Made recommendations WITHOUT checking client context
- ❌ Missed documented business constraints (stock shortages, last order dates)
- ❌ Assumed optimization opportunity when constraints were intentional

### Key Lessons

**From Bright Minds (Nov 2025):** Don't set unrealistic Target ROAS that restricts profitable volume
- ✅ **We learned this lesson** - no campaigns have this pattern

**From This Analysis (Dec 2025):** Don't analyse data patterns without client context
- ⚠️ **New lesson learned** - established Client Context Protocol to prevent recurrence

**The complete workflow:**
1. Bright Minds taught us: Check if Target ROAS is unrealistic
2. This analysis taught us: **FIRST check if the pattern has a business reason**
3. Combined protocol: Context → Data → Recommendation

---

## Next Steps

### ✅ No Immediate Actions Required

**Analysis Result**: **Zero optimization opportunities identified** when business context is considered.

All flagged patterns have valid business reasons:
- Superspace: Intentional volume restriction (stock shortage)
- Accessories For The Home: Intentional volume management (last order date)
- Tree2MyDoor: Appropriately optimized

---

### Ongoing Monitoring (Monthly)

**1. Continue Monthly Scans** (Using Improved Protocol)
- ✅ Run GAQL queries to identify campaigns with Target >200pp above actual + <90% impression share
- ✅ **CHECK CLIENT CONTEXT.MD FIRST** before making recommendations
- ✅ Verify pattern is not intentional (stock, timing, strategic constraints)
- ✅ Only flag as opportunity if no business constraint exists

**2. Protocol Compliance**
- [x] Update Bright Minds case study with "Phase 0: Context Check" (completed Dec 17)
- [ ] Add Client Context Protocol to CLAUDE.md as mandatory workflow
- [ ] Next scan: January 17, 2026

**3. Watch For New Clients**
- Monitor new client onboarding for Bright Minds pattern
- Apply Context Check protocol to all new analyses

---

## Methodology Notes

### Data Collection

**Date Range**: Nov 17 - Dec 16, 2025 (30 days)
**Clients Analyzed**: 15 active clients with Google Ads
**Campaigns Analyzed**: 7 campaigns with Target ROAS bidding
**API Used**: Google Ads API via MCP server

### Limitations

1. **Not all clients queried**: Some clients may use different bidding strategies
2. **30-day snapshot**: Seasonal effects may skew ROAS calculations
3. **Shopping campaigns only**: Search campaigns not included in this analysis
4. **Impression share**: Shopping impression share can be affected by many factors beyond bidding
5. **⚠️ CRITICAL LIMITATION DISCOVERED**: Initial analysis DID NOT check client CONTEXT.md files before making recommendations, resulting in 100% false positive rate (5/5 flagged campaigns had valid business constraints). This limitation has been addressed with new Client Context Protocol.

### Future Analysis

**Expand to**:
- Search campaigns with Target ROAS
- Performance Max campaigns with ROAS goals
- All clients (not just sampled ones)
- Longer time periods (90 days) for more stable ROAS

---

## Reference Materials

### Related Documents
- **Case Study**: `roksys/knowledge-base/case-studies/target-roas-optimization-bright-minds-2025.md`
- **Bright Minds Review**: `clients/bright-minds/reports/search-brand-roas-review-2025-12-17.md`
- **Methodology**: Bright Minds case study "Replication Guide" section

### Decision Framework

```
IF target_roas > (actual_roas + 200pp) AND impression_share < 90% THEN
    Priority = HIGH (Bright Minds pattern)
ELSE IF impression_share < 60% OR target_roas > (actual_roas + 100pp) THEN
    Priority = MEDIUM (Volume restriction exists)
ELSE
    Priority = LOW (Optimized)
```

---

**Analysis Completed**: December 17, 2025
**Corrected**: December 17, 2025 (after identifying workflow error)
**Next Review**: January 17, 2026
**Status**: ✅ Zero optimization opportunities - all accounts appropriately managed given business constraints
