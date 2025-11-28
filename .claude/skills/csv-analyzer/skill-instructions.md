# CSV Analyzer Skill

## Description

Automatically analyzes CSV files containing Google Ads performance data, client reports, or any tabular data. Provides instant insights, identifies trends, spots anomalies, and generates actionable recommendations.

## Trigger Patterns

Activate when the user:
- References a CSV file or mentions analyzing CSV data
- Uploads or provides a path to a CSV file
- Asks for analysis of exported Google Ads reports
- Requests trend analysis or performance comparisons
- Mentions product-level, campaign-level, or keyword-level data in CSV format

## Instructions

When this skill is triggered:

1. **Load and validate the CSV**:
   - Read the file using appropriate encoding
   - Identify column structure
   - Detect data types (dates, numbers, strings)
   - Check for missing values or malformed data

2. **Identify the data type**:
   - Google Ads campaign report
   - Product/Shopping performance data
   - Keyword performance data
   - Search terms report
   - Custom export or analytics data

3. **Perform automatic analysis**:

### For Google Ads Performance Data

#### Campaign-Level Analysis
- **Summary metrics**: Total impressions, clicks, spend, conversions, ROAS, CTR, CPC
- **Top performers**: Best campaigns by ROAS, conversion volume, or spend
- **Bottom performers**: Worst campaigns requiring attention
- **Trends**: Week-over-week or period-over-period changes
- **Anomalies**: Unusual spikes or drops in key metrics
- **Budget efficiency**: Spend distribution and pacing issues

#### Product-Level Analysis (Shopping)
- **Product performance**: Top/bottom products by ROAS
- **Inventory issues**: Products with declining performance (may indicate stock issues)
- **Opportunity products**: High impressions but low clicks (creative issues)
- **Wasted spend**: Products with clicks but no conversions
- **Price competitiveness**: Average CPC vs conversion rate patterns

#### Keyword Analysis
- **Performance tiers**: Group keywords by performance (winners, break-even, losers)
- **Search volume trends**: Impression patterns over time
- **Quality score indicators**: CTR as proxy for quality
- **Negative keyword candidates**: High spend, zero conversions
- **Bid optimization opportunities**: Under/over-performing relative to bid

4. **Calculate derived metrics** (if not present):
   ```
   CTR = (Clicks / Impressions) * 100
   CPC = Cost / Clicks
   CVR = Conversions / Clicks * 100
   CPA = Cost / Conversions
   ROAS = Conversion Value / Cost
   ```

5. **Identify actionable insights**:
   - Flag metrics outside normal ranges (use ±15% threshold)
   - Highlight budget allocation inefficiencies
   - Spot opportunity areas (high IS loss, strong ROAS but limited budget)
   - Identify underperformers to pause or adjust

6. **Generate visualization suggestions**:
   - Time series for trends
   - Distribution charts for performance spread
   - Top/bottom lists for quick wins
   - Correlation matrices for metric relationships

7. **Create recommendations**:
   - 3-5 prioritized action items
   - Specific, quantified recommendations (e.g., "Increase Budget Brand Campaign by $500/day")
   - Root cause hypotheses for performance issues

8. **Format output**:
   - Executive summary (2-3 sentences)
   - Key metrics table
   - Top 10 performers and bottom 10 underperformers
   - Trend analysis with period comparisons
   - Actionable recommendations list

## Analysis Templates

### Template 1: Campaign Performance Review
```
## Executive Summary
[2-3 sentence overview of account health]

## Key Metrics (Total)
| Metric | Value | Change vs Previous |
|--------|-------|-------------------|
| Spend | $X | ±Y% |
| Conversions | N | ±Y% |
| ROAS | X.XX | ±Y% |

## Top Performers (by ROAS)
[Table of top 10 campaigns]

## Underperformers (require attention)
[Table of bottom 10 or threshold-based flagging]

## Notable Changes
- [Campaign/product] saw [metric] [increase/decrease] by X%
- [Specific anomaly or trend]

## Recommendations
1. [Specific action with expected impact]
2. [Specific action with expected impact]
3. [Specific action with expected impact]
```

### Template 2: Product-Level Deep Dive
```
## Product Performance Summary
Total products: N
Products with sales: N (X%)
Average product ROAS: X.XX

## Best Performers (Top 20)
[Table with product ID, title, impressions, clicks, spend, conversions, ROAS]

## Products Requiring Attention

### High Spend, Low ROAS
[Products to pause or investigate]

### High Impressions, Low Clicks
[Products with creative/image issues]

### Declining Performance
[Products with >15% WoW drops]

## Optimization Opportunities
[Specific product-level actions]
```

### Template 3: Search Terms Analysis
```
## Search Terms Overview
Total queries: N
Queries with conversions: N (X%)
Average query CTR: X.X%

## Negative Keyword Candidates
[Search terms with high cost, zero conversions]

## High-Potential Queries
[Strong performance, consider exact match keywords]

## Low CTR Queries
[Poor relevance, review match types]
```

## Thresholds and Benchmarks

Use these for flagging:
- **Excellent ROAS**: > 4.0
- **Good ROAS**: 2.0 - 4.0
- **Break-even ROAS**: 1.5 - 2.0
- **Poor ROAS**: < 1.5
- **High CTR**: > 3% (Shopping), > 5% (Search)
- **Low CTR**: < 0.5% (Shopping), < 1% (Search)
- **Significant change**: ±15% or more
- **Critical change**: ±30% or more

## Output Format

Always provide:
1. ✅ Executive summary
2. ✅ Data quality notes (missing data, date range, etc.)
3. ✅ Key metrics table
4. ✅ Performance distributions
5. ✅ Top/bottom performers
6. ✅ Trend analysis (if time-series data present)
7. ✅ Actionable recommendations (3-5 items)
8. ✅ Follow-up questions or deeper analysis suggestions

## Special Cases

### Missing Data
- Note gaps in data
- Suggest potential causes (timezone, conversion lag, export issues)
- Proceed with analysis on available data

### Single-Point Data (no time series)
- Focus on performance distribution
- Benchmark against account averages
- Skip trend analysis

### Mixed Campaign Types
- Separate analysis by campaign type (Shopping, Search, Performance Max)
- Note different benchmarks for each type

## Resources

- [Analysis Framework](analysis-framework.md) - Detailed methodology
- [Metric Definitions](metric-definitions.md) - Google Ads metrics explained
- [ROK Analysis Prompts](../../../roksys/knowledge-base/rok-methodologies/google-ads-analysis-prompts.md)

## Notes

- Handle large CSVs efficiently (>10k rows)
- Support common date formats (YYYY-MM-DD, MM/DD/YYYY, etc.)
- Convert currency strings ($X,XXX.XX) to numeric values
- Preserve precision for ROAS and conversion metrics
- Use pandas or similar for robust CSV handling

