# 🖼️ How To Select Images for Performance Max Campaigns

**For**: Alex (Smythson Marketing Team)
**Purpose**: Guide to selecting image assets and populating the Google Sheet
**Last Updated**: 15th December 2025

---

## 🎯 Quick Summary

You need to select images from Smythson's Google Ads Asset Library and add their **Asset IDs** (numeric codes) to the Google Sheet. This guide shows you how to:

1. **Generate an Asset Library Browser** - Creates a clickable spreadsheet of all available images
2. **Review images** - View thumbnails and check where they're currently used
3. **Copy Asset IDs** - Add the correct IDs to the deployment spreadsheet
4. **Meet minimum requirements** - Ensure each campaign has required image types

**⏱️ Time Required**: 15-30 minutes for all regions

---

## 📋 Minimum Requirements (MUST FOLLOW)

Each Performance Max asset group **MUST** have at least:

| Image Type | Aspect Ratio | Minimum Count | Examples |
|------------|--------------|---------------|----------|
| **Landscape** | 1.91:1 | 1+ | 1200×628, 1600×837 |
| **Square** | 1:1 | 1+ | 1200×1200, 1000×1000 |
| **Portrait** | 4:5 | 0 (optional) | 960×1200, 800×1000 |

⚠️ **If you don't include at least 1 landscape + 1 square, the deployment will fail.**

---

## 🚀 Step-by-Step Workflow

### Step 1: Generate the Asset Library Browser

**What this does**: Creates a Google Sheet listing ALL images in Smythson's Google Ads account with clickable preview links.

**How to request it from Peter**:

```
"Hi Peter, can you generate the image asset catalog for [UK/US/EUR/ROW]?
I need to select new images for the [date] deployment."
```

**What Peter runs** (FYI - you don't need to do this):
```bash
cd /Users/administrator/Documents/PetesBrain.nosync/clients/smythson/scripts
python3 export-image-catalog-to-sheet.py --region uk
```

**What you'll receive**:
- Link to a new Google Sheet titled "Smythson Image Asset Catalog - [Region] - [Date]"
- Contains 7 columns:
  - **Asset ID** ← This is what you'll copy to the deployment sheet
  - **Asset Name** - Description/filename
  - **Dimensions** - Width×Height (tells you landscape/square/portrait)
  - **Format** - JPEG, PNG, etc.
  - **View Image** - Clickable link to see full image
  - **Usage Count** - How many campaigns currently use this
  - **Currently Used In** - Which asset groups have this image

---

### Step 2: Review Available Images

**Open the Asset Library Browser spreadsheet** Peter sends you.

**What to look for**:

✅ **Check dimensions** to identify image types:
- **Landscape (1.91:1)**: Width ÷ Height ≈ 1.9 (e.g., 1200×628, 1600×837)
- **Square (1:1)**: Width = Height (e.g., 1200×1200, 1000×1000)
- **Portrait (4:5)**: Width ÷ Height ≈ 0.8 (e.g., 960×1200)

✅ **Click "View Image" links** to see the actual image

✅ **Check "Currently Used In"** to see if an image is already performing well elsewhere

**Pro tip**: Sort by "Usage Count" to see which images are popular/proven performers.

---

### Step 3: Select Images for Your Campaign

**Open the PMax Deployment Spreadsheet**:
[Smythson PMax Master Sheet](https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit)

**Navigate to the correct tab**:
- UK campaigns → "UK PMax Assets" tab
- US campaigns → "US PMax Assets" tab
- EUR campaigns → "EUR PMax Assets" tab
- ROW campaigns → "ROW PMax Assets" tab

**Find the image columns** (starts at column AW):
- Columns **AW-BC** = Landscape images (1.91:1)
- Columns **BD-BJ** = Square images (1:1)
- Columns **BK-BQ** = Portrait images (4:5)
- Column **BT** = Logo (optional)

**How to populate**:

1. **Find the asset group row** you're updating (look at columns A-D for campaign/asset group names)

2. **Copy Asset IDs from the Asset Library Browser**:
   - Go back to the Asset Library Browser spreadsheet
   - Find the image you want
   - **Copy the Asset ID from column A** (e.g., `1234567890`)
   - Paste into the deployment spreadsheet in the appropriate column:
     - Landscape image? → Paste in columns AW-BC
     - Square image? → Paste in columns BD-BJ
     - Portrait image? → Paste in columns BK-BQ

3. **Repeat until you have**:
   - ✅ At least 1 landscape Asset ID (in AW-BC range)
   - ✅ At least 1 square Asset ID (in BD-BJ range)
   - Optional: Portrait images (in BK-BQ range)

**Example**:

| Campaign ID | Campaign Name | Asset Group ID | Asset Group Name | ... | Landscape 1 (AW) | Landscape 2 (AX) | ... | Square 1 (BD) | Square 2 (BE) | ... |
|-------------|--------------|---------------|------------------|-----|------------------|------------------|-----|---------------|---------------|-----|
| 12345 | UK \| P1 \| Diaries | 67890 | Diaries - Leather | ... | 9876543210 | 8765432109 | ... | 7654321098 | 6543210987 | ... |

---

### Step 4: Verify Your Selection

**Before you tell Peter it's ready**, check each row:

✅ **Minimum requirements met**:
- At least 1 Asset ID in columns AW-BC (landscape)
- At least 1 Asset ID in columns BD-BJ (square)

✅ **Asset IDs are numeric**: e.g., `1234567890` (NOT image filenames or URLs)

✅ **No duplicate IDs in same row**: Each Asset ID should only appear once per asset group

✅ **Empty cells are OK**: You don't need to fill all image columns

❌ **Common mistakes to avoid**:
- Putting landscape Asset IDs in square columns (or vice versa)
- Using image filenames instead of Asset IDs
- Missing the minimum requirements (1 landscape + 1 square)

---

### Step 5: Notify Peter

**Once your selection is complete**:

```
"Hi Peter, I've updated the image Asset IDs in the [UK/US/EUR/ROW] PMax Assets tab.
Ready for deployment when you are."
```

Peter will:
1. Run a dry-run test to validate your selection
2. Deploy the images via API
3. Confirm deployment success

---

## 🎨 Image Selection Strategy (Best Practices)

### For New Campaigns

**Start with proven performers**:
- Check "Usage Count" in Asset Library Browser
- High usage count = working well across multiple campaigns
- Consider reusing these first

**Diversify image types**:
- Mix product shots with lifestyle imagery
- Include both close-ups and contextual scenes
- Test different colour palettes

### For Seasonal Updates (e.g., Christmas, Valentine's)

**Refresh with themed imagery**:
- Select seasonal product shots
- Update lifestyle images to match season
- Keep brand assets consistent (logos, etc.)

**Keep best performers**:
- If an image has high "Usage Count", consider keeping it
- Only replace if you have stronger seasonal alternative

### For Testing New Creative

**Add 1-2 new images per update**:
- Keep most existing images (for consistency)
- Replace 1-2 underperformers with new options
- Monitor performance before making wholesale changes

---

## 📏 Image Specifications Reference

### Landscape (MARKETING_IMAGE)

**Aspect Ratio**: 1.91:1
**Recommended Dimensions**: 1200×628 (minimum 600×314)
**Where It Appears**: Display ads, Gmail ads, Discovery feeds
**Best For**: Wide product shots, lifestyle scenes, brand messaging

### Square (SQUARE_MARKETING_IMAGE)

**Aspect Ratio**: 1:1
**Recommended Dimensions**: 1200×1200 (minimum 300×300)
**Where It Appears**: Social-style placements, mobile feeds
**Best For**: Product close-ups, square compositions

### Portrait (PORTRAIT_MARKETING_IMAGE) - Optional

**Aspect Ratio**: 4:5
**Recommended Dimensions**: 960×1200 (minimum 480×600)
**Where It Appears**: Mobile-first placements, stories-style formats
**Best For**: Vertical product shots, portrait-oriented lifestyle

### Logo (LOGO) - Optional

**Aspect Ratio**: 1:1
**Recommended Dimensions**: 1200×1200 (minimum 128×128)
**Where It Appears**: Brand attribution in ads
**Best For**: Company logo, brand mark

---

## 🚨 Troubleshooting

### "I can't find the Asset Library Browser spreadsheet"

**Solution**: Ask Peter to regenerate it:
```
"Hi Peter, can you generate a fresh image asset catalog for [region]?"
```

---

### "The Asset ID I selected shows as 'invalid' when Peter tests"

**Possible causes**:
1. **Typo in Asset ID** - Double-check you copied the full number
2. **Wrong region** - Asset IDs are region-specific (UK assets won't work in US campaigns)
3. **Asset was deleted** - If the Asset Library Browser is old, the asset may no longer exist

**Solution**:
- Verify the Asset ID in the Asset Library Browser
- Generate a fresh Asset Library Browser if it's more than a week old

---

### "Peter says the deployment failed validation"

**Cause**: Missing minimum requirements (1 landscape + 1 square)

**Solution**:
- Check the row that failed
- Ensure at least 1 Asset ID in columns AW-BC (landscape)
- Ensure at least 1 Asset ID in columns BD-BJ (square)

---

### "I want to see the image before copying the Asset ID"

**Solution**:
- Click the "🖼️ View Image" link in column E of the Asset Library Browser
- Opens the full-size image in a new tab
- Once you're happy, copy the Asset ID from column A

---

## 📞 Need Help?

If you're stuck or unsure:

```
"Hi Peter, I have a question about selecting images for [specific asset group/campaign].
Can you help me understand [specific question]?"
```

**Common questions to ask**:
- "Which images are currently performing best for this campaign?"
- "Should I keep these existing images or replace them all?"
- "Is this Asset ID correct for a landscape image?"

---

## 🎓 Quick Reference Card

**Copy this for your notes**:

```
MINIMUM REQUIREMENTS:
✅ 1+ Landscape (1.91:1) → Columns AW-BC
✅ 1+ Square (1:1) → Columns BD-BJ

WORKFLOW:
1. Request Asset Library Browser from Peter
2. Open Asset Library Browser + PMax Deployment Spreadsheet side-by-side
3. For each asset group:
   - Find row in deployment spreadsheet
   - Select images from Asset Library Browser
   - Copy Asset IDs (column A) to deployment spreadsheet
   - Paste in correct columns (landscape = AW-BC, square = BD-BJ)
4. Verify: 1+ landscape, 1+ square per row
5. Notify Peter when ready

SPREADSHEET LINKS:
- PMax Deployment: https://docs.google.com/spreadsheets/d/1wwILYgddS946SAlvD5yjLjbLMRFQagsi0-5XFJmvC1g/edit
- Asset Library Browser: [Peter will send fresh link when needed]
```

---

**Questions? Ask Peter!** 🚀
