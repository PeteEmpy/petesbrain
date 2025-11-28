"""
Google Chat Client for PetesBrain

Simple wrapper around Google Chat API for fetching messages from shared spaces
and processing them similar to inbox messages.
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/chat.messages.readonly",
    "https://www.googleapis.com/auth/chat.spaces.readonly"
]


class GoogleChatClient:
    """Client for interacting with Google Chat API"""
    
    def __init__(self):
        """Initialize the Google Chat client with OAuth credentials"""
        self.service = self._get_service()
    
    def _get_service(self):
        """Create and return a Google Chat service instance using OAuth"""
        # Use same credentials pattern as Google Tasks
        token_path = Path(__file__).parent / "mcp-servers" / "google-tasks-mcp-server" / "token.json"
        credentials_path = Path(__file__).parent / "mcp-servers" / "google-tasks-mcp-server" / "credentials.json"
        
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
                        f"You may need to re-authenticate with Google Chat API scopes."
                    )
            else:
                raise ValueError(
                    f"OAuth credentials not found or invalid.\n"
                    f"Token path: {token_path}\n"
                    f"Credentials path: {credentials_path}\n"
                    f"Please ensure credentials.json exists and run OAuth flow with Chat API scopes."
                )
        
        return build("chat", "v1", credentials=creds)
    
    def list_spaces(self, page_size: int = 100) -> List[Dict]:
        """
        List all accessible Google Chat spaces.
        
        Returns:
            List of space dictionaries
        """
        try:
            result = self.service.spaces().list(pageSize=page_size).execute()
            return result.get('spaces', [])
        except HttpError as e:
            print(f"Error listing spaces: {e}")
            return []
    
    def get_space_messages(
        self,
        space_name: str,
        page_size: int = 100,
        page_token: Optional[str] = None,
        filter_by_time: Optional[datetime] = None
    ) -> Dict:
        """
        Get messages from a specific space.
        
        Args:
            space_name: Space name (e.g., "spaces/AAAAxxxxxxx")
            page_size: Number of messages to fetch per page
            page_token: Token for pagination
            filter_by_time: Only fetch messages after this datetime
            
        Returns:
            Dictionary with 'messages' list and 'nextPageToken'
        """
        try:
            params = {
                'parent': space_name,
                'pageSize': page_size
            }
            
            if page_token:
                params['pageToken'] = page_token
            
            # Google Chat API doesn't support time filtering directly in list()
            # We'll filter after fetching
            result = self.service.spaces().messages().list(**params).execute()
            
            messages = result.get('messages', [])
            next_page_token = result.get('nextPageToken')
            
            # Filter by time if specified
            if filter_by_time:
                filtered_messages = []
                for msg in messages:
                    create_time_str = msg.get('createTime', '')
                    if create_time_str:
                        try:
                            # Parse RFC 3339 timestamp
                            msg_time = datetime.fromisoformat(create_time_str.replace('Z', '+00:00'))
                            if msg_time.replace(tzinfo=None) >= filter_by_time:
                                filtered_messages.append(msg)
                        except Exception:
                            # If parsing fails, include the message
                            filtered_messages.append(msg)
                messages = filtered_messages
            
            return {
                'messages': messages,
                'nextPageToken': next_page_token
            }
        except HttpError as e:
            print(f"Error fetching messages from {space_name}: {e}")
            return {'messages': [], 'nextPageToken': None}
    
    def get_all_recent_messages(
        self,
        days_back: int = 7,
        space_filter: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Get all recent messages from all accessible spaces.
        
        Args:
            days_back: Number of days to look back
            space_filter: Optional list of space names to filter by (if None, gets all spaces)
            
        Returns:
            List of message dictionaries with space context
        """
        cutoff_time = datetime.now() - timedelta(days=days_back)
        all_messages = []
        
        # Get spaces
        if space_filter:
            spaces = [{'name': name} for name in space_filter]
        else:
            spaces = self.list_spaces()
        
        print(f"Checking {len(spaces)} space(s) for messages since {cutoff_time.strftime('%Y-%m-%d %H:%M')}")
        
        for space in spaces:
            space_name = space.get('name', '')
            space_display = space.get('displayName', space_name)
            
            if not space_name:
                continue
            
            try:
                # Fetch messages from this space
                result = self.get_space_messages(space_name, filter_by_time=cutoff_time)
                messages = result.get('messages', [])
                
                # Add space context to each message
                for msg in messages:
                    msg['_space_name'] = space_name
                    msg['_space_display'] = space_display
                    all_messages.append(msg)
                
                if messages:
                    print(f"  ✓ {space_display}: {len(messages)} message(s)")
                
            except Exception as e:
                print(f"  ⚠️  Error fetching from {space_display}: {e}")
                continue
        
        # Sort by creation time (newest first)
        all_messages.sort(
            key=lambda m: m.get('createTime', ''),
            reverse=True
        )
        
        return all_messages
    
    def format_message_for_inbox(self, message: Dict) -> str:
        """
        Format a Google Chat message for inbox processing.
        
        Args:
            message: Message dictionary from Google Chat API
            
        Returns:
            Formatted markdown string ready for inbox processing
        """
        sender = message.get('sender', {})
        sender_name = sender.get('name', 'Unknown')
        sender_email = sender.get('email', '')
        
        create_time = message.get('createTime', '')
        text = message.get('text', '')
        space_display = message.get('_space_display', 'Unknown Space')
        space_name = message.get('_space_name', '')
        message_id = message.get('name', '').split('/')[-1] if message.get('name') else ''
        
        # Parse timestamp
        try:
            if create_time:
                msg_datetime = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
                formatted_time = msg_datetime.strftime('%Y-%m-%d %H:%M:%S')
            else:
                formatted_time = 'Unknown time'
        except Exception:
            formatted_time = create_time
        
        # Build formatted content
        content = f"""# Google Chat Message

**Space:** {space_display}
**From:** {sender_name} {f'<{sender_email}>' if sender_email else ''}
**Time:** {formatted_time}
**Message ID:** {message_id}

---

{text}

---

**Source:** Google Chat
**Space ID:** {space_name}
"""
        
        return content
    
    def save_message_to_inbox(self, message: Dict, inbox_dir: Path) -> Optional[Path]:
        """
        Save a Google Chat message to the inbox directory for processing.
        
        Args:
            message: Message dictionary from Google Chat API
            inbox_dir: Path to inbox directory
            
        Returns:
            Path to saved file or None if error
        """
        try:
            inbox_dir.mkdir(exist_ok=True)
            
            # Create filename from timestamp and message ID
            create_time = message.get('createTime', '')
            message_id = message.get('name', '').split('/')[-1] if message.get('name') else 'unknown'
            
            try:
                if create_time:
                    msg_datetime = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
                    timestamp = msg_datetime.strftime('%Y%m%d-%H%M%S')
                else:
                    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            except Exception:
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            
            filename = f"{timestamp}-google-chat-{message_id[:8]}.md"
            filepath = inbox_dir / filename
            
            # Format and save
            content = self.format_message_for_inbox(message)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
            
        except Exception as e:
            print(f"Error saving message to inbox: {e}")
            return None

