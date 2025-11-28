#!/usr/bin/env python3
"""
Google Drive Granola Document Fetcher

Helper script that uses Google Drive MCP to fetch Granola documents.
This can be called from the main importer or run standalone.

Usage:
    python3 fetch-granola-docs.py [--days 7] [--output json]
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# This script is designed to be run via Claude Code with MCP access
# It will use the Google Drive MCP server to search for documents


def search_granola_docs(days: int = 7) -> list:
    """
    Search Google Drive for Granola documents.
    
    This function should be called from within Claude Code where
    MCP tools are available. It uses the Google Drive MCP server.
    
    Args:
        days: Number of days to look back
    
    Returns:
        List of document dictionaries with 'id', 'name', 'modified_time', 'content'
    """
    # Note: This function is designed to be called from Claude Code
    # where MCP tools are available. For standalone use, you'll need
    # to implement direct Google Drive API calls.
    
    print("=" * 60)
    print("Searching Google Drive for Granola documents...")
    print("=" * 60)
    print()
    
    # Calculate cutoff date
    cutoff_date = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff_date.strftime("%Y-%m-%d")
    
    print(f"Looking for documents modified after: {cutoff_str}")
    print(f"Pattern: 'ROK | Granola -'")
    print()
    
    # Instructions for Claude Code:
    # 1. Use mcp_google-drive-mcp-server_search_files to search for:
    #    - Query: "name contains 'ROK | Granola -'"
    #    - Modified time: after cutoff_date
    #    - In Shared Drive or "Shared with me"
    #
    # 2. For each document found, use mcp_google-drive-mcp-server_read_file
    #    to fetch the content
    #
    # 3. Return list of documents with:
    #    - id: document ID
    #    - name: document name
    #    - modified_time: last modified timestamp
    #    - content: full text content
    
    print("⚠️  This function requires MCP access to Google Drive")
    print("   Run this from Claude Code or implement direct API calls")
    print()
    
    return []


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch Granola documents from Google Drive"
    )
    
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Look back N days (default: 7)"
    )
    
    parser.add_argument(
        "--output",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    
    args = parser.parse_args()
    
    docs = search_granola_docs(days=args.days)
    
    if args.output == "json":
        print(json.dumps(docs, indent=2))
    else:
        print(f"\nFound {len(docs)} document(s):\n")
        for doc in docs:
            print(f"  • {doc['name']}")
            print(f"    ID: {doc['id']}")
            print(f"    Modified: {doc.get('modified_time', 'Unknown')}")
            print()


if __name__ == "__main__":
    main()

