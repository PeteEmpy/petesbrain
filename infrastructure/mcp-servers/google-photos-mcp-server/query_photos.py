#!/usr/bin/env python3
"""
Quick script to query Google Photos directly
"""

import sys
import json
from pathlib import Path

# Add server directory to path
sys.path.insert(0, str(Path(__file__).parent))

from server import GooglePhotosService

def main():
    try:
        service = GooglePhotosService()

        # List albums
        print("📷 Your Google Photos Albums:\n")
        result = service.list_albums(page_size=20)

        albums = result.get('albums', [])
        if not albums:
            print("No albums found.")
            return

        for i, album in enumerate(albums, 1):
            print(f"{i}. {album['title']}")
            print(f"   Items: {album.get('mediaItemsCount', 'Unknown')}")
            print(f"   URL: {album['productUrl']}")
            print()

        print(f"Total albums shown: {len(albums)}")
        if result.get('nextPageToken'):
            print("(More albums available)")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
