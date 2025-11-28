#!/usr/bin/env python3
"""
Reconstruct historical Product Hero labels (Aug-Oct 2025) based on:
1. Campaign placement (campaign names reveal segmentation intent)
2. Conversion patterns (30-day lookback to distinguish heroes from sidekicks)

Strategy:
- Heroes campaign → heroes
- H&S campaign + 2+ conversions → heroes
- H&S campaign + 1 conversion → sidekicks
- H&S campaign + 0 conversions → sidekicks (low confidence)
- Zombies campaign → zombies
- Villains campaign → villains
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Configuration
CONFIG_FILE = Path(__file__).parent / "config.json"
GOOGLE_ADS_CONFIG = Path.home() / "google-ads.yaml"

# Months to reconstruct
MONTHS = [
    ("2025-08-01", "2025-08-31", "2025-08"),
    ("2025-09-01", "2025-09-30", "2025-09"),
    ("2025-10-01", "2025-10-31", "2025-10"),
]

def load_config():
    """Load client configuration"""
    with open(CONFIG_FILE) as f:
        return json.load(f)

def detect_campaign_intent(campaign_name):
    """
    Detect label intent from campaign name.

    Returns:
        tuple: (intent, confidence)
        intent: 'heroes', 'sidekicks', 'villains', 'zombies', 'h&s', 'h&s_zombies', 'unknown'
        confidence: 'high', 'medium', 'low'
    """
    name_lower = campaign_name.lower()

    # Tree2mydoor terminology mappings:
    # - "highly profitable" or "HP&P" → Heroes & Sidekicks (highly profitable & profitable)
    # - "profitable" → Sidekicks
    # - "unprofitable" → Villains
    # - "low traffic" → Zombies

    # Exact patterns (high confidence)
    if 'heroes' in name_lower and 'sidekick' not in name_lower and 'zombie' not in name_lower:
        return ('heroes', 'high')

    if 'villain' in name_lower or 'unprofitable' in name_lower:
        return ('villains', 'high')

    if 'zombie' in name_lower and ('h&s' in name_lower or 'hs' in name_lower):
        return ('h&s_zombies', 'high')

    if 'zombie' in name_lower or 'low traffic' in name_lower:
        return ('zombies', 'high')

    # H&S patterns (need conversion data to disambiguate)
    # Includes Tree2mydoor's "HP&P" (Highly Profitable & Profitable)
    if ('h&s' in name_lower or
        'hs' in name_lower or
        ('heroes' in name_lower and 'sidekick' in name_lower) or
        'hp&p' in name_lower or
        'highly profitable' in name_lower):
        return ('h&s', 'medium')

    # Profitable only → sidekicks
    if 'profitable' in name_lower and 'highly' not in name_lower and 'un' not in name_lower:
        return ('sidekicks', 'high')

    return ('unknown', 'low')

def fetch_product_placements(client_config, start_date, end_date):
    """
    Fetch which campaigns each product was in during this period.

    Returns:
        dict: {product_id: [(campaign_name, impressions, clicks)]}
    """
    customer_id = client_config["google_ads_customer_id"]
    label_field = client_config["label_tracking"]["label_field"]
    label_number = label_field.split("_")[-1]

    client = GoogleAdsClient.load_from_storage(str(GOOGLE_ADS_CONFIG))
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
          segments.product_item_id,
          campaign.name,
          metrics.impressions,
          metrics.clicks,
          metrics.conversions
        FROM shopping_performance_view
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    """

    placements = defaultdict(list)

    try:
        request = client.get_type("SearchGoogleAdsStreamRequest")
        request.customer_id = customer_id
        request.query = query

        stream = ga_service.search_stream(request=request)

        # Aggregate by product + campaign (since GAQL returns daily rows)
        temp_aggregation = defaultdict(lambda: defaultdict(lambda: {"impressions": 0, "clicks": 0, "conversions": 0}))

        for batch in stream:
            for row in batch.results:
                product_id = row.segments.product_item_id
                campaign_name = row.campaign.name
                impressions = row.metrics.impressions
                clicks = row.metrics.clicks
                conversions = row.metrics.conversions

                if product_id and campaign_name:
                    temp_aggregation[product_id][campaign_name]["impressions"] += impressions
                    temp_aggregation[product_id][campaign_name]["clicks"] += clicks
                    temp_aggregation[product_id][campaign_name]["conversions"] += conversions

        # Convert to final format
        for product_id, campaigns in temp_aggregation.items():
            for campaign_name, metrics in campaigns.items():
                placements[product_id].append({
                    "campaign": campaign_name,
                    "impressions": metrics["impressions"],
                    "clicks": metrics["clicks"],
                    "conversions": metrics["conversions"]
                })

        return placements

    except GoogleAdsException as ex:
        print(f"❌ Google Ads API Error:")
        for error in ex.failure.errors:
            print(f"  {error.message}")
        return None

def infer_label(placements, product_id):
    """
    Infer historical label from campaign placement and conversion data.

    Args:
        placements: List of campaign placements for this product
        product_id: Product ID

    Returns:
        dict: {
            "label": str,
            "confidence": str,
            "evidence": dict
        }
    """
    if not placements:
        return {
            "label": "not_active",
            "confidence": "high",
            "evidence": {"reason": "No campaign placement"}
        }

    # Use campaign with most impressions as primary
    primary = max(placements, key=lambda x: x["impressions"])

    campaign_name = primary["campaign"]
    conversions = primary["conversions"]

    intent, base_confidence = detect_campaign_intent(campaign_name)

    # Apply inference rules
    if intent == 'heroes':
        return {
            "label": "heroes",
            "confidence": "high",
            "evidence": {
                "campaign": campaign_name,
                "conversions": conversions,
                "rule": "Heroes campaign"
            }
        }

    elif intent == 'villains':
        return {
            "label": "villains",
            "confidence": "high",
            "evidence": {
                "campaign": campaign_name,
                "conversions": conversions,
                "rule": "Villains campaign"
            }
        }

    elif intent == 'zombies':
        return {
            "label": "zombies",
            "confidence": "high",
            "evidence": {
                "campaign": campaign_name,
                "conversions": conversions,
                "rule": "Zombies campaign"
            }
        }

    elif intent == 'h&s_zombies':
        return {
            "label": "zombies",
            "confidence": "high",
            "evidence": {
                "campaign": campaign_name,
                "conversions": conversions,
                "rule": "H&S Zombies campaign (demoted from H&S)"
            }
        }

    elif intent == 'h&s':
        # Distinguish heroes from sidekicks by conversion count
        if conversions >= 2:
            return {
                "label": "heroes",
                "confidence": "high",
                "evidence": {
                    "campaign": campaign_name,
                    "conversions": conversions,
                    "rule": "H&S campaign with 2+ conversions"
                }
            }
        elif conversions == 1:
            return {
                "label": "sidekicks",
                "confidence": "medium",
                "evidence": {
                    "campaign": campaign_name,
                    "conversions": conversions,
                    "rule": "H&S campaign with 1 conversion"
                }
            }
        else:
            # 0 conversions - likely sidekick or misplaced zombie
            return {
                "label": "sidekicks",
                "confidence": "low",
                "evidence": {
                    "campaign": campaign_name,
                    "conversions": conversions,
                    "rule": "H&S campaign with 0 conversions (possibly misplaced)"
                }
            }

    else:
        # Unknown campaign pattern - use conversion heuristic only
        if conversions >= 2:
            label = "heroes"
            confidence = "low"
        elif conversions == 1:
            label = "sidekicks"
            confidence = "low"
        else:
            label = "zombies"
            confidence = "low"

        return {
            "label": label,
            "confidence": confidence,
            "evidence": {
                "campaign": campaign_name,
                "conversions": conversions,
                "rule": f"Unknown campaign pattern, inferred from {conversions} conversions"
            }
        }

def reconstruct_month(client_config, start_date, end_date, month_label):
    """
    Reconstruct labels for a specific month.
    """
    client_name = client_config["name"].lower().replace(" ", "-")

    print(f"\n{'='*80}")
    print(f"RECONSTRUCTING: {client_config['name']} - {month_label}")
    print(f"{'='*80}")
    print(f"Period: {start_date} to {end_date}")

    # Fetch placements
    print(f"\nFetching campaign placements...")
    placements = fetch_product_placements(client_config, start_date, end_date)

    if placements is None:
        print(f"❌ Failed to fetch placements")
        return None

    print(f"Found {len(placements)} products with placements")

    # Infer labels
    print(f"\nInferring labels from placements and conversions...")
    reconstructed = {}
    confidence_counts = defaultdict(int)
    label_counts = defaultdict(int)

    for product_id, product_placements in placements.items():
        result = infer_label(product_placements, product_id)
        reconstructed[product_id] = result

        confidence_counts[result["confidence"]] += 1
        label_counts[result["label"]] += 1

    print(f"\nReconstructed {len(reconstructed)} products:")
    print(f"  By label: {dict(label_counts)}")
    print(f"  By confidence: {dict(confidence_counts)}")

    # Save snapshot
    client_dir = Path(__file__).parent / "history" / "label-transitions" / client_name
    client_dir.mkdir(parents=True, exist_ok=True)

    snapshot = {
        "month": month_label,
        "last_updated": datetime.now().isoformat(),
        "source": "reconstructed",
        "reconstruction_method": "campaign_placement_and_conversions",
        "date_range": {
            "start": start_date,
            "end": end_date
        },
        "total_products": len(reconstructed),
        "label_distribution": dict(label_counts),
        "confidence_distribution": dict(confidence_counts),
        "products": reconstructed
    }

    output_file = client_dir / f"{month_label}-reconstructed.json"
    with open(output_file, 'w') as f:
        json.dump(snapshot, f, indent=2)

    print(f"\n✅ Saved to: {output_file}")

    return snapshot

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 reconstruct_historical_labels.py <client-name>")
        print("  python3 reconstruct_historical_labels.py --all")
        print()
        print("This will reconstruct Aug-Oct 2025 labels based on:")
        print("  - Campaign placement (Heroes, H&S, Villains, Zombies)")
        print("  - Conversion patterns (2+ = heroes, 1 = sidekicks, 0 = sidekicks)")
        return

    config = load_config()

    if sys.argv[1] == "--all":
        clients_to_process = [
            c for c in config["clients"]
            if c.get("enabled") and c.get("label_tracking", {}).get("enabled")
        ]

        print(f"\n{'='*80}")
        print(f"HISTORICAL LABEL RECONSTRUCTION")
        print(f"{'='*80}")
        print(f"Clients: {len(clients_to_process)}")
        print(f"Months: August, September, October 2025")
        print(f"Method: Campaign placement + conversion analysis")
        print(f"{'='*80}")

        results = []

        for client in clients_to_process:
            for start_date, end_date, month_label in MONTHS:
                snapshot = reconstruct_month(client, start_date, end_date, month_label)

                if snapshot:
                    results.append({
                        "client": client["name"],
                        "month": month_label,
                        "products": snapshot["total_products"],
                        "high_confidence": snapshot["confidence_distribution"].get("high", 0),
                        "medium_confidence": snapshot["confidence_distribution"].get("medium", 0),
                        "low_confidence": snapshot["confidence_distribution"].get("low", 0)
                    })

        print(f"\n{'='*80}")
        print(f"RECONSTRUCTION SUMMARY")
        print(f"{'='*80}")
        for r in results:
            print(f"{r['client']:30} {r['month']}: {r['products']:4} products "
                  f"(H:{r['high_confidence']} M:{r['medium_confidence']} L:{r['low_confidence']})")

    else:
        # Single client
        client_name = sys.argv[1]

        client = None
        for c in config["clients"]:
            if c["name"].lower().replace(" ", "-") == client_name:
                client = c
                break

        if not client:
            print(f"❌ Client not found: {client_name}")
            return

        for start_date, end_date, month_label in MONTHS:
            reconstruct_month(client, start_date, end_date, month_label)

if __name__ == "__main__":
    main()
