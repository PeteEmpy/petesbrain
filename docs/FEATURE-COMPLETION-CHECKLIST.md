# Feature Completion Checklist

## Problem
Features are documented as "complete" but missing critical functionality (e.g., Product Impact Analyzer promised price tracking but wasn't capturing it).

## Solution: Mandatory Completion Steps

### 1. Specification Review
Before marking ANY feature complete, verify:
- [ ] Read the original requirements/README
- [ ] List ALL promised capabilities
- [ ] Check each capability is actually implemented

### 2. End-to-End Testing
- [ ] Run the feature with real data
- [ ] Verify all outputs match documentation
- [ ] Check data completeness (all promised fields present)
- [ ] Test edge cases mentioned in docs

### 3. Documentation Validation
- [ ] Compare README examples with actual output
- [ ] If examples show data fields, verify those fields exist in real output
- [ ] Update docs if capability isn't implemented (don't leave promises)

### 4. Integration Check
- [ ] Verify downstream systems can consume the output
- [ ] Check dependent tools receive expected data format
- [ ] Test the full workflow, not just the feature in isolation

### 5. Completion Artifact
Create a `COMPLETION-VERIFICATION.md` in the feature directory with:
```markdown
# Completion Verification: [Feature Name]

**Date:** YYYY-MM-DD
**Verified By:** [Name/Claude]

## Promised Capabilities
- [x] Capability 1: Description
  - Evidence: [File/output showing it works]
- [x] Capability 2: Description
  - Evidence: [File/output showing it works]
- [ ] Capability 3: **NOT IMPLEMENTED**
  - Status: Documented but not coded
  - Action: Remove from README or implement

## Real Output Sample
[Paste actual output showing all promised fields]

## Known Gaps
- Gap 1: Description and planned resolution
- Gap 2: Description and planned resolution
```

## Example: Product Impact Analyzer Gap

### What Happened
- **README Example** (line 125): Shows "Price increased £34.99 → £39.99"
- **Actual Implementation**: analyzer.py expects price columns 7-9
- **Data Collection**: merchant_center_via_google_ads.py doesn't write price to spreadsheet
- **Result**: Feature promises price tracking but doesn't capture it

### What Should Have Happened
1. Run analyzer against real Tree2mydoor data
2. Notice price columns are empty
3. Either:
   a. Implement price capture in fetch_data_automated.py, OR
   b. Remove price examples from README with "Future enhancement" note

### Immediate Action for Product Impact Analyzer
Create `/tools/product-impact-analyzer/COMPLETION-VERIFICATION.md`:
```markdown
# Completion Verification: Product Impact Analyzer

## Promised Capabilities
- [x] Track product availability changes (add/remove from feed)
- [x] Track product label changes (custom_label_0 through 4)
- [x] Correlate changes with performance (clicks, conversions, revenue)
- [x] Historical trend analysis
- [x] Automated weekly reports
- [ ] **Price tracking - NOT IMPLEMENTED**
  - Status: Code exists in analyzer.py but data not captured
  - Action: Add price field to fetch_data_automated.py

## Known Gap: Price Tracking
- README shows price change examples (line 125-135)
- analyzer.py has price parsing (line 38-40, 173-188)
- merchant_center_via_google_ads.py has price extraction methods
- **Missing**: Price not written to daily spreadsheet snapshots

### To Complete Price Tracking
1. Modify `merchant_center_via_google_ads.py` line ~200 to include price field
2. Add price column to spreadsheet schema (after "Label")
3. Update config to specify price column index
4. Backfill historical price data from Merchant Center API
5. Test analyzer detects price changes
```

## Enforcement

### For New Features
Before marking "DONE":
1. Run `./verify_completion.sh` (create this script)
2. Create COMPLETION-VERIFICATION.md
3. Add to git commit message: "Verified complete per FEATURE-COMPLETION-CHECKLIST"

### For Existing Features
Priority audit list (features with examples in docs):
1. Product Impact Analyzer - Price tracking **[FOUND GAP]**
2. Google Ads Generator - All promised ad types working?
3. Monthly Report Generator - All metrics present?
4. Email Sync Auto-labeling - All label rules working?
5. Knowledge Base Processor - All sources ingested?

## Template: verify_completion.sh

```bash
#!/bin/bash
# Feature Completion Verification Script
# Usage: ./verify_completion.sh <feature-directory>

FEATURE_DIR=$1

if [ -z "$FEATURE_DIR" ]; then
    echo "Usage: ./verify_completion.sh <feature-directory>"
    exit 1
fi

echo "🔍 Verifying completion for: $FEATURE_DIR"
echo ""

# Check for completion verification doc
if [ ! -f "$FEATURE_DIR/COMPLETION-VERIFICATION.md" ]; then
    echo "❌ FAIL: Missing COMPLETION-VERIFICATION.md"
    echo "   Create this file documenting all promised capabilities"
    exit 1
fi

# Check README exists
if [ ! -f "$FEATURE_DIR/README.md" ]; then
    echo "❌ FAIL: Missing README.md"
    exit 1
fi

# Extract capabilities from README (look for examples)
echo "📋 Checking for capability examples in README..."
EXAMPLE_COUNT=$(grep -c "Example\|```" "$FEATURE_DIR/README.md" || echo "0")
echo "   Found $EXAMPLE_COUNT code blocks/examples"

# Check if COMPLETION-VERIFICATION covers all examples
echo ""
echo "📝 Manual verification required:"
echo "   1. Run the feature with real data"
echo "   2. Compare output to README examples"
echo "   3. Verify all fields shown in examples are present"
echo "   4. Document any gaps in COMPLETION-VERIFICATION.md"
echo ""
echo "✅ Ready to mark complete? Confirm all examples work!"
```

## Prevention Strategy

### Code Review Prompt
Before any "feature complete" commit, Claude should:
1. Read the feature README
2. Identify all examples with specific data fields
3. Check if those fields exist in actual output
4. Flag any discrepancies

### Documentation Standard
Every feature README must include:
```markdown
## Verified Output
[PASTE REAL OUTPUT HERE - not invented examples]

Last verified: YYYY-MM-DD
Verification method: [Command run to generate this output]
```

## Immediate TODO

1. **Audit Product Impact Analyzer**
   - Add price capture to data collection
   - OR remove price examples from README
   - Create COMPLETION-VERIFICATION.md

2. **Create verify_completion.sh script**

3. **Audit other tools with examples in docs**
   - Priority: Tools with "Example" sections showing specific output

4. **Add to project workflow**
   - Update CLAUDE.md with completion checklist
   - Make verification mandatory before "done"
