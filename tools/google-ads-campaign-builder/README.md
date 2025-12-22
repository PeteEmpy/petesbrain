# Google Ads Campaign Builder

**Status**: ✅ AI Generation Features Complete | ⏳ MCP Integration Pending (Dec 15, 2025)

Web-based interface for creating Google Ads campaigns, ad groups, and Performance Max asset groups with AI-powered keyword and ad copy generation.

## Features

- ✅ **Progressive disclosure UI** - Step-by-step guided workflow
- ✅ **Client selection** - Choose from configured clients
- ✅ **Campaign type filtering** - Performance Max or Search
- ✅ **Flexible creation** - New campaigns or add to existing
- ✅ **AI-powered keyword generation** - Intelligent, conversion-focused keywords with quality scoring
- ✅ **AI-powered ad copy generation** - Professional RSAs and asset group text
- ✅ **Model selection** - Choose Haiku (economical) or Sonnet (premium quality) per generation
- ✅ **Cost tracking** - Real-time display of tokens used and API costs
- ✅ **Modal selection interface** - Review and select AI-generated content
- ✅ **Keyword deduplication** - Filters duplicates (placeholder for MCP activation)
- ✅ **Safety first** - All entities created in PAUSED state
- ⏳ **MCP integration** - Direct Google Ads API calls (Dec 15, 2025)

## What You Can Create

### New Campaigns
- Search campaigns with Target ROAS or Target CPA bidding
- Performance Max campaigns with Target ROAS or Target CPA bidding
- Custom budgets and location targeting

### Ad Groups (Search Campaigns)
- Add ad groups to existing Search campaigns
- Set Max CPC bids (optional for Smart Bidding)
- Created in PAUSED state for safety

### Asset Groups (Performance Max Campaigns)
- Add asset groups to existing Performance Max campaigns
- Text assets: headlines (3-5), long headlines (1-5), descriptions (2-5)
- Business name and final URLs
- **Note**: Images and videos must be added manually in Google Ads UI

## Requirements

- Python 3.8+
- Flask 3.0.0+
- Virtual environment (`.venv`)
- **ANTHROPIC_API_KEY** environment variable (for AI generation features)
  - Must be set in your shell profile (`~/.zshrc` or `~/.bashrc`)
  - Requires active Anthropic API credits
  - Top up credits at: https://console.anthropic.com/settings/plans
  - **Cost control**: Defaults to Haiku model (12x cheaper than Sonnet)
- MCP Google Ads server configured (for production use Dec 15+)

## Usage

### Quick Start

```bash
cd tools/google-ads-campaign-builder
./start.sh
```

Open http://127.0.0.1:5003 in your browser.

### Workflow

1. **Select Client** - Choose client from dropdown
2. **Choose Campaign Type** - Performance Max or Search
3. **New or Existing** - Create new campaign or add to existing
4. **Fill Details** - Complete the appropriate form
5. **Submit** - Entity created in PAUSED state

### Safety Features

- ✅ All campaigns created with `status: PAUSED`
- ✅ All ad groups created with `status: PAUSED`
- ✅ All asset groups created with `status: PAUSED`
- ✅ Review in Google Ads UI before enabling
- ✅ No accidental spend or impressions

### AI Model Selection & Cost Management

**Default Model: Haiku** (Economical)
- $0.25 per 1M input tokens, $1.25 per 1M output tokens
- Fast generation (~15-20 seconds)
- 70-90% cost savings vs Sonnet
- Ideal for most use cases

**Premium Option: Sonnet** (Maximum Quality)
- $3.00 per 1M input tokens, $15.00 per 1M output tokens
- Slower generation (~20-30 seconds)
- Higher quality, more nuanced copy
- Use when quality is critical

**How to Use:**
1. Each modal (Keywords, RSA, Asset Groups) has radio buttons
2. **Haiku** is pre-selected by default
3. Switch to **Sonnet** if you need premium quality
4. Cost is displayed after generation: `Model • X,XXX tokens • Cost: $0.XXXX`

**Example Costs (Keyword Generation for 25 keywords):**
- Haiku: ~2,500 tokens → ~$0.0015 per generation
- Sonnet: ~2,500 tokens → ~$0.0180 per generation

## Technical Details

### Architecture

- **Frontend**: HTML/CSS/JavaScript (progressive disclosure)
- **Backend**: Flask (Python)
- **API Integration**: Google Ads MCP server tools
- **Port**: 5003

### MCP Tools Used

- `mcp__platform-ids__get_client_platform_ids` - Get customer ID from client name
- `mcp__google-ads__run_gaql` - List existing campaigns
- `mcp__google-ads__create_campaign` - Create new campaigns
- `mcp__google-ads__create_ad_group` - Create new ad groups
- `mcp__google-ads__create_asset_group` - Create new asset groups

### File Structure

```
google-ads-campaign-builder/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── start.sh               # Startup script
├── templates/
│   └── index.html         # Main UI template
└── static/
    ├── css/
    │   └── style.css      # Styling (matches Google Ads Text Generator)
    └── js/
        └── app.js         # Progressive disclosure logic
```

## Development Status

### ✅ Phase 1: UI Complete (Nov 17, 2025)
- Progressive disclosure interface
- Client/campaign type selection
- Form validation
- Visual design matching Google Ads Text Generator
- Checkbox system for multi-selection

### ✅ Phase 2: AI Generation Complete (Nov 17, 2025)
- AI-powered keyword generation with quality scoring
- AI-powered RSA headline and description generation
- AI-powered asset group text generation
- **Model selection**: Haiku (economical) vs Sonnet (premium quality)
- **Cost tracking**: Real-time token usage and cost display
- Modal selection interface for reviewing AI content
- Landing page content extraction with BeautifulSoup
- Keyword deduplication logic (placeholders for MCP activation)
- Match type intelligence (EXACT/BROAD preferred)
- Intent scoring (high/medium/low conversion potential)
- Relevance scoring (0-1 scale)

### ⏳ Phase 3: MCP Integration (Pending Dec 15, 2025)
- Direct calls to Google Ads MCP server tools
- Campaign listing via GAQL queries
- Entity creation with proper error handling
- Real keyword deduplication with account data
- Search volume integration via Keyword Planner

### 📅 Phase 4: Testing (Pending - Requires API Credits)
- Full end-to-end testing with real landing pages
- Quality assessment of AI-generated keywords
- Quality assessment of AI-generated ad copy
- Validate all creation workflows
- Error handling edge cases

### 📅 Phase 5: Production (Scheduled Dec 15, 2025)
- Align with MCP server write operations activation
- Team training
- Documentation finalization

## Known Limitations

1. **Asset Groups**: Text assets only - images/videos must be added manually in Google Ads UI
2. **MCP Server**: Write operations coded but not yet active (Dec 15, 2025)
3. **Campaign Types**: Currently supports Search and Performance Max only
4. **AI Generation**: Requires active Anthropic API credits for keyword/ad copy generation
5. **Keyword Deduplication**: Uses placeholder logic until MCP activation (Dec 15, 2025)
6. **Extensions**: Sitelinks and callouts UI complete but MCP integration pending

## Future Enhancements

- [x] AI-powered keyword generation ✅ (Nov 17, 2025)
- [x] AI-powered RSA generation ✅ (Nov 17, 2025)
- [x] AI-powered asset group generation ✅ (Nov 17, 2025)
- [x] Keyword deduplication logic ✅ (placeholder until Dec 15)
- [ ] Sitelink and callout creation for campaigns
- [ ] AI-powered sitelink and callout generation
- [ ] Sequential creation (campaign → ad group → keywords/RSAs in one flow)
- [ ] Bulk import from CSV/spreadsheet
- [ ] Template library for common campaign structures
- [ ] Integration with experiment tracking system
- [ ] Performance prediction using historical data

## Related Documentation

- **MCP Server Implementation**: `/infrastructure/mcp-servers/google-ads-mcp-server/IMPLEMENTATION-2025-11-14.md`
- **Build vs Buy Analysis**: `/roksys/knowledge-base/ai-strategy/2025-11-14-google-ads-campaign-automation-feasibility.md`
- **API Verification**: `/roksys/knowledge-base/ai-strategy/2025-11-14-google-ads-api-write-operations-verification.md`
- **MCP Tools Reference**: `/docs/MCP-SERVERS.md`

## Support

For questions or issues, see:
- Main documentation: `docs/CLAUDE.md` (or `CLAUDE.md` at project root)
- Troubleshooting guide: `docs/TROUBLESHOOTING.md`

---

**Last Updated**: 2025-11-17
**Status**: Development (Phase 2 - MCP Integration)
**Launch Target**: December 15, 2025 (aligned with MCP server activation)
