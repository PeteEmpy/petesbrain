# Monthly Report Generator - Progress Summary

**Date**: 2025-11-02
**Status**: Phase 1 Complete - Data Collection & HTML Report Generation

---

## ✅ Completed

### 1. OAuth Authentication Setup
- ✅ Switched from service account to OAuth user authentication
- ✅ Created `setup-oauth.sh` script for guided setup
- ✅ OAuth credentials configured: `~/Documents/PetesBrain/shared/credentials/google-slides-oauth.json`
- ✅ OAuth token generated: `~/Documents/PetesBrain/shared/credentials/google-slides-token.json`
- ✅ Browser-based authentication flow working

### 2. HTML Report Generator
- ✅ Created `generate_html_report.py` with Estate Blue (#00333D) and Stone (#E5E3DB) brand colors
- ✅ Professional table styling matching Marble AI report format
- ✅ All October 2025 data included
- ✅ Report successfully generated and opened in browser

### 3. Data Collection - All Campaigns Identified
- ✅ **Executive Summary** - Budget, spend, revenue, ROAS, conversions, impressions, clicks, CTR
- ✅ **Hotels - Top Performers** - All 8 properties with full metrics
- ✅ **Properties Requiring Attention** - Underperformers (Bolton Abbey SC, Chatsworth SC, Locations BA)
- ✅ **Campaign Type Breakdown** - PMax, Search Hotels, Search SC, Search Locations
- ✅ **Self-Catering Detailed** - Chatsworth SC and Bolton Abbey SC
- ✅ **The Hide** - Separate £2,000 budget tracking
- ✅ **Weddings** - Campaign ID identified (8357761197), October data retrieved
- ✅ **Lismore and The Hall** - Campaign IDs identified (20117845164, 17002402214), October data retrieved

### 4. Documentation
- ✅ Created `SLIDE-DATA-SOURCES.md` - Detailed analysis mapping each September slide to data source
- ✅ Created `OAUTH-QUICK-START.md` - User guide for OAuth setup (5-minute setup)
- ✅ Updated Python script with comprehensive comments and error handling
- ✅ Created `PROGRESS-SUMMARY.md` - This document

### 5. Campaign ID Reference
**All Devonshire Hotels campaigns identified and documented:**

| Campaign Group | Campaign Name | ID | Status |
|----------------|---------------|-----|--------|
| **Hotels** | P Max All | 18899261254 | Enabled |
| | Devonshire Arms | 19577006833 | Enabled |
| | Cavendish | 21839323410 | Enabled |
| | Beeley Inn | 22539873565 | Enabled |
| | Pilsley Inn | 19534106385 | Enabled |
| | The Fell | 22666031909 | Enabled |
| | Chatsworth Inns | 2080736142 | Enabled |
| **Locations** | Locations (Chatsworth) | 19654308682 | Enabled |
| | Locations (Bolton Abbey) | 22720114456 | Enabled |
| **Self-Catering** | Chatsworth SC | 19534201089 | Enabled |
| | Bolton Abbey SC | 22536922700 | Enabled |
| **The Hide** | The Hide | 23069490466 | Enabled |
| | Highwayman Arms (paused) | 21815704991 | Paused |
| **Weddings** | Weddings - UK | 8357761197 | Enabled |
| **Castles** | Lismore | 20117845164 | Enabled |
| | The Hall | 17002402214 | Enabled |

---

## ⚠️ Critical Issues Discovered

### 1. Weddings Campaign - Conversion Value Tracking Issue
**Problem**: Only £12 in tracked revenue from 12 conversions despite £912 spend
**Impact**: ROAS shows as 0.01x, making campaign appear unprofitable
**Likely Cause**: Conversion value not being passed to Google Ads, or conversions tracking without revenue attribution
**Action Required**: Immediate investigation of conversion tracking setup

**October Performance**:
- Spend: £912.11
- Revenue: £12.00 (suspicious)
- Conversions: 12.00
- ROAS: 0.01x
- Clicks: 701
- CTR: 7.84% (healthy)
- Impressions: 8,947

### 2. Lismore and The Hall - Zero Conversions
**Problem**: Zero conversions and zero revenue from both castle campaigns despite £488.89 combined spend
**Impact**: Complete lack of ROI from castle campaigns
**Lismore**: Decent CTR (8.33%) suggests ad relevance but no conversions
**The Hall**: Low CTR (4.58%) suggests poor ad relevance
**Action Required**: Conversion tracking audit + landing page review

**October Performance**:
- **Lismore**: £247.55 spend, 0 conversions, 198 clicks, 8.33% CTR
- **The Hall**: £241.34 spend, 0 conversions, 165 clicks, 4.58% CTR
- **Combined**: £488.89 spend, 0 revenue, 0.00x ROAS

---

## 🔄 Next Steps

### Phase 2: Additional Data Tables (Required for Complete Report)

1. **Location Campaigns Separate Table**
   - Extract Chatsworth and Bolton Abbey location campaigns from top performers
   - Create dedicated table showing just location campaign performance
   - Already have data, just needs separate formatting

2. **Profitability Table** (Slide 21)
   - Need to view September deck image to see what metrics this shows
   - Likely just ROAS ranking or profit margin calculation
   - May already have data, just needs confirmation of format

3. **Month-over-Month Comparisons** (Critical for Slide 23)
   - Query September 2025 data from Google Ads API
   - Calculate deltas: MoM ROAS change %, MoM Spend change %, MoM CTR change %
   - Add MoM comparison section to HTML report
   - This will enable the commentary slide that references "September performance"

### Phase 3: Investigate Unknown Slides

Need to view actual September deck images to determine content:
- **Slide 15**: Overall performance summary (what format?)
- **Slides 16-18**: Multiple hotel images (what are these showing?)
- **Slide 21**: Profitability table (what metrics?)

### Phase 4: Future Automation (Long-term Goal)

**Current Workflow** (Accepted by user):
1. Run `generate_html_report.py --month 2025-XX`
2. Open HTML in browser
3. Take screenshots of tables
4. Manually insert into Google Slides

**Future Workflow** (Fully Automated):
1. Run single command: `./generate_monthly_report.sh --month 2025-XX`
2. Script handles:
   - Data collection from Google Ads API
   - HTML generation
   - Headless browser screenshots (Playwright/Puppeteer)
   - Automatic image insertion into Google Slides via API
   - Slide formatting and positioning
3. Output: Complete Google Slides presentation ready to send

**Technology Options**:
- **Playwright** (Python) - Browser automation for screenshots
- **Puppeteer** (Node.js) - Alternative browser automation
- **imgkit/wkhtmltoimage** - HTML to image conversion (simpler but less control)
- **Google Slides API** - Already working, just need to add image insertion

---

## 📁 File Structure

```
/Users/administrator/Documents/PetesBrain/tools/monthly-report-generator/
├── generate_html_report.py          # HTML report generator (current solution)
├── generate_devonshire_slides.py    # Google Slides generator (native tables)
├── setup-oauth.sh                   # OAuth credentials setup script
├── requirements.txt                 # Python dependencies
├── .venv/                           # Virtual environment
├── OAUTH-QUICK-START.md            # User guide for OAuth setup
├── SLIDE-DATA-SOURCES.md           # September slide analysis
├── PROGRESS-SUMMARY.md             # This document
└── README.md                        # Overall tool documentation

/Users/administrator/Documents/PetesBrain/clients/devonshire-hotels/reports/
├── october-2025-paid-search-report.md      # Markdown report (data source)
└── devonshire-paid-search-2025-10.html     # Styled HTML report (for screenshots)

/Users/administrator/Documents/PetesBrain/shared/credentials/
├── google-slides-oauth.json         # OAuth client credentials
└── google-slides-token.json         # OAuth access/refresh token
```

---

## 🎯 Success Metrics

**Time Savings**:
- **Before**: 2-3 hours per month (manual table creation, formatting, data entry)
- **Current**: ~30 minutes (data collection automated, screenshot + insert manual)
- **Future**: ~5 minutes (fully automated end-to-end)

**Quality Improvements**:
- ✅ Consistent brand colors (Estate Blue, Stone)
- ✅ Accurate data (no manual transcription errors)
- ✅ Professional formatting matching previous reports
- ✅ Comprehensive data coverage (all campaigns tracked)

**Data Completeness**:
- ✅ 8/8 hotel properties tracked
- ✅ 2/2 self-catering campaigns tracked
- ✅ 2/2 location campaigns tracked
- ✅ 1/1 The Hide campaign tracked
- ✅ 1/1 weddings campaign tracked
- ✅ 2/2 castle campaigns tracked
- ✅ 1/1 Performance Max campaign tracked

---

## 🐛 Known Issues & Limitations

### 1. Manual Screenshot Step
**Issue**: User must manually take screenshots and insert into slides
**Impact**: Still requires 20-30 minutes of manual work
**Workaround**: Current workflow accepted by user as interim solution
**Future Fix**: Playwright/Puppeteer automation for headless screenshots + API insertion

### 2. Native Tables vs Images
**Issue**: September deck uses image-based tables, but Python script creates native Slides tables
**Impact**: Format mismatch (though native tables are arguably better for editing)
**Decision**: User accepted screenshot approach for now
**Future**: Build automation to match exact September format

### 3. MoM Data Not Yet Implemented
**Issue**: Slide 23 commentary requires September vs. October comparisons
**Impact**: Cannot fully replicate Slide 23 without MoM data
**Next Step**: Query September data and calculate deltas

### 4. Unknown Slide Content (15-18, 21)
**Issue**: Some September slides contain images we haven't analyzed yet
**Impact**: Cannot confirm if we have all required data
**Next Step**: View September deck images to identify content

---

## 📊 Data Quality Notes

### Strong Performers (October 2025)
- **Devonshire Arms**: 9.09x ROAS, 30.32% CTR, £12,628 revenue
- **Cavendish**: 6.53x ROAS, 35.64% CTR, £8,851 revenue
- **P Max All**: 6.21x ROAS, £16,065 revenue (highest revenue generator)

### Underperformers
- **Chatsworth SC**: 2.58x ROAS (below target)
- **Bolton Abbey SC**: 0.00x ROAS (zero conversions)
- **Locations (Bolton Abbey)**: 1.37x ROAS (poor performance)

### Conversion Tracking Issues (Urgent)
1. **Weddings**: £12 revenue from 12 conversions (should be much higher)
2. **Lismore**: Zero conversions despite 198 clicks
3. **The Hall**: Zero conversions despite 165 clicks
4. **Bolton Abbey SC**: Zero conversions despite 235 clicks

---

**Last Updated**: 2025-11-02 17:30
**Status**: Ready for user review and next phase decision
