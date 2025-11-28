"""
WhatsApp Business API Client for PetesBrain

Processes WhatsApp messages via WhatsApp Business API and routes them
similar to inbox messages. Allocates chats to clients and creates tasks.

Note: Requires WhatsApp Business API setup with Meta/Facebook.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import hmac
import hashlib

class WhatsAppBusinessClient:
    """Client for interacting with WhatsApp Business API"""
    
    def __init__(self, access_token: str = None, phone_number_id: str = None, verify_token: str = None):
        """
        Initialize WhatsApp Business API client.
        
        Args:
            access_token: WhatsApp Business API access token
            phone_number_id: Your WhatsApp Business phone number ID
            verify_token: Webhook verification token (for webhook setup)
        """
        self.access_token = access_token or os.environ.get('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = phone_number_id or os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
        self.verify_token = verify_token or os.environ.get('WHATSAPP_VERIFY_TOKEN')
        self.api_version = 'v21.0'
        self.base_url = f'https://graph.facebook.com/{self.api_version}'
        
        if not self.access_token or not self.phone_number_id:
            raise ValueError(
                "WhatsApp Business API credentials not found. "
                "Set WHATSAPP_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID environment variables, "
                "or pass them to the constructor."
            )
    
    def verify_webhook(self, mode: str, token: str, challenge: str) -> Optional[str]:
        """
        Verify webhook subscription (for webhook setup).
        
        Returns challenge string if verification succeeds, None otherwise.
        """
        if mode == 'subscribe' and token == self.verify_token:
            return challenge
        return None
    
    def get_messages(self, limit: int = 50) -> List[Dict]:
        """
        Fetch recent messages from WhatsApp Business API.
        
        Note: WhatsApp Business API uses webhooks for real-time messages.
        This method would need to query your database/logs of received messages.
        
        For production, use webhooks to receive messages in real-time.
        """
        # WhatsApp Business API doesn't have a direct "list messages" endpoint
        # Messages are received via webhooks. You need to store them in a database.
        # This is a placeholder - implement based on your message storage.
        
        print("⚠️  WhatsApp Business API uses webhooks for messages.")
        print("    Messages should be stored when received via webhook.")
        print("    Implement message storage/retrieval based on your setup.")
        
        return []
    
    def format_message_for_inbox(self, message: Dict) -> str:
        """
        Format a WhatsApp message for inbox processing.
        
        Args:
            message: Message dictionary with WhatsApp message data
            
        Returns:
            Formatted markdown string ready for inbox processing
        """
        from_number = message.get('from', 'Unknown')
        message_text = message.get('text', {}).get('body', '')
        message_id = message.get('id', '')
        timestamp = message.get('timestamp', '')
        
        # Parse timestamp
        try:
            if timestamp:
                msg_datetime = datetime.fromtimestamp(int(timestamp))
                formatted_time = msg_datetime.strftime('%Y-%m-%d %H:%M:%S')
            else:
                formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            formatted_time = timestamp or 'Unknown time'
        
        # Build formatted content
        content = f"""# WhatsApp Message

**From:** {from_number}
**Time:** {formatted_time}
**Message ID:** {message_id}

---

{message_text}

---

**Source:** WhatsApp Business API
**Phone Number:** {from_number}
"""
        
        return content
    
    def save_message_to_inbox(self, message: Dict, inbox_dir: Path) -> Optional[Path]:
        """
        Save a WhatsApp message to the inbox directory for processing.
        
        Args:
            message: Message dictionary from WhatsApp Business API
            inbox_dir: Path to inbox directory
            
        Returns:
            Path to saved file or None if error
        """
        try:
            inbox_dir.mkdir(exist_ok=True)
            
            # Create filename from timestamp and message ID
            timestamp = message.get('timestamp', '')
            message_id = message.get('id', 'unknown')
            
            try:
                if timestamp:
                    msg_datetime = datetime.fromtimestamp(int(timestamp))
                    timestamp_str = msg_datetime.strftime('%Y%m%d-%H%M%S')
                else:
                    timestamp_str = datetime.now().strftime('%Y%m%d-%H%M%S')
            except Exception:
                timestamp_str = datetime.now().strftime('%Y%m%d-%H%M%S')
            
            filename = f"{timestamp_str}-whatsapp-{message_id[:8]}.md"
            filepath = inbox_dir / filename
            
            # Format and save
            content = self.format_message_for_inbox(message)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
            
        except Exception as e:
            print(f"Error saving message to inbox: {e}")
            return None
    
    def process_webhook(self, webhook_data: Dict) -> Optional[Dict]:
        """
        Process incoming webhook data from WhatsApp Business API.
        
        Args:
            webhook_data: Webhook payload from WhatsApp
            
        Returns:
            Extracted message dictionary or None
        """
        try:
            # WhatsApp webhook structure
            entry = webhook_data.get('entry', [{}])[0]
            changes = entry.get('changes', [{}])[0]
            value = changes.get('value', {})
            messages = value.get('messages', [])
            
            if not messages:
                return None
            
            # Get the first message
            message = messages[0]
            
            # Extract message data
            return {
                'id': message.get('id'),
                'from': message.get('from'),
                'timestamp': message.get('timestamp'),
                'text': message.get('text', {}),
                'type': message.get('type'),
                'contacts': value.get('contacts', [])
            }
            
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return None

