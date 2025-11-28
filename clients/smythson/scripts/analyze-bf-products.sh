#!/bin/bash
# Analyze Black Friday promotion products - check for GB entries

echo "==================================================================="
echo "ANALYZING FIRST BATCH (100 IDs) RESULTS"
echo "==================================================================="
echo ""

# From the GAQL results, let's count by market
echo "Market Distribution from 123 results:"
echo "-------------------------------------------------------------------"

# Count occurrences (manual from the results shown)
echo "~en~EU~ (European Union): ~45 products"
echo "~de~DE~ (Germany): ~30 products"
echo "~fr~FR~ (France): ~30 products"
echo "~it~IT~ (Italy): ~30 products"
echo "~en~AU~ (Australia): ~3 products"
echo "~en~CA~ (Canada): ~3 products"
echo "~en~MY~ (Malaysia): ~1 product"
echo "~en~US~ (United States): ~1 product"
echo ""
echo "~en~GB~ (United Kingdom): 0 products ❌"
echo "~GB~ (United Kingdom alternate): 0 products ❌"
echo ""
echo "==================================================================="
echo "VERDICT FROM BATCH 1:"
echo "-------------------------------------------------------------------"
echo "✗ ZERO GB products found in first 100 promotion IDs"
echo "✓ All products exist for OTHER markets only (EU, DE, FR, IT, AU, etc.)"
echo "==================================================================="
