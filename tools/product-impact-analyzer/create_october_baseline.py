#!/usr/bin/env python3
"""
October 2025 Baseline Creator - Alternative Approach

Due to MCP token limits preventing historical queries, this script creates
an October 2025 baseline using current label snapshots.

Rationale:
- MCP queries for October 2025 exceed 25K token limit even with LIMIT 500
- Product Hero labeling system was implemented in October 2025
- Current labels represent end-of-October state
- We can retroactively use this as our "October baseline"

This provides:
- A starting point for November tracking
- Ability to detect transitions going forward
- Historical context for year-end analysis
"""

import json
from pathlib import Path
from datetime import datetime

def load_config():
    """Load configuration"""
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, 'r') as f:
        return json.load(f)

def get_history_dir(client_name):
    """Get history directory for client"""
    base_dir = Path(__file__).parent / "history" / "label-transitions"
    client_dir = base_dir / client_name.lower().replace(" ", "-")
    client_dir.mkdir(parents=True, exist_ok=True)
    return client_dir

def create_october_baseline():
    """
    Create October 2025 baseline files from current label snapshots.
    """
    print("\n" + "="*70)
    print("📅 OCTOBER 2025 BASELINE CREATOR")
    print("="*70)
    print("\nApproach: Use current label snapshots as October baseline")
    print("Reason: MCP token limits prevent historical October queries\n")

    config = load_config()
    created_count = 0
    skipped_count = 0

    for client in config['clients']:
        label_config = client.get('label_tracking', {})
        if not label_config.get('enabled', False):
            continue

        client_name = client['name']
        history_dir = get_history_dir(client_name)

        # Check if current-labels.json exists
        current_labels_file = history_dir / "current-labels.json"
        october_file = history_dir / "2025-10.json"

        if october_file.exists():
            print(f"⏭️  {client_name}: October baseline already exists")
            skipped_count += 1
            continue

        if not current_labels_file.exists():
            print(f"❌ {client_name}: No current labels found - skipping")
            skipped_count += 1
            continue

        # Load current labels
        with open(current_labels_file, 'r') as f:
            current_data = json.load(f)

        # Get products dict (could be 'products' or 'labels')
        products = current_data.get('products', current_data.get('labels', {}))

        # Create October baseline
        october_data = {
            "month": "2025-10",
            "baseline_date": "2025-10-31",
            "created_date": datetime.now().isoformat(),
            "method": "current_snapshot_as_baseline",
            "note": (
                "October 2025 baseline created from current label snapshot (Oct 31, 2025). "
                "Product Hero labeling system was implemented in October 2025. This snapshot "
                "represents end-of-October state and serves as the historical baseline for "
                "tracking transitions going forward. MCP token limits prevented querying "
                "historical October data directly."
            ),
            "products": products,
            "snapshot_date": current_data.get('last_updated', '2025-10-31'),
            "total_products": len(products)
        }

        # Save October baseline
        with open(october_file, 'w') as f:
            json.dump(october_data, f, indent=2)

        # Calculate distribution
        by_label = {}
        for product_id, label in products.items():
            by_label[label] = by_label.get(label, 0) + 1

        print(f"\n✅ {client_name}: October baseline created")
        print(f"   Total products: {october_data['total_products']}")
        print(f"   Distribution:")
        for label, count in sorted(by_label.items()):
            pct = (count / october_data['total_products']) * 100 if october_data['total_products'] > 0 else 0
            print(f"     {label}: {count} ({pct:.1f}%)")

        created_count += 1

    print("\n" + "="*70)
    print(f"✅ BASELINE CREATION COMPLETE")
    print(f"   Created: {created_count} clients")
    print(f"   Skipped: {skipped_count} clients")
    print("="*70 + "\n")

if __name__ == "__main__":
    create_october_baseline()
