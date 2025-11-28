#!/bin/bash

# Review and correct client assignment for meeting notes
# Usage: ./review-meeting-client.sh

CLIENTS_DIR="/Users/administrator/Documents/PetesBrain/clients"
ROKSYS_DIR="/Users/administrator/Documents/PetesBrain/roksys"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Review Meeting Client Assignment${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Find all recent meeting notes (last 7 days)
recent_meetings=$(find "$CLIENTS_DIR" "$ROKSYS_DIR" -path "*/meeting-notes/*.md" -mtime -7 2>/dev/null | sort -r)

if [ -z "$recent_meetings" ]; then
    echo "No recent meetings found (last 7 days)"
    exit 0
fi

echo -e "${GREEN}Recent meetings (last 7 days):${NC}"
echo ""

count=0
declare -a meeting_files
while IFS= read -r meeting; do
    count=$((count+1))
    meeting_files[$count]=$meeting

    # Extract info
    filename=$(basename "$meeting")
    client_folder=$(echo "$meeting" | sed 's|.*/\([^/]*\)/meeting-notes/.*|\1|')

    # Try to extract date from filename
    date_part=$(echo "$filename" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}')

    echo "$count) $date_part - $client_folder"
    echo "   ${filename:0:60}..."
    echo ""
done <<< "$recent_meetings"

echo ""
echo "Enter meeting number to review (or 'q' to quit): "
read meeting_num

if [ "$meeting_num" = "q" ]; then
    echo "Cancelled."
    exit 0
fi

# Validate input
if ! [[ "$meeting_num" =~ ^[0-9]+$ ]] || [ "$meeting_num" -lt 1 ] || [ "$meeting_num" -gt "$count" ]; then
    echo -e "${YELLOW}Invalid selection.${NC}"
    exit 1
fi

selected_meeting="${meeting_files[$meeting_num]}"

echo ""
echo -e "${GREEN}Selected meeting:${NC}"
echo "$selected_meeting"
echo ""

# Show preview
echo -e "${YELLOW}Preview (first 30 lines):${NC}"
echo "---"
head -30 "$selected_meeting"
echo "---"
echo ""

# Ask what to do
echo "What would you like to do?"
echo "1) Move to different client"
echo "2) Move to roksys (company meeting)"
echo "3) Keep as is"
echo "4) Cancel"
echo ""
echo -n "Select option: "
read action

case $action in
    1)
        # List clients
        echo ""
        echo -e "${GREEN}Available clients:${NC}"
        echo ""
        clients=($(ls -d $CLIENTS_DIR/*/ | grep -v "_templates" | grep -v "_unassigned" | xargs -n 1 basename))

        for i in "${!clients[@]}"; do
            num=$((i+1))
            client="${clients[$i]}"
            display_name=$(echo "$client" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
            echo "$num) $display_name"
        done

        echo ""
        echo -n "Select client number: "
        read client_num

        if ! [[ "$client_num" =~ ^[0-9]+$ ]] || [ "$client_num" -lt 1 ] || [ "$client_num" -gt "${#clients[@]}" ]; then
            echo -e "${YELLOW}Invalid selection.${NC}"
            exit 1
        fi

        client_idx=$((client_num-1))
        target_client="${clients[$client_idx]}"
        target_dir="$CLIENTS_DIR/$target_client/meeting-notes"

        # Create meeting-notes dir if doesn't exist
        mkdir -p "$target_dir"

        # Move file
        filename=$(basename "$selected_meeting")
        mv "$selected_meeting" "$target_dir/$filename"

        echo ""
        echo -e "${GREEN}✓ Moved to $target_client/meeting-notes/${NC}"
        ;;

    2)
        # Move to roksys
        target_dir="$ROKSYS_DIR/meeting-notes"
        mkdir -p "$target_dir"

        filename=$(basename "$selected_meeting")
        mv "$selected_meeting" "$target_dir/$filename"

        echo ""
        echo -e "${GREEN}✓ Moved to roksys/meeting-notes/${NC}"
        ;;

    3)
        echo ""
        echo "Kept as is."
        ;;

    4)
        echo ""
        echo "Cancelled."
        exit 0
        ;;

    *)
        echo -e "${YELLOW}Invalid option.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}Review another? Run script again.${NC}"
