# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Google Ads Text Generator that creates optimized ad copy (headlines, descriptions, sitelinks, callouts, search themes) for Google Ads campaigns, specifically targeting ROAS optimization following ROK specifications.

The project has evolved to include:
1. **Original CLI tool**: Manual/programmatic generation of Google Ads assets
2. **Web scraping system**: Automated ad copy generation from website URLs
3. **Claude AI integration**: Professional copywriting using Anthropic's Claude API
4. **Flask web application**: User-friendly interface for generating ad copy
5. **Desktop application**: Native macOS app using PyWebView (standalone .app bundle)

## Architecture

### Core Components

**Ad Copy Generation Pipeline (Current - Claude API):**
```
URL Input → Website Content Fetch → Claude API Analysis → Structured JSON Response → User Selection/Export
```

**Legacy Pipeline (Rule-based generators):**
```
URL Input → Website Analysis → Content Extraction → Pattern Matching → Template Generation → User Selection/Export
```

1. **claude_copywriter.py**: AI-powered professional copywriting (PRIMARY GENERATOR)
   - Uses Anthropic Claude API for high-quality ad copy generation
   - Fetches website content and sends to Claude for analysis
   - Loads ROK specifications from `ROK _ Google Ads Text Asset Generation.txt`
   - Returns structured JSON with headlines, descriptions, sitelinks, callouts
   - Requires `ANTHROPIC_API_KEY` environment variable
   - Produces human-quality copy that follows ROK best practices

2. **ad_copy_generator.py**: Content-first ad copy generation (LEGACY/FALLBACK)
   - Takes URL, extracts ALL usable phrases from page content
   - Generates 50 headlines + 50 descriptions across 5 sections:
     - **Benefits**: Why customers need it (pain relief, comfort focused)
     - **Technical**: Product specifics (materials, specifications, certifications)
     - **Quirky**: Engaging, personality-driven copy
     - **CTA**: Action-oriented (not aggressive, persuasive)
     - **Brand**: Company/product positioning
   - Uses phrase extraction with benefit/technical keyword matching
   - Trims to Google Ads limits: 30 chars (headlines), 90 chars (descriptions)

3. **website_analyzer.py**: Deep website analysis (USED BY LEGACY GENERATORS)
   - Crawls homepage + up to 5 key pages (about, products, shop)
   - Extracts: headings (h1/h2/h3), lists, paragraphs, meta descriptions
   - Synthesizes insights: brand name, products, benefits, technical features, tone
   - Uses pattern matching to identify product categories and benefit keywords

4. **professional_ad_writer.py**: ROK-guideline focused writer (LEGACY)
   - Takes insights from website_analyzer.py
   - Generates copy following strict ROK best practices
   - Hardcoded templates with brand/product substitution
   - Used for high-quality, guideline-compliant output

5. **google_ads_generator.py**: Original manual generation tool
   - Interactive CLI for manual input
   - Validates character limits strictly
   - Generates CSV exports for Google Ads Editor

6. **app.py**: Flask web application
   - Routes: `/` (home), `/analyze` (processes URL with Claude API), `/rsa_editor` (selection UI)
   - Uses global `latest_result` variable (no session storage) to pass data between requests
   - Primary generator: `ClaudeCopywriter` (Claude API)
   - Export endpoints: `/export_rsa_csv`, `/get_copy_text`
   - JavaScript loads data dynamically via `/get_latest_data` endpoint

7. **desktop.py**: Desktop application wrapper
   - Wraps Flask app using PyWebView for native window
   - Starts Flask in background daemon thread
   - Creates desktop window (1200x900, resizable)
   - No browser required - all-in-one executable
   - Can be packaged as standalone .app using PyInstaller

### Key Design Patterns

**Content Extraction Strategy:**
- Extracts ALL headings, lists, bold text, paragraphs from pages
- Cleans text (removes extra whitespace, special chars)
- Deduplicates phrases using lowercase comparison
- Stores in `all_phrases[]` for later use

**Ad Copy Generation Strategy:**
- **Primary method (Claude API)**: Uses AI to analyze website and write professional copy following ROK specs
- **Legacy method (ad_copy_generator.py)**: Content-first approach using actual page phrases
- **Keyword filtering** (legacy): Matches phrases to sections using keyword lists
- **Template fallback** (legacy): Uses templates only when insufficient content extracted
- **Word-boundary trimming**: Cuts at last space to avoid truncating words

**Character Limit Enforcement:**
- Headlines: **25-30 characters** (strictly enforced with validation)
  - Minimum 25 chars to maximize ad space
  - Maximum 30 chars (Google Ads hard limit)
  - Target: 27-30 characters
  - Post-processing filters out items outside this range
- Descriptions: **70-90 characters** (strictly enforced with validation)
  - Minimum 70 chars to maximize ad space
  - Maximum 90 chars (Google Ads hard limit)
  - Target: 85-90 characters
  - Post-processing filters out items outside this range
- Sitelink headlines: 25 characters max
- Sitelink descriptions: 35 characters max
- Callouts: 25 characters max

## Development Commands

### Environment Setup

**Set up API key for Claude AI (REQUIRED for web/desktop app):**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Add to `~/.bashrc` or `~/.zshrc` for persistence.

### Running the Application

**Option 1: Flask web app (browser-based):**
```bash
./start.sh
```
This will:
- Create venv if missing
- Install requirements
- Launch Flask on http://localhost:5001

**Option 2: Desktop app (native window):**
```bash
python3 desktop.py
```
This will:
- Start Flask in background thread
- Open native window using PyWebView
- No browser needed

**Option 3: Manual start (if start.sh fails):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py  # or: python3 desktop.py
```

### Building Desktop Application

**Build standalone .app for macOS:**
```bash
./build.sh
```
Creates: `dist/Google Ads Text Generator.app`

**Manual build:**
```bash
pip install -r requirements.txt
pyinstaller desktop.spec
```

See DESKTOP_BUILD.md for detailed build instructions.

### Testing

**Test URL analysis (mock data):**
```bash
python3 test_url_analysis.py
```

**Test with real URL:**
```bash
python3 ad_copy_generator.py  # Will prompt for URL in interactive mode
```

**Test professional writer:**
```bash
python3 professional_ad_writer.py
```

**Test website analyzer:**
```bash
python3 website_analyzer.py
```

**View example output:**
```bash
python3 example_template.py
```

### Debugging

**Kill Flask if port 5001 in use:**
```bash
lsof -ti:5001 | xargs kill -9
```

**Check what's running on port 5001:**
```bash
lsof -i:5001
```

## Important Implementation Details

### Claude API Integration

**How it works (claude_copywriter.py):**
1. Fetches website content (title, meta description, H1/H2 tags, paragraphs, list items)
2. Loads ROK specifications from `ROK _ Google Ads Text Asset Generation.txt`
3. Constructs prompt with website content + ROK specs + additional user context
4. Calls Claude API with structured output request (JSON format)
5. Parses JSON response containing headlines, descriptions, sitelinks, callouts
6. Returns structured data to Flask app

**Expected JSON structure:**
```python
{
    "url": "https://example.com",
    "page_info": {
        "brand": "Brand Name",
        "product": "Product Name",
        "category": "Category"
    },
    "headlines": {
        "benefits": [...],      # 10 headlines
        "technical": [...],     # 10 headlines
        "quirky": [...],        # 10 headlines
        "cta": [...],           # 10 headlines
        "brand": [...]          # 10 headlines
    },
    "descriptions": {
        "benefits": [...],      # 10 descriptions
        "technical": [...],     # 10 descriptions
        "quirky": [...],        # 10 descriptions
        "cta": [...],           # 10 descriptions
        "brand": [...]          # 10 descriptions
    },
    "sitelinks": [...],         # 4-6 sitelinks
    "callouts": [...]           # 5-10 callouts
}
```

### Tone-of-Voice Analysis and Quality Control

**Critical improvements made to ensure ad copy matches brand voice:**

The Claude API prompt (claude_copywriter.py:120-221) includes comprehensive analysis instructions:

**A) Tone of Voice Analysis:**
- Formality level (professional/casual/friendly/authoritative)
- Emotional tone (warm/clinical/energetic/calm/playful)
- Language style (simple/technical/poetic/direct/conversational)
- Actual word choices and sentence structure from website
- Humor style and personality indicators
- Question vs statement vs exclamation usage
- **Goal**: Ad copy MUST sound like same person who wrote website

**B) Target Audience Analysis:**
- Demographics: age, gender, income, location
- Psychographics: values, lifestyle, priorities
- Pain points: what problem they're solving
- Motivations: why choose THIS product/service
- Language the audience actually uses
- Decision triggers: what makes them buy NOW
- **Goal**: Write as if talking to ONE specific person in audience

**C) Enhanced Content Extraction:**
- H1, H2, H3 tags (8+20+15 items)
- Button/CTA text (reveals brand's action language)
- Paragraphs (35 items - more for tone analysis)
- List items (40 items - features/benefits)
- Meta descriptions and titles

**D) Character Limit Examples in Prompt:**
- Shows concrete examples of 25-30 char headlines
- Shows concrete examples of 70-90 char descriptions
- Includes both good (✓) and bad (✗) examples
- Emphasizes maximizing character usage

**E) Post-Processing Validation:**
After Claude generates content, code validates every item (claude_copywriter.py:279-339):
```python
# Headlines: Must be 25-30 characters
if char_count > 30:
    # Rejected - over Google Ads limit
elif char_count < 25:
    # Rejected - wastes ad space
else:
    # Valid - kept for user selection

# Descriptions: Must be 70-90 characters
if char_count > 90:
    # Rejected - over Google Ads limit
elif char_count < 70:
    # Rejected - wastes ad space
else:
    # Valid - kept for user selection
```

Filtered items are logged with reason for transparency.

**F) API Parameters:**
- Model: `claude-sonnet-4-20250514`
- Max tokens: 12000 (allows thorough analysis)
- Temperature: 0.8 (balanced creativity and accuracy)

### URL Fetching Limitations

**Will work:**
- Small to medium business websites
- E-commerce sites without heavy bot protection
- Standard HTML content sites

**Won't work:**
- Major brands (Nike, Adidas, Apple) - they block bots
- JavaScript-heavy SPAs (React, Vue without SSR)
- Sites with Cloudflare/aggressive bot detection
- Authentication-required pages

See TESTING_GUIDE.md for full details.

### Content Extraction Patterns

**Category detection** (ad_copy_generator.py:410-444):
```python
categories = {
    "bag": "Bags", "heat": "Heat Products", "bottle": "Bottles",
    "shoes": "Footwear", "clothing": "Clothing", ...
}
```
Searches URL + title + description + all_phrases for keywords.

**Benefit keyword matching** (ad_copy_generator.py:187-194):
```python
benefit_words = ['for', 'relief', 'comfort', 'support', 'help', 'ease',
                 'sooth', 'relax', 'warm', 'hot', 'cold', 'pain']
```

**Technical keyword matching** (ad_copy_generator.py:211-218):
```python
tech_words = ['made', 'designed', 'manufactured', 'original', 'traditional',
              'shaped', 'size', 'material', 'fabric']
```

### Data Flow in Web App

Flask app uses global variable instead of sessions (app.py:26):
```python
latest_result = None  # Stores latest generated ad data
```

Flow:
1. User submits URL at `/` → POST to `/analyze`
2. `/analyze` generates ad copy via Claude API, stores in `latest_result`, returns JSON
3. Frontend redirects to `/rsa_editor`
4. JavaScript on editor page calls `/get_latest_data` to retrieve stored data
5. User selects headlines/descriptions → POST to `/export_rsa_csv` or `/get_copy_text`

### Output Formats and Selection Limits

**RSA Selection Requirements:**
- **Minimum**: 3 headlines, 2 descriptions (enforced on export)
- **Maximum**: 15 headlines, 4 descriptions (enforced by UI)
- Users cannot select more than the maximum
- Export functions validate minimum requirements

**RSA CSV Format (per ROK specifications):**

Implemented in app.py:100-172

```csv
Ad type,Final URL,Path 1,Path 2,Headline 1,Headline 2,...,Headline 15,Description 1,...,Description 4
Responsive search ad,https://example.com,,,Headline text,...,,,Description text,...,
```

Key implementation details:
- No Campaign or Ad group columns (user requirement)
- All 15 headline columns + 4 description columns present
- Empty cells for unused slots
- Automatically limits to first 15 headlines and 4 descriptions
- Tab-separated for easy paste into spreadsheets

**Copy to Clipboard Format:**

Matches CSV structure exactly (app.py:173-223):
- Tab-separated values
- Same header row as CSV
- Same data row structure
- Can be pasted directly into Google Ads Editor or spreadsheets

**Legacy Formats (not used in current app):**

2. **Sitelink Extensions CSV:**
```
Campaign,Ad group,Sitelink text,Description line 1,Description line 2,Final URL,Device preference,Start date,End date,Schedule
```

3. **Callout Extensions CSV:**
```
Campaign,Ad group,Callout text,Device preference,Start date,End date,Schedule
```

## Common Tasks

### Adding a New Ad Section

1. Update sections list in both generators
2. Add generation method (e.g., `_generate_custom_headlines()`)
3. Update templates if using template approach
4. Add to output formatting in `generate_output()`

### Modifying Character Limits

Update constants in google_ads_generator.py:
```python
HEADLINE_MAX = 30
DESCRIPTION_MAX = 90
SITELINK_HEADLINE_MAX = 25
SITELINK_DESC_MAX = 35
```

### Adding New Category Detection

Add to categories dict in `_get_category()` (ad_copy_generator.py:417-434).

### Improving Content Extraction

Modify `_extract_all_phrases()` in ad_copy_generator.py:129-171.
Current sources: title, meta description, h1/h2/h3, lists, strong text.

### UI/UX Improvements

**Reduced Spacing for Better Visibility (templates/rsa_editor_dynamic.html):**

All spacing has been optimized to show more items per screen:
- Body padding: 20px → 15px
- Header padding: 30px → 20px, margin: 30px → 20px
- Panel padding: 20px → 15px
- Section margin: 30px → 20px
- H3 margin: 15px → 10px, font-size: 16px → 14px
- Asset items: padding 12px → 8px 10px, margin 8px → 4px
- Checkbox size: 20px → 18px
- Text font-size: 14px → 13px
- Character count: font-size 12px → 11px

**Selection Limit Enforcement (JavaScript):**
```javascript
// Headlines: max 15
if (isHeadline && headlineCount > 15) {
    this.checked = false;
    showNotification('Maximum 15 headlines allowed for RSA ads', 'error');
    return;
}

// Descriptions: max 4
if (isDescription && descriptionCount > 4) {
    this.checked = false;
    showNotification('Maximum 4 descriptions allowed for RSA ads', 'error');
    return;
}
```

**Visual Feedback:**
- Counter shows: "0 / 15" and "0 / 4"
- Numbers turn red when limit reached
- Panel headers show: "Select 3-15 for RSA" and "Select 2-4 for RSA"
- Checkbox disabled via JavaScript when limit reached

**Export Validation:**
- Won't export unless minimum met (3 headlines, 2 descriptions)
- Clear error messages guide user to requirements

## File Organization

**Core modules:**
- `ad_copy_generator.py` - Main content-first generator
- `google_ads_generator.py` - Manual/CLI generator with validation
- `professional_ad_writer.py` - ROK-compliant writer
- `website_analyzer.py` - Deep website analysis

**Web app:**
- `app.py` - Flask application (uses Claude API via claude_copywriter.py)
- `claude_copywriter.py` - Claude API integration for AI-powered copywriting
- `templates/` - HTML templates (index.html, rsa_editor_dynamic.html, asset_group_editor.html)

**Desktop app:**
- `desktop.py` - PyWebView desktop wrapper
- `desktop.spec` - PyInstaller configuration for macOS .app
- `build.sh` - Build script for packaging standalone app

**Documentation:**
- `README.md` - User-facing documentation
- `README_WEB_APP.md` - Web app specific docs
- `DESKTOP_BUILD.md` - Desktop app build and distribution guide
- `TESTING_GUIDE.md` - URL testing and troubleshooting
- `CHANGELOG.md` - Version history
- `CLAUDE.md` - This file (for Claude Code)

**Scripts:**
- `start.sh` - Quick start script for Flask web app
- `build.sh` - Build script for desktop .app

**Examples/Tests:**
- `example_template.py` - Complete working example
- `test_url_analysis.py` - Unit test with mock data
- `example_google_ads_assets.txt/csv` - Sample output

**ROK Specifications:**
- `ROK _ Google Ads Text Asset Generation.txt` - Complete ROK spec with output formats

**Legacy/Superseded:**
- `ad_copy_generator_old.py` - Previous version (reference only)
- `url_analyzer.py` - Earlier analyzer (superseded by website_analyzer.py)
- `app_old.py` - Previous app version (superseded by current app.py with Claude API)
- `professional_copywriter.py` - Earlier copywriter (superseded by claude_copywriter.py)
- `smart_ad_generator.py` - Legacy generator

## ROK Specifications

This tool follows ROK Google Ads best practices:

**The 5 Content Sections:**
1. Benefits - Emotional, outcome-focused
2. Technical - Specific advantages with benefit framing
3. Quirky - Engaging with appropriate humor
4. CTA - Persuasive but not aggressive
5. Brand - Company positioning with personality

**Best Practices:**
- Use full character limits when possible
- Specific to client and product (not generic)
- No Dynamic Keyword Insertion (DKI)
- No customizers
- Focus on benefits over features
- Test multiple variations
- Mobile-first (key info in first 20-25 chars)

## Dependencies

```
Flask==3.0.0
beautifulsoup4==4.12.2
requests==2.31.0
pywebview==4.4.1
pyinstaller==6.3.0
anthropic==0.39.0
```

Python 3.6+ required. No database dependencies.

**Required Environment Variables:**
- `ANTHROPIC_API_KEY` - Required for Claude API integration (web/desktop app)

## Recent Improvements (Latest Session)

### 1. Tone-of-Voice Matching
**Problem**: Ad copy was generic and didn't match brand's actual voice or target audience.

**Solution**: Enhanced Claude API prompt with deep analysis:
- Analyzes formality, emotional tone, language style from website content
- Studies actual word choices, sentence structure, humor style
- Identifies target audience demographics and psychographics
- Extracts button/CTA text to understand brand's action language
- Instruction: "Ad copy MUST sound like same person who wrote website"

**Location**: `claude_copywriter.py:120-221`

### 2. Strict Character Limit Enforcement
**Problem**: Some headlines/descriptions were over limits or too short (wasting space).

**Solution**: Three-part enforcement:
1. **Concrete examples in prompt** showing ideal length
2. **Minimum requirements**: Headlines 25-30 chars, descriptions 70-90 chars
3. **Post-processing validation** that filters invalid items (claude_copywriter.py:279-339)

**Results**: Every item now falls within optimal range.

### 3. Fixed CSV Export Format
**Problem**: CSV format didn't match user requirements.

**Solution**:
- Removed Campaign and Ad group columns per user request
- Format: `Ad type,Final URL,Path 1,Path 2,Headline 1-15,Description 1-4`
- Copy to clipboard matches CSV format exactly (tab-separated)

**Location**: `app.py:100-172` (export), `app.py:173-223` (copy)

### 4. Selection Limit Enforcement
**Problem**: Users could select unlimited items, but RSA has strict limits.

**Solution**:
- UI enforces max 15 headlines, 4 descriptions
- Export validates min 3 headlines, 2 descriptions
- Visual feedback: counters show "X / 15" and turn red at limit
- Panel headers show requirements: "Select 3-15 for RSA"

**Location**: `templates/rsa_editor_dynamic.html:387-452`

### 5. Reduced UI Spacing
**Problem**: Too much whitespace, couldn't see enough items per screen.

**Solution**: Reduced all spacing by 25-40%:
- Asset items: 12px → 8px padding, 8px → 4px margin
- Sections, panels, headers all reduced
- Result: 30-40% more items visible

**Location**: `templates/rsa_editor_dynamic.html:95-195`

### Key Takeaways for Future Development

1. **Always validate character limits** - Claude AI is good but not perfect at counting
2. **Tone matters more than you think** - Generic copy performs poorly
3. **Extract MORE content** - More website text = better tone analysis
4. **Show clear limits in UI** - Users need to know constraints upfront
5. **Match export formats exactly** - No assumptions, follow specs precisely