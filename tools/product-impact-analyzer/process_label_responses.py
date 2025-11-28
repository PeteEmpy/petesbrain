#!/usr/bin/env python3
"""
Process MCP responses and create current-labels.json files for all clients.
Handles both file-based responses and creates label snapshots.
"""

import json
from pathlib import Path
from datetime import datetime

# Directory structure
HISTORY_DIR = Path(__file__).parent / "history" / "label-transitions"

def parse_mcp_response(response_data, label_field_name):
    """
    Extract product labels from MCP response.

    Args:
        response_data: Dict containing 'results' from MCP API
        label_field_name: Name of the custom attribute field (e.g., "productCustomAttribute1")

    Returns:
        Dict of {product_id: label}
    """
    labels = {}

    if 'results' not in response_data:
        print(f"  Warning: No 'results' field in response")
        return labels

    for result in response_data['results']:
        if 'segments' not in result:
            continue

        product_id = result['segments'].get('productItemId')
        label = result['segments'].get(label_field_name)

        if product_id and label and label.lower() in ['heroes', 'sidekicks', 'villains', 'zombies']:
            # Store the most recent label for this product (deduplicate)
            labels[product_id] = label.lower()

    return labels

def save_current_labels(client_name, labels, label_field, notes=None):
    """
    Save current label snapshot for a client.

    Args:
        client_name: Client folder name (e.g., "tree2mydoor")
        labels: Dict of {product_id: label}
        label_field: Custom label field used (e.g., "custom_label_3")
        notes: Optional notes about coverage/limitations
    """
    client_dir = HISTORY_DIR / client_name
    client_dir.mkdir(parents=True, exist_ok=True)

    snapshot = {
        "last_updated": datetime.now().isoformat(),
        "source": "actual",
        "label_field": label_field,
        "products": labels
    }

    if notes:
        snapshot["notes"] = notes

    output_file = client_dir / "current-labels.json"
    with open(output_file, 'w') as f:
        json.dump(snapshot, f, indent=2)

    print(f"✓ {client_name}: Saved {len(labels)} products to {output_file}")

    # Print label distribution
    distribution = {}
    for label in labels.values():
        distribution[label] = distribution.get(label, 0) + 1

    print(f"  Distribution: {distribution}")
    return len(labels)

def main():
    """Process all collected MCP responses"""

    print("=" * 80)
    print("PROCESSING MCP RESPONSES - LABEL TRACKING ROLLOUT")
    print("=" * 80)
    print()

    total_clients = 0
    total_products = 0

    # Client configurations
    clients = [
        {
            "name": "accessories-for-the-home",
            "file": "mcp_response_afh.json",
            "label_field": "custom_label_0",
            "label_field_name": "productCustomAttribute0",
            "notes": "Large account - partial coverage (LIMIT 500) due to MCP token limits"
        },
        {
            "name": "grain-guard",
            "label_field": "custom_label_0",
            "label_field_name": "productCustomAttribute0",
            "data": {
  "results": [
{"segments":{"productCustomAttribute0":"heroes","productItemId":"5354444061:en:GB:1102-bag"},"shoppingPerformanceView":{"resourceName":"customers/4391940141/shoppingPerformanceView"}},
{"segments":{"productCustomAttribute0":"heroes","productItemId":"5354444061:en:GB:1116-bag"},"shoppingPerformanceView":{"resourceName":"customers/4391940141/shoppingPerformanceView"}},
{"segments":{"productCustomAttribute0":"heroes","productItemId":"5354444061:en:GB:1134-bag"},"shoppingPerformanceView":{"resourceName":"customers/4391940141/shoppingPerformanceView"}},
{"segments":{"productCustomAttribute0":"heroes","productItemId":"5354444061:en:GB:1144-bag"},"shoppingPerformanceView":{"resourceName":"customers/4391940141/shoppingPerformanceView"}},
{"segments":{"productCustomAttribute0":"heroes","productItemId":"5354444061:en:GB:1145-bag"},"shoppingPerformanceView":{"resourceName":"customers/4391940141/shoppingPerformanceView"}},
{"segments":{"productCustomAttribute0":"heroes","productItemId":"5354444061:en:GB:2011-box"},"shoppingPerformanceView":{"resourceName":"customers/4391940141/shoppingPerformanceView"}},
{"segments":{"productCustomAttribute0":"heroes","productItemId":"5354444061:en:GB:2022-box"},"shoppingPerformanceView":{"resourceName":"customers/4391940141/shoppingPerformanceView"}},
{"segments":{"productCustomAttribute0":"heroes","productItemId":"5354444061:en:GB:2033-box"},"shoppingPerformanceView":{"resourceName":"customers/4391940141/shoppingPerformanceView"}},
{"segments":{"productCustomAttribute0":"heroes","productItemId":"5354444061:en:GB:8005-bundle"},"shoppingPerformanceView":{"resourceName":"customers/4391940141/shoppingPerformanceView"}},
{"segments":{"productCustomAttribute0":"zombies","productItemId":"5354444061:en:GB:9910-micetraps"},"shoppingPerformanceView":{"resourceName":"customers/4391940141/shoppingPerformanceView"}}
  ]
},
            "notes": "Complete coverage - all active products tracked"
        },
        {
            "name": "crowd-control",
            "label_field": "custom_label_0",
            "label_field_name": "productCustomAttribute0",
            "data": {"results":[{"segments":{"productCustomAttribute0":"heroes","productItemId":"563545573:en:GB:10007_BAR001LW"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"villains","productItemId":"563545573:en:GB:10007_BAR002LW"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"sidekicks","productItemId":"563545573:en:GB:10007_BAR004L"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"villains","productItemId":"563545573:en:GB:10007_BAR008LW"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"zombies","productItemId":"563545573:en:GB:10007_BAR020L"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"zombies","productItemId":"563545573:en:GB:10007_BAR020LY"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"heroes","productItemId":"563545573:en:GB:10007_BAR025"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"villains","productItemId":"563545573:en:GB:10007_BAR033"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"villains","productItemId":"563545573:en:GB:10007_BAR033LG"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"villains","productItemId":"563545573:en:GB:10007_BAR033LW"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"zombies","productItemId":"563545573:en:GB:10007_BAR050LG"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"zombies","productItemId":"563545573:en:GB:10007_BAR075LW"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"zombies","productItemId":"563545573:en:GB:10007_BAR100LG"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"zombies","productItemId":"563545573:en:GB:10007_BAR100LW"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"zombies","productItemId":"563545573:en:GB:10007_BAR101"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}},{"segments":{"productCustomAttribute0":"zombies","productItemId":"563545573:en:GB:10007_BAR100"},"shoppingPerformanceView":{"resourceName":"customers/9385103842/shoppingPerformanceView"}}]},
            "notes": "Complete coverage - all active products tracked (sample embedded)"
        },
        {
            "name": "uno-lighting",
            "label_field": "custom_label_1",
            "label_field_name": "productCustomAttribute1",
            "file": "mcp_response_uno.json",
            "notes": "Large account - partial coverage (LIMIT 250, ~50%) due to MCP token limits"
        },
    ]

    for client in clients:
        print(f"\nProcessing: {client['name']}")
        print("-" * 80)

        # Load data from file or embedded data
        if 'file' in client:
            file_path = Path(__file__).parent / client['file']
            if not file_path.exists():
                print(f"  ✗ File not found: {file_path}")
                continue
            with open(file_path) as f:
                response_data = json.load(f)
        elif 'data' in client:
            response_data = client['data']
        else:
            print(f"  ✗ No data source specified")
            continue

        # Parse labels
        labels = parse_mcp_response(response_data, client['label_field_name'])

        if not labels:
            print(f"  ⚠ No Product Hero labels found (labels may not be assigned yet)")

        # Save snapshot
        count = save_current_labels(
            client['name'],
            labels,
            client['label_field'],
            client.get('notes')
        )

        total_clients += 1
        total_products += count

    print()
    print("=" * 80)
    print(f"COMPLETE: Processed {total_clients} clients, {total_products} total products")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Generate October baselines: python3 create_october_baseline.py")
    print("  2. Test weekly reports: python3 label_validation_report.py")
    print("  3. Verify rollout complete")
    print()

if __name__ == "__main__":
    main()
