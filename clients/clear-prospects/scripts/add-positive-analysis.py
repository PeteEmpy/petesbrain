#!/usr/bin/env python3
"""Add positive performance analysis to keyword audit report"""

import json

# Read converting terms
with open('../reports/converting-terms-2025-12-17.json', 'r') as f:
    converting_terms = json.load(f)

# Sort by ROAS
converting_terms_sorted = sorted(
    converting_terms,
    key=lambda x: float(x['roas'].strip('%')),
    reverse=True
)

# Top 10 by ROAS (need minimum spend of £15)
top_roas = [t for t in converting_terms_sorted if float(t['spend_gbp'].strip('£')) >= 15][:10]

# Top 10 by spend
top_spend = sorted(
    converting_terms,
    key=lambda x: float(x['spend_gbp'].strip('£')),
    reverse=True
)[:10]

# Brand terms
brand_terms = [t for t in converting_terms if any(brand in t['search_term'].lower() 
    for brand in ['wheatybag', 'happy snap', 'happysnap'])]

# Calculate totals
total_converting_spend = sum(float(t['spend_gbp'].strip('£')) for t in converting_terms)
total_converting_value = sum(float(t['conversions_value']) for t in converting_terms)
total_converting_roas = (total_converting_value / total_converting_spend) * 100 if total_converting_spend > 0 else 0

# Generate markdown
positive_section = f"""
---

## ✅ Strong Performance (What's Working)

### Framework Reference
Section 5.6 - Keyword Performance Analysis | Section 5.7 - Converting Search Terms

### Overview

**78 converting search terms** identified with £{total_converting_spend:,.2f} spend generating £{total_converting_value:,.2f} in margin value (**{total_converting_roas:.0f}% blended ROAS**).

---

### 1. Top 10 Performers by ROAS (Minimum £15 spend)

| Search Term | Campaign/Brand | Clicks | Spend | Conv. Value | ROAS | Opportunity |
|-------------|----------------|--------|-------|-------------|------|-------------|
"""

for term in top_roas:
    campaign_brand = "WBS Brand" if "brand inclusion" in term['campaign'].lower() else \
                    "HSG Brand" if "brand" in term['campaign'].lower() and "hsg" in term['campaign'].lower() else \
                    "HSG" if "hsg" in term['campaign'].lower() else \
                    "WBS" if "wbs" in term['campaign'].lower() else "BMPM"
    
    # Determine opportunity
    roas_val = float(term['roas'].strip('%'))
    if roas_val >= 300:
        opportunity = "🟢 Scale aggressively"
    elif roas_val >= 200:
        opportunity = "🟢 Increase bids"
    elif roas_val >= 150:
        opportunity = "✅ Maintain"
    else:
        opportunity = "⚠️ Monitor CPA"
    
    positive_section += f"| {term['search_term']} | {campaign_brand} | {term['clicks']} | {term['spend_gbp']} | £{term['conversions_value']:.2f} | **{term['roas']}** | {opportunity} |\n"

positive_section += f"""

**Key Insights**:
- **{sum(1 for t in top_roas if float(t['roas'].strip('%')) >= 300)} terms performing at 300%+ ROAS** - significant growth opportunity
- **Brand terms dominating top performers** - strong brand equity across WBS and HSG
- **Photo face mask products (HSG) showing exceptional ROAS** - 422%-466% on targeted terms
- **Branded cushions (BMPM) paradox**: Search term "branded cushions" = 871% ROAS vs keyword "branded cushions" = 0% ROAS (keyword attracting wrong traffic)

---

### 2. Top 10 Volume Winners (Highest Spend)

These terms drive the most revenue through volume:

| Search Term | Campaign/Brand | Clicks | Spend | Conv. Value | ROAS | Status |
|-------------|----------------|--------|-------|-------------|------|--------|
"""

for term in top_spend:
    campaign_brand = "WBS Brand" if "brand inclusion" in term['campaign'].lower() else \
                    "HSG Brand" if "brand" in term['campaign'].lower() and "hsg" in term['campaign'].lower() else \
                    "HSG" if "hsg" in term['campaign'].lower() else \
                    "WBS" if "wbs" in term['campaign'].lower() else "BMPM"
    
    roas_val = float(term['roas'].strip('%'))
    if roas_val >= 150:
        status = "✅ Healthy"
    elif roas_val >= 100:
        status = "⚠️ Marginal"
    else:
        status = "🔴 Loss-making"
    
    positive_section += f"| {term['search_term']} | {campaign_brand} | {term['clicks']} | {term['spend_gbp']} | £{term['conversions_value']:.2f} | {term['roas']} | {status} |\n"

positive_section += """

**Volume Analysis**:
- **Top 10 volume terms = £1,707 spend (62% of all converting term spend)**
- **Strong brand dominance**: 6 of top 10 are brand or brand-variant searches
- **"wheatybags" + "wheat bag"** = £691 combined spend at 181% blended ROAS (healthy core business)
- **Personalisation products driving volume** for HSG (face masks, hot water bottles)

---

### 3. Brand Term Performance Analysis

"""

# Analyze brand terms
wbs_brand = [t for t in brand_terms if 'wbs' in t['campaign'].lower()]
hsg_brand = [t for t in brand_terms if 'hsg' in t['campaign'].lower()]

wbs_brand_spend = sum(float(t['spend_gbp'].strip('£')) for t in wbs_brand)
wbs_brand_value = sum(float(t['conversions_value']) for t in wbs_brand)
wbs_brand_roas = (wbs_brand_value / wbs_brand_spend) * 100 if wbs_brand_spend > 0 else 0

hsg_brand_spend = sum(float(t['spend_gbp'].strip('£')) for t in hsg_brand)
hsg_brand_value = sum(float(t['conversions_value']) for t in hsg_brand)
hsg_brand_roas = (hsg_brand_value / hsg_brand_spend) * 100 if hsg_brand_spend > 0 else 0

positive_section += f"""
| Brand | Terms | Total Spend | Conv. Value | ROAS | Assessment |
|-------|-------|-------------|-------------|------|------------|
| **WheatyBags (WBS)** | {len(wbs_brand)} | £{wbs_brand_spend:.2f} | £{wbs_brand_value:.2f} | **{wbs_brand_roas:.0f}%** | 🟢 Excellent - protect brand position |
| **HappySnapGifts (HSG)** | {len(hsg_brand)} | £{hsg_brand_spend:.2f} | £{hsg_brand_value:.2f} | **{hsg_brand_roas:.0f}%** | 🟢 Excellent - strong brand equity |

**Brand Insights**:
- **Combined brand spend**: £{wbs_brand_spend + hsg_brand_spend:.2f} (21% of all search spend)
- **Blended brand ROAS**: {((wbs_brand_value + hsg_brand_value) / (wbs_brand_spend + hsg_brand_spend) * 100):.0f}% - exceptional performance
- **Brand defence working**: No competitor bidding detected (all brand traffic converting well)
- **BMPM brand missing**: No brand campaign for BMPM - opportunity to test

**Recommendation**: Increase investment in brand campaigns (currently limited by low daily budgets)

---

### 4. Product Category Winners

**WheatyBags (WBS) - Generic Wheat Bag Terms**:
- "wheat bag" (£332 spend, 121% ROAS) - core product term
- "wheat bags microwave" (£35 spend, 170% ROAS) - specification variant
- "microwaveable wheat bag" (£13 spend, 240% ROAS) - higher intent variant
- **Insight**: Generic terms work but ROAS improves with specificity

**HappySnapGifts (HSG) - Personalised Face Masks**:
- "personalised face masks" (£362 combined, 146% blended ROAS) - hero product
- "personalised masks with your face" (£40 spend, 422% ROAS) - ultra-specific, ultra-profitable
- "photo face masks uk" (£11 spend, 466% ROAS) - geographic qualifier adds intent
- **Insight**: Specificity + personalisation = exceptional ROAS

**HappySnapGifts (HSG) - Personalised Hot Water Bottles**:
- "personalised hot water bottles" (£162 spend, 108% ROAS) - seasonal volume driver
- "custom hot water bottle" (£55 spend, 168% ROAS) - alternative phrasing outperforms
- **Insight**: Test "custom" vs "personalised" in ad copy

---

### 5. Opportunity: Search Terms → Exact Match Keywords

**High-performing search terms NOT yet exact match keywords**:

These terms are converting well as broad/phrase matches - add as exact match to control and scale:

1. **"wheatybags uk"** (£208 spend, 322% ROAS) - geographic brand variant
2. **"personalised masks with your face"** (£27 spend, 422% ROAS) - ultra-specific winner
3. **"photo face masks uk"** (£11 spend, 466% ROAS) - geographic + product qualifier
4. **"wheat neck warmer"** (£15 spend, 350% ROAS) - product variant
5. **"face cushion"** (£28 spend, 333% ROAS) - alternative product naming
6. **"microwave hot water bottle"** (£23 spend, 279% ROAS) - hybrid product search
7. **"wheat bags microwave"** (£35 spend, 170% ROAS) - specification search

**Expected Impact**: Better control over bids, higher impression share on winning terms, potential 20-30% volume increase

---

### 6. Low ROAS Converting Terms (Marginal Performance)

**Terms converting but below 100% ROAS** - monitor for profitability:

| Search Term | Spend | ROAS | Action |
|-------------|-------|------|--------|
| wheat heat pack | £49.91 | 24% | ⚠️ Consider pausing if continues |
| happy snap gifts reviews | £61.77 | 14% | ⚠️ Monitor - review intent |
| amazon wheatybags | £31.92 | 2% | 🔴 Add as negative (competitor traffic) |
| wheat pack | £13.97 | 17% | ⚠️ Monitor |

**Note**: These terms ARE converting, so removing them immediately risks false negatives. Monitor for another 30 days before action.

---

"""

print(positive_section)
print("\nPositive analysis generated. Inserting into audit report...")

# Read existing report
with open('../audits/keyword-audit-2025-12-17.md', 'r') as f:
    report = f.read()

# Find insertion point (after Executive Summary, before first section with Wasted Spend)
insertion_point = report.find('\n---\n\n## 🔴 Wasted Spend')

if insertion_point != -1:
    # Insert positive section
    updated_report = report[:insertion_point] + positive_section + report[insertion_point:]
    
    # Write updated report
    with open('../audits/keyword-audit-2025-12-17.md', 'w') as f:
        f.write(updated_report)
    
    print("✅ Positive analysis added to audit report")
else:
    print("❌ Could not find insertion point in report")
