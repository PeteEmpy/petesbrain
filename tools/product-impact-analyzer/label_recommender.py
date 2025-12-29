#!/usr/bin/env python3
"""
Automated Hero/Villain Label Recommendations

Generates confidence-scored recommendations for Product Hero label changes.

Key Features:
- Multi-factor scoring: revenue, ROAS, conversion rate, click volume, trends
- Confidence scoring based on data quality and consistency
- Upgrade recommendations (Zombie → Villain → Sidekick → Hero)
- Downgrade recommendations (Hero → Sidekick → Villain → Zombie)
- Threshold-based decision logic with hysteresis to prevent label flapping

Usage:
    from label_recommender import LabelRecommender

    recommender = LabelRecommender()
    recommendations = recommender.generate_recommendations(
        current_labels={'product_1': 'zombie', 'product_2': 'hero'},
        performance_data={'product_1': {...}, 'product_2': {...}},
        target_roas=4.0
    )
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json


@dataclass
class LabelRecommendation:
    """Label change recommendation"""
    product_id: str
    product_title: str
    current_label: str
    recommended_label: str
    confidence: str  # high, medium, low
    recommendation_score: float
    reasons: List[str]
    action_required: str
    timestamp: str


class LabelRecommender:
    """
    Generates automated recommendations for Product Hero label changes.

    Scoring Factors:
    - Revenue performance (35 points)
    - ROAS vs target (30 points)
    - Conversion rate (20 points)
    - Click volume (10 points)
    - Trend direction (5 points)

    Max Score: 100 points

    Label Thresholds:
    - Hero: ≥75 points
    - Sidekick: 50-74 points
    - Villain: 25-49 points
    - Zombie: <25 points
    """

    def __init__(self):
        """Initialize label recommender"""

        # Scoring weights
        self.WEIGHTS = {
            'revenue_performance': 35,
            'roas_performance': 30,
            'conversion_rate': 20,
            'click_volume': 10,
            'trend_direction': 5
        }

        self.MAX_SCORE = sum(self.WEIGHTS.values())

        # Label thresholds (with hysteresis)
        self.LABEL_THRESHOLDS = {
            'hero': 75,
            'sidekick': 50,
            'villain': 25,
            'zombie': 0
        }

        # Hysteresis buffer (prevents label flapping)
        self.HYSTERESIS_BUFFER = 5  # 5 points buffer

    def generate_recommendations(
        self,
        current_labels: Dict[str, str],
        performance_data: Dict[str, Dict],
        target_roas: float = 4.0,
        min_revenue_threshold: float = 50
    ) -> List[LabelRecommendation]:
        """
        Generate label change recommendations.

        Args:
            current_labels: Dict of {product_id: current_label}
            performance_data: Dict of {product_id: {revenue, spend, conversions, clicks, trends, ...}}
            target_roas: Target ROAS threshold
            min_revenue_threshold: Minimum revenue to consider for upgrade (£50)

        Returns:
            List of LabelRecommendation objects
        """
        recommendations = []

        # Calculate total revenue for relative scoring
        total_revenue = sum(data.get('revenue', 0) for data in performance_data.values())

        for product_id, performance in performance_data.items():
            current_label = current_labels.get(product_id, 'unknown').lower()

            if current_label == 'unknown':
                continue

            # Calculate recommendation score
            score = self._calculate_recommendation_score(
                performance,
                total_revenue,
                target_roas
            )

            # Determine recommended label
            recommended_label = self._determine_recommended_label(
                score,
                current_label
            )

            # Only recommend if label should change
            if recommended_label != current_label:
                # Calculate confidence
                confidence = self._calculate_confidence(
                    performance,
                    score,
                    current_label,
                    recommended_label
                )

                # Generate reasons
                reasons = self._generate_reasons(
                    performance,
                    score,
                    current_label,
                    recommended_label,
                    target_roas,
                    min_revenue_threshold
                )

                # Determine action required
                action = self._determine_action(
                    current_label,
                    recommended_label,
                    confidence
                )

                recommendations.append(LabelRecommendation(
                    product_id=product_id,
                    product_title=performance.get('product_title', 'Unknown'),
                    current_label=current_label,
                    recommended_label=recommended_label,
                    confidence=confidence,
                    recommendation_score=score,
                    reasons=reasons,
                    action_required=action,
                    timestamp=datetime.now().isoformat()
                ))

        # Sort by recommendation score (descending) and confidence
        recommendations.sort(
            key=lambda x: (
                {'high': 3, 'medium': 2, 'low': 1}.get(x.confidence, 0),
                x.recommendation_score
            ),
            reverse=True
        )

        return recommendations

    def _calculate_recommendation_score(
        self,
        performance: Dict,
        total_revenue: float,
        target_roas: float
    ) -> float:
        """Calculate recommendation score for a product"""
        score = 0

        # Factor 1: Revenue performance (35 points)
        revenue = performance.get('revenue', 0)
        revenue_share = (revenue / total_revenue) if total_revenue > 0 else 0

        if revenue_share >= 0.10:  # Top 10% revenue
            score += self.WEIGHTS['revenue_performance']
        elif revenue_share >= 0.05:  # Top 5-10%
            score += self.WEIGHTS['revenue_performance'] * 0.8
        elif revenue_share >= 0.02:  # Top 2-5%
            score += self.WEIGHTS['revenue_performance'] * 0.6
        elif revenue_share >= 0.01:  # Top 1-2%
            score += self.WEIGHTS['revenue_performance'] * 0.4
        elif revenue > 0:  # Some revenue
            score += self.WEIGHTS['revenue_performance'] * 0.2

        # Factor 2: ROAS vs target (30 points)
        revenue = performance.get('revenue', 0)
        spend = performance.get('spend', 0)
        roas = (revenue / spend) if spend > 0 else 0

        if roas >= target_roas * 1.5:  # 50% above target
            score += self.WEIGHTS['roas_performance']
        elif roas >= target_roas * 1.2:  # 20% above target
            score += self.WEIGHTS['roas_performance'] * 0.9
        elif roas >= target_roas:  # Meets target
            score += self.WEIGHTS['roas_performance'] * 0.7
        elif roas >= target_roas * 0.8:  # Within 20% of target
            score += self.WEIGHTS['roas_performance'] * 0.5
        elif roas >= target_roas * 0.5:  # Within 50% of target
            score += self.WEIGHTS['roas_performance'] * 0.3

        # Factor 3: Conversion rate (20 points)
        conversions = performance.get('conversions', 0)
        clicks = performance.get('clicks', 0)
        cvr = (conversions / clicks) if clicks > 0 else 0

        if cvr >= 0.05:  # 5%+ CVR (excellent)
            score += self.WEIGHTS['conversion_rate']
        elif cvr >= 0.03:  # 3-5% CVR (good)
            score += self.WEIGHTS['conversion_rate'] * 0.8
        elif cvr >= 0.02:  # 2-3% CVR (average)
            score += self.WEIGHTS['conversion_rate'] * 0.6
        elif cvr >= 0.01:  # 1-2% CVR (below average)
            score += self.WEIGHTS['conversion_rate'] * 0.4
        elif cvr > 0:  # Some conversions
            score += self.WEIGHTS['conversion_rate'] * 0.2

        # Factor 4: Click volume (10 points)
        if clicks >= 1000:  # High volume
            score += self.WEIGHTS['click_volume']
        elif clicks >= 500:  # Medium-high volume
            score += self.WEIGHTS['click_volume'] * 0.8
        elif clicks >= 100:  # Medium volume
            score += self.WEIGHTS['click_volume'] * 0.6
        elif clicks >= 50:  # Low-medium volume
            score += self.WEIGHTS['click_volume'] * 0.4
        elif clicks > 0:  # Some clicks
            score += self.WEIGHTS['click_volume'] * 0.2

        # Factor 5: Trend direction (5 points)
        trend = performance.get('trend_direction', 'stable')  # 'improving', 'stable', 'declining'

        if trend == 'improving':
            score += self.WEIGHTS['trend_direction']
        elif trend == 'stable':
            score += self.WEIGHTS['trend_direction'] * 0.5
        # Declining: 0 points

        return score

    def _determine_recommended_label(
        self,
        score: float,
        current_label: str
    ) -> str:
        """Determine recommended label based on score and current label"""

        # Apply hysteresis to prevent label flapping
        if current_label == 'hero':
            # Need to drop below (hero threshold - buffer) to downgrade
            if score < self.LABEL_THRESHOLDS['hero'] - self.HYSTERESIS_BUFFER:
                if score >= self.LABEL_THRESHOLDS['sidekick']:
                    return 'sidekick'
                elif score >= self.LABEL_THRESHOLDS['villain']:
                    return 'villain'
                else:
                    return 'zombie'
            else:
                return 'hero'

        elif current_label == 'sidekick':
            # Can upgrade if above hero threshold
            if score >= self.LABEL_THRESHOLDS['hero']:
                return 'hero'
            # Downgrade if below (sidekick threshold - buffer)
            elif score < self.LABEL_THRESHOLDS['sidekick'] - self.HYSTERESIS_BUFFER:
                if score >= self.LABEL_THRESHOLDS['villain']:
                    return 'villain'
                else:
                    return 'zombie'
            else:
                return 'sidekick'

        elif current_label == 'villain':
            # Can upgrade
            if score >= self.LABEL_THRESHOLDS['hero']:
                return 'hero'
            elif score >= self.LABEL_THRESHOLDS['sidekick']:
                return 'sidekick'
            # Downgrade if below (villain threshold - buffer)
            elif score < self.LABEL_THRESHOLDS['villain'] - self.HYSTERESIS_BUFFER:
                return 'zombie'
            else:
                return 'villain'

        else:  # zombie
            # Can upgrade
            if score >= self.LABEL_THRESHOLDS['hero']:
                return 'hero'
            elif score >= self.LABEL_THRESHOLDS['sidekick']:
                return 'sidekick'
            elif score >= self.LABEL_THRESHOLDS['villain']:
                return 'villain'
            else:
                return 'zombie'

    def _calculate_confidence(
        self,
        performance: Dict,
        score: float,
        current_label: str,
        recommended_label: str
    ) -> str:
        """Calculate confidence level for recommendation"""

        # High confidence requires:
        # 1. Clear score difference (≥20 points from threshold)
        # 2. Sufficient data volume (≥100 clicks, ≥5 conversions)
        # 3. Stable or improving trend

        clicks = performance.get('clicks', 0)
        conversions = performance.get('conversions', 0)
        trend = performance.get('trend_direction', 'stable')

        # Calculate distance from current label threshold
        current_threshold = self.LABEL_THRESHOLDS.get(current_label, 0)
        score_difference = abs(score - current_threshold)

        if score_difference >= 20 and clicks >= 100 and conversions >= 5 and trend != 'declining':
            return "high"
        elif score_difference >= 10 and clicks >= 50 and conversions >= 3:
            return "medium"
        else:
            return "low"

    def _generate_reasons(
        self,
        performance: Dict,
        score: float,
        current_label: str,
        recommended_label: str,
        target_roas: float,
        min_revenue_threshold: float
    ) -> List[str]:
        """Generate human-readable reasons for recommendation"""
        reasons = []

        revenue = performance.get('revenue', 0)
        spend = performance.get('spend', 0)
        roas = (revenue / spend) if spend > 0 else 0
        conversions = performance.get('conversions', 0)
        clicks = performance.get('clicks', 0)
        cvr = (conversions / clicks) if clicks > 0 else 0
        trend = performance.get('trend_direction', 'stable')

        # ROAS reason
        if roas >= target_roas * 1.2:
            reasons.append(f"Exceeds target ROAS ({roas:.1f}x vs {target_roas:.1f}x target)")
        elif roas >= target_roas:
            reasons.append(f"Meets target ROAS ({roas:.1f}x)")
        elif roas < target_roas * 0.5:
            reasons.append(f"Well below target ROAS ({roas:.1f}x vs {target_roas:.1f}x target)")

        # Revenue reason
        if revenue >= min_revenue_threshold * 10:
            reasons.append(f"High revenue (£{revenue:.0f})")
        elif revenue >= min_revenue_threshold:
            reasons.append(f"Moderate revenue (£{revenue:.0f})")
        elif revenue > 0 and revenue < min_revenue_threshold:
            reasons.append(f"Low revenue (£{revenue:.0f})")

        # Conversion rate reason
        if cvr >= 0.03:
            reasons.append(f"Strong conversion rate ({cvr*100:.1f}%)")
        elif cvr <= 0.01 and conversions > 0:
            reasons.append(f"Low conversion rate ({cvr*100:.1f}%)")

        # Trend reason
        if trend == 'improving':
            reasons.append("Performance improving")
        elif trend == 'declining':
            reasons.append("Performance declining")

        # Score-based reason
        reasons.append(f"Recommendation score: {score:.0f}/{self.MAX_SCORE}")

        return reasons

    def _determine_action(
        self,
        current_label: str,
        recommended_label: str,
        confidence: str
    ) -> str:
        """Determine action required for recommendation"""

        label_hierarchy = ['zombie', 'villain', 'sidekick', 'hero']
        current_idx = label_hierarchy.index(current_label) if current_label in label_hierarchy else 0
        recommended_idx = label_hierarchy.index(recommended_label) if recommended_label in label_hierarchy else 0

        if recommended_idx > current_idx:
            # Upgrade
            if confidence == "high":
                return f"🟢 RECOMMEND: Upgrade {current_label.title()} → {recommended_label.title()}"
            elif confidence == "medium":
                return f"🟡 CONSIDER: Upgrade {current_label.title()} → {recommended_label.title()}"
            else:
                return f"⚪ MONITOR: May upgrade {current_label.title()} → {recommended_label.title()} if trend continues"
        else:
            # Downgrade
            if confidence == "high":
                return f"🔴 RECOMMEND: Downgrade {current_label.title()} → {recommended_label.title()}"
            elif confidence == "medium":
                return f"🟡 CONSIDER: Downgrade {current_label.title()} → {recommended_label.title()}"
            else:
                return f"⚪ MONITOR: May downgrade {current_label.title()} → {recommended_label.title()} if trend continues"

    def generate_html_report(
        self,
        client: str,
        recommendations: List[LabelRecommendation]
    ) -> str:
        """
        Generate HTML report for label recommendations.

        Args:
            client: Client name
            recommendations: List of label recommendations

        Returns:
            HTML string
        """
        if not recommendations:
            return f"""
            <h3>{client} - Label Recommendations</h3>
            <p>✅ No label changes recommended. All products correctly classified.</p>
            """

        html = f"""
        <h3>{client} - Automated Label Recommendations</h3>
        <p>{len(recommendations)} product(s) recommended for label changes:</p>

        <table>
            <tr>
                <th>Product</th>
                <th>Current Label</th>
                <th>Recommended Label</th>
                <th>Score</th>
                <th>Confidence</th>
                <th>Reasons</th>
                <th>Action Required</th>
            </tr>
        """

        for rec in recommendations:
            # Color code based on confidence
            confidence_color = {
                'high': '#059669',
                'medium': '#F59E0B',
                'low': '#6B7280'
            }.get(rec.confidence, '#6B7280')

            reasons_str = "<br>• ".join(rec.reasons)

            html += f"""
            <tr>
                <td>{rec.product_title[:50]}</td>
                <td>{rec.current_label.title()}</td>
                <td><strong>{rec.recommended_label.title()}</strong></td>
                <td>{rec.recommendation_score:.0f}/{self.MAX_SCORE} ({rec.recommendation_score/self.MAX_SCORE*100:.0f}%)</td>
                <td style="color: {confidence_color}; font-weight: 600;">{rec.confidence.upper()}</td>
                <td><em>• {reasons_str}</em></td>
                <td>{rec.action_required}</td>
            </tr>
            """

        html += """
        </table>
        <p><em>Recommendation score based on: Revenue (35%), ROAS (30%), CVR (20%), clicks (10%), trend (5%)</em></p>
        <p><em>High confidence recommendations should be implemented. Medium/low confidence should be monitored.</em></p>
        """

        return html


if __name__ == "__main__":
    # Test the label recommender
    print("Testing Label Recommendation System...")

    # Mock data
    current_labels = {
        'product_1': 'zombie',  # Should upgrade to hero
        'product_2': 'hero',  # Should downgrade to sidekick
        'product_3': 'villain'  # Should stay villain
    }

    performance_data = {
        'product_1': {
            'product_title': 'High Performing Zombie (should upgrade)',
            'revenue': 1000,
            'spend': 200,
            'conversions': 20,
            'clicks': 400,
            'trend_direction': 'improving'
        },
        'product_2': {
            'product_title': 'Underperforming Hero (should downgrade)',
            'revenue': 100,
            'spend': 50,
            'conversions': 2,
            'clicks': 80,
            'trend_direction': 'declining'
        },
        'product_3': {
            'product_title': 'Stable Villain (no change)',
            'revenue': 200,
            'spend': 100,
            'conversions': 4,
            'clicks': 120,
            'trend_direction': 'stable'
        }
    }

    recommender = LabelRecommender()
    recommendations = recommender.generate_recommendations(
        current_labels=current_labels,
        performance_data=performance_data,
        target_roas=4.0
    )

    print(f"\nGenerated {len(recommendations)} recommendations:\n")
    for rec in recommendations:
        print(f"  Product: {rec.product_title}")
        print(f"  Current: {rec.current_label.title()} → Recommended: {rec.recommended_label.title()}")
        print(f"  Score: {rec.recommendation_score:.0f}/{recommender.MAX_SCORE} ({rec.recommendation_score/recommender.MAX_SCORE*100:.0f}%)")
        print(f"  Confidence: {rec.confidence}")
        print(f"  Reasons: {', '.join(rec.reasons)}")
        print(f"  Action: {rec.action_required}")
        print()
