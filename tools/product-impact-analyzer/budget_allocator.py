#!/usr/bin/env python3
"""
Budget Allocation Optimizer

Optimizes campaign budget allocation based on product performance metrics.

Key Features:
- Performance scoring using revenue, ROAS, conversion rate, click trends
- Weighted allocation based on performance scores
- Budget reallocation recommendations (increase/decrease/maintain)
- Respects minimum budget thresholds (£50/day minimum per campaign)
- Calculates optimal distribution across Heroes, Sidekicks, Villains

Usage:
    from budget_allocator import BudgetAllocator

    allocator = BudgetAllocator()
    recommendations = allocator.optimize_budget(
        current_budgets={'Campaign 1': 100, 'Campaign 2': 200},
        performance_data={'Campaign 1': {...}, 'Campaign 2': {...}},
        total_budget=500
    )
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import json


@dataclass
class BudgetRecommendation:
    """Budget allocation recommendation"""
    campaign_id: str
    campaign_name: str
    current_budget: float
    recommended_budget: float
    budget_change: float
    budget_change_pct: float
    performance_score: float
    action: str  # increase, decrease, maintain
    reason: str
    confidence: str  # high, medium, low


class BudgetAllocator:
    """
    Optimizes budget allocation based on product performance.

    Scoring Factors:
    - ROAS vs target (40 points)
    - Revenue contribution (30 points)
    - Conversion rate trend (20 points)
    - Click growth (10 points)

    Max Score: 100 points
    """

    def __init__(self):
        """Initialize budget allocator"""

        # Scoring weights
        self.WEIGHTS = {
            'roas_performance': 40,  # ROAS vs target
            'revenue_contribution': 30,  # % of total revenue
            'conversion_trend': 20,  # CVR trend (up/down)
            'click_growth': 10  # Click trend (up/down)
        }

        self.MAX_SCORE = sum(self.WEIGHTS.values())

        # Budget constraints
        self.MIN_BUDGET_PER_CAMPAIGN = 50  # £50/day minimum
        self.MAX_BUDGET_SHIFT_PCT = 0.30  # Max 30% change per reallocation

    def optimize_budget(
        self,
        current_budgets: Dict[str, float],
        performance_data: Dict[str, Dict],
        total_budget: float,
        target_roas: float = 4.0
    ) -> List[BudgetRecommendation]:
        """
        Optimize budget allocation based on performance.

        Args:
            current_budgets: Dict of {campaign_name: current_daily_budget}
            performance_data: Dict of {campaign_name: {revenue, spend, conversions, clicks, ...}}
            total_budget: Total daily budget to allocate
            target_roas: Target ROAS threshold (default 4.0)

        Returns:
            List of BudgetRecommendation objects sorted by performance score
        """
        recommendations = []

        # Calculate performance scores for each campaign
        scores = self._calculate_performance_scores(
            performance_data,
            total_budget,
            target_roas
        )

        # Calculate optimal budget allocation
        optimal_budgets = self._calculate_optimal_allocation(
            scores,
            total_budget
        )

        # Generate recommendations
        for campaign_name, optimal_budget in optimal_budgets.items():
            current_budget = current_budgets.get(campaign_name, 0)
            budget_change = optimal_budget - current_budget
            budget_change_pct = (budget_change / current_budget * 100) if current_budget > 0 else 0

            # Determine action
            if budget_change_pct >= 10:
                action = "increase"
            elif budget_change_pct <= -10:
                action = "decrease"
            else:
                action = "maintain"

            # Generate reason
            score = scores[campaign_name]
            reason = self._generate_reason(
                campaign_name,
                performance_data[campaign_name],
                score,
                target_roas
            )

            # Determine confidence
            confidence = self._calculate_confidence(
                performance_data[campaign_name],
                score
            )

            recommendations.append(BudgetRecommendation(
                campaign_id=campaign_name,
                campaign_name=campaign_name,
                current_budget=current_budget,
                recommended_budget=optimal_budget,
                budget_change=budget_change,
                budget_change_pct=budget_change_pct,
                performance_score=score,
                action=action,
                reason=reason,
                confidence=confidence
            ))

        # Sort by performance score (descending)
        recommendations.sort(key=lambda x: x.performance_score, reverse=True)

        return recommendations

    def _calculate_performance_scores(
        self,
        performance_data: Dict[str, Dict],
        total_budget: float,
        target_roas: float
    ) -> Dict[str, float]:
        """Calculate performance score for each campaign"""
        scores = {}
        total_revenue = sum(data.get('revenue', 0) for data in performance_data.values())

        for campaign_name, data in performance_data.items():
            score = 0

            # Factor 1: ROAS vs target (40 points)
            revenue = data.get('revenue', 0)
            spend = data.get('spend', 0)
            roas = (revenue / spend) if spend > 0 else 0

            if roas >= target_roas * 1.2:  # 20% above target
                score += self.WEIGHTS['roas_performance']
            elif roas >= target_roas:  # Meets target
                score += self.WEIGHTS['roas_performance'] * 0.8
            elif roas >= target_roas * 0.8:  # Within 20% of target
                score += self.WEIGHTS['roas_performance'] * 0.5
            elif roas >= target_roas * 0.5:  # Within 50% of target
                score += self.WEIGHTS['roas_performance'] * 0.3
            # else: 0 points

            # Factor 2: Revenue contribution (30 points)
            revenue_share = (revenue / total_revenue) if total_revenue > 0 else 0
            score += self.WEIGHTS['revenue_contribution'] * revenue_share

            # Factor 3: Conversion rate trend (20 points)
            # Compare current CVR to historical baseline
            current_cvr = data.get('conversion_rate', 0)
            baseline_cvr = data.get('baseline_conversion_rate', current_cvr)

            if baseline_cvr > 0:
                cvr_change_pct = ((current_cvr - baseline_cvr) / baseline_cvr) * 100

                if cvr_change_pct >= 20:  # 20%+ improvement
                    score += self.WEIGHTS['conversion_trend']
                elif cvr_change_pct >= 10:  # 10-20% improvement
                    score += self.WEIGHTS['conversion_trend'] * 0.7
                elif cvr_change_pct >= 0:  # Stable or slight improvement
                    score += self.WEIGHTS['conversion_trend'] * 0.5
                elif cvr_change_pct >= -10:  # Slight decline
                    score += self.WEIGHTS['conversion_trend'] * 0.3
                # else: 0 points (major decline)
            else:
                # No baseline, give neutral score
                score += self.WEIGHTS['conversion_trend'] * 0.5

            # Factor 4: Click growth (10 points)
            current_clicks = data.get('clicks', 0)
            baseline_clicks = data.get('baseline_clicks', current_clicks)

            if baseline_clicks > 0:
                click_change_pct = ((current_clicks - baseline_clicks) / baseline_clicks) * 100

                if click_change_pct >= 20:  # 20%+ growth
                    score += self.WEIGHTS['click_growth']
                elif click_change_pct >= 10:  # 10-20% growth
                    score += self.WEIGHTS['click_growth'] * 0.7
                elif click_change_pct >= 0:  # Stable or slight growth
                    score += self.WEIGHTS['click_growth'] * 0.5
                elif click_change_pct >= -10:  # Slight decline
                    score += self.WEIGHTS['click_growth'] * 0.3
                # else: 0 points
            else:
                # No baseline
                score += self.WEIGHTS['click_growth'] * 0.5

            scores[campaign_name] = score

        return scores

    def _calculate_optimal_allocation(
        self,
        scores: Dict[str, float],
        total_budget: float
    ) -> Dict[str, float]:
        """Calculate optimal budget allocation based on scores"""

        # Calculate total score
        total_score = sum(scores.values())

        if total_score == 0:
            # No performance data, distribute evenly
            num_campaigns = len(scores)
            per_campaign = total_budget / num_campaigns
            return {campaign: per_campaign for campaign in scores.keys()}

        # Allocate budget proportional to scores
        optimal_budgets = {}

        for campaign, score in scores.items():
            # Calculate proportional budget
            proportion = score / total_score
            allocated_budget = total_budget * proportion

            # Apply minimum budget constraint
            allocated_budget = max(allocated_budget, self.MIN_BUDGET_PER_CAMPAIGN)

            optimal_budgets[campaign] = allocated_budget

        # Normalize to fit total budget (after applying minimums)
        actual_total = sum(optimal_budgets.values())
        if actual_total != total_budget:
            scaling_factor = total_budget / actual_total
            optimal_budgets = {
                campaign: budget * scaling_factor
                for campaign, budget in optimal_budgets.items()
            }

        return optimal_budgets

    def _generate_reason(
        self,
        campaign_name: str,
        performance_data: Dict,
        score: float,
        target_roas: float
    ) -> str:
        """Generate human-readable reason for budget recommendation"""
        revenue = performance_data.get('revenue', 0)
        spend = performance_data.get('spend', 0)
        roas = (revenue / spend) if spend > 0 else 0

        reasons = []

        # ROAS analysis
        if roas >= target_roas * 1.2:
            reasons.append(f"Exceeds target ROAS ({roas:.1f}x vs {target_roas:.1f}x target)")
        elif roas >= target_roas:
            reasons.append(f"Meets target ROAS ({roas:.1f}x)")
        elif roas >= target_roas * 0.8:
            reasons.append(f"Below target ROAS ({roas:.1f}x vs {target_roas:.1f}x target)")
        else:
            reasons.append(f"Significantly below target ROAS ({roas:.1f}x vs {target_roas:.1f}x target)")

        # Revenue contribution
        if revenue > 0:
            reasons.append(f"£{revenue:.0f} revenue")

        # Conversion trend
        current_cvr = performance_data.get('conversion_rate', 0)
        baseline_cvr = performance_data.get('baseline_conversion_rate', 0)

        if baseline_cvr > 0:
            cvr_change_pct = ((current_cvr - baseline_cvr) / baseline_cvr) * 100
            if cvr_change_pct >= 10:
                reasons.append(f"CVR improving (+{cvr_change_pct:.0f}%)")
            elif cvr_change_pct <= -10:
                reasons.append(f"CVR declining ({cvr_change_pct:.0f}%)")

        return "; ".join(reasons)

    def _calculate_confidence(
        self,
        performance_data: Dict,
        score: float
    ) -> str:
        """Calculate confidence level for recommendation"""

        # High confidence requires:
        # 1. High performance score (≥70/100)
        # 2. Sufficient data volume (≥100 clicks, ≥10 conversions)

        clicks = performance_data.get('clicks', 0)
        conversions = performance_data.get('conversions', 0)

        score_pct = (score / self.MAX_SCORE) * 100

        if score_pct >= 70 and clicks >= 100 and conversions >= 10:
            return "high"
        elif score_pct >= 50 and clicks >= 50 and conversions >= 5:
            return "medium"
        else:
            return "low"

    def generate_html_report(
        self,
        client: str,
        recommendations: List[BudgetRecommendation],
        current_total_budget: float,
        recommended_total_budget: float
    ) -> str:
        """
        Generate HTML report for budget recommendations.

        Args:
            client: Client name
            recommendations: List of budget recommendations
            current_total_budget: Current total daily budget
            recommended_total_budget: Recommended total daily budget

        Returns:
            HTML string
        """
        if not recommendations:
            return f"""
            <h3>{client} - Budget Allocation</h3>
            <p>No budget recommendations (insufficient performance data)</p>
            """

        html = f"""
        <h3>{client} - Budget Allocation Recommendations</h3>
        <p><strong>Current Total Budget:</strong> £{current_total_budget:.2f}/day</p>
        <p><strong>Recommended Total Budget:</strong> £{recommended_total_budget:.2f}/day</p>

        <table>
            <tr>
                <th>Campaign</th>
                <th>Current Budget</th>
                <th>Recommended Budget</th>
                <th>Change</th>
                <th>Action</th>
                <th>Performance Score</th>
                <th>Reason</th>
                <th>Confidence</th>
            </tr>
        """

        for rec in recommendations:
            # Color code action
            action_color = {
                'increase': '#059669',
                'decrease': '#DC2626',
                'maintain': '#6B7280'
            }.get(rec.action, '#6B7280')

            # Confidence badge color
            confidence_color = {
                'high': '#059669',
                'medium': '#F59E0B',
                'low': '#6B7280'
            }.get(rec.confidence, '#6B7280')

            change_display = f"{rec.budget_change:+.2f} ({rec.budget_change_pct:+.0f}%)"

            html += f"""
            <tr>
                <td>{rec.campaign_name}</td>
                <td>£{rec.current_budget:.2f}/day</td>
                <td>£{rec.recommended_budget:.2f}/day</td>
                <td style="color: {action_color}; font-weight: 600;">{change_display}</td>
                <td style="color: {action_color}; font-weight: 600; text-transform: uppercase;">{rec.action}</td>
                <td><strong>{rec.performance_score:.0f}/{self.MAX_SCORE}</strong> ({rec.performance_score/self.MAX_SCORE*100:.0f}%)</td>
                <td><em>{rec.reason}</em></td>
                <td style="color: {confidence_color}; font-weight: 600; text-transform: uppercase;">{rec.confidence}</td>
            </tr>
            """

        html += """
        </table>
        <p><em>Performance score based on: ROAS vs target (40%), revenue contribution (30%), CVR trend (20%), click growth (10%)</em></p>
        <p><em>Minimum budget: £50/day per campaign</em></p>
        """

        return html


if __name__ == "__main__":
    # Test the budget allocator
    print("Testing Budget Allocation Optimizer...")

    # Mock data
    current_budgets = {
        'Heroes Campaign': 200,
        'Sidekicks Campaign': 150,
        'Catch-All Campaign': 100
    }

    performance_data = {
        'Heroes Campaign': {
            'revenue': 1200,
            'spend': 200,
            'conversions': 15,
            'clicks': 250,
            'conversion_rate': 0.06,
            'baseline_conversion_rate': 0.05,
            'baseline_clicks': 200
        },
        'Sidekicks Campaign': {
            'revenue': 600,
            'spend': 150,
            'conversions': 8,
            'clicks': 180,
            'conversion_rate': 0.044,
            'baseline_conversion_rate': 0.05,
            'baseline_clicks': 200
        },
        'Catch-All Campaign': {
            'revenue': 200,
            'spend': 100,
            'conversions': 3,
            'clicks': 120,
            'conversion_rate': 0.025,
            'baseline_conversion_rate': 0.03,
            'baseline_clicks': 150
        }
    }

    allocator = BudgetAllocator()
    recommendations = allocator.optimize_budget(
        current_budgets=current_budgets,
        performance_data=performance_data,
        total_budget=500,
        target_roas=4.0
    )

    print(f"\nGenerated {len(recommendations)} recommendations:\n")
    for rec in recommendations:
        print(f"  {rec.campaign_name}")
        print(f"  Current: £{rec.current_budget:.2f}/day → Recommended: £{rec.recommended_budget:.2f}/day")
        print(f"  Change: {rec.budget_change:+.2f} ({rec.budget_change_pct:+.0f}%)")
        print(f"  Action: {rec.action.upper()}")
        print(f"  Score: {rec.performance_score:.0f}/{allocator.MAX_SCORE} ({rec.performance_score/allocator.MAX_SCORE*100:.0f}%)")
        print(f"  Reason: {rec.reason}")
        print(f"  Confidence: {rec.confidence}")
        print()
