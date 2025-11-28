#!/usr/bin/env python3
"""
Wrapper script for label_tracker.py that handles MCP integration.

This script is designed to be run by Claude Code, which has direct access
to MCP tools. It wraps the label tracking logic and provides MCP connectivity.

Usage (by Claude Code):
    python3 run_label_tracker.py --all-clients
    python3 run_label_tracker.py --client "Accessories for the Home"
"""

import json
import sys
from datetime import datetime, date
from pathlib import Path

# Import label tracker functions
from label_tracker import (
    load_config,
    get_history_dir,
    load_current_labels,
    save_current_labels,
    load_monthly_transitions,
    save_monthly_transitions,
    detect_transitions
)


def fetch_labels_via_mcp(customer_id, label_field, manager_id=None):
    """
    Fetch Product Hero labels using MCP tools.

    This function is called by Claude Code which has access to mcp__google-ads__run_gaql.
    When this script is executed, Claude Code will see the MCP call and execute it.

    Returns: dict of {product_id: label}
    """
    # Map custom_label field name to segments field
    field_mapping = {
        "custom_label_0": "product_custom_attribute0",
        "custom_label_1": "product_custom_attribute1",
        "custom_label_2": "product_custom_attribute2",
        "custom_label_3": "product_custom_attribute3",
        "custom_label_4": "product_custom_attribute4"
    }

    segment_field = field_mapping.get(label_field, "product_custom_attribute0")

    query = f"""SELECT
  segments.product_item_id,
  segments.{segment_field}
FROM shopping_performance_view
WHERE segments.date DURING LAST_7_DAYS
  AND metrics.impressions > 0
LIMIT 10000"""

    print(f"    📊 Fetching labels from Google Ads...")
    print(f"       Field: {label_field} ({segment_field})")
    print(f"       Customer ID: {customer_id}")
    if manager_id:
        print(f"       Manager ID: {manager_id}")

    # Return MCP call request
    # Claude Code will see this and execute the MCP tool
    return {
        "mcp_tool": "mcp__google-ads__run_gaql",
        "customer_id": customer_id,
        "manager_id": manager_id,
        "query": query,
        "segment_field": segment_field
    }


def track_client(client_config):
    """Track labels for a single client"""
    client_name = client_config["name"]
    customer_id = client_config["google_ads_customer_id"]

    # Check if label tracking is enabled
    label_config = client_config.get("label_tracking", {})
    if not label_config.get("enabled", False):
        print(f"  ⏭️  Label tracking not enabled for {client_name}")
        return

    label_field = label_config.get("label_field", "custom_label_0")
    manager_id = label_config.get("manager_id")

    print(f"\n{'='*70}")
    print(f"🏷️  {client_name}")
    print(f"{'='*70}")

    # Load previous labels
    previous_snapshot = load_current_labels(client_name)
    previous_labels = previous_snapshot.get("products", {})
    print(f"  ✓ Loaded previous snapshot: {len(previous_labels)} products")

    # Fetch current labels - return MCP request
    mcp_request = fetch_labels_via_mcp(customer_id, label_field, manager_id)

    # Output the MCP request for Claude Code to execute
    print(f"\n  🤖 MCP Request:")
    print(f"     Please execute: {mcp_request['mcp_tool']}")
    print(f"     customer_id: {mcp_request['customer_id']}")
    if mcp_request['manager_id']:
        print(f"     manager_id: {mcp_request['manager_id']}")
    print(f"     query: {mcp_request['query'][:100]}...")
    print(f"\n  ⏸️  Execution paused - Claude Code needs to run MCP tool")
    print(f"     (This is where Claude Code integration is needed)")

    return mcp_request


def main():
    """Main tracking process"""
    import argparse

    parser = argparse.ArgumentParser(description="Track Product Hero label changes via MCP")
    parser.add_argument("--client", help="Track specific client")
    parser.add_argument("--all-clients", action="store_true", help="Track all enabled clients")
    args = parser.parse_args()

    config = load_config()

    # Determine which clients to track
    if args.all_clients:
        clients = [
            c for c in config["clients"]
            if c.get("label_tracking", {}).get("enabled", False)
        ]
    elif args.client:
        clients = [c for c in config["clients"] if c["name"] == args.client]
    else:
        print("Error: Specify --client NAME or --all-clients")
        return 1

    if not clients:
        print("No clients found with label tracking enabled")
        return 1

    print(f"\n{'='*70}")
    print(f"🏷️  Product Hero Label Tracker (MCP Integration)")
    print(f"{'='*70}")
    print(f"Date: {date.today().isoformat()}")
    print(f"Clients to track: {len(clients)}")
    print(f"{'='*70}")

    mcp_requests = []

    for client in clients:
        try:
            request = track_client(client)
            if request:
                mcp_requests.append({
                    "client": client["name"],
                    "request": request
                })
        except Exception as e:
            print(f"\n❌ Error tracking {client['name']}: {e}")
            continue

    print(f"\n{'='*70}")
    print(f"📋 Summary:")
    print(f"   {len(mcp_requests)} MCP requests generated")
    print(f"   These need to be executed by Claude Code with MCP access")
    print(f"{'='*70}\n")

    # Output JSON for Claude Code to parse
    output_file = Path(__file__).parent / "mcp_requests.json"
    with open(output_file, 'w') as f:
        json.dump(mcp_requests, f, indent=2)

    print(f"✅ MCP requests saved to: {output_file}")
    print(f"\n💡 Next step: Claude Code should execute these MCP calls")

    return 0


if __name__ == "__main__":
    sys.exit(main())
