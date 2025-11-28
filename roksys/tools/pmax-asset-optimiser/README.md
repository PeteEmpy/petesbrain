# PMAX Asset Optimiser

A complete workflow for analysing, generating, and swapping underperforming Performance Max text assets in Google Ads.

## Overview

This tool automates the process of optimising PMAX text assets by:
1. Analysing asset performance from Google Ads CSV reports
2. Identifying underperformers using statistical thresholds
3. Generating AI-powered replacement text that preserves brand voice
4. Safely swapping assets via Google Ads API with comprehensive safety checks

**Tested on:** Tree2mydoor (Nov 2025) - 100% success rate on 2 live swaps
**Status:** Production-ready for e-commerce clients

---

## Quick Start

### Prerequisites

- Python 3.9+
- Google Ads API access (~/google-ads.yaml configured)
- Anthropic API key (for AI text generation)

### Installation

```bash
cd /Users/administrator/Documents/PetesBrain/roksys/tools/pmax-asset-optimiser
pip3 install beautifulsoup4 requests anthropic pyyaml
```

### Basic Workflow

```bash
# 1. Export Asset performance report from Google Ads (last 30 days)
# Save as: output/{client}-asset-performance-YYYY-MM-DD.csv

# 2. Analyse performance
/usr/bin/python3 analyse_asset_performance.py

# 3. Generate AI-powered replacements
/usr/bin/python3 generate_replacement_text.py

# 4. Review output/replacement-candidates.csv
# - Open in Google Sheets
# - Review Replacement_Text column
# - Set Action to SWAP or SKIP for each row

# 5. Test with dry-run
/usr/bin/python3 execute_asset_optimisation.py \
  --customer-id {customer_id} \
  --campaign-id {campaign_id} \
  --csv output/replacement-candidates.csv \
  --dry-run

# 6. Execute live swaps
/usr/bin/python3 execute_asset_optimisation.py \
  --customer-id {customer_id} \
  --campaign-id {campaign_id} \
  --csv output/replacement-candidates.csv \
  --live
```

---

## Workflow Steps (Detailed)

### Step 1: Export Asset Performance Report

1. Go to Google Ads → Reports → Predefined Reports
2. Select **Asset performance** report
3. Configure date range (last 30 days recommended)
4. Include columns:
   - Asset
   - Asset type
   - Campaign
   - Performance label
   - Impressions
   - Clicks
   - CTR
   - Conversions
   - Conv. rate
   - Cost / conv.
5. Export as CSV
6. Save to `output/{client}-asset-performance-{date}.csv`

**Important:** The CSV will have 2 header rows. The scripts handle this automatically.

---

### Step 2: Analyse Performance

```bash
/usr/bin/python3 analyse_asset_performance.py
```

**What it does:**
- Loads the most recent CSV in `output/` directory
- Filters to PMAX text assets only (Headlines, Descriptions, Long headlines)
- Excludes Google AI-generated assets
- Calculates campaign averages (CTR, conv rate, cost/conv)
- Flags underperformers based on thresholds (see Configuration)
- Assigns priority (HIGH/MEDIUM/LOW)

**Output:** `output/underperforming-assets.csv`

**Example results (Tree2mydoor):**
- Total assets: 1,074
- PMAX text assets: 180
- **Underperformers: 59** (40 HIGH, 19 MEDIUM)

---

### Step 3: Generate Replacement Text

```bash
/usr/bin/python3 generate_replacement_text.py
```

**What it does:**
- Analyses client website to extract brand voice (tone, key messages)
- Identifies winning patterns from top-performing assets
- Uses Claude Sonnet 4 AI to generate 3 alternatives per underperformer
- Enforces Google Ads character limits (Headlines: 30, Long headlines: 90, Descriptions: 90)
- Triple validation (AI prompt, post-generation check, smart truncation)

**Output:** `output/replacement-candidates.csv`

**Character Limits (CRITICAL):**
| Asset Type | Max Characters |
|------------|----------------|
| Headline | 30 |
| Long headline | 90 |
| Description | 90 |

**Google Ads API will REJECT assets exceeding these limits.**

---

### Step 4: Review & Edit Replacements

Open `output/replacement-candidates.csv` in Google Sheets:

**Columns:**
- `Original_Text` - Current underperforming asset
- `Asset_Type` - Headline, Long headline, or Description
- `Impressions` - How many times shown
- `CTR` - Click-through rate
- `Conv_Rate` - Conversion rate
- `Flag_Reason` - Why it was flagged
- `Priority` - HIGH/MEDIUM/LOW
- `Option_Number` - 1, 2, or 3 (three alternatives per asset)
- `Replacement_Text` - AI-generated alternative
- `Char_Count` - Character count
- `Char_Limit` - Maximum allowed
- `Valid` - TRUE if within limit
- **`Action`** - **REVIEW** (change to SWAP or SKIP)

**Review checklist:**
1. Verify `Replacement_Text` maintains brand voice
2. Check `Char_Count ≤ Char_Limit` (should be TRUE)
3. Choose one option per underperforming asset
4. Set `Action` to:
   - **SWAP** - Execute this replacement
   - **SKIP** - Don't change this asset
5. Only ONE row per original asset should have `Action=SWAP`

**Editing guidelines:**
- If you edit `Replacement_Text`, update `Char_Count` manually
- NEVER exceed `Char_Limit`
- Preserve brand-specific terms ("Tree2mydoor", "MyTree™ warranty", etc.)
- Test headlines read well with "Tree2mydoor | " prefix

---

### Step 5: Test with Dry-Run

```bash
/usr/bin/python3 execute_asset_optimisation.py \
  --customer-id 4941701449 \
  --campaign-id 15820346778 \
  --csv output/replacement-candidates.csv \
  --dry-run
```

**What it does:**
- Loads CSV and filters to `Action=SWAP` rows
- Finds asset groups containing each asset
- Finds old asset IDs by text matching
- Validates safety (ensures minimum requirements maintained)
- **Simulates** swap without making changes
- Generates execution report in `logs/`

**Safety checks:**
- Headlines: Minimum 3 must remain ENABLED
- Long headlines: Minimum 1 must remain ENABLED
- Descriptions: Minimum 2 must remain ENABLED

**If dry-run succeeds, you're safe to execute live.**

---

### Step 6: Execute Live Swaps

```bash
/usr/bin/python3 execute_asset_optimisation.py \
  --customer-id 4941701449 \
  --campaign-id 15820346778 \
  --csv output/replacement-candidates.csv \
  --live
```

**What it does:**
1. **Pause** old asset (changes status to PAUSED)
2. **Create** new text asset with replacement text
3. **Link** new asset to the same asset group
4. **Log** all operations

**Execution flow per asset:**
```
Original asset: "Buy Olive Trees Online"
  ↓
Find asset group ID (via GAQL query)
  ↓
Find old asset ID (match text exactly)
  ↓
Validate safety (check minimums won't be violated)
  ↓
Pause old asset (status → PAUSED)
  ↓
Create new asset ("Olive Trees With Lifetime Care")
  ↓
Link new asset to group (status → ENABLED)
  ↓
✅ Swap complete!
```

**Execution report:** Saved to `logs/execution-report-live-{timestamp}.json`

---

## Configuration

Edit `config.yaml` to adjust thresholds:

```yaml
thresholds:
  ctr_multiplier: 0.7              # Flag if CTR < avg * 0.7
  conv_rate_multiplier: 0.7        # Flag if conv rate < avg * 0.7
  cost_per_conv_multiplier: 1.3   # Flag if cost/conv > avg * 1.3
  min_impressions_for_judgement: 100
  zero_conv_high_impr_threshold: 200

clients:
  tree2mydoor:
    customer_id: "4941701449"
    campaign_id: "15820346778"
    brand_voice: "tree2mydoor"
```

---

## Tree2mydoor Example Walkthrough

### Context
- **Campaign:** T2MD | P Max | HP&P (ID: 15820346778)
- **Date range:** 29 Oct - 25 Nov 2025
- **Total PMAX text assets:** 180
- **Underperformers identified:** 59 (40 HIGH, 19 MEDIUM)

### Analysis Results

**Campaign averages:**
- CTR: 0.63%
- Conv Rate: 2.83%
- Cost/Conv: £19.72

**Worst offenders:**
1. "All our gifts are packed with love & care..." - 51,148 impr, 0 conv, £10.19 wasted
2. Generic "living gifts" without product specificity - 190,000+ impr, 0 conv
3. Anniversary rose rhetoric - 150,000+ impr, £220+ wasted

**Winning patterns identified:**
1. "Tree2mydoor Tree & Plant Gifts" - 16.78 conv
2. "An Ethical Gift That Will Last" - 14.64 conv
3. Product-specific + "packed with love & care" = 8.50-10.76% conv rate

**Key insight:** The SAME text performs differently by asset type!
- "Living gifts that last..." as **Description**: 16.95 conv (WINNER)
- "Living gifts that last..." as **Long headline**: 0 conv (LOSER)

### Text Generation Results

**177 alternatives generated (3 per asset)**
- 100% character limit compliance
- Brand voice preserved (warm, friendly, trustworthy, ethical)
- Product specificity added where missing

**Example replacements:**
| Original (0 conv) | Replacement | Type |
|-------------------|-------------|------|
| Buy Olive Trees Online | Olive Trees With Lifetime Care | Headline |
| UK Grown Bay Trees | Premium UK Bay Tree Gifts | Headline |

### Execution Results

**Test swaps: 2 assets**
- Dry-run: ✅ 2/2 passed safety checks
- Live execution: ✅ 2/2 swapped successfully
- Verification: ✅ Both visible in Google Ads with correct status

**Next steps:**
1. Monitor performance over 2 weeks
2. Compare new asset metrics to old baseline
3. Execute remaining 57 swaps if successful

---

## Smythson Adaptation Guide

### Use Case: Black Friday → Christmas Copy Swap (Dec 2nd)

The tool was built to be reusable. For Smythson's Dec 2nd Black Friday revert:

**Differences from Tree2mydoor:**
- Skip analysis (replacement text pre-written)
- Skip generation (Christmas copy already created)
- Direct to execution
- Process 52 asset groups across 4 accounts (UK, US, EUR, ROW)

**Workflow:**
1. Load Smythson replacement CSVs (already prepared)
2. Run execution script per account:
   ```bash
   # UK
   /usr/bin/python3 execute_asset_optimisation.py \
     --customer-id 5755827834 \
     --campaign-id {uk_campaign_id} \
     --csv uk-replacement-copy.csv \
     --live

   # Repeat for US, EUR, ROW
   ```

**Reuses:**
- `asset_swap_engine.py` (same swap logic)
- Same safety checks
- Same logging format
- Rollback available via `rollback-to-backup.py`

---

## Troubleshooting

### Issue: "CSV file not found"

**Cause:** Wrong file path
**Fix:** Ensure CSV is in `output/` directory or specify full path with `--csv`

### Issue: "Asset not found in campaign"

**Cause:** Asset text doesn't match exactly (whitespace, punctuation)
**Fix:**
1. Check CSV for exact text (including ellipsis "...")
2. Query Google Ads to verify asset exists:
   ```sql
   SELECT asset.text_asset.text
   FROM asset_group_asset
   WHERE campaign.id = {campaign_id}
   ```

### Issue: "Safety check failed: Cannot remove X assets"

**Cause:** Removing the asset would violate Google's minimum requirements
**Fix:** This is a safety feature. Don't override. The asset group needs more assets before you can remove this one.

### Issue: "Character limit exceeded"

**Cause:** Replacement text too long
**Fix:** Edit the `Replacement_Text` in CSV to fit within `Char_Limit`

### Issue: Invalid enum 'AssetGroupAssetStatusEnum'

**Cause:** Google Ads API version mismatch
**Fix:** Already fixed in code (uses `AssetLinkStatusEnum.PAUSED`)

---

## File Structure

```
/pmax-asset-optimiser/
├── README.md                       # This file
├── config.yaml                     # Configuration & thresholds
├── asset_swap_engine.py            # Core swap logic (reusable)
├── analyse_asset_performance.py    # Performance analysis
├── generate_replacement_text.py    # AI text generation
├── execute_asset_optimisation.py   # Execution orchestrator
├── download_and_prepare.py         # Download from Google Sheets & prepare CSV
├── query_google_ads_changes.py     # Universal change history query script
├── query_change_history.py         # Legacy change history script (direct API)
├── show_changes_today.sh           # Quick wrapper for today's changes
├── output/
│   ├── {client}-asset-performance-{date}.csv  # Source data
│   ├── underperforming-assets.csv             # Analysis results
│   ├── replacement-candidates.csv             # AI-generated alternatives
│   └── execution-ready.csv                    # User selections prepared for execution
├── logs/
│   ├── execution-report-{mode}-{timestamp}.json  # Execution audit trail
│   └── generate-test-full.log                    # Generation logs
├── CHANGE-HISTORY-2025-11-27.md    # Example: Complete audit documentation
├── backups/                        # (future: pre-swap backups)
└── templates/                      # (future: fallback templates)
```

---

## API Credentials

### Google Ads API

**Location:** `~/google-ads.yaml`

**Required fields:**
```yaml
developer_token: YOUR_DEV_TOKEN
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
login_customer_id: YOUR_MANAGER_ID
```

### Anthropic API

**Location:** `/Users/administrator/Documents/PetesBrain/tools/google-ads-generator/.env`

**Required:**
```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Safety Features

1. **Dry-run mode default** - Always test before executing
2. **Minimum requirements enforced** - Cannot drop below Google's minimums
3. **Safety validation** - Checks before every swap
4. **Sequential swapping** - One-by-one with validation between each
5. **Comprehensive logging** - Every operation logged with timestamp
6. **Execution reports** - JSON audit trail of all operations
7. **Character limit validation** - Triple-checked before API submission

**Google Ads Minimum Requirements:**
- Headlines: 3 ENABLED minimum
- Long headlines: 1 ENABLED minimum
- Descriptions: 2 ENABLED minimum

**The engine will NEVER allow a swap that would violate these minimums.**

---

## Performance Monitoring

After executing swaps, monitor new assets for 14 days:

**Metrics to track:**
- Impressions
- Clicks
- CTR
- Conversions
- Conv. rate
- Cost/conv
- Performance label (Google's automated rating)

**How to check:**
1. Export new Asset performance report (14 days after swap)
2. Filter to new asset IDs (saved in execution report)
3. Compare to old baseline metrics
4. If improved: Continue with remaining swaps
5. If declined: Rollback (re-enable old, pause new)

---

## Known Limitations

1. **Manual CSV review required** - Cannot fully automate without human approval
2. **Text matching only** - Finds assets by exact text match (no fuzzy matching)
3. **Single campaign at a time** - Must run separately per campaign
4. **No automatic rollback** - Must manually re-enable old assets if needed
5. **Website analysis may be slow** - Takes 30-60 seconds to scrape client site

---

## Future Enhancements

**Potential additions:**
- [ ] Automated A/B test setup (50/50 traffic split)
- [ ] Performance monitoring dashboard
- [ ] Automatic rollback if new assets underperform
- [ ] Bulk campaign processing
- [ ] Pre-swap backups to `backups/` directory
- [ ] Slack/email notifications on completion
- [ ] Integration with Tree2mydoor's existing workflow

---

## Credits

**Author:** PetesBrain
**Created:** 2025-11-25
**Tested:** Tree2mydoor (2 live swaps, 100% success)
**Status:** Production-ready

**Dependencies:**
- Google Ads API v20
- Anthropic Claude Sonnet 4
- BeautifulSoup4 (website scraping)
- PyYAML (config)

---

## Querying Change History

After executing swaps, you can verify changes in Google Ads using the universal change history query script:

```bash
# All changes today for a customer
python3 query_google_ads_changes.py --customer-id 4941701449

# Asset changes in specific asset group
python3 query_google_ads_changes.py --customer-id 4941701449 --asset-group-id 6519856317

# All changes in the last 7 days
python3 query_google_ads_changes.py --customer-id 4941701449 --days 7

# Only asset creations
python3 query_google_ads_changes.py --customer-id 4941701449 --operation CREATE --resource-type asset

# Changes in specific campaign
python3 query_google_ads_changes.py --customer-id 4941701449 --campaign-id 15820346778
```

**What it shows:**
- Timestamp of each change
- Operation type (CREATE, UPDATE, REMOVE)
- User email who made the change
- Resource names and IDs
- Asset text content (for asset changes)
- Asset group links

**Output includes:**
- Changes grouped by resource type (assets, campaigns, adGroups, etc.)
- Asset details with text content
- Asset group associations
- Summary statistics

**Example output:**
```
================================================================================
ASSETS CHANGES (3)
================================================================================

[1/3] 2025-11-27 10:05:45 - CREATE
  User: petere@roksys.co.uk
  Resource ID: 312332933791
  Type: TEXT
  Text: "Premium Olive Trees - Perfect For Patios - Gift Wrapped With Next Day Delivery"
  Linked to 1 asset group(s):
    - Asset Group 6519856317 (Olive Tree Competitors)
      Field Type: LONG_HEADLINE
```

**See also:** `CHANGE-HISTORY-2025-11-27.md` for an example of complete audit documentation

---

## Support

**Issues:** Report to `peter@roksys.co.uk`
**Documentation:** This README + inline code comments
**Logs:** Check `logs/` directory for execution reports
**Change History:** Use `query_google_ads_changes.py` to audit Google Ads changes

---

**⚠️ IMPORTANT REMINDERS**

1. **Always dry-run first** - Never skip testing
2. **Character limits are CRITICAL** - Google Ads API will reject violations
3. **Brand voice must be preserved** - Review all AI-generated text
4. **Monitor performance** - Track new assets for 14 days minimum
5. **One option per asset** - Only mark ONE replacement as SWAP per original

**✅ If you follow this workflow, you'll safely optimise PMAX assets with minimal risk.**
