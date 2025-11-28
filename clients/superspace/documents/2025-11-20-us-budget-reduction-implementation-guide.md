# Superspace US Budget Reduction - Implementation Guide

**Date:** 2025-11-20 08:55  
**Urgency:** HIGH - Stock depletion  
**Requested by:** Craig Spencer (Co-founder)  
**Reduction:** 20% across all US campaigns  

---

## Executive Summary

**Current Total US Daily Budget:** £14,460/day  
**New Total After 20% Reduction:** £11,568/day  
**Daily Savings:** £2,892/day  

⚠️ **IMPORTANT:** Current budget (£14,460) is higher than Nov 13 figure (£12,010) - budgets were increased since last email. This means 20% reduction saves MORE than originally discussed with Craig.

---

## Campaign-by-Campaign Changes

### 1. SUP | US | Shopping Branded 500 15/7 550 6/10 600 17/11
- **Current:** £4,500/day
- **New:** £3,600/day
- **Cut:** £900/day (-20%)
- **Budget ID:** 14412940053

### 2. SUP | US | P Max 700 Brand Excluded 24/2 500 15/7 550 6/10 600 17/11
- **Current:** £3,800/day
- **New:** £3,040/day
- **Cut:** £760/day (-20%)
- **Budget ID:** 11914791987

### 3. SUP | US | Shopping Brand Excluded 700 9/1 500 15/7 550 6/10 600 17/11
- **Current:** £3,200/day
- **New:** £2,560/day
- **Cut:** £640/day (-20%)
- **Budget ID:** 14021953807

### 4. SUP | US | Search | Brand Inclusion 21/5 550 15/7 incl removed 6/10 600 17/11
- **Current:** £1,700/day
- **New:** £1,360/day
- **Cut:** £340/day (-20%)
- **Budget ID:** 12349718339

### 5. SUP | US | Search | Generics 650 4/5 AI Max 3/7 Off 15/7 500 On 6/8 550 6/10 600 17/11
- **Current:** £790/day
- **New:** £632/day
- **Cut:** £158/day (-20%)
- **Budget ID:** 12362766610

### 6. SUP | US | Demand Gen 60 17/11
- **Current:** £300/day
- **New:** £240/day
- **Cut:** £60/day (-20%)
- **Budget ID:** 14944784554

### 7. SUP | US | Demand Gen Retargeting 60 17/11
- **Current:** £150/day
- **New:** £120/day
- **Cut:** £30/day (-20%)
- **Budget ID:** 14986597866

### 8. SUP | US | Search | Play House 40 Broad Test Recommendations trial
- **Current:** £20/day
- **New:** £16/day
- **Cut:** £4/day (-20%)
- **Budget ID:** 11922350365

---

## Implementation Steps (Google Ads UI)

**Account:** 7482100090 (Superspace)

For each campaign above:

1. Navigate to Google Ads > Campaigns
2. Find campaign by name
3. Click "Edit" next to the budget
4. Enter new daily budget amount
5. Click "Save"
6. Record timestamp of change

**Estimated Time:** 10-15 minutes for all 8 campaigns

---

## Verification Query

After making changes, run this GAQL query to verify:

```sql
SELECT 
  campaign.name,
  campaign_budget.amount_micros
FROM campaign 
WHERE campaign.status = 'ENABLED' 
  AND campaign.name LIKE 'SUP | US%'
ORDER BY campaign_budget.amount_micros DESC
```

**Expected Results:**
- Shopping Branded: 3,600,000,000 micros (£3,600)
- P Max Brand Excluded: 3,040,000,000 micros (£3,040)
- Shopping Brand Excluded: 2,560,000,000 micros (£2,560)
- Search Brand Inclusion: 1,360,000,000 micros (£1,360)
- Search Generics: 632,000,000 micros (£632)
- Demand Gen: 240,000,000 micros (£240)
- Demand Gen Retargeting: 120,000,000 micros (£120)
- Search Play House: 16,000,000 micros (£16)

**Total should be:** 11,568,000,000 micros (£11,568/day)

---

## Context & Rationale

**Reason for Change:**
- US Christmas stock selling faster than anticipated
- Tracking to be out of stock by next week (week of Nov 25)
- Need to extend stock runway without killing all momentum
- 20% reduction is Phase 1 of potential 40-50% total reduction over next 3-4 days

**Why Budget Reduction vs ROAS Increase:**
- Budget cuts take effect within 2-3 hours
- ROAS increases (600% applied Nov 17-18) take 3-5 days to fully take effect
- Stock timeline requires immediate impact
- At 892% actual ROAS, budget reduction maintains profitability

**Client Communication:**
- Craig Spencer requested this via email Nov 20, 13:41
- Ant Erwin (Co-founder) CC'd on thread
- Asked how quickly we can reduce safely
- Mentioned potential 40-50% total reduction within 3-4 days

**Next Steps:**
- Monitor stock depletion rate
- Prepare for Phase 2 (additional 20%) on Friday Nov 21 if needed
- Potential Phase 3 (final 10%) on Monday Nov 24 if stock critical

---

## Documentation Checklist

After implementation:

- [ ] Verify all 8 budgets changed via GAQL
- [ ] Log to `clients/superspace/tasks-completed.md`
- [ ] Update `clients/superspace/CONTEXT.md` with Nov 20 budget strategy
- [ ] Log technical details to `clients/superspace/api-changes-log.json`
- [ ] Send confirmation email to Craig with new totals
- [ ] Add entry to `roksys/spreadsheets/rok-experiments-client-notes.csv`

---

**Implementation Started:** [TIMESTAMP]  
**Implementation Completed:** [TIMESTAMP]  
**Verified By:** [GAQL QUERY RESULTS]
