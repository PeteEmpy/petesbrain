#!/usr/bin/env python3
"""
Product Impact Analyzer - Phase 1 (Claude-Assisted)

Analyzes product feed changes and their impact on Google Ads Shopping performance.

Phase 1 Usage (via Claude Code):
    User: "Run the product impact analysis"
    Claude: Fetches data via MCP, runs this script, shows results

Phase 2 (Future - Standalone):
    python analyzer.py --auto

Architecture:
    - Input: JSON files with Sheets data and Google Ads data
    - Processing: Correlate changes with performance
    - Output: Impact analysis report (JSON + text summary)
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class ProductChange:
    """Represents a product change from the Outliers Report"""
    client: str
    product_id: str
    change_type: str  # REMOVED, NEW, MODIFIED, PRICE_CHANGE
    date_changed: str
    product_title: str
    days_since_change: int
    old_price: Optional[float] = None  # Price before change (micros)
    new_price: Optional[float] = None  # Price after change (micros)
    price_change_percent: Optional[float] = None  # Percentage change


@dataclass
class PerformanceMetrics:
    """Performance metrics for a time period"""
    impressions: int = 0
    clicks: int = 0
    conversions: float = 0.0
    revenue: float = 0.0
    cost: float = 0.0

    @property
    def ctr(self) -> float:
        return (self.clicks / self.impressions * 100) if self.impressions > 0 else 0

    @property
    def cpc(self) -> float:
        return (self.cost / self.clicks) if self.clicks > 0 else 0

    @property
    def conversion_rate(self) -> float:
        return (self.conversions / self.clicks * 100) if self.clicks > 0 else 0

    @property
    def roas(self) -> float:
        return (self.revenue / self.cost) if self.cost > 0 else 0


@dataclass
class ImpactAnalysis:
    """Analysis of a product change's impact"""
    client: str
    product_id: str
    product_title: str
    change_type: str
    date_changed: str
    days_since_change: int

    before: Optional[PerformanceMetrics]
    after: Optional[PerformanceMetrics]

    def clicks_change_pct(self) -> Optional[float]:
        if not self.before or not self.after or self.before.clicks == 0:
            return None
        return ((self.after.clicks - self.before.clicks) / self.before.clicks * 100)

    def revenue_change_pct(self) -> Optional[float]:
        if not self.before or not self.after or self.before.revenue == 0:
            return None
        return ((self.after.revenue - self.before.revenue) / self.before.revenue * 100)

    def revenue_change_abs(self) -> Optional[float]:
        if not self.before or not self.after:
            return None
        return self.after.revenue - self.before.revenue

    def impact_flag(self) -> str:
        """Returns emoji flag for impact severity"""
        revenue_change = self.revenue_change_abs()
        if revenue_change is None:
            return "⚪"  # No data

        if abs(revenue_change) < 10:
            return "⚪"  # Minimal
        elif revenue_change > 100:
            return "📈"  # Strong positive
        elif revenue_change > 0:
            return "🟢"  # Positive
        elif revenue_change > -100:
            return "🟠"  # Negative
        else:
            return "📉"  # Strong negative

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON output"""
        return {
            'client': self.client,
            'product_id': self.product_id,
            'product_title': self.product_title,
            'change_type': self.change_type,
            'date_changed': self.date_changed,
            'days_since_change': self.days_since_change,
            'impact_flag': self.impact_flag(),
            'before': asdict(self.before) if self.before else None,
            'after': asdict(self.after) if self.after else None,
            'clicks_change_pct': self.clicks_change_pct(),
            'revenue_change_pct': self.revenue_change_pct(),
            'revenue_change_abs': self.revenue_change_abs()
        }


def normalize_product_id(product_id: str) -> str:
    """
    Normalize product IDs for matching.

    Sheets: "287", "3539"
    Ads: "00287", "03539"

    Returns: Normalized form for comparison
    """
    if not product_id:
        return ""
    # Remove leading zeros but keep at least one character
    normalized = product_id.lstrip('0')
    return normalized if normalized else '0'


def parse_product_changes(outliers_data: List[List[str]]) -> List[ProductChange]:
    """
    Parse product changes from Outliers Report data.

    Expected format (with optional price columns):
    [["Client", "Product ID", "Change Type", "Date Changed", "Product Title", "Days Since Change", "Flag",
      "Old Price", "New Price", "Price Change %"], ...]
    """
    changes = []

    for row in outliers_data[1:]:  # Skip header
        if len(row) < 6:
            continue

        try:
            # Parse core fields
            change = ProductChange(
                client=row[0],
                product_id=normalize_product_id(row[1]),
                change_type=row[2],
                date_changed=row[3],
                product_title=row[4],
                days_since_change=int(row[5]) if row[5].isdigit() else 0
            )

            # Parse price fields if available (columns 7-9)
            if len(row) > 7 and row[7]:
                try:
                    change.old_price = float(row[7])
                except ValueError:
                    pass

            if len(row) > 8 and row[8]:
                try:
                    change.new_price = float(row[8])
                except ValueError:
                    pass

            if len(row) > 9 and row[9]:
                try:
                    change.price_change_percent = float(row[9].replace('%', ''))
                except ValueError:
                    pass

            changes.append(change)
        except (IndexError, ValueError) as e:
            print(f"Warning: Skipping invalid row: {row[:3] if len(row) >= 3 else row}")
            continue

    return changes


def aggregate_performance_by_product(ads_data: List[Dict],
                                     start_date: str,
                                     end_date: str) -> Dict[str, PerformanceMetrics]:
    """
    Aggregate Google Ads performance data by product for a date range.

    Returns: Dict mapping product_id -> PerformanceMetrics
    """
    performance_by_product = defaultdict(lambda: PerformanceMetrics())

    for row in ads_data:
        try:
            product_id = normalize_product_id(row['segments']['productItemId'])
            date = row['segments']['date']

            # Check if date is in range
            if not (start_date <= date <= end_date):
                continue

            metrics = row['metrics']
            perf = performance_by_product[product_id]

            perf.impressions += int(metrics.get('impressions', 0))
            perf.clicks += int(metrics.get('clicks', 0))
            perf.conversions += float(metrics.get('conversions', 0))
            perf.revenue += float(metrics.get('conversionsValue', 0))
            perf.cost += float(metrics.get('costMicros', 0)) / 1_000_000  # Convert micros to currency

        except (KeyError, ValueError) as e:
            print(f"Warning: Skipping invalid ads row: {e}")
            continue

    return dict(performance_by_product)


def analyze_impact(product_changes: List[ProductChange],
                   ads_data_by_client: Dict[str, List[Dict]],
                   comparison_days: int = 7) -> List[ImpactAnalysis]:
    """
    Correlate product changes with performance impact.

    For each product change:
    - Get performance N days before change
    - Get performance N days after change
    - Calculate impact metrics
    """
    analyses = []

    for change in product_changes:
        # Parse change date
        try:
            change_date = datetime.strptime(change.date_changed, '%d/%m/%Y')
        except ValueError:
            print(f"Warning: Invalid date format for {change.product_id}: {change.date_changed}")
            continue

        # Calculate before/after windows
        before_start = (change_date - timedelta(days=comparison_days)).strftime('%Y-%m-%d')
        before_end = (change_date - timedelta(days=1)).strftime('%Y-%m-%d')
        after_start = change_date.strftime('%Y-%m-%d')
        after_end = (change_date + timedelta(days=comparison_days)).strftime('%Y-%m-%d')

        # Get ads data for this client
        client_ads_data = ads_data_by_client.get(change.client, [])

        if not client_ads_data:
            print(f"Warning: No ads data for client {change.client}")
            continue

        # Aggregate performance for before/after periods
        perf_before_all = aggregate_performance_by_product(client_ads_data, before_start, before_end)
        perf_after_all = aggregate_performance_by_product(client_ads_data, after_start, after_end)

        # Get performance for this specific product
        perf_before = perf_before_all.get(change.product_id)
        perf_after = perf_after_all.get(change.product_id)

        # Create analysis
        analysis = ImpactAnalysis(
            client=change.client,
            product_id=change.product_id,
            product_title=change.product_title,
            change_type=change.change_type,
            date_changed=change.date_changed,
            days_since_change=change.days_since_change,
            before=perf_before,
            after=perf_after
        )

        analyses.append(analysis)

    return analyses


def generate_text_summary(analyses: List[ImpactAnalysis]) -> str:
    """Generate human-readable text summary"""

    summary_lines = []
    summary_lines.append("=" * 80)
    summary_lines.append("PRODUCT IMPACT ANALYSIS SUMMARY")
    summary_lines.append("=" * 80)
    summary_lines.append("")

    # Group by client
    by_client = defaultdict(list)
    for analysis in analyses:
        by_client[analysis.client].append(analysis)

    for client, client_analyses in by_client.items():
        summary_lines.append(f"\n{client}")
        summary_lines.append("-" * 80)

        # Filter for significant impacts
        significant = [a for a in client_analyses
                      if a.revenue_change_abs() and abs(a.revenue_change_abs()) > 10]

        if not significant:
            summary_lines.append("  No significant impacts detected")
            continue

        # Sort by absolute revenue impact
        significant.sort(key=lambda a: abs(a.revenue_change_abs() or 0), reverse=True)

        for analysis in significant[:10]:  # Top 10
            flag = analysis.impact_flag()
            product = f"{analysis.product_id}: {analysis.product_title[:60]}"
            rev_change = analysis.revenue_change_abs()
            rev_pct = analysis.revenue_change_pct()

            summary_lines.append(f"  {flag} {product}")
            summary_lines.append(f"     Change Type: {analysis.change_type}")
            summary_lines.append(f"     Revenue: £{rev_change:+.2f} ({rev_pct:+.1f}%)")

            if analysis.before and analysis.after:
                summary_lines.append(
                    f"     Clicks: {analysis.before.clicks} → {analysis.after.clicks} "
                    f"({analysis.clicks_change_pct():+.1f}%)"
                )

            # Show price change if available (find from original changes data)
            # Note: This would require passing the ProductChange object through to ImpactAnalysis
            # For now, we'll add this in a future enhancement

            summary_lines.append("")

    summary_lines.append("=" * 80)
    return "\n".join(summary_lines)


def main():
    """Main analysis pipeline"""

    print("Product Impact Analyzer - Phase 1")
    print()

    # Load configuration
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)

    # Load input data (created by Claude via MCP)
    data_dir = Path(__file__).parent / "data"

    print("Loading product changes from Outliers Report...")
    outliers_path = data_dir / "outliers_report.json"
    if not outliers_path.exists():
        print(f"Error: {outliers_path} not found")
        print("Claude needs to fetch this data via MCP first")
        return 1

    with open(outliers_path) as f:
        outliers_data = json.load(f)

    product_changes = parse_product_changes(outliers_data)
    print(f"  Found {len(product_changes)} product changes")

    # Load Google Ads data by client
    print("\nLoading Google Ads performance data...")
    ads_data_by_client = {}

    for client_config in config['clients']:
        if not client_config.get('enabled'):
            continue

        client_name = client_config['name']
        ads_path = data_dir / f"ads_{client_name.replace(' ', '_').lower()}.json"

        if not ads_path.exists():
            print(f"  Warning: {ads_path} not found, skipping {client_name}")
            continue

        with open(ads_path) as f:
            ads_data_by_client[client_name] = json.load(f)

        print(f"  Loaded {len(ads_data_by_client[client_name])} rows for {client_name}")

    # Run impact analysis
    print("\nAnalyzing impact...")
    comparison_days = config['analysis_settings']['comparison_window_days']
    analyses = analyze_impact(product_changes, ads_data_by_client, comparison_days)
    print(f"  Analyzed {len(analyses)} product changes")

    # Generate outputs
    print("\nGenerating reports...")

    # JSON output for Claude to write to Sheets
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    json_output = output_dir / "impact_analysis.json"
    with open(json_output, 'w') as f:
        json.dump([a.to_dict() for a in analyses], f, indent=2)
    print(f"  Saved JSON report: {json_output}")

    # Text summary for user
    summary = generate_text_summary(analyses)
    summary_output = output_dir / "summary.txt"
    with open(summary_output, 'w') as f:
        f.write(summary)
    print(f"  Saved summary: {summary_output}")

    print("\n" + summary)

    return 0


if __name__ == "__main__":
    sys.exit(main())
