# Slide Footnotes Reference

**Date:** November 4, 2025
**Purpose:** Documentation of footnotes added to all October 2025 slides

## Overview

All 11 slides now include small, unobtrusive footnotes (7-8pt font, gray color, italic style) at the bottom explaining the data sources, criteria, and date ranges used. This helps clarify exactly what data is being shown and addresses questions about data accuracy.

## Footnote Details by Slide

### Slide 1: Core Hotel Properties - Metric Boxes
**Footnote Text:**
```
Data: Core hotel properties only (Devonshire Arms, Chatsworth Hotel, Bolton Abbey, Cavendish Hotel, The Peacock, Pilsley Inn, Beeley Inn, The Fell)
Excludes: Self-catering, Weddings, Lismore, The Hall, The Hide, Highwayman | Date range: October 1-31, 2025
```

**Purpose:** Clarifies that the metric boxes show ONLY core hotel properties, not the entire account. This explains why the revenue figure (£58,694) may differ from total account performance.

---

### Slide 2: Hotels - Individual Property Performance
**Footnote Text:**
```
Data: October 1-31, 2025 | Metrics: conversions_by_conversion_date
```

**Purpose:** States date range and conversion metric used.

---

### Slide 3: Performance Max Campaign Results
**Footnote Text:**
```
Data: October 1-31, 2025 | Metrics: conversions_by_conversion_date
```

**Purpose:** States date range and conversion metric used.

---

### Slide 4: Search Campaign Results
**Footnote Text:**
```
Data: October 1-31, 2025 | Metrics: conversions_by_conversion_date
```

**Purpose:** States date range and conversion metric used.

---

### Slide 5: Hotels - Overall Profitability
**Footnote Text:**
```
Data: October 1-31, 2025 | Combined PMax + Search ROAS by property
```

**Purpose:** Clarifies that ROAS shown is the combined performance of both PMax and Search campaigns for each property.

---

### Slide 6: Location Based Search Campaigns
**Footnote Text:**
```
Data: October 1-31, 2025 | Bolton Abbey & Chatsworth Escapes location-based campaigns | Metrics: conversions_by_conversion_date
```

**Purpose:** Identifies which campaigns are included (location-based campaigns only).

---

### Slide 7: Self Catering Campaign Performance
**Footnote Text:**
```
Data: October 1-31, 2025 | Ad groups from Chatsworth Escapes Self Catering and Bolton Abbey Escapes Self Catering campaigns
Includes all 7 active ad groups: Chatsworth Estate Cottages, Chatsworth Self Catering, Peak District Cottages, Shepherds Huts, Hunting Tower, Russian Cottage, Yorkshire Cottages
```

**Purpose:** Lists exactly which campaigns and ad groups are included, confirming all 7 ad groups are shown (including Russian Cottage which may be paused in future).

---

### Slide 8: The Hide / Highwayman
**Footnote Text:**
```
Data: October 1-31, 2025 | The Hide campaign (launched Oct 10) + Highwayman Arms campaign | Metrics: conversions_by_conversion_date
```

**Purpose:** Clarifies both campaigns are shown, notes The Hide's launch date, and states conversion metric.

**Note:** This slide also includes a yellow note box explaining the tracking investigation.

---

### Slide 8a: Hide & Highwayman Trends
**Footnote Text:**
```
Data: January-October 2025 (monthly) | Consolidated performance for The Hide + Highwayman Arms campaigns
Red dashed line marks The Hide launch (October 10, 2025) | Metrics: conversions_by_conversion_date
```

**Purpose:** Explains the date range (10 months), what campaigns are consolidated, and what the red vertical line indicates.

---

### Slide 9: Weddings
**Footnote Text:**
```
Data: October 1-31, 2025 | Chatsworth Weddings campaign | 8 ad groups (Luxury Wedding, Wedding, Getting Married, Wedding Venues, Countryside Wedding, Wedding Hotels, Wedding Packages, Weddings Yorkshire)
```

**Purpose:** Lists the campaign name and all 8 ad groups included.

---

### Slide 10: Lismore and The Hall
**Footnote Text:**
```
Data: October 1-31, 2025 | Lismore campaign (1 ad group) + The Hall campaign (2 ad groups: Search - The Hall, Search - Mansion Rental)
```

**Purpose:** Breaks down exactly how many ad groups are from each campaign and names them.

---

## Implementation Notes

### Typography
- **Font Size:** 7-8pt (varies by slide for readability)
- **Color:** #666666 (medium gray)
- **Style:** Italic
- **Position:** Bottom of each slide using `plt.figtext()` or `ax.text()`

### Design Philosophy
- Small and unobtrusive (per user request)
- Provides transparency about data sources
- Helps user verify data accuracy
- Makes slides self-documenting
- Answers "what's included?" questions

### Technical Implementation
All footnotes are added in the `generate_slide_images.py` script before the `plt.tight_layout()` call in each slide generation function.

## User Feedback

User specifically noted:
> "In all the previous iterations of these slides you've put at the bottom as a footnote the criteria that was used for the creation of the slide. This made it very understandable. Could you reintroduce that? It needs to be quite small and unobtrusive but it makes it easy for me to see what's actually been looked at because as an example on the KPI slide the revenue to me doesn't look correct."

The footnotes now address this concern by:
1. Being small and unobtrusive (7-8pt, gray, italic)
2. Explaining exactly what data is included/excluded
3. Providing date ranges and metric definitions
4. Making it easy to verify data accuracy

## Status

✅ Complete - All 11 slides regenerated with footnotes on November 4, 2025
