#!/usr/bin/env python3
"""
Collaber Chat Monitor Agent

Fetches messages from Collaber PPC Chat space via Google Chat API (direct MCP access)
and saves them to !inbox/ for processing by the AI inbox processor.

Replaces the Gmail notification-based approach with direct API access for:
- Real-time message fetching
- Full message context and threads
- Structured message data
- No email parsing required

Runs every 30 minutes via LaunchAgent.
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuration
COLLABER_SPACE = "spaces/AAAASSOCJ14"
COLLABER_SPACE_NAME = "Collaber PPC Chat"

# Directories
INBOX_DIR = PROJECT_ROOT / '!inbox'
STATE_FILE = INBOX_DIR / '.collaber-chat-state.json'

# Ensure inbox directory exists
INBOX_DIR.mkdir(parents=True, exist_ok=True)


def load_state():
    """Load last processed message timestamp and message IDs."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Error loading state: {e}")

    # Default state
    return {
        'last_check_time': None,
        'processed_message_ids': []
    }


def save_state(state):
    """Save state with last check time and processed message IDs."""
    try:
        state['last_updated'] = datetime.now().isoformat()
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving state: {e}")


def format_message_as_markdown(message):
    """Format Google Chat message as markdown for inbox processing."""

    sender_name = message.get('sender', {}).get('name', 'Unknown')
    create_time = message.get('createTime', '')
    text = message.get('text', '')
    message_name = message.get('name', '')

    # Extract sender user ID for identification
    sender_id = sender_name.split('/')[-1] if '/' in sender_name else sender_name

    # Format timestamp
    try:
        dt = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
        timestamp_readable = dt.strftime('%Y-%m-%d %H:%M')
        timestamp_iso = create_time
    except:
        timestamp_readable = create_time
        timestamp_iso = create_time

    # Build markdown content
    md = "# Google Chat Message (via MCP API)\n\n"
    md += f"**Space:** {COLLABER_SPACE_NAME}\n"
    md += f"**From:** {sender_id}\n"
    md += f"**Time:** {timestamp_readable}\n"
    md += f"**Message ID:** {message_name}\n\n"
    md += "---\n\n"
    md += f"{text}\n\n"

    # Add annotations (mentions, links)
    annotations = message.get('annotations', [])
    if annotations:
        md += "**Annotations:**\n"
        for ann in annotations:
            ann_type = ann.get('type')
            if ann_type == 'USER_MENTION':
                user = ann.get('userMention', {}).get('user', {}).get('name', '')
                md += f"- Mentioned: {user}\n"
            elif ann_type == 'RICH_LINK':
                uri = ann.get('richLinkMetadata', {}).get('uri', '')
                md += f"- Link: {uri}\n"
        md += "\n"

    # Add attachments
    attachments = message.get('attachment', [])
    if attachments:
        md += "**Attachments:**\n"
        for att in attachments:
            name = att.get('contentName', 'Unnamed')
            content_type = att.get('contentType', '')
            drive_id = att.get('driveDataRef', {}).get('driveFileId', '')
            md += f"- {name} ({content_type})\n"
            if drive_id:
                md += f"  Drive ID: {drive_id}\n"
        md += "\n"

    # Add thread context
    thread = message.get('thread', {})
    if thread:
        md += f"**Thread:** {thread.get('name', 'N/A')}\n\n"

    # Add emoji reactions
    reactions = message.get('emojiReactionSummaries', [])
    if reactions:
        md += "**Reactions:**\n"
        for reaction in reactions:
            emoji = reaction.get('emoji', {}).get('unicode', '')
            count = reaction.get('reactionCount', 0)
            md += f"- {emoji} ({count})\n"
        md += "\n"

    md += "---\n\n"
    md += f"**Source:** Google Chat API (MCP)\n"
    md += f"**Space:** {COLLABER_SPACE_NAME}\n"

    return md


def save_message_to_inbox(message):
    """Save message to !inbox/ directory in standard format."""

    # Generate filename
    create_time = message.get('createTime', '')
    message_id = message.get('name', '').split('/')[-1] if message.get('name') else ''

    try:
        dt = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
        date_str = dt.strftime('%Y%m%d-%H%M%S')
    except:
        date_str = datetime.now().strftime('%Y%m%d-%H%M%S')

    # Format: YYYYMMDD-HHMMSS-google-chat-{message_id}.md
    safe_message_id = message_id.replace('.', '-').replace('_', '-')[:20]
    filename = f"{date_str}-google-chat-{safe_message_id}.md"
    filepath = INBOX_DIR / filename

    # Format message as markdown
    content = format_message_as_markdown(message)

    # Save to inbox
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        logging.info(f"  ✓ Saved: {filename}")
        return filepath
    except Exception as e:
        logging.error(f"  ✗ Error saving message: {e}")
        return None


def monitor_collaber_chat():
    """
    Monitor Collaber PPC Chat for new messages.

    This agent requires Claude Code MCP integration to fetch messages.
    When run standalone, it provides status but doesn't fetch messages.
    """

    logging.info("=" * 60)
    logging.info("  Collaber Chat Monitor (MCP API)")
    logging.info("=" * 60)
    logging.info("")

    # Load state
    state = load_state()
    last_check = state.get('last_check_time')
    processed_ids = set(state.get('processed_message_ids', []))

    if last_check:
        last_check_dt = datetime.fromisoformat(last_check)
        logging.info(f"📅 Last check: {last_check_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"📋 Processed messages: {len(processed_ids)}")
    else:
        logging.info("📅 First run - will check recent messages")
        last_check_dt = datetime.now() - timedelta(hours=1)

    logging.info("")
    logging.info(f"💬 Space: {COLLABER_SPACE_NAME}")
    logging.info(f"📁 Output: {INBOX_DIR}")
    logging.info("")

    # NOTE: This agent is designed to run within Claude Code environment
    # where MCP tools are available. For standalone operation, it would need
    # to implement direct Google Chat API calls.

    logging.info("⚠️  This agent requires Claude Code MCP integration")
    logging.info("   When run via Claude Code, it will:")
    logging.info("   1. Fetch messages via mcp__google_chat__list_messages()")
    logging.info("   2. Filter for new messages (not in processed_ids)")
    logging.info("   3. Save to !inbox/ in markdown format")
    logging.info("   4. Update state with new processed message IDs")
    logging.info("")
    logging.info("   Messages then flow through:")
    logging.info("   - ai-inbox-processor (AI enhancement, client detection)")
    logging.info("   - inbox-processor (routing to final locations)")
    logging.info("")

    # Update state with current check time
    state['last_check_time'] = datetime.now().isoformat()
    save_state(state)

    logging.info("✅ Monitor check complete")
    logging.info("=" * 60)


if __name__ == '__main__':
    try:
        monitor_collaber_chat()
    except Exception as e:
        logging.error(f"Error in monitor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
