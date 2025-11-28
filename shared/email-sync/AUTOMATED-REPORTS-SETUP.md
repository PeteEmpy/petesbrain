# Automated Reports - Email Labeling Setup

**Date Added**: November 16, 2025

## What Was Added

The auto-labeling system has been extended to capture **self-sent automated report emails** from Google Ads scripts. These are emails sent FROM `petere@roksys.co.uk` TO `petere@roksys.co.uk` containing valuable client data.

### New Email Patterns (11 patterns added)

#### HIGH VALUE - Client-Specific (8 patterns)

1. **Negative Keyword Logs** (`negative-keywords`)
   - Pattern: `Negatives added for {client} on YYYY-MM-DD #rokscript`
   - Label: `client/{client}`
   - Value: Historical record of keyword exclusions (explains traffic drops)
   - Found: 33 emails across Positive Bakes, Superspace, Accessories For The Home

2. **Product Feed Alerts** (`product-feed-alerts`)
   - Pattern: `[Script Alert] Best sellers not eligible for Shopping - {client}`
   - Label: `client/{client}`
   - Value: Tracks product disapprovals (explains revenue drops)
   - Found: 28 emails across Go Glean, UNO Lighting

3. **Client Performance Reports** (`client-performance-reports`)
   - Pattern: `{client} Google Ads Performance Report`
   - Label: `client/{client}`
   - Value: Performance snapshots with Google Sheets links
   - Found: Smythson (2 emails)

4. **Client Change History** (`client-change-history`)
   - Pattern: `{client} Google Ads Change History Report`
   - Label: `client/{client}`
   - Value: Complete account change log with Google Sheet
   - Found: Smythson (1 email)

5. **Strategy Dashboards** (`client-strategy-dashboards`)
   - Pattern: `{client} Q4 Dashboard`
   - Label: `client/{client}`
   - Value: Strategic tracking dashboards with Google Sheets
   - Found: Smythson Q4 Dashboard

6. **Budget Optimization** (`budget-optimization`)
   - Pattern: `💡 {client} Budget Optimization - {date}`
   - Label: `client/{client}`
   - Value: Budget strategy recommendations
   - Found: Devonshire (1 email)

#### HIGH VALUE - Cross-Client (2 patterns)

7. **Performance Alerts** (`performance-alerts`)
   - Pattern: `🚨 Performance Alerts - {date}`
   - Label: `roksys/reports`
   - Value: Cross-client performance anomalies
   - Found: 6 emails

8. **Disapproved Ads Report** (`disapproved-ads`)
   - Pattern: `[MCC Alert] Disapproved Ads and Extensions Report`
   - Label: `roksys/reports`
   - Value: Cross-client ad disapproval tracking with Google Sheet
   - Found: 2 emails

#### MEDIUM VALUE - Cross-Client (1 pattern)

9. **PMax Alerts** (`pmax-alerts`)
   - Pattern: `[GAds Script][account name] - PMax Alert - You've got N Non-Converting Search Terms`
   - Label: `roksys/reports`
   - Value: PMax performance issues with Google Sheet
   - Found: 1 email

#### LOW VALUE - Already Captured (2 patterns)

10. **Daily Briefings** (`daily-briefings`)
    - Pattern: `Daily Briefing - {day}, {month} {date}, {year}`
    - Label: `roksys/briefings`
    - Note: Already captured in `briefing/` folder, low priority

11. **Weekly Summaries** (`weekly-summaries`)
    - Pattern: `📅 Weekly Summary & Week Ahead - {dates}`
    - Label: `roksys/briefings`
    - Note: Already captured, low priority

### New Client Entries Added

Added missing clients that appeared in automated reports:

1. `positive-bakes` - Positive Bakes
2. `go-glean` - Go Glean
3. `grain-guard` - Grain Guard
4. `just-bin-bags` - Just Bin Bags
5. `crowd-control` - Crowd Control

## Files Modified

1. **`auto-label-config.yaml`**
   - Added 5 new client entries
   - Added `automated-reports` section with 11 patterns
   - Added 150+ lines of well-documented configuration

2. **`ADDING-NEW-PATTERNS.md`** (NEW)
   - Complete guide for adding new patterns
   - Step-by-step instructions
   - Pattern testing checklist
   - Troubleshooting guide

3. **`AUTOMATED-REPORTS-SETUP.md`** (THIS FILE)
   - Summary of what was added
   - Next steps for implementation

## What Happens Now

### Automatic Behavior

Once the auto-labeling runs, these self-sent emails will be:

1. **Detected** by subject line pattern matching
2. **Client extracted** from subject (e.g., "Positive Bakes" → "positive-bakes")
3. **Labeled** in Gmail (e.g., `client/positive-bakes`)
4. **Synced** to client folders (e.g., `clients/positive-bakes/emails/`)

### Historical Data Captured

You'll now have historical records of:
- When negative keywords were added (and which ones)
- When products became ineligible for Shopping
- Performance alerts and anomalies
- Budget/ROAS strategy changes
- Complete change history logs
- Performance snapshots (with Google Sheet links)

### Analysis Benefits

This data helps explain:
- **Traffic drops**: Check negative keyword logs for exclusions
- **Revenue drops**: Check product feed alerts for disapprovals
- **Lost impressions**: Check disapproved ads report
- **Strategy timeline**: Check budget optimization and change history
- **Performance trends**: Check performance reports and dashboards

## Next Steps

### 1. Test the Configuration (RECOMMENDED)

Run dry-run to see what would be labeled:

```bash
cd /Users/administrator/Documents/PetesBrain/shared/email-sync
source .venv/bin/activate
python3 auto_label.py --dry-run
```

Review output to ensure patterns match correctly.

### 2. Run Auto-Labeling

Apply labels to historical emails:

```bash
python3 auto_label.py
```

This will label up to 100 emails (configurable in settings).

### 3. Sync Emails to Folders

Run email sync to download labeled emails:

```bash
./sync
```

### 4. Verify Results

Check client folders for new automated report emails:

```bash
ls -la clients/positive-bakes/emails/
ls -la clients/smythson/emails/
ls -la clients/go-glean/emails/
```

### 5. Review Google Sheets Links

Some emails contain Google Sheets links. Consider:
- Adding sheet links to client CONTEXT.md "Quick Reference" section
- Downloading CSV snapshots for archival

### 6. Add to Automation (OPTIONAL)

To run auto-labeling automatically:

```bash
# Add to crontab to run daily at 6am
crontab -e

# Add this line:
0 6 * * * cd /Users/administrator/Documents/PetesBrain/shared/email-sync && .venv/bin/python3 auto_label.py >> logs/auto-label.log 2>&1
```

## Future Pattern Additions

When you discover new useful email patterns:

1. Run `scan_personal_emails.py` to find them
2. Run `identify_useful_patterns.py` to analyze value
3. Follow guide in `ADDING-NEW-PATTERNS.md`
4. Test with `--dry-run` before deploying

## Pattern Categories for Future

Watch for these pattern types:

**Client-Specific:**
- Budget change alerts
- ROAS adjustment notifications
- Campaign launch confirmations
- Conversion tracking issues
- Quality score changes
- Bid strategy updates

**Cross-Client:**
- MCC-wide policy changes
- Platform update notifications
- Account access alerts
- Billing notifications
- API quota warnings

**High-Value Indicators:**
- Explains performance changes (drops/spikes)
- Shows strategic decisions timeline
- Contains historical data not available elsewhere
- Includes Google Sheets links with live data
- Tracks issues that affect revenue

## Impact Summary

**Before**: Self-sent automated reports were scattered in inbox, not organized by client

**After**:
- 158 client-relevant emails discovered
- 11 high/medium value patterns identified
- Automatic labeling and filing by client
- Historical data preserved for analysis
- Google Sheets links captured for reference

**Result**: Complete audit trail of automated changes and alerts, organized by client, searchable, and ready for analysis.

## Questions?

See `ADDING-NEW-PATTERNS.md` for detailed guide on extending this system.
