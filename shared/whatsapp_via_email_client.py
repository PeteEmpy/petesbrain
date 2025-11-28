"""
WhatsApp via Email Client for PetesBrain

Processes WhatsApp messages by reading WhatsApp notification emails from Gmail.
This approach is simpler and doesn't require WhatsApp Business API setup.
"""

import os
import json
import re
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


class WhatsAppViaEmailClient:
    """Client for accessing WhatsApp messages via Gmail API (notification emails)"""
    
    def __init__(self):
        """Initialize the Gmail client with OAuth credentials"""
        self.service = self._get_service()
    
    def _get_service(self):
        """Create and return a Gmail service instance using OAuth"""
        # Use email-sync Gmail OAuth credentials
        token_path = Path(__file__).parent / "email-sync" / "token.json"
        credentials_path = Path(__file__).parent / "email-sync" / "credentials.json"
        
        creds = None
        
        # Load existing token if available
        if token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            except Exception as e:
                print(f"Warning: Could not load existing token: {e}")
                creds = None
        
        # Refresh token if expired
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    # Save refreshed token
                    with open(token_path, "w") as token_file:
                        token_file.write(creds.to_json())
                except Exception as e:
                    raise ValueError(
                        f"OAuth credentials not valid. Token refresh failed: {e}\n"
                        f"Token path: {token_path}\n"
                        f"You may need to re-authenticate with Gmail API scopes."
                    )
            else:
                raise ValueError(
                    f"OAuth credentials not found or invalid.\n"
                    f"Token path: {token_path}\n"
                    f"Credentials path: {credentials_path}\n"
                    f"Please ensure credentials.json exists and run OAuth flow with Gmail API scopes."
                )
        
        return build("gmail", "v1", credentials=creds)
    
    def extract_whatsapp_message_from_email(self, email_body: str, subject: str) -> Optional[Dict]:
        """
        Extract WhatsApp message details from Gmail notification email.
        
        Returns:
            Dict with sender_name, sender_number, message_text, timestamp
        """
        # Extract sender information
        # WhatsApp notification emails typically have format like:
        # "John Doe: Message text" or "+44 1234 567890: Message text"
        sender_match = re.search(r'^([^:]+):\s*(.+)$', email_body, re.MULTILINE)
        if sender_match:
            sender_info = sender_match.group(1).strip()
            message_text = sender_match.group(2).strip()
        else:
            # Try alternative patterns
            sender_match = re.search(r'From:\s*([^\n]+)', email_body, re.IGNORECASE)
            sender_info = sender_match.group(1).strip() if sender_match else "Unknown"
            
            # Extract message text (everything after sender info)
            message_lines = email_body.split('\n')
            message_started = False
            message_text_parts = []
            
            for line in message_lines:
                if ':' in line and not message_started:
                    message_started = True
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            message_text_parts.append(parts[1].strip())
                    continue
                
                if message_started:
                    # Stop at email footer patterns
                    if any(footer in line.lower() for footer in ['unsubscribe', 'view this', 'whatsapp', '---']):
                        break
                    message_text_parts.append(line)
            
            message_text = '\n'.join(message_text_parts).strip()
        
        # Try to extract phone number from sender info
        phone_match = re.search(r'\+?\d[\d\s\-\(\)]+', sender_info)
        phone_number = phone_match.group(0) if phone_match else None
        
        # Extract name (remove phone number if present)
        sender_name = re.sub(r'\+?\d[\d\s\-\(\)]+', '', sender_info).strip()
        if not sender_name:
            sender_name = phone_number or "Unknown"
        
        return {
            'sender_name': sender_name,
            'sender_number': phone_number,
            'message_text': message_text or "WhatsApp notification (content extraction needed)",
            'subject': subject
        }
    
    def get_whatsapp_notification_emails(
        self,
        days_back: int = 7,
        max_results: int = 100
    ) -> List[Dict]:
        """
        Fetch WhatsApp notification emails from Gmail.
        
        Args:
            days_back: Number of days to look back
            max_results: Maximum number of emails to fetch
            
        Returns:
            List of email dictionaries with WhatsApp message details
        """
        try:
            # Calculate date filter
            cutoff_date = datetime.now() - timedelta(days=days_back)
            date_str = cutoff_date.strftime('%Y/%m/%d')
            
            # Search for WhatsApp notification emails
            # WhatsApp notifications typically come from noreply@whatsapp.com or similar
            query = f'(from:noreply@whatsapp.com OR from:whatsapp.com OR subject:"WhatsApp") after:{date_str}'
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            whatsapp_messages = []
            
            print(f"Found {len(messages)} WhatsApp notification email(s)")
            
            for msg_ref in messages:
                try:
                    # Get full message
                    msg = self.service.users().messages().get(
                        userId='me',
                        id=msg_ref['id'],
                        format='full'
                    ).execute()
                    
                    # Extract headers
                    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
                    subject = headers.get('Subject', '')
                    from_addr = headers.get('From', '')
                    date_str = headers.get('Date', '')
                    
                    # Extract body
                    body = self._extract_email_body(msg['payload'])
                    
                    # Extract WhatsApp message details
                    whatsapp_details = self.extract_whatsapp_message_from_email(body, subject)
                    
                    if whatsapp_details:
                        whatsapp_details.update({
                            'email_id': msg_ref['id'],
                            'email_date': date_str,
                            'email_from': from_addr,
                            'email_subject': subject,
                            'raw_body': body[:500]  # Keep first 500 chars for debugging
                        })
                        whatsapp_messages.append(whatsapp_details)
                
                except Exception as e:
                    print(f"  ⚠️  Error processing email {msg_ref.get('id', 'unknown')}: {e}")
                    continue
            
            return whatsapp_messages
            
        except HttpError as e:
            print(f"Error fetching WhatsApp emails: {e}")
            return []
    
    def _extract_email_body(self, payload: Dict) -> str:
        """Extract text body from email payload"""
        body = ''
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8', errors='ignore')
                        break
                elif part['mimeType'] == 'text/html':
                    # Fallback to HTML if plain text not available
                    if 'data' in part['body'] and not body:
                        html_body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8', errors='ignore')
                        # Simple HTML tag removal
                        body = re.sub(r'<[^>]+>', '', html_body)
        elif 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(
                payload['body']['data']
            ).decode('utf-8', errors='ignore')
        
        return body
    
    def format_message_for_inbox(self, whatsapp_message: Dict) -> str:
        """
        Format a WhatsApp message for inbox processing.
        
        Args:
            whatsapp_message: WhatsApp message dictionary from extract_whatsapp_message_from_email
            
        Returns:
            Formatted markdown string ready for inbox processing
        """
        sender_name = whatsapp_message.get('sender_name', 'Unknown')
        sender_number = whatsapp_message.get('sender_number', '')
        message_text = whatsapp_message.get('message_text', '')
        email_date = whatsapp_message.get('email_date', '')
        email_id = whatsapp_message.get('email_id', '')
        
        # Parse timestamp
        try:
            if email_date:
                # Try parsing email date header
                from email.utils import parsedate_to_datetime
                msg_datetime = parsedate_to_datetime(email_date)
                formatted_time = msg_datetime.strftime('%Y-%m-%d %H:%M:%S')
            else:
                formatted_time = 'Unknown time'
        except Exception:
            formatted_time = email_date
        
        # Build formatted content
        sender_display = f"{sender_name}"
        if sender_number:
            sender_display += f" ({sender_number})"
        
        content = f"""# WhatsApp Message (via Email)

**From:** {sender_display}
**Time:** {formatted_time}
**Email ID:** {email_id}

---

{message_text}

---

**Source:** WhatsApp (via Gmail notification)
**Sender:** {sender_display}
"""
        
        return content
    
    def save_message_to_inbox(self, whatsapp_message: Dict, inbox_dir: Path) -> Optional[Path]:
        """
        Save a WhatsApp message to the inbox directory for processing.
        
        Args:
            whatsapp_message: WhatsApp message dictionary
            inbox_dir: Path to inbox directory
            
        Returns:
            Path to saved file or None if error
        """
        try:
            inbox_dir.mkdir(exist_ok=True)
            
            # Create filename from timestamp and email ID
            email_id = whatsapp_message.get('email_id', 'unknown')
            email_date = whatsapp_message.get('email_date', '')
            
            try:
                if email_date:
                    from email.utils import parsedate_to_datetime
                    msg_datetime = parsedate_to_datetime(email_date)
                    timestamp = msg_datetime.strftime('%Y%m%d-%H%M%S')
                else:
                    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            except Exception:
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            
            filename = f"{timestamp}-whatsapp-{email_id[:8]}.md"
            filepath = inbox_dir / filename
            
            # Format and save
            content = self.format_message_for_inbox(whatsapp_message)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
            
        except Exception as e:
            print(f"Error saving message to inbox: {e}")
            return None

