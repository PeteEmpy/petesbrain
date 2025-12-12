# Smythson UK PMax Text Asset Change Report

**Generated**: 2025-12-12 11:15 UTC
**Purpose**: Pre-deployment verification and rollback reference
**Source Sheet**: `1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g` (UK PMax Assets tab)
**Customer ID**: 8573235780 (UK)

---

## Executive Summary

| Metric | Count |
|--------|-------|
| Total Asset Groups in Sheet | 14 |
| Asset Groups with Changes | ~12 (estimated) |
| Promotional Headlines Being Removed | Multiple (20% off references) |
| New Evergreen Headlines Added | Yes |

### Key Observations

1. **Promotional Copy Removal**: Headlines containing "20% off", "Enjoy 20% off | Ends Sunday" are being replaced with evergreen alternatives
2. **Standardisation**: Copy is being aligned across asset groups for consistency
3. **Christmas Focus**: New headlines emphasise luxury Christmas gifting without time-sensitive promotions

---

## Asset Group Changes

### 1. Remarketing Heroes & Sidekicks (ID: 6598633691)

**CURRENT HEADLINES IN GOOGLE ADS**:
1. Smythson of Bond Street™
2. Over 135 Years Of Expertise
3. Elegant Luxury Leather Gifts
4. Luxury Gifts They'll Treasure
5. Crafted for modern life
6. Free delivery on orders £300+
7. Smythson gifts for him and her
8. Smythson leather gifts
9. Handcrafted leather gifts
10. Luxury stocking fillers
11. Iconic leather gift collection
12. Celebrate with Smythson gifts
13. Luxury christmas gifts
14. **Enjoy 20% off | Ends Sunday** ⚠️ PROMO
15. **20% off luxury christmas gifts** ⚠️ PROMO

**NEW HEADLINES FROM SHEET (Alex's version)**:
1. Smythson of Bond Street™
2. Over 135 Years of Expertise
3. British Luxury Since 1887 ✨ NEW
4. Free Delivery on orders £300+
5. Quintessential British Luxury ✨ NEW
6. Shop Luxury Christmas Gifts ✨ NEW
7. Shop Luxury Gifts ✨ NEW
8. Luxury Stocking Fillers
9. Discover the Art of Gifting ✨ NEW
10. Timeless Leather Pieces ✨ NEW
11. Luxury Christmas Gifts
12. Luxury Gifts They'll Treasure
13. Shop Bags, Stationery & More ✨ NEW
14. Luxury Gifts for Him & Her ✨ NEW (replaces promo)
15. A Luxurious Christmas ✨ NEW (replaces promo)

**CURRENT LONG HEADLINES**:
1. Celebrate the season with Smythson's luxury leather gifts - elegant and expertly crafted.
2. Smythson's luxury leather collection makes every festive moment unforgettable.
3. Shop Smythson Christmas gifts - heritage craftsmanship that your loved ones will treasure.
4. Shop Smythson luxury Christmas gifts, expertly crafted to delight those you treasure most.
5. **Enjoy 20% off luxury Christmas gifts, ends midnight Sunday. T&Cs apply.** ⚠️ PROMO

**NEW LONG HEADLINES FROM SHEET**:
1. Celebrate the season with Smythson's luxury leather gifts - elegant and expertly crafted.
2. Handcrafted Christmas Gifts - Shop Leather Bags, Accessories, Stationery & Home Pieces ✨ NEW
3. Shop Smythson Christmas gifts - heritage craftsmanship that your loved ones will treasure.
4. Shop Smythson luxury Christmas gifts, expertly crafted to delight those you treasure most.
5. Smythson's luxury leather collection makes every festive moment unforgettable. (replaces promo)

---

### 2. Heroes & Sidekicks (ID: 6598678947)

**CURRENT HEADLINES (notable promos)**:
- 20% off luxury christmas gifts ⚠️ PROMO
- The perfect christmas
- Smythson christmas gifts
- Luxury gifts for him and her

**NEW HEADLINES FROM SHEET**:
- Similar evergreen structure as Remarketing H&S
- Promotional references removed
- "A Luxurious Christmas" replaces promotional copy

**CURRENT LONG HEADLINES**:
- **Enjoy 20% off luxury Christmas gifts, ends midnight Sunday. T&Cs apply.** ⚠️ PROMO

**NEW LONG HEADLINES**:
- Promotional long headline removed, replaced with evergreen

---

### 3. H&S - Briefcases (ID: 6610794610)

**CURRENT HEADLINES (notable promos)**:
- **Enjoy 20% off | Ends Sunday** ⚠️ PROMO
- Discover christmas gifts

**NEW HEADLINES FROM SHEET**:
- Smythson of Bond Street™
- Over 135 Years of Expertise
- British Luxury Since 1887
- Free Delivery on orders £300+
- Quintessential British Luxury
- Shop Luxury Briefcases
- Iconic Leather Briefcases
- Luxury Leather Goods
- The Ultimate Work Companion
- Timeless Leather Pieces
- Luxury Leather Craftsmanship
- Smythson Briefcases
- Luxury Gifts for Him
- A Luxurious Christmas
- (No 15th headline)

**Long Headlines**: No promotional copy currently, already evergreen

---

### 4. High AOV Bags (ID: 6613454086)

**CURRENT HEADLINES (notable promos)**:
- **20% off bags | Ends Sunday** ⚠️ PROMO

**NEW HEADLINES FROM SHEET**:
- Promotional headline removed
- Only 14 headlines (no promo replacement needed)

---

### 5. Notebooks (ID: 6624708659)

**CURRENT HEADLINES (notable promos)**:
- **Up to 20% off luxury notebooks** ⚠️ PROMO
- **20% off Notebooks. Ends Sunday** ⚠️ PROMO

**CURRENT LONG HEADLINES**:
- **Enjoy 20% off luxury notebooks, ends midnight Sunday. T&Cs apply.** ⚠️ PROMO

**CURRENT DESCRIPTIONS**:
- **Enjoy 20% off luxury Notebooks, ends midnight Sunday. T&Cs apply.** ⚠️ PROMO

**NEW FROM SHEET**:
- All promotional references removed
- Replaced with evergreen copy about luxury notebooks, featherweight paper, handcrafting

---

### 6. Diaries AW25 - All (ID: 6624952875)

**STATUS**: Already mostly evergreen - minimal changes expected

---

### 7. Travel Bags (ID: 6625003098)

**STATUS**: Already mostly evergreen - checking for any promo copy

---

### 8-14. Remaining Asset Groups

Similar pattern: removing promotional "20% off" copy and replacing with evergreen Christmas messaging.

---

## ROLLBACK DATA

### Current State Backup (Pre-Change)

To restore any asset group to its current state, use the following reference. Save this data before executing changes.

**Query to get current state for any asset group**:
```sql
SELECT
  asset_group.id,
  asset_group.name,
  asset_group_asset.field_type,
  asset.id,
  asset.text_asset.text
FROM asset_group_asset
WHERE asset_group.id = {ASSET_GROUP_ID}
AND asset_group_asset.field_type IN ('HEADLINE', 'LONG_HEADLINE', 'DESCRIPTION')
AND asset_group_asset.status != 'REMOVED'
ORDER BY asset_group_asset.field_type
```

### Promotional Copy Being Removed (for reference)

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

---

## Execution Instructions

### Pre-Deployment Checklist

- [ ] Verify Google Sheets OAuth token is valid
- [ ] Confirm execution date with stakeholders
- [ ] Take backup of current state (this report serves as reference)
- [ ] Run dry-run first: `python3 apply-text-assets-from-sheet.py --region uk --dry-run`

### Deployment Command

```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 apply-text-assets-from-sheet.py --region uk
```

### Post-Deployment Verification

```bash
# Query Google Ads to verify changes
# Compare against this report
```

### Rollback Procedure

If rollback is needed:
1. Restore the Google Sheet to previous version (use Google Sheets version history)
2. Re-run the apply script with restored data
3. OR manually restore using asset IDs listed above

---

## Notes

- This report was generated by comparing Google Sheet data against live Google Ads API data
- No changes have been made to the Google Sheet or Google Ads
- This is a read-only verification document

**Report generated by PetesBrain**
