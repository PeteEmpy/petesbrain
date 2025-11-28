# Unassigned Meetings

This folder contains meeting notes that could not be automatically assigned to a specific client.

## What This Folder Is For

The Granola Meeting Importer tries to automatically detect which client each meeting belongs to by:
1. Analyzing the meeting title
2. Analyzing the meeting content (notes + transcript)

When both methods fail to find a match, meetings are saved here.

## What To Do

Review meetings in this folder and manually move them to the appropriate client folder:

```bash
# Example: Move a meeting to the correct client
mv meeting-notes/2025-10-28-strategy-call.md ../bright-minds/meeting-notes/
```

## Improving Auto-Detection

If meetings are consistently ending up here for a specific client, you can:

1. **Use more specific meeting titles** in Granola that include the client name
2. **Mention the client name early** in the meeting discussion
3. **Check that the client folder name** matches common variations (e.g., "uno-lighting" matches "Uno", "Uno Lighting", "UnoLighting")

## Common Scenarios

- **Generic titles**: "Weekly Check-in", "Status Update", "Quick Call"
- **Internal meetings**: Team meetings, planning sessions
- **Personal meetings**: 1-on-1s, reviews, interviews
- **Prospect meetings**: Calls with potential clients not yet added to the system

You may want to create additional folders for these categories if needed.
