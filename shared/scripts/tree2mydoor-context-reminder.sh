#!/bin/bash
#
# Tree2MyDoor CONTEXT.md Daily Upload Reminder
# Creates a notification file at 7 AM daily
#

REMINDER_FILE="$HOME/.petesbrain-tree2mydoor-upload-reminder.txt"
LOG_FILE="$HOME/.petesbrain-tree2mydoor-context-upload.log"
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# Create reminder
cat > "$REMINDER_FILE" << EOF
====================================================================
Tree2MyDoor CONTEXT.md Upload Reminder
====================================================================
Date: $DATE

ACTION NEEDED: Upload today's CONTEXT.md to Google Drive

In Claude Code, say:
"Upload Tree2MyDoor CONTEXT.md to Google Drive for today"

This will update the file at:
https://drive.google.com/file/d/1M0ZLvTsv8_WDIK8A16IPVYKSv3CEX4sL/view

Filename format: Tree2MyDoor CONTEXT YYYY-MM-DD.md
====================================================================
EOF

# Log the reminder creation
echo "[$DATE] Reminder created at $REMINDER_FILE" >> "$LOG_FILE"

# Display the reminder
cat "$REMINDER_FILE"

exit 0
