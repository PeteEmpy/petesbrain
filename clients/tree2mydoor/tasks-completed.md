# Completed Tasks

This file tracks completed tasks for Client: Tree2Mydoor.
Tasks are logged automatically by the Google Tasks monitoring system.

---

## Black Friday ROAS Reduction - 120% Experiment
**Completed:** 2025-11-24
**Source:** Weekly Report Analysis

**Trigger:** Impression share analysis revealed severe rank losses:
- P Max HP&P: 36% impression share, **64% lost to rank**
- Search Roses: 10% impression share, **90% lost to rank**
- Search Trees: 10% impression share, **90% lost to rank**
- All campaigns losing to RANK, not budget

**Campaigns Updated:**

| Campaign | ID | Previous ROAS | New ROAS |
|----------|-----|---------------|----------|
| T2MD \| P Max \| HP&P | 15820346778 | 140% | **120%** |
| T2MD \| P Max Shopping \| Unprofitable | 21610656469 | 140% | **120%** |
| T2MD \| Search \| Roses | 17324490442 | 150% | **120%** |
| T2MD \| Shopping \| Catch All | 22986754502 | 150% | **120%** |
| T2MD \| Shopping \| Low Traffic | 22122810626 | 140% | **120%** |

**Time-Limited:** This is a BLACK FRIDAY WEEK experiment only.
- Start: Nov 24, 2025
- Revert: Tuesday Nov 25, 2025 (unless significantly improved)

**Monitoring:**
- Day 1 check: End of day Nov 24
- Full review: Tuesday Nov 25 morning
- Google Tasks created for both checkpoints

**Rollback Plan:**
- Revert immediately if ROAS drops below 100%
- Revert immediately if spend explodes unexpectedly
- Default: Revert to original values on Tuesday unless clear improvement

**Risk Level:** HIGH - Peter flagged nervousness about this change

---

## Brand Campaign Consolidation - Paused "Brand Tree To My Door"
**Completed:** 2025-11-24
**Source:** Task note investigation - Nils Rooijmans best practice review

**Campaign Paused:** T2MD | Brand Tree To My Door (ID: 22485131646)
**Campaign Kept:** T2MD | Brand Inclusion 120 14/7 Ai Max 11/11 (ID: 598474059)

**Why Paused:**
1. **Cannibalisation** - Both campaigns competing for brand term variations
2. **Running too broad** - "Brand Tree To My Door" showing for:
   - Generic terms: "bay tree", "birch tree", "trees for sale", "online plants uk"
   - Competitor names: "sarah raven", "plants4presents"
3. **Overlap on brand terms** - Both picking up "tree2mydoor" variants

**Pre-Pause Performance (Last 30 Days):**

| Campaign | Spend | Conv | Revenue | ROAS |
|----------|-------|------|---------|------|
| Brand Inclusion (KEPT) | £216 | 15.8 | £264 | 123% |
| Brand Tree To My Door (PAUSED) | £127 | 14.3 | £209 | 165% |
| **Combined** | **£343** | **30.1** | **£473** | **138%** |

**EXPERIMENT: Consolidation Test**
- **Hypothesis:** Single brand campaign will capture same brand volume at lower cost
- **Success Criteria:** Brand Inclusion maintains ~30 conversions over next 30 days
- **Failure Criteria:** Brand conversions drop >20% (below 24 conversions)
- **Review Date:** Dec 24, 2025 (30 days)

**Expected Outcome:**
- Brand Inclusion should absorb genuine brand searches
- Generic/competitor traffic will stop (saving wasted spend)
- Net effect: Similar brand conversions, less wasted spend

---

## Tree2mydoor: Review Q4 Christmas campaign performance
**Completed:** 2025-10-29 08:41  
**Source:** Peter's List  

Analyze the performance of Christmas campaigns for Tree2mydoor and prepare recommendations for next year.

---

## Tree2mydoor: Implement LLMS.txt and agents.txt files
**Completed:** 2025-10-29 08:55  
**Source:** Peter's List  

From Tree2mydoor meeting with Gareth on 2025-10-27. Create AI discoverability files (llms.txt and agents.txt) for the tree2mydoor website to improve how AI assistants like ChatGPT and Claude understand and recommend their business. Research website, create structured content, and provide implementation instructions to client.

Files generated and instructions given to tree2mydoor

---

## Tree2mydoor: Start using Google Chat space for regular updates
**Completed:** 2025-10-30 10:34  
**Source:** Peter's List  

From Tree2mydoor meeting with Gareth on 2025-10-27. Begin posting regular campaign updates in the Google Chat space instead of relying solely on email. This will improve communication cadence and make it easier for the client to stay informed on campaign performance and changes.

---

## Complete Product Hero Label Tracking Rollout - All Clients
**Completed:** 2025-11-03 11:22  
**Source:** Peter's List  

Complete the label tracking rollout for all 8 enabled clients. This should take 30-45 minutes.

📋 REFERENCE: /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer/ROLLOUT-COMPLETION-GUIDE.md

✅ CURRENT STATUS:
- Tree2mydoor: 208 products tracked, October baseline created ✓
- AFH: 500 products fetched (have labels)
- Clear Prospects (BMPM): 500 products fetched (awaiting Product Hero labeling)
- Pending: Uno Lights, Grain Guard, Crowd Control, HappySnapGifts, WheatyBags

🔄 STEP-BY-STEP PROMPTS:

Step 1 (15 min): Execute Remaining MCP Queries
Prompt: "Complete the label tracking rollout for all remaining clients. Execute the MCP queries from pending_label_queries.json for: Uno Lights, Grain Guard (with manager_id), Crowd Control. Process all responses and create current-labels.json files for all 8 enabled clients."

Step 2 (5 min): Generate October Baselines
Prompt: "Generate October 2025 baselines for all clients with label tracking enabled."

Step 3 (10 min): Test Weekly Report Generation
Prompt: "Test the weekly report generation with label validation for one client (Tree2mydoor)."

Step 4 (5 min): Verify Complete Rollout
Prompt: "Verify the complete label tracking rollout. Check that all 8 enabled clients have: 1. current-labels.json 2. 2025-10.json (October baseline) 3. Proper directory structure. Generate a summary report."

✅ SUCCESS CRITERIA:
- All 8 clients have current-labels.json
- All 8 clients have 2025-10.json (October baseline)
- Test weekly report generates with label validation section
- First daily tracking run completes without errors

⚠️ IMPORTANT NOTES:
- Grain Guard requires manager_id: 2569949686
- AFH and Uno Lights use LIMIT 500 (partial coverage)
- Clear Prospects serves 3 brands (HappySnapGifts, WheatyBags, BMPM)
- BMPM products may not have labels assigned yet (normal - will track once assigned)

---

## Tree2MyDoor: Investigate POAS decline from 215% to 121% YoY
**Completed:** 2025-11-06 10:07  
**Source:** Peter's List  

Complete the POAS decline analysis for Tree2MyDoor October 2025 report.

Key actions:
1. Review ProfitMetrics product-level margin data
2. Analyze sales mix Oct 2024 vs Oct 2025
3. Check promotional calendar for discounting
4. Verify Channable feed rules for margin segmentation
5. Determine root cause of POAS drop (215% to 121%)

Context: Similar spend YoY but profit dropped 46%

---

## Tree2mydoor: Request Shopify access permissions
**Completed:** 2025-11-09 10:10  
**Source:** Peter's List  

From Tree2mydoor meeting with Gareth on 2025-10-27. Send email requesting specific Shopify access permissions needed for campaign optimization and conversion tracking setup. Need to specify exactly which permissions are required (product catalog, orders, customer data for GA4 integration, etc.).

---

## Tree2mydoor: Verify ProfitMetrics conversion tracking optimizing to profit value
**Completed:** 2025-11-14 09:10
**Source:** Manual completion (reported in Claude Code)

**Verification:** Confirmed ProfitMetrics conversion tracking is working correctly and has always been optimizing to profit value (not just revenue).

**Findings:**
- Google Ads conversion actions properly configured with ProfitMetrics profit values
- No issues found with tracking implementation
- System has been functioning correctly since initial setup
- This was a false concern - tracking verified as working as intended

**Conclusion:** No action required. ProfitMetrics integration working correctly with profit-based optimization active.

---

## Tree2mydoor: Request Shopify access permissions
**Completed:** 2025-11-09 10:10  
**Source:** Peter's List  

From Tree2mydoor meeting with Gareth on 2025-10-27. Send email requesting specific Shopify access permissions needed for campaign optimization and conversion tracking setup. Need to specify exactly which permissions are required (product catalog, orders, customer data for GA4 integration, etc.).

---

## [Tree2Mydoor] Review Olive Tree (Product 01090) Merchant Center feed stability
**Completed:** 2025-11-14 09:23  
**Source:** Client Work  

---
**Source:** AI Generated (2025-11-12 09:25)
**Client:** tree2mydoor
**Priority:** P1
**Time Estimate:** 30 mins
**Reason:** Recent feed flickering caused massive click spike (Oct 26-28) that disrupted campaign performance. Immediate verification needed to prevent potential recurrence and algorithmic disruption.
**AI Task ID:** fd34e2db-853e-4767-9dcd-605dfc29c7fb
---

Recent feed flickering caused massive click spike (Oct 26-28) that disrupted campaign performance. Immediate verification needed to prevent potential recurrence and algorithmic disruption.

---

## [Tree2Mydoor] Verify ProfitMetrics conversion tracking is optimizing to profit value
**Completed:** 2025-11-14 09:13  
**Source:** Client Work  

---
**Source:** AI Generated (2025-11-11 10:38)
**Client:** tree2mydoor
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Known technical issue identified in documentation that could impact campaign optimization and ROAS performance. Need to confirm tracking is using profit value, not just revenue.
**AI Task ID:** 30d01e3e-bc29-4851-8402-173f479f7b05
---

Known technical issue identified in documentation that could impact campaign optimization and ROAS performance. Need to confirm tracking is using profit value, not just revenue.

---

## [Tree2Mydoor] Verify ProfitMetrics conversion tracking is optimizing to profit value, not just revenue
**Completed:** 2025-11-14 09:13  
**Source:** Client Work  

---
**Source:** AI Generated (2025-11-12 07:01)
**Client:** tree2mydoor
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Critical technical issue identified that could impact campaign optimization and ROAS performance. Needs immediate confirmation to ensure accurate tracking.
**AI Task ID:** d8b537de-683c-4a70-a8a3-6c7385321b7a
---

Critical technical issue identified that could impact campaign optimization and ROAS performance. Needs immediate confirmation to ensure accurate tracking.

---

## [Tree2Mydoor] Verify ProfitMetrics conversion tracking is optimizing to profit value
**Completed:** 2025-11-14 09:13  
**Source:** Client Work  

---
**Source:** AI Generated (2025-11-12 09:25)
**Client:** tree2mydoor
**Priority:** P2
**Time Estimate:** 30 mins
**Reason:** Critical technical issue identified that could impact campaign optimization and ROAS performance. Need to confirm tracking is using profit value, not just revenue.
**AI Task ID:** 1d8ed410-8092-44e2-ac31-08a3aa3f8c52
---

Critical technical issue identified that could impact campaign optimization and ROAS performance. Need to confirm tracking is using profit value, not just revenue.

---

## [Tree2MyDoor] Investigate Search Campaign Performance Collapse - Weekly Report Rerun
**Completed:** 2025-11-23 19:00
**Source:** Manual completion (reported in Claude Code)

**Original Task:** Rerun the weekly report taking conversion lag into consideration.

**Investigation Findings:**
The original Nov 20 weekly report flagged concerning performance collapse:
- ROAS showing 90% (was 122% prior week)
- Several search campaigns showing 0% ROAS
- Conversions dropped from 40.1 to 26.3 (-34%)

**Root Cause:** Conversion attribution lag. The Nov 20 report only had 2 days of lag, causing significant understatement.

**Lag-Cleared Results (Nov 23):**
| Metric | Original Report (Nov 20) | Lag-Cleared (Nov 23) |
|--------|-------------------------|---------------------|
| Conversions | 26.3 | 87.4 (+232%) |
| Conv Value | £517 | £1,465 (+183%) |
| ROAS | 90% | 130% (+40pp) |
| CPA | £21.79 | £12.91 (-41%) |

**Actual Week-over-Week Performance:**
- ROAS: 130% vs 133% last week (-3pp) - stable, not collapsed
- Conversions: 87.4 vs 98.8 (-11.5%) - minor decline, not collapse
- Spend: £1,128 vs £1,263 (-10.7%) - intentional reduction

**Campaign Status Update:**
- The "Anniversary - Exact", "Olive Tree Gifts", and "Roses - Broad" campaigns flagged in original report were legacy/paused campaigns, not active ones
- Active search campaigns: Roses (218% ROAS, up +35pp), Trees (40% ROAS, down -87pp), Memorial (53%)

**Outcome:**
- New lag-cleared weekly report generated: `clients/tree2mydoor/reports/weekly/2025-11-23-weekly-report.md`
- No P0 critical issues identified
- Two P2 recommendations: Scale Roses search campaign, investigate Trees search campaign

**Key Learning:** Allow minimum 3 days conversion lag before weekly report generation.

**Status:** Task cleared from active list (Nov 24, 2025) - investigation completed and documented.

---
## [LOW] Tree2mydoor - Consider Renaming "Shirazz" Tree (optional)
**Completed:** 2025-11-26 13:52
**Source:** Migrated from Google Tasks (Nov 18, 2025)
**Priority:** P1

**Resolution:**
Task completed - no action taken (as recommended). The "Shirazz" tree product flagged as alcohol is a false positive affecting only 1 product out of thousands. Impact is negligible and acceptable.

**Decision:**
Leave product name as-is. This is an acceptable loss - the product name "Shirazz" is botanically accurate and renaming would be unnecessary overhead for minimal benefit.

**Reference:** /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md

**Original Task Notes:**
**Priority**: LOW (Optional)
**Products Affected**: 1 tree variety

**Issue**: Tree named "Shirazz" flagged as alcohol (false positive)

**Action Options**:
1. Rename to "Ornamental Tree - Shirazz Variety" to avoid trigger
2. OR leave as-is (acceptable loss - 1 product out of thousands)

**Recommendation**: Monitor only, no immediate action required

**Expected Impact**: NEGLIGIBLE

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md

---

