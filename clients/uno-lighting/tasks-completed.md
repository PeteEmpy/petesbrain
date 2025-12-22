# Completed Tasks

This file tracks completed tasks for Uno Lighting.
Tasks are logged when work is completed or closed.

---

## Fix 32 disapproved products - URLs return 404 errors (Task Closed - Duplicate)
**Completed:** 2025-11-19 23:00
**Source:** Manual completion (reported in Claude Code)

**Reason for Closure:** This task is a duplicate - same issue being tracked in `clients/uno-lights/tasks.json` as "[HIGH] Uno Lights - Fix Landing Page Errors (32 products)".

**Context:** 32 product variants (3.3% of feed) disapproved with "Unavailable desktop landing page" error in Merchant Center ID 513812383.

**Root Cause Identified:** Product URLs in feed return 404 errors - products deleted/unpublished from Shopify but Channable feed integration didn't remove them, or URLs changed.

**Affected Products (10 parent products, 32 variants):**
1. 10W "CUT ANYWHERE" COB LED STRIP - 12 variants
2. Connectors for 5W/10W COB - 6 variants
3. 12W RGB COB STRIP - 4 variants
4. Connectors for 12W RGB - 2 variants
5. 10W SMD DIGITAL PIXEL - 2 variants
6. 12W COB DIGITAL PIXEL - 2 variants
7. RF+WIFI CONTROLLER - 1 variant
8. 10W QUIK FLEX SMD - 1 variant
9. Black Bezel - 1 variant
10. Yuri ceiling light - 1 variant

**Action:** Work will continue under the task in `clients/uno-lights/` folder. This duplicate task closed to avoid confusion.

**Note:** Client folders "uno-lighting" and "uno-lights" need to be consolidated.

---
## [Uno Lighting] Review AI Max performance and search term quality
**Completed:** 2025-12-17 10:30
**Source:** Follow-up from AI Max implementation

Investigation completed with statistically rigorous methodology.

**Report:** clients/uno-lighting/reports/2025-12-17-ai-max-search-term-quality-investigation.md

**Methodology:**
- 30-day account performance analysis (17th Nov - 16th Dec)
- 60-day search term analysis (18th Oct - 17th Dec)
- Three-tier classification system with 30+ click threshold
- Zero product assumptions (purely statistical)

**Key Findings:**

1. ✅ AI Max (Brand Campaign) Performing Excellently
   - 225% ROAS (69pp above 156% target)
   - Highly relevant search terms only ("uno lighting" 7128% ROAS, "uno lights" 3704% ROAS)
   - No problematic query expansion after 2 months
   - 100% search impression share

2. ⚠️ Search Term Quality: 4 High-Confidence Negative Candidates
   - **Tier 1 (high confidence):** 4 terms, £403 waste in 60 days (£806/month projected)
     - "led strip lights" (177 clicks, £152, 0 conv)
     - "led plaster in profile" (52 clicks, £116, 0 conv)
     - "plaster in downlights" (43 clicks, £90, 0 conv)
     - "led light strips" (43 clicks, £44, 0 conv)
   - **Tier 2 (monitor closely):** 39 terms, £698 in 60 days (10-29 clicks, 0 conv)
   - **Tier 3 (insufficient data):** 0 terms (all terms have 10+ clicks)

3. ✅ Converting Terms Strong
   - 26 converting terms (38% of total)
   - Average ROAS: 1520%
   - Total: £853 spend, 85.4 conversions

4. 📊 Conversion Lag Caveat (Still Relevant)
   - Recent data (Dec 15-17) affected by 26-66% conversion lag
   - Apparent ROAS drop (124%) is artifact - true ROAS likely 200%+
   - Re-analysis scheduled Friday 20th Dec when data mature

**Methodology Improvement:**
- **Original analysis:** 7-day lookback, insufficient statistical power, some product assumptions incorrect
- **Revised analysis:** 60-day lookback, 30+ click threshold, zero product assumptions
- **Result:** Only 4 terms meet high-confidence criteria (vs. 20+ in original)

**Actions Taken:**
- Comprehensive revised investigation report created (20K words)
- 4 high-confidence exact-match negative keywords identified
- 39 Tier 2 terms in monitoring pool
- Original 7-day report preserved as backup ("-ORIGINAL-7DAY.md")
- Weekly monitoring cadence established

**Immediate Next Steps:**
1. Add 4 exact-match negative keywords to Shopping campaign ([led strip lights], [led plaster in profile], [plaster in downlights], [led light strips])
2. Schedule weekly Tier 2 review (every Monday)
3. Re-analyse Friday 20th Dec with mature conversion data

**Projected Impact:**
- £800/month waste reduction
- Shopping campaign ROAS improvement from 108% towards 156% target


---
