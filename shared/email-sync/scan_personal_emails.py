#!/usr/bin/env python3
"""
Scan SENT emails from petere@roksys.co.uk for client-relevant content and Google Sheets links
This is separate from the auto-labeling system and scans for data to extract
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from email.utils import parsedate_to_datetime

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Error: Gmail API dependencies not installed.")
    sys.exit(1)

# Gmail API scopes - ONLY gmail.modify needed (includes read access)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify'  # Read, modify, labels, send
]

# Known clients to search for
KNOWN_CLIENTS = [
    'smythson', 'devonshire', 'tree2mydoor', 'superspace', 'national design academy',
    'nda', 'clear prospects', 'accessories for the home', 'uno lighting',
    'bright minds', 'godshot', 'otc', 'print my pdf', 'grain guard',
    'just bin bags', 'crowd control', 'positive bakes', 'go glean'
]

class PersonalEmailScanner:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.service = None

    def authenticate(self):
        """Authenticate with Gmail API."""
        creds = None
        token_file = self.script_dir / 'token.json'
        credentials_file = self.script_dir / 'credentials.json'

        if token_file.exists():
            creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not credentials_file.exists():
                    print("Error: credentials.json not found!")
                    return False
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_file), SCOPES)
                creds = flow.run_local_server(port=0)

            with open(token_file, 'w') as f:
                f.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)
        return True

    def extract_google_sheets_links(self, text: str) -> List[str]:
        """Extract Google Sheets links from text."""
        if not text:
            return []

        # Pattern for Google Sheets URLs
        pattern = r'https://docs\.google\.com/spreadsheets/d/[a-zA-Z0-9-_]+(?:/[^\s]*)?'
        links = re.findall(pattern, text)
        return list(set(links))  # Remove duplicates

    def extract_client_mentions(self, text: str) -> List[str]:
        """Extract client mentions from text."""
        if not text:
            return []

        text_lower = text.lower()
        mentioned = []

        for client in KNOWN_CLIENTS:
            if client in text_lower:
                mentioned.append(client)

        return list(set(mentioned))

    def get_email_body(self, message: Dict) -> str:
        """Extract email body from message."""
        body = ""

        if 'payload' not in message:
            return body

        payload = message['payload']

        # Handle multipart messages
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        import base64
                        body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                elif part['mimeType'] == 'text/html':
                    if 'data' in part['body']:
                        import base64
                        html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                        # Strip HTML tags for content analysis
                        body += re.sub('<[^<]+?>', '', html)
        else:
            # Simple message
            if 'body' in payload and 'data' in payload['body']:
                import base64
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')

        return body

    def get_email_subject(self, message: Dict) -> str:
        """Extract subject from message."""
        if 'payload' not in message:
            return ""

        headers = message['payload'].get('headers', [])
        for header in headers:
            if header['name'].lower() == 'subject':
                return header['value']
        return ""

    def get_email_date(self, message: Dict) -> str:
        """Extract date from message."""
        if 'payload' not in message:
            return ""

        headers = message['payload'].get('headers', [])
        for header in headers:
            if header['name'].lower() == 'date':
                return header['value']

        # Fallback to internalDate
        if 'internalDate' in message:
            timestamp = int(message['internalDate']) / 1000
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        return ""

    def scan_emails(self, max_results: int = 100):
        """Scan SENT emails from petere@roksys.co.uk."""
        print("=" * 60)
        print("Scanning SENT emails from petere@roksys.co.uk")
        print("=" * 60)
        print()

        # Search for emails in Sent folder
        query = "in:sent"

        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                print("No sent emails found")
                return

            print(f"Found {len(messages)} sent emails to analyze")
            print()

            findings = []

            for i, msg in enumerate(messages, 1):
                # Get full message
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='full'
                ).execute()

                subject = self.get_email_subject(message)
                date = self.get_email_date(message)
                body = self.get_email_body(message)

                # Extract data
                sheets_links = self.extract_google_sheets_links(body + " " + subject)
                client_mentions = self.extract_client_mentions(body + " " + subject)

                # Only show emails with relevant content
                if sheets_links or client_mentions:
                    finding = {
                        'number': i,
                        'date': date,
                        'subject': subject,
                        'clients': client_mentions,
                        'sheets_links': sheets_links,
                        'body_preview': body[:300] if body else ""
                    }
                    findings.append(finding)

            # Display findings
            if findings:
                print(f"\n{'=' * 60}")
                print(f"Found {len(findings)} emails with client-relevant content or Google Sheets links:")
                print(f"{'=' * 60}\n")

                for finding in findings:
                    print(f"📧 Email #{finding['number']}")
                    print(f"   Date: {finding['date']}")
                    print(f"   Subject: {finding['subject']}")

                    if finding['clients']:
                        print(f"   📊 Client mentions: {', '.join(finding['clients'])}")

                    if finding['sheets_links']:
                        print(f"   📈 Google Sheets links:")
                        for link in finding['sheets_links']:
                            print(f"      • {link}")

                    if finding['body_preview']:
                        print(f"   Preview: {finding['body_preview'][:150]}...")

                    print()

                # Save results to JSON
                output_file = Path('/Users/administrator/Documents/PetesBrain/data/cache/personal-email-scan-results.json')
                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, 'w') as f:
                    json.dump(findings, f, indent=2)

                print(f"\n✓ Results saved to: {output_file}")
                print(f"\nNext steps:")
                print(f"1. Review the findings above")
                print(f"2. For each email with Google Sheets links:")
                print(f"   - Open the sheet")
                print(f"   - Determine which client it belongs to")
                print(f"   - Download/save data to appropriate client folder")
                print(f"3. For emails with client mentions but no sheets:")
                print(f"   - Consider if the content should be saved to client folder")

            else:
                print("\nNo sent emails found with client mentions or Google Sheets links.")
                print("All analyzed sent emails appear to be personal/non-client related.")

        except Exception as e:
            print(f"Error scanning emails: {e}")
            import traceback
            traceback.print_exc()

def main():
    scanner = PersonalEmailScanner()

    print("Authenticating with Gmail...")
    if not scanner.authenticate():
        print("Authentication failed")
        return 1

    print("✓ Authentication successful\n")

    scanner.scan_emails(max_results=200)  # Scan last 200 emails

    return 0

if __name__ == '__main__':
    sys.exit(main())
