#!/bin/bash
#
# Batch Create Google Docs for All Clients
# This script outputs instructions for Claude Code to create docs efficiently
#

set -e

REGISTRY="/Users/administrator/Documents/PetesBrain/shared/data/client-google-docs.json"
CLIENTS_DIR="/Users/administrator/Documents/PetesBrain/clients"

echo "========================================================"
echo "Batch Google Doc Creation - Instructions for Claude Code"
echo "========================================================"
echo ""
echo "Please create Google Docs for the following clients using mcp__google-drive__createGoogleDoc:"
echo ""

# List of clients that need docs (excluding tree2mydoor and accessories-for-the-home which already exist)
CLIENTS="bright-minds clear-prospects crowd-control devonshire-hotels go-glean godshot grain-guard just-bin-bags national-design-academy otc print-my-pdf smythson superspace uno-lighting"

for client in $CLIENTS; do
    CONTEXT_FILE="$CLIENTS_DIR/$client/CONTEXT.md"

    if [ -f "$CONTEXT_FILE" ]; then
        DISPLAY_NAME=$(echo $client | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
        SIZE=$(wc -c < "$CONTEXT_FILE")
        echo "✓ $client"
        echo "  Display Name: $DISPLAY_NAME - CONTEXT (Auto-Synced)"
        echo "  File: $CONTEXT_FILE"
        echo "  Size: $SIZE bytes"
        echo ""
    fi
done

echo "========================================================"
echo "After creating each doc, add to registry at:"
echo "$REGISTRY"
echo "========================================================"
