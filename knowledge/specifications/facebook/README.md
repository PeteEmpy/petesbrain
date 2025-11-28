# Facebook Specifications Knowledge Base System

**Status:** ✅ Active  
**Last Updated:** 2025-11-12

---

## Overview

The Facebook Specifications Knowledge Base is a comprehensive system for managing Facebook Ads, Instagram Ads, and Meta Business Suite specifications, requirements, and best practices. It serves as the authoritative source for account setup requirements and campaign optimization guidance.

**Key Features**:
- **Source Tagging**: Every specification tagged with source (official docs, Meta rep, etc.)
- **Dual Format**: JSON (programmatic) + Markdown (searchable)
- **Comprehensive Coverage**: Facebook Ads + Instagram Ads + Meta Business Suite

---

## Architecture

### Knowledge Base Structure

```
facebook-specifications/
├── facebook-ads/          # Facebook Ads specifications
├── meta-business-suite/   # Meta Business Suite specifications
├── _inbox/                # Manual input staging area
└── index.json             # Master index for programmatic access
```

### Dual Format System

**1. Structured Data (JSON)**
- Location: `{category}/specifications/` subdirectories
- Purpose: Programmatic access for tools and validation
- Format: Standardized JSON schema with versioning and source metadata

**2. Searchable Documentation (Markdown)**
- Location: `{category}/best-practices/` subdirectories
- Purpose: Human-readable guides, searchable via KB search tool
- Format: Markdown with frontmatter

---

## Key Specification Areas

### Facebook Ads
- **Ad Formats**: Single Image, Video, Carousel, Collection, Stories, Reels
- **Campaign Types**: Awareness, Traffic, Engagement, Conversions, App Promotion
- **Audience Targeting**: Custom Audiences, Lookalike Audiences, Detailed Targeting
- **Bidding Strategies**: Lowest Cost, Cost Cap, Bid Cap, ROAS, Value Optimization
- **Facebook Pixel Setup**: Installation, event tracking, standard events
- **Conversions API**: Server-side tracking, event matching, deduplication
- **Creative Specifications**: Image sizes, video lengths, text limits, aspect ratios
- **Account Structure**: Ad Accounts, Business Manager, Pages, Instagram Accounts

### Meta Business Suite
- Business Manager setup and configuration
- Page management and permissions
- Ad account management and billing
- User roles and permissions
- Payment methods and billing settings

---

## Source Tagging System

Every specification includes comprehensive source metadata:

```json
{
  "sources": [
    {
      "type": "official_documentation",
      "url": "https://www.facebook.com/business/help/...",
      "last_checked": "2025-11-12",
      "verified": true,
      "content_hash": "sha256:..."
    }
  ]
}
```

**Source Types**:
- `official_documentation` - Meta's official docs
- `meta_rep_recommendation` - From Meta representative
- `api_reference` - From Meta Marketing API docs
- `support_article` - From Meta Business Help Center
- `best_practice_guide` - From Meta's best practice resources
- `code_extraction` - Extracted from existing codebase

---

## Integration Points

### Claude Code Skills
- Auto-references specs when providing Facebook Ads advice
- Validates recommendations against current specifications
- Cites specification sources
- Distinguishes between official specs and rep recommendations

### Knowledge Base Search
- Extended `tools/kb-search.py` to search Facebook specifications
- Filter by source type and category
- Search both technical specs and best practices

---

## File Locations

**Knowledge Base**: `/Users/administrator/Documents/PetesBrain/facebook-specifications/`

**State Files**:
- `shared/data/facebook-specs-state.json`
- `shared/data/facebook-specs-changelog.json`
- `shared/data/facebook-specs-index.json`

**Configuration**:
- `facebook-specifications/monitor-urls.json` (future)
- `facebook-specifications/index.json` (master index)

---

## Related Documentation

- [Knowledge Base System](../docs/KNOWLEDGE-BASE.md) - Overview of news KB
- [Google Specifications KB](../docs/GOOGLE-SPECIFICATIONS-KB.md) - Reference implementation
- [Knowledge Base Search](../docs/KNOWLEDGE-BASE-SEARCH.md) - Search functionality

---

**Last Updated**: 2025-11-12  
**Maintained By**: Peter Empson, ROK Systems


