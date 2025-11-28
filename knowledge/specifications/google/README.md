# Google Specifications Knowledge Base

**Purpose**: Authoritative source for Google Ads, GA4, and ROK methodology specifications, requirements, and best practices.

**Status**: Active - Updated weekly via automated monitoring

---

## Overview

This knowledge base serves as the **single source of truth** for:

- **Google Ads Specifications**: Asset requirements, Merchant Center feeds, campaign structure, bidding strategies
- **GA4 Specifications**: Event definitions, conversion tracking, dimensions/metrics, data retention
- **ROK Methodologies**: Product Hero, Channel Profit Metrics, Channable implementation guides

**Key Features**:
- ✅ Source tagging - Every specification includes source metadata
- ✅ Dual format - JSON (programmatic) + Markdown (searchable)
- ✅ Weekly automated updates from Google documentation
- ✅ Manual input processing for Google rep recommendations
- ✅ Comprehensive coverage of all specification areas

---

## Structure

```
google-specifications/
├── google-ads/          # Google Ads specifications and best practices
├── ga4/                 # GA4 specifications and best practices
├── rok-methodologies/   # ROK-specific tools and methodologies
├── _inbox/              # Manual input staging area
└── index.json           # Master index for programmatic access
```

---

## Usage

### Search Specifications

```bash
# Search specifications KB only
python3 tools/kb-search.py --specs "headline requirements"

# Search both KBs (news + specs)
python3 tools/kb-search.py "performance max" --include-specs

# Filter by source
python3 tools/kb-search.py --specs "headlines" --source "official_documentation"
```

### Programmatic Access

```python
import json

# Load master index
with open('google-specifications/index.json') as f:
    index = json.load(f)

# Access specific specification
spec_file = index['google_ads']['specifications']['asset-groups']['performance-max']['file']
with open(f'google-specifications/{spec_file}') as f:
    specs = json.load(f)
```

### Adding Manual Inputs

1. **Google Rep Recommendations**: Drop emails/meeting notes in `_inbox/google-rep-emails/` or `_inbox/meeting-notes/`
2. **Manual Additions**: Drop files in `_inbox/manual-additions/`
3. **Processing**: Files are automatically processed every 2 hours
4. **Source Tagging**: All content is tagged with source metadata automatically

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## Source Types

Every specification includes source metadata:

- `official_documentation` - Google's official docs
- `google_rep_recommendation` - From Google representative
- `api_reference` - From Google Ads/GA4 API docs
- `support_article` - From Google Support Center
- `best_practice_guide` - From Google's best practice resources
- `code_extraction` - Extracted from existing codebase
- `product_hero_blog` - From Product Hero blog articles

---

## Automation

**Weekly Monitoring**: Sunday 2:00 AM
- Checks Google Ads and GA4 documentation for updates
- Extracts new/changed specifications
- Updates JSON files with source tags

**Continuous Processing**: Every 2 hours
- Processes manual inputs from inbox
- Extracts specifications and best practices
- Tags with source metadata

---

## Integration

This knowledge base integrates with:

- **Google Ads Generator** - Validates assets against specifications
- **Audit Tools** - References specs when auditing accounts
- **Claude Code Skills** - Auto-references specs in recommendations
- **Product Impact Analyzer** - Uses ROK methodology specs

---

## Maintenance

**Last Updated**: 2025-11-10
**Total Specifications**: See `index.json` for current count
**Change Log**: `shared/data/google-specs-changelog.json`

For questions or issues, see [CONTRIBUTING.md](CONTRIBUTING.md) or check the system documentation in `docs/GOOGLE-SPECIFICATIONS-KB.md`.

