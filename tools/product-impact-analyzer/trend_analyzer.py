#!/usr/bin/env python3
"""
Trend Analysis and Anomaly Detection for Product Impact Analyzer

Analyzes historical impact data to identify:
- Recurring patterns (e.g., seasonal price changes)
- Anomalies (unexpected performance changes)
- Trends over time
- Predictive insights

Usage:
    from trend_analyzer import TrendAnalyzer

    analyzer = TrendAnalyzer(history_dir="history/")
    trends = analyzer.analyze_trends()
    anomalies = analyzer.detect_anomalies()
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import statistics


@dataclass
class TrendMetrics:
    """Trend metrics for a product over time"""
    product_id: str
    product_title: str
    client: str

    # Historical performance
    avg_revenue_impact: float
    avg_clicks_impact: float
    total_changes: int

    # Trend indicators
    improving: bool  # Getting better over time
    volatile: bool   # High variance in impacts

    # Recent vs historical
    recent_avg: float  # Last 4 weeks
    historical_avg: float  # Before last 4 weeks


@dataclass
class Anomaly:
    """Represents an anomalous impact"""
    product_id: str
    product_title: str
    client: str
    date: str

    revenue_impact: float
    expected_impact: float
    deviation_percent: float

    anomaly_type: str  # "spike", "drop", "unusual"
    severity: str  # "low", "medium", "high"


class TrendAnalyzer:
    """Analyzes historical impact data for trends and anomalies"""

    def __init__(self, history_dir: Path):
        """Initialize with path to history directory"""
        self.history_dir = Path(history_dir)
        self.historical_data = self._load_all_history()

    def _load_all_history(self) -> List[Dict]:
        """Load all historical analysis files"""
        all_data = []

        if not self.history_dir.exists():
            return all_data

        for history_file in sorted(self.history_dir.glob("analysis_*.json")):
            try:
                with open(history_file) as f:
                    data = json.load(f)
                    # Add filename date to each record
                    date = history_file.stem.replace("analysis_", "")
                    for record in data:
                        record['_analysis_date'] = date
                    all_data.extend(data)
            except Exception as e:
                print(f"Warning: Could not load {history_file}: {e}")

        return all_data

    def get_product_history(self, client: str, product_id: str) -> List[Dict]:
        """Get all historical analyses for a specific product"""
        return [
            record for record in self.historical_data
            if record['client'] == client and record['product_id'] == product_id
        ]

    def analyze_trends(self) -> List[TrendMetrics]:
        """Analyze trends for all products"""
        # Group by client + product_id
        by_product = defaultdict(list)
        for record in self.historical_data:
            key = (record['client'], record['product_id'])
            by_product[key].append(record)

        trends = []
        for (client, product_id), records in by_product.items():
            if len(records) < 2:  # Need at least 2 data points
                continue

            # Sort by date
            records = sorted(records, key=lambda r: r.get('_analysis_date', ''))

            # Extract revenue impacts (skip None values)
            revenue_impacts = [
                r['revenue_change_abs']
                for r in records
                if r['revenue_change_abs'] is not None
            ]

            if len(revenue_impacts) < 2:
                continue

            # Extract clicks impacts
            clicks_impacts = [
                r['clicks_change_pct']
                for r in records
                if r['clicks_change_pct'] is not None
            ]

            # Calculate metrics
            avg_revenue = statistics.mean(revenue_impacts)
            avg_clicks = statistics.mean(clicks_impacts) if clicks_impacts else 0

            # Check if improving (recent better than historical)
            recent = revenue_impacts[-2:]  # Last 2
            historical = revenue_impacts[:-2] if len(revenue_impacts) > 2 else revenue_impacts

            recent_avg = statistics.mean(recent) if recent else 0
            historical_avg = statistics.mean(historical) if historical else 0
            improving = recent_avg > historical_avg

            # Check volatility (high standard deviation)
            volatile = False
            if len(revenue_impacts) >= 3:
                stdev = statistics.stdev(revenue_impacts)
                mean = abs(avg_revenue)
                if mean > 0 and (stdev / mean) > 0.5:  # 50% coefficient of variation
                    volatile = True

            trend = TrendMetrics(
                product_id=product_id,
                product_title=records[0]['product_title'],
                client=client,
                avg_revenue_impact=avg_revenue,
                avg_clicks_impact=avg_clicks,
                total_changes=len(records),
                improving=improving,
                volatile=volatile,
                recent_avg=recent_avg,
                historical_avg=historical_avg
            )

            trends.append(trend)

        return trends

    def detect_anomalies(self, threshold: float = 2.0) -> List[Anomaly]:
        """Detect anomalies using statistical methods

        Args:
            threshold: Number of standard deviations to consider anomalous
        """
        # Group by client + product
        by_product = defaultdict(list)
        for record in self.historical_data:
            if record['revenue_change_abs'] is None:
                continue
            key = (record['client'], record['product_id'])
            by_product[key].append(record)

        anomalies = []

        for (client, product_id), records in by_product.items():
            if len(records) < 3:  # Need at least 3 points for meaningful stats
                continue

            # Extract revenue impacts
            revenue_impacts = [r['revenue_change_abs'] for r in records]

            # Calculate mean and stdev
            mean = statistics.mean(revenue_impacts)
            stdev = statistics.stdev(revenue_impacts) if len(revenue_impacts) > 1 else 0

            if stdev == 0:
                continue

            # Check each record for anomalies
            for record in records:
                impact = record['revenue_change_abs']

                # Calculate z-score
                z_score = abs((impact - mean) / stdev)

                if z_score > threshold:
                    deviation_pct = ((impact - mean) / abs(mean) * 100) if mean != 0 else 0

                    # Classify anomaly type
                    if impact > mean + (threshold * stdev):
                        anomaly_type = "spike"
                    elif impact < mean - (threshold * stdev):
                        anomaly_type = "drop"
                    else:
                        anomaly_type = "unusual"

                    # Classify severity
                    if z_score > 3:
                        severity = "high"
                    elif z_score > 2.5:
                        severity = "medium"
                    else:
                        severity = "low"

                    anomaly = Anomaly(
                        product_id=product_id,
                        product_title=record['product_title'],
                        client=client,
                        date=record.get('_analysis_date', 'unknown'),
                        revenue_impact=impact,
                        expected_impact=mean,
                        deviation_percent=deviation_pct,
                        anomaly_type=anomaly_type,
                        severity=severity
                    )

                    anomalies.append(anomaly)

        return anomalies

    def generate_insights(self) -> Dict[str, any]:
        """Generate high-level insights from trends and anomalies"""
        trends = self.analyze_trends()
        anomalies = self.detect_anomalies()

        # Count improving vs declining products
        improving_count = sum(1 for t in trends if t.improving)
        declining_count = sum(1 for t in trends if not t.improving)

        # Find most volatile products
        volatile = [t for t in trends if t.volatile]
        volatile = sorted(volatile, key=lambda t: abs(t.avg_revenue_impact), reverse=True)

        # Find high-severity anomalies
        critical_anomalies = [a for a in anomalies if a.severity == "high"]

        # Calculate average impact by client
        by_client = defaultdict(list)
        for trend in trends:
            by_client[trend.client].append(trend.avg_revenue_impact)

        client_averages = {
            client: statistics.mean(impacts)
            for client, impacts in by_client.items()
        }

        return {
            'total_products_tracked': len(trends),
            'improving_products': improving_count,
            'declining_products': declining_count,
            'volatile_products': len(volatile),
            'top_volatile': volatile[:5],  # Top 5
            'total_anomalies': len(anomalies),
            'critical_anomalies': len(critical_anomalies),
            'anomaly_details': critical_anomalies[:10],  # Top 10
            'client_averages': client_averages,
            'data_date_range': self._get_date_range()
        }

    def _get_date_range(self) -> Tuple[str, str]:
        """Get the date range of historical data"""
        if not self.historical_data:
            return ("N/A", "N/A")

        dates = [r.get('_analysis_date', '') for r in self.historical_data if r.get('_analysis_date')]
        if not dates:
            return ("N/A", "N/A")

        return (min(dates), max(dates))


def main():
    """Test trend analyzer"""
    import sys

    history_dir = Path(__file__).parent / "history"

    if not history_dir.exists() or not list(history_dir.glob("*.json")):
        print("No historical data found in history/")
        print("Run some analyses first to build up historical data.")
        return 1

    analyzer = TrendAnalyzer(history_dir)

    print("TREND ANALYSIS")
    print("="*80)

    insights = analyzer.generate_insights()

    print(f"\nData Range: {insights['data_date_range'][0]} to {insights['data_date_range'][1]}")
    print(f"Products Tracked: {insights['total_products_tracked']}")
    print(f"Improving: {insights['improving_products']}")
    print(f"Declining: {insights['declining_products']}")
    print(f"Volatile: {insights['volatile_products']}")
    print(f"\nAnomalies Detected: {insights['total_anomalies']}")
    print(f"Critical Anomalies: {insights['critical_anomalies']}")

    if insights['anomaly_details']:
        print("\nTop Critical Anomalies:")
        for anomaly in insights['anomaly_details']:
            print(f"  {anomaly.client} - {anomaly.product_id}: {anomaly.product_title[:50]}")
            print(f"    Date: {anomaly.date}")
            print(f"    Impact: £{anomaly.revenue_impact:.2f} (expected: £{anomaly.expected_impact:.2f})")
            print(f"    Type: {anomaly.anomaly_type} | Severity: {anomaly.severity}")
            print()

    print("\nClient Performance Averages:")
    for client, avg in insights['client_averages'].items():
        print(f"  {client}: £{avg:+.2f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
