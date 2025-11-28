#!/usr/bin/env python3
"""
October 2025 Historical Backfill - Practical Implementation

This script works with Claude Code's MCP access to:
1. Fetch product-campaign data from October 2025
2. Infer labels from campaign names
3. Generate historical baseline for label tracking

Strategy for large accounts (AFH, Uno Lights):
- Sample 3 dates in October (1st, 15th, 30th) instead of all 31 days
- LIMIT 500 per query to stay under token limits
- Provides representative snapshot without overwhelming data
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List

# Import label inference
from label_inference import LabelInferencer, LabelConfidence

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

def generate_backfill_queries():
    """
    Generate MCP queries for October 2025 backfill.

    Returns: Dict of {client_name: query_config}
    """
    config = load_config()
    queries = {}

    for client in config['clients']:
        label_config = client.get('label_tracking', {})
        if not label_config.get('enabled', False):
            continue

        client_name = client['name']
        customer_id = client['google_ads_customer_id']
        manager_id = label_config.get('manager_id')
        label_field_num = label_config.get('label_field', 'custom_label_0').replace('custom_label_', '')

        # Use sampled approach for ALL clients to avoid token limits
        # Sample 3 dates in October (beginning, middle, end)
        sample_dates = ["2025-10-01", "2025-10-15", "2025-10-30"]

        # Universal LIMIT 500 to stay under 25K token limit
        limit = 500

        queries[client_name] = {
            "config": client,
            "strategy": "sampled_dates",
            "queries": []
        }

        for date in sample_dates:
            query = f"""SELECT
  segments.product_item_id,
  segments.product_custom_attribute{label_field_num},
  campaign.name
FROM shopping_performance_view
WHERE segments.date = '{date}'
  AND metrics.impressions > 0
ORDER BY segments.product_item_id
LIMIT {limit}"""

            queries[client_name]["queries"].append({
                "customer_id": customer_id,
                "manager_id": manager_id,
                "query": query,
                "date": date,
                "limit": limit
            })

    return queries

def process_mcp_response(client_name, response_data, strategy):
    """
    Process MCP response and infer labels.

    Args:
        client_name: Client name
        response_data: List of MCP query responses (one per query)
        strategy: "sampled_dates" or "full_month"

    Returns: List of inferred label records
    """
    inferencer = LabelInferencer(assessment_window_days=30)
    inferred_records = []

    for query_response in response_data:
        date = query_response.get('date', '2025-10')
        rows = query_response.get('rows', [])

        print(f"  Processing {len(rows)} products for {date}")

        for row in rows:
            product_id = row.get('segments', {}).get('productItemId', 'unknown')
            actual_label = row.get('segments', {}).get('productCustomAttribute', '').lower()
            campaign_name = row.get('campaign', {}).get('name', '')

            # If actual label exists, use it (HIGH confidence)
            if actual_label in ['heroes', 'sidekicks', 'villains', 'zombies']:
                record = {
                    "product_id": product_id,
                    "date": date,
                    "label": actual_label,
                    "confidence": "high",
                    "method": "actual_feed_label",
                    "campaign": campaign_name,
                    "evidence": {
                        "source": "product_feed",
                        "campaign": campaign_name
                    }
                }
            else:
                # Infer from campaign name
                inferred = inferencer.infer_label(
                    product_id=product_id,
                    date=date,
                    campaign_name=campaign_name
                )

                record = {
                    "product_id": product_id,
                    "date": date,
                    "label": inferred.label,
                    "confidence": inferred.confidence.value,
                    "method": inferred.method,
                    "campaign": campaign_name,
                    "evidence": inferred.evidence
                }

            inferred_records.append(record)

    return inferred_records

def save_october_backfill(client_name, inferred_records, strategy):
    """
    Save October 2025 backfill data.

    Args:
        client_name: Client name
        inferred_records: List of inferred label records
        strategy: "sampled_dates" or "full_month"
    """
    history_dir = get_history_dir(client_name)
    output_file = history_dir / "2025-10.json"

    # All clients use sampled approach (3 dates) to avoid token limits
    note = (
        "Labels for October 2025 are SAMPLED (3 dates: Oct 1, 15, 30) "
        "to avoid MCP token limits. Provides representative historical baseline. "
        "Actual Product Hero labels used where available, otherwise inferred from "
        "campaign names."
    )

    output_data = {
        "month": "2025-10",
        "backfill_date": datetime.now().isoformat(),
        "strategy": strategy,
        "note": note,
        "total_records": len(inferred_records),
        "inferred_labels": inferred_records
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    # Generate summary stats
    by_label = defaultdict(int)
    by_confidence = defaultdict(int)

    for record in inferred_records:
        by_label[record['label']] += 1
        by_confidence[record['confidence']] += 1

    print(f"\n  📊 October 2025 Summary for {client_name}:")
    print(f"     Total products: {len(inferred_records)}")
    print(f"     Label distribution:")
    for label, count in sorted(by_label.items()):
        pct = (count / len(inferred_records)) * 100
        print(f"       {label}: {count} ({pct:.1f}%)")
    print(f"     Confidence distribution:")
    for conf, count in sorted(by_confidence.items()):
        pct = (count / len(inferred_records)) * 100
        print(f"       {conf}: {count} ({pct:.1f}%)")
    print(f"  ✅ Saved to {output_file}")

def main():
    """Main backfill orchestration"""
    print("\n" + "="*70)
    print("🔄 OCTOBER 2025 HISTORICAL BACKFILL")
    print("="*70)

    # Generate queries
    print("\n📋 Step 1: Generating backfill queries...")
    queries = generate_backfill_queries()

    print(f"\n  Clients to backfill: {len(queries)}")
    for client_name, client_queries in queries.items():
        strategy = client_queries['strategy']
        num_queries = len(client_queries['queries'])
        print(f"    - {client_name}: {strategy} ({num_queries} queries)")

    # Save queries for Claude Code to execute
    queries_file = Path(__file__).parent / "pending_backfill_queries.json"
    with open(queries_file, 'w') as f:
        json.dump(queries, f, indent=2)

    print(f"\n  ✅ Queries saved to {queries_file}")
    print("\n" + "="*70)
    print("⏸️  EXECUTION PAUSED - MCP QUERIES NEEDED")
    print("="*70)
    print("\n📌 Next Steps:")
    print("  1. Claude Code will execute MCP queries from pending_backfill_queries.json")
    print("  2. Pass responses back to this script via process_backfill_responses()")
    print("  3. Script will infer labels and generate 2025-10.json files")
    print("\n" + "="*70 + "\n")

    return queries

def process_backfill_responses(responses_by_client):
    """
    Process MCP responses and generate historical files.

    Args:
        responses_by_client: Dict of {client_name: [list of MCP responses]}
    """
    print("\n" + "="*70)
    print("📊 PROCESSING BACKFILL RESPONSES")
    print("="*70)

    config = load_config()
    queries = generate_backfill_queries()

    for client_name, responses in responses_by_client.items():
        if client_name not in queries:
            print(f"\n⚠️  Skipping {client_name} (not in enabled clients)")
            continue

        print(f"\n🔄 Processing {client_name}...")
        strategy = queries[client_name]['strategy']

        # Process responses and infer labels
        inferred_records = process_mcp_response(client_name, responses, strategy)

        # Save to 2025-10.json
        save_october_backfill(client_name, inferred_records, strategy)

    print("\n" + "="*70)
    print("✅ OCTOBER 2025 BACKFILL COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    # Generate queries (for Claude Code to execute)
    queries = main()
