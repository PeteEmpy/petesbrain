# Product Impact Analyzer - Enhancement Research
**Date**: 2025-12-28
**Session Type**: Enhancement Planning & Research
**Status**: ✅ Research Complete - Awaiting Prioritisation

---

## 🎯 Research Objective

Generate enhancement ideas to provide greater insight into e-commerce client performance, specifically focusing on how individual product changes impact overall account performance.

**Context**: Product Impact Analyzer monitors 17 e-commerce clients. Individual product changes (disapprovals, price changes, stock outages, label transitions) can have significant impact on revenue and ROAS.

---

## 🔍 Current System Strengths

### Data Collection & Automation
- **17 Clients Tracked**: Comprehensive coverage across e-commerce portfolio
- **5 LaunchAgents**: Fully automated data collection and monitoring
  - Weekly analysis (Tuesday 9 AM)
  - Daily tracking (7:45 AM)
  - Real-time monitoring (every 2 hours)
  - Daily data fetching (7 AM)
  - Daily Sheets sync (8 AM)

### Intelligence & Alerting
- **Product Hero Classification**: Heroes/Sidekicks/Villains/Zombies segmentation
- **Multi-level Alerting**: Per-client configurable thresholds
- **Historical Trend Analysis**: 4-week rolling baselines
- **Label Transition Tracking**: Monitors product status changes over time
- **Per-client Google Sheets Integration**: Automated reporting

---

## 🚨 Critical Gaps Identified

### 1. **Product Feed Errors (CRITICAL)**
**Impact**: 5 clients affected (BMPM, Grain Guard, Crowd Control, Just Bin Bags, Just Bin Bags JHD)
**Error**: `'str' object has no attribute 'get'`
**Result**: Availability status shows "NOT_SET"
**Priority**: P0 - Fix before new features

### 2. **Missing Cross-Client Intelligence**
**Current State**: Each client analysed in isolation
**Opportunity**: Patterns across clients could reveal platform-wide issues or seasonal trends
**Example**: If 5 clients all see Heroes drop same week = likely Google Merchant Centre policy change

### 3. **No Proactive Opportunity Detection**
**Current State**: Reactive alerts when things go wrong
**Opportunity**: Proactive alerts when opportunities emerge
**Example**: "Product X became a Hero - consider featuring in PMAX assets"

### 4. **Limited Revenue Attribution**
**Current State**: Heroes/Sidekicks/Villains/Zombies by clicks/conversions
**Opportunity**: Revenue-weighted classification shows true impact
**Example**: High-value product with low conversions = Hero (current system may miss this)

### 5. **No Competitive Intelligence**
**Current State**: Only internal product performance data
**Opportunity**: External context (Google Trends, competitor pricing) provides strategic insight

### 6. **Zombie Reactivation Not Automated**
**Current State**: Manual review of Zombies
**Opportunity**: Automated scoring of "reactivation probability" saves time

### 7. **Disapproval Monitoring Stale**
**Current State**: Last snapshot 6 days old
**Opportunity**: Verify agent health, ensure critical alerts aren't missed

---

## 💡 12 Enhancement Ideas

### 🟢 Quick Wins (1 Week Implementation)

#### 1. **Fix Product Feed Loading Error**
**Problem**: 5 clients can't load availability status
**Solution**: Debug `'str' object has no attribute 'get'` error in feed parsing
**Impact**: Restores full monitoring coverage
**Effort**: 2-3 hours
**Priority**: P0

#### 2. **Opportunity Alerts for Label Changes**
**Problem**: Zombies → Heroes transitions not flagged proactively
**Solution**: Add alert type: "🎯 Opportunity: Product became a Hero"
**Impact**: Catch revenue opportunities faster
**Effort**: 4-6 hours (add alert logic + email template)
**Priority**: P1

#### 3. **Multi-Variable Root Cause Dashboard**
**Problem**: Alerts show "Hero dropped" but not why
**Solution**: When alert fires, show: price change %, stock status, label transition, disapproval status
**Impact**: Faster diagnosis, less manual investigation
**Effort**: 6-8 hours (aggregate data sources, update alert format)
**Priority**: P1

#### 4. **Disapproval Monitor Health Check**
**Problem**: Last snapshot 6 days old, uncertain if agent running
**Solution**: Add health check to `monitor.py` to verify disapproval agent status
**Impact**: Ensures critical alerts aren't missed
**Effort**: 2-3 hours
**Priority**: P0

---

### 🟡 Strategic Improvements (2-3 Weeks Implementation)

#### 5. **Cross-Client Pattern Detection**
**Concept**: Analyse Heroes/Villains across all clients to detect platform-wide issues
**Example Alert**: "⚠️ 5 clients saw Hero drops this week - possible Google Merchant Centre policy change"
**Data Sources**: Existing product snapshots across all clients
**Output**: Weekly "Cross-Client Intelligence" email section
**Impact**: Catch systemic issues before they spread
**Effort**: 12-16 hours (cross-client aggregation + pattern detection logic)
**Priority**: P2

#### 6. **Smart Zombie Reactivation Scorer**
**Concept**: Score each Zombie on "reactivation probability" based on historical patterns
**Factors**:
- Was this a Hero in past 90 days? (+50 points)
- High historical conversion rate? (+30 points)
- Stock recently restored? (+20 points)
- Price competitive vs baseline? (+20 points)
**Output**: "Top 10 Zombies to Reactivate" weekly report
**Impact**: Prioritise which Zombies worth re-investing in
**Effort**: 16-20 hours (scoring algorithm + historical data analysis)
**Priority**: P2

#### 7. **Revenue Attribution Breakdown**
**Concept**: Re-classify Heroes/Sidekicks/Villains/Zombies using revenue weight, not just conversions
**Change**: Hero = Top 20% revenue contributors (not just conversion volume)
**Impact**: Identifies high-value low-volume products missed by current system
**Data Sources**: `metrics.conversions_value` from Google Ads API
**Effort**: 10-12 hours (update classification logic + historical recalculation)
**Priority**: P1

#### 8. **Weekly Performance Summary Email**
**Concept**: Consolidated weekly email showing trends across all clients
**Sections**:
- Total Heroes/Sidekicks/Villains/Zombies count changes
- Top 5 rising stars (Sidekicks → Heroes)
- Top 5 falling stars (Heroes → Villains)
- Cross-client patterns detected
- Recommended actions
**Impact**: One email replaces 17 individual client reviews
**Effort**: 12-16 hours (aggregation logic + email template)
**Priority**: P2

---

### 🔵 Advanced Capabilities (1-2 Months Implementation)

#### 9. **Google Trends Integration**
**Concept**: Correlate product performance with search demand trends
**Example**: "Rose Bushes revenue down 15% + Google Trends shows 20% demand drop = seasonal, not campaign issue"
**Data Sources**: Google Trends API + existing product data
**Output**: Trend correlation section in weekly reports
**Impact**: Distinguishes campaign issues from market trends
**Effort**: 20-24 hours (API integration + correlation logic)
**Priority**: P3

#### 10. **Competitive Price Intelligence**
**Concept**: Track competitor pricing for top products to identify margin compression
**Data Sources**: Google Shopping API (competitor price data)
**Alert**: "⚠️ Competitor undercutting Hero product by 15%"
**Impact**: Proactive price competitiveness monitoring
**Effort**: 24-30 hours (API integration + price scraping + storage)
**Priority**: P3
**Note**: Requires Google Shopping API access or web scraping

#### 11. **Predictive ROAS Modeling**
**Concept**: Predict ROAS impact if specific products are paused/promoted
**Model**: Train ML model on historical product status → ROAS correlation
**Output**: "If you pause these 3 Villains, expect +8% ROAS improvement"
**Impact**: Data-driven product management decisions
**Effort**: 40-50 hours (data pipeline + model training + validation)
**Priority**: P3
**Note**: Requires sufficient historical data (6+ months)

#### 12. **Interactive Performance Dashboard**
**Concept**: Web-based dashboard for real-time product performance exploration
**Features**:
- Filter by client, Hero status, date range
- Visualise label transitions over time
- Drill down into individual products
- Export custom reports
**Tech Stack**: Flask + Chart.js or Plotly
**Impact**: Self-service analysis, reduces manual report requests
**Effort**: 50-60 hours (full-stack development + deployment)
**Priority**: P3

---

## 🗺️ Implementation Roadmap

### Phase 1: Critical Fixes (1 Week)
**Goal**: Restore full system health + quick wins
1. Fix product feed loading error (P0)
2. Verify disapproval monitor health (P0)
3. Add opportunity alerts for label changes (P1)
4. Build multi-variable root cause dashboard (P1)

**Outcome**: System fully operational + faster diagnosis

---

### Phase 2: Strategic Intelligence (2-3 Weeks)
**Goal**: Smarter insights + less manual work
5. Implement revenue attribution breakdown (P1)
6. Build cross-client pattern detection (P2)
7. Create weekly performance summary email (P2)
8. Develop smart Zombie reactivation scorer (P2)

**Outcome**: One weekly email replaces 17 individual reviews + revenue-weighted insights

---

### Phase 3: Advanced Capabilities (1-2 Months)
**Goal**: External intelligence + predictive power
9. Integrate Google Trends correlation (P3)
10. Add competitive price intelligence (P3)
11. Build predictive ROAS modeling (P3)
12. Launch interactive performance dashboard (P3)

**Outcome**: Market context + predictive insights + self-service exploration

---

## 🎯 Prioritisation Questions

**Before selecting enhancements to implement, clarify:**

1. **What questions do you ask most often when reviewing reports?**
   - Helps prioritise dashboard/alert enhancements

2. **How much time do you spend manually investigating alerts?**
   - Justifies multi-variable root cause dashboard investment

3. **Which clients generate the most 'noise' vs 'signal' in alerts?**
   - Informs cross-client pattern detection priority

4. **Would you use an interactive dashboard, or prefer email reports?**
   - Determines if Dashboard (Enhancement 12) is worth 50-60 hour investment

5. **Are there external data sources you already pay for?**
   - Google Trends, competitor intelligence tools, etc.
   - Helps prioritise external integrations

---

## 📊 Enhancement Comparison Matrix

| Enhancement | Effort (Hours) | Impact | Priority | Dependencies |
|-------------|----------------|--------|----------|--------------|
| 1. Fix Product Feed Error | 2-3 | Critical | P0 | None |
| 4. Disapproval Monitor Health | 2-3 | Critical | P0 | None |
| 2. Opportunity Alerts | 4-6 | High | P1 | None |
| 3. Multi-Variable Dashboard | 6-8 | High | P1 | #1 (product feed fix) |
| 7. Revenue Attribution | 10-12 | High | P1 | None |
| 8. Weekly Summary Email | 12-16 | Medium | P2 | None |
| 5. Cross-Client Patterns | 12-16 | Medium | P2 | None |
| 6. Zombie Reactivation Scorer | 16-20 | Medium | P2 | #7 (revenue attribution) |
| 9. Google Trends Integration | 20-24 | Medium | P3 | Google Trends API |
| 10. Competitive Price Intel | 24-30 | Medium | P3 | Google Shopping API |
| 11. Predictive ROAS Model | 40-50 | High | P3 | 6+ months historical data |
| 12. Interactive Dashboard | 50-60 | High | P3 | Flask/web framework |

---

## 🔄 Next Steps

**Awaiting user feedback on:**
1. Which enhancements to prioritise
2. Answers to 5 prioritisation questions above
3. Budget/time allocation for implementation

**Recommended Starting Point** (if unsure):
- **Week 1**: Implement Phase 1 (Critical Fixes) - restores system health + immediate wins
- **Week 2-3**: User reviews impact, decides on Phase 2 priorities
- **Month 2+**: Evaluate Phase 3 based on Phase 1/2 results

---

**Research Completed**: 2025-12-28
**Status**: ✅ Ready for user prioritisation
**Documentation**: This file + session-log.md entry
