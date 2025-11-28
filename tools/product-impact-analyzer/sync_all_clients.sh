#!/bin/bash

# Sync All Clients - Standardize Spreadsheet Format
# Runs sync for each client individually with progress reporting

cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer

export GOOGLE_APPLICATION_CREDENTIALS=/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json

echo "========================================"
echo "Syncing All Clients to Spreadsheets"
echo "Started: $(date)"
echo "========================================"
echo ""

# Array of all e-commerce clients (with product feeds)
# Note: Devonshire Hotels excluded (services, not e-commerce)
clients=(
    "Tree2mydoor"
    "Smythson UK"
    "BrightMinds"
    "Accessories for the Home"
    "Go Glean UK"
    "Positive Bakes"
    "Superspace"
    "Uno Lights"
    "Godshot"
    "Crowd Control"
    "Grain Guard"
    "HappySnapGifts"
    "WheatyBags"
    "Just Bin Bags"
    "Just Bin Bags JHD"
)

total=${#clients[@]}
success=0
failed=0

for i in "${!clients[@]}"; do
    client="${clients[$i]}"
    num=$((i+1))

    echo "[$num/$total] Syncing: $client"

    if .venv/bin/python3 sync_to_sheets.py --client "$client" 2>&1 | grep -q "✅ Completed"; then
        echo "  ✅ Success"
        ((success++))
    else
        echo "  ❌ Failed"
        ((failed++))
    fi

    echo ""
done

echo "========================================"
echo "Sync Complete"
echo "Finished: $(date)"
echo "Success: $success/$total"
echo "Failed: $failed/$total"
echo "========================================"
