---
title: Google Analytics 4 Analysis Prompts - ROK Systematic Analysis Framework
source: GoMarble Prompt Library (https://prompting.gomarble.ai/)
date_added: 2025-10-30
tags: [google-analytics, ga4, analysis, prompts, ecommerce, conversion-optimization, attribution, funnel-analysis, methodology, claude, mcp]
category: Analytics
---

## Summary

This is ROK's systematic framework for analyzing Google Analytics 4 properties using Claude Code with MCP integration. These prompts provide structured, repeatable analysis for conversion optimization, attribution, audience segmentation, and traffic monitoring.

**Key Analysis Areas Covered:**
- Attribution model comparison and channel profitability
- Conversion funnel analysis and drop-off identification
- Customer segmentation and audience performance
- Checkout abandonment diagnosis
- Real-time traffic monitoring (24-hour reports)
- Seasonality patterns and revenue forecasting
- Channel performance and budget reallocation

**Usage:** These prompts can be used directly with Claude Code when connected to GA4 via MCP, or adapted for manual analysis workflows.

---

## Prompt 1: Find Your Most Profitable Marketing Channels

**Use Case:** Attribution model comparison to understand true channel value
**Best For:** Multi-channel marketing with attribution uncertainty
**Output:** Channel comparison report showing last-click vs. data-driven attribution discrepancies

### Prompt

```
Using last-click and data-driven attribution models, compare the top channels driving conversions and revenue. Highlight any attribution discrepancies that might affect budget allocation decisions for scaling.
```

### Key Insights

- **Attribution Comparison:** Last-click vs. data-driven reveals channels getting over/under-credited
- **Budget Impact:** Identifies channels that deserve more/less budget based on true contribution
- **Scaling Decisions:** Shows which channels to scale based on data-driven (not just last-click) value
- **Multi-Touch Value:** Reveals assist value that last-click attribution misses

### ROK Implementation Notes

**Common Findings:**
- **Display/YouTube often under-credited** in last-click (assists early in journey)
- **Branded Search often over-credited** in last-click (final touch, not driver)
- **Email/Social may show stronger assist value** than last-click suggests

**Action Items:**
- If data-driven shows channel with +30% more value → Increase budget
- If last-click over-credits channel (e.g., branded search) → Consider reallocating
- Use to inform Google Ads Smart Bidding (which uses data-driven attribution)

---

## Prompt 2: Find Your Website's Conversion Leaks

**Use Case:** Comprehensive funnel analysis to identify drop-off points
**Best For:** E-commerce sites with conversion rate concerns
**Output:** Funnel report with engagement metrics and drop-off analysis

### Prompt

```
Analyze visitor behavior on your site <Your Property ID> in GA4 to understand where visitors are entering, what pages they're interacting with, and how they're progressing through the funnel. Track engagement metrics such as page views, time spent on page, and scroll depth for key pages (e.g., landing pages, product pages). Use Funnel Exploration to identify where users are dropping off during the checkout process. Analyze the exit rates on the cart and checkout pages to identify friction points and recommend possible improvements.
```

### Key Insights

- **Entry Point Analysis:** Understand which pages drive traffic and their engagement quality
- **Engagement Tracking:** Page views, time on page, scroll depth reveal content effectiveness
- **Funnel Drop-offs:** Pinpoint exact stages where users abandon (cart, checkout, payment)
- **Exit Rate Analysis:** High exit rates on specific pages indicate friction or confusion
- **Actionable Recommendations:** Suggests specific improvements (UX, copy, trust signals)

### ROK Implementation Notes

**Common Conversion Leaks:**
- **Cart Page:** High exit rate → Test free shipping threshold, shipping cost visibility
- **Checkout Page:** Drop-off → Simplify form fields, add guest checkout, show security badges
- **Payment Page:** Abandonment → Add more payment options, improve load speed
- **Product Pages:** Low scroll depth → Improve product descriptions, add video, better images

**Cross-Reference with Google Ads:**
- If GA4 shows high cart abandonment, check if Google Ads is driving low-intent traffic
- Compare landing page bounce rates to Google Ads ad copy relevance
- Use GA4 funnel data to optimize Google Ads conversion tracking

---

## Prompt 3: Discover Your Best Customer Segments

**Use Case:** Audience segmentation to find high-value and untapped segments
**Best For:** Accounts with broad targeting or expansion opportunities
**Output:** Segmentation report with demographic performance and audience opportunities

### Prompt

```
In GA4 <Your Property ID> analyze your audience data to determine which demographic segments are performing well. Segment users by gender, geographic location, and age to evaluate performance across these dimensions. Look for trends in conversion rate and average order value (AOV) for each segment, and identify any underperforming groups. Leverage the Audience Builder to create audiences based on specific behaviors (e.g., users who have viewed high-value products but haven't converted) and assess their performance. Look for untapped opportunities, especially in terms of underperforming geos or demographic groups, and identify new segments for offsite targeting through paid or remarketing campaigns.
```

### Key Insights

- **Demographic Performance:** Gender, age, location breakdown with conversion rate and AOV
- **Underperforming Segments:** Identifies groups with high traffic but low conversion (opportunity)
- **Behavioral Audiences:** Creates segments based on intent signals (product views, engagement)
- **Untapped Opportunities:** Finds geos or demographics worth testing
- **Remarketing Fuel:** Identifies high-intent audiences for Google Ads remarketing

### ROK Implementation Notes

**Audience Export to Google Ads:**
1. Identify high-performing segments in GA4 (e.g., "25-34, Female, UK, High AOV")
2. Create GA4 audiences for these segments
3. Link GA4 to Google Ads and import audiences
4. Create Google Ads campaigns/bid adjustments targeting these audiences

**Common Findings:**
- **Mobile users:** Often higher traffic but lower conversion → Test mobile UX improvements
- **Specific geos:** High AOV in certain cities → Geo-targeted campaigns
- **Product viewers:** High-value product viewers without purchase → Remarketing opportunity
- **Age segments:** Certain age ranges with high CVR → Adjust Google Ads demographics

---

## Prompt 4: Reduce Checkout Abandonment

**Use Case:** Deep dive into checkout flow to reduce abandonment
**Best For:** E-commerce sites with high cart-to-purchase drop-off
**Output:** Checkout funnel report with device comparison and friction point recommendations

### Prompt

```
Using GA4's Funnel Exploration for <Your Property ID> generate a report to track user flow through your checkout process and identify critical drop-off points. Track users from the product page to the cart page, then to the checkout and purchase completion. Identify the exit rate and conversion rate at each stage of the funnel. Compare mobile vs. desktop performance, as mobile users may experience higher abandonment rates. Based on the results, recommend changes such as simplifying the checkout process, offering guest checkout options, or adding trust signals (e.g., security badges) to reduce friction.
```

### Key Insights

- **Stage-by-Stage Tracking:** Product → Cart → Checkout → Purchase with conversion rates
- **Critical Drop-off Points:** Identifies exact stage with highest abandonment
- **Mobile vs. Desktop:** Reveals if mobile checkout experience is broken
- **Friction Point Diagnosis:** Exit rates pinpoint where users give up
- **UX Recommendations:** Specific suggestions (guest checkout, trust badges, form simplification)

### ROK Implementation Notes

**Checkout Funnel Stages:**
1. **Product Page → Cart:** Low rate → Test "Add to Cart" CTA, cart preview
2. **Cart → Checkout:** High drop-off → Test shipping cost transparency, progress indicators
3. **Checkout → Payment:** Abandonment → Simplify form, add autofill, show security
4. **Payment → Completion:** Drop-off → Test payment options, load speed, error messaging

**Mobile-Specific Issues:**
- Small buttons (tap accuracy)
- Long forms (keyboard fatigue)
- Slow load times (impatience)
- Lack of payment options (Apple Pay, Google Pay)

**Google Ads Integration:**
- If checkout abandonment is high, don't increase Google Ads budget (fix funnel first)
- Use GA4 cart abandoners audience for Google Ads remarketing
- Check if certain Google Ads campaigns drive users who abandon more (quality vs. quantity)

---

## Prompt 5: Spot Traffic Issues - 24-Hour Traffic Report

**Use Case:** Daily traffic monitoring to catch anomalies quickly
**Best For:** Active campaigns or post-launch monitoring
**Output:** 24-hour traffic overview with source/device segmentation

### Prompt

```
Generate a traffic overview report for <Your Property ID> for the past 24 hours in GA4. Segment the traffic by source (e.g., Direct, Organic Search, Paid Search, Social, Referral). Include metrics such as sessions, bounce rate, engaged sessions, pages per session, and average session duration. Segment this by device (Mobile, Desktop) to compare how different devices are performing. Highlight any traffic sources with unusually high or low engagement rates.
```

### Key Insights

- **Real-Time Monitoring:** Catch traffic drops or spikes immediately
- **Source Segmentation:** Understand which channels are driving today's traffic
- **Engagement Quality:** Bounce rate, pages/session, duration reveal traffic quality
- **Device Comparison:** Mobile vs. desktop performance differences
- **Anomaly Detection:** Highlights unusual patterns (bot traffic, broken campaigns, viral posts)

### ROK Implementation Notes

**When to Run:**
- **Daily:** For active campaign launches or major changes
- **After Google Ads changes:** Check if new campaigns are driving quality traffic
- **Post-website updates:** Verify traffic and engagement hasn't dropped
- **Before client calls:** Have fresh data on current performance

**Common Anomalies:**
- **Paid Search spike with low engagement:** Check Google Ads for broad match runaway spend
- **Direct traffic spike with high bounce:** Bot traffic or tracking issue
- **Mobile traffic drop:** Mobile site broken or slow
- **Referral spike with low quality:** Spam referrer (add to referral exclusion list)

**Integration with Google Ads:**
- If Paid Search shows low engagement (high bounce, low duration) → Check ad relevance
- Compare Paid Search engagement to Organic → Quality benchmark
- Use to inform same-day Google Ads bid adjustments

---

## Prompt 6: Maximize Seasonal Opportunities with Traffic & Revenue Patterns

**Use Case:** Seasonality analysis for planning and forecasting
**Best For:** Annual planning, inventory decisions, campaign calendars
**Output:** Multi-year seasonality report with traffic and revenue patterns

### Prompt

```
Analyze seasonality patterns in traffic and revenue for <Your Property ID> for the past 2 years to identify upcoming high-opportunity windows for scaling spend, improving inventory planning, and aligning promotional calendars.
```

### Key Insights

- **Year-over-Year Patterns:** Identifies consistent seasonal peaks and troughs
- **Revenue Timing:** Shows when revenue (not just traffic) peaks
- **Scaling Windows:** Pinpoints best times to increase Google Ads budget
- **Inventory Planning:** Informs stock levels based on historical demand
- **Promotional Calendar:** Aligns marketing campaigns with high-conversion periods

### ROK Implementation Notes

**Seasonal Planning Workflow:**
1. **Identify peaks:** Black Friday, Christmas, Valentine's Day, Back-to-School, etc.
2. **Compare YoY:** Check if patterns are consistent (2023 vs. 2024)
3. **Plan budget ramps:** Increase Google Ads 2-4 weeks before peak
4. **Prepare creative:** Update ad copy and landing pages for seasonal themes
5. **Coordinate with client:** Align on inventory, promotions, pricing

**Google Ads Strategy:**
- **Pre-seasonal ramp:** Start increasing budget 2-4 weeks before peak (build momentum)
- **Peak performance:** Maximize budget during high-conversion window
- **Post-seasonal wind-down:** Reduce budget as demand drops
- **Off-season testing:** Use low-volume periods to test new campaigns/strategies

**Cross-Reference with Client Context:**
- Check `clients/[client-name]/CONTEXT.md` for documented seasonality notes
- Reference previous seasonal campaigns and learnings
- Align with client's business calendar (product launches, sales events)

---

## Prompt 7: GA4 - Cut Low-Performing Channels

**Use Case:** Channel performance audit for budget reallocation
**Best For:** Accounts with multi-channel spend and limited budget
**Output:** Channel efficiency report with ROAS and reallocation recommendations

### Prompt

```
Analyze traffic sources in GA4 for <Your Property ID> for the last 45 days:

Report traffic, conversion rate, revenue, and ROAS by channel (Organic, Paid Search, Paid Social, Email).

Identify underperforming channels with high spend and low ROAS.

Recommend budget reallocation based on LTV and CAC insights.
```

### Key Insights

- **Channel Efficiency:** Traffic, CVR, revenue, ROAS comparison across channels
- **Underperformers:** High spend + low ROAS = budget waste
- **LTV/CAC Analysis:** Not just ROAS, but customer lifetime value vs. acquisition cost
- **Reallocation Strategy:** Where to move budget for maximum impact
- **Multi-Channel View:** Combines paid and organic performance

### ROK Implementation Notes

**Channel Performance Benchmarks:**
- **Paid Search:** Target ROAS 3-5x (varies by industry)
- **Paid Social:** Target ROAS 2-4x (lower than search due to colder audience)
- **Email:** Target ROAS 10x+ (low cost, warm audience)
- **Organic Search:** High value but not direct budget control

**Reallocation Decision Framework:**
1. **Cut:** ROAS < 2x with high spend → Reduce or pause
2. **Test:** ROAS 2-3x → Optimize before scaling
3. **Scale:** ROAS 4x+ → Increase budget gradually
4. **Maintain:** ROAS 3-4x → Keep current spend

**Google Ads Specific Actions:**
- If **Paid Social** underperforms → Reallocate to Google Ads Search/Shopping
- If **Google Display** low ROAS → Move budget to Search/Shopping/PMax
- If **Google Shopping** high ROAS → Scale with impression share analysis (Prompt 2 from Google Ads prompts)

**LTV Consideration:**
- If channel has low ROAS but high repeat purchase rate → May be worth keeping
- Check GA4 cohort analysis to compare LTV by channel
- Email often has lower initial ROAS but drives high LTV (retention)

---

## Usage Guidelines

### When to Use Each Prompt

| Prompt | Best Used For | Frequency | Client Stage |
|--------|--------------|-----------|--------------|
| **Prompt 1: Attribution Analysis** | Budget allocation strategy | Monthly | Established multi-channel |
| **Prompt 2: Conversion Leaks** | Funnel optimization | Quarterly or when CVR drops | All stages |
| **Prompt 3: Customer Segments** | Audience discovery | Monthly | Growth phase |
| **Prompt 4: Checkout Abandonment** | Cart optimization | Monthly or when abandonment spikes | E-commerce |
| **Prompt 5: 24-Hour Traffic** | Daily monitoring | Daily (active campaigns) | Campaign launches |
| **Prompt 6: Seasonality Patterns** | Annual planning | Quarterly (planning cycles) | Established accounts |
| **Prompt 7: Channel Performance** | Budget reallocation | Monthly | All stages |

### Integration with Claude Code MCP

These prompts are designed to work with Claude Code's Google Analytics MCP integration:

1. **Setup:** Ensure GA4 MCP server is configured (see `.mcp.json`)
2. **Usage:** Replace `<Your Property ID>` with actual GA4 property ID
3. **Data Fetching:** Claude Code will use `mcp__google-analytics__*` tools to fetch data
4. **Analysis:** Claude applies the prompt framework to generate structured insights
5. **Output:** Markdown reports saved to client folders for documentation

### MCP Tools Used by Each Prompt

| Prompt | Primary MCP Tools |
|--------|-------------------|
| **Prompt 1** | `run_report` (attribution models), `get_traffic_sources` |
| **Prompt 2** | `get_page_views`, `run_report` (funnel data), `get_events` |
| **Prompt 3** | `run_report` (demographics), `get_active_users` |
| **Prompt 4** | `run_report` (funnel exploration), `get_device_metrics` |
| **Prompt 5** | `get_traffic_sources`, `get_active_users`, `get_device_metrics` |
| **Prompt 6** | `run_report` (date ranges), `get_page_views`, `get_events` |
| **Prompt 7** | `get_traffic_sources`, `run_report` (conversion data) |

---

## ROK Analysis Workflow

### Weekly Client Analysis (Combined GA4 + Google Ads)

**Step 1: GA4 Foundation (Prompt 5 or 7)**
- Run 24-hour traffic report (Prompt 5) for real-time pulse
- OR run channel performance (Prompt 7) for weekly efficiency check

**Step 2: Google Ads Analysis**
- Use Google Ads Prompt 1 (Weekly E-commerce Analysis) from paired knowledge base doc
- Cross-reference Google Ads performance with GA4 traffic sources

**Step 3: Deep Dive Based on Findings**
- **If CVR is down:** Run GA4 Prompt 2 (Conversion Leaks) to find funnel issues
- **If Google Ads ROAS varies by audience:** Run GA4 Prompt 3 (Customer Segments)
- **If cart abandonment is high:** Run GA4 Prompt 4 (Checkout Abandonment)
- **If attribution is unclear:** Run GA4 Prompt 1 (Attribution Analysis)

**Step 4: Strategic Planning**
- Monthly: Run GA4 Prompt 6 (Seasonality) to inform next month's strategy
- Quarterly: Re-run GA4 Prompt 3 (Segments) to find new audience opportunities

---

## Cross-Referencing with Google Ads

**Combined Analysis Example:**

```
Scenario: Google Ads ROAS is declining

Step 1: Run Google Ads Prompt 1 (Weekly Analysis)
Finding: ROAS down 20% WoW, clicks stable

Step 2: Run GA4 Prompt 7 (Channel Performance)
Finding: GA4 shows Paid Search CVR down 25%, traffic quality unchanged

Step 3: Run GA4 Prompt 2 (Conversion Leaks)
Finding: Checkout page exit rate up 30% (site issue, not Google Ads)

Conclusion: ROAS decline is due to website checkout issue, not Google Ads performance.
Action: Fix checkout flow BEFORE adjusting Google Ads strategy.
```

**Root Cause Framework (Combined):**
1. **Check GA4 first:** Is CVR down at website level? (GA4 Prompt 2, 4)
2. **Check attribution:** Is Google Ads being under-credited? (GA4 Prompt 1)
3. **Check audience:** Is Google Ads driving wrong traffic? (GA4 Prompt 3)
4. **Then check Google Ads:** Campaign structure, bids, targeting (Google Ads prompts)

---

## Advanced Techniques

### Prompt Chaining for Comprehensive Diagnosis

**Example: Declining E-commerce Performance**

```
Step 1: GA4 Prompt 7 (Channel Performance)
→ Identifies Paid Search revenue down 15%

Step 2: GA4 Prompt 1 (Attribution Analysis)
→ Confirms Paid Search decline in both last-click and data-driven

Step 3: GA4 Prompt 2 (Conversion Leaks)
→ Shows no funnel issues, CVR stable

Step 4: Google Ads Prompt 2 (Auction Insights)
→ Reveals impression share lost to budget (competitor increased spend)

Conclusion: Need budget increase to compete, not a website or quality issue.
```

### Integration with Client CONTEXT.md

After running GA4 analysis, **ALWAYS update client CONTEXT.md:**

**Add to "Key Learnings" section:**
- Seasonal patterns discovered (GA4 Prompt 6)
- High-value audience segments (GA4 Prompt 3)
- Known conversion friction points (GA4 Prompt 2, 4)

**Add to "Technical Issues" section:**
- Checkout abandonment causes (GA4 Prompt 4)
- Mobile performance gaps (GA4 Prompt 5)
- Traffic quality issues (GA4 Prompt 7)

**Add to "Strategic Context" section:**
- Attribution insights affecting budget decisions (GA4 Prompt 1)
- Channel efficiency benchmarks (GA4 Prompt 7)

---

## GA4 + Google Ads Combined Insights

### Attribution Alignment

**GA4 Prompt 1 (Attribution)** reveals true channel value
↓
**Google Ads Smart Bidding** uses data-driven attribution automatically
↓
**Ensure alignment:** If GA4 shows data-driven favors certain channels, these will also perform better in Google Ads with Smart Bidding

### Audience Export Workflow

**GA4 Prompt 3 (Customer Segments)** identifies high-value audiences
↓
**Create GA4 Audience** (e.g., "High AOV, Female, 25-34, UK")
↓
**Link GA4 to Google Ads** (Admin → Product Linking)
↓
**Import to Google Ads** (Tools → Audience Manager)
↓
**Use in Google Ads:** Bid adjustments, remarketing, Performance Max signals

### Conversion Rate Optimization Priority

Before scaling Google Ads spend, fix GA4-identified issues:

1. **GA4 Prompt 4:** Checkout abandonment 70%+ → Fix checkout first
2. **GA4 Prompt 2:** High exit rate on product pages → Improve content first
3. **GA4 Prompt 5:** Mobile engagement 50% lower → Fix mobile UX first

Then scale Google Ads with confidence that site can convert the traffic.

---

## Customization Tips

### Adjusting Date Ranges

- **Prompt 5 (24-hour):** Extend to 7 days for weekly patterns
- **Prompt 7 (45 days):** Reduce to 30 days for faster-moving businesses
- **Prompt 6 (2 years):** Use 3 years for very established businesses

### Industry-Specific Adaptations

**Lead Gen (not E-commerce):**
- Replace "revenue" and "ROAS" with "leads" and "CPL" (cost per lead)
- Prompt 2: Focus on form completion funnel (not checkout)
- Prompt 3: Segment by company size, industry (B2B demographics)

**Content/Media Sites:**
- Replace conversion metrics with engagement (time on site, pages/session)
- Prompt 2: Analyze content consumption patterns
- Prompt 4: N/A (no checkout flow)

**SaaS:**
- Add trial signup and activation funnels
- Prompt 3: Segment by plan type, company size
- Prompt 7: Calculate LTV carefully (recurring revenue)

---

## Related Resources

### Knowledge Base
- **Google Ads Analysis Prompts:** `roksys/knowledge-base/rok-methodologies/google-ads-analysis-prompts.md` (companion document)
- **GA4 Best Practices:** `roksys/knowledge-base/analytics/` (additional GA4 guides)
- **Platform Updates:** `roksys/knowledge-base/google-ads/platform-updates/` (check for GA4 changes)

### Client Workflows
- **CONTEXT.md:** Always cross-reference GA4 insights with client-specific context
- **Completed Tasks:** Check if recent website changes affected GA4 metrics
- **Meeting Notes:** Reference GA4 discussions with clients

### MCP Integration
- **Setup:** `.mcp.json` configuration for GA4 MCP server
- **Property IDs:** `mcp__google-analytics__list_properties` to find property IDs
- **Documentation:** GA4 MCP server README for technical details

---

## Common Questions

**Q: Which prompt should I run first?**
A: Start with Prompt 5 (24-hour traffic) for daily checks or Prompt 7 (channel performance) for weekly reviews.

**Q: How often should I run these?**
A: Prompt 5 daily during active campaigns, others monthly, Prompt 6 quarterly.

**Q: Can I combine multiple prompts?**
A: Yes! Use prompt chaining (see Advanced Techniques) for comprehensive diagnosis.

**Q: Do I need GA4 MCP integration?**
A: No, but it makes analysis 10x faster. You can also use these prompts manually in GA4 UI.

**Q: Should I run GA4 or Google Ads prompts first?**
A: GA4 first (website foundation), then Google Ads (traffic source optimization).

---

## Document History

| Date | Change |
|------|--------|
| 2025-10-30 | Initial import from GoMarble Prompt Library |
