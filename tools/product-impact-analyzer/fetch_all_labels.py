#!/usr/bin/env python3
"""
Fetch Product Hero Labels for All Clients

This script is designed to be run BY CLAUDE CODE manually or on-demand.
It fetches labels via MCP and saves them locally.

The LaunchAgent then runs label_tracking_executor.py which processes
the saved data (doesn't require MCP access).

Usage:
    # Run via Claude Code (has MCP access)
    claude code: "Run fetch_all_labels.py"

    # Or manually if API keys configured
    python3 fetch_all_labels.py
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from label_tracking_executor import (
    load_config,
    generate_label_query,
    track_client_labels
)


def main():
    """
    Main entry point.

    IMPORTANT: This script must be run by Claude Code which has MCP access.
    It will generate a list of MCP queries that Claude Code should execute.
    """
    print("=" * 70)
    print("🏷️  Product Hero Label Fetcher")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Load configuration
    config_path = Path(__file__).parent / "config.json"
    config = load_config()

    # Get enabled clients with label tracking
    enabled_clients = [
        c for c in config["clients"]
        if c.get("label_tracking", {}).get("enabled", False)
    ]

    if not enabled_clients:
        print("❌ No clients with label tracking enabled")
        return 1

    print(f"📋 Found {len(enabled_clients)} clients with label tracking enabled:")
    for client in enabled_clients:
        label_config = client.get("label_tracking", {})
        notes = label_config.get("notes", "")
        print(f"   • {client['name']}")
        if notes:
            print(f"     Note: {notes}")
    print()

    print("=" * 70)
    print("⚠️  IMPORTANT: This script requires Claude Code to execute MCP calls")
    print("=" * 70)
    print()
    print("Claude Code should execute the following MCP queries for each client:")
    print("Then pass the responses to track_client_labels() function.")
    print()

    # Generate queries for all clients
    queries_by_client = {}

    for client in enabled_clients:
        label_config = client.get("label_tracking", {})
        label_field = label_config.get("label_field", "custom_label_0")
        manager_id = label_config.get("manager_id")
        customer_id = client["google_ads_customer_id"]

        # For large accounts, use LIMIT 500
        # Check if client has "partial coverage" note
        notes = label_config.get("notes", "")
        limit = 500 if "partial coverage" in notes.lower() else 10000

        query_info = generate_label_query(
            customer_id=customer_id,
            label_field=label_field,
            manager_id=manager_id,
            limit=limit
        )

        queries_by_client[client["name"]] = {
            "config": client,
            "query": query_info
        }

        print(f"📊 {client['name']}")
        print(f"   Customer ID: {customer_id}")
        if manager_id:
            print(f"   Manager ID: {manager_id}")
        print(f"   Label Field: {label_field}")
        print(f"   Limit: {limit}")
        print()

    # Save queries for Claude Code to execute
    queries_file = Path(__file__).parent / "pending_label_queries.json"
    with open(queries_file, 'w') as f:
        json.dump(queries_by_client, f, indent=2)

    print(f"✅ Generated {len(queries_by_client)} MCP queries")
    print(f"   Saved to: {queries_file}")
    print()
    print("=" * 70)
    print("NEXT STEPS FOR CLAUDE CODE:")
    print("=" * 70)
    print()
    print("1. Load pending_label_queries.json")
    print("2. For each client, execute the MCP query:")
    print("   mcp__google-ads__run_gaql(customer_id, query, manager_id)")
    print("3. Pass response to track_client_labels(client_config, mcp_response)")
    print("4. Repeat for all clients")
    print()
    print("This will update all current-labels.json files and detect transitions.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
