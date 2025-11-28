#!/usr/bin/env python3
"""
Google Chat Processor for PetesBrain

Fetches Google Chat messages from shared spaces and processes them similar to inbox:
- Fetches recent messages from all accessible Google Chat spaces
- Saves them to !inbox/ for processing by inbox-processor.py
- Can optionally process them directly (similar to inbox-processor)

Runs periodically to check for new Google Chat messages.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import Google Chat client (via Gmail)
try:
    from shared.google_chat_via_gmail_client import GoogleChatViaGmailClient
    GOOGLE_CHAT_ENABLED = True
except Exception as e:
    print(f"⚠️  Google Chat integration not available: {e}")
    GOOGLE_CHAT_ENABLED = False

INBOX_DIR = PROJECT_ROOT / '!inbox'
PROCESSED_CHATS_DIR = PROJECT_ROOT / '!inbox' / 'processed-chats'
STATE_FILE = PROJECT_ROOT / '!inbox' / '.google-chat-processor-state.json'


def load_processed_message_ids() -> set:
    """Load set of already processed message IDs"""
    if STATE_FILE.exists():
        try:
            import json
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                return set(state.get('processed_message_ids', []))
        except Exception:
            return set()
    return set()


def save_processed_message_ids(message_ids: set):
    """Save set of processed message IDs"""
    try:
        import json
        PROCESSED_CHATS_DIR.mkdir(parents=True, exist_ok=True)
        
        state = {
            'processed_message_ids': list(message_ids),
            'last_run': datetime.now().isoformat()
        }
        
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"⚠️  Error saving state: {e}")


def process_google_chats(days_back: int = 7, space_filter: list = None):
    """
    Fetch and process Google Chat messages.
    
    Args:
        days_back: Number of days to look back for messages
        space_filter: Optional list of space names to filter by
    """
    if not GOOGLE_CHAT_ENABLED:
        print("❌ Google Chat integration not available")
        return
    
    print("=" * 60)
    print("  Google Chat Processor")
    print("=" * 60)
    print()
    
    # Load already processed messages
    processed_ids = load_processed_message_ids()
    print(f"📋 Already processed: {len(processed_ids)} message(s)")
    print()
    
    try:
        # Initialize client
        client = GoogleChatViaGmailClient()
            
        # Fetch recent messages from Gmail
        print(f"🔍 Fetching Chat notification emails from last {days_back} day(s)...")
        chat_messages = client.get_chat_notification_emails(
            days_back=days_back
        )
        
        print()
        print(f"📬 Found {len(chat_messages)} Chat message(s)")
        print()
        
        if not chat_messages:
            print("✅ No new Chat messages to process")
            return
        
        # Filter out already processed messages
        new_messages = []
        for msg in chat_messages:
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
            space_display = msg.get('space_name', 'Unknown Space')
            sender_name = msg.get('sender_name', 'Unknown')
            
            print(f"📄 Processing: {space_display} - {sender_name}")
            
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
        print(f"❌ Error processing Google Chats: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Process Google Chat messages')
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to look back (default: 7)'
    )
    parser.add_argument(
        '--spaces',
        nargs='+',
        help='Filter by specific space names (optional)'
    )
    
    args = parser.parse_args()
    
    process_google_chats(
        days_back=args.days,
        space_filter=args.spaces
    )

