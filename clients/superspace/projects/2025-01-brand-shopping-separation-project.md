# Superspace - Brand Shopping Separation Project

**Status**: Planning (January 2025)
**Priority**: P2 (Strategic improvement - not urgent)
**Source**: Nils Rooijmans technique ([AMA] Brand campaigns in Shopping with PMax)
**Created**: 2025-11-27

---

## Executive Summary

**Objective**: Separate brand and non-brand traffic in Shopping campaigns to force Performance Max to optimise for non-brand conversions instead of taking credit for low-hanging brand searches.

**Why This Matters for Superspace**:
- Current PMax campaigns likely capturing branded searches ("superspace tiles", "superspace magnetic tiles")
- High ROAS from brand searches masks underperformance on non-brand searches
- Smart bidding optimises aggregate ROAS, allowing PMax to coast on brand performance
- Separating brand gives tight control over brand CPC, impression share, and product selection

**Strategic Fit**:
- Superspace has strong brand recognition (unique product positioning)
- Currently running PMax as primary campaign type (90%+ of budget)
- Target ROAS bidding strategy (600% current, 550% normal) - perfect for this technique
- Q4 2025 stock crisis showed need for granular budget control

**Timeline**: January 2025 (after Q4 peak, when stock position stabilises)

---

## The Technique (Nils Rooijmans Method)

### For PMax Accounts (Superspace's Situation)

Create a **dual-priority Shopping campaign structure** to force brand searches away from PMax:

1. **High-Priority Shopping Campaign** (Brand Catcher)
   - Contains same products as brand campaign
   - Purpose: Catches all non-brand traffic before PMax sees it
   - Extremely low manual CPC bids (£0.05-£0.10)
   - Negative keyword list with ALL brand terms attached
   - Minimal spend expected (acts as filter)

2. **Medium-Priority Shopping Campaign** (Brand Campaign)
   - Contains products to show for brand searches
   - Purpose: Serves all brand searches with high visibility
   - High manual CPC bids or Target ROAS bidding
   - Brand traffic flows here (filtered from high-priority campaign)

3. **PMax Campaigns** (Non-Brand Forced)
   - Negative keyword list with ALL brand terms attached
   - Forced to optimise for non-brand conversions only
   - Can no longer coast on easy brand conversions

### How Priority Funneling Works

**Traffic Flow**:
```
User Search Query
    ↓
High-Priority Shopping (catches all non-brand) → Very low bids → Minimal spend
    ↓
Medium-Priority Brand Shopping (catches all brand) → High bids → Maximum visibility
    ↓
PMax (catches nothing - has brand negatives) → Forced to find non-brand conversions
```

**Brand Terms Negative List** (attached to high-priority AND all PMax campaigns):
- superspace
- superspace tiles
- super space
- get superspace
- getsuperspace
- + all variations/misspellings

---

## Current Superspace Account Structure

### Existing Campaigns (US Market - Nov 2025)

| Campaign | Type | Budget/Day | Target ROAS | Purpose |
|----------|------|------------|-------------|---------|
| Shopping Branded | Shopping | £3,229 | 600% | Brand searches |
| P Max Brand Excluded | PMax | £2,809 | 600% | Non-brand (allegedly) |
| Shopping Brand Excluded | Shopping | £2,352 | 600% | Non-brand Shopping |
| Search Brand Inclusion | Search | £1,403 | 600% | Brand Search |
| Search Generics | Search | £604 | 600% | Non-brand Search |

**Total US Budget**: £10,397/day (down from £14,460 peak due to stock crisis)

### Key Observations

✅ **Already has brand/non-brand separation attempt**:
- "Shopping Branded" campaign exists
- "Shopping Brand Excluded" campaign exists
- "P Max Brand Excluded" campaign exists

❓ **Unknown Implementation Quality**:
- Are brand negatives actually attached to PMax?
- Is Shopping Branded using low-priority (wrong) or high+medium priority (correct)?
- Are brand terms comprehensive?

⚠️ **Potential Issues**:
- Shopping Branded has £3,229/day budget (33% of total) - suggests it's getting significant traffic
- If Shopping Branded is low-priority (common mistake), it's only catching overflow
- PMax "Brand Excluded" name suggests negatives exist, but need verification

---

## Requirements for Implementation

### 1. Account Audit (Week 1 - January 2025)

**What to Check**:

□ **Current Brand Negative Lists**:
- Does "P Max Brand Excluded" actually have brand negatives attached?
- What terms are in the brand negative list?
- Are negatives comprehensive (include misspellings, variations)?

□ **Current Shopping Campaign Priorities**:
- What priority is "Shopping Branded" campaign? (Low, Medium, or High?)
- What priority is "Shopping Brand Excluded"?
- What products are in each campaign?

□ **Current Performance Split**:
- Pull search term report for all Shopping campaigns (last 90 days)
- Identify what % of Shopping traffic is brand vs non-brand
- Measure ROAS difference: brand searches vs non-brand searches
- Check if PMax is showing for brand searches (shouldn't be if negatives work)

□ **Budget Distribution**:
- Current: Shopping Branded £3,229/day (31% of total)
- Is this spend on brand searches or leaking to non-brand?

**Audit Script**:
```python
# Use Google Ads API to pull:
# 1. Campaign priorities (shopping_campaign.priority)
# 2. Negative keyword lists attached to each campaign
# 3. Search term report by campaign (last 90 days)
# 4. Performance by brand/non-brand classification
```

**Expected Findings**:
- Shopping Branded is likely low-priority (common mistake)
- Brand negative list exists but may not be attached to PMax
- Some brand searches leaking to PMax campaigns

---

### 2. Brand Term Research (Week 1)

**Compile Comprehensive Brand Term List**:

**Core Brand Terms**:
- superspace
- super space
- superspace tiles
- super space tiles
- get superspace
- getsuperspace

**Product Name Variations**:
- superspace magnetic tiles
- superspace building tiles
- superspace giant tiles
- superspace life size tiles

**Common Misspellings** (use voice-to-text + typo patterns):
- supaspace
- supurspace
- superspce
- super-space

**Competitor Comparison Searches** (brand + competitor):
- superspace vs magna tiles
- superspace vs picasso tiles
- superspace magna tiles

**Research Methods**:
1. Pull existing Shopping search term report (90 days)
2. Filter for queries containing "superspace" or "super space"
3. Identify patterns and variations
4. Check Google Search Console for brand query patterns
5. Review Shopify site search logs for how customers search

**Deliverable**: Brand negative keyword list (50-100 terms, exact + phrase match)

---

### 3. Campaign Structure Redesign (Week 2)

**New Structure** (following Nils technique exactly):

**Campaign A: High-Priority Non-Brand Filter**
- **Name**: "US Shopping | High Priority Filter | Non-Brand"
- **Type**: Standard Shopping
- **Priority**: High
- **Products**: All products (same as brand campaign)
- **Bidding**: Manual CPC - £0.05 default bid
- **Budget**: £500/day (shared with medium-priority campaign)
- **Negative Keywords**: Brand negative list attached
- **Purpose**: Catches all non-brand traffic, spends almost nothing (low bids)

**Campaign B: Medium-Priority Brand Campaign**
- **Name**: "US Shopping | Medium Priority | Brand"
- **Type**: Standard Shopping
- **Priority**: Medium
- **Products**: All products (same as high-priority campaign)
- **Bidding**: Target ROAS 600% (or manual CPC £2-3)
- **Budget**: £3,500/day (shared with high-priority campaign)
- **Negative Keywords**: None (receives brand traffic filtered from high-priority)
- **Purpose**: Serves all brand searches with maximum visibility

**Campaign C: PMax Non-Brand Forced**
- **Name**: "US P Max | Brand Excluded | Non-Brand"
- **Type**: Performance Max
- **Products**: All products
- **Bidding**: Target ROAS 600%
- **Budget**: £6,000/day
- **Negative Keywords**: Brand negative list attached (forces non-brand optimization)
- **Purpose**: Forced to find non-brand conversions

**Shared Budget Setup**:
- High-priority + Medium-priority campaigns share budget (£3,500/day total)
- Ensures high-priority never runs out of budget before medium-priority
- Prevents non-brand traffic leaking to medium-priority campaign

**Settings Alignment** (critical):
- All campaigns: Same location targeting (US)
- All campaigns: Same ad schedule (24/7)
- All campaigns: Same device targeting (all)
- All campaigns: Same audience targeting (none/observation only)

---

### 4. Product Feed Review (Week 1-2)

**Verify Products**:

□ All products must exist in:
- High-priority non-brand filter campaign
- Medium-priority brand campaign
- PMax campaigns

□ Product titles in Merchant Center optimized for:
- Non-brand searches: "Giant Magnetic Building Tiles for Kids - Life Size Fort Builder"
- Brand searches will work regardless (searching "superspace" will match any title)

□ Check Merchant Center feed for:
- Product count: ~10-15 SKUs (Big Set, Rectangles, Squares, variations)
- All products approved and active
- No disapprovals blocking product inclusion

**Superspace Merchant Center ID**: 645236311

---

### 5. Implementation Plan (Week 3)

**Day 1 - Setup**:
1. Create brand negative keyword list (if doesn't exist)
2. Create high-priority Shopping campaign (£0.05 bids, brand negatives attached)
3. Create medium-priority Shopping campaign (Target ROAS 600%, no negatives)
4. Create shared budget (£3,500/day)
5. Pause old "Shopping Branded" campaign
6. Verify brand negatives attached to all PMax campaigns

**Day 2 - Verification**:
1. Test brand searches (manual Google search for "superspace tiles")
2. Confirm ads showing from medium-priority campaign (check auction insights)
3. Confirm high-priority campaign showing minimal impressions
4. Check search term reports (should see brand terms in medium-priority only)

**Day 3-7 - Monitoring**:
1. Daily check: search term reports for leakage
2. Monitor high-priority campaign spend (should be <£50/day)
3. Monitor medium-priority campaign spend (should be ~£3,000/day)
4. Check PMax campaign search terms (should have ZERO brand terms)

**Week 2-4 - Learning Period**:
- PMax needs 14-30 days to adapt to non-brand traffic
- Expect ROAS drop initially (PMax loses easy brand conversions)
- Monitor non-brand search term performance closely
- Compare: Previous aggregate ROAS vs new non-brand ROAS (apples-to-apples)

---

### 6. Success Metrics

**Technical Success** (Implementation):
- [ ] Zero brand searches appearing in PMax search term reports
- [ ] 95%+ of brand searches flowing to medium-priority campaign
- [ ] High-priority campaign spending <£100/day
- [ ] Shared budget preventing non-brand leakage to medium-priority

**Performance Success** (30 days post-implementation):

**Brand Campaign Performance**:
- Target ROAS: 800%+ (brand searches convert very well)
- Target CPA: £30-40 (lower than non-brand)
- Target Impression Share: 90%+ for brand terms

**PMax Non-Brand Performance**:
- Initial ROAS: Expect 400-500% (drop from 600% due to losing brand)
- 30-day ROAS: Target 550%+ (should recover as algorithm adapts)
- Non-brand CPA: £60-70 (higher than brand, still profitable)

**Overall Account**:
- Total conversions: Maintain or increase (better optimization of each traffic type)
- Blended ROAS: May drop 50-100 points initially, should recover
- Non-brand impression share: Increase (PMax forced to compete)

**Strategic Success**:
- Visibility into true brand vs non-brand performance
- Ability to scale non-brand independently
- Protection of brand traffic during stock shortages (can pause brand campaign independently)

---

### 7. Required Resources

**Time Investment**:
- Week 1 (Audit): 4-6 hours (account analysis, search term research)
- Week 2 (Setup): 3-4 hours (campaign build, testing)
- Week 3-4 (Monitoring): 2 hours/week (daily checks, reporting)
- **Total**: ~15 hours over 4 weeks

**Tools Needed**:
- Google Ads API access (for audit scripts) ✅ Already available
- Search term report export (90 days) ✅ Standard reporting
- Merchant Center access ✅ Already have (ID: 645236311)
- Spreadsheet for brand term research ✅ Google Sheets

**Skills Required**:
- Shopping campaign priority understanding ✅ Core PPC knowledge
- Negative keyword list management ✅ Standard capability
- Python scripting for audit ✅ Already available (existing scripts)

**No Additional Costs**:
- No new tools needed
- No budget increase required (restructuring existing £10k/day)
- No client approval needed initially (testing phase)

---

### 8. Risks & Mitigation

**Risk 1: PMax Performance Drop**
- **Likelihood**: High (expected during learning period)
- **Impact**: ROAS drops 100-150 points for 14-30 days
- **Mitigation**:
  - Implement in January (lowest-risk period, post-Q4)
  - Monitor daily, ready to pause if drop >200 ROAS points
  - Client expects testing period (January = experimentation month)

**Risk 2: Brand Traffic Leakage**
- **Likelihood**: Medium (misconfiguration possible)
- **Impact**: Non-brand searches leak to brand campaign, waste budget
- **Mitigation**:
  - Shared budget setup (high-priority always funded first)
  - Daily search term report checks (Week 1-2)
  - Automated script to alert on brand terms in PMax

**Risk 3: Budget Shift Impacts Stock**
- **Likelihood**: Low (January = lower demand)
- **Impact**: Unexpected sales spike if brand campaign over-performs
- **Mitigation**:
  - January timing (stock position should be stable)
  - Can quickly pause brand campaign if stock concerns arise
  - Budget caps on both campaigns (£3,500/day total brand)

**Risk 4: Incomplete Brand Term List**
- **Likelihood**: Medium (always some edge cases)
- **Impact**: Brand searches slip through to PMax, dilute results
- **Mitigation**:
  - Comprehensive research phase (Week 1)
  - Ongoing monitoring and additions (search term reports)
  - Use broad match negatives where appropriate

---

### 9. Decision Gates

**GO Decision** (Implement in January 2025):
✅ Stock position stable (new inventory arrived early Dec)
✅ Post-Q4 experimentation window (lower risk period)
✅ Current brand/non-brand split unclear (audit reveals issues)
✅ Client receptive to testing (Ant/Craig data-driven)
✅ 15 hours time investment available

**NO-GO Decision** (Defer or abandon):
❌ Audit reveals brand separation already working perfectly
❌ Stock constraints continue (risky to experiment)
❌ Client prioritizes other initiatives (Demand Gen, NZ expansion)
❌ Q1 budget cuts reduce testing tolerance

**PAUSE Decision** (Implement but halt after Week 1):
⚠️ PMax ROAS drops >200 points
⚠️ Brand traffic leaking significantly (>20% to wrong campaign)
⚠️ Stock issues re-emerge
⚠️ Client requests pause for other priorities

---

### 10. Client Communication

**When to Discuss**:
- Early January 2025 (after Q4 debrief, before implementation)
- Frame as: "Optimization opportunity discovered through industry research"

**Talking Points**:

**Problem Statement**:
"Currently, your Performance Max campaigns are likely taking credit for easy brand searches (people searching 'superspace tiles'). This masks underperformance on harder non-brand searches. We can't see the true performance split."

**Solution**:
"Industry best practice (Nils Rooijmans technique) uses Shopping campaign priority layers to separate brand and non-brand traffic. This forces PMax to optimize for non-brand conversions instead of coasting on brand."

**Benefits for Superspace**:
1. **Visibility**: See true brand vs non-brand performance (currently hidden)
2. **Control**: Tight control over brand CPC and impression share
3. **Optimization**: PMax forced to find new non-brand customers (better long-term)
4. **Flexibility**: Can pause brand independently during stock shortages

**Expected Impact**:
- Short-term: ROAS may dip 50-100 points for 2-4 weeks (learning period)
- Long-term: Better optimization of each traffic type, more non-brand growth
- January timing = lowest risk (post-Q4, stock stable)

**Ask**:
"Can we proceed with implementation in early January? I'll monitor daily and pause immediately if we see issues."

---

## Next Steps

**December 2025**:
- [ ] File this project plan
- [ ] Monitor for stock position stabilisation (new inventory arrival)
- [ ] Wait for Q4 to complete

**Early January 2025**:
- [ ] Discuss with Ant/Craig (client approval)
- [ ] Run account audit (Week 1)
- [ ] Compile brand term list (Week 1)
- [ ] Review audit findings, confirm GO/NO-GO decision

**Mid-January 2025** (if GO):
- [ ] Implement campaign structure (Week 2-3)
- [ ] Daily monitoring (Week 3-4)
- [ ] 30-day performance review (end of January)

---

## Reference Materials

**Source Email**: `/Users/administrator/Documents/PetesBrain/roksys/knowledge-base/google-ads/shopping/2025-11-27_nils-brand-campaigns-shopping-pmax.md`

**Knowledge Base Locations**:
- `/Users/administrator/Documents/PetesBrain/roksys/knowledge-base/google-ads/shopping/`
- `/Users/administrator/Documents/PetesBrain/roksys/knowledge-base/google-ads/performance-max/`

**Nils Rooijmans**:
- Daily newsletter: https://nilsrooijmans.com/daily/
- Email: nilsr@nilsrooijmans.com

**Related Superspace Documents**:
- CONTEXT.md: `/Users/administrator/Documents/PetesBrain/clients/superspace/CONTEXT.md`
- Current campaign structure documented in CONTEXT.md lines 295-343

---

## Document History

| Date | Change | Updated By |
|------|--------|------------|
| 2025-11-27 | Initial project plan created from Nils email technique | Claude Code |

