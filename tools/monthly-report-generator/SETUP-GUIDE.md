# Setup Guide - Enhanced Monthly Report Generator

This guide will walk you through setting up the automated monthly report generator with professionally formatted slides.

## Overview

The enhanced version creates Google Slides with:
- **Branded tables** with Estate Blue (#00333D) headers and Stone (#E5E3DB) backgrounds
- **Professional formatting** matching your September 2025 deck
- **Editable native tables** (not images) that you can modify directly
- **Full automation** from data query to finished presentation

## One-Time Setup (15-20 minutes)

### Prerequisites

- Python 3.7 or higher installed
- Google account with Drive access
- Admin access to Google Cloud Console (or permission to create projects)

### Step 1: Run Setup Script

```bash
cd /Users/administrator/Documents/PetesBrain/tools/monthly-report-generator
python3 setup_google_api.py
```

The setup script will guide you through:
1. Creating a Google Cloud project
2. Enabling Google Slides and Drive APIs
3. Creating a service account
4. Downloading credentials
5. Sharing a Drive folder with the service account
6. Installing Python dependencies

**Important**: Follow each step carefully, especially Step 6 (sharing the folder).

### Step 2: Test the Setup

Generate a test presentation to verify everything works:

```bash
python3 generate_devonshire_slides.py --month 2025-10
```

If successful, you'll see:
```
✅ Presentation created successfully!
🔗 Presentation ID: [ID]
🔗 URL: https://docs.google.com/presentation/d/[ID]
```

Open the URL to see your test presentation with branded tables.

### Step 3: Verify Formatting

Open the generated presentation and check:
- ✅ Table headers are Estate Blue (#00333D) with white text
- ✅ Table data cells are Stone (#E5E3DB) with dark gray text
- ✅ Tables are editable (click on them to edit)
- ✅ Text is readable and professional-looking

## Monthly Usage (5 minutes)

Once set up, generating monthly reports is simple:

### Generate Report

Wait until 3-5 days after month end (data finalization), then run:

```bash
cd /Users/administrator/Documents/PetesBrain/tools/monthly-report-generator
python3 generate_devonshire_slides.py --month 2025-11
```

Replace `2025-11` with the month you want to generate.

### What Happens

The script will:
1. Query Google Ads API for the specified month
2. Calculate all performance metrics
3. Generate insights and recommendations
4. Create a new Google Slides presentation
5. Format tables with your brand colors
6. Return a link to the finished presentation

### Review and Deliver

1. Open the generated presentation link
2. Review data accuracy
3. Make any final adjustments (all tables are editable)
4. Copy slides into your shared deck (with SEO/other sections)
5. Send to Gary at A Cunning Plan

**Total time**: ~5 minutes (vs 2-3 hours manual)

## Customization

### Change Colors

To modify the brand colors, edit `generate_devonshire_slides.py`:

```python
# Brand Colors (lines 30-34)
ESTATE_BLUE = {'red': 0, 'green': 0.2, 'blue': 0.24}  # #00333D
STONE = {'red': 0.898, 'green': 0.890, 'blue': 0.859}  # #E5E3DB
WHITE = {'red': 1.0, 'green': 1.0, 'blue': 1.0}
DARK_GRAY = {'red': 0.2, 'green': 0.2, 'blue': 0.2}
```

RGB values are 0-1 range (not 0-255). To convert hex to RGB:
- Divide each hex pair by 255
- Example: #00333D = RGB(0, 51, 61) = (0, 0.2, 0.24)

### Custom Presentation Name

```bash
python3 generate_devonshire_slides.py --month 2025-10 \
    --output-name "My Custom Title"
```

### Different Credentials Path

```bash
python3 generate_devonshire_slides.py --month 2025-10 \
    --credentials /path/to/credentials.json
```

## Troubleshooting

### "Credentials file not found"

**Solution**: Run `python3 setup_google_api.py` to set up credentials.

### "Permission denied" or "Access not configured"

**Solution**:
1. Verify you enabled both Google Slides API and Google Drive API
2. Check that you shared the Drive folder with the service account email
3. Wait 1-2 minutes for permissions to propagate

### "Module not found" errors

**Solution**: Install dependencies:
```bash
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Tables don't look right

**Solution**:
1. Check that colors are defined correctly (RGB 0-1 range)
2. Verify font sizes are reasonable (8-12pt for data, 18-24pt for titles)
3. Adjust table dimensions in the script if needed

### Can't find generated presentation

**Solution**:
1. Check the Google Drive folder you shared with the service account
2. Look for presentations created by `[service-account-name]@[project].iam.gserviceaccount.com`
3. Search Drive by title: "Devonshire Paid Search - [Month]"

## Advanced: Integration with Claude Code

For even faster generation, you can ask Claude Code:

```
"Generate the November 2025 Devonshire report"
```

Claude Code will:
1. Run the Python script
2. Query the Google Ads data
3. Generate the presentation
4. Return the link

This combines the automation with AI assistance for maximum efficiency.

## File Locations

- **Main script**: `/tools/monthly-report-generator/generate_devonshire_slides.py`
- **Setup script**: `/tools/monthly-report-generator/setup_google_api.py`
- **Credentials**: `~/Documents/PetesBrain/shared/credentials/google-slides-credentials.json`
- **Documentation**: `/tools/monthly-report-generator/` (this guide and others)

## Support

If you encounter issues:
1. Check this troubleshooting section
2. Review the setup script output for errors
3. Verify all Google Cloud Console settings
4. Test with a simple example month first

## Next Steps

Once you've completed setup and tested successfully:
1. Generate the October 2025 report with proper formatting
2. Review and compare to your September 2025 manual deck
3. Adjust colors or formatting if needed
4. Use for November 2025 onwards

The initial setup takes 15-20 minutes, but saves 2-3 hours every month thereafter.

---

**Last Updated**: 2025-11-02
**Version**: 2.0 (Enhanced with full API support)
