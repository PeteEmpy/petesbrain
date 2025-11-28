# Contributing to Google Specifications Knowledge Base

This guide explains how to add content to the Google Specifications Knowledge Base.

---

## Adding Manual Inputs

### Google Rep Recommendations

**Location**: `google-specifications/_inbox/google-rep-emails/` or `_inbox/meeting-notes/`

**Process**:
1. Drop email exports or meeting notes in the appropriate inbox folder
2. Files are automatically processed every 2 hours
3. Specifications are extracted and tagged with source metadata
4. Processed files are moved to `_inbox/processed/`

**File Formats Supported**:
- `.md` (Markdown)
- `.txt` (Plain text)
- `.eml` (Email exports)

**Naming**: No specific naming convention required - processor handles everything

---

## Source Tagging Guidelines

Every specification **MUST** include source metadata. The processor automatically adds this, but if manually creating files:

### Source Metadata Format

```json
{
  "sources": [
    {
      "type": "google_rep_recommendation",
      "source": "Sarah Johnson - Google Ads Account Manager",
      "date": "2025-11-05",
      "context": "Quarterly review meeting",
      "file": "best-practices/google-ads/google-rep-recommendations/2025-11-05-sarah-johnson-pmax-headlines.md",
      "verified": false
    }
  ]
}
```

### Source Types

- `official_documentation` - Google's official docs (developers.google.com, support.google.com)
- `google_rep_recommendation` - From Google representative (meeting/email)
- `api_reference` - From Google Ads/GA4 API docs
- `support_article` - From Google Support Center
- `best_practice_guide` - From Google's best practice resources
- `code_extraction` - Extracted from existing codebase
- `product_hero_blog` - From Product Hero blog articles

### Verification Status

- `verified: true` - Confirmed accurate (official docs, verified rep recommendations)
- `verified: false` - Unverified recommendation (needs validation)

---

## File Organization

### Specifications (JSON)

**Location**: `{category}/specifications/{subcategory}/{filename}.json`

**Structure**:
```json
{
  "specification": {
    "title": "Specification Title",
    "version": "1.0",
    "last_updated": "2025-11-10",
    "sources": [...],
    "content": {
      // Specification details
    }
  }
}
```

### Best Practices (Markdown)

**Location**: `{category}/best-practices/{subcategory}/{filename}.md`

**Format**:
```markdown
---
title: Best Practice Title
source: Source name/URL
date_added: 2025-11-10
tags: [tag1, tag2]
---

## Summary
- Key point 1
- Key point 2

## Full Content
[content here]
```

---

## Categories

### Google Ads
- `google-ads/specifications/asset-groups/`
- `google-ads/specifications/merchant-center/`
- `google-ads/specifications/campaign-structure/`
- `google-ads/specifications/bidding-strategies/`
- `google-ads/specifications/ad-formats/`

### GA4
- `ga4/specifications/events/`
- `ga4/specifications/conversions/`
- `ga4/specifications/dimensions/`
- `ga4/specifications/metrics/`
- `ga4/specifications/audiences/`
- `ga4/specifications/data-retention/`

### ROK Methodologies
- `rok-methodologies/specifications/product-hero/`
- `rok-methodologies/specifications/profit-metrics/`
- `rok-methodologies/specifications/channable/`

---

## Processing Workflow

1. **Drop files** in `_inbox/` subdirectories
2. **Wait for processing** (runs every 2 hours automatically)
3. **Check processed files** in `_inbox/processed/` if needed
4. **Review generated content** in appropriate category folders
5. **Verify source tagging** is correct

---

## Manual Processing

If you need to process files immediately:

```bash
cd /Users/administrator/Documents/PetesBrain
python3 agents/google-specs-processor/google-specs-processor.py
```

---

## Questions?

- See `docs/GOOGLE-SPECIFICATIONS-KB.md` for system overview
- Check `README.md` for usage examples
- Review existing files for format examples

