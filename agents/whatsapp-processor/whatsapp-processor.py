#!/usr/bin/env python3
"""
WhatsApp Processor for PetesBrain

Processes WhatsApp messages via WhatsApp Business API webhooks and routes them
similar to inbox messages. Allocates chats to clients and creates tasks.

Note: Requires WhatsApp Business API setup with Meta/Facebook.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import WhatsApp client (try email-based first, then Business API)
try:
    from shared.whatsapp_via_email_client import WhatsAppViaEmailClient
    WHATSAPP_EMAIL_ENABLED = True
except Exception as e:
    WHATSAPP_EMAIL_ENABLED = False

try:
    from shared.whatsapp_business_client import WhatsAppBusinessClient
    WHATSAPP_API_ENABLED = True
except Exception as e:
    WHATSAPP_API_ENABLED = False

WHATSAPP_ENABLED = WHATSAPP_EMAIL_ENABLED or WHATSAPP_API_ENABLED

INBOX_DIR = PROJECT_ROOT / '!inbox'
PROCESSED_WHATSAPP_DIR = PROJECT_ROOT / '!inbox' / 'processed-whatsapp'
STATE_FILE = PROJECT_ROOT / '!inbox' / '.whatsapp-processor-state.json'


def load_processed_message_ids() -> set:
    """Load set of already processed message IDs"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                return set(state.get('processed_message_ids', []))
        except Exception:
            return set()
    return set()


def save_processed_message_ids(message_ids: set):
    """Save set of processed message IDs"""
    try:
        PROCESSED_WHATSAPP_DIR.mkdir(parents=True, exist_ok=True)
        
        state = {
            'processed_message_ids': list(message_ids),
            'last_run': datetime.now().isoformat()
        }
        
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"⚠️  Error saving state: {e}")


def process_whatsapp_messages_via_email(days_back: int = 7):
    """
    Process WhatsApp messages via Gmail notification emails.
    
    Args:
        days_back: Number of days to look back
    """
    if not WHATSAPP_EMAIL_ENABLED:
        print("❌ WhatsApp email integration not available")
        return
    
    print("=" * 60)
    print("  WhatsApp Processor (via Email)")
    print("=" * 60)
    print()
    
    # Load already processed messages
    processed_ids = load_processed_message_ids()
    print(f"📋 Already processed: {len(processed_ids)} message(s)")
    print()
    
    try:
        # Initialize client
        client = WhatsAppViaEmailClient()
        
        # Fetch recent messages from Gmail
        print(f"🔍 Fetching WhatsApp notification emails from last {days_back} day(s)...")
        whatsapp_messages = client.get_whatsapp_notification_emails(
            days_back=days_back
        )
        
        print()
        print(f"📬 Found {len(whatsapp_messages)} WhatsApp message(s)")
        print()
        
        if not whatsapp_messages:
            print("✅ No new WhatsApp messages to process")
            print("   Note: Enable email notifications in WhatsApp settings to receive messages via email")
            return
        
        # Filter out already processed messages
        new_messages = []
        for msg in whatsapp_messages:
            email_id = msg.get('email_id', '')
            if email_id and email_id not in processed_ids:
                new_messages.append(msg)
        
        print(f"🆕 New messages: {len(new_messages)}")
        print()
        
        if not new_messages:
            print("✅ No new messages to process")
            return
        
        # Process each new message
        processed_count = 0
        new_processed_ids = set(processed_ids)
        
        for msg in new_messages:
            email_id = msg.get('email_id', '')
            sender_name = msg.get('sender_name', 'Unknown')
            sender_number = msg.get('sender_number', '')
            
            sender_display = f"{sender_name}"
            if sender_number:
                sender_display += f" ({sender_number})"
            
            print(f"📄 Processing: {sender_display}")
            
            # Save to inbox
            filepath = client.save_message_to_inbox(msg, INBOX_DIR)
            
            if filepath:
                print(f"  ✓ Saved to: {filepath.name}")
                processed_count += 1
                
                # Mark as processed
                if email_id:
                    new_processed_ids.add(email_id)
            else:
                print(f"  ⚠️  Failed to save message")
            
            print()
        
        # Save updated state
        save_processed_message_ids(new_processed_ids)
        
        print("=" * 60)
        print(f"✅ Processed {processed_count}/{len(new_messages)} new message(s)")
        print(f"   Messages saved to: !inbox/")
        print(f"   Next: Run inbox-processor.py to route them")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error processing WhatsApp messages: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def process_whatsapp_message(message_data: Dict):
    """
    Process a single WhatsApp message.
    
    Args:
        message_data: Message dictionary from WhatsApp Business API
    """
    if not WHATSAPP_ENABLED:
        print("❌ WhatsApp integration not available")
        return False
    
    try:
        # Load processed IDs
        processed_ids = load_processed_message_ids()
        
        message_id = message_data.get('id')
        if message_id and message_id in processed_ids:
            print(f"  ⚠️  Message {message_id} already processed")
            return False
        
        # Initialize client
        client = WhatsAppBusinessClient()
        
        # Save to inbox
        filepath = client.save_message_to_inbox(message_data, INBOX_DIR)
        
        if filepath:
            print(f"  ✓ Saved to: {filepath.name}")
            
            # Mark as processed
            if message_id:
                processed_ids.add(message_id)
                save_processed_message_ids(processed_ids)
            
            return True
        else:
            print(f"  ⚠️  Failed to save message")
            return False
            
    except Exception as e:
        print(f"❌ Error processing WhatsApp message: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Process WhatsApp messages')
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to look back (for email-based processing, default: 7)'
    )
    parser.add_argument(
        '--webhook',
        action='store_true',
        help='Process webhook data from stdin (Business API)'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Process message from JSON file (Business API)'
    )
    parser.add_argument(
        '--email',
        action='store_true',
        help='Process via email notifications (default if no other option)'
    )
    
    args = parser.parse_args()
    
    if args.webhook:
        # Read webhook data from stdin (Business API)
        if not WHATSAPP_API_ENABLED:
            print("❌ WhatsApp Business API not configured")
            sys.exit(1)
        
        webhook_data = json.load(sys.stdin)
        client = WhatsAppBusinessClient()
        message_data = client.process_webhook(webhook_data)
        
        if message_data:
            print("=" * 60)
            print("  WhatsApp Message Processor (Business API)")
            print("=" * 60)
            print()
            process_whatsapp_message(message_data)
        else:
            print("No message found in webhook data")
    
    elif args.file:
        # Read message from file (Business API)
        if not WHATSAPP_API_ENABLED:
            print("❌ WhatsApp Business API not configured")
            sys.exit(1)
        
        with open(args.file, 'r') as f:
            message_data = json.load(f)
        
        print("=" * 60)
        print("  WhatsApp Message Processor (Business API)")
        print("=" * 60)
        print()
        process_whatsapp_message(message_data)
    
    else:
        # Default: process via email (simpler approach)
        process_whatsapp_messages_via_email(days_back=args.days)

