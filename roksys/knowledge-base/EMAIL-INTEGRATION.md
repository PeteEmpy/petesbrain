# Email Integration with Knowledge Base Inbox

This guide explains how to automatically route emails from trusted sources (Google Ads updates, industry newsletters, etc.) into the knowledge base inbox for automatic processing.

## Overview

The email sync system can automatically:
1. Label emails from trusted knowledge sources
2. Export labeled emails to the knowledge base inbox
3. Let the inbox processor organize them into the knowledge base

## Setup

### Step 1: Add Knowledge Base Labels to Email Sync

Edit `/Users/administrator/Documents/PetesBrain/shared/email-sync/auto-label-config.yaml`

Add a new section for knowledge base sources:

```yaml
  knowledge-base-google-ads:
    label: "knowledge-base/google-ads"
    domains:
      - "googleadservices.com"
      - "google.com"
      - "ads-noreply@google.com"
    emails:
      - "googleads-noreply@google.com"
      - "ads-noreply@google.com"
    keywords:
      - "Google Ads Update"
      - "Performance Max"
      - "Smart Bidding"
      - "Google Ads News"
      - "New in Google Ads"
    company_names:
      - "Google Ads"
      - "Google Marketing Platform"

  knowledge-base-industry:
    label: "knowledge-base/industry"
    domains:
      - "searchengineland.com"
      - "marketingland.com"
      - "wordstream.com"
      - "ppchero.com"
      - "thesempost.com"
    emails: []
    keywords:
      - "PPC news"
      - "Paid search update"
      - "Digital marketing"
      - "Performance marketing"
    company_names:
      - "Search Engine Land"
      - "Marketing Land"
      - "WordStream"
      - "PPC Hero"

  knowledge-base-ai:
    label: "knowledge-base/ai"
    domains:
      - "deepview.ai"
      - "thedeepview.ai"
      - "openai.com"
      - "anthropic.com"
    emails: []
    keywords:
      - "AI in advertising"
      - "AI in marketing"
      - "Machine learning"
      - "Automation"
    company_names:
      - "OpenAI"
      - "Anthropic"
      - "Deep View"
```

### Step 2: Create Email Export Script

Create a script that exports labeled emails to the inbox:

**File**: `/Users/administrator/Documents/PetesBrain/shared/scripts/export-kb-emails.py`

```python
#!/usr/bin/env python3
"""
Export knowledge base emails from Gmail to inbox
Runs after auto-labeling to move KB emails to processing inbox
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import re

PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
KB_INBOX = PROJECT_ROOT / "roksys/knowledge-base/_inbox/emails"
TOKEN_FILE = PROJECT_ROOT / "shared/email-sync/token.json"

# Gmail API setup
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Get authenticated Gmail service"""
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No valid credentials. Run email sync first.")

    return build('gmail', 'v1', credentials=creds)

def export_email(service, msg_id):
    """Export email to markdown in inbox"""
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

    # Extract headers
    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
    subject = headers.get('Subject', 'No Subject')
    from_email = headers.get('From', 'Unknown')
    date = headers.get('Date', '')

    # Get body
    body = ""
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
    elif 'body' in msg['payload']:
        body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')

    # Create filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_subject = re.sub(r'[^a-z0-9]+', '-', subject.lower())[:50]
    filename = f"{date_str}-{safe_subject}.md"

    # Create markdown content
    content = f"""---
from: {from_email}
subject: {subject}
date: {date}
gmail_id: {msg_id}
---

# {subject}

**From**: {from_email}
**Date**: {date}

## Content

{body}
"""

    # Write to inbox
    filepath = KB_INBOX / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Exported: {filename}")
    return True

def main():
    """Export all knowledge base labeled emails"""
    service = get_gmail_service()

    # Query for knowledge base labels
    labels = ['knowledge-base/google-ads', 'knowledge-base/industry', 'knowledge-base/ai']

    for label_name in labels:
        # Get label ID
        labels_list = service.users().labels().list(userId='me').execute()
        label_id = None
        for label in labels_list.get('labels', []):
            if label['name'] == label_name:
                label_id = label['id']
                break

        if not label_id:
            continue

        # Get messages with this label
        results = service.users().messages().list(
            userId='me',
            labelIds=[label_id],
            maxResults=10  # Process last 10 from each category
        ).execute()

        messages = results.get('messages', [])
        print(f"Found {len(messages)} emails with label: {label_name}")

        for msg in messages:
            export_email(service, msg['id'])

if __name__ == "__main__":
    main()
```

### Step 3: Update Email Sync Workflow

Modify the email sync cron/LaunchAgent to run both scripts:

```bash
#!/bin/bash
# Email sync workflow with knowledge base export

cd /Users/administrator/Documents/PetesBrain/shared/email-sync

# Step 1: Sync emails
./sync-all

# Step 2: Auto-label emails
python3 auto_label.py

# Step 3: Export knowledge base emails
python3 ../scripts/export-kb-emails.py
```

## Manual Export

To manually export knowledge base emails:

```bash
cd /Users/administrator/Documents/PetesBrain
python3 shared/scripts/export-kb-emails.py
```

## Workflow Summary

1. **Email arrives** from Google, industry source, etc.
2. **Auto-labeler** applies `knowledge-base/*` label
3. **Export script** moves email to `_inbox/emails/`
4. **Inbox processor** (every 6 hours):
   - Reads email content
   - Analyzes with Claude API
   - Categorizes by topic
   - Creates formatted KB document
   - Moves to appropriate category folder
   - Clears from inbox

## Testing

1. Forward a Google Ads email to yourself
2. Run auto-labeler: `cd shared/email-sync && python3 auto_label.py`
3. Check if it got labeled: Look for `knowledge-base/google-ads` label
4. Export to inbox: `python3 shared/scripts/export-kb-emails.py`
5. Check inbox: `ls roksys/knowledge-base/_inbox/emails/`
6. Test processor: `python3 shared/scripts/knowledge-base-processor.py`
7. Verify organized: Check `roksys/knowledge-base/google-ads/` folders

## Trusted Sources to Add

Consider adding these sources to auto-label-config.yaml:

**Google Ads Official**
- googleads-noreply@google.com
- google-ads-developers@google.com

**Industry Publications**
- Search Engine Land
- Search Engine Journal
- Marketing Land
- WordStream
- PPC Hero
- The SEM Post

**AI & Tech**
- OpenAI newsletters
- Anthropic updates
- Google AI Blog
- DeepMind
- The Deep View

**Analytics & Tracking**
- Google Analytics updates
- Google Tag Manager news

## Maintenance

- Review `~/.petesbrain-knowledge-base.log` for processing status
- Check `shared/data/kb-processing.log` for detailed activity
- Periodically review knowledge base index for organization
- Update auto-label rules as new sources are discovered

---

**Setup Complete!** Emails will now automatically flow into your knowledge base.
