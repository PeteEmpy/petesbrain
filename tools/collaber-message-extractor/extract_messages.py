#!/usr/bin/env python3
"""
Collaber Chat Message Extractor

Extracts messages from Collaber PPC Chat space and saves them to Tree2mydoor client folder.

Usage:
    python3 extract_messages.py --days 7              # Last 7 days
    python3 extract_messages.py --since "2025-12-01"  # Since specific date
    python3 extract_messages.py --keywords "SKU,price,stock"  # Filter by keywords
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Collaber PPC Chat space ID
COLLABER_SPACE = "spaces/AAAASSOCJ14"

# Output directory
TREE2MYDOOR_UPDATES = PROJECT_ROOT / "clients" / "tree2mydoor" / "collaber-updates"
TREE2MYDOOR_UPDATES.mkdir(parents=True, exist_ok=True)


def extract_messages(days_back=7, since_date=None, keywords=None, save_format="markdown"):
    """
    Extract messages from Collaber PPC Chat.

    Args:
        days_back: Number of days to look back (default: 7)
        since_date: Specific date to start from (YYYY-MM-DD)
        keywords: Comma-separated keywords to filter for
        save_format: Output format (markdown, json, both)
    """
    print("=" * 60)
    print("  Collaber Chat Message Extractor")
    print("=" * 60)
    print()

    # Determine date range
    if since_date:
        start_date = datetime.fromisoformat(since_date)
    else:
        start_date = datetime.now() - timedelta(days=days_back)

    print(f"📅 Extracting messages since: {start_date.strftime('%Y-%m-%d')}")
    print(f"💬 Space: Collaber PPC Chat")
    print()

    # NOTE: This script is meant to be run within Claude Code environment
    # where MCP tools are available. For standalone usage, would need to
    # implement direct Google Chat API calls.

    print("⚠️  This tool requires Claude Code environment with Google Chat MCP server")
    print("    Run this script via Claude Code, not standalone Python")
    print()
    print("    Example Claude Code usage:")
    print("    - 'Extract last 7 days of Collaber Chat messages'")
    print("    - 'Get product updates from Collaber Chat this month'")
    print()

    # When run via Claude Code, messages would be passed as argument or
    # fetched via MCP tool calls

    return {
        "status": "requires_claude_code",
        "space": COLLABER_SPACE,
        "start_date": start_date.isoformat(),
        "output_dir": str(TREE2MYDOOR_UPDATES)
    }


def save_messages_markdown(messages, output_file):
    """Save messages in markdown format."""

    with open(output_file, 'w') as f:
        f.write("# Collaber PPC Chat Messages\n\n")
        f.write(f"**Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        for msg in messages:
            sender = msg.get('sender', {}).get('name', 'Unknown')
            create_time = msg.get('createTime', '')
            text = msg.get('text', '')

            # Format timestamp
            try:
                dt = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
                timestamp = dt.strftime('%Y-%m-%d %H:%M')
            except:
                timestamp = create_time

            f.write(f"## Message - {timestamp}\n\n")
            f.write(f"**From:** {sender}\n\n")
            f.write(f"{text}\n\n")

            # Add annotations if present
            annotations = msg.get('annotations', [])
            if annotations:
                f.write("**Mentions/Links:**\n")
                for ann in annotations:
                    ann_type = ann.get('type')
                    if ann_type == 'USER_MENTION':
                        user = ann.get('userMention', {}).get('user', {}).get('name', '')
                        f.write(f"- Mentioned: {user}\n")
                    elif ann_type == 'RICH_LINK':
                        uri = ann.get('richLinkMetadata', {}).get('uri', '')
                        f.write(f"- Link: {uri}\n")
                f.write("\n")

            # Add attachments if present
            attachments = msg.get('attachment', [])
            if attachments:
                f.write("**Attachments:**\n")
                for att in attachments:
                    name = att.get('contentName', 'Unnamed')
                    content_type = att.get('contentType', '')
                    f.write(f"- {name} ({content_type})\n")
                f.write("\n")

            f.write("---\n\n")

    print(f"✅ Saved to: {output_file}")


def save_messages_json(messages, output_file):
    """Save messages in JSON format."""

    with open(output_file, 'w') as f:
        json.dump({
            "extracted_at": datetime.now().isoformat(),
            "space": COLLABER_SPACE,
            "message_count": len(messages),
            "messages": messages
        }, f, indent=2)

    print(f"✅ Saved to: {output_file}")


def extract_product_updates(messages):
    """Extract product-related updates from messages."""

    product_keywords = [
        'sku', 'product', 'price', 'stock', 'variant',
        'tree2mydoor', 'back in stock', 'out of stock',
        '£', 'revised to', 'updated'
    ]

    updates = []

    for msg in messages:
        text = msg.get('text', '').lower()

        # Check if message contains product-related keywords
        if any(keyword in text for keyword in product_keywords):
            updates.append({
                "timestamp": msg.get('createTime'),
                "text": msg.get('text'),
                "sender": msg.get('sender', {}).get('name'),
                "has_links": bool(msg.get('annotations', []))
            })

    return updates


def main():
    parser = argparse.ArgumentParser(description='Extract messages from Collaber PPC Chat')
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to look back (default: 7)'
    )
    parser.add_argument(
        '--since',
        type=str,
        help='Extract since specific date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--keywords',
        type=str,
        help='Comma-separated keywords to filter for'
    )
    parser.add_argument(
        '--format',
        choices=['markdown', 'json', 'both'],
        default='markdown',
        help='Output format (default: markdown)'
    )

    args = parser.parse_args()

    result = extract_messages(
        days_back=args.days,
        since_date=args.since,
        keywords=args.keywords,
        save_format=args.format
    )

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
