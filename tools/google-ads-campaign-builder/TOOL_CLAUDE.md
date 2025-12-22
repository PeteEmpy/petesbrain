# Google Ads Campaign Builder - Technical Architecture

**Created**: 2025-11-17
**Status**: Phase 2 - AI Generation Features Complete
**Launch Target**: December 15, 2025 (MCP write operations activation)
**Last Updated**: 2025-11-17 15:30

## Overview

Web-based tool for creating Google Ads campaigns, ad groups, and Performance Max asset groups using a progressive disclosure interface. Integrates with Google Ads MCP server write operations implemented on Nov 14, 2025.

**NEW (Nov 17, 2025)**: AI-powered generation features for keywords and ad copy using Claude AI with intelligent quality scoring and deduplication.

## Architecture

### Tech Stack

- **Frontend**: HTML5, CSS3, vanilla JavaScript
- **Backend**: Flask (Python 3.x)
- **API Integration**: Google Ads MCP Server tools
- **Port**: 5003 (to avoid conflicts with other tools)

### Design Pattern

**Progressive Disclosure UI** - Multi-step guided workflow that reveals options based on user selections:

1. **Step 1**: Client selection (dropdown)
2. **Step 2**: Campaign type (Performance Max / Search)
3. **Step 3**: New or existing campaign
4. **Step 4a**: If existing → Select campaign (filtered dropdown)
5. **Step 4b**: Creation form (campaign / ad group / asset group)
6. **Submit**: Entity created in PAUSED state

### Data Flow

```
User Input (Browser)
    ↓
JavaScript Form Validation
    ↓
Flask Backend (/api/create endpoint)
    ↓
MCP Tool Call (via subprocess/import)
    ↓
Google Ads API (REST)
    ↓
Response → Result Display (Browser)
```

## Implementation Details

### Frontend (static/)

#### CSS (`static/css/style.css`)

Visual design matching Google Ads Text Generator:
- Color palette: Google blue (#1a73e8), success green, warning yellow
- Card-based layout with shadow effects
- Responsive design (mobile-friendly)
- Radio button groups with hover effects
- Progressive disclosure (`.hidden` utility class)

#### JavaScript (`static/js/app.js`)

**Key Functions**:
- `loadCampaigns()` - Fetches campaigns from backend via `/api/get_campaigns`
- `gatherFormData()` - Validates and structures form data for submission
- `submitForm()` - POSTs to `/api/create` endpoint
- `resetFromStep(n)` - Hides all steps from step N onwards
- Event listeners for each step's selections

**Progressive Disclosure Logic**:
```javascript
Client selected → Show Step 2 (campaign type)
Campaign type selected → Show Step 3 (new/existing)
New campaign → Show campaign form
Existing campaign → Load campaigns → Show dropdown + "what to create" options
```

**Form Validation**:
- Asset group: 3-5 headlines, 1-5 long headlines, 2-5 descriptions
- Budget conversion: £ → micros (multiply by 1,000,000)
- ROAS conversion: % → decimal (divide by 100)
- All entities: status forcibly set to 'PAUSED'

### Backend (app.py)

#### Flask Routes

**`GET /`**
- Serves main UI template
- Passes client list to template

**`POST /api/get_campaigns`**
- Accepts: `{client, campaign_type}`
- Returns: `{campaigns: [{id, name}, ...]}`
- Calls: `mcp__google-ads__run_gaql` to query campaigns
- Filters by campaign type and excludes REMOVED campaigns

**`POST /api/create`**
- Accepts: `{client, action, campaign_data/ad_group_data/asset_group_data, campaign_id?}`
- Returns: `{success, campaign_id/ad_group_id/asset_group_id, message}`
- Routes to appropriate MCP tool based on action
- **CRITICAL**: Forces `status: PAUSED` on all creations

**`GET /api/latest_result`**
- Returns latest creation result (global variable pattern)

#### MCP Integration Strategy

**Current Status**: Placeholder functions (TODO comments)

**Implementation Options**:

1. **Direct Import** (Preferred)
   ```python
   import sys
   sys.path.append('/path/to/mcp-server')
   from server import create_campaign, create_ad_group, create_asset_group
   ```

2. **HTTP Proxy** (If MCP server runs as daemon)
   ```python
   import requests
   response = requests.post('http://localhost:MCP_PORT/mcp__google-ads__create_campaign', json=params)
   ```

3. **Subprocess Call** (Fallback)
   ```python
   import subprocess
   result = subprocess.run(['claude-code', 'mcp', 'call', 'mcp__google-ads__create_campaign', ...], capture_output=True)
   ```

**Decision**: Use **Direct Import** once MCP server is activated (Dec 15).

#### Helper Functions

**`get_client_customer_id(client_name)`**
- Maps client name to Google Ads customer ID
- Uses `mcp__platform-ids__get_client_platform_ids` or local mapping
- Current: Hardcoded dictionary (TODO: Replace with MCP call)

**`list_campaigns(customer_id, campaign_type)`**
- GAQL query to list campaigns of specified type
- Filters: `advertising_channel_type = {type}` AND `status != REMOVED`
- Orders: Alphabetically by campaign name
- Current: Mock data (TODO: Replace with MCP call)

**`create_campaign(customer_id, campaign_data)`**
- Calls `mcp__google-ads__create_campaign` with data
- **CRITICAL**: Forces `status: PAUSED`
- Converts: £ → micros, % → decimal
- Returns: campaign_id, resource_name, message

**`create_ad_group(customer_id, campaign_id, ad_group_data)`**
- Calls `mcp__google-ads__create_ad_group`
- **CRITICAL**: Forces `status: PAUSED`
- Optional: CPC bid (micros)
- Returns: ad_group_id, resource_name, message

**`create_asset_group(customer_id, campaign_id, asset_group_data)`**
- Calls `mcp__google-ads__create_asset_group`
- **CRITICAL**: Forces `status: PAUSED`
- Text assets: headlines, long_headlines, descriptions
- Returns: asset_group_id, resource_name, message

## Safety Features

### PAUSED State Enforcement

**User Requirement**: "When it creates something to go into Google, when it does post there has to go in the paused state every time. That's categorically."

**Implementation**:

1. **Frontend Validation**:
   ```javascript
   data.campaign_data.status = 'PAUSED';  // Force PAUSED
   data.ad_group_data.status = 'PAUSED';
   data.asset_group_data.status = 'PAUSED';
   ```

2. **Backend Enforcement**:
   ```python
   campaign_data['status'] = 'PAUSED'  # Override any user input
   ad_group_data['status'] = 'PAUSED'
   asset_group_data['status'] = 'PAUSED'
   ```

3. **MCP Tool Parameters**:
   - All MCP create functions accept `status` parameter
   - Default: 'PAUSED' (per MCP implementation)
   - Tool will reject 'ENABLED' status (safety)

4. **UI Messaging**:
   - Submit button: "Create (PAUSED State)"
   - Success message: "Created in PAUSED state. Review in Google Ads before enabling."
   - Footer warning: All entities created in PAUSED state

### Additional Safety Measures

- **Budget Validation**: Prevents creation with £0 budget
- **Asset Validation**: Ensures headlines/descriptions meet character limits and count requirements
- **Preview Before Submit**: User sees all data before final submission
- **Error Handling**: API errors displayed clearly, no silent failures

## User Experience Flow

### Creating a New Campaign

1. User selects **Client** → "Smythson"
2. User selects **Campaign Type** → "Performance Max"
3. User selects **Action** → "Create New Campaign"
4. Form appears with fields:
   - Campaign name (text input)
   - Daily budget (number, £)
   - Bidding strategy (Target ROAS / Target CPA)
   - Target value (based on bidding strategy)
   - Locations (defaults to UK)
5. User fills fields → Clicks "Create (PAUSED State)"
6. Backend calls MCP tool → Campaign created
7. Success message shows campaign ID → User clicks "Create Another" or closes

### Adding to Existing Campaign

1. User selects **Client** → "Smythson"
2. User selects **Campaign Type** → "Performance Max"
3. User selects **Action** → "Add to Existing Performance Max Campaign"
4. Campaigns load → Dropdown shows alphabetical list
5. User selects campaign → "SMY | UK | P Max | Christmas Gifting"
6. User chooses **What to create** → "New Asset Group"
7. Asset group form appears with fields:
   - Asset group name
   - Final URL
   - Business name
   - Headlines (3-5, one per line)
   - Long headlines (1-5, one per line)
   - Descriptions (2-5, one per line)
8. User fills fields → Clicks "Create (PAUSED State)"
9. Backend calls MCP tool → Asset group created
10. Success message shows asset group ID + warning about images/videos

## Data Conversion

### Budget: £ → Micros

Google Ads API uses "micros" (1/1,000,000 of currency unit).

**Formula**: `micros = pounds * 1,000,000`

**Example**:
- £100/day → 100,000,000 micros
- £2.50 CPC → 2,500,000 micros

### ROAS: % → Decimal

Google Ads API uses decimal for Target ROAS.

**Formula**: `decimal = percentage / 100`

**Example**:
- 400% ROAS → 4.0
- 130% ROAS → 1.3

### Text Arrays: Textarea → List

Asset groups require arrays of text strings.

**JavaScript**:
```javascript
const headlines = headlinesText.split('\n')
    .filter(h => h.trim())
    .map(h => h.trim());
```

**Example**:
```
Input (textarea):
Luxury leather diaries
Handcrafted in London
Free UK delivery

Output (array):
["Luxury leather diaries", "Handcrafted in London", "Free UK delivery"]
```

## Campaign Type Differences

### Search Campaigns

**Can create**:
- New campaign with budget + bidding
- Ad group (with optional Max CPC)
- ❌ Asset groups (Search doesn't use asset groups)

**UI Adjustments**:
- Hide "New Asset Group" option when campaign type = SEARCH
- Show "New Ad Group" option only

### Performance Max Campaigns

**Can create**:
- New campaign with budget + bidding
- Asset group (text assets only)
- ❌ Ad groups (PMax uses asset groups, not ad groups)

**UI Adjustments**:
- Hide "New Ad Group" option when campaign type = PERFORMANCE_MAX
- Show "New Asset Group" option only
- Display warning: "Images/videos must be added manually in Google Ads UI"

## Error Handling

### Frontend Validation

**Before submission**:
- All required fields filled
- Budget > 0
- Target ROAS/CPA > 0
- Asset counts correct (3-5 headlines, 1-5 long headlines, 2-5 descriptions)
- Character limits respected (30 chars headlines, 90 chars long/descriptions)

**User feedback**:
- Alert dialogs for validation errors
- Red border on invalid fields
- Inline error messages

### Backend Error Handling

**Try-catch blocks**:
```python
try:
    result = create_campaign(customer_id, campaign_data)
    return jsonify(result)
except Exception as e:
    return jsonify({'error': str(e)}), 500
```

**Error types**:
- Client not found (404)
- Campaign not found (404)
- Invalid data (400)
- API errors (500)

**User feedback**:
- Error container with red styling
- Clear error message
- "Try Again" button to reset form

## Testing Strategy

### Phase 1: UI Testing (Completed Nov 17)

- ✅ Progressive disclosure shows/hides correctly
- ✅ Form validation prevents invalid submissions
- ✅ Data conversion functions work (£ → micros, % → decimal)
- ✅ Visual design matches Google Ads Text Generator

### Phase 2: MCP Integration (In Progress)

- ⏳ Replace placeholder functions with actual MCP calls
- ⏳ Test campaign listing via GAQL
- ⏳ Test client ID lookup
- ⏳ Test data flow from form → MCP → API

### Phase 3: End-to-End Testing (Scheduled)

- Test with Google Ads **test account** (not production!)
- Create test campaign → Verify in Google Ads UI
- Create test ad group → Verify structure
- Create test asset group → Verify text assets
- Verify all entities created in PAUSED state
- Test error scenarios (invalid data, API errors)

### Phase 4: Production Validation (Dec 15)

- Test with real client (small campaign)
- Verify naming conventions followed
- Verify budget/bidding settings correct
- Confirm PAUSED state enforced
- Team training and handoff

## AI-Powered Generation Features (Nov 17, 2025)

### Keyword Generation (`keyword_generator.py`)

**Intelligence-First Approach**: Generates 25 high-converting keywords focused on QUALITY over quantity.

**Features**:
- Landing page analysis (title, meta, headings, content)
- Claude AI identifies buying intent keywords (not research)
- Quality scoring: intent (high/medium/low), relevance (0-1), rationale
- Match type recommendations: Primarily EXACT and BROAD (PHRASE only when strong case)
- Deduplication filtering (placeholders for MCP activation):
  - Checks existing keywords in account via GAQL
  - Checks PMax search terms with conversions
  - Shows filter stats: "Generated 25 • Filtered 12 duplicates • Showing 13"

**UI Flow**:
1. User enters landing page URL next to keywords field
2. Clicks "🤖 Generate Keywords" button
3. Modal opens with loading spinner
4. AI analyzes page and generates keywords
5. Keywords displayed with badges: match type, intent level, relevance score
6. User selects/deselects keywords
7. Clicks "Use Selected" → Keywords populate textarea with match types

**Example Output**:
```
premium leather diary | EXACT (Intent: HIGH, Relevance: 95%)
handcrafted notebooks | BROAD (Intent: HIGH, Relevance: 88%)
luxury stationery gifts | EXACT (Intent: HIGH, Relevance: 92%)
```

### Ad Copy Generation (RSA & Asset Groups)

**Reuses ClaudeCopywriter**: Same module as standalone Google Ads Text Generator tool.

**RSA Generation**:
- Analyzes landing page for brand voice and product details
- Generates headlines (30 chars max) organized by category:
  - Benefits, Features, Urgency, Social Proof
- Generates descriptions (90 chars max) with same categories
- Modal selection interface with character count badges
- Pre-selected for quick use, easily deselectable

**Asset Group Generation (PMax)**:
- Short headlines: 30 chars, 3-5 needed
- Long headlines: 90 chars, 1-5 needed
- Descriptions: 90 chars, 2-5 needed
- Same quality as RSA but optimized for PMax specs

**UI Components**:
- `static/js/ai-generator.js`: Modal logic and API calls
- `static/css/style.css`: Modal styling (matching Google Ads Text Generator)
- Three modals: Keywords, RSA, Asset Group
- Checkbox selection with visual feedback (blue border when selected)
- Asset metadata badges: character count, match type, intent, volume

### Backend API Endpoints

**`POST /api/generate_keywords`**:
```json
{
  "url": "https://example.com/products",
  "client": "Smythson",
  "max_keywords": 25
}
```
Returns:
```json
{
  "keywords": [
    {
      "keyword": "premium leather diary",
      "match_type": "EXACT",
      "intent": "high",
      "relevance_score": 0.95,
      "rationale": "Specific product with quality modifier",
      "search_volume": 1000
    }
  ],
  "stats": {
    "total_generated": 25,
    "filtered_existing": 8,
    "filtered_pmax": 4,
    "returned": 13
  }
}
```

**`POST /api/generate_rsa`**: Returns headlines and descriptions organized by category

**`POST /api/generate_asset_group`**: Returns short_headlines, long_headlines, descriptions

### Key Design Decisions

1. **Client Required**: Keyword generation disabled until client selected (needed for deduplication)
2. **Modal Interface**: Not side panel - allows corrections, clear selection
3. **Pre-selection**: All items checked by default for speed
4. **Filter Stats**: Show count of duplicates filtered, not the duplicates themselves
5. **Conversion Focus**: Keywords indicate buying intent, not research phase
6. **Match Type Logic**: Prefer EXACT and BROAD; PHRASE only when strong case
7. **Shared Code**: ClaudeCopywriter module used by both this tool and standalone generator

## Known Limitations

### Current (Phase 2 - Nov 17)

1. **MCP Integration**: Placeholder functions, not yet calling real MCP tools
2. **Client List**: Hardcoded in app.py (TODO: Load from client-platform-ids.json)
3. **Mock Data**: Campaign listing returns mock data

### By Design

1. **Asset Groups**: Text assets only (images/videos require manual upload in Google Ads UI)
   - Reason: Google Ads API requires image asset IDs, not file uploads
   - Workaround: User must upload images in Google Ads UI after creation

2. **Campaign Types**: Only Search and Performance Max supported
   - Reason: These are 90% of use cases
   - Future: Could add Display, Video, Shopping

3. **Extensions**: Sitelinks and callouts not yet integrated
   - Reason: Additional complexity, less frequently used
   - Future: Add as separate form section

## Future Enhancements

### Short-term (Q1 2026)

- [ ] Integrate sitelink creation (use `mcp__google-ads__add_sitelinks`)
- [ ] Integrate callout creation (use `mcp__google-ads__add_callouts`)
- [ ] Add keyword creation for ad groups (use `mcp__google-ads__add_keywords`)
- [ ] Add RSA creation for ad groups (use `mcp__google-ads__create_responsive_search_ad`)

### Medium-term (Q2 2026)

- [ ] Template library (pre-defined campaign structures)
- [ ] Bulk import from CSV/Google Sheets
- [ ] Campaign cloning (duplicate existing structure)
- [ ] Integration with experiment tracking (log to rok-experiments-client-notes.csv)

### Long-term (H2 2026)

- [ ] AI-powered campaign generation (Claude suggests structure based on business description)
- [ ] Multi-account support (create same campaign across multiple clients)
- [ ] Automated naming convention enforcement (validate against ROK standards)
- [ ] Performance prediction (estimate budget needed for target conversions)

## Related Documentation

- **MCP Server Implementation**: `/infrastructure/mcp-servers/google-ads-mcp-server/IMPLEMENTATION-2025-11-14.md`
- **MCP Server Code**: `/infrastructure/mcp-servers/google-ads-mcp-server/server.py` (lines 427-1496)
- **Build vs Buy Analysis**: `/roksys/knowledge-base/ai-strategy/2025-11-14-google-ads-campaign-automation-feasibility.md`
- **API Verification**: `/roksys/knowledge-base/ai-strategy/2025-11-14-google-ads-api-write-operations-verification.md`
- **Google Ads Text Generator**: `/tools/google-ads-text-generator/` (UI reference)
- **Smythson PMax Setup**: `/clients/smythson/documents/international-pmax-campaigns-setup-2025-11-11.md` (real-world use case)

## Development Notes

### Code Quality Standards

- **PEP 8** compliance for Python code
- **ESLint** compliance for JavaScript (if linter added)
- **Semantic HTML** - Proper use of form elements
- **Accessibility** - ARIA labels where needed
- **Comments** - Document complex logic

### Version Control

- Commit messages follow format: `[google-ads-campaign-builder]: description`
- Branch strategy: feature branches → main
- Tag releases: `v1.0.0` (on Dec 15 activation)

### Deployment Checklist (Dec 15)

- [ ] MCP server write operations activated
- [ ] Replace all placeholder functions with real MCP calls
- [ ] Test with Google Ads test account
- [ ] Update client list from client-platform-ids.json
- [ ] Validate PAUSED state enforcement
- [ ] Team training session
- [ ] Documentation updated
- [ ] Add to main README.md tools list

---

**Last Updated**: 2025-11-17
**Next Review**: 2025-12-15 (Production Launch)
**Owner**: ROK Systems Development Team
