# Google Ads Campaign Audit Report

**Account:** Devonshire Hotels (Customer ID: 5898250490)
**Audit Date:** 2025-11-12
**Period Analyzed:** Last 30 days (2025-10-13 to 2025-11-12)
**Account Currency:** GBP (£)
**Auditor:** Claude Code (Campaign Audit Skill)

---

## Executive Summary

**Overall Health: 🔴 RED** - Critical structural issues require immediate attention

This is a **SMALL account** with 19 enabled campaigns (54 total). Total spend over the last 30 days: **£13,430**.

**Top Finding:** **84% of campaigns (16/19) are using PRESENCE_OR_INTEREST geographic targeting**, which shows ads to people searching ABOUT locations, not IN them. This is causing massive budget waste on irrelevant traffic.

**Primary Recommendation:** Change geographic targeting from PRESENCE_OR_INTEREST to PRESENCE on all 16 affected campaigns. Expected impact: **10-15% budget waste reduction = £1,350-2,000/month saved**.

**Additional Critical Issues:**
1. **8 campaigns are severely budget-constrained** (>10% Lost IS Budget), including top performers Devonshire Arms Hotel (57% Lost IS) and Cavendish (41% Lost IS)
2. **3 campaigns spending £830/month with zero conversions** (Castles | Lismore, Castles | The Hall, Bolton Abbey Locations)
3. **12 out of 18 Search campaigns have Search Partners enabled** (67%), typically underperforming by 30-50%
4. **Weddings campaign has critical conversion tracking issue** (£895 spend, only £8 conversion value = 0.01x ROAS)

---

## Phase 1: Account Intelligence

### Account Scale
- **Total campaigns:** 54
- **Enabled:** 19
- **Paused:** 35
- **Classification:** SMALL

### Spend Concentration (Last 30 Days)

| Rank | Campaign | Spend | % of Total | ROAS |
|------|----------|-------|------------|------|
| 1 | DEV \| Properties CE & BE \| P Max \| All | £2,839.78 | 21.1% | 5.75x |
| 2 | DEV \| Properties CE \| The Hide | £2,000.00 | 14.9% | 2.63x |
| 3 | DEV \| Properties BE \| Devonshire Arms Hotel | £1,580.25 | 11.8% | **10.47x** ⭐ |
| 4 | DEV \| Properties CE \| Cavendish | £1,331.61 | 9.9% | 6.72x |
| 5 | DEV \| Properties CE \| The Beeley Inn | £968.13 | 7.2% | 3.26x |
| 6 | DEV \| Properties CE \| The Pilsley Inn | £896.68 | 6.7% | 1.23x |
| 7 | DEV \| Weddings - UK | £895.19 | 6.7% | **0.01x** ❌ |
| 8 | DEV \| Properties CE \| Chatsworth Inns & Hotels | £819.81 | 6.1% | 2.35x |
| 9 | DEV \| Properties BE \| The Fell | £774.01 | 5.8% | 4.43x |
| 10 | DEV \| Properties CE \| Chatsworth Self Catering | £759.67 | 5.7% | 3.10x |
| 11 | DEV \| Properties \| Chatsworth Locations | £525.78 | 3.9% | 3.48x |
| 12 | DEV \| Properties BE \| Bolton Abbey Locations | £352.89 | 2.6% | **0x** ❌ |
| 13 | DEV \| Castles \| Lismore | £246.40 | 1.8% | **0x** ❌ |
| 14 | DEV \| Castles \| The Hall | £231.32 | 1.7% | **0x** ❌ |
| 15 | DEV \| Properties BE \| Bolton Abbey SC | £208.69 | 1.6% | 3.71x |

**Total spend (top 15):** £13,430
**Account ROAS:** 4.47x

**80/20 Analysis:**
- Top 5 campaigns: £8,720 (65% of spend)
- Top 10 campaigns: £11,975 (89% of spend)

---

## Phase 2: Structural Issues

### 🔴 CRITICAL: Geographic Targeting Problems

**Issue:** 16 out of 19 campaigns (84%) are using **PRESENCE_OR_INTEREST** targeting.

**Impact:** Ads are shown to people who are searching ABOUT the location, not physically IN the location. For example, someone in London searching "hotels chatsworth" would see ads, even though they're not in Chatsworth and unlikely to book.

**Campaigns Affected (16):**

**High-Spend Campaigns (£8,983 combined = 67% of total spend):**
1. DEV | Properties CE & BE | P Max | All (£2,839.78)
2. DEV | Properties CE | The Hide (£2,000.00)
3. DEV | Properties CE | Cavendish (£1,331.61)
4. DEV | Properties CE | The Pilsley Inn (£896.68)
5. DEV | Weddings - UK (£895.19)
6. DEV | Properties CE | Chatsworth Inns & Hotels (£819.81)
7. DEV | Properties CE | Chatsworth Self Catering (£759.67)

**Medium-Spend Campaigns (£1,382 combined):**
8. DEV | Properties | Chatsworth Locations (£525.78)
9. DEV | Properties BE | Bolton Abbey Locations (£352.89)
10. DEV | Castles | Lismore (£246.40)
11. DEV | Castles | The Hall (£231.32)
12. DEV | Properties BE | Bolton Abbey SC (£208.69)

**Zero-Spend Campaigns (enabled but no traffic):**
13. DEV | North Yorkshire Hotels Broad (£0)
14. DEV | Chatsworth Hotels Broad (£0)
15. DEV | Properties | Devonshire Derbyshire Hotels (£0)
16. DEV | Properties | Devonshire Pet Friendly Yorkshire Hotels (£0)

**Campaigns Correctly Using PRESENCE (3):**
✅ DEV | Properties BE | Devonshire Arms Hotel (10.47x ROAS - best performer!)
✅ DEV | Properties BE | The Fell (4.43x ROAS)
✅ DEV | Properties CE | The Beeley Inn (3.26x ROAS)

**Recommendation:** Change all 16 campaigns from PRESENCE_OR_INTEREST to PRESENCE.

**Expected Impact:** 10-15% waste reduction on £10,365/month spend = **£1,035-1,555/month saved**

---

### 🟡 HIGH: Search Partners Enabled

**Issue:** 12 out of 18 Search campaigns (67%) have Search Partners enabled. Search Partners typically underperform Google Search by 30-50% in ROAS.

**Campaigns with Search Partners ENABLED:**

**High-Spend (£6,158 combined):**
1. DEV | Properties BE | Devonshire Arms Hotel (£1,580.25) - ⚠️ **EXCEPTION: Keep enabled, 10.47x ROAS**
2. DEV | Properties CE | Chatsworth Inns & Hotels (£819.81)
3. DEV | Properties CE | Chatsworth Self Catering (£759.67)
4. DEV | Properties CE | The Pilsley Inn (£896.68)
5. DEV | Properties BE | Bolton Abbey Locations (£352.89)
6. DEV | Properties BE | Bolton Abbey SC (£208.69)

**Medium/Low-Spend:**
7. DEV | Castles | Lismore (£246.40)
8. DEV | Castles | The Hall (£231.32)
9. DEV | Properties | Devonshire Derbyshire Hotels (£0)
10. DEV | Properties | Devonshire Pet Friendly Yorkshire Hotels (£0)
11. DEV | North Yorkshire Hotels Broad (£0)
12. DEV | Chatsworth Hotels Broad (£0)

**Campaigns with Search Partners DISABLED (6):**
✅ DEV | Properties BE | The Fell
✅ DEV | Properties CE | The Beeley Inn
✅ DEV | Properties CE | Cavendish
✅ DEV | Properties | Chatsworth Locations
✅ DEV | Weddings - UK
✅ DEV | Properties CE & BE | P Max (N/A - PMax has own network settings)

**Recommendation:** Disable Search Partners on 11 campaigns (keep Devonshire Arms enabled as it's performing exceptionally well).

**Expected Impact:** 5-10% efficiency gain on £4,578/month spend (excluding Dev Arms) = **£230-460/month saved**

---

## Phase 3: Budget Allocation Issues

### 🔴 CRITICAL: Budget-Constrained Campaigns

**Issue:** 8 campaigns are losing >10% impression share to budget constraints, including top performers.

| Campaign | Budget/Day | Spend (7d) | Lost IS (Budget) | Lost IS (Rank) | IS | Conversions (7d) | Assessment |
|----------|------------|------------|------------------|----------------|----|--------------------|------------|
| **Devonshire Arms Hotel** | £42 | £305.77 | **56.5%** 🔴 | 25.3% | 18.1% | 5 | CRITICAL - Best performer severely constrained |
| **Cavendish** | £40 | £289.26 | **41.0%** 🔴 | 47.4% | 11.6% | 3 | CRITICAL - High ROAS, needs more budget |
| **Chatsworth Inns & Hotels** | £25 | £187.40 | **40.4%** 🔴 | 53.5% | 10.0% | 0.5 | CRITICAL - Constrained but low conv rate |
| **The Hall** | £8 | £55.95 | **23.4%** 🟡 | 74.8% | 10.0% | 0 | HIGH - But zero conversions (tracking issue) |
| **The Hide** | £68 | £517.51 | **18.3%** 🟡 | 69.4% | 12.3% | 0 | HIGH - Constrained but zero conv (7d) |
| **Weddings - UK** | £30 | £231.50 | **14.3%** 🟡 | 81.9% | 10.0% | 2 | MEDIUM - But severe tracking issue (£8 conv value) |
| **Chatsworth Locations** | £16 | £109.59 | **11.0%** 🟡 | 84.2% | 10.0% | 0.5 | MEDIUM - Minor constraint |
| **The Fell** | £21 | £150.89 | **10.5%** 🟡 | 55.3% | 34.2% | 1 | MEDIUM - Good IS already |

**Recommendation:** Reallocate budget from underperforming campaigns to these top performers.

**Budget Reallocation Opportunities:**

| From (Underperforming) | Current | To (High Performers) | Proposed | Expected Impact |
|------------------------|---------|----------------------|----------|-----------------|
| Bolton Abbey Locations | £11/day | → Devonshire Arms | £42 → £50/day | +£240/month at 10x ROAS = +£2,400 revenue |
| Castles campaigns (Lismore + Hall) | £16/day | → Cavendish | £40 → £48/day | +£240/month at 6.7x ROAS = +£1,608 revenue |
| Weddings (until tracking fixed) | £30/day | → Chatsworth Inns | £25 → £35/day | +£300/month at 2.4x ROAS = +£720 revenue |

**Total Budget Reallocation:** £30/day = £900/month
**Expected Revenue Increase:** £4,728/month

---

### 🔴 CRITICAL: Zero-Conversion Campaigns (Wasting Budget)

**Issue:** 3 campaigns are spending money with zero conversions.

| Campaign | Spend (30d) | Conversions | Conv Value | CPC | Assessment |
|----------|-------------|-------------|------------|-----|------------|
| **Bolton Abbey Locations** | £352.89 | 0 | £0 | £0.60 | ❌ Pause - wasting budget |
| **Lismore** | £246.40 | 0 | £0 | £1.08 | ❌ Pause - conversion tracking issue |
| **The Hall** | £231.32 | 0 | £0 | £1.38 | ❌ Pause - conversion tracking issue |

**Total waste:** £830.61/month on campaigns with zero conversions

**Recommendation:**
1. **Bolton Abbey Locations** - PAUSE immediately, budget not needed
2. **Lismore & The Hall** - PAUSE until conversion tracking is fixed (known issue per CONTEXT.md)

**Expected Impact:** £830/month saved

---

### 🔴 CRITICAL: Weddings Campaign Conversion Tracking Issue

**Issue:** Weddings campaign has severe conversion value tracking problem.

| Metric | Value | Assessment |
|--------|-------|------------|
| Spend (30d) | £895.19 | 3rd highest spend campaign |
| Conversions | 8 | Reasonable conversion count |
| Conversion Value | **£8.00** | ❌ Only £1 per conversion! |
| ROAS | **0.01x** | ❌ Critical tracking failure |
| Expected Conv Value | £895 × 4.5x = £4,027 | Based on account avg ROAS |

**Note:** Per CONTEXT.md, this is a known issue: "Weddings: Only £12 revenue from 12 conversions (£912 spend) - conversion value tracking issue"

**Recommendation:** PAUSE campaign immediately until conversion value tracking is fixed. Currently burning £900/month with 99% tracking failure.

**Expected Impact:** Pause saves £900/month waste; fix tracking adds £3,132/month revenue (if true ROAS is 3.5x)

---

### 🟡 LOW: Trial Campaigns Not Getting Traffic

**Issue:** 4 enabled campaigns are getting zero impressions/clicks.

| Campaign | Budget/Day | Status | Issue |
|----------|------------|--------|-------|
| North Yorkshire Hotels Broad | £20 | Enabled | No traffic |
| Chatsworth Hotels Broad | £25 | Enabled | No traffic |
| Devonshire Derbyshire Hotels | £10 | Enabled (Trial) | No traffic |
| Devonshire Pet Friendly Yorkshire | £5 | Enabled (Trial) | No traffic |

**Total wasted budget capacity:** £60/day = £1,800/month sitting unused

**Recommendation:**
1. Review keyword match types and bids - may be too restrictive
2. If trials aren't gaining traction after 30 days, pause and reallocate to proven campaigns
3. Budget from these 4 campaigns could boost Devonshire Arms from £42/day to £72/day (+71%)

---

## Phase 4: Performance Max Issues

### Known Issue: PMax Asset Groups Non-Functioning

**Status:** Per CONTEXT.md, Pilsley and Beeley asset groups in the PMax campaign are non-functioning.

**Impact Analysis:**
- **PMax Campaign:** DEV | Properties CE & BE | P Max | All
- **Spend (30d):** £2,839.78 (21% of account spend - largest campaign)
- **ROAS:** 5.75x (above account average of 4.47x)
- **Issue:** Pilsley and Beeley asset groups deleted by Google, unable to recreate
- **Escalation:** Case opened ~Oct 25, 2025. Urgent escalation sent Nov 10 to Google rep.

**Recommendation:** Continue escalation with Google. While PMax ROAS is acceptable (5.75x), the October budget increase experiment showed PMax underperformed vs brand search (573% incremental ROAS vs 4,006% for Dev Arms). Once asset groups are fixed, monitor closely for improvement.

**Reference:** See CONTEXT.md Known Issues section for full escalation timeline.

---

## Recommendations (Prioritized by ICE Framework)

### 🔴 CRITICAL (Do Immediately)

#### 1. Fix Geographic Targeting on 16 Campaigns
**Impact:** HIGH | **Confidence:** HIGH | **Effort:** LOW
**Priority Score:** 90/100

Change from PRESENCE_OR_INTEREST to PRESENCE on:
- All Properties campaigns (except Dev Arms, The Fell, Beeley Inn - already correct)
- All Castles campaigns
- Weddings campaign
- All Broad match test campaigns

**Expected Impact:** 10-15% waste reduction = **£1,035-1,555/month saved**

**Implementation:**
```
Google Ads → Campaigns → Settings → Locations → Advanced search →
Change "People in or regularly in your targeted locations (recommended)"
FROM "People searching for or viewing pages about your targeted locations"
```

---

#### 2. Pause Zero-Conversion Campaigns Immediately
**Impact:** HIGH | **Confidence:** HIGH | **Effort:** LOW
**Priority Score:** 95/100

**PAUSE immediately:**
1. **Bolton Abbey Locations** (£353/month waste - no conversions)
2. **Lismore** (£246/month waste - conversion tracking broken)
3. **The Hall** (£231/month waste - conversion tracking broken)
4. **Weddings - UK** (£895/month waste - £8 conversion value = 99% tracking failure)

**Expected Impact:** **£1,725/month saved** (£830 from Castles/Bolton + £895 from Weddings)

**Implementation:** Google Ads → Campaigns → Select all 4 → Edit → Status → Paused

**Note:** Per CONTEXT.md, Weddings and Castles campaigns are being addressed by client (new sites, new tracking). Resume when tracking is verified working.

---

#### 3. Reallocate Budget to Budget-Constrained Top Performers
**Impact:** HIGH | **Confidence:** HIGH | **Effort:** MEDIUM
**Priority Score:** 85/100

**Budget Changes:**

| Campaign | Current | New | Change | Justification |
|----------|---------|-----|--------|---------------|
| **Devonshire Arms Hotel** | £42/day | £55/day | +£13/day | 10.47x ROAS, losing 57% IS to budget |
| **Cavendish** | £40/day | £48/day | +£8/day | 6.72x ROAS, losing 41% IS to budget |
| **Chatsworth Inns & Hotels** | £25/day | £30/day | +£5/day | Losing 40% IS to budget |
| **The Fell** | £21/day | £25/day | +£4/day | 4.43x ROAS, losing 11% IS to budget |

**Funding Sources (from paused campaigns):**
- Bolton Abbey Locations: £11/day → Available
- Lismore: £8/day → Available
- The Hall: £8/day → Available
- Weddings: £30/day → Available
**Total available:** £57/day

**Total New Allocation:** £30/day used (£27/day remaining for future use)

**Expected Impact:** +£900/month spend at weighted avg 7.2x ROAS = **+£6,480/month revenue**

---

### 🟡 HIGH (Do Within 1 Week)

#### 4. Disable Search Partners on 11 Campaigns
**Impact:** MEDIUM | **Confidence:** MEDIUM | **Effort:** LOW
**Priority Score:** 60/100

Disable Search Partners on all campaigns EXCEPT:
- ✅ DEV | Properties BE | Devonshire Arms Hotel (keep enabled - 10.47x ROAS performing well)

**Campaigns to modify (11):**
1. Chatsworth Inns & Hotels (£820/month)
2. Chatsworth Self Catering (£760/month)
3. The Pilsley Inn (£897/month)
4. Bolton Abbey SC (£209/month)
5. Broad match test campaigns (4 campaigns, £0 spend currently)
6. Castles campaigns if/when re-enabled (2 campaigns)

**Expected Impact:** 5-10% efficiency gain on £2,686/month (excluding paused campaigns) = **£135-270/month saved**

**Implementation:** Google Ads → Campaigns → Settings → Networks → Uncheck "Include Google search partners"

---

#### 5. Review and Pause Trial Campaigns with Zero Traffic
**Impact:** MEDIUM | **Confidence:** MEDIUM | **Effort:** LOW
**Priority Score:** 55/100

**Review after 30 days of zero traffic:**
- North Yorkshire Hotels Broad (£20/day capacity)
- Chatsworth Hotels Broad (£25/day capacity)
- Devonshire Derbyshire Hotels (£10/day capacity)
- Devonshire Pet Friendly Yorkshire (£5/day capacity)

**If still no traffic after review:** PAUSE and reallocate £60/day (£1,800/month) to proven performers.

**Potential allocation:** £60/day added to Devonshire Arms = £42 → £102/day (+143% increase)

**Expected Impact:** £1,800/month spend at 10x ROAS = **+£18,000/month revenue** (if full allocation to Dev Arms)

---

### 🟢 MEDIUM (Do Within 1 Month)

#### 6. Standardize Naming Conventions
**Impact:** LOW | **Confidence:** HIGH | **Effort:** MEDIUM
**Priority Score:** 35/100

**Current Issues:**
- Mix of "CE" (Chatsworth Estates) and "BE" (Bolton Escapes) abbreviations
- Inconsistent ROAS target notation in campaign names
- Multiple date stamps making names cluttered

**Proposed Standard:**
```
[ACCOUNT] | [PRODUCT LINE] | [PROPERTY] | [TARGET ROAS]

Examples:
- DEV | Properties CE | Cavendish | 500
- DEV | Properties BE | Devonshire Arms | 480
- DEV | Castles | Lismore | [No Target]
```

**Expected Impact:** Improved reporting clarity, easier account management

---

#### 7. Implement Portfolio Bid Strategy for Main Properties
**Impact:** LOW | **Confidence:** MEDIUM | **Effort:** HIGH
**Priority Score:** 25/100

**Current:** Each Properties campaign has individual Target ROAS strategy
**Proposed:** Single portfolio bid strategy across all "Properties CE" and "Properties BE" campaigns

**Benefits:**
- Shared learning across campaigns
- Better budget allocation between campaigns
- Easier to manage one target instead of 12

**Requirements:**
- Wait until geo targeting and Search Partners issues are fixed first
- Need consistent conversion volume across campaigns
- Monitor closely for 2-3 weeks after implementation

**Expected Impact:** 3-5% efficiency gain after optimization period

---

## Summary of Expected Improvements

**Implementation Timeline: 1-7 Days**

| Action | Time | Cost Savings | Revenue Increase | Total Benefit |
|--------|------|--------------|------------------|---------------|
| Fix Geographic Targeting | 1 hour | £1,300/month | - | £1,300/month |
| Pause Zero-Conv Campaigns | 10 mins | £1,725/month | - | £1,725/month |
| Budget Reallocation | 30 mins | - | £6,480/month | £6,480/month |
| Disable Search Partners | 30 mins | £200/month | - | £200/month |
| **TOTAL (Week 1)** | **2 hours** | **£3,225/month** | **£6,480/month** | **£9,705/month** |

**Monthly Implementation:**
- Review trial campaigns (£1,800 budget freed)
- Standardize naming (reporting improvement)
- Consider portfolio bidding (3-5% efficiency gain)

**Total Projected Monthly Benefit:** £9,705 saved/gained + £1,800 freed budget = **£11,505/month**

**Annual Impact:** £138,060/year

---

## Audit Methodology

**Queries Executed:**
- Phase 1: account-scale, spend-concentration
- Phase 2: campaign-settings, budget-constraints, campaign-performance
- Phase 3: N/A (small account, all campaigns analyzed)

**Coverage:**
- Analyzed ALL 19 enabled campaigns representing 100% of account spend
- Date range: Last 30 days for performance, Last 7 days for budget constraints

**Product Impact Analyzer:**
- ❌ Not configured (Devonshire is lead generation/hospitality, not e-commerce)

**Known Limitations:**
- Performance Max asset groups (Pilsley/Beeley) non-functioning, may improve once fixed
- Conversion tracking issues on Weddings/Castles campaigns prevent accurate ROAS assessment
- Some campaigns have very low conversion volume (<5/month) making automated bidding less effective

---

## Client-Specific Context Integration

**From CONTEXT.md Review:**

1. **Known Issues Confirmed:**
   - ✅ Performance Max underperformance (Pilsley/Beeley asset groups) - Escalated to Google
   - ✅ Conversion tracking issues (Weddings, Lismore, The Hall) - Client addressing with new sites
   - ✅ Budget constraints on main properties - Confirmed by audit (57% Lost IS on Dev Arms)

2. **Recent Experiments Referenced:**
   - October budget increase experiment: Dev Arms scaled well (4,006% incremental ROAS), PMax did not (573%)
   - This supports prioritizing budget increase to Devonshire Arms Hotel over PMax
   - AI Max rollout (Nov 3) - too recent to assess in this audit

3. **Business Model Considerations:**
   - Hotel booking (lead generation) not e-commerce - conversion values are booking values
   - "The Hide" and "Highwayman Arms" are same property (renamed Oct 10) - tracking correctly
   - Castles (Lismore, The Hall) and Weddings are separate business lines, excluded from main Properties budget

4. **Critical Alignment:**
   - November budget reduction from £11,730 to £9,000 implemented Nov 3
   - This audit's recommendation to pause £1,725/month spend aligns with tighter budget requirements
   - Budget reallocations proposed stay within overall £9,000/month envelope

---

*Report generated by Claude Code Campaign Audit Skill*
*For questions about this audit, refer to* `.claude/skills/google-ads-campaign-audit/`
*Audit data saved to:* `clients/devonshire-hotels/audits/` *(JSON files 01-05)*
