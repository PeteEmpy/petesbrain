#!/usr/bin/env python3
"""
FINAL Product-Feeds Tasks Migration
Moves all clients/{client}/product-feeds/tasks.json → clients/{client}/tasks.json

This script:
1. Finds all product-feeds/tasks.json files
2. Moves them to client root (or merges if root file exists)
3. Verifies migration
4. Deletes old product-feeds locations
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path('/Users/administrator/Documents/PetesBrain.nosync')
CLIENTS_DIR = PROJECT_ROOT / 'clients'

def merge_tasks(existing_tasks, product_feeds_tasks):
    """Merge two task lists, avoiding duplicates"""
    # Use task titles as deduplication key
    seen_titles = {task['title'] for task in existing_tasks}

    merged = existing_tasks.copy()
    added_count = 0

    for task in product_feeds_tasks:
        if task['title'] not in seen_titles:
            merged.append(task)
            added_count += 1
            seen_titles.add(task['title'])

    return merged, added_count

def migrate_client_tasks(client_dir, files_existed_before):
    """Migrate tasks from product-feeds to root for a single client"""
    client_name = client_dir.name

    # Source: product-feeds/tasks.json
    product_feeds_file = client_dir / 'product-feeds' / 'tasks.json'

    # Target: tasks.json
    root_file = client_dir / 'tasks.json'

    # Skip if no product-feeds file
    if not product_feeds_file.exists():
        return None

    print(f"\n📂 {client_name}")
    print(f"   Source: product-feeds/tasks.json")

    # Read product-feeds tasks
    with open(product_feeds_file, 'r') as f:
        pf_data = json.load(f)

    pf_tasks = pf_data.get('tasks', [])
    print(f"   Found: {len(pf_tasks)} tasks in product-feeds")

    # Check if root file already exists
    if root_file.exists():
        print(f"   ⚠️  Root tasks.json already exists")

        with open(root_file, 'r') as f:
            root_data = json.load(f)

        root_tasks = root_data.get('tasks', [])
        print(f"   Existing: {len(root_tasks)} tasks in root")

        # Merge tasks
        merged_tasks, added_count = merge_tasks(root_tasks, pf_tasks)

        if added_count > 0:
            print(f"   ✅ Merged: {added_count} new tasks added to root")
            root_data['tasks'] = merged_tasks
            root_data['last_updated'] = datetime.now().isoformat()

            with open(root_file, 'w') as f:
                json.dump(root_data, f, indent=2)
        else:
            print(f"   ✓ No new tasks to merge (all already in root)")

    else:
        # Simply move product-feeds file to root
        print(f"   ➜ Moving product-feeds/tasks.json to root")

        # Update last_updated timestamp
        pf_data['last_updated'] = datetime.now().isoformat()

        with open(root_file, 'w') as f:
            json.dump(pf_data, f, indent=2)

        print(f"   ✅ Created {len(pf_tasks)} tasks in root location")

    return {
        'client': client_name,
        'product_feeds_tasks': len(pf_tasks),
        'root_file_created': not files_existed_before.get(client_name, False)
    }

def main():
    """Run migration"""
    print("=" * 80)
    print("FINAL Product-Feeds Tasks Migration")
    print("=" * 80)

    # Track which files existed before migration
    files_existed_before = {}
    for client_dir in CLIENTS_DIR.iterdir():
        if client_dir.is_dir() and not client_dir.name.startswith('_'):
            root_file = client_dir / 'tasks.json'
            files_existed_before[client_dir.name] = root_file.exists()

    results = []

    # Process all clients
    for client_dir in sorted(CLIENTS_DIR.iterdir()):
        if client_dir.is_dir() and not client_dir.name.startswith('_'):
            result = migrate_client_tasks(client_dir, files_existed_before)
            if result:
                results.append(result)

    # Summary
    print("\n" + "=" * 80)
    print("MIGRATION SUMMARY")
    print("=" * 80)
    print(f"Clients migrated: {len(results)}")

    for result in results:
        status = "NEW" if result['root_file_created'] else "MERGED"
        print(f"  ✓ {result['client']}: {result['product_feeds_tasks']} tasks ({status})")

    # Verification step
    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)

    all_clients = [d for d in CLIENTS_DIR.iterdir() if d.is_dir() and not d.name.startswith('_')]

    clients_with_root = 0
    clients_with_product_feeds = 0

    for client_dir in sorted(all_clients):
        root_file = client_dir / 'tasks.json'
        pf_file = client_dir / 'product-feeds' / 'tasks.json'

        if root_file.exists():
            clients_with_root += 1

        if pf_file.exists():
            clients_with_product_feeds += 1
            print(f"  ⚠️  {client_dir.name} still has product-feeds/tasks.json")

    print(f"\nClients with root tasks.json: {clients_with_root}/{len(all_clients)}")
    print(f"Clients with product-feeds/tasks.json: {clients_with_product_feeds}/{len(all_clients)}")

    if clients_with_product_feeds == 0:
        print("\n✅ Migration complete - all tasks now in root locations!")
        print("\nNext step: Delete product-feeds/tasks.json files")
        return 0
    else:
        print("\n⚠️  Migration incomplete - some product-feeds files still exist")
        return 1

if __name__ == '__main__':
    exit(main())
