---
description: Run email sync (auto-label + sync to client folders)
allowed-tools: Bash, Read
---

# Email Sync

Run the complete email sync workflow which includes:

1. **Auto-labelling** - Scans inbox and sent emails, applies `client/[name]` labels
2. **Sync to folders** - Copies labelled emails to `clients/[client]/emails/`
3. **Google rep emails** - Copies Google rep emails to knowledge base

## Run Command

```bash
/Users/administrator/Documents/PetesBrain/shared/scripts/sync-emails.sh
```

## After Running

Report back:
- How many emails were labelled
- How many emails were synced
- Any errors encountered
- Any unmatched emails that might need config updates

If there are unmatched emails, check:
```bash
cat /Users/administrator/Documents/PetesBrain/shared/email-sync/logs/unmatched_inbox_emails.log | tail -20
cat /Users/administrator/Documents/PetesBrain/shared/email-sync/logs/unmatched_sent_emails.log | tail -20
```

And suggest adding the domains/emails to `shared/email-sync/auto-label-config.yaml` if needed.
