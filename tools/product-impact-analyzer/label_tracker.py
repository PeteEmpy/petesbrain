#!/usr/bin/env python3
"""
Product Hero Label Tracker - Daily Prospective Tracking

Tracks Product Hero label assignments (heroes, sidekicks, villains, zombies)
daily for all enabled e-commerce clients.

Stores:
- Current labels snapshot (current-labels.json)
- Transitions only (monthly files: YYYY-MM.json)

Usage:
    python label_tracker.py --all-clients
    python label_tracker.py --client "Accessories for the Home"

Schedule: Daily at 10:00 AM (via LaunchAgent)
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict

def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, 'r') as f:
        return json.load(f)

def get_history_dir(client_name):
    """Get or create history directory for client"""
    base_dir = Path(__file__).parent / "history" / "label-transitions"
    client_dir = base_dir / client_name.lower().replace(" ", "-")
    client_dir.mkdir(parents=True, exist_ok=True)
    return client_dir

def load_current_labels(client_name):
    """Load current labels snapshot for a client"""
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
    """Load transitions for a specific month (YYYY-MM)"""
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
    """Save transitions for a month"""
    history_dir = get_history_dir(client_name)
    monthly_file = history_dir / f"{year_month}.json"

    with open(monthly_file, 'w') as f:
        json.dump(transitions_data, f, indent=2)

def fetch_current_labels_from_ads(customer_id, label_field="custom_label_0", manager_id=None):
    """
    Fetch current Product Hero labels from Google Ads API via MCP.

    NOTE: This script should be run by Claude Code which has access to MCP tools.
    Direct execution will fail without MCP access.

    Returns: dict of {product_id: label}
    """
    print(f"  📊 Querying Google Ads for label field: {label_field}")

    # Map custom_label field name to segments field
    field_mapping = {
        "custom_label_0": "product_custom_attribute0",
        "custom_label_1": "product_custom_attribute1",
        "custom_label_2": "product_custom_attribute2",
        "custom_label_3": "product_custom_attribute3",
        "custom_label_4": "product_custom_attribute4"
    }

    segment_field = field_mapping.get(label_field, "product_custom_attribute0")

    query = f"""
    SELECT
      segments.product_item_id,
      segments.{segment_field}
    FROM shopping_performance_view
    WHERE segments.date DURING LAST_7_DAYS
      AND metrics.impressions > 0
    LIMIT 10000
    """

    # This function is designed to be called by Claude Code with MCP access
    # Manual execution should use: claude code run label_tracker.py --all-clients
    print(f"  ⚠️  This script requires Claude Code with MCP access")
    print(f"  ⚠️  Run via: claude code run {Path(__file__).name} --all-clients")
    print(f"")
    print(f"  MCP Call Details:")
    print(f"    Tool: mcp__google-ads__run_gaql")
    print(f"    Customer ID: {customer_id}")
    print(f"    Manager ID: {manager_id or 'None'}")
    print(f"    Query: {query.strip()}")
    print(f"")

    return {}

def detect_transitions(old_labels, new_labels):
    """
    Compare old and new labels to detect transitions.

    Returns: list of transitions [
        {
            "product_id": "287",
            "from": "sidekicks",
            "to": "heroes",
            "date": "2025-11-01"
        },
        ...
    ]
    """
    transitions = []
    today = date.today().isoformat()

    # Check for label changes
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

def track_labels_for_client(client_config):
    """Track labels for a single client"""
    client_name = client_config["name"]
    customer_id = client_config["google_ads_customer_id"]

    # Check if label tracking is enabled
    label_config = client_config.get("label_tracking", {})
    if not label_config.get("enabled", False):
        print(f"  ⏭️  Label tracking not enabled for {client_name}")
        return

    label_field = label_config.get("label_field", "custom_label_0")

    print(f"\n{'='*60}")
    print(f"Tracking labels: {client_name}")
    print(f"{'='*60}")

    # Load previous labels
    previous_snapshot = load_current_labels(client_name)
    previous_labels = previous_snapshot.get("products", {})

    # Fetch current labels from Google Ads
    current_labels = fetch_current_labels_from_ads(customer_id, label_field)

    if not current_labels:
        print(f"  ⚠️  No labels fetched (MCP integration needed)")
        return

    # Detect transitions
    transitions = detect_transitions(previous_labels, current_labels)

    if transitions:
        print(f"  📊 Detected {len(transitions)} label transition(s):")
        for t in transitions:
            print(f"     Product {t['product_id']}: {t['from']} → {t['to']}")

        # Save to monthly transitions file
        today = date.today()
        year_month = today.strftime("%Y-%m")
        monthly_data = load_monthly_transitions(client_name, year_month)
        monthly_data["transitions"].extend(transitions)
        save_monthly_transitions(client_name, year_month, monthly_data)

        print(f"  ✅ Saved to {year_month}.json")
    else:
        print(f"  ✓ No label changes detected")

    # Update current snapshot
    current_snapshot = {
        "last_updated": datetime.now().isoformat(),
        "source": "actual",
        "products": current_labels
    }
    save_current_labels(client_name, current_snapshot)
    print(f"  ✅ Updated current-labels.json")

def main():
    """Main tracking process"""
    import argparse

    parser = argparse.ArgumentParser(description="Track Product Hero label changes")
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

    print(f"\n🏷️  Product Hero Label Tracker")
    print(f"{'='*60}")
    print(f"Tracking {len(clients)} client(s)")
    print(f"Date: {date.today().isoformat()}")
    print(f"{'='*60}\n")

    for client in clients:
        try:
            track_labels_for_client(client)
        except Exception as e:
            print(f"❌ Error tracking {client['name']}: {e}")
            continue

    print(f"\n{'='*60}")
    print("✅ Label tracking complete")
    print(f"{'='*60}\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
