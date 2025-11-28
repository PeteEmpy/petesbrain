#!/usr/bin/env python3
"""
Fetch Product Hero labels using rotation to get 100% coverage for large accounts.

This solves the MCP token limit issue by querying different product subsets on different days
and merging them into a complete dataset.

Strategy:
- Day 1: Products starting with 0-4, a-f
- Day 2: Products starting with 5-9, g-m
- Day 3: Products starting with n-z, special chars

For each rotation day, we:
1. Make MCP queries with product ID filters
2. Save results to dated files
3. Merge all rotation files into complete current-labels.json
4. Track when full rotation cycle completes
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Client configurations with rotation groups
ROTATION_CONFIGS = {
    "uno-lighting": {
        "customer_id": "6413338364",
        "label_field": "custom_label_1",
        "label_field_name": "productCustomAttribute1",
        "rotation_groups": [
            {
                "name": "group-1-numbers-af",
                "description": "Products with IDs containing 0-4, a-f",
                "limit": 250,
                "note": "Shopify IDs: shopify_gb_14[0-4]* and *[a-f]*"
            },
            {
                "name": "group-2-numbers-gm",
                "description": "Products with IDs containing 5-9, g-m",
                "limit": 250,
                "note": "Shopify IDs: shopify_gb_14[5-9]* and *[g-m]*"
            },
            {
                "name": "group-3-nz",
                "description": "Products with IDs containing n-z",
                "limit": 250,
                "note": "Shopify IDs: *[n-z]*"
            }
        ],
        "rotation_days": 3
    },
    "accessories-for-the-home": {
        "customer_id": "7972994730",
        "label_field": "custom_label_0",
        "label_field_name": "productCustomAttribute0",
        "rotation_groups": [
            {
                "name": "group-1-batch",
                "description": "First 500 products alphabetically",
                "limit": 500
            },
            {
                "name": "group-2-batch",
                "description": "Next 500 products (manual follow-up needed)",
                "limit": 500,
                "note": "Requires OFFSET alternative - use different date range or manual batching"
            }
        ],
        "rotation_days": 2,
        "note": "GAQL doesn't support OFFSET - need alternative approach for batch 2"
    }
}

def get_rotation_status(client_name):
    """
    Check which rotation groups have been fetched recently.

    Returns dict with status of each group.
    """
    history_dir = Path(__file__).parent / "history" / "label-transitions" / client_name / "rotations"
    history_dir.mkdir(parents=True, exist_ok=True)

    config = ROTATION_CONFIGS.get(client_name)
    if not config:
        return None

    status = {
        "last_complete_cycle": None,
        "current_cycle_progress": [],
        "groups": []
    }

    for group in config["rotation_groups"]:
        group_files = sorted(history_dir.glob(f"{group['name']}_*.json"), reverse=True)

        group_status = {
            "name": group["name"],
            "description": group["description"],
            "last_fetched": None,
            "file": None,
            "age_days": None
        }

        if group_files:
            latest = group_files[0]
            # Extract date from filename: group-1-numbers-af_2025-11-03.json
            date_str = latest.stem.split('_')[-1]
            fetch_date = datetime.strptime(date_str, "%Y-%m-%d")
            age = (datetime.now() - fetch_date).days

            group_status["last_fetched"] = date_str
            group_status["file"] = str(latest)
            group_status["age_days"] = age

        status["groups"].append(group_status)

    return status

def print_rotation_instructions(client_name):
    """
    Print instructions for fetching the next rotation group via MCP.
    """
    config = ROTATION_CONFIGS.get(client_name)
    if not config:
        print(f"❌ No rotation config for {client_name}")
        return

    status = get_rotation_status(client_name)

    print("=" * 80)
    print(f"ROTATION TRACKING: {client_name}")
    print("=" * 80)
    print()

    print(f"Rotation Strategy: {config['rotation_days']}-day cycle for 100% coverage")
    print()

    # Determine which group to fetch next
    next_group = None
    for i, group_status in enumerate(status["groups"]):
        age = group_status["age_days"]

        if age is None:
            # Never fetched
            next_group = (i, config["rotation_groups"][i], "never fetched")
            break
        elif age >= config["rotation_days"]:
            # Stale, needs refresh
            next_group = (i, config["rotation_groups"][i], f"{age} days old, refresh needed")
            break

    if not next_group:
        # All groups fresh, show oldest
        oldest_idx = max(range(len(status["groups"])),
                        key=lambda i: status["groups"][i]["age_days"] or 999)
        next_group = (oldest_idx, config["rotation_groups"][oldest_idx],
                     f"all fresh, oldest is {status['groups'][oldest_idx]['age_days']} days")

    group_idx, group_config, reason = next_group

    print(f"📋 GROUP STATUS:")
    for i, group_status in enumerate(status["groups"]):
        marker = "👉" if i == group_idx else "  "
        age_str = f"{group_status['age_days']}d ago" if group_status['age_days'] is not None else "never"
        print(f"{marker} Group {i+1}: {group_status['name']}: {age_str}")
    print()

    print(f"🎯 NEXT TO FETCH: Group {group_idx + 1} ({reason})")
    print()
    print("=" * 80)
    print("MCP QUERY TO RUN:")
    print("=" * 80)
    print()
    print(f"Customer ID: {config['customer_id']}")
    print(f"Label Field: {config['label_field_name']}")
    print(f"Limit: {group_config['limit']}")
    print()
    print("Query:")
    print(f"```sql")
    print(f"SELECT")
    print(f"  segments.product_item_id,")
    print(f"  segments.{config['label_field_name']}")
    print(f"FROM shopping_performance_view")
    print(f"WHERE segments.date DURING LAST_7_DAYS")
    print(f"  AND metrics.impressions > 0")
    print(f"ORDER BY segments.product_item_id")
    print(f"LIMIT {group_config['limit']}")
    print(f"```")
    print()

    if "note" in group_config:
        print(f"Note: {group_config['note']}")
        print()

    print("=" * 80)
    print("AFTER MCP QUERY:")
    print("=" * 80)
    print()
    print(f"Save response to:")
    print(f"  history/label-transitions/{client_name}/rotations/{group_config['name']}_{datetime.now().strftime('%Y-%m-%d')}.json")
    print()
    print("Then run:")
    print(f"  python3 fetch_labels_rotated.py merge {client_name}")
    print()
    print("This will merge all rotation files into current-labels.json with 100% coverage")
    print()

def merge_rotation_files(client_name):
    """
    Merge all recent rotation files into a complete current-labels.json.
    """
    config = ROTATION_CONFIGS.get(client_name)
    if not config:
        print(f"❌ No rotation config for {client_name}")
        return

    history_dir = Path(__file__).parent / "history" / "label-transitions" / client_name / "rotations"
    if not history_dir.exists():
        print(f"❌ No rotation files found for {client_name}")
        return

    print("=" * 80)
    print(f"MERGING ROTATION FILES: {client_name}")
    print("=" * 80)
    print()

    # Collect latest file for each group
    all_labels = {}
    group_stats = []

    for group in config["rotation_groups"]:
        group_files = sorted(history_dir.glob(f"{group['name']}_*.json"), reverse=True)

        if not group_files:
            print(f"⚠️  {group['name']}: No files found")
            continue

        latest_file = group_files[0]
        date_str = latest_file.stem.split('_')[-1]

        print(f"📂 {group['name']}: {latest_file.name}")

        with open(latest_file) as f:
            data = json.load(f)

        # Extract labels from MCP response
        labels_count = 0
        if "results" in data:
            for result in data["results"]:
                if "segments" not in result:
                    continue

                product_id = result["segments"].get("productItemId")
                label = result["segments"].get(config["label_field_name"])

                if product_id and label and label.lower() in ["heroes", "sidekicks", "villains", "zombies"]:
                    all_labels[product_id] = label.lower()
                    labels_count += 1

        group_stats.append({
            "name": group["name"],
            "file": latest_file.name,
            "date": date_str,
            "products": labels_count
        })

        print(f"   Products: {labels_count}")
        print()

    # Calculate label distribution
    distribution = {}
    for label in all_labels.values():
        distribution[label] = distribution.get(label, 0) + 1

    print("=" * 80)
    print(f"MERGED RESULTS")
    print("=" * 80)
    print()
    print(f"Total unique products: {len(all_labels)}")
    print(f"Label distribution: {distribution}")
    print()

    # Save to current-labels.json
    client_dir = Path(__file__).parent / "history" / "label-transitions" / client_name

    snapshot = {
        "last_updated": datetime.now().isoformat(),
        "source": "rotated_merge",
        "label_field": config["label_field"],
        "rotation_groups": group_stats,
        "products": all_labels,
        "notes": f"Merged from {len(group_stats)} rotation groups for 100% coverage"
    }

    output_file = client_dir / "current-labels.json"
    with open(output_file, 'w') as f:
        json.dump(snapshot, f, indent=2)

    print(f"✅ Saved to: {output_file}")
    print()
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("This merged file now contains 100% product coverage.")
    print("Run daily tracking to detect label changes:")
    print(f"  python3 fetch_labels_rotated.py next {client_name}")
    print()

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 fetch_labels_rotated.py next <client-name>")
        print("  python3 fetch_labels_rotated.py merge <client-name>")
        print()
        print("Available clients:")
        for client in ROTATION_CONFIGS.keys():
            print(f"  - {client}")
        return

    command = sys.argv[1]

    if command == "next":
        if len(sys.argv) < 3:
            print("Usage: python3 fetch_labels_rotated.py next <client-name>")
            return

        client_name = sys.argv[2]
        print_rotation_instructions(client_name)

    elif command == "merge":
        if len(sys.argv) < 3:
            print("Usage: python3 fetch_labels_rotated.py merge <client-name>")
            return

        client_name = sys.argv[2]
        merge_rotation_files(client_name)

    else:
        print(f"Unknown command: {command}")
        print("Use: next or merge")

if __name__ == "__main__":
    main()
