# NDA PMax Asset Replacement - Quality Improvements Summary

**Date**: 12 December 2025
**Time**: 16:24

---

## Overview

This document summarises the complete evolution of the NDA PMax asset replacement system from initial implementation to final quality-optimised state.

---

## Evolution Timeline

### Phase 1: Initial Implementation (Absolute Thresholds)
**Status**: Replaced with relative thresholds

**Original Criteria**:
- HEADLINE: 0 conversions AND cost ≥ £200
- LONG_HEADLINE: 0 conversions AND cost ≥ £30
- DESCRIPTION: 0 conversions AND cost ≥ £50
- Analysis period: 90 days (Sep 14 - Dec 12, 2025)

**Problem Identified**:
- High CTR + 0 conversions = landing page problem (shouldn't change text)
- Low CTR + 0 conversions = text problem (should change text)
- Absolute cost thresholds don't account for CTR performance

**Result**: 67 assets flagged

### Phase 2: Relative CTR Thresholds
**Status**: Implemented and optimised

**Updated Criteria**:
- CTR < 50% of asset group median (relative comparison)
- 0 conversions
- ≥1,000 impressions (~33/day over 30 days)
- Analysis period: 30 days (Nov 12 - Dec 12, 2025)

**Benefits**:
- Context-aware: Compares assets to their peers in same asset group
- Fair: High-intent campaigns aren't penalised for higher CTR standards
- Accurate: Identifies TRUE underperformers, not just low-volume assets
- Fresh data: 30 days ensures actionable, recent performance

**Result**: 12 assets flagged (more targeted, higher quality selections)

### Phase 3: Landing Page Context Integration
**Status**: Implemented

**Problem Identified**:
- Generating alternatives without knowing which landing page the asset sends users to
- Asset groups have different final URLs (landing pages)
- Alternatives must match the landing page messaging

**Solution Implemented**:
- Added `get_asset_group_urls()` function to query Google Ads API
- Modified `generate_batch()` to fetch and include landing page content
- Updated prompt to include landing page context
- Grouped generation by (landing_url, asset_type)

**Result**: All alternatives now contextually relevant to their destination pages

### Phase 4: Single-Sentence Quality Enforcement
**Status**: Implemented and verified

**Problem Identified**:
- Claude generating TWO sentences for long headlines/descriptions
- Example: "Study interior design online. Flexible learning with 0% finance." (TWO sentences)
- Should be: "Study accredited interior design diplomas online with flexible learning and 0% finance available" (ONE sentence)

**Solution Implemented**:

1. **Updated Prompt Instructions**:
   - Explicit "ONE CONTINUOUS SENTENCE - NO periods, NO two sentences"
   - Added GOOD/BAD examples
   - Increased target from 75-90 to 85-90 chars (use FULL 90)
   - Added guidance: "Use connecting words (with, that, for, from, and) to extend the sentence"

2. **Updated Validation**:
   - Increased min_chars from 60 to 75 for LONG_HEADLINE and DESCRIPTION
   - Added `check_single_sentence` validation
   - Rejects any text with periods in the middle (two sentences)

3. **Verified Results**:
   - All 4 descriptions are single sentences
   - All 4 descriptions use 87-90 characters (target: 85-90)
   - 0 two-sentence outputs

**Result**: Professional, scan-friendly copy that uses full character limits

---

## Final System Configuration

### Analysis Parameters
```python
START_DATE = '2025-11-12'  # Last 30 days
END_DATE = '2025-12-12'
MIN_IMPRESSIONS = 1000  # ~33/day over 30 days
RELATIVE_CTR_THRESHOLD = 0.5  # 50% of group median
```

### Quality Standards
```python
# For LONG_HEADLINE and DESCRIPTION
MIN_CHARS = 75  # Increased from 60
TARGET_CHARS = 85-90  # Use FULL 90 characters
check_single_sentence = True  # Reject two-sentence outputs
```

---

## Results Summary

### Assets Identified
- **Total assets queried**: 348 (197 HEADLINE, 75 LONG_HEADLINE, 76 DESCRIPTION)
- **Underperformers flagged**: 12 assets
  - 9 HEADLINES
  - 0 LONG_HEADLINES
  - 3 DESCRIPTIONS
- **Alternatives generated**: 11/12 assets (92%)
- **Dropdowns added**: 11 rows

### Quality Metrics

**Descriptions**:
- Total descriptions generated: 4
- ✅ Single sentences: 4/4 (100%)
- ✅ Using 85-90 chars: 4/4 (100%)
- Character range: 87-90 chars (avg: 88.2 chars)

**Headlines**:
- Total headlines generated: 70
- Character range: 20-27 chars (avg: 22.6 chars)
- Within 25-30 char range: 12/70 (17%)
- All within 20-30 char range: 70/70 (100%)

### Cost Efficiency
- Batch size: 5 texts per API call
- Total batches: 6 (grouped by landing page + type)
- Total API calls: 6
- Model: Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- Estimated cost: ~$0.62 for 11 asset texts
- Quality justification: Sonnet 4 required for high-quality alternatives

---

## Key Improvements Over Initial System

1. **Smarter Selection** - Relative thresholds identify true underperformers (12 vs 67 assets)
2. **Fresh Data** - 30 days vs 90 days ensures actionable, recent performance
3. **Context-Aware** - Landing page content included in all generations
4. **Professional Quality** - Single-sentence enforcement for scan-friendly copy
5. **Full Character Usage** - 85-90 chars for long headlines/descriptions (not 60-70)
6. **Statistical Validity** - 1,000 impressions = ~33/day ensures reliable CTR data

---

## Next Steps

1. **Review Google Sheet**: https://docs.google.com/spreadsheets/d/1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto
2. **Make Selections**: Choose alternatives from dropdowns (or "Keep" to preserve current text)
3. **Run Implementation**: Execute `implement-sheet-selections.py` to push changes to Google Ads
4. **Confirm Changes**: Review proposed changes and type "YES" to execute

---

## File Inventory

| File | Purpose | Status |
|------|---------|--------|
| `populate-by-asset-type.py` | Query underperformers, populate sheet | ✅ Updated with relative thresholds + 1,000 impressions |
| `batch-generate-all-alternatives.py` | Generate alternatives via Claude API | ✅ Updated with single-sentence enforcement + landing page context |
| `implement-sheet-selections.py` | Bridge sheet → Google Ads | ✅ Ready (no changes needed) |
| `final-alternatives-for-dropdowns.json` | Generated alternatives | ✅ Regenerated with quality improvements |
| `final-alternatives-for-dropdowns.json.backup` | Backup (pre-quality enforcement) | ✅ Preserved |
| `SYSTEM-STATE-VERIFICATION.md` | System state documentation | ✅ Updated with quality standards |
| `30-DAY-PERIOD-RATIONALE.md` | Analysis period rationale | ✅ Documented |
| `RELATIVE-THRESHOLD-UPDATE.md` | Relative threshold rationale | ✅ Documented |

---

## Technical Notes

**Google Ads API Version**: v22
**Python Environment**: `/Users/administrator/Documents/PetesBrain.nosync/venv/bin/python3`
**Customer ID**: 1994728449
**Spreadsheet ID**: 1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto

**Claude API**:
- Model: `claude-sonnet-4-20250514`
- Batch size: 5 texts per call
- Rate limiting: 2 seconds between calls
- Quality validation: Single-sentence enforcement + character limits

---

## Lessons Learned

1. **Relative thresholds are superior** - Comparing assets to their peers (not absolute benchmarks) provides context-aware selection
2. **Fresh data matters** - 30 days beats 90 days for actionable insights (avoids seasonal drift)
3. **Statistical thresholds are flexible** - 2,000 impressions too restrictive, 1,000 captures 33% more underperformers
4. **Landing page context is critical** - Alternatives must match the destination page messaging
5. **Explicit prompt instructions work** - GOOD/BAD examples + validation enforcement = quality output
6. **Claude quality worth the cost** - Sonnet 4 ($0.62 for 11 texts) delivers professional-quality alternatives

---

## System Status

**Ready for implementation** ✅

- 12 underperforming assets identified
- 11 have alternatives with dropdowns
- All descriptions are single sentences using 87-90 characters
- All alternatives include landing page context
- Google Sheet populated and ready for review
- Implementation script ready for execution

**No changes made to Google Ads yet** - awaiting your selections in the Google Sheet.
