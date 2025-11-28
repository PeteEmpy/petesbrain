#!/usr/bin/env python3
"""
Historical Label Backfill Script

Reconstructs Product Hero labels for historical dates (before Nov 1, 2025)
using campaign naming conventions and performance data.

Usage:
    python backfill_historical_labels.py --client "Accessories for the Home" \\
        --start-date 2025-10-01 --end-date 2025-10-31

    python backfill_historical_labels.py --all-clients \\
        --start-date 2025-10-01 --end-date 2025-10-31
"""

import json
import sys
import os
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import defaultdict

# Import label inference module
from label_inference import LabelInferencer, InferredLabel, LabelConfidence

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

def fetch_product_campaigns_for_date(customer_id, target_date):
    """
    Fetch which campaign each product was in on a specific date.

    Returns: dict of {product_id: campaign_name}
    """
    # This would use Google Ads change history API or shopping_performance_view
    # For now, outline the query needed

    query = f"""
    SELECT
      segments.product_item_id,
      campaign.name,
      metrics.clicks
    FROM shopping_performance_view
    WHERE segments.date = '{target_date}'
      AND metrics.impressions > 0
    """

    print(f"    Query needed: {query}")
    print(f"    ⚠️  MCP integration required")

    # Placeholder
    return {}

def fetch_product_performance(customer_id, product_id, start_date, end_date):
    """
    Fetch performance metrics for a product over a date range.

    Returns: {
        "clicks_30d": int,
        "conversions_30d": float,
        "revenue_30d": float
    }
    """
    query = f"""
    SELECT
      SUM(metrics.clicks) as clicks,
      SUM(metrics.conversions) as conversions,
      SUM(metrics.conversions_value) as revenue
    FROM shopping_performance_view
    WHERE segments.product_item_id = '{product_id}'
      AND segments.date BETWEEN '{start_date}' AND '{end_date}'
    """

    print(f"    Query: {query}")

    # Placeholder
    return {
        "clicks_30d": 0,
        "conversions_30d": 0,
        "revenue_30d": 0
    }

def backfill_client_labels(
    client_config,
    start_date: date,
    end_date: date
):
    """
    Backfill historical labels for one client.

    Args:
        client_config: Client configuration dict
        start_date: First date to backfill
        end_date: Last date to backfill
    """
    client_name = client_config["name"]
    customer_id = client_config["google_ads_customer_id"]

    # Check if label tracking is configured
    label_config = client_config.get("label_tracking", {})
    if not label_config.get("enabled", False):
        print(f"  ⏭️  Label tracking not enabled for {client_name}")
        return

    assessment_window = label_config.get("assessment_window_days", 30)

    print(f"\n{'='*60}")
    print(f"Backfilling: {client_name}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"Assessment window: {assessment_window} days")
    print(f"{'='*60}")

    # Initialize inferencer
    inferencer = LabelInferencer(assessment_window_days=assessment_window)

    # Group inferred labels by month
    monthly_inferences = defaultdict(list)

    # Iterate through each date
    current_date = start_date
    while current_date <= end_date:
        print(f"\n  Processing: {current_date}")

        # Fetch product-campaign mapping for this date
        product_campaigns = fetch_product_campaigns_for_date(customer_id, current_date)

        if not product_campaigns:
            print(f"    ⚠️  No data (MCP needed)")
            current_date += timedelta(days=1)
            continue

        # For each product, infer its label
        for product_id, campaign_name in product_campaigns.items():
            # Fetch performance for assessment window
            perf_start = current_date - timedelta(days=assessment_window)
            perf_end = current_date

            performance_data = fetch_product_performance(
                customer_id,
                product_id,
                perf_start.isoformat(),
                perf_end.isoformat()
            )

            # Infer label
            inferred = inferencer.infer_label(
                product_id=product_id,
                date=current_date.isoformat(),
                campaign_name=campaign_name,
                performance_data=performance_data
            )

            # Store inference
            year_month = current_date.strftime("%Y-%m")
            monthly_inferences[year_month].append({
                "product_id": product_id,
                "date": current_date.isoformat(),
                "inferred_label": inferred.label,
                "confidence": inferred.confidence.value,
                "campaign": campaign_name,
                "evidence": inferred.evidence
            })

        current_date += timedelta(days=1)

    # Save monthly inference files
    history_dir = get_history_dir(client_name)

    for year_month, inferences in monthly_inferences.items():
        monthly_file = history_dir / f"{year_month}.json"

        monthly_data = {
            "month": year_month,
            "note": (
                "Labels for this period are INFERRED from campaign names and "
                "performance data. Actual Product Hero labels not available "
                "before Nov 1, 2025."
            ),
            "backfill_date": datetime.now().isoformat(),
            "method": "campaign_name_inference",
            "inferred_labels": inferences
        }

        with open(monthly_file, 'w') as f:
            json.dump(monthly_data, f, indent=2)

        print(f"\n  ✅ Saved {len(inferences)} inferences to {year_month}.json")

    print(f"\n{'='*60}")
    print(f"✅ Backfill complete for {client_name}")
    print(f"{'='*60}")

def main():
    """Main backfill process"""
    import argparse

    parser = argparse.ArgumentParser(description="Backfill historical Product Hero labels")
    parser.add_argument("--client", help="Client name to backfill")
    parser.add_argument("--all-clients", action="store_true", help="Backfill all enabled clients")
    parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    # Parse dates
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date()
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        return 1

    # Load config
    config = load_config()

    # Determine clients to process
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

    print(f"\n🔄 Historical Label Backfill")
    print(f"{'='*60}")
    print(f"Clients: {len(clients)}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"Method: Campaign name inference + performance data")
    print(f"{'='*60}")
    print(f"\n⚠️  WARNING: This script requires MCP integration to be complete.")
    print(f"Currently in blueprint/outline mode.")
    print(f"{'='*60}\n")

    for client in clients:
        try:
            backfill_client_labels(client, start_date, end_date)
        except Exception as e:
            print(f"❌ Error backfilling {client['name']}: {e}")
            import traceback
            traceback.print_exc()
            continue

    print(f"\n{'='*60}")
    print("✅ Backfill process complete")
    print(f"{'='*60}\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
