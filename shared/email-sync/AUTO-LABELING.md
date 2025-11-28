# Email Auto-Labeling System

**Status**: ✅ Active (Added 2025-11-06, Updated 2025-11-07)

## Overview

The email sync system now includes **intelligent auto-labeling** that automatically detects and labels:
1. **Inbox emails** from clients, Google reps, and other sources
2. **Sent emails** to clients (matches based on recipient domains/emails)

## How It Works

### 1. Inbox Email Labeling
Scans **inbox** emails for:
- Domain matches (e.g., `@smythson.com`)
- Exact email addresses (e.g., `garry@acunningplan.co.uk`)
- Keywords in subject/body (e.g., "devonshire hotels")
- Company names in sender field

### 2. Sent Email Labeling (NEW)
Scans **sent** emails for:
- Recipient domains in To: field (e.g., sent to `@clearprospects.com`)
- Specific recipient emails (e.g., sent to `michael.robinson@clearprospects.com`)
- Keywords in subject/body (secondary confirmation)

### 3. Client Detection Patterns
Pattern matching uses confidence scoring:

| Client | Detection Patterns |
|--------|-------------------|
| accessories-for-the-home | "accessories for the home", "accessoriesforthehome" |
| bright-minds | "bright minds", "brightminds", "bright-minds" |
| clear-prospects | "clear prospects", "clearprospects" |
| crowd-control | "crowd control", "crowdcontrol" |
| devonshire-hotels | "devonshire hotels", "devonshire", "cavendish", "property arms" |
| godshot | "godshot" |
| national-design-academy | "national design academy", "nda", "design academy" |
| otc | "otc", "online training" |
| print-my-pdf | "print my pdf", "printmypdf" |
| smythson | "smythson" |
| superspace | "superspace", "super space" |
| tree2mydoor | "tree2mydoor", "tree 2 my door" |
| uno-lighting | "uno lights", "uno lighting", "uno-lights", "unolighting" |

### 4. Confidence Scoring

**Inbox emails (From: field matching)**:
- Domain match: +50 points (e.g., `from:person@smythson.com`)
- Exact email match: +40 points
- Subject keyword: +15 points
- Body keyword: +10 points
- Company name in sender: +20 points

**Sent emails (To: field matching)**:
- Domain match: +50 points (e.g., `to:person@clearprospects.com`)
- Exact email match: +40 points
- Subject keyword: +15 points
- Body keyword: +10 points

**Minimum confidence**: 70 points (configurable in `auto-label-config.yaml`)

## Implementation

### Files Modified

**`shared/email-sync/auto_label.py`** (Standalone auto-labeling tool):
- `_process_emails_with_query()` - Generic email processing with query
- `_match_client_sent()` - NEW: Match sent emails based on To: field
- `auto_label_emails()` - Processes both inbox AND sent emails
- `_match_client()` - Match inbox emails based on From: field

**`shared/email-sync/sync_emails.py`** (Email sync tool):
- `sync_sent_emails()` - Syncs sent emails to client folders
- `_get_client_search_terms()` - Gets search terms for sent email matching
- Integrated with `sync_emails()` main workflow

**`shared/email-sync/auto-label-config.yaml`**:
- Client detection rules (domains, emails, keywords)
- Confidence threshold settings

### Integration

**Option 1: Standalone Auto-Labeling**
```bash
# Label inbox AND sent emails
python3 shared/email-sync/auto_label.py

# Dry run to test
python3 shared/email-sync/auto_label.py --dry-run
```

**Option 2: Email Sync (includes auto-labeling)**
```bash
# Sync inbox AND sent emails (already labeled)
python3 shared/email-sync/sync_emails.py

# Dry run to test
python3 shared/email-sync/sync_emails.py --dry-run
```

**Automated**: The LaunchAgent runs email sync automatically every 6 hours, which now includes sent emails.

## Example Output

```
============================================================
Pete's Brain - Auto Email Labeling
============================================================

📧 Authenticating with Gmail...
✓ Authentication successful

🏷️  Starting auto-labeling...

📧 Processing inbox emails: in:inbox after:2024/11/07 -in:spam -in:trash
Max emails to process: 100

Found 23 inbox emails to analyze

[1] From: garry@acunningplan.co.uk
    Subject: November budget update
    Matched: devonshire-hotels (confidence: 90%)
    Reasons: domain:acunningplan.co.uk, email:garry@acunningplan.co.uk
    ✓ Labeled as: client/devonshire-hotels

[2] From: michael.robinson@clearprospects.com
    Subject: Photo Cushions performance
    Matched: clear-prospects (confidence: 90%)
    Reasons: domain:clearprospects.com, email:michael.robinson@clearprospects.com
    ✓ Labeled as: client/clear-prospects

📧 Processing sent emails: in:sent after:2024/11/07 -in:spam -in:trash
Max emails to process: 100

Found 15 sent emails to analyze

[1] Sent: garry@acunningplan.co.uk
    Subject: Re: Budget increase proposal
    Matched: devonshire-hotels (confidence: 90%)
    Reasons: to_domain:acunningplan.co.uk, to_email:garry@acunningplan.co.uk
    ✓ Labeled as: client/devonshire-hotels

[2] Sent: ant@getsuperspace.com
    Subject: Weekly performance update
    Matched: superspace (confidence: 90%)
    Reasons: to_domain:getsuperspace.com, to_email:ant@getsuperspace.com
    ✓ Labeled as: client/superspace

============================================================
Auto-Labeling Complete!
============================================================
Total emails processed: 38
Successfully labeled: 32
No match found: 6
Errors: 0
============================================================

💡 Tip: Check logs/unmatched_inbox_emails.log and logs/unmatched_sent_emails.log to review unmatched emails
   You can add their domains/keywords to auto-label-config.yaml
```

## Maintenance

### Adding New Clients
Edit `shared/email-sync/auto-label-config.yaml`:

```yaml
clients:
  new-client:
    label: "client/new-client"
    domains:
      - "newclient.com"
      - "newclient.co.uk"
    emails:
      - "contact@newclient.com"
    keywords:
      - "new client"
      - "newclient"
    company_names:
      - "New Client Ltd"
```

Then add to `shared/email-sync/config.yaml`:

```yaml
client_labels:
  "client/new-client": "new-client"
```

### Adjusting Confidence Threshold
Edit `auto-label-config.yaml`:

```yaml
settings:
  min_confidence: 70  # Increase for stricter matching, decrease for looser
```

### Adjusting Time Window
Default lookback is 365 days. Edit `auto-label-config.yaml`:

```yaml
settings:
  lookback_days: 365  # Change to desired lookback period
```

## Troubleshooting

### Labels not being applied?
1. Check that client labels exist in Gmail (format: `client/client-name`)
2. Verify client patterns in `client_patterns` dictionary
3. Run with `--dry-run` to see what would be labeled

### Email still not syncing?
1. Ensure the label was actually applied in Gmail
2. Check that `config.yaml` includes the client label mapping
3. Verify the email isn't already in `synced_ids` (check `.email-sync-state.json`)

### False positives?
If emails are being mislabeled:
1. Refine the detection patterns to be more specific
2. Add exclusion patterns if needed
3. Adjust the `_is_google_rep_email()` logic to exclude certain sender types

## Benefits

✅ **Automatic**: No manual labeling needed for client emails (inbox or sent)
✅ **Bidirectional**: Labels both incoming and outgoing client communications
✅ **Smart detection**: Confidence scoring ensures accurate matching
✅ **Non-destructive**: Only adds labels, never removes them
✅ **Backwards compatible**: Works with existing manual labels
✅ **Separate logs**: Inbox and sent emails logged separately for easier review

## Example Use Cases

### Use Case 1: Inbox Email
**Before**: Client sends "Budget update for November"
- ❌ Email stays in inbox unlabeled (if domain not recognized)
- ❌ Doesn't sync to client folder
- ❌ Requires manual Gmail labeling

**After**:
- ✅ Auto-detects client from sender domain
- ✅ Applies `client/devonshire-hotels` label
- ✅ Syncs to `clients/devonshire-hotels/emails/`
- ✅ Available in client context

### Use Case 2: Sent Email
**Before**: You send "Q4 Strategy" to `ant@getsuperspace.com`
- ❌ Email stays in Sent folder unlabeled
- ❌ Doesn't appear in client folder
- ❌ No record in client context

**After**:
- ✅ Auto-detects client from recipient domain
- ✅ Applies `client/superspace` label
- ✅ Syncs to `clients/superspace/emails/`
- ✅ Marked as **[SENT]** in filename and with 📤 indicator
- ✅ Complete communication history in one place

## Performance

- Processes up to 100 inbox + 100 sent emails per run
- Typical run time: 10-20 seconds for both inbox and sent
- Only processes emails without client labels (avoids re-processing)
- Lookback period: 365 days (configurable)

## Future Enhancements

Potential improvements:
- [ ] AI-powered client detection for ambiguous emails
- [ ] Support for other rep types (agency contacts, partners)
- [ ] Learning system to improve pattern matching over time
- [ ] Dashboard showing auto-labeling accuracy
- [ ] Email threading (link sent emails to received replies)
