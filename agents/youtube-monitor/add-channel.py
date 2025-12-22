#!/usr/bin/env python3
"""
Add YouTube Channel to Monitor

Simple script to add a new YouTube channel to the monitoring list.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
CHANNELS_FILE = PROJECT_ROOT / "agents/youtube-monitor/channels.json"
YOUTUBE_API_KEY = "AIzaSyDowdeXxrfH2TLrgxfxM70_javptOVYv4U"


def search_channel(query):
    """Search for YouTube channel by name"""
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    search_request = youtube.search().list(
        part='snippet',
        q=query,
        type='channel',
        maxResults=5
    )
    search_response = search_request.execute()

    channels = []
    for item in search_response.get('items', []):
        snippet = item['snippet']
        channels.append({
            'name': snippet['title'],
            'channel_id': item['id']['channelId'],
            'description': snippet['description'][:100] + '...' if len(snippet['description']) > 100 else snippet['description']
        })

    return channels


def load_config():
    """Load channels config"""
    if CHANNELS_FILE.exists():
        with open(CHANNELS_FILE, 'r') as f:
            return json.load(f)
    return {"channels": [], "suggested_channels": []}


def save_config(config):
    """Save channels config"""
    with open(CHANNELS_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def add_channel(name, channel_id, category="", notes=""):
    """Add channel to monitoring list"""
    config = load_config()

    # Check if already exists
    existing = [ch for ch in config['channels'] if ch['channel_id'] == channel_id]
    if existing:
        print(f"❌ Channel already exists: {existing[0]['name']}")
        return False

    # Add to channels list
    new_channel = {
        "name": name,
        "channel_id": channel_id,
        "added_date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "notes": notes
    }

    config['channels'].append(new_channel)

    # Remove from suggested if present
    config['suggested_channels'] = [
        ch for ch in config.get('suggested_channels', [])
        if ch['channel_id'] != channel_id
    ]

    save_config(config)
    print(f"✅ Added channel: {name}")
    print(f"   Channel ID: {channel_id}")
    print(f"   Category: {category}")
    return True


def list_channels():
    """List all monitored channels"""
    config = load_config()

    print("\n📺 Currently Monitored Channels:")
    print("=" * 60)

    if not config['channels']:
        print("No channels configured yet.")
    else:
        for ch in config['channels']:
            print(f"\n{ch['name']}")
            print(f"  ID: {ch['channel_id']}")
            print(f"  Category: {ch.get('category', 'N/A')}")
            print(f"  Added: {ch.get('added_date', 'N/A')}")
            if ch.get('notes'):
                print(f"  Notes: {ch['notes']}")

    if config.get('suggested_channels'):
        print("\n\n💡 Suggested Channels (not yet monitored):")
        print("=" * 60)
        for ch in config['suggested_channels']:
            print(f"\n{ch['name']}")
            print(f"  ID: {ch['channel_id']}")
            print(f"  Category: {ch.get('category', 'N/A')}")
            if ch.get('notes'):
                print(f"  Notes: {ch['notes']}")


def interactive_add():
    """Interactive channel addition"""
    print("\n🔍 YouTube Channel Search")
    print("=" * 60)

    query = input("\nEnter channel name to search: ").strip()

    if not query:
        print("❌ Search query required")
        return

    print(f"\nSearching for '{query}'...")
    results = search_channel(query)

    if not results:
        print("❌ No channels found")
        return

    print(f"\nFound {len(results)} channels:")
    for i, ch in enumerate(results, 1):
        print(f"\n{i}. {ch['name']}")
        print(f"   ID: {ch['channel_id']}")
        print(f"   {ch['description']}")

    choice = input("\nSelect channel (1-5) or 0 to cancel: ").strip()

    try:
        choice = int(choice)
        if choice == 0:
            print("Cancelled")
            return
        if choice < 1 or choice > len(results):
            print("❌ Invalid choice")
            return

        selected = results[choice - 1]

        category = input("\nCategory (e.g., Google Ads, E-commerce, Analytics): ").strip()
        notes = input("Notes (optional): ").strip()

        add_channel(
            selected['name'],
            selected['channel_id'],
            category,
            notes
        )

        print("\n✅ Channel added successfully!")
        print("Next run of youtube-monitor will include this channel.")

    except ValueError:
        print("❌ Invalid input")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            list_channels()

        elif command == "add":
            if len(sys.argv) < 4:
                print("Usage: add-channel.py add <channel_name> <channel_id> [category] [notes]")
                sys.exit(1)

            name = sys.argv[2]
            channel_id = sys.argv[3]
            category = sys.argv[4] if len(sys.argv) > 4 else ""
            notes = sys.argv[5] if len(sys.argv) > 5 else ""

            add_channel(name, channel_id, category, notes)

        elif command == "search":
            if len(sys.argv) < 3:
                print("Usage: add-channel.py search <query>")
                sys.exit(1)

            query = sys.argv[2]
            results = search_channel(query)

            print(f"\nFound {len(results)} channels:")
            for ch in results:
                print(f"\n{ch['name']}")
                print(f"  ID: {ch['channel_id']}")
                print(f"  {ch['description']}")

        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  list              - List all monitored channels")
            print("  add <name> <id>   - Add channel by name and ID")
            print("  search <query>    - Search for channels")
            print("  (no command)      - Interactive mode")
            sys.exit(1)
    else:
        # Interactive mode
        interactive_add()


if __name__ == "__main__":
    main()
