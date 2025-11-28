#!/usr/bin/env python3
"""
Email Sync for Pete's Brain
Syncs Gmail emails with client labels to local directories as markdown files
"""

import os
import sys
import json
import re
import base64
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from email.utils import parsedate_to_datetime

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Error: Gmail API dependencies not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Gmail API scopes - ONLY gmail.modify needed (includes read access)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify'  # Read, modify, labels, send
]

class EmailSyncer:
    def __init__(self, config_path: str = "config.yaml", auto_label_config_path: str = "auto-label-config.yaml"):
        """Initialize the email syncer with configuration."""
        self.script_dir = Path(__file__).parent
        self.config = self._load_config(config_path)
        self.auto_label_config = self._load_config(auto_label_config_path)
        self.base_dir = Path(self.config['base_dir'])
        self.state_file = self.base_dir / self.config['sync_state_file']
        self.synced_ids = self._load_state()
        self.service = None

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        config_file = self.script_dir / config_path
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def _load_state(self) -> Set[str]:
        """Load previously synced email IDs."""
        if not self.state_file.exists():
            return set()

        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                return set(state.get('synced_ids', []))
        except Exception as e:
            print(f"Warning: Could not load state file: {e}")
            return set()

    def _save_state(self):
        """Save synced email IDs to state file."""
        state = {
            'synced_ids': list(self.synced_ids),
            'last_sync': datetime.now().isoformat()
        }

        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def authenticate(self) -> bool:
        """Authenticate with Gmail API."""
        creds = None
        token_file = self.script_dir / 'token.json'
        credentials_file = self.script_dir / 'credentials.json'

        # Check for existing token
        if token_file.exists():
            creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

            # Check if token has the required scopes
            if creds and creds.scopes:
                required_scopes = set(SCOPES)
                current_scopes = set(creds.scopes)
                if not required_scopes.issubset(current_scopes):
                    print(f"⚠️  Token missing required scopes. Required: {required_scopes}, Current: {current_scopes}")
                    print("🔄 Deleting old token and re-authenticating...")
                    token_file.unlink()
                    creds = None

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not credentials_file.exists():
                    print("Error: credentials.json not found!")
                    print("Please follow setup instructions in README.md")
                    return False

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_file), SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)
        return True

    def _slugify(self, text: str, max_length: int = 50) -> str:
        """Convert text to filesystem-safe slug."""
        # Remove special characters
        text = re.sub(r'[^\w\s-]', '', text.lower())
        # Replace spaces and multiple dashes
        text = re.sub(r'[-\s]+', '-', text)
        # Trim and remove leading/trailing dashes
        text = text.strip('-')[:max_length]
        return text or 'email'

    def _decode_body(self, part: Dict) -> str:
        """Decode email body from base64."""
        if 'data' in part['body']:
            data = part['body']['data']
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        return ''

    def _get_email_body(self, payload: Dict) -> tuple[str, str]:
        """Extract plain text and HTML body from email payload."""
        plain_text = ''
        html_text = ''

        if 'parts' in payload:
            for part in payload['parts']:
                mime_type = part.get('mimeType', '')

                if mime_type == 'text/plain':
                    plain_text += self._decode_body(part)
                elif mime_type == 'text/html':
                    html_text += self._decode_body(part)
                elif 'parts' in part:  # Nested parts
                    pt, ht = self._get_email_body(part)
                    plain_text += pt
                    html_text += ht
        else:
            # Single part message
            mime_type = payload.get('mimeType', '')
            if mime_type == 'text/plain':
                plain_text = self._decode_body(payload)
            elif mime_type == 'text/html':
                html_text = self._decode_body(payload)

        return plain_text, html_text

    def _convert_html_to_text(self, html: str) -> str:
        """Basic HTML to text conversion."""
        # Remove script and style tags
        html = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        # Decode HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&quot;', '"')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    def _format_email_as_markdown(self, message: Dict, client_folder: str = None,
                                  email_date: datetime = None) -> str:
        """Convert email message to markdown format."""
        payload = message.get('payload', {})
        headers = {h['name']: h['value'] for h in payload.get('headers', [])}

        # Extract email details
        from_addr = headers.get('From', 'Unknown')
        to_addr = headers.get('To', 'Unknown')
        cc_addr = headers.get('Cc', '')
        subject = headers.get('Subject', 'No Subject')
        date_str = headers.get('Date', '')

        # Parse date
        try:
            email_date = parsedate_to_datetime(date_str)
            formatted_date = email_date.strftime('%Y-%m-%d %H:%M:%S')
        except:
            formatted_date = date_str

        # Get email body
        plain_text, html_text = self._get_email_body(payload)

        # Use plain text if available, otherwise convert HTML
        body = plain_text if plain_text else self._convert_html_to_text(html_text)

        # Build markdown
        md_lines = [
            f"# {subject}",
            "",
            "## Email Details",
            "",
            f"- **From:** {from_addr}",
            f"- **To:** {to_addr}",
        ]

        if cc_addr:
            md_lines.append(f"- **Cc:** {cc_addr}")

        md_lines.extend([
            f"- **Date:** {formatted_date}",
            f"- **Gmail ID:** {message['id']}",
            "",
            "---",
            "",
            "## Message",
            "",
            body,
            ""
        ])

        # Check for attachments
        if 'parts' in payload:
            attachments = [
                p for p in payload['parts']
                if p.get('filename') and p.get('body', {}).get('attachmentId')
            ]

            if attachments and client_folder and email_date:
                md_lines.extend([
                    "",
                    "---",
                    "",
                    "## Attachments",
                    ""
                ])

                # Determine save directory
                date_str = email_date.strftime(self.config['sync']['date_format'])
                # Handle paths with slashes (e.g., "roksys/news")
                if '/' in client_folder:
                    save_dir = self.base_dir / client_folder / 'emails' / 'attachments' / date_str
                elif client_folder in ['roksys', 'personal']:
                    save_dir = self.base_dir / client_folder / 'emails' / 'attachments' / date_str
                else:
                    save_dir = self.base_dir / 'clients' / client_folder / 'emails' / 'attachments' / date_str

                for att in attachments:
                    filename = att['filename']
                    size = att.get('body', {}).get('size', 0)
                    attachment_id = att.get('body', {}).get('attachmentId')

                    # Download attachment
                    saved_path = self._download_attachment(
                        message['id'],
                        attachment_id,
                        filename,
                        save_dir
                    )

                    if saved_path:
                        # Link to local file
                        rel_path = f"attachments/{date_str}/{filename}"
                        size_kb = size / 1024 if size > 1024 else size
                        size_unit = "KB" if size > 1024 else "bytes"
                        md_lines.append(f"- [{filename}]({rel_path}) ({size_kb:.1f} {size_unit})")
                    else:
                        # Fallback if download failed
                        md_lines.append(f"- **{filename}** ({size} bytes) - Download failed")
            elif attachments:
                # Just list metadata if we don't have folder info
                md_lines.extend([
                    "",
                    "---",
                    "",
                    "## Attachments",
                    ""
                ])
                for att in attachments:
                    filename = att['filename']
                    size = att.get('body', {}).get('size', 0)
                    md_lines.append(f"- **{filename}** ({size} bytes)")

        return '\n'.join(md_lines)

    def _download_attachment(self, msg_id: str, attachment_id: str, filename: str,
                            save_dir: Path) -> Optional[Path]:
        """Download an attachment from Gmail and save it to disk."""
        try:
            # Get attachment data
            attachment = self.service.users().messages().attachments().get(
                userId='me',
                messageId=msg_id,
                id=attachment_id
            ).execute()

            # Decode attachment data
            data = attachment['data']
            file_data = base64.urlsafe_b64decode(data)

            # Save to disk
            save_dir.mkdir(parents=True, exist_ok=True)
            file_path = save_dir / filename

            with open(file_path, 'wb') as f:
                f.write(file_data)

            return file_path

        except Exception as e:
            print(f"    ⚠️  Failed to download attachment {filename}: {e}")
            return None

    def _save_email(self, email_md: str, client_folder: str, subject: str, date: datetime) -> bool:
        """Save email markdown to client folder."""
        # Create filename
        date_str = date.strftime(self.config['sync']['date_format'])
        subject_slug = self._slugify(subject)
        filename = f"{date_str}_{subject_slug}.md"

        # Create full path
        # Handle paths with slashes (e.g., "roksys/news")
        if '/' in client_folder:
            client_dir = self.base_dir / client_folder / 'emails'
        # Handle special folders (roksys, personal)
        elif client_folder in ['roksys', 'personal']:
            client_dir = self.base_dir / client_folder / 'emails'
        else:
            client_dir = self.base_dir / 'clients' / client_folder / 'emails'

        # Ensure directory exists
        client_dir.mkdir(parents=True, exist_ok=True)

        # Handle duplicate filenames
        file_path = client_dir / filename
        counter = 1
        while file_path.exists():
            filename = f"{date_str}_{subject_slug}_{counter}.md"
            file_path = client_dir / filename
            counter += 1

        # Write file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(email_md)
            return True
        except Exception as e:
            print(f"Error saving email to {file_path}: {e}")
            return False

    def _get_client_search_terms(self, client_key: str) -> List[str]:
        """Get search terms (domains and emails) for a client."""
        client_config = self.auto_label_config['clients'].get(client_key, {})
        search_terms = []

        # Add domain searches
        for domain in client_config.get('domains', []):
            search_terms.append(f"to:@{domain}")

        # Add specific email searches
        for email in client_config.get('emails', []):
            search_terms.append(f"to:{email}")

        return search_terms

    def sync_sent_emails(self, dry_run: bool = False) -> Dict[str, int]:
        """Sync sent emails to clients."""
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        # Check if sent email sync is enabled
        if not self.config['sync'].get('sync_sent_emails', False):
            return {'total_processed': 0, 'newly_synced': 0, 'already_synced': 0, 'errors': 0}

        stats = {
            'total_processed': 0,
            'newly_synced': 0,
            'already_synced': 0,
            'errors': 0
        }

        print("\n📤 Syncing sent emails...")

        # Process each client
        for gmail_label, client_folder in self.config['client_labels'].items():
            client_key = client_folder  # e.g., "clear-prospects"

            # Get search terms for this client
            search_terms = self._get_client_search_terms(client_key)

            if not search_terms:
                continue

            # Build Gmail query: sent emails to this client
            search_query = " OR ".join(search_terms)
            query = f"in:sent ({search_query})"

            try:
                results = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    maxResults=self.config['sync']['max_emails_per_run']
                ).execute()

                messages = results.get('messages', [])

                if messages:
                    print(f"\n  {client_folder}: Found {len(messages)} sent emails")

                for msg_ref in messages:
                    msg_id = msg_ref['id']
                    stats['total_processed'] += 1

                    # Skip if already synced
                    if msg_id in self.synced_ids:
                        stats['already_synced'] += 1
                        continue

                    # Fetch full message
                    try:
                        message = self.service.users().messages().get(
                            userId='me',
                            id=msg_id,
                            format='full'
                        ).execute()

                        # Extract subject and date
                        headers = {h['name']: h['value'] for h in message['payload']['headers']}
                        subject = headers.get('Subject', 'No Subject')
                        date_str = headers.get('Date', '')

                        try:
                            email_date = parsedate_to_datetime(date_str)
                        except:
                            email_date = datetime.now()

                        print(f"    ✓ [SENT] {subject[:45]}... ({email_date.strftime('%Y-%m-%d')})")

                        if not dry_run:
                            # Convert to markdown with attachments
                            email_md = self._format_email_as_markdown(
                                message,
                                client_folder=client_folder,
                                email_date=email_date
                            )

                            # Add a note that this is a sent email
                            email_md = email_md.replace(
                                "## Message",
                                "**📤 Sent Email**\n\n---\n\n## Message"
                            )

                            # Save to client folder
                            if self._save_email(email_md, client_folder, f"[SENT] {subject}", email_date):
                                self.synced_ids.add(msg_id)
                                stats['newly_synced'] += 1
                            else:
                                stats['errors'] += 1
                        else:
                            stats['newly_synced'] += 1

                    except Exception as e:
                        print(f"    ✗ Error processing sent message {msg_id}: {e}")
                        stats['errors'] += 1

            except Exception as e:
                print(f"  ✗ Error querying sent emails for {client_folder}: {e}")
                stats['errors'] += 1

        return stats

    def sync_emails(self, dry_run: bool = False) -> Dict[str, int]:
        """Sync emails from Gmail to local folders."""
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        stats = {
            'total_processed': 0,
            'newly_synced': 0,
            'already_synced': 0,
            'errors': 0
        }

        # Process each client label
        for gmail_label, client_folder in self.config['client_labels'].items():
            print(f"\nProcessing label: {gmail_label} → {client_folder}")

            try:
                # Search for emails with this label
                query = f"label:{gmail_label}"
                results = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    maxResults=self.config['sync']['max_emails_per_run']
                ).execute()

                messages = results.get('messages', [])

                if not messages:
                    print(f"  No emails found")
                    continue

                print(f"  Found {len(messages)} emails")

                for msg_ref in messages:
                    msg_id = msg_ref['id']
                    stats['total_processed'] += 1

                    # Skip if already synced
                    if msg_id in self.synced_ids:
                        stats['already_synced'] += 1
                        continue

                    # Fetch full message
                    try:
                        message = self.service.users().messages().get(
                            userId='me',
                            id=msg_id,
                            format='full'
                        ).execute()

                        # Extract subject and date
                        headers = {h['name']: h['value'] for h in message['payload']['headers']}
                        subject = headers.get('Subject', 'No Subject')
                        date_str = headers.get('Date', '')

                        try:
                            email_date = parsedate_to_datetime(date_str)
                        except:
                            email_date = datetime.now()

                        print(f"  ✓ {subject[:50]}... ({email_date.strftime('%Y-%m-%d')})")

                        if not dry_run:
                            # Convert to markdown with attachments
                            email_md = self._format_email_as_markdown(
                                message,
                                client_folder=client_folder,
                                email_date=email_date
                            )

                            # Save to client folder
                            if self._save_email(email_md, client_folder, subject, email_date):
                                self.synced_ids.add(msg_id)
                                stats['newly_synced'] += 1
                            else:
                                stats['errors'] += 1
                        else:
                            stats['newly_synced'] += 1

                    except Exception as e:
                        print(f"  ✗ Error processing message {msg_id}: {e}")
                        stats['errors'] += 1

            except Exception as e:
                print(f"  ✗ Error querying label {gmail_label}: {e}")
                stats['errors'] += 1

        # Sync sent emails
        sent_stats = self.sync_sent_emails(dry_run)
        stats['total_processed'] += sent_stats['total_processed']
        stats['newly_synced'] += sent_stats['newly_synced']
        stats['already_synced'] += sent_stats['already_synced']
        stats['errors'] += sent_stats['errors']

        # Save state
        if not dry_run:
            self._save_state()

        return stats


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Sync Gmail emails to Pete\'s Brain')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be synced without actually syncing')
    parser.add_argument('--config', default='config.yaml',
                       help='Path to config file (default: config.yaml)')

    args = parser.parse_args()

    print("=" * 60)
    print("Pete's Brain - Email Sync")
    print("=" * 60)

    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No files will be saved\n")

    try:
        # Initialize syncer
        syncer = EmailSyncer(args.config)

        # Authenticate
        print("\n📧 Authenticating with Gmail...")
        if not syncer.authenticate():
            sys.exit(1)
        print("✓ Authentication successful\n")

        # Sync emails
        print("🔄 Starting email sync...\n")
        stats = syncer.sync_emails(dry_run=args.dry_run)

        # Print summary
        print("\n" + "=" * 60)
        print("Sync Complete!")
        print("=" * 60)
        print(f"Total emails processed: {stats['total_processed']}")
        print(f"Newly synced: {stats['newly_synced']}")
        print(f"Already synced: {stats['already_synced']}")
        print(f"Errors: {stats['errors']}")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n❌ Sync cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
