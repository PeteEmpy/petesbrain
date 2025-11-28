# Google Ads Feature Email Processor

**Status:** ✅ Active  
**Last Updated:** 2025-11-11

## Overview

Automatically processes Google Ads feature announcement emails by:
1. Detecting emails from Google about new features
2. Deduplicating using content hashing
3. Extracting links from email body
4. Fetching content from linked pages
5. Processing with Claude API to extract specifications
6. Saving to Google Specifications KB

## How It Works

### 1. Email Detection

The auto-labeler (`shared/email-sync/auto_label.py`) automatically labels emails from Google that match:
- **Domains**: `google.com`
- **Keywords**: "new feature", "now available", "announcing", "introducing", "Google Ads update", etc.
- **Excludes**: Emails with "personal", "account manager", "consultation", "meeting", "appointment"

These emails get the `google-ads-features` label in Gmail.

### 2. Processing Flow

```
Google Ads Feature Email Arrives
    ↓
Auto-Labeler (runs periodically)
    - Labels as "google-ads-features"
    ↓
Feature Email Processor (every 2 hours)
    - Fetches emails with label
    - Deduplicates using content hash
    - Extracts links from email
    - Fetches content from links
    - Processes with Claude API
    - Saves to specifications KB
```

### 3. Deduplication

- Uses SHA-256 hash of subject + first 500 chars of body
- Tracks processed hashes in `shared/data/google-ads-feature-emails-processed.json`
- Skips emails with identical or near-identical content

### 4. Link Extraction & Fetching

- Extracts URLs from HTML and plain text email body
- Filters to Google domains only:
  - `google.com`
  - `developers.google.com`
  - `support.google.com`
  - `blog.google.com`
- Fetches content from each link (up to 10 concurrent)
- Parses HTML and extracts text content

### 5. Specification Extraction

- Batches 6 emails per Claude API call for efficiency
- Extracts:
  - New features announced
  - Specifications (character limits, requirements)
  - Best practices
  - Categories and subcategories
- Saves as JSON specifications and Markdown best practices

## Files Created

**Agent Script:**
- `agents/google-ads-feature-email-processor/google-ads-feature-email-processor.py`

**LaunchAgent:**
- `agents/launchagents/com.petesbrain.google-ads-feature-email-processor.plist`
- Runs every 2 hours (7200 seconds)

**State Files:**
- `shared/data/google-ads-feature-emails-processed.json` - Tracks processed emails
- `shared/data/google-ads-feature-email-processor.log` - Processing logs

**Configuration:**
- Updated `shared/email-sync/auto-label-config.yaml` - Added `google-ads-features` detection rules

## Setup

### 1. Run Auto-Labeler

First, run the auto-labeler to create the `google-ads-features` label and label existing emails:

```bash
cd shared/email-sync
python3 auto_label.py
```

This will:
- Create the `google-ads-features` label in Gmail
- Label matching emails from the last 365 days

### 2. Load LaunchAgent

```bash
launchctl load ~/Library/LaunchAgents/com.petesbrain.google-ads-feature-email-processor.plist
```

Or copy the plist file:
```bash
cp agents/launchagents/com.petesbrain.google-ads-feature-email-processor.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.petesbrain.google-ads-feature-email-processor.plist
```

### 3. Test Manually

```bash
cd /Users/administrator/Documents/PetesBrain
export ANTHROPIC_API_KEY="your-key-here"
python3 agents/google-ads-feature-email-processor/google-ads-feature-email-processor.py
```

## Output

Specifications are saved to:
- `google-specifications/google-ads/specifications/platform-updates/` (or other subcategories)
- `google-specifications/google-ads/best-practices/platform-updates/`

Each specification includes source metadata:
```json
{
  "type": "google_feature_email",
  "source": "Email subject",
  "date": "2025-11-11",
  "email_id": "Gmail message ID",
  "verified": true
}
```

## Monitoring

Check logs:
```bash
tail -f ~/.petesbrain-google-ads-feature-email.log
tail -f ~/.petesbrain-google-ads-feature-email-error.log
```

Check processed emails:
```bash
cat shared/data/google-ads-feature-emails-processed.json
```

## Troubleshooting

**No emails being processed:**
1. Check if auto-labeler has run and created the label
2. Verify emails match the detection criteria
3. Check Gmail API authentication

**Duplicates still being processed:**
- Check `shared/data/google-ads-feature-emails-processed.json` exists
- Verify hashing logic is working correctly

**Links not being fetched:**
- Check internet connectivity
- Verify URLs are valid Google domains
- Check for rate limiting

## Related Systems

- **Google Specs Processor**: Processes manual inputs from Google rep emails
- **Google Specs Monitor**: Weekly checks of Google documentation
- **Auto-Labeler**: Labels emails automatically

---

**Last Updated**: 2025-11-11  
**Maintained By**: Peter Empson, ROK Systems

