#!/usr/bin/env python3
"""
Extract Google Rep Documents

Scans client emails from the last 12 months to find:
1. Emails from Google reps (@google.com, excluding automated addresses)
2. Attachments in those emails
3. Links to Google Docs, Sheets, Slides, Drive files
4. Downloads/extracts them to knowledge base inbox

Also creates a report of all Google rep emails found for review.
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
CLIENTS_ROOT = PROJECT_ROOT / "clients"
KB_INBOX = PROJECT_ROOT / "roksys/knowledge-base/_inbox/documents"
REPORT_FILE = PROJECT_ROOT / "roksys/google-rep-emails-report.md"

# Google rep email patterns
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

# Document link patterns
DOC_LINK_PATTERNS = [
    r'https://docs\.google\.com/document/d/([a-zA-Z0-9_-]+)',
    r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)',
    r'https://docs\.google\.com/presentation/d/([a-zA-Z0-9_-]+)',
    r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
    r'https://drive\.google\.com/drive/folders/([a-zA-Z0-9_-]+)',
]


def log_message(message):
    """Log message to console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


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


def extract_document_links(content):
    """Extract Google Doc/Drive links from content"""
    links = []

    for pattern in DOC_LINK_PATTERNS:
        matches = re.findall(pattern, content)
        for match in matches:
            # Reconstruct full URL
            if 'document' in pattern:
                links.append(('Google Doc', f'https://docs.google.com/document/d/{match}'))
            elif 'spreadsheets' in pattern:
                links.append(('Google Sheet', f'https://docs.google.com/spreadsheets/d/{match}'))
            elif 'presentation' in pattern:
                links.append(('Google Slides', f'https://docs.google.com/presentation/d/{match}'))
            elif 'file' in pattern:
                links.append(('Google Drive File', f'https://drive.google.com/file/d/{match}'))
            elif 'folders' in pattern:
                links.append(('Google Drive Folder', f'https://drive.google.com/drive/folders/{match}'))

    return links


def parse_email_markdown(file_path):
    """Parse email markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata
        metadata = {}
        lines = content.split('\n')

        for line in lines:
            if line.startswith('- **From:**'):
                metadata['from'] = line.replace('- **From:**', '').strip()
            elif line.startswith('- **To:**'):
                metadata['to'] = line.replace('- **To:**', '').strip()
            elif line.startswith('- **Cc:**'):
                metadata['cc'] = line.replace('- **Cc:**', '').strip()
            elif line.startswith('- **Date:**'):
                metadata['date'] = line.replace('- **Date:**', '').strip()
            elif line.startswith('- **Subject:**'):
                metadata['subject'] = line.replace('- **Subject:**', '').strip()

        metadata['content'] = content
        metadata['file_path'] = str(file_path)

        return metadata

    except Exception as e:
        log_message(f"Error parsing {file_path}: {e}")
        return None


def find_google_rep_emails(days=365):
    """Find all emails from Google reps in the last N days"""
    log_message(f"Scanning for Google rep emails from last {days} days...")

    cutoff_date = datetime.now() - timedelta(days=days)
    google_rep_emails = []

    # Scan all client email folders
    for client_dir in CLIENTS_ROOT.iterdir():
        if not client_dir.is_dir():
            continue

        emails_dir = client_dir / "emails"
        if not emails_dir.exists():
            continue

        for email_file in emails_dir.glob("*.md"):
            # Check file age
            if email_file.stat().st_mtime < cutoff_date.timestamp():
                continue

            # Parse email
            email_data = parse_email_markdown(email_file)
            if not email_data:
                continue

            # Check if from, to, or cc contains Google rep email
            google_emails = []

            for field in ['from', 'to', 'cc']:
                if field in email_data:
                    found_emails = extract_google_emails(email_data[field])
                    google_emails.extend(found_emails)

            if google_emails:
                # Extract document links
                doc_links = extract_document_links(email_data['content'])

                email_data['google_reps'] = list(set(google_emails))
                email_data['document_links'] = doc_links
                email_data['client'] = client_dir.name

                google_rep_emails.append(email_data)

    log_message(f"✓ Found {len(google_rep_emails)} emails involving Google reps")
    return google_rep_emails


def create_report(emails):
    """Create markdown report of Google rep emails"""
    log_message("Creating report...")

    report_lines = [
        "# Google Rep Emails Report",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Period**: Last 12 months",
        f"**Total Emails Found**: {len(emails)}",
        "",
        "---",
        "",
    ]

    # Group by client
    by_client = {}
    for email in emails:
        client = email['client']
        if client not in by_client:
            by_client[client] = []
        by_client[client].append(email)

    # Generate report
    for client, client_emails in sorted(by_client.items()):
        report_lines.append(f"## {client.replace('-', ' ').title()}")
        report_lines.append(f"")
        report_lines.append(f"**Total emails**: {len(client_emails)}")
        report_lines.append("")

        for email in sorted(client_emails, key=lambda x: x.get('date', ''), reverse=True):
            date = email.get('date', 'Unknown')[:10]  # Just the date part
            subject = email.get('subject', email['file_path'].split('/')[-1])
            google_reps = ', '.join(email['google_reps'])

            report_lines.append(f"### {subject}")
            report_lines.append(f"- **Date**: {date}")
            report_lines.append(f"- **Google Reps**: {google_reps}")
            report_lines.append(f"- **File**: `{email['file_path']}`")

            if email['document_links']:
                report_lines.append(f"- **Documents Found**: {len(email['document_links'])}")
                for doc_type, doc_link in email['document_links']:
                    report_lines.append(f"  - [{doc_type}]({doc_link})")
            else:
                report_lines.append(f"- **Documents Found**: None")

            report_lines.append("")

        report_lines.append("---")
        report_lines.append("")

    # Write report
    with open(REPORT_FILE, 'w') as f:
        f.write('\n'.join(report_lines))

    log_message(f"✓ Report saved: {REPORT_FILE}")


def create_inbox_entries(emails):
    """Create inbox entries for documents to be processed"""
    log_message("Creating inbox entries for documents...")

    KB_INBOX.mkdir(parents=True, exist_ok=True)

    created_count = 0

    for email in emails:
        if not email['document_links']:
            continue

        # Create a text file with all document links from this email
        date = email.get('date', 'Unknown')[:10]
        client = email['client']
        doc_id = email['file_path'].split('/')[-1].replace('.md', '')

        filename = f"{date}_google-rep_{client}_{doc_id}.txt"
        filepath = KB_INBOX / filename

        # Build content
        content_lines = [
            f"# Google Rep Documents",
            f"",
            f"**Client**: {client}",
            f"**Date**: {date}",
            f"**Google Reps**: {', '.join(email['google_reps'])}",
            f"**Subject**: {email.get('subject', 'N/A')}",
            f"",
            f"## Documents",
            f""
        ]

        for doc_type, doc_link in email['document_links']:
            content_lines.append(f"### {doc_type}")
            content_lines.append(f"{doc_link}")
            content_lines.append(f"")

        with open(filepath, 'w') as f:
            f.write('\n'.join(content_lines))

        created_count += 1

    log_message(f"✓ Created {created_count} inbox entries for processing")


def main():
    log_message("=" * 60)
    log_message("Google Rep Document Extraction")
    log_message("=" * 60)

    # Find Google rep emails
    emails = find_google_rep_emails(days=365)

    if not emails:
        log_message("No Google rep emails found.")
        return 0

    # Create report
    create_report(emails)

    # Create inbox entries
    create_inbox_entries(emails)

    log_message("=" * 60)
    log_message("Processing Complete")
    log_message("=" * 60)
    log_message("")
    log_message(f"📊 Report: {REPORT_FILE}")
    log_message(f"📥 Inbox: {KB_INBOX}")
    log_message("")
    log_message("Next steps:")
    log_message("1. Review the report to see all Google rep emails found")
    log_message("2. Document links have been added to knowledge base inbox")
    log_message("3. Knowledge base processor will categorize them automatically")

    return 0


if __name__ == '__main__':
    sys.exit(main())
