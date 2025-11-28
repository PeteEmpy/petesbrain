#!/usr/bin/env python3
"""
Copy Google Rep Emails to Knowledge Base

Finds Google rep emails in client folders and copies them to the knowledge base inbox.
This allows them to be:
1. Stored with the client for context
2. Processed into the knowledge base for broader learning

Runs automatically after email sync.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
CLIENTS_ROOT = PROJECT_ROOT / "clients"
KB_INBOX = PROJECT_ROOT / "roksys/knowledge-base/_inbox/emails"
LOG_FILE = PROJECT_ROOT / "data/cache/google-rep-kb-copy.log"

# Google rep email patterns (same as extraction script)
GOOGLE_REP_PATTERN = r'([a-zA-Z0-9._%+-]+@google\.com)'
EXCLUDE_PATTERNS = [
    'noreply',
    'no-reply',
    'calendar-notification',
    'support-appointments-noreply',
    'googleads-noreply',
    'ads-noreply',
    'google-support',
    'notification',
    'automated',
    'donotreply'
]


def log_message(message):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    print(log_entry.strip())

    # Ensure log directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)


def is_google_rep_email(email):
    """Check if email is from a Google rep (not automated)"""
    email = email.lower()

    # Must be @google.com
    if '@google.com' not in email:
        return False

    # Exclude automated addresses
    for pattern in EXCLUDE_PATTERNS:
        if pattern in email:
            return False

    return True


def extract_google_emails(content):
    """Extract all Google email addresses from content"""
    matches = re.findall(GOOGLE_REP_PATTERN, content, re.IGNORECASE)
    return [email for email in matches if is_google_rep_email(email)]


def has_substantial_attachments(file_path):
    """Check if email has substantial attachments (PDFs, PPTX, DOCX, not .ics)"""
    try:
        # Check if attachments directory exists
        email_dir = file_path.parent
        date_str = file_path.stem.split('_')[0]  # Extract date from filename
        attachments_dir = email_dir / 'attachments' / date_str

        if not attachments_dir.exists():
            return False

        # Check for substantial files
        for att_file in attachments_dir.iterdir():
            ext = att_file.suffix.lower()
            if ext in ['.pdf', '.pptx', '.docx', '.xlsx', '.doc', '.ppt']:
                return True

        return False
    except:
        return False


def has_document_links(content):
    """Check if email has Google Doc/Drive/Sheets links"""
    doc_patterns = [
        r'docs\.google\.com/document',
        r'docs\.google\.com/spreadsheets',
        r'docs\.google\.com/presentation',
        r'drive\.google\.com/file',
        r'drive\.google\.com/drive/folders'
    ]

    for pattern in doc_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True

    return False


def has_substantial_content(content):
    """Check if email has substantial content (not just a calendar invite or very short)"""
    # Extract message body
    message_start = content.find('## Message')
    if message_start == -1:
        return False

    message_body = content[message_start:]

    # Remove common calendar boilerplate
    message_body = re.sub(r'Join with Google Meet.*?More phone numbers', '', message_body, flags=re.DOTALL)
    message_body = re.sub(r'Google Calendar.*?wrote:', '', message_body, flags=re.DOTALL)
    message_body = re.sub(r'support-appointments-noreply.*?wrote:', '', message_body, flags=re.DOTALL)

    # Remove HTML tags, extra whitespace
    message_body = re.sub(r'<[^>]+>', '', message_body)
    message_body = re.sub(r'\s+', ' ', message_body).strip()

    # Check length (should be more than 100 characters of actual content)
    if len(message_body) < 100:
        return False

    # Check for keywords that indicate substantial content
    substantial_keywords = [
        'deck', 'slides', 'document', 'attached', 'review',
        'implementation', 'tracking', 'conversion', 'setup',
        'configuration', 'technical', 'performance', 'campaign',
        'enhanced conversions', 'measurement', 'tag', 'pixel',
        'support', 'issue', 'problem', 'help', 'question'
    ]

    content_lower = message_body.lower()
    for keyword in substantial_keywords:
        if keyword in content_lower:
            return True

    # If it's more than 200 characters and doesn't look like just a calendar invite, keep it
    if len(message_body) > 200:
        # Check it's not just OOO or calendar boilerplate
        if not re.search(r'out of office|ooo|away from|on leave', content_lower):
            return True

    return False


def parse_email_markdown(file_path):
    """Parse email markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract From, To, Cc lines
        metadata = {'content': content}

        for line in content.split('\n'):
            if line.startswith('- **From:**'):
                metadata['from'] = line.replace('- **From:**', '').strip()
            elif line.startswith('- **To:**'):
                metadata['to'] = line.replace('- **To:**', '').strip()
            elif line.startswith('- **Cc:**'):
                metadata['cc'] = line.replace('- **Cc:**', '').strip()
            elif line.startswith('- **Date:**'):
                metadata['date'] = line.replace('- **Date:**', '').strip()

        return metadata

    except Exception as e:
        log_message(f"Error parsing {file_path}: {e}")
        return None


def is_google_rep_email_file(file_path):
    """Check if email file involves Google reps"""
    email_data = parse_email_markdown(file_path)
    if not email_data:
        return False

    # Check if from, to, or cc contains Google rep email
    for field in ['from', 'to', 'cc']:
        if field in email_data:
            google_emails = extract_google_emails(email_data[field])
            if google_emails:
                return True

    return False


def copy_email_to_kb_inbox(source_path, client_name):
    """Copy email to knowledge base inbox with client prefix"""
    KB_INBOX.mkdir(parents=True, exist_ok=True)

    # Create destination filename with client prefix
    original_filename = source_path.name
    dest_filename = f"google-rep_{client_name}_{original_filename}"
    dest_path = KB_INBOX / dest_filename

    # Only copy if destination doesn't exist or source is newer
    if dest_path.exists():
        if source_path.stat().st_mtime <= dest_path.stat().st_mtime:
            return False  # Already copied and up to date

    # Copy file
    shutil.copy2(source_path, dest_path)
    return True


def process_client_emails(client_dir, days_back=180):
    """Process emails from a single client (default: last 6 months)"""
    emails_dir = client_dir / "emails"
    if not emails_dir.exists():
        return 0

    client_name = client_dir.name
    cutoff_date = datetime.now() - timedelta(days=days_back)
    copied_count = 0
    skipped_count = 0

    # Check each email file
    for email_file in emails_dir.glob("*.md"):
        # Only process recent emails
        if email_file.stat().st_mtime < cutoff_date.timestamp():
            continue

        # Check if it's a Google rep email
        if not is_google_rep_email_file(email_file):
            continue

        # Parse email to check for substantial content
        email_data = parse_email_markdown(email_file)
        if not email_data:
            continue

        content = email_data['content']

        # Check if email has value (substantial content, attachments, or document links)
        has_attachments = has_substantial_attachments(email_file)
        has_links = has_document_links(content)
        has_content = has_substantial_content(content)

        if has_attachments or has_links or has_content:
            if copy_email_to_kb_inbox(email_file, client_name):
                reasons = []
                if has_attachments:
                    reasons.append("attachments")
                if has_links:
                    reasons.append("doc links")
                if has_content:
                    reasons.append("substantial content")

                log_message(f"  ✓ Copied: {email_file.name} ({', '.join(reasons)})")
                copied_count += 1
        else:
            skipped_count += 1
            log_message(f"  ⊘ Skipped: {email_file.name} (no substantial content/attachments)")

    if skipped_count > 0:
        log_message(f"  Skipped {skipped_count} calendar invites/short emails")

    return copied_count


def main():
    log_message("=" * 60)
    log_message("Google Rep Email → KB Inbox Copy Process")
    log_message("Searching last 6 months for substantial content")
    log_message("=" * 60)

    total_copied = 0

    # Process each client
    for client_dir in CLIENTS_ROOT.iterdir():
        if not client_dir.is_dir():
            continue

        # Skip template directories
        if client_dir.name.startswith('_'):
            continue

        log_message(f"Processing: {client_dir.name}")
        copied = process_client_emails(client_dir, days_back=180)  # 6 months

        if copied > 0:
            total_copied += copied
            log_message(f"  Total copied: {copied} emails with substantial content")

    log_message("=" * 60)
    log_message(f"Complete: {total_copied} Google rep emails copied to KB inbox")
    log_message("=" * 60)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
