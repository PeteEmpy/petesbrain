# Testing Guide

## Important: URL Requirements

Not all URLs will work with the automated scraper. Here's what you need to know:

### URLs That WILL Work ✅

- **E-commerce sites without heavy bot protection**
- **Small to medium business websites**
- **Blog posts and content sites**
- **Product pages with standard HTML structure**
- **Sites that allow automated access**

### URLs That WON'T Work ❌

- **Major brands (Nike, Adidas, Apple, etc.)** - They block automated requests
- **Sites requiring login/authentication**
- **Heavy JavaScript-rendered content** (React SPAs, etc.)
- **Sites with aggressive bot detection** (Cloudflare, etc.)
- **Sites that return 404/403 errors**

## How to Test

### Step 1: Open the App
Navigate to **http://localhost:5001** in your browser.

### Step 2: Try These Test URLs

Here are some URLs that should work for testing:

**Example Product Page:**
```
https://www.example.com
```
(Limited content, but should work)

**Wikipedia Products:**
```
https://en.wikipedia.org/wiki/Running_shoe
```
(Will extract general information)

**Your Own Website:**
If you have a website or can access a small business website, those typically work best!

### Step 3: Check the Console Output

When you submit a URL, the terminal running Flask will show:
```
================================================================================
ANALYZED URL: https://example.com
Product: Product Name Here
Category: Detected Category
Brand: Brand Name
Features extracted: 5
Benefits extracted: 3
================================================================================
```

This tells you what the system found!

### Step 4: Review Generated Assets

On the RSA Editor page, you should see:
- **Header shows**: Product name, Category, and Brand
- **Headlines** with content specific to your URL
- **Descriptions** referencing the actual product

## What to Look For

### Signs It's Working:
✅ Product name from the page appears in headlines/descriptions
✅ Category is relevant to the product (not just "Products")
✅ Some headlines use phrases from the actual page
✅ Descriptions mention specific features or benefits

### Signs It's Not Working:
❌ All copy is generic ("Transform Your Products", "Quality You Can Trust")
❌ Category shows as "Products" (fallback)
❌ No product name shown in header
❌ Features extracted: 0, Benefits extracted: 0

## Troubleshooting

### "Failed to fetch URL content"
**Problem**: The website is blocking automated access or the URL is invalid.

**Solutions**:
- Try a different URL
- Try a smaller website (not major brands)
- Check if the URL works in a regular browser first
- Try your own website if you have one

### Generic Content Generated
**Problem**: The page doesn't have structured content the scraper can extract.

**Reasons**:
- Page is mostly JavaScript-rendered
- Content is in iframes or dynamic elements
- Page has minimal text/no product information
- Content is behind authentication

**Solutions**:
- Try a page with clear product information
- Look for pages with:
  - Clear headings (H1, H2, H3)
  - Bullet-point lists of features
  - Product descriptions
  - Visible text content

### Error: "Address already in use"
**Problem**: Flask is already running on port 5001.

**Solution**:
```bash
lsof -ti:5001 | xargs kill -9
```

Then restart with:
```bash
./start.sh
```

## Testing with Mock Data

If you can't find a working URL, you can test the functionality directly:

```bash
python3 test_url_analysis.py
```

This runs a test with mock HTML content to demonstrate that the extraction and generation logic works correctly.

## Best Practices for Real Use

When using this tool for actual campaigns:

1. **Test with multiple pages** from the same site
2. **Review all generated copy** - automation helps but human review is essential
3. **Edit as needed** - use the generated copy as a starting point
4. **Verify accuracy** - ensure technical claims are accurate
5. **Brand consistency** - adjust tone to match brand voice

## Debug Information

The app now shows debug information in:

1. **Terminal Output** - Shows what was extracted
2. **Page Header** - Shows product, category, brand
3. **Generated Copy** - Should reflect the specific product

If you see "Features extracted: 0", the page likely:
- Has no list items
- Has no bolded text
- Has minimal headings
- Uses JavaScript for content

## Need Help?

If you're consistently seeing generic results:
1. Check terminal output when submitting a URL
2. Note the "Features extracted" and "Benefits extracted" counts
3. Try a different URL type
4. Consider testing with your own website first

The tool works best with traditional HTML websites that have:
- Clear product information in text
- Structured content (headings, lists, bold text)
- Accessible HTML (not all JavaScript)
