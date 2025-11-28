#!/bin/bash
# Add Shared Drive Resources section to all client CONTEXT.md files

CLIENTS=(
    "accessories-for-the-home"
    "bright-minds"
    "clear-prospects"
    "crowd-control"
    "go-glean"
    "godshot"
    "grain-guard"
    "just-bin-bags"
    "national-design-academy"
    "otc"
    "print-my-pdf"
    "superspace"
    "tree2mydoor"
    "uno-lighting"
)

for client in "${CLIENTS[@]}"; do
    context_file="/Users/administrator/Documents/PetesBrain/clients/$client/CONTEXT.md"

    if [ ! -f "$context_file" ]; then
        echo "✗ $client - CONTEXT.md not found"
        continue
    fi

    # Check if section already exists
    if grep -q "## Shared Drive Resources" "$context_file"; then
        echo "⊘ $client - Section already exists"
        continue
    fi

    echo "✓ $client - Adding section..."

    # Find the line with "## Document History"
    line_num=$(grep -n "^## Document History" "$context_file" | cut -d: -f1)

    if [ -z "$line_num" ]; then
        echo "  ⚠ Warning: Could not find Document History section - appending to end"
        cat >> "$context_file" << 'EOF'

---

## Shared Drive Resources

**Last Scanned:** 2025-10-31

### Key Shared Documents

_Automatic monitoring via "Shared with Me" in Google Drive_
_Updated documents will appear here when detected by daily scans_

**Note**: This section tracks important resources shared by the client via Google Drive, including:
- Monthly reports and presentations
- Campaign briefs and strategy documents
- Product data and assets
- Client-maintained documentation

---
EOF
    else
        # Insert before Document History
        temp_file=$(mktemp)
        head -n $((line_num - 2)) "$context_file" > "$temp_file"
        cat >> "$temp_file" << 'EOF'

## Shared Drive Resources

**Last Scanned:** 2025-10-31

### Key Shared Documents

_Automatic monitoring via "Shared with Me" in Google Drive_
_Updated documents will appear here when detected by daily scans_

**Note**: This section tracks important resources shared by the client via Google Drive, including:
- Monthly reports and presentations
- Campaign briefs and strategy documents
- Product data and assets
- Client-maintained documentation

---

EOF
        tail -n +$((line_num - 1)) "$context_file" >> "$temp_file"
        mv "$temp_file" "$context_file"
    fi
done

echo ""
echo "✅ Shared Drive Resources section added to all clients"
