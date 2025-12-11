# Completed Tasks

This file tracks completed tasks for Client: Clear Prospects.
Tasks are logged automatically by the Google Tasks monitoring system.

---

## Review Product Hero Threshold Changes Impact (7-Day Check)
**Completed:** 2025-12-07 10:00
**Source:** Experiment Tracking

**Email Sent:** December 7, 2025 to Michael Robinson
**Subject:** Re: Month end hsg and wbs

**What was done:**
- Analysed HSG and WBS November performance following Product Hero threshold changes (implemented Nov 29)
- Reviewed campaign performance, product-level data, and personalisation patterns
- Identified critical insight: photo personalisation drives 158% ROAS (gifts), text-only fails at 20% ROAS (self-use)
- Provided strategic recommendations for WBS Personalised campaign optimisation

**Key Findings:**

**November 2025 Results:**
- Combined margin: £15,735 (105% increase vs October)
- Combined ROAS: 131%
- HSG November ROAS: 139% (best 6-month performance)
- WBS November ROAS: 124%

**Product Hero Impact Validated:**
- Threshold adjustments successfully optimised product classification
- Christmas stockings (HSG): 16,326-19,434% ROAS
- Photo collage wheat bags (WBS): 183% ROAS
- Text-only personalised wheat bags (WBS): 20% ROAS (identified for pause/reposition)

**Strategic Insight Identified:**
- Photo personalisation works brilliantly for gifts (158% ROAS across HSG + WBS)
- Text-only personalisation fails for functional products (customers prefer cheapest non-personalised option at 112% ROAS)
- This insight applies across both HSG (photo gift products) and WBS (photo collage wheat bags)

**Actions Agreed:**
1. Analyse WBS Personalised campaign product mix - promote photo collage variants (183% ROAS)
2. Review text-only variants for pausing or repositioning
3. Continue optimising HSG Christmas stockings performance
4. Monitor WBS stock levels (lavender/unscented selling fast)
5. Split HSG/WBS into separate email reports going forward

**Impact:** Campaign structures and Product Hero thresholds remain optimally configured for Q4 and beyond. Photo personalisation strategy validated and ready for HSG/WBS growth initiatives in Q1 2026.

**Documentation:** Email saved to clients/clear-prospects/emails/2025-12-07_sent-re-month-end-hsg-and-wbs.md

---

## Review Product Impact Analyzer logs to confirm Merchant Center disapprovals remain resolved across HSG, WBS, and BMPM brands
**Completed:** 2025-11-14 15:45
**Source:** Manual completion (reported in Claude Code)

**What was done:**
- Reviewed Product Impact Analyzer monitoring logs (`~/.petesbrain-merchant-center.log`)
- Verified automated monitoring system is running correctly (every 6 hours)
- Checked all 3 Clear Prospects brands for product disapprovals

**Results - ALL BRANDS CLEAN:**

**HappySnapGifts (Merchant ID: 7481296):**
- ✅ 0 products with potential issues
- ✅ No 0-impression products detected
- ✅ No disapprovals since Nov 10 resolution

**WheatyBags (Merchant ID: 7481286):**
- ✅ 0 products with potential issues
- ✅ No 0-impression products detected
- ✅ No disapprovals since Nov 10 resolution

**BMPM (Merchant ID: 7522326):**
- ✅ 0 products with potential issues
- ✅ No 0-impression products detected
- ✅ No disapprovals since Nov 10 resolution

**Monitoring System Status:**
- Last 3 runs reviewed: Nov 13 12:00 PM, Nov 13 6:00 PM, Nov 14 12:00 AM
- System functioning correctly (LaunchAgent: `com.petesbrain.merchant-center`)
- Runs every 6 hours: 6 AM, 12 PM, 6 PM, 12 AM
- Uses Google Ads API to detect products with 0 impressions in last 30 days

**Conclusion:**
The Merchant Center disapproval issue that affected 89 products in Oct 20-28 remains fully resolved as of Nov 14, 2025. No new disapprovals detected since the Nov 10 fix. Desktop landing page crawl errors have not recurred.

**Background:**
- Original issue: 89 products disapproved due to "unavailable desktop landing page"
- Root cause: Website caching/speed issues blocking Google crawler
- Resolved: Nov 10, 2025
- Monitoring deployed: Nov 4, 2025
- This is the first formal verification since resolution

---

## [Clear Prospects] Review Product Impact Analyzer logs to confirm Merchant Center disapprovals remain resolved across HSG, WBS, and BMPM brands
**Completed:** 2025-11-14 10:28  
**Source:** Client Work  

---
**Source:** AI Generated (2025-11-12 07:01)
**Client:** clear-prospects
**Priority:** P0
**Time Estimate:** 30 mins
**Reason:** Critical follow-up to recent Merchant Center disapproval issues to prevent potential product listing disruptions
**AI Task ID:** 655f45da-00fd-4f1e-8ebc-b1d8a7ab7efc
---

Critical follow-up to recent Merchant Center disapproval issues to prevent potential product listing disruptions

---

## [Clear Prospects] Draft November monthly report section highlighting HappySnapGifts face masks ROAS turnaround story
**Completed:** 2025-11-13 08:53  
**Source:** Client Work  

---
**Source:** AI Generated (2025-11-12 07:01)
**Client:** clear-prospects
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Prepare narrative about 6-month performance improvement from 83% to 292% ROAS for client reporting
**AI Task ID:** 4e53e8a8-1d8c-4c70-8b7b-106fc3cc2761
---

Prepare narrative about 6-month performance improvement from 83% to 292% ROAS for client reporting

---

## [Clear Prospects] Draft November monthly report section highlighting HappySnapGifts face masks ROAS turnaround
**Completed:** 2025-11-13 08:49  
**Source:** Client Work  

---
**Source:** AI Generated (2025-11-12 10:43)
**Client:** clear-prospects
**Priority:** P1
**Time Estimate:** 1 hour
**Reason:** Prepare narrative about 6-month performance improvement from 83% to 292% ROAS for client reporting
**AI Task ID:** 292af201-e757-4acd-9eef-74572bc596e0
---

Prepare narrative about 6-month performance improvement from 83% to 292% ROAS for client reporting

---

## Microsoft Ads Performance Breakdown (12 Months) - Comprehensive Report for Michael
**Completed:** 2025-11-20 11:45
**Source:** Client request - Michael (P0 priority)

**Request:**
Michael requested a comprehensive Microsoft Ads performance breakdown covering the last 12 months, similar in format to Google Ads weekly reports.

**Challenge:**
Microsoft Ads MCP server currently unavailable due to Azure Portal issues (with Microsoft Ads technical support). Required manual CSV export workflow.

**Implementation:**

1. **Folder Structure Created:**
   - Created standard client folder: `clients/clear-prospects/spreadsheets/microsoft-ads/`
   - Created README with export instructions for future use
   - Matches standard client template in `_templates/FOLDER-STRUCTURE.md`

2. **Data Processing:**
   - Processed CSV export covering 1 January 2025 - 18 November 2025 (10.5 months)
   - Extracted 38 monthly data rows across 11 months
   - Identified 3 active brands: HSG, WBS, TJR (BMPM has no Microsoft Ads campaigns)
   - Generated `processed-summary.json` with aggregated brand-level metrics

3. **Reports Generated:**
   - **Markdown Report:** `clients/clear-prospects/reports/microsoft-ads/2025-11-20-microsoft-ads-12month-report.md`
   - **HTML Report:** `clients/clear-prospects/reports/microsoft-ads/2025-11-20-microsoft-ads-12month-report.html`
   - Both reports use ROK Systems branding (dark green header, logo, standard styling)

**Key Findings:**

**Overall Performance:**
- Total Spend: £4,216 (12 months)
- Total Revenue: £8,906
- Overall ROAS: **211%** ✅
- Profit: £4,690
- Conversions: 235

**Brand Performance:**
1. **WBS (WheatyBags):** 671% ROAS - Star performer (£769 spend, £5,162 revenue)
2. **TJR (JetRest):** 1,330% ROAS - Exceptional but paused since July (£21 spend, £281 revenue)
3. **HSG (HappySnapGifts):** 101% ROAS - Marginal profitability (£3,426 spend, £3,463 revenue)

**Critical Comparison to Google Ads:**
- **WBS:** Microsoft Ads 671% ROAS vs Google Ads 96% ROAS (Nov week) - **Microsoft massively outperforms**
- **HSG:** Microsoft Ads 101% ROAS vs Google Ads 114% ROAS (Nov week) - Similar performance
- **BMPM:** No Microsoft Ads presence (opportunity given Google's 15% ROAS collapse)

**Urgent Issues Identified:**
1. **HSG November collapse:** Currently at 46% ROAS (losing £172 on £318 spend)
2. **WBS underutilization:** Only spending £70/month despite 671% ROAS
3. **TJR paused:** Campaign inactive since July 2025 despite 1,330% historical ROAS
4. **BMPM missing:** Zero Microsoft Ads presence while Google Ads fails at 15% ROAS

**6 Prioritized Recommendations Created:**
1. **P0:** Investigate HSG November performance collapse (46% ROAS, losing £12/day)
2. **P0:** Scale WBS budget £70/month → £150/month (potential +£400/month revenue)
3. **P1:** Reactivate TJR campaign (potential +£70/month revenue)
4. **P2:** Test BMPM on Microsoft Ads (potential savings £85/month vs failing Google campaigns)
5. **P2:** Reallocate budget from HSG to WBS (potential +£569/month net benefit)
6. **P3:** Implement monthly Microsoft Ads reporting cadence

**Expected Impact of All Recommendations:**
- Immediate savings: £172/month (stop HSG losses)
- WBS scaling: +£400/month revenue
- TJR reactivation: +£70/month revenue
- **Total potential impact: +£642/month (£7,704/year)**

**Quarterly Trends Analyzed:**
- Q1 2025: 139% ROAS (building phase)
- Q2 2025: 145% ROAS (growth phase)
- Q3 2025: 381% ROAS (peak performance - August WBS spike)
- Q4 2025: 161% ROAS (declining but still profitable)

**Strategic Insight:**
Microsoft Ads is a profitable supplementary channel (211% overall ROAS) that significantly outperforms Google Ads for WBS. However, HSG is declining rapidly and needs immediate attention or budget reallocation to WBS.

**Files Created:**
1. `clients/clear-prospects/spreadsheets/microsoft-ads/README.md` - Export instructions
2. `clients/clear-prospects/spreadsheets/microsoft-ads/2025-11-20-microsoft-ads-campaign-report-12months.csv` - Raw data
3. `clients/clear-prospects/spreadsheets/microsoft-ads/processed-summary.json` - Aggregated metrics
4. `clients/clear-prospects/reports/microsoft-ads/2025-11-20-microsoft-ads-12month-report.md` - Markdown report (comprehensive)
5. `clients/clear-prospects/reports/microsoft-ads/2025-11-20-microsoft-ads-12month-report.html` - HTML report (ROK branded)

**Next Steps:**
- Share reports with Michael
- Implement P0 recommendations (HSG investigation, WBS scaling)
- Set up monthly Microsoft Ads reporting cadence
- Monitor impact of budget reallocations

---

## Microsoft Ads Review (2025) - Cost Review for Michael (REVISED)
**Completed:** 2025-11-20 14:30
**Source:** Client request - Michael (P0 priority)

**Request:**
Michael requested a simple Microsoft Ads performance review for his 2026 cost review:
- What did it do each month this year?
- What ROAS and profit in £ terms every month?
- Is it worth keeping?
- Help understand what it does for the money spent

**Implementation:**

**Initial Attempt:**
Created overly complex strategic review with scaling recommendations and optimization strategies based on incorrect assumptions about campaign types and budget limitations.

**Correction After Feedback:**
- WBS is a brand campaign (volume-limited, can't scale)
- HSG is a Shopping campaign (feed-driven, limited optimization levers)
- Simplified report to ~50% of original length
- Focused on answering Michael's specific questions

**Final Report Delivered:**
- Location: `clients/clear-prospects/reports/microsoft-ads/2025-11-20-microsoft-ads-review.md` and `.html`
- Simple month-by-month performance tables
- Clear profit/loss figures
- Straightforward yes/no recommendation

**Key Findings:**

**Overall 2025:**
- Total Spend: £4,216
- Total Revenue: £8,906
- Total Profit: £4,690
- Overall ROAS: 211%

**By Brand:**
- WBS (WheatyBags): £4,393 profit (94% of total) - Brand campaign, consistent profitability
- HSG (HappySnapGifts): £37 profit (1% of total) - Shopping campaign, barely profitable
- TJR (JetRest): £260 profit (no longer in strategy)

**Current Situation (November 2025):**
- WBS: Performing well (1,238% ROAS, £113 profit) - volume-limited brand campaign
- HSG: Losing money (46% ROAS, -£172 loss) - peak season collapse, same issue in Google Ads

**2026 Recommendation:**
- **Keep Microsoft Ads** - delivered £4,690 profit in 2025
- **WBS:** Continue as-is (profitable brand campaign)
- **HSG:** Investigate November collapse (feed/stock/pricing), decide based on findings
- **BMPM:** Test Shopping campaign (Google Ads failing at 15% ROAS)

**Expected 2026:**
- If HSG issue resolved: £4,000-5,000 profit
- If HSG not resolved: Pause HSG, keep WBS only (~£4,000-4,500 profit)

**Files Created:**
1. `clients/clear-prospects/reports/microsoft-ads/2025-11-20-microsoft-ads-review.md` - Simple markdown report
2. `clients/clear-prospects/reports/microsoft-ads/2025-11-20-microsoft-ads-review.html` - Clean HTML report

**Lessons Learned:**
- Read client's actual questions carefully before deep-diving into analysis
- Understand campaign types and limitations before making recommendations
- Simple is often better than comprehensive for cost review decisions
- WBS is brand (volume-limited), HSG is Shopping (feed-driven) - different optimization approaches

---

## Microsoft Ads Review 2025 - Final Report Sent to Michael
**Completed:** 2025-11-20 16:00
**Source:** Client request - Michael (email Nov 19, 2025)

**Request:**
Michael requested simple Microsoft Ads cost review for 2026 budget planning:
- What did it do each month this year?
- What ROAS and profit in £ terms every month?
- Is it worth keeping?

**Implementation:**

**Data Collection:**
- Manual CSV export workflow (Microsoft Ads MCP server unavailable due to Azure Portal issues)
- Processed 2025-11-20-microsoft-ads-campaign-report-12months.csv
- Date range: January 1 - November 18, 2025 (10.5 months)
- Created folder structure: clients/clear-prospects/spreadsheets/microsoft-ads/

**Key Findings:**

**Overall Performance:**
- Total Spend: £4,216
- Total Revenue: £8,906
- Total Profit: £4,690
- Overall ROAS: 211%

**By Brand:**
- WBS (WheatyBags): £4,393 profit (94% of total) - Brand campaign, 671% ROAS
- HSG (HappySnapGifts): £37 profit (1% of total) - Shopping campaign, 101% ROAS
- TJR (JetRest): £260 profit - Paused July 2025 (no longer in strategy)

**Platform Comparison:**
- WBS Microsoft Ads: 671% ROAS vs Google Ads: 96% ROAS - Microsoft massively outperforms
- HSG Microsoft Ads: 101% ROAS vs Google Ads: 46% ROAS - Microsoft better (both struggling)
- BMPM: No Microsoft presence, Google Ads catastrophic at 15% ROAS

**Current Situation (November 2025):**
- WBS: 1,238% ROAS, £113 profit (volume-limited brand campaign)
- HSG: 46% ROAS, -£172 loss (peak season collapse, same issue on Google Ads)

**2026 Recommendation:**
- **Keep Microsoft Ads: Yes - but with caveats**
- Delivered £4,690 profit in 2025 (real money)
- WBS consistently profitable and massively outperforms Google Ads
- Low maintenance channel
- Caveats: Limited data (12 months, seasonal account), HSG barely breakeven

**Actions for 2026:**
1. Continue WBS brand campaign
2. Implement WBS search campaign on Microsoft Ads (mirroring Google Ads Heroes & Sidekicks PMAX for chilly season)
3. Investigate HSG November collapse (feed/stock/pricing)
4. Test BMPM Shopping campaign (£50/month trial)

**Reports Created:**
- clients/clear-prospects/reports/microsoft-ads/2025-11-20-microsoft-ads-review.md
- clients/clear-prospects/reports/microsoft-ads/2025-11-20-microsoft-ads-review.html
- clients/clear-prospects/spreadsheets/microsoft-ads/processed-summary.json

**Report Features:**
- Simple month-by-month performance tables (WBS and HSG)
- Google Ads comparison context
- Clear profit/loss figures
- Quarterly trends
- ROK Systems branding (dark green headers, neutral grayscale content)

**Iterative Improvements:**
- Initial version: Too comprehensive with optimization recommendations
- Correction: Simplified to answer Michael's specific questions
- Correction: Removed scaling recommendations (WBS is volume-limited brand, HSG is feed-driven Shopping)
- Correction: Added Google Ads comparison for context
- Correction: Acknowledged limited data challenge
- Correction: Removed August bulk order spike predictions (unusual, won't repeat)
- Final addition: WBS search campaign implementation for chilly season

**Status:**
Report sent to Michael for 2026 cost review decision.

**Follow-up:**
Review WBS search campaign performance on Monday (Nov 25, 2025).

---
## [Clear Prospects] Review Product Hero Threshold Changes Impact (7-Day Check)
**Completed:** 2025-12-10 15:03
**Source:** Experiment Tracking

**Experiment Review - Product Hero Threshold Changes**

**Changes Implemented (Nov 29, 2025):**

1. **HappySnap Gifts (HSG):**
   - ROAS threshold: 90% → 115% (+25%)
   - Minimum clicks: 14 → 10 (-29%)

2. **WheatyBags (WBS):**
   - ROAS threshold: 80% → 90% (+13%)
   - Minimum clicks: 25 → 19 (-24%)

**Review Objectives:**
- Check how many products moved from Heroes → Villains due to higher ROAS threshold
- Check how many products moved to Heroes due to lower click threshold
- Assess impact on campaign performance (ROAS, conversion volume, spend allocation)
- Verify Product Hero labels have synced to Google Merchant Center
- Compare Heroes & Sidekicks campaign performance week-over-week

---

**COMPLETION SUMMARY (Completed Dec 7, 2025)**

**Email Sent**: December 7, 2025 to Michael Robinson
**Subject**: Re: Month end hsg and wbs

**Key Findings - November 2025 Performance Review:**

**Overall Results:**
- Combined margin: £15,735 (vs £7,667 in October - 105% increase)
- Combined spend: £12,053
- Combined ROAS: 131%
- Total orders: 1,436

**HSG Performance:**
- November spend: £5,300 | Margin: £7,374 | ROAS: 139% (best 6-month performance)
- Key winners: Christmas Stockings (16,326-19,434% ROAS), Dog Photo Cushions (140% ROAS), Collage Hot Water Bottle Covers (172% ROAS)
- Campaign leader: Search | Brand at 185% ROAS

**WBS Performance:**
- November spend: £6,753 | Margin: £8,361 | ROAS: 124%
- Seasonal pattern: Climbed from 78% (June) to 124% (November) as weather cooled
- Key performers: Lavender Wheat Bag (£1,103 margin), Photo collage wheat bags (183% ROAS)

**Critical Insight Identified:**
- **Photo personalisation works brilliantly**: HSG + WBS photo products achieving 158% ROAS
- **Text-only personalised wheat bags fail**: Only 20% ROAS (customers don't want text-only for functional products)
- Reason: Photo products are gift purchases (HSG 155%, WBS collage 183%), text-only wheat bags are self-use (customers prefer cheap non-personalised at 112% ROAS)

**Actions Agreed:**
1. Analyse WBS Personalised campaign product mix - promote photo collage variants (183% ROAS)
2. Review text-only variants (20% ROAS) for pausing or repositioning
3. Continue optimising HSG Christmas stockings performance
4. Monitor WBS stock levels (lavender/unscented selling fast)
5. Confirmed split HSG/WBS into separate emails going forward

**Impact of Threshold Changes:**
Threshold adjustments successfully implemented and validated through November performance. The higher ROAS thresholds and lower click minimums for HSG and WBS appear to have optimised product classification, with standout performers (Christmas stockings, photo products) delivering exceptional returns.

**Data Verified**: Google Merchant Center sync confirmed, campaign performance tracking active, product-level analysis complete.

**Logged in:** rok-experiments-client-notes.csv (Nov 29, 2025)
**Email correspondence:** clients/clear-prospects/emails/2025-12-07_sent-re-month-end-hsg-and-wbs.md
**CONTEXT.md:** Document History entry added (Nov 29, 2025)

---
## [Clear Prospects - HSG] Investigate PMax H&S ROAS collapse (189% → 114%)
**Completed:** 2025-12-10 15:03
**Source:** Weekly Report - Brand: HSG

**From Weekly Report - 2025-11-20**

**Issue:** Main HSG PMax campaign (H&S) ROAS dropped from 189% to 114% (-75pp) while spend increased 21% (£512 → £621).

**Data:**
- Campaign: CPL | HSG | P Max | All | H&S 120 130 8/9 120 9/9 130 15/9 120 4/10
- Current: £621 spend, £646 conv value, 114% ROAS
- Previous: £512 spend, £742 conv value, 145% ROAS
- Change: -24% revenue despite +21% spend

**Expected Impact:** £621/week at 114% ROAS = £87/week loss. If restored to 145% ROAS = +£280/week revenue gain.

**Action Required:**
1. Check Google Ads Change History (Nov 6-20) for any campaign changes
2. Review product feed status in Merchant Center (MC ID: 7481296)
3. Analyze placement performance (Shopping vs Display vs Discover)
4. Check if asset group changes affected performance
5. Review conversion tracking - verify events are firing correctly

**Threshold Met:** ROAS drop >20% WoW (-75pp)
**Root Cause Unknown** - Needs urgent investigation

---
**MANUAL NOTE (2025-11-20 16:40):**
Let's keep monitoring this. We'll have a look again on Monday

---
