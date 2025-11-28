# Finish Client Google Docs Setup

## Status: 2/16 Complete

✅ **Created:**
1. Tree2mydoor - https://docs.google.com/document/d/1mXPdLygmIxngrWVOdsjZSBgnvw9AE9qtTaMyE4fn-Xk/edit
2. Accessories For The Home - https://docs.google.com/document/d/1lJpoyDFn-X6XfcL4AFQw09wXLZLNGk0qcc6xl8W2y-Q/edit

⏳ **Remaining (14 clients):**
- Bright Minds
- Clear Prospects
- Crowd Control
- Devonshire Hotels
- Go Glean
- Godshot
- Grain Guard
- Just Bin Bags
- National Design Academy
- OTC
- Print My PDF
- Smythson
- Superspace
- Uno Lighting

---

## Quick Completion Command

**To finish setup, paste this into Claude Code:**

```
Create Google Docs for all remaining clients (14 clients) using their CONTEXT.md files. For each client:

1. Read /Users/administrator/Documents/PetesBrain/clients/[client]/CONTEXT.md
2. Create Google Doc with name: "[Display Name] - CONTEXT (Auto-Synced)"
3. Add doc ID and URL to /Users/administrator/Documents/PetesBrain/shared/data/client-google-docs.json
4. Update /Users/administrator/Documents/PetesBrain/claude-ai-custom-instructions.txt with the custom instruction block

Clients to create:
- bright-minds
- clear-prospects
- crowd-control
- devonshire-hotels
- go-glean
- godshot
- grain-guard
- just-bin-bags
- national-design-academy
- otc
- print-my-pdf
- smythson
- superspace
- uno-lighting

Process them in batches to manage token usage.
```

---

## What's Already Set Up

✅ **Infrastructure Complete:**
1. **Automated Daily Sync Script**: `/Users/administrator/Documents/PetesBrain/shared/scripts/sync-all-client-contexts.sh`
   - Syncs all client CONTEXT.md files to Google Drive .md files
   - Creates marker files for Google Doc updates
   - Runs daily at 7 AM (once LaunchAgent is configured)

2. **Registry**: `/Users/administrator/Documents/PetesBrain/shared/data/client-google-docs.json`
   - Tracks all client Google Doc IDs
   - Used by sync script to know which docs to update

3. **Reference Sheet**: `/Users/administrator/Documents/PetesBrain/claude-ai-custom-instructions.txt`
   - Contains custom instructions for Claude.ai for each client
   - Ready to paste into Claude.ai when working on specific clients
   - Will be complete once all 14 remaining docs are created

---

## Next Steps

1. **Finish Creating Docs**: Use command above to create remaining 14 client Google Docs
2. **Configure LaunchAgent**: Update `/Users/administrator/Library/LaunchAgents/com.petesbrain.tree2mydoor-context-upload.plist` to use the new universal sync script
3. **Test Sync**: Run sync script manually to verify all clients sync correctly
4. **Share Instructions**: Provide completed `claude-ai-custom-instructions.txt` to user

---

## Testing

Once all docs are created, test the sync:

```bash
# Run sync manually
/Users/administrator/Documents/PetesBrain/shared/scripts/sync-all-client-contexts.sh

# Check log
cat ~/.petesbrain-all-clients-sync.log | tail -50

# Verify files in Google Drive
ls -lh ~/Library/CloudStorage/GoogleDrive-petere@roksys.co.uk/My\ Drive/PetesBrain-Context/
```
