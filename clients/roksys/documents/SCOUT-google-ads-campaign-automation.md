# SCOUT Planning: Google Ads Campaign Automation

**Created:** 2025-12-12
**Project:** Extend Google Ads MCP server with write operations for campaign creation
**Goal:** Build campaign automation to replace Markifact (£3,600/year saving)

---

## Success: What does "done" look like?

### v1 Success Criteria (Minimum Viable - Target: 1 week)

- [ ] **6 MCP write tools added** to `infrastructure/mcp-servers/google-ads-mcp-server/server.py`:
  - [ ] `create_campaign` - Create new campaigns with budget, bidding, location
  - [ ] `create_ad_group` - Add ad groups to campaigns
  - [ ] `create_responsive_search_ad` - Create RSAs with headlines/descriptions
  - [ ] `add_keywords` - Add keywords with match types (EXACT, PHRASE, BROAD)
  - [ ] `add_sitelinks` - Add sitelink extensions
  - [ ] `add_callouts` - Add callout extensions

- [ ] **Complete campaign creation via conversation** (not UI):
  - Campaign settings configured (budget, location, bidding strategy)
  - Ad groups created with appropriate CPC bids
  - RSAs created (minimum 3 headlines, 2 descriptions)
  - Keywords added with correct match types
  - Extensions attached (sitelinks, callouts)

- [ ] **Safety & verification**:
  - All campaigns created in PAUSED state for review
  - Verification query after creation (confirm settings applied)
  - Error handling and rollback capability
  - Test account validation before production use

- [ ] **Real-world validation**:
  - Create 1 complete campaign for real client using these tools
  - Process takes <5 minutes of my time (vs 20-30 minutes manually)
  - Campaign quality matches or exceeds manual creation

**Success measurement:**
- ✅ Campaign created successfully in Google Ads
- ✅ All settings match requirements
- ✅ Time saved: 15-25 minutes per campaign
- ✅ No manual UI interaction required

### v2 Success Criteria (Target: 2-3 weeks)

- [ ] **Conversational skill** at `.claude/skills/google-ads-campaign-builder/`
  - Guided requirements gathering (goal, budget, keywords, copy)
  - Claude generates campaign structure from brief
  - User review and approval before creation
  - Automatic documentation to client CONTEXT.md

- [ ] **Integration with existing tools**:
  - Pull ad copy from Google Ads text generator automatically
  - Use client CONTEXT.md for default settings (location, currency, language)
  - Auto-log to experiments if A/B test campaign

- [ ] **Quality improvements**:
  - Campaign preview before creation (formatted markdown)
  - Template library (Brand, Generic, Competitors, Product)
  - Bulk campaign creation (multiple campaigns at once)

### v3 Success Criteria (Future)

- [ ] Performance Max campaign support
- [ ] Shopping campaign support
- [ ] Campaign cloning/templating from existing campaigns
- [ ] Automated campaign structure recommendations based on client goals

---

## Context: Current state

### Data Sources

**Already available:**
- ✅ Google Ads API v19 (integrated in MCP server)
- ✅ OAuth authentication (working, tokens in `~/.google-ads/`)
- ✅ Read operations (GAQL, keyword planner, list accounts)
- ✅ Client platform IDs (stored in CONTEXT.md, extracted via `platform_ids.py`)

**What we're adding:**
- ❌ Write operations (campaign creation, ad creation, keyword addition)

### Manual Process (Current Workflow)

**Time:** 20-30 minutes per campaign

**Steps:**
1. **Planning** (5 mins) - Decide campaign goal, budget, structure
2. **Google Ads UI** (10-15 mins):
   - Create campaign (set budget, location, bidding strategy)
   - Create ad group (set CPC bid or inherit campaign bidding)
   - Create RSA (write or copy/paste 15 headlines, 4 descriptions)
   - Add keywords (type or paste list, select match types)
   - Add sitelinks (5-10 sitelinks with descriptions)
   - Add callouts (8-10 callouts)
3. **Review** (3 mins) - Check settings, enable or leave paused
4. **Documentation** (5 mins) - Update client CONTEXT.md, log to experiments

**Pain Points:**

**Repetitive manual work:**
- Clicking through campaign setup wizard (10+ screens)
- Copy/paste between Google Ads text generator and UI
- Manually typing keywords with match type selection
- Adding sitelinks one-by-one (5+ clicks each)

**Easy to miss settings:**
- Ad rotation preference (optimize vs rotate evenly)
- Conversion tracking selection
- Ad schedule (if needed)
- Audience targeting (if applicable)

**No template reuse:**
- Creating similar campaigns (e.g., Brand campaigns across clients) requires full manual setup each time
- Can't clone campaign structure across accounts easily

**Disconnected documentation:**
- CONTEXT.md updates happen separately (manual copy/paste of campaign details)
- Experiments log requires manual entry

### User Behaviour

**Campaign creation frequency:**
- 2-3 new campaigns per month (across all clients)
- Most common types: Brand (50%), Generic (30%), Competitors (15%), Product (5%)

**Typical patterns:**
- Brand campaigns: Exact match brand keywords, high Target ROAS, tightly controlled
- Generic campaigns: Phrase/Broad match, moderate ROAS targets, broader reach
- Competitor campaigns: Exact match competitor names, aggressive bidding
- Product campaigns: Product-specific keywords, integrated with Shopping

**Current tools used:**
- Google Ads text generator (`tools/google-ads-generator/`) for headlines/descriptions
- CONTEXT.md for client-specific settings (location, currency, ROAS targets)
- Manual UI for campaign creation
- Experiments log for A/B test tracking

### Alternative Considered

**Markifact (Rejected):**
- **Cost:** £3,600/year
- **Pros:** Pre-built campaign automation, GPT integration
- **Cons:** Expensive, doesn't integrate with our existing MCP infrastructure, less flexible than custom solution
- **Decision:** Build our own using existing Google Ads MCP server foundation

---

## Outline: Input → Process → Output

### INPUT (Requirements)

**Campaign-level settings:**
- `client_name` (string) - To fetch customer_id from CONTEXT.md
- `campaign_name` (string) - e.g., "Brand Search | UK | Main"
- `campaign_type` (enum) - SEARCH, DISPLAY, SHOPPING, VIDEO, PERFORMANCE_MAX
- `daily_budget` (float) - In client currency (£)
- `bidding_strategy` (enum) - TARGET_ROAS, TARGET_CPA, MAXIMIZE_CONVERSIONS
- `target_roas` (float, optional) - e.g., 4.0 for 400% ROAS
- `target_cpa` (float, optional) - e.g., 10.00 for £10 CPA
- `locations` (array) - Default from CONTEXT.md, e.g., ["UK"]
- `language` (string) - Default from CONTEXT.md, e.g., "en"

**Ad group settings:**
- `ad_group_name` (string) - e.g., "Brand Keywords"
- `cpc_bid` (float, optional) - Max CPC if not using Smart Bidding

**Ad copy:**
- `headlines` (array) - 3-15 headlines (max 30 chars each)
- `descriptions` (array) - 2-4 descriptions (max 90 chars each)
- `final_urls` (array) - Landing page URLs
- `path1` (string, optional) - Display path 1 (max 15 chars)
- `path2` (string, optional) - Display path 2 (max 15 chars)

**Keywords:**
- `keywords` (array of objects) - Each with `text` and `match_type` (EXACT, PHRASE, BROAD)

**Extensions:**
- `sitelinks` (array of objects, optional) - Each with `text`, `url`, `description1`, `description2`
- `callouts` (array of strings, optional) - Max 25 chars each

### PROCESS (Transformation)

**Step 1: Fetch Client Context**
```python
# Get platform IDs from CONTEXT.md
from shared.platform_ids import get_client_platform_ids
client_data = get_client_platform_ids(client_name)
customer_id = client_data['google_ads_customer_id']
manager_id = client_data.get('google_ads_manager_id', '')

# Get default settings from CONTEXT.md
# - Default location (UK, US, etc.)
# - Default language (en)
# - Reporting currency (GBP, USD, EUR)
# - Typical ROAS targets
```

**Step 2: Create Campaign**
```python
# Call MCP tool
campaign = mcp__google_ads__create_campaign(
    customer_id=customer_id,
    manager_id=manager_id,
    campaign_name=campaign_name,
    daily_budget_micros=daily_budget * 1_000_000,
    target_roas=target_roas,
    locations=locations,
    campaign_type=campaign_type,
    status='PAUSED'  # Always start paused
)
campaign_id = campaign['campaign_id']
```

**Step 3: Create Ad Group**
```python
ad_group = mcp__google_ads__create_ad_group(
    customer_id=customer_id,
    manager_id=manager_id,
    campaign_id=campaign_id,
    ad_group_name=ad_group_name,
    cpc_bid_micros=cpc_bid * 1_000_000 if cpc_bid else None,
    status='ENABLED'
)
ad_group_id = ad_group['ad_group_id']
```

**Step 4: Create Responsive Search Ad**
```python
ad = mcp__google_ads__create_responsive_search_ad(
    customer_id=customer_id,
    manager_id=manager_id,
    ad_group_id=ad_group_id,
    headlines=headlines,
    descriptions=descriptions,
    final_urls=final_urls,
    path1=path1,
    path2=path2,
    status='ENABLED'
)
ad_id = ad['ad_id']
```

**Step 5: Add Keywords**
```python
keywords_result = mcp__google_ads__add_keywords(
    customer_id=customer_id,
    manager_id=manager_id,
    ad_group_id=ad_group_id,
    keywords=keywords  # [{"text": "luxury diary", "match_type": "EXACT"}, ...]
)
```

**Step 6: Add Extensions (Optional)**
```python
if sitelinks:
    mcp__google_ads__add_sitelinks(
        customer_id=customer_id,
        manager_id=manager_id,
        campaign_id=campaign_id,
        sitelinks=sitelinks
    )

if callouts:
    mcp__google_ads__add_callouts(
        customer_id=customer_id,
        manager_id=manager_id,
        campaign_id=campaign_id,
        callouts=callouts
    )
```

**Step 7: Verify Creation**
```python
# Query created campaign to verify settings
verification_query = f"""
    SELECT
        campaign.id,
        campaign.name,
        campaign.status,
        campaign_budget.amount_micros,
        campaign.target_roas
    FROM campaign
    WHERE campaign.id = {campaign_id}
"""
verification = mcp__google_ads__run_gaql(customer_id, manager_id, verification_query)

# Compare actual vs expected
assert verification['campaign']['name'] == campaign_name
assert verification['campaign_budget']['amount_micros'] == daily_budget * 1_000_000
# etc.
```

**Step 8: Document Campaign**
```python
# Save campaign details to clients/{client}/campaigns/[campaign-name].md
campaign_doc = f"""
# {campaign_name}

**Created:** {today}
**Campaign ID:** {campaign_id}
**Status:** PAUSED (awaiting review)

## Settings
- **Budget:** £{daily_budget}/day
- **Bidding:** Target ROAS {target_roas}x
- **Location:** {locations}
- **Campaign Type:** {campaign_type}

## Ad Groups
- {ad_group_name} (ID: {ad_group_id})

## Ads
- RSA (ID: {ad_id})
  - {len(headlines)} headlines
  - {len(descriptions)} descriptions

## Keywords
- {len(keywords)} keywords added

## Next Steps
1. Review campaign settings in Google Ads UI
2. Enable campaign when ready
3. Monitor performance for first 7 days
"""

# Save to clients/{client}/campaigns/
# Update CONTEXT.md with campaign reference
```

### OUTPUT (Deliverables)

**1. Campaign in Google Ads**
- Campaign created in PAUSED state
- Ad group(s) created and enabled
- RSA(s) created and enabled
- Keywords added
- Extensions attached (if provided)

**2. Documentation**
- `clients/{client}/campaigns/{campaign-name}.md` - Campaign details
- `clients/{client}/CONTEXT.md` - Updated with campaign reference
- `clients/{client}/experiments/{experiment-name}.md` - If A/B test

**3. Verification Report**
- Campaign ID and resource name
- Settings verification (actual vs expected)
- Preview link (https://ads.google.com/aw/campaigns?campaignId={campaign_id})

**4. Success Confirmation**
```
✅ Campaign created successfully

Campaign: Brand Search | UK | Main
Campaign ID: 12345678
Status: PAUSED (ready for review)

Preview: https://ads.google.com/aw/campaigns?campaignId=12345678

Documentation saved to:
- clients/smythson/campaigns/brand-search-uk-main.md

Next steps:
1. Review campaign in Google Ads UI
2. Enable when ready to launch
```

---

## Upskill: Knowledge gaps

### What You Already Know ✅

- ✅ Google Ads API structure (customer > campaign > ad group > ad > keyword)
- ✅ GAQL queries (read operations, filtering, aggregation)
- ✅ MCP server development (built 11 MCP servers already)
- ✅ OAuth authentication (working for read operations)
- ✅ Google Ads campaign structure (22+ years PPC experience)
- ✅ Client data architecture (CONTEXT.md, platform_ids.py)
- ✅ Safety protocols (docs/GOOGLE-ADS-PROTOCOL.md - backup/verify/rollback)

### What You Need to Learn 📚

#### 1. Google Ads API Write Operations

**Learning goal:** Understand how to create campaigns via API

**Resources:**
- [ ] Read: [Google Ads API - Create campaigns](https://developers.google.com/google-ads/api/docs/campaigns/create)
- [ ] Read: [CampaignService documentation](https://developers.google.com/google-ads/api/reference/rpc/v19/CampaignService)
- [ ] Study: Your existing MCP server read operations as examples (`infrastructure/mcp-servers/google-ads-mcp-server/server.py`)

**Key concepts to understand:**
- `CampaignOperation` mutation structure
- Required fields vs optional fields
- Bidding strategy configuration (TARGET_ROAS, TARGET_CPA, etc.)
- Budget creation (shared vs campaign-specific)
- Location targeting (geo_target_constants)

**Practical exercise:**
- [ ] Test campaign creation in Google Ads test account via API
- [ ] Compare API-created campaign vs UI-created campaign (verify they match)

**Time estimate:** 2-3 hours

---

#### 2. Ad Group & RSA Creation

**Learning goal:** Create ad groups and responsive search ads via API

**Resources:**
- [ ] Read: [AdGroupService documentation](https://developers.google.com/google-ads/api/reference/rpc/v19/AdGroupService)
- [ ] Read: [Create Responsive Search Ads](https://developers.google.com/google-ads/api/docs/ads/create-responsive-search-ads)
- [ ] Read: [Ad asset requirements](https://developers.google.com/google-ads/api/docs/ads/overview)

**Key concepts:**
- `AdGroupOperation` structure
- CPC bidding at ad group level (vs campaign-level Smart Bidding)
- `AdGroupAdService` for creating ads
- RSA asset structure (headlines, descriptions, pinning)
- Minimum requirements (3 headlines, 2 descriptions)

**Practical exercise:**
- [ ] Create ad group in test campaign
- [ ] Create RSA with 5 headlines, 3 descriptions
- [ ] Test pinning (e.g., pin headline to position 1)

**Time estimate:** 2-3 hours

---

#### 3. Keyword & Extension Creation

**Learning goal:** Add keywords and extensions via API

**Resources:**
- [ ] Read: [Keywords overview](https://developers.google.com/google-ads/api/docs/keywords/overview)
- [ ] Read: [AdGroupCriterionService](https://developers.google.com/google-ads/api/reference/rpc/v19/AdGroupCriterionService)
- [ ] Read: [Extensions overview](https://developers.google.com/google-ads/api/docs/extensions/overview)
- [ ] Read: [Sitelink assets](https://developers.google.com/google-ads/api/docs/extensions/sitelink)

**Key concepts:**
- `AdGroupCriterionOperation` for keywords
- Match type enums (EXACT, PHRASE, BROAD)
- Asset creation for extensions
- Campaign vs ad group level extensions
- Extension scheduling (optional)

**Practical exercise:**
- [ ] Add 10 keywords to test ad group (mix of match types)
- [ ] Create 5 sitelinks for test campaign
- [ ] Create 8 callouts for test campaign

**Time estimate:** 2-3 hours

---

#### 4. Error Handling for Write Operations

**Learning goal:** Handle API errors gracefully and implement rollback

**Resources:**
- [ ] Read: [Error handling](https://developers.google.com/google-ads/api/docs/best-practices/error-handling)
- [ ] Read: Your own `docs/GOOGLE-ADS-PROTOCOL.md` (backup/verify/rollback pattern)
- [ ] Study: Existing error handling in your MCP server read operations

**Key concepts:**
- API error responses (validation errors, policy violations, quota limits)
- Partial failure handling (some operations succeed, others fail)
- Rollback strategy (if ad group fails, should campaign be deleted?)
- Verification queries (confirm creation succeeded with expected settings)
- Rate limiting and retry logic

**Practical exercise:**
- [ ] Test error scenarios (invalid budget, missing required field, policy violation)
- [ ] Implement rollback (create campaign, fail ad group, delete campaign)
- [ ] Test verification query (compare actual vs expected settings)

**Time estimate:** 2-3 hours

---

#### 5. MCP Server Tool Implementation Patterns

**Learning goal:** Follow existing MCP server patterns for consistency

**Resources:**
- [ ] Study: `infrastructure/mcp-servers/google-ads-mcp-server/server.py` (read operations)
- [ ] Study: Other MCP servers for write operation patterns (Google Tasks, Google Sheets)
- [ ] Read: `infrastructure/mcp-servers/MCP-IMPLEMENTATION-PATTERNS.md`

**Key patterns to follow:**
- Function signature structure (parameters, type hints, docstrings)
- Error handling and logging
- Return value format (consistent JSON structure)
- Parameter validation
- Manager ID handling (optional parameter, default to empty string)

**Practical exercise:**
- [ ] Review `run_gaql` function structure
- [ ] Review `list_accounts` function structure
- [ ] Identify common patterns to reuse

**Time estimate:** 1 hour

---

### Total Upskill Time Estimate: 8-12 hours (1-2 days)

**Recommended approach:**
1. Day 1 morning: Campaign creation API (2-3 hours)
2. Day 1 afternoon: Test campaign creation in test account (2-3 hours)
3. Day 2 morning: Ad group & RSA creation (2-3 hours)
4. Day 2 afternoon: Keywords & extensions (2-3 hours)

**Don't skip this phase!** Understanding the API before coding prevents costly mistakes and rework.

---

## Tune: Launch plan

### v1 Scope (Target: 1 week from today)

**Goal:** Ship working MCP write tools, create 1 real campaign

**Deliverables:**
- [ ] 6 MCP tools added to server (`create_campaign`, `create_ad_group`, `create_responsive_search_ad`, `add_keywords`, `add_sitelinks`, `add_callouts`)
- [ ] Test account validation (create test campaign end-to-end)
- [ ] Production campaign created (1 real client campaign using these tools)
- [ ] Documentation updated (`infrastructure/mcp-servers/google-ads-mcp-server/README.md`)

**v1 Success Metrics:**
- ✅ Does it work? (campaign created successfully in Google Ads)
- ✅ Time saved? (measure actual time: manual 20-30 mins vs automated <5 mins)
- ✅ Errors encountered? (log all errors, fix critical ones before v2)
- ✅ Quality match? (automated campaign quality = manual campaign quality)

**Feedback mechanism:**
- Document process in `clients/roksys/documents/campaign-automation-v1-notes.md`
- Track:
  - What was annoying? (repetitive prompts, unclear parameters, etc.)
  - Where did I manually intervene? (fix settings in UI after creation)
  - What settings did I forget to include? (ad rotation, conversion tracking, etc.)
  - How long did it actually take? (stopwatch: start to finish)

**Known limitations of v1:**
- No conversational skill (manual tool calls via Claude Code)
- No template library (must specify all settings each time)
- No automatic documentation (manual CONTEXT.md update)
- Search campaigns only (no Performance Max, Shopping, Display)

---

### v2 Scope (Target: 2-3 weeks from today)

**Goal:** Add conversational skill, improve UX, automate documentation

**Deliverables:**
- [ ] `.claude/skills/google-ads-campaign-builder/` skill created
- [ ] Conversational requirements gathering (guided prompts)
- [ ] Campaign preview before creation (formatted markdown review)
- [ ] Automatic documentation to CONTEXT.md and campaigns folder
- [ ] Integration with Google Ads text generator (fetch copy automatically)

**v2 Success Metrics:**
- ✅ Can I create a campaign in <5 minutes total? (including conversation)
- ✅ Is the output quality as good as manual? (client-ready, no edits needed)
- ✅ Am I actually using this for every new campaign? (adoption metric)
- ✅ Does it save time on documentation? (CONTEXT.md updates automatic)

**Improvements based on v1 feedback:**
- Fix: [List issues discovered in v1]
- Add: [Features requested during v1 usage]
- Optimise: [Steps that took too long in v1]

---

### v3 Scope (Target: 4-6 weeks from today)

**Goal:** Expand to other campaign types, add templates, enable bulk creation

**Deliverables:**
- [ ] Performance Max campaign support (create_asset_group tool)
- [ ] Shopping campaign support (link Merchant Center feed)
- [ ] Template library (Brand template, Generic template, Competitors template)
- [ ] Bulk campaign creation (create 5 campaigns at once from template)
- [ ] Campaign cloning (clone existing campaign structure to new account)

**v3 Success Metrics:**
- ✅ Can I create any campaign type? (Search, PMax, Shopping, Display)
- ✅ Can I create campaigns faster with templates? (<3 minutes with template)
- ✅ Can I clone campaign structures across clients? (standardise Brand campaigns)

---

### Long-term Vision (3-6 months)

**Goal:** Full campaign lifecycle automation

**Future capabilities:**
- Automated campaign structure recommendations (Claude analyses client goals, suggests structure)
- Campaign performance monitoring (alert when campaign underperforms)
- Automated budget rebalancing (move budget from low ROAS to high ROAS campaigns)
- A/B test automation (create test variations, monitor, apply winners)
- Seasonal campaign scheduling (auto-enable/pause campaigns based on calendar)

**Decision point:** After v2, evaluate if this should become a standalone product (sell to other agencies)

---

## Next Steps

**Immediate actions (today):**
- [x] SCOUT planning document created
- [ ] Review and refine Success criteria (confirm v1 scope is right)
- [ ] Decide: Build it? Simplify scope? Defer?
- [ ] If building: Schedule Upskill phase (block 8-12 hours this week)

**This week (if proceeding):**
1. **Upskill Phase** (1-2 days)
   - Read Google Ads API documentation (campaign, ad group, ad creation)
   - Test write operations in test account
   - Review existing MCP server patterns

2. **Build v1** (2-3 days)
   - Implement 6 MCP write tools
   - Test in test account (full campaign creation workflow)
   - Create 1 real client campaign using tools

3. **Document & Review** (0.5 days)
   - Update MCP server README
   - Log v1 feedback and issues
   - Plan v2 improvements

**Total time commitment:** 1 week (3.5-5.5 days of work)

---

## Decision Checkpoint

**Should we build this?**

**Pros:**
- ✅ Clear ROI (£3,600/year saved vs Markifact)
- ✅ Builds on existing infrastructure (MCP server, OAuth working)
- ✅ Solves real pain (20-30 mins manual work per campaign)
- ✅ Extensible foundation (can add templates, PMax, bulk creation later)
- ✅ Learning value (Google Ads API write operations useful for other automations)

**Cons:**
- ⚠️ Time investment (1 week upfront, ongoing maintenance)
- ⚠️ API complexity (write operations more complex than reads)
- ⚠️ Testing overhead (need test account, careful validation)

**Risk mitigation:**
- Use test account for all development and validation
- Follow existing safety protocols (backup/verify/rollback)
- Start with v1 (6 tools only), expand later if successful
- Can defer/cancel if upskill phase reveals unexpected complexity

**Recommendation:** **BUILD IT** - the ROI is clear, foundation exists, scope is manageable.

---

**Status:** Planning complete, awaiting decision to proceed.
