#!/usr/bin/env python3
"""
Product Hero Label Tracking Executor

This script is executed BY Claude Code, which provides MCP integration.
It tracks Product Hero label assignments and transitions.

Usage by Claude Code:
    Execute this script with --all-clients or --client NAME
    The script will request MCP calls which Claude Code executes inline
"""

import json
import sys
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict


def load_config():
    """Load configuration"""
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, 'r') as f:
        return json.load(f)


def get_history_dir(client_name):
    """Get or create history directory"""
    base_dir = Path(__file__).parent / "history" / "label-transitions"
    client_dir = base_dir / client_name.lower().replace(" ", "-")
    client_dir.mkdir(parents=True, exist_ok=True)
    return client_dir


def load_current_labels(client_name):
    """Load current labels snapshot"""
    history_dir = get_history_dir(client_name)
    current_file = history_dir / "current-labels.json"

    if current_file.exists():
        with open(current_file, 'r') as f:
            return json.load(f)
    else:
        return {
            "last_updated": None,
            "source": "actual",
            "products": {}
        }


def save_current_labels(client_name, labels_data):
    """Save current labels snapshot"""
    history_dir = get_history_dir(client_name)
    current_file = history_dir / "current-labels.json"

    with open(current_file, 'w') as f:
        json.dump(labels_data, f, indent=2)


def load_monthly_transitions(client_name, year_month):
    """Load monthly transitions"""
    history_dir = get_history_dir(client_name)
    monthly_file = history_dir / f"{year_month}.json"

    if monthly_file.exists():
        with open(monthly_file, 'r') as f:
            return json.load(f)
    else:
        return {
            "month": year_month,
            "transitions": []
        }


def save_monthly_transitions(client_name, year_month, transitions_data):
    """Save monthly transitions"""
    history_dir = get_history_dir(client_name)
    monthly_file = history_dir / f"{year_month}.json"

    with open(monthly_file, 'w') as f:
        json.dump(transitions_data, f, indent=2)


def parse_mcp_response(response_data, segment_field):
    """
    Parse MCP response and extract Product Hero labels.

    Args:
        response_data: Raw MCP response (dict with 'results')
        segment_field: Field name to extract (e.g., 'product_custom_attribute3')

    Returns:
        dict of {product_id: label}
    """
    labels = {}

    # Convert field name to camelCase for API response
    camel_field = ''.join(word.capitalize() if i > 0 else word
                          for i, word in enumerate(segment_field.split('_')))
    # Fix: productCustomAttribute not ProductCustomAttribute
    if camel_field.startswith('Product'):
        camel_field = 'product' + camel_field[7:]

    if "results" in response_data:
        for row in response_data["results"]:
            product_id = row.get("segments", {}).get("productItemId")
            label_value = row.get("segments", {}).get(camel_field, "").lower()

            # Only store valid Product Hero labels
            if label_value in ["heroes", "sidekicks", "villains", "zombies"]:
                labels[product_id] = label_value

    return labels


def generate_label_query(customer_id, label_field, manager_id=None, limit=10000):
    """
    Generate GAQL query for fetching Product Hero labels.

    Note: GAQL has significant pagination limitations:
    - No OFFSET support
    - No comparison operators (>, <) on product_item_id
    - Cannot paginate using WHERE product_item_id > 'last_id'

    For large accounts (>500 products), LIMIT restricts to first N products alphabetically.
    This provides partial coverage but still enables transition tracking.

    Args:
        customer_id: Google Ads customer ID
        label_field: custom_label_N field name
        manager_id: Optional manager ID
        limit: Maximum products to fetch (default 10000, max before token limit ~500-1000)

    Returns:
        Query dict
    """
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
ORDER BY segments.product_item_id
LIMIT {limit}"""

    return {
        "customer_id": customer_id,
        "manager_id": manager_id,
        "query": query,
        "limit": limit
    }


def detect_transitions(old_labels, new_labels):
    """Detect label transitions"""
    transitions = []
    today = date.today().isoformat()

    all_products = set(old_labels.keys()) | set(new_labels.keys())

    for product_id in all_products:
        old_label = old_labels.get(product_id)
        new_label = new_labels.get(product_id)

        if old_label != new_label and old_label is not None and new_label is not None:
            transitions.append({
                "product_id": product_id,
                "date": today,
                "from": old_label,
                "to": new_label,
                "confidence": "actual",
                "source": "product_hero_daily_sync"
            })

    return transitions


def track_client_labels(client_config, mcp_responses):
    """
    Track labels for a client using MCP response(s).

    Args:
        client_config: Client configuration dict
        mcp_responses: MCP API response (parsed JSON) or list of responses for pagination
    """
    client_name = client_config["name"]
    label_config = client_config.get("label_tracking", {})
    label_field = label_config.get("label_field", "custom_label_0")

    # Map to segment field
    field_mapping = {
        "custom_label_0": "product_custom_attribute0",
        "custom_label_1": "product_custom_attribute1",
        "custom_label_2": "product_custom_attribute2",
        "custom_label_3": "product_custom_attribute3",
        "custom_label_4": "product_custom_attribute4"
    }
    segment_field = field_mapping.get(label_field, "product_custom_attribute0")

    print(f"\n{'='*70}")
    print(f"🏷️  {client_name}")
    print(f"{'='*70}")

    # Load previous labels
    previous_snapshot = load_current_labels(client_name)
    previous_labels = previous_snapshot.get("products", {})
    print(f"  ✓ Previous snapshot: {len(previous_labels)} products")

    # Handle both single response and list of paginated responses
    if not isinstance(mcp_responses, list):
        mcp_responses = [mcp_responses]

    # Parse and merge labels from all responses
    current_labels = {}
    for i, response in enumerate(mcp_responses, 1):
        batch_labels = parse_mcp_response(response, segment_field)
        current_labels.update(batch_labels)
        if len(mcp_responses) > 1:
            print(f"  ✓ Batch {i}/{len(mcp_responses)}: {len(batch_labels)} products")

    print(f"  ✓ Total current labels: {len(current_labels)} products")

    # Detect transitions
    transitions = detect_transitions(previous_labels, current_labels)

    if transitions:
        print(f"\n  📊 Detected {len(transitions)} transition(s):")
        for t in transitions[:10]:  # Show first 10
            print(f"     • Product {t['product_id']}: {t['from']} → {t['to']}")
        if len(transitions) > 10:
            print(f"     ... and {len(transitions) - 10} more")

        # Save to monthly file
        today = date.today()
        year_month = today.strftime("%Y-%m")
        monthly_data = load_monthly_transitions(client_name, year_month)
        monthly_data["transitions"].extend(transitions)
        save_monthly_transitions(client_name, year_month, monthly_data)

        print(f"\n  ✅ Saved {len(transitions)} transition(s) to {year_month}.json")
    else:
        print(f"  ✓ No label changes detected")

    # Update current snapshot
    current_snapshot = {
        "last_updated": datetime.now().isoformat(),
        "source": "actual",
        "label_field": label_field,
        "products": current_labels
    }
    save_current_labels(client_name, current_snapshot)
    print(f"  ✅ Updated current-labels.json")


def main():
    """
    Main entry point - displays instructions for Claude Code.

    This script doesn't execute MCP calls directly.
    It's designed to be run BY Claude Code step-by-step.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Track Product Hero labels via Claude Code")
    parser.add_argument("--client", help="Track specific client")
    parser.add_argument("--all-clients", action="store_true", help="Track all enabled clients")
    parser.add_argument("--test-parse", help="Test parsing with MCP response file")
    args = parser.parse_args()

    config = load_config()

    # Test mode - parse a saved MCP response
    if args.test_parse:
        test_file = Path(args.test_parse)
        if not test_file.exists():
            print(f"Error: Test file not found: {test_file}")
            return 1

        with open(test_file, 'r') as f:
            test_data = json.load(f)

        client_name = test_data.get("client_name", "Test Client")
        mcp_response = test_data.get("mcp_response", {})

        # Find client config
        client_config = next(
            (c for c in config["clients"] if c["name"] == client_name),
            None
        )

        if not client_config:
            print(f"Error: Client '{client_name}' not found in config")
            return 1

        track_client_labels(client_config, mcp_response)
        return 0

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
    print(f"🏷️  Product Hero Label Tracker")
    print(f"{'='*70}")
    print(f"Date: {date.today().isoformat()}")
    print(f"Clients: {len(clients)}")
    print(f"{'='*70}\n")

    print("📋 This script requires Claude Code to execute MCP calls.")
    print("   Claude Code should:")
    print("   1. Run this script")
    print("   2. For each client below, execute the MCP call")
    print("   3. Pass the response back to track_client_labels()")
    print()

    # Output MCP requests needed
    for client in clients:
        label_config = client.get("label_tracking", {})
        label_field = label_config.get("label_field", "custom_label_0")
        manager_id = label_config.get("manager_id")

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

        print(f"Client: {client['name']}")
        print(f"  MCP Tool: mcp__google-ads__run_gaql")
        print(f"  Customer ID: {client['google_ads_customer_id']}")
        if manager_id:
            print(f"  Manager ID: {manager_id}")
        print(f"  Label Field: {label_field} ({segment_field})")
        print(f"  Query: {query[:80]}...")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
