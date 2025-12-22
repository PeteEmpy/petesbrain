#!/usr/bin/env python3
"""
Product Analyzer - Integrates Product Impact Analysis into Campaign Reports

Analyzes product-level performance and changes for e-commerce clients, correlating
product feed changes with campaign performance.

Based on: /tools/product-impact-analyzer/
Integrated with: Campaign Analysis system
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class ProductMetrics:
    """Performance metrics for a product"""
    product_id: str
    product_title: str
    clicks: int = 0
    impressions: int = 0
    conversions: float = 0.0
    revenue: float = 0.0
    cost: float = 0.0
    availability: str = "NOT_SET"

    @property
    def ctr(self) -> float:
        return (self.clicks / self.impressions * 100) if self.impressions > 0 else 0

    @property
    def conversion_rate(self) -> float:
        return (self.conversions / self.clicks * 100) if self.clicks > 0 else 0

    @property
    def roas(self) -> float:
        return (self.revenue / self.cost) if self.cost > 0 else 0


@dataclass
class ProductChange:
    """Represents a product change"""
    product_id: str
    product_title: str
    change_type: str  # PRICE_DROP, PRICE_INCREASE, DISAPPROVED, REMOVED, NEW
    date_changed: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    impact_flag: str = "⚪"  # 📈 🟢 ⚪ 🟠 📉


@dataclass
class ProductIssue:
    """Product-level issue detected"""
    product_id: str
    product_title: str
    issue_type: str  # disapproval, high_cost_low_roas, price_issue, availability_issue
    severity: str  # P0, P1, P2, P3
    description: str
    metrics: Dict
    recommendation: str


class ProductAnalyzer:
    """Analyzes product-level performance and changes"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        # Path to product-impact-analyzer
        self.product_analyzer_dir = self.base_dir.parent / 'product-impact-analyzer'

    def normalize_product_id(self, product_id: str) -> str:
        """Normalize product IDs for matching (handles leading zeros)"""
        if not product_id:
            return ""
        normalized = product_id.lstrip('0')
        return normalized if normalized else '0'

    def load_product_snapshot(self, client_slug: str) -> Dict[str, Dict]:
        """Load latest product feed snapshot"""
        monitor_dir = self.product_analyzer_dir / 'monitoring'

        if not monitor_dir.exists():
            return {}

        # Find latest snapshot for client
        client_normalized = client_slug.replace('-', '_').lower()
        snapshot_files = sorted(monitor_dir.glob(f"snapshot_{client_normalized}_*.json"))

        if not snapshot_files:
            return {}

        latest = snapshot_files[-1]

        try:
            with open(latest) as f:
                products = json.load(f)

            # Normalize product IDs for matching
            normalized = {}
            for pid, product in products.items():
                norm_id = self.normalize_product_id(pid)
                normalized[norm_id] = product

            return normalized
        except Exception as e:
            print(f"Warning: Could not load product snapshot: {e}")
            return {}

    def aggregate_product_performance(self,
                                     campaign_data: List[Dict],
                                     date_range: Dict) -> Dict[str, ProductMetrics]:
        """Aggregate performance metrics by product from campaign data

        This method processes product-level data from shopping_performance_view queries.
        Product records have 'segments' with product_item_id and product_title.
        """
        product_metrics = {}

        for record in campaign_data:
            # Only process records that have product-level data (segments.product_item_id)
            segments = record.get('segments', {})
            product_id = segments.get('product_item_id', '')

            if not product_id:
                # Skip campaign-level records (no product_item_id)
                continue

            # This is a product-level record
            norm_id = self.normalize_product_id(product_id)
            metrics = record.get('metrics', {})

            # Create or get product metrics object
            if norm_id not in product_metrics:
                product_metrics[norm_id] = ProductMetrics(
                    product_id=norm_id,
                    product_title=segments.get('product_title', 'Unknown')
                )

            # Aggregate metrics across dates
            product = product_metrics[norm_id]
            product.clicks += metrics.get('clicks', 0)
            product.impressions += metrics.get('impressions', 0)
            product.conversions += metrics.get('conversions', 0.0)
            product.revenue += metrics.get('conversions_value', 0.0)
            product.cost += metrics.get('cost_micros', 0) / 1_000_000

        return product_metrics

    def detect_product_changes(self,
                              current_snapshot: Dict[str, Dict],
                              days_back: int = 7) -> List[ProductChange]:
        """Detect product changes from snapshot data"""
        changes = []

        # In a full implementation, this would compare current vs previous snapshots
        # and detect price changes, disapprovals, removals, etc.

        # For now, check for disapproved products in current snapshot
        for pid, product in current_snapshot.items():
            status = product.get('status', {})

            # Check for disapprovals
            if status.get('destination_statuses'):
                for dest_status in status['destination_statuses']:
                    if dest_status.get('status') == 'DISAPPROVED':
                        disapproval_reasons = dest_status.get('disapproval_reasons', [])
                        changes.append(ProductChange(
                            product_id=pid,
                            product_title=product.get('title', 'Unknown'),
                            change_type='DISAPPROVED',
                            date_changed=datetime.now().strftime('%Y-%m-%d'),
                            old_value='APPROVED',
                            new_value=', '.join(disapproval_reasons[:2]) if disapproval_reasons else 'DISAPPROVED',
                            impact_flag='📉'
                        ))

            # Check for price changes (requires historical comparison)
            # This would be implemented when we have access to previous snapshots

        return changes

    def detect_product_issues(self,
                             product_metrics: Dict[str, ProductMetrics],
                             product_snapshot: Dict[str, Dict],
                             target_roas: float = 3.0) -> List[ProductIssue]:
        """Detect product-level issues"""
        issues = []

        for pid, metrics in product_metrics.items():
            # Issue 1: High spend, low ROAS
            if metrics.cost > 50 and metrics.roas < (target_roas * 0.5):
                issues.append(ProductIssue(
                    product_id=pid,
                    product_title=metrics.product_title,
                    issue_type='high_cost_low_roas',
                    severity='P1',
                    description=f'Product spending £{metrics.cost:.2f} with ROAS {metrics.roas:.2f}x (target: {target_roas:.2f}x)',
                    metrics={
                        'cost': metrics.cost,
                        'revenue': metrics.revenue,
                        'roas': metrics.roas,
                        'target_roas': target_roas
                    },
                    recommendation=f'Review product profitability. Consider pausing if ROAS remains below {target_roas * 0.7:.2f}x or reducing bid.'
                ))

            # Issue 2: Zero conversions with significant spend
            if metrics.cost > 30 and metrics.conversions == 0:
                issues.append(ProductIssue(
                    product_id=pid,
                    product_title=metrics.product_title,
                    issue_type='zero_conversions',
                    severity='P1',
                    description=f'Product has spent £{metrics.cost:.2f} with 0 conversions',
                    metrics={
                        'cost': metrics.cost,
                        'clicks': metrics.clicks,
                        'conversions': metrics.conversions
                    },
                    recommendation='Investigate: poor product-market fit, pricing issue, or technical tracking problem.'
                ))

            # Issue 3: Disapproved products (from snapshot)
            if pid in product_snapshot:
                product_data = product_snapshot[pid]
                status = product_data.get('status', {})

                if status.get('destination_statuses'):
                    for dest_status in status['destination_statuses']:
                        if dest_status.get('status') == 'DISAPPROVED':
                            disapproval_reasons = dest_status.get('disapproval_reasons', [])
                            issues.append(ProductIssue(
                                product_id=pid,
                                product_title=metrics.product_title,
                                issue_type='disapproval',
                                severity='P0',
                                description=f'Product disapproved: {", ".join(disapproval_reasons[:2])}',
                                metrics={'disapproval_reasons': disapproval_reasons},
                                recommendation='Fix feed issues immediately. Product is not showing in Shopping ads.'
                            ))

        return issues

    def analyze_products(self,
                        client_slug: str,
                        campaign_data: List[Dict],
                        date_range: Dict,
                        target_roas: float = 3.0) -> Dict:
        """
        Perform comprehensive product analysis

        Returns:
            Dict with:
            - product_metrics: Dict of product-level performance
            - product_changes: List of detected changes
            - product_issues: List of issues requiring attention
            - summary: Text summary
        """
        # Load product snapshot
        product_snapshot = self.load_product_snapshot(client_slug)

        # Aggregate product performance
        product_metrics = self.aggregate_product_performance(campaign_data, date_range)

        # Detect changes
        product_changes = self.detect_product_changes(product_snapshot)

        # Detect issues
        product_issues = self.detect_product_issues(product_metrics, product_snapshot, target_roas)

        # Generate summary
        summary = self.generate_summary(product_metrics, product_changes, product_issues)

        return {
            'product_metrics': {pid: asdict(m) for pid, m in product_metrics.items()},
            'product_changes': [asdict(c) for c in product_changes],
            'product_issues': [asdict(i) for i in product_issues],
            'summary': summary,
            'total_products': len(product_metrics),
            'products_with_issues': len(product_issues),
            'disapproved_products': len([i for i in product_issues if i.issue_type == 'disapproval'])
        }

    def generate_summary(self,
                        product_metrics: Dict[str, ProductMetrics],
                        product_changes: List[ProductChange],
                        product_issues: List[ProductIssue]) -> str:
        """Generate text summary of product analysis"""
        lines = []

        lines.append(f"Product Analysis Summary")
        lines.append(f"========================")
        lines.append("")
        lines.append(f"Total Products: {len(product_metrics)}")
        lines.append(f"Products with Issues: {len(product_issues)}")
        lines.append(f"Recent Changes: {len(product_changes)}")
        lines.append("")

        # Critical issues
        critical_issues = [i for i in product_issues if i.severity == 'P0']
        if critical_issues:
            lines.append(f"⚠️  Critical Issues ({len(critical_issues)}):")
            for issue in critical_issues[:5]:
                lines.append(f"  • {issue.product_title}: {issue.description}")
            lines.append("")

        # Top spending products
        top_products = sorted(
            product_metrics.values(),
            key=lambda p: p.cost,
            reverse=True
        )[:10]

        if top_products:
            lines.append(f"Top 10 Products by Spend:")
            for i, product in enumerate(top_products, 1):
                lines.append(
                    f"  {i}. {product.product_title[:50]} - "
                    f"£{product.cost:.2f} spend, {product.roas:.2f}x ROAS"
                )

        return "\n".join(lines)


def main():
    """Test product analyzer with sample data"""
    analyzer = ProductAnalyzer()

    # Test data
    test_campaigns = [
        {
            'id': '12345',
            'name': 'Shopping Campaign',
            'advertising_channel_type': 'SHOPPING',
            'segments': {
                'product_item_id': '00287',
                'product_title': 'Test Product'
            },
            'metrics': {
                'clicks': 100,
                'impressions': 1000,
                'conversions': 5.0,
                'conversions_value': 250.0,
                'cost_micros': 100000000  # £100
            }
        }
    ]

    result = analyzer.analyze_products(
        client_slug='test-client',
        campaign_data=test_campaigns,
        date_range={'start_date': '2025-12-01', 'end_date': '2025-12-15'},
        target_roas=3.0
    )

    print(result['summary'])
    print("\nProduct Issues:", len(result['product_issues']))


if __name__ == '__main__':
    main()
