# Adding New Email Auto-Labeling Patterns

This guide explains how to add new automated email patterns to the auto-labeling system.

## Quick Reference

**When you discover a new useful email pattern:**

1. **Scan for patterns**: `python3 scan_personal_emails.py`
2. **Analyze patterns**: `python3 identify_useful_patterns.py`
3. **Add to config**: Edit `auto-label-config.yaml`
4. **Test**: `python3 auto_label.py --dry-run`
5. **Deploy**: Run full sync

## Step-by-Step Guide

### 1. Discover New Patterns

Run the personal email scanner to find self-sent emails:

```bash
cd /Users/administrator/Documents/PetesBrain/shared/email-sync
source .venv/bin/activate
python3 scan_personal_emails.py
```

This scans your last 200 sent emails for:
- Client mentions
- Google Sheets links
- Automated report patterns

Results saved to: `data/cache/personal-email-scan-results.json`

### 2. Analyze Patterns

Run the pattern analyzer to identify useful patterns:

```bash
python3 identify_useful_patterns.py
```

This categorizes patterns by value:
- **HIGH VALUE**: Archive to client folders (changes, issues, optimizations)
- **MEDIUM VALUE**: Consider archiving (summaries, context)
- **OPERATIONAL**: Don't archive (daily regenerating reports)

### 3. Add Pattern to Config

Edit `auto-label-config.yaml` and add to the `automated-reports` section:

#### For Client-Specific Patterns

Use `{client}` placeholder and `extract_client: true`:

```yaml
automated-reports:
  your-new-pattern:
    subject_patterns:
      - "Pattern with {client} name"
      - "Another pattern - {client}"
    extract_client: true
    label_template: "client/{client}"
    priority: high  # or medium, low
    notes: "Explain why this is valuable for analysis"
```

#### For Cross-Client Patterns

Use fixed label:

```yaml
automated-reports:
  your-cross-client-pattern:
    subject_patterns:
      - "Pattern without client"
      - "Another cross-client pattern"
    label: "roksys/reports"
    priority: medium
    notes: "Explain what this contains"
```

### 4. Pattern Matching Rules

**Client Name Extraction:**
- `{client}` placeholder will match any client name
- Client names are normalized: "Positive Bakes" → "positive-bakes"
- Case-insensitive matching
- Supports multiple clients from the `clients` section

**Priority Levels:**
- `high`: Critical data (changes, issues, disapprovals)
- `medium`: Useful context (reports, summaries)
- `low`: Background info (briefings, already captured elsewhere)

**Pattern Examples:**

```yaml
# Exact match
subject_patterns:
  - "Daily Briefing -"

# Client placeholder
subject_patterns:
  - "Negatives added for {client} on"
  - "{client} Performance Report"

# Multiple patterns (OR logic)
subject_patterns:
  - "[Script Alert] Issue - {client}"
  - "[MCC Alert] Issue - {client}"
  - "Issue Alert - {client}"
```

### 5. Test Your Pattern

**Dry run** (shows what would happen without making changes):

```bash
python3 auto_label.py --dry-run
```

**Check logs** to see if your pattern is matching correctly:

```bash
tail -f logs/auto-label.log
```

**Expected output:**
```
[2025-11-16 20:00:00] INFO: Processing email: "Negatives added for Smythson on 2025-11-16"
[2025-11-16 20:00:00] INFO: Matched pattern: negative-keywords
[2025-11-16 20:00:00] INFO: Extracted client: smythson
[2025-11-16 20:00:00] INFO: Would apply label: client/smythson
```

### 6. Deploy

Run the full auto-labeling process:

```bash
python3 auto_label.py
```

Then sync emails to folders:

```bash
./sync
```

## Common Patterns to Add

### Script Alerts

```yaml
new-script-alert:
  subject_patterns:
    - "[Script Alert] {alert_type} - {client}"
  extract_client: true
  label_template: "client/{client}"
  priority: high
  notes: "Description of what this alert means"
```

### Performance Reports

```yaml
new-performance-report:
  subject_patterns:
    - "{client} {report_type} Report"
  extract_client: true
  label_template: "client/{client}"
  priority: medium
  notes: "Performance snapshot for analysis"
```

### Budget/Strategy Changes

```yaml
budget-change-alert:
  subject_patterns:
    - "{client} Budget Change -"
    - "💰 {client} Budget Update"
  extract_client: true
  label_template: "client/{client}"
  priority: high
  notes: "Strategic budget adjustments"
```

## Pattern Testing Checklist

Before deploying a new pattern:

- [ ] Ran `identify_useful_patterns.py` to verify pattern exists
- [ ] Added pattern to `auto-label-config.yaml`
- [ ] Verified YAML syntax (no tabs, correct indentation)
- [ ] Ran `auto_label.py --dry-run` to test
- [ ] Checked logs for correct matching
- [ ] Confirmed `extract_client: true` if pattern includes `{client}`
- [ ] Set appropriate priority level
- [ ] Added clear notes explaining value

## Troubleshooting

**Pattern not matching:**
- Check YAML syntax (use spaces, not tabs)
- Verify pattern is case-insensitive match
- Check if client name normalization is working
- Review logs for errors

**Wrong client extracted:**
- Verify client exists in `clients` section of config
- Check client name variations in `keywords` and `company_names`
- Test with `--dry-run` to see what's being extracted

**Too many/few emails matched:**
- Adjust pattern specificity
- Use more specific subject patterns
- Check priority order (high patterns match first)

## Where Patterns Are Used

1. **Auto-labeling**: `auto_label.py` reads patterns and applies Gmail labels
2. **Email sync**: `sync_emails.py` syncs labeled emails to client folders
3. **Pattern analysis**: `identify_useful_patterns.py` discovers new patterns

## File Locations

- **Config**: `shared/email-sync/auto-label-config.yaml`
- **Scanner**: `shared/email-sync/scan_personal_emails.py`
- **Analyzer**: `shared/email-sync/identify_useful_patterns.py`
- **Auto-labeler**: `shared/email-sync/auto_label.py`
- **Logs**: `shared/email-sync/logs/auto-label.log`
- **Results**: `data/cache/personal-email-scan-results.json`

## Examples from Production

Current high-value patterns in production:

1. **Negative Keywords**: Tracks keyword exclusions over time
2. **Product Feed Alerts**: Explains sudden performance drops
3. **Disapproved Ads**: Shows lost impression causes
4. **Budget Optimization**: Strategic decision timeline
5. **Change History**: Complete account change log
6. **Performance Reports**: Historical snapshots with Google Sheets

See `auto-label-config.yaml` for complete examples.
