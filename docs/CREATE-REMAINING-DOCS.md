# Create Remaining Client Google Docs

## Status: 3/16 Complete

✅ **Created:**
1. Tree2mydoor
2. Accessories For The Home
3. Bright Minds

⏳ **Remaining (13 clients):**
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

---

## Quick Command to Finish

Paste this into Claude Code:

```
Create Google Docs for these 13 remaining clients. For each:

1. Read /Users/administrator/Documents/PetesBrain/clients/[client]/CONTEXT.md
2. Create Google Doc titled "[Display Name] - CONTEXT (Auto-Synced)" using mcp__google-drive__createGoogleDoc
3. Track the doc ID

Clients (in order):
1. clear-prospects (Clear Prospects)
2. crowd-control (Crowd Control)
3. devonshire-hotels (Devonshire Hotels)
4. go-glean (Go Glean)
5. godshot (Godshot)
6. grain-guard (Grain Guard)
7. just-bin-bags (Just Bin Bags)
8. national-design-academy (National Design Academy)
9. otc (OTC)
10. print-my-pdf (Print My PDF)
11. smythson (Smythson)
12. superspace (Superspace)
13. uno-lighting (Uno Lighting)

After all are created:
- Update /Users/administrator/Documents/PetesBrain/shared/data/client-google-docs.json with all doc IDs
- Update /Users/administrator/Documents/PetesBrain/claude-ai-custom-instructions.txt with all custom instruction blocks
```

---

## Files to Update After Creation

1. **Registry**: `/Users/administrator/Documents/PetesBrain/shared/data/client-google-docs.json`
   - Add each client with: doc_id, display_name, created_date, doc_url

2. **Custom Instructions**: `/Users/administrator/Documents/PetesBrain/claude-ai-custom-instructions.txt`
   - Add custom instruction block for each client following the pattern of Tree2mydoor and Accessories For The Home

---

## Current Registry (3 clients):

```json
{
  "tree2mydoor": {
    "doc_id": "1mXPdLygmIxngrWVOdsjZSBgnvw9AE9qtTaMyE4fn-Xk",
    "display_name": "Tree2mydoor",
    "created_date": "2025-11-04",
    "doc_url": "https://docs.google.com/document/d/1mXPdLygmIxngrWVOdsjZSBgnvw9AE9qtTaMyE4fn-Xk/edit"
  },
  "accessories-for-the-home": {
    "doc_id": "1lJpoyDFn-X6XfcL4AFQw09wXLZLNGk0qcc6xl8W2y-Q",
    "display_name": "Accessories For The Home",
    "created_date": "2025-11-04",
    "doc_url": "https://docs.google.com/document/d/1lJpoyDFn-X6XfcL4AFQw09wXLZLNGk0qcc6xl8W2y-Q/edit"
  },
  "bright-minds": {
    "doc_id": "1kvqdXB6De2A6jjfGU2FyDNEF8Eg0w4jWgzSyEjacrfU",
    "display_name": "Bright Minds",
    "created_date": "2025-11-04",
    "doc_url": "https://docs.google.com/document/d/1kvqdXB6De2A6jjfGU2FyDNEF8Eg0w4jWgzSyEjacrfU/edit"
  }
}
```
