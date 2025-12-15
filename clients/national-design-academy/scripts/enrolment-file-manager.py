#!/usr/bin/env python3
"""
NDA Enrolment File Manager

Monitors emails from pk@nda.ac.uk for enrolment file attachments and automatically:
1. Archives current active versions with datestamp
2. Saves new attachments as active versions
3. Logs all updates

Target files:
- NDA UK Enrolments 25-26.xlsx → NDA-UK-Enrolments-ACTIVE.xlsx
- NDA International Enrolments 25-26.xlsx → NDA-International-Enrolments-ACTIVE.xlsx
"""

import os
import sys
import json
import shutil
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from pathlib import Path

# Configuration
GMAIL_USER = os.environ.get('GMAIL_USER', 'petere@roksys.co.uk')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')
SENDER_EMAIL = 'pk@nda.ac.uk'
CLIENT_DIR = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy')
ENROLMENTS_DIR = CLIENT_DIR / 'enrolments'
HISTORY_DIR = ENROLMENTS_DIR / 'history'
STATE_FILE = ENROLMENTS_DIR / '.processed-emails.json'
LOG_FILE = Path.home() / '.petesbrain-nda-enrolments.log'

# File mapping: attachment filename pattern → active filename
FILE_MAPPINGS = {
    'NDA UK Enrolments': 'NDA-UK-Enrolments-ACTIVE.xlsx',
    'NDA International Enrolments': 'NDA-International-Enrolments-ACTIVE.xlsx'
}

def log(message):
    """Log message to both console and log file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')

def load_processed_emails():
    """Load list of already processed email IDs"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'processed_ids': []}

def save_processed_emails(state):
    """Save list of processed email IDs"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def archive_current_file(active_file, date_str):
    """Archive current active file to history with datestamp"""
    if active_file.exists():
        filename_base = active_file.stem.replace('-ACTIVE', '')
        archived_name = f"{filename_base}-{date_str}.xlsx"
        archived_path = HISTORY_DIR / archived_name

        shutil.copy2(active_file, archived_path)
        log(f"Archived: {active_file.name} → {archived_name}")
        return archived_path
    return None

def save_attachment(attachment_data, filename, email_date):
    """Save attachment as active file and archive old version"""
    # Determine which active file this maps to
    active_filename = None
    for pattern, active_name in FILE_MAPPINGS.items():
        if pattern in filename:
            active_filename = active_name
            break

    if not active_filename:
        log(f"Skipping: {filename} (not a target enrolment file)")
        return False

    active_path = ENROLMENTS_DIR / active_filename
    date_str = email_date.strftime('%Y-%m-%d')

    # Archive current active file if it exists
    if active_path.exists():
        archive_current_file(active_path, date_str)

    # Save new file as active
    with open(active_path, 'wb') as f:
        f.write(attachment_data)

    log(f"Updated: {active_filename} (from email dated {date_str})")
    return True

def decode_filename(filename):
    """Decode email attachment filename"""
    if filename:
        decoded = decode_header(filename)
        if decoded and decoded[0][0]:
            if isinstance(decoded[0][0], bytes):
                return decoded[0][0].decode(decoded[0][1] or 'utf-8')
            return decoded[0][0]
    return filename

def process_email_attachments(msg, email_date, email_id):
    """Process attachments from an email message"""
    updated_files = []

    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        if filename:
            filename = decode_filename(filename)

            # Check if this is one of our target files
            is_target = any(pattern in filename for pattern in FILE_MAPPINGS.keys())

            if is_target and filename.endswith('.xlsx'):
                attachment_data = part.get_payload(decode=True)
                if save_attachment(attachment_data, filename, email_date):
                    updated_files.append(filename)

    return updated_files

def connect_to_gmail():
    """Connect to Gmail via IMAP"""
    if not GMAIL_APP_PASSWORD:
        log("ERROR: GMAIL_APP_PASSWORD environment variable not set")
        sys.exit(1)

    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        return mail
    except Exception as e:
        log(f"ERROR: Failed to connect to Gmail: {e}")
        sys.exit(1)

def process_new_emails():
    """Main function to check for new enrolment emails and process them"""
    log("Starting NDA enrolment file manager...")

    # Ensure directories exist
    ENROLMENTS_DIR.mkdir(exist_ok=True)
    HISTORY_DIR.mkdir(exist_ok=True)

    # Load state
    state = load_processed_emails()
    processed_ids = set(state['processed_ids'])

    # Connect to Gmail
    mail = connect_to_gmail()
    mail.select('inbox')

    # Search for emails from pk@nda.ac.uk
    search_criteria = f'(FROM "{SENDER_EMAIL}")'
    status, messages = mail.search(None, search_criteria)

    if status != 'OK':
        log(f"ERROR: Failed to search emails: {status}")
        mail.close()
        mail.logout()
        return

    email_ids = messages[0].split()
    new_emails_found = 0
    files_updated = 0

    log(f"Found {len(email_ids)} total emails from {SENDER_EMAIL}")

    # Process emails from oldest to newest
    for email_id in email_ids:
        email_id_str = email_id.decode()

        # Skip if already processed
        if email_id_str in processed_ids:
            continue

        new_emails_found += 1

        # Fetch email
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        if status != 'OK':
            log(f"ERROR: Failed to fetch email {email_id_str}")
            continue

        # Parse email
        msg = email.message_from_bytes(msg_data[0][1])

        # Get email date
        date_str = msg.get('Date')
        try:
            email_date = email.utils.parsedate_to_datetime(date_str)
        except:
            email_date = datetime.now()

        subject = decode_header(msg['Subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        log(f"Processing email from {email_date.strftime('%Y-%m-%d')}: {subject}")

        # Process attachments
        updated_files = process_email_attachments(msg, email_date, email_id_str)

        if updated_files:
            files_updated += len(updated_files)
            log(f"Updated {len(updated_files)} file(s) from this email")

        # Mark as processed
        processed_ids.add(email_id_str)

    # Save state
    state['processed_ids'] = list(processed_ids)
    state['last_run'] = datetime.now().isoformat()
    save_processed_emails(state)

    # Cleanup
    mail.close()
    mail.logout()

    log(f"Completed: {new_emails_found} new emails processed, {files_updated} files updated")

if __name__ == '__main__':
    # Ensure directories exist
    ENROLMENTS_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    try:
        process_new_emails()
    except Exception as e:
        log(f"ERROR: Unexpected error: {e}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)
