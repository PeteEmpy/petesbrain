# Google Ads Text Generator

A Python tool for creating Google Ads text assets optimized for ROAS campaigns, following ROK specifications.

## Overview

This toolset helps you create comprehensive Google Ads text assets including:

1. **Search Themes** (50 terms for Performance Max asset groups)
2. **Headlines** (50 total: 10 per section, 30 character max)
3. **Descriptions** (50 total: 10 per section, 90 character max)
4. **Sitelinks** (with headlines, descriptions, and URLs)
5. **Callout Extensions** (5 total)

### The 5 Content Sections

All headlines and descriptions are organized into these sections:

1. **Benefits** - Why customers can't live without the product
2. **Technical** - Technical advantages and features
3. **Quirky** - Humorous and engaging descriptions
4. **Call to Action** - Persuasive CTAs to drive purchases
5. **Brand/Category** - Product and brand highlights

## Files Included

- `google_ads_generator.py` - Core generator class with validation
- `example_template.py` - Complete example with sample ad copy
- `ROK _ Google Ads Text Asset Generation.docx` - Original specifications

## Quick Start

### Web Application (Recommended)

**Automated ad copy generation from any URL:**

**Browser-based (Terminal + Browser):**
```bash
./start.sh
# Then open http://localhost:5001 in your browser
```

**Desktop App (Native Window):**
```bash
python3 desktop.py
# Native window opens automatically - no browser needed!
```

**Or build as standalone .app:**
```bash
./build.sh
# Creates dist/Google Ads Text Generator.app
```

See [DESKTOP_BUILD.md](DESKTOP_BUILD.md) for full desktop app instructions.

---

### CLI Tools

### Option 1: View the Example Output

See a complete example for running shoes:

```bash
python3 example_template.py
```

This generates:
- `example_google_ads_assets.txt` - Formatted text output
- `example_google_ads_assets.csv` - CSV for Google Ads Editor

### Option 2: Interactive Mode

Create your own assets interactively:

```bash
python3 google_ads_generator.py
```

Follow the prompts to enter:
- Product/service name
- Brand name
- Website URL
- Headlines for each section
- Descriptions for each section

### Option 3: Use as a Python Module

Import and use programmatically:

```python
from google_ads_generator import GoogleAdsAssetGenerator

# Initialize
generator = GoogleAdsAssetGenerator(
    product_name="Your Product",
    brand="Your Brand",
    website_url="https://yoursite.com"
)

# Add headlines (returns True if valid)
generator.add_headline("Amazing Product Here", "Benefits")

# Add descriptions
generator.add_description("Experience amazing benefits with our product today.", "Benefits")

# Add sitelinks
generator.add_sitelink(
    headline="Shop Now",
    desc1="Browse our collection",
    desc2="Free shipping available",
    url="https://yoursite.com/shop"
)

# Add callouts
generator.add_callout("Free Shipping")

# Add search themes
generator.add_search_theme("best product online")

# Generate output
output = generator.generate_output()
print(output)

# Export CSV
csv_output = generator.export_csv()
```

## Character Limits

The tool automatically validates all character limits:

| Asset Type | Character Limit |
|------------|----------------|
| Headlines | 30 characters max |
| Descriptions | 90 characters max |
| Sitelink Headlines | 25 characters max |
| Sitelink Descriptions | 35 characters max |
| Callouts | 25 characters max |
| Search Themes | No limit |

## Best Practices

### Headlines
- Use the full 30 characters when possible
- Mix informative, CTA, features, benefits, and quirky
- Be specific to the client and product
- Strong calls to action without being aggressive

### Descriptions
- Maximize the 90 character limit
- Use a range of types (benefits, technical, quirky, CTA, brand)
- Don't use Dynamic Keyword Insertion (DKI)
- Don't use customizers

### Sitelinks
- Must have unique, validated URLs
- URLs must exist on the website
- Include clear, compelling headlines
- Two descriptive lines per sitelink

### Search Themes
- Cover all different ways visitors search for products
- Include variations (singular/plural, formal/casual)
- Mix broad and specific terms
- Include brand and non-brand terms
- 50 terms maximum, choose the very best

### Callout Extensions
- Highlight key benefits or offers
- Keep concise (under 25 characters)
- Focus on what makes you unique
- Examples: "Free Shipping", "24/7 Support", "30-Day Returns"

## Output Format

The tool generates two files:

### 1. Text File (`.txt`)
Formatted, human-readable output with:
- Character counts for each asset
- Organized by section
- Clear headers and separators
- Summary totals

### 2. CSV File (`.csv`)
Google Ads Editor compatible format with:
- Type (Headline/Description)
- Text content
- Character count
- Section category
- Landing page URL

## Example Output Structure

```
================================================================================
GOOGLE ADS TEXT ASSETS - COMPLETE OUTPUT
Product: Your Product | Brand: Your Brand
================================================================================

1. SEARCH THEMES (for Performance Max Asset Group)
--------------------------------------------------------------------------------
search term 1
search term 2
...

2. HEADLINES (30 character max)
--------------------------------------------------------------------------------
BENEFITS
 1. Your Amazing Headline Here   [28 chars]
 2. Another Great Headline       [21 chars]
...

3. DESCRIPTIONS (90 character max)
--------------------------------------------------------------------------------
BENEFITS
 1. Your compelling description goes here with benefits and value propositions.  [78 chars]
...

4. SITELINKS
--------------------------------------------------------------------------------
Sitelink 1:
  Headline: Shop Now [9 chars]
  Desc 1:   Browse our products [19 chars]
  Desc 2:   Free shipping today [19 chars]
  URL:      https://example.com/shop
...

5. CALLOUT EXTENSIONS
--------------------------------------------------------------------------------
1. Free Shipping
2. 24/7 Support
...
```

## Guidelines and Resources

The tool follows best practices from these sources:
- [Google Ads RSA Guidelines](https://support.google.com/google-ads/answer/6167115?hl=en-GB)
- [Funnel.io: Google Ads Headlines](https://funnel.io/blog/google-ads-headlines)
- [Jasper AI: Google Ads Generator](https://www.jasper.ai/blog/google-ads-generator)
- [BigBlue: Killer Ad Titles](https://www.bigblue.co/blog/secrets-of-generating-killer-ad-titles-for-google-adwords-campaign)
- [Midsummer Agency: Headlines That Convert](https://midsummer.agency/blog/best-practices-for-writing-google-ads-headlines-that-convert/)
- [Rocket Made: Google Ads Headlines](https://rocketmadal.com/google-ads-headlines/)
- [Google Business: Write Online Ads](https://business.google.com/uk/resources/articles/write-online-ads/)

## Tips for ROAS Optimization

1. **Test Multiple Variations** - Create 3-5 versions for A/B testing
2. **Focus on Benefits** - Lead with value propositions
3. **Include Pricing/Offers** - When appropriate, mention discounts or special offers
4. **Use Numbers** - Specific numbers (e.g., "40% More", "10,000+ Customers") increase credibility
5. **Match Search Intent** - Align headlines with user search queries
6. **Mobile-First** - Keep key info in first 20-25 characters
7. **Brand Consistency** - Maintain consistent voice across all assets
8. **Urgency Without Aggression** - Create FOMO subtly (e.g., "Limited Stock" vs "BUY NOW!!!")

## Customization

### Modify Section Names
Edit the `sections` list in `google_ads_generator.py`:

```python
sections = [
    ("Benefits", "Your custom description"),
    ("Technical", "Your custom description"),
    # ... etc
]
```

### Change Character Limits
Modify the class constants:

```python
class GoogleAdsAssetGenerator:
    HEADLINE_MAX = 30  # Change as needed
    DESCRIPTION_MAX = 90  # Change as needed
```

### Add New Asset Types
Extend the `GoogleAdsAssetGenerator` class with new methods following the existing pattern.

## Requirements

- Python 3.6 or higher
- No external dependencies required

## Support

For issues or questions about the ROK specifications, refer to:
- Original document: `ROK _ Google Ads Text Asset Generation.docx`
- Google Ads official documentation

## License

Internal tool for ROK Google Ads campaign creation.
