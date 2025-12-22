# Chatsworth Inns Campaign - Negative Keywords Implementation Plan

**Date Created**: 2025-12-22
**Campaign**: DEV | Core Properties CE | Chatsworth Escapes Inns & Hotels
**Campaign ID**: 2080736142
**Issue**: Property cannibalization causing 35.1% wasted spend (£83.59 over 15 days)
**Status**: Ready for implementation

---

## Executive Summary

**Problem**: The "Chatsworth Escapes Inns & Hotels" campaign is capturing searches for properties with dedicated campaigns (The Hide, Pilsley Inn, Beeley Inn), resulting in:
- 211 wasted clicks (35.1% of total)
- £83.59 wasted spend over 15 days (Dec 8-22)
- Zero conversions from property-specific searches
- Budget cannibalization across campaigns

**Solution**: Add 18 negative keywords (14 property-specific, 4 informational) to prevent overlap with dedicated property campaigns.

**Expected Impact**:
- Save £167/month in wasted spend
- Reduce zero-conversion clicks by 35%
- Improve campaign ROAS by focusing on true generic searches
- Eliminate inter-campaign competition

---

## Negative Keywords Required

### Property-Specific Negatives (Prevent Cannibalization)

**Properties with Dedicated Campaigns:**

| Property | Dedicated Campaign ID | Negative Keywords | Match Type | Rationale |
|----------|----------------------|-------------------|------------|-----------|
| **The Hide** | 23069490466 | hide | EXACT | Prevents "the hide", "hide hotel", "hide chatsworth" |
| | | hide | PHRASE | Blocks all hide variations |
| | | highwayman | EXACT | Old property name (pre-Oct 2025) |
| | | highwayman | PHRASE | Blocks all highwayman variations |
| **Pilsley Inn** | 19534106385 | pilsley | EXACT | Prevents "pilsley inn", "the pilsley inn" |
| | | pilsley | PHRASE | Blocks all pilsley variations |
| **Beeley Inn** | 22539873565 | beeley | EXACT | Prevents "beeley inn chatsworth" |
| | | beeley | PHRASE | Blocks all beeley variations |
| **Devonshire Arms** | 19577006833 | devonshire arms | PHRASE | Prevents "devonshire arms hotel" searches |
| **The Fell** | 22666031909 | fell | PHRASE | Prevents "the fell", "fell hotel" |
| **Cavendish** | 21839323410 | cavendish | PHRASE | Prevents "cavendish hotel baslow" |

**Wasted Spend from Properties (Dec 8-22)**:
- The Hide: £33.63 (80 clicks)
- Pilsley Inn: £45.16 (115 clicks)
- Beeley Inn: £4.80 (16 clicks)
- **Total**: £83.59 (211 clicks)

---

### Informational/Non-Commercial Negatives

| Search Intent | Negative Keywords | Match Type | Rationale |
|---------------|-------------------|------------|-----------|
| **Menu searches** | menu | EXACT | "pilsley inn menu" - not booking intent |
| | menus | EXACT | Plural variation |
| **Pub searches** | pub | EXACT | "chatsworth pubs" - food/drink, not accommodation |
| | pubs | EXACT | Plural variation |

**Wasted Spend from Informational (Dec 8-22)**:
- Menu searches: £0.33 (12 clicks)
- Pub searches: £2.19 (10 clicks)
- **Total**: £2.52 (22 clicks)

---

## Complete Negative Keyword List (18 Total)

**Copy-Paste Ready for Google Ads:**

```
hide
hide
highwayman
highwayman
pilsley
pilsley
beeley
beeley
devonshire arms
fell
cavendish
menu
menus
pub
pubs
```

**Match Type Assignment:**
1. hide - EXACT
2. hide - PHRASE
3. highwayman - EXACT
4. highwayman - PHRASE
5. pilsley - EXACT
6. pilsley - PHRASE
7. beeley - EXACT
8. beeley - PHRASE
9. devonshire arms - PHRASE
10. fell - PHRASE
11. cavendish - PHRASE
12. menu - EXACT
13. menus - EXACT
14. pub - EXACT
15. pubs - EXACT

---

## Implementation Plan

### Option 1: Manual Implementation (Google Ads UI)

**Time Required**: 10 minutes

**Steps**:

1. **Open Google Ads UI**
   - Navigate to account 5898250490
   - Go to Campaigns → "DEV | Core Properties CE | Chatsworth Escapes Inns & Hotels"

2. **Access Negative Keywords**
   - Click "Keywords" in left menu
   - Click "Negative keywords" tab
   - Click blue "+" button

3. **Add Negative Keywords**
   - Select "Add to campaign"
   - Paste keywords (one per line):
     ```
     hide
     highwayman
     pilsley
     beeley
     devonshire arms
     fell
     cavendish
     menu
     menus
     pub
     pubs
     ```

4. **Set Match Types**
   - Add EXACT match for: hide, highwayman, pilsley, beeley, menu, menus, pub, pubs
   - Add PHRASE match for: hide, highwayman, pilsley, beeley, devonshire arms, fell, cavendish

5. **Save and Verify**
   - Click "Save"
   - Verify 18 negative keywords appear in list
   - Check match types are correct

---

### Option 2: Automated Implementation (Google Ads MCP)

**Time Required**: 5 minutes (scripted)

**Prerequisites**:
- Google Ads Change Protection Protocol
- Backup current campaign state

**Implementation Script**:

```python
# Step 1: Create backup
from google_ads_backup_integration import create_backup_with_mcp

backup = create_backup_with_mcp(
    customer_id='5898250490',
    campaign_id='2080736142',
    change_description='Add 18 negative keywords to prevent property cannibalization',
    expected_changes={
        'negative_keywords_added': 18,
        'campaigns_modified': ['2080736142']
    }
)

# Step 2: Add negative keywords via MCP
negative_keywords = [
    {'text': 'hide', 'match_type': 'EXACT'},
    {'text': 'hide', 'match_type': 'PHRASE'},
    {'text': 'highwayman', 'match_type': 'EXACT'},
    {'text': 'highwayman', 'match_type': 'PHRASE'},
    {'text': 'pilsley', 'match_type': 'EXACT'},
    {'text': 'pilsley', 'match_type': 'PHRASE'},
    {'text': 'beeley', 'match_type': 'EXACT'},
    {'text': 'beeley', 'match_type': 'PHRASE'},
    {'text': 'devonshire arms', 'match_type': 'PHRASE'},
    {'text': 'fell', 'match_type': 'PHRASE'},
    {'text': 'cavendish', 'match_type': 'PHRASE'},
    {'text': 'menu', 'match_type': 'EXACT'},
    {'text': 'menus', 'match_type': 'EXACT'},
    {'text': 'pub', 'match_type': 'EXACT'},
    {'text': 'pubs', 'match_type': 'EXACT'},
]

mcp__google_ads__add_campaign_negative_keywords(
    customer_id='5898250490',
    campaign_id='2080736142',
    keywords=negative_keywords
)

# Step 3: Verify changes
# Query negative keywords to confirm all 18 were added
```

**Note**: Google Ads MCP currently has `add_campaign_negative_keywords` tool available.

---

## Monitoring & Validation Plan

### Immediate Validation (Within 24 Hours)

**Check 1: Negative Keywords Applied**
- [ ] Verify all 18 negative keywords appear in campaign
- [ ] Verify match types are correct (EXACT vs PHRASE)
- [ ] Check for any API errors or warnings

**Check 2: Search Terms Report**
- [ ] Monitor Dec 23-24 search terms
- [ ] Confirm zero "hide", "pilsley", "beeley" searches
- [ ] Ensure legitimate searches still triggering ads

---

### 7-Day Performance Review (Dec 23-29)

**Metrics to Track**:

| Metric | Before (Dec 8-22) | Expected After | Actual After |
|--------|-------------------|----------------|--------------|
| Daily clicks | ~16/day | ~10/day | ___ |
| Daily spend | £15.88/day | £10.32/day (-35%) | £___ |
| Conversions | 0 | 1-2 | ___ |
| Property searches | 211 clicks | 0 clicks | ___ |
| Wasted spend | £83.59 (15 days) | £0 | £___ |

**Success Criteria**:
- ✅ Zero clicks on property-specific searches (hide, pilsley, beeley)
- ✅ Spend reduction of 30-40%
- ✅ At least 1 conversion within 7 days
- ✅ Remaining searches are truly generic "chatsworth" queries

**Red Flags**:
- 🚨 Spend drops >50% (over-negation blocking legitimate searches)
- 🚨 Zero impressions (campaign effectively disabled)
- 🚨 Still seeing property searches in search terms report

---

### 30-Day Strategic Review (Dec 23 - Jan 22)

**Question to Answer**: Should this campaign continue to exist?

**Evaluation Criteria**:

| Criterion | Threshold | Action |
|-----------|-----------|--------|
| **Conversions** | 0-1/month | PAUSE - Redundant with other campaigns |
| | 2-4/month | MONITOR - Marginal value |
| | 5+/month | CONTINUE - Provides unique value |
| **ROAS** | <300% | PAUSE - Below profitability |
| | 300-500% | MONITOR - Below target (570%) |
| | >500% | CONTINUE - Meeting/exceeding target |
| **Budget Efficiency** | <£100/month | PAUSE - Reallocate to better performers |
| | £100-£300/month | MONITOR - Assess opportunity cost |
| | >£300/month | CONTINUE - Significant budget |

**Alternative Strategies if Underperforming**:

1. **Pause Campaign** - Reallocate budget to property-specific campaigns
2. **Consolidate** - Merge into Performance Max campaign
3. **Restructure** - Focus ONLY on "chatsworth accommodation" generic searches
4. **Location-Based** - Pivot to "hotels near chatsworth" location searches

---

## Expected Impact & ROI

### Financial Impact (Monthly Projections)

| Metric | Current | After Implementation | Improvement |
|--------|---------|---------------------|-------------|
| **Monthly Spend** | £476 | £309 (-35%) | **£167 saved** |
| **Property Cannibalization** | £167/month | £0 | **£167 saved** |
| **Conversions** | 0-2/month | 2-4/month (est.) | **+2 conversions** |
| **Revenue** | £580/month | £870/month (est.) | **+£290** |
| **ROAS** | 161% | 280% (est.) | **+119pp** |

**ROI Calculation**:
- Time to implement: 10 minutes
- Monthly savings: £167
- Annual savings: £2,004
- ROI: ∞ (zero cost, pure savings)

---

## Risk Assessment & Mitigation

### Risk 1: Over-Negation (LOW RISK)

**Scenario**: Legitimate "chatsworth hotels" searches blocked due to broad PHRASE match

**Likelihood**: Low - PHRASE match only blocks when exact phrase appears

**Mitigation**:
- Monitor search terms daily for first week
- Use EXACT match for single words (hide, fell, menu) where appropriate
- Keep PHRASE match for multi-word properties (devonshire arms, cavendish)

**Rollback Plan**: Remove overly broad negatives within 24 hours if detected

---

### Risk 2: Campaign Becomes Redundant (MEDIUM RISK)

**Scenario**: After removing property searches, campaign has no unique value vs Performance Max or property campaigns

**Likelihood**: Medium - Campaign may have been relying on property cannibalization for volume

**Mitigation**:
- 30-day evaluation period to assess unique value
- Compare search terms with Performance Max to identify overlap
- Decision point: Pause vs restructure vs continue

**Action Plan**: If <2 conversions in 30 days, recommend pause and budget reallocation

---

### Risk 3: Property Campaigns Miss Broad Match Searches (LOW RISK)

**Scenario**: Generic searches like "chatsworth accommodation" previously caught by this campaign, now missed

**Likelihood**: Low - Performance Max should capture broad searches

**Mitigation**:
- Monitor overall account conversions for "chatsworth" searches
- Check if Performance Max or other campaigns capturing generic queries
- If gap identified, add broad keywords to Performance Max

---

## Approval & Sign-Off

**Prepared By**: Peter Empson (PetesBrain AI Investigation)
**Date**: 2025-12-22
**Client**: Devonshire Hotels (via A Cunning Plan)

**Recommended Approach**: Option 2 (Automated via MCP) with Google Ads Change Protection Protocol

**Approval Required**: Yes - Client/Agency approval before implementation

**Estimated Implementation Time**: 5 minutes (automated) or 10 minutes (manual)

**Monitoring Commitment**: Daily for 7 days, then weekly for 4 weeks

---

## Implementation Checklist

**Pre-Implementation**:
- [ ] Review negative keyword list with client/agency
- [ ] Confirm no business reason for property overlap
- [ ] Create backup of current campaign state
- [ ] Schedule 7-day performance review

**Implementation**:
- [ ] Add 18 negative keywords to campaign 2080736142
- [ ] Verify all match types correct (EXACT vs PHRASE)
- [ ] Document implementation date/time
- [ ] Save backup JSON with expected state

**Post-Implementation**:
- [ ] Verify negative keywords active (within 2 hours)
- [ ] Monitor search terms for property searches (Dec 23)
- [ ] Check spend reduction (Dec 24)
- [ ] Review conversions (7 days)
- [ ] Strategic evaluation (30 days)

---

## Supporting Documentation

**Related Files**:
- Investigation report: `clients/devonshire-hotels/tasks-completed.md` (Dec 22, 2025)
- Campaign backup: `clients/devonshire-hotels/reports/chatsworth-inns-backup-2025-12-22.json` (to be created)
- Search terms data: Available via Google Ads API (campaign 2080736142, Dec 1-22)

**Reference Campaigns**:
- Pilsley Inn: Campaign ID 19534106385
- Beeley Inn: Campaign ID 22539873565
- The Hide: Campaign ID 23069490466
- Devonshire Arms: Campaign ID 19577006833
- The Fell: Campaign ID 22666031909
- Cavendish: Campaign ID 21839323410

---

## Next Steps

1. **Review with client** - Share this plan with Helen/Gary (Devonshire Hotels) via A Cunning Plan
2. **Get approval** - Confirm client agrees with negative keyword strategy
3. **Implement** - Add negative keywords via preferred method (manual or automated)
4. **Monitor** - Daily search terms review for 7 days
5. **Evaluate** - 30-day strategic review to determine campaign future

**Timeline**:
- Day 0 (Dec 22): Plan created, awaiting approval
- Day 1-2: Client review and approval
- Day 3: Implementation
- Day 3-10: Daily monitoring
- Day 33: Strategic review and decision
