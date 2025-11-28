# PMAX Asset Optimiser - Complete Workflow

**Purpose**: Automated system for identifying underperforming Performance Max assets and generating AI-powered replacement suggestions with safe execution.

**Location**: `/Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser/`

**Status**: Production-ready (as of 2025-11-27)

---

## 🚨 READ THIS FIRST - MANDATORY FOR ALL PMAX WORK

**BEFORE running analysis for ANY client, you MUST:**

1. ✅ **READ the "Quick Reference Commands" section** (bottom of this file)
2. ✅ **Follow ALL 3 steps** - do NOT skip Step 2 (generate replacements)
3. ✅ **Verify output has Option_Number column (1, 2, 3)** before delivery

**Why?** The client doesn't want just data - they want **3 actionable options to choose from** for each underperformer.

**Quick link to correct workflow:** [Jump to Complete Pipeline](#quick-reference-commands)

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Prerequisites](#prerequisites)
4. [Complete Workflow](#complete-workflow)
5. [Scripts Reference](#scripts-reference)
6. [File Outputs](#file-outputs)
7. [Safety Features](#safety-features)
8. [Troubleshooting](#troubleshooting)
9. [Future Automation](#future-automation)

---

## Overview

### What It Does

1. **Analyses** Google Ads Performance Max asset performance data
2. **Identifies** underperforming assets (low CTR, zero conversions, high cost/conv)
3. **Generates** AI-powered replacement suggestions using Claude Sonnet 4
4. **Creates** review interface in Google Sheets for approval
5. **Executes** asset swaps safely via Google Ads API

### Key Features

- ✅ **Deduplication**: Ensures unique suggestions within asset groups
- ✅ **URL-based context**: Uses landing page content for relevant suggestions
- ✅ **Safety checks**: Validates minimum requirements before execution
- ✅ **Dry-run mode**: Test changes before going live
- ✅ **Asset Group ID tracking**: Prevents wrong-group execution
- ✅ **Batch processing**: Efficient handling of multiple assets

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PMAX Asset Optimiser                         │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  1. DATA INPUT   │
│  ───────────────┤
│  • Google Ads    │───┐
│  • Asset data    │   │
│  • Performance   │   │
└──────────────────┘   │
                       ▼
               ┌───────────────────┐
               │  2. ANALYSIS      │
               │  ────────────────┤
               │  • Identify poor  │
               │    performers     │
               │  • Calculate avg  │
               │  • Flag issues    │
               └───────────────────┘
                       │
                       ▼
               ┌───────────────────┐
               │  3. GENERATION    │
               │  ────────────────┤
               │  • Claude API     │
               │  • URL context    │
               │  • Deduplication  │
               └───────────────────┘
                       │
                       ▼
               ┌───────────────────┐
               │  4. REVIEW        │
               │  ────────────────┤
               │  • Google Sheets  │
               │  • User selection │
               │  • Approval UI    │
               └───────────────────┘
                       │
                       ▼
               ┌───────────────────┐
               │  5. EXECUTION     │
               │  ────────────────┤
               │  • Dry-run test   │
               │  • User approval  │
               │  • Live execution │
               └───────────────────┘
```

---

## Prerequisites

### Required Credentials

1. **Google Ads API** (`google-ads.yaml`)
   - Developer token
   - OAuth2 credentials (client ID, client secret, refresh token)
   - Customer ID (10-digit account number)

2. **Anthropic API** (`.env`)
   - `ANTHROPIC_API_KEY` for Claude Sonnet 4

3. **Google Sheets API** (credentials for upload/download)
   - OAuth2 credentials
   - Sheet ID for review interface

### Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Key Dependencies:**
- `google-ads` (Google Ads API)
- `anthropic` (Claude API)
- `beautifulsoup4` (URL scraping)
- `pandas` (data processing)
- `gspread` / `google-auth` (Google Sheets)

---

## Complete Workflow

### Phase 1: Data Collection & Analysis

**Objective**: Pull asset performance data and identify underperformers

#### Step 1.1: Extract Asset Performance Data

**Script**: `extract_asset_performance.py`

```bash
.venv/bin/python3 extract_asset_performance.py \
  --customer-id 4941701449 \
  --campaign-id 15820346778 \
  --start-date 2025-08-28 \
  --end-date 2025-11-26
```

**What it does**:
- Queries Google Ads API for asset-level performance
- Extracts: impressions, clicks, CTR, conversions, conv rate, cost/conv
- Includes: Campaign ID, Asset Group ID, Asset Group Name, Asset Type
- Saves to: `output/asset-performance-{customer_id}-{date}.csv`

**Output columns**:
```
Campaign ID, Campaign, Asset Group ID, Asset Group, Asset Group URL,
Asset, Asset type, Status, Impr., Clicks, CTR, Conversions, Conv. rate,
Currency code, Cost, Cost / conv., Conv. value, Avg. CPC
```

#### Step 1.2: Identify Underperformers

**Script**: `identify_underperformers.py`

```bash
.venv/bin/python3 identify_underperformers.py \
  --customer-id 4941701449 \
  --csv output/asset-performance-4941701449-2025-11-26.csv
```

**What it does**:
- Calculates average CTR and conversion rate per asset type
- Flags assets that are:
  - Zero conversions with high impressions (>1000)
  - Low CTR (below average)
  - Low conversion rate (below average)
  - High cost/conversion (above average)
- Assigns priority: HIGH, MEDIUM, LOW
- Saves to: `output/underperforming-assets.csv`

**Flagging logic**:
```python
if conversions == 0 and impressions > 1000:
    priority = HIGH
elif ctr < avg_ctr and conv_rate < avg_conv_rate:
    priority = HIGH
elif cost_per_conv > avg_cost_per_conv * 1.5:
    priority = MEDIUM
```

---

### Phase 2: Generate Replacement Suggestions

**Objective**: Create AI-powered, unique replacement suggestions

#### Step 2.1: Generate Replacements

**Script**: `generate_replacement_text.py`

```bash
.venv/bin/python3 generate_replacement_text.py \
  --customer-id 4941701449 \
  --csv output/asset-performance-4941701449-2025-11-26.csv
```

**What it does**:
1. **Groups assets** by Asset Group + URL + Type
2. **Extracts URL content** (product info, features, benefits)
3. **Generates 3 alternatives** per asset using Claude Sonnet 4
4. **Deduplicates** within asset groups:
   - Tracks all generated texts in batch
   - Passes avoid list to AI prompt
   - Ensures unique suggestions per group
5. Validates character limits (30 for headlines, 90 for long/desc)
6. Saves to: `output/replacement-candidates.csv`

**AI Prompt Structure**:
```
You are a Google Ads copywriter for Tree2mydoor...

Current underperforming asset:
- Text: "Big Choice - Affordable Prices"
- Type: Headline (max 30 chars)
- Issue: Zero conversions, low CTR

Product context from landing page:
- Features: Gift-wrapped, next-day delivery
- Benefits: Mediterranean garden style

CRITICAL: AVOID DUPLICATES
Already generated for this group:
- "Mediterranean Olive Trees"
- "Premium Patio Plants"

Generate 3 UNIQUE alternatives...
```

**Deduplication mechanism**:
```python
batch_generated_texts = []

for asset in asset_group:
    alternatives = generate_replacements(
        asset,
        num_alternatives=3,
        avoid_texts=batch_generated_texts  # Pass existing suggestions
    )
    batch_generated_texts.extend([alt['text'] for alt in alternatives])
```

**Output columns**:
```
Campaign_ID, Campaign, Asset_Group_ID, Asset_Group, Original_Text,
Asset_Type, Impressions, CTR, Conv_Rate, Flag_Reason, Priority,
Option_Number, Replacement_Text, Char_Count, Char_Limit, Valid
```

**Timing**: ~3 seconds per asset, ~7-8 minutes for 154 assets

---

### Phase 3: Review & Selection

**Objective**: Present suggestions in Google Sheets for user approval

#### Step 3.1: Create Review Sheet

**Script**: `create_review_sheet.py`

```bash
.venv/bin/python3 create_review_sheet.py \
  --customer-id 4941701449
```

**What it does**:
1. Reads `replacement-candidates.csv`
2. Transforms to "Devonshire format" (wide format with options as columns)
3. Saves to: `output/tree2mydoor-review-sheet.csv`

**Format transformation**:

**Before (replacement-candidates.csv)**:
```
Asset,Type,Priority,Option_Number,Replacement_Text
"Big Choice",Headline,HIGH,1,"Mediterranean Olive Trees"
"Big Choice",Headline,HIGH,2,"Premium Patio Plants"
"Big Choice",Headline,HIGH,3,"Authentic Tree Gifts"
```

**After (review-sheet.csv)**:
```
Asset,Type,Priority,Option 1,Option 2,Option 3,Selected Option
"Big Choice",Headline,HIGH,"Mediterranean..","Premium..","Authentic..",""
```

#### Step 3.2: Upload to Google Sheets

**Manual step** (or could be automated):
1. Open: https://docs.google.com/spreadsheets/d/1XYW4jVS785qnj2gFauPc4uJSnpOZOJck0OLo4nFZNTI/edit
2. Go to sheet: "Replacement Candidates"
3. Clear existing data
4. Import `output/tree2mydoor-review-sheet.csv`

**Google Sheets Interface**:
- Column M: "Selected Option" dropdown (1, 2, 3, or blank)
- Conditional formatting highlights selections
- Filters for priority, asset type, campaign

#### Step 3.3: User Makes Selections

**User action**:
1. Review each asset and its 3 options
2. Select preferred option in Column M
3. Can select multiple assets across different asset groups
4. Save when complete

---

### Phase 4: Execution Preparation

**Objective**: Download selections and prepare for execution

#### Step 4.1: Download Selections

**Script**: `download_review_selections.py`

```bash
.venv/bin/python3 download_review_selections.py
```

**What it does**:
1. Connects to Google Sheets
2. Reads "Replacement Candidates" sheet
3. Filters rows with selections in Column M
4. Downloads to: `output/tree2mydoor-reviewed-selections.csv`

**Output**: Same format as review sheet, but only selected rows

#### Step 4.2: Convert to Execution Format

**Script**: `convert_to_execution_format.py`

```bash
.venv/bin/python3 convert_to_execution_format.py \
  --input output/tree2mydoor-reviewed-selections.csv \
  --output output/execution-ready.csv
```

**What it does**:
1. Reads reviewed selections
2. Converts "Selected Option" (1/2/3) to specific replacement text
3. Adds "Action" column = "SWAP"
4. Saves to: `output/execution-ready.csv`

**Format transformation**:

**Before (reviewed-selections.csv)**:
```
Campaign_ID,Asset_Group_ID,Original_Text,Option 1,Option 2,Option 3,Selected Option
15820346778,6519856317,"Big Choice","Mediterranean..","Premium..","Authentic..",1
```

**After (execution-ready.csv)**:
```
Campaign_ID,Asset_Group_ID,Original_Text,Asset_Type,Replacement_Text,Action
15820346778,6519856317,"Big Choice",Headline,"Mediterranean Olive Trees",SWAP
```

---

### Phase 5: Execution

**Objective**: Safely swap assets in Google Ads

#### Step 5.1: Dry-Run Test

**Script**: `execute_asset_optimisation.py`

```bash
.venv/bin/python3 execute_asset_optimisation.py \
  --customer-id 4941701449 \
  --campaign-id 15820346778 \
  --csv output/execution-ready.csv \
  --dry-run
```

**What it does**:
1. **Reads execution-ready.csv** with Asset Group IDs
2. **Groups swaps** by (Asset Group ID, Field Type)
3. **Validates safety** for each batch:
   - Checks current asset counts
   - Ensures won't violate minimums (3 headlines, 1 long headline, 2 descriptions)
   - Verifies won't exceed maximums (15 headlines, 5 long/desc)
4. **Simulates execution** without making changes
5. **Logs operations**:
   - Asset group targeted
   - Assets created
   - Assets linked
   - Assets removed
6. **Saves report**: `logs/execution-report-dry-run-{timestamp}.json`

**Dry-run output example**:
```
================================================================================
BATCH 1/3: 1 swap(s)
Asset Group: 6519856317 (Olive Tree Competitors), Type: HEADLINE
================================================================================

📦 BATCH SWAP: 1 HEADLINEs in asset group 6519856317
   🛡️  Validating batch safety...
   ✅ Batch is safe (current: 5, removing: 1, minimum: 3)
   📝 Below limit (5/15), will CREATE→LINK→REMOVE

   📝 Creating 1 new assets...
   [1/1] Creating: Mediterranean Olive Trees...
   ℹ️  Created text asset: "Mediterranean Olive Trees" (ID: 305359271122)

   🔗 Linking 1 new assets to asset group...
   [1/1] Linking: Mediterranean Olive Trees...
   ℹ️  Linked asset 305359271122 to group 6519856317

   🗑️  Removing 1 old assets...
   [1/1] Removing: Big Choice - Affordable Prices...
   ℹ️  Found asset ID 8328637908 for text: "Big Choice - Affordable Prices..."
   ℹ️  Removed asset 8328637908 from group
   ✅ Removed asset 8328637908

   ✅ Batch DRY-RUN: 1 successful, 0 failed
```

#### Step 5.2: Review Dry-Run Results

**User action**:
1. Check `logs/execution-report-dry-run-{timestamp}.json`
2. Verify correct asset groups targeted
3. Confirm asset IDs match expectations
4. Check for any errors or warnings

**Key validations**:
- ✅ All asset groups match selections (check Asset Group ID)
- ✅ All asset texts found
- ✅ No safety violations
- ✅ Counts match expectations (processed = selected)

#### Step 5.3: Live Execution

**Script**: `execute_asset_optimisation.py` (with --live flag)

```bash
.venv/bin/python3 execute_asset_optimisation.py \
  --customer-id 4941701449 \
  --campaign-id 15820346778 \
  --csv output/execution-ready.csv \
  --live
```

**What it does**:
1. **Same process as dry-run** BUT with real API calls
2. **Creates** new text assets via Google Ads API
3. **Links** new assets to asset groups
4. **Removes** old underperforming assets
5. **Saves report**: `logs/execution-report-live-{timestamp}.json`

**Execution strategies**:

**Strategy 1: CREATE→LINK→REMOVE** (when below max limit)
```python
1. Create new asset (returns asset_id)
2. Link new asset to asset group (assetGroupAsset.create)
3. Remove old asset (assetGroupAsset.remove)
```
- Safer: Ensures new asset is live before removing old one
- Used when: current_count < max_limit

**Strategy 2: REMOVE→CREATE→LINK** (when at max limit)
```python
1. Remove old asset first (make room)
2. Create new asset
3. Link new asset to asset group
```
- Necessary when at Google Ads maximum (15 headlines, 5 long/desc)
- Used when: current_count >= max_limit

**Safety checks**:
```python
# Before any swap
current_count = get_current_asset_counts(asset_group_id)
minimum_required = MINIMUM_REQUIREMENTS[field_type]

if current_count - removal_count < minimum_required:
    abort("Would violate minimum requirements")

if current_count >= MAX_LIMITS[field_type]:
    use_remove_first_strategy()
else:
    use_create_first_strategy()
```

#### Step 5.4: Verify Live Execution

**Verification steps**:
1. Check `logs/execution-report-live-{timestamp}.json`
2. Verify all swaps successful
3. Check Google Ads UI:
   - Go to campaign → Asset groups
   - Verify new assets present
   - Verify old assets removed
   - Check asset counts correct

---

## Scripts Reference

### Core Scripts

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `extract_asset_performance.py` | Pull asset data from Google Ads | Customer ID, Campaign ID, Date range | `asset-performance-{id}-{date}.csv` |
| `identify_underperformers.py` | Analyze and flag poor performers | Asset performance CSV | `underperforming-assets.csv` |
| `generate_replacement_text.py` | Generate AI-powered suggestions | Asset performance CSV | `replacement-candidates.csv` |
| `create_review_sheet.py` | Create review interface format | Replacement candidates CSV | `tree2mydoor-review-sheet.csv` |
| `download_review_selections.py` | Download user selections | Google Sheets | `tree2mydoor-reviewed-selections.csv` |
| `convert_to_execution_format.py` | Prepare for execution | Reviewed selections CSV | `execution-ready.csv` |
| `execute_asset_optimisation.py` | Execute asset swaps | Execution-ready CSV | Execution report JSON |

### Supporting Scripts

| Script | Purpose |
|--------|---------|
| `asset_swap_engine.py` | Core Google Ads API wrapper |
| `url_context_extractor.py` | Scrapes landing page content |
| `revert_incorrect_change.py` | One-time script to fix mistakes |

---

## File Outputs

### Data Directory Structure

```
roksys/tools/pmax-asset-optimiser/
├── output/
│   ├── asset-performance-{customer_id}-{date}.csv    # Raw Google Ads data
│   ├── underperforming-assets.csv                    # Flagged assets
│   ├── replacement-candidates.csv                    # AI suggestions
│   ├── tree2mydoor-review-sheet.csv                  # Review format
│   ├── tree2mydoor-reviewed-selections.csv           # User selections
│   └── execution-ready.csv                           # Final execution format
├── logs/
│   ├── execution-report-dry-run-{timestamp}.json     # Dry-run results
│   ├── execution-report-live-{timestamp}.json        # Live execution results
│   ├── investigation-report-{date}.md                # Problem analysis
│   └── resolution-summary-{date}.md                  # Fix summaries
└── backups/
    └── (automatic backups before execution)
```

### Key File Formats

#### `execution-ready.csv` (most important for execution)
```csv
Campaign_ID,Campaign,Asset_Group_ID,Asset_Group,Original_Text,Asset_Type,
Impressions,CTR,Conv_Rate,Flag_Reason,Priority,Option_Number,
Replacement_Text,Char_Count,Char_Limit,Valid,Action

15820346778,"T2MD | P Max | HP&P",6519856317,"Olive Tree Competitors",
"Big Choice - Affordable Prices",Headline,82287,0.38%,0.00%,
"Zero conversions",HIGH,1,"Mediterranean Olive Trees",25,30,True,SWAP
```

**Critical columns**:
- `Asset_Group_ID`: Used by execution engine (fixes wrong-group bug)
- `Campaign_ID`: Campaign context
- `Original_Text`: Asset to remove
- `Replacement_Text`: New asset to create
- `Action`: SWAP/SKIP (only SWAP processed)

#### Execution Report JSON
```json
{
  "timestamp": "2025-11-27_10-17-14",
  "mode": "live",
  "customer_id": "4941701449",
  "csv_path": "output/execution-ready.csv",
  "results": {
    "processed": 3,
    "successful": 3,
    "failed": 0,
    "skipped": 0,
    "errors": []
  },
  "engine_log": [
    {
      "timestamp": "2025-11-27T10:17:09",
      "level": "INFO",
      "message": "Asset group 6519856317 counts: {'HEADLINE': 11, 'LONG_HEADLINE': 5}"
    }
  ]
}
```

---

## Safety Features

### 1. Minimum Asset Requirements

Google Ads requires minimum assets per asset group:
- **3 headlines** minimum
- **1 long headline** minimum
- **2 descriptions** minimum

**Protection**:
```python
MINIMUM_REQUIREMENTS = {
    'HEADLINE': 3,
    'LONG_HEADLINE': 1,
    'DESCRIPTION': 2
}

def validate_swap_safety(asset_group_id, field_type, removal_count):
    current_count = get_current_asset_counts(asset_group_id)[field_type]
    minimum = MINIMUM_REQUIREMENTS[field_type]

    if current_count - removal_count < minimum:
        return False, f"Would violate minimum ({current_count} - {removal_count} < {minimum})"

    return True, "Safe to proceed"
```

### 2. Maximum Asset Limits

Google Ads maximum assets per asset group:
- **15 headlines** maximum
- **5 long headlines** maximum
- **5 descriptions** maximum

**Handling**:
- If at limit: Use REMOVE→CREATE→LINK strategy
- If below limit: Use CREATE→LINK→REMOVE strategy (safer)

### 3. Asset Group ID Verification

**Problem prevented**: Duplicate asset text across multiple asset groups

**Solution**:
- CSV contains `Asset_Group_ID`
- Execution engine uses ID directly
- No text-based searching across groups

**Before fix**:
```python
# WRONG: Searched all groups, could match wrong one
asset_group_id = find_asset_group_by_text(campaign_id, asset_text)
```

**After fix**:
```python
# CORRECT: Uses exact ID from CSV
asset_group_id = instruction['asset_group_id']  # From CSV
```

### 4. Dry-Run Mode

**Always run dry-run first**:
- Simulates all operations
- Shows exactly what will happen
- No actual changes made
- Validates safety checks
- Logs all operations

### 5. Execution Reports

Every execution creates detailed JSON reports:
- Timestamp
- Mode (dry-run vs live)
- Customer ID
- CSV path
- Success/failure counts
- Full operation log

Stored in: `logs/execution-report-{mode}-{timestamp}.json`

### 6. Deduplication

**Within asset groups**:
- Tracks all generated texts in batch
- Passes avoid list to AI
- Ensures unique suggestions

**Why important**:
- Prevents repetitive suggestions
- Maintains ad variety
- Improves user experience

---

## Troubleshooting

### Common Issues

#### Issue 1: "Asset not found in campaign"

**Symptom**: Dry-run shows asset not found

**Causes**:
1. Asset already removed
2. Asset text doesn't match exactly (whitespace, special chars)
3. Asset in different campaign

**Solution**:
```bash
# Check asset exists
.venv/bin/python3 -c "
from asset_swap_engine import AssetSwapEngine
engine = AssetSwapEngine('CUSTOMER_ID', dry_run=True)
engine.initialise_client()

# Query asset group
query = '''
    SELECT asset.id, asset.text_asset.text
    FROM asset_group_asset
    WHERE asset_group.id = ASSET_GROUP_ID
      AND asset_group_asset.field_type = 'HEADLINE'
'''
# Check if asset exists
"
```

#### Issue 2: "Would violate minimum requirements"

**Symptom**: Safety check fails

**Cause**: Not enough assets in group to safely remove

**Solution**:
- Check current asset counts in Google Ads UI
- Only remove assets if counts are above minimums
- Consider swapping fewer assets at once

#### Issue 3: Duplicate suggestions within asset group

**Symptom**: Multiple assets get same replacement text

**Cause**: Deduplication not working

**Solution**:
- Verify `generate_replacement_text.py` has deduplication code (lines 595-619)
- Check `avoid_texts` parameter passed to API
- Regenerate suggestions

#### Issue 4: Wrong asset group modified

**Symptom**: Changes appear in unexpected asset group

**Cause**: Execution engine using text search instead of Asset Group ID

**Solution**:
- Verify `execute_asset_optimisation.py` reads `Asset_Group_ID` from CSV (line 84)
- Check CSV has `Asset_Group_ID` column
- Run dry-run to verify targeting

#### Issue 5: Google Ads API errors

**Common errors**:
- `INVALID_ARGUMENT`: Query syntax error
- `PERMISSION_DENIED`: Missing API access
- `RESOURCE_EXHAUSTED`: Rate limit exceeded
- `UNAUTHENTICATED`: OAuth token expired

**Solutions**:
```bash
# Check credentials
cat google-ads.yaml

# Test API connection
.venv/bin/python3 -c "
from google.ads.googleads.client import GoogleAdsClient
client = GoogleAdsClient.load_from_storage('google-ads.yaml')
print('API connection successful')
"

# Refresh OAuth token (if expired)
# Re-run OAuth flow to get new refresh_token
```

---

## Future Automation

### Recommended Sub-Agents

#### 1. Asset Performance Analyzer Agent

**Purpose**: Automated data extraction and analysis

**Triggers**:
- Weekly schedule (every Monday morning)
- Manual trigger: `/analyze-assets tree2mydoor`
- Event-based: After significant spend or campaign changes

**Actions**:
1. Extract asset performance data
2. Identify underperformers
3. Generate summary report
4. Create task if action needed

**Skills needed**:
- Google Ads API access
- Statistical analysis
- Report generation

#### 2. Replacement Generator Agent

**Purpose**: AI-powered suggestion generation

**Triggers**:
- After Asset Performance Analyzer identifies issues
- Manual trigger: `/generate-replacements tree2mydoor`
- Scheduled: Bi-weekly review

**Actions**:
1. Load underperforming assets
2. Extract URL context
3. Generate deduplicated suggestions
4. Create review sheet
5. Upload to Google Sheets

**Skills needed**:
- Claude API access
- Web scraping
- Google Sheets API

#### 3. Review Sheet Manager Agent

**Purpose**: Manage selection workflow

**Triggers**:
- After suggestions generated
- Manual trigger: `/check-selections tree2mydoor`
- Scheduled: Daily check for new selections

**Actions**:
1. Create/update Google Sheets
2. Monitor for selections
3. Download when ready
4. Convert to execution format
5. Notify user for approval

**Skills needed**:
- Google Sheets API
- State tracking
- Notifications

#### 4. Execution Engine Agent

**Purpose**: Safe asset swap execution

**Triggers**:
- Manual trigger: `/execute-swaps tree2mydoor --dry-run`
- After user approval
- Never automatic (requires approval)

**Actions**:
1. Run dry-run
2. Generate preview report
3. Request user approval
4. Execute live (if approved)
5. Generate execution report
6. Verify changes

**Skills needed**:
- Google Ads API
- Safety validation
- Approval workflow
- Verification

### Agent Interaction Flow

```
┌──────────────────────────┐
│  Asset Performance       │  Weekly/Manual
│  Analyzer Agent          │  ──────────────►  Identifies underperformers
└──────────────────────────┘
            │
            │ If issues found
            ▼
┌──────────────────────────┐
│  Replacement Generator   │  Generates AI suggestions
│  Agent                   │  ──────────────►  Creates review sheet
└──────────────────────────┘
            │
            │ Auto-upload
            ▼
┌──────────────────────────┐
│  Google Sheets           │  User makes selections
│  (Review Interface)      │  ──────────────►  Manual step
└──────────────────────────┘
            │
            │ Selections detected
            ▼
┌──────────────────────────┐
│  Review Sheet Manager    │  Downloads selections
│  Agent                   │  ──────────────►  Converts format
└──────────────────────────┘
            │
            │ Ready for execution
            ▼
┌──────────────────────────┐
│  Execution Engine        │  Dry-run → Approval → Live
│  Agent                   │  ──────────────►  Executes swaps
└──────────────────────────┘
            │
            │ Execution complete
            ▼
┌──────────────────────────┐
│  Verification &          │  Confirms success
│  Reporting               │  ──────────────►  Notifies user
└──────────────────────────┘
```

### Agent Implementation

**Location**: `/Users/administrator/Documents/PetesBrain/roksys/agents/`

**Structure**:
```
roksys/agents/
├── asset-performance-analyzer/
│   ├── agent.py
│   ├── config.yaml
│   └── README.md
├── replacement-generator/
│   ├── agent.py
│   ├── config.yaml
│   └── README.md
├── review-sheet-manager/
│   ├── agent.py
│   ├── config.yaml
│   └── README.md
└── execution-engine/
    ├── agent.py
    ├── config.yaml
    └── README.md
```

**Agent config template**:
```yaml
name: asset-performance-analyzer
description: Automated asset performance analysis
triggers:
  - schedule: "0 9 * * 1"  # Every Monday 9am
  - manual: "/analyze-assets {client}"
  - event: "campaign_spend_threshold"

actions:
  - extract_data
  - analyze_performance
  - generate_report
  - create_task_if_needed

dependencies:
  - google-ads-api
  - statistical-analysis
  - report-generator

outputs:
  - "Asset performance report"
  - "Task if action required"
  - "Notification to user"
```

---

## Best Practices

### 1. Always Run Dry-Run First

Never skip dry-run mode. It catches:
- Wrong asset group targeting
- Missing assets
- Safety violations
- Unexpected counts

### 2. Verify Asset Group IDs

Before execution:
```bash
# Check CSV has correct IDs
head -2 output/execution-ready.csv

# Verify against Google Ads UI
# Campaign → Asset groups → Check IDs match
```

### 3. Small Batches First

For first execution:
- Select 2-3 assets only
- Test across different asset types
- Verify results before scaling

### 4. Monitor Deduplication

After generation:
```bash
# Check for duplicates within asset groups
.venv/bin/python3 -c "
import pandas as pd
df = pd.read_csv('output/replacement-candidates.csv')
dupes = df.groupby(['Asset_Group', 'Replacement_Text']).size()
dupes = dupes[dupes > 1]
if len(dupes) > 0:
    print('DUPLICATES FOUND:')
    print(dupes)
else:
    print('No duplicates - deduplication working!')
"
```

### 5. Keep Execution Reports

All execution reports are saved:
- `logs/execution-report-dry-run-*.json`
- `logs/execution-report-live-*.json`

Never delete these - they're your audit trail.

### 6. Document Issues

When things go wrong:
- Create investigation report in `logs/`
- Document root cause
- Document fix applied
- Update this workflow document

---

## Quick Reference Commands

### Complete Pipeline (Manual)

```bash
# 1. Extract data
.venv/bin/python3 extract_asset_performance.py \
  --customer-id 4941701449 \
  --campaign-id 15820346778 \
  --start-date 2025-08-28 \
  --end-date 2025-11-26

# 2. Identify underperformers
.venv/bin/python3 identify_underperformers.py \
  --customer-id 4941701449 \
  --csv output/asset-performance-4941701449-2025-11-26.csv

# 3. Generate suggestions
.venv/bin/python3 generate_replacement_text.py \
  --customer-id 4941701449 \
  --csv output/asset-performance-4941701449-2025-11-26.csv

# 4. Create review sheet
.venv/bin/python3 create_review_sheet.py \
  --customer-id 4941701449

# 5. Upload to Google Sheets (manual)
# - Open sheet, import CSV

# 6. User makes selections (manual)

# 7. Download selections
.venv/bin/python3 download_review_selections.py

# 8. Convert to execution format
.venv/bin/python3 convert_to_execution_format.py \
  --input output/tree2mydoor-reviewed-selections.csv \
  --output output/execution-ready.csv

# 9. Dry-run
.venv/bin/python3 execute_asset_optimisation.py \
  --customer-id 4941701449 \
  --campaign-id 15820346778 \
  --csv output/execution-ready.csv \
  --dry-run

# 10. Review dry-run results

# 11. Live execution (ONLY after approval)
.venv/bin/python3 execute_asset_optimisation.py \
  --customer-id 4941701449 \
  --campaign-id 15820346778 \
  --csv output/execution-ready.csv \
  --live
```

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-27 | 1.0 | Initial documentation after production fixes |

**Author**: PetesBrain AI Assistant
**Status**: Production-ready
**Last Updated**: 2025-11-27

---

## ⚠️ CRITICAL LESSON: Devonshire Hotels Mistake (2025-11-27)

### What Went Wrong

**User Request**: "Run this for Devonshire Hotels"

**What I Delivered**:
1. ✅ Pulled API data (80 assets)
2. ✅ Identified 7 underperformers in markdown analysis
3. ❌ **SKIPPED generating 3 replacement options per underperformer**
4. ❌ Created Google Sheet with just raw asset data (no suggestions)

**What User Expected** (based on Tree2mydoor workflow):
1. ✅ Pull API data
2. ✅ Identify underperformers
3. ✅ **Generate 3 replacement options for EACH underperformer**
4. ✅ Google Sheet with: Original asset + Option 1 + Option 2 + Option 3

### The Correct Output Format

**Each underperforming asset must appear as 3 rows:**

```csv
Campaign_ID,Asset_Group_ID,Original_Text,Asset_Type,Priority,Option_Number,Replacement_Text
5898250490,6456703966,"Luxury Yorkshire Dales Retreat",Headline,HIGH,1,"Premium Yorkshire Retreat"
5898250490,6456703966,"Luxury Yorkshire Dales Retreat",Headline,HIGH,2,"Yorkshire Dales Spa Hotel"
5898250490,6456703966,"Luxury Yorkshire Dales Retreat",Headline,HIGH,3,"Bolton Abbey Luxury Stay"
```

**NOT just:**
```csv
Campaign,Asset_Group,Asset,Asset_Type,Impr.,Clicks,CTR
DEV | Core...,The Devonshire Arms Hotel,"Luxury Yorkshire Dales Retreat",Headline,3662,246,6.72%
```

### Why This Matters

**User Quote**: "I don't just want a list of the assets. Where are the recommendations for her to choose from? The options one, two, three that we've already decided on."

**Client needs:**
- Helen (Devonshire Hotels) needs ACTIONABLE suggestions
- She wants to CHOOSE between alternatives
- Raw data + analysis ≠ executable changes
- The VALUE is in the AI-generated replacement options

### Root Cause

1. **No explicit Step 3 in my mental model** - I went:
   - Step 1: Pull data ✅
   - Step 2: Identify issues ✅
   - Step 3: Create sheet ❌ (should have been "Generate replacements")
   - Step 4: Create sheet ❌ (with replacements)

2. **Focused on "new" request** (campaign name + asset groups) instead of following established workflow

3. **Didn't check previous Tree2mydoor output format** before creating Devonshire version

### Prevention Going Forward

**MANDATORY WORKFLOW FOR ALL CLIENTS:**

```bash
# Step 1: Pull API Data
python3 fetch_pmax_assets.py --customer-id X --campaign-id Y

# Step 2: Generate Replacements (CANNOT SKIP!)
python3 generate_replacement_text.py --csv output/{client}-asset-performance.csv

# Step 3: Create Google Sheet
# Use replacement-candidates.csv (with 3 options per asset)
# NOT the raw asset performance CSV
```

**Before delivering ANY PMAX work:**
1. ✅ Check output has Option_Number column (1, 2, 3)
2. ✅ Verify 3 rows per underperformer
3. ✅ Confirm Replacement_Text column present
4. ✅ Review sample to ensure suggestions are unique and relevant

### Updated Script Requirement

**The primary script must ALWAYS generate 3 options:**

```python
# generate_replacement_text.py MUST:
# 1. Identify underperformers
# 2. For EACH underperformer:
#    - Generate Option 1 (alternative approach)
#    - Generate Option 2 (different angle)
#    - Generate Option 3 (third variation)
# 3. Output with Option_Number column
# 4. Validate uniqueness within asset groups
```

**The output is NOT complete without 3 options per asset.**

---

**Documented by**: Claude Code
**Date**: 2025-11-27 14:45 GMT
**Trigger**: User correction after incomplete Devonshire delivery
