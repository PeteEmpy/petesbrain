---
name: csv-analyzer
description: Analyses CSV files with automated scripts OR flexible instructions. For Google Ads reports, uses specialised analyser with ROAS as %, British English, £ currency. For ad-hoc analysis, uses flexible instruction-based approach.
allowed-tools: Read, Write, Bash, Glob
---

# CSV Analyser Skill

## Two Approaches Available

### **Approach 1: Automated Scripts (RECOMMENDED for Google Ads)**
Fast, consistent, automated visualisations
- **Use for:** Google Ads exports, standard reports, repeatable analysis
- **Scripts:** `analyse.py` (general), `analyse_google_ads.py` (Google Ads specific)
- **Benefits:** Consistent results, automatic 4-chart generation, ROAS as %

### **Approach 2: Instruction-Based (RECOMMENDED for ad-hoc analysis)**
Flexible, customisable, Claude-driven analysis
- **Use for:** Exploratory analysis, custom metrics, unusual data formats
- **Instructions:** See `skill-instructions.md`
- **Benefits:** Flexible, adapts to any data type, custom insights

---

## ⚠️ CRITICAL BEHAVIOUR: NO QUESTIONS

**DO NOT ASK THE USER WHAT THEY WANT TO DO.**

**IMMEDIATELY:**
1. Detect if this is Google Ads data → Use `analyse_google_ads.py`
2. Otherwise → Use `analyse.py` for general analysis
3. Generate ALL visualisations automatically
4. Present complete results

**NO questions, NO options, NO waiting for user input.**

---

## Approach 1: Automated Scripts

### When to Use Scripts

✅ **Use scripts for:**
- Google Ads ad group reports
- Campaign performance CSVs
- Standard monthly/weekly reports
- Any Google Ads export

### How It Works

**Auto-detection:**
1. Script checks first 2 lines of CSV
2. If contains "report" + month name → Google Ads format
3. Automatically skips header rows
4. Applies Google Ads-specific cleaning

**Google Ads Cleaning:**
- Removes commas from numbers (1,234 → 1234)
- Handles '--' as zero (Google Ads null indicator)
- Cleans currency symbols (£, $)
- Separates enabled vs paused ad groups
- Calculates campaign-level aggregations

**Output:**
- Text analysis in terminal
- 4 PNG visualisations saved to current directory:
  1. `ad_groups_by_spend.png` - Top 15 by spend
  2. `campaign_performance.png` - 4-panel campaign metrics
  3. `status_distribution.png` - Enabled vs paused pie chart
  4. `cost_vs_conversions.png` - Performance scatter plot

### Using the Scripts

**From Claude Code:**
```python
# For any CSV
from analyse import summarise_csv
print(summarise_csv("/path/to/file.csv"))

# For Google Ads specifically
from analyse_google_ads import analyse_google_ads_csv
analyse_google_ads_csv("/path/to/ad_group_report.csv")
```

**From command line:**
```bash
# General analysis
python3 analyse.py /path/to/file.csv

# Google Ads analysis
python3 analyse_google_ads.py /path/to/ad_group_report.csv

# Specify output directory
python3 analyse_google_ads.py /path/to/file.csv /path/to/output/
```

### PetesBrain Standards (Built-in)

✅ **British English:** analyse, visualisation, summarise
✅ **ROAS as %:** 292% (not £2.92 or 2.92x)
✅ **Currency:** £ symbol
✅ **Enabled/Paused separation:** Accurate performance metrics

---

## Approach 2: Instruction-Based Analysis

### When to Use Instructions

✅ **Use instructions for:**
- Exploratory data analysis
- Non-standard CSV formats
- Custom metric calculations
- Flexible, ad-hoc analysis
- Data types other than Google Ads

### How It Works

Claude follows structured instructions in `skill-instructions.md`:
- Load and validate CSV
- Identify data type (Google Ads, e-commerce, financial, etc.)
- Calculate relevant metrics
- Generate custom insights
- Create recommendations

**See:** `skill-instructions.md` for complete instructions

---

## Quick Decision Guide

**User says:** "Analyse this Google Ads ad group report"
→ **Use:** `analyse_google_ads.py` (Approach 1)

**User says:** "Analyse this CSV"
→ **Check:** Is it Google Ads? → Use script. Otherwise → Use instructions.

**User says:** "What's the ROAS by campaign in this report?"
→ **Use:** `analyse_google_ads.py` (it calculates this automatically)

**User says:** "Find correlations between product price and CTR"
→ **Use:** Instruction-based (Approach 2) - custom analysis

---

## Files

- `skill.md` - This file (main skill definition)
- `skill-instructions.md` - Detailed instructions for Approach 2
- `analyse.py` - General CSV analyser script
- `analyse_google_ads.py` - Google Ads specific analyser
- `requirements.txt` - Python dependencies
- `metric-definitions.md` - Google Ads metrics explained
- `examples/` - Sample CSV files

---

## Setup

**First time:**
```bash
cd /Users/administrator/Documents/PetesBrain/.claude/skills/csv-analyzer
python3 -m pip install -r requirements.txt
```

**Test:**
```bash
# Test general analyser
python3 analyse.py examples/sample.csv

# Test Google Ads analyser (if you have an export)
python3 analyse_google_ads.py /path/to/your/ad_group_report.csv
```

---

## Output Examples

### Script Output (Approach 1)

```
============================================================
📊 GOOGLE ADS AD GROUP PERFORMANCE ANALYSIS
============================================================

📊 DATASET OVERVIEW
Total Ad Groups: 42
  • Enabled: 28 (66.7%)
  • Paused: 14 (33.3%)

💰 SPEND & VOLUME METRICS
Total Spend: £12,456.78
Total Conversions: 143.50
Total Conversion Value: £36,370.34

📈 EFFICIENCY METRICS
Average CPC: £1.23
Cost per Conversion: £86.82
ROAS: 292% (2.92x revenue per £1 spent)

🏆 TOP PERFORMING AD GROUPS (by Conversions)
  Brand | Exact Match
    Spend: £2,345.67 | Conv: 45.0 | ROAS: 450%

📊 VISUALISATIONS CREATED:
  ✓ ad_groups_by_spend.png
  ✓ campaign_performance.png
  ✓ status_distribution.png
  ✓ cost_vs_conversions.png
```

### Instruction-Based Output (Approach 2)

```
## Executive Summary
Account shows strong performance with 292% ROAS across 42 ad groups.
Brand campaigns outperforming shopping by 2.1x.

## Key Metrics
[Custom analysis based on specific request]

## Recommendations
1. Increase brand campaign budget by £500/day
2. Pause 5 underperforming ad groups (ROAS < 150%)
3. Review shopping feed for 12 products with declining performance
```

---

## Notes

- **Automated scripts are faster** for standard Google Ads analysis
- **Instructions are more flexible** for custom analysis
- **Both produce British English output** with ROAS as %
- **Scripts handle messy Google Ads data** automatically
- **Instructions allow deeper, customised insights**

**Default choice:** Use automated scripts for Google Ads, instructions for everything else.
