# ROK Systems Knowledge Base

A curated collection of reference materials, best practices, and strategic guidance for Google Ads, Facebook Ads, Shopify, AI, and performance marketing. This knowledge base is used by Claude Code to provide informed, up-to-date advice on client campaigns and strategies.

## Purpose

This knowledge base serves as the **authoritative reference** for:
- Google Ads best practices and platform updates
- Facebook Ads and Instagram Ads best practices and platform updates
- Shopify platform features, integrations, and optimization
- AI strategy and automation approaches
- Analytics and measurement frameworks
- Industry insights and trends
- ROK's proprietary methodologies

When Claude Code provides strategic advice, it consults this knowledge base to ensure recommendations are current and aligned with proven practices.

## Folder Structure

```
knowledge-base/
├── _inbox/                    # 📥 DROP ZONE - Add unprocessed materials here
│   ├── emails/               # Email exports from Google, Meta, partners, etc.
│   ├── documents/            # PDFs, articles, research papers
│   └── videos/               # Video transcripts, YouTube notes
├── google-ads/               # Google Ads platform guidance
│   ├── performance-max/      # PMax strategies, optimization
│   ├── shopping/             # Shopping campaigns, feeds
│   ├── search/               # Search campaigns, keywords
│   ├── platform-updates/     # Latest Google announcements
│   └── bidding-automation/   # Smart Bidding, tROAS strategies
├── facebook-ads/             # Facebook & Instagram Ads platform guidance
│   ├── campaigns/            # Campaign strategies, optimization
│   ├── audiences/            # Audience targeting, lookalikes
│   ├── creative/              # Ad creative best practices
│   ├── platform-updates/     # Meta/Facebook announcements
│   ├── bidding-optimization/ # Bid strategies, cost caps
│   ├── measurement/          # Pixel, Conversions API, attribution
│   └── meta-business-suite/  # Meta Business Suite features
├── shopify/                  # Shopify platform guidance
│   ├── product-feeds/        # Feed optimization for Google Shopping
│   ├── checkout-conversion/  # Checkout optimization, cart recovery
│   ├── marketing-channels/   # Google Shopping, campaign setup
│   ├── analytics-tracking/   # Conversion tracking, pixels
│   ├── store-management/     # Store setup, configuration
│   ├── apps-integrations/    # Marketing apps, third-party tools
│   └── platform-updates/     # Shopify feature updates
├── ai-strategy/              # AI in marketing and advertising
├── analytics/                # GA4, attribution, tracking
├── industry-insights/        # Market trends, competitive intel
└── rok-methodologies/        # ROK's frameworks and processes
```

## 📥 Using the Inbox

### Drop files here for automatic processing

The `_inbox/` folder is a **staging area** for unprocessed knowledge materials:

1. **Drop any relevant content**:
   - Email exports (.eml, .md, .txt)
   - PDFs, Word docs, articles
   - **YouTube URLs** (transcripts auto-fetched!)
   - Video transcripts or notes
   - URLs in text files
   - Screenshots of important info

2. **Automated processing runs every 6 hours**:
   - Script reads each file
   - **YouTube transcripts automatically fetched** from URLs
   - Extracts key information
   - Categorizes by topic
   - Moves to appropriate folder
   - Updates this index
   - Clears inbox

3. **Email auto-import** (optional):
   - Configure email sync to pull labeled emails
   - Emails from trusted sources (Google, partners)
   - Automatically saved to `_inbox/emails/`

### File Naming Conventions

When adding files manually, use descriptive names:
- `2025-10-pmax-audience-signals-update.pdf`
- `google-newsletter-2025-10-29.md`
- `youtube-transcript-smart-bidding-strategies.txt`

Dates help track freshness of information.

## 🤖 Automated Industry News Monitoring

**NEW**: The system now automatically monitors top Google Ads AND Facebook Ads industry websites!

Every 6 hours, the industry news monitors:
1. ✅ **Google Ads Monitor**: Checks RSS feeds from 9+ respected Google Ads sources
2. ✅ **Facebook Ads Monitor**: Checks RSS feeds from 10+ Facebook/Meta advertising sources
3. 🤖 Scores each article for relevance (0-10) using AI
4. 📥 Imports articles scoring 6+ to the inbox
5. 🗂️ Articles auto-processed and categorized by existing inbox system

**Google Ads Sources monitored:**
- Search Engine Land (Google Ads & PPC)
- Search Engine Journal (PPC)
- Google Ads Blog (Official)
- Think with Google
- WordStream Blog
- PPC Hero
- Neil Patel Blog
- Unbounce Blog

**Facebook Ads Sources monitored:**
- Meta for Business Blog (Official)
- Social Media Examiner (Facebook Ads)
- AdEspresso Blog
- WordStream (Facebook Ads)
- Hootsuite Blog (Facebook)
- Buffer Blog (Facebook)
- Sprout Social (Facebook)
- Reddit r/FacebookAds
- And more...

**Benefits:**
- Stay current with platform updates automatically (both Google and Facebook)
- High-quality, AI-filtered content (no noise)
- Zero manual effort required
- Knowledge base always up-to-date

**Learn more:** See `INDUSTRY-NEWS-MONITORING.md` for details

## 📝 Document Format

All knowledge base documents follow this markdown format:

```markdown
---
title: Document Title
source: URL or Source Name
date_added: YYYY-MM-DD
last_updated: YYYY-MM-DD
tags: [tag1, tag2, tag3]
---

## Summary

Brief overview of key takeaways (3-5 bullet points)

## Full Content

[Main content here]

## Key Insights

- Important insights extracted from content
- Actionable recommendations
- Strategic implications

## Related Topics

- Links to related knowledge base docs
```

## 🔄 How Claude Code Uses This

When working on client tasks, Claude Code will:

1. **Check relevant sections** before giving strategic advice
2. **Reference specific documents** (e.g., "Per roksys/knowledge-base/google-ads/performance-max/asset-optimization.md...")
3. **Prioritize KB guidance** over generic best practices
4. **Cross-reference** with client CONTEXT.md for informed recommendations
5. **Stay current** with platform updates and industry changes

## 📊 Knowledge Base Index

### Google Ads
- (Documents will be listed here as they're added)

### Facebook Ads
- (Documents will be listed here as they're added)

### Shopify
#### Product Feeds (`shopify/product-feeds/`)
- [Google Shopping Feed Optimization (2025)](shopify/product-feeds/google-shopping-feed-optimization-2025.md) - Complete guide to optimizing product feeds for Google Shopping, including titles, images, GTINs, and custom labels

#### Checkout & Conversion (`shopify/checkout-conversion/`)
- [Checkout Optimization Best Practices (2025)](shopify/checkout-conversion/checkout-optimization-best-practices-2025.md) - 13 proven strategies to reduce cart abandonment (69.82% avg) and increase conversion rates

#### Marketing Channels (`shopify/marketing-channels/`)
- [Google Shopping Master Guide (2025)](shopify/marketing-channels/google-shopping-master-guide-2025.md) - Complete setup and optimization guide for Google Shopping campaigns via Shopify (case study: 71% revenue increase)

#### Analytics & Tracking (`shopify/analytics-tracking/`)
- [Conversion Tracking Setup Guide (2025)](shopify/analytics-tracking/conversion-tracking-setup-guide-2025.md) - Step-by-step guide for Google Ads conversion tracking via Google & YouTube app or custom pixel

#### Apps & Integrations (`shopify/apps-integrations/`)
- [Essential Marketing Apps (2025)](shopify/apps-integrations/essential-marketing-apps-2025.md) - Curated list of essential Shopify apps for advertising, email, reviews, upselling, and analytics

**See also**: [Shopify Knowledge Base README](shopify/README.md) for complete overview

### AI Strategy
- (Documents will be listed here as they're added)

### Analytics
- (Documents will be listed here as they're added)

### Industry Insights
- (Documents will be listed here as they're added)

### ROK Methodologies
- (Documents will be listed here as they're added)

---

**Last Updated**: 2025-11-12
**Total Documents**: 1117
**Inbox Items Pending**: 1
