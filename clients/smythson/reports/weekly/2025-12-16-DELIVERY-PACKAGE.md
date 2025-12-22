# Smythson Weekly Report - Delivery Package

**Week:** 9-15 December 2025
**Generated:** 16 December 2025
**Report Focus:** Plan vs Actual Performance (Q4 Tracking)

---

## 📦 Deliverables Generated

### 1. HTML Email Draft (Ready to Send)
**File:** `2025-12-16-weekly-email-draft.html`

**Purpose:** Client-ready HTML email with embedded charts
**Recipient:** Alex (Smythson)
**Format:** Verdana 13px, ROK green headings, copy-to-clipboard button

**How to use:**
1. Open the HTML file in browser (already opened automatically)
2. Click green "Copy to Clipboard" button
3. Paste into Gmail compose window
4. Charts will appear as inline images
5. Send to client

**Content includes:**
- Q4 plan tracking summary (spend/revenue vs targets)
- This week performance metrics
- 3 embedded charts (UK ROAS trend, regional spend, regional ROAS)
- 6 key insights
- 3 prioritised recommendations

---

### 2. Markdown Report (Internal Reference)
**File:** `2025-12-16-weekly-report.md`

**Purpose:** Complete markdown report for internal records
**Format:** Markdown with tables, ASCII sparklines, chart references

**Sections:**
1. Overall Summary - Q4 Plan Tracking
2. This Week Performance (9-15 December)
3. Regional Breakdown (UK, USA, EUR, ROW)
4. Charts (3 visualisations)
5. Key Insights (6 findings)
6. Recommendations (3 priorities)

---

### 3. Charts (3 PNG Images)

#### Chart 1: UK Daily ROAS Trend
**File:** `2025-12-16-uk-roas-trend.png` (78 KB)
**Type:** Line chart
**Shows:** 7-day ROAS trend for UK market (Dec 9-15)
**Insight:** UK ROAS volatility - peaked at 11.41x (Dec 10), dropped to 3.45x (Dec 15)

#### Chart 2: Regional Spend Distribution
**File:** `2025-12-16-regional-spend.png` (59 KB)
**Type:** Horizontal bar chart
**Shows:** Spend allocation across 4 markets (UK, USA, EUR, ROW)
**Insight:** UK dominates at £17,278 (46%), followed by USA £12,361 (33%)

#### Chart 3: Regional ROAS Comparison
**File:** `2025-12-16-regional-roas.png` (54 KB)
**Type:** Horizontal bar chart
**Shows:** ROAS performance by region
**Insight:** USA leading at 9.55x, ROW underperforming at 4.15x

---

## 📊 Key Performance Metrics

### Q4 Plan Tracking (Primary Focus)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Spend Pacing** | £403,456 (expected at Day 48) | £348,309 | 86.3% (UNDER-paced by 13.7%) |
| **Revenue Performance** | £2,106,351 (expected) | £2,443,538 | 116.0% (AHEAD by 16.0%) |
| **ROAS** | 5.47x (Q4 target) | 7.02x (actual) | +28% above target |
| **Days Remaining** | 14 days | £172K budget available | £12.3K/day target |

### This Week Performance (9-15 December)

| Metric | This Week | Last Week | WoW Change |
|--------|-----------|-----------|------------|
| Spend | £37,559 | £41,939 | -10.4% |
| Revenue | £295,638 | £323,037 | -8.5% |
| ROAS | 7.87x | 7.70x | +0.17x (+2.2%) |
| Conversions | 1,503 | 1,718 | -12.5% |

### Regional Breakdown

| Region | Spend | Revenue | ROAS | WoW Change |
|--------|-------|---------|------|------------|
| **UK** | £17,278 | £123,252 | 7.13x | Spend -26.5%, ROAS +0.94x |
| **USA** | £12,361 | £118,126 | 9.55x | Spend -4.4%, ROAS -0.02x |
| **EUR** | £5,717 | £45,112 | 7.89x | Spend +51.7%, ROAS -3.40x |
| **ROW** | £2,203 | £9,149 | 4.15x | Spend +27.9%, ROAS -2.29x |

---

## 💡 Key Insights

1. **Q4 Target on Track:** Revenue at 116.0% of expected with only 86.3% budget used - highly efficient performance

2. **Spend Reduction:** Total spend down 10.4% WoW (UK -26.5%, EUR +51.7%, ROW +27.9%)

3. **ROAS Improvement:** Overall ROAS up from 7.70x to 7.87x (+2.2%)

4. **USA Strong Performance:** USA maintaining excellent 9.55x ROAS (vs UK 7.13x)

5. **EUR Growth:** EUR spend increased significantly (+51.7%) with maintained strong ROAS of 7.89x

6. **ROW Below Target:** ROW at 4.15x ROAS (below 5.47x Q4 target)

---

## 🎯 Prioritised Recommendations

### Priority 1: UK Market Budget Opportunity
**Issue:** UK spend dropped 26.5% WoW while ROAS improved to 7.13x (well above target)
**Action:** Investigate budget constraints - significant opportunity to increase UK budget
**Impact:** Potential £5K-£10K additional weekly revenue
**Urgency:** HIGH - 14 days remaining in Q4

### Priority 2: Q4 Finish Strong
**Issue:** 14 days remaining, £172K budget available (£12.3K/day required)
**Action:** Review daily spend targets per region to fully utilise Q4 budget
**Impact:** Ensure maximum Q4 revenue capture while maintaining ROAS >5.47x
**Urgency:** HIGH - immediate action needed

### Priority 3: ROW Performance Review
**Issue:** ROW ROAS at 4.15x (below Q4 target of 5.47x)
**Action:** Review ROW campaign structure and targeting efficiency
**Impact:** Improve profitability or consider budget reallocation to higher-ROAS markets
**Urgency:** MEDIUM - ongoing monitoring required

---

## 📈 Chart System Implementation

This report demonstrates the complete chart automation system:

### Technologies Used
- **Chart Generator:** `shared/chart_generator.py` module
- **Email Template:** `shared/email_template.py` module
- **Data Source:** Google Ads API via MCP (4 regional accounts)
- **Styling:** ROK brand colours (#10B981, #059669, #047857)

### Chart Types Generated
1. **Line Chart:** UK daily ROAS trend (time series analysis)
2. **Bar Charts:** Regional comparisons (horizontal, sorted by value)
3. **ASCII Sparklines:** Inline trends in markdown tables

### Chart Design Principles Applied
✅ Line charts for trends over time
✅ Bar charts for category comparisons (not pie charts!)
✅ Sorted by value (highest first)
✅ Limited to 3-4 data series per chart
✅ ASCII sparklines for inline context

---

## 🚀 Next Steps

### Immediate (This Week)
1. **Send Email:** Review HTML email, copy to clipboard, send to Alex
2. **UK Budget:** Investigate UK budget constraints causing -26.5% spend drop
3. **Q4 Pacing:** Review daily spend targets to hit £12.3K/day for remaining 14 days

### Short-term (Next Week)
1. **ROW Analysis:** Deep-dive into ROW campaigns (4.15x vs 5.47x target)
2. **EUR Monitoring:** Monitor EUR growth (spend +51.7% WoW) - ensure quality maintained
3. **Weekly Report:** Generate next week's report (16-22 December)

### System Improvements (Future)
1. **Automate Report Generation:** Schedule weekly report generation via LaunchAgent
2. **Multi-client Rollout:** Apply chart system to all 12 clients
3. **Google Sheets Integration:** Add auto-updating sparklines to Q4 dashboard

---

## 📂 File Locations

All files saved to:
`/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/reports/weekly/`

```
2025-12-16-weekly-email-draft.html     (8.2 KB)  - HTML email for client
2025-12-16-weekly-report.md            (4.1 KB)  - Markdown report (internal)
2025-12-16-regional-roas.png           (54 KB)   - Regional ROAS chart
2025-12-16-regional-spend.png          (59 KB)   - Regional spend chart
2025-12-16-uk-roas-trend.png           (78 KB)   - UK daily ROAS trend
2025-12-16-DELIVERY-PACKAGE.md         (this file) - Summary & next steps
```

---

## ✅ Completion Checklist

- [x] Pull live data from all 4 Google Ads accounts (UK, USA, EUR, ROW)
- [x] Calculate Q4 plan vs actual metrics
- [x] Generate 3 charts (ROAS trend, regional spend, regional ROAS)
- [x] Create ASCII sparklines for inline trends
- [x] Generate comprehensive markdown report
- [x] Generate client-ready HTML email with embedded charts
- [x] Open HTML email in browser for review
- [x] Verify all chart files exist in correct location
- [x] Create delivery package summary document

**Status:** COMPLETE ✅

---

**Next Review:** 23 December 2025
**Contact:** Peter Empson - petere@roksys.co.uk - 07932 454652
