# Tree2MyDoor PMAX Search Trends Analyzer

**Purpose**: Weekly analysis of trending PMAX search categories to identify high-quality expansion opportunities for Search campaigns.

**Run Schedule**: Every Friday at 10:00 AM

**Data Source**: Google Sheet (auto-updated weekly by Product Hero/Google Ads)
https://docs.google.com/spreadsheets/d/14ACzJ8TfJd_8wPreCryno_EkWD6M1RBX2jbXNQgdb84/

---

## What This Agent Does

1. **Pulls trending PMAX search category data** from the spreadsheet
2. **Stores historical snapshots** to track long-term trends (not just week-to-week)
3. **Applies quality filters** to identify genuinely notable opportunities:
   - Minimum impression threshold (100+)
   - Significant trend changes (+200% growth OR -60% decline)
   - High commercial intent (birthday, anniversary, memorial, gifts)
   - New opportunities (not already flagged in recent weeks)
4. **Analyzes conversion data** via GAQL for flagged categories
5. **Outputs to daily briefing** ONLY if truly notable

---

## Quality Filters (HIGH BAR)

**Only flag opportunities that meet ALL criteria:**

✅ **Volume Threshold**: 100+ impressions in last 7 days
✅ **Trend Significance**:
   - Growth: +200% or higher
   - OR Decline: -60% or worse (on previously high-performing categories)
✅ **Commercial Intent**: Contains gift/birthday/anniversary/memorial/sympathy keywords
✅ **Novelty**: Not flagged in last 4 weeks (avoid repetitive alerts)
✅ **Conversion Potential**: If GAQL data available, prefer categories with proven conversion history

**Result**: Only 2-3 truly notable opportunities per month (not weekly noise)

---

## Output Format

Findings written to: `data/cache/tree2mydoor-search-trends.json`

**Schema**:
```json
{
  "last_updated": "2025-11-20T10:00:00",
  "flagged_opportunities": [
    {
      "category": "60th birthday rose",
      "impressions_last_7d": 291,
      "impressions_prior_7d": 65,
      "relative_change_pct": 347.7,
      "conversions_last_30d": 12,
      "conv_rate": 4.1,
      "why_notable": "347% growth surge + high conversion rate (4.1%) + commercial intent",
      "recommended_action": "Create dedicated Search ad group for '60th Birthday Rose' with Fab at 60 product",
      "first_flagged": "2025-11-15"
    }
  ],
  "historical_snapshots": []
}
```

---

## Integration with Daily Briefing

If opportunities flagged, agent creates: `briefing/tree2mydoor-search-opportunity-YYYY-MM-DD.md`

Daily intel report picks this up and includes in briefing under "Client Opportunities" section.

**Presentation style**: Brief, actionable, data-driven
- "New PMAX search trend: '60th birthday rose' up 348% (291 impr, 12 conv last 30d). Consider dedicated Search ad group."

---

## Historical Trend Tracking

Agent maintains 12-week rolling history to identify:
- **Seasonal patterns** (e.g., "memorial rose" peaks in November)
- **Sustained growth** (not just one-week spikes)
- **Category lifecycle** (emerging → growing → mature → declining)

**Long-term value**: Industry trend insights for strategic planning

---

## Technical Notes

- Uses Google Drive MCP server to fetch spreadsheet
- Uses Google Ads MCP server for GAQL conversion analysis
- Stores data in `agents/tree2mydoor-search-trends/data/` for historical tracking
- Runs via LaunchAgent: `com.petesbrain.tree2mydoor-search-trends.plist`

---

## Success Metrics

**Quality over quantity**:
- ✅ 2-3 truly notable opportunities per month
- ❌ NOT 10+ low-quality alerts every week

**Actionability**:
- Each flagged opportunity should be worth investigating
- Clear recommended action (create ad group, analyze further, etc.)
- Supporting data (impressions, conversions, trend %)

---

## Example Output (What Gets Flagged)

**✅ WOULD FLAG:**
- "60th birthday rose" +348% (291 impr) - new surge, high intent, product match
- "housewarming gifts" -98% (7 impr, was 335) - major collapse worth investigating

**❌ WOULD NOT FLAG:**
- "rose bush" -56% (102 impr, was 231) - below -60% threshold
- "plants" +50% (20 impr) - below 100 impression minimum
- "60th birthday rose" +10% week 2 - already flagged week 1, no new info

---

**Created**: 2025-11-20
**Owner**: Peter Empson
**Client**: Tree2MyDoor
