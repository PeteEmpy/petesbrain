#!/usr/bin/env python3
"""
Product Hero Label Tracker - Merchant Centre API Version

Tracks Product Hero label assignments (heroes, sidekicks, villains, zombies)
daily for all enabled e-commerce clients by querying Merchant Centre API.

Queries custom_label_0 through custom_label_4 to find which field contains
the Product Hero labels, then saves current snapshot and tracks transitions.

Usage:
    python label_tracker_merchant_centre.py --all-clients
    python label_tracker_merchant_centre.py --client "Tree2mydoor"
    python label_tracker_merchant_centre.py --dry-run

Schedule: Daily at 7:00 AM (via LaunchAgent)
"""

import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict
import argparse
from typing import Dict, List, Optional, Set
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Valid Product Hero label values
VALID_LABELS = {'heroes', 'sidekicks', 'villains', 'zombies', 'unknown'}

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
            "source": "merchant_centre_api",
            "label_field": None,
            "products": {}
        }

def save_current_labels(client_name, labels_data):
    """Save current labels snapshot"""
    history_dir = get_history_dir(client_name)
    current_file = history_dir / "current-labels.json"

    labels_data["last_updated"] = datetime.now().isoformat()

    with open(current_file, 'w') as f:
        json.dump(labels_data, f, indent=2)

    print(f"✅ Saved current labels for {client_name} ({len(labels_data['products'])} products)")

def save_transitions(client_name, transitions: List[Dict]):
    """Save label transitions to monthly file"""
    if not transitions:
        return

    history_dir = get_history_dir(client_name)
    month_str = date.today().strftime('%Y-%m')
    transitions_file = history_dir / f"{month_str}.json"

    # Load existing transitions for this month
    if transitions_file.exists():
        with open(transitions_file, 'r') as f:
            existing = json.load(f)
    else:
        existing = []

    # Append new transitions
    existing.extend(transitions)

    # Save back
    with open(transitions_file, 'w') as f:
        json.dump(existing, f, indent=2)

    print(f"✅ Saved {len(transitions)} transitions to {transitions_file.name}")

def detect_label_field(products: List[Dict]) -> Optional[str]:
    """
    Detect which custom_label field contains Product Hero labels.

    Returns the field name (e.g., 'customLabel0', 'customLabel1', etc.)
    or None if not found.
    """
    custom_label_fields = ['customLabel0', 'customLabel1', 'customLabel2', 'customLabel3', 'customLabel4']

    # Count how many products have valid labels in each field
    field_scores = defaultdict(int)

    for product in products:
        for field in custom_label_fields:
            value = product.get(field, '').lower().strip()
            if value in VALID_LABELS:
                field_scores[field] += 1

    if not field_scores:
        return None

    # Return field with most valid labels
    best_field = max(field_scores.items(), key=lambda x: x[1])

    # Only return if at least 10 products have valid labels
    if best_field[1] >= 10:
        return best_field[0]

    return None

def fetch_products_from_merchant_centre(merchant_id: str, credentials_path: str) -> List[Dict]:
    """
    Fetch all products from Merchant Centre API.

    Returns list of product dictionaries with custom labels.
    """
    print(f"📡 Fetching products from Merchant Centre (ID: {merchant_id})...")

    scopes = ['https://www.googleapis.com/auth/content']
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=scopes
    )

    service = build('content', 'v2.1', credentials=creds)

    products = []
    page_token = None

    while True:
        try:
            request = service.products().list(
                merchantId=merchant_id,
                maxResults=250,
                pageToken=page_token
            )
            response = request.execute()

            batch = response.get('resources', [])
            products.extend(batch)

            page_token = response.get('nextPageToken')
            if not page_token:
                break

            print(f"   Fetched {len(products)} products so far...")

        except HttpError as e:
            print(f"❌ Error fetching products: {e}")
            return []

    print(f"✅ Fetched {len(products)} total products")
    return products

def extract_labels_from_products(products: List[Dict], label_field: str) -> Dict[str, str]:
    """
    Extract Product Hero labels from products.

    Args:
        products: List of product dicts from Merchant Centre API
        label_field: The custom label field to use (e.g., 'customLabel3')

    Returns:
        Dictionary mapping product_id -> label
    """
    labels = {}

    for product in products:
        product_id = product.get('offerId')  # offerId is the SKU/product ID
        if not product_id:
            continue

        label_value = product.get(label_field, '').lower().strip()

        if label_value in VALID_LABELS:
            labels[product_id] = label_value

    return labels

def detect_transitions(old_labels: Dict[str, str], new_labels: Dict[str, str]) -> List[Dict]:
    """
    Detect label transitions between old and new snapshots.

    Returns list of transition dictionaries.
    """
    transitions = []
    today = date.today().isoformat()

    # All product IDs in either snapshot
    all_product_ids = set(old_labels.keys()) | set(new_labels.keys())

    for product_id in all_product_ids:
        old_label = old_labels.get(product_id)
        new_label = new_labels.get(product_id)

        # Skip if no change
        if old_label == new_label:
            continue

        # Record transition
        transition = {
            "date": today,
            "product_id": product_id,
            "from_label": old_label,
            "to_label": new_label
        }

        transitions.append(transition)

    return transitions

def process_client(client: Dict, credentials_path: str, dry_run: bool = False):
    """Process label tracking for a single client"""
    client_name = client['name']
    merchant_id = client['merchant_id']

    print(f"\n{'='*70}")
    print(f"Processing: {client_name}")
    print(f"{'='*70}")

    # Check if label tracking enabled
    label_config = client.get('label_tracking', {})
    if not label_config.get('enabled', False):
        print(f"⏭️  Label tracking disabled for {client_name}")
        return

    configured_field = label_config.get('label_field')

    # Fetch products from Merchant Centre
    products = fetch_products_from_merchant_centre(merchant_id, credentials_path)

    if not products:
        print(f"❌ No products fetched for {client_name}")
        return

    # Detect which custom label field has Product Hero labels
    detected_field = detect_label_field(products)

    if not detected_field:
        print(f"⚠️  No Product Hero labels detected in any custom_label field")
        return

    print(f"✅ Detected Product Hero labels in: {detected_field}")

    # Warn if different from configured field
    if configured_field:
        config_field_name = f"customLabel{configured_field.split('_')[-1]}"
        if detected_field != config_field_name:
            print(f"⚠️  WARNING: Detected field ({detected_field}) differs from config ({config_field_name})")

    # Extract labels
    new_labels = extract_labels_from_products(products, detected_field)

    print(f"📊 Label distribution:")
    label_counts = defaultdict(int)
    for label in new_labels.values():
        label_counts[label] += 1

    for label in sorted(label_counts.keys()):
        print(f"   {label}: {label_counts[label]} products")

    if dry_run:
        print(f"\n🔍 DRY RUN - Would save {len(new_labels)} products")
        return

    # Load previous labels
    old_snapshot = load_current_labels(client_name)
    old_labels = old_snapshot.get('products', {})

    # Detect transitions
    transitions = detect_transitions(old_labels, new_labels)

    if transitions:
        print(f"\n🔄 Detected {len(transitions)} label transitions:")
        for t in transitions[:5]:  # Show first 5
            print(f"   {t['product_id']}: {t['from_label']} → {t['to_label']}")
        if len(transitions) > 5:
            print(f"   ... and {len(transitions) - 5} more")

        # Save transitions
        save_transitions(client_name, transitions)
    else:
        print(f"\n✅ No label transitions detected")

    # Save current snapshot
    new_snapshot = {
        "last_updated": datetime.now().isoformat(),
        "source": "merchant_centre_api",
        "label_field": detected_field,
        "products": new_labels
    }
    save_current_labels(client_name, new_snapshot)

def main():
    parser = argparse.ArgumentParser(description='Track Product Hero labels from Merchant Centre')
    parser.add_argument('--all-clients', action='store_true', help='Process all enabled clients')
    parser.add_argument('--client', type=str, help='Process specific client by name')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode (no changes)')

    args = parser.parse_args()

    # Load config
    config = load_config()

    # Find credentials
    credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        # Default path
        credentials_path = Path.home() / 'Documents/PetesBrain/infrastructure/mcp-servers/google-sheets-mcp-server/credentials.json'

    if not Path(credentials_path).exists():
        print(f"❌ Credentials not found: {credentials_path}")
        print(f"   Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        sys.exit(1)

    print(f"🔑 Using credentials: {credentials_path}")

    if args.dry_run:
        print(f"\n🔍 DRY RUN MODE - No changes will be saved\n")

    # Process clients
    clients_to_process = []

    if args.all_clients:
        clients_to_process = [c for c in config['clients'] if c.get('enabled', False)]
    elif args.client:
        matching = [c for c in config['clients'] if c['name'].lower() == args.client.lower()]
        if not matching:
            print(f"❌ Client not found: {args.client}")
            sys.exit(1)
        clients_to_process = matching
    else:
        print("❌ Must specify --all-clients or --client")
        sys.exit(1)

    print(f"\n🚀 Processing {len(clients_to_process)} client(s)\n")

    success_count = 0
    for client in clients_to_process:
        try:
            process_client(client, str(credentials_path), args.dry_run)
            success_count += 1
        except Exception as e:
            print(f"❌ Error processing {client['name']}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*70}")
    print(f"✅ Processed {success_count}/{len(clients_to_process)} clients successfully")
    print(f"{'='*70}")

    sys.exit(0 if success_count == len(clients_to_process) else 1)

if __name__ == '__main__':
    main()
