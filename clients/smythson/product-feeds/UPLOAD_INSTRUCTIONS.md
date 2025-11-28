# Smythson Custom Label 4 - Upload Instructions

## Files Created
- **CSV File**: `Smythson_Custom_Label_4_Gifts_2025-11-06-0945.csv`
- **Desktop Copy**: `~/Desktop/Smythson_Custom_Label_4_Gifts.csv` (for easy upload)

## Data Summary
- **Total Products**: 573
- **Gifts for Him**: 504 products
- **Gifts for Her**: 69 products
- **Custom Label**: `custom_label_4`

## Upload to Google Sheets

### Method 1: Direct Upload (Recommended)
1. Go to [Google Sheets](https://sheets.google.com)
2. Click **File** > **Import**
3. Click **Upload** tab
4. Select the CSV file from your Desktop: `Smythson_Custom_Label_4_Gifts.csv`
5. Choose **Replace spreadsheet** or **Create new spreadsheet**
6. Click **Import data**
7. Rename the sheet to: "Smythson - Custom Label 4 - Gifts (Him/Her)"

### Method 2: Copy/Paste
1. Open the CSV file
2. Select all data (Cmd+A)
3. Copy (Cmd+C)
4. Create new Google Sheet or open existing
5. Paste (Cmd+V) into cell A1

## Add to Google Merchant Center

Once uploaded to Google Sheets:

1. **Get the Sheet URL** from your browser
2. **Go to Google Merchant Center** > Data sources > Supplemental feeds
3. **Add supplemental source**:
   - Source type: **Google Sheets**
   - Paste the Google Sheet URL
   - Feed name: `Smythson Custom Label 4 - Gifts`
4. **Configure the feed**:
   - Update `custom_label_4` field
   - Apply to both **UK** and **USA** accounts
   - Schedule: Daily automatic fetch
5. **Save and test**

## Verify in Merchant Center

After 24 hours, check products have the new label:
1. Go to **Products** > **All products**
2. Click any product
3. Check **Labels** section
4. Should see `custom_label_4: Gifts for Him` or `Gifts for Her`

## Use in Google Ads Campaigns

Once verified in GMC:
1. Go to **Performance Max** campaigns
2. Edit **Asset Groups** > **Listing groups**
3. Add partition by **Custom label 4**
4. Create separate asset groups for:
   - Gifts for Him
   - Gifts for Her

---

**Created**: 2025-11-06
**Script**: `clients/smythson/scripts/scrape-gift-products.py`
**URLs Scraped**:
- Him: https://www.smythson.com/uk/search/?prefn1=gender&prefv1=For%20Him&q=gifts
- Her: https://www.smythson.com/uk/search/?prefn1=gender&prefv1=For%20Her&q=gifts
