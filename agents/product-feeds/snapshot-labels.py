#!/usr/bin/env python3
"""
Fetch Product Hero labels using Google Ads API directly with pagination.

This bypasses MCP token limits by using the native Google Ads API pagination
to fetch ALL products regardless of account size.

Usage:
    python3 fetch_labels_api.py <client-name>
    python3 fetch_labels_api.py --all
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Load configuration
CONFIG_FILE = Path(__file__).parent / "config.json"
GOOGLE_ADS_CONFIG = Path.home() / "google-ads.yaml"

def load_config():
    """Load client configuration"""
    with open(CONFIG_FILE) as f:
        return json.load(f)

def fetch_all_labels_for_client(client_config):
    """
    Fetch ALL product labels for a client using Google Ads API pagination.

    Args:
        client_config: Dict with client configuration including:
            - name: Client name
            - google_ads_customer_id: Customer ID
            - label_tracking: Dict with label_field, etc.

    Returns:
        Dict of {product_id: label} for all products
    """
    customer_id = client_config["google_ads_customer_id"]
    label_field = client_config["label_tracking"]["label_field"]

    # Map custom_label_N to segments field name
    label_number = label_field.split("_")[-1]
    segments_field = f"segments.product_custom_attribute{label_number}"

    print(f"\n{'='*80}")
    print(f"FETCHING LABELS: {client_config['name']}")
    print(f"{'='*80}")
    print(f"Customer ID: {customer_id}")
    print(f"Label Field: {label_field} → {segments_field}")

    # Check for manager_id
    manager_id = client_config["label_tracking"].get("manager_id")
    if manager_id:
        print(f"Manager ID: {manager_id}")

    # Initialize Google Ads client
    try:
        client = GoogleAdsClient.load_from_storage(str(GOOGLE_ADS_CONFIG))
    except Exception as e:
        print(f"\n❌ ERROR: Could not load Google Ads client: {e}")
        print(f"\nMake sure {GOOGLE_ADS_CONFIG} exists and is properly configured.")
        return None

    ga_service = client.get_service("GoogleAdsService")

    # Build query
    query = f"""
        SELECT
          segments.product_item_id,
          {segments_field}
        FROM shopping_performance_view
        WHERE segments.date DURING LAST_7_DAYS
          AND metrics.impressions > 0
    """

    # Use manager_id if specified (for sub-accounts)
    if manager_id:
        login_customer_id = manager_id
    else:
        login_customer_id = customer_id

    all_labels = {}
    page_count = 0

    try:
        # Create request with pagination
        request = client.get_type("SearchGoogleAdsStreamRequest")
        request.customer_id = customer_id
        request.query = query

        # Stream results (handles pagination automatically)
        print(f"\nFetching products...")

        stream = ga_service.search_stream(request=request)

        for batch in stream:
            page_count += 1
            for row in batch.results:
                product_id = row.segments.product_item_id

                # Extract label from the appropriate custom attribute
                label_value = getattr(row.segments, f"product_custom_attribute{label_number}", None)

                if product_id and label_value:
                    label_lower = label_value.lower()
                    if label_lower in ["heroes", "sidekicks", "villains", "zombies"]:
                        all_labels[product_id] = label_lower

            print(f"  Page {page_count}: {len(all_labels)} products so far...")

        print(f"\n✅ Complete: Fetched {len(all_labels)} products with labels")

        # Calculate distribution
        distribution = {}
        for label in all_labels.values():
            distribution[label] = distribution.get(label, 0) + 1

        print(f"Distribution: {distribution}")

        return all_labels

    except GoogleAdsException as ex:
        print(f"\n❌ Google Ads API Error:")
        for error in ex.failure.errors:
            print(f"  Error: {error.error_code.error_code}")
            print(f"  Message: {error.message}")
            if error.location:
                for field in error.location.field_path_elements:
                    print(f"  Field: {field.field_name}")
        return None

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None

def save_labels(client_name, labels, label_field, notes=None):
    """
    Save current label snapshot and create dated backup.

    Args:
        client_name: Client folder name
        labels: Dict of {product_id: label}
        label_field: Custom label field used
        notes: Optional notes
    """
    client_dir = Path(__file__).parent / "history" / "label-transitions" / client_name
    client_dir.mkdir(parents=True, exist_ok=True)

    snapshot = {
        "last_updated": datetime.now().isoformat(),
        "source": "google_ads_api",
        "label_field": label_field,
        "products": labels,
        "total_products": len(labels)
    }

    if notes:
        snapshot["notes"] = notes

    # Calculate distribution
    distribution = {}
    for label in labels.values():
        distribution[label] = distribution.get(label, 0) + 1
    snapshot["distribution"] = distribution

    # Save as current-labels.json
    current_file = client_dir / "current-labels.json"
    with open(current_file, 'w') as f:
        json.dump(snapshot, f, indent=2)

    print(f"\n💾 Saved to: {current_file}")

    # Also save dated backup
    dated_file = client_dir / f"{datetime.now().strftime('%Y-%m-%d')}_labels.json"
    with open(dated_file, 'w') as f:
        json.dump(snapshot, f, indent=2)

    print(f"💾 Backup: {dated_file}")

def detect_transitions(client_name):
    """
    Compare current labels to previous snapshot and detect transitions.

    Returns:
        List of dicts with transition details
    """
    client_dir = Path(__file__).parent / "history" / "label-transitions" / client_name
    current_file = client_dir / "current-labels.json"

    if not current_file.exists():
        print(f"No current snapshot for {client_name}")
        return []

    # Load current snapshot
    with open(current_file) as f:
        current_snapshot = json.load(f)

    current_labels = current_snapshot["products"]

    # Find most recent dated backup (excluding today)
    today = datetime.now().strftime('%Y-%m-%d')
    dated_files = sorted([
        f for f in client_dir.glob("*_labels.json")
        if not f.name.startswith(today)
    ], reverse=True)

    if not dated_files:
        print(f"No previous snapshot for comparison")
        return []

    previous_file = dated_files[0]
    previous_date = previous_file.stem.split('_')[0]

    print(f"\n{'='*80}")
    print(f"DETECTING TRANSITIONS: {client_name}")
    print(f"{'='*80}")
    print(f"Comparing to: {previous_date}")

    with open(previous_file) as f:
        previous_snapshot = json.load(f)

    previous_labels = previous_snapshot["products"]

    # Find transitions
    transitions = []

    for product_id, current_label in current_labels.items():
        if product_id in previous_labels:
            previous_label = previous_labels[product_id]

            if current_label != previous_label:
                transitions.append({
                    "product_id": product_id,
                    "from": previous_label,
                    "to": current_label,
                    "date": datetime.now().strftime('%Y-%m-%d'),
                    "previous_date": previous_date
                })

    # Also check for new products (not in previous snapshot)
    new_products = set(current_labels.keys()) - set(previous_labels.keys())
    for product_id in new_products:
        transitions.append({
            "product_id": product_id,
            "from": None,
            "to": current_labels[product_id],
            "date": datetime.now().strftime('%Y-%m-%d'),
            "previous_date": previous_date,
            "note": "New product"
        })

    # Check for removed products (in previous but not current)
    removed_products = set(previous_labels.keys()) - set(current_labels.keys())
    for product_id in removed_products:
        transitions.append({
            "product_id": product_id,
            "from": previous_labels[product_id],
            "to": None,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "previous_date": previous_date,
            "note": "Product removed/no impressions"
        })

    if transitions:
        print(f"\n🔄 Found {len(transitions)} transitions:")
        for t in transitions[:10]:  # Show first 10
            if t.get("note"):
                print(f"  {t['product_id']}: {t['from']} → {t['to']} ({t['note']})")
            else:
                print(f"  {t['product_id']}: {t['from']} → {t['to']}")

        if len(transitions) > 10:
            print(f"  ... and {len(transitions) - 10} more")
    else:
        print(f"\n✅ No label transitions detected")

    return transitions

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 fetch_labels_api.py <client-name>")
        print("  python3 fetch_labels_api.py --all")
        print()
        print("Examples:")
        print("  python3 fetch_labels_api.py uno-lighting")
        print("  python3 fetch_labels_api.py accessories-for-the-home")
        print("  python3 fetch_labels_api.py --all")
        return

    # Load config
    config = load_config()

    if sys.argv[1] == "--all":
        # Fetch for all enabled clients
        clients_to_fetch = [
            c for c in config["clients"]
            if c.get("enabled") and c.get("label_tracking", {}).get("enabled")
        ]

        print(f"\n{'='*80}")
        print(f"FETCHING LABELS FOR {len(clients_to_fetch)} CLIENTS")
        print(f"{'='*80}")

        results = []
        for client in clients_to_fetch:
            labels = fetch_all_labels_for_client(client)

            if labels is not None:
                save_labels(
                    client["name"].lower().replace(" ", "-"),
                    labels,
                    client["label_tracking"]["label_field"],
                    client["label_tracking"].get("notes")
                )

                # Detect transitions
                transitions = detect_transitions(
                    client["name"].lower().replace(" ", "-")
                )

                results.append({
                    "client": client["name"],
                    "products": len(labels),
                    "transitions": len(transitions)
                })

        print(f"\n{'='*80}")
        print(f"SUMMARY")
        print(f"{'='*80}")
        for r in results:
            print(f"{r['client']}: {r['products']} products, {r['transitions']} transitions")

    else:
        # Fetch for specific client
        client_name = sys.argv[1]

        # Find client in config
        client = None
        for c in config["clients"]:
            if c["name"].lower().replace(" ", "-") == client_name:
                client = c
                break

        if not client:
            print(f"❌ Client not found: {client_name}")
            print("\nAvailable clients:")
            for c in config["clients"]:
                if c.get("label_tracking", {}).get("enabled"):
                    print(f"  - {c['name'].lower().replace(' ', '-')}")
            return

        # Fetch labels
        labels = fetch_all_labels_for_client(client)

        if labels is not None:
            save_labels(
                client_name,
                labels,
                client["label_tracking"]["label_field"],
                client["label_tracking"].get("notes")
            )

            # Detect transitions
            transitions = detect_transitions(client_name)

if __name__ == "__main__":
    main()
