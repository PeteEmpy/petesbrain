#!/usr/bin/env python3
"""
Google Ads Diagnostics Monitor - Clear Prospects

Tracks the "Product status" diagnostics data that Michael checks daily at 7 AM.
Monitors for unexpected changes in "Not eligible" products.

Baseline (Nov 2025):
- ~9,600 products: Custom label "ads off" (intentionally excluded)
- ~3,183 products: Not actively advertised (seasonal/low performers)
- Total "No campaigns advertising": ~12,783 (76% of not eligible)
- Actual issues needing fixes: ~41 products (0.18%)

Runs: Daily at 6:30 AM (before Michael's 7 AM check)
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
except ImportError:
    print("ERROR: google-ads-python library not installed")
    print("Install with: pip install google-ads")
    sys.exit(1)


class DiagnosticsMonitor:
    """Monitor Google Ads Diagnostics for Clear Prospects brands"""

    # Clear Prospects account
    CUSTOMER_ID = "6281395727"

    # Merchant Center IDs
    MERCHANT_IDS = {
        "HappySnapGifts": "7481296",
        "WheatyBags": "7481286",
        "BMPM": "7522326"
    }

    # Baseline thresholds (Nov 2025)
    BASELINE = {
        "no_campaigns_advertising": 12783,  # Expected (9,600 "ads off" + 3,183 not active)
        "missing_shopping_info": 14,
        "missing_age_group": 11,
        "missing_size": 11,
        "missing_color": 2,
        "unavailable_landing_page": 1,
        "offensive_content": 1,
        "invalid_gtin": 1
    }

    # Alert thresholds (percentage increase that triggers alert)
    ALERT_THRESHOLDS = {
        "no_campaigns_advertising": 0.10,  # 10% increase (e.g., 12,783 → 14,061)
        "missing_shopping_info": 5,  # Absolute increase of 5+ products
        "unavailable_landing_page": 3,  # Absolute increase of 3+ (critical issue)
        "offensive_content": 1,  # Any increase is critical
        "total_not_eligible": 0.15  # 15% increase in total
    }

    def __init__(self):
        """Initialize with Google Ads client"""
        google_ads_yaml = os.path.expanduser("~/google-ads.yaml")
        if not os.path.exists(google_ads_yaml):
            raise ValueError(f"google-ads.yaml not found at {google_ads_yaml}")

        self.client = GoogleAdsClient.load_from_storage(google_ads_yaml)

        # Data directory
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)

        self.snapshot_file = self.data_dir / "diagnostics_snapshot.json"
        self.history_file = self.data_dir / "diagnostics_history.json"

    def get_diagnostics_data(self) -> Dict:
        """
        Query Google Ads API for diagnostics issue counts

        Returns dict with issue counts per category
        """
        ga_service = self.client.get_service("GoogleAdsService")

        # This query gets shopping products grouped by approval status
        # Note: The exact query may need adjustment based on API capabilities
        query = """
            SELECT
                shopping_product_stats.channel,
                shopping_product_stats.channel_exclusive,
                shopping_product_stats.condition,
                shopping_product_stats.status,
                shopping_product_stats.issue_count,
                shopping_product_stats.disapproval_date,
                shopping_product_stats.product_type_l1,
                shopping_product_stats.product_item_id
            FROM shopping_product_stats
            WHERE segments.date = TODAY
        """

        # Alternative: Get product counts from shopping_performance_view
        # This is more reliable for detecting changes
        performance_query = """
            SELECT
                segments.product_item_id,
                segments.product_title,
                metrics.impressions
            FROM shopping_performance_view
            WHERE segments.date DURING LAST_7_DAYS
        """

        diagnostics = {
            "timestamp": datetime.now().isoformat(),
            "customer_id": self.CUSTOMER_ID,
            "products_with_zero_impressions": 0,
            "products_serving": 0,
            "total_products": 0
        }

        try:
            search_request = self.client.get_type("SearchGoogleAdsRequest")
            search_request.customer_id = self.CUSTOMER_ID
            search_request.query = performance_query

            response = ga_service.search(request=search_request)

            product_ids = set()
            zero_impression_products = set()

            for row in response:
                product_id = row.segments.product_item_id
                impressions = row.metrics.impressions

                product_ids.add(product_id)

                if impressions == 0:
                    zero_impression_products.add(product_id)

            diagnostics["total_products"] = len(product_ids)
            diagnostics["products_with_zero_impressions"] = len(zero_impression_products)
            diagnostics["products_serving"] = len(product_ids) - len(zero_impression_products)

        except GoogleAdsException as ex:
            print(f"ERROR: Google Ads API error: {ex}")
            return None

        return diagnostics

    def check_for_alerts(self, current: Dict, previous: Dict) -> List[Dict]:
        """
        Compare current diagnostics to previous and baseline

        Returns list of alerts if thresholds exceeded
        """
        alerts = []

        if not previous:
            return []  # First run, no comparison

        # Check zero impression products (proxy for "not eligible")
        zero_current = current.get("products_with_zero_impressions", 0)
        zero_previous = previous.get("products_with_zero_impressions", 0)
        baseline_total = self.BASELINE["no_campaigns_advertising"]

        # Alert if significant increase
        if zero_current > zero_previous:
            increase = zero_current - zero_previous
            pct_increase = (increase / zero_previous * 100) if zero_previous > 0 else 0

            if increase >= 100 or pct_increase >= 10:  # 100+ products or 10% increase
                alerts.append({
                    "type": "zero_impressions_spike",
                    "severity": "warning",
                    "current": zero_current,
                    "previous": zero_previous,
                    "increase": increase,
                    "pct_increase": round(pct_increase, 1),
                    "message": f"Zero-impression products increased by {increase} (+{pct_increase:.1f}%)"
                })

        # Alert if above baseline
        if zero_current > baseline_total * 1.15:  # 15% above baseline
            alerts.append({
                "type": "above_baseline",
                "severity": "warning",
                "current": zero_current,
                "baseline": baseline_total,
                "difference": zero_current - baseline_total,
                "message": f"Zero-impression products ({zero_current}) significantly above baseline ({baseline_total})"
            })

        return alerts

    def save_snapshot(self, diagnostics: Dict):
        """Save current diagnostics to snapshot file"""
        with open(self.snapshot_file, 'w') as f:
            json.dump(diagnostics, f, indent=2)

    def load_previous_snapshot(self) -> Dict:
        """Load previous diagnostics snapshot"""
        if not self.snapshot_file.exists():
            return {}

        with open(self.snapshot_file, 'r') as f:
            return json.load(f)

    def save_to_history(self, diagnostics: Dict):
        """Append current diagnostics to history"""
        history = []
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                history = json.load(f)

        history.append(diagnostics)

        # Keep last 90 days only
        cutoff_date = datetime.now() - timedelta(days=90)
        history = [
            h for h in history
            if datetime.fromisoformat(h["timestamp"]) > cutoff_date
        ]

        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def run(self):
        """Main monitoring workflow"""
        print("="*80)
        print("GOOGLE ADS DIAGNOSTICS MONITOR")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print()

        # Get current diagnostics
        print("Fetching diagnostics data...")
        current = self.get_diagnostics_data()

        if not current:
            print("ERROR: Failed to fetch diagnostics data")
            return

        # Load previous snapshot
        previous = self.load_previous_snapshot()

        # Check for alerts
        alerts = self.check_for_alerts(current, previous)

        # Display results
        print(f"Total products in feed: {current['total_products']}")
        print(f"Products serving (with impressions): {current['products_serving']}")
        print(f"Products with zero impressions (proxy for 'not eligible'): {current['products_with_zero_impressions']}")
        print()

        if previous:
            prev_zero = previous.get('products_with_zero_impressions', 0)
            change = current['products_with_zero_impressions'] - prev_zero
            if change > 0:
                print(f"⚠️  CHANGE: +{change} products since last check")
            elif change < 0:
                print(f"✓ IMPROVEMENT: {abs(change)} fewer products with issues")
            else:
                print("✓ No change since last check")
            print()

        # Display alerts
        if alerts:
            print("🚨 ALERTS:")
            for alert in alerts:
                print(f"  [{alert['severity'].upper()}] {alert['message']}")
            print()
        else:
            print("✅ No alerts - diagnostics within normal range")
            print()

        # Save snapshot and history
        self.save_snapshot(current)
        self.save_to_history(current)

        print(f"✓ Snapshot saved to {self.snapshot_file}")
        print(f"✓ History updated in {self.history_file}")


def main():
    """Entry point"""
    monitor = DiagnosticsMonitor()
    monitor.run()


if __name__ == "__main__":
    main()
