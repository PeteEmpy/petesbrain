# Standard Client Folder Structure

This document defines the standard folder structure for all client directories in Pete's Brain.

## Purpose

- **Consistency** across all client folders
- **Easy navigation** - know where to find specific types of files
- **Clean root directory** - only essential files at top level
- **Logical grouping** - files organized by purpose, not date
- **Scalability** - structure works for small and large clients

---

## Folder Structure

```
clients/[client-name]/
├── CONTEXT.md                    ⭐ PRIMARY - Strategic notes & institutional memory
├── tasks-completed.md            ⭐ AUTO-UPDATED - Log of completed Google Tasks
├── README.md                     (Optional - High-level client overview)
├── llms.txt                      (Optional - AI discoverability file)
├── agents.txt                    (Optional - AI agent guidance file)
│
├── emails/                       📧 Email communications (markdown, dated)
│   └── YYYY-MM-DD_subject.md
│
├── meeting-notes/                🎙️ Meeting transcripts and notes
│   └── YYYY-MM-DD_meeting-title.md
│
├── briefs/                       📋 Campaign briefs, project specs
│   └── [brief-name].md
│
├── documents/                    📄 Strategy docs, analysis, written deliverables
│   └── [document-name].md
│
├── analysis/                     🔍 Performance investigations, analytical audit trail
│   └── YYYY-MM-DD-brief-description.md
│
├── presentations/                📊 Client presentations, slide decks
│   └── [presentation-name].pdf/.pptx
│
├── spreadsheets/                 📈 Data exports, analysis sheets
│   └── [spreadsheet-name].xlsx/.csv
│
├── reports/                      📑 Strategy reports, analysis documents (HTML, PDF)
│   ├── q[X]-[year]/             (Quarterly reports grouped together)
│   │   └── [report-name].html
│   ├── pmax-analysis/           (Performance Max analysis reports)
│   │   └── [report-name].html
│   ├── monthly/                 (Monthly performance reports)
│   │   └── YYYY-MM_[report].html
│   └── ad-hoc/                  (One-off analysis and investigations)
│       └── [analysis-name].html
│
├── product-feeds/                🛍️ Product data, supplemental feeds, feed files
│   ├── [active-feed].csv        (Active supplemental feeds at top level)
│   ├── [category-1]/            (Product data organized by category)
│   │   └── [product-data].csv
│   └── [category-2]/
│       └── [product-data].csv
│
└── scripts/                      💻 Client-specific scripts, automation
    └── [script-name].py/.sh
```

---

## Core Files (Root Level Only)

These files **MUST** stay in the root directory:

### ⭐ CONTEXT.md
- **Purpose**: Primary institutional memory for the client
- **Updated by**: Humans + automated tasks monitor
- **Contains**: Strategic notes, learnings, client preferences, historical context
- **Read first**: Always read this before working on client tasks

### ⭐ tasks-completed.md
- **Purpose**: Auto-generated log of all completed Google Tasks
- **Updated by**: Automated tasks monitor (every 6 hours)
- **Contains**: Chronological list of completed tasks with dates and notes
- **DO NOT** manually edit this file

### Optional Root Files:
- **README.md**: High-level client overview, quick facts
- **llms.txt**: AI discoverability file (for client's website)
- **agents.txt**: AI agent guidance file (for client's website)

---

## Folder Descriptions

### 📧 emails/
- Email communications in markdown format
- Filename format: `YYYY-MM-DD_subject.md`
- Auto-imported via email sync system
- Organized chronologically by date in filename

### 🎙️ meeting-notes/
- Meeting transcripts from Granola AI or manual notes
- Filename format: `YYYY-MM-DD_meeting-title.md`
- Auto-imported every 5 minutes from Granola
- **IMPORTANT**: Validate client assignment (may be mis-assigned to wrong client)

### 📋 briefs/
- Campaign briefs, project specifications
- Client requirements documents
- RFPs and proposals

### 📄 documents/
- Strategy documents
- Written analysis and reports (markdown)
- Client deliverables (non-presentation format)
- Investigation notes

### 🔍 analysis/
- **Performance investigations** - Root cause analyses, data deep-dives
- **Analytical audit trail** - Documents WHY decisions were made
- **Methodology findings** - Discovered account behaviors (e.g., conversion lag)
- **Opportunity assessments** - Should we do X? Analysis says...
- **Strategic decision docs** - Why we did/didn't take an action

**What NOT to include**:
- Account changes (those go in experiment log)
- Client-facing reports (those go in reports/)
- Standard reporting (goes in reports/monthly/)

**File naming**: `YYYY-MM-DD-brief-description.md`

**When to create**: Non-trivial investigations (>15 mins) that inform decisions or reveal important account patterns

### 📊 presentations/
- PowerPoint, Google Slides, PDF presentations
- Client-facing slide decks
- Visual reports for meetings

### 📈 spreadsheets/
- Data exports from Google Ads, GA4, etc.
- Analysis spreadsheets
- Budget tracking sheets
- Performance data files

### 📑 reports/
- **Strategy reports** (HTML, PDF)
- **Performance reports** (monthly, quarterly)
- **Analysis reports** (PMax, campaign deep-dives)

**Subdirectories**:
- `q[X]-[year]/` - Quarterly reports (e.g., `q4-2025/`)
- `pmax-analysis/` - Performance Max analysis reports
- `monthly/` - Monthly performance reports (filename: `YYYY-MM_report.html`)
- `ad-hoc/` - One-off investigations and analysis

### 🛍️ product-feeds/
- Product feed files (CSV, JSON, XML)
- Supplemental feeds for Google Merchant Center
- Product data exports

**Organization**:
- Active feeds at top level (e.g., `Client_Custom_Label_0_Q4_2025.csv`)
- Historical/working files in subdirectories by category
- Example subdirs: `card-holders/`, `travel-bags/`, `shoes/`, etc.

### 💻 scripts/
- Client-specific Python/Bash scripts
- Automation tools
- Data processing scripts
- Upload/download utilities

---

## Migration Guidelines

When migrating an existing client to this structure:

1. **DO NOT delete anything** - only move files
2. **Create new folders** as needed
3. **Move files** to appropriate folders based on type and purpose
4. **Keep CONTEXT.md and tasks-completed.md** in root
5. **Test after migration** - verify no broken paths in scripts/docs

### Common Files to Organize:

| File Type | Destination |
|-----------|-------------|
| `.html` reports | `reports/[subdir]/` |
| `.csv` product data | `product-feeds/[category]/` |
| `.csv` analysis data | `spreadsheets/` |
| `.py`, `.sh` scripts | `scripts/` |
| `.md` analysis docs | `documents/` |
| `.md` investigation notes | `documents/` or `reports/ad-hoc/` |

---

## Examples

### Clean Root (Godshot)
```
clients/godshot/
├── CONTEXT.md
├── tasks-completed.md
├── emails/
├── meeting-notes/
└── [other standard folders]
```

### Organized Reports (Smythson)
```
clients/smythson/
├── CONTEXT.md
├── tasks-completed.md
├── reports/
│   ├── q4-2025/
│   │   ├── q4-2025-strategy-report-final.html
│   │   └── asset-groups-to-create.html
│   └── pmax-analysis/
│       ├── pmax-asset-usage-guide.html
│       └── pmax-placement-examples.html
└── product-feeds/
    ├── Smythson_Custom_Label_0_Q4_2025.csv
    ├── card-holders/
    │   └── product-data.csv
    └── travel-bags/
        └── product-data.csv
```

### Messy (Before Organization)
```
clients/superspace/
├── CONTEXT.md
├── aus-data-new.csv              ❌ Root clutter
├── uk-search-terms.csv           ❌ Root clutter
├── upload_us_data.py             ❌ Root clutter
├── fetch_all_search_terms.py     ❌ Root clutter
└── [30+ more files in root]      ❌ Root clutter
```

### Clean (After Organization)
```
clients/superspace/
├── CONTEXT.md
├── tasks-completed.md
├── product-feeds/
│   ├── aus/
│   │   ├── aus-data-new.csv
│   │   └── aus-search-terms.csv
│   ├── uk/
│   │   ├── uk-data-new.csv
│   │   └── uk-search-terms.csv
│   └── us/
│       ├── us-data-new.csv
│       └── us-search-terms.csv
└── scripts/
    ├── upload_us_data.py
    ├── fetch_all_search_terms.py
    └── fetch_and_organize.py
```

---

## Rollout Process

1. **Phase 1**: Document standard (this file) ✅
2. **Phase 2**: Update CLAUDE.md with new standard
3. **Phase 3**: Migrate high-priority clients (Smythson ✅, Tree2mydoor, Superspace)
4. **Phase 4**: Migrate remaining active clients
5. **Phase 5**: Update automation scripts to respect new structure

---

## Benefits

✅ **Consistency** - All clients follow same structure
✅ **Scalability** - Works for 10 files or 1000 files
✅ **Discoverability** - Easy to find specific types of files
✅ **Clean root** - Only essential files at top level
✅ **Logical grouping** - Files organized by purpose
✅ **Future-proof** - New file types have obvious homes
✅ **Automation-friendly** - Scripts know where to find/place files

---

## Questions?

See `/docs/CLIENT-FOLDER-ORGANIZATION.md` for more details or ask Claude Code for help with migration.
