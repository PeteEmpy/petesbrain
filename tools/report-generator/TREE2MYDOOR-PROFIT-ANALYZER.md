# Tree2mydoor Profit-Focused Campaign Analyzer

**Created:** 2025-12-16
**Status:** ✅ Complete and tested

## Overview

Comprehensive campaign analyzer specifically built for Tree2mydoor's profit-based optimization using ProfitMetrics integration. This analyzer understands that Tree2mydoor is NOT a typical revenue-based account.

## Key Differentiators from Generic Analyzer

### 1. Profit-Based Optimization (Not Revenue)

**Critical Understanding:**
- `conversions_value` field = **PROFIT** (not revenue)
- All "ROAS" references changed to **POAS (Profit on Ad Spend)**
- Example: £100 spend generating £160 profit = 160% POAS

**Why This Matters:**
- Generic analyzer treats conversions_value as revenue → wrong strategic decisions
- Profit-based analyzer understands true margins → correct optimization priorities
- POAS 1.60x is very different from ROAS 1.60x (profit margin already factored in)

### 2. Tier A/B/C Campaign Structure

Respects Tree2mydoor's Channable/Product Hero tier structure:

| Tier | POAS Threshold | Action |
|------|----------------|--------|
| **Tier A** | ≥1.80x | Scale aggressively (+20-30% budget) |
| **Tier B** | ≥1.45x | Maintain budget, optimize to Tier A |
| **Tier C** | ≥1.35x | THROTTLE (-30% budget) |
| **Below Tier C** | <1.35x | PAUSE or reduce -50% |

**Generic Analyzer**: Uses simple ROAS >1.6x / <1.6x split (too simplistic)
**Profit Analyzer**: 4-tier structure with specific budget actions per tier

### 3. Product Hero Integration

Provides guidance on Product Hero label system:

- **Heroes**: Top profit generators → maximize impression share
- **Sidekicks**: Good converters → scale carefully
- **Villains**: Underperformers → review/optimize
- **Zombies**: No conversions → exclude or throttle heavily

**Actionable Recommendations:**
- "Check Product Hero labels via Channable"
- "Shift budget to Heroes/Sidekicks"
- "Ensure Zombies aren't draining budget from Heroes"
- "Calculate POAS by label (Heroes vs Sidekicks vs Villains vs Zombies)"

### 4. Seasonality Awareness

Recognizes Tree2mydoor's seasonal patterns:

**Peak Seasons (Automatic Detection):**
- December: Christmas gifts, memorial trees
- November: Pre-Christmas shopping
- May: Mother's Day

**Peak Season Actions:**
- Increase Tier A budgets by 30-50%
- Focus on Heroes (maximum impression share)
- Monitor stock stability (OOS during peak = massive missed opportunity)
- Update assets with seasonal messaging

**Non-Peak Actions:**
- Maintain POAS targets strictly
- Test new products/categories (lower CPCs)
- Build up high-performing campaigns for next peak

### 5. Client-Specific Considerations

**Gareth's Needs (ADHD Consideration):**
- Comprehensive written reports (not just summaries)
- Clear actionable steps with specific numbers
- Structured monthly format with MoM trends
- No phone communication - written/transcribed only

**Known Issues (Factored In):**
- Stock instability affects campaign learning
- CPC inflation outpacing efficiency gains
- Feed issues can reset learning on bestsellers
- Profit compression at scale

### 6. Knowledge Base Integration

Searches knowledge base for relevant recommendations:
- Performance Max optimization strategies
- Profit-based bidding best practices
- Product feed management
- Seasonal campaign strategies
- Google ecosystem best practices

## File Structure

```
tools/report-generator/
├── tree2mydoor_profit_analyzer.py      # Core profit analyzer (extends CampaignAnalyzer)
├── tree2mydoor_html_generator.py       # HTML generator with profit-specific sections
├── run_tree2mydoor_profit_report.py    # Test script with real data
└── reports/
    ├── tree2mydoor_profit_analysis_TIMESTAMP.html
    └── tree2mydoor_profit_analysis_TIMESTAMP.json
```

## Usage

### Generate Profit-Focused Report

```python
from tree2mydoor_profit_analyzer import Tree2mydoorProfitAnalyzer
from tree2mydoor_html_generator import Tree2mydoorHTMLGenerator

# Initialize
analyzer = Tree2mydoorProfitAnalyzer()
html_generator = Tree2mydoorHTMLGenerator()

# Analyze campaigns
analysis = analyzer.analyze_campaigns(
    'tree2mydoor',
    campaign_data,  # From Google Ads API
    date_range={'start_date': '2025-12-07', 'end_date': '2025-12-13'}
)

# Generate HTML report
html = html_generator.generate_html_report(
    analysis,
    'Tree2mydoor',
    (date_range['start_date'], date_range['end_date'])
)

# Save and open
output_path.write_text(html)
```

### Quick Test with Real Data

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/tools/report-generator
.venv/bin/python3 run_tree2mydoor_profit_report.py
```

## HTML Report Sections

### Standard Sections (from base analyzer)
1. **Header** - Client name, date range, conversion lag note
2. **Health Score Card** - Total spend, total profit, account POAS, conversions, issues
3. **Campaign Performance Breakdown** - All campaigns with metrics table
4. **Prioritised Recommendations** - P0/P1/P2 actions

### Profit-Specific Sections (NEW)
1. **Profit-Based Optimization Context**
   - ProfitMetrics explanation (conversions_value = PROFIT)
   - Tier A/B/C structure definitions
   - Key considerations (stock stability, seasonality, CPC inflation)

2. **Tier-Based Campaign Assessment**
   - Visual tier distribution bars
   - Campaigns grouped by POAS performance
   - Specific budget actions per tier

3. **Seasonality Context**
   - Peak/non-peak season identification
   - Season-specific recommendations
   - Strategic guidance for current period

## Example Output (Dec 7-13, 2025)

```
Health Score: 77/100
Total Spend: £2,323.76
Total Profit: £3,355.37 (conversions_value = PROFIT)
Account POAS: 1.44x (target: 1.60x)
Total Conversions: 176

TIER DISTRIBUTION:
  Tier A (≥1.80x): 2 campaigns ✅ Scale these
  Tier B (≥1.45x): 1 campaigns  ⚠️  Optimize
  Tier C (≥1.35x): 3 campaigns  ⚠️  Throttle
  Below Tier C: 3 campaigns     🚨 PAUSE/reduce

SEASONALITY:
  Season: Christmas Peak (December)
  Peak Season: YES 🎄

RECOMMENDATIONS:
  1. [P1] Low POAS Performance
  2. [P1] Account-Level POAS Below Target
  3. [P1] December Peak Season Optimization
```

## Key Insights Provided

### Campaign-Level Insights
- Which campaigns are Tier A/B/C/Below
- Specific budget actions per campaign with expected impact
- POAS gaps vs targets with percentage below
- Lost impression share opportunities

### Account-Level Insights
- Account POAS vs 1.60x target
- Profit opportunity from budget reallocation
- Product Hero label distribution analysis
- Feed quality and stock stability issues

### Strategic Insights
- Seasonal optimization opportunities
- Product Hero label-based budget shifts
- CPC inflation vs profit gain analysis
- Risk management (don't sacrifice POAS for volume)

## Profit-Focused Recommendations

### Example: Account-Level POAS Below Target

```
🎯 ACCOUNT-LEVEL PROFIT OPTIMIZATION REQUIRED

Current Account POAS: 1.44x
Target Account POAS: 1.60x
Gap: 0.16x (10% below target)

ROOT CAUSE ANALYSIS:
This account uses ProfitMetrics - conversions_value = PROFIT (not revenue).
Account-level POAS below 1.60x target indicates:

1. Too much budget on low-margin products (Villains/Zombies)
2. CPC inflation outpacing profit gains (noted in context)
3. Stock instability disrupting campaign learning
4. Insufficient budget on Heroes/Sidekicks

IMMEDIATE ACTIONS:

Budget Reallocation (Channable + Google Ads):
1. Tier A campaigns (≥1.80x): +20% budget
2. Tier B campaigns (1.45x-1.80x): Hold steady
3. Tier C campaigns (1.35x-1.45x): -30% budget
4. Below Tier C (<1.35x): Pause or -50% budget

Product Hero Review:
1. Export product labels from Channable
2. Calculate POAS by label (Heroes vs Sidekicks vs Villains vs Zombies)
3. Ensure Zombies are excluded from campaigns
4. Shift impressions to Heroes through bidding/budgets

Expected Impact:
- Account POAS increase: +0.15-0.25x within 14 days
- Profit increase: £372-£604 over 30 days
- Campaign learning improvement from stable feed
```

## Comparison: Generic vs Profit Analyzer

### Generic Analyzer Output
```
❌ "Campaign X has ROAS 1.44x"
   → Unclear if this is good/bad for profit margins

❌ "Increase budget on campaigns above 1.6x ROAS"
   → Ignores tier structure and product margins

❌ "Total Revenue: £3,355"
   → This is PROFIT, not revenue - misleading terminology

❌ Generic recommendations without Product Hero context
```

### Profit Analyzer Output
```
✅ "Campaign X has POAS 1.44x (Tier B - below Tier A threshold)"
   → Clear tier classification with profit understanding

✅ "Tier A campaigns (≥1.80x): Scale +20-30% budget"
   → Respects tier structure, specific actions

✅ "Total Profit: £3,355.37 (conversions_value = PROFIT)"
   → Correct terminology, explicit clarification

✅ "Review Product Hero labels - shift budget to Heroes/Sidekicks"
   → Client-specific optimization strategy
```

## Documentation Updates

**CONTEXT.md Updated:**
- Added explicit note that `conversions_value` = PROFIT
- Documented POAS terminology requirement
- Example: "£100 spend generating £160 profit = 160% POAS (not ROAS)"

## Next Steps

1. **Integrate into Weekly Report Skill**
   - Update `google-ads-weekly-report` skill to use Tree2mydoorProfitAnalyzer
   - Automatically generate profit-focused reports for Tree2mydoor

2. **Product Data Integration**
   - Pull product-level data from Google Ads API
   - Analyze performance by Product Hero labels
   - Add product-level recommendations section

3. **Historical Comparison**
   - Compare current POAS to previous weeks/months
   - Highlight POAS trends (improving/declining)
   - Show seasonal patterns year-over-year

4. **Automated Insights**
   - Detect POAS drops >10% week-over-week
   - Alert when campaigns drop below tier thresholds
   - Flag Hero products going out of stock

## Testing

✅ **Core Analyzer**: Tested with real Tree2mydoor data (Dec 7-13, 2025)
✅ **HTML Generator**: Profit sections rendering correctly
✅ **Tier Classification**: Correctly grouping campaigns
✅ **Seasonality Detection**: December identified as peak season
✅ **POAS Calculations**: All conversions_value treated as profit
✅ **Recommendations**: Comprehensive, actionable, profit-focused

## Files Created

1. **tree2mydoor_profit_analyzer.py** (600 lines)
   - Core profit-focused analysis logic
   - Tier classification
   - Seasonality detection
   - Product Hero guidance
   - Profit-specific recommendations

2. **tree2mydoor_html_generator.py** (300 lines)
   - Extends base HTML generator
   - Profit context section
   - Tier distribution visualization
   - Seasonality section
   - POAS terminology throughout

3. **run_tree2mydoor_profit_report.py** (370 lines)
   - Test script with real Tree2mydoor data
   - Data transformation (MCP format → analyzer format)
   - Report generation and browser display

4. **TREE2MYDOOR-PROFIT-ANALYZER.md** (this file)
   - Complete documentation
   - Usage examples
   - Key differentiators
   - Comparison to generic analyzer

## Success Metrics

✅ **Correctly identifies profit vs revenue** - All conversions_value treated as PROFIT
✅ **Respects tier structure** - 4-tier classification with specific actions
✅ **Product Hero integration** - Guidance on Heroes/Sidekicks/Villains/Zombies
✅ **Seasonality awareness** - December recognized as peak season
✅ **Client-specific considerations** - Gareth's needs (ADHD), stock stability, feed issues
✅ **Comprehensive reporting** - 30KB HTML with all profit-specific sections
✅ **Actionable recommendations** - Specific campaigns, budgets, expected impact

---

**This analyzer is now ready for production use with Tree2mydoor.**

**All future Tree2mydoor campaign analysis should use this profit-focused analyzer instead of the generic analyzer.**
