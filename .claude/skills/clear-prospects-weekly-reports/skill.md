---
name: clear-prospects-weekly-reports
description: Generates three separate weekly Google Ads reports for Clear Prospects brands (HSG, WBS, BMPM) with brand-specific filtering and analysis. Use when user says "Clear Prospects weekly reports", "Clear Prospects report", or needs multi-brand performance analysis for Clear Prospects.
allowed-tools: mcp__google-ads__run_gaql, mcp__google-ads__list_accounts, Read, Write, Bash
---

# Clear Prospects Weekly Reports (Multi-Brand)

---

## Instructions

When this skill is invoked:

### 1. Get Context and Confirm Date Range

Read Clear Prospects context:
```bash
Read: clients/clear-prospects/CONTEXT.md
```

Ask user to confirm:
- **Date range** (defaults to last 7 days if not specified)

Display:
```
Generating weekly reports for Clear Prospects (3 brands):
✓ HappySnapGifts (HSG)
✓ WheatyBags (WBS)
✓ British Made Promotional Merchandise (BMPM)

Period: [Start Date] - [End Date]
This will create 3 separate reports...
```

### 2. Extract Account Details

From CONTEXT.md:
- **Google Ads Customer ID**: 6281395727
- **Merchant Centre IDs**:
  - HSG: 7481296
  - WBS: 7481286
  - BMPM: 7522326

### 3. Generate Three Separate Reports

For each brand (HSG, WBS, BMPM), generate a complete weekly report following the same structure as the google-ads-weekly-report skill, but with brand-specific filtering:

#### Brand Configuration:

```python
BRANDS = {
    'hsg': {
        'name': 'HappySnapGifts',
        'short_name': 'HSG',
        'campaign_prefix': 'CPL | HSG |',
        'merchant_centre_id': '7481296',
        'website': 'https://happysnapgifts.co.uk/',
        'color': '#FF6B6B'  # For HTML styling
    },
    'wbs': {
        'name': 'WheatyBags',
        'short_name': 'WBS',
        'campaign_prefix': 'CPL | WBS |',
        'merchant_centre_id': '7481286',
        'website': 'https://wheatybags.co.uk/',
        'color': '#4ECDC4'
    },
    'bmpm': {
        'name': 'British Made Promotional Merchandise',
        'short_name': 'BMPM',
        'campaign_prefix': 'CPL | BMPM |',
        'merchant_centre_id': '7522326',
        'website': 'https://bmpm.trade/',
        'color': '#95E1D3'
    }
}
```

#### Data Extraction (Per Brand):

**Step 1: Pull Campaign-Level Data**

Filter campaigns by brand prefix:

```python
# For each brand, run GAQL query with campaign name filter
query = f"""
SELECT
  campaign.name,
  campaign.id,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.clicks,
  metrics.impressions,
  metrics.ctr,
  metrics.average_cpc,
  metrics.search_impression_share
FROM campaign
WHERE segments.date DURING {date_range}
  AND campaign.status = 'ENABLED'
  AND campaign.name LIKE '{brand_prefix}%'
ORDER BY metrics.cost_micros DESC
"""
```

**Step 2: Pull Product-Level Data**

Filter products by Merchant Centre ID:

```python
# Product performance filtered by MC ID
query = f"""
SELECT
  segments.product_item_id,
  segments.product_title,
  segments.product_merchant_id,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.clicks,
  metrics.impressions
FROM shopping_performance_view
WHERE segments.date DURING {date_range}
  AND segments.product_merchant_id = {merchant_centre_id}
ORDER BY metrics.conversions_value DESC
LIMIT 100
"""
```

**Step 3: Pull Placement Data (Per Brand)**

Filter ad network performance by campaigns matching brand prefix:

```python
# Get placement data for brand campaigns only
query = f"""
SELECT
  segments.ad_network_type,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.clicks,
  metrics.impressions
FROM campaign
WHERE segments.date DURING {date_range}
  AND campaign.name LIKE '{brand_prefix}%'
  AND campaign.status = 'ENABLED'
"""
```

### 4. Generate Brand-Specific Reports

For each brand, create a complete report with:

**Report Structure** (same as google-ads-weekly-report but brand-scoped):

```markdown
# Google Ads Weekly Report: [Brand Name]
**Period:** [Start Date] - [End Date]
**Website:** [Brand Website]
**Generated:** [Today's Date]

---

## Executive Summary

### Account Performance ([Brand])
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Spend | £X,XXX | £X,XXX | +X% |
| Conversions | XXX | XXX | +X% |
| Conv Value | £XX,XXX | £XX,XXX | +X% |
| ROAS | XXX% | XXX% | +Xpp |
| CPA | £XXX | £XXX | -X% |
| CTR | X.X% | X.X% | +X% |
| Avg CPC | £X.XX | £X.XX | +X% |

**Key Takeaway:** [One-line summary of brand performance]

---

## Campaign Breakdown

### Top Performing Campaigns
[Only campaigns with '{brand_prefix}' prefix]

### Campaigns Requiring Attention
[Brand-specific campaign issues]

---

## Product Performance

### Top 10 Products by Revenue
[Only products from MC ID {merchant_centre_id}]

### Bottom 10 Products (High Spend, Low ROAS)
[Brand-specific product issues]

---

## Placement Analysis

[Brand-specific placement data]

---

## Prioritised Recommendations

[Brand-specific recommendations]

---

**Next Review:** [Next week's date]
```

### 5. Save Reports with Brand-Specific Naming

**File naming convention:**

```python
# Create reports/weekly/ directory if needed
reports_dir = Path("clients/clear-prospects/reports/weekly")
reports_dir.mkdir(parents=True, exist_ok=True)

# For each brand:
for brand_key, brand_config in BRANDS.items():
    report_date = datetime.now().strftime('%Y-%m-%d')
    brand_slug = brand_key  # 'hsg', 'wbs', 'bmpm'

    # Markdown version
    md_path = reports_dir / f"{report_date}-{brand_slug}-weekly-report.md"

    # HTML version
    html_path = reports_dir / f"{report_date}-{brand_slug}-weekly-report.html"

    # Save both versions
    with open(md_path, 'w') as f:
        f.write(markdown_content)

    with open(html_path, 'w') as f:
        f.write(html_content)
```

**File paths created** (for each brand):
- `clients/clear-prospects/reports/weekly/YYYY-MM-DD-hsg-weekly-report.md`
- `clients/clear-prospects/reports/weekly/YYYY-MM-DD-hsg-weekly-report.html`
- `clients/clear-prospects/reports/weekly/YYYY-MM-DD-wbs-weekly-report.md`
- `clients/clear-prospects/reports/weekly/YYYY-MM-DD-wbs-weekly-report.html`
- `clients/clear-prospects/reports/weekly/YYYY-MM-DD-bmpm-weekly-report.md`
- `clients/clear-prospects/reports/weekly/YYYY-MM-DD-bmpm-weekly-report.html`

### 6. Task Creation (Per Brand)

**Apply same smart task creation logic from google-ads-weekly-report skill:**

For each brand's P0 recommendations that meet threshold criteria:
- Create tasks with brand prefix: `[Clear Prospects - HSG]`, `[Clear Prospects - WBS]`, `[Clear Prospects - BMPM]`
- All tasks go to `clients/clear-prospects/tasks.json`
- Tag with brand: `["weekly-report", "optimization", brand_key]`

**Threshold criteria** (same as google-ads-weekly-report):
- ROAS drop >20% WoW
- Campaign with 0 conversions spending >£50/week
- ROAS >15% below target
- Identified waste >£100/month

### 7. Generate Summary for User

**Multi-Brand Summary:**

```
✅ Clear Prospects Weekly Reports Generated (3 Brands)

**Period:** [Start Date] - [End Date]
**Reports Saved:** clients/clear-prospects/reports/weekly/

---

### HappySnapGifts (HSG)
- Spend: £X,XXX (+X% WoW)
- ROAS: XXX% (+Xpp WoW)
- Conversions: XXX (+X% WoW)
- **Status:** [✅ On target / ⚠️ Needs attention / 🔴 Critical]
- **Top Issue:** [Most important recommendation or "None - performing well"]

### WheatyBags (WBS)
- Spend: £X,XXX (+X% WoW)
- ROAS: XXX% (+Xpp WoW)
- Conversions: XXX (+X% WoW)
- **Status:** [✅ On target / ⚠️ Needs attention / 🔴 Critical]
- **Top Issue:** [Most important recommendation or "None - performing well"]

### British Made Promotional Merchandise (BMPM)
- Spend: £X,XXX (+X% WoW)
- ROAS: XXX% (+Xpp WoW)
- Conversions: XXX (+X% WoW)
- **Status:** [✅ On target / ⚠️ Needs attention / 🔴 Critical]
- **Top Issue:** [Most important recommendation or "None - performing well"]

---

**Tasks Created:** X tasks (Y from HSG, Z from WBS, A from BMPM)

**Files:**
- YYYY-MM-DD-hsg-weekly-report.html
- YYYY-MM-DD-wbs-weekly-report.html
- YYYY-MM-DD-bmpm-weekly-report.html
```

---

## Brand-Specific Context

### HappySnapGifts (HSG)
- **Target ROAS:** ~115% (based on CONTEXT.md)
- **Key Products:** Photo cushions, face masks, bunting, photo aprons
- **Recent Strategy:** Face masks consolidated into Search campaign (Sep 2025) - significant performance improvement
- **Watch For:** Shopping vs Search channel performance

### WheatyBags (WBS)
- **Target ROAS:** ~130% (based on CONTEXT.md)
- **Key Products:** Wheat bags, hot water bottles, heat packs
- **Budget:** Main Search campaign has 24% Budget Lost IS - monitor closely
- **Watch For:** Budget utilization and impression share

### BMPM
- **Target ROAS:** 70% (newly set Nov 2025)
- **Status:** Restructuring for profitability (was unprofitable in Sep/Oct)
- **Key Products:** Branded cushions, promotional merchandise
- **Recent Changes:** PMax budget reduced to £50/day, new Search campaign started Oct 21
- **Watch For:** Whether new 70% ROAS target improves algorithm performance

---

## HTML Report Branding

Each brand report should use **brand-specific header color** while maintaining ROK branding:

```html
<style>
    .header {
        background: linear-gradient(135deg,
            ${brand.color} 0%,
            ${darken(brand.color, 20%)} 100%);
        color: white;
        padding: 30px;
    }

    .brand-badge {
        background: ${brand.color};
        color: white;
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>

<div class="header">
    <div class="logo">
        <img src="file:///Users/administrator/Documents/PetesBrain/shared/assets/branding/roksys-logo-200x50.png" alt="ROK Systems">
    </div>
    <h1>Google Ads Weekly Report: <span class="brand-badge">${brand.short_name}</span></h1>
    <div class="meta">
        ${brand.name} | ${brand.website}<br>
        Period: ${period_dates} | Generated: ${report_date}
    </div>
</div>
```

---

## Error Handling

**If brand has no campaigns:**
- Note in report: "No active campaigns found for [Brand] during this period"
- Skip task creation for that brand
- Continue with other brands

**If product data missing for brand:**
- Note in report: "Product-level data unavailable for [Brand]"
- Check Merchant Centre feed status in recommendations
- Focus on campaign-level analysis

**If one brand fails:**
- Continue generating reports for other brands
- Show error message for failed brand
- Still provide summary of successfully generated reports

---

## State Tracking

Update `data/state/weekly-reports-generated.json` with all three reports:

```json
{
  "reports": [
    {
      "client": "Clear Prospects",
      "client_slug": "clear-prospects",
      "brand": "HappySnapGifts",
      "brand_slug": "hsg",
      "date": "2025-11-20",
      "period": "2025-11-13 to 2025-11-19",
      "md_path": "clients/clear-prospects/reports/weekly/2025-11-20-hsg-weekly-report.md",
      "html_path": "clients/clear-prospects/reports/weekly/2025-11-20-hsg-weekly-report.html",
      "tasks_created": 2,
      "generated_at": "2025-11-20T10:30:00"
    },
    // ... WBS and BMPM entries
  ]
}
```

---

## Testing Checklist

✅ All 3 reports generate successfully
✅ Each report only shows brand-specific campaigns
✅ Product data correctly filtered by Merchant Centre ID
✅ Brand-specific colors applied in HTML
✅ Calculations accurate (spot-check ROAS for one campaign per brand)
✅ Tasks created with correct brand prefix in title
✅ Summary shows all 3 brands clearly
✅ Reports generated in <10 minutes total

---

## Notes

- This skill is **Clear Prospects-specific** (not generic multi-brand)
- Uses same analysis logic as `google-ads-weekly-report` skill
- Each brand treated as independent report (no cross-brand comparison)
- British English throughout (analyse, optimise)
- ROAS always as percentage (120% not £1.20)
- Tasks only created for P0 + threshold criteria (prevents flooding)

---

**Last Updated:** 2025-11-20
**Status:** Ready for testing
