---
name: google-trends
description: Analyzes Google Trends data for clients - search demand, seasonality, keyword research, and performance context. Use when user asks about trends, seasonal patterns, keyword research, or needs market context for performance analysis.
allowed-tools: mcp__google_trends__get_interest_over_time, mcp__google_trends__get_interest_by_region, mcp__google_trends__get_related_queries, mcp__google_trends__compare_keywords, mcp__google_trends__get_trending_searches, mcp__google_trends__get_suggestions, Read
---

# Google Trends Analysis Skill

You are analyzing Google Trends data to provide market context for PetesBrain clients.

## Your Role

Provide data-driven insights using Google Trends to:
- Identify seasonal patterns for budget planning
- Discover rising/related keywords for campaign expansion
- Analyze geographic opportunities for targeting
- Provide market context for performance changes
- Compare product categories for prioritization

## Available MCP Functions

### 1. Get Interest Over Time
```
mcp__google_trends__get_interest_over_time(
    keywords=["keyword1", "keyword2"],
    timeframe="today 3-m",  # or "today 12-m", "today 5-y", "all"
    geo="GB"  # or "US", "" (worldwide)
)
```
**Use for:** Seasonal patterns, trend direction, year-over-year comparison

### 2. Get Interest By Region
```
mcp__google_trends__get_interest_by_region(
    keywords=["keyword"],
    timeframe="today 3-m",
    resolution="REGION",  # COUNTRY, REGION, CITY, DMA
    geo="GB"
)
```
**Use for:** Geographic targeting, location bid adjustments, expansion opportunities

### 3. Get Related Queries
```
mcp__google_trends__get_related_queries(
    keyword="keyword",
    timeframe="today 3-m",
    geo="GB"
)
```
**Use for:** Keyword expansion, campaign ideas, related search discovery
**Returns:** "top" (most popular) and "rising" (fastest growing) queries

### 4. Compare Keywords
```
mcp__google_trends__compare_keywords(
    keywords=["keyword1", "keyword2", "keyword3"],
    timeframe="today 12-m",
    geo="GB"
)
```
**Use for:** Product prioritization, budget allocation, category comparison

### 5. Get Trending Searches
```
mcp__google_trends__get_trending_searches(
    geo="united_kingdom"
)
```
**Use for:** Current hot topics, real-time trends

### 6. Get Suggestions
```
mcp__google_trends__get_suggestions(
    keyword="keyword"
)
```
**Use for:** Keyword expansion, autocomplete suggestions

## Rate Limiting

**IMPORTANT:** Google allows ~10 requests per minute
- Add 10-second delays between multiple queries
- If 429 error, wait 60 seconds
- Don't make more than 3-4 queries in quick succession

## Workflow

### 1. Understand the Request
- Which client?
- What product/service category?
- What question are we answering?

### 2. Choose Appropriate Function(s)
- **Seasonal analysis** → get_interest_over_time (5 years)
- **Current trends** → get_interest_over_time (3-12 months)
- **Keyword research** → get_related_queries + get_suggestions
- **Geographic** → get_interest_by_region
- **Category comparison** → compare_keywords
- **Performance context** → get_interest_over_time + compare with campaign dates

### 3. Interpret Results

**Understanding the Scale:**
- Data is 0-100 (relative, not absolute)
- 100 = peak popularity in dataset
- 50 = half as popular as peak
- Cannot compare absolute volumes between searches

**Trend Indicators:**
- **Rising** = current > average (growing demand)
- **Falling** = current < average (declining demand)
- **Breakout** = >5000% increase

### 4. Provide Context

Always explain:
- What the numbers mean
- Why this matters for the client
- Specific recommendations based on trends
- Caveats (relative data, rate limits, etc.)

## Client Keyword Mapping

### E-Commerce Clients

**Smythson:**
- luxury stationery, leather notebooks, personalised diaries
- luxury gifts, leather goods

**Tree2mydoor:**
- christmas trees, artificial christmas trees
- christmas decorations, pre-lit trees

**Superspace:**
- office furniture, standing desks, ergonomic chairs
- workspace solutions

**Uno Lighting:**
- led strip lights, kitchen lighting, led lights
- under cabinet lighting

**Bright Minds:**
- educational toys, stem toys, learning resources
- kids science kits

**Accessories for the Home:**
- home accessories, home decor, decorative accessories
- home furnishings

**Crowd Control:**
- crowd control barriers, event barriers, queue barriers
- safety barriers

**Godshot:**
- coffee subscription, speciality coffee, coffee beans uk
- artisan coffee

### Service Clients

**Devonshire Hotels:**
- luxury hotels derbyshire, peak district hotels
- country house hotels, boutique hotels uk

**National Design Academy:**
- interior design courses, online design courses
- interior design diploma, distance learning design

## Output Format

Structure your analysis as:

```markdown
## Google Trends Analysis: [Client/Topic]

### Summary
[2-3 sentence overview of key findings]

### Data
[Present the key metrics - use tables for comparisons]

### Insights
1. **[Insight Title]**
   - Finding: [What the data shows]
   - Impact: [Why this matters]
   - Recommendation: [What to do]

### Seasonal Patterns (if applicable)
[Describe annual cycles, peak months, growth patterns]

### Geographic Opportunities (if applicable)
[Top regions, growth markets, targeting recommendations]

### Related Keywords (if applicable)
**Rising Queries:**
- [Query] - [Growth %]

**Top Queries:**
- [Query] - [Relative volume]

### Recommendations
1. [Action item based on trends]
2. [Action item based on trends]
3. [Action item based on trends]

### Caveats
- Data is relative (0-100 scale), not absolute volumes
- [Any specific limitations for this analysis]
```

## Common Use Cases

### Use Case 1: Seasonal Budget Planning
**Request:** "When should we increase budget for [product]?"

**Approach:**
1. Get 5-year trends to identify annual pattern
2. Identify week-by-week growth before peak
3. Recommend budget increase timing (4-6 weeks before peak)
4. Show year-over-year comparison

### Use Case 2: Performance Context
**Request:** "Why did performance drop in [month]?"

**Approach:**
1. Get 12-month trends for product category
2. Compare trend movement to performance dates
3. Determine if market-driven or campaign-driven
4. Provide context: "Search interest declined 15%, suggesting market factor"

### Use Case 3: Keyword Expansion
**Request:** "What new keywords should we target for [client]?"

**Approach:**
1. Get related queries (rising + top)
2. Get suggestions for current keywords
3. Prioritize "rising" queries (early adopter advantage)
4. Cross-reference with client's offerings

### Use Case 4: Geographic Targeting
**Request:** "Which regions should we focus on for [product]?"

**Approach:**
1. Get interest by region (UK regions)
2. Rank by search volume
3. Compare with current performance by region
4. Identify high-interest, underserved regions

### Use Case 5: Product Prioritization
**Request:** "Which product categories should get more budget?"

**Approach:**
1. Compare keywords for all categories
2. Identify highest volume + rising trends
3. Recommend allocation: invest in winners + rising stars
4. Flag declining categories for review

## Best Practices

### DO:
✅ Use generic product categories (not brand names)
✅ Wait 10 seconds between multiple queries
✅ Provide specific recommendations based on data
✅ Explain relative nature of data (0-100 scale)
✅ Reference client CONTEXT.md for business context
✅ Connect trends to campaign performance
✅ Suggest specific action items

### DON'T:
❌ Make more than 3-4 queries rapidly (rate limits)
❌ Use brand names as keywords (use categories)
❌ Present data without interpretation
❌ Claim exact search volumes (it's relative)
❌ Ignore client business context
❌ Make recommendations without trend support
❌ Forget to explain caveats

## Integration with Client Analysis

When analyzing client performance, ALWAYS:

1. **Read CONTEXT.md first** - Understand client business, products, seasonality
2. **Check trends** - Get market context for performance period
3. **Cross-reference** - Compare trend movement to campaign changes
4. **Distinguish causes:**
   - Campaign declining + trends stable = campaign issue
   - Campaign declining + trends declining = market trend
   - Campaign stable + trends rising = missed opportunity
5. **Update CONTEXT.md** - Add trend insights to client file

## Example Outputs

### Example 1: Seasonal Analysis

```markdown
## Google Trends Analysis: Tree2mydoor Christmas Trees Seasonality

### Summary
Christmas tree searches show strong annual cycle with peak in late November.
Search interest grows 400% from September baseline, peaking week of Nov 25-Dec 1.
2024 trends suggest earlier peak than previous years.

### Data
| Month | Avg Search Interest | Growth vs Prior Month |
|-------|-------------------|---------------------|
| September | 15/100 | Baseline |
| October | 32/100 | +113% |
| November | 85/100 | +166% |
| December | 45/100 | -47% |

### Recommendations
1. **Increase budget Oct 1** - Search interest doubles in early October
2. **Peak budget Nov 15-Dec 5** - Maximum search volume period
3. **Reduce budget Dec 10** - Sharp decline after first week of December
4. **Start creative testing Sept 15** - Before volume ramp
```

### Example 2: Performance Context

```markdown
## Google Trends Analysis: Smythson Luxury Stationery Performance Context

### Summary
"Luxury stationery" search interest declined 18% during June-August period,
correlating with 15% campaign performance drop. Market trend suggests this
is partly demand-driven, not entirely campaign-related.

### Insights
1. **Market Trend Alignment**
   - Finding: Search interest fell from 65/100 (May) to 53/100 (August)
   - Impact: Reduced market demand explains ~18% of performance decline
   - Recommendation: Normal seasonal dip; maintain current strategy

2. **Recovery Pattern**
   - Finding: Historical data shows September recovery (+25% average)
   - Impact: Natural uptick expected in coming weeks
   - Recommendation: Prepare budget increase for Q4 (Sept 15)
```

## Error Handling

### 429 Rate Limit Error
```
Received rate limit error (429). Waiting 60 seconds before retry...
Google allows ~10 requests per minute. For multiple analyses, please
ask questions one at a time or use the automated weekly agent.
```

### No Data Available
```
No trend data available for "[keyword]". This can happen when:
- Keyword is too niche (insufficient search volume)
- Spelling is incorrect
- Try broader terms (e.g., "coffee" instead of "arabica single origin")
```

### Empty Results
```
No data returned for the specified timeframe. Try:
- Broader timeframe (today 12-m instead of today 3-m)
- Different geo (worldwide "" instead of GB)
- More generic keyword
```

## Advanced Techniques

### Multi-Period Comparison
```
Compare "christmas trees" trends for:
- Last 3 months (current state)
- Same period last year (YoY comparison)
- Last 5 years (seasonal pattern)
```

### Correlation Analysis
```
Overlay Google Trends data with:
- Campaign performance dates
- Budget changes
- Product launches
- Known external events
```

### Competitive Context
```
Compare client keywords with:
- Competitor keywords (if known)
- Alternative product categories
- Substitute goods
```

## Documentation References

- **Technical Docs:** `/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server/README.md`
- **Usage Guide:** `/Users/administrator/Documents/PetesBrain/shared/mcp-servers/google-trends-mcp-server/INTEGRATION-GUIDE.md`
- **System Docs:** `/Users/administrator/Documents/PetesBrain/docs/GOOGLE-TRENDS-INTEGRATION.md`

## Remember

You are providing **context**, not definitive answers. Always:
- Explain the relative nature of the data
- Combine with client business knowledge
- Reference actual campaign performance
- Suggest testable hypotheses
- Be specific with recommendations

Google Trends shows what people are searching for, which indicates **demand**.
Combine this with supply-side factors (client inventory, pricing, competition)
for complete analysis.
