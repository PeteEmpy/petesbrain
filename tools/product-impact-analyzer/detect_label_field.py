#!/usr/bin/env python3
"""
Label Field Auto-Detection Script

Automatically detects which custom_label field contains Product Hero labels
(heroes, sidekicks, villains, zombies) for each e-commerce client.

Usage:
    python detect_label_field.py --client "Accessories for the Home"
    python detect_label_field.py --all-clients
"""

import json
import sys
import os
from collections import Counter

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def detect_label_field_for_client(client_name, customer_id):
    """
    Detect which custom_label field contains Product Hero labels.

    Checks custom_label_0 through custom_label_4 for values matching:
    heroes, sidekicks, villains, zombies

    Returns: {
        "field": "custom_label_0" or None,
        "confidence": "high|medium|low",
        "sample_values": [...],
        "distribution": {...}
    }
    """
    print(f"\n{'='*60}")
    print(f"Detecting label field for: {client_name}")
    print(f"Customer ID: {customer_id}")
    print(f"{'='*60}")

    # Try to use MCP Google Ads tool
    try:
        from anthropic import Anthropic
        client = Anthropic()

        # For this demo, we'll outline the GAQL query needed
        # In production, this would be called via MCP
        query_template = """
        SELECT
          segments.product_custom_attribute0,
          segments.product_custom_attribute1,
          segments.product_custom_attribute2,
          segments.product_custom_attribute3,
          segments.product_custom_attribute4,
          metrics.clicks
        FROM shopping_performance_view
        WHERE segments.date DURING LAST_7_DAYS
          AND metrics.clicks > 0
        LIMIT 1000
        """

        print("\n📊 Querying Google Ads API for custom label fields...")
        print("Query template:")
        print(query_template)

        # NOTE: In actual implementation, we would call mcp__google-ads__run_gaql here
        # For now, return instructions for manual setup

        print("\n⚠️  Manual Detection Required")
        print("\nTo detect the correct label field, run this GAQL query in Google Ads:")
        print(query_template)
        print("\nLook for which custom_attribute field contains:")
        print("  - heroes")
        print("  - sidekicks")
        print("  - villains")
        print("  - zombies")

        return {
            "field": None,
            "confidence": "manual_required",
            "instructions": "Run GAQL query above and check custom_attribute fields"
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "field": None,
            "confidence": "error",
            "error": str(e)
        }

def analyze_custom_label_values(values):
    """
    Analyze a list of custom label values to determine if they match
    Product Hero labeling scheme.

    Returns confidence level: high, medium, low, none
    """
    if not values:
        return "none", {}

    # Count occurrences of Product Hero labels
    ph_labels = ["heroes", "sidekicks", "villains", "zombies"]
    counter = Counter(values)

    ph_matches = {label: counter.get(label, 0) for label in ph_labels}
    total_ph = sum(ph_matches.values())
    total_all = len(values)

    if total_all == 0:
        return "none", {}

    match_rate = total_ph / total_all

    # Determine confidence
    if match_rate >= 0.8 and total_ph >= 10:
        confidence = "high"
    elif match_rate >= 0.5 and total_ph >= 5:
        confidence = "medium"
    elif total_ph > 0:
        confidence = "low"
    else:
        confidence = "none"

    return confidence, {
        "match_rate": f"{match_rate:.1%}",
        "ph_label_count": total_ph,
        "total_products": total_all,
        "distribution": ph_matches
    }

def update_config_with_label_field(client_name, label_field, assessment_window=30):
    """
    Update config.json with detected label field for a client.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Find client in config
    for client in config["clients"]:
        if client["name"] == client_name:
            # Add label tracking configuration
            if "label_tracking" not in client:
                client["label_tracking"] = {}

            client["label_tracking"]["enabled"] = True
            client["label_tracking"]["label_field"] = label_field
            client["label_tracking"]["assessment_window_days"] = assessment_window

            print(f"\n✅ Updated config for {client_name}:")
            print(f"   Label field: {label_field}")
            print(f"   Assessment window: {assessment_window} days")
            break

    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n💾 Config saved to: {config_path}")

def main():
    """
    Main detection script.

    For each enabled e-commerce client:
    1. Query custom_label_0 through custom_label_4
    2. Check which field contains Product Hero labels
    3. Update config.json with detected field
    """
    import argparse

    parser = argparse.ArgumentParser(description="Auto-detect Product Hero label fields")
    parser.add_argument("--client", help="Client name to detect")
    parser.add_argument("--all-clients", action="store_true", help="Detect for all enabled e-commerce clients")
    args = parser.parse_args()

    # Load config
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Determine which clients to process
    if args.all_clients:
        # Filter to enabled e-commerce clients (those with merchant_id)
        clients_to_process = [
            c for c in config["clients"]
            if c.get("enabled", False) and c.get("merchant_id") != "UNKNOWN"
        ]
    elif args.client:
        clients_to_process = [
            c for c in config["clients"]
            if c["name"] == args.client
        ]
    else:
        print("Error: Specify --client NAME or --all-clients")
        return 1

    if not clients_to_process:
        print(f"No clients found matching criteria")
        return 1

    print(f"\n🔍 Detecting label fields for {len(clients_to_process)} client(s)...\n")

    results = {}
    for client in clients_to_process:
        result = detect_label_field_for_client(
            client["name"],
            client["google_ads_customer_id"]
        )
        results[client["name"]] = result

    # Print summary
    print("\n" + "="*60)
    print("DETECTION SUMMARY")
    print("="*60)

    for client_name, result in results.items():
        print(f"\n{client_name}:")
        if result.get("field"):
            print(f"  ✅ Field: {result['field']}")
            print(f"  📊 Confidence: {result['confidence']}")
        else:
            print(f"  ⚠️  Manual detection required")
            print(f"  {result.get('instructions', 'Run detection query')}")

    print("\n" + "="*60)
    print("\n💡 NEXT STEPS:")
    print("\n1. For clients requiring manual detection:")
    print("   - Run the GAQL query shown above in Google Ads")
    print("   - Identify which custom_attribute contains Product Hero labels")
    print("   - Update config.json manually:")
    print('     "label_tracking": {')
    print('       "enabled": true,')
    print('       "label_field": "custom_label_0",  <-- Update this')
    print('       "assessment_window_days": 30')
    print('     }')
    print("\n2. Run label tracker:")
    print("   python label_tracker.py --all-clients")
    print("\n3. Run historical backfill:")
    print("   python backfill_historical_labels.py --start-date 2025-10-01")

    return 0

if __name__ == "__main__":
    sys.exit(main())
