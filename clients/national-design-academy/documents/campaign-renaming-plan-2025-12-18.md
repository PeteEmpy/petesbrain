# National Design Academy - Campaign Renaming Plan
## Regional Grouping Implementation

**Date**: 18 December 2025  
**Customer ID**: 1994728449  
**Purpose**: Add regional grouping identifiers to campaign names based on location targeting

---

## Regional Groupings Defined

| Regional Code | Countries Included |
|---------------|-------------------|
| **UAE** | United Arab Emirates, Abu Dhabi |
| **Europe** | Austria, France, Netherlands, Germany, Sweden, Belgium, Italy, Spain, Switzerland, Cyprus, Denmark, Norway, Ireland, Poland, Romania, Hungary, Latvia, Serbia |
| **GCC** | Oman, Saudi Arabia, Bahrain, Kuwait, Qatar |
| **US/Canada** | United States, Canada |
| **India** | India |
| **ROTW** | Rest of World (all other countries) |

---

## Current Campaign Analysis

**Total Campaigns**: 187  
**Campaigns With Location Data**: 182  
**ENABLED Campaigns Requiring Update**: 40  

### Current Regional Distribution (ENABLED Only):

| Region | Count | Notes |
|--------|-------|-------|
| UK (Pure) | 11 | Currently labeled "UK" - needs change to "Europe" |
| UAE (Pure) | 5 | Correctly labeled "UAE" - no change needed |
| GCC | 4 | Correctly labeled "OM/SA/BH/KW" - standardize to "GCC" |
| India | 3 | Correctly labeled "IN" or "India" - standardize to "India" |
| US/Canada | 4 | Labeled "US/CA" - standardize to "US/Canada" |
| Mixed Regions | 7 | Need careful review - may target multiple regions |
| ROTW | 6 | Currently labeled various ways - standardize to "ROTW" |

---

## Naming Convention Standard

### Proposed Format:

```
NDA | [REGION] | [TYPE] | [PRODUCT] | [MODIFIERS]
```

### Regional Identifiers:

- **UAE** - United Arab Emirates only
- **Europe** - European countries (including UK + Ireland)
- **GCC** - Gulf Cooperation Council (Oman/Saudi/Bahrain/Kuwait/Qatar)
- **India** - India only
- **US/Canada** - United States + Canada
- **ROTW** - Rest of World (multi-country)

---

## Campaign Renaming Examples (ENABLED Campaigns)

### 1. UK Campaigns → Europe

**Current Issue**: Campaigns targeting "United Kingdom" are labeled "UK" but UK is part of Europe regional grouping.

| Current Name | Proposed New Name | Reason |
|--------------|-------------------|--------|
| `NDA \| UK \| Search \| Brand 100 New Customer 1/8 No Target` | `NDA \| Europe \| Search \| Brand 100 New Customer 1/8 No Target` | Targets United Kingdom (part of Europe region) |
| `NDA \| UK \| Search \| Interior Design Diploma 140 Ai Max 5/8` | `NDA \| Europe \| Search \| Interior Design Diploma 140 Ai Max 5/8` | Targets United Kingdom (part of Europe region) |
| `NDA \| UK \| Search \| Curtain Making Courses No Target` | `NDA \| Europe \| Search \| Curtain Making Courses No Target` | Targets United Kingdom (part of Europe region) |
| `NDA \| UK \| Search \| Landscape Design Diplomas No Target` | `NDA \| Europe \| Search \| Landscape Design Diplomas No Target` | Targets United Kingdom (part of Europe region) |
| `NDA \| UK \| Search \| Retail Design Degree No Target` | `NDA \| Europe \| Search \| Retail Design Degree No Target` | Targets United Kingdom (part of Europe region) |
| `NDA \| P Max \| Interior Design Degree - UK 100 17/3 No Target 30/4` | `NDA \| P Max \| Interior Design Degree - Europe 100 17/3 No Target 30/4` | Targets United Kingdom (part of Europe region) |
| `NDA \| P Max \| Interior Design Diploma - UK 100 Remarketing 17/3 No Target 30/4 New Customers 1/8` | `NDA \| P Max \| Interior Design Diploma - Europe 100 Remarketing 17/3 No Target 30/4 New Customers 1/8` | Targets United Kingdom (part of Europe region) |
| `NDA \| Search \| Interior Design Degree- UK 120 No Target 24/4` | `NDA \| Search \| Interior Design Degree - Europe 120 No Target 24/4` | Targets United Kingdom (part of Europe region) |

**Note**: "UK" in campaign names will change to "Europe" to reflect the regional grouping.

---

### 2. GCC Campaigns → Standardize

**Current Issue**: GCC campaigns use verbose country codes (OM/SA/BH/KW) instead of regional identifier.

| Current Name | Proposed New Name | Reason |
|--------------|-------------------|--------|
| `NDA \| OM/SA/BH/KW \| Search \| Interior Design Diploma No Target` | `NDA \| GCC \| Search \| Interior Design Diploma No Target` | Simplify to regional grouping "GCC" |
| `NDA \| OM/SA/UAE \| Search \| Landscape Design No Target` | `NDA \| GCC+UAE \| Search \| Landscape Design No Target` | Mixed GCC + UAE targeting |
| `NDA \| P Max Reboot \| Interior Design Diploma - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target 24/4` | `NDA \| P Max Reboot \| Interior Design Diploma - GCC 135 Split 11/3 No Target 24/4` | Full GCC targeting, simplify to "GCC" |
| `NDA \| P Max \| Interior Design Degree - Oman/Saudi/Bahrain/Kuwait/Qatar 135 Split 11/3 No Target` | `NDA \| P Max \| Interior Design Degree - GCC 135 Split 11/3 No Target` | Full GCC targeting, simplify to "GCC" |
| `NDA \| Search \| Interior Design Degree - Oman/Saudi/Bahrain/Kuwait 175 Split 11/3 No Target` | `NDA \| Search \| Interior Design Degree - GCC 175 Split 11/3 No Target` | GCC (minus Qatar), still use "GCC" for simplicity |

---

### 3. India Campaigns → Standardize

**Current Issue**: Inconsistent India naming ("IN" vs "India").

| Current Name | Proposed New Name | Reason |
|--------------|-------------------|--------|
| `NDA \| IN \| Search \| Interior Design Degree No Target` | `NDA \| India \| Search \| Interior Design Degree No Target` | Standardize to "India" (more readable) |
| `NDA \| P Max \| Interior Design - India 135 29/11 No Target 10/9` | `NDA \| P Max \| Interior Design - India 135 29/11 No Target 10/9` | Already correct |
| `NDA \| Search \| Interior Design Diploma - India Ai Max 19/9` | `NDA \| Search \| Interior Design Diploma - India Ai Max 19/9` | Already correct |

---

### 4. US/Canada Campaigns → Standardize

**Current Issue**: Inconsistent US/Canada naming ("US/CA" vs "USA/Canada").

| Current Name | Proposed New Name | Reason |
|--------------|-------------------|--------|
| `NDA \| US/CA \| Search \| Interior Design Degree 250 No Target 15/9` | `NDA \| US/Canada \| Search \| Interior Design Degree 250 No Target 15/9` | Standardize to "US/Canada" |
| `NDA \| P Max \| Interior Design Degree - USA/Canada 250 Split 11/3` | `NDA \| P Max \| Interior Design Degree - US/Canada 250 Split 11/3` | Standardize to "US/Canada" |
| `NDA \| P Max \| Interior Design Diploma - USA/Canada 250 Split 11/3 No Target 29/5` | `NDA \| P Max \| Interior Design Diploma - US/Canada 250 Split 11/3 No Target 29/5` | Standardize to "US/Canada" |
| `NDA \| Search \| Interior Design Diploma - USA/ Canada 250 Split 11/3` | `NDA \| Search \| Interior Design Diploma - US/Canada 250 Split 11/3` | Standardize to "US/Canada" (fix spacing) |

---

### 5. ROTW Campaigns → Standardize

**Current Issue**: Multi-country campaigns need "ROTW" identifier.

| Current Name | Proposed New Name | Reason |
|--------------|-------------------|--------|
| `NDA \| P Max Reboot \| Interior Design Diploma - ROTW 200 13/1 No target 28/5` | `NDA \| ROTW \| P Max Reboot \| Interior Design Diploma 200 13/1 No target 28/5` | Move ROTW to region position |
| `NDA \| P Max \| Interior Design Degree - ROTW 200 13/1 No Target 23/9` | `NDA \| ROTW \| P Max \| Interior Design Degree 200 13/1 No Target 23/9` | Move ROTW to region position |
| `NDA \| AT/FR/NL/MA/DE/SW \| Search \| Interior Design Diploma 250 No Target 22/9` | `NDA \| Europe \| Search \| Interior Design Diploma 250 No Target 22/9` | European countries = Europe region |
| `NDA \| AT/FR/NL/MA/DE/SW \| Search \| Landscape Design Diplomas No Target` | `NDA \| Europe \| Search \| Landscape Design Diplomas No Target` | European countries = Europe region |
| `NDA \| EUR \| Search \| Landscape Design Courses 65` | `NDA \| Europe \| Search \| Landscape Design Courses 65` | Standardize "EUR" to "Europe" |
| `NDA \| BH/CY/KW \| Search \| Interior Design Degree No Target` | `NDA \| ROTW \| Search \| Interior Design Degree No Target` | Mixed countries (Bahrain/Cyprus/Kuwait/Qatar/Singapore) = ROTW |
| `NDA \| BH/IN/CYSI \| Search \| Landscape Design Course No Target` | `NDA \| ROTW \| Search \| Landscape Design Course No Target` | Mixed countries (11 countries) = ROTW |
| `NDA \| Low Intl \| Search \| Curtain Making Course No Target` | `NDA \| ROTW \| Search \| Curtain Making Course No Target` | "Low Intl" is 11 mixed countries = ROTW |
| `NDA \| Low Intl \| Search \| Retail Design Degree No Target` | `NDA \| ROTW \| Search \| Retail Design Degree No Target` | "Low Intl" is 11 mixed countries = ROTW |
| `NDA \| Search \| Interior Design Degree - Austria/France/Holland/Malta/Germany/Sweden Split 12/3 No Target 24/4` | `NDA \| Europe \| Search \| Interior Design Degree Split 12/3 No Target 24/4` | European countries = Europe region |
| `NDA \| Search \| Interior Design Diploma - Bahrain/Cyprus/Kuwait+ 135 Split 11/3` | `NDA \| ROTW \| Search \| Interior Design Diploma 135 Split 11/3` | Mixed countries = ROTW |

---

### 6. UAE Campaigns → No Change Needed

**Already Correct**: These campaigns correctly use "UAE" regional identifier.

| Current Name | Status |
|--------------|--------|
| `NDA \| UAE \| Search \| Interior Design Degree No Target` | ✅ Correct |
| `NDA \| UAE \| Search \| Interior Design Diploma No Target` | ✅ Correct |
| `NDA \| P Max Reboot \| Interior Design Diploma - UAE 175 no target 28/5` | ✅ Correct |
| `NDA \| P Max \| Interior Design Degree - UAE 175 No Target 24/4` | ✅ Correct |
| `NDA \| Search \| Brand - UAE No Target 7/7` | ✅ Correct |

---

### 7. Special Cases - Mixed Targeting

**Campaigns with mixed regional targeting** need careful review:

| Current Name | Location Targeting | Recommendation |
|--------------|-------------------|----------------|
| `NDA \| OM/SA/UAE \| Search \| Landscape Design No Target` | Oman, Saudi Arabia, UAE | `NDA \| GCC+UAE \| Search \| Landscape Design No Target` |
| `Learn SketchUp, Photos...` | Oman, Qatar, Saudi Arabia, UAE, UK | `NDA \| Multi-Region \| Video \| Learn SketchUp` |
| `NDA \| UK \| Search \| Interior Design Careers No Target` | UK + 5 specific UK cities | `NDA \| Europe \| Search \| Interior Design Careers No Target` |
| `NDA \| Pro Curtain Making & Soft Furnishings Fast-Track I 2023` | UK + Dubai | `NDA \| Europe+UAE \| Search \| Pro Curtain Making Fast-Track` |

---

## Legacy Campaigns (PAUSED)

**127 paused campaigns** with outdated naming conventions. These should be reviewed and potentially archived if no longer needed.

Examples:
- `01A4 - COURSES - DISPLAY - Interior Design - UK`
- `NDA Degrees 2017`
- `Interior Design Degree`
- `Garden Design Diploma - Mobile`

**Recommendation**: Review with client whether these should be:
1. Renamed to new convention (if potentially re-enabling)
2. Archived/deleted (if obsolete)
3. Left as-is (if historical reference only)

---

## Implementation Plan

### Phase 1: Review & Approval
1. Present this analysis to client (Paul Riley)
2. Confirm regional grouping definitions
3. Get approval for naming convention

### Phase 2: Prepare Rename Script
1. Create Python script to bulk rename via Google Ads API
2. Include backup/rollback capability
3. Test on sandbox account first

### Phase 3: Execute Rename
1. Backup current campaign names to CSV
2. Execute bulk rename (ENABLED campaigns first)
3. Verify all names updated correctly
4. Update internal documentation

### Phase 4: Legacy Cleanup (Optional)
1. Review 127 paused campaigns with client
2. Archive/delete obsolete campaigns
3. Rename remaining paused campaigns (if needed)

---

## Data Files Generated

**Location**: `/tmp/` (temporary analysis files)

1. `nda_campaigns.json` - All campaign data (187 campaigns)
2. `nda_campaign_locations.json` - Location targeting for each campaign
3. `nda_geo_mapping.json` - Geo constant ID → Country name mapping (125 locations)
4. `nda_campaign_analysis.json` - Regional analysis results
5. `nda_regional_analysis_report.txt` - Full text report
6. `nda_campaign_renaming_recommendations.md` - This document

---

## Questions for Client

Before implementing, confirm:

1. **Regional Grouping Approval**: Do the defined regional groupings match your business structure and reporting needs?

2. **UK → Europe Change**: Are you comfortable with "UK" campaigns being relabeled as "Europe"? (UK is part of Europe regional grouping)

3. **Legacy Campaign Cleanup**: Should we archive/delete the 127 paused legacy campaigns, or leave them as-is?

4. **Mixed Region Campaigns**: For campaigns targeting multiple regions (e.g., UK + Dubai), should we use:
   - `Europe+UAE` format
   - `Multi-Region` generic label
   - Split into separate campaigns?

5. **Rollout Timeline**: When should this renaming be executed? (Recommend outside of peak enrollment periods)

---

**Next Steps**: Present to client for review and approval.

