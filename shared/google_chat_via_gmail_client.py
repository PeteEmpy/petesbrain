"""
Google Chat via Gmail Client for PetesBrain

Processes Google Chat messages by reading Chat notification emails from Gmail.
This approach is more reliable and doesn't require Chat app configuration.
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


class GoogleChatViaGmailClient:
    """Client for accessing Google Chat messages via Gmail API"""
    
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
    
    def extract_chat_message_from_email(self, email_body: str, subject: str) -> Optional[Dict]:
        """
        Extract Chat message details from Gmail notification email.
        
        Returns:
            Dict with space_name, sender_name, sender_email, message_text, timestamp
        """
        # Extract space name from subject
        # Format: "'Space Name' space mention – Message preview"
        space_match = re.search(r"'([^']+)'\s+(?:space|chat)", subject, re.IGNORECASE)
        space_name = space_match.group(1) if space_match else "Unknown Space"
        
        # Extract sender information
        # Look for patterns like "Sender Name <email@domain.com> mentioned you"
        sender_match = re.search(r'([^<]+)\s*<([^>]+)>', email_body)
        if sender_match:
            sender_name = sender_match.group(1).strip()
            sender_email = sender_match.group(2).strip()
        else:
            # Try alternative pattern
            sender_match = re.search(r'([A-Za-z\s]+)\s+mentioned you', email_body, re.IGNORECASE)
            sender_name = sender_match.group(1).strip() if sender_match else "Unknown"
            sender_email = None
        
        # Extract message text
        # Chat notifications usually have the message content in the email body
        # Look for the actual message content (after headers/metadata)
        message_lines = email_body.split('\n')
        message_started = False
        message_text_parts = []
        
        for line in message_lines:
            # Skip email headers and metadata
            if 'mentioned you' in line.lower() or 'while you were away' in line.lower():
                message_started = True
                continue
            
            if message_started:
                # Skip empty lines at start
                if not line.strip() and not message_text_parts:
                    continue
                
                # Stop at email footer patterns
                if any(footer in line.lower() for footer in ['unsubscribe', 'view this', 'google chat', '---']):
                    break
                
                message_text_parts.append(line)
        
        message_text = '\n'.join(message_text_parts).strip()
        
        # If we didn't find message content, try extracting from HTML or use subject
        if not message_text or len(message_text) < 10:
            # Try to get preview from subject
            subject_match = re.search(r'–\s*(.+)$', subject)
            if subject_match:
                message_text = subject_match.group(1).strip()
            else:
                message_text = "Chat notification (content extraction needed)"
        
        return {
            'space_name': space_name,
            'sender_name': sender_name,
            'sender_email': sender_email,
            'message_text': message_text,
            'subject': subject
        }
    
    def get_chat_notification_emails(
        self,
        days_back: int = 7,
        max_results: int = 100
    ) -> List[Dict]:
        """
        Fetch Chat notification emails from Gmail.
        
        Args:
            days_back: Number of days to look back
            max_results: Maximum number of emails to fetch
            
        Returns:
            List of email dictionaries with Chat message details
        """
        try:
            # Calculate date filter
            cutoff_date = datetime.now() - timedelta(days=days_back)
            date_str = cutoff_date.strftime('%Y/%m/%d')
            
            # Search for Chat notification emails
            # Google Chat notifications come from chat-noreply@google.com
            query = f'from:chat-noreply@google.com after:{date_str}'
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            chat_messages = []
            
            print(f"Found {len(messages)} Chat notification email(s)")
            
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
                    
                    # Extract Chat message details
                    chat_details = self.extract_chat_message_from_email(body, subject)
                    
                    if chat_details:
                        chat_details.update({
                            'email_id': msg_ref['id'],
                            'email_date': date_str,
                            'email_from': from_addr,
                            'email_subject': subject,
                            'raw_body': body[:500]  # Keep first 500 chars for debugging
                        })
                        chat_messages.append(chat_details)
                
                except Exception as e:
                    print(f"  ⚠️  Error processing email {msg_ref.get('id', 'unknown')}: {e}")
                    continue
            
            return chat_messages
            
        except HttpError as e:
            print(f"Error fetching Chat emails: {e}")
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
    
    def format_message_for_inbox(self, chat_message: Dict) -> str:
        """
        Format a Chat message for inbox processing.
        
        Args:
            chat_message: Chat message dictionary from extract_chat_message_from_email
            
        Returns:
            Formatted markdown string ready for inbox processing
        """
        space_name = chat_message.get('space_name', 'Unknown Space')
        sender_name = chat_message.get('sender_name', 'Unknown')
        sender_email = chat_message.get('sender_email', '')
        message_text = chat_message.get('message_text', '')
        email_date = chat_message.get('email_date', '')
        email_id = chat_message.get('email_id', '')
        
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
        content = f"""# Google Chat Message (via Gmail)

**Space:** {space_name}
**From:** {sender_name} {f'<{sender_email}>' if sender_email else ''}
**Time:** {formatted_time}
**Email ID:** {email_id}

---

{message_text}

---

**Source:** Google Chat (via Gmail notification)
**Space:** {space_name}
"""
        
        return content
    
    def save_message_to_inbox(self, chat_message: Dict, inbox_dir: Path) -> Optional[Path]:
        """
        Save a Chat message to the inbox directory for processing.
        
        Args:
            chat_message: Chat message dictionary
            inbox_dir: Path to inbox directory
            
        Returns:
            Path to saved file or None if error
        """
        try:
            inbox_dir.mkdir(exist_ok=True)
            
            # Create filename from timestamp and email ID
            email_id = chat_message.get('email_id', 'unknown')
            email_date = chat_message.get('email_date', '')
            
            try:
                if email_date:
                    from email.utils import parsedate_to_datetime
                    msg_datetime = parsedate_to_datetime(email_date)
                    timestamp = msg_datetime.strftime('%Y%m%d-%H%M%S')
                else:
                    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            except Exception:
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            
            filename = f"{timestamp}-google-chat-{email_id[:8]}.md"
            filepath = inbox_dir / filename
            
            # Format and save
            content = self.format_message_for_inbox(chat_message)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
            
        except Exception as e:
            print(f"Error saving message to inbox: {e}")
            return None

