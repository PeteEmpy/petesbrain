#!/usr/bin/env python3
"""
Revenue-Based Product Classification

Alternative classification system based on revenue contribution rather than
conversion volume. Identifies high-value low-volume products that may be
missed by conversion-based classifications.

Classification Rules:
- Revenue Heroes: Top 20% of revenue contributors
- Revenue Sidekicks: 60-80th percentile
- Revenue Villains: 20-60th percentile
- Revenue Zombies: Bottom 20% of revenue contributors

This runs alongside (not replacing) the external Product Hero labels from
Google Merchant Centre.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RevenueClassification:
    """Revenue-based product classification result"""
    product_id: str
    product_title: str
    revenue: float
    revenue_rank_pct: float  # Percentile ranking (0-100)
    revenue_label: str  # revenue_hero, revenue_sidekick, revenue_villain, revenue_zombie
    external_label: str  # From Product Hero (heroes, sidekicks, villains, zombies)
    label_mismatch: bool  # True if revenue label differs from external label

    def __str__(self):
        mismatch_flag = " ⚠️ MISMATCH" if self.label_mismatch else ""
        return f"{self.product_title}: {self.revenue_label} (£{self.revenue:.2f}, {self.revenue_rank_pct:.0f}th percentile){mismatch_flag}"


class RevenueClassifier:
    """
    Classifies products based on revenue contribution.

    Useful for identifying:
    - High-value low-volume products (revenue_hero but external zombie)
    - Low-value high-volume products (revenue_zombie but external hero)
    - Revenue concentration (what % of revenue comes from top 20%?)
    """

    def __init__(self):
        """Initialize classifier"""
        pass

    def classify_products(
        self,
        products: Dict[str, Dict],
        external_labels: Dict[str, str] = None
    ) -> Tuple[List[RevenueClassification], Dict]:
        """
        Classify products by revenue contribution.

        Args:
            products: Dict of {product_id: {revenue, product_title, ...}}
            external_labels: Optional dict of {product_id: external_label}

        Returns:
            Tuple of (classifications, summary_stats)
        """
        if not products:
            return [], {}

        # Extract revenue data
        revenue_data = []
        for product_id, metrics in products.items():
            revenue = metrics.get('revenue', 0)
            if revenue > 0:  # Only classify products with revenue
                revenue_data.append({
                    'product_id': product_id,
                    'product_title': metrics.get('product_title', 'Unknown'),
                    'revenue': revenue
                })

        if not revenue_data:
            return [], {'total_products': 0, 'total_revenue': 0}

        # Sort by revenue (descending)
        revenue_data.sort(key=lambda x: x['revenue'], reverse=True)

        # Calculate percentile thresholds
        total_products = len(revenue_data)
        hero_threshold_idx = int(total_products * 0.20)  # Top 20%
        sidekick_threshold_idx = int(total_products * 0.40)  # 20-40th percentile
        villain_threshold_idx = int(total_products * 0.80)  # 40-80th percentile
        # 80-100th = zombies

        # Calculate total revenue for concentration analysis
        total_revenue = sum(p['revenue'] for p in revenue_data)
        hero_revenue = sum(p['revenue'] for p in revenue_data[:hero_threshold_idx])

        # Classify each product
        classifications = []

        for idx, product in enumerate(revenue_data):
            # Determine revenue label based on percentile
            if idx < hero_threshold_idx:
                revenue_label = 'revenue_hero'
            elif idx < sidekick_threshold_idx:
                revenue_label = 'revenue_sidekick'
            elif idx < villain_threshold_idx:
                revenue_label = 'revenue_villain'
            else:
                revenue_label = 'revenue_zombie'

            # Calculate percentile (higher = better)
            revenue_rank_pct = ((total_products - idx) / total_products) * 100

            # Get external label if available
            external_label = 'unknown'
            if external_labels:
                external_label = external_labels.get(product['product_id'], 'unknown').lower()

            # Check for mismatch (simplified comparison)
            label_mismatch = False
            if external_label != 'unknown':
                # Extract base label (e.g., 'hero' from 'revenue_hero' and 'heroes')
                revenue_base = revenue_label.replace('revenue_', '').rstrip('s')
                external_base = external_label.rstrip('s')
                label_mismatch = (revenue_base != external_base)

            classifications.append(RevenueClassification(
                product_id=product['product_id'],
                product_title=product['product_title'],
                revenue=product['revenue'],
                revenue_rank_pct=revenue_rank_pct,
                revenue_label=revenue_label,
                external_label=external_label,
                label_mismatch=label_mismatch
            ))

        # Calculate summary statistics
        summary_stats = {
            'total_products': total_products,
            'total_revenue': total_revenue,
            'hero_count': hero_threshold_idx,
            'sidekick_count': sidekick_threshold_idx - hero_threshold_idx,
            'villain_count': villain_threshold_idx - sidekick_threshold_idx,
            'zombie_count': total_products - villain_threshold_idx,
            'hero_revenue': hero_revenue,
            'hero_revenue_pct': (hero_revenue / total_revenue * 100) if total_revenue > 0 else 0,
            'mismatch_count': sum(1 for c in classifications if c.label_mismatch),
            'mismatch_pct': (sum(1 for c in classifications if c.label_mismatch) / total_products * 100) if total_products > 0 else 0
        }

        return classifications, summary_stats

    def find_high_value_mismatches(
        self,
        classifications: List[RevenueClassification],
        min_revenue: float = 100
    ) -> List[RevenueClassification]:
        """
        Find high-value products that are misclassified.

        These are products generating significant revenue but labeled as
        villains/zombies by the external system.

        Args:
            classifications: List of RevenueClassification objects
            min_revenue: Minimum revenue to be considered "high-value"

        Returns:
            List of mismatched high-value products
        """
        return [
            c for c in classifications
            if c.label_mismatch
            and c.revenue >= min_revenue
            and c.revenue_label in ['revenue_hero', 'revenue_sidekick']
            and c.external_label in ['villains', 'zombies']
        ]

    def generate_report_section(
        self,
        client: str,
        classifications: List[RevenueClassification],
        summary_stats: Dict
    ) -> str:
        """
        Generate HTML report section showing revenue classification insights.

        Args:
            client: Client name
            classifications: List of RevenueClassification objects
            summary_stats: Summary statistics dict

        Returns:
            HTML string for report
        """
        html = f"""
        <h3>Revenue Attribution Analysis - {client}</h3>

        <h4>Revenue Concentration</h4>
        <p>
            Top 20% of products ({summary_stats['hero_count']} products) generate
            <strong>£{summary_stats['hero_revenue']:.2f}</strong>
            (<strong>{summary_stats['hero_revenue_pct']:.1f}%</strong> of total revenue)
        </p>

        <h4>Revenue Classification Distribution</h4>
        <table>
            <tr>
                <th>Classification</th>
                <th>Count</th>
                <th>Percentage</th>
            </tr>
            <tr>
                <td>Revenue Heroes (Top 20%)</td>
                <td>{summary_stats['hero_count']}</td>
                <td>{summary_stats['hero_count'] / summary_stats['total_products'] * 100:.1f}%</td>
            </tr>
            <tr>
                <td>Revenue Sidekicks (60-80%)</td>
                <td>{summary_stats['sidekick_count']}</td>
                <td>{summary_stats['sidekick_count'] / summary_stats['total_products'] * 100:.1f}%</td>
            </tr>
            <tr>
                <td>Revenue Villains (20-60%)</td>
                <td>{summary_stats['villain_count']}</td>
                <td>{summary_stats['villain_count'] / summary_stats['total_products'] * 100:.1f}%</td>
            </tr>
            <tr>
                <td>Revenue Zombies (Bottom 20%)</td>
                <td>{summary_stats['zombie_count']}</td>
                <td>{summary_stats['zombie_count'] / summary_stats['total_products'] * 100:.1f}%</td>
            </tr>
        </table>

        <h4>Label Mismatches</h4>
        <p>
            {summary_stats['mismatch_count']} products ({summary_stats['mismatch_pct']:.1f}%)
            have different revenue-based vs external classifications.
        </p>
        """

        # Show high-value mismatches if any
        high_value_mismatches = self.find_high_value_mismatches(classifications, min_revenue=100)

        if high_value_mismatches:
            html += """
            <h4>⚠️ High-Value Mismatches (Action Required)</h4>
            <p>These products generate significant revenue but are classified as Villains/Zombies by Product Hero:</p>
            <table>
                <tr>
                    <th>Product</th>
                    <th>Revenue</th>
                    <th>Revenue Rank</th>
                    <th>Revenue Label</th>
                    <th>External Label</th>
                </tr>
            """

            for c in high_value_mismatches[:10]:  # Top 10 mismatches
                html += f"""
                <tr>
                    <td>{c.product_title}</td>
                    <td>£{c.revenue:.2f}</td>
                    <td>{c.revenue_rank_pct:.0f}th percentile</td>
                    <td>{c.revenue_label.replace('revenue_', '').title()}</td>
                    <td>{c.external_label.title()}</td>
                </tr>
                """

            html += "</table>"

        html += "<br>"

        return html


if __name__ == "__main__":
    # Test the classifier
    print("Testing Revenue Classifier...")

    # Mock data
    test_products = {
        'prod_1': {'revenue': 1000, 'product_title': 'High Value Product'},
        'prod_2': {'revenue': 500, 'product_title': 'Medium Value Product'},
        'prod_3': {'revenue': 100, 'product_title': 'Low Value Product'},
        'prod_4': {'revenue': 50, 'product_title': 'Very Low Value Product'},
        'prod_5': {'revenue': 10, 'product_title': 'Minimal Value Product'}
    }

    test_external_labels = {
        'prod_1': 'zombies',  # Mismatch - high revenue but labeled zombie
        'prod_2': 'sidekicks',
        'prod_3': 'villains',
        'prod_4': 'zombies',
        'prod_5': 'zombies'
    }

    classifier = RevenueClassifier()
    classifications, stats = classifier.classify_products(test_products, test_external_labels)

    print(f"\nTotal Products: {stats['total_products']}")
    print(f"Total Revenue: £{stats['total_revenue']:.2f}")
    print(f"Hero Revenue: £{stats['hero_revenue']:.2f} ({stats['hero_revenue_pct']:.1f}%)")
    print(f"Mismatches: {stats['mismatch_count']} ({stats['mismatch_pct']:.1f}%)")

    print("\nClassifications:")
    for c in classifications:
        print(f"  {c}")

    print("\nHigh-Value Mismatches:")
    mismatches = classifier.find_high_value_mismatches(classifications, min_revenue=100)
    for m in mismatches:
        print(f"  ⚠️  {m}")
