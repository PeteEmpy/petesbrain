# Smythson Multi-Region Text Asset Change Report

**Generated**: 2025-12-12
**Purpose**: Pre-deployment verification and rollback reference for ALL regions
**Prepared by**: PetesBrain automated analysis

---

## Executive Summary

| Region | Account | Asset Groups | Promotional Copy Status | Action Required |
|--------|---------|--------------|------------------------|-----------------|
| **UK** | 8573235780 | 14 | ⚠️ BEING REMOVED | Ready for deployment |
| **US** | 7808690871 | 17 | ✅ Already evergreen | No changes needed |
| **EUR** | 7679616761 | 15 | ⚠️ STILL CONTAINS PROMOS | Needs Alex review |
| **ROW** | 5556710725 | 4 | ⚠️ STILL CONTAINS PROMOS | Needs Alex review |

### Critical Finding

**UK spreadsheet has been updated to evergreen copy**, but **EUR and ROW spreadsheets still contain promotional "20% off" headlines**. This may be intentional (promo still running) or an oversight requiring Alex's attention.

---

## UK Region - READY FOR DEPLOYMENT

**Customer ID**: 8573235780
**Spreadsheet Tab**: UK PMax Assets
**Asset Groups**: 14

### Changes Being Made

The UK spreadsheet has removed all promotional copy ("20% off", "Ends Sunday") and replaced with evergreen Christmas messaging.

**Promotional Headlines Being Removed**:
- "Enjoy 20% off | Ends Sunday"
- "20% off luxury christmas gifts"
- "20% off bags | Ends Sunday"
- "Up to 20% off luxury notebooks"
- "20% off Notebooks. Ends Sunday"

**Promotional Long Headlines Being Removed**:
- "Enjoy 20% off luxury Christmas gifts, ends midnight Sunday. T&Cs apply."
- "Enjoy 20% off luxury notebooks, ends midnight Sunday. T&Cs apply."

**New Evergreen Headlines Added**:
- "British Luxury Since 1887"
- "Quintessential British Luxury"
- "Shop Luxury Christmas Gifts"
- "Discover the Art of Gifting"
- "Timeless Leather Pieces"
- "A Luxurious Christmas"
- "Shop Bags, Stationery & More"
- "Luxury Gifts for Him & Her"

**Full UK change details**: See `UK-PMAX-TEXT-ASSET-CHANGE-REPORT-2025-12-12.md`

---

## US Region - NO CHANGES NEEDED

**Customer ID**: 7808690871
**Spreadsheet Tab**: US PMax Assets
**Asset Groups**: 17

### Current State

✅ **US spreadsheet already contains evergreen copy** - no promotional "20% off" messaging found.

**US-Specific Adaptations**:
- Free delivery threshold: "$500+" (vs £300+ UK)
- Uses "Holiday" instead of "Christmas" in some places (US market preference)
- Currency and terminology appropriate for US market

**Sample US Headlines**:
- "Smythson of Bond Street™"
- "British Luxury Since 1887"
- "Free Delivery On Orders $500+"
- "Quintessential British Luxury"
- "Luxury Holiday Gifts"
- "Luxury Stocking Fillers"

**Conclusion**: No deployment action required for US.

---

## EUR Region - ⚠️ REVIEW REQUIRED

**Customer ID**: 7679616761
**Spreadsheet Tab**: EUR PMax Assets
**Asset Groups**: 15

### ⚠️ WARNING: Promotional Copy Still Present

The EUR spreadsheet **still contains promotional "20% off" headlines** across multiple languages:

#### French (FR) Asset Groups
**Headlines containing promotions**:
- "-20% sur les cadeaux de Noël" (Christmas Gifting for Her)
- "-20% sur les cadeaux de Noël" (Christmas Gifting)
- "-20% sur les cadeaux de Noël" (Christmas Gifting for Him)

#### German (DE) Asset Groups
**Headlines containing promotions**:
- "-20 % auf Weihnachtsgeschenke" (Christmas Gifting)
- "-20 % auf Weihnachtsgeschenke" (Christmas Gifting for Her)
- "-20 % auf Weihnachtsgeschenke" (Christmas Gifting for Him)

#### Italian (IT) Asset Groups
**Headlines containing promotions**:
- "-20% regali natalizi di lusso" (Christmas Gifting for Her)
- "-20% regali natalizi di lusso" (Christmas Gifting for Him)
- "-20% regali natalizi di lusso" (Christmas Gifting)

#### Generic EUR Asset Groups (English)
**Headlines containing promotions**:
- "Enjoy 20% off | Ends Sunday" (Christmas Gifting for Him - AG 6631187726)
- "Enjoy 20% off | Ends Sunday" (Christmas Gifting for Her - AG 6631187777)
- "Enjoy 20% off | Ends Sunday" (Christmas Gifting - AG 6631187780)

### Action Required

**Question for Alex**: Is this intentional (promo still running in EUR) or should these be updated to evergreen copy before deployment?

---

## ROW Region - ⚠️ REVIEW REQUIRED

**Customer ID**: 5556710725
**Spreadsheet Tab**: ROW PMax Assets
**Asset Groups**: 4

### ⚠️ WARNING: Promotional Copy Still Present

The ROW spreadsheet **still contains promotional "Enjoy 20% off | Ends Sunday" headlines**:

| Asset Group ID | Asset Group Name | Promotional Headline |
|----------------|------------------|---------------------|
| 6631187327 | Christmas Gifting for Him | Enjoy 20% off \| Ends Sunday |
| 6631187330 | Christmas Gifting for Her | Enjoy 20% off \| Ends Sunday |
| 6631187333 | Christmas Gifting | Enjoy 20% off \| Ends Sunday |

**Diaries AW25 - All (AG 6631187342)**: Already evergreen, no promotional copy.

### Action Required

**Question for Alex**: Is this intentional (promo still running in ROW) or should these be updated to evergreen copy before deployment?

---

## RSA (Responsive Search Ads) Status

**RSA Spreadsheet ID**: `189nkILOXt5qbIO5dO-MQsU1pB_mGLoDHTWmAJlPkHLo`

### USA RSAs
✅ **All evergreen** - Christmas-focused but no promotional "20% off" copy

Sample headlines:
- "Smythson of Bond Street™"
- "British heritage since 1887"
- "Explore luxury Christmas gifts"
- "Shop luxury stocking fillers"
- "Luxury gifts for him"
- "Luxury gifts for her"

### EUR RSAs
✅ **All evergreen** - Multi-language (DE, FR, IT, CH) without promotional copy

### ROW RSAs
✅ **All evergreen** - No promotional copy found

**Conclusion**: RSA spreadsheets across all regions appear ready for deployment with evergreen copy.

---

## Deployment Recommendations

### Immediate Actions

1. **UK PMax**: ✅ Ready for deployment - run `apply-text-assets-from-sheet.py --region uk`

2. **US PMax**: ✅ No action needed - already evergreen

3. **EUR PMax**: ⚠️ **HOLD** - Confirm with Alex whether promotional copy should remain or be updated

4. **ROW PMax**: ⚠️ **HOLD** - Confirm with Alex whether promotional copy should remain or be updated

5. **All RSAs**: ✅ Ready for deployment via Google Ads Editor CSV import

### Pre-Deployment Checklist

- [ ] Verify Google Sheets OAuth token is valid
- [ ] Confirm UK deployment date with stakeholders
- [ ] Clarify EUR/ROW promotional copy intention with Alex
- [ ] Take backup of current Google Ads state (this report serves as reference)
- [ ] Run dry-run first: `python3 apply-text-assets-from-sheet.py --region uk --dry-run`

---

## Rollback Reference

### UK PMax Promotional Assets (Being Removed)

| Asset Group | Promotional Copy | Asset ID |
|------------|-----------------|----------|
| Remarketing H&S | Enjoy 20% off \| Ends Sunday | 315191380237 |
| Remarketing H&S | 20% off luxury christmas gifts | 315250668130 |
| Remarketing H&S | Enjoy 20% off luxury Christmas gifts, ends midnight Sunday. T&Cs apply. | 315250668133 |
| Heroes & Sidekicks | 20% off luxury christmas gifts | 315250668130 |
| Heroes & Sidekicks | Enjoy 20% off luxury Christmas gifts, ends midnight Sunday. T&Cs apply. | 315250668133 |
| H&S - Briefcases | Enjoy 20% off \| Ends Sunday | 315191380237 |
| High AOV Bags | 20% off bags \| Ends Sunday | 315175995134 |
| Notebooks | Up to 20% off luxury notebooks | 309902516241 |
| Notebooks | 20% off Notebooks. Ends Sunday | 315191380234 |
| Notebooks | Enjoy 20% off luxury notebooks, ends midnight Sunday. T&Cs apply. | 315291486600 |

### Rollback Procedure

If rollback is needed after UK deployment:
1. Restore the Google Sheet to previous version (use Google Sheets version history)
2. Re-run the apply script with restored data
3. OR manually restore using asset IDs listed above

---

## Technical Details

### Spreadsheet IDs

| Purpose | Spreadsheet ID |
|---------|---------------|
| PMax Text Assets | `1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g` |
| RSA Text Assets | `189nkILOXt5qbIO5dO-MQsU1pB_mGLoDHTWmAJlPkHLo` |

### Customer IDs

| Region | Customer ID | Manager ID |
|--------|-------------|------------|
| UK | 8573235780 | 2569949686 |
| US | 7808690871 | 2569949686 |
| EUR | 7679616761 | 2569949686 |
| ROW | 5556710725 | 2569949686 |

### Deployment Scripts

```bash
# UK PMax (ready)
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 apply-text-assets-from-sheet.py --region uk --dry-run  # Test first
python3 apply-text-assets-from-sheet.py --region uk            # Live execution

# RSA via Google Ads Editor
python3 ../../shared/scripts/generate-rsa-update-csv.py \
  --client smythson \
  --input ../data/uk_rsa_updates.json \
  --output uk_rsa_updates.csv
```

---

## Notes

- This report was generated by comparing Google Sheet data against live Google Ads API data
- No changes have been made to the Google Sheet or Google Ads
- This is a read-only verification document
- EUR and ROW promotional copy status requires human decision before proceeding

**Report generated by PetesBrain**
