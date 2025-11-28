# Google Ads Text Generator - Web Application

A web-based tool for generating and managing Google Ads text assets optimized for ROAS campaigns. Simply enter a URL and get professionally crafted headlines and descriptions with an easy-to-use selection interface.

## Features

- **URL-Based Generation**: Automatically analyze any website and generate relevant ad copy
- **Interactive Selection**: Easy checkbox interface to select the assets you want
- **Export Options**:
  - Export to CSV (Google Ads Editor compatible)
  - Copy to clipboard
- **Real-time Stats**: See how many assets you've selected
- **Character Validation**: Visual indicators for character limits
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Option 1: Using the Start Script (Recommended)

```bash
./start.sh
```

This will:
1. Create a virtual environment (if needed)
2. Install dependencies (if needed)
3. Start the Flask application
4. Open http://localhost:5001 in your browser

### Option 2: Manual Start

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 app.py
```

Then open your browser and go to: **http://localhost:5001**

## How to Use

### Step 1: Enter URL and Select Ad Type

1. Enter the URL of the product/service page you want to advertise
2. Choose between:
   - **RSA (Responsive Search Ad)** - For standard search campaigns
   - **Asset Group** - For Performance Max campaigns (coming soon)
3. Click "Generate Ad Assets"

### Step 2: Review and Select Assets

The generator will create:
- **50 Headlines** (30 characters max) organized into 5 sections:
  - Benefits - Why customers need this product
  - Technical - Technical advantages and features
  - Quirky - Creative, humorous copy with personality
  - Call to Action - Persuasive CTAs
  - Brand/Category - Brand and product category descriptions

- **50 Descriptions** (90 characters max) following the same structure

### Step 3: Select Your Favorites

- Click checkboxes next to the assets you want to use
- Use "Select All Headlines" or "Select All Descriptions" for bulk selection
- Selected items are highlighted in blue
- See real-time count of selected assets in the header

### Step 4: Export or Copy

**Export to CSV**
- Click "Export to CSV" button
- Download a Google Ads Editor compatible CSV file
- Import directly into Google Ads Editor

**Copy to Clipboard**
- Click "Copy to Clipboard" button
- Paste into any document or spreadsheet
- Includes formatted text with character counts

## File Structure

```
.
├── app.py                          # Flask web application
├── ad_copy_generator.py            # URL analyzer and ad copy generator
├── requirements.txt                # Python dependencies
├── start.sh                        # Quick start script
├── templates/
│   ├── index.html                  # Landing page with URL input
│   ├── rsa_editor.html            # RSA editor with selection interface
│   └── asset_group_editor.html    # Asset Group editor (coming soon)
├── google_ads_generator.py         # Original CLI generator
├── example_template.py             # Example templates
└── README_WEB_APP.md              # This file
```

## Google Ads Editor CSV Format

The exported CSV uses the format required by Google Ads Editor:

```csv
Ad type,Text,Final URL
Responsive search ad headline,"Your Headline Here",https://yoursite.com
Responsive search ad description,"Your description here.",https://yoursite.com
```

To import into Google Ads Editor:
1. Open Google Ads Editor
2. Go to Account → Import → From file
3. Select the exported CSV file
4. Review and post to Google Ads

## Character Limits

The tool enforces Google Ads character limits:

| Asset Type | Character Limit | Visual Warning |
|------------|----------------|----------------|
| Headlines | 30 characters | Orange at 27+, Red at 30+ |
| Descriptions | 90 characters | Orange at 85+, Red at 90+ |

## Ad Generation Strategy

### The 5-Section Approach

Each section serves a specific purpose in your ad strategy:

1. **Benefits Section**
   - Focus: Customer value and outcomes
   - Tone: Aspirational, benefit-driven
   - Example: "Transform Your Running Game"

2. **Technical Section**
   - Focus: Features and specifications
   - Tone: Professional, authoritative
   - Example: "Advanced Carbon Plate Tech"

3. **Quirky Section**
   - Focus: Personality and differentiation
   - Tone: Creative, memorable
   - Example: "Your Feet's New Best Friend"

4. **Call to Action Section**
   - Focus: Urgency and action
   - Tone: Persuasive but not aggressive
   - Example: "Shop Now - Free Shipping"

5. **Brand/Category Section**
   - Focus: Trust and credibility
   - Tone: Professional, trustworthy
   - Example: "UK's #1 Running Shoe"

## Best Practices

### URL Selection
- Use your main product or landing page URL
- Ensure the page has clear product information
- Pages with rich content generate better results

### Asset Selection
- Mix assets from different sections for variety
- Google Ads works best with 8-15 headlines and 2-4 descriptions
- Test different combinations to find what works best

### Testing Strategy
1. Start with a diverse selection across all sections
2. Let Google's algorithm optimize for 2-4 weeks
3. Review performance by asset
4. Replace low-performing assets with new variations

## Troubleshooting

**"Failed to fetch URL content"**
- Check that the URL is accessible
- Some websites block automated requests
- Try using a different page from the same site

**"No data available"**
- Clear your browser cookies and try again
- Restart the Flask application

**CSV export not working**
- Ensure you've selected at least one asset
- Check that the Flask app is still running

**Characters over limit**
- Red highlighted assets exceed Google's limits
- Edit the text manually before using
- Or choose different assets from the same section

## Command Line Tools

The original command-line tools are still available:

### View Example
```bash
python3 example_template.py
```

### Interactive CLI Generator
```bash
python3 google_ads_generator.py
```

### Test Ad Copy Generator
```bash
python3 ad_copy_generator.py
```

## Requirements

- Python 3.7 or higher
- Flask 3.0.0
- BeautifulSoup4 4.12.2
- Requests 2.31.0

All dependencies are listed in `requirements.txt` and installed automatically by the start script.

## Development

### Running in Development Mode

The app runs with Flask's debug mode enabled by default, which provides:
- Auto-reload on code changes
- Detailed error messages
- Debug toolbar

### Extending the Tool

**Add new ad sections:**
1. Edit `ad_copy_generator.py`
2. Add section to `generate_rsa_headlines()` and `generate_rsa_descriptions()`
3. Update the section colors in `rsa_editor.html` if desired

**Customize generation logic:**
- Modify the `AdCopyGenerator` class in `ad_copy_generator.py`
- Update template patterns in `_get_category()` method
- Adjust character trimming logic in `_trim_to_length()`

## Security Notes

- This tool should be run locally for security
- Do not expose port 5001 to the internet without authentication
- Sessions are used to store temporary data
- No data is permanently stored or transmitted externally

## Future Features

- [ ] Performance Max Asset Group editor
- [ ] AI-powered generation using GPT/Claude API
- [ ] Save/load asset sets
- [ ] Performance tracking integration
- [ ] Bulk URL processing
- [ ] Custom templates and sections
- [ ] Multi-language support

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the original specifications in `ROK _ Google Ads Text Asset Generation.docx`
- Test with the example template first to ensure setup is correct

## License

Internal tool for ROK Google Ads campaign creation.

---

**Ready to create amazing Google Ads?** Run `./start.sh` and get started!
