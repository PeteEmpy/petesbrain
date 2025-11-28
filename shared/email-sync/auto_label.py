#!/usr/bin/env python3
"""
Auto-Labeling for Pete's Brain Email Sync
Automatically labels incoming emails with appropriate client labels
"""

import os
import sys
import yaml
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from email.utils import parseaddr

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

class AutoLabeler:
    def __init__(self, config_path: str = "auto-label-config.yaml"):
        """Initialize the auto-labeler with configuration."""
        self.script_dir = Path(__file__).parent
        self.config = self._load_config(config_path)
        self.service = None
        self.label_cache = {}  # Cache Gmail label IDs

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        config_file = self.script_dir / config_path
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def authenticate(self) -> bool:
        """Authenticate with Gmail API using existing token."""
        token_file = self.script_dir / 'token.json'
        credentials_file = self.script_dir / 'credentials.json'

        if not token_file.exists():
            print("Error: token.json not found!")
            print("Please run sync_emails.py first to authenticate.")
            return False

        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

        # Check if token has the required scopes
        if creds and creds.scopes:
            required_scopes = set(SCOPES)
            current_scopes = set(creds.scopes)
            if not required_scopes.issubset(current_scopes):
                print(f"⚠️  Token missing required scopes!")
                print(f"   Required: {required_scopes}")
                print(f"   Current: {current_scopes}")
                print("🔄 Please delete token.json and run sync_emails.py to re-authenticate.")
                return False

        # Refresh if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)
        return True

    def _get_or_create_label(self, label_name: str) -> Optional[str]:
        """Get or create a Gmail label and return its ID."""
        # Check cache first
        if label_name in self.label_cache:
            return self.label_cache[label_name]

        try:
            # List existing labels
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            # Check if label exists
            for label in labels:
                if label['name'] == label_name:
                    self.label_cache[label_name] = label['id']
                    return label['id']

            # Label doesn't exist, create it
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }

            created_label = self.service.users().labels().create(
                userId='me',
                body=label_object
            ).execute()

            self.label_cache[label_name] = created_label['id']
            return created_label['id']

        except Exception as e:
            print(f"Error getting/creating label '{label_name}': {e}")
            return None

    def _extract_domain(self, email: str) -> str:
        """Extract domain from email address."""
        _, addr = parseaddr(email)
        if '@' in addr:
            return addr.split('@')[1].lower()
        return ''

    def _match_client(self, email_data: Dict) -> Tuple[Optional[str], int]:
        """
        Match an email to a client and return (client_key, confidence_score).

        Returns:
            (client_key, confidence) or (None, 0) if no match
        """
        sender = email_data.get('from', '').lower()
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()

        sender_email = parseaddr(sender)[1].lower()
        sender_domain = self._extract_domain(sender)

        best_match = None
        best_confidence = 0

        for client_key, client_config in self.config['clients'].items():
            confidence = 0
            matches = []

            # Check domain match (highest confidence)
            domains = [d.lower() for d in client_config.get('domains', [])]
            if sender_domain and sender_domain in domains:
                confidence += 50
                matches.append(f"domain:{sender_domain}")

            # Check exact email match (highly reliable - increased from 40 to 70)
            emails = [e.lower() for e in client_config.get('emails', [])]
            if sender_email and sender_email in emails:
                confidence += 70
                matches.append(f"email:{sender_email}")

            # Check keywords in subject (medium confidence)
            keywords = [k.lower() for k in client_config.get('keywords', [])]
            for keyword in keywords:
                if keyword in subject:
                    confidence += 15
                    matches.append(f"subject_keyword:{keyword}")
                    break  # Only count once per client

            # Check keywords in body (lower confidence)
            for keyword in keywords:
                if keyword in body:
                    confidence += 10
                    matches.append(f"body_keyword:{keyword}")
                    break

            # Check company names in sender
            company_names = [c.lower() for c in client_config.get('company_names', [])]
            for company in company_names:
                if company in sender.lower():
                    confidence += 20
                    matches.append(f"sender_name:{company}")
                    break

            # Check exclude_keywords (reduce confidence if found)
            exclude_keywords = [k.lower() for k in client_config.get('exclude_keywords', [])]
            for exclude_keyword in exclude_keywords:
                if exclude_keyword in subject or exclude_keyword in body:
                    confidence -= 50  # Heavily penalize if exclude keyword found
                    matches.append(f"excluded:{exclude_keyword}")
                    break

            # Update best match if this is better
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = (client_key, matches)

        if best_match and best_confidence >= self.config['settings']['min_confidence']:
            client_key, matches = best_match
            print(f"    Matched: {client_key} (confidence: {best_confidence}%)")
            print(f"    Reasons: {', '.join(matches)}")
            return client_key, best_confidence

        return None, 0

    def _get_email_data(self, message: Dict) -> Dict:
        """Extract email data from Gmail message."""
        headers = {h['name']: h['value'] for h in message['payload']['headers']}

        # Get body (simplified - just get snippet)
        body = message.get('snippet', '')

        return {
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'body': body
        }

    def _apply_label(self, message_id: str, label_id: str) -> bool:
        """Apply a label to a message."""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            return True
        except Exception as e:
            print(f"    Error applying label: {e}")
            return False

    def auto_label_emails(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Auto-label recent emails based on detection rules.

        Returns:
            Statistics dictionary
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        stats = {
            'total_processed': 0,
            'labeled': 0,
            'unmatched': 0,
            'errors': 0
        }

        # Build query for unlabeled emails
        lookback = datetime.now() - timedelta(days=self.config['settings']['lookback_days'])
        query_date = lookback.strftime('%Y/%m/%d')

        # Query: in inbox, newer than lookback date, not in spam/trash
        query = f"in:inbox after:{query_date} -in:spam -in:trash"

        # Exclude emails that already have client labels
        # (We want to label only truly unlabeled emails)

        print(f"\nSearching for emails: {query}")
        print(f"Max emails to process: {self.config['settings']['max_emails_per_run']}\n")

        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=self.config['settings']['max_emails_per_run']
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                print("No emails found to process.\n")
                return stats

            print(f"Found {len(messages)} emails to analyze\n")

            unmatched_emails = []

            for msg_ref in messages:
                msg_id = msg_ref['id']
                stats['total_processed'] += 1

                try:
                    # Fetch full message
                    message = self.service.users().messages().get(
                        userId='me',
                        id=msg_id,
                        format='full'
                    ).execute()

                    # Check if already has a client label
                    existing_labels = message.get('labelIds', [])
                    label_names = []
                    for label_id in existing_labels:
                        for name, lid in self.label_cache.items():
                            if lid == label_id:
                                label_names.append(name)

                    # Skip if already has a client label
                    has_client_label = any(name.startswith('client/') for name in label_names)
                    if has_client_label:
                        continue

                    # Extract email data
                    email_data = self._get_email_data(message)

                    print(f"[{stats['total_processed']}] From: {email_data['from'][:60]}")
                    print(f"    Subject: {email_data['subject'][:60]}")

                    # Match to client
                    client_key, confidence = self._match_client(email_data)

                    if client_key:
                        # Get label name and ID
                        label_name = self.config['clients'][client_key]['label']
                        label_id = self._get_or_create_label(label_name)

                        if label_id:
                            if not dry_run:
                                if self._apply_label(msg_id, label_id):
                                    print(f"    ✓ Labeled as: {label_name}\n")
                                    stats['labeled'] += 1
                                else:
                                    stats['errors'] += 1
                            else:
                                print(f"    [DRY RUN] Would label as: {label_name}\n")
                                stats['labeled'] += 1
                        else:
                            stats['errors'] += 1
                    else:
                        print(f"    ✗ No match found\n")
                        stats['unmatched'] += 1
                        unmatched_emails.append({
                            'from': email_data['from'],
                            'subject': email_data['subject']
                        })

                except Exception as e:
                    print(f"    Error processing message: {e}\n")
                    stats['errors'] += 1

            # Log unmatched emails
            if unmatched_emails and self.config['settings']['log_unmatched']:
                log_file = self.script_dir / 'logs' / 'unmatched_emails.log'
                log_file.parent.mkdir(exist_ok=True)

                with open(log_file, 'a') as f:
                    f.write(f"\n--- {datetime.now().isoformat()} ---\n")
                    for email in unmatched_emails:
                        f.write(f"From: {email['from']}\n")
                        f.write(f"Subject: {email['subject']}\n\n")

        except Exception as e:
            print(f"Error querying emails: {e}")
            stats['errors'] += 1

        return stats


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Auto-label Gmail emails for Pete\'s Brain')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be labeled without actually labeling')
    parser.add_argument('--config', default='auto-label-config.yaml',
                       help='Path to config file (default: auto-label-config.yaml)')

    args = parser.parse_args()

    print("=" * 60)
    print("Pete's Brain - Auto Email Labeling")
    print("=" * 60)

    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No labels will be applied\n")

    try:
        # Initialize auto-labeler
        labeler = AutoLabeler(args.config)

        # Authenticate
        print("\n📧 Authenticating with Gmail...")
        if not labeler.authenticate():
            sys.exit(1)
        print("✓ Authentication successful\n")

        # Auto-label emails
        print("🏷️  Starting auto-labeling...\n")
        stats = labeler.auto_label_emails(dry_run=args.dry_run)

        # Print summary
        print("\n" + "=" * 60)
        print("Auto-Labeling Complete!")
        print("=" * 60)
        print(f"Total emails processed: {stats['total_processed']}")
        print(f"Successfully labeled: {stats['labeled']}")
        print(f"No match found: {stats['unmatched']}")
        print(f"Errors: {stats['errors']}")
        print("=" * 60)

        if stats['unmatched'] > 0:
            print(f"\n💡 Tip: Check logs/unmatched_emails.log to review unmatched emails")
            print("   You can add their domains/keywords to auto-label-config.yaml")

    except KeyboardInterrupt:
        print("\n\n❌ Auto-labeling cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
