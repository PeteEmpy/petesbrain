# Crowd Control - Completed Tasks

## Comprehensive Barricades Performance Analysis & Report for Jeremy
**Completed:** 2025-11-20 14:10
**Source:** Client request - Jeremy Foster (email Nov 20, 2025)

**Client Request:**
Jeremy requested "a report for me for the cost of advertising the Barricade category for the year so far for each product" via email on Nov 20, 2025. Initial request referenced steel barricades page (https://crowdcontrolcompany.co.uk/prod/steel-barricades/) but expanded to cover ALL barricade products.

**What Was Created:**

1. **Comprehensive Excel Spreadsheet** (`all-barricades-12month-performance-2025-11-20.xlsx`)
   - Sheet 1: All 51 barricade products with 12-month performance data
   - Sheet 2: Summary by category (Steel, Gates, Expanding Metal, Expanding Plastic, Post & Panel)
   - Sheet 3: Overall performance summary
   - Columns: Product ID, Name, SKU, Category, Price, Stock Status, Spend, Impressions, Clicks, CTR, CPC, Conversions, Revenue, ROAS, Performance Notes
   - Formatted with Roksys branding (green headers), currency formatting, sortable/filterable for client use

2. **Customer-Facing Email** (`email-draft-2025-11-20-steel-barricades-report.html`)
   - 12-month overview for all 51 barricade products
   - Category performance breakdown
   - Critical finding: Silver 2.3m barricade out of stock (was 52% of steel barricade revenue)
   - Top performing products table
   - Poor performing products table
   - Product insights (gates outperform, specialty colours win, premium FlexPro not converting online)
   - Seasonal inventory planning guidance
   - 6 key actionable recommendations focused on inventory decisions Jeremy can control
   - Applied company standards: Verdana 13px, auto-sized tables (columns only as wide as content), Roksys green branding

**Key Findings:**

**Overall Performance (12 Months):**
- 51 total barricade products in catalogue
- 23 products advertised (28 not advertised)
- £17,052 total spend → £27,847 revenue
- 163% overall ROAS

**Performance by Category:**
- **Steel Barricades:** £3,946 → £8,936 (226% ROAS) ⭐ Best performing category
- **Expanding - Metal (FlexPro):** £3,989 → £7,057 (177% ROAS)
- **Expanding - Plastic (FlexMaster/FlexGate):** £8,669 → £11,817 (136% ROAS) - Highest spend category
- **Steel Gates:** £288 → £243 (84% ROAS) - Poor conversion
- **Post & Panel:** £4 → £0 - Minimal activity

**Critical Product Insights:**
- **Out of Stock Winner:** Silver 2.3m barricade (Product 6713) - Generated £4,711 from £2,285 spend (206% ROAS) before going OOS in June 2025. Lost revenue opportunity: £3,000-£5,000/quarter
- **Top Performers:** Pink barricades (424% ROAS), Yellow steel (795% ROAS), Yellow Small Gate (1,779% ROAS), FlexMaster 110 Yellow (137% ROAS)
- **Poor Performers:** Blue steel (0.4% ROAS), Green steel (0% ROAS), Silver Large Gate (£154 spend, £0 revenue)
- **Not Converting:** FlexPro 110 metal expanding (£55 spend, £0 return) - Premium products may need different sales approach

**Seasonal Patterns Identified:**
- Peak: March-April (420-887% ROAS)
- Good: June-July (500-807% ROAS)
- Weak: August-September (significant drop)
- Off: November-January (low volume)

**Recommendations Provided to Client:**
1. **Urgent:** Restock Silver 2.3m barricade if possible (high-revenue product)
2. Stock more Pink, Yellow steel, FlexMaster 110 Yellow (proven winners)
3. Consider discontinuing Blue and Green steel (tying up inventory capital with 0% returns)
4. Review gates category pricing/specifications (traffic but poor conversion)
5. Ensure adequate stock of FlexMaster 110 and FlexPro 160 (highest-spend category)
6. Stock up for March-April peak season (2-3x better conversion rates)

**Data Sources:**
- Google Ads API (GAQL query): 12-month shopping performance data (Nov 2024 - Nov 2025)
- WooCommerce API: Product catalogue, pricing, stock status, SKUs
- Customer ID: 9385103842
- Merchant Centre ID: 563545573

**Technical Implementation:**
- Created Python script to combine Google Ads performance data with WooCommerce product catalogue
- Generated Excel with openpyxl formatting (currency, percentages, Roksys branding)
- Applied company HTML standards: auto-sized tables, white-space: nowrap for numeric columns, normal wrapping for product names
- Customer-facing report excludes Google Ads technical recommendations (budgets, campaigns, bidding) per standard practice

**Files Created:**
- `/clients/crowd-control/reports/all-barricades-12month-performance-2025-11-20.xlsx` (Excel spreadsheet for client manipulation)
- `/clients/crowd-control/documents/email-draft-2025-11-20-steel-barricades-report.html` (Customer-facing email)
- `/clients/crowd-control/reports/steel-barricades-12month-performance-CLIENT-2025-11-20.html` (Detailed HTML report - superseded by Excel)
- `/clients/crowd-control/scripts/create-all-barricades-excel.py` (Generation script)

**Client Context:**
Jeremy at Crowd Control manages inventory decisions. This analysis helps him make data-driven choices about:
- Which products to keep in stock
- Which colours/styles to prioritise
- Seasonal inventory levels
- Products to discontinue
- Potential restocking opportunities

**Follow-Up:**
- Monitor if Jeremy requests similar analysis for other product categories
- Track if Silver 2.3m barricade gets restocked (high-value opportunity)
- Consider quarterly barricades performance reviews during seasonal planning (Feb for March-April peak, May for June-July season)

---
## [MEDIUM] Crowd Control - Fix Price Mismatches (6 products)
**Completed:** 2025-12-12 15:23
**Source:** Migrated from Google Tasks (Nov 18, 2025)

**Priority**: MEDIUM
**Products Affected**: 6 products with price mismatches

**Issue**: Feed price doesn't match landing page price

**Action Items**:
1. Access Crowd Control Merchant Center (ID: 563545573)
2. Identify 6 products with price mismatches
3. Compare feed price to landing page price
4. Update feed to match current website price
   - OR update website if feed price is correct

**Expected Impact**: Restore 6 products

**Reference**: See /tools/product-impact-analyzer/DISAPPROVAL-ACTION-PLAN.md

---
**MANUAL NOTE (2025-11-20 16:40):**
The problem here is that Google is seeing the exclusive VAT price and we're passing through the inclusive VAT price. This is something to do with snippets I think. Further investigation needs doing here. We need to drill down onto the page and look at what the metadata is.

---
**MANUAL NOTE (2025-11-20 17:15):**

**Page Analysis Completed:**

Compared two products:
- **A4 Sign Stand** (has issues): https://crowdcontrolcompany.co.uk/shop/210mm-x-297mm-black-a4-sign-stand/
- **Weathermaster Twin** (working correctly): https://crowdcontrolcompany.co.uk/shop/weathermaster-twin/

**KEY FINDING: Product Type Difference**

Both pages are missing proper Product schema markup (only have OnlineStore + Organization schemas), BUT:

**A4 Sign Stand (problematic):**
- Price: £82.80 inc. VAT (feed has correct price)
- Appears to be a **WooCommerce Variable Product**
- Variations: Black base, Polished Stainless (+£8), Polished Brass (+£34)
- Issue: Variable products may show base price (£69 excl. VAT?) + variation prices simultaneously

**Weathermaster Twin (working):**
- Price: £70.00 (sale) / £84.00 (regular) inc. VAT
- Product type: **Simple Product** with PPOM add-ons
- Add-ons: Belt length, custom colors (separate from base price)
- No price conflict visible to Google

**Next Steps for Tomorrow:**
1. Check in WooCommerce if A4 Sign Stand is set up as Variable Product
2. If yes, consider converting to Simple Product with add-ons (like Weathermaster)
3. Alternative: Ensure only ONE variation price displays at a time
4. Add proper Product schema markup to all product pages (separate issue but worth fixing)

---
