#!/bin/bash
# Feature Completion Verification Script
# Usage: ./verify_completion.sh <feature-directory>

FEATURE_DIR=$1

if [ -z "$FEATURE_DIR" ]; then
    echo "Usage: ./verify_completion.sh <feature-directory>"
    echo "Example: ./verify_completion.sh tools/product-impact-analyzer"
    exit 1
fi

echo "🔍 Verifying completion for: $FEATURE_DIR"
echo ""

# Check directory exists
if [ ! -d "$FEATURE_DIR" ]; then
    echo "❌ FAIL: Directory not found: $FEATURE_DIR"
    exit 1
fi

# Check for completion verification doc
if [ ! -f "$FEATURE_DIR/COMPLETION-VERIFICATION.md" ]; then
    echo "❌ FAIL: Missing COMPLETION-VERIFICATION.md"
    echo "   Create this file documenting all promised capabilities"
    echo "   Template: docs/FEATURE-COMPLETION-CHECKLIST.md"
    exit 1
fi

# Check README exists
if [ ! -f "$FEATURE_DIR/README.md" ]; then
    echo "❌ FAIL: Missing README.md"
    exit 1
fi

# Extract capabilities from README (look for examples)
echo "📋 Checking README structure..."
EXAMPLE_COUNT=$(grep -c "Example" "$FEATURE_DIR/README.md" || echo "0")
CODE_BLOCKS=$(grep -c '```' "$FEATURE_DIR/README.md" || echo "0")
echo "   Found $EXAMPLE_COUNT examples and $CODE_BLOCKS code blocks"

# Check for "Verified Output" section
if grep -q "## Verified Output\|## Real Output" "$FEATURE_DIR/README.md"; then
    echo "   ✅ README includes verified output section"
else
    echo "   ⚠️  WARN: README missing '## Verified Output' section"
    echo "       Add real output examples, not theoretical ones"
fi

# Check completion verification has evidence
echo ""
echo "📝 Checking completion verification..."
if grep -q "Evidence:" "$FEATURE_DIR/COMPLETION-VERIFICATION.md"; then
    echo "   ✅ Evidence provided for capabilities"
else
    echo "   ⚠️  WARN: No evidence links found"
    echo "       Add 'Evidence: [file/output]' for each capability"
fi

# Check for known gaps documentation
if grep -q "NOT IMPLEMENTED\|Known Gap" "$FEATURE_DIR/COMPLETION-VERIFICATION.md"; then
    echo "   ⚠️  Found documented gaps - review before marking complete"
    echo ""
    echo "   Gaps found:"
    grep -A 2 "NOT IMPLEMENTED\|Known Gap" "$FEATURE_DIR/COMPLETION-VERIFICATION.md" | sed 's/^/     /'
fi

echo ""
echo "📊 Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Manual verification required:"
echo "1. Run the feature with real data"
echo "2. Compare output to README examples"
echo "3. Verify all fields shown in examples are present in actual output"
echo "4. Check COMPLETION-VERIFICATION.md documents any gaps"
echo ""
echo "✅ Ready to mark complete when all examples verified!"
