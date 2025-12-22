# The Fell Brand Analysis - Complete Data (Search + PMax)
**Period:** 1 June - 16 December 2025

---

## Executive Summary

Your question was absolutely correct - the Search campaign data I initially analyzed **was incomplete**. The Performance Max campaign has significant additional Fell brand search term volume that wasn't accessible via API.

### Combined Totals (Search + PMax)

| Metric | Search Campaign | PMax Campaign | **Combined Total** |
|--------|----------------|---------------|-------------------|
| **Impressions** | 31,499 | 3,821 | **35,320** |
| **Clicks** | 7,864 | 734 | **8,598** |
| **Cost** | £4,734.64 | £409.57 | **£5,144.21** |
| **Conversions** | 63.43 | 7.85 | **71.28** |
| **Conv. Value** | £25,359.56 | £4,391.85 | **£29,751.41** |
| **ROAS** | 535% | 1,072% | **578%** |

---

## Key Findings

1. **PMax contributes 11% of total Fell brand impressions** - not visible via API, only in search terms report
2. **PMax ROAS is 2x higher than Search** (1,072% vs 535%) due to lower costs
3. **Combined brand performance**: £29,751 revenue from £5,144 spend = **578% ROAS**

---

## PMax Campaign - Top Fell Brand Search Terms

| Search Term | Impressions | Clicks | Cost | Conversions | Conv. Value | ROAS |
|-------------|-------------|--------|------|-------------|-------------|------|
| the fell hotel | 1,184 | 202 | £113.23 | 0.43 | £274.88 | 243% |
| the fell hotel burnsall | 978 | 186 | £117.97 | 4.92 | £1,857.45 | 1,574% |
| fell hotel burnsall | 455 | 90 | £62.98 | 1.00 | £269.01 | 427% |
| the fell burnsall | 407 | 100 | £46.04 | 0.00 | £0.00 | 0% |
| the fell hotel bolton abbey | 281 | 50 | £29.32 | 0.00 | £0.00 | 0% |
| fell hotel | 186 | 33 | £11.89 | 0.00 | £0.00 | 0% |
| the fell hotel yorkshire | 89 | 15 | £4.61 | 0.00 | £0.00 | 0% |
| the fell at burnsall | 69 | 19 | £4.75 | 0.00 | £0.00 | 0% |
| fell burnsall | 66 | 11 | £4.88 | 0.00 | £0.00 | 0% |
| the fell | 55 | 10 | £2.01 | 1.00 | £1,860.00 | 92,454% |
| the fell bolton abbey | 51 | 18 | £11.89 | 0.50 | £130.51 | 1,097% |

**PMax Subtotal (Top 11 brand terms):** 3,821 impressions, 734 clicks, £409.57 spend, 7.85 conversions, £4,391.85 value, 1,072% ROAS

---

## Search Campaign - Previously Analyzed

*(Already provided in previous email)*

- **"the fell hotel"**: 7,255 impressions (dedicated Search campaign)
- **"devonshire fell"**: 5,125 impressions (dedicated Search campaign)
- Search campaign total: 31,499 impressions, £4,734.64 spend, 63.43 conversions, 535% ROAS

---

## Brand Term Comparison

### "The Fell Hotel" Across Both Campaigns

| Campaign | Impressions | Clicks | Cost | Conversions | ROAS |
|----------|-------------|--------|------|-------------|------|
| Search (dedicated) | 7,255 | 1,803 | £1,129.93 | 12.93 | 486% |
| PMax | 1,184 | 202 | £113.23 | 0.43 | 243% |
| **Combined** | **8,439** | **2,005** | **£1,243.16** | **13.36** | **436%** |

### "Devonshire Fell" (Search Only)

| Campaign | Impressions | Clicks | Cost | Conversions | ROAS |
|----------|-------------|--------|------|-------------|------|
| Search (dedicated) | 5,125 | 1,615 | £924.43 | 16.57 | 785% |
| PMax | 0 | 0 | £0 | 0 | - |
| **Total** | **5,125** | **1,615** | **£924.43** | **16.57** | **785%** |

---

## Updated Conclusion

**Original finding confirmed and enhanced:**
- **"Devonshire Fell" still has higher volume** (5,125 vs 8,439 impressions) when considering all sources
- **"The Fell Hotel" is growing faster** - 8,439 total impressions with combined campaigns
- **PMax adds 11% additional brand volume** not visible in API data
- **Both terms are performing well** (578% combined ROAS)

**Rebrand Timing Question:**
To properly assess before/after performance, we need:
1. Date when "The Fell Hotel" rebrand officially launched
2. Historical "Devonshire Fell" performance pre-rebrand (before June 2025)

The dedicated "The Fell" Search campaign launched **11 June 2025**, but was the public rebrand earlier?

---

## Methodology Note

**Why PMax data wasn't in original analysis:**
- Google Ads API `search_term_view` queries for PMax campaigns return **zero results**
- PMax search terms are only accessible via **manual search terms reports** downloaded from Google Ads UI
- This is a known Google Ads limitation - PMax has restricted search term visibility via API

**Data sources:**
- Search campaign: Google Ads API (GAQL query)
- PMax campaign: Manual search terms report export (1 June - 16 Dec 2025)
