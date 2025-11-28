# Smythson Black Friday 2025 - Merchant Centre Promotions Setup Guide

**Date Created**: 13 November 2025
**Effective Dates**: 17 November 2025 - 1 December 2025
**Total Products**: 368 products (302 Leather + 66 Books)

---

## Files Created

**Primary File (Recommended)**:
1. **`smythson-bf2025-promotions-feed.csv`** - Complete promotion feed with all details (368 products)
   - Includes both promotions with full specifications
   - Ready to upload as a promotion source in Merchant Centre

**Alternative Files (Not needed if using promotion feed above)**:
2. **`smythson-bf2025-leather-30off-products.csv`** - 302 leather products (standalone)
3. **`smythson-bf2025-books-20off-products.csv`** - 66 books products (standalone)

---

## Promotion 1: Leather 30% Off

### Basic Details
- **Promotion ID**: `BF2025_LEATHER_30`
- **Promotion Long Title**: `Black Friday 30% off Leather`
- **Promotion Effective Dates**:
  - Start: `2025-11-17T00:00:00Z`
  - End: `2025-12-01T23:59:59Z`
- **Redemption Channel**: `ONLINE`
- **Country**: `GB` (or add US, EU, etc. as needed)

### Discount Details
- **Offer Type**: `PERCENT_OFF`
- **Percent Off**: `30`

### Product Applicability
- **Product Applicability**: `SPECIFIC_PRODUCTS`
- **Upload Method**: CSV file upload
- **File**: `smythson-bf2025-leather-30off-products.csv` (302 products)

---

## Promotion 2: Books 20% Off

### Basic Details
- **Promotion ID**: `BF2025_BOOKS_20`
- **Promotion Long Title**: `Black Friday 20% off Books`
- **Promotion Effective Dates**:
  - Start: `2025-11-17T00:00:00Z`
  - End: `2025-12-01T23:59:59Z`
- **Redemption Channel**: `ONLINE`
- **Country**: `GB` (or add US, EU, etc. as needed)

### Discount Details
- **Offer Type**: `PERCENT_OFF`
- **Percent Off**: `20`

### Product Applicability
- **Product Applicability**: `SPECIFIC_PRODUCTS`
- **Upload Method**: CSV file upload
- **File**: `smythson-bf2025-books-20off-products.csv` (66 products)

---

## Step-by-Step Setup Instructions

### Recommended Method: Upload Promotion Feed

**This is the easiest method - upload one file and both promotions are created automatically.**

### 1. Access Google Merchant Centre
1. Log in to [Google Merchant Centre](https://merchants.google.com/)
2. Navigate to **Marketing** → **Promotions**
3. Click **"Promotion feeds"** or **"Add promotion source"**

### 2. Upload the Promotion Feed
1. Click **"Add promotion source"**
2. Choose upload method:
   - **One-time upload**: Upload `smythson-bf2025-promotions-feed.csv` directly
   - **Scheduled fetch**: Set up recurring fetch from URL (if hosted)
3. Upload the file: **`smythson-bf2025-promotions-feed.csv`**
4. Wait for Google to process (usually 5-30 minutes)

### 3. Verify Both Promotions
1. Go to **Marketing** → **Promotions** → **All promotions**
2. Verify you see:
   - **BF2025_LEATHER_30** - 302 products
   - **BF2025_BOOKS_20** - 66 products
3. Check status shows **Active** (once start date arrives)
4. Review any errors or warnings

---

## Alternative Method: Manual Promotion Creation

**Only use this if the promotion feed upload doesn't work.**

### 1. Access Google Merchant Centre
1. Log in to [Google Merchant Centre](https://merchants.google.com/)
2. Navigate to **Marketing** → **Promotions**

### 2. Create Promotion 1 (Leather 30% Off)
1. Click **+ Create Promotion**
2. Fill in the details:
   - **Promotion ID**: `BF2025_LEATHER_30`
   - **Long Title**: `30% off Leather Goods`
   - **Effective Dates**: 17 Nov 2025 - 1 Dec 2025
   - **Redemption Channel**: Online
   - **Country**: GB (+ any other target countries)
3. **Discount Details**:
   - Offer Type: **Percent off**
   - Value: **30**%
4. **Product Applicability**:
   - Select **Specific products**
   - Choose **Upload CSV file**
   - Upload: `smythson-bf2025-leather-30off-products.csv`
5. Click **Save**

### 3. Create Promotion 2 (Books 20% Off)
1. Click **+ Create Promotion**
2. Fill in the details:
   - **Promotion ID**: `BF2025_BOOKS_20`
   - **Long Title**: `20% off Books & Stationery`
   - **Effective Dates**: 17 Nov 2025 - 1 Dec 2025
   - **Redemption Channel**: Online
   - **Country**: GB (+ any other target countries)
3. **Discount Details**:
   - Offer Type: **Percent off**
   - Value: **20**%
4. **Product Applicability**:
   - Select **Specific products**
   - Choose **Upload CSV file**
   - Upload: `smythson-bf2025-books-20off-products.csv`
5. Click **Save**

### 4. Verify Promotions
1. Check that both promotions show status: **Active** (once start date arrives)
2. Verify product count matches:
   - Leather: 302 products
   - Books: 66 products
3. Check for any errors or warnings

---

## Important Notes

### Product ID Format
- Product IDs in CSV files match the **ARTICLE** column from the source spreadsheet
- These should match the `id` field in your Google Shopping feed
- If your feed uses a different format (e.g., SKU instead of ARTICLE), you may need to adjust

### CSV File Format
- Both CSV files include two columns: `id,promotion_id`
- Each product is linked to its respective promotion ID:
  - Leather products: `BF2025_LEATHER_30`
  - Books products: `BF2025_BOOKS_20`
- This format allows Merchant Centre to automatically link products to promotions

### Multi-Country Setup
If promoting in multiple countries (US, EU, etc.):
- Create separate promotions for each country
- Use country-specific pricing from the source spreadsheet
- Example: `BF2025_LEATHER_30_US`, `BF2025_LEATHER_30_EU`

### Timing
- Promotions should be set up **at least 24 hours before start date** to allow Google processing time
- Current date: 13 November 2025
- Start date: 17 November 2025
- **Setup today or tomorrow to allow processing time**

### Monitoring
After setup, monitor:
- Promotion approval status in Merchant Centre
- Products showing "Sale" badge in Shopping results
- Performance Max campaigns picking up promotion signals
- Any disapproved products or errors

---

## Troubleshooting

### Common Issues

**Issue**: Product IDs not matching
- **Solution**: Verify your Shopping feed uses ARTICLE numbers as product IDs
- Check a few sample products in your feed vs. the CSV files

**Issue**: Promotion shows fewer products than expected
- **Solution**: Some products may not be in your active feed
- Check feed status and approve any pending products

**Issue**: Promotion not showing in Shopping ads
- **Solution**: Allow 24-48 hours for Google to process
- Verify promotion dates are correct
- Check products are approved in Shopping feed

**Issue**: Wrong discount showing
- **Solution**: Verify percent off value (30% for leather, 20% for books)
- Check no conflicting promotions exist

---

## Source Data

**Original Spreadsheet**: `AW25 Black Friday Promotion 30% off Leather 20% Books (incl. exclusions).csv`
**Location**: `/clients/smythson/spreadsheets/`

**Product Selection Criteria**:
- Excluded products marked as "DUPLICATE" in spreadsheet
- Filtered by "MARKETING CAPSULE" column:
  - "LEATHER @ 30% OFF" → 302 products
  - "BOOKS @ 20% OFF" → 66 products

---

## Next Steps After Setup

1. ✓ Create promotions in Merchant Centre (using this guide)
2. Verify promotions are active and products are matched
3. Update Performance Max campaigns if needed (promotion signals)
4. Monitor promotion performance during 17 Nov - 1 Dec period
5. Prepare post-Black Friday analysis

---

**Questions or Issues?** Contact Pete or refer to Google Merchant Centre documentation.
