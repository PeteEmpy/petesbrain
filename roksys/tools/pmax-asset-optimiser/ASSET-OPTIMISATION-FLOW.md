# PMAX Asset Text Optimisation Flow

## Overview

The Asset Text Optimisation Flow is a complete workflow for identifying underperforming Performance Max text assets and replacing them with AI-generated alternatives. This is the full end-to-end optimisation process.

## When to Use This

**Use this workflow when:**
- You want to improve PMAX campaign performance through better ad copy
- You have sufficient data (30+ days, thousands of impressions)
- You want AI-generated replacement suggestions
- You need data-driven asset decisions

**Don't use this for:**
- Full asset refreshes (use spreadsheet-based swap instead)
- Brand messaging changes (manual approach better)
- New campaigns with insufficient data

## Complete Workflow

```
1. Analyse Performance
   ↓
2. Generate AI Replacements
   ↓
3. Review & Edit CSV
   ↓
4. Execute Swaps (Dry-Run)
   ↓
5. Execute Swaps (Live)
```

## Step 1: Analyse Asset Performance

**Script:** `analyse_asset_performance.py`

**Purpose:** Identifies underperforming assets based on performance thresholds

**Usage:**
```bash
python3 analyse_asset_performance.py \
  --customer-id 4941701449 \
  --campaign-ids 23294632479,23294632480 \
  --start-date 2025-10-01 \
  --end-date 2025-11-25
```

**What it does:**
1. Fetches asset performance data from Google Ads
2. Applies thresholds from `config.yaml`:
   - Minimum impressions (default: 1000)
   - Maximum CTR (default: 2.5%)
   - Maximum conversion rate (default: 8%)
3. Flags underperformers with reasons
4. Exports to `output/underperforming-assets-YYYYMMDD-HHMMSS.csv`

**Configuration (config.yaml):**
```yaml
thresholds:
  min_impressions: 1000
  max_ctr: 2.5
  max_conversion_rate: 8.0

priorities:
  low_impressions_low_performance: HIGH
  high_impressions_low_performance: HIGH
  moderate_impressions_low_ctr: MEDIUM
  low_volume: LOW
```

**Output CSV columns:**
- Campaign, Asset Group, Asset Text, Asset Type
- Impressions, Clicks, CTR, Conversions, Conv Rate
- Flag Reason, Priority

**Example output:**
```csv
Campaign,Asset_Group,Asset_Text,Asset_Type,Impressions,CTR,Conv_Rate,Flag_Reason,Priority
"T2MD | PMAX | Main","Brand","Free Delivery",Headline,15234,1.8%,3.2%,Low CTR + Low Conv,HIGH
```

## Step 2: Generate AI Replacement Text

**Script:** `generate_replacement_text.py`

**Purpose:** Uses Claude AI to generate optimised replacement copy based on client context

**Usage:**
```bash
python3 generate_replacement_text.py \
  --customer-id 4941701449 \
  --input output/underperforming-assets-20251125-103045.csv \
  --client-context /Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md
```

**What it does:**
1. Reads underperforming assets CSV
2. Loads client context (brand voice, USPs, messaging)
3. For each flagged asset:
   - Analyses why it's underperforming
   - Generates 3 alternative options using Claude AI
   - Validates character limits
   - Prioritises by performance impact
4. Exports to `output/replacement-suggestions-YYYYMMDD-HHMMSS.csv`

**AI Prompt includes:**
- Client brand guidelines
- Product category context
- Current messaging analysis
- Performance data (why it's flagged)
- Character limit constraints

**Output CSV columns:**
- All columns from input CSV
- Option_Number (1, 2, or 3)
- Replacement_Text
- Char_Count, Char_Limit, Valid
- Action (set to REVIEW by default)

**Example output:**
```csv
Original_Text,Asset_Type,Impressions,CTR,Priority,Option_Number,Replacement_Text,Char_Count,Valid,Action
"Free Delivery",Headline,15234,1.8%,HIGH,1,"Rose Bushes + Lifetime Care",27,True,REVIEW
"Free Delivery",Headline,15234,1.8%,HIGH,2,"Gifts That Keep On Growing",27,True,REVIEW
"Free Delivery",Headline,15234,1.8%,HIGH,3,"Birthday Roses With Care",24,True,REVIEW
```

**Character Limit Validation:**
- Headlines: ≤30 characters
- Long Headlines: ≤90 characters
- Descriptions: ≤90 characters
- Invalid options marked `Valid=False` (won't be used)

## Step 3: Review & Select Replacements

**Manual step - review the CSV in Google Sheets or Excel**

**Actions:**
1. Review each `Replacement_Text` option
2. Edit if needed (keep within character limits)
3. Select which option to use (delete unwanted rows)
4. Change `Action` from `REVIEW` to `SWAP` for approved replacements
5. Save as CSV

**Tips:**
- You'll see 3 options per underperformer - pick the best one
- Delete rows for options you don't want
- Edit text if needed, but check `Char_Count` stays within limit
- Only set `Action=SWAP` for assets you're confident about
- Consider A/B testing by swapping only half of underperformers

**HTML Visualization:**

The system can generate an HTML view for easier review:

```bash
# (To be implemented - generates output/replacement-suggestions-YYYYMMDD.html)
```

## Step 4: Execute Swaps (Dry-Run)

**Script:** `execute_asset_optimisation.py`

**Purpose:** Validate swaps without making changes

**Usage:**
```bash
python3 execute_asset_optimisation.py \
  --customer-id 4941701449 \
  --campaign-id 23294632479 \
  --csv output/replacement-suggestions-20251125-reviewed.csv \
  --dry-run
```

**What it validates:**
- All `Original_Text` assets can be found in Google Ads
- Asset groups are correctly identified
- Character limits are met
- No minimum requirements will be violated
- Batching strategy is appropriate

**Output:**
- Console: Shows what would be swapped
- Log file: `logs/execution-report-dry-run-YYYYMMDD-HHMMSS.json`

**Check for:**
- "Asset not found" warnings (text doesn't match exactly)
- Any validation errors
- Batch vs one-by-one execution strategy

## Step 5: Execute Swaps (Live)

**Script:** `execute_asset_optimisation.py`

**Purpose:** Execute the approved swaps in Google Ads

**Usage:**
```bash
python3 execute_asset_optimisation.py \
  --customer-id 4941701449 \
  --campaign-id 23294632479 \
  --csv output/replacement-suggestions-20251125-reviewed.csv \
  --live
```

**What happens:**
1. Finds each asset by Original_Text
2. Intelligently orders operations (REMOVE→CREATE→LINK or CREATE→LINK→REMOVE)
3. Executes swaps (batched when safe, one-by-one when at limits)
4. Logs all operations
5. Generates execution report

**Output:**
- Console: Real-time progress with ✅ success / ❌ error indicators
- Log file: `logs/execution-report-live-YYYYMMDD-HHMMSS.json`

**Monitor:**
- Success rate (should be 100% if dry-run passed)
- Any errors (check logs for details)
- Time taken (batching is faster)

## Configuration Reference

**config.yaml structure:**

```yaml
# Performance analysis thresholds
thresholds:
  min_impressions: 1000           # Assets with fewer impressions get lower priority
  max_ctr: 2.5                    # Flag assets with CTR below this (%)
  max_conversion_rate: 8.0        # Flag assets with Conv Rate below this (%)

# Priority levels for flagged assets
priorities:
  low_impressions_low_performance: HIGH    # <1000 impr + low CTR/Conv
  high_impressions_low_performance: HIGH   # >1000 impr + low CTR/Conv
  moderate_impressions_low_ctr: MEDIUM     # 500-1000 impr + low CTR
  low_volume: LOW                          # <500 impressions total

# AI text generation settings
ai:
  model: claude-sonnet-4              # Claude model to use
  temperature: 0.7                    # Creativity (0-1, higher = more creative)
  max_tokens: 2000                    # Max response length

# Asset limits (Google Ads Performance Max)
asset_limits:
  headlines:
    min: 3
    max: 15
  long_headlines:
    min: 1
    max: 5
  descriptions:
    min: 2
    max: 5

# Character limits
character_limits:
  headline: 30
  long_headline: 90
  description: 90
```

## File Naming Convention

**Analyse output:**
`output/underperforming-assets-YYYYMMDD-HHMMSS.csv`

**AI suggestions output:**
`output/replacement-suggestions-YYYYMMDD-HHMMSS.csv`

**Reviewed/edited file (manual save):**
`output/replacement-suggestions-YYYYMMDD-reviewed.csv`

**Execution logs:**
`logs/execution-report-{dry-run|live}-YYYYMMDD-HHMMSS.json`

## Complete Example Workflow

```bash
# 1. Analyse performance (last 30 days)
python3 analyse_asset_performance.py \
  --customer-id 4941701449 \
  --campaign-ids 23294632479 \
  --start-date 2025-10-26 \
  --end-date 2025-11-25

# Output: output/underperforming-assets-20251125-103045.csv
# Found 59 underperformers

# 2. Generate AI replacements
python3 generate_replacement_text.py \
  --customer-id 4941701449 \
  --input output/underperforming-assets-20251125-103045.csv \
  --client-context /Users/administrator/Documents/PetesBrain/clients/tree2mydoor/CONTEXT.md

# Output: output/replacement-suggestions-20251125-104523.csv
# Generated 177 alternatives (3 per asset)

# 3. Manual review
# - Open output/replacement-suggestions-20251125-104523.csv
# - Review AI suggestions, pick best options
# - Edit if needed
# - Change Action to SWAP for approved ones
# - Save as output/replacement-suggestions-20251125-reviewed.csv

# 4. Dry-run test
python3 execute_asset_optimisation.py \
  --customer-id 4941701449 \
  --campaign-id 23294632479 \
  --csv output/replacement-suggestions-20251125-reviewed.csv \
  --dry-run

# Check logs/execution-report-dry-run-YYYYMMDD-HHMMSS.json
# Verify all assets found, no errors

# 5. Live execution
python3 execute_asset_optimisation.py \
  --customer-id 4941701449 \
  --campaign-id 23294632479 \
  --csv output/replacement-suggestions-20251125-reviewed.csv \
  --live

# Check logs/execution-report-live-YYYYMMDD-HHMMSS.json
# Verify 100% success rate
```

## Best Practices

### Performance Analysis
- Use at least 30 days of data
- Exclude first 7 days after campaign launch (learning phase)
- Run monthly for ongoing optimisation
- Adjust thresholds based on industry/client benchmarks

### AI Text Generation
- Keep client CONTEXT.md updated with latest messaging
- Review all AI suggestions - don't blindly accept
- Test different options (A/B testing approach)
- Maintain brand voice consistency

### Review Process
- Check character limits carefully
- Ensure messaging aligns with landing pages
- Consider seasonal/promotional context
- Get client approval for major changes

### Execution
- Always dry-run first
- Start with low-priority swaps to test
- Monitor performance after swaps (give 7-14 days)
- Document results for future optimisations

## Troubleshooting

### "No underperformers found"

**Possible causes:**
- Thresholds too strict (lower max_ctr/max_conversion_rate)
- Insufficient data (increase date range)
- Campaign performing well (check overall metrics)

**Solutions:**
- Adjust `config.yaml` thresholds
- Use longer date range
- Verify campaign has sufficient volume

### "AI generation failed"

**Possible causes:**
- Claude API key missing/invalid
- Client CONTEXT.md not found
- Rate limiting

**Solutions:**
- Check `~/.anthropic/api_key` exists
- Verify CONTEXT.md path is correct
- Wait 60 seconds if rate limited

### "Character limit exceeded"

**Possible causes:**
- AI generated text too long
- Manual edits exceeded limit

**Solutions:**
- Regenerate with stricter prompts
- Manually edit to fit within limits
- Check `Char_Count` column in CSV

## Integration with Other Workflows

**Combine with Spreadsheet Swaps:**
Can use AI suggestions workflow for some assets, spreadsheet approach for others in same campaign.

**Combine with Manual Testing:**
Use AI to generate options, then A/B test in Google Ads UI before bulk swapping.

**Recurring Optimisation:**
Run monthly:
1. Week 1: Analyse + Generate
2. Week 2: Review + Approve
3. Week 3: Execute + Monitor
4. Week 4: Analyse results

## Performance Expectations

**Typical results:**
- 10-30% of assets flagged as underperformers
- 3 AI options per flagged asset
- 95%+ character limit compliance
- 90%+ of swaps execute successfully
- 7-14 days to see performance impact

**Success metrics:**
- Campaign-level CTR increase: 0.1-0.5%
- Campaign-level Conv Rate increase: 0.5-2%
- Time saved vs manual: 80-90%
