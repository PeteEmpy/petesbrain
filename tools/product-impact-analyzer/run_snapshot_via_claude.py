#!/usr/bin/env python3
"""
Claude Code Helper Script for Product Feed Snapshots

This script is designed to be called by Claude Code, which will:
1. Fetch product data via MCP (Google Ads API)
2. Cache the data locally
3. Run the snapshot script
4. Write results to Google Sheets via MCP

Usage (via Claude Code):
    User: "Run the product feed snapshot"
    Claude: Calls this script with MCP data

Manual usage:
    python run_snapshot_via_claude.py --client "Tree2mydoor"
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta


def save_gaql_results(customer_id: str, results: list):
    """Save GAQL query results to cache for snapshot script"""
    cache_path = Path(__file__).parent / "data" / f"snapshot_cache_{customer_id}.json"
    cache_path.parent.mkdir(exist_ok=True)

    with open(cache_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Cached {len(results)} rows for customer {customer_id}")
    return cache_path


def generate_gaql_query(days_back: int = 1) -> tuple:
    """Generate GAQL query for fetching product data"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    query = f"""
    SELECT
        segments.product_item_id,
        segments.product_title,
        segments.product_brand,
        segments.product_condition,
        segments.product_channel,
        segments.date,
        metrics.clicks,
        metrics.impressions,
        metrics.cost_micros
    FROM shopping_performance_view
    WHERE segments.date >= '{start_date}'
        AND segments.date <= '{end_date}'
    ORDER BY segments.product_item_id, segments.date DESC
    """

    return query, start_date, end_date


def print_instructions_for_claude():
    """Print instructions for Claude Code to execute"""
    print("\n" + "="*80)
    print("INSTRUCTIONS FOR CLAUDE CODE")
    print("="*80)
    print("""
This script needs product data from Google Ads API.

**Workflow for Claude:**

1. Load client configuration:
   - Read tools/product-impact-analyzer/config.json
   - Get list of enabled clients

2. For each enabled client:

   a) Generate and run GAQL query:
      query, start_date, end_date = generate_gaql_query(days_back=1)

      results = mcp__google-ads__run_gaql(
          customer_id=client['google_ads_customer_id'],
          query=query
      )

   b) Save results to cache:
      save_gaql_results(customer_id, results['results'])

3. Run the snapshot script:
   python snapshot_product_feed.py

4. Read the output files:
   - data/snapshot_{client}_{date}.json - Current snapshot
   - data/price_changes.json - Detected changes

5. Write to Google Sheets:

   a) Append snapshot to "Product Feed History" sheet
   b) Append changes to "Price Change Log" sheet
   c) Update "Outliers Report" with price change details

6. Report summary to user

**Example Claude workflow:**

# Step 1: Load config
config = json.load(open('tools/product-impact-analyzer/config.json'))

# Step 2: For each client
for client in config['clients']:
    if not client['enabled']:
        continue

    # Generate query
    query = f'''
    SELECT
        segments.product_item_id,
        segments.product_title,
        segments.date,
        metrics.clicks,
        metrics.impressions,
        metrics.cost_micros
    FROM shopping_performance_view
    WHERE segments.date = '2025-10-29'
    ORDER BY segments.product_item_id
    '''

    # Fetch via MCP
    results = mcp__google-ads__run_gaql(
        customer_id=client['google_ads_customer_id'],
        query=query
    )

    # Cache locally
    save_gaql_results(client['google_ads_customer_id'], results['results'])

# Step 3: Run snapshot
subprocess.run(['python', 'snapshot_product_feed.py'])

# Step 4: Read outputs and write to Sheets via MCP

""")
    print("="*80)


def main():
    """Main orchestration"""
    parser = argparse.ArgumentParser(description='Run product feed snapshot via Claude Code')
    parser.add_argument('--client', help='Client name to process')
    parser.add_argument('--all', action='store_true', help='Process all enabled clients')
    parser.add_argument('--instructions', action='store_true', help='Show instructions for Claude')

    args = parser.parse_args()

    if args.instructions or len(sys.argv) == 1:
        print_instructions_for_claude()
        return 0

    print("This script is designed to be called by Claude Code with MCP integration.")
    print("Run with --instructions to see the workflow.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
