#!/bin/bash

# Add ad hoc notes to client CONTEXT.md files
# Usage: ./add-context-note.sh

CLIENTS_DIR="/Users/administrator/Documents/PetesBrain/clients"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
DATE_ONLY=$(date "+%Y-%m-%d")

# Colors for better UX
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Add Note to Client CONTEXT.md${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# List clients
echo -e "${GREEN}Available clients:${NC}"
echo ""
clients=($(ls -d $CLIENTS_DIR/*/ | grep -v "_templates" | grep -v "_unassigned" | xargs -n 1 basename))

for i in "${!clients[@]}"; do
    num=$((i+1))
    client="${clients[$i]}"
    # Format client name nicely
    display_name=$(echo "$client" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
    echo "$num) $display_name"
done

echo ""
echo -n "Select client number (or 'q' to quit): "
read client_num

if [ "$client_num" = "q" ]; then
    echo "Cancelled."
    exit 0
fi

# Validate input
if ! [[ "$client_num" =~ ^[0-9]+$ ]] || [ "$client_num" -lt 1 ] || [ "$client_num" -gt "${#clients[@]}" ]; then
    echo -e "${YELLOW}Invalid selection.${NC}"
    exit 1
fi

# Get selected client
client_idx=$((client_num-1))
client_slug="${clients[$client_idx]}"
client_name=$(echo "$client_slug" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
context_file="$CLIENTS_DIR/$client_slug/CONTEXT.md"

if [ ! -f "$context_file" ]; then
    echo -e "${YELLOW}CONTEXT.md not found for $client_name${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Adding note for: $client_name${NC}"
echo ""

# Show section options
echo "Which section should this note be added to?"
echo ""
echo "1) Strategic Context - Strategy decisions, approach changes"
echo "2) Client Preferences - Communication style, sensitivities discovered"
echo "3) Business Context - Product changes, pricing, website updates"
echo "4) Known Issues - Current problems or challenges"
echo "5) Key Learnings - What works, what doesn't, insights discovered"
echo "6) Campaign Notes - Campaign-specific observations"
echo "7) Action Items - Tasks or reminders"
echo "8) Quick Reference - Links, contacts, important info"
echo "9) General Note - Add to end of file"
echo ""
echo -n "Select section number: "
read section_num

# Map section numbers to section headers
case $section_num in
    1) section="## Strategic Context";;
    2) section="## Client Preferences & Communication";;
    3) section="## Business Context";;
    4) section="## Known Issues & Challenges";;
    5) section="## Key Learnings & Insights";;
    6) section="## Campaign-Specific Notes";;
    7) section="## Action Items & Reminders";;
    8) section="## Quick Reference";;
    9) section="## Ad Hoc Notes";;
    *)
        echo -e "${YELLOW}Invalid selection.${NC}"
        exit 1
        ;;
esac

echo ""
echo "Enter your note (press Ctrl+D when finished):"
echo -e "${YELLOW}---${NC}"
note=$(cat)

if [ -z "$note" ]; then
    echo -e "${YELLOW}No note entered. Cancelled.${NC}"
    exit 0
fi

# Create backup
cp "$context_file" "${context_file}.backup"

# Add note to appropriate section
if [ "$section" = "## Ad Hoc Notes" ]; then
    # Add to end of file if Ad Hoc Notes section
    if ! grep -q "^## Ad Hoc Notes" "$context_file"; then
        # Create section if it doesn't exist
        echo "" >> "$context_file"
        echo "---" >> "$context_file"
        echo "" >> "$context_file"
        echo "## Ad Hoc Notes" >> "$context_file"
        echo "" >> "$context_file"
        echo "Quick notes and observations that don't fit elsewhere:" >> "$context_file"
        echo "" >> "$context_file"
    fi

    echo "**$DATE_ONLY**: $note" >> "$context_file"
    echo "" >> "$context_file"
else
    # Insert after the section header
    # This is a bit complex - we'll append at end of section
    temp_file="${context_file}.temp"
    awk -v section="$section" -v note="$note" -v date="$DATE_ONLY" '
        /^'"$section"'/ {
            print
            in_section=1
            next
        }
        /^## / && in_section {
            print ""
            print "**Note added " date "**:"
            print note
            print ""
            in_section=0
        }
        {print}
        END {
            if (in_section) {
                print ""
                print "**Note added " date "**:"
                print note
                print ""
            }
        }
    ' "$context_file" > "$temp_file"

    mv "$temp_file" "$context_file"
fi

# Update "Last Updated" date at top of file
sed -i.bak "s/\*\*Last Updated\*\*:.*/\*\*Last Updated\*\*: $DATE_ONLY/" "$context_file"
rm "${context_file}.bak"

# Add to document history
echo "" >> "$context_file"
echo "| $DATE_ONLY | Ad hoc note added to $(echo $section | sed 's/## //') | User (via add-context-note.sh) |" >> "$context_file"

echo ""
echo -e "${GREEN}✓ Note added successfully!${NC}"
echo ""
echo "Location: $context_file"
echo "Section: $section"
echo "Backup saved: ${context_file}.backup"
echo ""
echo -e "${BLUE}Tip: You can also add notes directly by editing the CONTEXT.md file.${NC}"
