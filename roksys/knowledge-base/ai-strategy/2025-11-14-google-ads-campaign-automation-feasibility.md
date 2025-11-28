---
title: Google Ads Campaign Automation - Build vs Buy Analysis (GPT-5.1 Era)
source: Internal analysis following Markifact announcement
date_added: 2025-11-14
last_updated: 2025-11-14
tags: [google-ads, automation, gpt-5.1, api-integration, build-vs-buy, markifact]
source_type: technical-analysis
---

## Executive Summary

**Question**: Can we build Google Ads campaign automation ourselves using GPT-5.1 + Google Ads API, or should we use Markifact?

**Answer**: Yes, we can build this ourselves. We already have 90% of the infrastructure:
- ✅ Direct Google Ads API access via MCP server
- ✅ OAuth authentication working
- ✅ Claude Code AI assistance (better than GPT-5.1 for our use case)
- ❌ Missing: Write operations in our MCP server (create campaigns, ad groups, ads, extensions)

**Recommendation**: **Build it ourselves.** Extending our MCP server is a one-time investment that gives us full control, no ongoing costs, and deeper customization.

---

## Current State Analysis

### What We Have

**Google Ads MCP Server** (`infrastructure/mcp-servers/google-ads-mcp-server/`):
- ✅ OAuth2 authentication working
- ✅ Developer token configured
- ✅ Four read-only tools:
  1. `run_gaql` - Execute GAQL queries (campaign data, performance, structure)
  2. `list_accounts` - List all accessible accounts
  3. `run_keyword_planner` - Generate keyword ideas
  4. `get_client_platform_ids` - Client account ID lookups

**What's Missing**: Write operations
- ❌ Create campaigns
- ❌ Create ad groups
- ❌ Add keywords
- ❌ Create RSAs (Responsive Search Ads)
- ❌ Add extensions (sitelinks, callouts, structured snippets)
- ❌ Set budgets, bidding strategies

**AI Models Available**:
- ✅ **Claude (Sonnet)** - Current model used in Claude Code
  - Excellent instruction-following
  - Strong structured output capabilities
  - Already integrated into our workflow
- ✅ **GPT-5.1** - New OpenAI model (optional)
  - 50% faster than GPT-5
  - Better instruction-following than previous versions
  - Available via OpenAI API

---

## What Markifact Does

**Markifact Platform** (competitor analysis):
- Natural language campaign creation interface
- Uses GPT-5.1 for instruction parsing
- Google Ads API integration (same API we have access to)
- Two execution modes: Quality (deep reasoning) vs Speed (fast actions)
- Creates: campaigns, ad groups, sitelinks, callouts, assets
- **Price**: Unknown (SaaS model, likely $100-500/month)

**What they're doing technically**:
```
User Input (natural language)
    ↓
GPT-5.1 (parses requirements, structures data)
    ↓
Google Ads API (creates campaign entities)
    ↓
User Approval → Push to Google Ads
```

**Key Insight**: Markifact is essentially a UI wrapper around GPT-5.1 + Google Ads API. Both of these components are accessible to us.

---

## Building It Ourselves - Technical Plan

### Phase 1: Extend Google Ads MCP Server (High Priority)

**Add write operations to existing MCP server:**

```python
# New MCP tools to add:

@mcp.tool
def create_campaign(
    customer_id: str,
    campaign_name: str,
    budget_micros: int,
    target_roas: float,
    locations: List[str],
    ctx: Context = None
) -> Dict[str, Any]:
    """Create a new Google Ads campaign."""
    # Implementation using Google Ads API v19
    # POST to customers/{customer_id}/campaigns:mutate

@mcp.tool
def create_ad_group(
    customer_id: str,
    campaign_id: str,
    ad_group_name: str,
    cpc_bid_micros: int,
    ctx: Context = None
) -> Dict[str, Any]:
    """Create a new ad group in a campaign."""
    # POST to customers/{customer_id}/adGroups:mutate

@mcp.tool
def create_responsive_search_ad(
    customer_id: str,
    ad_group_id: str,
    headlines: List[str],
    descriptions: List[str],
    final_urls: List[str],
    ctx: Context = None
) -> Dict[str, Any]:
    """Create a Responsive Search Ad with up to 15 headlines and 4 descriptions."""
    # POST to customers/{customer_id}/adGroupAds:mutate

@mcp.tool
def add_sitelinks(
    customer_id: str,
    campaign_id: str,
    sitelinks: List[Dict[str, str]],
    ctx: Context = None
) -> Dict[str, Any]:
    """Add sitelink extensions to a campaign."""
    # POST to customers/{customer_id}/campaignExtensionSettings:mutate

@mcp.tool
def add_callouts(
    customer_id: str,
    campaign_id: str,
    callouts: List[str],
    ctx: Context = None
) -> Dict[str, Any]:
    """Add callout extensions to a campaign."""
    # POST to customers/{customer_id}/campaignExtensionSettings:mutate

@mcp.tool
def add_keywords(
    customer_id: str,
    ad_group_id: str,
    keywords: List[Dict[str, str]],  # [{"text": "keyword", "match_type": "BROAD"}]
    ctx: Context = None
) -> Dict[str, Any]:
    """Add keywords to an ad group."""
    # POST to customers/{customer_id}/adGroupCriteria:mutate
```

**Estimated effort**: 2-3 days for experienced Python developer
- Most code structure already exists (authentication, error handling, GAQL execution)
- Google Ads API documentation is comprehensive
- Can test against test customer account

### Phase 2: Create Campaign Builder Skill (Medium Priority)

**New Claude Code Skill** (`.claude/skills/google-ads-campaign-builder/`):

```markdown
# Google Ads Campaign Builder Skill

When user says: "Create Google Ads campaign for [client]"

1. **Gather requirements conversationally**:
   - Campaign goal (sales, leads, traffic)
   - Budget (daily, monthly)
   - Geographic targeting (countries, cities)
   - Product/service being promoted
   - Target ROAS or CPA (if conversion campaign)
   - Landing page URL

2. **Generate campaign structure using Claude**:
   - Campaign name following ROK naming convention
   - Ad group structure (themed keyword groupings)
   - 3-5 keyword themes with 5-10 keywords each
   - 10-15 headline variations
   - 3-4 description variations
   - 4-6 sitelinks with descriptions
   - 6-8 callout extensions

3. **Review with user before creating**:
   - Display proposed structure in markdown
   - Show estimated monthly spend
   - Highlight any concerns (budget too low, etc.)
   - Ask: "Approve? Or what should I change?"

4. **Create campaign via MCP tools**:
   - Use new write operations to create entities
   - Create in paused state
   - Enable when user confirms

5. **Confirm completion**:
   - Provide Google Ads UI link to new campaign
   - Document in client CONTEXT.md
   - Log to experiment tracking
```

**Estimated effort**: 1-2 days
- Primarily writing skill instructions
- Testing with real campaigns
- Iterating on prompting strategy

### Phase 3: GPT-5.1 Integration (Optional)

**If we want to use GPT-5.1 specifically**:

```python
# Add OpenAI API call in skill
import openai

def parse_campaign_requirements(user_input: str) -> Dict[str, Any]:
    """Use GPT-5.1 to parse natural language campaign requirements."""

    response = openai.ChatCompletion.create(
        model="gpt-5.1-instant",  # or gpt-5.1-thinking for complex
        messages=[{
            "role": "system",
            "content": "You are a Google Ads expert. Extract structured campaign requirements from natural language input."
        }, {
            "role": "user",
            "content": user_input
        }],
        functions=[{
            "name": "campaign_structure",
            "description": "Structured Google Ads campaign",
            "parameters": {
                "type": "object",
                "properties": {
                    "campaign_name": {"type": "string"},
                    "budget_daily": {"type": "number"},
                    "target_roas": {"type": "number"},
                    "locations": {"type": "array", "items": {"type": "string"}},
                    "keywords": {"type": "array", "items": {"type": "string"}},
                    # ... more fields
                }
            }
        }],
        function_call={"name": "campaign_structure"}
    )

    return response["choices"][0]["message"]["function_call"]["arguments"]
```

**Why this is optional**:
- Claude (our current model) is already excellent at structured output
- GPT-5.1's main advantage is speed (50% faster), but campaign creation isn't time-critical
- Using Claude keeps everything in one system (Claude Code)
- GPT-5.1 adds dependency on OpenAI API key and billing

---

## Build vs Buy Comparison

| Aspect | **Build Ourselves** | **Use Markifact** |
|--------|---------------------|-------------------|
| **Upfront Cost** | 3-5 days dev time (~£1,500-2,500 internal cost) | $0-500 (trial period?) |
| **Ongoing Cost** | $0 (we own the code) | $100-500/month (~£1,200-6,000/year) |
| **Customization** | Full control, can add ROK-specific features | Limited to Markifact's features |
| **Integration** | Native Claude Code integration | Separate platform, context switching |
| **Learning Curve** | Minimal (uses our existing workflow) | New platform to learn |
| **Data Control** | All data stays in our infrastructure | Campaign data passes through Markifact |
| **ROK Brand** | Can add ROK naming conventions, templates | Generic campaign structures |
| **API Limits** | Direct API access (no middleman) | Markifact's rate limits may apply |
| **Maintenance** | We maintain (rare Google API changes) | Markifact maintains |
| **Multi-Client** | Already works across all 30+ clients | May have client/account limits |

**Break-even Analysis**:
- Markifact cost: ~£300/month (estimate) = £3,600/year
- Build cost: £2,000 one-time
- **Break-even: 7 months**

After 7 months, building ourselves is cheaper. And we own it forever.

---

## Recommended Approach

### Option A: Full Build (Recommended)

**Phase 1 (Week 1-2)**: Extend Google Ads MCP Server
- Add 6 core write operations (campaign, ad group, RSA, keywords, sitelinks, callouts)
- Test with test account
- Deploy to production MCP server

**Phase 2 (Week 3)**: Create Campaign Builder Skill
- Write skill instructions for conversational campaign creation
- Test with real client (start with small campaign)
- Document workflow

**Phase 3 (Week 4)**: Productionize
- Add error handling and validation
- Create templates for common campaign types (Shopping, Search, PMax)
- Add to ROK workflow documentation

**Total Investment**: 4 weeks, ~£5,000 internal cost
**Payoff**: Own the tool forever, zero ongoing costs, full customization

### Option B: Quick Start (Fast but Limited)

**Use existing tools + manual workflow**:
1. User describes campaign in Claude Code
2. Claude generates GAQL-style campaign structure as text
3. User manually creates in Google Ads UI using generated structure
4. Claude logs to experiments

**Investment**: 1 day to create skill
**Limitation**: Not truly automated (user still does manual work)
**Use case**: Temporary solution while Phase 1 is being built

### Option C: Use Markifact (Not Recommended)

**When this might make sense**:
- Need solution TODAY (can't wait 4 weeks)
- Don't have Python dev resources
- Don't want to maintain code
- Only creating 1-2 campaigns per month

**Why we don't recommend it**:
- Ongoing cost adds up quickly
- Less control over campaign quality
- Doesn't integrate with our existing ROK workflows
- Data passes through third-party
- May have limitations on customization

---

## Risk Analysis

### Building Ourselves - Risks

**Technical Risks**:
- **Google API changes**: Low risk. Google Ads API is stable, rarely breaks. We're already using it for read operations.
- **OAuth token management**: Solved. Already working in our read-only MCP server.
- **Error handling**: Medium risk. Need robust handling of API errors (rate limits, validation errors, etc.)

**Business Risks**:
- **Development time**: Low risk. 4 weeks is manageable, and we can use existing tools in the meantime.
- **Maintenance burden**: Low risk. Once built, rarely needs updates (Google API is stable).

**Mitigation**:
- Start with test account to avoid breaking client campaigns
- Build incrementally (one operation at a time)
- Extensive testing before production use

### Using Markifact - Risks

**Vendor Risks**:
- **Platform shutdown**: Medium risk. Markifact is new (launched 2025), could shut down.
- **Price increases**: High risk. SaaS platforms often increase prices once adopted.
- **Feature removal**: Medium risk. They could remove features or change pricing tiers.

**Integration Risks**:
- **Context switching**: High risk. Moving between Claude Code and Markifact breaks workflow.
- **Data privacy**: Low-medium risk. Campaign data (keywords, budgets) passes through Markifact.
- **Rate limits**: Unknown. Markifact may have rate limits on API calls.

---

## Real-World Use Cases

### Use Case 1: New Client Campaign Setup

**Current workflow** (manual):
1. User researches keywords (30 mins)
2. User creates campaign in Google Ads UI (60 mins)
3. User creates ad groups manually (30 mins)
4. User writes ad copy (45 mins)
5. User adds extensions (15 mins)
**Total**: 3 hours

**With automation** (our build):
1. User tells Claude: "Create campaign for [client] selling [products]"
2. Claude asks 5 questions (goal, budget, locations, keywords, landing page)
3. Claude generates full structure (2 mins)
4. User reviews and approves (5 mins)
5. Claude creates via MCP tools (1 min)
**Total**: 10 minutes

**Time saved**: 2 hours 50 minutes per campaign
**ROK volume**: ~10-15 new campaigns per month = 28-42 hours saved/month

### Use Case 2: Campaign Iteration

**Scenario**: Client wants to test new product category with separate campaign

**Current workflow**:
1. Duplicate existing campaign (10 mins)
2. Rename and restructure (20 mins)
3. Update keywords (15 mins)
4. Rewrite ad copy (30 mins)
5. Update extensions (10 mins)
**Total**: 85 minutes

**With automation**:
1. "Clone [campaign name] but for [new product]"
2. Claude generates variant (2 mins)
3. User approves (2 mins)
**Total**: 5 minutes

**Time saved**: 80 minutes per iteration

### Use Case 3: Multi-Client Rollout

**Scenario**: New Google Ads feature/strategy needs to be applied to 20 clients

**Current workflow**:
1. Manually implement for each client (30 mins × 20) = 10 hours

**With automation**:
1. Create template once (30 mins)
2. Claude applies to all clients with variations (5 mins × 20) = 100 mins
**Total**: 2.5 hours

**Time saved**: 7.5 hours

---

## Implementation Timeline

### Week 1-2: Core MCP Extensions

**Monday-Wednesday**:
- Design API structure for write operations
- Implement `create_campaign` tool
- Test with test account

**Thursday-Friday**:
- Implement `create_ad_group` and `create_responsive_search_ad` tools
- Test end-to-end campaign creation

**Monday-Wednesday (Week 2)**:
- Implement keyword and extension tools
- Add error handling and validation

**Thursday-Friday (Week 2)**:
- Integration testing
- Documentation

### Week 3: Campaign Builder Skill

**Monday-Tuesday**:
- Write skill instructions
- Create conversation flow
- Define campaign templates

**Wednesday-Thursday**:
- Test with real client (small campaign)
- Iterate on prompting
- Add ROK-specific customizations

**Friday**:
- Documentation and training

### Week 4: Production Deployment

**Monday-Tuesday**:
- Deploy to production MCP server
- Test with multiple clients
- Monitor for errors

**Wednesday-Friday**:
- Create templates for common campaign types
- Document workflow
- Team training

---

## Conclusion

**We should build this ourselves.** Here's why:

1. **We already have 90% of the infrastructure**
   - Google Ads API access ✅
   - OAuth authentication ✅
   - MCP server framework ✅
   - AI integration (Claude) ✅

2. **The missing 10% is straightforward**
   - Add write operations to MCP server (2-3 days)
   - Create campaign builder skill (1-2 days)
   - Total: 4-5 days of development

3. **The economics make sense**
   - One-time cost: ~£2,000-5,000
   - Ongoing cost: £0
   - Break-even vs Markifact: 7 months
   - Time saved: 30+ hours/month

4. **Full control**
   - Customize to ROK workflows
   - Add ROK naming conventions
   - Integrate with experiment tracking
   - No vendor lock-in

5. **Better than Markifact**
   - Native Claude Code integration (no context switching)
   - Data stays in our infrastructure
   - Unlimited campaigns (no per-campaign pricing)
   - Works across all 30+ clients without restrictions

**Next Steps**:
1. Get approval to allocate 4 weeks for development
2. Create feature specification document
3. Set up test Google Ads account for development
4. Begin Phase 1 (MCP server extensions)

---

## Additional Resources

**Google Ads API Documentation**:
- Campaign Management: https://developers.google.com/google-ads/api/docs/campaigns/overview
- Mutate Operations: https://developers.google.com/google-ads/api/docs/mutating/overview
- API v19 Reference: https://developers.google.com/google-ads/api/reference/rpc/v19/overview

**Related ROK Documentation**:
- Current Google Ads MCP Server: `/infrastructure/mcp-servers/google-ads-mcp-server/`
- MCP Server Guide: `/docs/MCP-SERVERS.md`
- Skills Documentation: `.claude/skills/README.md`

**Markifact Comparison**:
- Markifact announcement: User-provided email, Nov 14 2025
- GPT-5.1 analysis: `/roksys/knowledge-base/ai-strategy/2025-11-14-openai-gpt-5-1-launch.md`

---

*Analysis completed: 2025-11-14*
*Recommendation: Build ourselves - 4 weeks, £5K investment, zero ongoing costs*
