# File Structure Cleanup - November 8, 2025

## Overview

This document records all file moves and organizational changes made during the project structure cleanup on November 8, 2025.

## Root Directory Cleanup

### Documentation Files Moved to `docs/`

The following files were moved from root to `docs/`:
- `CLAUDE.md`, `CLAUDE 2.md`, `CLAUDE 3.md`, `CLAUDE-MD-REFACTOR.md` → `docs/`
- `CREATE-REMAINING-DOCS.md`, `CREATE-REMAINING-DOCS 2.md` → `docs/`
- `FINISH-CLIENT-DOCS-SETUP.md`, `FINISH-CLIENT-DOCS-SETUP 2.md` → `docs/`
- `SESSION_STATUS.md`, `SESSION_STATUS 2.md` → `docs/`
- `QUICK-REFERENCE.md` → `docs/`
- `WISPR-FLOW-PRIMARY-SYSTEM.md` → `docs/`
- `WISPR-FLOW-SETUP-COMPLETE.md` → `docs/`
- `claude-ai-custom-instructions.txt`, `claude-ai-custom-instructions 2.txt` → `docs/`

**Reason**: These are project documentation files and belong in the `docs/` directory for better organization.

### Client-Specific Files Moved to Client Folders

- `wedding_venues_trend.py` → `clients/devonshire-hotels/scripts/`
- `wedding_venues_chart.html` → `clients/devonshire-hotels/reports/ad-hoc/`

**Reason**: These files are specific to Devonshire Hotels and should be in their client folder.

## Client Folder Cleanup

### bright-minds
- `email-draft-2025-11-03.txt` → `emails/drafts/`
- `WEEKLY-REPORTING-SETUP.md` → `documents/`
- Removed: `WEEKLY-REPORTING-SETUP 2.md` (duplicate)

### clear-prospects
- `email-draft-*.html`, `email-draft-*.txt` → `emails/drafts/`
- `analysis-photo-cushions-channel-performance-2025-11-04.txt` → `documents/`
- `hsg-search-negative-keywords.csv` → `spreadsheets/`
- `EMAIL-STATUS-MICHAEL-OCT-2025.md` → `documents/`
- Removed: `EMAIL-STATUS-MICHAEL-OCT-2025 2.md` (duplicate)

### crowd-control
- `email-draft-*.html` → `emails/drafts/`
- `MONTHLY-REPORTING-WORKFLOW.md` → `documents/`
- `WOOCOMMERCE-MCP-README.md` → `documents/`
- Removed: `WOOCOMMERCE-MCP-README 2.md` (duplicate)

### devonshire-hotels
- `MONTHLY-REPORT-WORKFLOW.md` → `documents/`
- `MONTHLY-REPORT-WORKFLOW-FULL.md` → `documents/`
- `MONTHLY-REPORT-STATUS-OCTOBER-2025.md` → `documents/`
- Removed: `tasks-completed 2.md` (duplicate)

### national-design-academy
- `email-draft-2025-11-03-country-analysis.txt` → `emails/drafts/`

### smythson
- `email-draft-*.txt` → `emails/drafts/`
- `smythson-us-competitors.txt` → `documents/`
- `smythson-uk-pmax-competitors.txt` → `documents/`
- `q4-budget-roas-calculation-summary.txt` → `documents/`
- `DASHBOARD-UPDATE-SUMMARY.md` → `documents/`
- `DASHBOARD-UPDATE-CORRECTED.md` → `documents/`
- `Q4-STRATEGY-QUICK-START.md` → `documents/`
- Removed: `tasks-completed 2.md` (duplicate)

### superspace
- `*.py` files → `scripts/`
- `*.json` files → `product-feeds/`
- `*.txt` files → `documents/`

### tree2mydoor
- Removed duplicates: `README 2.md`, `agents 2.txt`, `llms 2.txt`, `tasks-completed 2.md`

### All Clients
- Removed all `CONTEXT 2.md` duplicate files

### Templates
- Removed duplicates from `clients/_templates/` and `clients/_unassigned/`

## Standard Folder Structure Applied

All client folders now follow the standard structure:
- Root level: Only `CONTEXT.md`, `tasks-completed.md`, `README.md`, `llms.txt`, `agents.txt`
- `emails/drafts/` - Email drafts
- `documents/` - Strategy docs, analysis, workflows
- `scripts/` - Client-specific scripts
- `spreadsheets/` - Data files
- `reports/` - Reports (with subfolders as needed)
- `product-feeds/` - Product data files

## Impact

- **Cleaner root directory**: Only essential project files remain
- **Better organization**: Client files are properly categorized
- **Easier navigation**: Standard structure across all clients
- **Reduced duplication**: Removed all duplicate files

## Notes

- All moves preserve file content and history
- No files were deleted except duplicates
- Scripts and automation should continue to work as file paths are updated
- If any scripts reference moved files, they will need to be updated

