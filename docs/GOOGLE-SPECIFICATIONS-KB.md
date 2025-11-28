# Google Specifications Knowledge Base System

**Status:** ✅ Active  
**Last Updated:** 2025-11-10

---

## Overview

The Google Specifications Knowledge Base is a comprehensive, automatically-updated system for managing Google Ads, GA4, and ROK methodology specifications, requirements, and best practices. It serves as the authoritative source for account setup requirements, ensuring all recommendations are based on current, verified specifications.

**Key Features**:
- **Source Tagging**: Every specification tagged with source (official docs, Google rep, etc.)
- **API Efficiency**: Batched API calls reduce costs by 80-90%
- **Efficient Initial Load**: Incremental processing with resume capability
- **Dual Format**: JSON (programmatic) + Markdown (searchable)
- **Comprehensive Coverage**: Google Ads + GA4 + ROK Methodologies

---

## Architecture

### Knowledge Base Structure

```
google-specifications/
├── google-ads/          # Google Ads specifications
├── ga4/                 # GA4 specifications
├── rok-methodologies/   # ROK-specific tools (Product Hero, ProfitMetrics, Channable)
├── _inbox/              # Manual input staging area
└── index.json           # Master index for programmatic access
```

### Dual Format System

**1. Structured Data (JSON)**
- Location: `{category}/specifications/` subdirectories
- Purpose: Programmatic access for tools and validation
- Format: Standardized JSON schema with versioning and source metadata
- Used by: Google Ads Generator, audit tools, validation scripts

**2. Searchable Documentation (Markdown)**
- Location: `{category}/best-practices/` subdirectories
- Purpose: Human-readable guides, searchable via KB search tool
- Format: Markdown with frontmatter (similar to current KB)
- Used by: Claude Code, manual reference, KB search tool

---

## Components

### 1. Weekly Documentation Monitor

**Location**: `agents/google-specs-monitor.py`

**Purpose**: Automatically check Google Ads and GA4 documentation for updates weekly

**Schedule**: Sunday 2:00 AM

**Process**:
1. Collects URLs from `monitor-urls.json` config file
2. Fetches all documentation pages in parallel (20-30 concurrent)
3. Compares SHA-256 content hashes to detect changes
4. Batches changed pages (6-8 per Claude API call) for efficiency
5. Extracts specifications and updates JSON files with source tags
6. Generates markdown summaries for best-practices/
7. Logs all changes with source URLs and timestamps

**Efficiency**: 80-90% reduction in API calls via batching

### 2. Manual Input Processor

**Location**: `agents/google-specs-processor.py`

**Purpose**: Process manual additions from Google rep emails/meetings

**Schedule**: Every 2 hours (same as KB processor)

**Process**:
1. Monitors inbox folders (`_inbox/google-rep-emails/`, `_inbox/meeting-notes/`, `_inbox/manual-additions/`)
2. Batches files (6-8 per Claude API call)
3. Extracts specifications, categorizes, and tags sources
4. Updates JSON files or creates best-practice markdown
5. Moves processed files to `_inbox/processed/`

**Source Tagging**: Every item tagged with source type, name, date, context, and verification status

### 3. Specification Index Generator

**Location**: `tools/google-specs-indexer.py`

**Purpose**: Generate master index for programmatic access

**Output**: `google-specifications/index.json`

**Structure**: Hierarchical index with version numbers, last updated dates, and source metadata

### 4. KB Search Integration

**Enhancement**: Extended `tools/kb-search.py` to search both knowledge bases

**New Commands**:
- `--specs` - Search specifications KB only
- `--include-specs` - Search both KBs
- `--source` - Filter by source type

### 5. Initial Specification Extraction

**Location**: `tools/extract-initial-specs.py`

**Purpose**: One-time extraction of specifications from multiple sources

**Sources**:
- Google Ads Generator code
- Existing KB articles
- Google documentation (web scraping)
- Product Hero blog articles
- Channable documentation
- ProfitMetrics from client CONTEXT.md files

**Process**: Phased extraction with batched API calls, incremental saving, and resume capability

---

## Source Tagging System

Every specification includes comprehensive source metadata:

```json
{
  "sources": [
    {
      "type": "official_documentation",
      "url": "https://developers.google.com/...",
      "last_checked": "2025-11-10",
      "verified": true,
      "content_hash": "sha256:..."
    }
  ]
}
```

**Source Types**:
- `official_documentation` - Google's official docs
- `google_rep_recommendation` - From Google representative
- `api_reference` - From Google Ads/GA4 API docs
- `support_article` - From Google Support Center
- `best_practice_guide` - From Google's best practice resources
- `code_extraction` - Extracted from existing codebase
- `product_hero_blog` - From Product Hero blog articles

---

## Key Specification Areas

### Google Ads
- Asset Groups (Performance Max, RSA, Standard Search)
- Merchant Center Feeds
- Campaign Structure
- Bidding Strategies
- Ad Formats

### GA4
- Events (Standard, Custom, Parameters)
- Conversions
- Dimensions & Metrics
- Audiences
- Data Retention

### ROK Methodologies
- Product Hero Labelizer
- Channel Profit Metrics (ProfitMetrics)
- Channable Feed Management

---

## Integration Points

### Google Ads Generator Tool
- Reads specs from `google-ads/specifications/asset-groups/performance-max.json`
- Validates generated assets against specifications
- Enforces requirements in prompts
- Cites sources in output

### Audit Tools
- References campaign structure specs
- Compares account setup against best practices
- Flags deviations from specifications
- Includes source citations in reports

### Claude Code Skills
- Auto-references specs when providing advice
- Validates recommendations against current specifications
- Cites specification sources
- Distinguishes between official specs and rep recommendations

### Product Impact Analyzer
- References Channable feed specifications
- Uses Product Hero label specifications
- References ProfitMetrics POAS calculations

---

## Automation Schedule

**Weekly**:
- Documentation monitor: Sunday 2:00 AM
- Specification index rebuild: After any updates

**Continuous**:
- Manual input processor: Every 2 hours

**LaunchAgents**:
- `com.petesbrain.google-specs-monitor.plist`
- `com.petesbrain.google-specs-processor.plist`

---

## File Locations

**Knowledge Base**: `/Users/administrator/Documents/PetesBrain/google-specifications/`

**Agent Scripts**:
- `agents/google-specs-monitor.py`
- `agents/google-specs-processor.py`

**Tools**:
- `tools/google-specs-indexer.py`
- `tools/extract-initial-specs.py`

**State Files**:
- `shared/data/google-specs-state.json`
- `shared/data/google-specs-changelog.json`
- `shared/data/google-specs-index.json`
- `shared/data/google-specs-content-hashes.json`
- `shared/data/extract-initial-specs-progress.json`

**Configuration**:
- `google-specifications/monitor-urls.json`
- `google-specifications/spec-schema.json`
- `google-specifications/rok-methodologies-sources.json`

---

## Usage Examples

### Search Specifications

```bash
# Search specs KB only
python3 tools/kb-search.py --specs "headline requirements"

# Search both KBs
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
spec_path = index['google_ads']['specifications']['asset-groups']['performance-max']['file']
with open(f'google-specifications/{spec_path}') as f:
    specs = json.load(f)
```

---

## Maintenance

**Monitoring**: Check LaunchAgent status regularly
**Logs**: Review `shared/data/google-specs-changelog.json` for updates
**Index**: Rebuild index after manual changes: `python3 tools/google-specs-indexer.py`

---

## Related Documentation

- [Knowledge Base System](../KNOWLEDGE-BASE.md) - Overview of news KB
- [Knowledge Base Search](../KNOWLEDGE-BASE-SEARCH.md) - Search functionality
- [CLAUDE.md](../CLAUDE.md) - System architecture

---

**Last Updated**: 2025-11-10  
**Maintained By**: Peter Empson, ROK Systems

