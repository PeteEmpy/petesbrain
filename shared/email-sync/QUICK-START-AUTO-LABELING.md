# Email Auto-Labeling - Quick Start

**Status**: ✅ Active (as of Nov 6, 2025)

## What Changed?

Your email sync now **automatically labels Google rep emails** so you don't have to manually apply labels in Gmail anymore.

## Example

**Before**:
- Lucy sends "Accessories for the Home & Uno Lights Meetings Tomorrow"
- ❌ Sits in inbox unlabeled
- ❌ Doesn't sync to client folders
- ❌ You have to manually apply labels

**After**:
- Lucy sends "Accessories for the Home & Uno Lights Meetings Tomorrow"
- ✅ System detects it's from Lucy (Google rep)
- ✅ Scans subject and finds both clients
- ✅ Auto-applies `client/accessories-for-the-home` label
- ✅ Auto-applies `client/uno-lighting` label
- ✅ Syncs to Accessories folder automatically

## How to Use It

**Nothing!** It runs automatically every time you sync emails.

```bash
# Just run sync as normal
cd /Users/administrator/Documents/PetesBrain
shared/email-sync/.venv/bin/python3 shared/email-sync/sync_emails.py
```

Output will show:
```
🏷️  Auto-labeling Google rep emails...
  Found 50 potential Google rep emails
    ✓ Labeled [accessories-for-the-home, uno-lighting]: Accessories for the Home & Uno Lights Me...
    ✓ Labeled [devonshire-hotels]: [please confirm] Google / Devonshire che...
    ⊘ No clients detected: Missing Think Leads? We've Got Your Backstage Pass...

🔄 Starting email sync...
[rest of sync process]

============================================================
Sync Complete!
============================================================
Auto-labeled: 25 emails
Total emails processed: 949
Newly synced: 15
Already synced: 934
Errors: 0
============================================================
```

## Which Emails Are Auto-Labeled?

### Google Reps Detected
- Lucy Loughlin (lucyloughlin@google.com) - Accessories for the Home
- Luiza Arruda (luizaarruda@google.com) - Uno Lighting
- Solomiya Karplyuk (solomiyak@google.com) - NDA, Clear Prospects
- Mdurand (mdurand@google.com) - Devonshire Hotels
- Jasmine (jasmine@google.com) - Superspace
- Ally Hamps (allyhamps@google.com) - Manager/backup
- Any other @google.com email (excluding automated emails)

### Clients Detected
System looks for these names in subject/body:

| Client | What It Looks For |
|--------|------------------|
| Accessories for the Home | "accessories for the home" |
| Uno Lighting | "uno lights", "uno lighting" |
| Devonshire Hotels | "devonshire", "cavendish", "property arms" |
| National Design Academy | "national design academy", "nda", "design academy" |
| Smythson | "smythson" |
| Clear Prospects | "clear prospects" |
| Superspace | "superspace" |
| + 6 more clients |

## Testing Before Using

Want to see what would be labeled without actually doing it?

```bash
cd /Users/administrator/Documents/PetesBrain
shared/email-sync/.venv/bin/python3 shared/email-sync/sync_emails.py --dry-run
```

This shows you what **would** be labeled and synced without actually doing it.

## When to Add New Google Reps

Got a new Google rep email?

1. Open `shared/email-sync/sync_emails.py`
2. Find the `_is_google_rep_email()` method
3. Add their email to the list:
   ```python
   google_rep_emails = [
       'lucyloughlin@google.com',
       'luizaarruda@google.com',
       'newrep@google.com',  # Add here
   ]
   ```

## When to Add New Client Patterns

Client being missed? Add a pattern:

1. Open `shared/email-sync/sync_emails.py`
2. Find the `_detect_client_from_content()` method
3. Add pattern to the dictionary:
   ```python
   'client-folder-name': ['pattern 1', 'alternate name', 'abbreviation'],
   ```

## Manual Override

Want to manually label an email? **Still works!**

Just apply labels in Gmail as you always did. The auto-labeling won't overwrite manual labels.

## Troubleshooting

**Email not being auto-labeled?**
1. Check it's from a Google rep (@google.com address)
2. Check client name is mentioned in subject/body
3. Run `--dry-run` to see detection logic

**False positive (wrong label)?**
1. Report it so patterns can be refined
2. Manually fix the label in Gmail
3. Email will sync to correct folder on next run

## More Details

- Full documentation: [AUTO-LABELING.md](AUTO-LABELING.md)
- Setup guide: [README.md](README.md)
- System integration: [docs/AUTOMATION.md](../../docs/AUTOMATION.md)

## Summary

🎉 **You no longer need to manually label Google rep emails!**

The system automatically:
- ✅ Detects Google rep emails
- ✅ Finds which clients are mentioned
- ✅ Applies the right labels
- ✅ Syncs to client folders

Just keep running your email sync as normal and it all happens automatically.
