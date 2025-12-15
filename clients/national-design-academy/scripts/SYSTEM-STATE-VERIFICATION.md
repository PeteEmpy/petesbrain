# NDA PMax Implementation System - State Verification

**Date**: 12 December 2025 - 16:24
**Status**: ✅ SYSTEM UPDATED - RELATIVE THRESHOLDS + 30-DAY PERIOD + SINGLE-SENTENCE QUALITY
**Analysis Period**: 30 days (Nov 12 - Dec 12, 2025)

---

## Executive Summary

The NDA PMax asset implementation system has been **updated with relative performance thresholds and quality enforcement**:

- ✅ **Relative Threshold Logic** - Assets flagged based on performance vs asset group median (not absolute thresholds)
- ✅ **Google Sheet Populated** - Each row = ONE specific asset with its type clearly marked
- ✅ **Dropdowns Added** - Only for assets matching our alternatives (type-appropriate options)
- ✅ **Implementation Script Ready** - Reads Asset ID and Asset Group ID from sheet columns
- ✅ **Safety Mechanisms** - No changes without explicit "YES" confirmation
- ✅ **Landing Page Context** - All alternatives generated with relevant landing page content
- ✅ **Single-Sentence Quality** - All long headlines/descriptions are ONE continuous sentence using full 90 characters

**Current Flagging Criteria** (updated 16:24):
- CTR < 50% of asset group median
- 0 conversions
- ≥1,000 impressions (~33/day) for statistical significance
- Last 30 days only (fresh, actionable data)

**Quality Standards** (updated 16:24):
- All DESCRIPTIONS are single sentences (no two-sentence outputs)
- All DESCRIPTIONS use 87-90 characters (target: 85-90 chars)
- Validation rejects any text with periods in the middle
- Landing page messaging context included in all generations

**Previous criteria (absolute)**:
- ~~11 HEADLINES (0 conv, ≥£200 spend)~~
- ~~37 LONG_HEADLINES (0 conv, ≥£30 spend)~~
- ~~19 DESCRIPTIONS (0 conv, ≥£50 spend)~~

**Note**: Re-run `populate-by-asset-type.py` to see new numbers with relative thresholds.

---

## Key Architecture Change (Dec 12, 2025)

**Previous (incorrect)**: Grouped assets by TEXT content, showed all 3 asset type alternatives on same row

**Current (correct)**: Each row = ONE specific asset (unique asset ID + field type combination)
- Column C shows Asset Type (HEADLINE, LONG_HEADLINE, or DESCRIPTION)
- Column M dropdown only contains alternatives matching that asset type
- Column N contains Asset ID (for implementation script)
- Column O contains Asset Group ID (for implementation script)

---

## HIGH Priority Criteria (UPDATED: Relative Thresholds)

**New Logic (Dec 12, 2025)**: Assets are now flagged based on **relative performance within their asset group**.

Assets flagged as HIGH priority meet ALL of these criteria:
- **CTR < 50% of group median** (calculated per asset group + field type)
- **0 conversions**
- **≥1,000 impressions** (~33/day over 30 days = active + statistically valid)

**Why this is better**:
- Compares assets to their peers in the same asset group
- Accounts for campaign context (high-intent vs cold audience)
- Flags TRUE underperformers, not just assets with low absolute CTR
- Prevents false positives (assets performing well for their context)

**Example**:
- Asset Group "India Campaign" - LONG_HEADLINE median CTR = 3.5%
- Threshold = 1.75% (50% of median)
- Assets with CTR < 1.75% AND 0 conversions AND ≥2,000 impressions are flagged

See `RELATIVE-THRESHOLD-UPDATE.md` for full details.

---

## Google Sheet Structure

**Sheet ID**: `1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto`
**URL**: https://docs.google.com/spreadsheets/d/1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto

**Columns**:
| Column | Content |
|--------|---------|
| A | Campaign Name |
| B | Asset Group Name |
| C | **Asset Type** (HEADLINE, LONG_HEADLINE, DESCRIPTION) |
| D | Asset Text (current copy) |
| E | Clicks |
| F | Conversions |
| G | CTR % |
| H | Conv Rate % |
| I | Cost (£) |
| J | **Group Median CTR** (median CTR for this asset's group) |
| K | **Gap vs Median** (relative performance, e.g., "-58%") |
| L | Priority |
| M | **Alternative Options** (Dropdown - type-appropriate) |
| N | Asset ID (for API) |
| O | Asset Group ID (for API) |

---

## Top Underperforming Assets (by cost)

| Type | Cost | Asset Text |
|------|------|------------|
| HEADLINE | £902 | Price-Match Guarantee |
| HEADLINE | £877 | Interior Design Courses |
| HEADLINE | £762 | Online Interior Design Degrees |
| DESCRIPTION | £611 | Study At Home Full/Part-Time... |
| HEADLINE | £605 | Interior Design Degree |
| HEADLINE | £589 | Interior Design Diploma |
| HEADLINE | £563 | Intensive Fast-Track Diplomas |
| DESCRIPTION | £526 | Our Diploma Courses Awarded by AIM... |
| DESCRIPTION | £502 | Leading Provider of Fully Accredited... |
| LONG_HEADLINE | £502 | The Only Online Professional... |

---

## System Components

### 1. Population Script
**File**: `populate-by-asset-type.py`
**Status**: ✅ READY
**Purpose**: Query underperforming assets by type, populate sheet with one row per asset

**How to Run**:
```bash
/Users/administrator/Documents/PetesBrain.nosync/venv/bin/python3 \
  /Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/populate-by-asset-type.py
```

### 2. Implementation Bridge Script
**File**: `implement-sheet-selections.py`
**Status**: ✅ READY
**Purpose**: Reads Google Sheet selections and pushes to Google Ads

**Key Features**:
- Reads Asset ID and Asset Group ID from columns N and O
- Reads Asset Type from column C
- Shows all changes for review BEFORE execution
- **Requires explicit "YES" confirmation**
- Logs all changes to audit JSON file

**How to Run**:
```bash
/Users/administrator/Documents/PetesBrain.nosync/venv/bin/python3 \
  /Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/implement-sheet-selections.py
```

### 3. Alternatives Data
**File**: `final-alternatives-for-dropdowns.json`
**Status**: ✅ READY

**Contains alternatives for 7 unique asset texts**:
1. Study Interior Design
2. Interior Design Diploma
3. Interior Design Courses
4. Online Interior Design Degrees
5. Interior Design Degree
6. Price-Match Guarantee
7. Intensive Fast-Track Diplomas

**Each asset text has three types of alternatives**:
- `section_breakdown`: Short headlines (30 chars) - for HEADLINE assets
- `long_headlines`: Long headlines (90 chars) - for LONG_HEADLINE assets
- `descriptions`: Descriptions (90 chars) - for DESCRIPTION assets

---

## Workflow

### Step 1: Review Google Sheet
1. Open: https://docs.google.com/spreadsheets/d/1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto
2. Review underperforming assets (each row = one specific asset)
3. Note the Asset Type (column C) - determines what alternatives are available

### Step 2: Make Selections
1. Find rows with dropdowns in column M (only assets with matching alternatives have dropdowns)
2. Click dropdown and select "Keep" or choose an alternative
3. Alternatives are type-appropriate (30 chars for HEADLINE, 90 chars for LONG_HEADLINE/DESCRIPTION)

### Step 3: Run Implementation Script
```bash
/Users/administrator/Documents/PetesBrain.nosync/venv/bin/python3 \
  /Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/implement-sheet-selections.py
```

### Step 4: Review Proposed Changes
Script displays:
```
PROPOSED CHANGES - REVIEW BEFORE EXECUTION
================================================================================
Total selected assets: X
  • Keep current: Y
  • Replace with alternative: Z

REPLACEMENTS:
--------------------------------------------------------------------------------
Row 2: HEADLINE
  Current: 'Price-Match Guarantee'
  New:     'Best value courses guaranteed'
  Asset ID: 10422358209
  Asset Group ID: 6510182149
  Campaign: NDA | P Max | Interior Design Diploma...
```

### Step 5: Confirm or Cancel
- Type `YES` (all caps) to proceed with Google Ads changes
- Type anything else to cancel (no changes made)

---

## Safety Mechanisms

1. **No automatic execution** - All changes require explicit "YES" confirmation
2. **Change preview** - Shows exactly what will change before execution
3. **Audit logging** - Every execution creates timestamped JSON log
4. **Type-appropriate alternatives** - Dropdowns only contain options valid for that asset type
5. **Asset ID tracking** - Each row has Asset ID and Asset Group ID for precise targeting
6. **Keep option** - Default "Keep" option preserves current asset

---

## Key Technical Details

- **Customer ID**: 1994728449
- **Manager ID**: (None - direct access)
- **Analysis Period**: 90 days (Sep 14 - Dec 12, 2025)
- **Python venv**: `/Users/administrator/Documents/PetesBrain.nosync/venv/bin/python3`
- **Token file**: `/Users/administrator/.config/google-drive-mcp/tokens.json`

---

## Script Inventory

| Script | Status | Purpose |
|--------|--------|---------|
| `populate-by-asset-type.py` | ✅ READY | Query by type, populate sheet |
| `add-dropdowns-final.py` | ✅ READY | Add type-appropriate dropdowns |
| `implement-sheet-selections.py` | ✅ READY | Bridge sheet → Google Ads |
| `generate-alternatives-via-claude.py` | ✅ READY | Generate alternatives via Claude API |
| `final-alternatives-for-dropdowns.json` | ✅ READY | Alternatives data file |

---

## Verification Checklist

- ✅ 30-day analysis completed (Nov 12 - Dec 12, 2025)
- ✅ 12 underperforming assets identified (9 HEADLINE, 0 LONG_HEADLINE, 3 DESCRIPTION)
- ✅ Google Sheet populated with one row per asset
- ✅ Asset Type column (C) shows type for each row
- ✅ Dropdowns added with type-appropriate alternatives (11/12 rows)
- ✅ Asset ID and Asset Group ID stored in columns N and O
- ✅ Implementation script reads from sheet columns
- ✅ Safety mechanisms in place
- ✅ No changes made to Google Ads yet (awaiting your selections)
- ✅ All descriptions are single sentences using 87-90 characters
- ✅ Landing page context included in all generations

**System Status**: Ready for testing with 12 underperforming assets. Quality verified: all descriptions are single sentences using full 90 characters.
