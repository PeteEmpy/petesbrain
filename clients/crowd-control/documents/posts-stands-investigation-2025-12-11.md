# Crowd Control: Posts & Panels Investigation Report
**Date**: 11 December 2025  
**Investigation**: Why are posts and stands performing poorly in UK vs US?

---

## Issue Summary

Jeremy reported that the US office is doing very well with posts and panels (stands), but they're getting zero clicks in the UK despite having these products listed.

**Email (Dec 9, 2025)**:
> "We are told by the US office that they are doing very well with posts and panels. I have them listed but we are not even getting any clicks."

---

## Data Analysis

### Actual Performance (Nov 11 - Dec 11, 2025)

**The claim is INCORRECT** - they ARE getting clicks:

- **79 distinct Posts/Panels products** with performance data
- **~72,000 impressions** across all posts/panels products
- **~533 clicks** across all products
- **Average CTR: 0.60%** (reasonable for e-commerce)

### Top Performing Posts/Panels Products

| Product | Impressions | Clicks | CTR | Cost | Revenue | ROAS |
|---------|-------------|--------|-----|------|---------|------|
| Belt Barrier 4 Pack | 10,447 | 115 | 1.10% | £785.51 | **£0.00** | 0% |
| A3 Floor Sign Stand | 6,010 | 39 | 0.65% | £117.94 | **£0.00** | 0% |
| Sign Stand A4 | 5,491 | 49 | 0.89% | £73.85 | **£0.00** | 0% |
| Belt Barrier 6 Pack | 4,292 | 20 | 0.47% | £136.61 | **£0.00** | 0% |
| Outdoor A3 Sign Stand | 4,247 | 23 | 0.54% | £74.68 | **£0.00** | 0% |

---

## Root Cause Analysis: THE REAL PROBLEM

❌ **NOT a visibility problem** - These products ARE getting clicks  
❌ **NOT zero clicks** - They're averaging 0.60% CTR which is healthy  

✅ **THE ACTUAL PROBLEM: 0% ROAS across ALL posts/panels products**

Every single post/panel product shows:
- Cost: Ranging from £0.51 to £785.51
- Revenue: **£0.00**
- Conversions: Mostly 0, a few with <10%

### What This Means

Customers are **clicking on the products** but:
1. **They're not converting to orders**, OR
2. **Conversions aren't being tracked/recorded**, OR
3. **The click→order path is broken**

---

## Secondary Clue: WooCommerce Outdated

Jeremy also mentioned:
> "Google Analytics is not working with WooCommerce as Woo is out of date."

**This is likely the issue**: If WooCommerce is outdated, the conversion tracking integration between Google Ads and WooCommerce may be broken. Customers click → view product → add to cart → checkout, but the conversion signal doesn't flow back to Google.

---

## Recommended Actions

1. **Priority 1**: Verify conversion tracking setup in Google Ads
   - Check if Google Analytics property is linked to Google Ads account
   - Verify WooCommerce conversion pixel is firing
   - Test a purchase from start to finish to see if it tracks

2. **Priority 2**: Update WooCommerce
   - Patch WooCommerce to latest version
   - Ensure Google Analytics 4 integration is current
   - Re-enable proper ecommerce tracking

3. **Priority 3**: Check product feed quality
   - Verify all posts/panels products have:
     - Correct pricing
     - Stock availability status
     - Product category tags
     - Landing page URLs

4. **Priority 4**: Monitor conversion funnel
   - After WooCommerce update, rerun this analysis
   - Compare ROAS before/after to confirm tracking fix

---

## Why They Work in US But Not UK

**This is likely NOT a product quality issue** - it's a **technical tracking issue specific to the UK account**:

- US office may be using different conversion tracking setup
- US site may have updated WooCommerce/GA4 integration
- UK site's setup is outdated and conversions aren't recording

**The posts/panels aren't bad products** - they're getting reasonable click volumes. The problem is the infrastructure to track those clicks into sales isn't working.

